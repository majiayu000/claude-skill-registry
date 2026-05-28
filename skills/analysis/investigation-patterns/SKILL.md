---
name: Investigation Patterns
description: This skill should be used when the user asks to "investigate code", "analyze implementation", "find patterns", "understand codebase", "debug issue", "find bug", "troubleshoot", or needs evidence-based code analysis and debugging. Provides systematic investigation and debugging methodology.
---

<purpose>
  Provide systematic patterns for codebase investigation and debugging, ensuring evidence-based analysis with proper confidence assessment.
</purpose>

<rules priority="critical">
  <rule>Always provide file:line references for all findings using format path/to/file.ext:line_number</rule>
  <rule>Rate confidence and coverage metrics for all investigation results</rule>
  <rule>Complete investigation before proposing solutions</rule>
</rules>

<rules priority="standard">
  <rule>Use Serena symbol tools before reading entire files</rule>
  <rule>Independently verify claims rather than confirming assumptions</rule>
  <rule>Document information gaps and unclear points</rule>
  <rule>Check multiple sources to increase confidence</rule>
  <rule>Use systematic debugging phases (reproduce, isolate, investigate, hypothesize, fix)</rule>
</rules>

<patterns>
  <pattern name="scope_classification">
    <description>Classify the question type to determine investigation approach</description>
    <decision_tree name="when_to_use">
      <question>Does the question require understanding codebase structure or behavior?</question>
      <if_yes>Apply scope classification to determine investigation depth and tools</if_yes>
      <if_no>Consider requirements-definition skill for unclear requirements</if_no>
    </decision_tree>
    <example>
      Architecture: System design, component relationships
      Implementation: Specific code behavior, algorithm details
      Debugging: Error causes, unexpected behavior
      Design: Pattern usage, code organization
    </example>
  </pattern>

  <pattern name="source_identification">
    <description>Identify relevant sources for investigation</description>
    <decision_tree name="when_to_use">
      <question>Is the codebase large or unfamiliar?</question>
      <if_yes>Apply source identification to locate relevant evidence efficiently</if_yes>
      <if_no>Directly examine known sources</if_no>
    </decision_tree>
    <example>
      Code: Use Serena for symbol search and dependency analysis
      Documentation: Check inline comments, README, API docs
      History: Git log for context on changes
      External: Context7 for library documentation
    </example>
  </pattern>

  <pattern name="evidence_collection">
    <description>Collect evidence systematically using appropriate tools</description>
    <decision_tree name="when_to_use">
      <question>Do you have specific symbols or patterns to investigate?</question>
      <if_yes>Apply evidence collection with symbol-level tools</if_yes>
      <if_no>Start with source identification to locate relevant areas</if_no>
    </decision_tree>
    <example>
      find_symbol: Locate specific symbols by name
      get_symbols_overview: Understand file structure
      find_referencing_symbols: Trace dependencies
      search_for_pattern: Find patterns across codebase
    </example>
  </pattern>

  <pattern name="synthesis">
    <description>Synthesize findings with confidence metrics</description>
    <decision_tree name="when_to_use">
      <question>Have you collected sufficient evidence from multiple sources?</question>
      <if_yes>Apply synthesis to combine findings with confidence metrics</if_yes>
      <if_no>Continue evidence collection to increase coverage</if_no>
    </decision_tree>
    <example>
      Combine evidence from multiple sources
      Rate confidence based on evidence quality (0-100)
      Report coverage of relevant code examined (0-100)
      Identify and document information gaps
    </example>
  </pattern>

  <pattern name="reproduce">
    <description>Confirm the issue is reproducible</description>
    <decision_tree name="when_to_use">
      <question>Is this a bug or unexpected behavior investigation?</question>
      <if_yes>Apply reproduce pattern to confirm issue before debugging</if_yes>
      <if_no>Use other investigation patterns for analysis tasks</if_no>
    </decision_tree>
    <example>
      Gather exact steps to reproduce
      Identify environment conditions
      Determine consistency (always/sometimes fails)
    </example>
  </pattern>

  <pattern name="isolate">
    <description>Narrow down the problem scope</description>
    <decision_tree name="when_to_use">
      <question>Is the bug reproducible but involves many components?</question>
      <if_yes>Apply isolate pattern to narrow down the problem scope</if_yes>
      <if_no>Proceed to investigate pattern if scope is clear</if_no>
    </decision_tree>
    <example>
      Identify when issue started (git bisect if needed)
      Remove unrelated components
      Create minimal reproduction case
    </example>
  </pattern>

  <pattern name="investigate">
    <description>Collect evidence systematically for debugging</description>
    <decision_tree name="when_to_use">
      <question>Has the issue been reproduced and isolated?</question>
      <if_yes>Apply investigate pattern to collect debugging evidence</if_yes>
      <if_no>Complete reproduce and isolate patterns first</if_no>
    </decision_tree>
    <example>
      Examine error messages and stack traces
      Check logs at relevant timestamps
      Use Serena for code path analysis
      Trace data flow through the system
    </example>
  </pattern>

  <pattern name="hypothesize">
    <description>Form and test hypotheses</description>
    <decision_tree name="when_to_use">
      <question>Have you collected sufficient debugging evidence?</question>
      <if_yes>Apply hypothesize pattern to form and test root cause theories</if_yes>
      <if_no>Continue investigate pattern to gather more evidence</if_no>
    </decision_tree>
    <example>
      List possible causes
      Rank by likelihood
      Design tests to confirm/refute each
    </example>
  </pattern>

  <pattern name="fix">
    <description>Implement and verify solution</description>
    <decision_tree name="when_to_use">
      <question>Has a hypothesis been confirmed as the root cause?</question>
      <if_yes>Apply fix pattern to implement and verify solution</if_yes>
      <if_no>Continue hypothesize pattern to test other theories</if_no>
    </decision_tree>
    <example>
      Make minimal targeted change
      Verify fix resolves the issue
      Check for regressions
      Add test to prevent recurrence
    </example>
  </pattern>
</patterns>

<workflow>
  <phase name="observe">
    <objective>Gather initial observations</objective>
    <step>1. Document the symptom or question clearly</step>
    <step>2. Identify relevant entry points for investigation</step>
    <step>3. Form initial hypotheses</step>
  </phase>
  <phase name="investigate">
    <objective>Systematically explore evidence</objective>
    <step>1. Use Serena tools to trace code paths</step>
    <step>2. Build evidence chain from symptom to cause</step>
    <step>3. Validate or invalidate hypotheses</step>
  </phase>
  <phase name="conclude">
    <objective>Form evidence-based conclusions</objective>
    <step>1. Synthesize findings into coherent explanation</step>
    <step>2. Rate confidence based on evidence quality</step>
    <step>3. Document for future reference</step>
  </phase>
</workflow>

<error_escalation>
  <level severity="low">
    <example>Evidence trail incomplete</example>
    <action>Note in report, proceed</action>
  </level>
  <level severity="medium">
    <example>Conflicting evidence found</example>
    <action>Document issue, use AskUserQuestion for clarification</action>
  </level>
  <level severity="high">
    <example>Root cause cannot be determined</example>
    <action>STOP, present options to user</action>
  </level>
  <level severity="critical">
    <example>Investigation reveals security issue</example>
    <action>BLOCK operation, require explicit user acknowledgment</action>
  </level>
</error_escalation>

<constraints>
  <must>Build evidence chains before conclusions</must>
  <must>Cite specific file:line references</must>
  <must>State confidence levels explicitly</must>
  <avoid>Speculation without evidence</avoid>
  <avoid>Confirmation bias in hypothesis testing</avoid>
  <avoid>Concluding without exploring alternatives</avoid>
</constraints>

<tools>
  <tool name="find_symbol">
    <description>Locate specific symbols by name in the codebase</description>
    <param name="name_path_pattern">Pattern to match symbol names</param>
    <param name="relative_path">Optional path to restrict search</param>
    <param name="depth">Depth to retrieve children (default 0)</param>
    <use_case>Finding class, function, or variable definitions</use_case>
  </tool>

  <tool name="get_symbols_overview">
    <description>Get high-level structure of a file</description>
    <param name="relative_path">Path to file to analyze</param>
    <param name="depth">Depth of symbol tree (default 0)</param>
    <use_case>Understanding file organization before detailed investigation</use_case>
  </tool>

  <tool name="find_referencing_symbols">
    <description>Find all references to a symbol</description>
    <param name="name_path">Symbol to find references for</param>
    <param name="relative_path">File containing the symbol</param>
    <use_case>Tracing dependencies and usage patterns</use_case>
  </tool>

  <tool name="search_for_pattern">
    <description>Search for regex patterns across codebase</description>
    <param name="substring_pattern">Regular expression to search</param>
    <param name="relative_path">Optional path to restrict search</param>
    <param name="restrict_search_to_code_files">Limit to code files</param>
    <use_case>Finding specific patterns or usage across files</use_case>
  </tool>
</tools>

<concepts>
  <concept name="evidence_standards">
    <description>Standards for collecting and reporting evidence</description>
    <example>
      Citation: Always provide file:line references (path/to/file.ext:line_number)

      Confidence levels:

      - 90-100: Direct code evidence, explicit documentation
      - 70-89: Strong inference from multiple sources
      - 50-69: Reasonable inference with some gaps
      - 0-49: Speculation, insufficient evidence

      Coverage levels:

      - 90-100: All relevant files examined
      - 70-89: Most relevant files examined
      - 50-69: Key files examined, some gaps
      - 0-49: Limited examination
    </example>
  </concept>

  <concept name="null_reference">
    <description>Null pointer or undefined reference errors</description>
    <example>
      Symptom: NullPointerException, undefined is not a function
      Investigation: Check all paths to the null access
      Fix: Add null checks or ensure initialization
    </example>
  </concept>

  <concept name="race_condition">
    <description>Concurrent access issues</description>
    <example>
      Symptom: Intermittent failures, works sometimes
      Investigation: Look for shared mutable state, async operations
      Fix: Add synchronization or redesign for immutability
    </example>
  </concept>

  <concept name="off_by_one">
    <description>Boundary condition errors</description>
    <example>
      Symptom: Missing first/last element, index out of bounds
      Investigation: Check loop boundaries and index calculations
      Fix: Verify start/end conditions, use inclusive/exclusive correctly
    </example>
  </concept>

  <concept name="resource_leak">
    <description>Unclosed resources accumulating over time</description>
    <example>
      Symptom: Memory growth, connection exhaustion
      Investigation: Check resource acquisition and release paths
      Fix: Ensure cleanup in finally/defer, use resource management patterns
    </example>
  </concept>

  <concept name="encoding_issue">
    <description>Character encoding mismatches</description>
    <example>
      Symptom: Garbled text, unexpected characters
      Investigation: Trace encoding at each transformation step
      Fix: Ensure consistent encoding throughout pipeline
    </example>
  </concept>

  <concept name="five_whys">
    <description>Ask "why" repeatedly to drill to root cause</description>
    <example>
      Why did the server crash? - Out of memory
      Why out of memory? - Connection pool exhausted
      Why exhausted? - Connections not being released
      Why not released? - Exception bypasses cleanup
      Root cause: Missing try-finally for connection release
    </example>
  </concept>

  <concept name="timeline_analysis">
    <description>Reconstruct sequence of events leading to failure</description>
    <example>
      Collect timestamps from logs
      Order events chronologically
      Identify divergence from expected behavior
    </example>
  </concept>

  <concept name="investigation_output">
    <description>Standard format for investigation results</description>
    <example>
      <question>Restate the question for confirmation</question>
      <investigation>Evidence-based findings with file:line references
        - Source 1: path/to/file.ts:42 - finding description
        - Source 2: path/to/other.ts:15 - finding description</investigation>
      <conclusion>Direct answer based on evidence</conclusion>
      <metrics>
        - Confidence: 0-100
        - Evidence Coverage: 0-100</metrics>
      <recommendations>Suggested actions without implementation</recommendations>
      <unclear_points>Information gaps that would improve the answer</unclear_points>
    </example>
  </concept>

  <concept name="debugging_output">
    <description>Standard format for debugging results</description>
    <example>
      <problem_statement>Clear description of the issue</problem_statement>
      <reproduction_steps>How to reproduce</reproduction_steps>
      <investigation>Evidence collected with file:line references</investigation>
      <root_cause>Identified cause with supporting evidence</root_cause>
      <solution>Proposed fix with rationale</solution>
      <verification>How to verify the fix works</verification>
      <prevention>How to prevent recurrence</prevention>
    </example>
  </concept>
</concepts>

<related_agents>
  <agent name="bug">Use for root cause investigation when user reports bugs or errors</agent>
  <agent name="ask">Use for answering questions about codebase architecture and implementation</agent>
  <agent name="execute">Delegate to after investigation confirms implementation approach</agent>
</related_agents>

<related_skills>
  <skill name="serena-usage">Use for memory operations and symbol-level code navigation</skill>
  <skill name="execution-workflow">Use after investigation to implement fixes with proper delegation</skill>
  <skill name="fact-check">Use to verify external documentation and library behavior</skill>
  <skill name="testing-patterns">Use to add regression tests after fixing identified bugs</skill>
  <skill name="requirements-definition">Use when investigation reveals unclear requirements</skill>
</related_skills>

<anti_patterns>
  <avoid name="speculation">
    <description>Guessing or making claims when evidence is insufficient</description>
    <instead>Clearly state confidence levels and information gaps; request additional context if needed</instead>
  </avoid>

  <avoid name="confirming_assumptions">
    <description>Confirming user assumptions without independent verification</description>
    <instead>Independently verify claims by examining code and collecting evidence</instead>
  </avoid>

  <avoid name="uncited_claims">
    <description>Making claims without file:line references</description>
    <instead>Always provide file:line citations for findings using format path/to/file.ext:line_number</instead>
  </avoid>

  <avoid name="premature_implementation">
    <description>Implementing fixes instead of completing analysis</description>
    <instead>Focus on investigation and analysis; provide recommendations without implementation</instead>
  </avoid>
</anti_patterns>

<best_practices>
  <practice priority="critical">Always provide file:line references for all findings using format path/to/file.ext:line_number</practice>
  <practice priority="critical">Rate confidence and coverage metrics for all investigation results</practice>
  <practice priority="critical">Complete investigation before proposing solutions</practice>
  <practice priority="high">Use Serena symbol tools before reading entire files</practice>
  <practice priority="high">Independently verify claims rather than confirming assumptions</practice>
  <practice priority="high">Document information gaps and unclear points</practice>
  <practice priority="medium">Check multiple sources to increase confidence</practice>
  <practice priority="medium">Use systematic debugging phases (reproduce, isolate, investigate, hypothesize, fix)</practice>
</best_practices>
