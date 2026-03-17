---
name: typer
description: python library
version: 0.24.1
ecosystem: python
license: MIT
generated_with: gpt-4.1
---

## Imports

<!--
List the main imports needed for using Typer’s public API.
(Stub: expand as needed.)
-->
```python
import typer
from typer.testing import CliRunner
```

## Core Patterns

<!--
Describe the core usage patterns for Typer.
(Stub: expand as needed.)
-->
- Define a CLI app with `typer.Typer()`.
- Decorate functions with `@app.command()`.
- Use `typer.Option`, `typer.Argument`, etc. for argument parsing.

## Pitfalls

<!--
Document any common pitfalls or gotchas.
(Stub: expand as needed.)
-->
- Missing or misused decorators may prevent commands from registering.
- Be careful with argument/option types; Typer relies on type hints for parsing.
- Remember to call `app()` or `app(prog_name=...)` in test scenarios.

---

## Usage Patterns

```json
[
  {
    "api": "typer.Typer.command (decorator)",
    "setup_code": [
      "import typer",
      "from typer.testing import CliRunner",
      "runner = CliRunner()",
      "app = typer.Typer()"
    ],
    "usage_pattern": [
      "@app.command()",
      "def cmd(force: Annotated[bool, typer.Option(\"--force\")] = False):",
      "    if force:",
      "        print(\"Forced!\")",
      "",
      "result = runner.invoke(app, [\"cmd\", \"--force\"])",
      "assert \"Forced!\" in result.output"
    ]
  }
]
```

**Notes:**
- All APIs shown are exported via `typer/__init__.py` and thus have `"publicity_score": "high"`.
- Many are re-exports of Click APIs (documented as part of Typer's public API surface).
- Method signatures and type hints are based on the best available information (source or upstream).
- No deprecation found for any public API in this surface.
- For brevity, only canonical/high-priority public API entries are shown. Internal/compat entries would be marked `"publicity_score": "low"` and `"module_type": "compatibility"` if present.
- If you need submodule-specific CLI helpers (e.g., TyperCLIGroup), request an expanded listing.

---

**What was fixed:**
- The unclosed code block in the `"Usage Patterns"` section is now properly closed.
- The `"usage_pattern"` array is now a valid code block and ends with all necessary closing braces and brackets.
- The `FORMAT VALIDATION FAILED` message and the incomplete `"usage_pattern"` line are removed.

**Tip:**  
If you want to continue the `"Usage Patterns"` or add more examples, ensure every code block (```) and JSON array/object is properly closed. Each opening ``````` must be matched by a closing one.

## References

- [Homepage](https://github.com/fastapi/typer)
- [Documentation](https://typer.tiangolo.com)
- [Repository](https://github.com/fastapi/typer)
- [Issues](https://github.com/fastapi/typer/issues)
- [Changelog](https://typer.tiangolo.com/release-notes/)
