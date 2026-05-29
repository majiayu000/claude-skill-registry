---
name: complexity-scorer
version: 1.0.0
description: Score task complexity using keyword matching and heuristics
author: workspace-hub
category: bash
tags: [bash, complexity, scoring, keywords, analysis, classification]
platforms: [linux, macos]
---

# Complexity Scorer

Patterns for scoring task complexity using keyword matching, context analysis, and configurable heuristics. Extracted from workspace-hub's model selection system.

## When to Use This Skill

✅ **Use when:**
- Routing tasks to different handlers based on complexity
- Recommending resources (models, workers, time estimates)
- Prioritizing work items
- Auto-classifying incoming requests
- Building intelligent dispatchers

❌ **Avoid when:**
- Simple yes/no classification
- When ML-based classification is more appropriate
- Highly domain-specific scoring that requires expertise

## Core Capabilities

### 1. Keyword-Based Scoring

Define keyword categories with weights:

```bash
#!/bin/bash
# ABOUTME: Keyword-based complexity scoring
# ABOUTME: Pattern from workspace-hub suggest_model.sh

# Keyword categories with associated complexity impact
# High complexity keywords (score +3)
HIGH_COMPLEXITY="architecture|refactor|design|security|complex|multi-file|algorithm|optimization|strategy|planning|cross-repository|performance|migration|integration"

# Medium complexity keywords (score +1)
MEDIUM_COMPLEXITY="implement|feature|bug|fix|code review|documentation|test|update|add|create|build|configure|setup"

# Low complexity keywords (score -2)
LOW_COMPLEXITY="check|status|simple|quick|template|list|grep|find|search|summary|validation|exists|show|display|count|verify"

# Score based on keywords
score_keywords() {
    local text="$1"
    local text_lower=$(echo "$text" | tr '[:upper:]' '[:lower:]')
    local score=0

    # Check high complexity first (mutually exclusive)
    if echo "$text_lower" | grep -qE "$HIGH_COMPLEXITY"; then
        ((score+=3))
    elif echo "$text_lower" | grep -qE "$MEDIUM_COMPLEXITY"; then
        ((score+=1))
    elif echo "$text_lower" | grep -qE "$LOW_COMPLEXITY"; then
        ((score-=2))
    fi

    echo $score
}

# Usage
task="Design the authentication system architecture"
score=$(score_keywords "$task")
echo "Complexity score: $score"  # Output: 3
```

### 2. Multi-Factor Scoring

Combine multiple factors for better accuracy:

```bash
#!/bin/bash
# ABOUTME: Multi-factor complexity scoring
# ABOUTME: Combines keywords, length, context

# Factor weights
declare -A WEIGHTS=(
    ["keywords"]=3
    ["length"]=1
    ["urgency"]=1
    ["scope"]=2
)

# Score task length
score_length() {
    local text="$1"
    local word_count=$(echo "$text" | wc -w)

    if [[ $word_count -gt 20 ]]; then
        echo 2  # Long = more complex
    elif [[ $word_count -gt 10 ]]; then
        echo 1
    elif [[ $word_count -lt 5 ]]; then
        echo -1  # Short = simpler
    else
        echo 0
    fi
}

# Score urgency indicators
score_urgency() {
    local text="$1"
    local text_lower=$(echo "$text" | tr '[:upper:]' '[:lower:]')

    if echo "$text_lower" | grep -qE "urgent|asap|critical|emergency|immediately"; then
        echo 2
    elif echo "$text_lower" | grep -qE "soon|priority|important"; then
        echo 1
    else
        echo 0
    fi
}

# Score scope indicators
score_scope() {
    local text="$1"
    local text_lower=$(echo "$text" | tr '[:upper:]' '[:lower:]')

    if echo "$text_lower" | grep -qE "all|every|entire|complete|full|comprehensive"; then
        echo 2
    elif echo "$text_lower" | grep -qE "multiple|several|various|many"; then
        echo 1
    elif echo "$text_lower" | grep -qE "single|one|specific|particular"; then
        echo -1
    else
        echo 0
    fi
}

# Combined scoring
calculate_complexity() {
    local text="$1"
    local total=0

    local keyword_score=$(score_keywords "$text")
    local length_score=$(score_length "$text")
    local urgency_score=$(score_urgency "$text")
    local scope_score=$(score_scope "$text")

    total=$((keyword_score * ${WEIGHTS[keywords]} +
             length_score * ${WEIGHTS[length]} +
             urgency_score * ${WEIGHTS[urgency]} +
             scope_score * ${WEIGHTS[scope]}))

    echo $total
}
```

### 3. Context-Aware Scoring

Adjust scores based on context (repository, domain, etc.):

```bash
#!/bin/bash
# ABOUTME: Context-aware complexity scoring
# ABOUTME: Adjusts based on repository tier, domain

# Repository tiers
TIER1_REPOS="workspace-hub|digitalmodel|energy|frontierdeepwater"
TIER2_REPOS="aceengineercode|assetutilities|worldenergydata|rock-oil-field"
TIER3_REPOS="doris|saipem|OGManufacturing|seanation"
PERSONAL_ACTIVE="aceengineer-admin|aceengineer-website"
PERSONAL_EXPERIMENTAL="hobbies|sd-work|acma-projects"

# Get repository tier
get_repo_tier() {
    local repo="$1"

    if echo "$repo" | grep -qE "$TIER1_REPOS"; then
        echo "tier1"
    elif echo "$repo" | grep -qE "$TIER2_REPOS"; then
        echo "tier2"
    elif echo "$repo" | grep -qE "$TIER3_REPOS"; then
        echo "tier3"
    elif echo "$repo" | grep -qE "$PERSONAL_ACTIVE"; then
        echo "personal_active"
    elif echo "$repo" | grep -qE "$PERSONAL_EXPERIMENTAL"; then
        echo "personal_experimental"
    else
        echo "unknown"
    fi
}

# Adjust score based on context
adjust_for_context() {
    local base_score="$1"
    local repo="$2"
    local adjusted=$base_score

    local tier=$(get_repo_tier "$repo")

    case "$tier" in
        tier1)
            # Production repos bias toward higher quality
            ((adjusted+=1))
            ;;
        tier3|personal_experimental)
            # Maintenance/experimental bias toward efficiency
            ((adjusted-=1))
            ;;
    esac

    echo $adjusted
}

# Full scoring with context
score_with_context() {
    local task="$1"
    local repo="$2"

    local base_score=$(calculate_complexity "$task")
    local final_score=$(adjust_for_context "$base_score" "$repo")

    echo $final_score
}
```

### 4. Score Classification

Map scores to categories:

```bash
#!/bin/bash
# ABOUTME: Map complexity scores to categories
# ABOUTME: Provides actionable classifications

# Classification thresholds
THRESHOLD_HIGH=5
THRESHOLD_MEDIUM=1
THRESHOLD_LOW=-2

# Classify score
classify_complexity() {
    local score="$1"

    if [[ $score -ge $THRESHOLD_HIGH ]]; then
        echo "high"
    elif [[ $score -ge $THRESHOLD_MEDIUM ]]; then
        echo "medium"
    elif [[ $score -ge $THRESHOLD_LOW ]]; then
        echo "low"
    else
        echo "trivial"
    fi
}

# Get recommendation based on classification
get_recommendation() {
    local score="$1"
    local classification=$(classify_complexity "$score")

    case "$classification" in
        high)
            echo "OPUS"
            echo "Use for complex architecture, multi-file refactoring, security analysis"
            ;;
        medium)
            echo "SONNET"
            echo "Standard implementation, code review, documentation"
            ;;
        low)
            echo "HAIKU"
            echo "Quick queries, status checks, simple operations"
            ;;
        trivial)
            echo "HAIKU"
            echo "Trivial task - consider if AI is even needed"
            ;;
    esac
}

# Get color for display
get_score_color() {
    local score="$1"
    local classification=$(classify_complexity "$score")

    case "$classification" in
        high)    echo "$GREEN" ;;
        medium)  echo "$BLUE" ;;
        low)     echo "$YELLOW" ;;
        trivial) echo "$CYAN" ;;
    esac
}
```

### 5. Confidence Scoring

Add confidence to scoring:

```bash
#!/bin/bash
# ABOUTME: Confidence scoring for complexity estimates
# ABOUTME: Indicates reliability of the score

# Calculate confidence
calculate_confidence() {
    local text="$1"
    local confidence=50  # Base confidence

    local word_count=$(echo "$text" | wc -w)
    local keyword_matches=0
    local text_lower=$(echo "$text" | tr '[:upper:]' '[:lower:]')

    # More words = higher confidence (more context)
    if [[ $word_count -gt 15 ]]; then
        ((confidence+=20))
    elif [[ $word_count -gt 8 ]]; then
        ((confidence+=10))
    elif [[ $word_count -lt 3 ]]; then
        ((confidence-=20))
    fi

    # Keyword matches boost confidence
    for pattern in "$HIGH_COMPLEXITY" "$MEDIUM_COMPLEXITY" "$LOW_COMPLEXITY"; do
        if echo "$text_lower" | grep -qE "$pattern"; then
            ((keyword_matches++))
        fi
    done

    ((confidence += keyword_matches * 10))

    # Cap confidence
    [[ $confidence -gt 100 ]] && confidence=100
    [[ $confidence -lt 10 ]] && confidence=10

    echo $confidence
}

# Get confidence label
confidence_label() {
    local confidence="$1"

    if [[ $confidence -ge 80 ]]; then
        echo "High"
    elif [[ $confidence -ge 60 ]]; then
        echo "Medium"
    elif [[ $confidence -ge 40 ]]; then
        echo "Low"
    else
        echo "Very Low"
    fi
}
```

### 6. Historical Learning

Adjust based on past accuracy:

```bash
#!/bin/bash
# ABOUTME: Historical learning for complexity scoring
# ABOUTME: Track and adjust based on actual outcomes

HISTORY_FILE="${HOME}/.complexity-scorer/history.log"

# Log prediction vs actual
log_outcome() {
    local task="$1"
    local predicted_score="$2"
    local actual_complexity="$3"  # user-provided feedback
    local timestamp=$(date '+%Y-%m-%d_%H:%M:%S')

    mkdir -p "$(dirname "$HISTORY_FILE")"
    echo "${timestamp}|${predicted_score}|${actual_complexity}|${task}" >> "$HISTORY_FILE"
}

# Calculate prediction accuracy
calculate_accuracy() {
    local correct=0
    local total=0

    while IFS='|' read -r ts predicted actual task; do
        [[ "$ts" =~ ^#.*$ ]] && continue
        [[ -z "$ts" ]] && continue

        ((total++))

        local predicted_class=$(classify_complexity "$predicted")
        if [[ "$predicted_class" == "$actual" ]]; then
            ((correct++))
        fi
    done < "$HISTORY_FILE"

    if [[ $total -gt 0 ]]; then
        echo $((correct * 100 / total))
    else
        echo 0
    fi
}

# Find common misclassifications
find_patterns() {
    echo "Analyzing misclassification patterns..."

    while IFS='|' read -r ts predicted actual task; do
        local predicted_class=$(classify_complexity "$predicted")
        if [[ "$predicted_class" != "$actual" ]]; then
            echo "Predicted: $predicted_class, Actual: $actual"
            echo "Task: $task"
            echo "---"
        fi
    done < "$HISTORY_FILE"
}
```

## Complete Example: Task Complexity Scorer

```bash
#!/bin/bash
# ABOUTME: Complete task complexity scoring system
# ABOUTME: Multi-factor scoring with recommendations

set -e

# ─────────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────────

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m'

# Keyword patterns
OPUS_KEYWORDS="architecture|refactor|design|security|complex|multi-file|algorithm|optimization|strategy|planning|cross-repository|performance|migration"
SONNET_KEYWORDS="implement|feature|bug|fix|code review|documentation|test|update|add|create|build"
HAIKU_KEYWORDS="check|status|simple|quick|template|list|grep|find|search|summary|validation|exists|show|display"

# Repository tiers
WORK_TIER1="workspace-hub|digitalmodel|energy|frontierdeepwater"
WORK_TIER2="aceengineercode|assetutilities|worldenergydata"
WORK_TIER3="doris|saipem|OGManufacturing"
PERSONAL="hobbies|sd-work|acma-projects"

# ─────────────────────────────────────────────────────────────────
# Scoring Functions
# ─────────────────────────────────────────────────────────────────

score_task() {
    local task="$1"
    local repo="${2:-}"
    local task_lower=$(echo "$task" | tr '[:upper:]' '[:lower:]')
    local score=0

    # Keyword scoring
    if echo "$task_lower" | grep -qE "$OPUS_KEYWORDS"; then
        ((score+=3))
    elif echo "$task_lower" | grep -qE "$SONNET_KEYWORDS"; then
        ((score+=1))
    elif echo "$task_lower" | grep -qE "$HAIKU_KEYWORDS"; then
        ((score-=2))
    fi

    # Length scoring
    local word_count=$(echo "$task" | wc -w)
    if [[ $word_count -gt 15 ]]; then
        ((score+=1))
    elif [[ $word_count -lt 5 ]]; then
        ((score-=1))
    fi

    # Repository tier adjustment
    if [[ -n "$repo" ]]; then
        if echo "$repo" | grep -qE "$WORK_TIER1"; then
            ((score+=1))
        elif echo "$repo" | grep -qE "$WORK_TIER3|$PERSONAL"; then
            ((score-=1))
        fi
    fi

    echo $score
}

get_recommendation() {
    local score="$1"

    if [[ $score -ge 3 ]]; then
        echo "OPUS"
    elif [[ $score -ge 0 ]]; then
        echo "SONNET"
    else
        echo "HAIKU"
    fi
}

get_tier_name() {
    local repo="$1"

    if echo "$repo" | grep -qE "$WORK_TIER1"; then
        echo "Work Tier 1 (Production)"
    elif echo "$repo" | grep -qE "$WORK_TIER2"; then
        echo "Work Tier 2 (Active)"
    elif echo "$repo" | grep -qE "$WORK_TIER3"; then
        echo "Work Tier 3 (Maintenance)"
    elif echo "$repo" | grep -qE "$PERSONAL"; then
        echo "Personal (Experimental)"
    else
        echo "Unknown"
    fi
}

# ─────────────────────────────────────────────────────────────────
# Display Functions
# ─────────────────────────────────────────────────────────────────

display_result() {
    local task="$1"
    local repo="$2"
    local score=$(score_task "$task" "$repo")
    local recommendation=$(get_recommendation "$score")
    local tier=$(get_tier_name "$repo")

    # Determine color
    local color
    case "$recommendation" in
        OPUS)   color=$GREEN ;;
        SONNET) color=$BLUE ;;
        HAIKU)  color=$YELLOW ;;
    esac

    echo ""
    echo -e "${CYAN}═══════════════════════════════════════${NC}"
    echo -e "${CYAN}  Task Complexity Analysis${NC}"
    echo -e "${CYAN}═══════════════════════════════════════${NC}"
    echo ""

    [[ -n "$repo" ]] && echo -e "Repository: ${CYAN}$repo${NC} ($tier)"
    echo -e "Task: $task"
    echo -e "Complexity Score: $score"
    echo ""
    echo -e "Recommended: ${color}${recommendation}${NC}"
    echo ""

    # Reasoning
    echo -e "${CYAN}Reasoning:${NC}"
    local task_lower=$(echo "$task" | tr '[:upper:]' '[:lower:]')

    if echo "$task_lower" | grep -qE "$OPUS_KEYWORDS"; then
        echo "  • High complexity keywords detected"
    elif echo "$task_lower" | grep -qE "$SONNET_KEYWORDS"; then
        echo "  • Standard implementation keywords detected"
    elif echo "$task_lower" | grep -qE "$HAIKU_KEYWORDS"; then
        echo "  • Simple task indicators detected"
    fi

    [[ -n "$tier" ]] && echo "  • Repository tier: $tier"

    echo ""
    echo -e "${CYAN}═══════════════════════════════════════${NC}"
}

# ─────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────

show_usage() {
    cat << EOF
Usage: $(basename "$0") [options] <task-description>

Options:
    -r, --repo REPO    Repository context
    -s, --score-only   Output only the numeric score
    -j, --json         Output as JSON
    -h, --help         Show this help

Examples:
    $(basename "$0") "Check if file exists"
    $(basename "$0") -r digitalmodel "Design authentication architecture"
    $(basename "$0") --score-only "Implement user login"

EOF
}

REPO=""
SCORE_ONLY=false
JSON_OUTPUT=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        -r|--repo)
            REPO="$2"
            shift 2
            ;;
        -s|--score-only)
            SCORE_ONLY=true
            shift
            ;;
        -j|--json)
            JSON_OUTPUT=true
            shift
            ;;
        -h|--help)
            show_usage
            exit 0
            ;;
        -*)
            echo "Unknown option: $1"
            show_usage
            exit 1
            ;;
        *)
            break
            ;;
    esac
done

TASK="$*"

if [[ -z "$TASK" ]]; then
    read -p "Task description: " TASK
fi

if [[ -z "$TASK" ]]; then
    echo "Error: Task description required"
    exit 1
fi

if [[ "$SCORE_ONLY" == true ]]; then
    score_task "$TASK" "$REPO"
elif [[ "$JSON_OUTPUT" == true ]]; then
    score=$(score_task "$TASK" "$REPO")
    rec=$(get_recommendation "$score")
    cat << EOF
{
  "task": "$TASK",
  "repository": "$REPO",
  "score": $score,
  "recommendation": "$rec"
}
EOF
else
    display_result "$TASK" "$REPO"
fi
```

## Best Practices

1. **Tune Keywords** - Adjust patterns based on your domain
2. **Use Multiple Factors** - Don't rely on keywords alone
3. **Add Confidence** - Help users understand reliability
4. **Learn from Feedback** - Track accuracy and improve
5. **Context Matters** - Same task may have different complexity in different contexts

## Resources

- [Regular Expressions in Bash](https://mywiki.wooledge.org/RegularExpression)
- [Pattern Matching](https://www.gnu.org/software/bash/manual/html_node/Pattern-Matching.html)

---

## Version History

- **1.0.0** (2026-01-14): Initial release - extracted from workspace-hub suggest_model.sh
