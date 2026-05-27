---
name: codex
description: Run OpenAI Codex CLI as a subagent for second opinions, code reviews, and questions. Use when you want a different AI model's perspective.
---

# Codex Subagent

Run OpenAI Codex CLI (GPT-5.2) for second opinions and external reviews.

## Availability Check

Before using Codex, verify it's installed:

```bash
which codex >/dev/null 2>&1 || echo "CODEX_NOT_INSTALLED"
```

If not installed, inform the user: "Codex CLI is not installed. Skipping Codex review."

## Execution Pattern

```bash
OUTPUT_FILE=$(mktemp)
codex exec \
  --skip-git-repo-check \
  --dangerously-bypass-approvals-and-sandbox \
  -o "$OUTPUT_FILE" \
  "$PROMPT" 2>/dev/null
cat "$OUTPUT_FILE"
rm "$OUTPUT_FILE"
```

### Flags

| Flag | Purpose |
|------|---------|
| `exec` | Non-interactive mode |
| `--skip-git-repo-check` | Run outside git repositories |
| `--dangerously-bypass-approvals-and-sandbox` | No prompts, no sandbox restrictions |
| `-o <file>` | Capture clean output to file |
| `2>/dev/null` | Suppress session info and stderr noise |

### Timeout

Codex can take several minutes for complex prompts. Use 15 minute timeout:

```bash
timeout 900 codex exec --skip-git-repo-check --dangerously-bypass-approvals-and-sandbox -o "$OUTPUT_FILE" "$PROMPT" 2>/dev/null
```

## Usage Examples

### Simple Question

```bash
OUTPUT_FILE=$(mktemp)
codex exec --skip-git-repo-check --dangerously-bypass-approvals-and-sandbox -o "$OUTPUT_FILE" \
  "What are the tradeoffs between Redis and Memcached for session storage?" 2>/dev/null
cat "$OUTPUT_FILE"
rm "$OUTPUT_FILE"
```

### Code Review

```bash
DIFF=$(git diff main...HEAD)
OUTPUT_FILE=$(mktemp)
codex exec --skip-git-repo-check --dangerously-bypass-approvals-and-sandbox -o "$OUTPUT_FILE" \
  "Review this diff for issues:

$DIFF

List concerns with severity (blocking/important/nice-to-have)." 2>/dev/null
cat "$OUTPUT_FILE"
rm "$OUTPUT_FILE"
```

### With Working Directory

```bash
OUTPUT_FILE=$(mktemp)
codex exec --dangerously-bypass-approvals-and-sandbox -C /path/to/repo -o "$OUTPUT_FILE" \
  "Analyze the architecture of this codebase" 2>/dev/null
cat "$OUTPUT_FILE"
rm "$OUTPUT_FILE"
```

### GitHub PR Review

Codex has access to `gh` CLI. Pass the PR URL and let it fetch the diff:

```bash
OUTPUT_FILE=$(mktemp)
timeout 900 codex exec --skip-git-repo-check --dangerously-bypass-approvals-and-sandbox -o "$OUTPUT_FILE" \
  "Review this PR: https://github.com/owner/repo/pull/123

   Use gh CLI to get the diff and review for issues." 2>/dev/null
cat "$OUTPUT_FILE"
rm "$OUTPUT_FILE"
```

## Notes

- Codex uses GPT-5.2, providing genuinely different perspective from Claude
- Each call is stateless - no conversation continuity
- API costs apply per call
- Output may contain duplicates - parse accordingly
