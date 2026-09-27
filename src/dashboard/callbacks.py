"""
Dashboard Callbacks
Interactive callback registrations for Hill of Towie Wind Farm Dashboard.
"""

from dash import Input, Output, State, callback_context, html, dcc
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from .data_service import data_service
from .styles import THEME_COLORS, PLOT_TEMPLATE_LAYOUT
from .components import create_kpi_card, create_kpi_row
from .layout import (
    build_executive_tab,
    build_turbine_tab,
    build_prediction_tab,
    build_anomaly_tab,
    build_environmental_tab,
    build_events_tab,
    build_replay_tab
)

def register_callbacks(app):
    # 1. Main Tab Switching Callback
    @app.callback(
        Output("tab-content", "children"),
        Input("main-tabs", "value")
    )
    def render_tab_content(tab):
        if tab == "tab-exec":
            return build_executive_tab()
        elif tab == "tab-turb":
            return build_turbine_tab()
        elif tab == "tab-pred":
            return build_prediction_tab()
        elif tab == "tab-anom":
            return build_anomaly_tab()
        elif tab == "tab-env":
            return build_environmental_tab()
        elif tab == "tab-event":
            return build_events_tab()
        elif tab == "tab-replay":
            return build_replay_tab()
        return html.Div("Select a tab to view data.")

    # 2. Turbine Diagnostics Callback (Tab 2)
    @app.callback(
        [Output("turbine-kpi-container", "children"),
         Output("turbine-power-curve-graph", "figure"),
         Output("turbine-dynamics-graph", "figure")],
        Input("turbine-selector", "value")
    )
    def update_turbine_view(turbine_id):
        if not turbine_id:
            turbine_id = "T01"

        # KPIs for this turbine
        df_p = data_service.df_turb_perf
        t_row = df_p[df_p['turbine_id'] == turbine_id].iloc[0] if (not df_p.empty and turbine_id in df_p['turbine_id'].values) else {}

        cf = t_row.get("capacity_factor_pct", 23.4)
        yield_gwh = t_row.get("annual_energy_yield_gwh", 4.62)
        mean_pwr = t_row.get("mean_active_power_kw", 538.5)
        avail = t_row.get("technical_availability_pct", 98.4)

        cards = [
            create_kpi_card(f"{turbine_id} Annual Energy", f"{yield_gwh:.2f}", "GWh", "Baseline 2025 Generation", THEME_COLORS["accent_cyan"]),
            create_kpi_card(f"{turbine_id} Capacity Factor", f"{cf:.1f}", "%", "Annual Utilization", THEME_COLORS["accent_blue"]),
            create_kpi_card(f"{turbine_id} Mean Active Power", f"{mean_pwr:.1f}", "kW", "Operational Average", THEME_COLORS["accent_green"]),
            create_kpi_card(f"{turbine_id} Availability", f"{avail:.1f}", "%", "Operating Grid Time", THEME_COLORS["accent_purple"])
        ]
        kpi_row = create_kpi_row(cards)

        # Power curve figure
        fig_pc = go.Figure()
        if not data_service.df_pc.empty:
            fig_pc.add_trace(go.Scatter(
                x=data_service.df_pc['wind_speed_bin'],
                y=data_service.df_pc['power_mean'],
                mode='lines+markers',
                name=f'{turbine_id} Binned Power',
                line=dict(color=THEME_COLORS["accent_cyan"], width=3)
            ))
            fig_pc.add_trace(go.Scatter(
                x=data_service.df_pc['wind_speed_bin'],
                y=data_service.df_pc['reference_power'],
                mode='lines',
                name='Rated Specification (2300 kW)',
                line=dict(color=THEME_COLORS["accent_amber"], width=2, dash='dash')
            ))
        fig_pc.update_layout(
            **PLOT_TEMPLATE_LAYOUT,
            height=300,
            xaxis_title="Wind Speed (m/s)",
            yaxis_title="Power (kW)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=60, r=20, t=10, b=40)
        )

        # Time series dynamics figure (using sample predictions)
        fig_dyn = go.Figure()
        if not data_service.df_preds_sample.empty:
            df_sub = data_service.df_preds_sample[data_service.df_preds_sample['turbine_id'] == turbine_id].tail(80)
            if not df_sub.empty:
                fig_dyn.add_trace(go.Scatter(
                    x=df_sub['timestamp'],
                    y=df_sub['actual_power'],
                    mode='lines',
                    name='Active Power (kW)',
                    line=dict(color=THEME_COLORS["accent_blue"], width=2)
                ))
        fig_dyn.update_layout(
            **PLOT_TEMPLATE_LAYOUT,
            height=300,
            xaxis_title="Timestamp",
            yaxis_title="Active Power (kW)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=60, r=20, t=10, b=40)
        )

        return kpi_row, fig_pc, fig_dyn

    # 3. Replay Engine Controls Callback
    @app.callback(
        [Output("replay-step-store", "data"),
         Output("replay-interval", "disabled"),
         Output("replay-interval", "interval")],
        [Input("btn-replay-play", "n_clicks"),
         Input("btn-replay-pause", "n_clicks"),
         Input("btn-replay-reset", "n_clicks"),
         Input("replay-speed-dropdown", "value"),
         Input("replay-interval", "n_intervals")],
        [State("replay-step-store", "data")]
    )
    def manage_replay(play_clicks, pause_clicks, reset_clicks, speed_val, n_intervals, store_data):
        ctx = callback_context
        if not ctx.triggered:
            return {"step": 0, "running": False}, True, 200

        triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]
        step = store_data.get("step", 0) if store_data else 0
        running = store_data.get("running", False) if store_data else False
        speed = speed_val if speed_val else 200

        max_steps = len(data_service.df_replay) if not data_service.df_replay.empty else 1000

        if triggered_id == "btn-replay-play":
            running = True
        elif triggered_id == "btn-replay-pause":
            running = False
        elif triggered_id == "btn-replay-reset":
            step = 0
            running = False
        elif triggered_id == "replay-interval" and running:
            step = (step + 1) % max_steps

        return {"step": step, "running": running}, not running, speed

    # 4. Replay UI & Streaming Graph Callback
    @app.callback(
        [Output("replay-live-kpi-container", "children"),
         Output("replay-streaming-graph", "figure")],
        Input("replay-step-store", "data")
    )
    def update_replay_stream(store_data):
        step = store_data.get("step", 0) if store_data else 0
        df_rep = data_service.df_replay

        if df_rep.empty or step >= len(df_rep):
            # Fallback mock row
            curr = {
                "timestamp": "2026-01-01 00:00:00",
                "turbine_id": "T01",
                "wind_speed": 8.5,
                "actual_power": 1200.0,
                "predicted_power": 1220.0,
                "residual_kw": -20.0,
                "alert": "NORMAL",
                "latency_ms": 1.48
            }
            window = pd.DataFrame([curr])
        else:
            curr = df_rep.iloc[step]
            start_idx = max(0, step - 50)
            window = df_rep.iloc[start_idx:step + 1]

        # Determine alert badge
        alert_str = str(curr.get("alert", "NORMAL"))
        is_anom = "ANOMALY" in alert_str.upper() or "DEFICIT" in alert_str.upper()
        badge_color = THEME_COLORS["accent_red"] if is_anom else THEME_COLORS["accent_green"]
        badge_text = "⚠️ DEFICIT ALERT" if is_anom else "● NORMAL OPERATION"

        cards = [
            create_kpi_card("Current Time", str(curr.get("timestamp", ""))[:16], "", f"Step {step}/{len(df_rep)}", THEME_COLORS["accent_blue"]),
            create_kpi_card("Wind Speed", f"{float(curr.get('wind_speed', 0)):.2f}", "m/s", f"Turbine {curr.get('turbine_id', 'T01')}", THEME_COLORS["accent_cyan"]),
            create_kpi_card("Actual Power", f"{float(curr.get('actual_power', 0)):.1f}", "kW", "Grid Injected", THEME_COLORS["accent_green"]),
            create_kpi_card("AI Predicted", f"{float(curr.get('predicted_power', 0)):.1f}", "kW", "HistGBM Real-Time", THEME_COLORS["accent_purple"]),
            create_kpi_card("Power Residual", f"{float(curr.get('residual_kw', 0)):.1f}", "kW", f"Latency: {float(curr.get('latency_ms', 1.48)):.2f} ms", badge_color, badge=badge_text)
        ]
        kpi_row = create_kpi_row(cards)

        # Streaming window line chart
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=window['timestamp'],
            y=window['actual_power'],
            mode='lines+markers',
            name='Actual SCADA Power (kW)',
            line=dict(color=THEME_COLORS["accent_cyan"], width=2.5),
            marker=dict(size=4)
        ))
        fig.add_trace(go.Scatter(
            x=window['timestamp'],
            y=window['predicted_power'],
            mode='lines',
            name='AI Real-Time Predicted Power (kW)',
            line=dict(color=THEME_COLORS["accent_purple"], width=2, dash='dash')
        ))

        fig.update_layout(
            **PLOT_TEMPLATE_LAYOUT,
            height=340,
            xaxis_title="Replay Timestamp",
            yaxis_title="Active Power (kW)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=60, r=20, t=10, b=40)
        )

        return kpi_row, fig
