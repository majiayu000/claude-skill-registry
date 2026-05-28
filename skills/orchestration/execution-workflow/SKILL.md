---
name: Execution Workflow
description: This skill should be used when the user asks to "execute task", "implement feature", "delegate work", "run workflow", "review code", "code quality check", or needs task orchestration and code review guidance. Provides execution, delegation, and code review patterns.
---

<purpose>
  Provide structured workflow for task execution through delegation to specialized sub-agents, and comprehensive code review standards.
</purpose>

<tools>
  <tool name="agent_groups">Specialized sub-agents: quality_assurance (quality, security - parallel), implementation (test, refactor, docs - parallel if independent), review (sequential after implementation)</tool>
  <tool name="delegation">Provide scope, file paths, Serena/Context7 tool instructions, reference implementations, memory checks</tool>
  <tool name="tool_selection">Coding: Codex MCP → Serena MCP → Context7 → Basic tools; Non-coding: Serena MCP → Context7 → Basic tools</tool>
</tools>

<concepts>
  <concept name="parallel_execution">Execute independent tasks concurrently; quality+security can run in parallel, test+docs can run in parallel when independent</concept>
  <concept name="sequential_dependencies">Tasks with data dependencies must run in order; verify outputs before dependent tasks start</concept>
  <concept name="delegation_context">Sub-agents need: specific scope, file paths, tool usage instructions, reference implementations, memory patterns</concept>
  <concept name="review_phases">Four phases: Initial scan (syntax), Deep analysis (logic), Context evaluation (impact), Standards compliance (naming/docs)</concept>
</concepts>

<patterns>
  <pattern name="code_review_phases">
    <description>Systematic code review process</description>
    <decision_tree name="when_to_use">
      <question>Has code been modified or newly created?</question>
      <if_yes>Apply code review phases systematically to ensure quality</if_yes>
      <if_no>Skip review and proceed to next task</if_no>
    </decision_tree>
    <example>
      Phase 1 - Initial Scan:
      - Syntax errors and typos
      - Missing imports or dependencies
      - Obvious logic errors
      - Code style violations

      Phase 2 - Deep Analysis:

      - Algorithm correctness
      - Edge case handling
      - Error handling completeness
      - Resource management

      Phase 3 - Context Evaluation:

      - Breaking changes to public APIs
      - Side effects on existing functionality
      - Dependency compatibility

      Phase 4 - Standards Compliance:

      - Naming conventions
      - Documentation requirements
      - Test coverage
    </example>
  </pattern>

  <pattern name="quality_criteria">
    <description>Evaluation criteria for code quality</description>
    <decision_tree name="when_to_use">
      <question>Is this a code review or quality assessment task?</question>
      <if_yes>Apply quality criteria across all dimensions</if_yes>
      <if_no>Focus on implementation patterns instead</if_no>
    </decision_tree>
    <example>
      Correctness:
      - Logic matches requirements
      - Edge cases handled
      - Error conditions covered

      Security:

      - Input validation
      - Authentication/authorization
      - Data sanitization
      - Secrets handling

      Performance:

      - Algorithm efficiency
      - Resource usage
      - Memory leaks
      - N+1 queries

      Maintainability:

      - Clear naming
      - Appropriate comments
      - Single responsibility
      - DRY principle

      Testability:

      - Test coverage adequate
      - Tests meaningful
      - Edge cases tested
    </example>
  </pattern>

  <pattern name="feedback_categories">
    <description>Categorization of review feedback by priority</description>
    <decision_tree name="when_to_use">
      <question>Have you identified issues during code review?</question>
      <if_yes>Apply feedback categories to prioritize by severity</if_yes>
      <if_no>Continue code review phases</if_no>
    </decision_tree>
    <example>
      Critical: Must fix before merge
      - Security vulnerabilities
      - Data corruption risks
      - Breaking changes

      Important: Should fix before merge

      - Logic errors
      - Missing error handling
      - Performance issues

      Suggestion: Nice to have improvements

      - Code style
      - Refactoring opportunities
      - Documentation

      Positive: What was done well

      - Good patterns
      - Clever solutions
      - Thorough testing
    </example>
  </pattern>

  <pattern name="review_output_format">
    <description>Standard format for code review results</description>
    <decision_tree name="when_to_use">
      <question>Is it time to communicate code review findings?</question>
      <if_yes>Apply review output format for structured communication</if_yes>
      <if_no>Continue analyzing code through review phases</if_no>
    </decision_tree>
    <example>
      <summary>Overall assessment and recommendation</summary>
      <critical_issues>Must-fix items with file:line references</critical_issues>
      <important_issues>Should-fix items</important_issues>
      <suggestions>Optional improvements</suggestions>
      <positive_feedback>Good practices observed</positive_feedback>
      <questions>Clarifications needed</questions>
    </example>
  </pattern>
</patterns>

<anti_patterns>
  <avoid name="nitpicking_style">
    <description>Focusing on code style issues when functionality is broken</description>
    <instead>Address critical and important issues first, style suggestions last</instead>
  </avoid>
  <avoid name="rubber_stamping">
    <description>Approving changes without thorough review</description>
    <instead>Systematically review all phases: scan, deep analysis, context, standards</instead>
  </avoid>
  <avoid name="only_negatives">
    <description>Providing only critical feedback without acknowledging good work</description>
    <instead>Balance feedback with positive observations of good practices</instead>
  </avoid>
  <avoid name="vague_feedback">
    <description>Giving feedback without specific, actionable suggestions</description>
    <instead>Provide file:line references and concrete improvement suggestions</instead>
  </avoid>
  <avoid name="sequential_when_parallel">
    <description>Executing independent tasks sequentially</description>
    <instead>Identify and execute independent tasks in parallel for efficiency</instead>
  </avoid>
  <avoid name="parallel_when_dependent">
    <description>Attempting to parallelize tasks with data dependencies</description>
    <instead>Analyze dependencies and execute dependent tasks sequentially</instead>
  </avoid>
</anti_patterns>

<workflow>
  <phase name="analyze">
    <description>Understand requirements and identify scope</description>
    <step>Parse task description for key objectives</step>
    <step>Identify affected files and components</step>
    <step>Check Serena memories for existing patterns</step>
  </phase>
  <phase name="break_down">
    <description>Split into manageable units</description>
    <step>Identify atomic tasks</step>
    <step>Estimate complexity of each task</step>
    <step>Assign to appropriate sub-agents</step>
  </phase>
  <phase name="organize">
    <description>Identify parallel vs sequential execution</description>
    <step>Map task dependencies</step>
    <step>Group independent tasks for parallel execution</step>
    <step>Order dependent tasks sequentially</step>
  </phase>
  <phase name="delegate">
    <description>Assign to sub-agents with detailed instructions</description>
    <step>Provide specific scope and expected deliverables</step>
    <step>Include target file paths</step>
    <step>Specify MCP tool usage instructions</step>
    <step>Reference existing implementations</step>
  </phase>
  <phase name="integrate">
    <description>Verify and combine results</description>
    <step>Review sub-agent outputs</step>
    <step>Resolve conflicts between outputs</step>
    <step>Ensure consistency across changes</step>
  </phase>
</workflow>

<best_practices>
  <practice priority="critical">Analyze task dependencies before execution to determine parallel vs sequential execution model</practice>
  <practice priority="critical">Provide comprehensive context to sub-agents including file paths, tool usage, and reference implementations</practice>
  <practice priority="critical">Systematically review all phases: initial scan, deep analysis, context evaluation, standards compliance</practice>
  <practice priority="high">Balance critical feedback with positive observations of good practices</practice>
  <practice priority="high">Provide file:line references and concrete improvement suggestions</practice>
  <practice priority="medium">Check Serena memories for existing patterns before delegating implementation tasks</practice>
</best_practices>

<rules priority="critical">
  <rule>Execute independent tasks in parallel</rule>
  <rule>Never parallelize tasks with data dependencies</rule>
  <rule>Verify sub-agent outputs before integration</rule>
  <rule>Run quality checks after changes</rule>
</rules>

<rules priority="standard">
  <rule>quality + security: Concurrent checks</rule>
  <rule>test + docs: Simultaneous creation when independent</rule>
  <rule>Ensure no regression in existing functionality</rule>
  <rule>Confirm all acceptance criteria met</rule>
</rules>

<error_escalation>
  <level severity="low">
    <example>Sub-agent returns partial results</example>
    <action>Note in report, proceed</action>
  </level>
  <level severity="medium">
    <example>Sub-agent task fails</example>
    <action>Document issue, use AskUserQuestion for clarification</action>
  </level>
  <level severity="high">
    <example>Critical task cannot be completed</example>
    <action>STOP, present options to user</action>
  </level>
  <level severity="critical">
    <example>Sub-agent introduces breaking change</example>
    <action>BLOCK operation, require explicit user acknowledgment</action>
  </level>
</error_escalation>

<related_agents>
  <agent name="execute">Primary agent for implementing features with sub-agent delegation</agent>
  <agent name="feedback">Use for post-implementation code review and quality assessment</agent>
  <agent name="bug">Delegate debugging tasks when critical issues are identified during review</agent>
</related_agents>

<related_skills>
  <skill name="serena-usage">Use for memory checks and symbol operations during delegation</skill>
  <skill name="investigation-patterns">Use when code review reveals unclear implementation details</skill>
  <skill name="testing-patterns">Use to verify test coverage and quality during review</skill>
</related_skills>

<constraints>
  <must>Delegate detailed work to sub-agents</must>
  <must>Execute independent tasks in parallel</must>
  <must>Verify outputs before integration</must>
  <avoid>Implementing detailed logic directly</avoid>
  <avoid>Sequential execution of independent tasks</avoid>
  <avoid>Skipping verification of sub-agent outputs</avoid>
</constraints>
