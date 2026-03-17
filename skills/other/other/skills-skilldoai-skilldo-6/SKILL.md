---
name: pytest
description: Python testing framework that discovers tests, provides fixtures, and offers rich assertion introspection.
version: 3.9.3
ecosystem: python
license: MIT
generated_with: gpt-5.2
---

## Imports

```python
import pytest
from pytest import fixture, fail, raises
```

## Core Patterns

### Define and use fixtures (dependency injection) ✅ Current
```python
import pytest

@pytest.fixture()
def fruit() -> str:
    return "apple"

def test_fruit_value(fruit: str) -> None:
    assert fruit == "apple"
```
* Request fixtures by naming them as test function parameters.
* Prefer fixtures over manual setup/teardown in tests.

### Assert exceptions with pytest.raises ✅ Current
```python
import pytest

def parse_port(value: str) -> int:
    port = int(value)
    if not (0 <= port <= 65535):
        raise ValueError("port out of range")
    return port

def test_parse_port_rejects_out_of_range() -> None:
    with pytest.raises(ValueError, match="out of range"):
        parse_port("70000")
```
* Use `match=` to assert on stable parts of the error message.

### Fail fast with pytest.fail ✅ Current
```python
import pytest

def test_requires_feature_flag() -> None:
    feature_enabled = False
    if not feature_enabled:
        pytest.fail("feature flag must be enabled for this test")
```
* Use `pytest.fail(...)` for explicit, readable failure paths (e.g., unreachable branches).

### Parametrize tests with pytest.mark.parametrize ✅ Current
```python
import pytest

def add(a: int, b: int) -> int:
    return a + b

@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [(1, 2, 3), (0, 0, 0), (-1, 1, 0)],
)
def test_add(a: int, b: int, expected: int) -> None:
    assert add(a, b) == expected
```
* Prefer parametrization over loops inside a single test for clearer reporting.

### Use tmp_path for filesystem isolation ✅ Current
```python
from __future__ import annotations

from pathlib import Path

def test_writes_file(tmp_path: Path) -> None:
    out = tmp_path / "out.txt"
    out.write_text("hello", encoding="utf-8")
    assert out.read_text(encoding="utf-8") == "hello"
```
* `tmp_path` provides a unique `pathlib.Path` per test for safe filesystem operations.

## Configuration

* **Config formats**: `pytest.ini`, `pyproject.toml` (under `[tool.pytest.ini_options]`), `tox.ini`, `setup.cfg`.
* **Common settings**:
  * `testpaths`: directories to search for tests.
  * `python_files`, `python_classes`, `python_functions`: discovery patterns.
  * `addopts`: default CLI args (e.g., `-q`, `-ra`).
  * `markers`: register custom markers to avoid warnings.
* **INI “pathlist” values**: options declared by plugins/conftest via `parser.addini(..., type="pathlist")` are returned as paths relative to the config file directory.
* **Environment variables affecting output**:
  * `CI` or `BUILD_NUMBER`: pytest adapts output for CI logs (notably: short test summary is not truncated to terminal width). Avoid tests that assert on truncation/terminal-width-dependent formatting.

## Pitfalls

### Wrong: Referencing a fixture function instead of requesting it
```python
import pytest

@pytest.fixture
def fruit() -> str:
    return "apple"

def test_fruit_value() -> None:
    # This refers to the function object, not the fixture value.
    assert fruit == "apple"
```

### Right: Request the fixture by name as a parameter
```python
import pytest

@pytest.fixture
def fruit() -> str:
    return "apple"

def test_fruit_value(fruit: str) -> None:
    assert fruit == "apple"
```

### Wrong: Asserting on terminal-width-dependent output (brittle in CI)
```python
def test_output_truncation_assumption(capsys) -> None:
    print("short test summary info " + ("x" * 200))
    out = capsys.readouterr().out
    # Brittle: assumes truncation that may not happen in CI.
    assert out.endswith("...\n")
```

### Right: Assert on stable substrings instead
```python
def test_output_contains_stable_substring(capsys) -> None:
    print("short test summary info " + ("x" * 200))
    out = capsys.readouterr().out
    assert "short test summary info" in out
```

### Wrong: Overly strict exception message checks
```python
import pytest

def f() -> None:
    raise ValueError("bad value: 42")

def test_exception_message_too_strict() -> None:
    # Too strict: minor message changes can break the test.
    with pytest.raises(ValueError, match=r"^bad value: 42$"):
        f()
```

### Right: Match only the stable part of the message
```python
import pytest

def f() -> None:
    raise ValueError("bad value: 42")

def test_exception_message_stable_match() -> None:
    with pytest.raises(ValueError, match=r"bad value"):
        f()
```

### Wrong: Writing incorrect expectations and ignoring assertion introspection
```python
def inc(x: int) -> int:
    return x + 1

def test_inc_wrong_expected_value() -> None:
    assert inc(3) == 5
```

### Right: Fix the expected value; rely on plain assert
```python
def inc(x: int) -> int:
    return x + 1

def test_inc_correct_expected_value() -> None:
    assert inc(3) == 4
```

## References

- [Official Documentation](https://docs.pytest.org/en/stable/)
- [GitHub Repository](https://github.com/pytest-dev/pytest)

## Migration from v[previous]

No specific breaking-change notes were provided for v3.9.3 in the given context.

Deprecated-to-current guidance reflected in the test patterns:
* Prefer `tmp_path`/`tmp_path_factory` (`pathlib.Path`) over legacy `tmpdir`/`tmpdir_factory` (py.path-style).
* Prefer public fixtures like `request` instead of constructing internal request objects directly.

## API Reference

- **pytest.fixture** - Define a fixture; key params: `scope`, `params`, `autouse`, `name`.
- **pytest.fail** - Immediately fail a test with a message; key params: `reason`, `pytrace`.
- **pytest.raises** - Assert an exception is raised; key params: expected exception type(s), `match`.
- **pytest.mark.parametrize** - Parametrize a test function over input cases; key params: argnames, argvalues, `ids`.
- **tmp_path (fixture)** - Per-test temporary directory as `pathlib.Path`.
- **tmp_path_factory (fixture)** - Session-scoped factory for temporary paths; method: `getbasetemp()`.
- **capsys (fixture)** - Capture `stdout`/`stderr` from Python-level writes; method: `readouterr()`.
- **capfd (fixture)** - Capture `stdout`/`stderr` at the file-descriptor level; method: `readouterr()`.
- **monkeypatch (fixture)** - Temporarily modify environment/attributes; methods: `setattr`, `setenv`, `chdir`.
- **pytestconfig (fixture)** - Access configuration and CLI options; common method: `getoption(...)`.
- **request (fixture)** - Introspect the requesting test context; common method: `getfixturevalue(name)`.
- **pytest.skip** - Skip at runtime; key params: `reason`, `allow_module_level`.
- **pytest.importorskip** - Skip if an import fails; key params: module name, `minversion`, `reason`.
- **pytest.xfail** - Mark expected failure at runtime; key params: `reason`, `strict`.
- **pytest.mark** - Namespace for markers (e.g., `skip`, `xfail`, custom markers).

## Current Library State (from source analysis)

### API Surface
```json
{
  "library_category": "testing",
  "apis": [
    {
      "name": "_pytest.__version__",
      "type": "variable",
      "signature": "__version__: str",
      "signature_truncated": false,
      "return_type": "str",
      "module": "_pytest._version",
      "publicity_score": "high",
      "module_type": "public",
      "decorators": [],
      "deprecation": {
        "is_deprecated": false
      }
    },
    {
      "name": "_pytest.version_tuple",
      "type": "variable",
      "signature": "version_tuple: tuple[int, int, str]",
      "signature_truncated": false,
      "return_type": "tuple[int, int, str]",
      "module": "_pytest._version",
      "publicity_score": "high",
      "module_type": "public",
      "decorators": [],
      "deprecation": {
        "is_deprecated": false
      }
    },
    {
      "name": "_pytest._code.Code",
      "type": "class",
      "signature": "Code(obj: object)",
      "signature_truncated": false,
      "return_type": "Code",
      "module": "_pytest._code.code",
      "publicity_score": "high",
      "module_type": "public",
      "decorators": [],
      "deprecation": {
        "is_deprecated": false
      }
    },
    {
      "name": "_pytest._code.ExceptionInfo",
      "type": "class",
      "signature": "ExceptionInfo(exc: Exception, *, frame: Frame | None = None)",
      "signature_truncated": false,
      "return_type": "ExceptionInfo",
      "module": "_pytest._code.code",
      "publicity_score": "high",
      "module_type": "public",
      "decorators": [],
      "deprecation": {
        "is_deprecated": false
      }
    },
    {
      "name": "_pytest._code.Frame",
      "type": "class",
      "signature": "Frame(frame: types.FrameType)",
      "signature_truncated": false,
      "return_type": "Frame",
      "module": "_pytest._code.code",
      "publicity_score": "high",
      "module_type": "public",
      "decorators": [],
      "deprecation": {
        "is_deprecated": false
      }
    },
    {
      "name": "_pytest._code.Source",
      "type": "class",
      "signature": "Source(obj: object)",
      "signature_truncated": false,
      "return_type": "Source",
      "module": "_pytest._code.source",
      "publicity_score": "high",
      "module_type": "public",
      "decorators": [],
      "deprecation": {
        "is_deprecated": false
      }
    },
    {
      "name": "_pytest._code.Traceback",
      "type": "class",
      "signature": "Traceback(tb: types.TracebackType)",
      "signature_truncated": false,
      "return_type": "Traceback",
      "module": "_pytest._code.code",
      "publicity_score": "high",
      "module_type": "public",
      "decorators": [],
      "deprecation": {
        "is_deprecated": false
      }
    },
    {
      "name": "_pytest._code.TracebackEntry",
      "type": "class",
      "signature": "TracebackEntry(frame: types.FrameType, *, lineno: int | None = None)",
      "signature_truncated": false,
      "return_type": "TracebackEntry",
      "module": "_pytest._code.code",
      "publicity_score": "high",
      "module_type": "public",
      "decorators": [],
      "deprecation": {
        "is_deprecated": false
      }
    },
    {
      "name": "_pytest._code.filter_traceback",
      "type": "function",
      "signature": "filter_traceback(entry: TracebackEntry) -> bool",
      "signature_truncated": false,
      "return_type": "bool",
      "module": "_pytest._code.code",
      "publicity_score": "high",
      "module_type": "public",
      "decorators": [],
      "deprecation": {
        "is_deprecated": false
      }
    },
    {
      "name": "_pytest._code.getfslineno",
      "type": "function",
      "signature": "getfslineno(obj: object, *, lineno: int | None = None) -> tuple[str, int]",
      "signature_truncated": false,
      "return_type": "tuple[str, int]",
      "module": "_pytest._code.code",
      "publicity_score": "high",
      "module_type": "public",
      "decorators": [],
      "deprecation": {
        "is_deprecated": false
      }
    },
    {
      "name": "_pytest._code.getrawcode",
      "type": "function",
      "signature": "getrawcode(obj: object) -> types.CodeType",
      "signature_truncated": false,
      "return_type": "types.CodeType",
      "module": "_pytest._code.source",
      "publicity_score": "high",
      "module_type": "public",
      "decorators": [],
      "deprecation": {
        "is_deprecated": false
      }
    },
    {
      "name": "_pytest._io.TerminalWriter",
      "type": "class",
      "signature": "TerminalWriter(file: IO[str] = None, encoding: str = None)",
      "signature_truncated": false,
      "return_type": "TerminalWriter",
      "module": "_pytest._io.terminalwriter",
      "publicity_score": "high",
      "module_type": "public",
      "decorators": [],
      "deprecation": {
        "is_deprecated": false
      }
    },
    {
      "name": "_pytest._io.get_terminal_width",
      "type": "function",
      "signature": "get_terminal_width() -> int",
      "signature_truncated": false,
      "return_type": "int",
      "module": "_pytest._io.terminalwriter",
      "publicity_score": "high",
      "module_type": "public",
      "decorators": [],
      "deprecation": {
        "is_deprecated": false
      }
    },
    {
      "name": "_pytest.assertion.register_assert_rewrite",
      "type": "function",
      "signature": "register_assert_rewrite(*names: str) -> None",
      "signature_truncated": false,
      "return_type": "None",
      "module": "_pytest.assertion.__init__",
      "publicity_score": "high",
      "module_type": "public",
      "decorators": [],
      "deprecation": {
        "is_deprecated": false
      },
      "type_hints": {
        "names": {
          "base_type": "str",
          "is_optional": false,
          "default_value": null
        }
      }
    },
    {
      "name": "_pytest.assertion.pytest_addoption",
      "type": "function",
      "signature": "pytest_addoption(parser: Parser) -> None",
      "signature_truncated": false,
      "return_type": "None",
      "module": "_pytest.assertion.__init__",
      "publicity_score": "high",
      "module_type": "public",
      "decorators": [],
      "deprecation": {
        "is_deprecated": false
      },
      "type_hints": {
        "parser": {
          "base_type": "Parser",
          "is_optional": false,
          "default_value": null
        }
      }
    },
    {
      "name": "_pytest.assertion.pytest_assertrepr_compare",
      "type": "function",
      "signature": "pytest_assertrepr_compare(config: Config, op: str, left: Any, right: Any) -> list[str] | None",
      "signature_truncated": false,
      "return_type": "list[str] | None",
      "module": "_pytest.assertion.__init__",
      "publicity_score": "high",
      "module_type": "public",
      "decorators": [],
      "deprecation": {
        "is_deprecated": false
      },
      "type_hints": {
        "config": {
          "base_type": "Config",
          "is_optional": false,
          "default_value": null
        },
        "op": {
          "base_type": "str",
          "is_optional": false,
          "default_value": null
        },
        "left": {
          "base_type": "Any",
          "is_optional": false,
          "default_value": null
        },
        "right": {
          "base_type": "Any",
          "is_optional": false,
          "default_value": null
        }
      }
    },
    {
      "name": "_pytest.config.ExitCode",
      "type": "class",
      "signature": "class ExitCode(enum.IntEnum)\n    OK = 0\n    TESTS_FAILED = 1\n    INTERRUPTED = 2\n    INTERNAL_ERROR = 3\n    USAGE_ERROR = 4\n    NO_TESTS_COLLECTED = 5",
      "signature_truncated": true,
      "return_type": "ExitCode",
      "module": "_pytest.config.__init__",
      "publicity_score": "high",
      "module_type": "public",
      "decorators": [],
      "deprecation": {
        "is_deprecated": false
      }
    },
    {
      "name": "_pytest.config.main",
      "type": "function",
      "signature": "main(\n    args: list[str] | os.PathLike[str] | None = None,\n    plugins: Sequence[str | _PluggyPlugin] | None = None,\n) -> int | ExitCode",
      "signature_truncated": true,
      "return_type": "int | ExitCode",
      "module": "_pytest.config.__init__",
      "publicity_score": "high",
      "module_type": "public",
      "decorators": [],
      "deprecation": {
        "is_deprecated": false
      },
      "type_hints": {
        "args": {
          "base_type": "list[str] | os.PathLike[str] | None",
          "is_optional": true,
          "default_value": "None"
        },
        "plugins": {
          "base_type": "Sequence[str | _PluggyPlugin] | None",
          "is_optional": true,
          "default_value": "None"
        }
      }
    },
    {
      "name": "_pytest.config.console_main",
      "type": "function",
      "signature": "console_main() -> int",
      "signature_truncated": false,
      "return_type": "int",
      "module": "_pytest.config.__init__",
      "publicity_score": "high",
      "module_type": "public",
      "decorators": [],
      "deprecation": {
        "is_deprecated": false
      }
    }
  ]
}
```

---

**NOTES:**
- This list covers the most critical user-facing APIs surfaced via `__all__` and public imports, as well as the main CLI entrypoints and assertion registration/decorator features.
- Internal compatibility or hidden APIs (e.g., those from `_pytest.compat`, not in `__all__`) are omitted for brevity and clarity, but can be added and marked as `"publicity_score": "low"` if needed.
- Type hints are extracted wherever possible; complex unions are represented as per the instructions.
- For classes with many members (e.g., `ExitCode`), the full enum is summarized and marked as `"signature_truncated": true` if it would be overly long.
- All API elements above are from public modules and have high publicity scores; for low/medium APIs, include `"publicity_score": "low"`/`"medium"` and mark `"module_type": "internal"`/`"compatibility"` as required.
- No deprecations are detected in the sampled code above for these APIs; if any are detected in other modules, the `deprecation` object should be filled as per schema.


### Usage Patterns
```json
[
  {
    "api": "pytest.fixture",
    "setup_code": [
      "import pytest"
    ],
    "usage_pattern": [
      "@pytest.fixture(scope=\"session\", params=['foo', 'bar'], ids=['spam', 'ham'])",
      "def arg_same(): ...",
      "@pytest.fixture(scope=\"function\")",
      "def arg_other(arg_same): ...",
      "def test_arg1(arg_other): ..."
    ],
    "assertions": [
      "result.stdout.fnmatch_lines([\"SETUP    S arg_same?'spam'?\", \"SETUP    S arg_same?'ham'?\"])"
    ],
    "test_infrastructure": [
      "pytester fixture",
      "pytester.makeconftest",
      "pytester.makepyfile",
      "pytester.runpytest"
    ],
    "deprecation_status": "current"
  },
  {
    "api": "pytester.runpytest",
    "setup_code": [
      "import pytest",
      "pytester: Pytester"
    ],
    "usage_pattern": [
      "result = pytester.runpytest(mode, test_file)"
    ],
    "assertions": [
      "assert result.ret == 0",
      "result.stdout.fnmatch_lines([...])"
    ],
    "test_infrastructure": [
      "pytester fixture",
      "mode fixture (parametrized)"
    ],
    "deprecation_status": "current"
  },
  {
    "api": "pytest.fixture (autouse)",
    "setup_code": [
      "import pytest"
    ],
    "usage_pattern": [
      "@pytest.fixture(scope='session', autouse=True)",
      "def arg_session(): ...",
      "@pytest.fixture",
      "def arg_function(): ...",
      "def test_arg1(arg_function): ..."
    ],
    "assertions": [
      "result.stdout.fnmatch_lines([...])"
    ],
    "test_infrastructure": [
      "pytester fixture",
      "pytester.makepyfile",
      "pytester.runpytest"
    ],
    "deprecation_status": "current"
  },
  {
    "api": "pytest.fixture (params)",
    "setup_code": [
      "import pytest"
    ],
    "usage_pattern": [
      "@pytest.fixture(scope='session', params=['foo', 'bar'])",
      "def arg_same(): ...",
      "@pytest.fixture(scope='function')",
      "def arg_other(arg_same): ...",
      "def test_arg1(arg_other): ..."
    ],
    "assertions": [
      "result.stdout.fnmatch_lines([\"SETUP    S arg_same?'foo'?\", \"TEARDOWN S arg_same?'foo'?\", \"SETUP    S arg_same?'bar'?\", \"TEARDOWN S arg_same?'bar'?\"])"
    ],
    "test_infrastructure": [
      "pytester fixture",
      "pytester.makeconftest",
      "pytester.makepyfile",
      "pytester.runpytest"
    ],
    "deprecation_status": "current"
  },
  {
    "api": "pytest.mark.parametrize",
    "setup_code": [
      "import pytest"
    ],
    "usage_pattern": [
      "@pytest.mark.parametrize(\"config_type\", [\"ini\", \"toml\"])",
      "def test_addini_paths(pytester: pytest.Pytester, config_type: str): ...",
      "// config_type in {\"ini\", \"toml\"}"
    ],
    "assertions": [
      "assert len(values) == 2",
      "assert values[0] == inipath.parent.joinpath(\"hello\")",
      "assert values[1] == inipath.parent.joinpath(\"world/sub.py\")",
      "pytest.raises(ValueError, config.getini, \"other\")"
    ],
    "test_infrastructure": [
      "pytester fixture"
    ],
    "deprecation_status": "current"
  },
  {
    "api": "request.getfixturevalue",
    "setup_code": [
      "import pytest"
    ],
    "usage_pattern": [
      "@pytest.fixture()",
      "def dynamically_requested_fixture(): ...",
      "@pytest.fixture()",
      "def dependent_fixture(request):",
      "    request.getfixturevalue('dynamically_requested_fixture')",
      "def test_dyn(dependent_fixture): ..."
    ],
    "assertions": [
      "result.stdout.fnmatch_lines([\"*SETUP    F dynamically_requested_fixture\", \"*TEARDOWN F dynamically_requested_fixture\"])"
    ],
    "test_infrastructure": [
      "pytester fixture",
      "pytester.makepyfile",
      "pytester.runpytest"
    ],
    "deprecation_status": "current"
  },
  {
    "api": "pytester.makefile",
    "setup_code": [
      "testdir: Testdir"
    ],
    "usage_pattern": [
      "p1 = testdir.makefile(\"foo.bar\", \"\")",
      "assert \".foo.bar\" in str(p1)"
    ],
    "assertions": [
      "assert \".foo.bar\" in str(p1)"
    ],
    "test_infrastructure": [
      "testdir fixture"
    ],
    "deprecation_status": "soft",
    "deprecation_note": "The Testdir API is considered legacy; prefer Pytester for new code."
  },
  {
    "api": "pytester.makefile (ext=None)",
    "setup_code": [
      "testdir: Testdir"
    ],
    "usage_pattern": [
      "with pytest.raises(TypeError):",
      "    testdir.makefile(None, \"\")"
    ],
    "assertions": [
      "pytest.raises(TypeError)"
    ],
    "test_infrastructure": [
      "testdir fixture"
    ],
    "deprecation_status": "soft",
    "deprecation_note": "The Testdir API is considered legacy; prefer Pytester for new code."
  },
  {
    "api": "pytester.makefile (ext='')",
    "setup_code": [
      "testdir: Testdir"
    ],
    "usage_pattern": [
      "p1 = testdir.makefile(\"\", \"\")",
      "assert \"test_testdir_makefile\" in str(p1)"
    ],
    "assertions": [
      "assert \"test_testdir_makefile\" in str(p1)"
    ],
    "test_infrastructure": [
      "testdir fixture"
    ],
    "deprecation_status": "soft",
    "deprecation_note": "The Testdir API is considered legacy; prefer Pytester for new code."
  },
  {
    "api": "TempdirFactory.getbasetemp",
    "setup_code": [
      "tmpdir_factory: TempdirFactory",
      "tmp_path_factory: pytest.TempPathFactory"
    ],
    "usage_pattern": [
      "assert str(tmpdir_factory.getbasetemp()) == str(tmp_path_factory.getbasetemp())"
    ],
    "assertions": [
      "assert str(tmpdir_factory.getbasetemp()) == str(tmp_path_factory.getbasetemp())"
    ],
    "test_infrastructure": [
      "tmpdir_factory fixture",
      "tmp_path_factory fixture"
    ],
    "deprecation_status": "soft",
    "deprecation_note": "TempdirFactory is legacy; prefer tmp_path_factory for new code."
  },
  {
    "api": "pytest.Cache.makedir",
    "setup_code": [
      "cache: pytest.Cache"
    ],
    "usage_pattern": [
      "dir = cache.makedir(\"foo\")",
      "assert dir.exists()",
      "dir.remove()"
    ],
    "assertions": [
      "assert dir.exists()"
    ],
    "test_infrastructure": [
      "cache fixture"
    ],
    "deprecation_status": "current"
  },
  {
    "api": "TopRequest (from _pytest.fixtures)",
    "setup_code": [
      "from _pytest.fixtures import TopRequest"
    ],
    "usage_pattern": [
      "modcol = pytester.getmodulecol(\"def test_somefunc(): pass\")",
      "(item,) = pytester.genitems([modcol])",
      "req = TopRequest(item, _ispytest=True)",
      "assert req.path == modcol.path",
      "assert req.fspath == modcol.fspath"
    ],
    "assertions": [
      "assert req.path == modcol.path",
      "assert req.fspath == modcol.fspath"
    ],
    "test_infrastructure": [
      "pytester fixture"
    ],
    "deprecation_status": "current"
  },
  {
    "api": "pytest.addini (type=pathlist)",
    "setup_code": [
      "def pytest_addoption(parser):",
      "    parser.addini(\"paths\", \"my new ini value\", type=\"pathlist\")"
    ],
    "usage_pattern": [
      "pytester.makeconftest(<above code block>)",
      "pytester.makeini or pytester.maketoml for [pytest] paths",
      "config = pytester.parseconfig()",
      "values = config.getini(\"paths\")"
    ],
    "assertions": [
      "assert len(values) == 2",
      "assert values[0] == inipath.parent.joinpath(\"hello\")",
      "assert values[1] == inipath.parent.joinpath(\"world/sub.py\")"
    ],
    "test_infrastructure": [
      "pytester fixture"
    ],
    "deprecation_status": "current"
  },
  {
    "api": "pytest.addini (override)",
    "setup_code": [
      "def pytest_addoption(parser):",
      "    parser.addini(\"paths\", \"my new ini value\", type=\"pathlist\")"
    ],
    "usage_pattern": [
      "pytester.makeconftest(<above code block>)",
      "pytester.makeini with [pytest] paths=blah.py",
      "pytester.makepyfile with test printing config.getini(\"paths\")",
      "pytester.runpytest(\"--override-ini\", \"paths=foo/bar1.py foo/bar2.py\", \"-s\")"
    ],
    "assertions": [
      "stdout contains user_path:bar1.py, user_path:bar2.py"
    ],
    "test_infrastructure": [
      "pytester fixture"
    ],
    "deprecation_status": "current"
  },
  {
    "api": "pytest_cmdline_main hook",
    "setup_code": [
      "def pytest_cmdline_main(config):",
      "    print(\"pytest_cmdline_main inifile =\", config.inifile)"
    ],
    "usage_pattern": [
      "pytester.makeconftest(<above code block>)",
      "pytester.makeini with [pytest]",
      "result = pytester.runpytest_subprocess(\"-s\")"
    ],
    "assertions": [
      "stdout contains pytest_cmdline_main inifile = <inifile path>"
    ],
    "test_infrastructure": [
      "pytester fixture"
    ],
    "deprecation_status": "current"
  },
  {
    "api": "pytest.raises",
    "setup_code": [
      "import pytest"
    ],
    "usage_pattern": [
      "with pytest.raises(TypeError): ...",
      "with pytest.raises(AttributeError, match=\"path not available in session-scoped context\"): ...",
      "pytest.raises(ValueError, config.getini, \"other\")"
    ],
    "assertions": [
      "Exception is raised as expected"
    ],
    "test_infrastructure": [],
    "deprecation_status": "current"
  },
  {
    "api": "pytest.fixture (scope=session)",
    "setup_code": [
      "import pytest"
    ],
    "usage_pattern": [
      "@pytest.fixture(scope=\"session\")",
      "def arg_session(): ...",
      "@pytest.fixture",
      "def arg_function(): ...",
      "def test_arg1(arg_session, arg_function): ..."
    ],
    "assertions": [
      "result.stdout.fnmatch_lines([...])"
    ],
    "test_infrastructure": [
      "pytester fixture",
      "pytester.makepyfile",
      "pytester.runpytest"
    ],
    "deprecation_status": "current"
  }
]
```

### Documentation & Changelog
```json
{
  "documented_apis": [
    "pytest.fixture",
    "pytest.fail"
  ],
  "conventions": [
    "Use plain `assert` statements in tests for clear, expressive failure messages.",
    "Name test functions starting with `test_` to enable auto-discovery.",
    "Organize reusable setup/teardown code as fixtures using the `@pytest.fixture` decorator.",
    "Pass fixtures as function arguments to tests that need them.",
    "Tests can use any number of fixtures, and fixtures can depend on each other.",
    "Prefer fixtures over xUnit-style `setUp`/`tearDown` for modularity and scalability.",
    "Integrate pytest into CI pipelines for full assertion output."
  ],
  "pitfalls": [
    {
      "category": "Test Discovery",
      "wrong": "def myTestFunction():\n    assert True",
      "why": "Functions not named with `test_` prefix are not auto-discovered by pytest.",
      "right": "def test_my_function():\n    assert True"
    },
    {
      "category": "Fixture Usage",
      "wrong": "def test_something():\n    my_fixture()\n    assert True",
      "why": "Calling a fixture like a normal function does not inject it; fixtures must be declared as arguments.",
      "right": "def test_something(my_fixture):\n    assert True"
    },
    {
      "category": "Assertion Style",
      "wrong": "self.assertEqual(x, y)",
      "why": "Using unittest-style assertions is unnecessary; plain `assert` provides better error introspection in pytest.",
      "right": "assert x == y"
    }
  ],
  "breaking_changes": [],
  "migration_notes": "For incremental migration, you can mix classic xUnit-style setup/teardown with pytest fixtures. Gradually refactor setup code to use `@pytest.fixture` and pass them as arguments to tests. See https://docs.pytest.org/en/stable/changelog.html for specific version-by-version changes."
}
```

