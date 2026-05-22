---
name: mathnet
description: >
  Guidance for Math.NET Numerics library for .NET.
  USE FOR: linear algebra (matrices, vectors, decompositions), statistics (descriptive, distributions, regression), numerical integration, interpolation, random number generation, signal processing.
  DO NOT USE FOR: symbolic math (use AngouriMath), expression parsing from strings (use NCalc), machine learning models (use ML.NET), GPU-accelerated computation.
license: MIT
metadata:
  displayName: Math.NET
  author: "Tyler-R-Kendrick"
  version: "1.0.0"
compatibility:
  - claude
  - copilot
  - cursor
references:
  - title: "Math.NET Numerics Documentation"
    url: "https://numerics.mathdotnet.com/"
  - title: "Math.NET Numerics GitHub Repository"
    url: "https://github.com/mathnet/mathnet-numerics"
  - title: "MathNet.Numerics NuGet Package"
    url: "https://www.nuget.org/packages/MathNet.Numerics"
---

# Math.NET Numerics

## Overview

Math.NET Numerics is the numerical computing foundation for .NET. It provides types and algorithms for linear algebra (dense and sparse matrices, vectors, decompositions), probability distributions, descriptive and inferential statistics, numerical integration, interpolation, curve fitting, and random number generation.

Math.NET Numerics is written in pure C# with optional native acceleration via MKL (Intel Math Kernel Library) or OpenBLAS for performance-critical workloads. The library integrates with F# via the `MathNet.Numerics.FSharp` package.

Install via NuGet:
```
dotnet add package MathNet.Numerics
```

For native acceleration:
```
dotnet add package MathNet.Numerics.Providers.MKL
```

## Linear Algebra: Matrices and Vectors

Create, manipulate, and decompose matrices and vectors.

```csharp
using MathNet.Numerics.LinearAlgebra;

// Create matrices
var matrix = Matrix<double>.Build.DenseOfArray(new double[,]
{
    { 1, 2, 3 },
    { 4, 5, 6 },
    { 7, 8, 10 }
});

// Create vectors
var vector = Vector<double>.Build.Dense(new[] { 1.0, 2.0, 3.0 });

// Matrix operations
var transpose = matrix.Transpose();
var inverse = matrix.Inverse();
var determinant = matrix.Determinant();
var trace = matrix.Trace();

// Matrix-vector multiplication
var result = matrix * vector;

// Matrix-matrix multiplication
var product = matrix * transpose;

// Element-wise operations
var scaled = matrix * 2.0;
var sum = matrix + Matrix<double>.Build.DenseIdentity(3);

Console.WriteLine($"Determinant: {determinant}");
Console.WriteLine($"Result vector: [{string.Join(", ", result)}]");
```

## Solving Linear Systems

Solve systems of linear equations Ax = b using various decomposition methods.

```csharp
using MathNet.Numerics.LinearAlgebra;

// System: Ax = b
var a = Matrix<double>.Build.DenseOfArray(new double[,]
{
    { 3, 2, -1 },
    { 2, -2, 4 },
    { -1, 0.5, -1 }
});

var b = Vector<double>.Build.Dense(new[] { 1.0, -2.0, 0.0 });

// Direct solve
var x = a.Solve(b);
Console.WriteLine($"Solution: [{string.Join(", ", x.Select(v => $"{v:F4}"))}]");

// LU decomposition
var lu = a.LU();
var xLu = lu.Solve(b);

// QR decomposition (for least squares)
var qr = a.QR();
var xQr = qr.Solve(b);

// SVD decomposition (for rank-deficient systems)
var svd = a.Svd();
Console.WriteLine($"Singular values: [{string.Join(", ", svd.S)}]");
Console.WriteLine($"Rank: {svd.Rank}");
```

## Descriptive Statistics

Compute statistical measures on data sets.

```csharp
using System;
using System.Linq;
using MathNet.Numerics.Statistics;

var data = new[] { 2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0 };

// Central tendency
var mean = data.Mean();                        // 5.0
var median = data.Median();                    // 4.5
var geometricMean = data.GeometricMean();

// Dispersion
var variance = data.Variance();                // population variance
var stdDev = data.StandardDeviation();
var popVariance = data.PopulationVariance();
var popStdDev = data.PopulationStandardDeviation();

// Percentiles and quartiles
var p90 = data.Percentile(90);
var q1 = data.LowerQuartile();
var q3 = data.UpperQuartile();
var iqr = data.InterquartileRange();

// Five-number summary
var min = data.Minimum();
var max = data.Maximum();

Console.WriteLine($"Mean={mean}, StdDev={stdDev:F3}, Median={median}");
Console.WriteLine($"Q1={q1}, Q3={q3}, IQR={iqr}");

// Correlation and covariance
var x = new[] { 1.0, 2.0, 3.0, 4.0, 5.0 };
var y = new[] { 2.0, 4.1, 5.8, 8.0, 10.1 };
var correlation = Correlation.Pearson(x, y);
Console.WriteLine($"Pearson correlation: {correlation:F4}");
```

## Probability Distributions

Generate samples and compute probabilities from standard distributions.

```csharp
using System;
using MathNet.Numerics.Distributions;

// Normal distribution
var normal = new Normal(mean: 100, stddev: 15); // IQ distribution
Console.WriteLine($"Random sample: {normal.Sample():F2}");
Console.WriteLine($"P(X < 115): {normal.CumulativeDistribution(115):F4}");
Console.WriteLine($"PDF at 100: {normal.Density(100):F4}");

// Generate samples
var samples = new double[1000];
normal.Samples(samples);

// Uniform distribution
var uniform = new ContinuousUniform(lower: 0, upper: 1);
Console.WriteLine($"Uniform sample: {uniform.Sample():F4}");

// Poisson distribution
var poisson = new Poisson(lambda: 4.5);
Console.WriteLine($"Poisson sample: {poisson.Sample()}");
Console.WriteLine($"P(X = 3): {poisson.Probability(3):F4}");

// Exponential distribution
var exponential = new Exponential(rate: 0.5);
Console.WriteLine($"Mean time between events: {exponential.Mean:F2}");

// Binomial distribution
var binomial = new Binomial(p: 0.3, n: 10);
Console.WriteLine($"P(X = 3): {binomial.Probability(3):F4}");
Console.WriteLine($"Expected value: {binomial.Mean:F2}");
```

## Interpolation and Curve Fitting

Interpolate between data points and fit curves to data.

```csharp
using MathNet.Numerics;
using MathNet.Numerics.Interpolation;

// Data points
var xData = new[] { 0.0, 1.0, 2.0, 3.0, 4.0, 5.0 };
var yData = new[] { 0.0, 0.8, 0.9, 0.1, -0.8, -1.0 };

// Linear interpolation
var linear = Interpolate.Linear(xData, yData);
Console.WriteLine($"Linear at x=2.5: {linear.Interpolate(2.5):F4}");

// Cubic spline interpolation
var spline = Interpolate.CubicSpline(xData, yData);
Console.WriteLine($"Spline at x=2.5: {spline.Interpolate(2.5):F4}");

// Polynomial curve fitting (least squares)
var coefficients = Fit.Polynomial(xData, yData, degree: 3);
Console.WriteLine($"Polynomial coefficients: [{string.Join(", ", coefficients.Select(c => $"{c:F4}"))}]");

// Linear regression (y = ax + b)
var (intercept, slope) = Fit.Line(xData, yData);
Console.WriteLine($"Linear fit: y = {slope:F4}x + {intercept:F4}");

// Evaluate the fit
var predicted = xData.Select(x => slope * x + intercept).ToArray();
var rSquared = GoodnessOfFit.RSquared(predicted, yData);
Console.WriteLine($"R-squared: {rSquared:F4}");
```

## Random Number Generation

Math.NET provides multiple high-quality random number generators.

```csharp
using MathNet.Numerics.Random;

// Mersenne Twister (default, high quality)
var mt = new MersenneTwister(seed: 42);
Console.WriteLine($"Random double: {mt.NextDouble():F6}");
Console.WriteLine($"Random int [0, 100): {mt.Next(100)}");

// Xoshiro256** (fast, modern)
var xoshiro = new Xoshiro256StarStar(seed: 42);
var randomValues = new double[10];
xoshiro.NextDoubles(randomValues);

// Thread-safe random
var systemRandom = SystemRandomSource.Default;
Console.WriteLine($"Thread-safe random: {systemRandom.NextDouble():F6}");

// Generate random matrices
var randomMatrix = Matrix<double>.Build.Random(3, 3, new Normal(0, 1));
```

## Best Practices

1. **Use `Matrix<double>.Build` and `Vector<double>.Build` factory methods** instead of constructors for clear, readable matrix and vector creation.
2. **Choose the right decomposition** -- use LU for general square systems, QR for overdetermined (least squares), and SVD for rank-deficient or ill-conditioned systems.
3. **Enable MKL native provider** for production workloads involving large matrices by calling `Control.UseNativeMKL()` at startup to get 10-100x speedup on linear algebra operations.
4. **Use `Statistics` extension methods** on `IEnumerable<double>` for quick descriptive statistics without creating intermediate objects.
5. **Prefer `Fit.Polynomial` and `Fit.Line` over manual matrix construction** for curve fitting -- these methods handle the normal equations internally and are numerically stable.
6. **Seed random number generators** with a fixed value in tests for reproducibility, and use `SystemRandomSource.Default` in production for thread safety.
7. **Use sparse matrix builders** (`Matrix<double>.Build.Sparse`) when the matrix has mostly zero entries (e.g., graph adjacency, finite element) to save memory and computation.
8. **Check matrix condition number** with `matrix.ConditionNumber()` before solving linear systems -- ill-conditioned matrices produce numerically unstable solutions.
9. **Use `GoodnessOfFit.RSquared`** to evaluate the quality of curve fits rather than assuming the fit is good after computing coefficients.
10. **Avoid creating large temporary matrices** in loops -- reuse allocated matrices with in-place operations (e.g., `matrix.Multiply(other, result)`) to reduce GC pressure.
