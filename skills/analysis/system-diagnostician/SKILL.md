---
name: System Diagnostician
description: Performs Codex-assisted project health diagnostics, identifies capability gaps, and produces prioritized improvement plans.
version: 1.0.0
category: analysis
tags:
  - diagnostics
  - capability-planning
  - project-health
---

# System Diagnostician

**Analyze project health and recommend capabilities using Codex-powered system understanding**

## Purpose

Performs comprehensive project health analysis to diagnose issues, identify missing capabilities, and recommend improvements. Uses Codex to understand project structure, detect anti-patterns, analyze dependencies, and suggest optimal capability additions based on project goals.

## When to Use

- New project onboarding: "What does this project need?"
- Health checks: "Is this project following best practices?"
- Gap analysis: "What's missing to achieve X?"
- Performance audits: "Why is this slow?"
- Security audits: "What security risks exist?"
- Dependency audits: "Are dependencies up to date and safe?"

## Key Capabilities

- **Project Structure Analysis**: Understands project type, framework, architecture
- **Capability Gap Detection**: Identifies missing or incomplete capabilities
- **Health Scoring**: Quantifies project health across multiple dimensions
- **Recommendation Engine**: Suggests capabilities with impact/effort estimates
- **Dependency Analysis**: Checks for outdated, vulnerable, or unnecessary dependencies
- **Anti-Pattern Detection**: Identifies code smells and architectural issues
- **Prioritized Action Plan**: Orders recommendations by impact and effort

## Inputs

```yaml
inputs:
  project_path: string # Path to project directory
  capability_graph: string # Path to capability-graph.json
  focus_areas: array # Optional: ["security", "performance", "testing"]
  include_metrics: boolean # Include detailed metrics (default: false)
```

## Process

### Step 1: Project Discovery

```bash
#!/bin/bash
# Analyze project structure

PROJECT_PATH="${1:-.}"
cd "$PROJECT_PATH"

echo "Discovering project structure..."

# Detect project type
PROJECT_TYPE="unknown"
FRAMEWORK="unknown"

if [ -f "package.json" ]; then
  PROJECT_TYPE="nodejs"

  # Detect framework
  if grep -q "\"next\"" package.json; then
    FRAMEWORK="nextjs"
  elif grep -q "\"react\"" package.json; then
    FRAMEWORK="react"
  elif grep -q "\"express\"" package.json; then
    FRAMEWORK="express"
  fi
elif [ -f "requirements.txt" ] || [ -f "pyproject.toml" ]; then
  PROJECT_TYPE="python"
fi

# Gather file statistics
FILE_COUNT=$(find . -type f -not -path "./node_modules/*" -not -path "./.git/*" | wc -l)
CODE_FILES=$(find . -name "*.js" -o -name "*.ts" -o -name "*.jsx" -o -name "*.tsx" -o -name "*.py" | wc -l)
TEST_FILES=$(find . -name "*.test.*" -o -name "*.spec.*" | wc -l)

# Check for common directories
HAS_TESTS=$([ -d "tests" ] || [ -d "test" ] || [ -d "__tests__" ] && echo "true" || echo "false")
HAS_DOCS=$([ -f "README.md" ] && echo "true" || echo "false")
HAS_CI=$([ -d ".github/workflows" ] || [ -f ".gitlab-ci.yml" ] && echo "true" || echo "false")

# Package.json analysis
if [ -f "package.json" ]; then
  DEPENDENCIES=$(jq -r '.dependencies // {} | keys | length' package.json)
  DEV_DEPENDENCIES=$(jq -r '.devDependencies // {} | keys | length' package.json)
  SCRIPTS=$(jq -r '.scripts // {} | keys | length' package.json)
fi

# Generate project state
cat > /tmp/project-state.json <<EOF
{
  "project_type": "$PROJECT_TYPE",
  "framework": "$FRAMEWORK",
  "statistics": {
    "total_files": $FILE_COUNT,
    "code_files": $CODE_FILES,
    "test_files": $TEST_FILES
  },
  "has_tests": $HAS_TESTS,
  "has_docs": $HAS_DOCS,
  "has_ci": $HAS_CI,
  "dependencies": ${DEPENDENCIES:-0},
  "dev_dependencies": ${DEV_DEPENDENCIES:-0},
  "scripts": ${SCRIPTS:-0}
}
EOF
```

### Step 2: Health Assessment with Codex

```bash
# Use Codex to assess project health
PROJECT_STATE=$(cat /tmp/project-state.json)

# Get file listing for context
FILE_STRUCTURE=$(find . -type f -not -path "./node_modules/*" -not -path "./.git/*" | head -100)

codex exec "
Analyze this project's health and identify issues:

PROJECT STATE:
$PROJECT_STATE

FILE STRUCTURE (first 100 files):
$FILE_STRUCTURE

PACKAGE.JSON:
$(cat package.json 2>/dev/null || echo "{}")

Perform health assessment across these dimensions:

1. **Testing**: Test coverage, test quality, missing tests
2. **Documentation**: README quality, API docs, comments
3. **Security**: Vulnerabilities, exposed secrets, auth patterns
4. **Performance**: Bottlenecks, optimization opportunities
5. **Code Quality**: Linting, formatting, type safety
6. **Architecture**: Structure, patterns, scalability
7. **Dependencies**: Outdated packages, security issues, bloat
8. **CI/CD**: Automation, deployment strategy

For each dimension, provide:
- score: 0.0-1.0
- status: \"excellent\" | \"good\" | \"needs_improvement\" | \"critical\"
- issues: array of problems found
- recommendations: array of specific actions

Output JSON:
{
  \"overall_health\": 0.75,
  \"dimensions\": {
    \"testing\": {
      \"score\": 0.60,
      \"status\": \"needs_improvement\",
      \"issues\": [\"Only 15% test coverage\", \"No E2E tests\"],
      \"recommendations\": [\"Add unit tests for core functions\", \"Set up Playwright for E2E\"]
    },
    \"security\": {
      \"score\": 0.50,
      \"status\": \"critical\",
      \"issues\": [\"No input validation\", \"SQL injection possible\"],
      \"recommendations\": [\"Add input sanitization\", \"Use parameterized queries\"]
    }
  }
}

Output ONLY valid JSON.
" > /tmp/health-assessment.json
```

### Step 3: Capability Gap Analysis

```bash
# Identify missing capabilities using capability graph
HEALTH_ASSESSMENT=$(cat /tmp/health-assessment.json)
CAPABILITY_GRAPH=$(cat META/capability-graph.json)

codex exec "
Based on this health assessment, identify missing or incomplete capabilities:

HEALTH ASSESSMENT:
$HEALTH_ASSESSMENT

AVAILABLE CAPABILITIES:
$CAPABILITY_GRAPH

For each identified issue, suggest capabilities that would address it.

Output JSON:
{
  \"gaps\": [
    {
      \"issue\": \"No input validation\",
      \"severity\": \"high\",
      \"dimension\": \"security\",
      \"suggested_capabilities\": [\"security-engineer\", \"input-validator-mcp\"],
      \"impact\": \"high\",
      \"effort\": \"medium\"
    }
  ]
}

Output ONLY valid JSON.
" > /tmp/capability-gaps.json
```

### Step 4: Generate Recommendations

```bash
# Prioritize recommendations by impact and effort
python3 <<'PYTHON_SCRIPT'
import json

# Load data
with open('/tmp/health-assessment.json') as f:
    health = json.load(f)

with open('/tmp/capability-gaps.json') as f:
    gaps = json.load(f)

# Score recommendations
for gap in gaps['gaps']:
    # Impact score
    impact_scores = {'critical': 1.0, 'high': 0.8, 'medium': 0.5, 'low': 0.3}
    impact = impact_scores.get(gap.get('impact', 'medium'), 0.5)

    # Effort score (inverted - lower effort = higher score)
    effort_scores = {'low': 1.0, 'medium': 0.6, 'high': 0.3}
    effort = effort_scores.get(gap.get('effort', 'medium'), 0.6)

    # Priority = impact * effort
    gap['priority_score'] = round(impact * effort, 3)

# Sort by priority
gaps['gaps'].sort(key=lambda x: x['priority_score'], reverse=True)

# Write prioritized gaps
with open('/tmp/recommendations.json', 'w') as f:
    json.dump(gaps, f, indent=2)

print(f"Generated {len(gaps['gaps'])} recommendations")
PYTHON_SCRIPT
```

### Step 5: Generate Action Plan

```bash
# Create structured action plan
python3 <<'PYTHON_SCRIPT'
import json
from datetime import datetime

# Load all data
with open('/tmp/health-assessment.json') as f:
    health = json.load(f)

with open('/tmp/recommendations.json') as f:
    recommendations = json.load(f)

# Generate action plan
action_plan = {
    'project': 'PROJECT_NAME',
    'analyzed_at': datetime.utcnow().isoformat() + 'Z',
    'overall_health': health.get('overall_health', 0),
    'health_assessment': health,
    'recommendations': recommendations['gaps'][:10],  # Top 10
    'quick_wins': [
        r for r in recommendations['gaps']
        if r.get('effort') == 'low' and r.get('impact') in ['high', 'critical']
    ][:3],
    'critical_issues': [
        r for r in recommendations['gaps']
        if r.get('severity') == 'high' or r.get('severity') == 'critical'
    ]
}

with open('/tmp/diagnostic-report.json', 'w') as f:
    json.dump(action_plan, f, indent=2)
PYTHON_SCRIPT
```

## Scoring System

### Health Dimensions

Each dimension scored 0.0-1.0:

```javascript
const dimensions = {
  testing: {
    weight: 0.15,
    factors: ['coverage', 'test_quality', 'test_types']
  },
  documentation: {
    weight: 0.1,
    factors: ['readme', 'api_docs', 'code_comments']
  },
  security: {
    weight: 0.2,
    factors: ['vulnerabilities', 'auth', 'input_validation']
  },
  performance: {
    weight: 0.15,
    factors: ['load_time', 'memory_usage', 'optimization']
  },
  code_quality: {
    weight: 0.15,
    factors: ['linting', 'typing', 'complexity']
  },
  architecture: {
    weight: 0.1,
    factors: ['structure', 'patterns', 'scalability']
  },
  dependencies: {
    weight: 0.1,
    factors: ['up_to_date', 'security', 'bloat']
  },
  ci_cd: {
    weight: 0.05,
    factors: ['automation', 'deployment', 'monitoring']
  }
}

// Overall health = weighted average
overallHealth = sum(dimension.score * dimension.weight)
```

### Recommendation Priority

```javascript
function calculatePriority(gap) {
  const impactScores = { critical: 1.0, high: 0.8, medium: 0.5, low: 0.3 }
  const effortScores = { low: 1.0, medium: 0.6, high: 0.3 }

  const impact = impactScores[gap.impact] || 0.5
  const effort = effortScores[gap.effort] || 0.6

  return impact * effort
}
```

## Example Output

```json
{
  "project": "my-nextjs-app",
  "analyzed_at": "2025-10-28T12:00:00Z",
  "overall_health": 0.68,
  "health_assessment": {
    "overall_health": 0.68,
    "dimensions": {
      "testing": {
        "score": 0.4,
        "status": "needs_improvement",
        "issues": ["Only 15% test coverage", "No E2E tests", "Missing integration tests"],
        "recommendations": [
          "Add unit tests for API routes",
          "Set up Playwright for E2E testing",
          "Add integration tests for database"
        ]
      },
      "security": {
        "score": 0.5,
        "status": "critical",
        "issues": [
          "No input validation on API routes",
          "CORS configured too permissively",
          "Environment variables exposed in client"
        ],
        "recommendations": [
          "Add input validation with Zod",
          "Restrict CORS to specific origins",
          "Use NEXT_PUBLIC_ prefix correctly"
        ]
      }
    }
  },
  "recommendations": [
    {
      "issue": "No input validation on API routes",
      "severity": "high",
      "dimension": "security",
      "suggested_capabilities": ["security-engineer", "api-designer"],
      "impact": "high",
      "effort": "medium",
      "priority_score": 0.48
    },
    {
      "issue": "Only 15% test coverage",
      "severity": "medium",
      "dimension": "testing",
      "suggested_capabilities": ["testing-strategist"],
      "impact": "high",
      "effort": "high",
      "priority_score": 0.24
    }
  ],
  "quick_wins": [
    {
      "issue": "Missing README documentation",
      "severity": "low",
      "dimension": "documentation",
      "suggested_capabilities": ["technical-writer"],
      "impact": "medium",
      "effort": "low",
      "priority_score": 0.5
    }
  ],
  "critical_issues": [
    {
      "issue": "No input validation on API routes",
      "severity": "high",
      "dimension": "security",
      "suggested_capabilities": ["security-engineer", "api-designer"],
      "impact": "high",
      "effort": "medium",
      "priority_score": 0.48
    }
  ]
}
```

## Integration

### With orchestration-planner

Recommendations include suggested capabilities that planner can use to generate workflows.

### With skill-validator

Health assessment includes validation of existing capabilities.

### With Repository Brain

Will integrate into `scripts/brain/diagnose` command for interactive diagnostics.

## Success Metrics

- ✅ Health scores correlate with manual audits
- ✅ Recommendations are actionable and specific
- ✅ Quick wins provide immediate value
- ✅ Critical issues correctly prioritized
- ✅ Suggested capabilities are relevant

## Related Skills

- orchestration-planner: Uses recommendations to plan improvements
- skill-validator: Validates existing capabilities
- capability-graph-builder: Provides capability options
