---
name: ai-assisted-operations
description: AI-powered issue operations via gh-models. TRIGGERS - issue summarization, auto-labeling, issue insights.
---

# AI-Powered Issue Operations

**Capability:** AI-assisted issue summarization, auto-labeling, Q&A, and documentation generation using gh-models

**When to use:** Leveraging LLMs for intelligent issue processing and automation

**Installation Required:** `gh extension install github/gh-models`

---

## Quick Start

### List Available Models

```bash
# Show all 29+ models
gh models list

# Popular models for issue operations:
# - openai/gpt-4.1
# - openai/gpt-4o-mini
# - anthropic/claude-3.5-sonnet
```

### Basic Usage

```bash
# Run AI model
gh models run "openai/gpt-4.1" "Your prompt here"

# With multi-line prompt
gh models run "openai/gpt-4.1" "$(cat <<'EOF'
Analyze this issue and suggest improvements:
- Title clarity
- Completeness
- Priority assessment
EOF
)"
```

---

## Common Workflows

### 1. Issue Summarization (88% effectiveness)

```bash
# Get issue content
ISSUE_BODY=$(gh issue view 123 --json body --jq .body)

# Summarize
gh models run "openai/gpt-4.1" "$(cat <<'EOF'
Summarize this issue in 2-3 bullet points:

$ISSUE_BODY
EOF
)"
```

**Use Case:** Creating concise summaries for long issues, weekly reports

---

### 2. Auto-Label Suggestion (89% effectiveness)

```bash
# Get issue content
ISSUE_CONTENT=$(gh issue view 123 --json title,body --jq '{title, body}')

# Available labels
LABELS="bug,feature,documentation,question,enhancement,wontfix,duplicate"

# Suggest labels
gh models run "openai/gpt-4.1" "$(cat <<'EOF'
Suggest 2-3 labels from this list: $LABELS

Issue:
$ISSUE_CONTENT

Respond with comma-separated label names only.
EOF
)"

# Apply suggested labels
gh issue edit 123 --add-label bug,priority:high
```

**Use Case:** Automating issue triage, maintaining consistent labeling

---

### 3. Issue Q&A (91% effectiveness)

```bash
# Knowledge base Q&A
QUERY="How do I use Claude Code plan mode?"

# Search relevant issues
ISSUES=$(gh search issues "$QUERY" --repo=terrylica/claude-code-skills-github-issues --json number,title,body --jq '.')

# Ask AI
gh models run "openai/gpt-4.1" "$(cat <<'EOF'
Answer this question based on these GitHub Issues:

Question: $QUERY

Issues:
$ISSUES

Provide a concise answer with issue references.
EOF
)"
```

**Use Case:** Knowledge base Q&A, finding relevant information across issues

---

### 4. Documentation Generation (86% effectiveness)

```bash
# Get related issues
ISSUES=$(gh search issues --label=feature-request --closed --json title,body --jq '.')

# Generate changelog
gh models run "openai/gpt-4.1" "$(cat <<'EOF'
Generate a user-facing changelog from these closed feature requests:

$ISSUES

Format:
## New Features
- Feature name: Brief description

Keep it concise and user-friendly.
EOF
)"
```

**Use Case:** Generating changelogs, release notes, feature documentation

---

### 5. Issue Classification

```bash
# Get issue
ISSUE=$(gh issue view 123 --json title,body --jq '{title, body}')

# Classify
gh models run "openai/gpt-4.1" "$(cat <<'EOF'
Classify this issue into ONE category:
- Bug Report
- Feature Request
- Documentation
- Question
- Enhancement

Issue:
$ISSUE

Respond with category name only.
EOF
)"
```

---

## Effectiveness Metrics (Empirical Testing)

| Operation                | Effectiveness | Test Count |
| ------------------------ | ------------- | ---------- |
| Issue Summarization      | 88%           | 5 tests    |
| Auto-Label Suggestion    | 89%           | 5 tests    |
| Issue Q&A                | 91%           | 5 tests    |
| Documentation Generation | 86%           | 5 tests    |
| Issue Classification     | 88%           | 5 tests    |

**Average Effectiveness: 88%**

**Detailed Results:** [GH-MODELS-POC-RESULTS.md](/docs/testing/GH-MODELS-POC-RESULTS.md)

---

## Model Selection

**Fast & Cheap (Good for bulk operations):**

- `openai/gpt-4o-mini` - Fast, cost-effective
- `openai/gpt-3.5-turbo` - Balanced

**High Quality (Complex analysis):**

- `openai/gpt-4.1` - Best quality
- `anthropic/claude-3.5-sonnet` - Long context, detailed analysis

**Testing:** Try different models to find best quality/cost tradeoff

---

## Best Practices

1. **Test prompts first** - Verify output quality before automation
2. **Provide context** - Include relevant labels, repo info in prompt
3. **Be specific** - Clear instructions = better results
4. **Iterate** - Refine prompts based on output quality
5. **Validate output** - AI can make mistakes, always verify
6. **Rate limits** - Be aware of API rate limits for batch operations

---

## Limitations

- **API rate limits** - Check GitHub API limits for your account
- **Cost** - Some models have usage costs
- **Accuracy** - Not 100% reliable, human review recommended
- **Context size** - Very long issues may hit token limits
- **No state** - Each call is independent, no conversation memory

---

## Integration Example: Auto-Triage Workflow

```bash
#!/bin/bash
# Auto-triage new issues

# Get new issues
gh issue list --label needs-triage --json number,title,body --jq '.[] | @json' | \
while read -r issue; do
  # Extract fields
  number=$(echo "$issue" | jq -r .number)
  content=$(echo "$issue" | jq -r '{title, body}')

  # Get AI suggestions
  labels=$(gh models run "openai/gpt-4o-mini" "$(cat <<EOF
Suggest 2-3 labels: bug,feature,documentation,question,enhancement
Issue: $content
Respond with comma-separated labels only.
EOF
  )")

  # Apply labels
  gh issue edit "$number" --add-label "$labels" --remove-label needs-triage

  echo "Triaged issue #$number: $labels"
done
```

---

**Installation:** `gh extension install github/gh-models`

**Full Extension Guide:** [GITHUB_CLI_EXTENSIONS.md](/docs/research/GITHUB_CLI_EXTENSIONS.md)

**Complete POC Results:** [GH-MODELS-POC-RESULTS.md](/docs/testing/GH-MODELS-POC-RESULTS.md)
