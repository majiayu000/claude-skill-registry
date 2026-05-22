---
name: analyze-codebase
description: Analyze a codebase to generate a comprehensive architecture and structure report. Use when user wants to understand a codebase, explore project structure, or generate analysis.
argument-hint: "[path]"
model: inherit
user-invocable: true
disable-model-invocation: false
allowed-tools: Read, Write, Glob, Grep, Bash, Task, AskUserQuestion
---

# Codebase Analysis Workflow

Execute a 3-phase codebase analysis workflow. This workflow explores a codebase, analyzes its architecture, and generates a comprehensive report.

**CRITICAL: Complete ALL 3 phases.** After completing each phase, immediately proceed to the next phase without waiting for user prompts.

## Phase Overview

1. **Codebase Exploration** - Explore structure, patterns, and dependencies
2. **Deep Analysis** - Analyze findings to identify architecture and patterns
3. **Output & Context Loading** - Present options and deliver results in user's preferred format

---

## Phase 1: Codebase Exploration

**Goal:** Thoroughly explore the codebase to gather raw findings.

1. Determine the analysis path:
   - If `$ARGUMENTS` was provided, use that path
   - Otherwise, use the current working directory
   - Inform the user of the scope being analyzed

2. **Launch 3 code-explorer agents in parallel** using the Task tool with `subagent_type: "dev-tools:code-explorer"`:

   **Agent 1: Project Structure & Configuration**
   ```
   Explore and analyze the project structure and configuration.
   Path to analyze: [path]

   Focus on:
   - Project root structure (directories and their purposes)
   - Entry points (main files, index files, CLI entry points)
   - Configuration files (package.json, pyproject.toml, tsconfig.json, etc.)
   - Build configuration (webpack, vite, rollup, etc.)
   - Development tools (.eslintrc, .prettierrc, etc.)
   - CI/CD configuration (.github/workflows, Jenkinsfile, etc.)
   - Environment configuration (.env.example, config files)

   Return a structured report of:
   - Directory structure overview
   - Key entry points and their purposes
   - Configuration summary
   - Build and development tooling
   ```

   **Agent 2: Core Modules & Business Logic**
   ```
   Explore and analyze the core modules and business logic.
   Path to analyze: [path]

   Focus on:
   - Core source directories (src/, lib/, app/)
   - Key classes, functions, and modules
   - Business logic and domain models
   - State management (if applicable)
   - Data models and schemas
   - Service layers and APIs
   - Utility and helper modules

   Return a structured report of:
   - Key modules and their responsibilities
   - Important classes/functions with brief descriptions
   - Design patterns observed
   - Code organization patterns
   ```

   **Agent 3: Dependencies & Integrations**
   ```
   Explore and analyze dependencies and external integrations.
   Path to analyze: [path]

   Focus on:
   - Package dependencies (production vs development)
   - Internal module dependencies (how modules import each other)
   - External API integrations
   - Database connections and ORM usage
   - Third-party service integrations
   - Authentication/authorization mechanisms
   - Caching layers
   - Message queues or event systems

   Return a structured report of:
   - Dependency analysis (major frameworks, libraries)
   - External integration points
   - Data storage mechanisms
   - Communication patterns
   ```

3. **Wait for all agents to complete** and collect their findings.

4. **Synthesize exploration findings:**
   - Combine results from all 3 agents
   - Identify overlapping or conflicting information
   - Note any gaps in coverage
   - Create a consolidated findings document

---

## Phase 2: Deep Analysis

**Goal:** Analyze exploration findings to identify architecture, patterns, and insights.

1. **Launch codebase-analyzer agent** using the Task tool with `subagent_type: "dev-tools:codebase-analyzer"`:

   ```
   Analyze the following codebase exploration findings and produce a deep analysis.

   Path analyzed: [path]

   ## Exploration Findings

   [Include the synthesized findings from Phase 1]

   ---

   Produce a comprehensive analysis covering:
   1. Architecture style identification
   2. Key modules and their responsibilities
   3. Dependency relationships between modules
   4. Technology stack summary
   5. Code patterns and conventions
   6. Entry points and data flow
   7. External integrations
   8. Testing approach
   9. Build and deployment patterns
   10. Strengths and areas for improvement
   ```

2. **Wait for analysis to complete** and collect the results.

---

## Phase 3: Output & Context Loading

**Goal:** Present output options and deliver analysis results in the user's preferred format.

1. **Ask user for output preferences** using `AskUserQuestion` with multi-select:

   ```
   Question: "How would you like to use the analysis results?"
   Header: "Output"
   Options:
     - Label: "Save detailed report"
       Description: "Generate a comprehensive markdown report to internal/reports/"
     - Label: "Load into session context"
       Description: "Inject analysis into this session so I can reference it when answering questions"
     - Label: "Update project docs"
       Description: "Update README.md and/or CLAUDE.md with analysis summary"
   MultiSelect: true
   ```

2. **Handle the user's selection:**

   ### If NEITHER option is selected:
   - Display a brief summary (~200-300 words) directly in the chat
   - Confirm: "Analysis complete. Key findings displayed above."
   - Skip to final message

   ### If "Save detailed report" is selected:
   - Ensure output directory exists: `mkdir -p internal/reports`
   - **Launch report-generator agent** using Task tool with `subagent_type: "dev-tools:report-generator"`:
     ```
     Generate a comprehensive codebase analysis report in markdown format.

     Path analyzed: [path]
     Analysis date: [current date]

     ## Analysis Findings

     [Include the complete analysis from Phase 2]

     ---

     Generate a well-structured markdown report and save it to:
     internal/reports/codebase-analysis-report.md
     ```
   - Confirm: "Report saved to `internal/reports/codebase-analysis-report.md`"

   ### If "Load into session context" is selected:
   - Ask for detail level (Condensed summary or Full analysis)
   - Display the formatted context directly in the response
   - Confirm: "Analysis loaded into session context."

   ### If "Update project docs" is selected:
   - Ask which files to update (README.md, CLAUDE.md, or both)
   - Launch report-generator agent with appropriate mode
   - Confirm which files were updated

3. **Final message:**
   - Summarize what was done
   - Offer next steps: ask questions, run on different path, deep-dive modules

---

## Error Handling

If any phase fails:
1. Explain what went wrong
2. Ask the user how to proceed: Retry, Skip, or Abort

If an agent returns incomplete results:
- Note the gaps in coverage
- Continue with available information
- Document limitations in the final report

## Agent Coordination

When launching parallel agents in Phase 1:
- Give each agent a distinct focus area
- Wait for all agents to complete before synthesizing
- Handle agent failures gracefully (continue with partial results)

When calling Task tool for agents:
- Use `model: "opus"` for codebase-analyzer agent
- Use default model (sonnet) for code-explorer and report-generator agents
