# lasso_component.py
import numpy as np
import pandas as pd
from dash import MATCH, Input, Output, dcc, html
from sklearn.linear_model import Lasso
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def make_lasso_component(app, uid="lasso", *, n=50, p=150):
    """Return a self-contained Dash LASSO equation component."""

    # ---------------------------
    # 1) Create synthetic data
    # ---------------------------
    rng = np.random.default_rng(0)
    X_raw = rng.normal(size=(n, p))

    beta_true = np.zeros(p)
    beta_true[[19, 39, 59, 79, 99, 98]] = [0.25, -0.75, 1.0, -3.5, 4.0, -6.0]

    signal = X_raw @ beta_true
    sigma = np.std(signal) / np.sqrt(5.0)
    noise = rng.normal(scale=sigma, size=n)
    y_raw = signal + noise

    X_train, X_test, y_train, y_test = train_test_split(
        X_raw, y_raw, test_size=0.2, random_state=47
    )

    scaler = StandardScaler().fit(X_train)
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)

    # ---------------------------
    # 2) Precompute LASSO fits
    # ---------------------------
    alphas = [0.0001, 0.001, 0.01, 0.1, 1, 10]
    coefs = np.zeros((len(alphas), X_raw.shape[1]))
    intercepts = np.zeros(len(alphas))
    r2s = np.zeros(len(alphas))

    for i, a in enumerate(alphas):
        m = Lasso(alpha=a, max_iter=20000, random_state=0)
        m.fit(X_train, y_train)
        coefs[i] = m.coef_
        intercepts[i] = m.intercept_
        r2s[i] = r2_score(y_test, m.predict(X_test))

    true_set = {j + 1 for j in np.flatnonzero(beta_true)}  # highlight these

    # ---------------------------
    # 3) Styles (local)
    # ---------------------------
    styles = {
        "wrap": {
            "maxWidth": "980px",
            "margin": "1rem auto",
            "fontFamily": "system-ui, Arial, sans-serif",
        },
        "title": {"margin": "0 0 0.25rem 0", "fontSize": "20px", "fontWeight": 700},
        "subtitle": {"color": "#555", "marginBottom": "0.75rem", "fontSize": "14px"},
        "metrics": {"marginTop": "0.5rem", "fontSize": "14px", "color": "#333"},
        "equation": {
            "fontSize": "20px",
            "lineHeight": "1.7",
            "overflowWrap": "anywhere",
        },
        "plus": {"fontWeight": 400, "padding": "0 0.25rem"},
        "termBold": {"fontWeight": 700},
        "termRed": {"fontWeight": 700, "color": "#c62828"},
    }

    marks = {i: f"{a:g}" for i, a in enumerate(alphas)}

    # ---------------------------
    # 4) Equation rendering
    # ---------------------------
    def _beta_x_term(j1: int, is_true: bool):
        st = styles["termRed"] if is_true else styles["termBold"]
        return html.Span(
            [
                html.Span("β", style={"fontStyle": "italic"}),
                html.Sub(str(j1)),
                html.Span("("),
                html.Span("x", style={"fontStyle": "italic"}),
                html.Sub(str(j1)),
                html.Span(")"),
            ],
            style=st,
        )

    def _equation_children(idx: int, wrap_every: int = 8):
        w = coefs[idx]
        nz = np.flatnonzero(w != 0.0)
        parts = []
        parts.append(html.Span("ŷ = ", style={"fontWeight": 700}))
        parts.extend(
            [
                html.Span("β", style={"fontStyle": "italic", "fontWeight": 700}),
                html.Sub("0"),
            ]
        )
        if nz.size:
            parts.append(html.Span("+", style=styles["plus"]))
            line_terms, count = [], 0
            for j in nz:
                j1 = j + 1
                line_terms.append(_beta_x_term(j1, j1 in true_set))
                count += 1
                if count < len(nz) and (count % wrap_every) != 0:
                    line_terms.append(html.Span("+", style=styles["plus"]))
                if count % wrap_every == 0 and count < len(nz):
                    parts.extend(line_terms)
                    parts.append(html.Br())
                    line_terms = []
            parts.extend(line_terms)
        else:
            parts.append(
                html.Span(" (no predictors selected)", style={"color": "#665"})
            )
        return parts

    # ---------------------------
    # 5) Component layout
    # ---------------------------
    container = html.Div(
        id={"type": "lasso-wrap", "uid": uid},
        style=styles["wrap"],
        children=[
            html.H1('A "Simple" Demonstration of LASSO Regularization'),
            html.P(
                """
To get a grasp of how the LASSO regression method handles high dimensional data, it is best to look at a simple example. In the real world, high dimensional data sets have thousands or even millions of parameters coupled with a smaller number of observations. However, such data sets do not lend themselves to easy explanations. Thus, we created a synthetic data set for demonstration purposes. 
"""
            ),
            html.P(
                """
The interactive graph below is based on our data set which we created with Numpy, a python module, and has 150 parameters (p=150) and 50 observations (n=50). This is no doubt a small data set. But, by definition, it is a high dimensional none the less (p >> n). Because the data is synthetic, we had the luxury of making our own true β’s which are located at β20, β40, β60, β80, β99, and β100. We set a signal to noise ratio of 5 to create our X matrix, β Matrix, error matrix and finally our y equation at y = Xβ + ε. 
"""
            ),
            html.P(
                """
Finally, using Sklearn, another python module, we split our synthetic data into a portion for training and a portion for testing and iteratively created 6 LASSO models at incremental alpha levels (0.0001, 0.001, 0.01, 0.1, 1, 10) to illustrate the model pushing β coefficients into and out of the model. Think of the alpha level as the “penalty” the model applies to each β coefficient. As the alpha level gets smaller, the β coefficients receive a small push towards zero, leaving most of the coefficients in the model. Conversely, as the alpha level grows larger, the β coefficients receive a large push towards zero which removes many of the coefficients entirely.
"""
            ),
            html.Div(
                "Visualization of the relationship between α and number of predictors",
                style=styles["title"],
            ),
            html.Div(
                "Move the alpha (α) slider to watch predictors add and drop from the model. True predictors are red.",
                style=styles["subtitle"],
            ),
            dcc.Slider(
                id={"type": "lasso-alpha", "uid": uid},
                min=0,
                max=len(alphas) - 1,
                step=None,
                value=len(alphas) // 2,
                marks=marks,
                tooltip={"always_visible": False},
            ),
            html.Div(id={"type": "lasso-metrics", "uid": uid}, style=styles["metrics"]),
            html.Div(
                id={"type": "lasso-equation", "uid": uid}, style=styles["equation"]
            ),
        ],
    )

    # ---------------------------
    # 6) Callback (scoped)
    # ---------------------------
    @app.callback(
        Output({"type": "lasso-equation", "uid": MATCH}, "children"),
        Output({"type": "lasso-metrics", "uid": MATCH}, "children"),
        Input({"type": "lasso-alpha", "uid": MATCH}, "value"),
        prevent_initial_call=False,
    )
    def _update(alpha_idx):
        eq = _equation_children(alpha_idx)
        selected = int(np.sum(coefs[alpha_idx] != 0.0))
        r2 = r2s[alpha_idx]
        a = alphas[alpha_idx]
        metrics = f"α = {a:g} | selected predictors = {selected} | Test R² = {r2:.3f}"
        return eq, metrics

    return container
