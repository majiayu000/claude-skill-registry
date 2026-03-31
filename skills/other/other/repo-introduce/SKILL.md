---
name: repo-introduce
description: "{{ 𝛀𝛀𝛀 }} Provide a detailed high-level overview of this codebase"
model: opus
disable-model-invocation: true
allowed-tools: ["Read", "Glob", "Grep", "Bash", "Write"]
argument-hint: [focus of analysis]
---

<overview>
  Produce an interactive visual overview of this codebase aimed at a newly-joined developer.
  Uses the visual-explainer plugin to generate a standalone HTML page with architecture diagrams,
  module relationships, and project context.
</overview>
<steps>
  1. Load the visual-explainer skill.
  2. Analyse the codebase:
     - Read README.md, package.json/go.mod/Cargo.toml/pyproject.toml for identity and dependencies
     - Map top-level directory structure and entry points
     - Read key source files to understand module structure and public API surface
     - Skim git log for recent activity and key decisions
  3. If $ARGUMENTS contains content, treat it as a focus area and weight the analysis accordingly.
  4. Generate a visual HTML page following the visual-explainer workflow:
     - Architecture snapshot (Mermaid diagram of modules and their relationships)
     - Project identity: what it does, who uses it, what stage it's at
     - Mental model essentials: invariants, non-obvious coupling, naming conventions, gotchas
     - Module map with responsibilities
  5. Write to ~/.agent/diagrams/ and open in browser.
</steps>
<inputs>
  $ARGUMENTS
</inputs>
