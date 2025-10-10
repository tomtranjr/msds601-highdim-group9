# Introduction

## 0: High-Dimensional Regression in one sentence

High-dimensional regression is what happens when you have too many variables trying to estimate too few data points ($p \geq n$), turning our nice, well-behaved OLS into a huge mess that then requires tools and techniques like Ridge, LASSO, or dimension reduction.

## 0.1: A couple more sentences about High-Dimensional Regression

High-dimensional regression is NOT a single method, rather an umbrella term for types of regression problems one may encounter during their linear regression journey, where:

$n \approx p$: the number of observations is about the same as the number of predictors.

$p \gg n$: the number of predictors is much larger than the number of observations.

## 1: Start from multiple regression

In "regular" multiple linear regression, we have:  

$y = X\beta + \varepsilon$

where:

- $y$ = response vector (length $n$),  
- $X$ = $n \times p$ design matrix (rows = observations, columns = predictors),  
- $\beta$ = coefficients,  
- $\varepsilon$ = errors.  

Usually, we are in the situation where $n \gg p$, i.e. way more observations than predictors. This is a comfortable situation! In this scenario, we can use our typical formulations as described in the next sub section.

## 1.1: “Comfortable” workflow when $n \gg p$

When we have many more observations than predictors, the **OLS** toolkit applies cleanly:

1. **Define the design matrix with intercept**
    - Let $X$ be an $n \times p$ matrix where the first column is all ones (for the intercept), followed by $X_1, \dots, X_{p-1}$.  
    - The parameter vector is $\beta = (\beta_0, \beta_1, \dots, \beta_{p-1})^\top$.

2. **OLS estimator**
    $
    \hat{\beta} = (X^\top X)^{-1} X^\top y.
    $ *If $X$ has full rank!

3. **Fitted values & residuals**
    $
    \hat y = X \hat{\beta} = X(X^\top X)^{-1} X^\top y  = Hy,
    \qquad
    e = y - \hat y = (I - H)y.
    $

4. **SSE, MSE (error variance)**
    $
    \text{SSE} = e^\top e,
    \qquad
    \hat\sigma^2 = \text{MSE} = \frac{\text{SSE}}{n - p} \quad\text{(parameters include the intercept)}.
    $

5. **Sampling variability of coefficients**
    $
    \operatorname{Var}(\hat{\beta}) = \hat\sigma^2 (X^\top X)^{-1},
    \qquad
    \text{SE}(\hat{\beta}) = \sqrt{\hat\sigma^2 \big[(X^\top X)^{-1}\big]}.
    $

---

## 2: The high-dimensional setting

Now imagine the number of predictors $p$ is **large relative to $n$**. This leads to two troublesome scenarios:  

1. **Wide data**: $p > n$.
   - Example: Gene expression: 20 patients, 10,000 genes.

2. **Comparable size**: $p \approx n$.  
   - Example: $n=100$, $p=80$. Not quite a disaster, but we definately start to get nervous.

This is what people mean by **high-dimensional regression**.

---

## 3: Why OLS breaks down

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

### Example: Why full column rank matters

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

## 4: The fix: regularization & dimension reduction

High-dimensional regression is really the art of dealing with **this problem**. Here's a non-exhaustive list of how to handle it:

- **Shrinkage (regularization):**
  - **Ridge regression**: penalize big coefficients with $\lambda \|\beta\|_2^2$. Like telling our model don't get too excited about any one variable.
  - **LASSO**: penalize with $\lambda \|\beta\|_1$, which can set coefficients exactly to 0.

- **Dimension reduction:**
  - **Principal Components Regression (PCR):** Take our correlated mess of predictors, find the main Principle Components or PCs, and regress on just the top ones.
  - **Partial Least Squares (PLS):** Like PCR, but it actually pays attention to our response when picking PCs.

---

## 5: Why this actually matters in the real world

High-dimensional problems are everywhere:

- **Genomics & bioinformatics:** You've got more genes than patients.
- **Finance:** Tons of economic indicators, not so many time points.
- **Text & NLP:** Every word in the dictionary becomes a feature.
- **Image/video ML:** Each pixel wants to be a predictor. Our smartphone photo has millions of predictors but you might only have thousands of training images.

Without high-dimensional methods, traditional regression basically gets a panic attack and starts giving you nonsense answers.

---
