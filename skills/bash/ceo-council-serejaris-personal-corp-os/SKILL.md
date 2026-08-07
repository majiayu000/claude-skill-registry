---
name: ceo-council
description: Use when needing strategic project analysis from multiple independent expert perspectives. Triggers on business decisions, growth strategy, product direction, competitive analysis, or any situation where diverse C-level opinions reduce blind spots
---

# CEO Council — Independent Strategic Analysis

Launch parallel sub-agents as isolated C-level experts. Each analyzes the same project data from their perspective. No coordination between experts — isolation produces genuine diversity of opinion. Then synthesize consensus and disagreements.

## Critical: How to Launch Experts

**MUST use the Task tool** with `subagent_type: "general-purpose"` and `model: "opus"`.

```
Task(
  subagent_type: "general-purpose",
  model: "opus",
  prompt: "<expert prompt with data>",
  description: "CFO analysis"
)
```

**DO NOT** use bash, shell scripts, or background commands to launch experts. They will fail.

Launch all experts in a **single message with multiple Task tool calls** for true parallelism.

## Step 1: Scan Project Context

Before suggesting experts, understand the project:

1. Read `CLAUDE.md` (or `README.md` if absent)
2. Scan `.claude/rules/` for domain context
3. Glance at top-level file structure

Based on findings, **generate 4-6 expert roles tailored to THIS project**. Roles must reflect the project's actual domain, challenges, and stage.

## Step 2: Assemble the Council

**MANDATORY: Ask the user before proceeding.** Do not pick roles yourself.

Use `AskUserQuestion` with `multiSelect: true`:
- Show 4-6 role options with short descriptions of their focus
- User can always pick "Other" to define custom roles
- **Minimum 2 experts.** If user picks 1, suggest adding one more for productive disagreement

### Role Examples by Project Type

**Don't copy these** — generate fresh roles based on actual project context:

| Project Type | Typical Roles |
|-------------|--------------|
| **SaaS** | Head of Engineering, Head of Product, Head of Growth, CFO, UX Researcher |
| **Open Source** | Community Manager, Technical Architect, DevRel, Security Advisor |
| **Content / Media** | Content Strategist, Audience Analyst, Monetization Expert, Distribution Expert |
| **EdTech** | CMO, CFO, CPO, COO, Growth Advisor |
| **E-commerce** | Head of Supply Chain, Marketing Director, CTO, Customer Experience Lead |
| **Agency / Consulting** | Sales Director, Delivery Lead, Talent Manager, CFO |

## Step 3: Gather Current Data

Collect project state to feed all experts. Stay focused on what's relevant:

**Read:**
- Key metrics/data files identified during context scan
- Strategy and planning documents
- Recent decisions or changes (git log --oneline -10)
- Previous council analyses (if any)

**Skip:** GitHub traffic stats, stargazer counts, clone data, contributor lists — these are vanity metrics, not strategic data.

**All experts must receive identical data context.** Prepare the data block ONCE, then paste it into each expert prompt.

## Step 4: Generate Expert Prompts

For each selected expert, create a prompt with the SAME data block:

```
You are the [ROLE] for [PROJECT NAME]. Analyze the data below from a [DOMAIN] perspective.

Focus on:
- [3-6 specific focus areas relevant to role and project]

Data:
[CURRENT PROJECT DATA — identical for all experts]

[Role-specific instruction: "show the math", "be the contrarian", "prioritize by effort/impact", etc.]

Respond in the same language as the data provided.
```

**Rules:**
- Each expert gets the SAME data block — prepare it once, reuse
- Focus areas must be specific to the project, not generic
- Include a personality instruction (contrarian, pragmatic, data-driven)
- Mention project constraints the expert should know

## Step 5: Execute

Launch ALL selected experts in **one message** using multiple Task tool calls:

```
# In a single response, call Task for each expert:
Task(subagent_type: "general-purpose", model: "opus", prompt: "<CFO prompt>", description: "CFO analysis")
Task(subagent_type: "general-purpose", model: "opus", prompt: "<CPO prompt>", description: "CPO analysis")
Task(subagent_type: "general-purpose", model: "opus", prompt: "<CTO prompt>", description: "CTO analysis")
```

Wait for all experts to return results before proceeding to synthesis.

## Step 6: Synthesize

**Do not skip this step.** The synthesis is the entire value of the council.

After all experts report, create a synthesis document:

```markdown
# Council Session: [DATE]

## Council Members
[List of selected experts and their focus]

## Context
[Current metrics/state snapshot — brief]

## [Expert 1 Name]
[Key findings and recommendations]

## [Expert 2 Name]
[Key findings and recommendations]

## Consensus (all agree)
1. ...
2. ...

## Disagreements
| Expert | Position | Argument |
|--------|----------|----------|
| ... | ... | ... |

## Decisions
_To be filled after discussion._
```

### Save Results

Save to a logical location:
- `docs/council-[DATE].md` — default
- Or project-specific path if context suggests one

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Picking roles without asking user | ALWAYS use AskUserQuestion first |
| Using bash to launch experts | ONLY use Task tool with subagent_type: "general-purpose" |
| Giving experts different data | Prepare ONE data block, paste into all prompts |
| Gathering vanity metrics | Focus on project docs, strategy, actual metrics |
| Too many experts (6+) | 3-4 is optimal for signal-to-noise |
| Skipping synthesis | The synthesis IS the value — never skip |
