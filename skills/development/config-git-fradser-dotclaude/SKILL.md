---
name: config-git
description: Interactive git configuration setup
user-invocable: true
allowed-tools: ["Bash(git:*)", "Bash(ls:*)", "Bash(find:*)", "Read", "Write", "Glob", "AskUserQuestion"]
argument-hint: "[no arguments needed]"
model: haiku
context: fork
version: 0.1.0
---

# Interactive Git Configuration

Set up Git user identity and create project-specific configuration file `.claude/git.local.md` with conventional commit scopes, types, and branch naming conventions.

Current Git Config Context:
!`git config --list --show-origin`

---

## Phase 1: Verify User Identity

**Goal**: Ensure git user.name and user.email are configured

**Actions**:
1. Review the "Current Git Config Context" above
2. Check if `user.name` and `user.email` are set
3. If EITHER is missing, use `AskUserQuestion` to request the missing information
4. Set the values globally (or locally if user specifies) using `git config`

---

## Phase 2: Analyze Project Context

**Goal**: Understand project structure and existing commit patterns

**Actions**:
1. Run `ls -F` or `find . -maxdepth 2 -not -path '*/.*'` to detect project languages/frameworks
2. Run `git log --format="%s" -n 50` (if git repo exists) to analyze existing commit message patterns and scopes

---

## Phase 3: Determine Scopes

**Goal**: Generate appropriate commit scopes based on project structure

**CRITICAL - Scope Naming Rules**:
- ALL scopes MUST be short (single words or abbreviations only)
- Single words: use as-is (e.g., `<word1>`, `<word2>`, `<word3>`)
- Multi-word names: MUST convert to first letters (e.g., `<multi-word-name>` → `<mwn>`, `<another-example>` → `<ae>`)
- MUST NOT use full multi-word names like `<multi-word-name>` or `<another-example>` as scopes

**Actions**:
1. Propose a list of commit scopes based on analysis
2. Ensure all scopes follow the naming rules above
3. Request user input ONLY if genuine ambiguity exists

---

## Phase 4: Generate Configuration File

**Goal**: Create `.claude/git.local.md` with complete structure from example template

**CRITICAL - Template Requirements**:
- Use the ENTIRE example file structure as template
- Preserve ALL sections from the example:
  - YAML frontmatter with `scopes`, `types`, `branch_prefixes`, AND `gitignore`
  - "# Project-Specific Git Settings" section
  - "## Usage" section with all bullet points
  - "## Additional Guidelines" section with all bullet points

**Actions**:
1. Read the example configuration file: `${CLAUDE_PLUGIN_ROOT}/examples/git.local.md`
2. Replace the `scopes` list with determined short scopes
3. Update `gitignore` technologies based on detected project languages/frameworks
4. Keep `types` as standard conventional commit types (unless user requests changes)
5. Keep `branch_prefixes` as shown in example (unless user requests changes)
6. Create or overwrite `.claude/git.local.md` in the project root
7. Read the file back to verify it matches the example's complete structure

**Output**: `.claude/git.local.md` file with project-specific configuration

---

## Phase 5: Confirmation

**Goal**: Inform user of successful configuration

**Actions**:
1. Confirm configuration is complete
2. Show the location of the created file
