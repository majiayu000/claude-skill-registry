---
name: mutation-test
description: Run mutation testing to validate test suite quality
argument-hint: "[--project=<test-project>] [--threshold=60]"
tags: [testing, mutation, quality, stryker]
user-invocable: true
---

# Mutation Testing with Stryker

Run mutation testing to verify your test suite actually catches bugs.

## For .NET (Stryker.NET)
```bash
dotnet tool install -g dotnet-stryker
cd src/backend/Tests/MatchingServiceTests
dotnet stryker
```

Configure `stryker-config.json`:
```json
{
  "stryker-config": {
    "project": "CandidateMatchingEngine.csproj",
    "mutate": ["**/Services/**/*.cs", "!**/Generated/**"],
    "thresholds": { "high": 80, "low": 60, "break": 40 },
    "reporters": ["html", "json", "progress"],
    "concurrency": 4
  }
}
```

## For TypeScript/JavaScript (StrykerJS)
```bash
npx stryker init
npx stryker run
```

## Interpreting Results
- **Killed**: Test caught the mutation (GOOD)
- **Survived**: Tests missed the change (BAD -- add tests)
- **Mutation score** = killed / (killed + survived) -- target >60%

## CI Integration
```yaml
- script: dotnet stryker --threshold-break 40
  displayName: "Mutation Testing"
  condition: eq(variables['Build.Reason'], 'PullRequest')
```

## Arguments
- `--project=<path>`: Path to test project
- `--threshold=<n>`: Break build if score below this (default: 60)