from pathlib import Path

import dash
from dash import Input, Output, dcc, html

from components.econ_demo import make_econ_component
from components.full_rank_component import make_full_rank_component
from components.interactive1 import interactive_layout
from components.interactive2 import another_plot
from components.lasso_component import make_lasso_component
from theme import COLORS

app = dash.Dash(__name__)

NOTES_DIR = Path("notes")

_SECTION_FILES = [
    "00_intro.md",
    "01_startMLR.md",
    "02_highdim_setting.md",
    "03_ols_breakdown.md",
    "04_regularization_dimred.md",
    "05_why_matters.md",
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


PAGE_STYLE = {
    "margin": "auto",
    "maxWidth": "850px",
    "padding": "40px",
    "fontFamily": "Helvetica, Arial, sans-serif",
    "lineHeight": "1.6",
    "color": COLORS["text_black"],
    "backgroundColor": COLORS["surface_white"],
}


app.layout = html.Div(
    style=PAGE_STYLE,
    children=[
        html.H1(
            "When Predictors Outnumber Data: Making Sense of High-Dimensional Regression",
            style={"textAlign": "center"},
        ),
        html.Hr(),
        # introduction
        render_section("00_intro.md"),
        render_section("01_startMLR.md"),
        render_section("02_highdim_setting.md"),
        render_section("03_ols_breakdown.md"),
        make_full_rank_component(app, uid="fullrank-demo"),
        render_section("04_regularization_dimred.md"),
        make_econ_component(app, uid="econ-demo"),
        make_lasso_component(app, uid="lasso-demo"),
        render_section("05_why_matters.md"),
        render_section("references.md"),
        # interactive_layout,
        # another_plot,
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
