---
name: "heir-sync-management"
description: "Master-Heir synchronization, contamination prevention, and promotion workflows"
metadata:
  inheritance: master-only
---

# Heir Sync Management

> Safely synchronize cognitive architecture from Master to Heirs without contamination.

**Scope**: Master-only skill. Covers sync pipelines, PII protection, drift detection, skill promotion, and clean-slate distribution.

## Core Concepts

| Concept | Definition |
|---------|-----------|
| **Heir** | Platform-specific deployment inheriting Master's DNA (VS Code, M365, GitHub Copilot Web) |
| **Deployment Channel** | Delivery mechanism for an heir (Marketplace, Teams Package, `.github/` commit) |
| **Integration** | Cross-heir communication (OneDrive Sync, GitHub Cloud) |
| **Translation Heir** | Heir requiring format/schema conversion (e.g., M365 — export pipeline) |
| **Deployment Heir** | Heir needing only configuration, no code translation (e.g., GitHub Copilot Web — `.github/` files only) |
| **Contamination** | Master-specific data leaking into heir packages |
| **Drift** | Heir diverging from Master's architecture over time |
| **Promotion** | Elevating heir-developed capabilities back to Master |

**Rule**: Never confuse delivery mechanism with inheritance relationship — the "what" (identity/DNA) stays constant, only the "how" (delivery) varies.

## Sync Architecture

### What Gets Synced

The sync script (`sync-architecture.js`) copies these folders from Master `.github/` to Heir `.github/`:

| Folder | Content |
|--------|---------|
| `instructions/` | Procedural memory |
| `prompts/` | Episodic memory |
| `config/` | Configuration (with exclusions) |
| `agents/` | Agent definitions |
| `muscles/` | Execution scripts |
| `skills/` | Skills (filtered by inheritance) |

### What Must NEVER Sync

| Item | Why |
|------|-----|
| `user-profile.json` (real) | Contains personal name, email, preferences |
| `episodic/` memories | Session-specific to Master |
| Master-only skills | Only useful for managing the Master repo |
| API keys, PATs, secrets | Environment-specific credentials |
| Working memory with populated P5-P7 | Gives new users pre-filled slots instead of clean defaults |

## 3-Layer PII Protection

Every sync pipeline must implement three independent defense layers:

### Layer 1: Exclusion List

Files that are never copied, period:

```javascript
const EXCLUDED_CONFIG_FILES = [
  'user-profile.json',      // Personal data
  'MASTER-ALEX-PROTECTED.json', // Kill switch marker
  'goals.json',             // Session-specific
];
```

### Layer 2: Source File Sanitization

Scan all files being copied for hardcoded personal data:

| Pattern | Action |
|---------|--------|
| Real names in source headers | Replace with team/org name |
| Email addresses in code | Replace with placeholder |
| Personal names in `package.json` | Use organization name |
| Populated P5-P7 working memory slots | Reset to `*(available)*` |

**Rule**: Personal identity belongs ONLY in `user-profile.json`. All other files use team/org names.

### Layer 3: Pipeline Validation Gate

Post-copy regex scan that blocks packaging on violations:

| Check | Regex Example | On Match |
|-------|--------------|----------|
| Real name in files | `/\bFirstName\s+LastName\b/g` | EXIT 1 |
| Email addresses | `/[\w.-]+@[\w.-]+\.\w+/g` | EXIT 1 (except templates) |
| API keys | `/[A-Za-z0-9]{32,}/` in non-code files | WARNING |
| Populated P5-P7 | Check copilot-instructions Memory Stores | EXIT 1 |

**Anti-pattern**: Manual checklists. The copy function itself must be architecturally incapable of leaking.

## Clean Slate Distribution

### Template Generation

Simply excluding personal files leaves heirs without expected file structure. Generate fresh templates:

| File | Master Version | Heir Template |
|------|---------------|--------------|
| `user-profile.json` | Real user data | Empty with defaults + setup instructions |
| `copilot-instructions.md` | Populated P5-P7 | P5-P7 set to `*(available)*` |
| `goals.json` | Active session goals | Empty goals array |

### Post-Sync Reset Sequence

After copying files, apply these transformations:

1. **Reset environment-specific values** — P5-P7 slots, session state
2. **Generate template files** — Fresh starters with clear defaults
3. **Remove broken synapse references** — Master synapse IDs that don't exist in heir
4. **Validate file structure** — Ensure all expected files exist (even if empty templates)

## Drift Detection

### Pre-Release Checklist

Run these validations before every release:

| Check | Method | Fail Condition |
|-------|--------|---------------|
| Skill count match | Count Master inheritable vs Heir skills | Mismatch |
| File hash comparison | SHA256 of synced files | Divergence without override |
| Inheritance field validation | All skills have `inheritance` in synapses | Missing field |
| Orphan reference detection | Grep for files referenced but not present | Broken references |
| Config drift | Compare heir config against Master template | Unexpected values |

### Heir Configuration Drift Signals

| Signal | Indicates |
|--------|----------|
| Heir P5-P7 slots populated | Sync overwrote clean defaults |
| Heir has master-only skills | Exclusion filter not working |
| Heir synapse IDs don't resolve | Broken references from Master copy |
| Heir `package.json` has personal name | Sanitization missed |

## Leakage Prevention Patterns

### Master-Only Content Categories

Content that must NEVER sync to heirs falls into three categories:

| Category | Examples | Filter Method |
|----------|----------|---------------|
| **Skills** | heir-curation, master-alex-audit | `inheritance: "master-only"` in synapses.json |
| **Files** | ROADMAP-UNIFIED.md, alex_docs/architecture/ | Path-based filtering in sync script |
| **Metadata** | Complete trifecta count (9 vs 8), safety imperatives I1-I4 | Content transformation rules |

### Dual Filtering Strategy (2026-02-14 Fix)

**Problem**: `cleanBrokenSynapseReferences()` only filtered master-only **skills**, not master-only **files**.

**Solution**: Enhanced function with dual target detection:

```javascript
// Master-only skills (from inheritance metadata)
skippedMasterOnly.some(removed => target.includes(removed))

// Master-only files (hardcoded registry)
masterOnlyFiles.some(file => target.includes(file))
```

**Master-Only Files Registry**:
- `ROADMAP-UNIFIED.md` — Master development roadmap
- `alex_docs/architecture/` — Architecture documentation not deployed to heirs
- `MASTER-ALEX-PROTECTED.json` — Kill-switch marker

### Content Transformation Rules

Some content needs **adjustment** not **removal**:

| Content | Master Value | Heir Value | Transform Rule |
|---------|--------------|------------|----------------|
| Complete trifectas count | 9 | 8 | Remove heir-curation from list |
| Safety imperatives | I1-I7 | I5-I6 only | Strip I1-I4, I7 (master workspace protection) |
| Active Context Persona | Current session | Developer (85%) | Reset to default |
| Last Assessed | Date | never | Clear assessment timestamp |

**Implementation**: `applyHeirTransformations()` in sync-architecture.js

### Validation Cascade (4-Stage Quality Gate)

1. **Sync**: Copy files with skill/config exclusions
2. **Transform**: Apply heir-specific content adjustments
3. **Validate**: PII scan, master-only file detection
4. **Audit**: Count verification, synapse connection integrity

**Fail-Fast**: Any contamination detection halts the build (exit 1).

## Heir → Master Promotion

### 6-Step Promotion Workflow

| Step | Action | Output |
|------|--------|--------|
| 1. **Discover** | Review heir DK/skill files for portable knowledge | Candidate list |
| 2. **Create Skill** | Write SKILL.md in Master's `.github/skills/` | New skill file |
| 3. **Compare Gaps** | Diff heir knowledge against Master's existing coverage | Gap analysis |
| 4. **Implement** | Port patterns, translate code (Python→TS if needed) | Working code |
| 5. **Test** | Validate in Master context | Passing tests |
| 6. **Document** | CHANGELOG entry, ROADMAP update | Release-ready |

### Consolidation During Promotion

Heirs naturally create granular one-capability-per-skill files during experimentation. During promotion:

1. **Identify clusters** — Group related heir skills by domain
2. **Choose anchor skill** — Pick the broadest skill in the cluster
3. **Merge content** — Absorb related skills into the anchor
4. **Deduplicate** — Remove redundancy from the merge
5. **Mark inheritance** — Set the promoted skill as inheritable

**Anti-pattern**: Promoting every heir skill as-is without consolidation review causes skill sprawl.

### Code Translation Patterns (Heir → Master)

When porting from Python heirs to TypeScript Master:

| Python | TypeScript |
|--------|-----------|
| `dataclass` | `interface` |
| `raise Exception` | `throw new Error` |
| `**kwargs` | Optional config object |
| `async def` | `async function` |
| `try/except` | `try/catch` |

## Skill Inheritance Classification

### Curation Rule

Ask: "Is this skill ONLY useful for managing the Alex repo itself?"

| Answer | Classification | Example |
|--------|---------------|---------|
| Yes, master-repo only | `master-only` | release-preflight, heir-curation |
| No, any developer benefits | `inheritable` | deep-thinking, meditation, security-review |

### Truly Master-Only Skills (small list)

Only a few skills are genuinely master-only:

- `heir-curation` — Managing what heirs receive
- `heir-sync-management` — This skill
- `master-alex-audit` — Master workspace auditing
- `release-preflight` — Marketplace publishing
- `release-process` — Release pipeline

## Heir Type Comparison

| Heir | Type | Translation | Deploy Mechanism | Maintenance Cost |
|------|------|-------------|-----------------|------------------|
| **VS Code Extension** | Source | Compile only | `npx vsce publish` | Low |
| **M365 Copilot Agent** | Translation | Full export/schema mapping | Teams Developer Portal | High |
| **GitHub Copilot Web** | Deployment | None (`.github/` files only) | `git commit` + push | Very Low |

Everything else should be inheritable unless it references Master-specific file paths or workflows.

## Heir-Specific Positioning

Each platform heir must position against its **native competitor**, not a generic category:

| Heir | Compares Against | Not Against |
|------|-----------------|-------------|
| VS Code Extension | GitHub Copilot (native) | "AI assistants" generically |
| M365 Agent | Microsoft 365 Copilot | "AI assistants" generically |
| GitHub Copilot Web | GitHub Copilot (untuned) | "AI assistants" generically |

Store descriptions, README headers, and comparison tables must use platform-specific language and keywords.

## Release Pipeline Integration

The release script must enforce sync before packaging:

1. Run `sync-architecture.js` (copies Master → Heir)
2. Apply post-sync transformations (clean slate)
3. Run PII validation gate (blocks on contamination)
4. Check `BUILD-MANIFEST.json` timestamp (prevents stale packaging)
5. Package and publish

**Rule**: It must be impossible to publish stale content through the official release process.
