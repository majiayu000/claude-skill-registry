---
name: setup-ast
description: "Configure tree-sitter CLI and language grammars for AST-powered code review. Use when AST extraction fails, tree-sitter not found, grammars missing, or setting up new machine. Triggers on: setup tree-sitter, install grammars, AST not working, tree-sitter not found, setup ast."
---

# Setup AST

Diagnose and configure tree-sitter for AST-powered code extraction.

## Quick Start (Non-Interactive)

For automated setup without prompts, use the shell script:

```bash
./scripts/setup-tree-sitter.sh          # Core grammars
./scripts/setup-tree-sitter.sh --all    # All grammars
./scripts/setup-tree-sitter.sh --status # Check status
```

---

## Interactive Flow (with guidance)

```
GROUND → DETECT → PLAN → INSTALL → VERIFY
```

---

## MANDATORY GATES

**These gates CANNOT be skipped. Period.**

| Gate | Requirement | Why |
|------|-------------|-----|
| **GROUND first** | Diagnosis MUST complete before INSTALL | Blind install can overwrite working setup |
| **VERIFY last** | Verification MUST run after INSTALL | Partial installs silently break extraction |
| **Tasks tracked** | Every step creates/updates tasks | User sees progress, agent can't skip |

**If user requests skipping diagnostics:**
```
"I need to check your current setup first. Blind installation can:
- Overwrite existing grammars that are working
- Create duplicate installations
- Miss the actual problem if something is broken

This takes ~30 seconds. Proceeding with diagnostics."
```

Then proceed with GROUND. Do NOT skip.

---

## Anti-Rationalization Table

| Rationalization | Reality |
|-----------------|---------|
| "User said skip diagnostics" | Diagnostics prevent breaking working setups |
| "Just install everything, it's faster" | Overwriting grammars can corrupt existing setup |
| "Verification is optional cleanup" | Without verification, user thinks it worked when it didn't |
| "I know what's needed from the error" | Errors can mislead; diagnose to find root cause |
| "User is impatient, just do it" | 30 seconds of diagnosis saves hours of debugging |
| "CLI exists so grammars will work" | CLI ≠ grammars ≠ query files ≠ env var |

---

## Quick Reference

| Situation | Action |
|-----------|--------|
| No tree-sitter CLI | Install via Homebrew/Cargo |
| CLI exists, no grammars | Clone + build grammars |
| Grammars exist, wrong location | Set TREE_SITTER_GRAMMAR_DIR |
| Grammars exist, no tags.scm | Grammar incomplete - reclone |
| Everything works | Report status, exit |

---

## STEP 1: GROUND - Assess Current State

**Create diagnostic task:**

```
TaskCreate(
  subject: "Diagnose tree-sitter setup",
  description: "Check CLI, grammars, environment",
  activeForm: "Diagnosing tree-sitter setup"
)
TaskUpdate(taskId: "...", status: "in_progress")
```

**Run diagnostics:**

```bash
# 1. Check CLI
command -v tree-sitter && tree-sitter --version

# 2. Check grammar directory
GRAMMAR_DIR="${TREE_SITTER_GRAMMAR_DIR:-$HOME/repos/tree-sitter-grammars}"
ls -la "$GRAMMAR_DIR" 2>/dev/null || echo "NOT_FOUND"

# 3. Run extraction status check
./agents/extract-units.sh --status

# 4. Check shell config for TREE_SITTER_GRAMMAR_DIR
grep -l "TREE_SITTER_GRAMMAR_DIR" ~/.zshrc ~/.bashrc ~/.bash_profile 2>/dev/null || echo "NOT_SET"
```

**Classify state:**

| CLI | Grammars | Env Var | State |
|-----|----------|---------|-------|
| ❌ | - | - | `FRESH_INSTALL` |
| ✅ | ❌ | - | `NEEDS_GRAMMARS` |
| ✅ | ✅ | ❌ | `NEEDS_ENV` |
| ✅ | ✅ | ✅ | `CHECK_HEALTH` |

**Complete diagnostic task:**

```
TaskUpdate(taskId: "...", status: "completed")
```

**Report to user:**

```markdown
## Tree-Sitter Status

| Component | Status |
|-----------|--------|
| CLI | ✅ v0.26.3 |
| Grammar Dir | ✅ ~/repos/tree-sitter-grammars |
| Installed Grammars | 12 |
| Working Parsers | 7 |
| Environment | ⚠️ TREE_SITTER_GRAMMAR_DIR not set |
```

---

## STEP 2: DETECT - Scan Project Languages

**Create detection task:**

```
TaskCreate(
  subject: "Detect project languages",
  description: "Scan repo for file types to determine needed grammars",
  activeForm: "Scanning project languages"
)
```

**Scan repository:**

```bash
# Count files by extension
find . -type f -name "*.ts" -o -name "*.tsx" | wc -l
find . -type f -name "*.js" -o -name "*.jsx" | wc -l
find . -type f -name "*.py" | wc -l
find . -type f -name "*.go" | wc -l
find . -type f -name "*.rs" | wc -l
find . -type f -name "*.java" | wc -l
find . -type f -name "*.rb" | wc -l
find . -type f -name "*.c" -o -name "*.h" | wc -l
find . -type f -name "*.cpp" -o -name "*.cc" | wc -l
find . -type f -name "*.swift" | wc -l
find . -type f -name "*.kt" | wc -l
```

**Map extensions to grammars:**

| Extension | Grammar Repo |
|-----------|--------------|
| ts, tsx | tree-sitter-typescript |
| js, jsx, mjs | tree-sitter-javascript |
| py | tree-sitter-python |
| go | tree-sitter-go |
| rs | tree-sitter-rust |
| java | tree-sitter-java |
| rb | tree-sitter-ruby |
| c, h | tree-sitter-c |
| cpp, cc, hpp | tree-sitter-cpp |
| swift | tree-sitter-swift |
| kt | tree-sitter-kotlin |

**Ask user to confirm:**

```
AskUserQuestion(
  questions: [{
    header: "Languages",
    question: "Which language grammars should I install?",
    multiSelect: true,
    options: [
      // Show detected languages first, sorted by file count
      {label: "TypeScript (142 files)", description: "tree-sitter-typescript"},
      {label: "JavaScript (23 files)", description: "tree-sitter-javascript"},
      // ... others detected
      {label: "All supported", description: "Install all 15+ grammars"}
    ]
  }]
)
```

---

## STEP 3: PLAN - Create Installation Tasks

Based on GROUND state, create appropriate tasks:

### If FRESH_INSTALL:

```
TaskCreate(subject: "Install tree-sitter CLI", description: "Install via Homebrew or Cargo", activeForm: "Installing tree-sitter CLI")
TaskCreate(subject: "Create grammar directory", description: "mkdir -p ~/repos/tree-sitter-grammars", activeForm: "Creating grammar directory")
TaskCreate(subject: "Clone language grammars", description: "Clone selected grammar repos", activeForm: "Cloning grammars")
TaskCreate(subject: "Build grammars", description: "Run tree-sitter generate for each", activeForm: "Building grammars")
TaskCreate(subject: "Set environment variable", description: "Add TREE_SITTER_GRAMMAR_DIR to shell config", activeForm: "Setting environment")
TaskCreate(subject: "Verify installation", description: "Test parsing with each grammar", activeForm: "Verifying installation")
```

### If NEEDS_GRAMMARS:

```
TaskCreate(subject: "Clone language grammars", ...)
TaskCreate(subject: "Build grammars", ...)
TaskCreate(subject: "Verify installation", ...)
```

### If NEEDS_ENV:

```
TaskCreate(subject: "Set environment variable", ...)
TaskCreate(subject: "Verify installation", ...)
```

### If CHECK_HEALTH:

```
TaskCreate(subject: "Verify all grammars working", ...)
TaskCreate(subject: "Fix broken grammars", ...) // if any found
```

---

## STEP 4: INSTALL - Execute Tasks

**GATE CHECK: Do NOT proceed unless:**
- [ ] GROUND task status = "completed"
- [ ] User has selected languages (or confirmed "all")
- [ ] Installation plan tasks are created

If GROUND not completed:
```
"Cannot install without diagnosis. Running GROUND step first..."
```
Then go back to STEP 1.

---

### Install tree-sitter CLI

```bash
# macOS
brew install tree-sitter

# Linux/Other (requires Rust)
cargo install tree-sitter-cli

# Verify
tree-sitter --version
```

### Create grammar directory

```bash
mkdir -p ~/repos/tree-sitter-grammars
```

### Clone grammars

For each selected language, clone the official grammar:

```bash
cd ~/repos/tree-sitter-grammars

# Core grammars (official tree-sitter org)
git clone https://github.com/tree-sitter/tree-sitter-javascript.git
git clone https://github.com/tree-sitter/tree-sitter-typescript.git
git clone https://github.com/tree-sitter/tree-sitter-python.git
git clone https://github.com/tree-sitter/tree-sitter-go.git
git clone https://github.com/tree-sitter/tree-sitter-rust.git
git clone https://github.com/tree-sitter/tree-sitter-java.git
git clone https://github.com/tree-sitter/tree-sitter-ruby.git
git clone https://github.com/tree-sitter/tree-sitter-c.git
git clone https://github.com/tree-sitter/tree-sitter-cpp.git

# Community grammars (different orgs)
git clone https://github.com/alex-pinkus/tree-sitter-swift.git
git clone https://github.com/fwcd/tree-sitter-kotlin.git
```

### Build grammars

```bash
cd ~/repos/tree-sitter-grammars

for dir in tree-sitter-*/; do
  echo "Building $dir..."
  cd "$dir"
  tree-sitter generate 2>/dev/null || true
  cd ..
done
```

### Set environment variable

```bash
# Detect shell
SHELL_CONFIG="$HOME/.zshrc"
[[ "$SHELL" == *"bash"* ]] && SHELL_CONFIG="$HOME/.bashrc"

# Add if not present
if ! grep -q "TREE_SITTER_GRAMMAR_DIR" "$SHELL_CONFIG"; then
  echo 'export TREE_SITTER_GRAMMAR_DIR="$HOME/repos/tree-sitter-grammars"' >> "$SHELL_CONFIG"
  echo "Added TREE_SITTER_GRAMMAR_DIR to $SHELL_CONFIG"
fi

# Source for current session
export TREE_SITTER_GRAMMAR_DIR="$HOME/repos/tree-sitter-grammars"
```

---

## STEP 5: VERIFY - Test Installation (MANDATORY)

**This step is NOT optional. Do NOT skip verification.**

If installation tasks completed but verification not run:
```
"Installation complete but not verified. Running verification now..."
```

**Create verification task:**

```
TaskCreate(
  subject: "Verify tree-sitter setup",
  description: "Test parsing with each installed grammar",
  activeForm: "Verifying tree-sitter setup"
)
```

**Test each grammar:**

```bash
# Run extraction status
./agents/extract-units.sh --status

# Test parsing a sample file for each language
for lang in javascript typescript python go rust java ruby c cpp; do
  echo "Testing $lang..."
  tree-sitter parse --quiet /dev/null --scope "source.$lang" 2>/dev/null && echo "✅ $lang" || echo "❌ $lang"
done
```

**Report final status:**

```markdown
## Installation Complete

| Grammar | Status | Test File |
|---------|--------|-----------|
| TypeScript | ✅ | src/index.ts parsed OK |
| JavaScript | ✅ | test.js parsed OK |
| Python | ❌ | Missing queries/tags.scm |

### Next Steps
- Run `/code-foundations:review --sanity` to test AST extraction
- Python grammar needs manual fix (see troubleshooting below)
```

**SKILL COMPLETE when:**
- [ ] Verification task status = "completed"
- [ ] At least 1 grammar shows ✅
- [ ] Final report displayed to user

If any grammar shows ❌, offer to fix it before ending.

---

## Troubleshooting

### Grammar has no tags.scm

Some grammars don't include query files. Fix:

```bash
cd ~/repos/tree-sitter-grammars/tree-sitter-python

# Check if queries directory exists
ls queries/

# If missing, check grammar repo for query files
# Some are in queries/, some in queries/python/
```

### Parser fails to build

```bash
cd ~/repos/tree-sitter-grammars/tree-sitter-problematic

# Clean and rebuild
rm -rf src/parser.c
tree-sitter generate
```

### Wrong grammar directory

```bash
# Check where extract-units.sh is looking
echo $TREE_SITTER_GRAMMAR_DIR

# Should match your grammar location
ls ~/repos/tree-sitter-grammars/
```

### CLI version mismatch

Some grammars require specific tree-sitter CLI versions:

```bash
# Upgrade CLI
brew upgrade tree-sitter
# or
cargo install tree-sitter-cli --force
```

---

## Grammar Repository Reference

| Language | Repository | Notes |
|----------|------------|-------|
| JavaScript | tree-sitter/tree-sitter-javascript | Official |
| TypeScript | tree-sitter/tree-sitter-typescript | Official, includes TSX |
| Python | tree-sitter/tree-sitter-python | Official |
| Go | tree-sitter/tree-sitter-go | Official |
| Rust | tree-sitter/tree-sitter-rust | Official |
| Java | tree-sitter/tree-sitter-java | Official |
| Ruby | tree-sitter/tree-sitter-ruby | Official |
| C | tree-sitter/tree-sitter-c | Official |
| C++ | tree-sitter/tree-sitter-cpp | Official |
| C# | tree-sitter/tree-sitter-c-sharp | Official |
| Swift | alex-pinkus/tree-sitter-swift | Community |
| Kotlin | fwcd/tree-sitter-kotlin | Community |
| Bash | tree-sitter/tree-sitter-bash | Official |
| HTML | tree-sitter/tree-sitter-html | Official |
| CSS | tree-sitter/tree-sitter-css | Official |
| JSON | tree-sitter/tree-sitter-json | Official |
