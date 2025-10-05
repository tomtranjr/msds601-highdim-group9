# msds601-highdim-group9

## Project Overview
This repository houses the MSDS 601 High-Dimensional Regression group project. The work focuses on comparing regularization techniques (Ridge, LASSO) and related linear modeling strategies in settings where the number of predictors approaches or exceeds the number of observations. Exploratory notebooks walk through data preparation, model fitting, diagnostics, and visualization, while `notes.md` captures supporting theory and intuition for high-dimensional regression.

## Repository Structure
- `Eames_lasso_working.ipynb` – exploratory notebook experimenting with LASSO, Ridge, and supporting visualizations.
- `Niki_Project_linear.ipynb` – complementary notebook covering linear modeling workflow and plotting utilities.
- `notes.md` – theory notes summarizing key ideas and formulas for high-dimensional regression.
- `test.py` – simple smoke script; extend or replace with project-specific tests.
- `requirements.txt` – Python dependencies required by the notebooks and supporting scripts.

## Environment Setup with uv
[`uv`](https://github.com/astral-sh/uv) is a fast Python package and environment manager. Follow the steps below to create a reproducible environment:

1. **Install uv** (if not already available). Follow the latest instructions from the uv documentation for your platform.
2. **Create a dedicated virtual environment** in the project directory:
   ```bash
   uv venv
   ```
3. **Activate the environment**:
   ```bash
   source .venv/bin/activate            # macOS/Linux
   # or
   .venv\\Scripts\\activate            # Windows PowerShell
   ```
4. **Install dependencies**:
   ```bash
   uv pip install -r requirements.txt
   ```

## Working with the Project
- **Launch Jupyter** to explore the notebooks:
  ```bash
  uv run jupyter notebook
  ```
  Open `Eames_lasso_working.ipynb` or `Niki_Project_linear.ipynb` inside the browser to reproduce the analyses or continue iterating.

- **Run helper scripts** such as `test.py` inside the managed environment:
  ```bash
  uv run python test.py
  ```

- **Add new packages** as work evolves:
  ```bash
  uv pip install <package-name>
  uv pip freeze > requirements.txt
  ```
  Commit the updated `requirements.txt` so collaborators stay in sync.

## Additional Notes
- `notes.md` is a living document—expand it with insights, references, or derivations uncovered during research.
- Keep notebooks tidy by clearing outputs before committing (`jupyter nbconvert --clear-output` can help).
- When collaborating, sync frequently (`git pull`) and resolve notebook merge conflicts promptly—consider using tools like `nbdime` in the uv environment if conflicts arise.

Happy modeling!
