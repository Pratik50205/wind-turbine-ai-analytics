"""
Dashboard Theme and Design System
Modern, dark, sleek design tokens and styles.
"""

THEME_COLORS = {
    "bg_dark": "#0b0f19",
    "bg_card": "#151e2e",
    "bg_card_secondary": "#1e293b",
    "border": "#2d3748",
    "accent_cyan": "#00f2fe",
    "accent_blue": "#38bdf8",
    "accent_green": "#10b981",
    "accent_amber": "#f59e0b",
    "accent_red": "#ef4444",
    "accent_purple": "#8b5cf6",
    "text_primary": "#f8fafc",
    "text_secondary": "#94a3b8",
    "text_muted": "#64748b"
}

BASE_STYLE = {
    "backgroundColor": THEME_COLORS["bg_dark"],
    "color": THEME_COLORS["text_primary"],
    "fontFamily": "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
    "minHeight": "100vh",
    "padding": "0px",
    "margin": "0px"
}

HEADER_STYLE = {
    "backgroundColor": THEME_COLORS["bg_card"],
    "borderBottom": f"1px solid {THEME_COLORS['border']}",
    "padding": "16px 32px",
    "display": "flex",
    "justifyContent": "space-between",
    "alignItems": "center"
}

CARD_STYLE = {
    "backgroundColor": THEME_COLORS["bg_card"],
    "border": f"1px solid {THEME_COLORS['border']}",
    "borderRadius": "12px",
    "padding": "20px",
    "boxShadow": "0 4px 12px rgba(0, 0, 0, 0.3)",
    "marginBottom": "20px"
}

KPI_CARD_STYLE = {
    "backgroundColor": THEME_COLORS["bg_card"],
    "border": f"1px solid {THEME_COLORS['border']}",
    "borderRadius": "10px",
    "padding": "16px 20px",
    "flex": "1",
    "minWidth": "180px",
    "boxShadow": "0 4px 12px rgba(0, 0, 0, 0.25)"
}

TAB_STYLE = {
    "backgroundColor": THEME_COLORS["bg_card_secondary"],
    "color": THEME_COLORS["text_secondary"],
    "border": "none",
    "padding": "12px 20px",
    "fontWeight": "600",
    "fontSize": "14px",
    "borderRadius": "8px 8px 0 0",
    "cursor": "pointer"
}

TAB_SELECTED_STYLE = {
    "backgroundColor": THEME_COLORS["bg_card"],
    "color": THEME_COLORS["accent_cyan"],
    "borderTop": f"3px solid {THEME_COLORS['accent_cyan']}",
    "borderLeft": f"1px solid {THEME_COLORS['border']}",
    "borderRight": f"1px solid {THEME_COLORS['border']}",
    "borderBottom": "none",
    "padding": "12px 20px",
    "fontWeight": "700",
    "fontSize": "14px"
}

PLOT_TEMPLATE_LAYOUT = {
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(0,0,0,0)",
    "font": {"color": THEME_COLORS["text_secondary"], "family": "Inter, sans-serif"},
    "xaxis": {"gridcolor": "#1e293b", "zerolinecolor": "#334155"},
    "yaxis": {"gridcolor": "#1e293b", "zerolinecolor": "#334155"}
}
