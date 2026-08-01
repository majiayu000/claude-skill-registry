---
name: prompts-ithinkihaveacat-dotfiles
description: Create an Agent Skill that helps agents work with Android Jetpack libraries.
---

# Prompt: Create Jetpack Library Utilities Skill

Create an Agent Skill that helps agents work with Android Jetpack libraries.
This skill should document the `jetpack` script's capabilities and strongly
encourage agents to use the script over raw commands.

## Goal

Produce a self-contained skill directory at `etc/skills/jetpack/` that an agent
can use to:

1. Run the bundled `jetpack` script directly (fast, deterministic, with
   intelligent package resolution and version handling)
2. Only fall back to raw commands when the script fails due to missing
   dependencies

**Important:** The `jetpack` script provides significant value beyond raw
commands (e.g., package-to-coordinate resolution with exceptions table, version
type handling, Kotlin Multiplatform support). The skill must make agents prefer
the script by default and only consult raw commands as a last resort by reading
the script source.

## Research Phase

Before creating files, research the following:

1. **Review the Agent Skills specification** at
   <https://agentskills.io/specification.md> to understand frontmatter
   requirements, directory structure, and naming conventions.

2. **Examine the `bin/jetpack` script thoroughly**:
   - All subcommands: `version`, `resolve`, `source`, `inspect`,
     `resolve-exceptions`
   - The underlying `curl`, `xmllint`, and `jar` commands
   - Dependencies (look for `require` calls)
   - Maven repository URLs used (Google Maven, androidx.dev snapshots)
   - Version type handling (ALPHA, BETA, RC, STABLE, LATEST, SNAPSHOT)
   - The exceptions table in the `resolve` subcommand

   For each subcommand, understand:
   - Purpose and when to use it
   - The underlying raw commands
   - Input/output format
   - Error conditions

## Deliverable Structure

Create this exact structure:

```text
etc/skills/jetpack/
├── SKILL.md              # Required: frontmatter + instructions
├── scripts/              # Copy of the jetpack script
└── references/           # Reference documentation
    ├── command-index.md
    └── troubleshooting.md
```

Do not create extra files like README.md, CHANGELOG.md, or INSTALLATION.md.

## Script Selection

Symlink `bin/jetpack` into `scripts/` using a relative path. Preserve the
filename and executable permissions.

### Transitive Script Dependencies

The `jetpack` script is self-contained and does not call other scripts from
`bin/`. No additional scripts need to be symlinked.

## SKILL.md Requirements

### Frontmatter

Follow the Agent Skills specification exactly:

```yaml
---
name: jetpack
description: [See below]
---
```

**Name requirements:**

- Lowercase letters, numbers, hyphens only
- Max 64 characters
- Must match directory name

**Description requirements (critical for discovery):**

- Max 1024 characters
- Write in **third person** (the description is injected into system prompts)
- Include what the skill does AND when to use it
- End with explicit trigger phrases using "Triggers:" prefix for reliable
  discovery across different agent implementations

Include these trigger phrases: androidx, jetpack, maven coordinate, jetpack
source, library version, snapshot, alpha, beta

Example pattern:

```yaml
description: >
  Resolves AndroidX/Jetpack library information including version lookup,
  package-to-Maven-coordinate conversion, and source code downloading. Provides
  tools for inspecting Jetpack library implementations. Use when working with
  androidx libraries, resolving Maven coordinates, downloading Jetpack source
  code, checking library versions (alpha/beta/stable/snapshot), or inspecting
  AndroidX class implementations. Triggers: androidx, jetpack, maven coordinate,
  jetpack source, library version, snapshot, alpha, beta.
```

**Compatibility requirements (recommended):**

- Max 500 characters
- Include if the skill has external dependencies or environment requirements
- Mention required command-line tools, network access needs, or target platforms
- Example:
  `compatibility: Requires curl, xmllint (libxml2-utils), jar (JDK). Needs network access to dl.google.com and androidx.dev.`

For maximum compatibility across skill loaders, prefer a single-line
`description:` value and avoid YAML block scalars like `description: |` (some
implementations treat multi-line descriptions inconsistently). If you need line
wrapping, prefer a folded scalar (`description: >`) rather than a literal block
(`description: |`).

### Body Content

Keep the body under 500 lines. Structure it for progressive disclosure—agents
load this only when the skill activates, so be concise.

#### Quick Start

- System requirements: `curl`, `xmllint` (libxml2-utils), `jar` (JDK)
- 4-5 highest-value commands to run first:
  - `scripts/jetpack inspect <CLASS_NAME>` (most common use case)
  - `scripts/jetpack version <PACKAGE> STABLE`
  - `scripts/jetpack resolve <CLASS_NAME>`
  - `scripts/jetpack source <PACKAGE> SNAPSHOT`
- Use paths relative to the skill: `scripts/jetpack`

#### Scripts First (Critical)

Add a prominent section near the top of SKILL.md body titled "Important: Use
Script First" that:

1. Tells agents to **ALWAYS use `scripts/jetpack`** over raw curl/xmllint
2. Notes that the script is located in the `scripts/` subdirectory of the
   skill's folder
3. Lists specific features the script provides that raw commands don't:
   - Package-to-coordinate resolution with exceptions table
   - Version type handling (ALPHA, BETA, STABLE, SNAPSHOT)
   - Kotlin Multiplatform platform-specific source detection
   - Build ID resolution for pinned snapshots
4. Explains when to read script source: if the script doesn't do exactly what's
   needed, or fails due to missing dependencies. The script encodes Maven
   repository URL patterns, version filtering logic, and package naming
   heuristics—it serves as valuable reference when building similar
   functionality.

This section ensures agents see the scripts-first guidance immediately when the
skill activates.

#### Subcommand Overview

A compact reference for each subcommand. For each, provide:

- **Purpose** (1-2 lines)
- **Basic usage**
- **Key options**

Subcommands to document:

1. **version** - Get specific version type for a Jetpack package
2. **resolve** - Convert Android package/class name to Maven coordinate
3. **source** - Download and extract source JARs
4. **inspect** - Convenience wrapper combining resolve + source
5. **resolve-exceptions** - Find missing exceptions for resolve command

#### Version Types

Document the version specifier system clearly:

**Symbolic (floating):** Resolve to latest matching version at runtime.

- ALPHA, BETA, RC, STABLE, LATEST, SNAPSHOT

**Pinned (immutable):** Always resolve to exact same code.

- Specific version strings (e.g., `1.6.0-alpha01`)
- Snapshot build IDs (e.g., `14710011` from androidx.dev)

#### Common Workflows

Document typical usage patterns:

1. **Inspecting a class implementation**

   ```bash
   cd "$(scripts/jetpack inspect androidx.wear.tiles.TileService)"
   ```

2. **Checking what version is available**

   ```bash
   scripts/jetpack version androidx.wear.tiles:tiles ALPHA
   scripts/jetpack version androidx.wear.tiles:tiles SNAPSHOT
   ```

3. **Working with bleeding-edge code**

   ```bash
   scripts/jetpack source androidx.compose.remote:remote-creation-compose SNAPSHOT
   ```

4. **Finding the Maven coordinate for a class**

   ```bash
   scripts/jetpack resolve androidx.core.splashscreen.SplashScreen
   ```

#### Safety Notes

- Script requires network access to Maven repositories
- SNAPSHOT versions change frequently; pinned versions are reproducible
- Some libraries may not have all version types available
- Kotlin Multiplatform libraries have platform-specific sources

## Reference Files

### references/command-index.md

If this file is longer than 100 lines, include a `## Contents` section at the
top (a short table of contents) so agents can see the full scope even when
previewing the file.

For each subcommand, document:

- **Purpose** (1 line)
- **Synopsis** (usage pattern)
- **Arguments** (with descriptions)
- **Options** (flags and their effects)
- **Examples** (2-3 practical examples)
- **Raw commands** (the underlying curl/xmllint/jar commands)
- **Exit codes** (success/failure conditions)

Include a section on the **exceptions table** from the `resolve` subcommand,
explaining:

- What it is (package prefix → Maven coordinate mapping)
- Why it exists (packages that don't follow the standard naming convention)
- How to add new exceptions using `resolve-exceptions`

### references/troubleshooting.md

If this file is longer than 100 lines, include a `## Contents` section at the
top (a short table of contents) so agents can see the full scope even when
previewing the file.

Cover:

- Missing dependencies (`curl`, `xmllint`, `jar`)
- Network errors (failed to fetch maven-metadata.xml)
- Package not found in repository
- No version of requested type available
- Snapshot-only packages (must explicitly request SNAPSHOT)
- Invalid package format errors
- Resolving ambiguous package names
- Kotlin Multiplatform libraries and platform-specific sources

## Writing Guidelines

- Be concise. Agents are intelligent; provide what they don't already know.
- Use imperative form ("Run this command" not "You can run this command").
- Include concrete examples with realistic package/class names.
- Emphasize the script over raw commands. The script provides features (package
  resolution, version handling, KMP support) that raw commands don't.
- Do not duplicate raw commands from the script into SKILL.md. Tell agents to
  read the script source if they need the underlying command.
- Keep file references one level deep from SKILL.md.

## Quality Checklist

Before finalizing, verify:

- [ ] Skill directory exists at `etc/skills/jetpack/`
- [ ] `SKILL.md` has valid frontmatter matching the spec
- [ ] Description is in third person and includes trigger phrases
- [ ] Compatibility field lists required tools (curl, xmllint, jar) and network
      access
- [ ] `SKILL.md` body is under 500 lines
- [ ] `SKILL.md` has "Important: Use Script First" section near top of body
- [ ] `scripts/` contains a symlink to `bin/jetpack`
- [ ] Script is executable (`chmod +x`)
- [ ] Raw commands are NOT in SKILL.md body (agents read script source)
- [ ] `references/command-index.md` documents each subcommand with raw commands
- [ ] `references/troubleshooting.md` covers common issues
- [ ] All five subcommands are documented
- [ ] Version types (ALPHA/BETA/RC/STABLE/LATEST/SNAPSHOT) are explained
- [ ] Pinned versions (specific strings, build IDs) are explained
- [ ] No extraneous files (README.md, etc.)
- [ ] Examples use realistic AndroidX package/class names

## Implementation Notes

- Use `mkdir -p` to create directories
- Use `ln -s` to create relative symlinks (e.g.,
  `ln -s ../../../../bin/jetpack scripts/jetpack`)
- Verify executable bits with `chmod +x scripts/*` if needed
- Do not modify the original `bin/jetpack` script—only symlink into the skill
- Test that the symlinked script works from the skill directory
- The script's `require` function will check for dependencies at runtime

## Package Name Examples

Use these realistic examples throughout the documentation:

**Common packages:**

- `androidx.wear.tiles:tiles`
- `androidx.lifecycle:lifecycle-runtime`
- `androidx.compose.ui:ui`
- `androidx.core:core-splashscreen`

**Class names for resolve:**

- `androidx.wear.tiles.TileService`
- `androidx.lifecycle.ViewModel`
- `androidx.core.splashscreen.SplashScreen`
- `androidx.compose.ui.Modifier`

**Snapshot-only packages (use SNAPSHOT explicitly):**

- `androidx.compose.remote:remote-creation-compose`
- `androidx.glance.wear:wear`
