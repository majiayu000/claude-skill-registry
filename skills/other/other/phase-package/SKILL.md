---
name: phase-package
description: "Create distributable packages including .mojopkg files and archives. Use during package phase to prepare components for distribution."
mcp_fallback: none
category: phase
phase: Package
user-invocable: false
---

# Package Phase Coordination Skill

Create distributable packages including Mojo packages (.mojopkg), archives, and installation procedures.

## When to Use

- Starting package phase (after Plan completes)
- Running in parallel with Test and Implementation phases
- Preparing components for distribution and reuse
- Creating installable packages or release artifacts

## Quick Reference

```bash
# Build Mojo package
pixi run mojo build -o packages/module.mojopkg shared/module/

# Create distribution archive
tar -czf dist/ProjectOdyssey-v0.1.0.tar.gz packages/ examples/ README.md

# Test installation
pixi run mojo run -I packages test_import.mojo
```

## Workflow

1. **Build packages** - Compile Mojo modules to `.mojopkg` files
2. **Create archives** - Package distributions (tar.gz, zip)
3. **Write installation docs** - Document setup procedures
4. **Test installation** - Verify in clean environment
5. **Create CI workflow** - Automate packaging in GitHub Actions
6. **Generate metadata** - Version info, dependencies, etc.

## Package Structure

**Input (module source)**:

```text
shared/tensor/
├── __init__.mojo
├── ops.mojo
└── types.mojo
```

**Output (packaged module)**:

```text
packages/
├── tensor.mojopkg
├── nn.mojopkg
└── utils.mojopkg
```

**Distribution archive**:

```text
ProjectOdyssey-v0.1.0/
├── packages/
├── examples/
├── docs/
├── README.md
├── LICENSE
└── INSTALL.md
```

## Build Configuration

**Mojo package build**:

```bash
# Single module
mojo build -o packages/tensor.mojopkg shared/tensor/

# All modules (in loop or script)
for module in shared/*/; do
    mojo build -o packages/$(basename $module).mojopkg "$module"
done
```

**Archive creation**:

```bash
# Tar.gz (Linux/Mac)
tar -czf dist/ProjectOdyssey-v0.1.0.tar.gz packages/ examples/ docs/

# Zip (cross-platform)
zip -r dist/ProjectOdyssey-v0.1.0.zip packages/ examples/ docs/
```

## Quality Checklist

Before marking package complete:

- [ ] All modules compile without warnings
- [ ] Package can be imported in test script
- [ ] Examples run correctly
- [ ] README and INSTALL.md included
- [ ] LICENSE file present
- [ ] Version tagged correctly
- [ ] No compilation warnings
- [ ] Dependencies documented

## Phase Dependencies

- **Input from**: Plan phase (deliverables and success criteria)
- **Parallel with**: Test phase (TDD) and Implementation phase
- **Precedes**: Cleanup phase (after parallel phases complete)

## Output Location

- **Packages**: `/packages/<module>.mojopkg`
- **Archives**: `/dist/<version>.tar.gz`, `.zip`
- **Documentation**: GitHub issue comments
- **Release artifacts**: GitHub releases section (after cleanup)

## Error Handling

| Error | Fix |
|-------|-----|
| Build fails | Check syntax, verify all files in module |
| Import fails | Verify `__init__.mojo` exports, check paths |
| Archive corrupted | Recreate archive, verify contents |
| Installation fails | Check permissions, test script paths |
| Missing files | Verify all deliverables before packaging |

## References

- `CLAUDE.md` - "Package Phase" in 5-phase workflow
- `.github/workflows/` - Example CI workflows
- `pixi.toml` - Build configuration and tasks

---

**Key Principle**: Package only what's been tested and approved. No untested code in releases.
