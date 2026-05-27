---
name: debate-start
description: Start structured red vs. blue team debates via subagents. Use when exploring a topic from multiple adversarial perspectives.
---

# Start Debate Skill

Orchestrate multi-perspective debates on a topic using color-coded team subagents.

> **Reference**: See [reference.md](reference.md) for moderation guidelines and intervention patterns.

---

## When to Use

- Exploring trade-offs in architectural decisions
- Evaluating competing approaches or technologies
- Risk analysis requiring devil's advocate perspectives
- Any topic benefiting from structured adversarial review

---

## Workflow

### Step 1: Initialize Debate

1. Parse topic from user input
2. Create slugs from topic and context (e.g., "API Design" → `api-design`, context max 3 words)
3. Ensure `./debates/` directory exists
4. Create scratchpad from template: `./debates/{topic}_{context}.md`

### Step 2: Configure Teams

Use **AskUserQuestion** to gather team configuration:

**Question 1: Optional Teams (multiSelect: true)**
```
Which additional teams should participate beyond Red and Blue?
- None: Just Red and Blue
- Green Team: Pragmatic/implementation focus
- Yellow Team: Risk/safety analysis
- Purple Team: Synthesis/integration bridge
```

**Question 2: Red Team Stance**
```
What position should Red Team (challenger/skeptic) argue?
```

**Question 3: Blue Team Stance**
```
What position should Blue Team (defender/advocate) argue?
```

**Questions 4-6: Additional team stances** (if selected)

Write all stances to the scratchpad's Team Positions section.

### Step 3: Spawn Opening Arguments (Parallel)

Launch all team subagents **simultaneously** using the Task tool:

```
Task(subagent_type="general-purpose", prompt="""
You are the {COLOR} TEAM in a debate on: {topic}

Your stance: {stance}

## Research Phase
Gather evidence before writing using read-only tools.

**Codebase research:**
- Glob/Grep/Read: Find relevant code, patterns, prior decisions

**External research (encouraged):**
- WebSearch: Find industry practices, benchmarks, expert opinions, case studies
- WebFetch: Retrieve specific documentation, articles, or technical references

For deep research questions, spawn focused subagents:
  Task(subagent_type="general-purpose", prompt="Research {specific question}...")

## Writing Phase
1. Read ./debates/{topic}_{context}.md
2. Edit your section: ### [{COLOR}]
3. Structure: Position → Evidence → Implications
4. Cite sources (files, URLs) for claims

## Constraints
- Read-only tools only (no code modifications)
- Stay on assigned perspective
- Arguments must be evidence-backed
""")
```

### Step 4: Monitor and Moderate

After subagents complete, the main agent:

1. **Read scratchpad** and summarize key points to user
2. **Assess debate health:**
   - Progress: Are teams making new points?
   - Balance: Is one team dominating?
   - Relevance: Staying on topic?
   - Depth: Avoiding superficial arguments?

3. **Intervene if needed** - write to Moderator Notes section:
   - `[MODERATOR] Stuck:` "Team X, consider addressing Y"
   - `[MODERATOR] Tunnel:` "Team X, you've repeated Z"
   - `[MODERATOR] Astray:` "Refocus on core question"
   - `[MODERATOR] Disconnected:` "Team X, respond to Team Y's point"

4. **Ask user** for next action:
   - "Advance to rebuttals?"
   - "Request synthesis round?"
   - "Conclude debate?"

### Step 5: Rebuttal Round (Sequential)

Spawn teams **sequentially** for direct responses:

Order: Red → Blue → Green → Yellow → Purple (active teams only)

Each team's prompt includes instruction to read and respond to specific opposing arguments.

### Step 6: Synthesis Round (Optional)

If requested, spawn Purple Team (or all teams) to find:
- Common ground
- Irreconcilable differences
- Potential compromises

### Step 7: Conclude Debate

Main agent writes Conclusion section:
- **Summary:** Key positions from each team
- **Agreements:** Points of consensus
- **Disagreements:** Unresolved tensions
- **Recommendations:** Suggested path forward (if applicable)

Update scratchpad status to "Completed".

---

## Templates

- [templates/debate-scratchpad.md](templates/debate-scratchpad.md) - Debate file template

---

## Success Criteria

- Scratchpad created at `./debates/{topic}_{context}.md`
- All active teams contributed arguments
- Moderator interventions documented transparently
- User controlled round progression
- Debate concluded with synthesis

---

## Integration

**Command:** `/debate {topic}`

**Related:**
- Tools: Task (subagents), AskUserQuestion (configuration), Edit (scratchpad)
- Pattern: Document-centric coordination via shared scratchpad

---

## Reference

See [reference.md](reference.md) for:
- Team perspective definitions
- Intervention decision tree
- Example debate flows
- Common failure modes
