# 3: Why OLS breaks down

The textbook steps outlined in 1.1 work beautifully when $n \gg p$ mainly because the design matrix $X$ has **full column rank**, think of it like having a solid foundation. Having full rank ensures that $X^\top X$ is invertible, which in linear algebra language is "hey, we can actually solve this thing."

When $X^\top X$ is invertible, life is good:

- Our OLS solutions are **unique** (no potential for multiple-choice answers)
- Our variance estimates are **well-defined** (we actually know how confident to be)
- Everything works like it should in the statistics textbooks

But here's where things get weird. As $n$ approaches $p$ (Our data points start running out), or when $p \gg n$ (the "more variables than observations" situation), $X^\top X$ becomes **singular or nearly singular**.

**Our nice, well-behaved mathematical foundation bursts into flames.**

When this happens, all those elegant formulas and "nice properties" we learned in linear regression essentially throw in the towel and walk away. Our unique solutions? Gone. Our reliable variance estimates? Also gone!

If $p > n$, i.e. we have a wide $X$ matrix, then $X^TX$ is **not invertible**. That means the OLS estimator  

$$
\hat{\beta} = (X^\top X)^{-1} X^\top y
$$

doesn't even exist. It's like trying to divide by zero! The math essentially gives up and walks away. There are infinitely many solutions that fit the training data perfectly, which initially seems great until we realize it's actually terrible because this means we have overfit on our data!

## Example: Why full column rank matters

Suppose  
$$
X =
\begin{bmatrix}
1 & 2 \\
3 & 4 \\
5 & 6
\end{bmatrix}
$$

This matrix has **2 columns** and **3 rows** ($n > p$), and its columns are linearly independent.  

Then,
$$
X^\top X =
\begin{bmatrix}
35 & 44 \\
44 & 56
\end{bmatrix}
$$

Since $\det(X^\top X) = 24 \neq 0$, $X^\top X$ is **invertible**, meaning OLS works perfectly.

---

Now imagine we have a **wide** matrix ($p > n$):
$$
X =
\begin{bmatrix}
1 & 2 & 3 \\
4 & 5 & 6
\end{bmatrix}
$$

Here the columns are linearly dependent (too many predictors, not enough data).

$$
X^\top X =
\begin{bmatrix}
17 & 22 & 27 \\
22 & 29 & 36 \\
27 & 36 & 45
\end{bmatrix}
$$

and $\det(X^\top X) = 0$, so it’s **not invertible**, no unique OLS solution exists.

Even when $p \approx n$, OLS solutions technically exist but a couple of issues:  

- **Overfit**: the model memorized the training data, but has zero clue about new data.
- **Unstable**: change one data point and our coefficients fluctuate like crazy.  

This is why high-dimensional problems aren't just "regular regression but harder". Instead, they're a completely different problem that requires a completely different tool set.

---
