from pathlib import Path

import dash
from dash import Input, Output, dcc, html

from components.interactive1 import interactive_layout
from components.interactive2 import another_plot

app = dash.Dash(__name__)

NOTES_DIR = Path("notes")
_SECTION_FILES = [
    "01_intro.md",
    "02_ols_breakdown.md",
    "03_regularization.md",
    "references.md",
]


def read_md(filename: str) -> str:
    return (NOTES_DIR / filename).read_text(encoding="utf-8")


def render_section(filename: str) -> dcc.Markdown:
    section_id = f"md-{Path(filename).stem}"
    return dcc.Markdown(
        read_md(filename),
        id=section_id,
        mathjax=True,
    )


app.layout = html.Div(
    style={
        "margin": "auto",
        "maxWidth": "850px",
        "padding": "40px",
        "fontFamily": "Helvetica, Arial, sans-serif",
        "lineHeight": "1.6",
        "color": "#222",
    },
    children=[
        html.H1(
            "When Predictors Outnumber Data: Making Sense of High-Dimensional Regression",
            style={"textAlign": "center"},
        ),
        html.Hr(),
        # introduction
        render_section("01_intro.md"),
        interactive_layout,
        render_section("02_ols_breakdown.md"),
        another_plot,
        render_section("03_regularization.md"),
        render_section("references.md"),
        dcc.Interval(id="refresh", interval=2000),
    ],
)


@app.callback(
    [Output(f"md-{Path(filename).stem}", "children") for filename in _SECTION_FILES],
    Input("refresh", "n_intervals"),
)
def update_markdown(_):
    return [read_md(filename) for filename in _SECTION_FILES]


if __name__ == "__main__":
    app.run(debug=True)
