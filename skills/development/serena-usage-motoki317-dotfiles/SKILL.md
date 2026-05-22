---
name: Serena Usage
description: This skill should be used when the user asks to "use serena", "semantic search", "symbol analysis", "find references", "code navigation", or needs Serena MCP guidance. Provides Serena tool usage patterns.
---

<purpose>
  Provide patterns for effective use of Serena MCP tools for semantic code operations.
</purpose>

<tools>
  <tool name="get_symbols_overview">
    <description>Get high-level view of symbols in a file</description>
    <param name="relative_path">Path to file (required)</param>
    <param name="depth">Descendant depth, 0 for top-level only</param>
    <use_case>First step when exploring a new file</use_case>
  </tool>

  <tool name="find_symbol">
    <description>Find symbols by name path pattern</description>
    <param name="name_path_pattern">Symbol name or path (e.g., "MyClass/myMethod")</param>
    <param name="relative_path">Restrict to file or directory</param>
    <param name="include_body">Include source code</param>
    <param name="depth">Include descendants</param>
    <param name="substring_matching">Match partial names</param>
    <use_case>Locate specific functions, classes, or methods</use_case>
  </tool>

  <tool name="find_referencing_symbols">
    <description>Find all references to a symbol</description>
    <param name="name_path">Symbol to find references for</param>
    <param name="relative_path">File containing the symbol</param>
    <use_case>Dependency analysis, impact assessment</use_case>
  </tool>

  <tool name="search_for_pattern">
    <description>Regex search across codebase</description>
    <param name="substring_pattern">Regex pattern</param>
    <param name="relative_path">Restrict search scope</param>
    <param name="context_lines_before">Lines before match</param>
    <param name="context_lines_after">Lines after match</param>
    <param name="restrict_search_to_code_files">Search only code files or all files</param>
    <param name="paths_include_glob">Glob pattern for files to include</param>
    <param name="paths_exclude_glob">Glob pattern for files to exclude</param>
    <use_case>Find patterns, non-code files, complex searches</use_case>
  </tool>

  <tool name="replace_symbol_body">
    <description>Replace entire symbol definition</description>
    <param name="name_path">Symbol to replace</param>
    <param name="relative_path">File containing symbol</param>
    <param name="body">New symbol body</param>
    <use_case>Refactoring entire functions or classes</use_case>
  </tool>

  <tool name="insert_before_symbol">
    <description>Insert content before a symbol</description>
    <param name="name_path">Symbol to insert before</param>
    <param name="relative_path">File containing symbol</param>
    <param name="body">Content to insert</param>
    <use_case>Add imports, decorators, comments</use_case>
  </tool>

  <tool name="insert_after_symbol">
    <description>Insert content after a symbol</description>
    <param name="name_path">Symbol to insert after</param>
    <param name="relative_path">File containing symbol</param>
    <param name="body">Content to insert</param>
    <use_case>Add new functions, classes</use_case>
  </tool>

  <tool name="rename_symbol">
    <description>Rename symbol across codebase</description>
    <param name="name_path">Symbol to rename</param>
    <param name="relative_path">File containing symbol</param>
    <param name="new_name">New symbol name</param>
    <use_case>Consistent renaming with reference updates</use_case>
  </tool>

  <tool name="list_memories">
    <description>List all available memory files</description>
    <use_case>Check existing patterns before implementation</use_case>
  </tool>

  <tool name="read_memory">
    <description>Read content of a memory file</description>
    <param name="memory_file_name">Name of memory file to read</param>
    <use_case>Load project patterns and conventions</use_case>
  </tool>

  <tool name="write_memory">
    <description>Write information to a memory file</description>
    <param name="memory_file_name">Name of memory file to write</param>
    <param name="content">Content to write</param>
    <use_case>Record new patterns and conventions</use_case>
  </tool>

  <tool name="delete_memory">
    <description>Delete a memory file</description>
    <param name="memory_file_name">Name of memory file to delete</param>
    <use_case>Remove obsolete or incorrect patterns</use_case>
  </tool>

  <tool name="edit_memory">
    <description>Replace content in a memory file using regex or literal matching</description>
    <param name="memory_file_name">Name of memory file to edit</param>
    <param name="needle">Pattern to search for</param>
    <param name="repl">Replacement string</param>
    <param name="mode">Either "literal" or "regex"</param>
    <use_case>Update specific parts of memory files</use_case>
  </tool>
</tools>

<concepts>
  <concept name="memory_files">
    <description>Persistent storage for project patterns, conventions, and architectural decisions</description>
    <example>
      list_memories  # Check existing patterns
      read_memory "nix-conventions"  # Load Nix patterns
      write_memory "api-patterns" "REST API conventions..."  # Record new pattern
      delete_memory "outdated-pattern"  # Remove obsolete info
    </example>
  </concept>

  <concept name="memory_naming">
    <description>Consistent naming conventions for memory files</description>
    <example>
      {project}-conventions  # Project-wide conventions
      {feature}-patterns     # Feature-specific patterns
      {domain}-patterns      # Domain-specific patterns
      architecture-{decision}  # Architecture decisions
    </example>
  </concept>

  <concept name="symbol_path">
    <description>Path to symbol within a file (e.g., MyClass/myMethod)</description>
    <example>
      find_symbol "MyClass/myMethod"  # Find specific method
      find_symbol "get*" substring_matching=true  # Find all getter methods
    </example>
  </concept>

  <concept name="reflection_tools">
    <description>Meta-cognitive tools for ensuring search quality and task alignment</description>
    <example>
      <note>After searching multiple files</note>
      think_about_collected_information

      <note>Before making changes</note>
      think_about_task_adherence

      <note>When task seems complete</note>
      think_about_whether_you_are_done
    </example>
  </concept>
</concepts>

<patterns>
  <pattern name="explore_file">
    <description>Systematically explore file structure from high-level to detailed</description>
    <example>
      <step>Step 1: Get top-level overview</step>
      get_symbols_overview relative_path="src/main.ts" depth=0

      <step>Step 2: Explore class members</step>
      get_symbols_overview relative_path="src/main.ts" depth=1

      <step>Step 3: Get specific implementation</step>
      find_symbol name_path_pattern="MyClass/myMethod" include_body=true
    </example>
  </pattern>

  <pattern name="trace_dependencies">
    <description>Trace symbol dependencies and callers</description>
    <example>
      <step>Step 1: Locate the symbol</step>
      find_symbol name_path_pattern="processData" relative_path="src/processor.ts"

      <step>Step 2: Find all callers</step>
      find_referencing_symbols name_path="processData" relative_path="src/processor.ts"

      <step>Step 3: Recursively trace for full dependency graph</step>
      <note>Repeat steps 1-2 for each caller to build complete dependency tree</note>
    </example>
  </pattern>

  <pattern name="safe_refactoring">
    <description>Refactor with full impact analysis</description>
    <example>
      <step>Step 1: Understand current implementation</step>
      find_symbol name_path_pattern="MyClass/oldMethod" include_body=true

      <step>Step 2: Identify all usages</step>
      find_referencing_symbols name_path="MyClass/oldMethod" relative_path="src/myclass.ts"

      <step>Step 3: Perform the change</step>
      replace_symbol_body name_path="MyClass/oldMethod" relative_path="src/myclass.ts" body="..."

      <step>Step 4: Update references if interface changed</step>
      <note>If method signature changed, update all calling sites identified in step 2</note>
    </example>
  </pattern>

  <pattern name="pattern_search">
    <description>Search for patterns with appropriate scope</description>
    <example>
      <note>Search only in code files</note>
      search_for_pattern substring_pattern="TODO:" restrict_search_to_code_files=true

      <note>Search in all files including configs</note>
      search_for_pattern substring_pattern="api-key" restrict_search_to_code_files=false

      <note>Include context around matches</note>
      search_for_pattern substring_pattern="function.\*async" context_lines_before=2 context_lines_after=3
    </example>
  </pattern>

  <pattern name="memory_workflow">
    <description>Use memories to maintain consistency across tasks</description>
    <example>
      <note>Before implementation</note>
      list_memories # Check what patterns exist
      read_memory "typescript-patterns" # Load relevant patterns

      <note>During implementation</note>
      <note>Follow the patterns loaded from memory</note>

      <note>After implementation</note>
      write_memory "api-client-pattern" "HTTP client pattern using fetch with retry logic..."
    </example>
  </pattern>

  <decision_tree name="tool_selection">
    <question>What type of operation is needed?</question>
    <branch condition="Symbol lookup">Use find_symbol with name_path_pattern</branch>
    <branch condition="File structure overview">Use get_symbols_overview with appropriate depth</branch>
    <branch condition="Find references">Use find_referencing_symbols</branch>
    <branch condition="Pattern search">Use search_for_pattern with regex</branch>
    <branch condition="Refactor symbol">Use replace_symbol_body</branch>
    <branch condition="Rename symbol">Use rename_symbol for consistent updates</branch>
    <branch condition="Add code">Use insert_before_symbol or insert_after_symbol</branch>
    <branch condition="Check patterns">Use list_memories then read_memory</branch>
    <branch condition="Record patterns">Use write_memory</branch>
  </decision_tree>
</patterns>

<anti_patterns>
  <avoid name="reading_entire_files">
    <description>Reading entire files when only specific symbols are needed</description>
    <instead>Use get_symbols_overview for file structure and find_symbol with include_body for specific implementations</instead>
  </avoid>

  <avoid name="unscoped_searches">
    <description>Searching entire codebase when scope is known</description>
    <instead>Use relative_path parameter to restrict search to known files or directories</instead>
  </avoid>

  <avoid name="ignoring_memories">
    <description>Implementing features without checking existing patterns</description>
    <instead>Always check list_memories and read_memory before implementation</instead>
  </avoid>

  <avoid name="manual_refactoring">
    <description>Manually updating symbol references across files</description>
    <instead>Use rename_symbol for consistent renaming with automatic reference updates</instead>
  </avoid>

  <avoid name="excessive_depth">
    <description>Using high depth values unnecessarily in get_symbols_overview</description>
    <instead>Start with depth=0, then incrementally increase if needed</instead>
  </avoid>
</anti_patterns>

<workflow>
  <phase name="prepare">
    <objective>Prepare for effective Serena tool usage</objective>
    <step>1. Check list_memories for existing patterns</step>
    <step>2. Identify target symbols or files</step>
    <step>3. Choose appropriate tool based on decision_tree</step>
  </phase>
  <phase name="execute">
    <objective>Execute Serena operations efficiently</objective>
    <step>1. Start with get_symbols_overview for file structure</step>
    <step>2. Use find_symbol with include_body for details</step>
    <step>3. Use find_referencing_symbols for dependencies</step>
  </phase>
  <phase name="verify">
    <objective>Verify results and record patterns</objective>
    <step>1. Call think_about_collected_information after searches</step>
    <step>2. Record new patterns with write_memory</step>
    <step>3. Call think_about_whether_you_are_done when complete</step>
  </phase>
</workflow>

<best_practices>
  <practice priority="critical">Always check memories with list_memories and read_memory before implementing new features</practice>
  <practice priority="critical">Use symbol operations (get_symbols_overview, find_symbol) over reading entire files</practice>
  <practice priority="high">Restrict searches by relative_path when scope is known to improve performance</practice>
  <practice priority="high">Use substring_matching for uncertain symbol names to broaden search results</practice>
  <practice priority="high">Record new patterns and conventions with write_memory for future reference</practice>
  <practice priority="medium">Use context_lines parameters in search_for_pattern to understand surrounding code</practice>
  <practice priority="medium">Verify symbol changes with find_referencing_symbols before refactoring</practice>
</best_practices>

<rules priority="critical">
  <rule>Always check memories before implementing new features</rule>
  <rule>Use symbol operations over reading entire files</rule>
  <rule>Call think_about_collected_information after non-trivial search sequences</rule>
  <rule>Call think_about_task_adherence before making code changes</rule>
</rules>

<rules priority="standard">
  <rule>Restrict searches by relative_path when scope is known</rule>
  <rule>Use substring_matching for uncertain symbol names</rule>
  <rule>Record new patterns with write_memory</rule>
  <rule>Call think_about_whether_you_are_done when task appears complete</rule>
</rules>

<related_agents>
  <agent name="design">Uses Serena for architecture analysis and pattern discovery</agent>
  <agent name="code-quality">Uses Serena for complexity analysis and refactoring</agent>
  <agent name="bug">Uses Serena for tracing dependencies and impact analysis</agent>
  <agent name="execute">Uses Serena for symbol-level operations and memory management</agent>
  <agent name="security">Uses Serena for vulnerability detection and security pattern analysis</agent>
  <agent name="database">Uses Serena for schema analysis and query optimization</agent>
  <agent name="performance">Uses Serena for performance bottleneck identification and optimization</agent>
  <agent name="test">Uses Serena for test coverage analysis and test generation</agent>
</related_agents>

<error_escalation>
  <level severity="low">
    <example>Symbol not found with exact match</example>
    <action>Note in report, proceed</action>
  </level>
  <level severity="medium">
    <example>Memory file not found</example>
    <action>Document issue, use AskUserQuestion for clarification</action>
  </level>
  <level severity="high">
    <example>Conflicting information in memories</example>
    <action>STOP, present options to user</action>
  </level>
  <level severity="critical">
    <example>Memory corruption or invalid state</example>
    <action>BLOCK operation, require explicit user acknowledgment</action>
  </level>
</error_escalation>

<related_skills>
  <skill name="investigation-patterns">Investigation methodology using Serena tools</skill>
  <skill name="nix-ecosystem">Nix patterns stored in Serena memories</skill>
  <skill name="typescript-ecosystem">TypeScript patterns stored in Serena memories</skill>
  <skill name="golang-ecosystem">Go patterns stored in Serena memories</skill>
  <skill name="rust-ecosystem">Rust patterns stored in Serena memories</skill>
  <skill name="common-lisp-ecosystem">Common Lisp patterns stored in Serena memories</skill>
  <skill name="emacs-ecosystem">Emacs patterns stored in Serena memories</skill>
</related_skills>

<constraints>
  <must>Check memories before implementing new features</must>
  <must>Use symbol operations over reading entire files</must>
  <must>Restrict searches by relative_path when scope is known</must>
  <avoid>Reading entire files when symbol operations suffice</avoid>
  <avoid>Unscoped searches across entire codebase</avoid>
  <avoid>Ignoring existing memory patterns</avoid>
</constraints>
