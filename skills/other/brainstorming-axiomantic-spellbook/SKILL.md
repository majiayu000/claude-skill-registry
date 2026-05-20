---
name: brainstorming
description: "Use when exploring design approaches, generating ideas, or making architectural decisions. Triggers: 'explore options', 'what are the tradeoffs', 'how should I approach', 'let's think through', 'sketch out an approach', 'I need ideas for', 'how would you structure', 'what are my options'. Also used in SYNTHESIS mode when implementing-features provides discovery context for autonomous design."
---

# Brainstorming Ideas Into Designs

<ROLE>
Creative Systems Architect. Reputation depends on designs that survive implementation without major rework.
</ROLE>

## Invariant Principles

1. **One Question Per Turn** - Cognitive load kills collaboration. Single questions get better answers.
2. **Explore Before Committing** - Always propose 2-3 approaches with trade-offs before settling.
3. **Incremental Validation** - Present designs in digestible sections, confirm understanding.
4. **YAGNI Ruthlessly** - Remove unnecessary features. Simplest design that solves the problem.
5. **Context Determines Mode** - Synthesis when context complete; interactive when discovery needed.

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| `context.feature_idea` | Yes | User's description of what they want to create/modify |
| `context.constraints` | No | Known constraints (tech stack, performance, timeline) |
| `context.existing_patterns` | No | Patterns from codebase research |
| `context.mode_override` | No | "SYNTHESIS MODE" to skip discovery |

## Outputs

| Output | Type | Description |
|--------|------|-------------|
| `design_document` | File | Design doc at `~/.local/spellbook/docs/<project>/plans/YYYY-MM-DD-<topic>-design.md` |
| `approach_decision` | Inline | Selected approach with rationale for alternatives considered |
| `implementation_ready` | Boolean | Whether design is complete enough to proceed |

## Mode Detection

<analysis>
Check context for synthesis mode indicators BEFORE starting process.
</analysis>

**Synthesis mode active when context contains:**
- "SYNTHESIS MODE" / "Mode: AUTONOMOUS" / "DO NOT ask questions"
- "Pre-Collected Discovery Context" or "design_context"
- Comprehensive architectural decisions, scope boundaries, success criteria already defined

| Mode | Behavior |
|------|----------|
| Synthesis | Skip discovery. Make autonomous decisions. Document rationale. Write complete design. |
| Interactive | Ask questions one at a time. Validate incrementally. Collaborate. |

## Synthesis Mode Protocol

<reflection>
Synthesis mode = all context provided. No need to discover, only to design.
</reflection>

**Skip:** Questions about purpose/constraints/criteria, "Which approach?", "Does this look right?", "Ready for implementation?"

**Decide Autonomously:** Architecture choice (document why), trade-offs (note alternatives), scope boundaries (flag ambiguity only).

**Circuit Breakers (still pause):**
- Security-critical decisions with no guidance
- Contradictory requirements irreconcilable
- Missing context making design impossible

## Interactive Mode Protocol

**Discovery Phase:**
- Check project state (files, docs, commits)
- Explore subagent for codebase patterns (saves main context)
- One question per message. Prefer multiple choice.
- Focus: purpose, constraints, success criteria

**Approach Selection:**
- Propose 2-3 approaches with trade-offs
- Lead with recommendation and reasoning

**Fractal exploration (optional):** When 2+ approaches have non-obvious trade-offs, invoke fractal-thinking with intensity `pulse` and seed: "What are the deep trade-offs between [approaches] for [feature]?". Use the synthesis to enrich the trade-off comparison presented to the user.

**Design Presentation:**
- 200-300 word sections
- Validate after each section
- Cover: architecture, components, data flow, error handling, testing

## After Design Complete

**Documentation:**
```bash
PROJECT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
PROJECT_ENCODED=$(echo "$PROJECT_ROOT" | sed 's|^/||' | tr '/' '-')
mkdir -p ~/.local/spellbook/docs/$PROJECT_ENCODED/plans
# Write to: ~/.local/spellbook/docs/$PROJECT_ENCODED/plans/YYYY-MM-DD-<topic>-design.md
```

**Implementation (interactive only):**
- Ask: "Ready to set up for implementation?"
- Use `using-git-worktrees` for isolation
- Use `writing-plans` for implementation plan

## Design Quality Assessment

After completing a design document, assess its quality using `/design-assessment`:

### When to Assess

| Scenario | Action |
|----------|--------|
| Design for evaluative skill/command | Run `/design-assessment --mode=autonomous` to generate framework for the design |
| Complex design with multiple stakeholders | Run assessment to validate completeness |
| Design review requested | Use assessment dimensions as review criteria |

### Assessment Protocol

1. **Generate framework**: `/design-assessment` with target type `document`
2. **Score dimensions**: Rate each dimension 0-5 using the generated rubric
3. **Document findings**: Use finding schema for any issues discovered
4. **Determine verdict**: Apply verdict logic to decide if design is ready

### Quality Gate

Design is ready for implementation when:
- All blocking dimensions (completeness, clarity, accuracy) score >= 3
- No CRITICAL or HIGH findings
- Verdict is READY

### Integration with Synthesis Mode

In synthesis mode, run assessment autonomously:
1. Generate document assessment framework
2. Self-score the design against dimensions
3. If any blocking dimension < 3: pause and report gaps
4. If verdict is NOT_READY or NEEDS_WORK: report gaps to user and iterate on design before proceeding

### Error Handling

If `/design-assessment` fails (command not found, execution error, timeout):
- Warn user: "Design assessment unavailable, proceeding without quality gate"
- Continue to implementation planning (degraded mode)
- Log the failure for debugging

<analysis>
Before proceeding to implementation planning:
- Has the design been assessed against standard dimensions?
- Are all blocking dimensions scoring >= 3?
- Have any CRITICAL or HIGH findings been addressed?
</analysis>

<FORBIDDEN>
- Asking multiple questions in one message (cognitive overload)
- Committing to approach without presenting alternatives
- Writing design doc to project directory (use ~/.local/spellbook/docs/)
- Skipping trade-off analysis to save time
- Proceeding with design when requirements are contradictory
- Adding features "just in case" (violates YAGNI)
</FORBIDDEN>

## Self-Check

Before completing:
- [ ] Presented 2-3 approaches with trade-offs before selecting
- [ ] Design doc written to correct external location (not project dir)
- [ ] All sections covered: architecture, components, data flow, error handling, testing
- [ ] No YAGNI violations (unnecessary complexity removed)
- [ ] Mode correctly detected (synthesis vs interactive)

If ANY unchecked: STOP and fix.
