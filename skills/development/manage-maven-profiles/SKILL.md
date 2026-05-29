---
name: manage-maven-profiles
description: Maven build profile classification and user workflow for unmatched profiles
user-invocable: false
allowed-tools: Read, Bash, AskUserQuestion
---

# Maven Profile Management

Classify Maven build profiles that weren't auto-matched during discovery.

## When to Use

This skill is invoked by `analyze-project-architecture` when:
1. Project contains Maven modules (`build_systems` includes `maven`)
2. Discovery found NO-MATCH-FOUND profiles

**Do not use directly** - invoked conditionally from architecture analysis workflow.

---

## Profile Classification

Maven profiles enable optional build features. Extension API classifies profiles during discovery:

| Classification | Meaning |
|----------------|---------|
| Canonical (e.g., `coverage`) | Generates build command |
| `NO-MATCH-FOUND` | No command generated |

**Key Insight**: Most NO-MATCH-FOUND profiles are **correctly unmatched**:
- `apache-release` → Release process, not a build command
- `skip-unit-tests` → Test skipping, not a positive command
- `use-apache-snapshots` → Repository config, not a command

---

## Workflow

### Step 1: Collect Unmatched Profiles Across All Modules

#### Step 1a: Get Module List

```bash
python3 .plan/execute-script.py plan-marshall:analyze-project-architecture:architecture modules
```

**Output (TOON)**:
```toon
modules[N]:
  - module-a
  - module-b
  - module-c
```

#### Step 1b: Query Each Module for Profiles

For each module in the list:

```bash
python3 .plan/execute-script.py plan-marshall:analyze-project-architecture:architecture \
  derived-module --name {module-name}
```

Parse the TOON output:
- Check `build_systems` contains `maven`
- If Maven, check `metadata.profiles` for entries with `canonical: NO-MATCH-FOUND`

#### Step 1c: Build Unmatched Profile Set

Collect all NO-MATCH-FOUND profiles into a deduplicated set:

```
unmatched_profiles = {profile-id-1, profile-id-2, ...}
```

**Note**: Same profile ID may appear in multiple modules. Only ask once per unique profile ID.

**If set is empty** → Exit, nothing to do.

### Step 2: Ask User About Each Unmatched Profile

For each NO-MATCH-FOUND profile:

```yaml
AskUserQuestion:
  question: "Maven profile '{profile-id}' is unmatched. What should it do?"
  header: "Profile"
  options:
    - label: "Ignore"
      description: "Leave as NO-MATCH-FOUND, no command generated"
    - label: "Skip"
      description: "Add to skip list, exclude from all processing"
    - label: "Map to canonical"
      description: "Map to integration-tests, coverage, benchmark, or quality-gate"
  multiSelect: false
```

### Step 3: Apply User Decision

| Choice | Action | Command |
|--------|--------|---------|
| Ignore | Leave as-is | None |
| Skip | Add to skip list | See below |
| Map | Add mapping | See below |

**Skip** - Add to skip list:
```bash
# Get current value first
python3 .plan/execute-script.py plan-marshall:manage-plan-marshall-config:plan-marshall-config ext-defaults get \
  --key build.maven.profiles.skip

# Append new profile (comma-separated)
python3 .plan/execute-script.py plan-marshall:manage-plan-marshall-config:plan-marshall-config ext-defaults set \
  --key build.maven.profiles.skip --value "{existing},{profile-id}"
```

**Map** - Add canonical mapping:
```bash
# Get current mappings first
python3 .plan/execute-script.py plan-marshall:manage-plan-marshall-config:plan-marshall-config ext-defaults get \
  --key build.maven.profiles.map.canonical

# Append new mapping (comma-separated profile:canonical pairs)
python3 .plan/execute-script.py plan-marshall:manage-plan-marshall-config:plan-marshall-config ext-defaults set \
  --key build.maven.profiles.map.canonical --value "{existing},{profile-id}:{canonical}"
```

### Step 4: Re-run Discovery

After any configuration change:

```bash
python3 .plan/execute-script.py plan-marshall:analyze-project-architecture:architecture discover --force
```

---

## Canonical Classifications

| Canonical | Description | Example Profile IDs |
|-----------|-------------|---------------------|
| `integration-tests` | Integration/E2E tests | `it`, `e2e`, `local-integration-tests` |
| `coverage` | Code coverage | `jacoco`, `istanbul` |
| `benchmark` | Benchmarks | `jmh`, `perf`, `stress` |
| `quality-gate` | Quality checks | `pre-commit`, `lint`, `checkstyle` |
| `skip` | Exclude from command generation | Internal profiles |

---

## Multiple Profiles to One Canonical

When multiple profiles map to the same canonical:

- Only ONE command is generated
- First discovered profile becomes primary
- All profiles listed in `all_profiles`

**User override**: Add unwanted profiles to skip list.

---

## Storage

Configuration stored in `marshal.json` under `extension_defaults`:

```json
{
  "extension_defaults": {
    "build.maven.profiles.skip": "itest,native",
    "build.maven.profiles.map.canonical": "local-integration-tests:integration-tests,perf:benchmark"
  }
}
```

**Key Formats**:
- `build.maven.profiles.skip` - Comma-separated profile IDs to exclude
- `build.maven.profiles.map.canonical` - Comma-separated `profile:canonical` pairs

Skip list and profile mappings are read during architecture discovery to classify profiles.

---

## Related Documents

| Document | Purpose |
|----------|---------|
| [maven-impl.md](../plan-marshall-plugin/standards/maven-impl.md) | Maven profile pipeline implementation |
| [canonical-commands.md](../../plan-marshall/skills/extension-api/standards/canonical-commands.md) | Command vocabulary |
