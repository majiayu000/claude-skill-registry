---
name: testing-prpm-cli
description: Use when testing PRPM CLI commands locally - provides build, environment setup, execution workflow, contract testing to verify documented behavior matches implementation, and comprehensive cross-format conversion testing against local registry
---

# Testing PRPM CLI

## Overview

Test PRPM CLI commands against a local registry by building the package, setting the registry URL, and invoking the CLI directly. Includes comprehensive cross-format conversion testing patterns and **contract testing** to verify documented behavior matches implementation.

## When to Use

- Testing new CLI commands or features
- Debugging CLI behavior
- Verifying CLI changes before committing
- Testing against local registry data
- **Validating cross-format conversions**
- **Testing new format converters**
- **Contract testing: verifying documented behavior matches implementation**

## Quick Reference

| Step | Command |
|------|---------|
| Build CLI | `npm run build --workspace=packages/cli` |
| Start local registry | `npm run dev --workspace=packages/registry` |
| Set local registry | `export PRPM_REGISTRY_URL=http://127.0.0.1:3111` |
| Run CLI directly | `node /Users/khaliqgant/Projects/prpm/app/packages/cli/dist/index.js <command>` |
| Run via npm link | `prpm <command>` (after linking) |

## Workflow

### 1. Build the CLI (Required First Step)

Always rebuild before testing to ensure you're testing current code:

```bash
npm run build --workspace=packages/cli
```

### 2. Start Local Registry

Start the registry server in background:

```bash
npm run dev --workspace=packages/registry &
sleep 3
lsof -i :3111  # Verify it's running
```

### 3. Configure Local Registry

Point CLI to local registry instead of production:

```bash
export PRPM_REGISTRY_URL=http://127.0.0.1:3111
```

Verify it's set:
```bash
echo $PRPM_REGISTRY_URL
```

### 4. Run CLI Commands

**Option A: Direct invocation (recommended for testing)**
```bash
node /Users/khaliqgant/Projects/prpm/app/packages/cli/dist/index.js search typescript
node /Users/khaliqgant/Projects/prpm/app/packages/cli/dist/index.js install some-package
```

**Option B: npm link (for interactive testing)**
```bash
cd packages/cli
npm link
prpm search typescript
```

## Comprehensive Conversion Testing

### Use Self-Improving Skill to Find Test Packages

Before testing conversions, use the `self-improving` skill to download a diverse set of packages:

```bash
# Search for packages of different types
node $CLI search "claude" --limit 10
node $CLI search "cursor" --limit 10
node $CLI search "agent" --limit 10
node $CLI search "skill" --limit 10
```

### Create Test Directory and Install Diverse Packages

```bash
mkdir -p /tmp/prpm-conversion-tests
cd /tmp/prpm-conversion-tests
export PRPM_REGISTRY_URL=http://127.0.0.1:3111
CLI="/Users/khaliqgant/Projects/prpm/app/packages/cli/dist/index.js"

# Install packages of different subtypes
node $CLI install @prpm/agent-builder-skill --as claude      # Skill
node $CLI install @prpm/creating-cursor-rules --as cursor    # Cursor Rule
node $CLI install @camoneart/context-engineering-agent --as claude  # Agent
```

### Supported Formats (CLI_SUPPORTED_FORMATS)

Test conversions across ALL supported formats:

| Format | Description |
|--------|-------------|
| cursor | Cursor IDE rules (.mdc) |
| claude | Claude Code (skills, agents, commands) |
| windsurf | Windsurf rules |
| continue | Continue rules |
| copilot | GitHub Copilot instructions |
| kiro | Kiro steering files |
| agents.md | Agents.md format |
| gemini | Gemini CLI extensions |
| ruler | Ruler format |
| zed | Zed editor extensions |
| opencode | OpenCode rules |
| aider | Aider conventions |
| trae | Trae rules |
| replit | Replit agent rules |
| zencoder | ZenCoder rules |
| droid | Factory/Droid rules |

### Conversion Test Matrix

Run comprehensive conversion tests:

```bash
cd /tmp/prpm-conversion-tests
mkdir -p /tmp/conversions
CLI="/Users/khaliqgant/Projects/prpm/app/packages/cli/dist/index.js"

# Claude Skill → All formats
for format in cursor windsurf kiro gemini zed continue copilot opencode aider trae replit zencoder droid; do
  node $CLI convert .claude/skills/*/SKILL.md --to $format -o /tmp/conversions/skill-to-$format.md 2>&1
done

# Cursor Rule → Multiple formats
for format in claude windsurf gemini zed; do
  node $CLI convert .cursor/rules/*.mdc --to $format -o /tmp/conversions/cursor-to-$format.md 2>&1
done

# Claude Agent → Multiple formats
for format in cursor gemini windsurf; do
  node $CLI convert .claude/agents/*.md --to $format -o /tmp/conversions/agent-to-$format.md 2>&1
done
```

### Round-Trip Testing

Verify content preservation through round-trip conversions:

```bash
# Claude → Cursor → Claude
node $CLI convert .claude/skills/*/SKILL.md --to cursor -o /tmp/conversions/step1-cursor.mdc
node $CLI convert /tmp/conversions/step1-cursor.mdc --to claude -o /tmp/conversions/step2-claude.md

# Compare file sizes (expect some reduction but not dramatic)
wc -c .claude/skills/*/SKILL.md /tmp/conversions/step1-cursor.mdc /tmp/conversions/step2-claude.md
```

### Validation Checklist

For each conversion, verify:

- [ ] **Command succeeds** - Exit code 0, no errors
- [ ] **Output file created** - File exists at specified path
- [ ] **Content preserved** - Core markdown structure intact
- [ ] **Format-specific frontmatter** - Correct fields for target format
- [ ] **File size reasonable** - Not truncated (compare with source)

### Expected File Sizes

| Conversion Type | Expected Size Ratio |
|----------------|---------------------|
| Claude → Cursor | ~95-100% |
| Claude → Windsurf | ~95-100% |
| Claude → Gemini | ~95-100% |
| Claude → OpenCode | May be smaller (format limits) |
| Claude → Droid | May be smaller (format limits) |
| Round-trip | ~50-70% (metadata loss expected) |

### Test Report Template

Document results in this format:

```markdown
## Conversion Test Report

### Test Setup
- Registry: Local (port 3111)
- Test packages: [list installed packages]

### Results

| Source | Target | Status | Output Size |
|--------|--------|--------|-------------|
| Claude Skill | Gemini | Pass/Fail | X bytes |
| ... | ... | ... | ... |

### Observations
- [Note any issues, truncations, or unexpected behavior]
```

## Contract Testing (CRITICAL)

**Contract testing ensures documented behavior matches implementation.** This is the most important type of testing for features with configurable behavior.

### Why Contract Testing Matters

The eager/lazy loading bug is a case study: documentation described a precedence chain (CLI > file > package > default), but implementation only handled CLI flags. Tests passed because they only tested the CLI flag path. **Contract testing would have caught this.**

### Contract Testing Principles

1. **Test EVERY documented behavior path, not just the happy path**
2. **Test precedence chains completely** - if docs say "A > B > C > default", test all 4 cases
3. **Test behavior WITHOUT flags** - verify defaults and configuration-driven behavior
4. **Test WITH and WITHOUT explicit settings** - don't assume flag presence

### Contract Testing Checklist

For ANY feature with documented behavior:

- [ ] **Read the documentation first** - what does it claim to do?
- [ ] **List all behavior paths** - every if/else/default mentioned
- [ ] **Create test for each path** - one test per documented behavior
- [ ] **Test WITHOUT user flags** - verify package/config defaults work
- [ ] **Test precedence** - verify higher-priority overrides lower
- [ ] **Verify error messages match** - documented errors should occur

### Example: Eager/Lazy Loading Contract Tests

Documentation states: "Precedence: CLI flag > package-level > default (lazy)"

**Required tests:**

```bash
# Setup test directory
mkdir -p /tmp/prpm-contract-tests
cd /tmp/prpm-contract-tests
export PRPM_REGISTRY_URL=http://127.0.0.1:3111
CLI="/Users/khaliqgant/Projects/prpm/app/packages/cli/dist/index.js"

# Test 1: CLI --eager flag (highest priority)
rm -rf .openskills AGENTS.md
node $CLI install @prpm/some-skill --as agents.md --eager
# VERIFY: AGENTS.md contains activation="eager" or priority="0"
grep -q 'activation="eager"\|priority="0"' AGENTS.md && echo "PASS: CLI --eager works" || echo "FAIL: CLI --eager"

# Test 2: CLI --lazy flag overrides package eager
rm -rf .openskills AGENTS.md
# Install a package that has eager:true in prpm.json with --lazy flag
node $CLI install @prpm/eager-package --as agents.md --lazy
# VERIFY: Should be lazy despite package setting
grep -q 'activation="lazy"\|priority="1"' AGENTS.md && echo "PASS: CLI --lazy overrides" || echo "FAIL: CLI --lazy"

# Test 3: Package-level eager (NO CLI flag) - THIS IS THE BUG THAT WAS MISSED
rm -rf .openskills AGENTS.md
# Install a package that has eager:true in its prpm.json WITHOUT --eager flag
node $CLI install @prpm/eager-package --as agents.md
# VERIFY: Should be eager based on package setting
grep -q 'activation="eager"\|priority="0"' AGENTS.md && echo "PASS: Package eager works" || echo "FAIL: Package eager"

# Test 4: Default (lazy) when no flags and no package setting
rm -rf .openskills AGENTS.md
node $CLI install @prpm/normal-skill --as agents.md
# VERIFY: Should be lazy by default
grep -q 'activation="lazy"\|priority="1"' AGENTS.md && echo "PASS: Default lazy works" || echo "FAIL: Default"
```

### Contract Test Template

For any new feature, create tests in this format:

```markdown
## Contract Tests for [Feature Name]

### Documentation Claims:
1. [Claim 1 from docs]
2. [Claim 2 from docs]
3. [Precedence/default behavior from docs]

### Test Cases:

| # | Documented Behavior | Test Setup | Expected Result | Pass/Fail |
|---|--------------------|-----------| ----------------|-----------|
| 1 | [Claim 1] | [How to test] | [What to verify] | |
| 2 | [Claim 2] | [How to test] | [What to verify] | |
| 3 | Default behavior | [No flags/config] | [Default result] | |

### Results:
- All tests must pass before feature is considered complete
- Document any deviations between docs and implementation
```

### Anti-Patterns to Avoid

| Anti-Pattern | Why It Fails | Correct Approach |
|--------------|--------------|------------------|
| Only testing with flags | Misses config/default paths | Test without flags first |
| Assuming documentation is implementation | Docs may describe intent, not reality | Verify each claim with test |
| Testing happy path only | Misses precedence bugs | Test all documented paths |
| Skipping default behavior test | Defaults often broken | Always test "no config" case |
| Not reading docs before testing | Miss documented behaviors | Read docs, list claims, test each |

## Common Mistakes

| Mistake | Symptom | Fix |
|---------|---------|-----|
| Forgetting to build | Old behavior, changes not reflected | Run `npm run build --workspace=packages/cli` |
| Missing registry env | Commands hit production registry | Set `PRPM_REGISTRY_URL` before running |
| Stale npm link | Wrong version running | Re-run `npm link` after rebuilding |
| Local registry not running | Connection refused errors | Start registry: `npm run dev --workspace=packages/registry` |
| Testing single format only | Miss format-specific bugs | Test ALL formats in CLI_SUPPORTED_FORMATS |
| No round-trip testing | Miss content loss bugs | Always verify round-trip preservation |
| **No contract testing** | **Docs ≠ implementation** | **Test EVERY documented behavior** |
| **Only testing with CLI flags** | **Miss config/default bugs** | **Test without flags to verify defaults** |

## One-Liner Setup

```bash
npm run build --workspace=packages/cli && export PRPM_REGISTRY_URL=http://127.0.0.1:3111
```

Then test commands:
```bash
node packages/cli/dist/index.js --help
```

## Unit Test Commands

Run converter unit tests:

```bash
# All converter tests
npm run test --workspace=packages/converters

# Specific test files
npm run test --workspace=packages/converters -- --testPathPattern="file-references"
npm run test --workspace=packages/converters -- --testPathPattern="security"
npm run test --workspace=packages/converters -- --testPathPattern="cross-format"
npm run test --workspace=packages/converters -- --testPathPattern="zed"
```
