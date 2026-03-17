---
name: ecosystem-health
description: Analyzes Claude Code ecosystem health by tracking all 27 extensibility components across 6 tiers - including plugin components, core configuration, environment/CLI, authentication, session features, and integrations. Use when checking if Claude Code components are up-to-date, orchestrating audits efficiently, tracking documentation coverage, applying updates from new Claude Code versions, or getting an overview of ecosystem component staleness.
user-invocable: false
allowed-tools: Read, Write, Glob, Grep, Skill
---

# Ecosystem Health

## MANDATORY: docs-management Delegation

> **CRITICAL:** This skill follows the anti-duplication principle. **ALL component details MUST be queried from docs-management at runtime.**

### What This Skill Hardcodes (Static - Changes Rarely)

| Data | Why Static |
| ---- | ---------- |
| Tier structure (1-6) | Design decision, architectural choice |
| Audit commands (`/audit-*`) | OUR commands in claude-ecosystem plugin |
| Audit types (automated/manual/documentation) | Classification policy |
| Scoring/prioritization logic | Policy decisions |

### What MUST Be Delegated (Dynamic - Changes With Releases)

| Data | Why Dynamic | How to Get |
| ---- | ----------- | ---------- |
| CLI flags list | New flags every release | Query: `docs-management: cli-reference.md CLI flags` |
| Environment variables | New env vars frequently | Query: `docs-management: settings.md environment variables` |
| Authentication methods | New providers added | Query: `docs-management: iam.md authentication methods` |
| Permission modes | Modes evolve | Query: `docs-management: iam.md permission modes` |
| Cloud providers | New providers added | Query: `docs-management: setup.md cloud providers` |
| IDE integrations | New integrations added | Query: `docs-management: third-party-integrations.md IDE` |
| Change keywords | Terminology evolves | Derive from docs-management index keywords |
| File patterns | Locations can change | Query official docs for current patterns |

### Delegation Rules

1. **NEVER use hardcoded lists** for CLI flags, env vars, auth methods, cloud providers, IDE integrations, permission modes, or any frequently-changing data
2. **ALWAYS query docs-management** when you need component details
3. **Use claude-code-guide agent** for live verification during `--discover` and `--check` modes
4. **If docs-management returns empty**, that's a signal to check if the component still exists

### Query Patterns for docs-management

```text
# Tier 3: Environment & CLI
"cli-reference.md CLI flags"              → Get current CLI flags list
"settings.md environment variables"       → Get current env vars list
"iam.md permission modes"                 → Get current permission modes

# Tier 4: Authentication & Access
"iam.md authentication methods"           → Get current auth methods
"iam.md configuring permissions"          → Get permission rule patterns
"iam.md credential management"            → Get credential features

# Tier 5: Session & Runtime
"cli-reference.md session features"       → Get session features (resume, checkpoints)
"security.md sandbox configuration"       → Get sandbox settings

# Tier 6: Integration
"third-party-integrations.md IDE"         → Get IDE integrations list
"setup.md cloud providers"                → Get cloud provider list
"common-workflows.md CI/CD"               → Get CI/CD platforms

# Changelog for change categorization
"CHANGELOG recent changes"                → Get changelog entries
```

---

## Overview

This skill tracks Claude Code ecosystem health across **ALL extensibility points** - not just plugin components. It monitors **27 component types** across **6 tiers**.

**Schema v2.2** introduces the **Tiered Validation Model** for changelog-triggered audit staleness:

- **Minor changes** (features, deprecations) → Targeted keyword validation (cheap)
- **Major changes** (behavior_change, security) → Full audit required (no shortcuts)
- **Bugfixes** → No validation needed

This approach provides **60-96% token savings** while maintaining strict accuracy requirements.

### Component Tiers

| Tier | Category | Components | Audit Type | Description |
| ---- | -------- | ---------- | ---------- | ----------- |
| 1 | Core Configuration | 4 | Mixed | User, project, and enterprise settings |
| 2 | Plugin Components | 12 | Automated | Components packaged in plugins |
| 3 | Environment & CLI | 3 | Documentation | Env vars, CLI flags, permission modes |
| 4 | Authentication & Access | 3 | Mixed | Auth methods, permission rules |
| 5 | Session & Runtime | 2 | Mixed | Session features, sandbox config |
| 6 | Integration | 3 | Documentation | IDEs, cloud providers, CI/CD |

### Audit Types Explained

| Type | Description | Has Audit Command? | Tracking Method |
| ---- | ----------- | ------------------ | --------------- |
| `automated` | Full audit via `/audit-*` | Yes | Pass rate, component count |
| `manual` | Requires human review | No | Human review tracking |
| `documentation` | Tracks doc coverage only | No | Doc coverage via docs-management queries |

---

## Tiered Validation Model (v2.2)

Schema v2.2 introduces a **three-tier validation model** that automatically invalidates audits when changelog changes affect components, while using the most token-efficient validation method appropriate for each change type.

### Change Severity Classification

| Change Type | Severity | Validation Requirement | Rationale |
| ----------- | -------- | ---------------------- | --------- |
| `feature` | Minor | Targeted validation (keyword check) | New features can be verified by checking keywords exist |
| `deprecation` | Minor | Targeted validation (keyword check) | Deprecations can be verified by checking warnings documented |
| `bugfix` | None | No validation needed | Bugfixes don't affect plugin documentation/compliance |
| `behavior_change` | **Major** | **Full audit required** | Behavior changes may have wide-ranging impacts |
| `security` | **Major** | **Full audit required** | Security changes require comprehensive review |

### Validation Tiers

#### Tier 1: Targeted Validation (Minor Changes)

For `feature` and `deprecation` changes:

- **Method:** Grep-based keyword verification
- **Evidence:** File path, line number, matched text
- **Cost:** ~100-500 tokens per change
- **Status on pass:** `VALIDATED`

**Algorithm:**

```text
1. Load validation spec from granular_changelog change entry
2. For each keyword in validation.keywords:
   a. Run grep against target_skill directory
   b. If match found, record evidence (file, line, match text)
3. If matches >= required_matches:
   a. Set validation_result.validated = true
   b. Set confidence based on match count:
      - 1 match = "medium"
      - 2+ matches = "high"
4. Update component_coverage validation tracking
```

#### Tier 2: Full Audit (Major Changes)

For `behavior_change` and `security` changes:

- **Method:** Spawns auditor agent(s)
- **Audit command:** Specified in validation.audit_command
- **Cost:** ~3,000-8,000 tokens
- **Status on pass:** `AUDITED`

**Important:** Major changes **cannot** be validated via targeted validation. The system must enforce this - no shortcuts.

#### Tier 3: Periodic Review

Regardless of validation status:

- **Threshold:** >90 days since last full audit
- **Action:** Triggers full audit
- **Rationale:** Ensures nothing drifts over time

### Validation Spec Schema (v2.2)

Each change in `granular_changelog` can have a validation spec:

```yaml
validation:
  method: "keyword_check"           # keyword_check | full_audit | manual | none
  target_skill: "hook-management"   # Which skill to validate (null for memory files)
  keywords:                         # Manual list - NEVER auto-extracted
    - "additionalContext"
    - "additional context"
    - "PreToolUse.*additionalContext"  # Regex supported
  required_matches: 1               # How many keywords must match
  reason: "..."                     # Optional explanation (esp. for method: none)

# For full_audit method:
validation:
  method: "full_audit"
  target_skill: "permission-management"
  audit_command: "/audit-settings"
  reason: "Security fix - targeted validation insufficient"
```

### Validation Result Schema

After validation runs, results are recorded:

```yaml
validation_result:
  validated: true                   # Did validation pass?
  validated_date: "2026-01-16"      # When validated
  evidence:                         # For keyword_check method
    - file: "path/to/file.md"
      line: 142
      match: "matched text"
  audit_performed: true             # For full_audit method
  audit_date: "2026-01-12"          # When audit was run
  confidence: "high"                # high | medium | low
```

### Status Calculation (Conservative)

Component status is determined by this priority order (first match wins):

| Priority | Condition | Status |
| -------- | --------- | ------ |
| 1 | Has `pending_major_changes` | `NEEDS AUDIT` ⚠️ |
| 2 | Has `pending_minor_changes` | `NEEDS VALIDATION` |
| 3 | `days_since(last_audit) > 90` | `STALE` |
| 4 | `validation_version == latest AND validation_confidence == "high"` | `VALIDATED` |
| 5 | `last_audit` recent AND no pending changes | `OK` |
| 6 | Never audited | `UNKNOWN` |

**Conservative Rule:** If ANY doubt exists, escalate to higher requirement.

---

## Validation Accuracy Rules (CRITICAL)

The system must **NEVER** report "validated" unless certain. These rules are non-negotiable.

### Rule 1: Keyword Matches Must Be Contextually Correct

```text
❌ Finding "context" when looking for "context: fork" is NOT a match
✅ Must match exact keyword or regex pattern
```

### Rule 2: Multiple Evidence Preferred

| Evidence Count | Confidence Level |
| -------------- | ---------------- |
| 0 matches | `validation_failed: true` |
| 1 match | `confidence: "medium"` |
| 2+ matches | `confidence: "high"` |

### Rule 3: Human Confirmation for Edge Cases

If confidence is `"low"`:

- Flag for manual review
- Do NOT auto-mark as validated
- Include in `--apply` output for user decision

### Rule 4: Evidence is Mandatory

- No validation without captured evidence
- Evidence must include file path and line number
- Empty evidence = validation failed

### Rule 5: Major Changes Cannot Use Targeted Validation

```text
❌ security change → keyword_check (FORBIDDEN)
❌ behavior_change → keyword_check (FORBIDDEN)
✅ security change → full_audit (REQUIRED)
✅ behavior_change → full_audit (REQUIRED)
```

The system must reject attempts to use targeted validation for major changes.

The skill provides:

1. **Parsing changelogs** to identify new features and changes
2. **Tracking audit coverage** across all 27 component types
3. **Documentation coverage** for non-auditable components (queried from docs-management)
4. **Identifying pending updates** needed for compliance
5. **Orchestrating audits** efficiently (avoiding token waste)
6. **Helping apply updates** from new Claude Code versions

## When to Use This Skill

Use this skill when:

- Checking if ANY Claude Code extensibility component is up-to-date
- Getting an overview of audit coverage and staleness across all tiers
- Tracking documentation coverage for non-auditable components
- Planning which audits to run (token-efficient approach)
- Applying updates after Claude Code releases new versions
- Preparing a plugin release
- Detecting new/deprecated Claude Code features

## Tracking File

**Location:** `.claude/ecosystem-health.yaml`

This file persists ecosystem health state across sessions. It stores **audit metadata ONLY** - not component details (which are delegated to docs-management).

**Schema v2.1 Structure:**

```yaml
schema_version: "2.1"

last_check:
  date: "YYYY-MM-DD"
  claude_code_version: "X.Y.Z"
  changelog_hash: "sha256:..."

component_coverage:
  # Tier 1: Core Configuration
  tier1_configuration:
    user_settings:
      last_audit: null
      components_audited: 0
      pass_rate: null
      audit_type: "manual"
      # Query docs-management for: settings.md user configuration
    project_settings:
      last_audit: "YYYY-MM-DD"
      components_audited: N
      pass_rate: 0.XX
      audit_type: "automated"
      audit_command: "/audit-settings"
    managed_settings: { ... }
    memory_system: { ... }

  # Tier 2: Plugin Components (12 components)
  tier2_plugins:
    skills: { audit_type: "automated", audit_command: "/audit-skills" }
    agents: { audit_type: "automated", audit_command: "/audit-agents" }
    # ... (12 components, each with audit_type and audit_command)

  # Tier 3-6: Documentation-tracked (DELEGATE to docs-management)
  tier3_environment:
    environment_variables:
      audit_type: "documentation"
      # DELEGATE: Query docs-management for: settings.md environment variables
    cli_flags: { ... }
    permission_modes: { ... }

  tier4_authentication: { ... }
  tier5_session: { ... }
  tier6_integration: { ... }

changelog_versions_checked:
  - version: "X.Y.Z"
    checked_date: "YYYY-MM-DD"
    changes_applied: true/false

pending_updates:
  - feature: "feature name"
    since_version: "X.Y.Z"
    affects: ["skills", "commands"]
    status: "pending" | "applied" | "skipped"

last_discovery:
  date: "YYYY-MM-DD"
  docs_scanned: [...]
  changelog_version: "X.Y.Z"
  components_detected: 27
  tiers_scanned: 6
  gaps_found: 0
```

**Key Design Decision:** The tracking file does NOT contain `tracked_*` arrays (no hardcoded lists of env vars, CLI flags, auth methods, etc.). All such data must be queried from docs-management at runtime.

## Changelog Access

**MANDATORY:** Access changelog via `docs-management` skill.

**Doc ID:** `raw-githubusercontent-com-anthropics-claude-code-refs-heads-main-CHANGELOG`

**Access pattern:**

```bash
python plugins/claude-ecosystem/skills/docs-management/scripts/core/find_docs.py \
  content raw-githubusercontent-com-anthropics-claude-code-refs-heads-main-CHANGELOG
```

### Version Extraction

Parse changelog for version entries:

```text
Pattern: ^##\s*\[?(\d+\.\d+\.\d+)\]?
Examples:
  "## 2.1.3" → version 2.1.3
  "## [2.1.0]" → version 2.1.0
```

## Change Categorization

Map changelog keywords to component types across all 6 tiers.

**IMPORTANT:** Do NOT use hardcoded keyword lists. Query docs-management for current keywords via the index, then match changelog entries against those keywords.

### Categorization Algorithm

1. Query docs-management index for keyword lists by doc section
2. For each changelog entry:
   a. Match against keywords from relevant doc sections
   b. Assign to tier(s) based on which docs matched
   c. Record affected components

### Tier-to-Doc Mapping

| Tier | Components | Query docs-management for |
| ---- | ---------- | ------------------------- |
| 1 | user_settings, project_settings, managed_settings, memory_system | settings.md, iam.md, memory.md |
| 2 | skills, agents, commands, hooks, mcp, memory, plugins, settings, output_styles, statuslines, rules, lsp | skills.md, sub-agents.md, slash-commands.md, hooks.md, mcp.md, memory.md, plugins-reference.md, terminal-config.md |
| 3 | environment_variables, cli_flags, permission_modes | settings.md, cli-reference.md, iam.md |
| 4 | authentication_methods, permission_rules, credential_management | iam.md |
| 5 | session_features, sandbox_configuration | cli-reference.md, security.md |
| 6 | ide_integrations, cloud_providers, cicd_integrations | third-party-integrations.md, setup.md, common-workflows.md |

For detailed categorization patterns, see [references/change-categories.md](references/change-categories.md).

## Modes of Operation

### Status Mode (Default / --status)

Shows current ecosystem health without running audits. Displays all 6 tiers.

**Algorithm:**

1. Load tracking file (or show "never checked" if missing)
2. Read audit data for each component in all 6 tiers
3. Calculate staleness (days since last audit/review)
4. Show summary tables by tier with recommendations

### Check Mode (--check)

Compares current changelog against last check. Identifies changes across all tiers.

**Algorithm:**

1. Load tracking file
2. Fetch changelog via docs-management
3. Compute changelog hash
4. If hash differs from tracked hash:
   a. Parse new versions since last check
   b. **Query docs-management for current keyword mappings**
   c. Categorize changes by tier
   d. Add to pending_updates with tier info
5. **Spawn claude-code-guide agent** for live verification of new features
6. Update tracking file
7. Report findings by tier

### Audit Mode (--audit [type])

Runs audits intelligently. Only applies to Tier 2 components (automated audits).

**Without type argument:** Audits all stale/never-audited Tier 2 components
**With type argument:** Audits only specified type

**Priority Order:**

1. Never audited (Priority 1)
2. Affected by recent changelog changes (Priority 2)
3. Stale >90 days (Priority 3)

**Batching:**

- Max 3 audits per batch
- Present results between batches
- Allow user to continue or stop

**Audit Command Mapping (Tier 2 Only):**

| Component | Audit Command |
| --------- | ------------- |
| skills | `/audit-skills` |
| agents | `/audit-agents` |
| commands | `/audit-commands` |
| hooks | `/audit-hooks` |
| mcp | `/audit-mcp` |
| memory | `/audit-memory` |
| plugins | `/audit-plugins` |
| settings | `/audit-settings` |
| output_styles | `/audit-output-styles` |
| statuslines | `/audit-statuslines` |
| rules | `/audit-rules` |
| lsp | `/audit-lsp` |

**Compliance Audits (Cross-Cutting):**

| Audit Type | Audit Command | Description |
| ---------- | ------------- | ----------- |
| docs-delegation | `/audit-docs-delegation` | Audits skills and memory files for proper docs-management delegation patterns |
| agent-consolidation | `/audit-agent-consolidation` | Analyzes agents for consolidation opportunities, groups by config, tracks references |

### Doc Coverage Mode (--doc-coverage)

Tracks documentation coverage for non-auditable components (Tiers 3-6).

**Algorithm:**

1. Load tracking file
2. For each documentation-tracked component:
   a. **Query docs-management** for official doc section
   b. Extract current feature list from doc content
   c. Report coverage status
3. **No hardcoded lists** - all data comes from docs-management queries

**Note:** Coverage is always based on current docs-management content. There's no "tracked list" to compare against - docs-management IS the source of truth.

### Apply Mode (--apply)

Interactive mode to apply pending updates.

**For each pending update:**

1. Show what changed in Claude Code
2. Show affected tiers
3. Load relevant development skill
4. Search codebase for affected patterns
5. Present affected files
6. Ask user for action:
   - Show detailed changes
   - Apply changes automatically
   - Skip this update
   - Mark as already applied

### Since Mode (--since <version>)

Shows all changes since a specific version, organized by tier.

**Algorithm:**

1. Fetch changelog
2. Parse entries from specified version to current
3. **Query docs-management for keyword mappings**
4. Categorize all changes by tier
5. Present summary by tier

### Overlap Mode (--overlap)

Detects plugin overlaps, redundancy, and consolidation opportunities.

**Algorithm:**

1. **Enumerate all plugins:**
   - Glob all `plugins/*/` directories
   - Read each plugin's manifest and README

2. **Extract component names:**
   - For each plugin, extract skill names from `skills/*/SKILL.md`
   - Extract command names from `commands/*.md`
   - Extract agent names from `agents/*.md`

3. **Detect duplicates:**
   - Find skill names that appear in multiple plugins
   - Find command names that appear in multiple plugins
   - Find agent names that appear in multiple plugins

4. **Semantic overlap analysis:**
   - Compare plugin descriptions for >70% semantic similarity
   - Compare skill descriptions within same domain
   - Flag plugins covering same methodology

5. **Published standard detection:**
   - For each plugin, check if methodology is a published standard
   - Query perplexity: "Is {methodology} a published standard?"
   - Published standards: ISO 25010, CRISP-DM, BABOK, Kimball, Design Thinking, TOGAF, WCAG, etc.
   - Flag plugins that ONLY wrap published standards with no unique value

6. **Generate overlap report:**

```markdown
## Plugin Overlap Analysis

**Duplicate Components Found:**

| Component | Type | Plugins |
| --------- | ---- | ------- |
| adr-management | skill | enterprise-architecture, documentation-standards |
| journey-mapping | skill | business-analysis, requirements-elicitation |

**Semantic Overlaps:**

| Plugin A | Plugin B | Overlap % | Domain | Status |
| -------- | -------- | --------- | ------ | ------ |
| ~~contract-testing~~ | test-strategy | 85% | Testing | ✅ CONSOLIDATED (v2.0) |
| ~~observability-planning~~ | ~~quality-attributes~~ | 70% | NFRs | ✅ BOTH REMOVED (v2.0) |

**Published Standard Plugins (Consolidation Candidates):**

| Plugin | Methodology | Standard Type | Recommendation | Status |
| ------ | ----------- | ------------- | -------------- | ------ |
| ~~quality-attributes~~ | ISO 25010 | International Standard | REMOVE | ✅ REMOVED (v2.0) |
| ~~ai-ml-planning~~ | CRISP-DM | Industry Framework | REMOVE | ✅ REMOVED (v2.0) |
| ~~data-architecture~~ | Kimball | Published Methodology | REMOVE | ✅ REMOVED (v2.0) |

**Consolidation Completed (v2.0):**

1. **~~contract-testing~~ → test-strategy** - DONE: `compatibility-analyzer` agent moved
2. **8 published standard plugins** - REMOVED: MCP research replaces them
3. **content-management-system** - KEPT: unique composition patterns
```

7. **Update tracking file:**
   - Record overlap analysis date
   - Store consolidation recommendations
   - Track which overlaps have been resolved

**Overlap Status in ecosystem-health.yaml:**

```yaml
plugin_overlap:
  last_analysis: "2026-01-17"
  total_plugins: 35
  duplicate_components:
    - component: "adr-management"
      type: "skill"
      plugins: ["enterprise-architecture", "documentation-standards"]
      resolution: "pending" | "resolved" | "intentional"
  published_standard_plugins:
    - plugin: "quality-attributes"
      methodology: "ISO 25010"
      recommendation: "remove"
      status: "pending" | "removed" | "kept_with_justification"
  consolidation_candidates:
    - source: "contract-testing"
      target: "test-strategy"
      assets_moved: ["compatibility-analyzer agent"]
      status: "completed"  # v2.0 consolidation
```

### Discover Mode (--discover)

Scans official documentation to detect ecosystem drift across ALL 6 tiers.

**Algorithm:**

1. **Query docs-management** for ALL relevant doc sections:
   - Tier 1: settings.md, iam.md, memory.md
   - Tier 2: plugins-reference.md, skills.md, hooks.md, etc.
   - Tier 3: settings.md#environment-variables, cli-reference.md, iam.md#permission-modes
   - Tier 4: iam.md#authentication-methods, iam.md#configuring-permissions
   - Tier 5: cli-reference.md, security.md
   - Tier 6: third-party-integrations.md, setup.md, common-workflows.md

2. **Spawn claude-code-guide agent** for live web verification of:
   - Recent changelog entries
   - New feature announcements
   - Deprecated features

3. Build detected components list by tier:
   - Extract features from docs-management responses
   - Compare to tracked component types (27 total)
   - Identify gaps

4. Report findings with evidence:
   - Show doc_id or changelog version as source
   - Provide recommendation (add tracking, update name, merge)
   - Indicate affected tier

## Quick Decision Tree

**What do you want to do?**

1. **Get overview of all Claude Code extensibility** → Use Status Mode (default)
2. **Check for Claude Code updates** → Use Check Mode (`--check`)
3. **Run audits for Tier 2 plugin components** → Use Audit Mode (`--audit`)
4. **Check documentation coverage for Tiers 3-6** → Use Doc Coverage Mode (`--doc-coverage`)
5. **Apply pending updates** → Use Apply Mode (`--apply`)
6. **See changes since version X** → Use Since Mode (`--since X.Y.Z`)
7. **Detect plugin overlaps and redundancy** → Use Overlap Mode (`--overlap`)
8. **Check for new/changed components in any tier** → Use Discover Mode (`--discover`)

## Delegation Pattern

This skill delegates to specialized skills for domain-specific guidance:

```text
ecosystem-health
    ├── docs-management (MANDATORY - changelog, official docs for all tiers)
    ├── claude-code-guide (live verification during --discover and --check)
    │
    ├── Tier 1 & 2 - Settings/Memory
    │   ├── settings-management
    │   └── memory-management
    │
    ├── Tier 2 - Plugin Components
    │   ├── skill-development
    │   ├── subagent-development
    │   ├── command-development
    │   ├── hook-management
    │   ├── mcp-integration
    │   ├── plugin-development
    │   ├── output-customization
    │   └── status-line-customization
    │
    ├── Tier 3-4 - Auth/Environment
    │   ├── settings-management
    │   ├── permission-management
    │   └── enterprise-security
    │
    ├── Tier 5 - Session/Runtime
    │   └── sandbox-configuration
    │
    └── Tier 6 - Integration (documentation tracking only)
```

## Token Efficiency

**Goal:** Minimize tokens while maintaining coverage.

**Strategies:**

1. Skip recently-audited components (use tracking file)
2. Prioritize by changelog impact (audit what changed)
3. Batch audits (max 3 at a time)
4. Progressive disclosure (load references only when needed)
5. Delegate to docs-management (no local caches to maintain)
6. Use claude-code-guide only when live verification needed

**Expected savings:** 60-80% compared to running all audits blindly.

## Schema Migration

The skill handles migration between schema versions:

**v1.0 → v2.0:** Tiered organization
**v2.0 → v2.1:** Delegation pattern (remove hardcoded lists)

Migration algorithm:

1. Detects schema version
2. Creates backup at `.claude/ecosystem-health.yaml.backup`
3. Preserves existing audit data (last_audit, pass_rate, components_audited)
4. Removes deprecated fields (tracked_*, file_patterns)
5. Writes new schema version

## References

For detailed implementation guidance:

- **Changelog Parsing:** See [references/changelog-parsing.md](references/changelog-parsing.md)
- **Change Categories:** See [references/change-categories.md](references/change-categories.md)
- **Audit Orchestration:** See [references/audit-orchestration.md](references/audit-orchestration.md)
- **Component Discovery:** See [references/component-discovery.md](references/component-discovery.md)
- **Delegation Detection:** See [references/delegation-detection.md](references/delegation-detection.md)

## Related Skills

| Skill | Relationship |
| ----- | ------------ |
| `docs-management` | **MANDATORY** - Primary source for ALL dynamic data |
| `claude-code-guide` | Live verification for --discover and --check modes |
| `skill-development` | Skills validation and guidance |
| `subagent-development` | Agents validation and guidance |
| `command-development` | Commands validation and guidance |
| `settings-management` | Settings guidance |
| All other `*-development` skills | Domain-specific validation |

## Test Scenarios

### Scenario 1: First Run

**Query:** `/ecosystem-health`
**Expected:** Creates tracking file with v2.1 schema, shows "never checked" status for all tiers
**Success:** Tracking file created, 27 components displayed across 6 tiers, NO hardcoded lists in file

### Scenario 2: Check for Updates (with Delegation)

**Query:** `/ecosystem-health --check`
**Expected:**

1. Fetches changelog via docs-management
2. Queries docs-management for keyword mappings
3. Spawns claude-code-guide for live verification
4. Reports new versions by tier
**Success:** Updates detected with evidence from docs-management, not hardcoded assumptions

### Scenario 3: Smart Audit (Tier 2)

**Query:** `/ecosystem-health --audit`
**Expected:** Audits only stale/never-audited Tier 2 components
**Success:** Targeted audits run, tracking file updated (audit metadata only)

### Scenario 4: Documentation Coverage (Delegated)

**Query:** `/ecosystem-health --doc-coverage`
**Expected:**

1. Queries docs-management for each Tier 3-6 doc section
2. Reports coverage based on current docs content
3. NO comparison against hardcoded lists
**Success:** Coverage reported from live docs-management queries

### Scenario 5: Component Discovery (with claude-code-guide)

**Query:** `/ecosystem-health --discover`
**Expected:**

1. Queries docs-management for ALL tier doc sections
2. Spawns claude-code-guide for live web verification
3. Reports gaps with evidence from both sources
**Success:** Discovery report generated with dual-source verification

## Version History

- v2.3.0 (2026-01-17): Plugin Overlap Detection
  - Added `--overlap` mode for detecting plugin redundancy and consolidation opportunities
  - Detects duplicate skill/command/agent names across plugins
  - Semantic overlap analysis for plugin descriptions
  - Published standard detection (ISO 25010, CRISP-DM, BABOK, etc.)
  - Consolidation recommendations with tracking in ecosystem-health.yaml
  - Integration with new audit scoring categories (Plugin Boundaries, Published Standard Test, Plugin Necessity)

- v2.2.0 (2026-01-16): Tiered Validation Model
  - Added changelog-triggered audit staleness with automatic invalidation
  - Three-tier validation: Minor (keyword) → Major (full audit) → Periodic
  - Change severity classification: feature/deprecation=minor, behavior_change/security=major
  - Validation spec schema with keywords, required_matches, evidence capture
  - Strict accuracy rules (never report "valid" unless certain)
  - Dual tracking in component_coverage (audit + validation)
  - New modes: `--validate` (read-only check), `--audit-required` (shows only major changes)
  - Enhanced status display with VALIDATED, NEEDS VALIDATION, NEEDS AUDIT states
  - Token cost reduction: 60-96% for typical workflows
  - Schema v2.2 with validation fields and confidence tracking

- v2.1.0 (2026-01-10): Delegation pattern
  - Removed ALL hardcoded lists (tracked_*, file_patterns)
  - Added MANDATORY docs-management delegation section
  - Added claude-code-guide integration for live verification
  - Schema v2.1 with audit-data-only tracking file
  - Anti-duplication compliance

- v2.0.0 (2026-01-10): Expanded to ALL Claude Code extensibility points
  - 27 component types across 6 tiers (up from 12 plugin components)
  - New schema version (v2.0) with tiered organization
  - Added doc-coverage mode for non-auditable components
  - Discover mode now scans all 6 tiers
  - Automatic schema migration from v1.0

- v1.1.0 (2026-01-10): Added discover mode
  - Self-audit capability for component drift detection
  - Scans official docs for new/deprecated components
  - Reports gaps with evidence and recommendations

- v1.0.0 (2026-01-10): Initial release
  - Status, check, audit, apply, and since modes
  - Tracking file persistence
  - Changelog parsing and categorization
  - Smart audit prioritization

---

## Last Updated

**Date:** 2026-01-17
**Model:** claude-opus-4-5-20251101
