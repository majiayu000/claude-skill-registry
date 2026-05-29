---
name: extension-api
description: Extension API for domain bundle discovery, module detection, and canonical command generation
allowed-tools: Read, Bash
---

# Extension API Skill

Unified API for domain bundle extensions providing module discovery, build system detection, and command generation. Provides the `ExtensionBase` abstract base class that all domain extensions must inherit from.

## Purpose

- **ExtensionBase ABC** - Abstract base class with required/optional methods
- **Canonical constants** - `CMD_*` constants for command names
- **Profile patterns** - `PROFILE_PATTERNS` vocabulary for classification
- **Discovery utilities** - Loading and discovering extensions
- **Build utilities** - Module discovery, log file management, issue parsing

## When to Reference This Skill

Reference when:
- Creating a new `extension.py` for a domain bundle
- Implementing `discover_modules()` for a build system
- Understanding canonical command names and resolution
- Parsing build output and handling issues

## Skill Structure

```
extension-api/
├── SKILL.md                        # This file
├── scripts/
│   ├── extension_base.py           # ExtensionBase ABC, canonical commands
│   ├── extension.py                # Extension discovery, loading, aggregation
│   ├── build_discover.py           # Module discovery, path building
│   ├── build_result.py             # Log file creation, result construction
│   └── build_parse.py              # Issue structures, warning filtering
└── standards/
    ├── extension-contract.md       # Extension API contract
    ├── canonical-commands.md       # Command vocabulary and resolution
    ├── config-callback.md          # Project configuration callback
    ├── build-base-libs.md          # Base library API reference (optional)
    ├── build-execution.md          # Execution patterns (optional)
    ├── build-return.md             # Return value structure (optional)
    ├── build-project-structure.md  # Module discovery output (optional)
    └── architecture-overview.md    # System architecture (optional)
```

---

## Quick Reference

All extensions **must** inherit from `ExtensionBase` and implement required methods.

### Required Methods (Abstract)

| Method | Purpose |
|--------|---------|
| `get_skill_domains() -> dict` | Return domain metadata with profiles |

### Primary Methods

| Method | Default | Purpose |
|--------|---------|---------|
| `discover_modules(project_root: str) -> list` | `[]` | Discover modules with paths, metadata, stats, commands |

### Optional Methods (With Defaults)

| Method | Default | Purpose |
|--------|---------|---------|
| `config_defaults(project_root: str) -> None` | no-op | Configure project defaults (called during init) |
| `provides_triage() -> str \| None` | `None` | Return triage skill reference |
| `provides_outline() -> str \| None` | `None` | Return outline skill reference |

---

## Architecture (Optional)

For understanding the complete system architecture, reference these documents:

| Document | Purpose | When to Read |
|----------|---------|--------------|
| [architecture-overview.md](standards/architecture-overview.md) | System flow, data dependencies | Understanding overall data flow |
| [config-callback.md](standards/config-callback.md) | Project configuration callback | Implementing `config_defaults()` |
| [build-base-libs.md](standards/build-base-libs.md) | Base library API reference | Implementing extension scripts |
| [build-execution.md](standards/build-execution.md) | Execution patterns | Running build commands |
| [build-return.md](standards/build-return.md) | Return value structure | Formatting command output |
| [build-project-structure.md](standards/build-project-structure.md) | Module discovery output | Implementing `discover_modules()` |
| [orchestrator-integration.md](../analyze-project-architecture/standards/orchestrator-integration.md) | Orchestrator merge logic | Understanding hybrid modules |

**Note**: These documents define the target architecture. Implementation may be in progress.

---

## Scripts

| Script | Type | Purpose |
|--------|------|---------|
| `extension_base.py` | Library | ExtensionBase ABC, canonical commands, profile patterns |
| `extension.py` | Library + CLI | Extension discovery, loading, aggregation, config defaults |
| `build_discover.py` | Library | Module discovery, path building, README detection |
| `build_result.py` | Library | Log file creation, result dict construction |
| `build_parse.py` | Library | Issue structures, warning filtering |

### CLI Commands

The `extension.py` script provides CLI commands for extension operations:

```bash
# Apply config_defaults() callback for all extensions
python3 .plan/execute-script.py plan-marshall:extension-api:extension apply-config-defaults
```

**Output (TOON)**:
```toon
status	success
extensions_called	3
extensions_skipped	2
errors_count	0
```

### Python Import Usage

Scripts can import discovery functions directly:

```python
import sys
from pathlib import Path

# Add extension-api scripts to path
extension_api_path = Path(__file__).parent.parent.parent / "extension-api" / "scripts"
sys.path.insert(0, str(extension_api_path))

from extension import (
    discover_all_extensions,
    discover_project_modules,
    get_build_systems_from_extensions,
    get_skill_domains_from_extensions,
    apply_config_defaults,
)

from build_discover import (
    discover_descriptors,
    build_module_base,
    find_readme,
)

from build_result import (
    create_log_file,
    success_result,
    error_result,
)

from build_parse import (
    Issue,
    filter_warnings,
    partition_issues,
)
```

---

## Canonical Command Constants

Import from `extension_base` for type-safe command references:

```python
from extension_base import (
    CMD_CLEAN,             # "clean"
    CMD_COMPILE,           # "compile"
    CMD_TEST_COMPILE,      # "test-compile"
    CMD_MODULE_TESTS,      # "module-tests"
    CMD_INTEGRATION_TESTS, # "integration-tests"
    CMD_COVERAGE,          # "coverage"
    CMD_BENCHMARK,         # "benchmark"
    CMD_QUALITY_GATE,      # "quality-gate"
    CMD_VERIFY,            # "verify"
    CMD_INSTALL,           # "install"
    CMD_CLEAN_INSTALL,     # "clean-install"
    CMD_PACKAGE,           # "package"
    ALL_CANONICAL_COMMANDS,
    PROFILE_PATTERNS,      # Profile ID to canonical mapping (for internal use)
)
```

| Constant | Value | Required | Description |
|----------|-------|----------|-------------|
| `CMD_CLEAN` | `clean` | No | Remove build artifacts |
| `CMD_QUALITY_GATE` | `quality-gate` | Yes | Static analysis, linting |
| `CMD_VERIFY` | `verify` | Yes* | Full verification (*non-pom modules) |
| `CMD_MODULE_TESTS` | `module-tests` | Conditional | Unit tests (if tests exist) |
| `CMD_COMPILE` | `compile` | No | Compile production sources |
| `CMD_TEST_COMPILE` | `test-compile` | No | Compile test sources |
| `CMD_INTEGRATION_TESTS` | `integration-tests` | No | Integration tests |
| `CMD_COVERAGE` | `coverage` | No | Coverage measurement |
| `CMD_BENCHMARK` | `benchmark` | No | Benchmark/performance tests |
| `CMD_INSTALL` | `install` | No | Install to local repository |
| `CMD_CLEAN_INSTALL` | `clean-install` | No | Clean and install combined |
| `CMD_PACKAGE` | `package` | No | Create deployable artifact |

**Note**: `clean` is a separate command. Other commands do NOT include clean goal.

See [canonical-commands.md](standards/canonical-commands.md) for command resolution logic.

---

## Minimal Extension Template

```python
#!/usr/bin/env python3
"""Extension API for {bundle-name} bundle."""

from pathlib import Path
from extension_base import ExtensionBase


class Extension(ExtensionBase):
    """Extension for {bundle-name} bundle."""

    def get_skill_domains(self) -> dict:
        """Domain metadata for skill loading."""
        return {
            "domain": {
                "key": "domain-key",
                "name": "Domain Name",
                "description": "Domain description"
            },
            "profiles": {
                "core": {"defaults": [], "optionals": []},
                "implementation": {"defaults": [], "optionals": []},
                "testing": {"defaults": [], "optionals": []},
                "quality": {"defaults": [], "optionals": []}
            }
        }

    def discover_modules(self, project_root: str) -> list:
        """Discover modules in the project.

        Returns list of module dicts with:
        - name, build_systems, paths, metadata, packages, dependencies, stats, commands
        """
        # Find descriptors
        from build_discover import discover_descriptors, build_module_base
        descriptors = discover_descriptors(project_root, "descriptor-file")

        modules = []
        for desc_path in descriptors:
            base = build_module_base(project_root, desc_path)
            # Enrich with extension-specific metadata, stats, commands
            modules.append({
                "name": base.name,
                "build_systems": ["my-build-system"],
                "paths": base.paths.to_dict(),
                "metadata": {},
                "packages": {},
                "dependencies": [],
                "stats": {"source_files": 0, "test_files": 0},
                "commands": self._resolve_commands(base)
            })
        return modules
```

---

## Integration Points

- **project-structure** - Orchestrates extensions, owns `.plan/*.json` files
- **plan-marshall-config** - Uses `discover_all_extensions()` for domain configuration
- **Domain bundles** - Implement `extension.py` inheriting from `ExtensionBase`

---

## References

- `standards/extension-contract.md` - Extension API contract (required)
- `standards/canonical-commands.md` - Command vocabulary and resolution (required)
- `standards/config-callback.md` - Project configuration callback (required)
- `standards/build-base-libs.md` - Base library API reference (optional)
- `standards/architecture-overview.md` - System architecture (optional)
