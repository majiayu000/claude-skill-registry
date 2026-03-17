---
name: ios-deps
description: Manage Swift Package Manager dependencies with security checks and update verification.
argument-hint: "[--check] [--audit] [--update] [--add <package>]"
allowed-tools: Bash, Write, Read, Glob, Grep
---

## Purpose
Manage SPM dependencies safely: check for updates, audit for issues, and add packages with verification.

## Arguments
- `--check` — Check for outdated packages (default if no args)
- `--audit` — Check for known security issues
- `--update` — Update to latest compatible versions with test verification
- `--add <package>` — Add a new package (URL or shorthand)

## Workflow

### Check (`--check`)
1. Parse `Package.swift` or `Package.resolved`
2. Query package registries for latest versions
3. Report packages with updates available
4. Categorize: minor, major

### Audit (`--audit`)
1. Check dependencies against known vulnerability databases
2. Report any security advisories
3. Suggest updates or alternatives

### Update (`--update`)
1. Show packages to update
2. **Ask for approval**
3. Update: `swift package update`
4. Build to verify: `xcodebuild build`
5. Run tests: `xcodebuild test`
6. If tests pass, report success
7. If tests fail, rollback and report

### Add (`--add`)
1. Validate package URL or resolve shorthand
2. Add to `Package.swift` or via Xcode
3. Resolve dependencies
4. Build to verify
5. Report usage instructions

## Package shorthands
Common packages can be added by name:
- `alamofire` → `https://github.com/Alamofire/Alamofire.git`
- `kingfisher` → `https://github.com/onevcat/Kingfisher.git`
- `swiftyjson` → `https://github.com/SwiftyJSON/SwiftyJSON.git`
- `snapkit` → `https://github.com/SnapKit/SnapKit.git`

For universal safety rules and update priority order, see `/shared-deps-safety`. iOS addition: prefer exact versions for production.

## Output

### Check output
```
Package dependencies:

Up to date:
  - swift-argument-parser 1.2.3

Updates available:
  - Alamofire: 5.8.0 → 5.9.1 (minor)
  - Kingfisher: 7.10.0 → 8.0.0 (major ⚠️)
```

### Audit output
```
Security audit:

No known vulnerabilities found.

Recommendations:
- Kingfisher: Consider updating to 8.x for iOS 17 improvements
```

## Reference
For SPM commands and common packages, see `reference/ios-deps-reference.md`
