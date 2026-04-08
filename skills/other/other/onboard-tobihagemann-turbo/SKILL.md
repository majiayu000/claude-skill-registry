---
name: onboard
description: "Developer onboarding guide that composes architecture mapping, tooling review, and agentic setup review with setup, troubleshooting, and next-steps agents to produce a comprehensive guide at .turbo/onboarding.md and .turbo/onboarding.html. Use when the user asks to \"onboard me\", \"onboard to this project\", \"generate onboarding guide\", \"new developer guide\", \"how do I get started\", or \"help me ramp up\"."
---

# Onboard

Developer onboarding pipeline. Composes `/map-codebase`, `/review-tooling`, and `/review-agentic-setup` with inline agents, then synthesizes everything into `.turbo/onboarding.md` and `.turbo/onboarding.html`. Analysis-only.

## Task Tracking

At the start, use `TaskCreate` to create a task for each phase:

1. Launch all agents
2. Synthesize and generate markdown report
3. Generate HTML report

## Step 1: Launch All Agents

Launch all Agent tool calls in parallel (`model: "opus"`, do not set `run_in_background`). Batch across multiple messages if the total exceeds what can be launched at once.

### Composed Skills

Launch one Agent tool call each. Each agent's prompt instructs it to invoke its assigned skill via the Skill tool.

| Skill | Onboarding role |
|---|---|
| `/map-codebase` | Architecture understanding: structure, tech stack, entry points, patterns, data flow, dependencies, testing |
| `/review-tooling` | Development workflow: linters, formatters, pre-commit hooks, test runners, CI/CD |
| `/review-agentic-setup` | Agentic coding: CLAUDE.md, AGENTS.md, skills, MCP servers, hooks, cross-tool compatibility |

### Inline Agents

Launch one Agent tool call each with the exploration brief below.

| Agent | Exploration Brief |
|---|---|
| Prerequisites and Setup | Read README.md, CONTRIBUTING.md, and package manager configs (package.json, Gemfile, Cargo.toml, go.mod, pyproject.toml, Package.swift, etc.). Extract: required language runtimes and versions, system dependencies, environment variables, database or service requirements, first-time setup steps (install, build, run, seed), and any bootstrap or setup scripts. |
| Troubleshooting | Search for troubleshooting content in README.md, TROUBLESHOOTING.md, docs/ directory, FAQ files, and GitHub Discussions/Wiki if accessible. Extract common errors, known quirks, platform-specific gotchas, and debugging tips. If no troubleshooting docs exist, report that. |
| Next Steps | Run `gh issue list --state open --json number,title,url,reactionGroups,comments,labels --limit 50`. Identify: (1) issues labeled `good-first-issue` or `good first issue`, (2) top 5 issues by engagement score (sum of reactions weighted 2x for thumbs-up, plus comment count). If `gh` is not available or not in a GitHub repo, skip and note that. |

Each agent writes its findings as structured markdown.

## Step 2: Synthesize and Generate Markdown Report

After all agents complete:

1. Read all agent reports. Check if `.turbo/threat-model.md` exists; if so, read it for the Security Considerations section.
2. Reframe review skill outputs as documentation. `/review-tooling` findings become "Development Workflow" (what tools are used and how to run them). `/review-agentic-setup` findings become "AI-Assisted Development" (what's set up and how to use it). Focus on what exists, not what's missing. Strip severity labels, findings numbering, and gap framing from review skill outputs. Present detected tools and configurations as project conventions the new developer should know.
3. Write a brief welcome summary (3-5 sentences) capturing what the project is, who it's for, and the fastest path to a first contribution.
4. Write `.turbo/onboarding.md` using the report template. Output the welcome summary as text before writing the file.

### Report Template

```markdown
# Onboarding Guide

**Date:** <date>
**Project:** <project name>

## Welcome

<3-5 sentences: what this project is, who it's for, fastest path to a first contribution>

## Prerequisites and Setup

<from Prerequisites and Setup agent: language runtimes, dependencies, first-time setup steps, build/run commands>

## Architecture Overview

<from /map-codebase: condensed executive summary and key structural insights — not the full report, which lives at .turbo/codebase-map.md>

## Development Workflow

<from /review-tooling: reframed as "how to develop" — what linters/formatters to run, how to test, pre-commit hooks, CI/CD pipeline>

## AI-Assisted Development

<from /review-agentic-setup: reframed as "how to use AI coding tools" — what CLAUDE.md/AGENTS.md cover, installed skills, MCP servers, cross-tool compatibility>

## Security Considerations

<from .turbo/threat-model.md if present: key trust boundaries, security-sensitive areas, and what to be careful with — or omit this section if no threat model exists>

## Troubleshooting

<from Troubleshooting agent: common errors, known quirks, debugging tips, or "no troubleshooting docs found">

## Next Steps

<from Next Steps agent: good-first-issue issues, top-engaged issues, or "no GitHub issues found">
```

## Step 3: Generate HTML Report

Convert the markdown report into a styled, interactive HTML page.

1. Run the `/frontend-design` skill to load design principles.
2. Read `.turbo/onboarding.md` for the full report content.
3. Write a self-contained `.turbo/onboarding.html` (single file, no external dependencies beyond Google Fonts) that presents the onboarding guide with:
   - Welcome section as a prominent header card
   - Sticky navigation between sections
   - Collapsible sections for Architecture Overview and Development Workflow
   - File and directory references as styled inline code
   - GitHub issue links as clickable cards with engagement indicators
   - Entrance animations and hover states
   - Print-friendly styles via `@media print`
   - Responsive layout for mobile

## Rules

- If any skill or agent fails, proceed with the remaining results and note the failure in the report.
- The `/map-codebase` skill produces its own full report at `.turbo/codebase-map.md`. The onboarding guide includes a condensed summary and links to the full report.
- Reframe review findings as documentation. The onboarding guide describes what exists and how to use it. Gaps from review skills can appear as brief recommendations, not as a findings list.
- Does not modify source code, stage files, or commit.
