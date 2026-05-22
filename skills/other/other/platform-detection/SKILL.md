---
name: platform-detection
description: Centralized tech-stack detection engine. Identifies iOS, Node.js, Rust, Python, Go from project files. Run once at workflow start; result is cached in platform-context.json.
---

# Platform Detection Engine

Runs **once at the start of any feature-marker workflow** and caches the result.
All subsequent phases read from the cached `platform-context.json` — never re-detect.

## When to run

- **First time**: Phase 0 (Inputs Gate) if `platform-context.json` does not exist in state dir
- **Skip**: If `platform-context.json` already exists — use the cached result
- **Force re-detect**: If user passes `--redetect` or deletes the file manually

## Detection logic

Scan the project root for the following signals, **in priority order**:

### 🍎 iOS / Swift

Detected when ANY of:
- `*.xcodeproj` found (up to 3 levels deep)
- `*.xcworkspace` found (up to 3 levels deep)
- `Package.swift` found in root

Subtype disambiguation:
- `xcworkspace` → CocoaPods/multi-target workspace
- `xcodeproj` → single Xcode project
- `swift-package` → Swift Package Manager (Package.swift, no .xcodeproj)

iOS confirmation (vs macOS/watchOS):
- `IPHONEOS_DEPLOYMENT_TARGET` in any `.pbxproj`
- `UIRequiredDeviceCapabilities` in any `Info.plist`

Test framework detection:
- Any `*Tests.swift` with `import Testing` → `swift-testing`
- Only `import XCTest` in test files → `xctest`
- No test files → default to `swift-testing`

Tool availability checks:
- `command -v swiftlint` → `capabilities.swiftlint_available`
- `~/.claude/skills/xcodebuildmcp/SKILL.md` exists → `capabilities.xcodebuildmcp_available`

### 🟨 Node.js / TypeScript

Detected when: `package.json` exists in root

Package manager detection from lockfiles:
- `pnpm-lock.yaml` → `pnpm`
- `yarn.lock` → `yarn`
- `bun.lockb` → `bun`
- `package-lock.json` or none → `npm`

Subtype:
- `next.config.{js,ts,mjs}` → `nextjs`
- `react-native` in `package.json` deps → `react-native`
- `nest-cli.json` → `nestjs`
- else → `node`

Test runner:
- `jest.config.{js,ts}` or `"jest"` in `package.json` → `jest`
- `vitest.config.{ts,js}` or `"vitest"` in `package.json` → `vitest`
- else → `{pm} test`

### 🦀 Rust

Detected when: `Cargo.toml` exists in root

### 🐍 Python

Detected when ANY of: `pyproject.toml`, `setup.py`, `requirements.txt`

### 🐹 Go

Detected when: `go.mod` exists in root

### Multi-stack / Monorepo

If signals from 2+ platforms detected → set `is_monorepo: true`.
Map each detected platform to its sub-directory when possible.

## Manual override

Check `.feature-marker.json` for manual platform override:
```json
{ "platform": "ios" }
```
If present, use that as `primary_platform` (overrides auto-detection).

## Output: platform-context.json

Save to `.claude/feature-state/{slug}/platform-context.json`:

```json
{
  "primary_platform": "ios",
  "platforms": [
    {
      "type": "ios",
      "subtype": "swift-package",
      "path": ".",
      "confidence": "high",
      "signals": ["Package.swift found", ".swift files present (47)", "IPHONEOS_DEPLOYMENT_TARGET detected"],
      "test_command": "swift test --parallel",
      "build_command": "xcodebuild build",
      "lint_command": "swiftlint",
      "test_framework": "swift-testing",
      "capabilities": {
        "swiftlint_available": true,
        "xcodebuildmcp_available": true,
        "swift_testing_available": true
      }
    }
  ],
  "is_monorepo": false,
  "detected_at": "2026-03-01T12:00:00Z"
}
```

Node.js example:
```json
{
  "primary_platform": "nodejs",
  "platforms": [
    {
      "type": "nodejs",
      "subtype": "nextjs",
      "path": ".",
      "confidence": "high",
      "signals": ["package.json found", "next.config found", "pnpm-lock.yaml found"],
      "package_manager": "pnpm",
      "package_manager_lock": "pnpm-lock.yaml",
      "test_command": "jest --findRelatedTests",
      "build_command": "pnpm run build",
      "lint_command": "pnpm run lint"
    }
  ],
  "is_monorepo": false,
  "detected_at": "2026-03-01T12:00:00Z"
}
```

## Confidence scoring

| Score | Signals |
|-------|---------|
| `high` | 3+ platform-specific signals |
| `medium` | 2 signals |
| `low` | 1 signal (config file only) |

## User output

After detection, always display:

```
✅ Platform detected: iOS (Swift Package) — swift test + SwiftLint + XcodeBuildMCP
```

Or for Node.js:
```
✅ Platform detected: Node.js / Next.js (pnpm) — jest + pnpm run lint
```

If unknown:
```
⚠️ Platform not detected. No known config files found.
   Running without platform-specific commands. Use .feature-marker.json to override.
```

## Usage by other phases

| Phase | What it reads |
|-------|---------------|
| Context Gathering | `primary_platform` to adjust file scan patterns |
| idea-explorer | `primary_platform` to frame questions in context of stack |
| spec-writer | `platforms[0].test_command`, `lint_command` for validation sections |
| TechSpec Validation | `primary_platform` to validate import paths format |
| Per-Task Execution | `test_command`, `lint_command`, `build_command` per task |
| Test Only mode | Full platform entry to route to correct test framework |
| commit.md | `primary_platform` + `package_manager` for pre-commit hooks |
