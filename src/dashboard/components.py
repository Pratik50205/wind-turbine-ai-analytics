"""
Dashboard UI Components
Reusable, modular, dark-themed UI components for Hill of Towie Wind Farm Dashboard.
"""

from dash import html, dcc
from .styles import THEME_COLORS, KPI_CARD_STYLE, CARD_STYLE

def create_header():
    return html.Div(
        style={
            "backgroundColor": THEME_COLORS["bg_card"],
            "borderBottom": f"1px solid {THEME_COLORS['border']}",
            "padding": "18px 36px",
            "display": "flex",
            "justifyContent": "space-between",
            "alignItems": "center",
            "flexWrap": "wrap",
            "gap": "15px"
        },
        children=[
            html.Div([
                html.Div([
                    html.Span("⚡ ", style={"fontSize": "26px"}),
                    html.Span("HILL OF TOWIE WIND FARM", style={
                        "fontSize": "22px",
                        "fontWeight": "800",
                        "letterSpacing": "1.5px",
                        "background": "linear-gradient(90deg, #00f2fe 0%, #4facfe 100%)",
                        "WebkitBackgroundClip": "text",
                        "WebkitTextFillColor": "transparent"
                    }),
                ], style={"display": "flex", "alignItems": "center", "gap": "10px"}),
                html.Div("AI-Based Performance Analysis, Power Prediction & SCADA Replay Engine", style={
                    "color": THEME_COLORS["text_secondary"],
                    "fontSize": "13px",
                    "marginTop": "4px",
                    "fontWeight": "500"
                })
            ]),
            html.Div([
                html.Div([
                    html.Span("● LIVE DATA ACTIVE", style={
                        "display": "inline-block",
                        "backgroundColor": "rgba(16, 185, 129, 0.15)",
                        "color": THEME_COLORS["accent_green"],
                        "border": f"1px solid {THEME_COLORS['accent_green']}",
                        "padding": "6px 14px",
                        "borderRadius": "20px",
                        "fontSize": "12px",
                        "fontWeight": "700",
                        "letterSpacing": "0.5px"
                    }),
                    html.Span("21 Turbines (48.3 MW)", style={
                        "backgroundColor": THEME_COLORS["bg_card_secondary"],
                        "color": THEME_COLORS["text_primary"],
                        "border": f"1px solid {THEME_COLORS['border']}",
                        "padding": "6px 14px",
                        "borderRadius": "20px",
                        "fontSize": "12px",
                        "fontWeight": "600",
                        "marginLeft": "10px"
                    })
                ], style={"display": "flex", "alignItems": "center"})
            ])
        ]
    )

def create_kpi_card(title, value, unit="", subtitle="", color=THEME_COLORS["accent_cyan"], badge=""):
    return html.Div(
        style={
            **KPI_CARD_STYLE,
            "borderTop": f"3px solid {color}",
            "position": "relative"
        },
        children=[
            html.Div([
                html.Span(title, style={
                    "color": THEME_COLORS["text_secondary"],
                    "fontSize": "12px",
                    "fontWeight": "600",
                    "textTransform": "uppercase",
                    "letterSpacing": "0.8px"
                }),
                html.Span(badge, style={
                    "color": color,
                    "fontSize": "11px",
                    "fontWeight": "700",
                    "float": "right"
                }) if badge else None
            ]),
            html.Div([
                html.Span(f"{value}", style={
                    "fontSize": "28px",
                    "fontWeight": "800",
                    "color": THEME_COLORS["text_primary"],
                    "letterSpacing": "-0.5px"
                }),
                html.Span(f" {unit}", style={
                    "fontSize": "14px",
                    "fontWeight": "600",
                    "color": THEME_COLORS["text_muted"],
                    "marginLeft": "4px"
                }) if unit else None
            ], style={"marginTop": "8px"}),
            html.Div(subtitle, style={
                "color": THEME_COLORS["text_muted"],
                "fontSize": "11px",
                "marginTop": "4px",
                "fontWeight": "500"
            }) if subtitle else None
        ]
    )

def create_kpi_row(cards):
    return html.Div(
        style={
            "display": "grid",
            "gridTemplateColumns": f"repeat(auto-fit, minmax(200px, 1fr))",
            "gap": "16px",
            "marginBottom": "24px"
        },
        children=cards
    )

def create_card_container(title, children, controls=None):
    return html.Div(
        style=CARD_STYLE,
        children=[
            html.Div(
                style={
                    "display": "flex",
                    "justifyContent": "space-between",
                    "alignItems": "center",
                    "borderBottom": f"1px solid {THEME_COLORS['border']}",
                    "paddingBottom": "14px",
                    "marginBottom": "16px"
                },
                children=[
                    html.H3(title, style={
                        "margin": 0,
                        "fontSize": "16px",
                        "fontWeight": "700",
                        "color": THEME_COLORS["text_primary"],
                        "letterSpacing": "0.3px"
                    }),
                    controls if controls else html.Div()
                ]
            ),
            html.Div(children)
        ]
    )
