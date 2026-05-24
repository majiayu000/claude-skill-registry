---
name: sharing-skills
description: "Use when contributing skills back to the community. Follow git workflow: sync upstream → create branch → develop skill → test with writing-skills → commit → push → PR. One skill per PR."
---

# Sharing Skills

## Core Principle

Skills that work for you can work for others. Share them upstream so the whole community benefits.

## When to Use This Skill

- You've created a skill that works well
- The skill applies broadly (not project-specific)
- The skill has been tested and validated
- You want to contribute to the community
- You've refined an existing pattern
- You've discovered a valuable technique

## The Iron Law

**ONE SKILL PER PULL REQUEST.**

Multiple skills in one PR are hard to review, harder to discuss, and harder to merge.

## Prerequisites

Before sharing a skill upstream:

### 1. Skill Quality Requirements

```
✅ Skill is tested and validated
✅ Skill applies broadly (not company/project specific)
✅ Skill follows the writing-skills pattern
✅ Skill has been tested with testing-skills-with-subagents
✅ Documentation is complete and clear
✅ Examples are realistic and helpful
✅ No proprietary or sensitive information
```

### 2. Repository Setup

```bash
# Add upstream remote (if not already added)
git remote add upstream https://github.com/superpowers/superpowers.git

# Verify remotes
git remote -v
# Should show:
# origin    https://github.com/yourusername/superpowers.git (fetch)
# origin    https://github.com/yourusername/superpowers.git (push)
# upstream  https://github.com/superpowers/superpowers.git (fetch)
# upstream  https://github.com/superpowers/superpowers.git (push)
```

## The Contribution Workflow

### Step 1: Sync with Upstream

```bash
# Ensure you're on main branch
git checkout main

# Fetch latest from upstream
git fetch upstream

# Merge upstream changes
git merge upstream/main

# Push to your fork
git push origin main
```

**Why sync first?**
- Prevents merge conflicts later
- Ensures you're building on latest code
- Makes PR easier to review

### Step 2: Create Feature Branch

```bash
# Create branch with descriptive name
git checkout -b skill/root-cause-tracing

# Verify branch
git branch
# Should show:
# main
# * skill/root-cause-tracing
```

**Branch naming convention:**
- `skill/[skill-name]` for new skills
- `fix/[skill-name]` for bug fixes
- `docs/[skill-name]` for documentation updates

### Step 3: Develop the Skill

```
📝 DEVELOPMENT Phase

Create skill following writing-skills pattern:

1. Write skill document:
   skills/debugging/root-cause-tracing/SKILL.md

2. Test skill with testing-skills-with-subagents:
   - Create pressure scenarios
   - Test without skill (RED)
   - Test with skill (GREEN)
   - Refine skill based on results

3. Ensure skill is complete:
   - Core Principle ✅
   - When to Use ✅
   - The Iron Law ✅
   - Detailed process ✅
   - Examples ✅
   - Integration with other skills ✅
   - Authority section ✅
   - Your Commitment ✅
   - Bottom Line ✅

4. Remove project-specific details:
   - No company names
   - No proprietary code
   - No internal tools
   - Generic examples only
```

### Step 4: Commit Changes

```bash
# Check status
git status
# Should show:
# new file:   skills/debugging/root-cause-tracing/SKILL.md

# Stage the skill
git add skills/debugging/root-cause-tracing/SKILL.md

# Commit with descriptive message
git commit -m "$(cat <<'EOF'
Add root-cause-tracing skill for debugging

Introduces systematic backward tracing through call chains
to identify original triggers rather than downstream symptoms.

Key features:
- Five-step backward tracing process
- Test pollution detection with binary search
- Real-world examples from performance, data corruption
- Integration with systematic-debugging skill
- Comprehensive troubleshooting patterns

Tested with multiple scenarios including intermittent
failures, performance issues, and test pollution.

EOF
)"
```

**Good commit message:**
- Explains what the skill does
- Describes key features
- Mentions testing
- Uses imperative mood ("Add" not "Added")

### Step 5: Push to Your Fork

```bash
# Push branch to your fork
git push -u origin skill/root-cause-tracing

# Output shows:
# remote: Create a pull request for 'skill/root-cause-tracing' on GitHub...
```

### Step 6: Create Pull Request

```bash
# Using GitHub CLI (if available)
gh pr create \
  --base main \
  --head yourusername:skill/root-cause-tracing \
  --title "Add root-cause-tracing skill" \
  --body "$(cat <<'EOF'
## Summary

Adds a new debugging skill for tracing bugs backward through call chains to find original triggers.

## Motivation

When debugging, we often fix symptoms instead of root causes. This skill provides a systematic approach to trace backward through the call chain until finding the original trigger.

## Key Features

- Five-step backward tracing process
- Test pollution detection with binary search pattern
- Real-world examples (performance, data corruption, intermittent failures)
- Integration with existing debugging skills
- Comprehensive checklists and red flags

## Testing

Tested with testing-skills-with-subagents across multiple scenarios:
- ✅ Performance degradation tracing
- ✅ Data corruption investigation
- ✅ Intermittent test failure diagnosis
- ✅ Test pollution detection

## Related Skills

Builds on:
- systematic-debugging (Step 3: Identify root cause)
- test-driven-development (Write test exposing root cause)

## Checklist

- [x] Follows writing-skills pattern
- [x] Tested with testing-skills-with-subagents
- [x] No project-specific details
- [x] Comprehensive examples
- [x] Integration section complete
- [x] Authority section included

EOF
)"
```

**Or create PR manually on GitHub:**

1. Go to upstream repository
2. Click "New Pull Request"
3. Click "compare across forks"
4. Select your fork and branch
5. Fill in title and description
6. Submit PR

### Step 7: Respond to Review Feedback

```
📬 REVIEW RESPONSE Phase

When maintainers review your PR:

1. Read feedback carefully
   - Understand the concern
   - Don't take it personally
   - Ask questions if unclear

2. Make requested changes:
   ```bash
   # Make edits to skill file
   vim skills/debugging/root-cause-tracing/SKILL.md

   # Commit changes
   git add skills/debugging/root-cause-tracing/SKILL.md
   git commit -m "Address review feedback: clarify tracing steps"

   # Push updates
   git push
   ```

3. Respond to comments:
   - Acknowledge feedback
   - Explain your changes
   - Ask for clarification if needed

4. Update PR description if scope changes

5. Mark conversations as resolved when addressed
```

### Step 8: After Merge

```bash
# Once PR is merged

# Sync your main branch
git checkout main
git fetch upstream
git merge upstream/main
git push origin main

# Delete feature branch (cleanup)
git branch -d skill/root-cause-tracing
git push origin --delete skill/root-cause-tracing

# Celebrate! Your skill is now available to everyone 🎉
```

## Pull Request Best Practices

### PR Title Format

```
✅ GOOD:
- "Add root-cause-tracing skill"
- "Fix typo in test-driven-development skill"
- "Update systematic-debugging examples"

❌ BAD:
- "New skill" (too vague)
- "Updates" (what updates?)
- "Fix bug" (what bug?)
```

### PR Description Template

```markdown
## Summary
Brief description of what this PR does (1-2 sentences)

## Motivation
Why is this skill needed? What problem does it solve?

## Key Features
- Feature 1
- Feature 2
- Feature 3

## Testing
How was this skill tested? What scenarios were validated?

## Related Skills
Which skills does this build on or integrate with?

## Checklist
- [ ] Follows writing-skills pattern
- [ ] Tested with testing-skills-with-subagents
- [ ] No project-specific details
- [ ] Examples are clear and realistic
- [ ] Authority section included
```

### Small, Focused PRs

```
✅ ONE SKILL PER PR:
PR #1: Add root-cause-tracing skill
PR #2: Add test-pollution-detection skill
PR #3: Update systematic-debugging with new examples

❌ MULTIPLE SKILLS IN ONE PR:
PR #1: Add 5 new debugging skills
- Hard to review
- Hard to discuss individual skills
- Hard to merge selectively
```

## Example: Complete Contribution Flow

```bash
# 1. SYNC
git checkout main
git fetch upstream
git merge upstream/main
git push origin main

# 2. BRANCH
git checkout -b skill/condition-based-waiting

# 3. DEVELOP
# Create skills/testing/condition-based-waiting/SKILL.md
# Test with testing-skills-with-subagents
# Refine based on feedback

# 4. COMMIT
git add skills/testing/condition-based-waiting/SKILL.md
git commit -m "Add condition-based-waiting skill for async testing

Introduces pattern for waiting on conditions in async tests
rather than using arbitrary timeouts.

Key features:
- Wait-for-condition pattern with timeout
- Polling strategies (linear, exponential backoff)
- Real-world async scenarios
- Integration with TDD

Tested with multiple async scenarios."

# 5. PUSH
git push -u origin skill/condition-based-waiting

# 6. CREATE PR
gh pr create --title "Add condition-based-waiting skill" \
  --body "Adds skill for handling async conditions in tests..."

# 7. RESPOND TO FEEDBACK
# Make requested changes, commit, push

# 8. AFTER MERGE
git checkout main
git fetch upstream
git merge upstream/main
git branch -d skill/condition-based-waiting
```

## What Makes a Good Contribution?

### ✅ GOOD

```
Skill characteristics:
- Solves a common problem
- Applies broadly across projects
- Well-tested and validated
- Clear, actionable guidance
- Realistic examples
- No proprietary content

Documentation:
- Follows writing-skills pattern
- Comprehensive but concise
- Clear authority section
- Integration with other skills
- Bottom line summary

PR quality:
- One skill per PR
- Clear title and description
- Explains motivation
- Shows testing approach
- Responds to feedback gracefully
```

### ❌ BAD

```
Skill issues:
- Too specific to one project
- Untested or unvalidated
- Vague or unclear guidance
- Unrealistic examples
- Contains proprietary info

Documentation:
- Missing sections
- Inconsistent format
- No examples
- No authority section
- Too verbose or too terse

PR issues:
- Multiple skills in one PR
- Vague title/description
- No testing information
- Defensive about feedback
- Includes unrelated changes
```

## Handling Common Scenarios

### Scenario 1: PR Needs Major Changes

```
Maintainer: "This skill is too specific to Laravel. Can you make it framework-agnostic?"

Response:
"Good point! I'll refactor the examples to show the general pattern
first, then include framework-specific examples (Laravel, Django, Rails)
as alternatives. This will make it more broadly applicable."

Action:
- Refactor skill to be framework-agnostic
- Add framework-specific examples as variations
- Update commit with changes
- Respond when ready for re-review
```

### Scenario 2: Skill Overlaps with Existing

```
Maintainer: "This is similar to systematic-debugging. Can you integrate
or explain the difference?"

Response:
"Great catch! The difference is:
- systematic-debugging: General 5-step process
- root-cause-tracing: Specific technique for Step 3 (Identify)

I'll add a section showing how this skill integrates with
systematic-debugging and when to use each."

Action:
- Add "Integration with systematic-debugging" section
- Clarify when to use root-cause-tracing vs general debugging
- Update examples to show integration
```

### Scenario 3: PR Conflicts with Main

```
GitHub: "This branch has conflicts that must be resolved"

Resolution:
```bash
# Sync with upstream main
git checkout main
git fetch upstream
git merge upstream/main

# Rebase your branch on updated main
git checkout skill/root-cause-tracing
git rebase main

# Resolve conflicts
# Edit conflicting files, then:
git add [resolved-files]
git rebase --continue

# Force push (rebase rewrites history)
git push --force-with-lease

# PR is now conflict-free
```
```

## Integration with Skills

**Required before sharing:**
- `writing-skills` - Create skill following pattern
- `testing-skills-with-subagents` - Validate skill works

**Use with:**
- `git-workflow` - For branch and commit management
- `code-review` - For responding to feedback

**After sharing:**
- Your skill helps the community
- Others can improve and extend it
- You build reputation as contributor

## Common Mistakes

### Mistake 1: Sharing Untested Skills

```
❌ BAD:
"I created this skill, let me share it immediately"

✅ GOOD:
"I created this skill, tested it in 5 scenarios,
refined it based on failures, now ready to share"
```

### Mistake 2: Including Proprietary Content

```
❌ BAD:
Example: "At AcmeCorp, we use our ProprietaryTool to..."

✅ GOOD:
Example: "Using standard debugging tools, we can..."
```

### Mistake 3: Multiple Skills in One PR

```
❌ BAD:
PR: "Add 5 new debugging skills"
- Hard to review individually
- One problem blocks all 5

✅ GOOD:
PR #1: "Add root-cause-tracing skill"
PR #2: "Add test-pollution-detection skill"
- Easy to review separately
- Can merge independently
```

## Contribution Checklist

Before submitting PR:
- [ ] Skill tested with testing-skills-with-subagents
- [ ] Skill applies broadly (not project-specific)
- [ ] Follows writing-skills pattern
- [ ] All sections complete
- [ ] Examples are clear and generic
- [ ] No proprietary content
- [ ] Synced with upstream main
- [ ] One skill per PR
- [ ] Descriptive commit message
- [ ] Clear PR title and description
- [ ] Explains motivation and testing

## Authority

**This skill is based on:**
- Open source contribution best practices
- GitHub flow workflow
- Code review research (Microsoft, Google studies)
- Community contribution guidelines

**Research**: Studies show small, focused PRs are reviewed 3x faster and merged 2x more often.

**Social Proof**: All major open source projects use similar contribution workflows.

## Your Commitment

When contributing skills:
- [ ] I will sync with upstream before starting
- [ ] I will create one skill per PR
- [ ] I will test skills before sharing
- [ ] I will remove project-specific content
- [ ] I will respond to feedback gracefully
- [ ] I will follow the contribution workflow
- [ ] I will help maintain clarity and quality

---

**Bottom Line**: Skills that work for you can work for everyone. Test them thoroughly, keep them generic, submit one per PR, and respond to feedback. Your contributions make the whole community stronger.
