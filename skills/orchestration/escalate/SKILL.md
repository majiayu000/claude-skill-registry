---
name: escalate
description: Use when stuck in circles and want to hand off to another agent (Codex CLI) with full context
disable-model-invocation: true
---

# Escalate

Generate a handoff prompt for another agent when you're stuck and need fresh perspective.

## When to Use

- You've tried multiple approaches and keep hitting the same walls
- You're going in circles and want a fresh perspective
- You need to context-switch but want to preserve progress for Codex CLI or another agent

## Workflow

```
/escalate → Choose detail level → Choose handoff mode → Analyze session → Generate prompt → pbcopy
```

## Step 1: Ask Detail Level

Use `AskUserQuestion` to ask:

```
How much context for the handoff?

1. Concise (~200-400 words) - Problem, key blockers, clear ask
2. Detailed (~500-800 words) - Above plus files, errors, code snippets
```

## Step 2: Ask Handoff Mode

Use `AskUserQuestion` to ask:

```
What should the next agent do?

1. Continue - Pick up where I left off and solve this
2. Fresh perspective - Ignore my approaches, try something new
3. Validate first - Confirm my understanding, then propose alternatives
4. Other - [let user specify custom instruction]
```

## Step 3: Analyze the Session

Review the conversation to extract:

| Section | What to Capture |
|---------|-----------------|
| **Problem** | The core objective - what you're trying to accomplish |
| **Approaches Tried** | Each attempt and why it didn't work |
| **Current Hypothesis** | What you think might be the root cause |
| **Relevant Files** | Key file paths that are central to the issue |
| **Error Messages** | Specific errors encountered (exact text) |
| **Constraints** | Things that must be preserved or avoided |

**For concise mode:** Focus on Problem, Approaches Tried, and one key blocker.

**For detailed mode:** Include all sections with code snippets and full error messages.

## Step 4: Generate the Prompt

### Template

```markdown
# Problem

[Clear statement of what you're trying to accomplish]

# Approaches Tried

- **Approach 1:** [what you tried]
  - Result: [what happened]
  - Why it failed: [analysis]

- **Approach 2:** [what you tried]
  - Result: [what happened]
  - Why it failed: [analysis]

[Continue for each significant approach]

# Current Hypothesis

[What you think might be the root cause or blocker]

# Relevant Context

**Files:**
- `path/to/file.ts` - [why it's relevant]
- `path/to/other.ts` - [why it's relevant]

**Errors:**
```
[Exact error messages]
```

**Constraints:**
- [Things that must be preserved]
- [Approaches to avoid and why]

# Your Task

[Based on handoff mode:]

- Continue: "Pick up where I left off. The context above shows what's been tried. Find a path forward and solve this."
- Fresh perspective: "Ignore the approaches above - they haven't worked. Look at this problem fresh and propose a different strategy."
- Validate first: "First, confirm whether my understanding of the problem is correct. Then propose an alternative approach."
- Other: [User's custom instruction]
```

## Step 5: Copy to Clipboard

```bash
echo "[generated prompt]" | pbcopy
```

Use a heredoc for multi-line content:

```bash
pbcopy << 'EOF'
[generated prompt content]
EOF
```

## Step 6: Confirm

Tell the user:

```
Handoff prompt copied to clipboard. Paste into Codex CLI to continue.
```

## Quality Checklist

- [ ] Problem statement is clear and self-contained
- [ ] Approaches include WHY they failed, not just WHAT was tried
- [ ] Hypothesis is specific, not vague
- [ ] File paths are absolute or repo-relative
- [ ] Error messages are exact, not paraphrased
- [ ] Constraints call out landmines to avoid
- [ ] Handoff instruction matches selected mode

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Vague problem statement | Be specific about the goal and success criteria |
| Listing approaches without failure analysis | Always explain WHY each approach didn't work |
| Missing context | Include enough that the next agent doesn't need to ask clarifying questions |
| Too much detail in concise mode | Ruthlessly cut to ~300 words for concise |
| Forgetting constraints | Warn about approaches that look promising but have been ruled out |

## Example Output (Concise)

```markdown
# Problem

Trying to get Jest tests to run in a WordPress plugin. Tests pass locally but fail in CI with "Cannot find module '@wordpress/scripts'" errors.

# Approaches Tried

- **Verified node_modules:** Confirmed package is installed, same versions local and CI
- **Cleared CI cache:** Rebuilt from scratch, same error
- **Checked path resolution:** Added moduleNameMapper in jest.config.js, no change

# Current Hypothesis

CI environment might have different NODE_PATH or module resolution behavior. The @wordpress/scripts package uses a nested dependency structure.

# Your Task

Pick up where I left off. The context above shows what's been tried. Find a path forward and solve this.
```
