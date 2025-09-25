# Notes on High Dimensional Regression

## 0: What is High Dimensional Regression in one line?

High-dimensional regression is what happens when you have way too many variables chasing too few data points ($p \geq n$), turning our nice, well-behaved OLS into a hot mess that needs tools and techniques like Ridge, LASSO, or dimension reduction to restore some semblance of sanity.

### A couple more lines

High-dimensional regression is NOT a single method, rather an umbrella term for types of regression problems one may encounter where:

$n \approx p$: the number of observations is about the same as the number of predictors.

$p \gg n$: the number of predictors is much larger than the number of observations.

## 1: Start from multiple regression
In "regular" multiple linear regression, we have:  

$y = X\beta + \varepsilon$

where  
- $y$ = response vector (length $n$),  
- $X$ = $n \times p$ design matrix (rows = observations, columns = predictors),  
- $\beta$ = coefficients,  
- $\varepsilon$ = errors.  

Usually, we assume $n \gg p$: way more observations than predictors. This is like having plenty of witnesses to back up our story (and life is all fine and good)! In this scenario, we can use our typical formulations as described in the next sub section.

## 1.1: “Comfortable” workflow when $n \gg p$

When you have many more observations than predictors, the **OLS** toolkit applies cleanly:

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
Now imagine the number of predictors $p$ is **large relative to $n$**. It's like trying to solve a jigsaw puzzle where you have more edge pieces than actual puzzle pieces. Two nightmare scenarios:  

1. **Wide data**: $p > n$. 
   - Example: Gene expression: 20 patients, 10,000 genes. (Good luck with that!)

2. **Comparable size**: $p$ is breathing down $n$'s neck.  
   - Example: $n=100$, $p=80$. Not quite a disaster, but definitely sweaty palms territory.

This is what people mean by **high-dimensional regression**, essential statistical hell.

---

## 3: Why OLS breaks down, the Math Stops Playing Nice
The textbook steps outlined in 1.1 work beautifully when $n \gg p$ mainly because the design matrix $X$ has **full column rank**, think of it like having a solid foundation. Having full rank ensures that $X^\top X$ is invertible, which is linear algebra math speak for "hey, we can actually solve this thing."

When $X^\top X$ is invertible, life is good:
- Our OLS solutions are **unique** (no potential for multiple-choice answers)
- Our variance estimates are **well-defined** (we actually know how confident to be)
- Everything works like it should in the statistics textbooks

But here's where things get weird. As $n$ approaches $p$ (Our data points start running out), or when $p \gg n$ (the dreaded "more variables than observations" nightmare), $X^\top X$ becomes **singular or nearly singular**.

Our nice, well-behaved mathematical foundation bursts into flames and the fire alarms start sounding. It's like trying to balance a house on a foundation made of jello. It's technically possible in theory, practically a disaster waiting to happen.

When this happens, all those elegant formulas and "nice properties" we learned in linear regression essentially throw in the towel and walk away. Our unique solutions? Gone. Our reliable variance estimates? Goodbye!

If $p > n$, then $X^TX$ is **not invertible**. That means the OLS estimator  

$ \hat{\beta} = (X^\top X)^{-1} X^\top y $

doesn't even exist. It's like trying to divide by zero! The math just throws up its hands and walks away. There are infinitely many solutions that fit the training data perfectly, which sounds great until you realize it's actually terrible.

Even when $p \approx n$, OLS solutions technically exist but they're about as reliable as weather forecasts:  
- **Overfit like crazy**: the model memorized the training data like a parrot, but has zero clue about new data.  
- **Unstable as a house of cards**: change one data point and our coefficients do backflips.  

Think of it like this: if you have 100 data points but 80 variables, you're essentially asking 80 different stories to explain the same 100 facts. Everyone's going to have an opinion, and most of them will be wrong.

This is why high-dimensional problems aren't just "regular regression but harder". Instead, they're a completely different beast that requires a completely different tool set.

---

## 4: The fix: regularization & dimension reduction
High-dimensional regression is really the art of **taming this beast**. Here's how the real experts handle it:

- **Shrinkage (regularization):** Put our coefficients on a diet.
  - **Ridge regression**: penalize big coefficients with $\lambda \|\beta\|_2^2$. Like telling our model "hey, don't get too excited about any one variable."
  - **LASSO**: penalize with $\lambda \|\beta\|_1$, which can set coefficients exactly to 0. It's the Marie Kondo of regression where if a variable doesn't spark joy (or significance), it gets tossed.

- **Dimension reduction:** Can't handle the chaos? Make it simpler.
  - **Principal Components Regression (PCR):** Take our correlated mess of predictors, find the main "themes" (aka Principle Components or PCs), and regress on just the top hits.
  - **Partial Least Squares (PLS):** Like PCR, but it actually pays attention to our response when picking themes.

- **Variable screening:** The bouncer approach. Kick out the troublemaker predictors before they cause problems.

- **Bayesian priors:** Give our coefficients some life advice upfront (like "try to stay small").

---

## 5: Why this actually matters in the real world
High-dimensional problems are everywhere:

- **Genomics & bioinformatics:** You've got more genes than patients, which is like trying to understand a person's life story from 20 Facebook posts but having access to their entire DNA.
- **Finance:** Tons of economic indicators, not so many time points.
- **Text & NLP:** Every word in the dictionary becomes a feature.
- **Image/video ML:** Each pixel wants to be a predictor. Our smartphone photo has millions of predictors but you might only have thousands of training images.

Without high-dimensional methods, traditional regression basically has a nervous breakdown and starts giving you nonsense answers.

---
