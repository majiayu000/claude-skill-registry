---
name: axel-skill
description: Structure of skill definition files - role, capabilities, enforcement, registry
type: reference
---

```xml
<document type="reference">

  <enforcement>
    - Read `src` and `ref` attributes from skill references to locate files
    - ${CLAUDE_PLUGIN_ROOT} resolves to plugin installation directory
    - Skill files located in .claude/skills/skill-{name}/ directory
  </enforcement>

  <objective>
    Structure of skill definition files. AXEL Skill is a configuration format that enables AI to specialize in a specific area. Each skill defines a role, capability set, and operating rules for the AI, ensuring consistent and high-quality output.
  </objective>

  <frontmatter>
    <![CDATA[
---
name: skill-frontend             # Skill identifier (with skill- prefix)
description: Frontend dev skill  # Short description, 200 characters
type: skill                      # Always "skill"
allowed-tools:                   # Available tools
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - AskUserQuestion
disable-model-invocation: false  # true = manual-only, no auto-invoke (optional)
---
    ]]>
  </frontmatter>

  <templates load="always" mode="context">
    <read src="${CLAUDE_PLUGIN_ROOT}/skills/skill-axel-core/templates/skill/AXEL-Skill-Template-Bootstrap.md"/>
    <axel-tag-structure>
      <![CDATA[
      AXEL-Skill-Tpl.md (Linear) / AXEL-Skill-Staged-Tpl.md (Staged)
      +-- Template Frontmatter
      +-- # AXEL Skill (title)
      +-- {{{xml}}}
      +-- <document type="skill">
      |   +-- <enforcement>
      |   +-- <objective>
      |   +-- <documents name=".." load="always" mode="context">
      |   |   +-- <read src="..."/>
      |   |   +-- <understanding>...</understanding> (required)
      |   +-- <documents name=".." load="on-trigger" mode="context">
      |   |   +-- <read src="..." trigger="..."/>
      |   |   +-- <understanding>...</understanding> (required)
      |   +-- <documents name=".." load="on-demand" mode="context">
      |   |   +-- <read src="..." ask="..."/>
      |   |   +-- <understanding>...</understanding> (required)
      |   +-- <role>
      |   +-- <capabilities>
      |   +-- <templates name=".." load="always|on-demand|on-trigger" mode="context"> (optional)
      |   |   +-- <read src="..." ask="..."/>
      |   |   +-- <understanding>...</understanding> (required)
      |   +-- <examples> (optional)
      |   |   +-- <example name="..." language="...">
      |   +-- <workflows name=".." load="always|on-demand|on-trigger" mode="context">
      |   |   +-- <read src="..." trigger="..."/>
      |   |   +-- <understanding>...</understanding> (required)
      |   +-- <skills name=".." load="on-demand"> (optional)
      |   |   +-- <ref src="..." ask="..."/>
      |   +-- <agents name=".." load="on-demand"> (optional)
      |   |   +-- <ref src="..." ask="..."/>
      |   +-- <triggers> (optional, for staged only)
      |   |   +-- <goto trigger="..." to="stage-id"/>
      |   +-- <execution flow="linear|staged">
      |   |   +-- (linear) text-based step instructions
      |   |   +-- (staged) <stage id="...">
      |   |       +-- <print>...</print>
      |   |       +-- <tasks output="...">...</tasks>
      |   |       +-- <bash run="..."/>
      |   |       +-- <workflow src="..." output="...">
      |   |       |   +-- <param name="..." value="..."/>
      |   |       +-- <call command="/..."/>
      |   |       +-- <ask var="..." prompt="...">
      |   |       |   +-- <goto when="..." to="stage-id"/>
      |   |       +-- <invoke name="Task|Skill" output="..." resumable="true|false">
      |   |       |   +-- <param name="..." value="..."/>
      |   |       +-- <set var="..." from="..."/>
      |   |       +-- <goto when="..." to="stage-id"/>
      |   |       +-- <stop kind="end|error"/>
      +-- </document>
      +-- {{{xml}}}
      ]]>
    </axel-tag-structure>
    <understanding>
      !! MANDATORY: READ → UNDERSTAND → APPLY !!
      - READ the template file first
      - UNDERSTAND the structure and patterns
      - APPLY the template structure EXACTLY
      Reference = HOW to think | Template = HOW to write
    </understanding>
  </templates>

  <context>
    - Used to specialize AI in a specific domain
    - Defines role, capabilities, and operating rules
    - Activated by trigger keywords
    - Ensures consistent and high-quality output
    - Integrates with documents, templates, and workflows
  </context>

  <principle name="skill-structure">
    - role: Defines who the AI is (persona, expertise level)
    - objective: Main goal and purpose of the skill
    - capabilities: What the skill can do (bullet list)
    - documents: Reference documents (load="always" or "on-trigger")
    - templates: Output templates (load="on-trigger")
    - workflows: Step-by-step processes (load="on-trigger")
    - triggers: Stage routing rules (optional, for staged execution)
    - execution: Linear text or staged XML blocks (flow="linear|staged")
  </principle>

  <principle name="staged-execution">
    When to use staged execution (flow="staged"):
    - Complex skills requiring multi-step processing
    - Skills with branching logic based on input
    - Skills that invoke agents or workflows
    - Skills needing user confirmation checkpoints

    When to use linear execution (flow="linear"):
    - Simple guidance-only skills
    - Skills with straightforward single-path logic
    - Skills focused on context provision, not task orchestration

    Stage elements:
    - stage id="...": Define execution stage
    - tasks output="...": Declarative task block
    - print: Output message to user
    - set var="..." from="...": Variable assignment
    - goto when="..." to="...": Conditional jump
    - invoke name="...": Call agent/skill
    - workflow src="...": Execute workflow
    - stop kind="end|error": Terminate execution
  </principle>

  <principle name="trigger-routing">
    Automatic stage routing based on user input triggers.

    Trigger format:
    - Single phrase: trigger="create component"
    - Multiple keywords: trigger="[a11y, accessibility, wcag]"

    Behavior:
    - When skill activates, check user message against triggers
    - If match found, jump directly to target stage
    - If no match, start from "init" stage (default)

    Example:
    <triggers>
      <goto trigger="create component" to="component-create"/>
      <goto trigger="[test, testing]" to="test-stage"/>
    </triggers>
  </principle>

  <principle name="registry-loading">
    - load="always": Always load into context
    - load="on-demand": Load when requested (ask keywords)
    - load="on-trigger": Load when specific triggers match
    - mode="context": Add document content to AI context
    - mode="map": Load as reference map only
  </principle>

  <pattern name="naming-convention">
    <![CDATA[
    Skill Naming (Claude Code Style)

    Two scope levels:

    1. Plugin Level:
       Format: {plugin}:{skill-name}
       Example: axel:skill-axel-expert

    2. User Project Level:
       Format: {project}:{skill-name}
       Example: myproject:skill-frontend

    Structure:
    <skills name="expert-skills" load="on-demand">
      <ref src="axel:skill-axel-expert" ask="axel, dsl, document"/>
      <ref src="axel:skill-axel-researcher" ask="research"/>
    </skills>

    Usage in registries:
    - src attribute uses this naming format
    - Claude Code resolves names to actual skill files
    - Plugin skills: Defined in plugin's skills/{skill-name}/ folder
    - User skills: Defined in project's .claude/skills/{skill-name}/ folder
    ]]>
  </pattern>

  <pattern name="agents-registry">
    <![CDATA[
    Agents registry for autonomous tasks within skills.

    Naming Format (Claude Code Style):

    1. Plugin Level:
       Format: {plugin}:{agent-folder}:{agent-name}
       Example: axel:agent-axel-project-create:agent-axel-project-create

    2. Plugin Skill Level:
       Format: {plugin}:{skill}:agents:{agent-name}
       Example: axel:skill-axel-expert:agents:agent-axel-expert-creator

    3. User Project Level:
       Format: {project}:{agent-folder}:{agent-name}
       Example: myproject:agent-code-reviewer:agent-code-reviewer

    4. User Skill Level:
       Format: {project}:{skill}:agents:{agent-name}
       Example: myproject:skill-frontend:agents:agent-component-generator

    Structure:
    <agents name="expert-agents" load="on-demand">
      <!-- Plugin skill sub-agent -->
      <ref src="axel:skill-axel-expert:agents:agent-axel-expert-creator" ask="create"/>
      <!-- Plugin level agent -->
      <ref src="axel:agent-project-analysis:agent-project-analysis" ask="analyze"/>
    </agents>

    Attributes:
    - name: Registry identifier (e.g., "expert-agents")
    - load: Always "on-demand" for agents
    - src: Claude Code agent naming style reference
    - ask: Keywords that trigger agent loading
    ]]>
  </pattern>

  <decision name="trigger-based-loading" date="2024-12">
    When: Defining document/template/workflow references
    Action: Use triggers attribute for conditional loading
    Example: triggers="[a11y, accessibility]"
    Reason: Optimizes context size by loading only relevant resources
  </decision>

  <decision name="enforcement-placement" date="2024-12">
    When: Creating skill files
    Action: AXEL-Enforcement.md comes from Bootstrap (no direct reference needed)
    Reason: Bootstrap provides core enforcement rules to all documents
  </decision>

  <requirements>
    - Frontmatter must include name (skill-* prefix), description, type: skill
    - Frontmatter must define allowed-tools list
    - Frontmatter may include disable-model-invocation (default: false)
    - Document root must have type="skill"
    - Role must define AI persona and expertise
    - Objective must specify skill purpose
    - Capabilities must be in bullet list format
    - Documents registry should be defined (AXEL-Enforcement comes from Bootstrap)
    - AXEL-Bootstrap.md MUST be loaded FIRST in documents registry with load="always"
    - Execution must specify flow="linear" or flow="staged"
    - Staged execution requires at least "init" and "complete" stages
    - Triggers tag is optional, only valid with flow="staged"
    - Stage ids must be unique within execution block
    - Last stage must end with <stop kind="end|error"/>
  </requirements>

  <implementation name="file-locations">
    <![CDATA[
    .claude/skills/skill-{name}/
    ├── SKILL.md                  # Main skill file (1,500-2,000 words max)
    ├── agents/                   # Skill-specific sub-agents
    │   └── agent-{name}/         # Sub-agent directory
    │       └── AGENT.md          # Sub-agent definition
    ├── references/               # Skill-specific references (2,000-5,000+ words each)
    │   ├── patterns.md           # Detailed patterns and guides
    │   └── advanced.md           # Advanced use cases
    ├── templates/                # Skill-specific templates
    ├── workflows/                # Skill-specific workflows
    ├── examples/                 # Working code examples
    │   ├── basic-example.sh      # Simple example
    │   └── advanced-example.json # Complex example
    └── scripts/                  # Validation/test tools
        ├── validate.sh           # Validation script
        └── test-trigger.sh       # Trigger test script
    ]]>
  </implementation>

  <principle name="progressive-disclosure">
    Content size management for context optimization:
    - Metadata (frontmatter): ~100 words, always in context
    - SKILL.md body: Max 5,000 words (ideal: 1,500-2,000)
    - Bundled resources (references/, examples/): Unlimited, load on-demand
    - Move detailed guides to references/
    - Move code samples to examples/
    - Move validation tools to scripts/
  </principle>

  <principle name="writing-style">
    <![CDATA[
    Imperative Form (MANDATORY):
    - CORRECT: "To create a hook, define the event type"
    - CORRECT: "Define the skill structure"
    - WRONG: "You should create a hook"
    - WRONG: "You need to define..."

    Third-Person Description (MANDATORY):
    - CORRECT: "This skill should be used when the user asks to..."
    - CORRECT: "This skill provides guidance for..."
    - WRONG: "Use this skill when you want to..."
    - WRONG: "I will help you with..."

    Content Rules:
    - Use bullet lists for tag contents
    - Keep instructions objective and instructional
    - Avoid second person ("you") in instructions
    - Use active voice in descriptions
    ]]>
  </principle>

  <principle name="trigger-description">
    <![CDATA[
    Description Format (in frontmatter):
    - Write detailed, specific trigger conditions
    - List exact phrases that should activate the skill
    - Include 2-4 concrete usage examples

    CORRECT Format:
    ---
    description: >
      This skill should be used when the user asks to "create a component",
      "add a React component", "build UI element", "implement frontend feature",
      or mentions component patterns (hooks, state, props, lifecycle).
      Provides guidance for React component development with TypeScript.
    ---

    WRONG Format:
    ---
    description: Frontend development skill
    ---

    Example Patterns in Description:
    - "This skill should be used when the user asks to..."
    - "...or mentions [topic] (keyword1, keyword2, keyword3)"
    - "Provides guidance for [specific domain]"
    ]]>
  </principle>

  <implementation name="creating-skill">
    Step 1 - Collect Identity:
    - Name: skill-* prefix, kebab-case (e.g., skill-frontend)
    - Description: max 200 chars

    Step 2 - Define Role & Objective:
    - Role: Who is the AI? (persona, expertise level)
    - Objective: Main goal and purpose

    Step 3 - Define Capabilities:
    - What can this skill do? (bullet list)

    Step 4 - Configure:
    - Tools: Read, Write, Edit, Glob, Grep, Bash, Task, WebFetch, WebSearch, AskUserQuestion
    - Disable model invocation: true | false (default: false)

    Step 5 - Define Execution:
    - Flow: linear | staged
    - If staged: which stages needed
    - Triggers for stage routing (optional)

    Step 6 - Validate:
    - Check against skill-validation checklist
    - Verify axel-tag-structure element order
    - Ensure understanding at document end

    Step 7 - Generate:
    - Map values to document elements in axel-tag-structure order
    - Save to: .claude/skills/${name}/SKILL.md

    Step 8 - AXEL Checklist:
    - MUST validate against AXEL-Checklist.md standards
    - Verify frontmatter, document-structure, element-order
    - Check execution-validation rules
  </implementation>

  <output format="markdown">
    File: SKILL.md
    Path: .claude/skills/skill-{name}/SKILL.md
    Structure:
    - YAML frontmatter (---)
    - Markdown title (# Skill Name)
    - AXEL XML in code fence (```xml ... ```)
    - Document type="skill" with role, capabilities, execution
  </output>

  <verification>
    - Is SKILL.md under .claude/skills/skill-{name}/?
    - Is frontmatter correct? (name: skill-*, type: skill)
    - Is allowed-tools list present?
    - Is role defined with persona and expertise?
    - Is objective clear and specific?
    - Is capabilities list present?
    - Is documents registry defined?
    - Is understanding at the end of document?
  </verification>

  <checklist name="skill-validation">
    Frontmatter:
    - Is name with skill-* prefix?
    - Is type: skill?
    - Is allowed-tools list present?
    - Is disable-model-invocation set correctly? (optional, default: false)

    Structure:
    - Is document type="skill" root element?
    - Is role defined with persona?
    - Is objective specified?
    - Is capabilities list in bullet format?

    Registries:
    - Is documents registry defined?
    - Is AXEL-Bootstrap.md FIRST in documents registry with load="always"?
    - Are load modes correct? (always/on-trigger)
    - Is understanding at the end of document?

    Execution (if staged):
    - Is flow="staged" set on execution element?
    - Is "init" stage defined?
    - Is "complete" stage defined?
    - Does last stage end with <stop/>?
    - Are all stage ids unique?

    Triggers (if using):
    - Is triggers tag inside document, before execution?
    - Does each goto have trigger and to attributes?
    - Do target stage ids exist in execution?
  </checklist>

  <understanding/>

</document>
```
