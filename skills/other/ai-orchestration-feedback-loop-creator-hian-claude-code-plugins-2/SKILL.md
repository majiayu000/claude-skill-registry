---
name: ai-orchestration-feedback-loop
description: Multi-AI engineering loop orchestrating Claude, Codex, and Gemini for comprehensive validation. USE WHEN (1) mission-critical features requiring multi-perspective validation, (2) complex architectural decisions needing diverse AI viewpoints, (3) security-sensitive code requiring deep analysis, (4) user explicitly requests multi-AI review or triple-AI loop. DO NOT USE for simple features or single-file changes. MODES - Triple-AI (full coverage), Dual-AI Codex-Claude (security/logic), Dual-AI Gemini-Claude (UX/creativity).
requires:
  - gemini-plugin:gemini-cli
  - codex-plugin:codex-cli
---

# AI Orchestration Feedback Loop

## Workflow

```
Standard:      Plan → Validate(AI-1) → Review(AI-2) → Synthesize → Implement → Review → Done
Co-Implement:  Plan → Validate → Review → Synthesize → Core(Claude) → Aux(Gemini) → Integrate → Review → Done
```

| Role | Responsibility |
|------|----------------|
| **Claude** | Planning, synthesis, core implementation |
| **Codex** | Deep validation, security, logic verification, edge cases |
| **Gemini** | Creative review, alternatives, UX + **auxiliary code generation** (Co-Impl) |

## CLI Patterns

| CLI | Command |
|-----|---------|
| Codex | `codex exec -m MODEL -c model_reasoning_effort=LEVEL -s read-only "prompt"` |
| Gemini | `gemini -m MODEL -p "prompt"` |

**Always use `timeout: 600000`** for all AI commands.

## Model & CLI References

**IMPORTANT**: For available models and CLI options, refer to the required skills:
- **Codex**: See `codex-plugin:codex-cli` skill for models, reasoning effort levels, and CLI options
- **Gemini**: See `gemini-plugin:gemini-cli` skill for models, output formats, and CLI options

When asking user for model selection in Phase 0, present options based on the current skill documentation.

## Phase 0: Pre-flight

```bash
mkdir -p .ai-orchestration
```

Ask user via `AskUserQuestion` with **4 questions**:

### Question 1: AI Participation Mode
**Header**: "Mode"
| Option | Description |
|--------|-------------|
| Triple-AI (default) | Full coverage: Claude + Codex + Gemini |
| Dual-AI: Codex-Claude | Security/logic focus |
| Dual-AI: Gemini-Claude | UX/creativity focus |

### Question 2: Role Assignment per Phase
**Header**: "Roles"
| Option | Description |
|--------|-------------|
| Standard | Claude: implement, Codex: validate, Gemini: review |
| Codex-Heavy | Claude: plan/synthesize, Codex: validate+implement review |
| Gemini-Heavy | Claude: plan/synthesize, Gemini: validate+implement review |
| Custom | User defines each phase assignment |

If **Custom** selected, ask follow-up:
| Phase | Options |
|-------|---------|
| Planning | Claude (default) / Codex / Gemini |
| First Validation | Codex / Gemini / Both (parallel) |
| Second Validation | Codex / Gemini / Skip (Dual-AI) |
| Implementation | Claude (default) / Codex-assisted / Gemini-assisted |
| Code Review | Codex / Gemini / Both (parallel) |

### Question 3: Model Selection
**Header**: "Models"

First, load the required skills to get current model lists:
1. Load `codex-plugin:codex-cli` → get Codex models and reasoning effort levels
2. Load `gemini-plugin:gemini-cli` → get Gemini models

Then present options:
| Option | Description |
|--------|-------------|
| Ultra Power | Codex: [highest capability model] + xhigh reasoning, Gemini: [highest capability model] |
| High Power | Codex: [highest capability model] + high reasoning, Gemini: [highest capability model] |
| Balanced (default) | Codex: [standard model] + high reasoning, Gemini: [stable pro model] |
| Fast | Codex: [mini model] + medium reasoning, Gemini: [flash model] |
| Custom | User specifies from available models in each skill |

### Question 4: Analysis Focus
**Header**: "Focus"
| Option | Description |
|--------|-------------|
| Balanced (default) | Equal weight to all aspects |
| Security | OWASP, auth, encryption, injection |
| Performance | Algorithms, memory, I/O, scaling |
| Architecture | Patterns, coupling, extensibility |

### Question 5: Gemini Co-Implementation
**Header**: "Co-Impl"
| Option | Description |
|--------|-------------|
| Disabled (default) | Gemini validation-only (standard workflow) |
| Documentation Only | Gemini generates docs, comments, README |
| Boilerplate Only | Gemini generates utilities, configs |
| Full Co-Implementation | Both documentation and boilerplate |

### Question 6: Gemini Generation Scope (if Co-Implementation enabled)
**Header**: "Gen Scope"
| Category | Options (multiSelect) |
|----------|----------------------|
| Documentation | API docs, Inline comments, README sections, JSDoc/TSDoc/XML |
| Boilerplate | Utility functions, Config files, Type interfaces, Test scaffolds |

### Question 7: Integration Review Mode (if Co-Implementation enabled)
**Header**: "Review Mode"
| Option | Description |
|--------|-------------|
| Review-first (default) | Show Gemini output to user before integration |
| Auto-integrate | Automatically integrate if syntax valid |
| Strict Review | Require explicit user approval per file |

Save to `.ai-orchestration/config.md`:
```markdown
# AI Orchestration Config
## Mode: [selected mode]
## Roles
- Planning: [AI]
- Validation 1: [AI]
- Validation 2: [AI or Skip]
- Implementation (Core): Claude
- Implementation (Auxiliary): [Disabled | Gemini]
- Code Review: [AI(s)]
## Models
- Codex: [model] (reasoning: [level])
- Gemini: [model]
## Focus: [focus area]
## Co-Implementation
- Enabled: [yes/no]
- Mode: [Disabled | Documentation Only | Boilerplate Only | Full]
- Documentation Scope: [api-docs, inline-comments, readme, jsdoc]
- Boilerplate Scope: [utilities, configs, interfaces, test-scaffolds]
- Review Mode: [review-first | auto-integrate | strict-review]
```

## Phase 1: Planning

**Executor**: Based on config (default: Claude)

Create `.ai-orchestration/plan.md` with: Objective, Approach, Steps, Risk Assessment, Validation Focus Areas

| Planner | Command |
|---------|---------|
| Claude (default) | Use native planning |
| Codex | `codex exec -m MODEL -c model_reasoning_effort=LEVEL -s read-only "Create plan for: [TASK]..."` |
| Gemini | `gemini -m MODEL -p "Create plan for: [TASK]..."` |

## Phase 2: First Validation

**Executor**: Based on config `Validation 1` setting

> **Detailed prompts**: See [prompt-templates.md](references/prompt-templates.md#phase-2-codex-validation-prompts) for Security/Performance/Architecture focused prompts

| Validator | Command | Output File |
|-----------|---------|-------------|
| Codex | `codex exec -m MODEL -c model_reasoning_effort=LEVEL -s read-only "Validate: $(cat plan.md)..."` | `phase2_codex_validation.md` |
| Gemini | `gemini -m MODEL -p "Review: $(cat plan.md)..."` | `phase2_gemini_validation.md` |
| Both | Execute in **parallel**, save both outputs | Both files |

## Phase 3: Second Validation

**Executor**: Based on config `Validation 2` setting (Skip if Dual-AI or config says Skip)

> **Detailed prompts**: See [prompt-templates.md](references/prompt-templates.md#phase-3-gemini-review-prompts) for Innovation/UX focused prompts

| Scenario | Reviewer | Key Focus | Output File |
|----------|----------|-----------|-------------|
| After Codex | Gemini | Complement (don't repeat): Alternatives, User Impact, Blind Spots | `phase3_gemini_review.md` |
| After Gemini | Codex | Build on Gemini: Security/Edge Cases analysis | `phase3_codex_review.md` |
| Both (parallel) | Both | Independent review, cross-reference in Phase 4 | Both files |

## Phase 4: Synthesis

Read validation results. Create `.ai-orchestration/phase4_synthesis.md`:

```markdown
# Synthesis
## Consensus Points
## Divergence Analysis
## Prioritized Actions (P0/P1/P2)
## Revised Plan
## User Decisions Needed
```

For synthesis methodology: See [synthesis-guide.md](references/synthesis-guide.md)

Present to user via `AskUserQuestion`: Proceed / Address issues / Request more validation

## Phase 5a: Core Implementation

**Executor**: Claude (always)

Implement core business logic using Edit/Write/Read tools.

Save `.ai-orchestration/implementation.md` with: Implemented By, Changes Made, Issues Addressed, Testing Notes

| Mode | Executor | Use Case |
|------|----------|----------|
| Default | Claude | Standard implementation |
| Codex-assisted | Claude + Codex | Complex logic (`-s workspace-write`) |

**If Co-Implementation enabled** → Create handoff spec for Phase 5b:

Save `.ai-orchestration/phase5b_handoff.md`:
```markdown
# Gemini Co-Implementation Handoff
## Implementation Summary
[Link to implementation.md]
## Files Created/Modified
[List of files]
## Generation Tasks
### Task 1: [Documentation/Boilerplate]
**Type**: [api-docs | inline-comments | readme | utilities | configs | interfaces]
**Target Files**: [list]
**Code Context**:
\`\`\`[language]
[relevant snippets for context]
\`\`\`
**Requirements**:
- [specific requirements]
```

## Phase 5b: Auxiliary Generation (Gemini)

**Executor**: Gemini (if Co-Implementation enabled)
**Skip if**: Co-Implementation disabled in config

> **Detailed prompts**: See [co-implementation-guide.md](references/co-implementation-guide.md) for handoff format and prompts

Generate auxiliary code based on handoff specification:

```bash
gemini -m MODEL -p "Generate auxiliary code per handoff spec:
$(cat .ai-orchestration/phase5b_handoff.md)

[Use prompt from co-implementation-guide.md based on scope]"
```

**Output Format** (FILE: marker system):
```markdown
FILE: path/to/file.ext
---
[generated content]
---
FILE: next/file.ext
---
[content]
---
```

Save to `.ai-orchestration/phase5b_gemini_output.md`

## Phase 5c: Integration

**Executor**: Claude
**Skip if**: Co-Implementation disabled

1. **Parse** Gemini output (FILE: markers)
2. **Validate** syntax and conflicts
3. **Apply Review Mode**:
   - Review-first → Show to user, ask approval
   - Auto-integrate → Integrate if valid
   - Strict → Ask per file
4. **Integrate** approved code via Edit/Write
5. **Handle Revision** (max 2 attempts):
   - If rejected → Request Gemini revision or Claude fallback

Save `.ai-orchestration/phase5c_integration.md` with: Files Integrated, Review Decisions, Revisions Made

## Phase 6: Code Review

**Executor**: Based on config `Code Review` setting

> **Detailed prompts**: See [prompt-templates.md](references/prompt-templates.md#phase-6-code-review-prompts)

| Reviewer | Verdict Format | Output File |
|----------|----------------|-------------|
| Codex | PASS/FAIL + Issue Status | `phase6a_codex_review.md` |
| Gemini | APPROVE/REQUEST CHANGES/REJECT | `phase6b_gemini_review.md` |
| Both | Execute **parallel**, combine verdicts | Both files |

## Phase 7: Final Assessment

- Both PASS/APPROVE → Complete
- FAIL/REJECT → Fix and re-validate
- REQUEST CHANGES → Apply and iterate

Save iterations to `.ai-orchestration/iterations.md`.

## Context Files

```
.ai-orchestration/
├── config.md
├── plan.md
├── phase2_*.md
├── phase3_*.md (Triple-AI only)
├── phase4_synthesis.md
├── implementation.md
├── phase5b_handoff.md          # Co-Implementation handoff spec
├── phase5b_gemini_output.md    # Gemini generated code
├── phase5c_integration.md      # Integration log
├── phase6a_codex_review.md
├── phase6b_gemini_review.md
└── iterations.md
```

## Error Handling

| Error | Solution |
|-------|----------|
| `stdin is not a terminal` | Use `codex exec` |
| Empty Gemini output | Use `-p` flag |
| Not in Git repo | Use `--skip-git-repo-check` for Codex |

## References

- **Prompt Templates**: [prompt-templates.md](references/prompt-templates.md) - Detailed prompts for each focus area
- **Workflow Patterns**: [workflow-patterns.md](references/workflow-patterns.md) - Security-First, Architecture Decision, Rapid Iteration patterns
- **Synthesis Guide**: [synthesis-guide.md](references/synthesis-guide.md) - Divergence analysis, priority matrix, resolution patterns
- **Co-Implementation Guide**: [co-implementation-guide.md](references/co-implementation-guide.md) - Handoff format, output format, integration process
