---
name: xdg-base-directory
description: When an application needs to store config, data, cache, or state files. When designing where user-specific files should live. When code writes to ~/.appname or hardcoded home paths. When implementing cross-platform file storage with platformdirs.
---

# XDG Base Directory Specification

Implement standardized directory paths for configuration, data, cache, and state files following the XDG Base Directory Specification.

## When to Use This Skill

Use this skill when:

- Creating CLI tools or applications that store user-specific files
- Implementing configuration file management for Linux/Unix applications
- Building cross-platform Python applications requiring standardized directory paths
- Migrating legacy applications from `~/.appname` to XDG-compliant paths
- Designing file storage architecture for Python packages
- Implementing proper environment variable handling for user directories
- Writing applications that respect user-configured directory preferences
- Testing applications with custom XDG directory overrides

## Core Specification Rules

The XDG Base Directory Specification (version 0.8, May 2021) defines these critical requirements:

### 1. All Paths Must Be Absolute

Environment variable values MUST be absolute paths. Relative paths are invalid and MUST be ignored.

```python
def validate_xdg_path(path_str: str | None) -> Path | None:
    """Validate XDG path is absolute per specification."""
    if not path_str:
        return None
    path = Path(path_str)
    if not path.is_absolute():
        return None  # Ignore relative paths per spec
    return path
```

### 2. Empty Variables Use Defaults

When an environment variable is unset or empty, use the specification-defined default value.

### 3. Priority Order for Search Paths

- User-specific directories (`$XDG_CONFIG_HOME`, `$XDG_DATA_HOME`) take precedence
- System directories (`$XDG_CONFIG_DIRS`, `$XDG_DATA_DIRS`) searched in order
- First match wins

### 4. Colon Separator for Search Paths

`$XDG_DATA_DIRS` and `$XDG_CONFIG_DIRS` use colon (`:`) as path separator, similar to `$PATH`.

## Environment Variables

### User-Specific Directories (Single Path)

| Variable | Purpose | Default | Use For |
| --- | --- | --- | --- |
| `$XDG_CONFIG_HOME` | User configuration files | `$HOME/.config` | Settings, preferences, user configs |
| `$XDG_DATA_HOME` | User data files | `$HOME/.local/share` | Databases, generated content, persistent data |
| `$XDG_STATE_HOME` | User state files | `$HOME/.local/state` | Logs, history, undo buffers, recent files |
| `$XDG_CACHE_HOME` | User cache files | `$HOME/.cache` | Temporary data, downloaded files, build artifacts |
| `$XDG_RUNTIME_DIR` | User runtime files | System-set (`/run/user/$UID`) | Sockets, pipes, lock files, IPC |

### System-Wide Directories (Search Paths)

| Variable           | Purpose                   | Default                         |
| ------------------ | ------------------------- | ------------------------------- |
| `$XDG_DATA_DIRS`   | System data search path   | `/usr/local/share/:/usr/share/` |
| `$XDG_CONFIG_DIRS` | System config search path | `/etc/xdg`                      |

### User Executables (Convention, Not XDG)

| Path               | Purpose                        |
| ------------------ | ------------------------------ |
| `$HOME/.local/bin` | User-specific executable files |

**Note**: Distributions should ensure `$HOME/.local/bin` appears in `$PATH`.

## Directory Selection Guide

Choose the appropriate directory based on data characteristics:

**Use `$XDG_CONFIG_HOME` for:**

- Application settings and preferences
- User-specific configuration files
- TOML/YAML/JSON configuration
- Example: `~/.config/myapp/config.toml`

**Use `$XDG_DATA_HOME` for:**

- Persistent application data
- User-generated content
- Downloaded models or assets
- Database files
- Example: `~/.local/share/myapp/models/model.gguf`

**Use `$XDG_STATE_HOME` for:**

- Action history (command history, undo buffers)
- Application state that can be regenerated
- Recently used files lists
- Log files specific to user actions
- Example: `~/.local/state/myapp/history.log`

**Use `$XDG_CACHE_HOME` for:**

- Temporary files safe to delete
- Downloaded data that can be re-fetched
- Build artifacts and compiled files
- Thumbnail caches
- Example: `~/.cache/myapp/downloads/`

**Use `$XDG_RUNTIME_DIR` for:**

- Unix domain sockets
- Named pipes (FIFOs)
- Lock files
- Temporary IPC files
- **Warning**: Often tmpfs-mounted with size limits; avoid large files
- **Warning**: Cleaned on logout; do not store persistent data
- Example: `/run/user/1000/myapp/socket`

## Python Implementation Patterns

### Stdlib-Only Implementation

Use for applications targeting only Linux/Unix systems or requiring no dependencies.

```python
"""XDG Base Directory compliant path management using stdlib only."""
from pathlib import Path
import os


def get_config_home() -> Path:
    """Get XDG_CONFIG_HOME path.

    Returns user-specific configuration directory.
    Falls back to $HOME/.config if XDG_CONFIG_HOME unset or relative.
    """
    xdg = os.environ.get('XDG_CONFIG_HOME')
    if xdg and Path(xdg).is_absolute():
        return Path(xdg)
    return Path.home() / '.config'


def get_data_home() -> Path:
    """Get XDG_DATA_HOME path.

    Returns user-specific data directory.
    Falls back to $HOME/.local/share if XDG_DATA_HOME unset or relative.
    """
    xdg = os.environ.get('XDG_DATA_HOME')
    if xdg and Path(xdg).is_absolute():
        return Path(xdg)
    return Path.home() / '.local' / 'share'


def get_state_home() -> Path:
    """Get XDG_STATE_HOME path.

    Returns user-specific state directory.
    Falls back to $HOME/.local/state if XDG_STATE_HOME unset or relative.
    """
    xdg = os.environ.get('XDG_STATE_HOME')
    if xdg and Path(xdg).is_absolute():
        return Path(xdg)
    return Path.home() / '.local' / 'state'


def get_cache_home() -> Path:
    """Get XDG_CACHE_HOME path.

    Returns user-specific cache directory.
    Falls back to $HOME/.cache if XDG_CACHE_HOME unset or relative.
    """
    xdg = os.environ.get('XDG_CACHE_HOME')
    if xdg and Path(xdg).is_absolute():
        return Path(xdg)
    return Path.home() / '.cache'


def get_runtime_dir() -> Path | None:
    """Get XDG_RUNTIME_DIR path.

    Returns user-specific runtime directory, or None if not set.
    This variable has no default - it must be set by the system.
    """
    xdg = os.environ.get('XDG_RUNTIME_DIR')
    if xdg and Path(xdg).is_absolute():
        return Path(xdg)
    return None


def get_config_dirs() -> list[Path]:
    """Get XDG_CONFIG_DIRS as list of paths.

    Returns preference-ordered list of system configuration directories.
    Falls back to [Path('/etc/xdg')] if XDG_CONFIG_DIRS unset.
    """
    xdg = os.environ.get('XDG_CONFIG_DIRS')
    if xdg:
        paths = [Path(p) for p in xdg.split(':') if p and Path(p).is_absolute()]
        if paths:
            return paths
    return [Path('/etc/xdg')]


def get_data_dirs() -> list[Path]:
    """Get XDG_DATA_DIRS as list of paths.

    Returns preference-ordered list of system data directories.
    Falls back to [Path('/usr/local/share'), Path('/usr/share')] if unset.
    """
    xdg = os.environ.get('XDG_DATA_DIRS')
    if xdg:
        paths = [Path(p) for p in xdg.split(':') if p and Path(p).is_absolute()]
        if paths:
            return paths
    return [Path('/usr/local/share'), Path('/usr/share')]
```

### Application-Specific Path Module

Create a dedicated paths module for your application:

```python
"""Path management for myapp following XDG specification."""
from pathlib import Path
import os

APP_NAME = 'myapp'


def get_config_dir() -> Path:
    """Get myapp config directory."""
    xdg = os.environ.get('XDG_CONFIG_HOME')
    base = Path(xdg) if xdg and Path(xdg).is_absolute() else Path.home() / '.config'
    return base / APP_NAME


def get_config_file() -> Path:
    """Get myapp config file path."""
    return get_config_dir() / 'config.toml'


def get_data_dir() -> Path:
    """Get myapp data directory."""
    xdg = os.environ.get('XDG_DATA_HOME')
    base = Path(xdg) if xdg and Path(xdg).is_absolute() else Path.home() / '.local' / 'share'
    return base / APP_NAME


def get_cache_dir() -> Path:
    """Get myapp cache directory."""
    xdg = os.environ.get('XDG_CACHE_HOME')
    base = Path(xdg) if xdg and Path(xdg).is_absolute() else Path.home() / '.cache'
    return base / APP_NAME


def get_state_dir() -> Path:
    """Get myapp state directory."""
    xdg = os.environ.get('XDG_STATE_HOME')
    base = Path(xdg) if xdg and Path(xdg).is_absolute() else Path.home() / '.local' / 'state'
    return base / APP_NAME


def ensure_directories() -> None:
    """Create all required directories with appropriate permissions."""
    for directory in [get_config_dir(), get_data_dir(), get_cache_dir(), get_state_dir()]:
        directory.mkdir(parents=True, exist_ok=True)
```

### Cross-Platform Implementation with platformdirs

For applications targeting Linux, macOS, and Windows, use the `platformdirs` library:

```python
"""Cross-platform path management using platformdirs."""
from platformdirs import user_config_dir, user_data_dir, user_cache_dir, user_state_dir
from pathlib import Path

APP_NAME = 'myapp'
APP_AUTHOR = 'myapp'  # Used on Windows

# Get platform-appropriate directories
# Linux: Uses XDG specification
# macOS: Uses ~/Library/Application Support, ~/Library/Caches
# Windows: Uses %APPDATA%, %LOCALAPPDATA%

config_dir = Path(user_config_dir(APP_NAME, APP_AUTHOR))
data_dir = Path(user_data_dir(APP_NAME, APP_AUTHOR))
cache_dir = Path(user_cache_dir(APP_NAME, APP_AUTHOR))
state_dir = Path(user_state_dir(APP_NAME, APP_AUTHOR))

# Auto-create directories
config_dir = Path(user_config_dir(APP_NAME, APP_AUTHOR, ensure_exists=True))
```

**Platform-specific paths:**

| Platform | Config | Data | Cache | State |
| --- | --- | --- | --- | --- |
| Linux | `~/.config/myapp` | `~/.local/share/myapp` | `~/.cache/myapp` | `~/.local/state/myapp` |
| macOS | `~/Library/Application Support/myapp` | `~/Library/Application Support/myapp` | `~/Library/Caches/myapp` | `~/Library/Application Support/myapp` |
| Windows | `C:\Users\<user>\AppData\Local\myapp\myapp` | `C:\Users\<user>\AppData\Local\myapp\myapp` | `C:\Users\<user>\AppData\Local\myapp\myapp\Cache` | `C:\Users\<user>\AppData\Local\myapp\myapp` |

**When to use platformdirs:**

- Application targets multiple operating systems
- Need native platform conventions (macOS `~/Library`, Windows `%APPDATA%`)
- Want automatic directory creation with `ensure_exists=True`

**When to use stdlib-only:**

- Application targets only Linux/Unix
- Minimize dependencies
- Need complete control over path resolution logic

## Common Anti-Patterns

### 1. Using `~/.appname` (Legacy Pattern)

**Problem**: Violates XDG specification, clutters home directory.

```python
# ❌ WRONG
config_file = Path.home() / '.myapp' / 'config.toml'
```

**Solution**: Use `~/.config/appname/`

```python
# ✅ CORRECT
def get_config_dir() -> Path:
    xdg = os.environ.get('XDG_CONFIG_HOME')
    base = Path(xdg) if xdg and Path(xdg).is_absolute() else Path.home() / '.config'
    return base / 'myapp'

config_file = get_config_dir() / 'config.toml'
```

### 2. Ignoring Environment Variables

**Problem**: Hardcoded paths prevent user customization.

```python
# ❌ WRONG
config_dir = Path.home() / '.config' / 'myapp'
```

**Solution**: Always check environment variables first.

```python
# ✅ CORRECT
xdg = os.environ.get('XDG_CONFIG_HOME')
base = Path(xdg) if xdg and Path(xdg).is_absolute() else Path.home() / '.config'
config_dir = base / 'myapp'
```

### 3. Accepting Relative Paths

**Problem**: XDG specification mandates absolute paths only.

```python
# ❌ WRONG
xdg = os.environ.get('XDG_CONFIG_HOME', str(Path.home() / '.config'))
return Path(xdg)  # Accepts relative paths
```

**Solution**: Validate absolute paths, fall back to default for relative.

```python
# ✅ CORRECT
xdg = os.environ.get('XDG_CONFIG_HOME')
if xdg and Path(xdg).is_absolute():
    return Path(xdg)
return Path.home() / '.config'  # Default for unset or relative
```

### 4. Missing Directory Creation

**Problem**: Writing files without ensuring parent directories exist.

```python
# ❌ WRONG
config_file = get_config_dir() / 'config.toml'
config_file.write_text(data)  # Fails if directory doesn't exist
```

**Solution**: Create directories before writing files.

```python
# ✅ CORRECT
config_file = get_config_dir() / 'config.toml'
config_file.parent.mkdir(parents=True, exist_ok=True)
config_file.write_text(data)
```

### 5. Storing Cache in Config Directory

**Problem**: Mixing regenerable data with configuration.

```python
# ❌ WRONG
cache_file = get_config_dir() / 'download_cache.json'
```

**Solution**: Use `$XDG_CACHE_HOME` for regenerable data.

```python
# ✅ CORRECT
cache_file = get_cache_dir() / 'download_cache.json'
```

### 6. Large Files in Runtime Directory

**Problem**: `$XDG_RUNTIME_DIR` often tmpfs-mounted with size limits.

```python
# ❌ WRONG
large_file = get_runtime_dir() / 'model.gguf'  # May be 1GB+
```

**Solution**: Use `$XDG_DATA_HOME` for large persistent files.

```python
# ✅ CORRECT
large_file = get_data_dir() / 'models' / 'model.gguf'
```

### 7. Not Handling Unset `XDG_RUNTIME_DIR`

**Problem**: `$XDG_RUNTIME_DIR` has no default value.

```python
# ❌ WRONG
runtime_dir = get_runtime_dir()
socket_path = runtime_dir / 'socket'  # Fails if None
```

**Solution**: Check for None before using.

```python
# ✅ CORRECT
runtime_dir = get_runtime_dir()
if runtime_dir is None:
    raise RuntimeError("XDG_RUNTIME_DIR not set by system")
socket_path = runtime_dir / 'socket'
```

## Testing XDG Compliance

### Manual Testing with Environment Variables

```bash
# Test with custom XDG directories
export XDG_CONFIG_HOME=/tmp/test-config
export XDG_DATA_HOME=/tmp/test-data
export XDG_CACHE_HOME=/tmp/test-cache
export XDG_STATE_HOME=/tmp/test-state

# Run application
myapp --help

# Verify files are in correct locations
ls -la /tmp/test-config/myapp/
ls -la /tmp/test-data/myapp/
ls -la /tmp/test-cache/myapp/
ls -la /tmp/test-state/myapp/

# Test with unset variables (should use defaults)
unset XDG_CONFIG_HOME XDG_DATA_HOME XDG_CACHE_HOME XDG_STATE_HOME
myapp --help
ls -la ~/.config/myapp/
ls -la ~/.local/share/myapp/
ls -la ~/.cache/myapp/
ls -la ~/.local/state/myapp/
```

### Automated Testing

```python
"""Test XDG compliance."""
import os
import tempfile
from pathlib import Path
import pytest


def test_xdg_config_home_override(monkeypatch):
    """XDG_CONFIG_HOME environment variable is respected."""
    with tempfile.TemporaryDirectory() as tmpdir:
        monkeypatch.setenv('XDG_CONFIG_HOME', tmpdir)
        config_dir = get_config_dir()
        assert config_dir == Path(tmpdir) / 'myapp'


def test_xdg_config_home_default(monkeypatch):
    """Default used when XDG_CONFIG_HOME unset."""
    monkeypatch.delenv('XDG_CONFIG_HOME', raising=False)
    config_dir = get_config_dir()
    assert config_dir == Path.home() / '.config' / 'myapp'


def test_relative_path_ignored(monkeypatch):
    """Relative paths in XDG variables are ignored per specification."""
    monkeypatch.setenv('XDG_CONFIG_HOME', 'relative/path')
    config_dir = get_config_dir()
    # Should fall back to default, not use relative path
    assert config_dir == Path.home() / '.config' / 'myapp'


def test_empty_string_uses_default(monkeypatch):
    """Empty string in XDG variable uses default."""
    monkeypatch.setenv('XDG_CONFIG_HOME', '')
    config_dir = get_config_dir()
    assert config_dir == Path.home() / '.config' / 'myapp'


def test_runtime_dir_none_when_unset(monkeypatch):
    """XDG_RUNTIME_DIR returns None when unset (no default)."""
    monkeypatch.delenv('XDG_RUNTIME_DIR', raising=False)
    runtime_dir = get_runtime_dir()
    assert runtime_dir is None


def test_config_dirs_search_path(monkeypatch):
    """XDG_CONFIG_DIRS parsed as colon-separated search path."""
    monkeypatch.setenv('XDG_CONFIG_DIRS', '/etc/xdg:/opt/config')
    dirs = get_config_dirs()
    assert dirs == [Path('/etc/xdg'), Path('/opt/config')]


def test_data_dirs_ignores_relative_paths(monkeypatch):
    """XDG_DATA_DIRS filters out relative paths."""
    monkeypatch.setenv('XDG_DATA_DIRS', '/usr/share:relative/path:/opt/data')
    dirs = get_data_dirs()
    assert dirs == [Path('/usr/share'), Path('/opt/data')]
```

## Example Directory Structure

```text
~/.config/myapp/              # XDG_CONFIG_HOME
    config.toml               # Main configuration
    credentials.json          # User credentials

~/.local/share/myapp/         # XDG_DATA_HOME
    models/                   # Downloaded models
        model-v1.gguf
    databases/
        user.db

~/.local/state/myapp/         # XDG_STATE_HOME
    history.log               # Command history
    recent-files.json         # Recently used files

~/.local/bin/                 # User binaries (convention)
    myapp                     # Application binary

~/.cache/myapp/               # XDG_CACHE_HOME
    downloads/                # Downloaded temporary files
    build/                    # Build artifacts
```

## Configuration File Loading Pattern

For TOML configuration files with XDG support, activate the toml-python skill:

```text
Skill(command: "toml-python")
```

The toml-python skill provides comprehensive guidance on TOML parsing with `tomllib` (Python 3.11+) and `tomli` (backport), including validation with Pydantic models.

## Related Skills

**Activate these skills for related functionality:**

- `toml-python` - TOML configuration file parsing and validation
- `python3-development` - Modern Python development patterns and best practices
- `uv` - Python package and project management

## References

### Official Specification

- [XDG Base Directory Specification v0.8](https://specifications.freedesktop.org/basedir-spec/latest/) - Primary authoritative source (accessed 2025-01-15)
- [Freedesktop.org Specifications Index](https://specifications.freedesktop.org/) - All freedesktop specifications
- [XDG Specs Git Repository](https://cgit.freedesktop.org/xdg/xdg-specs/tree/basedir) - Source repository

### Implementation Guides

- [ArchWiki: XDG Base Directory](https://wiki.archlinux.org/title/XDG_Base_Directory) - Comprehensive implementation guide (accessed 2025-01-15)
- [platformdirs Python Library](https://github.com/tox-dev/platformdirs) - Cross-platform Python implementation (accessed 2025-01-15)

### Community Resources

- [XDG Mailing List](http://lists.freedesktop.org/mailman/listinfo/xdg) - Official discussion forum
- [Freedesktop.org Wiki](https://www.freedesktop.org/wiki/Specifications/basedir-spec/) - Additional documentation

## Key Principles

1. **Absolute Paths Only**: Validate all XDG paths are absolute; ignore relative paths
2. **Environment Variable Priority**: Always check XDG environment variables before defaults
3. **Specification Compliance**: Follow XDG Base Directory Specification v0.8 exactly
4. **Directory Creation**: Create parent directories before writing files
5. **Appropriate Storage**: Use correct directory for data type (config vs data vs cache vs state)
6. **Runtime Directory Limits**: Avoid large files in `$XDG_RUNTIME_DIR` (tmpfs limits)
7. **Cross-Platform Awareness**: Use platformdirs for macOS/Windows support
8. **Search Path Handling**: Parse colon-separated search paths correctly
9. **No Default for Runtime**: `$XDG_RUNTIME_DIR` has no default; check for None
10. **Testing**: Validate XDG compliance with environment variable overrides
