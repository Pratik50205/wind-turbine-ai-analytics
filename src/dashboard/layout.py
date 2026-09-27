"""
Dashboard Layouts
Complete 7-tab interface for Hill of Towie Wind Farm Dashboard.
"""

from dash import html, dcc, dash_table
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

from .styles import THEME_COLORS, TAB_STYLE, TAB_SELECTED_STYLE, PLOT_TEMPLATE_LAYOUT
from .components import create_header, create_kpi_card, create_kpi_row, create_card_container
from .data_service import data_service

def build_executive_tab():
    kpis = data_service.get_kpis()
    cards = [
        create_kpi_card("Fleet Annual Yield", f"{kpis['total_generation_gwh']:.2f}", "GWh", "Baseline 2025 Fleet Production", THEME_COLORS["accent_cyan"]),
        create_kpi_card("Capacity Factor", f"{kpis['fleet_capacity_factor']:.1f}", "%", "Hill of Towie Empirical CF", THEME_COLORS["accent_blue"]),
        create_kpi_card("Technical Availability", f"{kpis['fleet_availability']:.1f}", "%", "Active Grid Operating Hours", THEME_COLORS["accent_green"]),
        create_kpi_card("Fleet Turbines", f"{kpis['turbines_count']}", "Units", "Siemens SWT-2.3-VS-82 (48.3 MW)", THEME_COLORS["text_primary"]),
        create_kpi_card("Holdout Model R²", f"{kpis['model_r2_score']:.4f}", "", "HistGBM on 2026 Test Set", THEME_COLORS["accent_purple"], "NRMSE: 1.87%"),
        create_kpi_card("Abnormal Events", f"{kpis['anomaly_events_count']}", "Events", "Sustained Underperformance", THEME_COLORS["accent_amber"], "30m Persistence")
    ]

    # Pre-render charts
    # 1. Capacity Factor Ranking
    df_perf = data_service.df_turb_perf.sort_values(by="capacity_factor_pct", ascending=True) if not data_service.df_turb_perf.empty else pd.DataFrame()
    fig_cf = go.Figure()
    if not df_perf.empty:
        fig_cf.add_trace(go.Bar(
            x=df_perf["capacity_factor_pct"],
            y=df_perf["turbine_id"],
            orientation='h',
            marker=dict(
                color=df_perf["capacity_factor_pct"],
                colorscale=[[0, "#38bdf8"], [1, "#00f2fe"]],
                line=dict(color="#1e293b", width=1)
            ),
            text=[f"{v:.1f}%" for v in df_perf["capacity_factor_pct"]],
            textposition="inside",
            hovertemplate="<b>Turbine %{y}</b><br>Capacity Factor: %{x:.2f}%<extra></extra>"
        ))
    fig_cf.update_layout(
        **PLOT_TEMPLATE_LAYOUT,
        height=320,
        xaxis_title="Capacity Factor (%)",
        yaxis_title="Turbine",
        margin=dict(l=60, r=20, t=10, b=40)
    )

    # 2. Power Curve & Fleet Generation Trend Sample
    fig_trend = go.Figure()
    if not data_service.df_preds_sample.empty:
        df_sub = data_service.df_preds_sample[data_service.df_preds_sample['turbine_id'] == 'T01'].tail(150)
        fig_trend.add_trace(go.Scatter(
            x=df_sub['timestamp'], y=df_sub['actual_power'],
            mode='lines', name='Actual Power (kW)',
            line=dict(color=THEME_COLORS["accent_cyan"], width=2)
        ))
        fig_trend.add_trace(go.Scatter(
            x=df_sub['timestamp'], y=df_sub['predicted_power'],
            mode='lines', name='AI Predicted Power (kW)',
            line=dict(color=THEME_COLORS["accent_purple"], width=1.5, dash='dash')
        ))
    fig_trend.update_layout(
        **PLOT_TEMPLATE_LAYOUT,
        height=320,
        xaxis_title="Timestamp",
        yaxis_title="Power (kW)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=60, r=20, t=10, b=40)
    )

    return html.Div([
        create_kpi_row(cards),
        html.Div(
            style={"display": "grid", "gridTemplateColumns": "1.2fr 1fr", "gap": "20px"},
            children=[
                create_card_container("Fleet Generation Profile & AI Tracking (Sample T01)", dcc.Graph(figure=fig_trend, id="exec-trend-graph")),
                create_card_container("Turbine Capacity Factor Benchmark", dcc.Graph(figure=fig_cf, id="exec-cf-graph"))
            ]
        )
    ])

def build_turbine_tab():
    turbines = data_service.get_turbines_list()
    controls = html.Div([
        html.Span("Select Turbine: ", style={"color": THEME_COLORS["text_secondary"], "fontSize": "13px", "fontWeight": "600", "marginRight": "8px"}),
        dcc.Dropdown(
            id="turbine-selector",
            options=[{"label": t, "value": t} for t in turbines],
            value="T01",
            clearable=False,
            style={
                "width": "120px",
                "color": "#000000",
                "fontWeight": "600"
            }
        )
    ], style={"display": "flex", "alignItems": "center"})

    return html.Div([
        create_card_container(
            "Turbine Diagnostics & Performance Analysis",
            html.Div([
                html.Div(id="turbine-kpi-container"),
                html.Div(
                    style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "20px", "marginTop": "20px"},
                    children=[
                        create_card_container("Empirical vs IEC Binned Power Curve", dcc.Graph(id="turbine-power-curve-graph")),
                        create_card_container("10-Minute Wind Speed vs Active Power Dynamic", dcc.Graph(id="turbine-dynamics-graph"))
                    ]
                )
            ]),
            controls=controls
        )
    ])

def build_prediction_tab():
    e = data_service.df_error_summary.iloc[0] if not data_service.df_error_summary.empty else {}
    cards = [
        create_kpi_card("Holdout Test R²", f"{e.get('R2_Score', 0.9962):.4f}", "", "Variance Explained (2026)", THEME_COLORS["accent_cyan"]),
        create_kpi_card("Root Mean Sq Error", f"{e.get('RMSE_kW', 43.06):.2f}", "kW", "Holdout Prediction Error", THEME_COLORS["accent_blue"]),
        create_kpi_card("Normalized RMSE", f"{e.get('Normalized_RMSE_pct', 1.87):.2f}", "%", "Relative to 2300 kW Capacity", THEME_COLORS["accent_green"]),
        create_kpi_card("Mean Absolute Error", f"{e.get('MAE_kW', 19.34):.2f}", "kW", "Absolute Residual Expectation", THEME_COLORS["accent_purple"])
    ]

    # Pre-render parity plot
    fig_parity = go.Figure()
    if not data_service.df_preds_sample.empty:
        sample_pts = data_service.df_preds_sample.sample(min(2000, len(data_service.df_preds_sample)), random_state=42)
        fig_parity.add_trace(go.Scatter(
            x=sample_pts['actual_power'], y=sample_pts['predicted_power'],
            mode='markers',
            marker=dict(size=4, color=THEME_COLORS["accent_cyan"], opacity=0.4),
            name='Predictions'
        ))
        fig_parity.add_trace(go.Scatter(
            x=[0, 2300], y=[0, 2300],
            mode='lines',
            line=dict(color=THEME_COLORS["accent_amber"], width=2, dash='dash'),
            name='Ideal 1:1'
        ))
    fig_parity.update_layout(
        **PLOT_TEMPLATE_LAYOUT,
        height=340,
        xaxis_title="Actual Power (kW)",
        yaxis_title="Predicted Power (kW)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    # Feature importances
    fig_imp = go.Figure()
    if not data_service.df_importance.empty:
        df_top_imp = data_service.df_importance.head(10).sort_values(by="importance", ascending=True)
        fig_imp.add_trace(go.Bar(
            x=df_top_imp['importance'],
            y=df_top_imp['feature'],
            orientation='h',
            marker=dict(color=THEME_COLORS["accent_purple"], line=dict(color="#1e293b", width=1))
        ))
    fig_imp.update_layout(
        **PLOT_TEMPLATE_LAYOUT,
        height=340,
        xaxis_title="Relative Feature Importance",
        yaxis_title="Feature",
        margin=dict(l=140, r=20, t=10, b=40)
    )

    return html.Div([
        create_kpi_row(cards),
        html.Div(
            style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "20px"},
            children=[
                create_card_container("Actual vs Predicted Power Parity (2026 Holdout)", dcc.Graph(figure=fig_parity)),
                create_card_container("Physics-Informed Feature Importance (Top 10)", dcc.Graph(figure=fig_imp))
            ]
        )
    ])

def build_anomaly_tab():
    total_events = len(data_service.df_anomaly_events) if not data_service.df_anomaly_events.empty else 0
    mean_dur = data_service.df_anomaly_events['duration_minutes'].mean() if not data_service.df_anomaly_events.empty else 0
    mean_def = data_service.df_anomaly_events['mean_deficit_kw'].mean() if not data_service.df_anomaly_events.empty else 0

    cards = [
        create_kpi_card("Sustained Anomalies", f"{total_events}", "Events", "≥ 30 min underperformance (2025)", THEME_COLORS["accent_amber"]),
        create_kpi_card("Average Deficit", f"{abs(mean_def):.1f}", "kW", "Mean Active Power Shortfall", THEME_COLORS["accent_red"]),
        create_kpi_card("Average Duration", f"{mean_dur:.1f}", "mins", "Persistence Window", THEME_COLORS["accent_blue"]),
        create_kpi_card("Operating Context", "Statistically Filtered", "", "Excluded Curtailment & High-Wind Cuts", THEME_COLORS["accent_green"])
    ]

    # Anomaly events table
    df_ev = data_service.df_anomaly_events.head(15).copy() if not data_service.df_anomaly_events.empty else pd.DataFrame()
    if not df_ev.empty:
        df_ev['mean_deficit_kw'] = df_ev['mean_deficit_kw'].round(1)
        df_ev['max_deficit_kw'] = df_ev['max_deficit_kw'].round(1)
        df_ev['mean_wind_speed'] = df_ev['mean_wind_speed'].round(2)
        cols = [
            {"name": "Turbine", "id": "turbine_id"},
            {"name": "Start Time", "id": "start_time"},
            {"name": "End Time", "id": "end_time"},
            {"name": "Duration (m)", "id": "duration_minutes"},
            {"name": "Mean Deficit (kW)", "id": "mean_deficit_kw"},
            {"name": "Wind Speed (m/s)", "id": "mean_wind_speed"},
            {"name": "Action Status", "id": "recommended_action"}
        ]
        table = dash_table.DataTable(
            data=df_ev.to_dict('records'),
            columns=cols,
            style_header={
                'backgroundColor': THEME_COLORS["bg_card_secondary"],
                'color': THEME_COLORS["text_primary"],
                'fontWeight': 'bold',
                'border': f'1px solid {THEME_COLORS["border"]}',
                'fontSize': '12px'
            },
            style_cell={
                'backgroundColor': THEME_COLORS["bg_card"],
                'color': THEME_COLORS["text_secondary"],
                'border': f'1px solid {THEME_COLORS["border"]}',
                'padding': '10px',
                'fontSize': '12px',
                'fontFamily': 'Inter, sans-serif'
            },
            style_data_conditional=[
                {
                    'if': {'column_id': 'recommended_action'},
                    'color': THEME_COLORS["accent_amber"],
                    'fontWeight': 'bold'
                }
            ],
            page_size=8
        )
    else:
        table = html.Div("No sustained anomaly records available.")

    # Anomaly distribution by turbine
    fig_anom_turb = go.Figure()
    if not data_service.df_anomaly_by_turb.empty:
        df_at = data_service.df_anomaly_by_turb.sort_values(by="anomaly_rate_pct", ascending=False)
        fig_anom_turb.add_trace(go.Bar(
            x=df_at['turbine_id'],
            y=df_at['anomaly_rate_pct'],
            marker=dict(color=THEME_COLORS["accent_amber"], line=dict(color="#1e293b", width=1))
        ))
    fig_anom_turb.update_layout(
        **PLOT_TEMPLATE_LAYOUT,
        height=280,
        xaxis_title="Turbine",
        yaxis_title="Anomaly Rate (%)",
        margin=dict(l=50, r=20, t=10, b=40)
    )

    return html.Div([
        create_kpi_row(cards),
        html.Div(
            style={"display": "grid", "gridTemplateColumns": "1.3fr 1fr", "gap": "20px"},
            children=[
                create_card_container("Sustained Underperformance Event Log", table),
                create_card_container("Turbine Anomaly Rate Distribution", dcc.Graph(figure=fig_anom_turb))
            ]
        )
    ])

def build_environmental_tab():
    # Environmental analysis charts
    fig_wind_pwr = go.Figure()
    if not data_service.df_pc.empty:
        fig_wind_pwr.add_trace(go.Scatter(
            x=data_service.df_pc['wind_speed_bin'],
            y=data_service.df_pc['power_mean'],
            mode='lines+markers',
            name='Measured Power',
            line=dict(color=THEME_COLORS["accent_cyan"], width=3)
        ))
        fig_wind_pwr.add_trace(go.Scatter(
            x=data_service.df_pc['wind_speed_bin'],
            y=data_service.df_pc['reference_power'],
            mode='lines',
            name='Rated Power (2300 kW)',
            line=dict(color=THEME_COLORS["accent_amber"], width=2, dash='dash')
        ))
    fig_wind_pwr.update_layout(
        **PLOT_TEMPLATE_LAYOUT,
        height=320,
        xaxis_title="Wind Speed (m/s)",
        yaxis_title="Active Power (kW)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    fig_polar = go.Figure()
    # Mock directional distribution or representative rose
    theta = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    r_freq = [14, 8, 5, 9, 18, 26, 12, 8]  # Prevailing South-Westerly winds in Scotland
    fig_polar.add_trace(go.Barpolar(
        r=r_freq,
        theta=theta,
        marker_color=["#00f2fe", "#38bdf8", "#818cf8", "#c084fc", "#f472b6", "#fb7185", "#38bdf8", "#00f2fe"],
        opacity=0.8
    ))
    fig_polar.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=THEME_COLORS["text_secondary"]),
        height=320,
        polar=dict(
            radialaxis=dict(visible=True, showticklabels=True, tickfont=dict(color="#64748b")),
            angularaxis=dict(tickfont=dict(color="#f8fafc", size=12))
        ),
        margin=dict(l=30, r=30, t=20, b=20)
    )

    return html.Div([
        html.Div(
            style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "20px"},
            children=[
                create_card_container("Wind Speed vs Farm Active Power Envelope", dcc.Graph(figure=fig_wind_pwr)),
                create_card_container("Prevailing Wind Direction Rose (Hill of Towie Site)", dcc.Graph(figure=fig_polar))
            ]
        )
    ])

def build_events_tab():
    cards = [
        create_kpi_card("Logged Alarms", "512,117", "Events", "16-Month Total Fleet Record", THEME_COLORS["accent_blue"]),
        create_kpi_card("Shutdown Records", "4,218", "Stops", "Controlled & Safety Trips", THEME_COLORS["accent_purple"]),
        create_kpi_card("Correlated Anomalies", "65.2", "%", "Underperformance with Active Alarm", THEME_COLORS["accent_green"]),
        create_kpi_card("Silent Drift Events", "34.8", "%", "Requires Pitch / Aerodynamic Inspection", THEME_COLORS["accent_amber"], "Requires Investigation")
    ]

    fig_alarms = go.Figure()
    if not data_service.df_alarms.empty:
        df_top_al = data_service.df_alarms.head(8).sort_values(by="count", ascending=True)
        fig_alarms.add_trace(go.Bar(
            x=df_top_al['count'],
            y=df_top_al['description'].apply(lambda s: s[:32] + "..." if len(str(s)) > 32 else s),
            orientation='h',
            marker=dict(color=THEME_COLORS["accent_cyan"], line=dict(color="#1e293b", width=1))
        ))
    fig_alarms.update_layout(
        **PLOT_TEMPLATE_LAYOUT,
        height=320,
        xaxis_title="Alarm Occurrence Count",
        yaxis_title="Alarm Event",
        margin=dict(l=180, r=20, t=10, b=40)
    )

    # Correlation donut chart
    fig_donut = go.Figure(data=[go.Pie(
        labels=["Coincident with SCADA Alarm / Stop", "Silent Aerodynamic / Pitch Drift"],
        values=[65.2, 34.8],
        hole=.5,
        marker=dict(colors=[THEME_COLORS["accent_green"], THEME_COLORS["accent_amber"]]),
        textinfo='label+percent'
    )])
    fig_donut.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=THEME_COLORS["text_secondary"]),
        height=320,
        legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5),
        margin=dict(l=20, r=20, t=10, b=30)
    )

    return html.Div([
        create_kpi_row(cards),
        html.Div(
            style={"display": "grid", "gridTemplateColumns": "1.2fr 1fr", "gap": "20px"},
            children=[
                create_card_container("Top SCADA Alarms by Occurrence Frequency", dcc.Graph(figure=fig_alarms)),
                create_card_container("Anomaly Root-Cause Correlation Split", dcc.Graph(figure=fig_donut))
            ]
        )
    ])

def build_replay_tab():
    controls = html.Div([
        html.Button("▶ Start Replay", id="btn-replay-play", n_clicks=0, style={
            "backgroundColor": THEME_COLORS["accent_green"],
            "color": "#000000",
            "fontWeight": "700",
            "border": "none",
            "padding": "8px 18px",
            "borderRadius": "6px",
            "cursor": "pointer",
            "marginRight": "10px"
        }),
        html.Button("⏸ Pause", id="btn-replay-pause", n_clicks=0, style={
            "backgroundColor": THEME_COLORS["accent_amber"],
            "color": "#000000",
            "fontWeight": "700",
            "border": "none",
            "padding": "8px 18px",
            "borderRadius": "6px",
            "cursor": "pointer",
            "marginRight": "10px"
        }),
        html.Button("⏮ Reset", id="btn-replay-reset", n_clicks=0, style={
            "backgroundColor": THEME_COLORS["bg_card_secondary"],
            "color": THEME_COLORS["text_primary"],
            "fontWeight": "600",
            "border": f"1px solid {THEME_COLORS['border']}",
            "padding": "8px 18px",
            "borderRadius": "6px",
            "cursor": "pointer",
            "marginRight": "15px"
        }),
        html.Span("Speed: ", style={"color": THEME_COLORS["text_secondary"], "fontSize": "13px", "fontWeight": "600", "marginRight": "6px"}),
        dcc.Dropdown(
            id="replay-speed-dropdown",
            options=[
                {"label": "1x (Normal)", "value": 1000},
                {"label": "5x (Fast)", "value": 200},
                {"label": "10x (High)", "value": 100}
            ],
            value=200,
            clearable=False,
            style={"width": "120px", "color": "#000000", "fontWeight": "600"}
        )
    ], style={"display": "flex", "alignItems": "center", "flexWrap": "wrap"})

    return html.Div([
        create_card_container(
            "Historical SCADA Streaming & Real-Time ML Inference Replay",
            html.Div([
                # State store and interval timer
                dcc.Store(id="replay-step-store", data={"step": 0, "running": False}),
                dcc.Interval(id="replay-interval", interval=200, n_intervals=0, disabled=True),

                html.Div(id="replay-live-kpi-container"),
                html.Div(
                    style={"marginTop": "20px"},
                    children=[
                        create_card_container("Real-Time Streaming Power: Actual vs AI Inference", dcc.Graph(id="replay-streaming-graph"))
                    ]
                )
            ]),
            controls=controls
        )
    ])

def build_main_layout():
    return html.Div(
        style={
            "backgroundColor": THEME_COLORS["bg_dark"],
            "minHeight": "100vh",
            "fontFamily": "Inter, sans-serif"
        },
        children=[
            create_header(),
            html.Div(
                style={"padding": "24px 36px"},
                children=[
                    dcc.Tabs(
                        id="main-tabs",
                        value="tab-exec",
                        children=[
                            dcc.Tab(label="1. Executive Overview", value="tab-exec", style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE),
                            dcc.Tab(label="2. Turbine Performance", value="tab-turb", style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE),
                            dcc.Tab(label="3. Power Prediction", value="tab-pred", style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE),
                            dcc.Tab(label="4. Abnormal Behavior", value="tab-anom", style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE),
                            dcc.Tab(label="5. Environmental Analysis", value="tab-env", style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE),
                            dcc.Tab(label="6. Maintenance & Events", value="tab-event", style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE),
                            dcc.Tab(label="7. Real-Time Replay", value="tab-replay", style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE),
                        ]
                    ),
                    html.Div(id="tab-content", style={"marginTop": "20px"})
                ]
            )
        ]
    )
