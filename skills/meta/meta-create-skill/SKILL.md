---
name: meta__create_skill
description: Creates or updates agent skills with proper structure, templates, testing, and documentation. Use when creating new skills or editing existing ones to keep them aligned with the Anthropic best practices.
---

Use this guide to add a new capability (skill/workflow) that follows Anthropic's "Complete Guide to Building Skills for Claude" playbook. Treat this document as the canonical example—any updates to it must satisfy the same standards described below.

## Quality Standards

### Structure & Progressive Disclosure
- Keep the three-layer model: concise YAML frontmatter → actionable `SKILL.md` body → optional linked references.
- Maintain composability; every skill must coexist with others without assuming exclusivity.
- Keep the body under ~500 lines. Move deep dives into `references/` or `templates/` and link from the main file.

### Frontmatter Requirements
- **name**: `prefix__slug` folder name, lowercase letters/numbers/hyphens, ≤64 characters, no `claude`/`anthropic`.
- **description**: ≤1024 characters describing *what* the skill does, *when* to use it (trigger phrases/file types), and key capabilities in third-person voice.
- Optional fields (`license`, `compatibility`, `metadata`) clarify distribution licensing, runtime expectations, or MCP dependencies. Avoid XML brackets to keep the system prompt safe.

### Folder Hygiene
- Directory format from the guide:
  ```
  .claude/skills/{prefix__slug}/
  ├── SKILL.md
  ├── templates/      # optional code or doc templates
  ├── references/     # optional deep guidance
  ├── assets/         # optional fonts/icons/mockups
  └── scripts/        # optional automation helpers
  ```
- Never add `README.md` inside the skill directory; human-facing docs live elsewhere.
- Reference template files (e.g., `templates/Command.cs`) instead of inlining large artifacts.

### Description & Trigger Checklist
- Lists both positive triggers ("Use when the user says…") and negative guards ("Do **not** use when…") to reduce under/over-triggering.
- Mentions relevant files/APIs (.fig, Linear, etc.) so Claude can match user intent accurately.
- Passes the self-test: Ask Claude "When would you use the {skill}?" and ensure the echoed description matches your intent.

### Instruction Crafting
- Begin with an opening statement summarizing the workflow outcome.
- Present numbered steps with validation gates, decision points, and references to reusable templates.
- Highlight error handling, rollbacks, and quality gates (e.g., iterative refinement loops) consistent with the guide's pattern library.
- Use `// turbo` callouts for steps that automation can perform without human approval.

## Planning Checklist

1. Document 2–3 concrete use cases with trigger phrases, tool requirements (built-in or MCP), and the "definition of done" for each.
2. Map each use case to one of Anthropic's categories: document creation, workflow automation, or MCP enhancement.
3. Establish success criteria before authoring:
   - ≥90% trigger rate on relevant prompts vs. manual enabling.
   - Clear metrics (tool calls, token budget, error rate) to compare with/without the skill.
4. Decide how progressive disclosure will split content between SKILL.md and linked references.

## Skill Creation Steps

1. **Plan Naming & Scope**
   - Reserve a unique `prefix__slug` and ensure the folder mirrors the name exactly.
   - Capture user outcome statements ("Help me plan this sprint") and negative cases upfront.

2. **Author Frontmatter**
   - Use [templates/SKILL.md](templates/SKILL.md) as the scaffold.
   - Populate `description` with outcome + trigger phrases + relevant assets/APIs.
   - Add optional metadata such as `compatibility: "Claude Code + MCP-Linear"` when the runtime matters.

3. **Draft Instructions**
   - Follow the recommended structure: overview, numbered workflow, examples, troubleshooting.
   - Link to reusable templates (e.g., `templates/Endpoint.cs`) instead of pasting long code blocks.
   - Include decision trees, validation steps, and error handling patterns pulled from the Anthropic guide.

4. **Add Supporting Resources**
   - Create `templates/`, `references/`, `assets/`, or `scripts/` as needed; use placeholders (`{ResourceName}`) for user-supplied values.
   - Keep references one level deep to respect progressive disclosure.

5. **Register in AGENTS.md**
   - Document the `/prefix__slug` command with a concise description and placement inside the Skills table.

6. **Test & Iterate**
   - Design trigger tests (should trigger vs. should not trigger lists), functional tests (end-to-end workflow success), and performance comparisons (token/tool-call deltas) per the guide.
   - Iterate descriptions when you detect under- or over-triggering; add negative triggers or clarifications as needed.

// turbo
7. **Automated Verification**
   - Lint YAML/Markdown, confirm template placeholders resolve, and ensure linked files exist.
   - Validate that SKILL.md stays under size limits and references valid paths.

8. **Distribute & Document**
   - Provide installation guidance (zip folder → upload via Claude.ai Settings > Skills or place in Claude Code skills directory).
   - Position the skill around outcomes ("set up project workspaces in seconds") and highlight the MCP + skill story when applicable.

## Testing Playbook

- **Trigger Coverage**: Maintain a regression list of prompts that *must* load the skill and another list that must not.
- **Functional Runs**: Exercise representative workflows ("Create project with 5 tasks") and log API/tool outcomes and error handling paths.
- **Performance Deltas**: Compare baseline vs. skill-enabled runs for conversation turns, tool invocations, and token counts.
- **Feedback Loop**: Capture under/over-triggering and execution issues; feed them back into the description or instruction updates.

## Distribution & Positioning

- Host skills in a public repo with a README for humans (outside the skill folder) plus screenshots or GIFs.
- Cross-link from your MCP documentation explaining how the skill and connector combine for faster workflows.
- Provide a short installation checklist so users can enable and test the skill immediately after download.

## Pattern Reference

- **Sequential Workflow Orchestration**: Stepwise actions with validation and rollback guidance.
- **Multi-MCP Coordination**: Phase-by-phase coordination across multiple services, with explicit data handoffs.
- **Iterative Refinement**: Draft → validate → refine loops with stopping criteria.
- **Context-Aware Tool Selection**: Decision trees that choose the right MCP/tool based on file type, size, or risk tier.
- **Domain-Specific Intelligence**: Embed compliance/intelligence rules that run before calling external tools.

## Related Skills

**Prerequisites**:
- Foundational skills such as [/meta__cheat_sheet](.claude/skills/meta__cheat_sheet/SKILL.md) for quick conventions.

**Next Steps**:
- After scaffolding, use `/test__verify_feature` or relevant automation to validate broader workflows.

**See Also**:
- [/meta__write_agents_md](.claude/skills/meta__write_agents_md/SKILL.md) for documentation guidance.
- Other `.claude/skills/` examples for reference implementations.
