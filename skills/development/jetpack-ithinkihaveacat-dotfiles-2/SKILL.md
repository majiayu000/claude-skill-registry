---
name: jetpack
description: >
  Resolves AndroidX/Jetpack library information including version lookup,
  package-to-Maven-coordinate conversion, and source code downloading. Provides
  tools for inspecting Jetpack library implementations. Use when working with
  androidx libraries, resolving Maven coordinates, downloading Jetpack source
  code, checking library versions (alpha/beta/stable/snapshot), or inspecting
  AndroidX class implementations. Triggers: androidx, jetpack, maven coordinate,
  jetpack source, library version, snapshot, alpha, beta.
compatibility: >
  Requires curl, xmllint (libxml2-utils), jar (JDK). Needs network access to
  dl.google.com and androidx.dev.
---

# Jetpack Library Utilities

## Important: Use Script First

**ALWAYS use `scripts/jetpack` over raw `curl` and `xmllint` commands.** The
script is located in the `scripts/` subdirectory of this skill's folder. It
provides features that raw commands do not:

- Package-to-coordinate resolution with exceptions table
- Version type handling (ALPHA, BETA, STABLE, SNAPSHOT)
- Kotlin Multiplatform platform-specific source detection
- Build ID resolution for pinned snapshots

**When to read the script source:** If the script doesn't do exactly what you
need, or fails due to missing dependencies, read the script source. It encodes
Maven repository URL patterns, version filtering logic, and package naming
heuristics—use it as reference when building similar functionality.

## Quick Start

**Requirements:** `curl`, `xmllint` (libxml2-utils), `jar` (JDK).

### Highest-Value Commands

- **Inspect a class (most common):**
  `scripts/jetpack inspect androidx.wear.tiles.TileService`
- **Check stable version:**
  `scripts/jetpack version androidx.wear.tiles:tiles STABLE`
- **Resolve package to Maven coordinate:**
  `scripts/jetpack resolve androidx.lifecycle.ViewModel`
- **Download bleeding-edge source:**
  `scripts/jetpack source androidx.compose.ui:ui SNAPSHOT`

## Subcommand Overview

### `version`

**Purpose**: Get specific version type (ALPHA, BETA, SNAPSHOT, etc.) for a
package. **Usage**: `scripts/jetpack version PACKAGE [TYPE] [REPO]` **Options**:
`ALPHA`, `BETA`, `RC`, `STABLE`, `LATEST`, `SNAPSHOT`.

### `resolve`

**Purpose**: Convert Android package/class name to Maven coordinate. **Usage**:
`scripts/jetpack resolve PACKAGE_OR_CLASS` **Note**: Uses heuristic rules and an
exceptions table.

### `source`

**Purpose**: Download and extract source JARs. **Usage**:
`scripts/jetpack source PACKAGE... [VERSION]` **Options**: `--output DIR` to
specify destination.

### `inspect`

**Purpose**: Convenience wrapper combining `resolve` + `source`. **Usage**:
`scripts/jetpack inspect CLASS_NAME [VERSION]` **Note**: Best for quickly
checking implementation details.

### `resolve-exceptions`

**Purpose**: Find missing exceptions for the `resolve` command. **Usage**:
`scripts/jetpack resolve-exceptions COORDINATE` **Note**: Analyzes SNAPSHOT JARs
to find packages violating naming conventions.

## Version Types

### Symbolic (Floating)

Resolves to the latest matching version at runtime.

- **ALPHA**: Latest alpha (e.g., `1.2.0-alpha05`)
- **BETA**: Latest beta (e.g., `1.2.0-beta02`)
- **RC**: Latest release candidate (e.g., `1.2.0-rc01`)
- **STABLE**: Latest stable release (e.g., `1.1.0`)
- **LATEST**: Latest version of any kind.
- **SNAPSHOT**: Latest build from `androidx.dev`.

### Pinned (Immutable)

Always resolve to the exact same code.

- **Version String**: Specific version (e.g., `1.6.0-alpha01`).
- **Build ID**: Specific snapshot build (e.g., `14710011` from
  `androidx.dev/snapshots/builds`).

## Common Workflows

### Inspecting a Class Implementation

```bash
cd "$(scripts/jetpack inspect androidx.wear.tiles.TileService)"
# Browse source files...
```

### Checking Available Versions

```bash
scripts/jetpack version androidx.wear.tiles:tiles ALPHA
scripts/jetpack version androidx.wear.tiles:tiles SNAPSHOT
scripts/jetpack version androidx.wear.tiles:tiles 14765146
```

### Working with Bleeding-Edge Code

```bash
scripts/jetpack source androidx.compose.remote:remote-creation-compose SNAPSHOT
```

### Finding Maven Coordinate

```bash
scripts/jetpack resolve androidx.core.splashscreen.SplashScreen
# Output: androidx.core:core-splashscreen
```

## Safety Notes

- **Network Access**: Requires access to `dl.google.com` and `androidx.dev`.
- **SNAPSHOTs**: Change frequently; use pinned versions or Build IDs for
  reproducibility.
- **Kotlin Multiplatform**: `source` and `inspect` automatically download
  platform-specific sources (e.g., `-android`, `-desktop`) if detected in the
  POM.
