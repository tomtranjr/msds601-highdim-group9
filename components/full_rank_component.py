"""Interactive component demonstrating why full column rank matters in OLS."""

from __future__ import annotations

import math
from typing import Dict, List, Optional

import numpy as np
from dash import MATCH, Input, Output, State, dcc, html, no_update


def make_full_rank_component(app, uid: str = "fullrank"):
    """Return a Dash layout that explores full column rank in linear regression."""

    debug = False  # Toggle to True for console diagnostics.

    rng = np.random.default_rng(2024)

    styles: Dict[str, Dict[str, str]] = {
        "wrap": {
            "maxWidth": "980px",
            "margin": "1.5rem auto",
            "fontFamily": "system-ui, Arial, sans-serif",
            "color": "#202124",
        },
        "introTitle": {"fontSize": "22px", "fontWeight": 700, "marginBottom": "0.5rem"},
        "introText": {"fontSize": "15px", "lineHeight": "1.6", "marginBottom": "1rem"},
        "controls": {
            "display": "grid",
            "gridTemplateColumns": "repeat(auto-fit, minmax(240px, 1fr))",
            "gap": "1rem",
            "alignItems": "center",
            "marginBottom": "1rem",
        },
        "sliderLabel": {"fontWeight": 600, "marginBottom": "0.25rem"},
        "warning": {
            "backgroundColor": "#fdecea",
            "border": "1px solid #f5c6c1",
            "color": "#b71c1c",
            "padding": "0.75rem 1rem",
            "borderRadius": "8px",
            "fontWeight": 600,
            "marginBottom": "1rem",
            "display": "none",
        },
        "warningActive": {
            "backgroundColor": "#fdecea",
            "border": "1px solid #f5c6c1",
            "color": "#b71c1c",
            "padding": "0.75rem 1rem",
            "borderRadius": "8px",
            "fontWeight": 600,
            "marginBottom": "1rem",
            "display": "block",
        },
        "summary": {
            "backgroundColor": "#f5f7fb",
            "borderRadius": "8px",
            "padding": "0.75rem 1rem",
            "marginBottom": "1rem",
            "fontSize": "14px",
            "lineHeight": "1.6",
        },
        "matrixStack": {
            "display": "flex",
            "flexDirection": "column",
            "gap": "1.25rem",
        },
        "panel": {
            "backgroundColor": "#ffffff",
            "border": "1px solid #e2e5ed",
            "borderRadius": "10px",
            "padding": "1rem",
            "boxShadow": "0 4px 10px rgba(15, 35, 95, 0.04)",
        },
        "panelTitle": {
            "fontSize": "16px",
            "fontWeight": 700,
            "marginBottom": "0.75rem",
        },
        "matrixText": {
            "fontFamily": "Menlo, Consolas, monospace",
            "fontSize": "12px",
            "whiteSpace": "pre",
            "overflowX": "auto",
            "overflowY": "auto",
            "maxHeight": "320px",
            "backgroundColor": "#fafcff",
            "padding": "0.75rem",
            "borderRadius": "8px",
            "border": "1px solid #e2e5ed",
        },
        "inverseMessage": {"color": "#6b7280", "fontStyle": "italic"},
    }

    presets = {
        "normal": (100, 5),
        "near": (40, 8),
        "square": (10, 10),
        "wide": (6, 10),
    }

    def _matrix_block(
        mat: np.ndarray,
        *,
        precision: int = 3,
        suppress: bool = True,
        floatmode: str = "maxprec_equal",
    ) -> html.Pre:
        with np.printoptions(
            precision=precision, suppress=suppress, floatmode=floatmode
        ):
            rendered = np.array2string(mat, separator=", ")
        return html.Pre(rendered, style=styles["matrixText"])

    container = html.Div(
        id={"type": "fullrank-wrap", "uid": uid},
        style=styles["wrap"],
        children=[
            html.H2(
                "Why Full Column Rank Keeps Ordinary Least Squares on Solid Ground",
                style=styles["introTitle"],
            ),
            html.P(
                (
                    "Adjust the number of observations and predictors to see how the "
                    "rank of the design matrix X affects the invertibility of XᵀX and "
                    "our ability to compute the OLS solution."
                ),
                style=styles["introText"],
            ),
            html.Div(
                style=styles["controls"],
                children=[
                    html.Div(
                        children=[
                            html.Div("Scenario presets", style=styles["sliderLabel"]),
                            dcc.Dropdown(
                                id={"type": "fullrank-preset", "uid": uid},
                                options=[
                                    {
                                        "label": "Normal case (n >> p)",
                                        "value": "normal",
                                    },
                                    {
                                        "label": "n ≈ p",
                                        "value": "near",
                                    },
                                    {
                                        "label": "n = p",
                                        "value": "square",
                                    },
                                    {
                                        "label": "p >> n",
                                        "value": "wide",
                                    },
                                ],
                                placeholder="Select a preset...",
                                clearable=True,
                            ),
                        ]
                    ),
                    html.Div(
                        children=[
                            html.Div(
                                "Number of observations (n)",
                                style=styles["sliderLabel"],
                            ),
                            dcc.Slider(
                                id={"type": "fullrank-n", "uid": uid},
                                min=2,
                                max=100,
                                step=1,
                                value=100,
                                marks=None,
                                tooltip={"always_visible": False},
                            ),
                        ]
                    ),
                    html.Div(
                        children=[
                            html.Div(
                                "Number of predictors (p)", style=styles["sliderLabel"]
                            ),
                            dcc.Slider(
                                id={"type": "fullrank-p", "uid": uid},
                                min=1,
                                max=10,
                                step=1,
                                value=5,
                                tooltip={"always_visible": False},
                            ),
                        ]
                    ),
                    html.Div(
                        children=[
                            html.Button(
                                "Generate New X",
                                id={"type": "fullrank-generate", "uid": uid},
                                n_clicks=0,
                                style={
                                    "padding": "0.6rem 1.2rem",
                                    "fontWeight": 600,
                                    "borderRadius": "8px",
                                    "border": "none",
                                    "backgroundColor": "#1a73e8",
                                    "color": "#ffffff",
                                    "cursor": "pointer",
                                },
                            ),
                        ]
                    ),
                ],
            ),
            html.Div(
                id={"type": "fullrank-warning", "uid": uid},
                style=styles["warning"],
            ),
            html.Div(
                id={"type": "fullrank-summary", "uid": uid},
                style=styles["summary"],
            ),
            html.Div(
                id={"type": "fullrank-visuals", "uid": uid},
                style=styles["matrixStack"],
            ),
            dcc.Store(
                id={"type": "fullrank-store", "uid": uid},
                data={"seed": 0},
            ),
        ],
    )

    @app.callback(
        Output({"type": "fullrank-n", "uid": MATCH}, "value"),
        Output({"type": "fullrank-p", "uid": MATCH}, "value"),
        Input({"type": "fullrank-preset", "uid": MATCH}, "value"),
        prevent_initial_call=True,
    )
    def _apply_preset(preset_key):
        if preset_key is None:
            return no_update, no_update
        n_val, p_val = presets[preset_key]
        return n_val, p_val

    @app.callback(
        Output({"type": "fullrank-store", "uid": MATCH}, "data"),
        Input({"type": "fullrank-generate", "uid": MATCH}, "n_clicks"),
        State({"type": "fullrank-store", "uid": MATCH}, "data"),
        prevent_initial_call=True,
    )
    def _update_seed(n_clicks, store_data):
        if not n_clicks:
            return store_data
        next_seed = int(rng.integers(0, 10_000_000))
        return {"seed": next_seed}

    @app.callback(
        Output({"type": "fullrank-warning", "uid": MATCH}, "children"),
        Output({"type": "fullrank-warning", "uid": MATCH}, "style"),
        Output({"type": "fullrank-summary", "uid": MATCH}, "children"),
        Output({"type": "fullrank-visuals", "uid": MATCH}, "children"),
        Input({"type": "fullrank-n", "uid": MATCH}, "value"),
        Input({"type": "fullrank-p", "uid": MATCH}, "value"),
        Input({"type": "fullrank-store", "uid": MATCH}, "data"),
    )
    def _render(n_val, p_val, store_data):
        if n_val is None or p_val is None:
            return no_update, no_update, no_update, no_update

        seed = int(store_data.get("seed", 0)) if store_data else 0
        local_rng = np.random.default_rng(seed)
        X = local_rng.integers(-9, 10, size=(n_val, p_val)).astype(float)

        xtx = X.T @ X
        rank = np.linalg.matrix_rank(X)
        condition_number = np.linalg.cond(xtx) if p_val > 0 else np.inf
        is_full_rank = rank == p_val
        near_singular = condition_number > 1e10

        if debug:
            print(">>> Checking matrix multiplication")
            print(f"Seed: {seed}")
            print(f"X shape: {X.shape}, dtype: {X.dtype}")
            print(f"XᵀX shape: {xtx.shape}")
            print("Sample X:\n", X[: min(5, n_val), : min(5, p_val)])
            print("Sample XᵀX:\n", xtx[: min(5, p_val), : min(5, p_val)])

        xtx_inv: Optional[np.ndarray] = None
        inverse_message: Optional[str] = None
        if is_full_rank and not near_singular:
            try:
                xtx_inv = np.linalg.inv(xtx)
                if debug:
                    identity_check = xtx_inv @ xtx
                    print("Inverse computed.")
                    print("Inverse(XᵀX) @ XᵀX ≈ I ? ", np.allclose(identity_check, np.eye(p_val)))
                    print("Condition number:", condition_number)
            except np.linalg.LinAlgError:
                xtx_inv = None
                inverse_message = "Numerical inversion failed."
        else:
            inverse_message = (
                "XᵀX is singular or ill-conditioned; inverse not available."
            )

        warning_needed = not is_full_rank or near_singular
        warning_children = []
        warning_style = styles["warning"]
        if warning_needed:
            warning_children = [
                "⚠️ Warning: X is not full column rank! (XᵀX is singular or nearly singular)."
            ]
            warning_style = styles["warningActive"]

        summary_children = [
            html.Div(f"n (rows of X): {n_val}"),
            html.Div(f"p (columns of X): {p_val}"),
            html.Div(f"rank(X): {rank}"),
            html.Div(
                f"Condition number of XᵀX: {'{:.2e}'.format(condition_number)}"
                if math.isfinite(condition_number)
                else "Condition number of XᵀX: undefined"
            ),
        ]
        if inverse_message and xtx_inv is None:
            summary_children.append(html.Div(inverse_message))

        visuals_children: List[html.Div] = []

        def _panel(title: str, body_children):
            return html.Div(
                style=styles["panel"],
                children=[
                    html.Div(title, style=styles["panelTitle"]),
                    body_children,
                ],
            )

        visuals_children.append(_panel("Design matrix X", _matrix_block(X, precision=0)))
        visuals_children.append(
            _panel("Cross-product XᵀX", _matrix_block(xtx, precision=2))
        )
        if xtx_inv is not None:
            visuals_children.append(
                _panel(
                    "Inverse (XᵀX)⁻¹",
                    _matrix_block(xtx_inv, precision=6, suppress=False),
                )
            )
        else:
            visuals_children.append(
                _panel(
                    "Inverse (XᵀX)⁻¹",
                    html.Div(
                        inverse_message or "Inverse not available.",
                        style=styles["inverseMessage"],
                    ),
                )
            )

        return warning_children, warning_style, summary_children, visuals_children

    return container


def _diagnostic_suite():
    print("=== Diagnostic suite for full_rank_component ===")
    test_cases = [
        np.array([[1., 2.], [3., 4.], [5., 6.]]),
        np.array([[2., -1., 0.], [0., 1., 1.], [1., 1., 0.]]),
    ]
    for idx, X in enumerate(test_cases, start=1):
        print(f"\nCase {idx}: X shape = {X.shape}")
        XTX = X.T @ X
        print("X:\n", X)
        print("XᵀX:\n", XTX)
        print("np.allclose(XᵀX, X.T @ X)?", np.allclose(XTX, X.T @ X))
        det = np.linalg.det(XTX)
        cond = np.linalg.cond(XTX)
        print(f"det(XᵀX) = {det:.6f}")
        print(f"cond(XᵀX) = {cond:.6f}")
        try:
            inv = np.linalg.inv(XTX)
            print("(XᵀX)⁻¹:\n", inv)
            identity_check = XTX @ inv
            print("np.allclose((XᵀX) @ (XᵀX)⁻¹, I)?", np.allclose(identity_check, np.eye(XTX.shape[0])))
        except np.linalg.LinAlgError:
            print("Matrix is singular; inverse does not exist.")


if __name__ == "__main__":
    _diagnostic_suite()
