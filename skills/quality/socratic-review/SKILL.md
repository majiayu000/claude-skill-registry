---
name: socratic-review
description: "Socratic code review using probing questions instead of direct critique. Based on Feynman's principle that teaching reveals gaps in understanding. Helps developers articulate reasoning, surface hidden assumptions, and discover issues themselves."
allowed-tools: ["Read", "Grep", "Glob", "Bash", "Task", "AskUserQuestion"]
user-invocable: true
auto-activation:
  priority: 3
  keywords: ["socratic review", "question my code", "help me understand my code", "dialogue review"]
---

# Socratic Code Review

You are initiating a Socratic code review session. Instead of telling the developer what's wrong, you'll ask probing questions that help them discover issues and articulate their reasoning.

## When to Use This Skill

Use Socratic review when:

- You want deeper understanding, not just compliance
- The developer should own the insights (learning > fixing)
- Design decisions need articulation and documentation
- You want to surface hidden assumptions
- The code is complex and needs explanation
- You're mentoring or onboarding

Use traditional review when:

- Time is critical and you need fast feedback
- Issues are obvious and straightforward
- You need a written report for documentation
- The developer explicitly wants direct feedback

## Usage

```bash
# Basic usage - reviews file with standard depth (7-10 questions)
/socratic-review path/to/file.py

# Quick review - 3-5 focused questions
/socratic-review path/to/file.py --depth=quick

# Deep review - 15-20 comprehensive questions
/socratic-review path/to/file.py --depth=deep

# Review specific function/class
/socratic-review path/to/file.py --focus="function_name"

# Review a directory
/socratic-review src/auth/

# Non-interactive mode (for CI/subprocess - asks all questions, synthesizes without waiting)
/socratic-review path/to/file.py --non-interactive

# Output structured JSON for programmatic processing
/socratic-review path/to/file.py --non-interactive --output=review.json

# Write insights to DECISIONS.md
/socratic-review path/to/file.py --write-decisions
```

## How It Works

### 1. Context Analysis

First, I'll analyze the code to understand:

- What files/functions are being reviewed
- Complexity level and patterns used
- Areas that warrant deeper questions

### 2. Question Selection

Based on the code, I'll select questions from six categories:

- **Design**: Why was this approach chosen?
- **Edge Cases**: What happens in unusual situations?
- **Clarity**: How would you explain this?
- **Philosophy**: Does this follow project principles?
- **Failure Modes**: What could go wrong?
- **Testing**: How do you know it works?

### 3. Dialogue

I'll ask questions one at a time and wait for your responses:

```
**Q1** [Category: Design]
Why did you choose to store session data in memory rather than a database?

[WAIT FOR YOUR RESPONSE]
```

After each answer, I may:

- Ask a follow-up question if the answer reveals uncertainty
- Move to the next question if understanding is solid
- Note insights for the final synthesis

### 4. Synthesis

After all questions, I'll summarize:

- **Insights Revealed**: What became clear through dialogue
- **Assumptions Surfaced**: Hidden assumptions that were exposed
- **Recommendations**: What should change based on the dialogue
- **Strengths**: What you clearly understood well

## Depth Levels

### Quick (3-5 questions, ~5 min)

Best for:

- Small bug fixes
- Simple changes
- Obvious code

Focus: Highest-risk areas only

### Standard (7-10 questions, ~15 min)

Best for:

- Feature implementations
- Refactoring
- Typical PRs

Focus: All question categories covered

### Deep (15-20 questions, ~30 min)

Best for:

- Security-sensitive code
- Core infrastructure
- Architectural changes

Focus: Comprehensive with follow-ups

## Example Session

```markdown
## Socratic Review: auth/login.py

I'm going to ask you some questions about this login implementation.
There are no wrong answers - the goal is to think through the design together.

---

**Q1** [Category: Design]
I see you're storing session data in an in-memory dictionary.
Why did you choose this approach over Redis or database storage?

> Your answer: "It was simpler to implement and we don't have many users yet."

That makes sense for simplicity. **Follow-up**: What would trigger you to
migrate to a different storage mechanism?

> Your answer: "Um... I guess when we scale? Or add multiple servers?"

**Insight noted**: Migration criteria aren't clearly defined.

---

**Q2** [Category: Edge Case]
What happens if a user's session expires while they're submitting a form?

> Your answer: "I... actually haven't thought about that."

**Insight noted**: Session timeout during active use is unhandled.

---

[... more questions ...]

---

## Review Synthesis

### Insights Revealed

- Session storage is pragmatic but migration path unclear
- Session timeout during active use is unhandled

### Assumptions Surfaced

- Single server deployment assumption
- Users won't have long form submissions

### Recommendations

1. Document session storage migration criteria
2. Add graceful session timeout handling

### Strengths Identified

- Clear awareness of simplicity trade-offs
- Quick recognition of gaps when prompted
```

## Integration with Workflow

Socratic review can replace standard review at Step 11 of DEFAULT_WORKFLOW:

```markdown
Step 11: Review the Code

Choose review approach:
A) Standard review - Direct feedback from reviewer agent
B) Socratic review - Dialogue with socratic-reviewer agent

Use Socratic when:

- Learning is as important as fixing
- Design decisions need documentation
- Mentoring/onboarding context
```

## Tips for Good Responses

When answering questions:

1. **Be specific**: "It handles null by returning empty array" is better than "It should be fine"
2. **Acknowledge uncertainty**: "I'm not sure what happens" is valuable - it reveals gaps
3. **Think out loud**: Explain your reasoning, not just the answer
4. **Ask for clarification**: If a question is unclear, say so

## Feedback Loop: How Insights Return

The key question: how do insights from dialogue become actual improvements?

### Interactive Mode (Default)

During live dialogue:

1. Each question and response is captured
2. Insights are noted inline
3. At the end, a synthesis is produced
4. You can use `--write-decisions` to persist insights to DECISIONS.md

### Non-Interactive Mode (CI/Subprocess)

For automated contexts:

1. All questions are asked rhetorically
2. Agent analyzes code to identify likely issues
3. Structured JSON output is produced
4. Output can be posted to PR comments automatically

**Auto-Detection:** The skill automatically detects non-interactive contexts (e.g., `claude --print`, CI pipelines, no TTY) and switches to non-interactive mode. This prevents the frustrating pattern of asking questions, waiting for responses that can't come, and exiting INCONCLUSIVE with no useful output.

### Posting to PR

```bash
# Run non-interactive review
/socratic-review src/auth/ --non-interactive --output=review.json

# Post results to PR
gh pr comment 123 --body "$(jq -r '.synthesis | "## Socratic Review\n\n### Insights\n" + (.insights_revealed | map("- " + .) | join("\n")) + "\n\n### Recommendations\n" + (.recommendations | map("- [" + .priority + "] " + .description) | join("\n"))' review.json)"
```

### Exit on Inconclusive

If 3 questions go unanswered in interactive mode, the session exits with `INCONCLUSIVE` status. Socratic review requires willing participation - without it, exit cleanly rather than pretend to do something else. The user can then choose to run traditional `/review` instead.

## What This Is NOT

- **Not a test**: There are no wrong answers
- **Not criticism**: Questions explore, not judge
- **Not a checklist**: Questions adapt to your code and answers
- **Not replacement for tests**: This is for understanding, not verification

## Underlying Philosophy

This skill is based on:

1. **Feynman Technique**: Teaching reveals gaps in understanding
2. **Socratic Method**: Questions create deeper insight than answers
3. **Rubber Duck Debugging**: Explaining forces thoroughness
4. **Pair Programming**: Dialogue catches what solo work misses

## Related

- **Agent**: `~/.amplihack/.claude/agents/amplihack/specialized/socratic-reviewer.md`
- **Traditional Review**: `/reviewing-code` skill for direct feedback
- **Philosophy Check**: `philosophy-guardian` agent for compliance

## Execution

When this skill is invoked:

1. Parse arguments (file path, depth level, focus)
2. Read and analyze the target code
3. Invoke the socratic-reviewer agent with context
4. Facilitate the dialogue, waiting for user responses
5. Synthesize findings at the end

```
Task(
  subagent_type="socratic-reviewer",
  prompt="Conduct Socratic review of [file] at [depth] level. Focus on: [areas]"
)
```

The agent will handle the question flow and wait for responses using [WAIT] markers.
