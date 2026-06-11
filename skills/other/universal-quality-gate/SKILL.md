---
name: universal-quality-gate
description: "Multi-language code quality gate with auto-detection and linters."
user-invocable: false
allowed-tools:
  - Read
  - Bash
  - Grep
  - Glob
routing:
  triggers:
    - "quality gate"
    - "lint check"
    - "multi-language lint"
    - "code quality check"
    - "language-agnostic lint"
  category: code-quality
  pairs_with:
    - code-linting
    - verification-before-completion
---

# Universal Quality Gate Skill

Language-agnostic code quality checking system. Automatically detects project languages via marker files and runs appropriate linters, formatters, and static analysis tools for each detected language.

## Overview

This skill implements a **Detect, Check, Report** pattern for multi-language code quality enforcement:
1. Auto-detect languages by scanning for marker files (go.mod, package.json, pyproject.toml, Cargo.toml, etc.)
2. Run language-specific lint, format, type-check, and security tools
3. Report complete results with graceful degradation for unavailable tools

**Key Principles:**
- **Read repository CLAUDE.md files first** — Project instructions override default behaviors
- **Only run configured tools** — Do not add new tools, languages, or checks unless explicitly requested. Keep quality checks focused on what is already defined in language_registry.json.
- **Show complete output** — Display full linter output, never summarize as "no issues"
- **Graceful degradation** — Skip unavailable tools without failing the entire gate
- **Fail only on required tools** — Only return non-zero exit if required tool failures occur

---

## Supported Languages

| Language | Marker Files | Tools |
|----------|--------------|-------|
| Python | pyproject.toml, requirements.txt | ruff, mypy, bandit |
| Go | go.mod | gofmt, golangci-lint, go vet |
| JavaScript | package.json | eslint, biome |
| TypeScript | tsconfig.json | tsc, eslint, biome |
| Rust | Cargo.toml | clippy, cargo fmt |
| Ruby | Gemfile | rubocop |
| Java | pom.xml, build.gradle | PMD |
| Shell | *.sh, *.bash | shellcheck |
| YAML | *.yml, *.yaml | yamllint |
| Markdown | *.md | markdownlint |

## Instructions

### Step 1: Execute Quality Gate

Run the quality gate check against the current project:

```bash
python3 ~/.claude/skills/code-quality/universal-quality-gate/scripts/run_quality_gate.py
```

This command automatically:
- Detects all languages in the project by scanning for marker files
- Runs language-specific tools for each detected language
- Reports full output with file paths and line numbers
- Returns zero exit code if all required tools pass

### Step 2: Choose Your Flow

**For pre-commit validation** (fastest):
```bash
python3 ~/.claude/skills/code-quality/universal-quality-gate/scripts/run_quality_gate.py --staged
```
Checks only git-staged files, enabling rapid feedback on recent changes.

**For auto-fixing** (when issues are found):
```bash
python3 ~/.claude/skills/code-quality/universal-quality-gate/scripts/run_quality_gate.py --fix
```
Auto-corrects fixable issues (formatting, imports, etc.), then re-run Step 1 to verify.

**For focused checking** (single language):
```bash
python3 ~/.claude/skills/code-quality/universal-quality-gate/scripts/run_quality_gate.py --lang python
```
Narrows scope when debugging language-specific issues.

**For verbose details**:
```bash
python3 ~/.claude/skills/code-quality/universal-quality-gate/scripts/run_quality_gate.py -v
```
Shows expanded diagnostic output for troubleshooting.

### Step 3: Interpret Results

**PASSED output:**
```
============================================================
 Quality Gate: PASSED
============================================================

Languages: python, javascript
Files: 15

Tool Results:
  [+] python/lint: passed
  [+] python/format: passed
  [-] python/typecheck: skipped (Optional tool not installed)
  [+] javascript/lint: passed
  [+] javascript/format: passed

Quality gate passed: 4/5 tools OK (1 skipped)
```
Gate passes when all required tools succeed. Skipped optional tools do not block.

**FAILED output:**
```
============================================================
 Quality Gate: FAILED
============================================================

Languages: python, go
Files: 8

Tool Results:
  [X] python/lint: FAILED
      hooks/example.py:42:1: F841 local variable 'x' is assigned but never used
      hooks/example.py:56:1: F401 'os' imported but unused
  [+] python/format: passed
  [+] go/format: passed
  [X] go/lint: FAILED
      main.go:15:2: S1000: should use for range instead of for select

Pattern Matches:
  [WARNING] hooks/example.py:78: Silent exception handler - add explanatory comment

Quality gate failed: 2 tool(s) reported issues, 1 error pattern(s)
```
Review marked failures [X] first. Pattern matches [WARNING] are informational.

### Step 4: Resolve Issues

**For auto-fixable issues:**
1. Run `python3 ~/.claude/skills/code-quality/universal-quality-gate/scripts/run_quality_gate.py --fix`
2. Review changes with `git diff` to verify correctness
3. Re-run Step 1 to confirm all checks pass
4. Commit with message documenting the fixes

**For manual fixes:**
1. Review each issue line-by-line in the output
2. Edit files to correct the reported problems
3. Re-run Step 1 to verify fixes
4. Commit changes

### Step 5: Commit

Once quality gate passes with zero required-tool failures:
1. Run project tests to catch logic regressions
2. Commit with descriptive message
3. Proceed to PR/merge workflow

---

## Common Workflows

**Pre-commit validation (fastest path):**
```bash
python3 ~/.claude/skills/code-quality/universal-quality-gate/scripts/run_quality_gate.py --staged
# If fails → fix issues → re-run
# If passes → git commit
```

**Full repo audit:**
```bash
python3 ~/.claude/skills/code-quality/universal-quality-gate/scripts/run_quality_gate.py
# Review all findings by language
# Fix by category: required failures → warnings → patterns
# Re-run after each batch of fixes
```

**Language-specific validation:**
```bash
python3 ~/.claude/skills/code-quality/universal-quality-gate/scripts/run_quality_gate.py --lang python
# Use when debugging a specific language's toolchain
# Narrows output and speeds iteration
```

---

## Extending with New Languages

To add language support without editing the script, modify the language registry:

```json
// hooks/lib/language_registry.json
{
  "new_language": {
    "extensions": [".ext"],
    "markers": ["config.file"],
    "tools": {
      "lint": {
        "cmd": "linter {files}",
        "fix_cmd": "linter --fix {files}",
        "description": "Language linter",
        "required": true
      }
    }
  }
}
```

The quality gate script automatically detects and uses new registry entries on next run.

---

## Error Handling

### Error: "No files to check"
**Cause**: No changed files detected or no language markers found in project
**Solution**:
1. Verify you are in the correct project directory
2. Check that marker files exist (go.mod, package.json, pyproject.toml, etc.)
3. If checking staged files with `--staged`, ensure files are staged with `git add`
4. For empty projects, this is expected behavior — add source files first

### Error: "Tool not found" / "Required tool not installed"
**Cause**: A required linter tool is not installed on the system
**Solution**:
1. Identify which tool is missing from the output (e.g., golangci-lint, ruff)
2. Install the tool using your package manager:
   - Python: `pip install ruff mypy bandit`
   - Go: `go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest`
   - JavaScript: `npm install --save-dev eslint biome`
   - Rust: `cargo install clippy` (usually pre-installed with rustup)
3. Re-run the quality gate to verify installation
4. **Alternative**: Mark the tool as optional in `language_registry.json` if you cannot install it

### Error: "Command timed out"
**Cause**: Tool taking longer than 60-second timeout (usually large file sets or performance issues)
**Solution**:
1. Use `--staged` to check only changed files instead of the entire project
2. Use `--lang` to check one language at a time
3. Check for generated files or very large files causing slowdown — add them to .gitignore
4. Verify your system has adequate disk I/O (slow disks can cause timeouts)

### Error: "Configuration file conflict"
**Cause**: Multiple conflicting linter configurations in the project (e.g., .eslintrc and biome.json)
**Solution**:
1. Check which tools the project actually uses (review package.json, go.mod, etc.)
2. Identify the unused tool in `language_registry.json`
3. Mark it as optional or disable it by removing it from the registry
4. Consult the project's CLAUDE.md for tool preferences — project preferences override defaults
5. Re-run to confirm conflict is resolved

### Pattern Match Warnings (not failures)
**Pattern Matches** like "Silent exception handler" or "Debug print" are informational warnings. They do not fail the gate. Review them and decide whether to fix:
- `[WARNING]` entries identify failure modes but don't block commits
- Use `--no-patterns` to skip pattern scanning if these are not relevant
- Manually fix patterns that represent actual problems in your code

### Graceful Degradation (Skipped Tools)
When a tool is marked optional and not installed:
- Tool appears as `[-] language/tool: skipped (Optional tool not installed)`
- Gate still passes because the tool is not required
- If you need that tool's checks, install it and re-run

---

## Architecture

```
hooks/lib/
  quality_gate.py        # Shared core library
  language_registry.json # Language configurations

skills/code-quality/universal-quality-gate/
  SKILL.md               # This file
  scripts/
    run_quality_gate.py  # Skill entry point (thin wrapper)
```

This skill uses the shared quality gate library from `hooks/lib/` for on-demand code quality checking.

---

## References

**Multi-language linting**: Language configurations in `hooks/lib/language_registry.json`

**Related skills**:
- Use `code-linting` for single-language lint/format tasks
- Use `systematic-code-review` for comprehensive code review beyond linting
- Use `test-driven-development` for full validation with tests

**Key principle**: Quality gates catch syntax and style issues. They do not replace:
- Unit and integration tests (logic errors, race conditions)
- Code review (architectural problems, API design)
- Domain-specific validation (business logic, performance)
