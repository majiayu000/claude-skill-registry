---
name: analyze-github-repo
description: >
  Deep analysis of a GitHub repository for tool spotlight inclusion in news digests.
  Evaluates the project's purpose, quality, popularity trajectory, and usefulness
  for AI practitioners.
license: MIT
compatibility: Requires OpenAI-compatible LLM API access and GitHub API access
metadata:
  kubani:
    domain: news
    category: diagnostic
    version: "1.0.0"
    mcp_servers: []
    requires_approval: false
    confidence: 0.8
input:
  - name: repo
    type: GithubRepo
    description: Repository metadata from fetch-github-trending
  - name: include_readme
    type: bool
    default: true
    description: Whether to fetch and analyze the README for deeper insights
output:
  - name: analysis
    type: RepoAnalysis
    description: Comprehensive repository analysis with summary and recommendations
  - name: spotlight_worthy
    type: bool
    description: Whether repo deserves a featured tool spotlight
  - name: spotlight_summary
    type: str
    description: Ready-to-use summary for digest if spotlight-worthy
---

# Analyze GitHub Repo

Evaluate a GitHub repository for potential inclusion as a tool spotlight in the news digest.

## When to Use

- Evaluating trending repos for digest tool spotlight section
- Assessing quality and usefulness of new AI tools
- Creating tool recommendation summaries
- Keywords: github, repository, tool, library, spotlight, analysis

## Prerequisites

- Repository metadata available (from fetch-github-trending)
- Network access to GitHub for README fetch (optional)

## Input Schema

```json
{
  "repo": {
    "full_name": "owner/repo-name",
    "name": "repo-name",
    "description": "Repository description",
    "url": "https://github.com/owner/repo-name",
    "stars": 5000,
    "forks": 300,
    "language": "Python",
    "topics": ["llm", "machine-learning"],
    "created_at": "2025-06-15",
    "pushed_at": "2026-01-26",
    "open_issues": 42
  },
  "include_readme": true
}
```

## Actions

### Step 1: Assess Project Category

Classify the repository:
- **Framework**: Full framework for building applications (e.g., LangChain)
- **Library**: Focused library for specific task (e.g., sentence-transformers)
- **Tool**: Standalone tool or CLI (e.g., ollama)
- **Model**: Model weights or implementation (e.g., Llama)
- **Dataset**: Dataset or data processing
- **Application**: Complete application (e.g., chat UI)
- **Tutorial/Demo**: Educational content

### Step 2: Evaluate Quality Signals

Assess quality based on:
1. **Documentation**: Is there a README? Is it comprehensive?
2. **Activity**: Recent commits? Active maintenance?
3. **Community**: Issues being addressed? PRs reviewed?
4. **Code Quality**: Based on language, structure visible from description
5. **Dependencies**: Are dependencies reasonable and maintained?

### Step 3: Analyze Popularity Trajectory

Calculate growth indicators:
- **Star velocity**: Stars gained recently (estimate from trending status)
- **Fork ratio**: Forks/Stars indicates adoption
- **Issue health**: Open issues vs total activity
- **Maturity**: Age vs popularity

### Step 4: Determine Use Cases

Identify who would benefit:
- **Researchers**: Academic use cases
- **Practitioners**: Production deployment
- **Hobbyists**: Personal projects
- **Enterprise**: Business applications

### Step 5: Identify Differentiators

What makes this repo special:
- **Novel approach**: Does something new
- **Better performance**: Faster/cheaper than alternatives
- **Ease of use**: Lower barrier than alternatives
- **Integration**: Works well with popular tools
- **Active community**: Good support and updates

### Step 6: Fetch and Analyze README (if enabled)

If `include_readme` is true:
1. Fetch README.md from GitHub
2. Extract:
   - Installation instructions
   - Quick start example
   - Feature list
   - Comparison with alternatives (if mentioned)

### Step 7: Generate Spotlight Summary

If spotlight-worthy, create a 2-3 sentence summary:
1. What the tool does
2. Why it's noteworthy now
3. Who should check it out

### Step 8: Determine Spotlight Worthiness

A repo is spotlight-worthy if:
- Stars >= 1000 OR growing rapidly (>500 in last week)
- Active maintenance (pushed within 7 days)
- Clear, useful purpose for AI practitioners
- Good documentation
- NOT primarily educational/tutorial content

## Output Schema

```json
{
  "analysis": {
    "full_name": "owner/repo-name",
    "category": "library",
    "quality_scores": {
      "documentation": 8,
      "activity": 9,
      "community": 7,
      "overall": 8
    },
    "popularity_metrics": {
      "star_count": 5000,
      "fork_count": 300,
      "fork_ratio": 0.06,
      "estimated_weekly_stars": 500,
      "growth_status": "rapid"
    },
    "use_cases": ["practitioners", "enterprise"],
    "differentiators": [
      "2x faster than alternative X",
      "Simple API with good defaults",
      "Active Discord community"
    ],
    "target_audience": "ML engineers building LLM applications",
    "maturity": "stable",
    "risk_factors": [
      "Single maintainer",
      "No enterprise support"
    ]
  },
  "spotlight_worthy": true,
  "spotlight_summary": "**repo-name** is a new Python library that makes LLM inference 2x faster with a simple API. It's gained 500 stars this week as developers discover its drop-in compatibility with popular frameworks. Worth checking out if you're running inference workloads."
}
```

## Success Criteria

- [ ] Category correctly identified
- [ ] Quality assessment reasonable
- [ ] Spotlight decision justified by metrics
- [ ] Summary is concise and informative
- [ ] Target audience identified

## Failure Handling

| Error Type | Handling Strategy |
|------------|-------------------|
| README fetch fails | Continue without README analysis |
| Minimal description | Use topics and repo name for analysis |
| Private/deleted repo | Return error with explanation |

## Examples

### Example 1: High-Quality New Library

**Input:**
```json
{
  "repo": {
    "full_name": "example/llm-accelerator",
    "name": "llm-accelerator",
    "description": "Fast LLM inference with automatic batching and caching",
    "url": "https://github.com/example/llm-accelerator",
    "stars": 3500,
    "forks": 180,
    "language": "Python",
    "topics": ["llm", "inference", "optimization"],
    "created_at": "2025-11-01",
    "pushed_at": "2026-01-26",
    "open_issues": 25
  },
  "include_readme": true
}
```

**Output:**
```json
{
  "analysis": {
    "full_name": "example/llm-accelerator",
    "category": "library",
    "quality_scores": {
      "documentation": 9,
      "activity": 10,
      "community": 8,
      "overall": 9
    },
    "popularity_metrics": {
      "star_count": 3500,
      "fork_count": 180,
      "fork_ratio": 0.05,
      "estimated_weekly_stars": 400,
      "growth_status": "rapid"
    },
    "use_cases": ["practitioners", "enterprise"],
    "differentiators": [
      "Automatic request batching",
      "Built-in caching layer",
      "Drop-in replacement for common APIs"
    ],
    "target_audience": "ML engineers and backend developers",
    "maturity": "growing",
    "risk_factors": []
  },
  "spotlight_worthy": true,
  "spotlight_summary": "**llm-accelerator** automatically batches and caches LLM requests, cutting inference costs without code changes. With 3,500 stars and 400 gained this week, it's becoming a go-to for teams looking to optimize their LLM deployments. Check it out if you're serving LLM requests at scale."
}
```

### Example 2: Tutorial Repository (Not Spotlight Worthy)

**Input:**
```json
{
  "repo": {
    "full_name": "someone/llm-tutorial",
    "name": "llm-tutorial",
    "description": "Learn how to build with LLMs - step by step tutorials",
    "url": "https://github.com/someone/llm-tutorial",
    "stars": 800,
    "forks": 150,
    "language": "Jupyter Notebook",
    "topics": ["tutorial", "llm", "learning"],
    "created_at": "2025-08-01",
    "pushed_at": "2026-01-20",
    "open_issues": 5
  },
  "include_readme": false
}
```

**Output:**
```json
{
  "analysis": {
    "full_name": "someone/llm-tutorial",
    "category": "tutorial",
    "quality_scores": {
      "documentation": 7,
      "activity": 6,
      "community": 5,
      "overall": 6
    },
    "popularity_metrics": {
      "star_count": 800,
      "fork_count": 150,
      "fork_ratio": 0.19,
      "estimated_weekly_stars": 20,
      "growth_status": "steady"
    },
    "use_cases": ["hobbyists", "researchers"],
    "differentiators": [
      "Comprehensive tutorial collection"
    ],
    "target_audience": "Beginners learning LLM development",
    "maturity": "stable",
    "risk_factors": [
      "Educational content, not production tool"
    ]
  },
  "spotlight_worthy": false,
  "spotlight_summary": ""
}
```

### Example 3: Popular But Stale Repository

**Input:**
```json
{
  "repo": {
    "full_name": "old/legacy-tool",
    "name": "legacy-tool",
    "description": "ML toolkit from 2023",
    "url": "https://github.com/old/legacy-tool",
    "stars": 15000,
    "forks": 2000,
    "language": "Python",
    "topics": ["machine-learning"],
    "created_at": "2022-01-01",
    "pushed_at": "2025-06-01",
    "open_issues": 500
  },
  "include_readme": false
}
```

**Output:**
```json
{
  "analysis": {
    "full_name": "old/legacy-tool",
    "category": "framework",
    "quality_scores": {
      "documentation": 7,
      "activity": 2,
      "community": 3,
      "overall": 4
    },
    "popularity_metrics": {
      "star_count": 15000,
      "fork_count": 2000,
      "fork_ratio": 0.13,
      "estimated_weekly_stars": 5,
      "growth_status": "declining"
    },
    "use_cases": ["practitioners"],
    "differentiators": [],
    "target_audience": "Legacy users",
    "maturity": "legacy",
    "risk_factors": [
      "No recent updates",
      "High open issue count",
      "Likely abandoned"
    ]
  },
  "spotlight_worthy": false,
  "spotlight_summary": ""
}
```

## Related Skills

- [fetch-github-trending](../../collection/fetch-github-trending/SKILL.md) - Fetch repos for analysis
- [compose-executive-digest](../../action/compose-executive-digest/SKILL.md) - Include in tool spotlight

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-27 | Initial version |
