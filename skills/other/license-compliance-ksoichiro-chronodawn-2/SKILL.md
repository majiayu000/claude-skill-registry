---
name: license-compliance
description: LGPL-3.0 license compliance guidelines
---

# License Compliance

**Purpose**: Guide for ensuring LGPL-3.0 license compliance when developing Chrono Dawn mod.

**How it works**: This skill is automatically activated when you mention tasks related to:
- Adding new dependencies to the project
- Checking license compatibility
- Preparing for mod distribution
- Reviewing third-party licenses
- Adding license headers to source files

Simply describe what you want to do, and Claude will reference the appropriate guidance from this skill.

---

## Project License

**Project License**: LGPL-3.0 (GNU Lesser General Public License v3.0)

**CRITICAL**: This project is licensed under LGPL-3.0. All contributions and modifications must comply with LGPL-3.0 terms.

---

## LGPL-3.0 Key Requirements

### 1. Copyleft

Derivative works must remain LGPL-3.0 (or compatible license)

### 2. Source Code Availability

Source code must be made available to users

### 3. License Notice

Include LGPL-3.0 license notice in distributions

### 4. Dynamic Linking

Mods using this code via dynamic linking (normal Minecraft mod usage) can use any license

**Example**: A mod that depends on Chrono Dawn as a library can be proprietary

### 5. Static Linking/Modification

Modified versions or statically linked code must be LGPL-3.0

**Example**: Forking Chrono Dawn and modifying source code requires LGPL-3.0 licensing

---

## Adding Dependencies

### License Compatibility Check

When adding dependencies, verify license is LGPL-3.0 compatible:

**Compatible Licenses** (can use):
- MIT License
- Apache 2.0 License
- BSD License (2-clause, 3-clause)
- LGPL-3.0 or LGPL-2.1
- Public Domain

**Incompatible Licenses** (avoid):
- Creative Commons Non-Commercial (CC-BY-NC)
- Proprietary licenses
- GPL-3.0 (only if statically linking; dynamic linking is OK)

### Documentation Requirement

Document all third-party licenses in `THIRD_PARTY_LICENSES.md`:

**Required Information**:
1. Project name
2. Version
3. Developer/Organization
4. License type
5. Project URL
6. License URL

**Where to Find License Info**:
- GitHub repository `LICENSE` file
- Maven Central / CurseForge / Modrinth project page
- Project website
- Source code headers

---

## License Headers in Source Files

**Optional but Recommended**:

Add license headers to core implementation files:

**Files Requiring Headers**:
- Core implementation files in `common/src/main/java/com/chronodawn/`
- Platform-specific entry points in `fabric/` and `neoforge/`

**Header Template**:

```java
/*
 * This file is part of Chrono Dawn.
 *
 * Chrono Dawn is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * Chrono Dawn is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with Chrono Dawn. If not, see <https://www.gnu.org/licenses/>.
 */
```

**When to Add**:
- New core class files
- Significant modifications to existing files
- Files intended for distribution

---

## Distribution Checklist

Before distributing the mod (CurseForge, Modrinth, GitHub Releases):

- [ ] Verify `LICENSE` file contains LGPL-3.0 text
- [ ] Update `THIRD_PARTY_LICENSES.md` with all dependencies
- [ ] Check all dependencies are LGPL-3.0 compatible
- [ ] Confirm source code is publicly available (GitHub repository)
- [ ] Include license notice in mod metadata (`fabric.mod.json`, `neoforge.mods.toml`)
- [ ] (Optional) Add license headers to core source files

---

## License Change History

**2025-12-27**: Changed from "All Rights Reserved" to LGPL-3.0 (T601-T608)

**Rationale**: Patchouli dependency removed (T706), enabling FOSS (Free and Open Source Software) licensing

---

## Common Questions

### Q: Can I use Chrono Dawn as a library in my proprietary mod?

**A**: Yes. Dynamic linking (normal Minecraft mod dependency) allows any license. Your mod does not need to be LGPL-3.0.

### Q: Can I fork Chrono Dawn and sell it?

**A**: Yes, but your fork must remain LGPL-3.0. Users have the right to the source code. Selling LGPL software is allowed, but buyers can redistribute it freely.

### Q: Can I add a GPL-3.0 dependency?

**A**: Yes, if it's dynamically linked (modImplementation). Avoid statically linking (shadowing/bundling) GPL dependencies.

### Q: Do I need to add license headers to every file?

**A**: No, it's optional but recommended for core files. The `LICENSE` file is sufficient for basic compliance.

### Q: Can I contribute to Chrono Dawn without agreeing to LGPL-3.0?

**A**: No. All contributions must be LGPL-3.0 compatible. By contributing, you agree to license your code under LGPL-3.0.

---

## Resources

- **LGPL-3.0 Full Text**: https://www.gnu.org/licenses/lgpl-3.0.en.html
- **GNU Licenses Explained**: https://www.gnu.org/licenses/licenses.html
- **SPDX License List**: https://spdx.org/licenses/

---

**Last Updated**: 2026-01-16
**Maintained by**: Chrono Dawn Development Team
