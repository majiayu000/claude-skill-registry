---
name: skill-axel-core
description: |
  Trigger-based workflow dispatcher for AXEL core operations. Receives explicit trigger from command and dispatches to matching workflow.
type: skill
model: inherit
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Bash
  - Task
  - AskUserQuestion
---

# AXEL Skill: Core

```xml
<document type="skill">

  <enforcement>
    <![CDATA[
    DOCUMENT LOADING ORDER:
    - AXEL-Bootstrap.md MUST be loaded FIRST before processing this skill
    - Bootstrap provides core AXEL rules and understanding guidelines
    - All other documents depend on Bootstrap being in context

    PATH RESOLUTION:
    - Read the `src`, `ref`, or `target` attribute from the document XML to locate referenced files
    - ${CLAUDE_PLUGIN_ROOT} resolves to plugin installation directory

    DOCUMENT REFERENCES:
    - CLAUDE.md is automatically loaded by Claude Code - DO NOT add to <documents> block
    - Use Read tool to access CLAUDE.md content during execution

    TRIGGER-BASED DISPATCH:
    - Command sends explicit trigger parameter
    - Skill matches trigger against workflows registry
    - Matching workflow is loaded and executed

    DOCUMENT CREATION VALIDATION:
    - Creator workflows (create:*) MUST load and apply AXEL-Checklist.md step-by-step
    - Location: ${CLAUDE_PLUGIN_ROOT}/references/AXEL-Checklist.md

    DOCUMENT RESOLUTION:
    - When trigger doesn't match workflows, resolve reference documents
    - Analyze prompt keywords against documents:references "ask" attributes
    - Load relevant reference documents on-demand
    - Use loaded references to answer user request
    ]]>
  </enforcement>

  <objective>
    Trigger-based workflow dispatcher for AXEL core operations.
    Matches incoming trigger to workflow registry and executes.
    When no workflow matches, resolves and loads reference documentation
    to answer user requests about AXEL concepts and patterns.
  </objective>

  <documents name="bootstrap" load="always" mode="context">
    <read src="${CLAUDE_PLUGIN_ROOT}/AXEL-Bootstrap.md"/>
    <understanding>
      !! MANDATORY: READ → UNDERSTAND → APPLY !!
      Bootstrap provides AXEL core, enforcement rules, and understanding guidelines.
    </understanding>
  </documents>

  <documents name="references" load="on-demand" mode="context">
    <read src="${CLAUDE_PLUGIN_ROOT}/skills/skill-axel-core/references/AXEL-Standards.md" ask="standard, pattern, element"/>
    <read src="${CLAUDE_PLUGIN_ROOT}/skills/skill-axel-core/references/AXEL-Conventions.md" ask="convention, style, format"/>
    <read src="${CLAUDE_PLUGIN_ROOT}/skills/skill-axel-core/references/AXEL-Agent.md" ask="agent, autonomous, executor"/>
    <read src="${CLAUDE_PLUGIN_ROOT}/skills/skill-axel-core/references/AXEL-Workflow.md" ask="workflow, process, step"/>
    <read src="${CLAUDE_PLUGIN_ROOT}/skills/skill-axel-core/references/AXEL-Skill.md" ask="skill, expertise, capability"/>
    <read src="${CLAUDE_PLUGIN_ROOT}/skills/skill-axel-core/references/AXEL-Command.md" ask="command, slash, invoke"/>
    <read src="${CLAUDE_PLUGIN_ROOT}/skills/skill-axel-core/references/AXEL-Brainstorm.md" ask="brainstorm, discovery, ideation"/>
    <read src="${CLAUDE_PLUGIN_ROOT}/skills/skill-axel-core/references/AXEL-Memory.md" ask="memory, context, persistence"/>
    <read src="${CLAUDE_PLUGIN_ROOT}/skills/skill-axel-core/references/AXEL-Claude.md" ask="claude, configuration, project"/>
    <understanding>
      !! LOAD ON-DEMAND: Trigger Mismatch Fallback !!

      When to Load:
      - ONLY when resolved trigger doesn't match workflows:operations registry
      - User request doesn't map to any workflow trigger
      - User asking about AXEL concepts, patterns, or documentation

      How to Load:
      - Analyze prompt keywords from user request
      - Match keywords against "ask" attributes of each reference document
      - Load all matching reference documents into context
      - Use loaded references to provide comprehensive answer

      Examples:
      - "what is an agent?" → load AXEL-Agent.md (ask: agent, autonomous, executor)
      - "how to write workflow?" → load AXEL-Workflow.md (ask: workflow, process, step)
      - "what are the standards?" → load AXEL-Standards.md (ask: standard, pattern, element)

      Available References:
      - Standards & Conventions (structural rules)
      - All AXEL document types (Agent, Workflow, Skill, Command, Memory, Brainstorm, Claude)
    </understanding>
  </documents>

  <role>
    Workflow dispatcher that routes trigger-based requests
    to appropriate AXEL core operation workflows.
  </role>

  <capabilities>
    - Receive trigger parameter from command
    - Match trigger against workflows registry
    - Load and execute matching workflow
    - Pass parameters to workflow
    - Resolve reference documents when workflow not matched
    - Answer user requests using loaded reference documentation
  </capabilities>

  <workflows name="operations" load="on-trigger">
    <!-- brainstorm -->
    <read src="${CLAUDE_PLUGIN_ROOT}/skills/skill-axel-core/workflows/brainstorm/AXEL-Brainstorm-Bootstrap.md" trigger="brainstorm"/>
    <!-- creators -->
    <read src="${CLAUDE_PLUGIN_ROOT}/skills/skill-axel-core/workflows/creators/AXEL-Agent-Creator-Workflow.md" trigger="create:agent"/>
    <read src="${CLAUDE_PLUGIN_ROOT}/skills/skill-axel-core/workflows/creators/AXEL-Brainstorm-Creator-Workflow.md" trigger="create:brainstorm"/>
    <read src="${CLAUDE_PLUGIN_ROOT}/skills/skill-axel-core/workflows/creators/AXEL-Workflow-Creator-Workflow.md" trigger="create:workflow"/>
    <read src="${CLAUDE_PLUGIN_ROOT}/skills/skill-axel-core/workflows/creators/AXEL-Skill-Creator-Workflow.md" trigger="create:skill"/>
    <read src="${CLAUDE_PLUGIN_ROOT}/skills/skill-axel-core/workflows/creators/AXEL-Command-Creator-Workflow.md" trigger="create:command"/>
    <!-- utilities -->
    <read src="${CLAUDE_PLUGIN_ROOT}/skills/skill-axel-core/workflows/utilities/AXEL-Fix-Workflow.md" trigger="fix"/>
    <read src="${CLAUDE_PLUGIN_ROOT}/skills/skill-axel-core/workflows/utilities/AXEL-Compact-Workflow.md" trigger="compact"/>
    <read src="${CLAUDE_PLUGIN_ROOT}/skills/skill-axel-core/workflows/utilities/AXEL-Bypass-Workflow.md" trigger="bypass"/>
    <read src="${CLAUDE_PLUGIN_ROOT}/skills/skill-axel-core/workflows/utilities/AXEL-Install-Workflow.md" trigger="install"/>
    <read src="${CLAUDE_PLUGIN_ROOT}/skills/skill-axel-core/workflows/utilities/AXEL-Commit-Workflow.md" trigger="commit"/>
    <understanding>
      !! MANDATORY: READ → UNDERSTAND → APPLY !!
      Trigger-based workflow registry. Match resolved trigger to execute workflow.
    </understanding>
  </workflows>

  <execution flow="linear"><![CDATA[
    WORKFLOW DISPATCH:

    Step 1 - Receive Parameters:
    - trigger: ${param.trigger} (optional)
    - prompt: ${param.prompt} (optional)
    - Additional: topic, doc_type, target_path

    Step 2 - Resolve Trigger:
    - IF trigger provided → use directly
    - IF trigger empty → detect from prompt:

      Keyword Priority (first match):
      1. "create" + "agent"      → create:agent
      2. "create" + "brainstorm" → create:brainstorm
      3. "create" + "workflow"   → create:workflow
      4. "create" + "skill"      → create:skill
      5. "create" + "command"    → create:command
      6. "brainstorm"            → brainstorm
      7. "validate" | "fix"      → validate
      8. "compact" | "archive"   → compact
      9. "bypass" | "permissions"→ bypass
      10. "install" | "init"     → install
      11. "commit"               → commit

    Step 3 - Match Workflow:
    - Check if resolved trigger matches workflows:operations registry
    - IF trigger matched → GO TO Step 4 (Execute workflow)
    - IF trigger NOT matched → GO TO Step 3.1 (Resolve Documents)

    Step 3.1 - Resolve Documents (fallback when no workflow match):
    - Analyze prompt keywords
    - Match keywords to documents:references "ask" attributes
    - Load relevant reference documents from on-demand registry
      → Example: "agent" keyword → load AXEL-Agent.md
      → Example: "workflow" keyword → load AXEL-Workflow.md
      → Example: "standard" keyword → load AXEL-Standards.md
    - Use loaded references to answer user request
    - SKIP Step 4

    Step 4 - Execute Workflow:
    - IF trigger starts with "create:":
      → Load ${CLAUDE_PLUGIN_ROOT}/references/AXEL-Checklist.md
      → Execute matched workflow with parameters
      → Validate created document step-by-step against checklist (all phases)
    - ELSE:
      → Execute matched workflow with parameters
  ]]></execution>

  <understanding/>

</document>
```
