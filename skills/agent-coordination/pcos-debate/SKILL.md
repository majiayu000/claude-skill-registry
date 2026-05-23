---
name: pcos-debate
description: "Shared protocol for PCOS Agent Team debates. Defines Critique Log format, Challenge/Proposal formats, debate flow mechanics, and standard constraints. Use when operating as a PCOS teammate agent (Planner, Critic, Optimizer, Synthesizer) during plan debates. Do NOT use for general discussion, brainstorming, or non-PCOS planning tasks -- those do not use the Agent Team debate protocol."
durability: encoded-preference
---

# PCOS Debate Protocol

## Debate Flow

### Planner (Blue/White Hat)
1. **Draft**: Analyze relevant files, create plan
2. **Share draft**: Send complete draft to **critic** and **optimizer**
3. **Receive feedback**: Critic sends challenges (problems), then Optimizer sends proposals (improvements, incorporating Critic's input)
4. **Respond to each item**:
   - **Accept**: Modify the plan and explain the change
   - **Reject**: Provide clear reasoning
   - **Defer**: Note for user to decide
5. **Send revised plan to all**: After responding to feedback, send the revised plan to **critic**, **optimizer**, AND **synthesizer**

### Critic (Black Hat)
1. **Pre-read**: Read relevant files while waiting for planner's draft
2. **Receive draft**: From planner
3. **Analyze**: Check against domain-specific review categories
4. **Send challenges to planner**: Ordered by severity (CRITICAL first)
5. **Copy challenges to optimizer**: So optimizer can propose alternatives
6. **Review planner's responses**: Verify changes or rejections are sound
7. **Send final assessment to synthesizer**: Summary of resolved/unresolved issues

### Optimizer (Green Hat)
1. **Pre-read**: Read relevant files while waiting
2. **WAIT for both**: Planner's draft AND Critic's challenges. **Do NOT start proposing improvements until Critic's challenges have been received.** Deadlock-breaking requires knowing both positions.
3. **Analyze independently**: Find improvements the plan missed
4. **Break deadlocks**: If Critic and Planner disagree, propose a third option
5. **Send proposals to planner**: Both independent improvements and deadlock-breaking alternatives
6. **Send final proposals to synthesizer**: All proposals with their status

### Synthesizer
1. **Pre-read**: Read relevant files for background
2. **Receive**: Planner's final plan, Critic's final assessment, Optimizer's final proposals
3. **Resolve**: For unresolved disagreements, make evidence-based final calls
4. **Produce final output**: Write output files directly (plan file, index updates, and any additional deliverables)

## Debate Constraints

- Maximum 2 rounds of Critic-Planner exchange
- Critic focuses on PROBLEMS only (not improvements)
- Optimizer focuses on IMPROVEMENTS only (not problems) and DEADLOCK RESOLUTION
- Synthesizer is neutral -- does not favor any participant

## Unverified Hypothesis Handling

### Planner Responsibilities
- Mark any technical feasibility assumption you are not 100% certain about with `[UNVERIFIED]`
- Do NOT delay the draft to verify -- mark and move on (speed over certainty at draft stage)

### Critic/Optimizer Responsibilities (Complex Mode)
- Use search tools (WebSearch, WebFetch, context7 MCP -- see web-research skill) to verify or refute `[UNVERIFIED]` items
- Report verification results in Challenge/Proposal format:
  - Verified true: `[VERIFIED]` with evidence link/quote
  - Verified false: Challenge with correct information
  - Cannot verify: Leave as `[UNVERIFIED]` with note

### Synthesizer Responsibilities
- For items that remain `[UNVERIFIED]` after debate:
  1. Record in the Critique Log with Resolution = "Unverified"
  2. Add an investigation task to the plan's Progress Tracking section:
     `- [ ] Investigate: [description of what needs verification]`
  3. The main session handles investigation before proceeding to the next phase (e.g., before `/update-claude-config` or `/tdd`)

### Simple Mode (No Critic/Optimizer)
- Planner marks `[UNVERIFIED]` items in the plan
- The main session investigates all `[UNVERIFIED]` items before proceeding to implementation

## Standard Agent Constraints

- Synthesizer writes output files directly (plan files, index updates, ADRs). Other roles (Planner, Critic, Optimizer) do NOT write files.
- Do NOT ask user questions (team lead handles user interaction)
- Planner, Critic, Optimizer: Do NOT read or write files in `docs/plans/` directory (team lead provides needed plan content)
- Synthesizer: MAY write to `docs/plans/` and `docs/adr/` directories as part of file-writing responsibilities
- You MAY read application source code files to analyze architecture and existing patterns

## Challenge Format

    **Challenge [N]**: [Category] - [One-line summary]
    Problem: [Specific description]
    Assumes: [Unstated assumption the plan relies on -- omit if none]
    Evidence: [File path, line numbers, convention reference]
    Suggestion: [Concrete fix]
    Severity: CRITICAL | HIGH | MEDIUM

## Proposal Format

    **Improvement [N]**: [Category] - [One-line summary]
    Current: [What the plan does now]
    Proposed: [What it could do instead]
    Benefit: [Why this is better]
    Priority: HIGH | MEDIUM | LOW

## Critique Log Format

The Synthesizer produces this as part of the final output:

    ## Critique Log

    | # | Source | Challenge/Proposal | Category | Resolution | Detail |
    |---|--------|-------------------|----------|------------|--------|
    | 1 | Critic | [challenge summary] | [category] | Accepted/Rejected/Deferred | [detail] |
    | 2 | Optimizer | [proposal summary] | [category] | Accepted/Rejected/Deferred | [detail] |

    **Debate rounds**: N
    **Critic challenges**: N (Accepted: N | Rejected: N | Deferred: N)
    **Optimizer proposals**: N (Accepted: N | Rejected: N | Deferred: N)
    **Deadlocks resolved by Optimizer**: N
