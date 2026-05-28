---
name: mcmc-sampling-stan
description: Guide for performing Markov Chain Monte Carlo (MCMC) sampling using RStan or PyStan. This skill should be used when implementing Bayesian statistical models, fitting hierarchical models, working with Stan modeling language, or running MCMC diagnostics. Applies to tasks involving posterior sampling, Bayesian inference, and probabilistic programming with Stan.
---

# MCMC Sampling with Stan

## Overview

This skill provides guidance for implementing Bayesian models and running MCMC sampling using Stan (via RStan or PyStan). It covers model specification, prior implementation, sampling configuration, and critical diagnostic checks that must be performed to validate results.

## Workflow

### Phase 1: Environment Setup

Before writing any Stan code:

1. **Verify Stan installation and version**
   - Check that the required version of RStan/PyStan is installed
   - RStan requires a C++ toolchain; verify compilation works before proceeding
   - For RStan: Check with `packageVersion("rstan")` and test compilation with a simple model

2. **Check system dependencies first**
   - Stan requires compilation; missing system libraries cause cryptic errors
   - On Linux: Ensure `g++`, `make`, and development libraries are installed
   - On macOS: Xcode command line tools required
   - Verify the toolchain before attempting package installation

3. **Common installation pitfalls**
   - R's `install.packages()` does not accept a `version` parameter for CRAN packages
   - To install a specific version, use `remotes::install_version()` or install from source
   - RStan compilation can fail silently; always test with a minimal model first

### Phase 2: Data Exploration

Before implementing the model:

1. **Analyze the data structure**
   - Examine dimensions: number of observations, groups, variables
   - Check for missing values, zeros, or extreme values
   - Understand the range and distribution of variables

2. **Identify potential issues**
   - Zero counts in binomial/Poisson models (valid but worth noting)
   - Extreme values that might cause numerical issues
   - Small sample sizes that may not support complex models

3. **Document data characteristics**
   - Record any data-specific considerations that affect model specification
   - Note whether the data provides enough information for the chosen priors

### Phase 3: Model Implementation

When writing the Stan model:

1. **Prior specification**
   - Translate mathematical priors correctly to Stan syntax
   - Use `target +=` for log-probability contributions (e.g., `target += -2.5 * log(alpha + beta)` for p(α,β) ∝ (α+β)^(-5/2))
   - Document the reasoning behind prior choices

2. **Parameter constraints**
   - Use appropriate bounds: `real<lower=0>`, `real<lower=0, upper=1>`, etc.
   - Consider whether improper priors will yield proper posteriors given the data
   - Add small lower bounds if numerical stability is a concern (e.g., `real<lower=0.001>`)

3. **Model block structure**
   - Follow Stan's block order: data, transformed data, parameters, transformed parameters, model, generated quantities
   - Keep transformations in appropriate blocks for efficiency

4. **Numerical stability considerations**
   - Improper priors (e.g., (α+β)^(-5/2)) may not integrate to finite values
   - The data must provide sufficient information for posterior propriety
   - Consider adding soft constraints if parameters can drift to extreme values

### Phase 4: Sampling Configuration

Configure MCMC sampling appropriately:

1. **Iteration and warmup settings**
   - RStan default: half of `iter` for warmup, half for sampling
   - Explicitly set `warmup` parameter for clarity
   - Example: `iter = 100000` with default settings = 50,000 warmup + 50,000 samples per chain

2. **Control parameters**
   - `adapt_delta`: Increase (e.g., 0.95 or 0.99) if divergent transitions occur
   - `max_treedepth`: Increase (e.g., 15) if hitting tree depth limits
   - Document why non-default values are chosen

3. **Chain configuration**
   - Multiple chains (typically 4) enable convergence diagnostics
   - Set seeds for reproducibility
   - Consider computational resources vs. chain count tradeoffs

### Phase 5: Diagnostic Checks (CRITICAL)

**Never skip diagnostics.** Successful sampling completion does not guarantee valid results.

1. **Convergence diagnostics (MANDATORY)**
   - **R-hat (Gelman-Rubin statistic)**: Must be < 1.01 for all parameters
   - **Effective Sample Size (ESS)**: Should be > 400 for reliable estimates; > 100 minimum
   - Check both bulk-ESS and tail-ESS

2. **Sampling diagnostics (MANDATORY)**
   - **Divergent transitions**: Must be 0; any divergences indicate model problems
   - **Tree depth**: Check for max treedepth warnings
   - **Energy diagnostics**: E-BFMI should be > 0.3

3. **Visual diagnostics (recommended)**
   - Trace plots: Chains should mix well ("fuzzy caterpillar" appearance)
   - Density plots: Posteriors should be smooth and reasonable
   - Pairs plots: Check for problematic correlations

4. **How to access diagnostics in RStan**
   ```r
   # Summary with R-hat and ESS
   print(fit, pars = c("alpha", "beta"))

   # Check for divergences
   sampler_params <- get_sampler_params(fit, inc_warmup = FALSE)
   sum(sapply(sampler_params, function(x) sum(x[, "divergent__"])))

   # Check tree depth
   sum(sapply(sampler_params, function(x) sum(x[, "treedepth__"] >= 15)))
   ```

5. **Interpreting diagnostic failures**
   - Divergences: Reparameterize model or increase `adapt_delta`
   - Low ESS: Run longer chains or reparameterize
   - High R-hat: Chains haven't converged; run longer or check model specification

### Phase 6: Results Extraction

After diagnostics pass:

1. **Extract posterior summaries**
   - Posterior means, medians, and credible intervals
   - Standard deviations and quantiles

2. **Validate against expectations**
   - Compare to known results for standard models (e.g., Bayesian Data Analysis examples)
   - Check that posteriors are in reasonable ranges
   - Verify that constraints are respected

3. **Output file handling**
   - Use appropriate functions for clean file output
   - In R: `writeLines()` or `cat()` with explicit formatting
   - Avoid artifacts like trailing newlines or formatting characters

## Common Pitfalls

### Installation Issues
- Attempting to specify version in `install.packages()` (use `remotes::install_version()` instead)
- Missing C++ toolchain or system libraries
- Not testing compilation before running full models

### Model Specification Errors
- Incorrect translation of mathematical priors to Stan code
- Missing or incorrect parameter bounds
- Not considering posterior propriety with improper priors

### Sampling Problems
- Not explicitly setting warmup period
- Using default control parameters when model requires tuning
- Running insufficient iterations for convergence

### Diagnostic Omissions
- Assuming successful sampling means valid results
- Not checking R-hat, ESS, or divergent transitions
- Ignoring warnings about tree depth or energy diagnostics

### Output Errors
- Bash command parsing issues with redirection operators in R scripts
- Not verifying output file format and content
- Missing error handling for file operations

## Verification Checklist

Before considering the task complete, verify:

- [ ] Stan/RStan/PyStan version matches requirements
- [ ] Model compiles without errors
- [ ] Priors are correctly implemented (verify mathematical translation)
- [ ] Parameter bounds are appropriate
- [ ] Sampling completes without errors
- [ ] R-hat < 1.01 for all parameters
- [ ] ESS > 400 (or reasonable for the application)
- [ ] Zero divergent transitions
- [ ] No max treedepth warnings (or addressed if present)
- [ ] Posterior summaries are reasonable
- [ ] Output files are correctly formatted

## References

For detailed information on Stan diagnostics and model reparameterization, consult:
- `references/stan_diagnostics.md` - Detailed diagnostic interpretation guide
