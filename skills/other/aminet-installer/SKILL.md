---
name: aminet-installer
description: "Aminet package installation: LhA/LZX extraction, Amiga filesystem mapping, dependency detection, install tracking, and scan gate enforcement. Use when installing, extracting, or uninstalling Amiga packages."
metadata:
  extensions:
    gsd-skill-creator:
      triggers:
        intents:
          - "aminet.*install"
          - "aminet.*extract"
          - "aminet.*uninstall"
          - "scan.*gate"
        files:
          - "src/aminet/lha-extractor.ts"
          - "src/aminet/lzx-extractor.ts"
          - "src/aminet/filesystem-mapper.ts"
          - "src/aminet/dependency-detector.ts"
          - "src/aminet/install-tracker.ts"
          - "src/aminet/scan-gate.ts"
        contexts:
          - "aminet installation"
          - "archive extraction"
        threshold: 0.7
      token_budget: "1.0%"
      version: 1
      enabled: true
      plan_origin: "242-aminet-integration"
      phase_origin: "242"
---

# Aminet Installer

## Purpose

Manages the complete Aminet package installation pipeline: extraction of LhA and LZX archives using native tools, mapping extracted files to Amiga filesystem conventions (11 assigns), dependency detection from .readme metadata, install tracking with atomic manifest persistence, and scan gate enforcement ensuring packages are verified clean before installation.

## Capabilities

- LhA extraction via lhasa with Zip-Slip path traversal prevention
- Volume prefix stripping for clean extraction paths
- 30-second extraction timeout for safety
- LZX extraction via unlzx with cwd workaround (no output dir flag)
- Tool validator with platform-specific install guidance (apt/brew)
- unlzx exit-code-2 detection for partial extraction handling
- Amiga filesystem mapping with 11 standard assigns (S:, C:, LIBS:, DEVS:, etc.)
- Case-insensitive assign lookup matching Amiga conventions
- Software/ default placement for unmapped paths
- placeFiles with SHA-256 tracking and temp directory cleanup
- 5 dependency types: package, os_version, hardware, library, unknown
- Dependency detection from .readme Requires: field
- Package deps cross-referenced against mirror state for availability
- Install tracker with atomic manifest persistence
- Slugified manifest filenames for cross-platform safety
- Uninstall with file removal and directory cleanup
- Scan gate enforcing INS-07 (refuse unscanned), INS-08 (refuse infected), INS-09 (suspicious override via confirmFn)
- installPackage orchestrator: gate -> extract -> place -> deps -> track -> state

## Key Modules

| Module | Purpose |
|--------|---------|
| `src/aminet/lha-extractor.ts` | LhA archive extraction via lhasa with Zip-Slip prevention |
| `src/aminet/lzx-extractor.ts` | LZX archive extraction via unlzx with cwd workaround |
| `src/aminet/filesystem-mapper.ts` | Maps extracted files to Amiga assigns (11 standard mappings) |
| `src/aminet/dependency-detector.ts` | Detects 5 dependency types from .readme Requires: field |
| `src/aminet/install-tracker.ts` | Atomic manifest persistence with install/uninstall tracking |
| `src/aminet/scan-gate.ts` | Enforces scan requirements before allowing installation |

## Usage Examples

**Extract an LhA archive:**
```typescript
import { extractLha } from './lha-extractor.js';

const result = await extractLha(archivePath, { outputDir: './extracted', timeout: 30000 });
// result.files: extracted file paths with Zip-Slip protection
```

**Map to Amiga filesystem:**
```typescript
import { placeFiles } from './filesystem-mapper.js';

const placed = await placeFiles(extractedFiles, {
  targetDir: './amiga-root',
  assigns: defaultAssigns,
});
// Files mapped to S:, C:, LIBS:, etc. with SHA-256 tracking
```

**Install with scan gate:**
```typescript
import { installPackage } from './scan-gate.js';

const result = await installPackage(packagePath, {
  scanReport, // Must be clean or user-confirmed suspicious
  outputDir: './amiga-root',
  manifestDir: './manifests',
  confirmFn: async (msg) => promptUser(msg), // For suspicious overrides
});
```

**Detect dependencies:**
```typescript
import { detectDependencies } from './dependency-detector.js';

const deps = detectDependencies(readmeText, mirrorState);
// deps: [{ type: 'package', name: 'util/libs/AHI.lha', available: true }, ...]
```

## Dependencies

- `lhasa` CLI tool for LhA extraction (installed via system package manager)
- `unlzx` CLI tool for LZX extraction
- Tool validator provides platform-specific install guidance
- Aminet scanner (aminet-scanner skill) for scan gate integration
- Node.js `node:crypto` for SHA-256 file tracking
- Node.js `node:child_process` for tool execution

## Token Budget Rationale

1.0% budget reflects the 6 modules covering extraction, filesystem mapping, dependencies, tracking, and scan gate. The installation pipeline is largely sequential and well-contained, requiring moderate context for the assign mapping and scan gate enforcement logic.
