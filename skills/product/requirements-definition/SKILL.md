---
name: Requirements Definition
description: This skill should be used when the user asks to "define requirements", "create specification", "clarify requirements", "write requirements document", or mentions requirement analysis. Provides comprehensive requirements definition methodology.
---

<purpose>
  Provide structured methodology for requirements definition, ensuring comprehensive specification before implementation.
</purpose>

<tools>
  <tool name="Glob">Directory structure analysis</tool>
  <tool name="get_symbols_overview">Symbol analysis via Serena</tool>
  <tool name="Grep">Keyword search</tool>
  <tool name="find_symbol">Symbol search via Serena</tool>
  <tool name="find_referencing_symbols">Dependency mapping via Serena</tool>
  <tool name="Read">Specific content details</tool>
  <tool name="Context7">Latest API documentation and best practices</tool>
</tools>

<patterns>
  <pattern name="investigation_workflow">
    <description>Sequential investigation process for gathering requirements context</description>
    <decision_tree name="when_to_use">
      <question>Is the current system state unclear or unknown?</question>
      <if_yes>Apply investigation workflow to gather context before requirements definition</if_yes>
      <if_no>Proceed directly to functional requirements if context is clear</if_no>
    </decision_tree>
    <steps>
      <step>Directory structure analysis using Glob</step>
      <step>Symbol analysis using get_symbols_overview</step>
      <step>Keyword search using Grep or find_symbol</step>
      <step>Dependency mapping using find_referencing_symbols</step>
      <step>Specific content details using Read</step>
      <step>Latest API documentation using Context7</step>
    </steps>
  </pattern>

  <pattern name="question_scoring">
    <description>Score each question by these criteria (1-5 each) to prioritize requirement clarification</description>
    <decision_tree name="when_to_use">
      <question>Have unclear or ambiguous requirements been identified?</question>
      <if_yes>Apply question scoring to prioritize critical clarifications</if_yes>
      <if_no>Proceed with documenting clear requirements</if_no>
    </decision_tree>
    <criteria>
      <criterion name="design_branching">How much does the answer affect design direction?</criterion>
      <criterion name="irreversibility">How difficult to change after implementation?</criterion>
      <criterion name="investigation_impossibility">Cannot be determined through code investigation alone?</criterion>
      <criterion name="effort_impact">How much does it affect implementation effort?</criterion>
    </criteria>
    <note>Present high-score questions first. Do not proceed without clear answers to critical questions (score >= 15)</note>
    <example>
      Question: "Should we use TypeScript's strict mode?"
      - Design Branching: 5 (affects all type decisions)
      - Irreversibility: 4 (hard to change later)
      - Investigation Impossibility: 3 (requires policy decision)
      - Effort Impact: 4 (affects development effort)
      Total: 16 (critical - must answer before proceeding)
    </example>
  </pattern>

  <pattern name="question_classification">
    <description>Categories of questions that arise during requirements definition</description>
    <decision_tree name="when_to_use">
      <question>Do you need to categorize questions for stakeholder communication?</question>
      <if_yes>Apply question classification to organize by type</if_yes>
      <if_no>Use question scoring to prioritize by impact</if_no>
    </decision_tree>
    <types>
      <type name="spec_confirmation">Confirming existing behavior or constraints</type>
      <type name="design_choice">Choosing between valid alternatives</type>
      <type name="constraint">Technical or business limitations</type>
      <type name="scope">Boundaries of implementation</type>
      <type name="priority">Order and importance of features</type>
    </types>
    <example>
      - Spec Confirmation: "Does the API return null or empty array for no results?"
      - Design Choice: "Should we use REST or GraphQL?"
      - Constraint: "Must support IE11 browsers?"
      - Scope: "Should admin features be included in v1?"
      - Priority: "Which feature should be implemented first?"
    </example>
  </pattern>

  <pattern name="functional_requirements">
    <description>Format functional requirements with clear identifiers and acceptance criteria</description>
    <decision_tree name="when_to_use">
      <question>Are feature behaviors and capabilities clearly defined?</question>
      <if_yes>Apply functional requirements format with acceptance criteria</if_yes>
      <if_no>Use question scoring to clarify unclear behaviors first</if_no>
    </decision_tree>
    <example>
      FR-001: User Authentication
      Priority: mandatory
      - Users must be able to log in with email and password
      - Session must expire after 24 hours of inactivity
      - Failed login attempts must be rate-limited (max 5 per hour)
    </example>
  </pattern>

  <pattern name="non_functional_requirements">
    <description>Specify measurable non-functional requirements across key dimensions</description>
    <decision_tree name="when_to_use">
      <question>Are quality attributes and constraints important for this feature?</question>
      <if_yes>Apply non-functional requirements with measurable targets</if_yes>
      <if_no>Focus on functional requirements only</if_no>
    </decision_tree>
    <example>
      Performance:
      - API response time < 200ms for 95th percentile
      - Support 1000 concurrent users

      Security:

      - All data encrypted at rest using AES-256
      - JWT tokens for authentication

      Maintainability:

      - Test coverage >= 80%
      - Documentation for all public APIs
    </example>
  </pattern>

  <pattern name="technical_specifications">
    <description>Document design policies, patterns, and key decisions with rationale</description>
    <decision_tree name="when_to_use">
      <question>Have key technical decisions been made or identified?</question>
      <if_yes>Apply technical specifications pattern with rationale and impact analysis</if_yes>
      <if_no>Continue requirements gathering to identify decision points</if_no>
    </decision_tree>
    <example>
      Design Decision: Use React Query for data fetching
      Rationale:
      - Built-in caching reduces API calls
      - Automatic background refetching
      - TypeScript support
      - Widely adopted in existing codebase

      Impact Scope:

      - All components making API calls
      - Testing utilities need to mock React Query
    </example>
  </pattern>

  <pattern name="requirement_quality_metrics">
    <description>Quantitative measures of requirement quality</description>
    <decision_tree name="when_to_use">
      <question>Are all requirements documented and ready for handoff?</question>
      <if_yes>Apply quality metrics to assess requirement completeness</if_yes>
      <if_no>Continue requirements definition until complete</if_no>
    </decision_tree>
    <example>
      Feasibility (0-100): Technical achievability given constraints
      - 90-100: Straightforward with existing tools
      - 70-89: Requires some research or new libraries
      - 50-69: Significant technical challenges
      - Below 50: May need architecture changes

      Objectivity (0-100): Evidence-based vs. assumption-based

      - 90-100: All requirements verified through investigation
      - 70-89: Most requirements verified, some assumptions documented
      - 50-69: Mix of verification and assumptions
      - Below 50: Mostly assumptions, needs more investigation
    </example>
  </pattern>
</patterns>

<output>
  <format>
    <summary>
      - One-sentence request description
      - Background and context
      - Expected outcomes
    </summary>
    <current_state>
      - Existing system description
      - Technology stack
      - Relevant patterns and conventions
    </current_state>
    <functional_requirements>
      Format: FR-XXX (FR-001, FR-002, ...)
      - Priority: mandatory or optional
      - Clear acceptance criteria
    </functional_requirements>
    <non_functional_requirements>
      - Performance: response time, throughput
      - Security: authentication, authorization, data protection
      - Maintainability: code quality, documentation
    </non_functional_requirements>
    <technical_specifications>
      - Design policies and patterns
      - Impact scope analysis
      - Key design decisions with rationale
    </technical_specifications>
    <metrics>
      - Feasibility (0-100): Technical achievability
      - Objectivity (0-100): Evidence-based specification
    </metrics>
    <constraints>
      - Technical constraints: platform, language, framework
      - Operational constraints: deployment, maintenance
    </constraints>
    <test_requirements>
      - Unit test coverage expectations
      - Integration test scenarios
      - Acceptance criteria verification
    </test_requirements>
    <task_breakdown>
      - Dependency graph: task dependencies and execution order
      - Phased tasks: files to modify/create, overview of changes, dependencies
      - Execute handoff: key decisions, reference implementations, constraints
    </task_breakdown>
  </format>
</output>

<rules priority="critical">
  <rule>Never proceed without clear answers to critical questions (score >= 15)</rule>
  <rule>All requirements must be verifiable and measurable</rule>
  <rule>Distinguish mandatory from optional requirements</rule>
</rules>

<rules priority="standard">
  <rule>Present high-score questions first in requirement discussions</rule>
  <rule>Document assumptions explicitly when requirements are unclear</rule>
  <rule>Include rationale for key design decisions</rule>
  <rule>Map requirements to test scenarios</rule>
</rules>

<best_practices>
  <practice priority="critical">Always investigate current state before defining requirements using Serena's symbol-level operations</practice>
  <practice priority="critical">Score questions using the 4-criteria scoring system and prioritize high-score questions (>= 15)</practice>
  <practice priority="critical">Clearly distinguish mandatory from optional requirements with explicit rationale</practice>
  <practice priority="high">Document all assumptions when requirements are unclear or incomplete</practice>
  <practice priority="high">Map each requirement to specific test scenarios for verification</practice>
  <practice priority="high">Include rationale for key design decisions in technical specifications</practice>
  <practice priority="medium">Use Context7 to verify latest library documentation and best practices</practice>
  <practice priority="medium">Create dependency graphs showing task execution order</practice>
</best_practices>

<workflow>
  <phase name="gather">
    <objective>Gather requirement information</objective>
    <step>1. Understand user request and context</step>
    <step>2. Investigate existing codebase patterns</step>
    <step>3. Identify stakeholders and constraints</step>
  </phase>
  <phase name="clarify">
    <objective>Clarify ambiguous requirements</objective>
    <step>1. Score questions by impact (design, irreversibility, effort)</step>
    <step>2. Use AskUserQuestion for structured decisions</step>
    <step>3. Document answers and implications</step>
  </phase>
  <phase name="document">
    <objective>Document requirements formally</objective>
    <step>1. Write functional requirements (FR-XXX format)</step>
    <step>2. Write non-functional requirements</step>
    <step>3. Define acceptance criteria</step>
  </phase>
</workflow>

<error_escalation>
  <level severity="low">
    <example>Minor ambiguity in non-critical detail</example>
    <action>Note in report, proceed</action>
  </level>
  <level severity="medium">
    <example>Unclear requirement affecting scope</example>
    <action>Document issue, use AskUserQuestion for clarification</action>
  </level>
  <level severity="high">
    <example>Technically infeasible requirement</example>
    <action>STOP, present options to user</action>
  </level>
  <level severity="critical">
    <example>Requirement violates security or ethics</example>
    <action>BLOCK operation, require explicit user acknowledgment</action>
  </level>
</error_escalation>

<constraints>
  <must>Investigate before concluding</must>
  <must>Ask questions before making assumptions</must>
  <must>Include (Recommended) option in AskUserQuestion</must>
  <avoid>Proceeding without answering critical questions</avoid>
  <avoid>Justifying user preferences over technical validity</avoid>
  <avoid>Documenting requirements without evidence</avoid>
</constraints>

<related_agents>
  <agent name="define">Primary agent for requirements definition and specification design</agent>
  <agent name="ask">Use for investigating current system state before requirements definition</agent>
  <agent name="execute">Delegate to after requirements are fully defined and approved</agent>
</related_agents>

<related_skills>
  <skill name="investigation-patterns">Use to understand current system state before requirements definition</skill>
  <skill name="execution-workflow">Use after requirements approval to delegate implementation</skill>
  <skill name="testing-patterns">Use to define test requirements and acceptance criteria</skill>
</related_skills>

<anti_patterns>
  <avoid name="vague_requirements">
    <description>Requirements that are unclear or unmeasurable</description>
    <instead>Write specific, testable requirements with clear acceptance criteria</instead>
  </avoid>
  <avoid name="implementation_details">
    <description>Specifying implementation details instead of requirements</description>
    <instead>Describe what needs to be achieved, not how to implement it</instead>
  </avoid>
  <avoid name="skipping_investigation">
    <description>Writing requirements without investigating existing code</description>
    <instead>Always investigate current state before defining requirements</instead>
  </avoid>
  <avoid name="missing_constraints">
    <description>Not identifying technical or operational constraints</description>
    <instead>Explicitly document all constraints that affect implementation</instead>
  </avoid>
  <avoid name="undefined_priorities">
    <description>Treating all requirements as equally important</description>
    <instead>Clearly mark requirements as mandatory or optional with rationale</instead>
  </avoid>
</anti_patterns>
