---
name: aminet-scanner
description: "Multi-layer virus scanning for Aminet packages. Signature-based detection, heuristic hunk analysis, boot block scanning, quarantine management, and scan orchestration. Use when scanning packages, checking virus status, or managing quarantine."
metadata:
  extensions:
    gsd-skill-creator:
      triggers:
        intents:
          - "scan.*aminet|aminet.*scan"
          - "virus.*check|check.*virus"
          - "quarantine"
          - "heuristic.*scan"
        files:
          - "src/aminet/signature-scanner.ts"
          - "src/aminet/heuristic-scanner.ts"
          - "src/aminet/scan-orchestrator.ts"
          - "src/aminet/quarantine.ts"
          - "src/aminet/signature-db.ts"
        contexts:
          - "aminet virus scanning"
          - "package security"
        threshold: 0.7
      token_budget: "1.5%"
      version: 1
      enabled: true
      plan_origin: "242-aminet-integration"
      phase_origin: "242"
---

# Aminet Scanner

## Purpose

Provides multi-layer virus scanning for Aminet packages targeting the Amiga malware landscape. Combines signature-based detection (52 virus signatures in ClamAV .ndb format), heuristic analysis of hunk structures and boot blocks, quarantine management with atomic file isolation, and a scan orchestrator that coordinates all layers into unified scan reports with configurable depth levels.

## Capabilities

- 52 virus signatures across 3 JSON database files (boot block, file, hunk viruses)
- Context-aware scanBuffer with hex pattern matching and wildcard bitmasks
- Boot block and hunk type dispatch for targeted scanning
- Sub-2-second scanning for 500KB files against 50 signatures
- Last-wins deduplication for extensible signature JSON drop-in
- 8 heuristic rules: 4 hunk-based, 4 boot block-based
- Zero false positives on legitimate Amiga files
- Worst-case verdict derivation across all findings
- Quarantine with atomic file moves and metadata sidecars
- Path traversal prevention on quarantine operations
- Restore round-trip (quarantine and recover)
- FS-UAE + CheckX emulated scanning with AbortController timeout
- Community checksum cross-reference for known-good verification
- Scan orchestrator coordinating signature + heuristic into unified ScanReport
- Configurable depth: fast (signatures only), standard (sig + heuristic), thorough (sig + heuristic + emulated)
- Batch processing with auto-quarantine for infected packages
- YAML-based scan policy with Zod validation

## Key Modules

| Module | Purpose |
|--------|---------|
| `src/aminet/signature-db.ts` | 52 virus signatures in 3 JSON files with last-wins deduplication |
| `src/aminet/signature-scanner.ts` | Context-aware hex pattern matching with wildcard bitmasks |
| `src/aminet/heuristic-scanner.ts` | 8 heuristic rules for hunk and boot block analysis |
| `src/aminet/quarantine.ts` | Atomic file isolation with metadata sidecars and restore |
| `src/aminet/scan-orchestrator.ts` | Coordinates all scan layers into unified ScanReport |
| `src/aminet/emulated-scanner.ts` | FS-UAE + CheckX emulated scanning with timeout control |

## Usage Examples

**Quick signature scan:**
```typescript
import { scanBuffer } from './signature-scanner.js';

const result = scanBuffer(fileBuffer, { context: 'hunk' });
// result.verdict: 'clean' | 'suspicious' | 'infected'
// result.findings: matched signature details
```

**Full orchestrated scan:**
```typescript
import { scanPackage } from './scan-orchestrator.js';

const report = await scanPackage(filePath, {
  depth: 'thorough', // fast | standard | thorough
  autoQuarantine: true,
  quarantineDir: './quarantine',
});
// report.verdict, report.signatureFindings, report.heuristicFindings
```

**Quarantine management:**
```typescript
import { quarantineFile, restoreFile } from './quarantine.js';

await quarantineFile(infectedPath, { quarantineDir: './quarantine', reason: 'SCA virus' });
await restoreFile(quarantinedId, { quarantineDir: './quarantine', restoreDir: './restored' });
```

**Batch scan with auto-quarantine:**
```typescript
import { batchScan } from './scan-orchestrator.js';

const results = await batchScan(filePaths, {
  depth: 'standard',
  autoQuarantine: true,
  quarantineDir: './quarantine',
});
```

## Dependencies

- Aminet hunk parser (`src/aminet/hunk-parser.ts`) for binary analysis
- Aminet boot block parser (`src/aminet/bootblock-parser.ts`) for boot sector analysis
- Node.js `node:fs` for file I/O and quarantine operations
- FS-UAE emulator (optional, for thorough/emulated scanning)
- Zod for scan policy YAML validation

## Token Budget Rationale

1.5% budget reflects the 6 modules covering the complete multi-layer scanning pipeline. The signature database format, hex pattern matching with wildcards, heuristic rule engine, quarantine atomicity, and orchestrator coordination logic require comprehensive context for correct security operation and troubleshooting.
