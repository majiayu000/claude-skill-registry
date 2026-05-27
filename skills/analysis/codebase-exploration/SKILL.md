# Codebase Exploration Skill

> Version: 1.0.0
> Compiler: skill-compiler/1.0.0
> Last Updated: 2026-01-23

Systematically survey unfamiliar codebases to build understanding before implementation work.

## When to Activate

Use this skill when:
- Exploring a new repository for the first time
- Surveying an unfamiliar codebase
- Conducting pre-implementation reconnaissance
- Performing architecture review or audit
- Onboarding to a project

## Core Principles

### 1. Documentation First

Read README, AGENTS.md, and existing docs before exploring code.

*Existing documentation captures intent and context that code alone cannot convey; saves exploration time when docs exist.*

### 2. Outside-In Discovery

Start with project boundaries (deps, config, structure) before diving into implementation.

*Understanding the shape of the system prevents getting lost in details; dependencies reveal technology choices and constraints.*

### 3. Parallel Exploration for Breadth

Explore multiple orthogonal aspects simultaneously using sub-agents when appropriate.

*Large codebases have independent concerns; parallel exploration covers more ground within context limits.*

### 4. Follow the References

When a file references another file or concept, trace that reference.

*Codebases are graphs of related concepts; following edges reveals the full picture.*

### 5. Capture Before Context Loss

Write observations and findings immediately; don't rely on memory across exploration.

*Context windows are finite; explicit capture preserves knowledge for later phases.*

### 6. Map the Territory

Build explicit maps (directory structure, component relationships) not just notes.

*Maps are reusable orientation tools; prose notes are harder to navigate.*

---

## Workflow

### Phase 1: Pre-Flight Check

Gather immediate context before exploration begins.

1. Identify exploration goal (audit, pre-implementation, onboarding, debugging)
2. Set scope boundaries (which directories, file types, depth limit, time budget)
3. Check for existing documentation that answers questions (README, AGENTS.md, docs/)
4. Note any specific questions to answer

**Outputs:** Exploration scope definition, known documentation inventory, question list

### Phase 2: Structural Survey

Map the shape of the codebase without reading implementation.

1. List top-level directory structure
2. Identify workspace/monorepo patterns (Cargo workspace, npm workspaces, etc.)
3. Locate entry points (main files, index files, CLI entry)
4. Identify test locations and patterns
5. Note documentation locations

**Outputs:** Directory tree (annotated), entry point map, test location summary

```bash
# Directory structure
tree -L 2 -d

# File type distribution
find . -type f -name "*.rs" | wc -l
find . -type f -name "*.ts" | wc -l

# Entry points
ls **/main.* **/index.* **/mod.* 2>/dev/null
```

### Phase 3: Dependency Analysis

Understand external dependencies and technology choices.

1. Read package manifests (Cargo.toml, package.json, go.mod, etc.)
2. Identify major frameworks and their versions
3. Note dev vs runtime dependencies
4. Look for lock files indicating version pinning
5. Check for workspace/monorepo configuration

**Outputs:** Dependency inventory with purposes, technology stack summary

**Files to check:**
- Cargo.toml, Cargo.lock
- package.json, package-lock.json, yarn.lock
- go.mod, go.sum
- pyproject.toml, requirements.txt
- Makefile, justfile

### Phase 4: Configuration Discovery

Find and understand configuration patterns.

1. Locate config files (.env, config/, settings)
2. Identify environment-specific configs
3. Note configuration formats (YAML, TOML, JSON, etc.)
4. Check for CI/CD configuration (.github/, .gitlab-ci.yml)
5. Look for editor/tooling configs (.vscode/, .editorconfig)

**Outputs:** Configuration file inventory, environment handling summary, CI/CD overview

### Phase 5: Documentation Deep-Read

Read existing documentation thoroughly.

1. Read README.md completely (not skimming)
2. Check for AGENTS.md or similar agent instructions
3. Read any architecture docs (docs/architecture.md, ADRs)
4. Check for API documentation
5. Look for contribution guides (CONTRIBUTING.md)

**Outputs:** Documentation quality assessment, key concepts extracted, gaps identified

**Priority order:**
1. README.md
2. AGENTS.md
3. docs/codebase-overview.md
4. docs/adr/*.md
5. CONTRIBUTING.md

### Phase 6: Code Pattern Recognition

Sample implementation files to understand conventions.

1. Read 2-3 representative source files in detail
2. Identify naming conventions (files, functions, types)
3. Note error handling patterns
4. Look for common abstractions and utilities
5. Check comment and documentation style

**Outputs:** Convention summary, common patterns catalog, code style notes

**Sampling strategy:** Don't read everything; sample strategically:
- One entry point file (main.rs, index.ts)
- One "core" module (often largest or most imported)
- One test file (reveals testing patterns)
- One utility/helper file (reveals abstractions)

### Phase 7: Integration Points

Identify how components connect and external boundaries.

1. Find module boundaries and exports
2. Identify external service integrations
3. Note CLI/API surface areas
4. Map internal dependencies between modules
5. Check for plugin/extension points

**Outputs:** Integration point inventory, external service dependencies, module graph

### Phase 8: Synthesis and Output

Consolidate findings into usable artifacts.

1. Write structured findings (tables, lists)
2. Create or update codebase map
3. Document open questions
4. Note technical debt or red flags observed
5. Recommend next exploration areas if incomplete

**Outputs:** Codebase overview document, open questions list, observations dump

---

## Patterns

| Pattern | When | Do | Why |
|---------|------|-----|-----|
| **Parallel Sub-Agent Exploration** | Codebase has separable concerns | Spawn Task agents for each concern; merge findings | Covers more ground within context limits |
| **Documentation-Existence Check** | Starting any repo exploration | `ls README.md AGENTS.md docs/*.md 2>/dev/null` | Existing docs may answer questions |
| **Dependency Purpose Annotation** | Reading package manifest | Note each dependency's purpose | Dependency lists without context are hard to interpret |
| **Progressive Depth** | Limited time budget | Complete each phase shallow before going deep | Broad coverage reveals structure |
| **Reference Chasing** | File mentions another file/concept | Note reference; trace if relevant | References reveal actual relationships |
| **Sampling Not Exhaustive** | Many files of similar type (50+) | Read 3-5 samples; infer patterns | Exhaustive reading exhausts context |

---

## Anti-Patterns to Avoid

| Anti-Pattern | Why It Fails | Instead |
|--------------|--------------|---------|
| **Diving Into Implementation First** | Get lost in details; miss architecture | Complete structural survey first |
| **Exhaustive Reading** | Context exhaustion; diminishing returns | Sample representative files |
| **Ignoring Documentation** | Miss intent and context code can't convey | Read docs first; verify against code |
| **Sequential Single-Threaded** | Covers less ground; misses connections | Use sub-agents for orthogonal concerns |
| **Mental-Only Notes** | Knowledge lost at context exhaustion | Write findings immediately |
| **Skipping Test Structure** | Miss usage patterns and expected behaviors | Always check test organization |

---

## Quality Checklist

Before completing exploration:

- [ ] README.md and AGENTS.md read (if they exist)
- [ ] Directory structure mapped
- [ ] Entry points identified
- [ ] Dependencies inventoried with purposes
- [ ] Configuration files located
- [ ] 2-3 source files sampled for conventions
- [ ] Test structure understood
- [ ] Integration points noted
- [ ] Findings written (not just remembered)
- [ ] Open questions documented

---

## Examples

**Survey unfamiliar Rust CLI project (beadsmith)**

```bash
# 1. Pre-flight: Goal is understanding for implementation work
# Scope: Full repo, focus on skill system

# 2. Check for docs first
ls README.md docs/ AGENTS.md
# Found: README.md, docs/ with ADRs

# 3. Structural survey
tree -L 2 -d
# Identified: crates/beadsmith (CLI), skills/ (bundled skills), planning/

# 4. Dependencies
cat Cargo.toml  # workspace config
cat crates/beadsmith/Cargo.toml  # clap, anyhow, colored, dirs

# 5. Read docs
# README.md - project overview, skill list
# docs/codebase-overview.md - comprehensive bootstrap guide

# 6. Sample source files
# main.rs - CLI entry, command dispatch
# skills.rs - include_str!() pattern for bundling
# commands/init.rs - skill extraction logic

# 7. Findings
# - Compile-time skill bundling via include_str!()
# - Skills have input.yaml (source) + SKILL.md (compiled)
# - Planning integration with external org-mode and beads
# - Well-documented with ADRs
```

**Quick audit under time pressure (15 minutes)**

```bash
# Use progressive depth - broad shallow first

# Phase 1: Immediate orientation (3 min)
cat README.md | head -100
tree -L 1
ls -la

# Phase 2: Dependencies (3 min)
cat package.json 2>/dev/null || cat Cargo.toml 2>/dev/null

# Phase 3: Entry points (3 min)
find . -name "main.*" -o -name "index.*" | head -5

# Phase 4: Quick doc scan (3 min)
ls docs/ 2>/dev/null
cat CONTRIBUTING.md 2>/dev/null | head -50

# Phase 5: Write findings (3 min)
# Even under time pressure, write what you learned
```

---

## Related Skills

| Skill | Relationship |
|-------|--------------|
| `research` | Use after exploration for deep investigation |
| `skill-compiler` | Understanding skill structure aids beadsmith exploration |

---

## References

- `research` skill - for deep investigation after initial survey
- `skill-compiler` skill - for understanding skill structure in beadsmith
- Anthropic: "Building Effective Agents" - context management patterns
