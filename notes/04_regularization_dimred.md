# 4: The fix: regularization & dimension reduction

High-dimensional regression is really the art of dealing with **this problem**. Here's a non-exhaustive list of how to handle it:

- **Shrinkage (regularization):**
  - **Ridge regression**: penalize big coefficients with $\lambda \|\beta\|_2^2$. Like telling our model don't get too excited about any one variable.
  - **LASSO**: penalize with $\lambda \|\beta\|_1$, which can set coefficients exactly to 0.

- **Dimension reduction:**
  - **Principal Components Regression (PCR):** Take our correlated mess of predictors, find the main Principle Components or PCs, and regress on just the top ones.
  - **Partial Least Squares (PLS):** Like PCR, but it actually pays attention to our response when picking PCs.

---
