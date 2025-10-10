# lasso_path_component.py
import numpy as np
from sklearn.linear_model import lasso_path
from dash import html, dcc
import plotly.graph_objs as go

# Optional style tokens (tweak or remove as you like)
STYLES = {
    "wrap": {"maxWidth": "1000px", "margin": "0 auto", "fontFamily": "system-ui, Arial, sans-serif"},
    "title": {"margin": "0.5rem 0 0.25rem 0", "fontSize": "20px", "fontWeight": 700},
    "subtitle": {"color": "#555", "marginBottom": "0.75rem", "fontSize": "14px"},
    "meta": {"fontSize": "14px", "color": "#555", "marginTop": "8px"},
}

def make_lasso_path_component(
    app,
    uid="lasso-path",
    *,
    n=40,
    p=120,
    seed=0,
    target_signal_noise_ratio=5.0,
    alphas=None,
    highlight_true_support=True,
):
    """
    Build a namespaced Dash component rendering LASSO coefficient paths.

    Parameters
    ----------
    app : dash.Dash
        Your Dash app instance (not used directly, but kept for API parity with your other components).
    uid : str
        Namespace prefix for element IDs to avoid collisions on larger pages.
    n, p : int
        Synthetic data dimensions (rows, columns).
    seed : int
        RNG seed for reproducibility.
    target_signal_noise_ratio : float
        Controls noise scale relative to signal.
    alphas : array-like or None
        If None, uses np.logspace(-2, 2, 50).
    highlight_true_support : bool
        Thicken/brighten lines for indices used in beta_true.

    Returns
    -------
    dash.html.Div
        A container with title, subtitle, the Plotly graph, and a small meta section.
    """
    # ----- Data generation (matches your script's structure) -----
    rng = np.random.default_rng(seed)
    X = rng.normal(size=(n, p))

    beta_true = np.zeros(p)
    # last index is p-1 to keep general for any p >= 120
    support_indices = [19, 39, 59, 79, 99, min(119, p - 1)]
    beta_true[support_indices] = [0.25, -0.75, 1.0, -3.5, 4.0, -6.0]

    signal = X @ beta_true
    sigma = np.std(signal) / np.sqrt(target_signal_noise_ratio)
    noise = rng.normal(scale=sigma, size=n)
    y = signal + noise

    # LASSO path
    if alphas is None:
        alphas = np.logspace(-2, 2, 50)
    alphas, coefs, _ = lasso_path(X, y, alphas=alphas)  # coefs shape: (p, n_alphas)

    true_support = set(support_indices)

    # ----- Build Plotly figure -----
    traces = []
    for j, coef_path in enumerate(coefs):
        is_true = (j in true_support) and highlight_true_support
        traces.append(
            go.Scatter(
                x=alphas,
                y=coef_path,
                mode="lines",
                name=f"β[{j}]",
                # Use f-string and escape braces so Plotly gets %{x}/%{y} placeholders
                hovertemplate=f"alpha=%{{x:.4f}}<br>coef=%{{y:.4f}}<extra>β[{j}]</extra>",
                line=dict(width=2 if is_true else 1, dash="solid"),
                opacity=1.0 if is_true else 0.5,
                showlegend=False,
            )
        )

    layout = go.Layout(
        title="LASSO Coefficient Paths (Synthetic)",
        xaxis=dict(title="Lambda (Regularization Strength)", type="log"),
        yaxis=dict(title="Coefficient Value"),
        hovermode="closest",
        margin=dict(l=60, r=20, t=60, b=60),
        plot_bgcolor="#fff",
        paper_bgcolor="#fff",
        height=650,
        font=dict(family=STYLES["wrap"]["fontFamily"], size=14),
    )
    fig = go.Figure(data=traces, layout=layout)

    # ----- Component -----
    return html.Div(
        id=f"{uid}-wrap",
        style=STYLES["wrap"],
        children=[
            html.Div("LASSO Coefficient Paths (Synthetic)", style=STYLES["title"], id=f"{uid}-title"),
            html.Div(
                "Replicates the matplotlib-style path plot using Plotly. "
                "Highlighted (thicker) paths correspond to the true non-zero coefficients.",
                style=STYLES["subtitle"],
                id=f"{uid}-subtitle",
            ),
            dcc.Graph(
                id=f"{uid}-graph",
                figure=fig,
                config={"displayModeBar": True, "responsive": True},
                style={"height": "650px"},
            ),
            html.Div(
                style=STYLES["meta"],
                children=[
                    html.Div(f"n = {n}, p = {p}, target SNR = {target_signal_noise_ratio}"),
                    html.Div("True support indices: " + ", ".join(map(str, sorted(true_support)))),
                ],
                id=f"{uid}-meta",
            ),
            html.P('''
The Lasso Coefficient Paths graph provides a visual representation of how predictor variables behave under different levels of regularization. On the x-axis, we have lambda (λ), the regularization strength, displayed on a logarithmic scale. Lambda acts as a penalty that controls how many predictors are allowed into the model. When lambda is small (on the left side), the penalty is weak, so many predictors are retained in the model. As lambda increases (moving to the right), the penalty grows stronger, forcing more coefficients to shrink toward zero until only the most important predictors remain. On the y-axis, the graph shows the coefficient values, which indicate the impact of each predictor on the forecast. Each colored line represents a predictor variable, and the height of the line reflects how strongly that predictor is influencing the outcome at a given penalty level.
            '''),
                        html.P('''
At the beginning of the path (low lambda), many lines are far from zero, showing that multiple predictors are active. However, as lambda increases, these lines gradually converge toward zero, meaning that predictors are being eliminated from the model. Ultimately, only a few predictors remain nonzero, highlighting the variables that carry the most predictive power. This shrinking process illustrates one of Lasso’s greatest strengths: the ability to perform both variable selection and regularization simultaneously, resulting in a simpler and more interpretable model.
            '''),
                        html.P('''
This concept is particularly important in high-dimensional forecasting problems. For example, Mei and Shi (2024) apply Lasso to forecast U.S. unemployment using more than 121 macroeconomic variables, a case where the number of predictors exceeds the number of observations (p > n). In such settings, Ordinary Least Squares (OLS) fails because the system becomes unsolvable and prone to overfitting. Lasso addresses this by shrinking coefficients and enforcing sparsity, allowing only the most relevant predictors to remain. However, the authors caution that “Plain Lasso” (Plasso) may perform poorly when predictors are highly persistent, such as inflation or interest rates. To resolve this, they propose using “Standardized Lasso” (Slasso), which adjusts for differences in persistence and provides more stable results.
            '''),
                                    html.P('''
To connect this back to the real world, imagine forecasting unemployment with 121 potential predictors, including CPI, oil prices, stock returns, and GDP growth. With a low lambda, the model attempts to use nearly all predictors, risking overfitting and noise. As lambda increases, irrelevant predictors are gradually dropped, leaving only the most predictive variables, such as interest rates or industrial production. This is precisely what the coefficient path graph demonstrates—Lasso narrowing down to the strongest signals as the regularization penalty grows.
            ''')
        ],
    )
