# When OLS Starts To Break Down

## Multicollinearity

When predictors are correlated, the columns of $X$ lose independence. The variance of $\hat{\beta}$ inflates, and model interpretation becomes unstable.

## Leverage Points

High leverage points can disproportionately influence the fitted hyperplane. In high dimensions, leverage becomes easier to obtain even by chance.

## Overfitting

As dimensionality increases, the hypothesis space explodes. Minimizing training error alone often leads to memorization instead of generalization.
