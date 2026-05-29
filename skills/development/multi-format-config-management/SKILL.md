---
name: multi-format-config-management
description: Implement configuration management supporting TOML/YAML/JSON formats with inheritance and runtime overrides
license: MIT
compatibility: opencode,claude
metadata:
  created_at: "2026-01-29T22:56:19.276Z"
  updated_at: "2026-01-29T22:56:19.276Z"
  version: "1"
  tags: "config,parsing,yaml,toml,json,inheritance,overrides"
  category: "infrastructure"
  complexity: "medium"
---
<!-- BEGIN:compound:skill-managed -->
# Purpose
Implement comprehensive configuration management that supports multiple file formats (TOML, YAML, JSON), environment inheritance, and runtime CLI overrides.

# When To Use
- User requests configuration management with multi-format support
- User needs config inheritance between environments
- User requires runtime configuration overrides
- Ticket specifies "config file formats" as a requirement

# Architecture
## Format Detection
- Search for config files in preference order: TOML → YAML → JSON
- Detect format from file extension (.toml, .yaml, .yml, .json)
- Map extensions to appropriate parsers: tomllib, yaml.safe_load, json.load
- Provide helpful error messages indicating which format failed

## Configuration Loading
```python
from pathlib import Path
import tomllib
import json

try:
    import yaml
    from yaml import YAMLError
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False
    YAMLError = type("YAMLError")

def _load_file_data(path: Path) -> dict[str, Any]:
    suffix = path.suffix.lower()

    if suffix == ".toml":
        with path.open("rb") as f:
            return tomllib.load(f)
    elif suffix in (".yaml", ".yml"):
        if not YAML_AVAILABLE:
            raise ValueError("YAML support requires PyYAML")
        with path.open("r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    elif suffix == ".json":
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    else:
        raise ValueError(f"Unsupported format: {suffix}")

def find_config_file(search_path: Path | None = None) -> Path | None:
    search_path = search_path or Path.cwd()
    config_names = [
        "vibepiper.toml",
        "vibepiper.yaml",
        "vibepiper.yml",
        "vibepiper.json",
    ]

    for path in [search_path, *search_path.parents]:
        for config_name in config_names:
            config_file = path / config_name
            if config_file.exists():
                return config_file
    return None
```

## Exception Handling for Strict MyPy
- Catch general Exception, then use isinstance() to distinguish specific errors:
```python
try:
    data = _load_file_data(path)
except Exception as e:
    if isinstance(e, (tomllib.TOMLDecodeError, json.JSONDecodeError, YAMLError)):
        msg = f"Invalid {_get_format_name(path)} syntax"
    else:
        msg = "Failed to read configuration file"
    raise ConfigLoadError(msg, path=path, cause=e) from e
```

## Environment Inheritance
### Two-Pass Parsing
1. First pass: Parse all environment configs into dictionary
2. Extract `inherits` field from each environment
3. Second pass: Merge child with parent using inheritance chain

### Merge Logic
- Child values override parent values
- Unspecified fields inherit from parent
- Use `_merge_additional_config()` for custom fields
```python
def _merge_additional_config(parent: dict[str, Any], child: dict[str, Any]) -> dict[str, Any]:
    merged = parent.copy()
    merged.update(child)
    return merged

# Inheritance parsing
environments_data = data.get("environments", {})

# First pass: parse all
for env_name, env_data in environments_data.items():
    environments[env_name] = EnvironmentConfig(...)

# Second pass: apply inheritance
for env_name, env_data in environments_data.items():
    inherits_from = env_data.get("inherits")
    if inherits_from:
        if inherits_from not in environments:
            raise ValueError(f"Environment '{env_name}' inherits from '{inherits_from}' which doesn't exist")

        parent_env = environments[inherits_from]
        child_env = environments[env_name]

        environments[env_name] = EnvironmentConfig(
            io_manager=child_env.io_manager or parent_env.io_manager,
            log_level=child_env.log_level or parent_env.log_level,
            parallelism=child_env.parallelism or parent_env.parallelism,
            bucket=child_env.bucket or parent_env.bucket,
            region=child_env.region or parent_env.region,
            endpoint=child_env.endpoint or parent_env.endpoint,
            credentials_path=child_env.credentials_path or parent_env.credentials_path,
            additional_config=_merge_additional_config(
                parent_env.additional_config,
                child_env.additional_config
            ),
        )
```

## Runtime Overrides
### Architecture
- Store CLI overrides separately in Config object
- Add `apply_overrides` parameter to `get_environment()` method
- Create `_apply_overrides()` method that returns new merged config

### Merge Implementation
```python
def get_environment(self, env_name: str, apply_overrides: bool = True) -> EnvironmentConfig:
    env_config = self.environments[env_name]

    if apply_overrides and self.cli_overrides:
        return self._apply_overrides(env_config)

    return env_config

def _apply_overrides(self, env_config: EnvironmentConfig) -> EnvironmentConfig:
    overrides = self.cli_overrides

    known_fields = {
        "io_manager", "log_level", "parallelism",
        "bucket", "region", "endpoint", "credentials_path",
    }
    additional_config = env_config.additional_config.copy()
    additional_config.update(
        {k: v for k, v in overrides.items() if k not in known_fields}
    )

    return EnvironmentConfig(
        io_manager=overrides.get("io_manager", env_config.io_manager),
        log_level=overrides.get("log_level", env_config.log_level),
        parallelism=overrides.get("parallelism", env_config.parallelism),
        bucket=overrides.get("bucket", env_config.bucket),
        region=overrides.get("region", env_config.region),
        endpoint=overrides.get("endpoint", env_config.endpoint),
        credentials_path=overrides.get("credentials_path", env_config.credentials_path),
        additional_config=additional_config,
    )
```

## Validation
### Cloud Storage Validation
```python
def _validate_environment_config(config: Config, env_name: str, env_config: Any) -> None:
    # Validate cloud storage configuration
    if env_config.io_manager in ("s3", "gcs", "azure") and not env_config.bucket:
        msg = f"Bucket is required for io_manager '{env_config.io_manager}'"
        raise ConfigValidationError(msg, field=f"environments.{env_name}.bucket")
```

### Dependencies
- Add `pyyaml>=6.0.0` to runtime dependencies
- Add `types-PyYAML>=6.0.0` to dev dependencies for MyPy

## Testing
### Test Structure
- **Multi-format tests**: Test loading TOML, YAML, JSON configs with valid/invalid syntax
- **Inheritance tests**: Test simple inheritance, inheritance with additional config, inheritance across formats
- **Override tests**: Test overriding all config fields, multiple overrides, overrides with/without apply_overrides
- Test validation errors (missing bucket, invalid log level, etc.)

### Examples
```toml
# vibepiper.toml - Inheritance example
[project]
name = "my-pipeline"
version = "0.1.0"

[environments.base]
io_manager = "s3"
bucket = "base-bucket"
region = "us-east-1"

[environments.prod]
inherits = "base"
log_level = "warning"
```

```yaml
# vibepiper.yaml - Same in YAML
project:
  name: "my-pipeline"
  version: "0.1.0"

environments:
  base:
    io_manager: s3
    bucket: "base-bucket"
    region: "us-east-1"

  prod:
    inherits: base
    log_level: warning
```

```python
# Runtime overrides example
from vibe_piper.config import load_config

config = load_config(
    "vibepiper.toml",
    cli_overrides={"io_manager": "s3", "bucket": "override-bucket"}
)

# Get environment with overrides applied
prod_env = config.get_environment("prod", apply_overrides=True)
print(f"IO Manager: {prod_env.io_manager}")
print(f"Bucket: {prod_env.bucket}")  # Uses override
```

## Acceptance Criteria
- [ ] Support TOML, YAML, JSON configuration formats
- [ ] Auto-detect format from file extension
- [ ] Search for config files in preference order
- [ ] Implement environment inheritance with 'inherits' field
- [ ] Support multi-level inheritance (grandparent → parent → child)
- [ ] Merge child values with parent values correctly
- [ ] Implement runtime CLI overrides
- [ ] Add apply_overrides parameter to get_environment()
- [ ] Preserve environment-specific values not being overridden
- [ ] Add comprehensive tests for all features
- [ ] Pass MyPy strict mode with proper type hints
- [ ] Update module documentation with examples
- [ ] Add PyYAML and types-PyYAML dependencies

## Gotchas
- YAML parsing requires pyyaml to be installed - provide clear error message
- MyPy requires types-PyYAML for YAML imports - add to dev dependencies
- Inheritance chains should not contain cycles - validation needed
- Runtime overrides should not modify stored config - create new merged objects
- File extension check should be case-insensitive (.TOML == .toml)
- JSON.load() returns Any type - use type: ignore[no-any-return] for strict MyPy

## Related Patterns
- See author-agents-md-uv-python for project setup conventions
- See loom-manager-workflow for ticket management patterns
<!-- END:compound:skill-managed -->

## Manual notes

_This section is preserved when the skill is updated. Put human notes, caveats, and exceptions here._
