# 1: Start from multiple regression

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
