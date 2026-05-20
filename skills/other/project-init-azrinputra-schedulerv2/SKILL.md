---
name: project-init
description: Initialize a new FIRE project by detecting workspace type and setting up standards.
version: 1.0.0
---

<objective>
Initialize a new FIRE project by detecting workspace type and setting up standards.
</objective>

<triggers>
  - User runs `/specsmd-fire` on uninitialized project
  - No `.specs-fire/state.yaml` exists
</triggers>

<flow>
  <step n="1" title="Welcome">
    <output>
      Welcome to FIRE (Fast Intent-Run Engineering).

      Let me analyze your project to get started.
    </output>
  </step>

  <step n="2" title="Detect Workspace">
    <action>Analyze project root for existing code</action>
    <check if="src/ or app/ or main entry points exist">
      <set>workspace.type = brownfield</set>
    </check>
    <check if="minimal files, no source directories">
      <set>workspace.type = greenfield</set>
    </check>
  </step>

  <step n="3a" title="Brownfield Setup" if="workspace.type == brownfield">
    <output>
      Existing project detected. I'll analyze your codebase to infer standards.
    </output>
    <action>Detect tech stack (language, framework, database)</action>
    <action>Detect structure (monolith, monorepo)</action>
    <action>Infer coding patterns</action>

    <monorepo_detection>
      Check for monorepo indicators:
      - nx.json, turbo.json, pnpm-workspace.yaml, lerna.json, rush.json
      - package.json with "workspaces" field
      - Cargo.toml with [workspace] section
      - go.work file
      - Multiple independent package/dependency manifests
      - Common patterns: packages/*, apps/*, services/*, libs/*

      If any indicator found → workspace.structure = "monorepo"
    </monorepo_detection>

    <output>
      Here's what I found:

      **Tech Stack**: {detected_tech}
      **Structure**: {detected_structure}
      **Patterns**: {detected_patterns}

      Does this look accurate? [Y/n/edit]
    </output>
  </step>

  <step n="3b" title="Greenfield Setup" if="workspace.type == greenfield">
    <ask>
      What do you want to build? Tell me about:
      - What the project does
      - Target users
      - Key features
    </ask>
    <action>Analyze description, suggest tech stack</action>
    <output>
      Based on your description, I suggest:

      **Language**: {suggested_language}
      **Framework**: {suggested_framework}
      **Database**: {suggested_database}

      Accept these suggestions? [Y/n/edit]
    </output>
  </step>

  <step n="4" title="Choose Autonomy Level">
    <output>
      How autonomous should FIRE be when executing work items?

      **[1] Autonomous** — AI executes more freely, fewer checkpoints
           (medium complexity → autopilot, high → confirm)

      **[2] Balanced** — Standard checkpoints based on complexity (Recommended)
           (low → autopilot, medium → confirm, high → validate)

      **[3] Controlled** — More human oversight, more checkpoints
           (low → confirm, medium/high → validate)

      Choose [1/2/3]:
    </output>
    <check if="response == 1">
      <set>workspace.autonomy_bias = autonomous</set>
    </check>
    <check if="response == 2">
      <set>workspace.autonomy_bias = balanced</set>
    </check>
    <check if="response == 3">
      <set>workspace.autonomy_bias = controlled</set>
    </check>
    <note>Can be changed later in .specs-fire/state.yaml</note>
  </step>

  <step n="5" title="Detect Modules" if="workspace.structure == monorepo">
    <output>
      Monorepo detected. Let me find and analyze the modules.
    </output>

    <action>Find module directories by exploring:</action>
    <substep>Paths from workspace config (nx.json projects, pnpm-workspace.yaml, etc.)</substep>
    <substep>Common patterns: packages/*, apps/*, services/*, libs/*, modules/*</substep>
    <substep>Directories with their own dependency manifest</substep>

    <action>For each discovered module, analyze (AI-driven, no hardcoded mappings):</action>
    <substep>Primary language (from file extensions, config files)</substep>
    <substep>Build/test commands (from CI config, package scripts, Makefile)</substep>
    <substep>Linter/formatter (from config files in module)</substep>
    <substep>Package manager (from lock files, manifests)</substep>

    <output>
      Found {{module_count}} modules:

      | Module | Language | Test Command | Linter |
      |--------|----------|--------------|--------|
      {{#each modules}}
      | {{path}} | {{language}} | {{test_cmd}} | {{linter}} |
      {{/each}}

      Create module-specific standards?
      [c] All modules — create standards for all
      [s] Select — choose which modules
      [n] None — I'll create them manually later
    </output>

    <check if="response == c or response == s">
      <action>For each selected module, create {module}/.specs-fire/standards/tech-stack.md</action>
      <note>Only tech-stack.md by default — other standards inherit from root</note>
    </check>
  </step>

  <step n="6" title="Create Structure">
    <action>Create .specs-fire/ directory</action>
    <action>Create .specs-fire/intents/</action>
    <action>Create .specs-fire/runs/</action>
    <action>Create .specs-fire/standards/</action>
    <action>Generate .specs-fire/state.yaml (include autonomy_bias, workspace.structure)</action>
    <action>Generate standards using templates:</action>
    <substep>constitution.md — templates/constitution.md.hbs</substep>
    <substep>tech-stack.md — templates/tech-stack.md.hbs</substep>
    <substep>coding-standards.md — templates/coding-standards.md.hbs</substep>
    <substep>testing-standards.md — templates/testing-standards.md.hbs</substep>
    <substep>system-architecture.md — templates/system-architecture.md.hbs</substep>

    <check if="workspace.structure == monorepo and modules_selected">
      <action>For each selected module:</action>
      <substep>Create {module}/.specs-fire/standards/</substep>
      <substep>Generate {module}/.specs-fire/standards/tech-stack.md with detected settings</substep>
    </check>
  </step>

  <step n="7" title="Complete">
    <output>
      FIRE initialized!

      Structure created:
      ```
      .specs-fire/
      ├── state.yaml
      ├── intents/
      ├── runs/
      └── standards/
          ├── constitution.md        # Universal policies (always inherited)
          ├── tech-stack.md
          ├── coding-standards.md
          ├── testing-standards.md
          └── system-architecture.md
      {{#if modules_created}}

      Module standards created:
      {{#each modules_created}}
      {{path}}/.specs-fire/standards/
      └── tech-stack.md
      {{/each}}
      {{/if}}
      ```

      Ready to capture your first intent.
      What do you want to build?
    </output>
    <route_to>planner-agent (intent-capture)</route_to>
  </step>
</flow>

<output_artifacts>

  | Artifact | Location | Template |
  |----------|----------|----------|
  | State | `.specs-fire/state.yaml` | — |
  | Constitution | `.specs-fire/standards/constitution.md` | `templates/constitution.md.hbs` |
  | Tech Stack | `.specs-fire/standards/tech-stack.md` | `templates/tech-stack.md.hbs` |
  | Coding Standards | `.specs-fire/standards/coding-standards.md` | `templates/coding-standards.md.hbs` |
  | Testing Standards | `.specs-fire/standards/testing-standards.md` | `templates/testing-standards.md.hbs` |
  | System Architecture | `.specs-fire/standards/system-architecture.md` | `templates/system-architecture.md.hbs` |
  | Module Tech Stack | `{module}/.specs-fire/standards/tech-stack.md` | AI-generated |
</output_artifacts>

<success_criteria>
  <criterion>Workspace type correctly detected (greenfield/brownfield)</criterion>
  <criterion>Workspace structure correctly detected (monolith/monorepo)</criterion>
  <criterion>Tech stack identified or suggested</criterion>
  <criterion>Autonomy level selected</criterion>
  <criterion>.specs-fire/ directory structure created</criterion>
  <criterion>constitution.md generated (universal policies)</criterion>
  <criterion>Standards files generated from templates</criterion>
  <criterion>state.yaml created with correct configuration</criterion>
  <criterion>If monorepo: modules detected and analyzed</criterion>
  <criterion>If monorepo: module standards created for selected modules</criterion>
</success_criteria>
