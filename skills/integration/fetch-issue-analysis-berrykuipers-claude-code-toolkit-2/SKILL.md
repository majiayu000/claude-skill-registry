---
name: fetch-github-issue-analysis
description: Fetch GitHub issue details with AI analysis comment from github-actions bot, extracting structured data for architecture planning in WescoBar workflows
---

# Fetch GitHub Issue Analysis

## Purpose

Retrieve complete GitHub issue information including title, body, labels, and AI-generated analysis comment (if present) for use in conductor workflow Phase 1.

## When to Use

- Conductor workflow Phase 1 (Issue Discovery and Planning)
- Workflow resumption with existing issue number
- Issue selection and validation
- Architecture planning with AI insights

## Instructions

### Step 1: Fetch Basic Issue Data

```bash
# Safe parameter handling with validation
ISSUE_NUMBER=${1:-""}

# Validate required parameter
if [ -z "$ISSUE_NUMBER" ]; then
  echo "❌ Error: Issue number required"
  echo "Usage: fetch-github-issue-analysis <issue_number>"
  exit 1
fi

# Get issue details
ISSUE_DATA=$(gh issue view "$ISSUE_NUMBER" --json title,body,labels,number,state)

# Extract fields
ISSUE_TITLE=$(echo "$ISSUE_DATA" | jq -r '.title')
ISSUE_BODY=$(echo "$ISSUE_DATA" | jq -r '.body')
ISSUE_STATE=$(echo "$ISSUE_DATA" | jq -r '.state')
LABELS=$(echo "$ISSUE_DATA" | jq -r '[.labels[].name] | join(",")')
```

### Step 2: Check for AI Analysis Label

```bash
# Check if issue has ai-analyzed label
if echo "$LABELS" | grep -q "ai-analyzed"; then
  HAS_AI_ANALYSIS=true
else
  HAS_AI_ANALYSIS=false
fi
```

### Step 3: Fetch AI Analysis Comment (if exists)

```bash
if [ "$HAS_AI_ANALYSIS" = true ]; then
  # Get repository name with owner
  REPO_NAME=$(gh repo view --json nameWithOwner --jq .nameWithOwner)

  # Fetch AI analysis comment from github-actions bot
  AI_ANALYSIS=$(gh api "repos/$REPO_NAME/issues/$ISSUE_NUMBER/comments" \
    --jq '.[] | select(.user.login == "github-actions[bot]" and (.body | contains("AI Issue Analysis"))) | .body')

  if [ -n "$AI_ANALYSIS" ]; then
    AI_ANALYSIS_FOUND=true
  else
    AI_ANALYSIS_FOUND=false
  fi
else
  AI_ANALYSIS=""
  AI_ANALYSIS_FOUND=false
fi
```

### Step 4: Return Structured Output

Output as JSON for easy parsing by conductor:

```json
{
  "issue": {
    "number": 137,
    "title": "Add user dark mode preference toggle",
    "body": "User wants to...",
    "state": "open",
    "labels": ["feature", "frontend", "ai-analyzed"]
  },
  "aiAnalysis": {
    "found": true,
    "content": "# AI Issue Analysis\n\n## Architectural Alignment...",
    "sections": {
      "architecturalAlignment": "...",
      "technicalFeasibility": "...",
      "implementationSuggestions": "...",
      "filesAffected": [...],
      "testingStrategy": "..."
    }
  }
}
```

### Step 5: Parse AI Analysis Sections (Optional)

If AI analysis found, extract key sections:

```bash
# Extract Architectural Alignment section
ARCH_ALIGNMENT=$(echo "$AI_ANALYSIS" | sed -n '/## Architectural Alignment/,/## /p' | sed '$d')

# Extract Technical Feasibility section
TECH_FEASIBILITY=$(echo "$AI_ANALYSIS" | sed -n '/## Technical Feasibility/,/## /p' | sed '$d')

# Extract Implementation Suggestions section
IMPL_SUGGESTIONS=$(echo "$AI_ANALYSIS" | sed -n '/## Implementation Suggestions/,/## /p' | sed '$d')

# Extract Files/Components section
FILES_AFFECTED=$(echo "$AI_ANALYSIS" | sed -n '/## Files/,/## /p' | sed '$d')

# Extract Testing Strategy section
TESTING_STRATEGY=$(echo "$AI_ANALYSIS" | sed -n '/## Testing Strategy/,/## /p' | sed '$d')
```

## Output Format

### Success Case

```json
{
  "status": "success",
  "issue": {
    "number": 137,
    "title": "Add user dark mode preference toggle",
    "state": "open",
    "labels": ["feature", "frontend", "ai-analyzed"]
  },
  "aiAnalysis": {
    "found": true,
    "architecturalAlignment": "Aligns with component-based architecture...",
    "technicalFeasibility": "High - uses existing React patterns...",
    "implementationSuggestions": "1. Add darkMode to state\n2. Create toggle component...",
    "filesAffected": ["src/components/Settings.tsx", "src/context/WorldContext.tsx"],
    "testingStrategy": "Unit tests for toggle, integration tests for persistence"
  }
}
```

### No AI Analysis Case

```json
{
  "status": "success",
  "issue": {
    "number": 123,
    "title": "Fix character portrait loading",
    "state": "open",
    "labels": ["bug", "frontend"]
  },
  "aiAnalysis": {
    "found": false
  }
}
```

## Integration with Conductor

Used in conductor Phase 1, Step 1:

```markdown
**Step 1: Issue Selection**

If issue number provided by user:

Use `fetch-github-issue-analysis` skill:
- Input: issue_number
- Output: issue details + AI analysis (if available)

If AI analysis found:
  ✅ Use AI insights for architecture planning
  📋 Extract: architectural alignment, implementation suggestions, testing strategy
  → Skip orchestrator selection, proceed to architecture review

If no AI analysis:
  → Delegate to orchestrator for issue selection logic
```

## Error Handling

### Issue Not Found

```json
{
  "status": "error",
  "error": "Issue #999 not found",
  "code": "NOT_FOUND"
}
```

### Issue Closed

```json
{
  "status": "warning",
  "issue": {...},
  "warning": "Issue is closed - confirm before proceeding"
}
```

### Rate Limit

```json
{
  "status": "error",
  "error": "GitHub API rate limit exceeded",
  "code": "RATE_LIMIT",
  "retryAfter": 3600
}
```

## Related Skills

- `parse-ai-analysis` - Deep parsing of AI analysis sections
- `select-optimal-issue` - Backlog selection when no issue specified
- `create-tracking-issue` - Create new issues

## Examples

### Example 1: Issue with AI Analysis

```bash
# Input
fetch-github-issue-analysis 137

# Output
{
  "status": "success",
  "issue": {
    "number": 137,
    "title": "Add user dark mode preference toggle"
  },
  "aiAnalysis": {
    "found": true,
    "architecturalAlignment": "Aligns with React Context patterns..."
  }
}
```

### Example 2: Issue without AI Analysis

```bash
# Input
fetch-github-issue-analysis 123

# Output
{
  "status": "success",
  "issue": {
    "number": 123,
    "title": "Fix character portrait loading"
  },
  "aiAnalysis": {
    "found": false
  }
}
```

## Best Practices

1. **Always check issue state** - Warn if closed
2. **Cache AI analysis** - Avoid repeated API calls
3. **Handle rate limits** - Implement exponential backoff
4. **Validate JSON output** - Ensure well-formed response
5. **Extract sections carefully** - AI analysis format may vary

## Notes

- AI analysis format is defined by github-actions bot
- Comment must contain "AI Issue Analysis" heading
- Sections may vary based on issue type
- Always validate AI analysis exists before parsing sections
