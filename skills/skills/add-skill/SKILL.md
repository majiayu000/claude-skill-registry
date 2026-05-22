---
description: Generate project-specific Claude Code skills from codebase patterns or framework best practices
version: 1.0
encoding: UTF-8
---

# Add Skill Workflow

## Overview

Generate customized Claude Code skill files based on either:
- **Mode A (--analyze)**: Analyze existing codebase patterns
- **Mode B (--best-practices)**: Use framework best practices templates

## Process Flow

<process_flow>

<step number="1" name="parse_arguments">

### Step 1: Parse Command Arguments

Parse and validate user-provided arguments.

<instructions>
  ACTION: Extract arguments from user command

  REQUIRED_ARGS:
    skill_type: Extract from --type argument
      VALID_VALUES: ["api", "component", "testing", "deployment"]
      IF missing: ERROR "Missing required --type argument. Use: api, component, testing, or deployment"

    mode: Determine from mode flags
      IF --analyze provided: SET mode = "analyze"
      ELSE IF --best-practices provided: SET mode = "best-practices"
      ELSE: ERROR "Mode required. Use --analyze or --best-practices"

  OPTIONAL_ARGS:
    framework: Extract from --framework argument (can be null)

  VALIDATE:
    IF skill_type NOT IN ["api", "component", "testing", "deployment"]:
      ERROR "Invalid skill type. Use: api, component, testing, or deployment"

    IF framework provided:
      VALIDATE framework matches skill_type
        api: spring-boot, express, fastapi, django, rails
        component: react, angular, vue, svelte
        testing: playwright, jest, vitest, pytest, rspec, cypress
        deployment: github-actions, gitlab-ci, jenkins, docker

      IF invalid:
        ERROR "Framework '{framework}' not valid for skill type '{skill_type}'"

  OUTPUT: Parsed arguments
    {
      skill_type: "api",
      mode: "analyze",
      framework: null | "spring-boot"
    }
</instructions>

</step>

<step number="2" name="detect_framework">

### Step 2: Detect Framework

Auto-detect framework if not provided by user.

<instructions>
  IF framework argument provided:
    SKIP: Auto-detection
    USE: User-specified framework
    LOG: "Using user-specified framework: {framework}"
    PROCEED: To step 3

  ELSE:
    EXECUTE: Framework detection based on skill_type

    IF skill_type == "api":
      ACTION: Detect backend framework

      USE: Glob tool to check for indicator files:
        - SEARCH pattern="pom.xml" → If found: Likely Spring Boot
        - SEARCH pattern="build.gradle*" → If found: Likely Spring Boot
        - SEARCH pattern="package.json" → If found: Check for express dependency
        - SEARCH pattern="requirements.txt" → If found: Check for fastapi/django
        - SEARCH pattern="pyproject.toml" → If found: Check for fastapi/django
        - SEARCH pattern="Gemfile" → If found: Check for rails gem
        - SEARCH pattern="manage.py" → If found: Likely Django

      IF pom.xml OR build.gradle found:
        READ: File content
        SEARCH: For "spring-boot" in content
        IF found:
          SET framework = "spring-boot"
          EXTRACT: Version from dependency
          CONFIDENCE: high

      ELSE IF package.json found:
        READ: package.json
        PARSE: JSON content
        CHECK: dependencies["express"] exists
        IF yes:
          SET framework = "express"
          EXTRACT: Version
          CONFIDENCE: high

      ELSE IF requirements.txt OR pyproject.toml found:
        READ: File content
        IF "fastapi" in content:
          SET framework = "fastapi"
        ELSE IF "django" in content OR manage.py found:
          SET framework = "django"

      ELSE IF Gemfile found:
        READ: Gemfile
        IF "rails" in content:
          SET framework = "rails"

      ELSE:
        framework = null
        CONFIDENCE: none

    ELSE IF skill_type == "component":
      ACTION: Detect frontend framework

      USE: Glob tool:
        - SEARCH pattern="package.json"
        - SEARCH pattern="angular.json"
        - SEARCH pattern="**/*.vue"
        - SEARCH pattern="**/*.svelte"

      IF package.json found:
        READ: package.json
        PARSE: JSON

        IF dependencies["react"]:
          SET framework = "react"
          CHECK: devDependencies["typescript"] for TypeScript usage

        ELSE IF dependencies["@angular/core"]:
          SET framework = "angular"

        ELSE IF dependencies["vue"]:
          SET framework = "vue"
          EXTRACT: Version to determine Vue 2 vs 3

        ELSE IF dependencies["svelte"]:
          SET framework = "svelte"
          CHECK: dependencies["@sveltejs/kit"] for SvelteKit

    ELSE IF skill_type == "testing":
      ACTION: Detect testing framework

      USE: Glob tool:
        - SEARCH pattern="playwright.config.*"
        - SEARCH pattern="jest.config.*"
        - SEARCH pattern="pytest.ini"
        - SEARCH pattern=".rspec"

      IF playwright.config found:
        SET framework = "playwright"
      ELSE IF jest.config found OR package.json has jest:
        SET framework = "jest"
      ELSE IF pytest.ini found OR requirements.txt has pytest:
        SET framework = "pytest"
      ELSE IF .rspec found OR Gemfile has rspec:
        SET framework = "rspec"

    ELSE IF skill_type == "deployment":
      ACTION: Detect CI/CD platform

      USE: Glob tool:
        - SEARCH pattern=".github/workflows/*.yml"
        - SEARCH pattern=".gitlab-ci.yml"
        - SEARCH pattern="Jenkinsfile"
        - SEARCH pattern="Dockerfile"

      IF .github/workflows found:
        SET framework = "github-actions"
      ELSE IF .gitlab-ci.yml found:
        SET framework = "gitlab-ci"
      ELSE IF Jenkinsfile found:
        SET framework = "jenkins"
      ELSE IF Dockerfile found:
        SET framework = "docker"

  IF framework == null:
    IF mode == "best-practices":
      ACTION: Ask user to select framework
      USE: AskUserQuestion
      QUESTION: "Which {skill_type} framework are you using?"
      OPTIONS: [List of frameworks for skill_type]
      RECEIVE: User selection
      SET framework = user_selection

    ELSE:
      ERROR: "Could not detect framework. Use --framework to specify, or use --best-practices mode."

  OUTPUT:
    detected_framework: {
      name: "spring-boot",
      version: "3.2.0",
      confidence: "high",
      source: "pom.xml"
    }
</instructions>

</step>

<step number="3" name="mode_routing">

### Step 3: Route to Appropriate Workflow

Branch based on selected mode.

<instructions>
  IF mode == "analyze":
    LOG: "Mode A: Analyzing existing codebase patterns"
    EXECUTE: Steps 4-7 (Pattern discovery, validation, improvement selection)

  ELSE IF mode == "best-practices":
    LOG: "Mode B: Using framework best practices"
    SKIP: Steps 4-7
    EXECUTE: Step 8 (Load best practices directly)

  PROCEED: To appropriate next step
</instructions>

</step>

<step number="4" subagent="Explore" name="discover_patterns" conditional="mode==analyze">

### Step 4: Discover Patterns (Mode A Only)

Use Explore agent to find code patterns in the codebase.

<instructions>
  ACTION: Use Task tool with subagent_type="Explore"
  THOROUGHNESS: "medium"

  IF skill_type == "api":
    CONSTRUCT: Prompt for API pattern discovery

    PROMPT:
      "Discover {framework} API patterns in the codebase:

      Search for:
      - Controller/Route files
      - Service files
      - Repository/Data access files

      For {framework}, look for these patterns:
      [Framework-specific file patterns based on detected framework]

      Find the top 10-15 most representative files and extract:
      - Routing/endpoint patterns
      - Request validation patterns
      - Error handling approaches
      - Data access patterns
      - Transaction management

      Return file paths and key pattern observations."

    EXECUTE: Explore agent task
    WAIT: For agent completion
    RECEIVE: List of discovered files and patterns

    THEN:
      FOR each discovered_file in results:
        USE: Read tool to get file content
        EXTRACT: Relevant code patterns
        CATEGORIZE: By pattern type (routing, validation, error_handling, etc.)

  ELSE IF skill_type == "component":
    PROMPT:
      "Discover {framework} component patterns:

      Search for component files and extract:
      - Component structure and organization
      - Props/interface definitions
      - State management approaches
      - Event handling patterns
      - Styling approaches

      Return top 10-15 representative components."

    EXECUTE: Explore agent task
    PROCESS: Results similar to API

  ELSE IF skill_type == "testing":
    PROMPT:
      "Discover {framework} testing patterns:

      Search for test files and extract:
      - Test structure (describe/it blocks)
      - Assertion patterns
      - Mocking strategies
      - Setup/teardown approaches
      - Page object patterns (if E2E)

      Return top 10-15 test files."

    EXECUTE: Explore agent task
    PROCESS: Results

  ELSE IF skill_type == "deployment":
    PROMPT:
      "Discover CI/CD and deployment patterns:

      Search for:
      - Workflow/pipeline files
      - Docker configurations
      - Build scripts

      Extract:
      - Build process
      - Test execution in CI
      - Deployment strategies
      - Caching patterns

      Return all relevant files."

    EXECUTE: Explore agent task
    PROCESS: Results

  OUTPUT:
    discovered_patterns: {
      files_analyzed: 15,
      patterns: [
        {
          category: "routing",
          code: "...",
          file: "UserController.java",
          occurrences: 12
        },
        ...
      ]
    }
</instructions>

</step>

<step number="5" name="validate_patterns" conditional="mode==analyze">

### Step 5: Validate Patterns Against Best Practices (Mode A Only)

Compare discovered patterns with framework best practices.

<instructions>
  ACTION: Load best practices for detected framework

  READ: @agent-os/workflows/skill/validation/best-practices/{framework}.md

  COMPARE: Discovered patterns vs best practices
    FOR each discovered_pattern:
      CHECK: Does it match a best practice pattern?
      CALCULATE: Similarity score
      IDENTIFY: Gaps or issues

  DETECT: Anti-patterns
    CHECK: For common anti-patterns:
      - SQL injection (string concatenation in queries)
      - Missing error handling
      - Security vulnerabilities
      - Performance issues

  GENERATE: Improvement suggestions
    FOR each gap or anti-pattern:
      CREATE: Improvement suggestion
        - Severity: critical | warning | info
        - Current pattern
        - Recommended pattern
        - Code examples (before/after)
        - Impact assessment

  CATEGORIZE: By severity
    critical_improvements: [...]
    warning_improvements: [...]
    info_improvements: [...]

  OUTPUT:
    validation_results: {
      overall_score: 72,
      improvements: [
        {
          id: "imp_001",
          severity: "critical",
          title: "Fix SQL Injection",
          current: "String concatenation",
          recommended: "Parameterized queries",
          files_affected: 2
        },
        ...
      ]
    }
</instructions>

</step>

<step number="6" name="present_improvements" conditional="mode==analyze">

### Step 6: Present Improvements to User (Mode A Only)

Show improvement suggestions and collect user selections.

<instructions>
  IF improvements.length == 0:
    MESSAGE: "No improvements needed - your code follows best practices!"
    SKIP: To step 8

  ELSE:
    DISPLAY: Improvement summary
      MESSAGE:
        "Found {total} improvement opportunities:
        - ❌ {critical_count} Critical
        - ⚠️ {warning_count} Warnings
        - ℹ️ {info_count} Suggestions"

    FOR each improvement IN [critical, warnings, info]:
      DISPLAY: Improvement details
        "═══════════════════════════════════════════
        {severity_icon} {title}
        ═══════════════════════════════════════════

        Impact: {impact}
        Effort: {effort}
        Files: {file_count}

        Current: {current_pattern_description}
        Issues: {issues}

        Recommended: {recommended_pattern_description}
        Benefits: {benefits}
        "

      USE: AskUserQuestion
      QUESTION: "Include this improvement?"
      OPTIONS:
        - "✅ Yes, include (Recommended)"
        - "📖 Show code examples"
        - "❌ No, skip"

      RECEIVE: User decision

      IF "Show code examples":
        DISPLAY: Before/after code
        ASK: Again for decision

      IF "Yes":
        RECORD: In accepted_improvements list
      ELSE:
        RECORD: In rejected_improvements list

    DISPLAY: Selection summary
      "You selected {accepted_count} out of {total_count} improvements.

      Critical: {critical_accepted}/{critical_total}
      Warnings: {warning_accepted}/{warning_total}
      Info: {info_accepted}/{info_total}"

    CONFIRM: "Continue with skill generation?"
    IF no: EXIT workflow

  OUTPUT:
    user_selections: {
      accepted: [imp_001, imp_002, ...],
      rejected: [imp_008, ...],
      accepted_count: 8
    }
</instructions>

</step>

<step number="7" name="apply_improvements" conditional="mode==analyze">

### Step 7: Apply Selected Improvements (Mode A Only)

Merge selected improvements into pattern data.

<instructions>
  FOR each accepted_improvement:
    FIND: Related discovered pattern

    IF pattern exists:
      ENHANCE: Pattern with improvement
        UPDATE: Pattern code with recommended version
        ADD: Improvement metadata
        MARK: As enhanced

    ELSE:
      ADD: New pattern from improvement
        CREATE: Pattern entry
        MARK: As added from improvement

  FOR each rejected_critical_improvement:
    CREATE: Warning note
      ADD: To "Known Issues" section
      DOCUMENT: Risk and recommendation

  OUTPUT:
    enhanced_patterns: {
      patterns: [
        {
          category: "error_handling",
          code: "[Enhanced code]",
          status: "enhanced",
          improvement_applied: "Centralized exception handling"
        },
        ...
      ],
      known_issues: [
        {
          issue: "SQL injection in UserRepository",
          severity: "critical",
          rejected_by_user: true
        }
      ]
    }
</instructions>

</step>

<step number="8" name="load_best_practices" conditional="mode==best-practices">

### Step 8: Load Best Practices (Mode B Only)

Load framework-specific best practices templates.

<instructions>
  ACTION: Confirm framework with user if auto-detected

  IF framework auto-detected:
    MESSAGE: "Detected framework: {framework} {version}"
    USE: AskUserQuestion
    QUESTION: "Use {framework} for skill generation?"
    OPTIONS:
      - "Yes, use {framework} (Recommended)"
      - "No, choose different framework"

    IF "No":
      USE: AskUserQuestion
      QUESTION: "Which {skill_type} framework?"
      OPTIONS: [Framework options for skill_type]
      SET framework = user_selection

  ELSE IF framework == null:
    USE: AskUserQuestion
    QUESTION: "Which {skill_type} framework?"
    OPTIONS: [Framework options for skill_type]
    SET framework = user_selection

  ACTION: Load best practices
    READ: @agent-os/workflows/skill/validation/best-practices/{framework}.md
    EXTRACT: All pattern sections
    STORE: As pattern_content

  OUTPUT:
    best_practices_content: {
      framework: "spring-boot",
      patterns: [Extracted from best practices file],
      examples: [Code examples from best practices],
      anti_patterns: [Anti-patterns to avoid]
    }
</instructions>

</step>

<step number="9" name="detect_project_name">

### Step 9: Detect Project Name

Auto-detect project name for skill file naming.

<instructions>
  ACTION: Try multiple detection sources in priority order

  PRIORITY_1: Check agent-os/config.yml
    USE: Glob pattern="agent-os/config.yml"
    IF found:
      READ: File
      PARSE: YAML (look for project.name field)
      IF project.name exists:
        SET project_name = value
        SOURCE: "agent-os-config"
        SKIP: Further detection

  PRIORITY_2: Check package.json (if not found in step 1)
    USE: Glob pattern="package.json"
    IF found:
      READ: File
      PARSE: JSON
      EXTRACT: name field
      IF name starts with "@":
        REMOVE: Scope (e.g., "@company/app" → "app")
      SET project_name = cleaned_name
      SOURCE: "package.json"
      SKIP: Further detection

  PRIORITY_3: Check Gemfile/gemspec
    USE: Glob pattern="*.gemspec"
    IF found:
      READ: File
      SEARCH: For spec.name = "..."
      EXTRACT: Gem name
      CONVERT: Underscores to hyphens
      SET project_name = gem_name

  PRIORITY_4: Use directory name
    GET: Current working directory
    EXTRACT: Last path component
    CLEAN:
      - Convert to lowercase
      - Replace spaces/underscores with hyphens
      - Remove special characters

    IF name is generic (src, app, test, project):
      SKIP: Too generic
    ELSE:
      SET project_name = cleaned_dir_name
      SOURCE: "directory-name"

  PRIORITY_5: Ask user
    IF project_name still null:
      USE: AskUserQuestion
      QUESTION: "What is your project name?"
      DEFAULT: Cleaned directory name (if available)
      RECEIVE: User input
      NORMALIZE: User input (lowercase, hyphens, no special chars)
      SET project_name = normalized_input
      SOURCE: "user-input"

  ACTION: Confirm with user
    MESSAGE: "Project name: {project_name} (from {source})"
    USE: AskUserQuestion
    QUESTION: "Is this correct?"
    OPTIONS: ["Yes", "Enter different name"]

    IF "Enter different name":
      ASK: For new name
      NORMALIZE: Input
      SET project_name = new_name

  OPTIONAL: Save to config
    IF agent-os/config.yml exists:
      ASK: "Save project name to agent-os/config.yml?"
      IF yes:
        READ: agent-os/config.yml
        UPDATE: project.name field (or add if missing)
        WRITE: Updated config

  OUTPUT:
    project_name: "my-app",
    source: "package.json"
</instructions>

</step>

<step number="10" name="process_template">

### Step 10: Process Skill Template

Load template and replace markers with content.

<instructions>
  ACTION: Load appropriate template
    template_path = "@agent-os/templates/skills/{skill_type}-patterns.md.template"

    IF skill_type == "api":
      READ: @agent-os/templates/skills/api-patterns.md.template
    ELSE IF skill_type == "component":
      READ: @agent-os/templates/skills/component-patterns.md.template
    ELSE IF skill_type == "testing":
      READ: @agent-os/templates/skills/testing-patterns.md.template
    ELSE IF skill_type == "deployment":
      READ: @agent-os/templates/skills/deployment-patterns.md.template

    STORE: template_content

  ACTION: Build replacement map

    project_replacements = {
      "NAME": project_name,
      "FRAMEWORK": framework,
      "FRAMEWORK_VERSION": detected_version,
      "DATE": current_date,
      "LANGUAGE": programming_language,
      "MODE": mode,
      "MODE_DESCRIPTION": mode == "analyze" ? "Analyzed from existing codebase" : "Generated from best practices"
    }

    glob_replacements = {
      "API_GLOBS": [Framework-specific globs],
      "COMPONENT_GLOBS": [Framework-specific globs],
      "TEST_GLOBS": [Framework-specific globs],
      "DEPLOYMENT_GLOBS": [Framework-specific globs]
    }

    IF mode == "analyze":
      customize_replacements = {
        "CONTROLLER_PATTERNS": Extract from discovered_patterns,
        "SERVICE_PATTERNS": Extract from discovered_patterns,
        "ROUTING_EXAMPLE": Best example from patterns,
        "VALIDATION_PATTERNS": Extract from patterns,
        "ERROR_HANDLING_PATTERNS": Extract from enhanced_patterns (with improvements),
        ...
      }

    ELSE IF mode == "best-practices":
      customize_replacements = {
        "CONTROLLER_PATTERNS": Extract from best_practices_content,
        "SERVICE_PATTERNS": Extract from best_practices_content,
        "ROUTING_EXAMPLE": Framework example from best practices,
        ...
      }

  ACTION: Replace markers in template

    processed_content = template_content

    FOR each [PROJECT:MARKER] in template:
      REPLACE: With project_replacements[MARKER]

    FOR each [PROJECT:TYPE_GLOBS] in template:
      REPLACE: With formatted YAML array of globs

    FOR each [CUSTOMIZE:MARKER] in template:
      REPLACE: With customize_replacements[MARKER]

    VALIDATE: No unresolved markers remain
      SEARCH: For any remaining [PROJECT: or [CUSTOMIZE:
      IF found:
        WARN: "Unresolved marker: {marker}"
        REPLACE: With placeholder or empty string

  OUTPUT:
    processed_template: "[Complete markdown with replacements]"
</instructions>

</step>

<step number="11" name="generate_skill_file">

### Step 11: Generate Final Skill File

Assemble frontmatter and content into complete skill file.

<instructions>
  ACTION: Generate frontmatter YAML

    skill_name = "{project_name}-{skill_type}-patterns"
    skill_description = "{framework} {skill_type} patterns for {project_name}"

    IF mode == "analyze":
      skill_description += " (analyzed from existing codebase)"

    frontmatter_yaml = """---
name: {skill_name}
description: {skill_description}
version: {framework_version}
framework: {framework}
created: {current_date}
mode: {mode}
globs:
{glob_list_formatted}
---"""

  ACTION: Assemble complete skill file

    skill_content = frontmatter_yaml + "\n\n" + processed_template

  ACTION: Validate structure
    CHECK: Valid YAML frontmatter
    CHECK: All required sections present
    CHECK: Code blocks have language identifiers
    CHECK: No empty required sections

    IF validation fails:
      ERROR: "Skill generation failed validation: {errors}"
      OFFER: "Show preview anyway?" | "Cancel"

  OUTPUT:
    skill_file: {
      content: "[Complete skill markdown]",
      name: "my-app-api-patterns.md",
      path: ".claude/skills/my-app-api-patterns.md",
      size: "12.5 KB",
      lines: 542
    }
</instructions>

</step>

<step number="12" name="preview_and_confirm">

### Step 12: Preview and Confirm with User

Show skill preview and save on approval.

<instructions>
  ACTION: Generate preview (abbreviated version)

    DISPLAY:
      "═══════════════════════════════════════════════════════════════
      📄 SKILL PREVIEW
      ═══════════════════════════════════════════════════════════════

      Skill Name: {skill_name}
      Framework: {framework} {version}
      Type: {skill_type}
      Mode: {mode}

      ─────────────────────────────────────────────────────────────
      📋 FRONTMATTER
      ─────────────────────────────────────────────────────────────

      {frontmatter_yaml}

      ─────────────────────────────────────────────────────────────
      🎯 KEY PATTERNS (Top 3)
      ─────────────────────────────────────────────────────────────

      1. {pattern_1_title}
         {brief_description}
         {code_snippet_abbreviated}

      2. {pattern_2_title}
      ...

      ─────────────────────────────────────────────────────────────
      📁 FILE COVERAGE
      ─────────────────────────────────────────────────────────────

      Active for files matching:
      {glob_list}

      ─────────────────────────────────────────────────────────────
      📊 STATISTICS
      ─────────────────────────────────────────────────────────────

      Total Patterns: {pattern_count}
      Code Examples: {example_count}
      {If mode A: Improvements Applied: {improvement_count}}

      ═══════════════════════════════════════════════════════════════
      "

  ACTION: Ask for user decision
    USE: AskUserQuestion
    QUESTION: "What would you like to do?"
    OPTIONS:
      - "✅ Yes, save it (Recommended)"
      - "📖 Show full content"
      - "❌ No, cancel"

    IF "Show full content":
      DISPLAY: Complete skill_content
      ASK: Again "Save this skill?"
      OPTIONS: ["Yes, save it", "No, cancel"]

    IF "Yes, save it":
      PROCEED: To save

    ELSE IF "No, cancel":
      MESSAGE: "Skill generation cancelled."
      EXIT: Workflow
</instructions>

</step>

<step number="13" name="save_skill_file">

### Step 13: Save Skill File

Write skill file to disk.

<instructions>
  ACTION: Determine file path
    skill_file_name = "{project_name}-{skill_type}-patterns.md"
    skill_file_path = ".claude/skills/{skill_file_name}"

  ACTION: Check if file exists
    USE: Glob pattern=".claude/skills/{skill_file_name}"

    IF file exists:
      USE: AskUserQuestion
      QUESTION: "File already exists. Overwrite?"
      OPTIONS: ["Yes, overwrite", "Use different name", "Cancel"]

      IF "Use different name":
        skill_file_name = "{project_name}-{skill_type}-patterns-2.md"
        skill_file_path = ".claude/skills/{skill_file_name}"

      ELSE IF "Cancel":
        EXIT: Workflow

      ELSE IF "Yes, overwrite":
        CREATE: Backup
          USE: Bash command: cp "{skill_file_path}" "{skill_file_path}.backup"

  ACTION: Create .claude/skills directory if needed
    USE: Bash command: mkdir -p .claude/skills

  ACTION: Write skill file
    USE: Write tool
    FILE_PATH: {skill_file_path}
    CONTENT: {skill_content}
    ENCODING: UTF-8

  ACTION: Verify file was written
    USE: Glob pattern="{skill_file_path}"
    IF not found:
      ERROR: "Failed to write skill file"

    USE: Bash command: wc -l "{skill_file_path}"
    VERIFY: Line count matches expected

  OUTPUT:
    saved_file: {
      path: ".claude/skills/my-app-api-patterns.md",
      size: "12.5 KB",
      lines: 542
    }
</instructions>

</step>

<step number="14" name="display_success">

### Step 14: Display Success Message

Show completion message with next steps.

<instructions>
  DISPLAY: Success message
    "✅ Skill created successfully!

    📄 File: {skill_file_path}
    📊 Patterns: {pattern_count}
    {If mode A: ✨ Improvements: {improvement_count}}

    🚀 Next Steps:

    1. The skill is now active for files matching:
       {glob_list}

    2. Test the skill:
       - Open a file that matches the globs
       - Claude will automatically use these patterns

    3. Optional: Reference in .claude/claude.json
       - Add to 'skills' array for explicit activation

    4. Update anytime:
       - Run /add-skill again to regenerate with latest patterns
    "

  OPTIONAL_OFFERS:
    USE: AskUserQuestion
    QUESTION: "Would you like to do anything else?"
    OPTIONS:
      - "Create another skill (different type)"
      - "View the generated skill file"
      - "Done"

    IF "Create another skill":
      MESSAGE: "Run /add-skill with different --type to create another skill."

    ELSE IF "View the generated skill file":
      READ: {skill_file_path}
      DISPLAY: Content

  LOG: Operation completed
    "Skill generation complete: {skill_file_path}"
</instructions>

</step>

</process_flow>

## Error Handling

<error_protocols>
  <invalid_arguments>
    ERROR: "Invalid arguments. See usage examples above."
    DISPLAY: Valid options for each argument
    EXIT: Workflow
  </invalid_arguments>

  <framework_detection_failed>
    IF mode == "analyze":
      ERROR: "Could not detect framework. Please specify with --framework flag."
      EXIT: Workflow
    ELSE:
      FALLBACK: Ask user to select framework
      CONTINUE: Workflow
  </framework_detection_failed>

  <pattern_discovery_failed>
    WARN: "Limited patterns found in codebase."
    ASK: "Continue with available patterns or switch to --best-practices mode?"
    IF switch:
      SET mode = "best-practices"
      GOTO: Step 8
  </pattern_discovery_failed>

  <file_write_failed>
    ERROR: "Failed to write skill file: {error}"
    CHECK: Directory permissions
    SUGGEST: Manual file creation or different location
  </file_write_failed>
</error_protocols>

## Quick Reference for Claude

**When user runs:** `/add-skill --analyze --type api`

**Execute:**
1. Parse args (skill_type=api, mode=analyze)
2. Detect backend framework (use Glob + Read for pom.xml, package.json, etc.)
3. Run Explore agent to find API patterns
4. Validate patterns against best practices
5. Present improvements to user (AskUserQuestion)
6. Apply selected improvements
7. Detect project name (check config, package.json, directory)
8. Load template (api-patterns.md.template)
9. Replace all markers (PROJECT, CUSTOMIZE, GLOBS)
10. Generate frontmatter
11. Show preview to user
12. Save on user approval (Write tool)
13. Display success message

**When user runs:** `/add-skill --best-practices --type component --framework react`

**Execute:**
1. Parse args (skill_type=component, mode=best-practices, framework=react)
2. Skip framework detection (user specified)
3. Skip pattern discovery (Mode B)
4. Load React best practices (read best-practices/react.md)
5. Detect project name
6. Load template (component-patterns.md.template)
7. Replace markers with best practices content
8. Show preview
9. Save on approval
10. Display success
