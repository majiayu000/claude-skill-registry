---
name: learn
description: This skill should be used when the user asks to "save learnings", "remember this for next time", "add this to CLAUDE.md", "update your instructions", or wants to extract lessons from the current conversation.
user-invocable: true
---

# Learn from Conversation

Extract learnings from the current conversation and persist them to CLAUDE.md, skills, or repo-specific documentation.

## What This Skill Does

1. Analyzes the conversation to identify:
   - **User feedback**: Code style, process preferences, tool usage, corrections
   - **Surprising discoveries**: Gotchas, undocumented behavior, non-obvious patterns found while working

2. Summarizes these into actionable rules

3. Updates the appropriate files:
   - **Global** (`~/dotfiles/claude/CLAUDE.md`): General coding style and behavior rules
   - **Skills** (`~/dotfiles/claude/skills/<skill-name>/SKILL.md`): Skill-specific learnings
   - **Current repo** (`AGENTS.md` or `CLAUDE.md`): Repo-specific gotchas and surprising behaviors

4. Commits and pushes the changes

5. If running in a dev container, runs `~/dotfiles/install.sh` to propagate global changes

## Workflow

### 1. Gather Context

If the current repo has an open PR, fetch PR review comments to include in the analysis:

```bash
# Get current repo info
repo=$(gh repo view --json nameWithOwner -q '.nameWithOwner')

# Check for open PR on current branch
pr_number=$(gh pr view --json number -q '.number' 2>/dev/null)

if [ -n "$pr_number" ]; then
  # Fetch PR review comments
  gh api repos/$repo/pulls/$pr_number/comments --paginate

  # Fetch PR review threads for more context
  gh api graphql -f query='
    query {
      repository(owner: "'${repo%/*}'", name: "'${repo#*/}'") {
        pullRequest(number: '$pr_number') {
          reviewThreads(first: 100) {
            nodes {
              comments(first: 10) {
                nodes {
                  body
                  author { login }
                }
              }
            }
          }
        }
      }
    }
  '
fi
```

### 2. Analyze the Conversation

Review the entire conversation looking for:

**User Feedback:**
- **Explicit corrections**: "Don't do X, do Y instead"
- **Style preferences**: "I prefer X over Y"
- **Code review feedback**: Comments pointing out issues with generated code
- **Process feedback**: "You should have done X before Y"
- **Repeated patterns**: Things the user corrected multiple times

**Surprising Discoveries (from working on tasks):**
- **Gotchas**: Non-obvious behaviors that caused bugs or confusion
- **Undocumented behavior**: Things that weren't in docs but were discovered through trial/error
- **Counterintuitive patterns**: Code patterns that look wrong but are actually correct (or vice versa)
- **Environment quirks**: Unexpected system, library, or framework behaviors
- **Integration issues**: Surprising interactions between components

Focus on learnings that are:
- Actionable (can be turned into a rule or warning)
- Not already documented
- Likely to help future work

### 3. Draft Updates

For each learning, draft a concise rule:

- Use imperative mood ("Use X", not "You should use X")
- Be specific (include examples where helpful)
- Keep it brief (one line if possible, a few bullets if needed)

Group related learnings under existing sections in CLAUDE.md when possible.

### 4. Determine Where to Add

**Add to `~/dotfiles/claude/CLAUDE.md` (global) if:**
- It's a general coding style rule
- It's a general behavior or process rule
- It applies across projects

**Add to a skill file (`~/dotfiles/claude/skills/<skill>/SKILL.md`) if:**
- It's specific to a particular workflow (commit, PR review, etc.)
- It only applies when using that skill

**Add to the current repo's `AGENTS.md` or `CLAUDE.md` if:**
- It's specific to this codebase (gotchas, quirks, non-obvious patterns)
- It documents surprising behavior discovered while working
- It would help future Claude sessions working on this repo
- It's something that "I wish I knew before starting"

Prefer `AGENTS.md` if it exists; otherwise use `CLAUDE.md`. Create the file if neither exists and the learning is valuable enough.

### 5. Read Current Files

Read the target file(s) to understand their structure:

```bash
# Global rules
cat ~/dotfiles/claude/CLAUDE.md

# Skill-specific
cat ~/dotfiles/claude/skills/<skill-name>/SKILL.md

# Current repo (check which exists)
cat AGENTS.md 2>/dev/null || cat CLAUDE.md 2>/dev/null || echo "No repo instructions file"
```

### 6. Apply Updates

Edit the file to add the new rules:
- Add to existing sections when there's a good fit
- Create new sections only when necessary
- Maintain consistent formatting with the rest of the file

### 7. Commit and Push

**For global/skill updates (dotfiles repo):**
```bash
cd ~/dotfiles
git add -A
git commit -m "Add learnings from conversation

<brief summary of what was added>

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
git push
```

**For current repo updates:**
```bash
# In the current repo (not dotfiles)
git add AGENTS.md CLAUDE.md 2>/dev/null
git commit -m "Document learnings from Claude session

<brief summary of gotchas/discoveries added>

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
git push
```

If updating both dotfiles and the current repo, make separate commits in each.

### 8. Propagate Changes (Dev Containers)

If running inside a dev container, run install.sh to propagate the updated CLAUDE.md:

```bash
# Check if we're in a dev container (not the dotfiles repo itself)
if [ -f /.dockerenv ] && [ "$PWD" != "$HOME/dotfiles" ] && [ "$PWD" != "/workspaces/dotfiles" ]; then
  ~/dotfiles/install.sh
fi
```

## Example Learnings

### Global CLAUDE.md (user feedback)

From a conversation where the user corrected test mocking practices:

```markdown
## Testing (pytest)
- Mock only at external boundaries (I/O, network, external libraries), not internal implementation details
- Prefer real data structures over MagicMock for return values
```

From PR feedback about error handling:

```markdown
## Python Style
- Fail early: prefer code that fails immediately over code that logs a warning and potentially behaves incorrectly later
```

### Repo AGENTS.md/CLAUDE.md (surprising discoveries)

From debugging a test failure:

```markdown
## Gotchas
- The `process_data()` function silently returns `None` if the input list is empty instead of raising an error
- Database migrations must be run with `--fake-initial` on first deploy due to legacy schema
```

From discovering undocumented API behavior:

```markdown
## API Notes
- The `/users` endpoint returns max 100 results even without pagination params (undocumented limit)
- Rate limiting kicks in at 50 req/min per IP, not per API key as docs suggest
```

## Notes

- Only extract learnings that are clearly intentional feedback, not off-hand comments
- When in doubt about whether something is a general rule or project-specific, ask the user
- If a learning contradicts an existing rule in CLAUDE.md, ask the user which should take precedence
- Don't add overly specific or one-off preferences that won't generalize
- For repo-specific learnings, focus on things that would save future sessions time/frustration
- Surprising discoveries should be documented even if the user didn't explicitly ask—these are valuable for future work
