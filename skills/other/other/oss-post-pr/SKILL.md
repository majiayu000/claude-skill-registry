---
name: oss-post-pr
description: |
  Handle PR review feedback - understand reviewer comments, research their concerns,
  and help the user address them. The LLM explains what reviewers want and why; the user
  decides how to respond and writes the code. Use when you receive review comments on
  a submitted PR.
---

# Post-PR Review

Your PR got reviewed. Now what? This skill helps you understand what reviewers are actually asking for, why they're asking for it, and how to address their feedback - without writing the code for you.

## Purpose

Review comments from maintainers are often terse. "Can you use X pattern instead?" doesn't explain WHY X is preferred, or WHERE to find examples of it. This skill bridges that gap: it researches the reviewer's concern, finds examples in the codebase, and explains the reasoning - so you can address feedback intelligently instead of blindly copy-pasting.

## Prerequisites

- A submitted PR with review comments (from `oss-submit-pr`)
- The repo cloned locally with your working branch checked out

## Process

### 1. Fetch all review feedback

```bash
# Get PR reviews
gh pr view {pr-number} -R {owner}/{repo} --json reviews,comments,reviewDecision,statusCheckRollup

# Get review comments (inline code comments)
gh api repos/{owner}/{repo}/pulls/{pr-number}/comments --jq '.[] | {path: .path, line: .line, body: .body, user: .user.login, state: .state}'

# Get PR conversation comments
gh api repos/{owner}/{repo}/issues/{pr-number}/comments --jq '.[] | {body: .body, user: .user.login, createdAt: .created_at}'
```

### 2. Categorize feedback

Sort each piece of feedback into categories:

| Category | What it means | How to handle |
|----------|--------------|---------------|
| **Blocking** | "This must change before merge" | Address immediately |
| **Suggestion** | "Consider doing X" / "nit:" | Evaluate - adopt if it improves the code |
| **Question** | "Why did you do X?" | Explain your reasoning (this tests YOUR understanding) |
| **Style** | "We prefer X convention" | Follow it - this is the repo's house rules |
| **Scope** | "This should be a separate PR" | Split if reviewer insists |

Present the categorized list:

```
## PR Review Summary: #{pr-number}

**Overall decision**: {approved / changes requested / commented}

### Blocking
1. `src/foo.ts:42` - {reviewer}: "{comment}" → **Must fix**
2. ...

### Suggestions
1. `src/bar.ts:15` - {reviewer}: "{comment}" → **Evaluate**
2. ...

### Questions (you need to answer these)
1. {reviewer}: "{question}" → **Explain your reasoning**
```

### 3. Research each blocking comment

For each blocking review comment, investigate what the reviewer actually wants:

```bash
# Find examples of the pattern they're suggesting
grep -rn "pattern_reviewer_mentioned" src/ --include="*.ts" --include="*.py" --include="*.go" --include="*.rs"

# Check if this is a documented convention
grep -r "pattern_name" CONTRIBUTING.md CLAUDE.md .eslintrc* .prettierrc* pyproject.toml

# Look at how similar code handles this elsewhere
# {specific search based on the comment}
```

Present findings for each blocking comment:

```
### Comment: "{reviewer's comment}" at {file}:{line}

**What they want**: {plain language explanation}
**Why**: {the reasoning - found from codebase patterns, docs, or common practice}
**Examples in codebase**: 
- `src/similar.ts:30` - does it this way
- `src/other.ts:55` - another example
**What you need to change**: {describe the change needed, don't write the code}
```

### 4. Thinking gate - user explains each comment

Before the user starts fixing anything:

> "For each blocking comment, tell me:
> 1. What is the reviewer asking for? (Look at the 'What they want' section I researched above)
> 2. Why do they want it that way? (Check the codebase examples I found - what pattern are they pointing to?)
> 3. Do you agree, or do you want to discuss it with them?"

This catches misunderstandings BEFORE the user writes code that still doesn't address the comment. Common failure: user makes a surface-level change that doesn't actually address the deeper concern.

If the user misunderstands a comment:
- Point to the specific example in the codebase: "Look at `src/similar.ts:30` - see how they handle the same case? The reviewer wants you to follow that pattern because {reason}."
- Don't write the fix - show the pattern and let them figure it out.

### 5. Handle questions from reviewers

For review comments that are questions ("Why did you do X?"), the user MUST answer these themselves. But help them formulate a clear response:

> "The reviewer asked why you chose X. Think back to when we investigated the issue - what was your reasoning? Write a clear response explaining your decision."

If the user struggles to explain their own code, that's a signal. Point them back to the relevant investigation from `oss-contribute` and ask what they remember.

### 6. User addresses feedback

The user fixes each blocking comment and responds to questions. During this phase:

**What the LLM DOES**:
- Answer questions about the codebase patterns the reviewer referenced
- Point to more examples if the user needs them
- Review the user's changes when asked (flag issues, don't fix)
- Help the user write response comments (review, don't write)

**What the LLM DOES NOT DO**:
- Write the code changes
- Write review response comments for the user
- Dismiss suggestions without the user evaluating them

**Review response writing rules** (enforce when reviewing user's draft responses):
- Answer the question directly. "I chose X because Y" - done
- No apologizing: "Sorry for the confusion" is noise. Just explain or fix
- No filler: "Great catch!" / "Thanks for pointing that out!" - one line max, then substance
- No AI jargon: "comprehensive", "robust", "leverages" - cut all of it
- If the response is longer than the reviewer's comment, it's probably too long
- Match the reviewer's tone: if they wrote two words, you don't need two paragraphs

### 7. Track progress

Keep a running status:

```
## Review Status

| # | Comment | Category | Status |
|---|---------|----------|--------|
| 1 | "Use X pattern" | Blocking | ✅ Addressed |
| 2 | "Why not Y?" | Question | ✅ Responded |
| 3 | "Consider Z" | Suggestion | ⏳ User evaluating |
| 4 | "Separate PR" | Scope | ❌ Needs discussion |
```

### 8. Re-submit

Once all blocking comments are addressed:

```bash
# Push changes
git push origin {branch-name}

# Respond to review thread (user writes, LLM reviews)
gh pr comment {pr-number} -R {owner}/{repo} --body "{user's response}"

# Request re-review if needed
gh pr edit {pr-number} -R {owner}/{repo} --add-reviewer {reviewer}
```

### 9. If significant rework is needed

If the reviewer requests a fundamentally different approach:

1. Don't panic - this is normal and educational
2. Research the suggested approach (same as step 3 but deeper)
3. Present the alternative approach with its trade-offs
4. Let the user decide whether to rework or discuss further with the reviewer
5. If reworking, hand off to → `oss-contribute` for a fresh investigation of the new approach

## Related Skills

- **Previous step**: ← `oss-submit-pr` - the PR submission
- **If significant rework**: → `oss-contribute` - re-investigate with the new approach
- **If minor fixes**: → `oss-submit-pr` - re-verify and push updates
- **Loop**: This skill may be invoked multiple times per PR as new reviews come in

## Anti-patterns

- **DO NOT** dismiss review comments - every comment from a maintainer has a reason
- **DO NOT** write response comments for the user - they need to explain their own code
- **DO NOT** write the fix for review comments - show the pattern, user writes the code
- **DO NOT** argue with reviewers through the LLM - if the user disagrees, they should discuss directly and respectfully
- **DO NOT** batch all fixes into one response - address each comment individually with its own commit if the repo prefers it
