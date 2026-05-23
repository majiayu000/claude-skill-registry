---
name: blind-review
description: Blind peer review for code - multiple agents critique independently, then synthesize privately to avoid groupthink
triggers:
  - /blind-review
  - blind review
  - peer review
  - multi-agent review
---

# Blind Peer Review Skill

**Based on**: Harvard+Stanford+CMU "LLM Review" paper - blind peer review improves quality while isolation protects originality.

**Key insight**: When agents openly see each other's work, they copy and converge. Blind review + private synthesis prevents groupthink.

## FULLY AUTONOMOUS EXECUTION

Claude executes ALL phases without user intervention. Never ask user to run commands.

---

## Phase 1: Identify Review Target

Determine what to review:
- If user specifies files/PR → use those
- If recent changes exist → review uncommitted changes
- If neither → ask user what to review

```bash
# Get files to review
git diff --name-only HEAD~1  # Recent commit
git diff --name-only         # Uncommitted changes
```

---

## Phase 2: Parallel Independent Reviews (BLIND)

Launch 3 reviewer agents **in parallel** using a SINGLE message with multiple Task tool calls.

**CRITICAL**: Each agent works in ISOLATION - they do NOT see each other's prompts or outputs.

### Reviewer 1: Architecture Strategist
```
Prompt: Review this code from an architectural perspective. Focus on:
- Component boundaries and responsibilities
- Coupling and cohesion
- Design pattern usage
- Scalability concerns

Do NOT suggest implementation details. Only identify structural issues.

Files to review: [FILE_LIST]
```

### Reviewer 2: Pattern Recognition Specialist
```
Prompt: Analyze this code for patterns and anti-patterns. Focus on:
- Code duplication
- Naming consistency
- Common anti-patterns (god objects, shotgun surgery, etc.)
- Adherence to codebase conventions

Do NOT suggest architecture changes. Only identify pattern issues.

Files to review: [FILE_LIST]
```

### Reviewer 3: Domain Expert (project-specific)
```
Prompt: Review this code for domain-specific correctness. For Random Timer:
- Timer logic accuracy
- Redux state management patterns
- React Native/Expo best practices
- Theme system usage

Do NOT suggest pattern changes. Only identify domain issues.

Files to review: [FILE_LIST]
```

### Execution

```typescript
// SINGLE message with 3 parallel Task calls
Task({
  subagent_type: "compound-engineering:review:architecture-strategist",
  prompt: "[Architecture review prompt with files]",
  description: "Blind architecture review"
})

Task({
  subagent_type: "compound-engineering:review:pattern-recognition-specialist",
  prompt: "[Pattern review prompt with files]",
  description: "Blind pattern review"
})

Task({
  subagent_type: "general-purpose",
  prompt: "[Domain review prompt with files]",
  description: "Blind domain review"
})
```

---

## Phase 3: Collect Critiques (NO CROSS-POLLINATION)

Store each agent's output separately. **Do NOT share outputs between phases.**

```
critique_1 = [Architecture Strategist output]
critique_2 = [Pattern Recognition output]
critique_3 = [Domain Expert output]
```

---

## Phase 4: Private Synthesis

A SINGLE synthesis agent receives all critiques and produces final recommendations.

**Key**: The synthesis agent sees critiques but reviewers never saw each other's work.

```
Prompt: You are synthesizing 3 independent code reviews into actionable improvements.

CRITIQUE 1 (Architecture):
{critique_1}

CRITIQUE 2 (Patterns):
{critique_2}

CRITIQUE 3 (Domain):
{critique_3}

Your task:
1. Identify overlapping concerns (high priority)
2. Identify unique insights from each reviewer
3. Resolve any contradictions by explaining trade-offs
4. Produce a prioritized list of improvements
5. For each improvement, provide specific file:line references

Output format:
## High Priority (multiple reviewers flagged)
- Issue: [description]
- Location: [file:line]
- Fix: [specific action]

## Medium Priority (single reviewer, significant)
...

## Low Priority (nice-to-have)
...
```

---

## Phase 5: Execute Improvements (Optional)

If user wants fixes applied:

```
For each High Priority item:
1. Read the file
2. Make the specific edit
3. Mark as complete

For each Medium Priority item:
1. Ask user if they want it applied
2. If yes, execute
```

---

## Output Format

After all phases complete, present:

```markdown
## Blind Peer Review Complete

### Review Scope
- Files reviewed: [count]
- Reviewers: Architecture, Patterns, Domain
- Mode: Blind (isolated) + Private Synthesis

### High Priority Issues
[From synthesis]

### Medium Priority Issues
[From synthesis]

### Low Priority Issues
[From synthesis]

### Consensus Areas
Issues flagged by multiple reviewers:
- [List]

### Unique Insights
- Architecture: [unique finding]
- Patterns: [unique finding]
- Domain: [unique finding]
```

---

## Why This Works

| Traditional Review | Blind Peer Review |
|-------------------|-------------------|
| Reviewers see each other | Reviewers isolated |
| Ideas converge (groupthink) | Ideas stay diverse |
| Later reviewers copy earlier | All reviews original |
| One perspective dominates | All perspectives equal |

The isolation phase protects **originality**.
The synthesis phase captures **quality feedback**.

---

## Automatic Invocation

Claude detects when blind review is appropriate:
- After significant code changes (3+ files modified)
- Before creating PRs with complex changes
- When user mentions "review" in context of recent work

No user commands needed - Claude invokes this skill autonomously when beneficial.

---

## ACT DON'T INSTRUCT

This skill is FULLY AUTONOMOUS:
- Claude launches all agents directly
- Claude collects and synthesizes results
- Claude presents findings
- Claude applies fixes if requested

**NEVER** tell user to run commands or invoke agents manually.
