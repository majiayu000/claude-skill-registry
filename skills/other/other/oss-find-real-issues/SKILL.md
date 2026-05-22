---
name: oss-find-real-issues
description: |
  Find actual code issues in a repo that aren't listed in GitHub issues. missing tests,
  inconsistent patterns, outdated dependencies, documentation gaps. Presents findings to
  the user for evaluation. Use when you want to make proactive contributions beyond
  existing issues, or when no good issues are available.
---

# Find Real Issues

Don't wait for someone to file an issue. find real problems in the code. This skill analyzes a codebase for actual issues that maintainers would appreciate being fixed: missing tests, inconsistent patterns, silent failures, documentation gaps. You evaluate whether they're worth filing. the LLM just finds them.

## Purpose

The best contributions aren't always in the issue tracker. Experienced contributors earn maintainer trust by finding and fixing problems nobody asked about. but that everyone benefits from. This skill teaches you to read code critically, spot patterns that are off, and evaluate whether a fix would be welcome.

## Prerequisites

- A repo cloned locally
- Basic understanding of the codebase (from `oss-prep-to-contribute` or your own exploration)
- Check that the repo accepts unsolicited PRs (some don't. verify in CONTRIBUTING.md)

## Process

### 1. Check if unsolicited contributions are welcome

Before analyzing anything:

```bash
# Read contribution guidelines
gh api repos/{owner}/{repo}/contents/CONTRIBUTING.md --jq '.content' | base64 -d 2>/dev/null

# Check if unsolicited PRs have been merged before
gh pr list -R {owner}/{repo} --state merged --limit 20 \
  --json title,labels,authorAssociation | \
  jq '[.[] | select(.authorAssociation != "MEMBER" and .authorAssociation != "OWNER")]'
```

Look for:
- "Please file an issue before submitting a PR": if present, you should file an issue first, not just submit a fix
- "We welcome contributions": green light
- No external PRs merged. yellow flag, ask in their communication channel first

Inform the user about the repo's stance on unsolicited contributions.

### 2. Systematic code analysis

Use Explore agents to analyze the codebase across multiple dimensions. For each dimension, look for concrete, specific problems. not vague "could be better" observations.

**Dimension 1: Test coverage gaps**

```bash
# Find source files without corresponding test files
find src/ lib/ -name "*.{ts,py,go,rs}" | while read f; do
  test_file=$(echo "$f" | sed 's/src/test/' | sed 's/\.ts/.test.ts/' | sed 's/\.py/test_&/')
  [ ! -f "$test_file" ] && echo "No test: $f"
done

# Find exported functions that aren't tested
# {language-specific analysis}
```

**Dimension 2: Error handling gaps**

```bash
# Find try/catch or error handling patterns and look for inconsistencies
grep -rn "catch\|except\|Error\|panic\|unwrap" src/ --include="*.ts" --include="*.py" --include="*.go" --include="*.rs" | head -30

# Find functions that call external services/APIs without error handling
# {trace external calls}
```

**Dimension 3: Inconsistent patterns**

```bash
# Compare naming conventions across modules
grep -rn "function\|def \|fn \|func " src/ --include="*.ts" --include="*.py" --include="*.go" --include="*.rs" | head -30
# Look for: camelCase vs snake_case mixing, inconsistent prefixes, different error types for the same kind of failure

# Find multiple approaches to the same problem
# Example: some modules use callbacks, others use promises, others use async/await
grep -rn "callback\|\.then(\|async " src/ --include="*.ts" --include="*.py" --include="*.go" --include="*.rs" | head -20

# Check for deprecated API usage
grep -rn "deprecated\|@deprecated\|DEPRECATED" src/ --include="*.ts" --include="*.py" --include="*.go" --include="*.rs"
```

**Dimension 4: Documentation gaps**

```bash
# Find README references to files that don't exist
grep -oP '\[.*?\]\(((?!http).*?)\)' README.md 2>/dev/null | while read link; do
  file=$(echo "$link" | grep -oP '\(.*?\)' | tr -d '()')
  [ ! -f "$file" ] && echo "Broken link: $link -> $file"
done

# Check if setup/install commands in README actually work
# Read the "Getting Started" section and verify each command

# Find public functions/classes without docstrings (Python example)
grep -rn "def \|class " src/ --include="*.py" -A1 | grep -B1 -v '"""' | grep "def \|class "
```

**Dimension 5: Dependency issues**

```bash
# Language-specific vulnerability checks
npm audit 2>/dev/null          # Node.js
pip audit 2>/dev/null          # Python (requires pip-audit)
cargo audit 2>/dev/null        # Rust
go list -m -json all 2>/dev/null | grep -i "deprecated"  # Go
```

### 3. Filter for actionable findings

Not every code smell is worth filing. Filter each finding:

| Keep | Discard |
|------|---------|
| Missing error handling that could cause silent failures | Style preferences ("I'd do it differently") |
| Untested critical code paths | Test coverage for trivial code |
| Documented behavior that doesn't match implementation | Minor doc typos (unless they cause confusion) |
| Security-relevant issues (input validation, auth checks) | Performance "optimizations" without benchmarks |
| Broken examples in docs | Cosmetic issues |
| Deprecated dependency with known vulnerabilities | Version bumps for non-critical deps |

### 4. Present findings to the user

For each finding, present:

```
## Finding #{n}: {one-line summary}

**Category**: {test gap / error handling / inconsistency / docs / security / dependency}
**Severity**: {high. could cause bugs or security issues / medium. code quality / low. cosmetic}
**Location**: `{file}:{line}` 
**What's wrong**: {specific description with code reference}
**Impact**: {what could go wrong because of this}
**Suggested approach**: {high-level. not a code fix, just the direction}
**Would a PR be welcome?**: {yes. clearly a bug / maybe. discuss first / probably not. too opinionated}
```

### 5. Thinking gate: user evaluates each finding

For each finding, ask the user:

> "Look at finding #{n}. I showed you the location and impact above.
> 1. Do you agree this is a real problem? (Look at the code at the location I cited)
> 2. If you were a maintainer, would you merge a PR fixing this?
> 3. What could go wrong if this stays unfixed? (Check the 'Impact' section above)"

**This is the most important part.** The skill isn't just about finding issues. it's about teaching the user to evaluate code critically. Their judgment matters more than the LLM's analysis.

If the user says "yes, fix it" without articulating WHY:

> "Before we proceed. explain why this is a problem. What could go wrong if it stays as-is? A maintainer will ask this in the PR review."

If the user disagrees with a finding:

> "Good. that's a valid call. Can you explain why you think it's not an issue? Understanding why something ISN'T a problem is just as valuable."

### 6. Fetch issue templates

Before filing, check if the repo has issue templates:

```bash
# Check for issue template directory (multiple templates)
gh api "repos/{owner}/{repo}/contents/.github/ISSUE_TEMPLATE" \
  --jq '[.[] | select(.name != "config.yml") | .name]' 2>/dev/null

# Check for single-file issue template
gh api "repos/{owner}/{repo}/contents/ISSUE_TEMPLATE.md" --jq '.content' 2>/dev/null | base64 -d 2>/dev/null
gh api "repos/{owner}/{repo}/contents/.github/ISSUE_TEMPLATE.md" --jq '.content' 2>/dev/null | base64 -d 2>/dev/null
```

**If a template directory exists**: fetch each template file (skip `config.yml`: it's not a template). Templates can be `.md` (with YAML frontmatter) or `.yml` (issue forms). For `.md` templates, parse the YAML frontmatter (`name`, `description`, `labels`). For `.yml` issue forms, parse the top-level `name`, `description`, and `labels` fields directly. Present the available templates:

```
Available issue templates:
1. Bug Report: Report a bug (labels: bug)
2. Feature Request: Suggest an enhancement (labels: enhancement)
3. Documentation: Report a docs issue (labels: documentation)
```

Ask the user: "Which template matches the issue you're filing?" Fetch the selected template and enforce its structure.

**If a single template exists**: use it as the required format.

**If no templates exist**: use the freeform issue format below.

### 7. File issues or proceed to fix

For findings the user validates:

**Option A: File an issue first** (recommended for medium+ changes or repos that require it):

Help the user write an issue description (they write it, LLM reviews). If a template was found in step 6, the description must follow that template's structure.

**Issue writing rules:**
- Title: what's wrong, in under 10 words. Not "Issue with...". State the problem directly
- Body: reproduction steps or code reference, expected vs actual behavior, that's it
- No filler, no "I believe", no "it seems like". State facts
- No AI jargon: "comprehensive", "robust", "fundamental". Cut all of it
- If you can't describe the issue in 5 lines, you don't understand it well enough yet

```bash
gh issue create -R {owner}/{repo} \
  --title "{descriptive title}" \
  --label "{label1}" --label "{label2}" \
  --body "$(cat <<'EOF'
{user's issue description. following template structure if one was found in step 6}
EOF
)"
# Omit --label flags entirely if no labels from template. Use one --label per label.
```

Then → `oss-find-issue` (claim the issue they just filed) → `oss-contribute` → `oss-submit-pr`

**Option B: Fix directly** (for small, obvious fixes in repos that accept unsolicited PRs):

→ `oss-contribute` directly. skip to the implementation phase

### 8. Track findings

Maintain a summary:

```
## Code Analysis: {repo}

| # | Finding | Category | Severity | User verdict | Action |
|---|---------|----------|----------|-------------|--------|
| 1 | Missing null check in auth | Error handling | High | Worth fixing | Filed #456 |
| 2 | Inconsistent date format | Inconsistency | Low | Not worth it | Skip |
| 3 | No test for edge case X | Test gap | Medium | Good find | Will fix with #456 |
```

## Related Skills

- **Next step (file issue)**: → `oss-find-issue`: to claim the issue you just filed
- **Next step (direct fix)**: → `oss-contribute`: to implement the fix
- **Preparation**: ← `oss-explore-repo`: build broad understanding before looking for issues
- **Previous step**: ← `oss-prep-to-contribute`: should understand the codebase first
- **Alternative to**: ← `oss-find-issue`: when no existing issues match your skills, find your own

## Common Rationalizations

| Shortcut | Why It Fails |
|----------|-------------|
| "I found a code smell, let me just fix it and submit a PR" | Uninvited PRs for subjective improvements get rejected. File an issue first. let the maintainer confirm it's wanted before you invest time in a fix. |
| "The security scanner found 50 issues, let me file them all" | Scanner output without analysis is noise. Most findings are false positives or low-severity. Filing 50 issues burns maintainer goodwill. Filter ruthlessly, present only actionable findings. |
| "This is obviously a bug, I don't need the user to evaluate it" | What looks like a bug might be intentional behavior, a known trade-off, or a design decision with context you don't have. The user's evaluation catches these before you embarrass yourself in an issue. |
| "Any test coverage improvement is welcome" | Testing trivial getters or obvious constructors wastes reviewer time. Focus on critical untested code paths. error handling, edge cases, security-relevant logic. |
| "I'll file the issue and fix it in the same PR" | Separate concerns. The issue gets maintainer buy-in. The PR delivers the fix. Combining them skips the "is this actually wanted?" check. |

## Red Flags

- All findings are severity "low". You're finding cosmetic issues, not real problems
- Findings cluster in one file. you may be looking too narrowly; expand to other modules
- User agrees with every finding without pushback. they're not evaluating critically
- Repo's CONTRIBUTING.md says "file an issue before submitting PRs" but user wants to skip straight to fixing

## Verification Checklist

- [ ] Repo accepts unsolicited contributions (verified)
- [ ] Each finding has a specific file:line reference
- [ ] Each finding has a clear impact statement (what could go wrong)
- [ ] User evaluated each finding and gave a reasoned verdict
- [ ] High-severity findings were filed as issues (if repo requires it)
- [ ] Issue descriptions follow repo template (if one exists)
- [ ] Findings summary table maintained with user verdicts and actions

## Anti-patterns

- **DO NOT** file issues for style preferences. "I'd do it differently" is not an issue
- **DO NOT** file issues without checking if the repo wants unsolicited contributions
- **DO NOT** present findings as definitive problems. always let the user evaluate and decide
- **DO NOT** submit fix PRs for issues you haven't filed first (unless the repo explicitly welcomes it)
- **DO NOT** run security scanners and dump the output. analyze, filter, and present only actionable findings
- **DO NOT** treat every finding as equally important. severity and maintainer-welcome-ness matter
