---
name: workflow
description: "Structured multi-phase workflows: review, debug, refactor (tidy up, clean up, untangle messy code, reorganize without changing behaviour), deploy, create, research, and more."
user-invocable: false
context: fork
routing:
  category: meta-tooling
  pairs_with:
    - planning
    - feature-lifecycle
    - verification-before-completion
  triggers:
    - "workflow"
    - "multi-phase task"
    - "structured pipeline"
    - "phased execution"
    - "orchestrated workflow"
    - "tidy up"
    - "tidy it"
    - "tidy into one place"
    - "clean up"
    - "messy"
    - "messy code"
    - "structure is messy"
    - "reorganize"
    - "reorganize without changing behaviour"
    - "reorganize without changing behavior"
    - "untangle"
    - "consolidate duplicated"
    - "duplicated everywhere"
    - "repeated everywhere"
allowed-tools:
  - Read
  - Edit
  - Write
  - Bash
  - Glob
  - Grep
  - Agent
  - Skill
---

# Workflow

Umbrella skill for all structured multi-phase workflows.
Load the appropriate workflow reference based on the task.

**Terminology:** "workflow" is the canonical term for these flows. "pipeline" is the retained legacy alias — kept for back-compat. Routing keys, `meta.name` exports, and `pipeline-index.json` keep their existing "pipeline" identifiers unchanged; do not rename them. Use "workflow" in new prose.

## Available Workflows

| Category | Workflow | Reference |
|----------|----------|-----------|
| **Code Review** | Comprehensive multi-wave review | `references/comprehensive-review.md` |
| **Code Review** | Systematic code review | `references/systematic-code-review.md` |
| **Debugging** | Evidence-based debugging pipeline | `references/systematic-debugging.md` |
| **Refactoring** | Safe refactoring with test gates | `references/systematic-refactoring.md` |
| **Features** | End-to-end feature lifecycle | `skills/process/feature-lifecycle/references/pipeline.md` |
| **PR Workflow** | PR creation pipeline | `skills/process/pr-workflow/references/pipeline.md` |
| **Research** | Formal research with source gates | `references/research-pipeline.md` |
| **Research** | Research to article pipeline | `references/research-to-article.md` |
| **Content** | Voice content generation | `references/voice-writer.md` |
| **Content** | Voice calibration | `references/voice-calibrator.md` |
| **Content** | Article evaluation | `references/article-evaluation-pipeline.md` |
| **Content** | De-AI content pipeline | `references/de-ai-pipeline.md` |
| **Content** | Documentation pipeline | `references/doc-pipeline.md` |
| **Exploration** | Codebase exploration | `references/explore-pipeline.md` |
| **Exploration** | Multi-perspective analysis | `references/do-perspectives.md` |
| **Creation** | Skill creation pipeline | `references/skill-creation-pipeline.md` |
| **Creation** | Hook development pipeline | `references/hook-development-pipeline.md` |
| **Creation** | MCP server pipeline | `references/mcp-pipeline-builder.md` |
| **Creation** | Pipeline scaffolding | `references/pipeline-scaffolder.md` |
| **Creation** | Domain research for pipelines | `references/domain-research.md` |
| **Creation** | Chain composition | `references/chain-composer.md` |
| **Creation** | Auto-pipeline generation | `references/auto-pipeline.md` |
| **Upgrade** | Agent/skill upgrade | `references/agent-upgrade.md` |
| **Upgrade** | System upgrade | `references/system-upgrade.md` |
| **Upgrade** | Toolkit improvement | `references/toolkit-improvement.md` |
| **Testing** | Pipeline test runner | `references/pipeline-test-runner.md` |
| **Testing** | Pipeline retro | `references/pipeline-retro.md` |
| **GitHub** | Profile rules extraction | `references/github-profile-rules.md` |
| **Orchestration** | Task orchestration | `references/workflow-orchestrator.md` |
| **Patterns** | Composable-pattern + failure-mode + cost-gate catalog | `references/workflow-patterns.md` |
| **Patterns** | Tournament (pairwise-comparison) template | `references/tournament-workflow.md` |
| **Patterns** | Quarantine (untrusted-source triage isolation) | `references/quarantine-pattern.md` |

## How to Use (MANDATORY)

**You MUST load the reference file before executing any workflow phase.** The table above is a routing index — the actual methodology, phases, gates, and instructions are in the reference files.

1. **Identify** the workflow category from the user's task using the table above
2. **Load** the matching reference file using `Read` tool on `${CLAUDE_SKILL_DIR}/references/<name>.md`
3. **Follow** the phases and gates defined in that reference exactly — do not improvise phases
4. **Report** using the output format specified in the loaded reference

If the task spans multiple workflows (e.g., research then write), load each reference in sequence and follow them in order.

**Workflow rule**: Load the reference file before executing a workflow phase. The table shows names only; the reference file contains the actual instructions, gates, artifact requirements, and quality criteria.

## Reference Loading Table

| Signal | Load These Files | Why |
|---|---|---|
| **Code Review** | `comprehensive-review.md` | Comprehensive multi-wave review |
| **Code Review** | `systematic-code-review.md` | Systematic code review |
| **Debugging** | `systematic-debugging.md` | Evidence-based debugging pipeline |
| **Refactoring** | `systematic-refactoring.md` | Safe refactoring with test gates |
| **Features** | `pipeline.md` | End-to-end feature lifecycle |
| **PR Workflow** | `pipeline.md` | PR creation pipeline |
| **Research** | `research-pipeline.md` | Formal research with source gates |
| **Research** | `research-to-article.md` | Research to article pipeline |
| **Content** | `voice-writer.md` | Voice content generation |
| **Content** | `voice-calibrator.md` | Voice calibration |
| **Content** | `article-evaluation-pipeline.md` | Article evaluation |
| **Content** | `de-ai-pipeline.md` | De-AI content pipeline |
| **Content** | `doc-pipeline.md` | Documentation pipeline |
| **Exploration** | `explore-pipeline.md` | Codebase exploration |
| **Exploration** | `do-perspectives.md` | Multi-perspective analysis |
| **Creation** | `skill-creation-pipeline.md` | Skill creation pipeline |
| **Creation** | `hook-development-pipeline.md` | Hook development pipeline |
| **Creation** | `mcp-pipeline-builder.md` | MCP server pipeline |
| **Creation** | `pipeline-scaffolder.md` | Pipeline scaffolding |
| **Creation** | `domain-research.md` | Domain research for pipelines |
| **Creation** | `chain-composer.md` | Chain composition |
| **Creation** | `auto-pipeline.md` | Auto-pipeline generation |
| **Upgrade** | `agent-upgrade.md` | Agent/skill upgrade |
| **Upgrade** | `system-upgrade.md` | System upgrade |
| **Upgrade** | `toolkit-improvement.md` | Toolkit improvement |
| **Testing** | `pipeline-test-runner.md` | Pipeline test runner |
| **Testing** | `pipeline-retro.md` | Pipeline retro |
| **GitHub** | `github-profile-rules.md` | Profile rules extraction |
| **Orchestration** | `workflow-orchestrator.md` | Task orchestration |
| **Patterns / cost gate / failure modes** | `workflow-patterns.md` | Which named pattern + when to escalate + when NOT to use |
| **Tournament** | `tournament-workflow.md` | Pairwise-comparison ranking template |
| **Quarantine** | `quarantine-pattern.md` | Isolate untrusted-source readers from privileged actions |
