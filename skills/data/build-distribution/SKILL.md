---
name: build-distribution
description: App build, code signing, TestFlight, and App Store distribution for all Apple platforms. Use when preparing releases, configuring signing, uploading to TestFlight, or submitting to App Store.
versions:
  xcode: 26
user-invocable: false
references: references/code-signing.md, references/testflight.md, references/app-store.md, references/app-icons.md
related-skills: swift-core, ios, macos, mcp-tools
---

# Build & Distribution

App build, signing, and distribution for all Apple platforms.

## Agent Workflow (MANDATORY)

Before ANY distribution, launch in parallel:

1. **fuse-ai-pilot:explore-codebase** - Check existing build configuration
2. **fuse-ai-pilot:research-expert** - Verify latest App Store requirements
3. **mcp__XcodeBuildMCP__show_build_settings** - Review build settings

After implementation, run **fuse-ai-pilot:sniper** for validation.

---

## Overview

### When to Use

- Preparing app for release
- Configuring code signing
- Uploading to TestFlight
- Submitting to App Store
- Creating app icons
- CI/CD pipeline setup

### Why Build Distribution Skill

| Feature | Benefit |
|---------|---------|
| Automatic signing | Simplifies certificate management |
| TestFlight | Beta testing with users |
| App Store | Public distribution |
| CI/CD | Automated releases |

---

## Reference Guide

| Need | Reference |
|------|-----------|
| Certificates, profiles | [code-signing.md](references/code-signing.md) |
| Beta testing | [testflight.md](references/testflight.md) |
| App Store submission | [app-store.md](references/app-store.md) |
| Icons, assets | [app-icons.md](references/app-icons.md) |

---

## Release Checklist

- [ ] Version and build number updated
- [ ] App icons complete (light/dark/tinted)
- [ ] Privacy manifest (PrivacyInfo.xcprivacy)
- [ ] Release configuration
- [ ] Archive validates
- [ ] TestFlight tested
- [ ] Screenshots updated
- [ ] App Store metadata complete

---

## Best Practices

1. **Automatic signing** - Let Xcode manage
2. **TestFlight first** - Always beta test
3. **Increment build** - Every upload needs new build number
4. **Privacy manifest** - Required for App Store
5. **fastlane** - Automate repetitive tasks
6. **CI/CD** - GitHub Actions for automation
