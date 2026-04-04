---
name: mfe-mapping
description: "Functions, categories, and information. How mathematical objects relate to each other — morphisms, entropy, signal processing."
user-invocable: false
allowed-tools: Read Grep Glob
metadata:
  extensions:
    gsd-skill-creator:
      version: 1
      createdAt: "2026-02-26"
      triggers:
        intents:
          - "function"
          - "morphism"
          - "category"
          - "functor"
          - "information"
          - "entropy"
          - "signal"
          - "probability"
          - "transform"
        contexts:
          - "mathematical problem solving"
          - "math reasoning"
---

# Mapping

## Summary

**Mapping** (Part VII: Mapping)
Chapters: 22, 23, 24, 25
Plane Position: (0.2, 0.4) radius 0.4
Primitives: 42

Functions, categories, and information. How mathematical objects relate to each other — morphisms, entropy, signal processing.

**Key Concepts:** Category, Probability Axioms, Functor, Natural Transformation, Shannon Entropy

## Key Primitives



**Category** (definition): A category C consists of a collection of objects ob(C), a collection of morphisms hom(C) between objects, an identity morphism id_A for each object A, and a composition operation that is associative and respects identities.
  - Analyzing structure-preserving maps between mathematical objects
  - Identifying universal properties in algebraic structures
  - Abstracting common patterns across different areas of mathematics

**Probability Axioms** (axiom): Kolmogorov's axioms: For a sample space Omega with sigma-algebra F, a probability measure P satisfies: (1) P(A) >= 0 for all A in F, (2) P(Omega) = 1, (3) P(union A_i) = sum P(A_i) for countably many disjoint events A_i.
  - Formalizing uncertainty in mathematical models
  - Defining the foundation for statistical inference
  - Setting up probability spaces for random experiments

**Functor** (definition): A functor F: C -> D maps objects of C to objects of D and morphisms of C to morphisms of D, preserving identity morphisms F(id_A) = id_{F(A)} and composition F(g . f) = F(g) . F(f).
  - Translating problems between different mathematical frameworks
  - Identifying when a map preserves essential structure
  - Building bridges between algebraic and geometric viewpoints

**Natural Transformation** (definition): A natural transformation eta: F => G between functors F, G: C -> D is a family of morphisms eta_A: F(A) -> G(A) for each object A in C, such that for every morphism f: A -> B in C, the diagram commutes: G(f) . eta_A = eta_B . F(f).
  - Comparing two different ways to transform mathematical structures
  - Establishing canonical relationships between functors
  - Verifying that a family of maps is independent of arbitrary choices

**Shannon Entropy** (definition): For a discrete random variable X with probability mass function P(x), the Shannon entropy is H(X) = -sum_x P(x) log_2 P(x), measuring the average information content in bits per symbol.
  - Measuring uncertainty or surprise in a random source
  - Determining minimum bits needed to encode a message
  - Quantifying information content of a probability distribution

**Fourier Transform** (definition): The Fourier transform of an integrable function f: R -> C is F{f}(xi) = integral_{-inf}^{inf} f(t) e^{-2pi i xi t} dt, mapping the function from the time domain to the frequency domain.
  - Analyzing frequency content of signals
  - Solving differential equations by transforming to the frequency domain
  - Converting between time-domain and frequency-domain representations

**Random Variable** (definition): A random variable X: Omega -> R is a measurable function from the sample space to the real numbers, assigning a numerical value to each outcome. Its distribution is characterized by the CDF F_X(x) = P(X <= x).
  - Modeling numerical outcomes of random experiments
  - Defining probability distributions over numerical values
  - Abstracting uncertain quantities for mathematical analysis

**Variance** (definition): The variance of a random variable X is Var(X) = E[(X - E[X])^2] = E[X^2] - (E[X])^2, measuring the expected squared deviation from the mean. Standard deviation sigma = sqrt(Var(X)).
  - Quantifying the spread or dispersion of a distribution
  - Assessing risk and uncertainty in financial and scientific models
  - Comparing the reliability of different estimators

**Probability Distributions** (definition): A probability distribution assigns probabilities to events. Key distributions: Binomial B(n,p) with PMF C(n,k)p^k(1-p)^{n-k}; Poisson Poi(lambda) with PMF e^{-lambda}lambda^k/k!; Normal N(mu,sigma^2) with PDF (1/(sigma*sqrt(2pi)))exp(-(x-mu)^2/(2sigma^2)).
  - Modeling specific types of random phenomena with parametric families
  - Computing probabilities for binomial experiments, rare events, or measurement errors
  - Selecting appropriate statistical models for data

**Joint Probability Distribution** (definition): The joint distribution of random variables X, Y is P(X in A, Y in B) for all measurable sets A, B. For continuous variables, the joint density f_{X,Y}(x,y) satisfies P(X in A, Y in B) = integral_A integral_B f(x,y) dy dx.
  - Modeling relationships between multiple random variables
  - Computing conditional distributions and independence properties

## Composition Patterns

- Category + foundations-group-definition -> Group as a single-object category where all morphisms are invertible (parallel)
- Functor + mapping-functor -> Composite functor G . F: C -> E (sequential)
- Natural Transformation + mapping-functor -> Whiskered natural transformation (horizontal composition) (nested)
- Yoneda Lemma + mapping-category -> Embedding of any category into its presheaf category (Yoneda embedding) (sequential)
- Adjunction + foundations-group-definition -> Free-forgetful adjunction between groups and sets (parallel)
- Monad + mapping-category -> Kleisli category for sequential composition of effectful computations (sequential)
- Universal Property + foundations-group-definition -> Characterization of free groups via universal property (sequential)
- Limits and Colimits + foundations-set-union -> Products, coproducts, equalizers, coequalizers in Set (parallel)
- Shannon Entropy + mapping-probability-axioms -> Entropy of joint distributions and conditional entropy (sequential)
- Mutual Information + mapping-shannon-entropy -> Data processing inequality: I(X;Z) <= I(X;Y) when X->Y->Z form a Markov chain (sequential)

## Cross-Domain Links

- **structure**: Compatible domain for composition and cross-referencing
- **foundations**: Compatible domain for composition and cross-referencing
- **waves**: Compatible domain for composition and cross-referencing
- **unification**: Compatible domain for composition and cross-referencing
- **emergence**: Compatible domain for composition and cross-referencing
- **synthesis**: Compatible domain for composition and cross-referencing

## Activation Patterns

- function
- morphism
- category
- functor
- information
- entropy
- signal
- probability
- transform
