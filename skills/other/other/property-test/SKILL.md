---
name: property-test
description: Generate property-based tests with FsCheck or fast-check
argument-hint: "<target-class> [--framework=fscheck|fast-check]"
tags: [testing, property-based, fscheck, quality]
user-invocable: true
---

# Property-Based Testing

Generate property-based tests that verify invariants across random inputs.

## For .NET (FsCheck)
```bash
dotnet add package FsCheck.Xunit
```
```csharp
[Property]
public Property Score_AlwaysBetween0And1(double[] weights)
{
    var score = MatchingService.CalculateScore(weights);
    return (score >= 0.0 && score <= 1.0).ToProperty();
}
```

## For TypeScript (fast-check)
```bash
npm install --save-dev fast-check
```
```typescript
fc.assert(fc.property(fc.array(fc.double()), (weights) => {
  const score = calculateScore(weights);
  return score >= 0 && score <= 1;
}));
```

## Arguments
- `<target-class>`: Class or module to test
- `--framework=<fscheck|fast-check>`: Testing framework