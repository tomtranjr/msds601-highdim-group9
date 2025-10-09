import dash
from dash import html, dcc
from pathlib import Path

# Initialize the Dash app
app = dash.Dash(__name__)

# Markdown content (your blog)
markdown_text = Path("notes.md").read_text()

# Define the layout
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
        html.H1("High Dimensional Regression Blog", style={"textAlign": "center"}),
        html.Hr(),
        dcc.Markdown(markdown_text, mathjax=True),
    ],
)

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)