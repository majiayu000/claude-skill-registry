---
name: code-review-assistant
description: Comprehensive PR review using multi-agent swarm with specialized reviewers for security, performance, style, tests, and documentation. Provides detailed feedback with auto-fix suggestions and merge readiness assessment.
tags: [review, pr, github, swarm, essential, tier-1]
version: 1.0.0
---

# Code Review Assistant

## Purpose

Automated comprehensive code review using specialized multi-agent swarm for PRs.

## Specialist Agent

I am a code review coordinator managing specialized review agents.

**Methodology** (Multi-Agent Swarm Review Pattern):
1. Initialize review swarm with specialized agents
2. Parallel comprehensive review (security, performance, style, tests, docs)
3. Run complete quality audit pipeline
4. Aggregate findings with severity ranking
5. Generate fix suggestions with Codex
6. Assess merge readiness with quality gates
7. Create detailed review comment

**Review Agents** (5 specialists):
- **Security Reviewer**: Vulnerabilities, unsafe patterns, secrets
- **Performance Analyst**: Bottlenecks, optimization opportunities
- **Style Reviewer**: Code style, best practices, maintainability
- **Test Specialist**: Test coverage, quality, edge cases
- **Documentation Reviewer**: Comments, API docs, README updates

## Input Contract

```yaml
input:
  pr_number: number (required) or
  changed_files: array[string] (file paths)
  focus_areas: array[enum] (default: all)
    - security
    - performance
    - style
    - tests
    - documentation
  suggest_fixes: boolean (default: true)
  auto_merge_if_passing: boolean (default: false)
```

## Output Contract

```yaml
output:
  review_summary:
    overall_score: number (0-100)
    merge_ready: boolean
    blocking_issues: number
    warnings: number
    suggestions: number
  detailed_reviews:
    security: object
    performance: object
    style: object
    tests: object
    documentation: object
  fix_suggestions: array[code_change]
  merge_decision: enum[approve, request_changes, needs_work]
```

## Execution Flow

```bash
#!/bin/bash
set -e

PR_NUMBER="$1"
FOCUS_AREAS="${2:-security,performance,style,tests,documentation}"
SUGGEST_FIXES="${3:-true}"

REVIEW_DIR="pr-review-$PR_NUMBER"
mkdir -p "$REVIEW_DIR"

echo "================================================================"
echo "Code Review Assistant: PR #$PR_NUMBER"
echo "================================================================"

# PHASE 1: PR Information Gathering
echo "[1/8] Gathering PR information..."
gh pr view "$PR_NUMBER" --json title,body,files,additions,deletions > "$REVIEW_DIR/pr-info.json"

PR_TITLE=$(cat "$REVIEW_DIR/pr-info.json" | jq -r '.title')
CHANGED_FILES=$(cat "$REVIEW_DIR/pr-info.json" | jq -r '.files[].path' | tr '\n' ' ')

echo "PR: $PR_TITLE"
echo "Files changed: $(echo $CHANGED_FILES | wc -w)"

# Checkout PR branch
gh pr checkout "$PR_NUMBER"

# PHASE 2: Initialize Review Swarm
echo "[2/8] Initializing multi-agent review swarm..."
npx claude-flow coordination swarm-init \
  --topology mesh \
  --max-agents 5 \
  --strategy specialized

# Spawn specialized review agents
npx claude-flow automation auto-agent \
  --task "Comprehensive code review of PR#$PR_NUMBER focusing on: $FOCUS_AREAS" \
  --strategy optimal \
  --max-agents 5

# PHASE 3: Parallel Specialized Reviews
echo "[3/8] Executing specialized reviews in parallel..."

# Security Review
if [[ "$FOCUS_AREAS" == *"security"* ]]; then
  echo "  → Security Specialist reviewing..."
  npx claude-flow security-scan . \
    --deep true \
    --check-secrets true \
    --output "$REVIEW_DIR/security-review.json" &
  SEC_PID=$!
fi

# Performance Review
if [[ "$FOCUS_AREAS" == *"performance"* ]]; then
  echo "  → Performance Analyst reviewing..."
  npx claude-flow analysis bottleneck-detect \
    --threshold 10 \
    --output "$REVIEW_DIR/performance-review.json" &
  PERF_PID=$!
fi

# Style Review
if [[ "$FOCUS_AREAS" == *"style"* ]]; then
  echo "  → Style Reviewer checking..."
  npx claude-flow style-audit . \
    --fix false \
    --output "$REVIEW_DIR/style-review.json" &
  STYLE_PID=$!
fi

# Test Review
if [[ "$FOCUS_AREAS" == *"tests"* ]]; then
  echo "  → Test Specialist analyzing..."
  npx claude-flow test-coverage . \
    --detailed true \
    --output "$REVIEW_DIR/test-review.json" &
  TEST_PID=$!
fi

# Documentation Review
if [[ "$FOCUS_AREAS" == *"documentation"* ]]; then
  echo "  → Documentation Reviewer checking..."
  # Check for README updates, JSDoc comments, etc.
  npx claude-flow docs-checker . \
    --output "$REVIEW_DIR/docs-review.json" &
  DOCS_PID=$!
fi

# Wait for all reviews to complete
wait $SEC_PID $PERF_PID $STYLE_PID $TEST_PID $DOCS_PID 2>/dev/null || true

# PHASE 4: Complete Quality Audit
echo "[4/8] Running complete quality audit..."
npx claude-flow audit-pipeline . \
  --phase all \
  --model codex-auto \
  --output "$REVIEW_DIR/quality-audit.json"

# PHASE 5: Aggregate Review Findings
echo "[5/8] Aggregating review findings..."
cat > "$REVIEW_DIR/aggregated-review.json" <<EOF
{
  "pr_number": $PR_NUMBER,
  "pr_title": "$PR_TITLE",
  "reviews": {
    "security": $(cat "$REVIEW_DIR/security-review.json" 2>/dev/null || echo "{}"),
    "performance": $(cat "$REVIEW_DIR/performance-review.json" 2>/dev/null || echo "{}"),
    "style": $(cat "$REVIEW_DIR/style-review.json" 2>/dev/null || echo "{}"),
    "tests": $(cat "$REVIEW_DIR/test-review.json" 2>/dev/null || echo "{}"),
    "documentation": $(cat "$REVIEW_DIR/docs-review.json" 2>/dev/null || echo "{}"),
    "quality_audit": $(cat "$REVIEW_DIR/quality-audit.json")
  }
}
EOF

# Calculate scores
SECURITY_SCORE=$(cat "$REVIEW_DIR/security-review.json" 2>/dev/null | jq '.score // 100')
PERF_SCORE=$(cat "$REVIEW_DIR/performance-review.json" 2>/dev/null | jq '.score // 100')
STYLE_SCORE=$(cat "$REVIEW_DIR/style-review.json" 2>/dev/null | jq '.quality_score // 100')
TEST_SCORE=$(cat "$REVIEW_DIR/test-review.json" 2>/dev/null | jq '.coverage_percent // 100')
QUALITY_SCORE=$(cat "$REVIEW_DIR/quality-audit.json" | jq '.overall_score // 100')

OVERALL_SCORE=$(echo "($SECURITY_SCORE + $PERF_SCORE + $STYLE_SCORE + $TEST_SCORE + $QUALITY_SCORE) / 5" | bc)

# PHASE 6: Generate Fix Suggestions
if [ "$SUGGEST_FIXES" = "true" ]; then
  echo "[6/8] Generating fix suggestions with Codex..."

  # Collect all issues
  ISSUES=$(cat "$REVIEW_DIR/aggregated-review.json" | jq '[.reviews[] | .issues? // [] | .[]]')

  if [ "$(echo $ISSUES | jq 'length')" -gt 0 ]; then
    codex --reasoning-mode "Suggest fixes for code review issues" \
      --context "$REVIEW_DIR/aggregated-review.json" \
      --output "$REVIEW_DIR/fix-suggestions.md"
  fi
fi

# PHASE 7: Assess Merge Readiness
echo "[7/8] Assessing merge readiness..."

CRITICAL_SECURITY=$(cat "$REVIEW_DIR/security-review.json" 2>/dev/null | jq '.critical_issues // 0')
TESTS_PASSING=$(cat "$REVIEW_DIR/quality-audit.json" | jq '.functionality_audit.all_passed // false')

MERGE_READY="false"
MERGE_DECISION="request_changes"

if [ "$CRITICAL_SECURITY" -eq 0 ] && [ "$TESTS_PASSING" = "true" ] && [ "$OVERALL_SCORE" -ge 80 ]; then
  MERGE_READY="true"
  if [ "$OVERALL_SCORE" -ge 90 ]; then
    MERGE_DECISION="approve"
  else
    MERGE_DECISION="approve_with_suggestions"
  fi
fi

# PHASE 8: Create Review Comment
echo "[8/8] Creating review comment..."

cat > "$REVIEW_DIR/review-comment.md" <<EOF
# 🤖 Automated Code Review

**Overall Score**: $OVERALL_SCORE/100
**Merge Ready**: $([ "$MERGE_READY" = "true" ] && echo "✅ Yes" || echo "⚠️ No")

## Review Summary

| Category | Score | Status |
|----------|-------|--------|
| 🔒 Security | $SECURITY_SCORE/100 | $([ "$SECURITY_SCORE" -ge 80 ] && echo "✅" || echo "⚠️") |
| ⚡ Performance | $PERF_SCORE/100 | $([ "$PERF_SCORE" -ge 80 ] && echo "✅" || echo "⚠️") |
| 🎨 Style | $STYLE_SCORE/100 | $([ "$STYLE_SCORE" -ge 80 ] && echo "✅" || echo "⚠️") |
| 🧪 Tests | $TEST_SCORE/100 | $([ "$TEST_SCORE" -ge 80 ] && echo "✅" || echo "⚠️") |
| 📊 Quality | $QUALITY_SCORE/100 | $([ "$QUALITY_SCORE" -ge 80 ] && echo "✅" || echo "⚠️") |

## Detailed Findings

### 🔒 Security Review
$(cat "$REVIEW_DIR/security-review.json" 2>/dev/null | jq -r '.summary // "No issues found ✅"')

### ⚡ Performance Review
$(cat "$REVIEW_DIR/performance-review.json" 2>/dev/null | jq -r '.summary // "No bottlenecks detected ✅"')

### 🎨 Style Review
$(cat "$REVIEW_DIR/style-review.json" 2>/dev/null | jq -r '.summary // "Code style looks good ✅"')

### 🧪 Test Review
- Test Coverage: $TEST_SCORE%
- All Tests Passing: $([ "$TESTS_PASSING" = "true" ] && echo "✅ Yes" || echo "❌ No")

## Fix Suggestions

$(cat "$REVIEW_DIR/fix-suggestions.md" 2>/dev/null || echo "No suggestions needed - code looks great! 🎉")

---

🤖 Generated by Claude Code Review Assistant
EOF

# Post review comment
gh pr comment "$PR_NUMBER" --body-file "$REVIEW_DIR/review-comment.md"

# Approve or request changes
if [ "$MERGE_DECISION" = "approve" ]; then
  gh pr review "$PR_NUMBER" --approve --body "Code review passed! Overall score: $OVERALL_SCORE/100 ✅"
elif [ "$MERGE_DECISION" = "approve_with_suggestions" ]; then
  gh pr review "$PR_NUMBER" --approve --body "Approved with suggestions. See detailed review comment. Score: $OVERALL_SCORE/100 ✅"
else
  gh pr review "$PR_NUMBER" --request-changes --body "Please address review findings before merging. Score: $OVERALL_SCORE/100"
fi

echo ""
echo "================================================================"
echo "Code Review Complete!"
echo "================================================================"
echo ""
echo "Overall Score: $OVERALL_SCORE/100"
echo "Merge Ready: $MERGE_READY"
echo "Decision: $MERGE_DECISION"
echo ""
echo "Review artifacts in: $REVIEW_DIR/"
echo "Review comment posted to PR #$PR_NUMBER"
echo ""
```

## Integration Points

### Cascades
- Part of `/github-automation-workflow` cascade
- Used by `/pr-quality-gate` cascade
- Invoked by `/review-pr` command

### Commands
- Uses: `/swarm-init`, `/auto-agent`, `/security-scan`
- Uses: `/bottleneck-detect`, `/style-audit`, `/test-coverage`
- Uses: `/audit-pipeline`, `/codex-reasoning`
- Uses GitHub CLI: `gh pr view`, `gh pr checkout`, `gh pr comment`, `gh pr review`

### Other Skills
- Invokes: `quick-quality-check`, `smart-bug-fix` (if issues)
- Output to: `merge-decision-maker`, `pr-enhancer`

## Usage Example

```bash
# Review PR with all checks
code-review-assistant 123

# Review focusing on security
code-review-assistant 123 security

# Review with auto-merge
code-review-assistant 123 "security,tests" true --auto-merge true
```

## Failure Modes

- **PR not found**: Verify PR number and repository access
- **Critical security issues**: Block merge, escalate to security team
- **Tests failing**: Request changes, provide fix suggestions
- **GitHub CLI not authenticated**: Guide user to authenticate
