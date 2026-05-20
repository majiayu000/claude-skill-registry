---
name: mathflow
description: >
  Guidance for mathematical expression parsing and evaluation in .NET using NCalc and related libraries.
  USE FOR: runtime mathematical expression evaluation, user-defined formulas, rule engines with math expressions, parameterized calculations, spreadsheet-style formula evaluation.
  DO NOT USE FOR: symbolic algebra (use AngouriMath), numerical linear algebra (use Math.NET), machine learning (use ML.NET), scientific computing with matrices.
license: MIT
metadata:
  displayName: MathFlow
  author: "Tyler-R-Kendrick"
  version: "1.0.0"
compatibility:
  - claude
  - copilot
  - cursor
references:
  - title: "NCalc Documentation"
    url: "https://ncalc.github.io/ncalc/"
  - title: "NCalc GitHub Repository"
    url: "https://github.com/ncalc/ncalc"
  - title: "NCalcSync NuGet Package"
    url: "https://www.nuget.org/packages/NCalcSync"
---

# MathFlow (Mathematical Expression Evaluation)

## Overview

Mathematical expression evaluation in .NET refers to parsing and computing results from string-based mathematical formulas at runtime. The primary library for this is NCalc, which parses expressions into an AST and evaluates them with support for variables, custom functions, and standard math operators.

This skill covers NCalc for general expression evaluation and touches on complementary approaches such as `System.Linq.Expressions` for compiled expression trees and Flee for lightweight evaluation. These libraries are commonly used in rule engines, configurable business logic, reporting calculations, and any scenario where formulas are provided by users or configuration rather than hardcoded.

Install via NuGet:
```
dotnet add package NCalc2
```

## Basic Expression Evaluation

NCalc parses mathematical expressions from strings and evaluates them with operator precedence, parentheses, and standard math functions.

```csharp
using NCalc;

// Simple arithmetic
var expr = new Expression("2 + 3 * 5");
var result = expr.Evaluate(); // 17

// Parentheses for grouping
var grouped = new Expression("(2 + 3) * 5");
var groupedResult = grouped.Evaluate(); // 25

// Built-in math functions
var mathExpr = new Expression("Sqrt(144) + Pow(2, 10)");
var mathResult = mathExpr.Evaluate(); // 1036 (12 + 1024)

// Trigonometric functions
var trigExpr = new Expression("Sin(PI / 2) + Cos(0)");
trigExpr.Parameters["PI"] = Math.PI;
var trigResult = trigExpr.Evaluate(); // 2.0

// Comparison and logical operators
var condition = new Expression("price > 100 && discount > 0");
condition.Parameters["price"] = 150.0;
condition.Parameters["discount"] = 10.0;
var isDiscounted = (bool)condition.Evaluate(); // true
```

## Parameterized Expressions

Bind named parameters to expressions for dynamic calculation with varying inputs.

```csharp
using NCalc;

// Pricing formula
var pricingFormula = new Expression("basePrice * quantity * (1 - discountRate)");
pricingFormula.Parameters["basePrice"] = 25.00;
pricingFormula.Parameters["quantity"] = 10;
pricingFormula.Parameters["discountRate"] = 0.15;
var total = (double)pricingFormula.Evaluate(); // 212.5

// BMI calculator
var bmi = new Expression("weight / Pow(height, 2)");
bmi.Parameters["weight"] = 75.0;  // kg
bmi.Parameters["height"] = 1.80;  // meters
var bmiValue = (double)bmi.Evaluate(); // ~23.15

// Temperature conversion
var celsiusToFahrenheit = new Expression("celsius * 9 / 5 + 32");
celsiusToFahrenheit.Parameters["celsius"] = 100.0;
var fahrenheit = (double)celsiusToFahrenheit.Evaluate(); // 212.0
```

## Custom Functions

Register custom functions that NCalc can call during expression evaluation.

```csharp
using System;
using NCalc;

var expr = new Expression("Clamp(value, minVal, maxVal)");
expr.Parameters["value"] = 150.0;
expr.Parameters["minVal"] = 0.0;
expr.Parameters["maxVal"] = 100.0;

expr.EvaluateFunction += (name, args) =>
{
    if (name == "Clamp")
    {
        var val = Convert.ToDouble(args.Parameters[0].Evaluate());
        var min = Convert.ToDouble(args.Parameters[1].Evaluate());
        var max = Convert.ToDouble(args.Parameters[2].Evaluate());
        args.Result = Math.Clamp(val, min, max);
    }
};

var result = expr.Evaluate(); // 100.0

// Multiple custom functions
var formula = new Expression("Round(Lerp(start, end, t), 2)");
formula.Parameters["start"] = 10.0;
formula.Parameters["end"] = 50.0;
formula.Parameters["t"] = 0.75;

formula.EvaluateFunction += (name, args) =>
{
    switch (name)
    {
        case "Lerp":
            var a = Convert.ToDouble(args.Parameters[0].Evaluate());
            var b = Convert.ToDouble(args.Parameters[1].Evaluate());
            var t = Convert.ToDouble(args.Parameters[2].Evaluate());
            args.Result = a + (b - a) * t;
            break;
        case "Round":
            var value = Convert.ToDouble(args.Parameters[0].Evaluate());
            var digits = Convert.ToInt32(args.Parameters[1].Evaluate());
            args.Result = Math.Round(value, digits);
            break;
    }
};

var lerped = formula.Evaluate(); // 40.0
```

## Expression Validation

Validate expressions before evaluating them to catch syntax errors and missing parameters.

```csharp
using NCalc;

public class FormulaValidator
{
    public (bool IsValid, string? Error) Validate(
        string expression,
        IReadOnlyDictionary<string, object> availableParameters)
    {
        try
        {
            var expr = new Expression(expression);

            if (expr.HasErrors())
            {
                return (false, $"Syntax error: {expr.Error}");
            }

            // Set all available parameters
            foreach (var param in availableParameters)
            {
                expr.Parameters[param.Key] = param.Value;
            }

            // Attempt evaluation to catch runtime errors
            expr.Evaluate();
            return (true, null);
        }
        catch (ArgumentException ex)
        {
            return (false, $"Missing parameter: {ex.Message}");
        }
        catch (Exception ex)
        {
            return (false, $"Evaluation error: {ex.Message}");
        }
    }
}

// Usage
var validator = new FormulaValidator();
var parameters = new Dictionary<string, object>
{
    ["price"] = 10.0,
    ["quantity"] = 5
};

var (isValid, error) = validator.Validate("price * quantity", parameters);
Console.WriteLine($"Valid: {isValid}"); // true

var (isValid2, error2) = validator.Validate("price * + quantity", parameters);
Console.WriteLine($"Valid: {isValid2}, Error: {error2}"); // false, syntax error
```

## Building a Configurable Rule Engine

Use NCalc expressions in a rule engine where business rules are stored as configuration.

```csharp
using System;
using System.Collections.Generic;
using System.Linq;
using NCalc;

public record Rule(string Name, string Condition, string ValueExpression);

public class RuleEngine
{
    private readonly List<Rule> _rules;

    public RuleEngine(IEnumerable<Rule> rules)
    {
        _rules = rules.ToList();
    }

    public double Evaluate(IDictionary<string, object> context)
    {
        foreach (var rule in _rules)
        {
            var condition = new Expression(rule.Condition);
            foreach (var param in context)
                condition.Parameters[param.Key] = param.Value;

            if ((bool)condition.Evaluate())
            {
                var valueExpr = new Expression(rule.ValueExpression);
                foreach (var param in context)
                    valueExpr.Parameters[param.Key] = param.Value;

                return Convert.ToDouble(valueExpr.Evaluate());
            }
        }

        throw new InvalidOperationException("No matching rule found");
    }
}

// Usage with shipping cost rules
var rules = new[]
{
    new Rule("Free Shipping", "orderTotal >= 100", "0"),
    new Rule("Flat Rate", "weight <= 5", "5.99"),
    new Rule("Heavy Package", "weight > 5", "weight * 1.50 + 5.99")
};

var engine = new RuleEngine(rules);
var cost = engine.Evaluate(new Dictionary<string, object>
{
    ["orderTotal"] = 45.00,
    ["weight"] = 8.0
});
Console.WriteLine($"Shipping: ${cost}"); // $17.99
```

## Expression Library Comparison

| Library | Evaluation | Compilation | Custom Functions | Safety | Use Case |
|---------|-----------|-------------|-----------------|--------|----------|
| NCalc | Interpreted | No | Yes | Sandboxed | User formulas, rule engines |
| Flee | Compiled IL | Yes | Yes | Limited | Performance-critical evaluation |
| `System.Linq.Expressions` | Compiled | Yes | Via delegates | Full CLR | Internal computed properties |
| Roslyn Scripting | Full C# | Yes | Full C# | None | Developer scripting |
| DataTable.Compute | Interpreted | No | No | Limited | Simple SQL-like expressions |

## Best Practices

1. **Validate expressions at configuration time** rather than at evaluation time by calling `HasErrors()` and catching exceptions during setup.
2. **Whitelist allowed functions** in user-facing scenarios by handling the `EvaluateFunction` event and rejecting unrecognized function names.
3. **Set evaluation timeouts** for user-provided expressions by wrapping `Evaluate()` in a `CancellationToken`-aware task to prevent denial-of-service via expensive computations.
4. **Cache `Expression` instances** when the same formula is evaluated repeatedly with different parameter values, since parsing is more expensive than parameter binding.
5. **Use `double` as the standard numeric type** for parameters because NCalc internally works with `double` for arithmetic, and mixing `int`/`decimal` can cause unexpected type coercion.
6. **Document available parameters and functions** for formula authors so they know what variables and functions are available in their expressions.
7. **Avoid using NCalc for general-purpose scripting** -- it is designed for mathematical formulas, not control flow or string manipulation.
8. **Test edge cases** including division by zero, very large numbers, `NaN` results, and negative inputs for square root to ensure your error handling covers all scenarios.
9. **Prefer NCalc over `DataTable.Compute`** for new code because NCalc supports custom functions, better error reporting, and a cleaner API.
10. **Separate expression parsing from evaluation** so you can report syntax errors during validation and parameter errors during execution with distinct error messages.
