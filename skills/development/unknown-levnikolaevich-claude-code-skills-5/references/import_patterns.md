# Import Patterns & Module Resolution

<!-- SCOPE: Language-specific grep patterns, module resolution algorithm, exclusion lists. -->

## Language Detection

```
IF Glob("**/*.py", root) has matches → language = "python"
IF Glob("**/*.ts", root) OR Glob("**/*.tsx", root) → language = "typescript"
IF Glob("**/*.js", root) OR Glob("**/*.jsx", root) → language = "javascript"
IF Glob("**/*.cs", root) → language = "csharp"
IF Glob("**/*.java", root) → language = "java"
```

Multiple languages possible (e.g., Python backend + TS frontend). Build separate graphs per language, then merge at module boundary level.

## Import Grep Patterns

### Python

| Pattern | Grep | Example |
|---------|------|---------|
| From import | `^from\s+([\w.]+)\s+import` | `from app.domain.user import User` |
| Plain import | `^import\s+([\w.]+)` | `import app.services.auth` |
| Relative import | `^from\s+\.+` | `from .models import User` |

**Notes:**
- Relative imports (`.`, `..`) resolve relative to current package
- `__init__.py` presence defines package boundaries
- Dynamic imports (`importlib.import_module`) not detected (acceptable)

### TypeScript / JavaScript

| Pattern | Grep | Example |
|---------|------|---------|
| ES6 import | `import\s+.*\s+from\s+['\"]([^'\"]+)['\"]` | `import { User } from './domain/user'` |
| require | `require\(['\"]([^'\"]+)['\"]\)` | `const auth = require('./services/auth')` |
| Dynamic import | `import\(['\"]([^'\"]+)['\"]\)` | `const mod = await import('./lazy')` |
| Re-export | `export\s+.*\s+from\s+['\"]([^'\"]+)['\"]` | `export { User } from './models'` |

**Notes:**
- Paths starting with `.` or `..` are relative
- Paths without `.` prefix are node_modules (exclude)
- `@/` or `~/` prefixes are project aliases (resolve via tsconfig paths)

### C#

| Pattern | Grep | Example |
|---------|------|---------|
| Using | `^using\s+([\w.]+);` | `using MyApp.Domain.Entities;` |
| Using static | `^using\s+static\s+([\w.]+);` | `using static MyApp.Utils.Helpers;` |
| Global using | `^global\s+using\s+([\w.]+);` | `global using MyApp.Common;` |

**Notes:**
- Namespace = module boundary (not file path)
- Project references in .csproj define valid dependencies
- System.* and Microsoft.* are stdlib (exclude)

### Java

| Pattern | Grep | Example |
|---------|------|---------|
| Import | `^import\s+([\w.]+);` | `import com.myapp.domain.User;` |
| Static import | `^import\s+static\s+([\w.]+);` | `import static com.myapp.utils.Helpers.*;` |
| Wildcard import | `^import\s+([\w.]+)\.\*;` | `import com.myapp.domain.*;` |

**Notes:**
- Package structure mirrors directory structure
- java.* and javax.* are stdlib (exclude)
- org.springframework.*, com.google.* etc. are third-party (exclude)

## Module Resolution Algorithm

Map import paths to module names using directory structure:

```
FUNCTION resolve_module(file_or_import, scan_root):
  # Get path relative to scan_root
  rel_path = relative(file_or_import, scan_root)

  # Extract top-level module (first directory component)
  parts = split(rel_path, "/")

  # Strategy 1: First meaningful directory
  IF parts[0] IN ["src", "app", "lib"]:
    module = parts[1]  # e.g., src/auth/... → "auth"
  ELSE:
    module = parts[0]  # e.g., auth/... → "auth"

  # Strategy 2: Use architecture.md module definitions if available
  FOR EACH defined_module IN architecture_modules:
    IF file_or_import matches defined_module.path:
      RETURN defined_module.name

  RETURN module
```

## Exclusion Lists

### Standard Library (exclude from graph)

| Language | Exclude patterns |
|----------|-----------------|
| Python | `os`, `sys`, `re`, `json`, `typing`, `collections`, `pathlib`, `datetime`, `logging`, `unittest`, `abc`, `dataclasses`, `enum`, `functools`, `itertools`, `contextlib`, `asyncio`, `io`, `math`, `copy`, `hashlib`, `base64`, `uuid`, `http`, `urllib`, `email`, `csv`, `sqlite3`, `subprocess`, `shutil`, `tempfile`, `glob`, `fnmatch`, `textwrap`, `inspect` |
| TypeScript/JS | `fs`, `path`, `os`, `http`, `https`, `url`, `util`, `crypto`, `events`, `stream`, `child_process`, `cluster`, `net`, `dns`, `tls`, `zlib`, `readline`, `assert`, `buffer`, `console`, `process`, `timers`, `worker_threads` |
| C# | `System.*`, `Microsoft.*` (unless project-specific Microsoft.Extensions config) |
| Java | `java.*`, `javax.*`, `jakarta.*` |

### Third-Party (exclude from graph)

| Language | Exclude patterns |
|----------|-----------------|
| Python | Imports not resolving to files under `scan_root`; common: `fastapi`, `flask`, `django`, `sqlalchemy`, `pydantic`, `httpx`, `requests`, `pytest`, `celery`, `redis` |
| TypeScript/JS | Imports without `.` or `..` prefix (node_modules); `@types/*` |
| C# | NuGet packages (not in project source tree) |
| Java | Maven/Gradle dependencies (not in project source tree) |

**General rule:** If the import target does not resolve to a file under `scan_root`, it is external and excluded from the graph.

## Limitations

- **Dynamic imports** not detected (Python `importlib`, JS `import()`, C# reflection)
- **Conditional imports** (inside if/try blocks) treated same as unconditional
- **Re-exports** (barrel files) may create phantom edges
- **Monorepo packages** may need custom module resolution

These limitations are acceptable for architecture-level audit. The graph captures the static dependency structure which represents the architectural intent.

---

**Version:** 1.0.0
**Last Updated:** 2026-02-11
