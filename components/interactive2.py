"""Interactive visualization for regularization paths."""

from dash import dcc, html
import numpy as np
import pandas as pd
import plotly.express as px

# Simulate a small ridge vs lasso coefficient path for illustration.
_lambda_grid = np.linspace(0, 10, 100)
_ridge_coef = 1 / (1 + _lambda_grid)
_lasso_coef = np.maximum(1 - _lambda_grid / 5, 0)
_path_df = pd.DataFrame(
    {
        "Penalty": np.concatenate([_lambda_grid, _lambda_grid]),
        "Coefficient": np.concatenate([_ridge_coef, _lasso_coef]),
        "Method": ["Ridge"] * len(_lambda_grid) + ["LASSO"] * len(_lambda_grid),
    }
)
_path_fig = px.line(
    _path_df,
    x="Penalty",
    y="Coefficient",
    color="Method",
    title="Regularization Path Comparison",
    labels={"Penalty": "Penalty Strength (λ)", "Coefficient": "Coefficient Value"},
)

another_plot = html.Section(
    style={"marginTop": "40px"},
    children=[
        html.H2("Regularization Paths"),
        html.P(
            "Compare how Ridge and LASSO shrink coefficients as the penalty strength increases."
        ),
        dcc.Graph(figure=_path_fig, config={"displayModeBar": False}),
    ],
)

