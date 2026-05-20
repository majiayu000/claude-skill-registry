---
name: aminet-emulator
description: "FS-UAE emulator configuration and launch: hardware profiles, ROM management, WHDLoad integration, config generation, and state snapshots. Use when configuring emulation, managing ROMs, or launching Amiga software."
metadata:
  extensions:
    gsd-skill-creator:
      triggers:
        intents:
          - "aminet.*run|aminet.*launch"
          - "fs-uae|fsuae"
          - "emulat.*config"
          - "whdload"
          - "rom.*manage"
        files:
          - "src/aminet/emulator-config.ts"
          - "src/aminet/hardware-profiles.ts"
          - "src/aminet/rom-manager.ts"
          - "src/aminet/whdload.ts"
          - "src/aminet/emulator-launch.ts"
          - "src/aminet/emulator-state.ts"
        contexts:
          - "amiga emulation"
          - "emulator configuration"
          - "fs-uae setup"
        threshold: 0.7
      token_budget: "1.0%"
      version: 1
      enabled: true
      plan_origin: "242-aminet-integration"
      phase_origin: "242"
---

# Aminet Emulator

## Purpose

Manages FS-UAE emulator configuration, hardware profiles, ROM provisioning, WHDLoad integration, launch orchestration, and emulator state snapshots. Enables launching Amiga software with the correct hardware configuration, Kickstart ROM, and WHDLoad settings derived from package metadata.

## Capabilities

- FS-UAE config generation with buildFsUaeConfig/generateFsUaeConfig
- Path normalization and sorted key output for deterministic configs
- Boolean 1/0 serialization matching FS-UAE format
- 5 hardware profiles: A500, A1200, A1200+030, A4000, WHDLoad
- Embedded TS constants with deep-frozen structuredClone copies
- getProfile/getAllProfiles/getProfileForModel accessors
- ROM manager with CRC32 IEEE polynomial (no external deps)
- 12 known ROM entries with checksums (no ROM data distributed)
- scanRomDirectory with Cloanto XOR decryption and overdump handling
- selectRomForProfile with WHDLoad-to-A1200 fallback mapping
- DI-based crc32Fn for testability
- selectProfileFromReadme with priority-based matching (WHDLoad > 040 > 030 > AGA > 020 > OS3.x > A500 default)
- writeFsUaeConfig with recursive mkdir
- launchEmulator orchestrating config gen + write + execFile
- Structured error types: NO_HARD_DRIVES, INVALID_PROFILE, FSUAE_MISSING, LAUNCH_FAILED
- WHDLoad .Slave detection (case-insensitive recursive scan)
- WHDLOAD_KICKSTART_MAP for 8 Kickstart revisions
- Per-game CPU/chipset/RAM/NTSC/clock overrides via buildWhdloadConfig
- save_states=0 forced for safety; PRELOAD hint at 4MB+
- 9-slot snapshot metadata (save/list/delete)
- shouldDisableSaveStates for directory hard drive safety
- buildMissingRomGuidance with CRC32 hex and legal source references

## Key Modules

| Module | Purpose |
|--------|---------|
| `src/aminet/emulator-config.ts` | FS-UAE config generation with path normalization and sorted keys |
| `src/aminet/hardware-profiles.ts` | 5 hardware profiles (A500/A1200/A1200+030/A4000/WHDLoad) |
| `src/aminet/rom-manager.ts` | CRC32 ROM identification, Cloanto decryption, directory scanning |
| `src/aminet/whdload.ts` | WHDLoad .Slave detection, kickstart mapping, per-game overrides |
| `src/aminet/emulator-launch.ts` | Launch orchestration with profile selection and structured errors |
| `src/aminet/emulator-state.ts` | 9-slot snapshots, save state safety checks, ROM guidance |

## Usage Examples

**Generate FS-UAE config:**
```typescript
import { buildFsUaeConfig, generateFsUaeConfig } from './emulator-config.js';

const config = buildFsUaeConfig({
  profile: a1200Profile,
  romPath: '/roms/kick31.rom',
  hardDrives: ['/games/Lemmings'],
});
const configText = generateFsUaeConfig(config);
// Sorted key=value pairs ready for FS-UAE
```

**Select profile from readme:**
```typescript
import { selectProfileFromReadme } from './emulator-launch.js';

const profile = selectProfileFromReadme(readmeText);
// Matches WHDLoad > 040 > 030 > AGA > 020 > OS3.x > A500 default
```

**Scan and select ROM:**
```typescript
import { scanRomDirectory, selectRomForProfile } from './rom-manager.js';

const roms = await scanRomDirectory('/roms');
const rom = selectRomForProfile(roms, 'a1200');
// Handles Cloanto encrypted ROMs and overdumps
```

**Configure WHDLoad:**
```typescript
import { detectSlaveFiles, buildWhdloadConfig } from './whdload.js';

const slaves = await detectSlaveFiles('/games/Lemmings');
const config = buildWhdloadConfig(slaves[0], {
  cpu: '68020',
  chipRam: 2048,
  ntsc: false,
});
```

**Launch emulator:**
```typescript
import { launchEmulator } from './emulator-launch.js';

const result = await launchEmulator({
  packageDir: '/games/Lemmings',
  romDir: '/roms',
  readmeText,
});
// Orchestrates: profile selection -> ROM match -> config gen -> launch
```

## Dependencies

- FS-UAE emulator installed on host system
- User-provided Kickstart ROMs (not distributed; CRC32 verification only)
- Node.js `node:child_process` for FS-UAE launch
- Node.js `node:fs` for config writing and ROM scanning
- Node.js `node:crypto` not used (CRC32 implemented inline, IEEE polynomial)

## Token Budget Rationale

1.0% budget reflects the 6 modules covering config generation, hardware profiles, ROM management, WHDLoad integration, launch orchestration, and state snapshots. Despite the module count, the patterns are well-structured with clear separation of concerns, requiring moderate context for correct configuration and launch sequences.
