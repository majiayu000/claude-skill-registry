---
name: RubyCritic Code Quality Analysis
description: Analyze Ruby and Rails code quality with RubyCritic. Identifies code smells, complexity issues, and refactoring opportunities. Provides detailed metrics, scores files A-F, compares branches, and prioritizes high-churn problem areas. Use when analyzing Ruby code quality, reviewing PRs, or identifying technical debt.
version: 1.0.0
author: Evan Sparkman
tags: [ruby, rails, code-quality, refactoring, rubycritic, testing, static-analysis]
---

# RubyCritic Code Quality Analysis Skill

A Claude Code skill for analyzing Ruby and Rails code quality using RubyCritic.

## Description

This skill integrates RubyCritic to provide comprehensive code quality analysis for Ruby and Rails projects. It helps identify code smells, complexity issues, and areas for refactoring with detailed metrics and actionable insights.

## Commands

### `/rubycritic [path]`

Analyze code quality for the specified path or entire project.

**Options:**
- `path` (optional): Specific file or directory to analyze. Defaults to current directory.

**Examples:**
```
/rubycritic
/rubycritic app/models
/rubycritic app/controllers/users_controller.rb
```

### `/rubycritic-summary`

Get a quick summary of code quality metrics without detailed file breakdowns.

### `/rubycritic-worst`

Show only the worst-rated files that need immediate attention.

**Options:**
- `--limit N`: Number of worst files to show (default: 10)

**Examples:**
```
/rubycritic-worst
/rubycritic-worst --limit 5
```

### `/rubycritic-compare [branch]`

Compare code quality between current branch and specified branch.

**Options:**
- `branch`: Branch to compare against (default: main/master)

**Examples:**
```
/rubycritic-compare main
/rubycritic-compare develop
```

## Usage Guidelines

### When to Use This Skill

1. **Before Code Reviews**: Run analysis on changed files to catch issues early
2. **After Refactoring**: Verify improvements in code quality metrics
3. **Regular Health Checks**: Weekly or sprint-based quality assessments
4. **Legacy Code**: Identify technical debt and prioritize refactoring efforts
5. **Onboarding**: Help new developers understand code quality standards

### Interpretation of Results

**Score Ranges:**
- **A (90-100)**: Excellent - minimal issues
- **B (80-89)**: Good - minor improvements needed
- **C (70-79)**: Fair - consider refactoring
- **D (60-69)**: Poor - refactoring recommended
- **F (<60)**: Critical - immediate attention required

**Key Metrics:**
- **Churn**: How frequently files change (high churn + low quality = priority)
- **Complexity**: Cyclomatic complexity (aim for < 10 per method)
- **Duplication**: Code duplication percentage (aim for < 5%)
- **Smells**: Code smell count by type (Long Method, Feature Envy, etc.)

### Best Practices

1. **Focus on Trends**: Track quality over time, not just absolute scores
2. **Prioritize High-Churn Files**: Files that change often with low quality scores
3. **Set Team Standards**: Define acceptable thresholds for your team
4. **Incremental Improvements**: Don't try to fix everything at once
5. **Context Matters**: Some low scores may be acceptable (e.g., configuration files)

## Implementation

### Installation

The skill automatically checks for RubyCritic and installs it if needed:

```bash
gem install rubycritic
```

### Configuration

Create a `.rubycritic.yml` in your project root for custom settings:

```yaml
# Minimum score for a file to be considered acceptable
minimum_score: 80.0

# Paths to exclude from analysis
paths:
  - 'db/schema.rb'
  - 'db/migrate/**/*'
  - 'config/**/*'
  - 'bin/**/*'
  - 'spec/factories/**/*'

# Enable/disable specific analyzers
analyzers:
  - flay      # Structural duplication
  - flog      # ABC complexity
  - reek      # Code smells
  - rubocop   # Style issues (if available)

# Format for output
formats:
  - console
  - html

# Branch for comparison mode
branch: main
```

### Output

The skill provides:

1. **Summary Statistics**: Overall project health
2. **File-Level Scores**: Detailed breakdown by file
3. **Code Smells**: Specific issues identified
4. **Complexity Metrics**: Cyclomatic complexity by method
5. **Recommendations**: Actionable suggestions for improvement

### Integration with Rails Workflows

**Pre-Commit Analysis:**
```bash
/rubycritic $(git diff --name-only --cached | grep '\.rb$')
```

**CI/CD Integration:**
- Run on pull requests to track quality trends
- Fail builds if quality drops below threshold
- Generate HTML reports for team review

**Performance Considerations:**
- Large projects may take time to analyze
- Use targeted paths for faster feedback
- Run full analysis periodically (CI/CD)
- Cache results when possible

## Common Issues and Solutions

### Issue: Analysis Takes Too Long

**Solution:** Narrow the scope
```
/rubycritic app/models/user.rb
/rubycritic app/controllers
```

### Issue: Too Many False Positives

**Solution:** Configure `.rubycritic.yml` to exclude problematic analyzers or paths

### Issue: Scores Seem Inconsistent

**Solution:** RubyCritic uses multiple analyzers; check individual metric breakdowns

## Advanced Usage

### Custom Thresholds

Set quality gates for your team:

```ruby
# In your CI/CD pipeline
if average_score < 75
  puts "Code quality below threshold!"
  exit 1
end
```

### Focused Refactoring

Target specific code smells:

```
/rubycritic app/models --smells "LongMethod,FeatureEnvy"
```

### Historical Tracking

Compare against previous commits:

```
/rubycritic-compare HEAD~5
```

## Rails-Specific Considerations

- **Models**: Pay attention to complexity in callbacks and validations
- **Controllers**: Watch for fat controllers (complexity > 10)
- **Services**: Service objects should have low complexity
- **Concerns**: Check for proper modularity and single responsibility
- **Helpers**: Avoid business logic in helpers

## Output Example

```
RubyCritic Analysis Results
===========================

Project Score: B (82.5)

Top Issues:
1. app/models/user.rb (Score: 65.2, Grade: D)
   - Long Method: #calculate_permissions (complexity: 18)
   - Feature Envy: accessing order.items repeatedly
   - Duplication: 3 similar conditional blocks

2. app/controllers/orders_controller.rb (Score: 71.3, Grade: C)
   - Long Method: #create (complexity: 15)
   - Too Many Instance Variables: 6 ivars in #index

Recommendations:
- Extract #calculate_permissions into a service object
- Use Law of Demeter for order.items access
- Refactor conditional logic in User model
- Slim down OrdersController#create method
```

## Resources

- [RubyCritic GitHub](https://github.com/whitesmith/rubycritic)
- [Code Smells Reference](https://github.com/troessner/reek/blob/master/docs/Code-Smells.md)
- [Cyclomatic Complexity](https://en.wikipedia.org/wiki/Cyclomatic_complexity)
- [Rails Best Practices](https://rails-bestpractices.com/)

## Tips for Claude Code

When using this skill, Claude should:

1. **Provide Context**: Explain why certain scores matter
2. **Prioritize Issues**: Focus on high-impact, high-churn files
3. **Suggest Refactorings**: Offer specific code improvements
4. **Show Examples**: Demonstrate better patterns for identified issues
5. **Track Progress**: Help monitor quality improvements over time
6. **Be Pragmatic**: Recognize when "perfect" scores aren't necessary
