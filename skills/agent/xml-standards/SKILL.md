---
name: xml-standards
description: XML tag structure patterns for Claude Code agents and commands. Use when designing or implementing agents to ensure proper XML structure following Anthropic best practices.
---

# XML Tag Standards

## Core Tags (Required for ALL Agents/Commands)

### `<role>`
Defines agent identity and purpose.

```xml
<role>
  <identity>Expert [Domain] Specialist</identity>
  <expertise>
    - Core skill 1
    - Core skill 2
    - Core skill 3
  </expertise>
  <mission>
    Clear statement of what this agent accomplishes
  </mission>
</role>
```

### `<instructions>`
Defines behavior constraints and workflow.

```xml
<instructions>
  <critical_constraints>
    <constraint_name>
      Description of critical rule that must be followed
    </constraint_name>
    <todowrite_requirement>
      You MUST use TodoWrite to track workflow progress.
    </todowrite_requirement>
  </critical_constraints>

  <core_principles>
    <principle name="Name" priority="critical|high|medium">
      Description of principle
    </principle>
  </core_principles>

  <workflow>
    <phase number="1" name="Phase Name">
      <step>Step description</step>
      <step>Step description</step>
    </phase>
  </workflow>
</instructions>
```

### `<knowledge>`
Domain-specific best practices and templates.

```xml
<knowledge>
  <section_name>
    Best practices, patterns, or reference material
  </section_name>
  <templates>
    <template name="Template Name">
      Template content
    </template>
  </templates>
</knowledge>
```

### `<examples>`
Concrete usage scenarios (2-4 required).

```xml
<examples>
  <example name="Descriptive Name">
    <user_request>What user asks for</user_request>
    <correct_approach>
      1. Step one
      2. Step two
      3. Step three
    </correct_approach>
  </example>
</examples>
```

### `<formatting>`
Communication style and output format.

```xml
<formatting>
  <communication_style>
    - Style guideline 1
    - Style guideline 2
  </communication_style>
  <completion_message_template>
    Template for completion messages
  </completion_message_template>
</formatting>
```

---

## Specialized Tags by Agent Type

### Orchestrators (Commands)

```xml
<orchestration>
  <allowed_tools>Task, Bash, Read, TodoWrite, AskUserQuestion</allowed_tools>
  <forbidden_tools>Write, Edit</forbidden_tools>

  <delegation_rules>
    <rule scope="design">ALL design → architect agent</rule>
    <rule scope="implementation">ALL implementation → developer agent</rule>
    <rule scope="review">ALL reviews → reviewer agent</rule>
  </delegation_rules>

  <phases>
    <phase number="1" name="Phase Name">
      <objective>What this phase achieves</objective>
      <steps>
        <step>Step description</step>
      </steps>
      <quality_gate>Exit criteria for this phase</quality_gate>
    </phase>
  </phases>
</orchestration>

<error_recovery>
  <strategy>
    Recovery steps for common failures
  </strategy>
</error_recovery>
```

### Planners (Architects)

```xml
<planning_methodology>
  <approach>How planning is performed</approach>
  <deliverables>What planning produces</deliverables>
</planning_methodology>

<gap_analysis>
  <checklist>Items to verify during planning</checklist>
</gap_analysis>

<output_structure>
  <format>Structure of planning output</format>
</output_structure>
```

### Implementers (Developers)

```xml
<implementation_standards>
  <file_writing_standards>
    <standard name="Standard Name">Description</standard>
  </file_writing_standards>

  <quality_checks mandatory="true">
    <check name="check_name" order="1">
      <tool>Tool name</tool>
      <command>Command to run</command>
      <requirement>What must pass</requirement>
      <on_failure>Recovery action</on_failure>
    </check>
  </quality_checks>

  <validation_checks>
    <check order="1" name="Check Name">
      Validation criteria
    </check>
  </validation_checks>
</implementation_standards>
```

### Reviewers

```xml
<review_criteria>
  <focus_areas>
    <area name="Area Name" priority="critical|high|medium" weight="20%">
      **Check:**
      - Item to verify
      - Item to verify

      **Common Issues:**
      - Issue description

      **Critical if**: Condition for critical severity
      **High if**: Condition for high severity
    </area>
  </focus_areas>

  <feedback_format>
    Template for review feedback
  </feedback_format>
</review_criteria>

<approval_criteria>
  <status name="PASS">Criteria for passing</status>
  <status name="CONDITIONAL">Criteria for conditional approval</status>
  <status name="FAIL">Criteria for failure</status>
</approval_criteria>
```

### Testers

```xml
<testing_strategy>
  <approach>Testing methodology</approach>
  <test_types>
    <type name="Type Name">Description</type>
  </test_types>
</testing_strategy>

<coverage_requirements>
  <requirement>Coverage criteria</requirement>
</coverage_requirements>
```

---

## Nesting Rules

1. **Proper Hierarchy** - Tags must be properly nested
2. **Closing Tags** - All opening tags must have closing tags
3. **Semantic Attributes** - Use `name`, `priority`, `order` attributes
4. **Consistent Naming** - Use lowercase-with-hyphens for tag names

## Code Blocks in XML

```xml
<template name="Example">
```language
// code here - note: opening ``` directly under tag
```
</template>
```

## Character Escaping

Only in XML attribute values and text nodes (NOT in code blocks):
- `&lt;` for `<`
- `&gt;` for `>`
- `&amp;` for `&`
