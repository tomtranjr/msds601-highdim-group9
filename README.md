# msds601-highdim-group9

Interactive Plotly Dash experience that walks through the concepts, intuition, and tooling for high-dimensional regression. The site blends live Markdown notes with reusable Dash components that demonstrate phenomena such as full-rank design matrices, LASSO selection, and economic intuition.

## Highlights

- **Live-updating notes** sourced from modular Markdown files under `notes/`.
- **Interactive demos** inside `components/` showing LASSO paths, rank diagnostics, and regression workflows.
- **Unified styling** via `assets/styles.css` and shared design tokens in `theme.py`.
- **Synthetic-data notebooks** (`*.ipynb`) that back up the narratives with exploratory work.

## Repository Layout

- `main.py` – Dash entry point that assembles Markdown sections and interactive components.
- `assets/styles.css` – Global styling (including smooth scrolling) loaded automatically by Dash.
- `theme.py` – Centralized color palette used across layouts.
- `components/` – Modular Dash components (`table_of_contents.py`, `full_rank_component.py`, `lasso_component.py`, etc.).
- `notes/` – Sectioned Markdown content (`00_intro.md`, `03_ols_breakdown.md`, `references.md`, `contributors.md`, …).
- `requirements.txt` / `pyproject.toml` – Locked dependencies (generated with `uv`).
- `Eames_lasso_working.ipynb`, `Niki_Project_linear.ipynb` – Supporting exploratory notebooks.
- `uv.lock` – Deterministic dependency lockfile.

## Getting Started (via `uv`)

[`uv`](https://github.com/astral-sh/uv) provides fast env/dep management.

1. **Create the virtual environment**

   ```bash
   uv venv
   ```

2. **Activate it**
   ```bash
   source .venv/bin/activate      # macOS/Linux
   # or
   .venv\Scripts\activate         # Windows PowerShell
   ```

3. **Install dependencies**

   ```bash
   uv pip install -r requirements.txt
   ```

4. **Run the Dash app**

   ```bash
   uv run python main.py
   ```

   Open `http://127.0.0.1:8050/` in your browser. Markdown edits refresh automatically every 2 seconds.

## Editing Content & Components

- **Markdown notes** live in `notes/`. Adding a new file? Append it to `_SECTION_FILES` in `main.py` and call `render_section("your_file.md")`.
- **Interactive modules** belong in `components/` and should follow the `make_<name>_component` pattern with scoped callbacks (see `full_rank_component.py`).
- **Styling tweaks** go in `assets/styles.css`; Dash reloads the file on change.

## Notebooks & Analysis

Exploratory notebooks remain available:
```bash
uv run jupyter notebook
```
Use them to prototype experiments or generate figures that feed back into the app.

Enjoy exploring high-dimensional regression! Feel free to open issues or PRs with improvements or new demos.
