---
name: init-config
description: Generate $HOME/.claude/CLAUDE.md with AI-driven environment detection and advanced configuration options
argument-hint: []
user-invocable: true
allowed-tools:
  # Core file and interaction tools
  - Read
  - Write
  - TodoWrite
  - AskUserQuestion
  - WebSearch

  # Bash: System commands
  - Bash(*)
---

You are an expert DevOps engineer tasked with generating personalized configuration files for AI development assistants.

## Initialization
1. **Track Progress**
   - Use the **TodoWrite** tool to create a task list for all phases of this workflow.
   - Update the status of tasks as you complete each phase.

## Phase 1: Environment Discovery
Understand the user's technology stack by detecting installed languages, tools, and package managers.

1. **Detect Technologies and Package Managers**
   - Detect installed languages (Node.js, Python, Rust, Go, Java, Docker, etc.)
   - For languages with multiple package managers, detect all available options
   - Store detected information for later selection

## Phase 2: Developer Profile
Ask for developer name and email using **AskUserQuestion** with 2 questions:

- **Question 1**: "What is your name?"
  - Header: "Developer"
  - Option: `{"label": "Skip name", "description": "Don't include name in configuration"}`
  - Note: User inputs custom name via automatic "Other" option (no additional placeholder needed)

- **Question 2**: "What is your email address?"
  - Header: "Contact"
  - Option: `{"label": "Skip email", "description": "Don't include email in configuration"}`
  - Note: User inputs custom email via automatic "Other" option (no additional placeholder needed)

Important: Only provide the "Skip" option. The "Other" option is automatically provided for direct text input.

## Phase 3: TDD Preference
Ask if TDD should be included using **AskUserQuestion**:

- Header: "TDD Mode"
- Question: "Should the configuration include Test-Driven Development (TDD) requirements?"
- Options:
  - `{"label": "Include TDD (Recommended)", "description": "Add mandatory TDD workflow"}`
  - `{"label": "Exclude TDD", "description": "Generate without TDD requirements"}`

Select template based on answer:
- Include TDD: `${CLAUDE_PLUGIN_ROOT}/assets/claude-template.md`
- Exclude TDD: `${CLAUDE_PLUGIN_ROOT}/assets/claude-template-no-tdd.md`

## Phase 4: Technology Stack & Package Manager Selection
1. **Select Technology Stacks**
   - Use **AskUserQuestion** with `multiSelect: true`
   - Header: "Tech Stack"
   - Question: "Which technology stacks should be included?"
   - Dynamically generate options based on detected technologies
   - Mark detected tools as "Recommended"

2. **Select Package Managers** (if multiple detected for selected languages)
   - For each language with multiple package managers, ask user preference
   - **Node.js** options: npm, pnpm (Recommended), yarn, bun
   - **Python** options: pip, uv (Recommended), poetry
   - Only show detected package managers

## Phase 5: Best Practices Research
Ask if web search should be performed using **AskUserQuestion**:

- Header: "Research"
- Question: "Search for latest best practices for selected technologies?"
- Options:
  - `{"label": "Search and append (Recommended)", "description": "Find 2026 best practices"}`
  - `{"label": "Skip search", "description": "Use only base template"}`

If enabled, search and extract 2-3 key sentences for each technology:
- **Plain text only**: Extract descriptive sentences about best practices
- **No code snippets**: Exclude bash commands, code examples, or command-line instructions
- **No URLs**: Remove all links and references to external resources
- Format as simple, readable paragraphs or bullet points

## Phase 6: Style Preference
Ask emoji preference using **AskUserQuestion**:

- Header: "Style"
- Question: "Should emojis be used in the configuration files?"
- Options:
  - `{"label": "No Emojis (Recommended)", "description": "Professional, text-only formatting"}`
  - `{"label": "Use Emojis", "description": "Add visual indicators using emojis"}`

## Phase 7: Assembly & Generation
1. **Read selected template** from Phase 3

2. **Prepare Developer Profile Section**
   ```markdown
   ## Developer Profile
   - **Name**: [User's Name or "Developer"]
   - **Email**: [User's Email or omit if skipped]
   ```

3. **Generate Tech Stack Sections**
   - Generate configuration for each selected technology
   - Use selected package managers in all examples
   - Apply emoji preference
   - Append web search summaries if enabled

4. **Assemble Final Content**
   - Combine: header + developer profile + base template + tech stack sections

## Phase 8: Length Validation
1. **Validate content length**
   - Write assembled content to a temporary file
   - Run validation script: `${CLAUDE_PLUGIN_ROOT}/scripts/validate-length.sh`

2. **Handle results**:
   - ACCEPTABLE/OPTIMAL: Proceed to Phase 9
   - TOO_LONG/EXCESSIVE: Ask user via **AskUserQuestion**:
     - Header: "Length"
     - Question: "Configuration exceeds best practice length. How to proceed?"
     - Options: Auto-trim / Keep as-is / Manual review
   - TOO_SHORT: Show info and proceed

## Phase 9: Write CLAUDE.md
1. **Write final file to `$HOME/.claude/CLAUDE.md`**
   - Check if `$HOME/.claude/CLAUDE.md` exists
   - Backup to `$HOME/.claude/CLAUDE.md.bak` if needed
   - Ensure directory `$HOME/.claude/` exists
   - Write assembled content to `$HOME/.claude/CLAUDE.md`

2. **Report summary**
   - File location: `$HOME/.claude/CLAUDE.md`
   - Backup location (if created)
   - Developer info
   - TDD mode
   - Technology stacks with package managers
   - Web search status
   - Word count and validation status

## Best Practices
- Progressive workflow: Each phase builds on previous results
- User control: Always ask before making significant decisions
- Safety: Always backup existing files before overwriting
