---
name: 70-02-concern-ownership-audit
description: Find split ownership — the same concept defined in multiple files, with duplicate types, shadow constants, orphaned loaders, and zombie exports. Use when codebase feels tangled, after major refactors, or when you find code that looks alive but nothing imports it.
---

# 70.02 Concern Ownership Audit

Find and fix **split ownership** — where a single domain concept is spread across multiple files, creating dead code, duplicate definitions, and confusion about what's canonical.

## The Problem

Refactors create new canonical homes for concepts but leave the old definitions in place. The consumer gets wired to the new code. The old code compiles, looks alive, but nothing imports it. Over time:

- Nobody knows which file owns the concept
- Old definitions drift from the canonical version
- New agents read the dead code and build on top of it
- The codebase accumulates weight that serves no purpose

This is NOT copy-paste duplication (grep finds that). This is the same *concern* — types, constants, loaders, helpers — defined in two places where only one is actually used.

## Anti-Patterns

### 1. Split Concern

The same domain concept defined in multiple files with different names.

**Real example — planet textures in trek:**

```
planet-shaders.ts:
  PlanetTextureType = "terrestrial" | "gas-giant" | "ice" | ...
  ALBEDO_TEXTURES: Record<PlanetTextureType, string[]>
  TEXTURE_BASE = "/textures/planets/"
  loadTexture(), textureCache, generatePlanetTextures()

planet-types.ts:
  PlanetType = "terrestrial" | "gas-giant" | "ice" | ...    ← same enum, different name
  TEXTURES = { terrain: [...], gasGiant: [...], ... }        ← same file lists, different shape
  TEXTURE_BASE = "/textures/planets/"                        ← identical constant
  getTexturePath(), pickRandomTexture()                      ← replacement helpers

planet.ts (consumer):
  imports from planet-types.ts                               ← only this is wired
  has its OWN loadTexture() and textureCache                 ← third copy of the loader
```

Three files, one concern. `planet-types.ts` was the clean replacement but the old code in `planet-shaders.ts` was never removed, and the loader got duplicated into the consumer.

**Detection pattern:**

```bash
# Same constant name or value in multiple files
rg -n 'TEXTURE_BASE|"/textures/planets/"' --glob '*.ts'

# Same type shape with different names
rg -n 'terrestrial.*gas-giant.*ice' --glob '*.ts'

# Same utility function in multiple files
rg -n 'function loadTexture|const textureLoader' --glob '*.ts'
```

### 2. Shadow Definitions

Types or interfaces that describe the same shape but with different names, often in different layers.

```
# Symptom: two interfaces that overlap 80%+
shaders/planet-shaders.ts:  interface PlanetMaterialOptions { albedoMap, bumpMap, ... }
entities/planet/planet-types.ts:  interface PlanetPreset { textures, hasBumpMap, ... }
```

One describes what the shader needs, the other describes what the preset provides. But shared fields (wavelengths, atmosphereColor, shininess) are defined in both with identical semantics.

**Detection pattern:**

```bash
# Interfaces with overlapping field names
rg -n 'interface.*Planet' --glob '*.ts'
# Then compare fields manually
```

### 3. Orphaned Infrastructure

Loading, caching, or utility code left behind after a refactor wired a new path. The infrastructure compiled but nothing reaches it.

```
# Old path (dead):
planet-shaders.ts: textureLoader → textureCache → loadTexture() → generatePlanetTextures()

# New path (alive):
planet-types.ts: getTexturePath() → planet.ts: loadTexture() → THREE.TextureLoader
```

The entire old loading chain is dead — but it looks like production code because it's well-written and exported.

**Detection pattern:**

```bash
# Exported symbols with zero external imports
# For each export in a file, check if anything imports it
rg -n '^export ' src/rendering/shaders/planet-shaders.ts
# Then for each symbol:
rg -n 'generatePlanetTextures' --glob '*.ts' --glob '*.tsx'
# If results are ONLY in the defining file → dead
```

### 4. Zombie Exports

Symbols that are `export`ed but imported by nobody. They inflate the API surface and confuse agents into thinking they're part of the contract.

**Detection pattern:**

```bash
# List all exports from a file
rg -n '^export (function|class|interface|type|const|enum)' <file>

# For each exported name, search for imports
rg -n '<symbol-name>' --glob '*.ts' --glob '*.tsx' | grep -v '<defining-file>'
```

## Process

### Phase 1: Automated Scan

Run these scans across the codebase (or scoped to a directory). Collect raw signals.

```bash
SCOPE="src/"  # adjust to target

# 1. Duplicate constants — same value in multiple files
rg -n 'const [A-Z_]+ =' $SCOPE --glob '*.ts' | \
  sed 's/.*const \([A-Z_]*\) =.*/\1/' | sort | uniq -c | sort -rn | \
  awk '$1 > 1'

# 2. Duplicate type names — same concept, possibly different names
rg -n '^export (type|interface|enum) ' $SCOPE --glob '*.ts' | \
  sed 's/.*export \(type\|interface\|enum\) \([A-Za-z]*\).*/\2/' | sort

# 3. Same function name in multiple files
rg -n '^export function |^function ' $SCOPE --glob '*.ts' | \
  sed 's/.*function \([a-zA-Z]*\).*/\1/' | sort | uniq -c | sort -rn | \
  awk '$1 > 1'

# 4. Zombie exports — find candidates
# (For each file with exports, check which exports have zero external importers)
```

### Phase 2: Manual Triage

For each signal from Phase 1:

1. **Read both definitions** — are they the same concern or intentional variants?
2. **Trace the consumers** — who imports what? (`rg -n 'from.*<module>'`)
3. **Identify the canonical home** — which file SHOULD own this concept based on the architecture?
4. **Classify:**
   - `DEAD` — exported but zero importers. Delete.
   - `SPLIT` — same concern, two homes. Consolidate into the canonical one.
   - `SHADOW` — overlapping types. Merge or create a shared base.
   - `INTENTIONAL` — looks like duplication but serves different layers. Document why.

### Phase 3: Report

Create a ticket with findings:

```
tk create "Concern ownership audit: <scope>" -t task --tags code-quality,ownership-audit
```

Ticket body structure:

```markdown
## Findings

### DEAD (safe to delete)
| Symbol | File | Evidence |
|--------|------|----------|
| `generatePlanetTextures` | planet-shaders.ts | 0 importers outside defining file |

### SPLIT (consolidate)
| Concern | File A | File B | Canonical Home | Action |
|---------|--------|--------|----------------|--------|
| Planet texture paths | planet-shaders.ts | planet-types.ts | planet-types.ts | Move loader, delete old |

### SHADOW (merge types)
| Type A | Type B | Overlap | Action |
|--------|--------|---------|--------|
| ... | ... | ... | ... |

### INTENTIONAL (document)
| What | Why Two Exist |
|------|---------------|
| ... | ... |
```

### Phase 4: Fix (on approval)

For each finding, the fix follows one pattern: **Move → Wire → Delete**.

1. **Move** the code to its canonical home (or merge definitions)
2. **Wire** all consumers to import from the new location
3. **Delete** the old definition
4. **Verify** — `rg` for the old symbol name, confirm zero hits outside comments
5. **Build** — run the build to confirm nothing broke

```bash
# After each fix, verify the old symbol is gone
rg -n '<old_symbol>' --glob '*.ts' --glob '*.tsx'
# Should return 0 hits (or only comments/docs)

# Build check
bun run build
```

## When to Run

- After any refactor that moved code between files
- When you find an export that nothing imports
- When you see the same constant/type in two files
- Periodically as part of project health (monthly)
- Before major feature work in an area — clean first

## What This Does NOT Cover

- **Copy-paste duplication** — use `architectural-analysis` skill
- **Semantic duplication** (different code, same intent) — use `30-02-convergence-audit`
- **Dead code within a file** (unused private functions) — use `architectural-analysis`
- **Naming conventions** — use `file-name-wizard`

This skill finds ONE thing: the same concern with split ownership across files.
