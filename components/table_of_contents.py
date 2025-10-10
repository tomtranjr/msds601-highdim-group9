"""Interactive Table of Contents that scrolls to each section."""

from dash import html


def make_table_of_contents():
    """Interactive Table of Contents that scrolls to each section."""

    toc_items = [
        ("0. Introduction", "md-00_intro"),
        ("1. Start from Multiple Linear Regression", "md-01_startMLR"),
        ("2. The High-Dimensional Setting", "md-02_highdim_setting"),
        ("3. Why OLS Breaks Down", "md-03_ols_breakdown"),
        ("4. Regularization & Dimension Reduction", "md-04_regularization_dimred"),
        ("5. Why This Matters", "md-05_why_matters"),
        ("References", "md-references"),
        ("Contributors", "md-contributors"),
    ]

    list_items = [
        html.Li(
            html.A(
                label,
                href=f"#{section_id}",
                style={
                    "textDecoration": "none",
                    "color": "#007bff",
                    "fontWeight": 500,
                },
            ),
            style={"marginBottom": "0.5rem"},
        )
        for label, section_id in toc_items
    ]

    container_style = {
        "marginBottom": "40px",
        "padding": "16px",
        "backgroundColor": "#f9f9f9",
        "borderRadius": "8px",
        "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
        "fontFamily": "Helvetica, Arial, sans-serif",
    }

    return html.Div(
        style=container_style,
        children=[
            html.H2("Table of Contents", style={"marginTop": 0}),
            html.Ul(list_items, style={"paddingLeft": "1.25rem", "margin": 0}),
        ],
    )

