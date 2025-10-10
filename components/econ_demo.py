# econometrics_component.py
import numpy as np
from sklearn.linear_model import LinearRegression
from dash import html, dcc
import plotly.graph_objects as go

def make_econ_component(app, uid="econ", *, n=50, seed=42):
    """
    Returns a namespaced, self-contained Dash component that:
      - generates data (inflation, gdp_growth, unemployment),
      - fits simple and multiple linear regressions,
      - shows a Plotly scatter with fitted line,
      - prints coefficients below the plot.

    Use: app.layout = html.Div([ make_regression_component(app, uid="econ1") ])
    """

    # ---------------------------
    # 1) Generate data (same logic as your snippet)
    # ---------------------------
    rng = np.random.default_rng(seed)
    inflation = rng.random((n, 1)) * 10                    # 0..10
    gdp_growth = rng.random((n, 1)) * 8 - 2                # -2..6
    noise = rng.standard_normal(n) * 0.5
    unemployment = 6 + 0.5*inflation.flatten() - 0.7*gdp_growth.flatten() + noise

    # ---------------------------
    # 2) Fit regressions
    # ---------------------------
    # Simple: Unemployment ~ Inflation
    model_simple = LinearRegression()
    model_simple.fit(inflation, unemployment)

    x_line = np.linspace(0, 10, 100).reshape(-1, 1)
    y_line = model_simple.predict(x_line)

    # Multiple: Unemployment ~ Inflation + GDP Growth
    X_multi = np.hstack([inflation, gdp_growth])
    model_multi = LinearRegression()
    model_multi.fit(X_multi, unemployment)

    # ---------------------------
    # 3) Build Plotly figure
    # ---------------------------
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=inflation.flatten(),
        y=unemployment,
        mode="markers",
        name="Data points"
    ))
    fig.add_trace(go.Scatter(
        x=x_line.flatten(),
        y=y_line,
        mode="lines",
        name="Fitted line"
    ))
    fig.update_layout(
        title="Simple Linear Regression: Unemployment ~ Inflation",
        xaxis_title="Inflation Rate (%)",
        yaxis_title="Unemployment Rate (%)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=40, r=20, t=60, b=40),
    )

    # ---------------------------
    # 4) Format outputs
    # ---------------------------
    simple_txt = (
        f"Simple regression results:\n"
        f"Intercept (β0): {model_simple.intercept_:.2f}\n"
        f"Slope for Inflation (β1): {model_simple.coef_[0]:.2f}"
    )
    multi_txt = (
        f"Multiple regression results:\n"
        f"Intercept (β0): {model_multi.intercept_:.2f}\n"
        f"Slope for Inflation (β1): {model_multi.coef_[0]:.2f}\n"
        f"Slope for GDP Growth (β2): {model_multi.coef_[1]:.2f}"
    )

    # ---------------------------
    # 5) Return namespaced component
    # ---------------------------
    return html.Div(
        id=f"{uid}-wrap",
        children=[
            html.H1('Why This Matters Today'),
            html.P("""
High-dimensional regression is central in many fields:\n
Genomics: finding key genes among thousands of measurements.\n
Finance: forecasting outcomes like unemployment with many indicators.\n
Image and speech recognition: working with pixel-level data where p >> n.\n
Recommendation systems: filtering huge user–item datasets.\n
In all of these areas, being able to identify the few predictors that matter is essential. This is why Lasso regression has become a cornerstone of high-dimensional analysis. It connects classical regression ideas to the demands of today’s big data world

            """),
            html.H3("Econometrics Demo", style={"textAlign": "center", "marginBottom": "0.4rem"}),
            html.P(
                "Scatter of unemployment vs inflation with the OLS fitted line; "
                "coefficients shown below (multiple regression includes GDP growth).",
                style={"textAlign": "center", "marginTop": 0, "marginBottom": "1rem"}
            ),
            dcc.Graph(id=f"{uid}-fig", figure=fig, style={"maxWidth": 800, "margin": "0 auto"}),
            html.Pre(simple_txt, id=f"{uid}-simple", style={"whiteSpace": "pre-wrap", "fontSize": "0.95rem"}),
            html.Pre(multi_txt, id=f"{uid}-multi", style={"whiteSpace": "pre-wrap", "fontSize": "0.95rem"}),
        ],
        # Inline styles + uid namespacing minimize interference from other page styles
        style={"padding": "1rem", "border": "1px solid #eee", "borderRadius": "12px", "maxWidth": "900px", "margin": "1rem auto"}
    )
