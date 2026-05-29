---
# VERSION: 2.88.1
name: gates
description: "9-language quality gate validation: linting, formatting, type checking, and test execution. Validates code changes meet quality standards before completion. Use when: (1) after code implementation, (2) before PR creation, (3) as part of /orchestrator Step 6, (4) manual quality check. Triggers: /gates, 'quality gates', 'run validation', 'check quality', 'validate code'."
context: fork
user-invocable: true
allowed-tools:
  - LSP
  - Read
  - Bash
  - Grep
  - Glob
hooks:
  PreToolUse:
    - path: .claude/hooks/validate-lsp-servers.sh
      match_tool: LSP
---

# Gates - Quality Validation (v2.37)

Comprehensive quality validation across 9 programming languages with **TLDR-assisted analysis**.

## v2.88 Key Changes (MODEL-AGNOSTIC)

- **Model-agnostic**: Uses model configured in `~/.claude/settings.json` or CLI/env vars
- **No flags required**: Works with the configured default model
- **Flexible**: Works with GLM-5, Claude, Minimax, or any configured model
- **Settings-driven**: Model selection via `ANTHROPIC_DEFAULT_*_MODEL` env vars

## Quick Start

```bash
/gates              # Run all quality gates
ralph gates         # Via CLI
ralph gates src/    # Specific directory
```

## LSP Usage for Type Checking

**IMPORTANT**: Use LSP for efficient type checking instead of reading entire files.

### When to Use LSP
- Type checking TypeScript/JavaScript files
- Finding type errors without running `tsc --noEmit`
- Getting hover information for symbols
- Finding references across the codebase

### LSP Commands
```yaml
# Type check a specific file (TypeScript)
LSP:
  server: typescript-language-server
  action: diagnostics
  file: src/auth/login.ts

# Get hover information for a symbol
LSP:
  server: typescript-language-server
  action: hover
  file: src/auth/login.ts
  line: 42
  character: 10

# Find all references
LSP:
  server: typescript-language-server
  action: references
  file: src/auth/login.ts
  line: 42
  character: 10

# Python type checking with pyright
LSP:
  server: pyright
  action: diagnostics
  file: src/auth/login.py
```

### LSP vs Traditional Type Checking
| Method | Tokens Used | Speed | Use Case |
|--------|-------------|-------|----------|
| `tsc --noEmit` | HIGH (reads all files) | Slow | Full project check |
| `LSP diagnostics` | LOW (indexed access) | Fast | Single file check |
| `LSP hover` | MINIMAL | Instant | Quick type lookup |

## Pre-Gates: TLDR Language Detection (v2.37)

**AUTOMATIC** - Detect project languages efficiently:

```bash
# Get codebase structure to detect languages (95% token savings)
tldr structure . > /tmp/project-structure.md

# From structure, identify:
# - Primary language(s)
# - Config files present
# - Test frameworks used
```

## Supported Languages

| Language | Linter | Formatter | Types |
|----------|--------|-----------|-------|
| TypeScript | ESLint | Prettier | tsc |
| JavaScript | ESLint | Prettier | - |
| Python | Ruff | Black | mypy |
| Rust | Clippy | rustfmt | cargo check |
| Go | golint | gofmt | go vet |
| Java | Checkstyle | google-java-format | - |
| Ruby | RuboCop | - | Sorbet |
| PHP | PHP_CodeSniffer | php-cs-fixer | PHPStan |
| Solidity | Solhint | prettier-solidity | - |

## Workflow

### 1. Detect Languages
```bash
# Auto-detect based on file extensions and config files
```

### 2. Run Linters
```bash
# Per-language linting
npx eslint src/          # TypeScript/JavaScript
ruff check .             # Python
cargo clippy             # Rust
golangci-lint run        # Go
```

### 3. Check Formatting
```bash
npx prettier --check .   # JS/TS
black --check .          # Python
rustfmt --check src/     # Rust
gofmt -l .               # Go
```

### 4. Type Checking
```bash
npx tsc --noEmit         # TypeScript
mypy .                   # Python
cargo check              # Rust
go vet ./...             # Go
```

### 5. Run Tests
```bash
npm test                 # Node projects
pytest                   # Python
cargo test               # Rust
go test ./...            # Go
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All gates passed |
| 1 | Lint errors |
| 2 | Format errors |
| 3 | Type errors |
| 4 | Test failures |

## Gate Configuration

### Minimal (fast)
```bash
ralph gates --minimal    # Lint only
```

### Standard (default)
```bash
ralph gates              # Lint + Format + Types
```

### Full (CI)
```bash
ralph gates --full       # Lint + Format + Types + Tests
```

## Integration

- Invoked by /orchestrator in Step 6
- **Pre-step: tldr structure for language detection** (v2.37)
- Must pass before VERIFIED_DONE
- Hooks: `quality-gates.sh` (PostToolUse)

## TLDR Integration (v2.37)

| Phase | TLDR Command | Purpose |
|-------|--------------|---------|
| Language detection | `tldr structure .` | Identify languages |
| Error context | `tldr context $FILE .` | Understand failing code |
| Impact analysis | `tldr deps $FILE .` | Find related tests |

## Agent Teams Integration (v2.88)

**Optimal Scenario**: Integrated (Agent Teams + Custom Subagents)

Quality gates use Agent Teams coordination with specialized ralph-tester agents for parallel quality validation.

### Why Scenario C for Gates
- Multiple quality checks require coordination (lint, format, type, test)
- Quality gates are meta-validation (hooks validate the validators)
- Language-specific specialization via ralph-tester
- TeammateIdle/TaskCompleted hooks for quality enforcement

### Subagent Roles

| Subagent | Role in Gates |
|----------|---------------|
| `ralph-tester` | Execute test suites in parallel |
| `ralph-reviewer` | Analyze code quality issues |
| `ralph-coder` | Apply auto-fixes for linting/formatting |

### Parallel Gates Execution
When Agent Teams is active, gates run in parallel across subagents:
1. **Team Lead** creates task list with gate phases
2. **ralph-tester** runs tests concurrently
3. **ralph-reviewer** reviews linter output
4. **ralph-coder** applies fixes

### Quality Gate Hooks
- `TeammateIdle`: Triggers before agent goes idle
- `TaskCompleted`: Validates gate completion

## Action Reporting (v2.93.0)

**Los resultados de `/gates` generan reportes automáticos completos**:

### Reporte Automático

Cuando `/gates` completa, se genera automáticamente:

1. **En la conversación de Claude**: Resultados visibles de todas las validaciones
2. **En el repositorio**: `docs/actions/gates/{timestamp}.md`
3. **Metadatos JSON**: `.claude/metadata/actions/gates/{timestamp}.json`

### Contenido del Reporte

Cada reporte incluye:
- ✅ **Summary**: Tipo de validación ejecutada
- ✅ **Results**: Resultados de linters, formatters, type checkers, tests
- ✅ **Errors**: Errores encontrados por categoría
- ✅ **Recommendations**: Acciones correctivas sugeridas
- ✅ **Next Steps**: Qué hacer según el resultado

### Generación Manual (Opcional)

```bash
# Al inicio
source .claude/lib/action-report-lib.sh
start_action_report "gates" "Running quality gates on src/"

# Ejecutar validaciones
if ! npx tsc --noEmit; then
    record_error "TypeScript errors found"
fi

if ! npx eslint .; then
    record_error "ESLint violations found"
fi

if ! npm test; then
    record_error "Test failures found"
fi

# Al completar
if [[ ${#CURRENT_ACTION_ERRORS[@]} -eq 0 ]]; then
    complete_action_report \
        "success" \
        "All quality gates passed" \
        "Safe to commit: git commit -m 'chore: pass quality gates'"
else
    complete_action_report \
        "failed" \
        "Quality gates failed" \
        "Fix errors and run /gates again"
fi
```

### Ver Reportes Anteriores

```bash
# Listar todos los reportes de gates
ls -lt docs/actions/gates/

# Ver el reporte más reciente
cat $(ls -t docs/actions/gates/*.md | head -1)

# Buscar reportes fallidos
grep -l "Status: FAILED" docs/actions/gates/*.md

# Ver tendencia de calidad
grep -c "Status: COMPLETED" docs/actions/gates/*.md
grep -c "Status: FAILED" docs/actions/gates/*.md
```

### Integración CI/CD

Los metadatos JSON permiten integración con pipelines:

```bash
# En tu CI pipeline
source .claude/lib/action-report-generator.sh

# Ejecutar gates
/gates

# Obtener resultado del último reporte
latest_report=$(find_latest_report "gates")
status=$(grep "Status:" "$latest_report" | awk '{print $2}')

if [[ "$status" != "COMPLETED" ]]; then
    echo "Quality gates failed - blocking commit"
    exit 1
fi
```

### Referencias del Sistema de Reportes

- [Action Reports System](docs/actions/README.md) - Documentación completa
- [action-report-lib.sh](.claude/lib/action-report-lib.sh) - Librería helper
- [action-report-generator.sh](.claude/lib/action-report-generator.sh) - Generador

## Anti-Patterns

- Never skip gates for "quick fixes"
- Never ignore type errors
- Never commit with lint warnings
