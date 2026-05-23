---
name: mathematical-modeling
description: Real-world problem formulation, mathematical abstraction, and applied mathematics for translating between practical problems and mathematical frameworks. Covers the modeling cycle (problem identification, assumptions, formulation, analysis, validation, interpretation), Polya's framework adapted for modeling, common model types (linear, exponential, logistic, periodic, power-law), dimensional analysis (Buckingham Pi theorem), optimization (linear programming, gradient descent, constraint satisfaction), probability models (Markov chains, queuing theory, Monte Carlo simulation), statistical modeling (regression, hypothesis testing, model selection), model criticism (overfitting, underfitting, sensitivity analysis), and real-world case studies. Use when formulating mathematical models, performing dimensional analysis, optimizing systems, running simulations, or evaluating model validity.
type: skill
category: math
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/math/mathematical-modeling/SKILL.md
superseded_by: null
---
# Mathematical Modeling

Mathematical modeling is the art and science of translating real-world phenomena into mathematical language, analyzing the resulting mathematical system, and translating the conclusions back into practical insights. It is applied mathematics at its most consequential — the bridge between abstract theory and physical, biological, economic, and engineering reality. This skill covers the complete modeling cycle, standard model types, optimization, probabilistic models, and the critical practice of model criticism.

**Agent affinity:** euler (analysis, differential equations, optimization), polya (problem-solving strategy, heuristic reasoning)

**Concept IDs:** math-functions, math-correlation-causation, math-descriptive-statistics, math-probability-foundations

## Part I — The Modeling Cycle

### The Six-Stage Framework

Mathematical modeling is iterative, not linear. The cycle repeats until the model is fit for purpose.

```
1. PROBLEM IDENTIFICATION
   What question are we answering? What decisions depend on the answer?
   
2. ASSUMPTIONS
   What simplifications make the problem tractable? What is ignored?
   
3. FORMULATION
   Translate assumptions into equations, inequalities, or algorithms.
   
4. ANALYSIS
   Solve the mathematical system (exactly or numerically).
   
5. VALIDATION
   Compare model predictions against real data. Quantify error.
   
6. INTERPRETATION
   Translate mathematical conclusions into actionable real-world answers.
   Report limitations and uncertainty.
```

The most common failure mode is skipping stage 2 (assumptions) and stage 5 (validation). A model without explicit assumptions is untestable; a model without validation is fiction.

### Polya's Framework Adapted for Modeling

George Polya's *How to Solve It* (1945) provides four phases that map directly to modeling:

**1. Understand the problem.** What is known? What is unknown? What are the constraints? Draw a picture. Introduce notation. Can you restate the problem in your own words?

**2. Devise a plan.** Have you seen a similar problem? Can you solve a simpler version first? What model type fits the phenomenon? What variables matter most?

**3. Carry out the plan.** Execute the mathematical analysis. Check each step. If stuck, go back to step 2.

**4. Look back.** Is the answer reasonable? Can you verify it by a different method? Can you generalize? What are the limitations?

Polya's emphasis on looking back corresponds directly to the validation and interpretation stages. Most student modelers and many professional ones skip this step, producing models that are mathematically correct but practically useless.

## Part II — Common Model Types

### Linear Models

y = mx + b. The simplest model, appropriate when the rate of change is constant.

**When to use.** Short-term predictions, small perturbations, situations where the relationship is approximately proportional. Linear models are the first approximation to any smooth function (Taylor's theorem guarantees this locally).

**Worked example.** *A company's revenue has been $2M in 2020, $2.4M in 2021, $2.8M in 2022, $3.2M in 2023. Project revenue for 2025.*

The data increases by $0.4M/year. Model: R(t) = 2 + 0.4(t - 2020) million dollars. For 2025: R(2025) = 2 + 0.4(5) = $4M.

**Limitation.** Linear growth cannot continue indefinitely in bounded systems (market size, resource constraints). Always state the range of validity.

### Exponential Models

y = A * e^(kt). Appropriate when the rate of change is proportional to the current value: dy/dt = ky.

**When to use.** Unrestricted growth or decay: radioactive decay (k < 0), compound interest, early-stage population growth, viral spread in early phases.

**Worked example.** *A bacterial culture doubles every 3 hours starting from 500 cells. How many cells after 12 hours?*

Doubling time T = 3 hours means k = ln(2)/T = ln(2)/3. Model: N(t) = 500 * e^(t*ln(2)/3) = 500 * 2^(t/3). At t = 12: N(12) = 500 * 2^4 = 8000 cells.

### Logistic Models

y = K / (1 + A * e^(-rt)), where K is the carrying capacity.

**When to use.** Growth that saturates: population with limited resources, technology adoption (S-curve), disease spread with herd immunity. The logistic model transitions from exponential growth (small y) to saturation (y near K).

**Derivation.** The logistic ODE is dy/dt = r*y*(1 - y/K). When y << K, this is approximately dy/dt = ry (exponential). As y approaches K, the growth rate drops to zero.

**Worked example.** *A rumor spreads in a school of 1000 students. Initially 10 know it, and after 2 days 100 know it. Model the spread.*

Logistic model: N(t) = 1000 / (1 + 99*e^(-rt)). At t = 0: N(0) = 1000/100 = 10. Check. At t = 2: 100 = 1000/(1 + 99*e^(-2r)). Solve: 1 + 99*e^(-2r) = 10, so e^(-2r) = 9/99 = 1/11. Thus r = ln(11)/2 approximately 1.20.

At t = 5: N(5) = 1000/(1 + 99*e^(-6.0)) approximately 1000/(1 + 99*0.00248) approximately 1000/1.245 approximately 803 students.

### Periodic Models

y = A*sin(omega*t + phi) + C. Appropriate for oscillating phenomena.

**When to use.** Seasonal patterns (temperature, sales cycles), wave phenomena, circadian rhythms, alternating current.

**Parameters.** A = amplitude, omega = angular frequency (omega = 2*pi/period), phi = phase shift, C = vertical offset (baseline).

### Power-Law Models

y = C * x^alpha. On a log-log plot, power laws appear as straight lines with slope alpha.

**When to use.** Scaling relationships in physics (gravity: F proportional to r^(-2)), biology (metabolic rate scales as mass^(3/4), Kleiber's law), network science (degree distributions), linguistics (Zipf's law: word frequency proportional to rank^(-1)).

**Detecting power laws.** Plot log(y) vs. log(x). A linear relationship indicates a power law. However, many claimed power laws in empirical data do not survive rigorous statistical testing (Clauset, Shalizi, and Newman, 2009).

## Part III — Dimensional Analysis

### The Buckingham Pi Theorem

If a physical relationship involves n variables with k independent dimensions (length, mass, time, etc.), then the relationship can be expressed in terms of n - k dimensionless groups (Pi groups).

**Worked example.** *Find the period T of a simple pendulum.*

Variables: T (period), L (length), m (mass), g (gravitational acceleration).
Dimensions: T = [T], L = [L], m = [M], g = [L*T^(-2)].
Number of variables: n = 4. Independent dimensions: k = 3 (M, L, T).
Number of Pi groups: n - k = 1.

The single dimensionless group must be: Pi = T * sqrt(g/L) (verify: [T] * [L^(1/2) * T^(-1) * L^(-1/2)] = [T * T^(-1)] = dimensionless).

Since Pi must be a constant: T = C * sqrt(L/g). Detailed analysis (or experiment) gives C = 2*pi, yielding the familiar T = 2*pi*sqrt(L/g).

**Power of the method.** Dimensional analysis determined the functional form T proportional to sqrt(L/g) without solving any differential equation. The mass m dropped out entirely, predicting (correctly) that the period is independent of mass.

### Dimensional Homogeneity

Every valid physical equation must be dimensionally homogeneous — every term must have the same dimensions. This provides a powerful error check: if the dimensions don't match, the equation is wrong.

## Part IV — Optimization

### Linear Programming (LP)

**Standard form.** Maximize c^T * x subject to Ax <= b, x >= 0.

The feasible region is a convex polytope. The optimal solution (if it exists) occurs at a vertex. The simplex method (Dantzig, 1947) traverses vertices until optimality is reached.

**Worked example.** *A factory makes chairs ($20 profit) and tables ($30 profit). Each chair needs 2 hours of carpentry and 1 hour of finishing. Each table needs 3 hours of carpentry and 2 hours of finishing. Available: 120 hours carpentry, 80 hours finishing. Maximize profit.*

Variables: x = chairs, y = tables.
Maximize: 20x + 30y
Subject to: 2x + 3y <= 120, x + 2y <= 80, x >= 0, y >= 0.

Corner points: (0, 0) -> $0, (60, 0) -> $1200, (0, 40) -> $1200, (24, 24) -> $1200... Wait, let's compute intersections properly.

2x + 3y = 120 and x + 2y = 80. From the second: x = 80 - 2y. Substitute: 2(80 - 2y) + 3y = 120, so 160 - 4y + 3y = 120, y = 40. Then x = 80 - 80 = 0. Corner: (0, 40) -> $1200.

Check (60, 0): 2(60) = 120 <= 120, 60 <= 80. Profit = $1200.
Check (0, 40): 3(40) = 120 <= 120, 2(40) = 80 <= 80. Profit = $1200.

Multiple optima along the line segment connecting (60, 0) and (0, 40).

### Gradient Descent

For unconstrained optimization of a differentiable function f(x): iterate x_{k+1} = x_k - alpha * grad(f(x_k)), where alpha is the step size (learning rate).

**Convergence.** For convex f with Lipschitz-continuous gradient, gradient descent converges at rate O(1/k). For strongly convex f, convergence is linear (geometric).

**Step size selection.** Too large causes divergence; too small causes slow convergence. Adaptive methods (Adam, RMSProp) adjust the step size automatically.

### Constraint Satisfaction

When the problem has constraints that must be satisfied exactly (not just optimized), techniques include: Lagrange multipliers (continuous equality constraints), penalty methods (convert constraints to penalty terms in the objective), and integer programming (discrete variables).

**Lagrange multipliers.** To optimize f(x) subject to g(x) = 0, solve the system grad(f) = lambda * grad(g) and g(x) = 0.

**Worked example.** *Find the rectangle of maximum area inscribed in the ellipse x^2/4 + y^2/9 = 1.*

By symmetry, the rectangle has corners at (+/-x, +/-y) with area A = 4xy. Maximize 4xy subject to x^2/4 + y^2/9 = 1.

Lagrangian: L = 4xy - lambda(x^2/4 + y^2/9 - 1).

dL/dx = 4y - lambda*x/2 = 0 => lambda = 8y/x.
dL/dy = 4x - 2*lambda*y/9 = 0 => lambda = 18x/y.

Setting equal: 8y/x = 18x/y => 8y^2 = 18x^2 => y^2 = 9x^2/4. Substitute into constraint: x^2/4 + x^2/4 = 1 => x^2 = 2 => x = sqrt(2), y = 3/sqrt(2). Area = 4*sqrt(2)*3/sqrt(2) = 12.

## Part V — Probability Models

### Markov Chains

A Markov chain is a sequence of random variables where the future depends only on the present, not the past (the Markov property). Described by a transition matrix P where P_{ij} = probability of moving from state i to state j.

**Worked example.** *Weather model: if today is sunny, tomorrow is sunny with probability 0.8 and rainy with probability 0.2. If today is rainy, tomorrow is sunny with probability 0.4 and rainy with probability 0.6.*

Transition matrix: P = [[0.8, 0.2], [0.4, 0.6]].

Steady-state: solve pi*P = pi with sum(pi) = 1. This gives 0.8*pi_S + 0.4*pi_R = pi_S and pi_S + pi_R = 1. From the first: 0.4*pi_R = 0.2*pi_S, so pi_S = 2*pi_R. With normalization: pi_S = 2/3, pi_R = 1/3. In the long run, it's sunny 2/3 of the time.

### Queuing Theory

**M/M/1 queue.** Arrivals are Poisson (rate lambda), service times are exponential (rate mu), one server. The system is stable when rho = lambda/mu < 1.

Key results:
- Average number in system: L = rho / (1 - rho)
- Average wait time: W = 1 / (mu - lambda)
- Probability of n customers: P(n) = (1 - rho) * rho^n

**Worked example.** *A help desk receives 6 calls per hour (Poisson) and handles each in 8 minutes on average (exponential). What is the average wait time?*

lambda = 6/hour, mu = 60/8 = 7.5/hour. rho = 6/7.5 = 0.8. W = 1/(7.5 - 6) = 1/1.5 hours = 40 minutes.

### Monte Carlo Simulation

Use random sampling to estimate quantities that are difficult to compute analytically.

**Worked example.** *Estimate pi using Monte Carlo.*

Generate N random points (x, y) uniformly in the unit square [0,1] x [0,1]. Count the number M that fall inside the quarter circle x^2 + y^2 <= 1. Then pi approximately equals 4M/N.

**Convergence.** Monte Carlo estimates converge at rate O(1/sqrt(N)) — independent of dimension. This makes Monte Carlo the method of choice for high-dimensional integration where deterministic quadrature rules suffer the curse of dimensionality.

## Part VI — Statistical Modeling

### Regression

**Linear regression.** Given data points (x_i, y_i), find the line y = a + bx that minimizes the sum of squared residuals: sum(y_i - a - bx_i)^2.

The ordinary least squares (OLS) solution:
b = (n*sum(x_i*y_i) - sum(x_i)*sum(y_i)) / (n*sum(x_i^2) - (sum(x_i))^2)
a = y_bar - b*x_bar

**R-squared.** The coefficient of determination R^2 = 1 - SS_res/SS_tot measures the proportion of variance explained by the model. R^2 = 1 is a perfect fit; R^2 = 0 means the model explains nothing beyond the mean.

**Multiple regression.** y = X*beta + epsilon, where X is the design matrix. OLS solution: beta_hat = (X^T*X)^(-1) * X^T * y.

### Hypothesis Testing

**Framework.** State null hypothesis H_0 and alternative H_1. Choose significance level alpha. Compute test statistic. Compare to critical value or compute p-value. Reject H_0 if p < alpha.

**Common tests:**
- **z-test / t-test:** Compare means (z for known variance or large samples, t for unknown variance and small samples).
- **Chi-squared test:** Test independence or goodness of fit for categorical data.
- **F-test:** Compare variances or test significance of regression models.

**Critical nuance.** Statistical significance (p < 0.05) does not imply practical significance. A large enough sample will detect trivially small effects. Always report effect sizes alongside p-values.

### Model Selection

**Bias-variance tradeoff.** Simple models (high bias, low variance) underfit; complex models (low bias, high variance) overfit. The optimal model balances both.

**Information criteria:**
- **AIC (Akaike):** AIC = 2k - 2*ln(L), where k = number of parameters, L = maximum likelihood. Penalizes complexity.
- **BIC (Bayesian):** BIC = k*ln(n) - 2*ln(L). Penalizes complexity more heavily than AIC for large n.

Lower AIC/BIC is better. These criteria enable principled model comparison without cross-validation.

## Part VII — Model Criticism

### Overfitting

A model that fits the training data perfectly but fails on new data is overfitting. Symptoms: high R^2 on training data, poor prediction on test data, coefficients with physically implausible magnitudes.

**Remedies.** Cross-validation, regularization (ridge/lasso), simpler model specification, more data.

### Underfitting

A model that is too simple to capture the real pattern. Symptoms: poor fit on both training and test data, systematic residual patterns.

**Remedies.** More complex model, additional predictors, nonlinear terms, interaction terms.

### Sensitivity Analysis

Vary each input parameter by a reasonable range and observe the change in model output. Parameters to which the output is highly sensitive require careful estimation; parameters to which it is insensitive can be set to rough estimates.

**One-at-a-time (OAT).** Vary one parameter while holding others fixed. Simple but misses interactions.

**Global sensitivity analysis.** Sobol indices decompose output variance into contributions from each input and their interactions. More informative but computationally expensive.

### Model Validation Checklist

- [ ] Are the assumptions explicit and defensible?
- [ ] Does the model reproduce known results in limiting cases?
- [ ] Has the model been tested against held-out data?
- [ ] Are residuals approximately random (no systematic pattern)?
- [ ] Have key parameters been subjected to sensitivity analysis?
- [ ] Are the conclusions robust to reasonable changes in assumptions?
- [ ] Are the limitations clearly stated?

## When to Use This Skill

- Formulating a mathematical model for a real-world problem
- Performing dimensional analysis to identify functional forms
- Optimization (LP, gradient descent, constrained optimization)
- Probabilistic modeling (Markov chains, queuing, simulation)
- Statistical analysis (regression, hypothesis testing, model selection)
- Evaluating model quality (overfitting, sensitivity, validation)

## When NOT to Use This Skill

- For pure algebraic manipulation — use algebraic-reasoning
- For proof writing or verification — use proof-techniques
- For pure geometry problems — use geometric-intuition
- For sequence analysis or conjecture generation — use pattern-recognition
- For calculus mechanics (integration techniques, series convergence) — use numerical-analysis

## Cross-References

- **euler agent:** Differential equations, optimization, and analytic methods that drive model analysis. Named for Leonhard Euler, who modeled everything from fluid flow to the motion of the moon.
- **polya agent:** Problem-solving heuristics that guide model formulation. Named for George Polya, whose *How to Solve It* is the foundational text on mathematical problem-solving strategy.
- **numerical-analysis skill:** Computational methods (Newton's method, Euler method, Simpson's rule) used to solve models that lack closed-form solutions.
- **algebraic-reasoning skill:** Symbolic manipulation for deriving model solutions.
- **pattern-recognition skill:** Identifying model types from data patterns.

## References

- Polya, G. (1945). *How to Solve It*. Princeton University Press.
- Strogatz, S. H. (2018). *Nonlinear Dynamics and Chaos*. 2nd edition. CRC Press.
- Giordano, F. R., Fox, W. P., & Horton, S. B. (2013). *A First Course in Mathematical Modeling*. 5th edition. Brooks/Cole.
- Dantzig, G. B. (1963). *Linear Programming and Extensions*. Princeton University Press.
- Boyd, S., & Vandenberghe, L. (2004). *Convex Optimization*. Cambridge University Press. (Free online.)
- Gelman, A., Carlin, J. B., Stern, H. S., Dunson, D. B., Vehtari, A., & Rubin, D. B. (2013). *Bayesian Data Analysis*. 3rd edition. CRC Press.
- Clauset, A., Shalizi, C. R., & Newman, M. E. J. (2009). "Power-law distributions in empirical data." *SIAM Review*, 51(4), 661-703.
- Buckingham, E. (1914). "On physically similar systems; illustrations of the use of dimensional equations." *Physical Review*, 4(4), 345-376.
