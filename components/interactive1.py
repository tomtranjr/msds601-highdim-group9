"""Interactive visualization exploring the bias-variance trade-off."""

from dash import dcc, html
import plotly.express as px

# Precompute figure to avoid recalculation on every layout render.
_bias_variance_fig = px.line(
    px.data.tips(),
    x="total_bill",
    y="tip",
    color="sex",
    title="OLS Fit Sensitivity Example",
)

interactive_layout = html.Section(
    style={"marginTop": "40px"},
    children=[
        html.H2("Interactive Example: Sensitivity in OLS"),
        html.P(
            "Explore how the fitted regression line changes across subgroups. "
            "Hover to inspect individual observations."
        ),
        dcc.Graph(figure=_bias_variance_fig, config={"displayModeBar": False}),
    ],
)

