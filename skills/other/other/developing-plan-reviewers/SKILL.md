---
name: developing-plan-reviewers
description: Create project-specific plan reviewer agents that integrate with the planning-project-features workflow. Use when a project needs domain-specialized reviewers for sub-plans (e.g., Go code reviewer, API layer reviewer, database reviewer) or when the planner warns that no suitable local reviewer exists for a sub-plan's domain.
---

# Developing Plan Reviewers

Create project-specific reviewer agents for the `planning-project-features` workflow. These agents review individual sub-plans for domain-specific correctness — catching issues that the generic global reviewers (architecture, risk) cannot.

For general agent development guidance (frontmatter fields, description examples, system prompt design), see the `developing-agents` skill.

## How Plan Reviewers Fit In

The planning workflow (Phase 5) uses two types of reviewers:

1. **Global reviewers** (`~/.claude/agents/`) — `plan-architect-reviewer` and `plan-risk-reviewer`. Project-agnostic, already exist.
2. **Local reviewers** (`.claude/agents/`) — project-specific, domain-specialized. **This is what you build.**

The planner discovers local reviewers in Phase 4 by reading their descriptions, matches each sub-plan to the most appropriate reviewer, and launches them in Phase 5. No naming convention is assumed — the description is what matters.

## Design Philosophy

A reviewer agent is a **thin shell**. It defines:

- **What to review** — the domain scope (via description and skills list)
- **How to output** — the standard review format (Verdict / Findings / Concerns / Observations)
- **What tone to use** — critical, not praising; specific, not vague

It does **not** define how to review. Domain knowledge comes from the preloaded **skills**, which encode conventions, patterns, and pitfalls. This separation prevents the reviewer from becoming a static checklist that rots as conventions evolve — the skills are maintained independently and stay in sync with the codebase.

## Reviewer Agent Template

```markdown
---
name: plan-<domain>-reviewer
description: "Use this agent to review sub-plans that involve <domain>. Evaluates <what it checks> against project conventions.\n\n<example>\nContext: A sub-plan covers <domain> implementation within a feature plan.\nuser: \"Review sub-plan 02-<task>.md for <domain> correctness.\"\nassistant: \"I'll review the sub-plan for <domain> issues using the plan-<domain>-reviewer agent.\"\n<commentary>\nSub-plan involves <domain> work. Launch the domain-specific reviewer.\n</commentary>\n</example>"
tools: Read, Glob, Grep
memory: project
skills:
  - <skill-1>
  - <skill-2>
---

You are a <domain> reviewer. Your job is to review implementation sub-plans
for <domain> correctness — ensuring the proposed approach follows established
conventions, avoids known pitfalls, and will produce correct results.

You are NOT here to praise, summarize, or restate the plan. You are here to
find what's wrong with it from a <domain> perspective.

## Memory

Consult your agent memory before starting work — it contains knowledge about
this project's <domain-specific patterns, file locations, conventions> from
previous reviews. This saves you from re-exploring the codebase.

After completing your review, update your agent memory with <domain-specific>
patterns, file locations, and conventions you discovered. Write concise notes
about what you found and where. Keep memory focused on facts that help future
reviews start faster.

## What You Review

You will be given a path to a specific sub-plan file (e.g.,
`.claude/plans/<feature>/02-<task>.md`). You also have access to the full
codebase to verify claims.

## How You Review

1. **Read the sub-plan** completely.
2. **Read ALL project documentation first** — AGENTS.md, component-level
   AGENTS.md files, and any project documentation (`docs/`, `doc/`, etc.).
   Documentation is orders of magnitude cheaper than code exploration. Do
   NOT use Glob/Grep to explore code before reading all available
   documentation.
3. **Apply your skills** to evaluate the plan against project conventions.
   Your preloaded skills encode the conventions for this domain. Use them
   as your review criteria.
4. **Verify specific claims only** — use Glob and Grep only to confirm
   specific claims the plan makes (e.g., an interface exists, a file path
   is correct). Do not broadly explore the codebase.

## Output Format

Return your findings as your response using the format below. The calling
agent (planner) is responsible for writing review files — you do not write
files.

[Insert the standard output format template from this skill]

## Rules

- **Be specific and actionable** — every finding must reference the exact
  plan section and provide a concrete recommendation.
- **Review the plan, not the code** — you evaluate whether the plan's
  strategy is sound for this domain. Code-level review happens during
  execution.
- **Don't invent requirements** — review against the sub-plan's stated
  objective and acceptance criteria.
- **Don't duplicate architecture or risk review** — focus only on your
  domain expertise.
- **Verify claims against the codebase** — if the plan says "extend the
  existing interface," confirm the interface exists and the extension
  makes sense.
```

### Key Choices

- **`tools: Read, Glob, Grep`** — No Write. Reviewers return findings as their Task response; the planner writes review files. This avoids the problem where Task sub-agents cannot write files regardless of permission mode.
- **`memory: project`** — Persistent memory scoped to the project. Reviewers build up knowledge about codebase patterns, file locations, and conventions across reviews. This dramatically reduces redundant codebase exploration — the reviewer knows where to look instead of rediscovering the same modules each time. Memory auto-enables Read/Write/Edit for the memory directory only, so it doesn't conflict with the no-Write-to-codebase design.
- **`skills`** — the differentiator. Preloads domain knowledge so the reviewer doesn't need to discover conventions at runtime. Skills are the review criteria — the agent should not hardcode evaluation checklists that duplicate what skills already teach. See [Choosing Skills to Preload](#choosing-skills-to-preload).
- **No `model` field** — inherits from parent, matching the global reviewers.
- **Description** — must be clear enough for the planner to match it to sub-plans. Include what domain it covers and what it evaluates. Use `\n` escapes for multi-line content (not literal newlines) to ensure valid YAML frontmatter.
- **No evaluation sections** — don't add numbered "Evaluate X" sections that restate skill content. The skills are injected into context and the reviewer applies them naturally. Static checklists rot; skills are maintained.

## Choosing Skills to Preload

The `skills` frontmatter field injects full skill content into the reviewer's context at startup. This is how domain knowledge gets into the reviewer.

**Selection criteria:**
- List only skills whose conventions the reviewer needs to evaluate sub-plans correctly
- Check both global (`~/.claude/skills/`) and local (`.claude/skills/`) skills
- Don't overload — each injected skill consumes context budget
- Prefer skills that teach conventions and point to source files over skills that duplicate config content

**Examples:**
| Reviewer Domain | Skills to Preload |
|-----------------|-------------------|
| Go code | `writing-go-code`, `applying-effective-go` |
| API layer | `writing-go-code` (or API-specific skill if one exists) |
| Shell config | `configuring-zsh` |
| CI/CD | `configuring-github-actions` |
| Dotfile management | `managing-chezmoi` |

## Standard Output Format

All plan reviewers **must** follow this format. The planner depends on the structure for output normalization (Phase 5, Step 2).

```markdown
# <Domain> Review: <Sub-Plan Name>

## Verdict

<PASS | PASS WITH CONCERNS | NEEDS REVISION>

## Critical Findings
<Issues that MUST be fixed before the plan can proceed. Empty if none.>

### Finding: <short title>
- **Affects**: <plan file and section>
- **Problem**: <what's wrong from a domain perspective>
- **Recommendation**: <how to fix it>

## Concerns
<Issues that SHOULD be addressed but aren't blockers. Empty if none.>

### Concern: <short title>
- **Affects**: <plan file and section>
- **Problem**: <what's wrong>
- **Recommendation**: <how to fix it>

## Observations
<Minor notes, suggestions, or things the planner might want to consider. Empty if none.>
```

## Examples

Complete, copy-and-adapt reviewer examples:

- **[Go Codebase Reviewer](examples/plan-go-reviewer.md)** — reviews sub-plans for idiomatic Go patterns. Preloads `writing-go-code` and `applying-effective-go` as review criteria.
- **[API Layer Reviewer](examples/plan-api-reviewer.md)** — reviews sub-plans for endpoint design and backward compatibility. Preloads `writing-go-code` as review criteria.

## Rules

- **Always follow the standard output format** — the planner depends on the Verdict/Critical Findings/Concerns/Observations structure
- **Return findings as response, never write files** — the planner writes review output to `reviews/<plan-file>.<reviewer-type>.md`
- **Review the plan, not the code** — evaluate whether the plan's strategy is sound for the domain; code-level review happens during execution
- **Be specific and actionable** — every finding must reference the exact plan section and provide a recommendation
- **Don't duplicate architecture or risk review** — focus only on domain expertise
- **Don't invent requirements** — review against the sub-plan's stated objective and acceptance criteria
- **Don't hardcode evaluation checklists** — let skills encode the conventions; the agent applies them
