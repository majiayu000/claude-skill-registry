# 🔍 Skill: Static Analysis

## 📋 Metadata

| Atributo | Valor |
|----------|-------|
| **ID** | `static-analysis` |
| **Nivel** | 🟡 Intermedio |
| **Versión** | 2.0.0 |
| **Keywords** | `static-analysis`, `analyze`, `lint`, `code-quality`, `sast`, `security-scan`, `multi-language-linting`, `super-linter` |
| **Lenguajes Soportados** | Dart, Python, Go, Bash, PowerShell, Rust, JavaScript/Node.js |
| **Referencia** | [Dart Analysis Tools](https://dart.dev/tools/analysis) |

## 🔑 Keywords para Invocación

- `static-analysis`
- `analyze`
- `lint`
- `code-quality`
- `sast`
- `security-scan`
- `dart-analyze`
- `python-lint`
- `go-lint`
- `bash-lint`
- `powershell-lint`
- `rust-lint`
- `javascript-lint`
- `eslint`
- `ruff`
- `golangci-lint`
- `shellcheck`
- `clippy`
- `super-linter`
- `@skill:static-analysis`

### Ejemplos de Prompts

```
Configura análisis estático para el proyecto
```

```
Agrega herramientas de análisis de código y seguridad
```

```
@skill:static-analysis - Integra Dart Analyzer, Datadog y CodeRabbit
```

## 📖 Descripción

Skill para configurar y utilizar herramientas de análisis estático de código que detectan errores, vulnerabilidades de seguridad, problemas de calidad y code smells antes de que el código llegue a producción. Incluye linting para múltiples lenguajes (Dart, Python, Go, Bash, PowerShell, Rust, JavaScript/Node.js), integración con herramientas nativas, plataformas de seguridad como Datadog y herramientas de revisión de código con IA como CodeRabbit.

**⚠️ IMPORTANTE:** Todos los comandos de este skill deben ejecutarse desde la **raíz del proyecto** (donde existe el directorio `mobile/`). El skill incluye verificaciones para asegurar que se está en el directorio correcto antes de ejecutar cualquier comando.

### ✅ Cuándo Usar Este Skill

- Necesitas detectar errores y vulnerabilidades temprano
- Quieres mantener alta calidad de código
- Requieres análisis de seguridad automatizado
- Deseas integrar análisis en CI/CD pipelines
- Necesitas métricas de calidad de código

### ❌ Cuándo NO Usar Este Skill

- Proyectos muy pequeños o prototipos rápidos
- Cuando el overhead de análisis es prohibitivo
- Proyectos legacy que requieren migración gradual

## 🛠️ Herramientas Incluidas

### Tabla Resumen de Linters

| Lenguaje | Herramienta Principal | Herramientas Adicionales | Velocidad | Configuración |
|----------|----------------------|-------------------------|-----------|---------------|
| **Dart** | `dart analyze` | `dart format` | ⚡⚡⚡ Rápido | `analysis_options.yaml` |
| **Python** | `ruff` | `black`, `mypy`, `pylint` | ⚡⚡⚡ Muy Rápido | `pyproject.toml` |
| **Go** | `golangci-lint` | `go vet`, `staticcheck` | ⚡⚡ Medio | `.golangci.yml` |
| **Bash** | `shellcheck` | `shfmt` | ⚡⚡⚡ Rápido | `.shellcheckrc` (opcional) |
| **PowerShell** | `PSScriptAnalyzer` | - | ⚡⚡ Medio | `PSScriptAnalyzerSettings.psd1` |
| **Rust** | `clippy` | `rustfmt`, `cargo-audit` | ⚡⚡ Medio | `Cargo.toml`, `clippy.toml` |
| **JavaScript/Node.js** | `ESLint` | `Prettier`, `TypeScript ESLint` | ⚡⚡ Medio | `.eslintrc.json`, `.prettierrc.json` |

### 1. Dart Analysis Tools

Herramientas nativas de Dart para análisis estático de código.

**Referencia:** [Dart Analysis Tools](https://dart.dev/tools/analysis)

#### Comandos Principales

**⚠️ IMPORTANTE: Siempre ejecutar desde la raíz del proyecto (donde está el directorio `mobile/`)**

```bash
# Verificar que estás en la raíz del proyecto
# Debe existir el directorio mobile/
if [ ! -d "mobile" ]; then
    echo "Error: Debes ejecutar este comando desde la raíz del proyecto"
    exit 1
fi

# Análisis estático básico (desde la raíz, apuntando a mobile/)
cd mobile
dart analyze
cd ..

# O desde la raíz directamente
dart analyze mobile/lib/

# Análisis con salida JSON
cd mobile
dart analyze --format=json
cd ..

# Análisis con fatal-infos (falla si hay infos)
cd mobile
dart analyze --fatal-infos
cd ..

# Análisis de un directorio específico
cd mobile
dart analyze lib/
cd ..

# Verificar formato de código
cd mobile
dart format --set-exit-if-changed .
cd ..

# Auto-formatear código
cd mobile
dart format .
cd ..

# Ejecutar pruebas unitarias
cd mobile
flutter test
cd ..

# Ejecutar pruebas con cobertura
cd mobile
flutter test --coverage
cd ..

# Linting completo (Análisis + Formato)
cd mobile
flutter analyze && dart format --set-exit-if-changed .
cd ..
```

> [!TIP]
> Para el proyecto AltruPets, se recomienda usar el script especializado `apps/mobile/flutter-sast.sh` que centraliza estas operaciones.

#### Configuración: analysis_options.yaml

```yaml
# analysis_options.yaml
include: package:flutter_lints/flutter.yaml

analyzer:
  exclude:
    - "**/*.g.dart"
    - "**/*.freezed.dart"
    - "**/*.mocks.dart"
  errors:
    invalid_annotation_target: ignore
  language:
    strict-casts: true
    strict-inference: true
    strict-raw-types: true

linter:
  rules:
    # Errores comunes
    - always_declare_return_types
    - avoid_print
    - avoid_unnecessary_containers
    - prefer_const_constructors
    - prefer_const_literals_to_create_immutables

    # Seguridad
    - avoid_web_libraries_in_flutter
    - no_duplicate_case_values

    # Calidad
    - prefer_single_quotes
    - require_trailing_commas
    - sort_pub_dependencies
```

#### Integración en CI/CD

```yaml
# .github/workflows/analyze.yml
name: Static Analysis

on: [push, pull_request]

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Dart
        uses: dart-lang/setup-dart@v1
        with:
          dart-version: '3.0.0'

      - name: Install dependencies
        run: dart pub get

      - name: Verify formatting
        run: dart format --output=none --set-exit-if-changed .

      - name: Analyze code
        run: dart analyze --fatal-infos
```

### 2. Python Analysis Tools

Herramientas de análisis estático para código Python.

**Referencia:** [Ruff Documentation](https://docs.astral.sh/ruff/), [MyPy Documentation](https://mypy.readthedocs.io/)

#### Comandos Principales

```bash
# Análisis estático con Ruff (linting)
ruff check .

# Auto-fix con Ruff
ruff check --fix .

# Análisis de tipo con MyPy
mypy .

# Verificar formato con Black
black --check .

# Auto-formatear con Black
black .

# Análisis completo
ruff check . && black --check . && mypy .
```

#### Configuración: pyproject.toml

```toml
# pyproject.toml
[tool.ruff]
line-length = 100
target-version = "py311"
exclude = [
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    "build",
    "dist",
    "*.egg-info"
]

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "B",   # flake8-bugbear
    "C4",  # flake8-comprehensions
    "UP",  # pyupgrade
    "ARG", # flake8-unused-arguments
    "SIM", # flake8-simplify
]
ignore = [
    "E501",  # line too long (handled by formatter)
    "B008",  # do not perform function calls in argument defaults
]

[tool.ruff.lint.per-file-ignores]
"__init__.py" = ["F401"]  # unused imports
"tests/**" = ["S101", "ARG"]  # assert in tests, unused args
"scripts/**" = ["T201"]  # print statements allowed

[tool.ruff.format]
quote-style = "double"
indent-style = "space"

[tool.black]
line-length = 100
target-version = ['py311']
include = '\.pyi?$'
exclude = '''
/(
    \.git
  | \.venv
  | venv
  | build
  | dist
  | \.eggs
  | __pycache__
)/
'''

[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = false
disallow_incomplete_defs = false
check_untyped_defs = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
strict_equality = true
show_error_codes = true

[[tool.mypy.overrides]]
module = [
    "tests.*",
    "scripts.*",
]
disallow_untyped_defs = false
```

#### Integración en CI/CD

```yaml
# .github/workflows/python-analyze.yml
name: Python Static Analysis

on: [push, pull_request]

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install dependencies
        run: |
          pip install ruff black mypy

      - name: Run Ruff
        run: ruff check .

      - name: Check formatting with Black
        run: black --check .

      - name: Run MyPy
        run: mypy .
```

### 3. Go Analysis Tools

Herramientas de análisis estático para código Go.

**Referencia:** [golangci-lint Documentation](https://golangci-lint.run/), [Go Vet](https://pkg.go.dev/cmd/vet)

#### Comandos Principales

```bash
# Análisis estático con golangci-lint
golangci-lint run

# Análisis de un paquete específico
golangci-lint run ./pkg/...

# Auto-fix
golangci-lint run --fix

# Solo linters rápidos
golangci-lint run --fast

# Con timeout personalizado
golangci-lint run --timeout=10m

# Análisis con go vet
go vet ./...

# Análisis con staticcheck
staticcheck ./...
```

#### Configuración: .golangci.yml

```yaml
# .golangci.yml
run:
  timeout: 5m
  tests: true
  skip-dirs:
    - vendor
    - .git
  skip-files:
    - ".*\\.pb\\.go$"
    - ".*\\.gen\\.go$"

linters-settings:
  errcheck:
    check-type-assertions: true
    check-blank: true
  goconst:
    min-len: 2
    min-occurrences: 2
  gocritic:
    enabled-tags:
      - diagnostic
      - experimental
      - opinionated
      - performance
      - style
  govet:
    check-shadowing: true
  gocyclo:
    min-complexity: 15
  dupl:
    threshold: 100
  funlen:
    lines: 100
    statements: 50
  gci:
    local-prefixes: github.com/myorg/myrepo
  goimports:
    local-prefixes: github.com/myorg/myrepo
  misspell:
    locale: US

linters:
  enable:
    - errcheck
    - gosimple
    - govet
    - ineffassign
    - staticcheck
    - unused
    - gocritic
    - gofmt
    - goimports
    - revive
    - gocyclo
    - dupl
    - funlen
    - misspell
    - unconvert
    - unparam
    - whitespace

issues:
  exclude-rules:
    - path: _test\.go
      linters:
        - gocyclo
        - errcheck
        - dupl
        - funlen
    - path: (.*/)?(mocks|mock|testdata|vendor)/.*
      linters:
        - all
  max-issues-per-linter: 0
  max-same-issues: 0
```

#### Integración en CI/CD

```yaml
# .github/workflows/go-analyze.yml
name: Go Static Analysis

on: [push, pull_request]

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Go
        uses: actions/setup-go@v5
        with:
          go-version: '1.21'

      - name: Run golangci-lint
        uses: golangci/golangci-lint-action@v3
        with:
          version: latest
          args: --timeout=5m

      - name: Run go vet
        run: go vet ./...
```

### 4. Bash Analysis Tools

Herramientas de análisis estático para scripts Bash/Shell.

**Referencia:** [ShellCheck Documentation](https://www.shellcheck.net/), [shfmt](https://github.com/mvdan/sh)

#### Comandos Principales

```bash
# Análisis estático con ShellCheck
shellcheck script.sh

# Análisis recursivo de todos los scripts
find . -name "*.sh" -exec shellcheck {} +

# Análisis con salida JSON
shellcheck --format=json script.sh

# Formateo con shfmt
shfmt -w script.sh

# Verificar formato
shfmt -d script.sh

# Análisis completo
shellcheck *.sh && shfmt -d *.sh
```

#### Configuración: .shellcheckrc (opcional)

```bash
# .shellcheckrc
# Deshabilitar reglas específicas globalmente
# shellcheck disable=SC2034  # Unused variable
# shellcheck disable=SC1091  # Not following source

# O en el código:
# shellcheck disable=SC2034
VARIABLE="value"
```

**Configuración shfmt:**
```bash
# .editorconfig (para shfmt)
[*.sh]
indent_style = space
indent_size = 2
```

#### Integración en CI/CD

```yaml
# .github/workflows/bash-analyze.yml
name: Bash Static Analysis

on: [push, pull_request]

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install ShellCheck
        run: |
          sudo apt-get update
          sudo apt-get install -y shellcheck

      - name: Run ShellCheck
        run: |
          find . -name "*.sh" -not -path "*/vendor/*" -exec shellcheck {} +

      - name: Install shfmt
        run: |
          go install mvdan.cc/sh/v3/cmd/shfmt@latest

      - name: Check formatting with shfmt
        run: |
          shfmt -d .
```

### 5. PowerShell Analysis Tools

Herramientas de análisis estático para scripts PowerShell.

**Referencia:** [PSScriptAnalyzer Documentation](https://github.com/PowerShell/PSScriptAnalyzer)

#### Comandos Principales

**⚠️ IMPORTANTE: Siempre ejecutar desde la raíz del proyecto (donde está el directorio `mobile/`)**

```powershell
# Verificar que estás en la raíz del proyecto
# Debe existir el directorio mobile/
if (-not (Test-Path "mobile")) {
    Write-Error "Error: Debes ejecutar este comando desde la raíz del proyecto"
    exit 1
}

# Análisis estático con PSScriptAnalyzer (desde la raíz)
Invoke-ScriptAnalyzer -Path scripts/*.ps1

# Análisis recursivo de scripts
Get-ChildItem -Path scripts -Recurse -Filter *.ps1 | Invoke-ScriptAnalyzer

# Con configuración personalizada
Invoke-ScriptAnalyzer -Path scripts/setup.ps1 -Settings .vscode/PSScriptAnalyzerSettings.psd1

# Solo errores y warnings
Invoke-ScriptAnalyzer -Path scripts/*.ps1 -Severity Error, Warning

# Exportar a JSON
Invoke-ScriptAnalyzer -Path scripts/*.ps1 | ConvertTo-Json | Out-File report.json

# Análisis con reglas específicas
Invoke-ScriptAnalyzer -Path scripts/*.ps1 -IncludeRule PSPlaceOpenBrace, PSPlaceCloseBrace
```

#### Configuración: PSScriptAnalyzerSettings.psd1

```powershell
# PSScriptAnalyzerSettings.psd1
@{
    # Incluir reglas por defecto
    IncludeDefaultRules = $true

    # Excluir reglas específicas
    ExcludeRules = @(
        'PSAvoidUsingWriteHost',
        'PSUseShouldProcessForStateChangingFunctions'
    )

    # Configuración de reglas
    Rules = @{
        PSAvoidUsingCmdletAliases = @{
            Whitelist = @('cd', 'ls', 'cat')
        }
        PSPlaceOpenBrace = @{
            Enable = $true
            OnSameLine = $false
            NewLineAfter = $true
        }
        PSPlaceCloseBrace = @{
            Enable = $true
            NewLineAfter = $false
            IgnoreOneLineBlock = $true
        }
        PSProvideCommentHelp = @{
            Enable = $true
            ExportOnly = $false
            BlockComment = $true
            VSCodeSnippetCorrection = $true
            Placement = 'begin'
        }
        PSUseConsistentIndentation = @{
            Enable = $true
            IndentationSize = 4
            PipelineIndentation = 'IncreaseIndentationForFirstPipeline'
            Kind = 'space'
        }
        PSUseConsistentWhitespace = @{
            Enable = $true
            CheckInnerBrace = $true
            CheckOpenBrace = $true
            CheckOpenParen = $true
            CheckOperator = $true
            CheckPipe = $true
            CheckPipeForRedundantWhitespace = $true
            CheckSeparator = $true
            CheckParameter = $false
        }
    }
}
```

#### Integración en CI/CD

```yaml
# .github/workflows/powershell-analyze.yml
name: PowerShell Static Analysis

on: [push, pull_request]

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install PSScriptAnalyzer
        shell: pwsh
        run: |
          Install-Module -Name PSScriptAnalyzer -Scope CurrentUser -Force

      - name: Run PSScriptAnalyzer
        shell: pwsh
        run: |
          $scripts = Get-ChildItem -Recurse -Filter *.ps1 | Where-Object { $_.FullName -notmatch '\\vendor\\|\\node_modules\\' }
          if ($scripts) {
            $results = $scripts | Invoke-ScriptAnalyzer -Settings PSScriptAnalyzerSettings.psd1
            if ($results) {
              $results | Format-Table
              exit 1
            }
          }
```

### 6. Rust Analysis Tools

Herramientas de análisis estático para código Rust.

**Referencia:** [Clippy Documentation](https://rust-lang.github.io/rust-clippy/), [rustfmt](https://github.com/rust-lang/rustfmt), [cargo-audit](https://github.com/rustsec/rustsec/tree/main/cargo-audit)

#### Comandos Principales

```bash
# Análisis estático con Clippy
cargo clippy

# Con warnings como errores
cargo clippy -- -D warnings

# Solo errores específicos
cargo clippy -- -W clippy::all

# Análisis de un paquete específico
cargo clippy -p mypackage

# Formateo con rustfmt
cargo fmt

# Verificar formato
cargo fmt --check

# Auditoría de seguridad
cargo audit

# Análisis completo
cargo clippy -- -D warnings && cargo fmt --check && cargo audit
```

#### Configuración: Cargo.toml y clippy.toml

```toml
# Cargo.toml
[package]
name = "myproject"
version = "0.1.0"
edition = "2021"

[dependencies]

# Configuración de Clippy
[lints.clippy]
# Permitir algunos lints en desarrollo
warn = ["clippy::all"]
deny = [
    "clippy::unwrap_used",
    "clippy::expect_used",
    "clippy::panic",
    "clippy::todo",
    "clippy::unimplemented",
]
allow = [
    "clippy::too_many_arguments",  # Permitir en casos específicos
]
```

```toml
# clippy.toml (opcional - configuración adicional)
# Configuración adicional de Clippy
avoid-breaking-exported-api = false
msrv = "1.70.0"
```

#### Integración en CI/CD

```yaml
# .github/workflows/rust-analyze.yml
name: Rust Static Analysis

on: [push, pull_request]

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Rust
        uses: dtolnay/rust-toolchain@stable
        with:
          toolchain: stable
          components: rustfmt, clippy

      - name: Cache cargo registry
        uses: actions/cache@v3
        with:
          path: |
            ~/.cargo/bin/
            ~/.cargo/registry/index/
            ~/.cargo/registry/cache/
            ~/.cargo/git/db/
            target/
          key: ${{ runner.os }}-cargo-${{ hashFiles('**/Cargo.lock') }}

      - name: Run Clippy
        run: cargo clippy -- -D warnings

      - name: Check formatting
        run: cargo fmt --check

      - name: Install cargo-audit
        run: cargo install cargo-audit --locked

      - name: Run cargo audit
        run: cargo audit
```

### 7. JavaScript/Node.js Analysis Tools

Herramientas de análisis estático para código JavaScript y TypeScript.

**Referencia:** [ESLint Documentation](https://eslint.org/), [Prettier Documentation](https://prettier.io/), [TypeScript ESLint](https://typescript-eslint.io/)

#### Comandos Principales

```bash
# Análisis estático con ESLint
npx eslint .

# Auto-fix
npx eslint . --fix

# Análisis de archivos específicos
npx eslint src/**/*.{js,ts}

# Con formato de salida
npx eslint . --format=json

# Formateo con Prettier
npx prettier --write .

# Verificar formato
npx prettier --check .

# Análisis completo
npx eslint . && npx prettier --check .
```

#### Configuración: .eslintrc.json y .prettierrc.json

```json
// .eslintrc.json
{
  "env": {
    "node": true,
    "es2021": true,
    "browser": true
  },
  "extends": [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "plugin:@typescript-eslint/recommended-requiring-type-checking",
    "prettier"
  ],
  "parser": "@typescript-eslint/parser",
  "parserOptions": {
    "ecmaVersion": "latest",
    "sourceType": "module",
    "project": "./tsconfig.json"
  },
  "plugins": [
    "@typescript-eslint",
    "import",
    "node",
    "promise"
  ],
  "rules": {
    "no-console": "warn",
    "no-unused-vars": "off",
    "@typescript-eslint/no-unused-vars": ["error", { "argsIgnorePattern": "^_" }],
    "prefer-const": "error",
    "no-var": "error",
    "@typescript-eslint/explicit-function-return-type": "warn",
    "@typescript-eslint/no-explicit-any": "warn",
    "@typescript-eslint/explicit-module-boundary-types": "warn",
    "import/order": [
      "error",
      {
        "groups": ["builtin", "external", "internal", "parent", "sibling", "index"],
        "newlines-between": "always",
        "alphabetize": { "order": "asc" }
      }
    ],
    "node/no-unsupported-features/es-syntax": "off"
  },
  "ignorePatterns": [
    "dist/",
    "node_modules/",
    "*.config.js",
    "build/",
    "coverage/"
  ],
  "overrides": [
    {
      "files": ["*.test.ts", "*.spec.ts"],
      "rules": {
        "@typescript-eslint/no-explicit-any": "off"
      }
    }
  ]
}
```

```json
// .prettierrc.json
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 100,
  "tabWidth": 2,
  "useTabs": false,
  "arrowParens": "avoid",
  "endOfLine": "lf"
}
```

```json
// .prettierignore
node_modules
dist
build
coverage
*.min.js
package-lock.json
yarn.lock
```

#### Integración en CI/CD

```yaml
# .github/workflows/js-analyze.yml
name: JavaScript Static Analysis

on: [push, pull_request]

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run ESLint
        run: npx eslint .

      - name: Check Prettier formatting
        run: npx prettier --check .
```

### 8. Datadog Static Analysis Engine

Plataforma de análisis estático de código (SAST) que detecta vulnerabilidades de seguridad y problemas de calidad.

**Referencia:** [Datadog Static Analysis](https://docs.datadoghq.com/es/security/code_security/static_analysis/static_analysis_rules/)

#### Características Principales

- **Detección de vulnerabilidades:** Identifica problemas de seguridad comunes
- **Integración IDE:** Plugins para VS Code, IntelliJ, etc.
- **CI/CD Integration:** Integración nativa con pipelines
- **Reglas personalizables:** Configuración de reglas específicas del proyecto
- **Reportes detallados:** Dashboard con métricas y tendencias

#### Configuración Básica

```yaml
# datadog-static-analysis.yml
version: '1.0'

rules:
  # Reglas de seguridad
  - id: sql-injection
    severity: high
    enabled: true

  - id: xss-vulnerability
    severity: high
    enabled: true

  # Reglas de calidad
  - id: code-smell
    severity: medium
    enabled: true

  - id: performance-issue
    severity: low
    enabled: true

exclude:
  - "**/*.g.dart"
  - "**/generated/**"
```

#### Integración en CI/CD

```yaml
# .github/workflows/datadog-sast.yml
name: Datadog SAST

on: [push, pull_request]

jobs:
  datadog-sast:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Datadog Static Analysis
        uses: datadog/static-analysis-action@v1
        with:
          api-key: ${{ secrets.DATADOG_API_KEY }}
          app-key: ${{ secrets.DATADOG_APP_KEY }}
          fail-on-error: true
```

#### Configuración en VS Code

```json
// .vscode/settings.json
{
  "datadog.staticAnalysis.enabled": true,
  "datadog.staticAnalysis.severity": {
    "high": "error",
    "medium": "warning",
    "low": "info"
  },
  "datadog.staticAnalysis.exclude": [
    "**/*.g.dart",
    "**/generated/**"
  ]
}
```

### 9. CodeRabbit CLI

Herramienta de revisión de código impulsada por IA que detecta problemas antes de commits.

**Referencia:** [CodeRabbit CLI](https://docs.coderabbit.ai/cli/overview)

#### Instalación

```bash
# Instalación global
npm install -g @coderabbitai/cli

# O con yarn
yarn global add @coderabbitai/cli

# Verificar instalación
coderabbit --version
```

#### Configuración Básica

```yaml
# .coderabbit.yaml
language: dart
framework: flutter

rules:
  enabled:
    - security
    - performance
    - best-practices
    - code-quality

  disabled:
    - style-only

severity:
  critical: error
  high: error
  medium: warning
  low: info

exclude:
  - "**/*.g.dart"
  - "**/*.freezed.dart"
  - "test/**"
```

#### Uso Básico

```bash
# Análisis de cambios en staging
coderabbit review --staged

# Análisis de un commit específico
coderabbit review --commit HEAD

# Análisis de un rango de commits
coderabbit review --range main..feature-branch

# Análisis completo del proyecto
coderabbit review --all

# Análisis con salida JSON
coderabbit review --staged --format json

# Análisis con configuración personalizada
coderabbit review --config .coderabbit.yaml
```

#### Integración en Git Hooks

```bash
#!/bin/sh
# .git/hooks/pre-commit

# Ejecutar CodeRabbit en archivos staged
coderabbit review --staged --fail-on-error

if [ $? -ne 0 ]; then
  echo "❌ CodeRabbit encontró problemas. Por favor, corrígelos antes de commitear."
  exit 1
fi
```

#### Integración en CI/CD

```yaml
# .github/workflows/coderabbit.yml
name: CodeRabbit Review

on: [pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'

      - name: Install CodeRabbit CLI
        run: npm install -g @coderabbitai/cli

      - name: Run CodeRabbit Review
        env:
          CODERABBIT_API_KEY: ${{ secrets.CODERABBIT_API_KEY }}
        run: |
          coderabbit review \
            --range ${{ github.event.pull_request.base.sha }}..${{ github.event.pull_request.head.sha }} \
            --format json \
            --output coderabbit-report.json

      - name: Upload Report
        uses: actions/upload-artifact@v3
        with:
          name: coderabbit-report
          path: coderabbit-report.json
```

## 🏗️ Estructura de Configuración

```
project-root/
├── analysis_options.yaml          # Configuración Dart Analyzer
├── .coderabbit.yaml                # Configuración CodeRabbit
├── datadog-static-analysis.yml     # Configuración Datadog SAST
├── pyproject.toml                  # Configuración Python (Ruff)
├── .golangci.yml                    # Configuración Go (golangci-lint)
├── .eslintrc.json                  # Configuración JavaScript/TypeScript
├── .prettierrc.json                # Configuración Prettier
├── PSScriptAnalyzerSettings.psd1   # Configuración PowerShell
├── clippy.toml                     # Configuración Rust (opcional)
├── Cargo.toml                      # Configuración Rust
├── .github/
│   └── workflows/
│       ├── analyze.yml             # Workflow Dart Analyzer
│       ├── python-lint.yml         # Workflow Python
│       ├── go-lint.yml             # Workflow Go
│       ├── bash-lint.yml           # Workflow Bash
│       ├── powershell-lint.yml     # Workflow PowerShell
│       ├── rust-lint.yml           # Workflow Rust
│       ├── js-lint.yml             # Workflow JavaScript
│       ├── datadog-sast.yml        # Workflow Datadog
│       └── coderabbit.yml          # Workflow CodeRabbit
└── .git/
    └── hooks/
        └── pre-commit              # Git hook con linting multi-lenguaje
```

## 📊 Flujo de Trabajo Recomendado

### Desarrollo Local

1. **Pre-commit Hook:** Linting multi-lenguaje revisa cambios antes de commit
2. **IDE Integration:** Datadog y linters muestran problemas en tiempo real
3. **Verificación Manual:** Ejecutar linters específicos antes de push:
   - `dart analyze` (Dart)
   - `ruff check .` (Python)
   - `golangci-lint run` (Go)
   - `shellcheck *.sh` (Bash)
   - `Invoke-ScriptAnalyzer` (PowerShell)
   - `cargo clippy` (Rust)
   - `npx eslint .` (JavaScript)

### CI/CD Pipeline

1. **Linting Multi-Lenguaje:** Ejecución paralela de linters según archivos modificados
2. **Dart Analyzer:** Verificación de formato y análisis estático
3. **Datadog SAST:** Escaneo de seguridad y vulnerabilidades
4. **CodeRabbit Review:** Análisis de cambios en PRs

### Post-Deployment

1. **Monitoreo Continuo:** Datadog dashboard con métricas
2. **Reportes Periódicos:** Análisis de tendencias de calidad
3. **Retroalimentación:** Mejora continua de reglas

## 🎯 Mejores Prácticas

### 1. Configuración Gradual

```yaml
# Comienza con reglas básicas y aumenta gradualmente
linter:
  rules:
    # Fase 1: Reglas críticas
    - avoid_print
    - avoid_unnecessary_containers

    # Fase 2: Agregar después de estabilizar
    # - prefer_const_constructors
    # - require_trailing_commas
```

### 2. Exclusiones Inteligentes

```yaml
analyzer:
  exclude:
    # Código generado
    - "**/*.g.dart"
    - "**/*.freezed.dart"

    # Dependencias externas
    - ".dart_tool/**"
    - "build/**"

    # Archivos de configuración
    - "**/*.config.dart"
```

### 3. Severidad Configurada

```yaml
analyzer:
  errors:
    # Errores críticos
    missing_return: error
    invalid_assignment: error

    # Warnings importantes
    unused_element: warning
    dead_code: warning

    # Infos informativos
    todo: info
```

### 4. Integración en Desarrollo

```dart
// Usar comentarios para supresión controlada
// ignore: avoid_print
print('Debug info'); // Solo cuando sea necesario

// ignore_for_file: prefer_const_constructors
// Para archivos generados o legacy
```

### 5. Pre-commit Hook Multi-Lenguaje

**Herramienta:** `pre-commit` framework (recomendado) o scripts personalizados

**Instalación pre-commit:**
```bash
# Instalar pre-commit
pip install pre-commit

# O con Homebrew
brew install pre-commit
```

**Configuración:**
```yaml
# .pre-commit-config.yaml
repos:
  # Python
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.6
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  # Go
  - repo: https://github.com/golangci/golangci-lint
    rev: v1.55.2
    hooks:
      - id: golangci-lint

  # Bash
  - repo: https://github.com/shellcheck-py/shellcheck-py
    rev: v0.9.0.6
    hooks:
      - id: shellcheck

  # Rust
  - repo: https://github.com/doublify/pre-commit-rust
    rev: v1.0
    hooks:
      - id: fmt
      - id: clippy
        args: [--, -D, warnings]

  # JavaScript/TypeScript
  - repo: https://github.com/pre-commit/mirrors-eslint
    rev: v8.56.0
    hooks:
      - id: eslint
        files: \.(js|ts|jsx|tsx)$
        types: [file]
        additional_dependencies:
          - eslint@8.56.0
          - '@typescript-eslint/parser@6.19.0'
          - '@typescript-eslint/eslint-plugin@6.19.0'

  # Prettier
  - repo: https://github.com/pre-commit/mirrors-prettier
    rev: v3.1.1
    hooks:
      - id: prettier
        files: \.(js|ts|jsx|tsx|json|md|yaml|yml)$

  # Dart (script personalizado)
  - repo: local
    hooks:
      - id: dart-format
        name: dart format
        entry: bash -c 'dart format --set-exit-if-changed "$@"' --
        language: system
        types: [dart]
        pass_filenames: true
      - id: dart-analyze
        name: dart analyze
        entry: bash -c 'dart analyze "$@"' --
        language: system
        types: [dart]
        pass_filenames: true

  # PowerShell (script personalizado)
  - repo: local
    hooks:
      - id: powershell-analyzer
        name: PSScriptAnalyzer
        entry: pwsh -c 'Get-ChildItem "$@" | Invoke-ScriptAnalyzer' --
        language: system
        types: [text]
        files: \.ps1$
        pass_filenames: true
```

**Instalación de hooks:**
```bash
# Instalar hooks en .git/hooks/
pre-commit install

# Instalar hook para commit-msg también
pre-commit install --hook-type commit-msg

# Ejecutar manualmente en todos los archivos
pre-commit run --all-files
```

**Script pre-commit personalizado (alternativa):**
```bash
#!/bin/bash
# .git/hooks/pre-commit

set -e

echo "🔍 Ejecutando linting multi-lenguaje..."

# Detectar archivos modificados
STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM)

# Python
if echo "$STAGED_FILES" | grep -qE '\.(py)$'; then
  echo "🐍 Linting Python..."
  ruff check --fix $(echo "$STAGED_FILES" | grep -E '\.(py)$')
  black --check $(echo "$STAGED_FILES" | grep -E '\.(py)$')
fi

# Go
if echo "$STAGED_FILES" | grep -qE '\.(go)$'; then
  echo "🐹 Linting Go..."
  golangci-lint run $(echo "$STAGED_FILES" | grep -E '\.(go)$' | xargs dirname | sort -u)
fi

# Bash
if echo "$STAGED_FILES" | grep -qE '\.(sh)$'; then
  echo "🐚 Linting Bash..."
  shellcheck $(echo "$STAGED_FILES" | grep -E '\.(sh)$')
fi

# Rust
if echo "$STAGED_FILES" | grep -qE '\.(rs)$'; then
  echo "🦀 Linting Rust..."
  cargo clippy -- -D warnings
  cargo fmt --check
fi

# JavaScript/TypeScript
if echo "$STAGED_FILES" | grep -qE '\.(js|ts|jsx|tsx)$'; then
  echo "📦 Linting JavaScript/TypeScript..."
  npx eslint $(echo "$STAGED_FILES" | grep -E '\.(js|ts|jsx|tsx)$')
  npx prettier --check $(echo "$STAGED_FILES" | grep -E '\.(js|ts|jsx|tsx)$')
fi

# Dart
if echo "$STAGED_FILES" | grep -qE '\.(dart)$'; then
  echo "🎯 Linting Dart..."
  dart format --set-exit-if-changed $(echo "$STAGED_FILES" | grep -E '\.(dart)$')
  dart analyze $(echo "$STAGED_FILES" | grep -E '\.(dart)$')
fi

# PowerShell
if echo "$STAGED_FILES" | grep -qE '\.(ps1)$'; then
  echo "💻 Linting PowerShell..."
  pwsh -Command "Get-ChildItem $(echo "$STAGED_FILES" | grep -E '\.(ps1)$') | Invoke-ScriptAnalyzer"
fi

echo "✅ Linting completado exitosamente!"
```

## 🔧 Solución de Problemas

### Dart Analyzer muy lento

```yaml
# analysis_options.yaml
analyzer:
  exclude:
    - "**/*.g.dart"
    - "build/**"
  # Reducir profundidad de análisis
  strong-mode:
    implicit-casts: false
```

### Falsos positivos en Datadog

```yaml
# datadog-static-analysis.yml
rules:
  - id: false-positive-rule
    enabled: false
    # O ajustar severidad
    severity: low
```

### CodeRabbit no detecta cambios

```bash
# Asegurar que los cambios están staged
git add .
coderabbit review --staged

# O especificar rango explícito
coderabbit review --range HEAD~1..HEAD
```

## 📚 Recursos Adicionales

### Dart
- [Dart Analysis Tools Documentation](https://dart.dev/tools/analysis)
- [Flutter Lints Package](https://pub.dev/packages/flutter_lints)
- [Dart Code Metrics](https://pub.dev/packages/dart_code_metrics)

### Python
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [Black Code Formatter](https://black.readthedocs.io/)
- [MyPy Type Checker](https://mypy.readthedocs.io/)
- [Pylint Documentation](https://pylint.readthedocs.io/)

### Go
- [golangci-lint Documentation](https://golangci-lint.run/)
- [Go Vet Documentation](https://pkg.go.dev/cmd/vet)
- [Staticcheck](https://staticcheck.io/)

### Bash
- [ShellCheck Documentation](https://www.shellcheck.net/)
- [shfmt Formatter](https://github.com/mvdan/sh)

### PowerShell
- [PSScriptAnalyzer Documentation](https://github.com/PowerShell/PSScriptAnalyzer)
- [PowerShell Best Practices](https://learn.microsoft.com/en-us/powershell/scripting/developer/cmdlet/strongly-encouraged-development-guidelines)

### Rust
- [Clippy Documentation](https://rust-lang.github.io/rust-clippy/)
- [rustfmt Documentation](https://github.com/rust-lang/rustfmt)
- [cargo-audit](https://github.com/rustsec/rustsec/tree/main/cargo-audit)

### JavaScript/Node.js
- [ESLint Documentation](https://eslint.org/)
- [Prettier Documentation](https://prettier.io/)
- [TypeScript ESLint](https://typescript-eslint.io/)

### Herramientas Generales
- [GitHub Super-Linter](https://github.com/super-linter/super-linter)
- [pre-commit Framework](https://pre-commit.com/)
- [Datadog Static Analysis Rules](https://docs.datadoghq.com/es/security/code_security/static_analysis/static_analysis_rules/)
- [CodeRabbit CLI Documentation](https://docs.coderabbit.ai/cli/overview)

## 🎓 Ejemplos de Uso

### ⚠️ Regla Fundamental: Verificar Directorio de Trabajo

**Todos los comandos deben ejecutarse desde la raíz del proyecto** (donde existe el directorio `mobile/`). Los skills deben incluir esta verificación:

```bash
# Verificación en Bash
if [ ! -d "mobile" ]; then
    echo "Error: Ejecuta este comando desde la raíz del proyecto"
    exit 1
fi
```

```powershell
# Verificación en PowerShell
if (-not (Test-Path "mobile")) {
    Write-Error "Error: Ejecuta este comando desde la raíz del proyecto"
    exit 1
fi
```

### Ejemplo 1: Setup Multi-Lenguaje Completo

```bash
# Verificar que estamos en la raíz del proyecto
if [ ! -d "mobile" ]; then
    echo "Error: Ejecuta este comando desde la raíz del proyecto"
    exit 1
fi

# 1. Instalar herramientas de linting

# Python
pip install ruff black mypy

# Go
go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest

# Bash
sudo apt-get install shellcheck  # Linux
# brew install shellcheck          # macOS

# Rust (ya viene con rustup)
rustup component add clippy rustfmt

# JavaScript/Node.js
npm install --save-dev eslint prettier

# PowerShell (desde PowerShell)
Install-Module -Name PSScriptAnalyzer -Scope CurrentUser -Force

# 2. Configurar pre-commit
pip install pre-commit
pre-commit install

# 3. Crear .pre-commit-config.yaml (ver sección anterior)

# 4. Verificar todo
pre-commit run --all-files
```

### Ejemplo 2: Setup Inicial Completo (Dart)

```bash
# Verificar que estamos en la raíz del proyecto
if [ ! -d "mobile" ]; then
    echo "Error: Ejecuta este comando desde la raíz del proyecto"
    exit 1
fi

# 1. Crear analysis_options.yaml en mobile/
cat > mobile/analysis_options.yaml << EOF
include: package:flutter_lints/flutter.yaml

analyzer:
  exclude:
    - "**/*.g.dart"
  language:
    strict-casts: true

linter:
  rules:
    - avoid_print
    - prefer_const_constructors
EOF

# 2. Instalar CodeRabbit
npm install -g @coderabbitai/cli

# 3. Crear configuración CodeRabbit
cat > .coderabbit.yaml << EOF
language: dart
framework: flutter
rules:
  enabled:
    - security
    - performance
EOF

# 4. Verificar análisis (desde la raíz)
cd mobile
dart analyze
cd ..
coderabbit review --all
```

### Ejemplo 3: Integración Multi-Lenguaje en CI/CD

```yaml
# .github/workflows/multi-lang-lint.yml
name: Multi-Language Linting

on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        language: [dart, python, go, bash, rust, javascript]

    steps:
      - uses: actions/checkout@v4

      # Dart
      - name: Setup Dart
        if: matrix.language == 'dart'
        uses: dart-lang/setup-dart@v1

      - name: Run Dart Analysis
        if: matrix.language == 'dart'
        run: |
          dart pub get
          dart format --set-exit-if-changed .
          dart analyze --fatal-infos

      # Python
      - name: Setup Python
        if: matrix.language == 'python'
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install Python Linters
        if: matrix.language == 'python'
        run: |
          pip install ruff black mypy

      - name: Run Python Linters
        if: matrix.language == 'python'
        run: |
          ruff check .
          black --check .
          mypy .

      # Go
      - name: Setup Go
        if: matrix.language == 'go'
        uses: actions/setup-go@v5
        with:
          go-version: '1.21'

      - name: Run Go Linters
        if: matrix.language == 'go'
        uses: golangci/golangci-lint-action@v3
        with:
          version: latest

      # Bash
      - name: Install ShellCheck
        if: matrix.language == 'bash'
        run: sudo apt-get install -y shellcheck

      - name: Run ShellCheck
        if: matrix.language == 'bash'
        run: |
          find . -name "*.sh" -exec shellcheck {} +

      # Rust
      - name: Setup Rust
        if: matrix.language == 'rust'
        uses: dtolnay/rust-toolchain@stable
        with:
          toolchain: stable
          components: rustfmt, clippy

      - name: Run Rust Linters
        if: matrix.language == 'rust'
        run: |
          cargo clippy -- -D warnings
          cargo fmt --check
          cargo audit

      # JavaScript/Node.js
      - name: Setup Node.js
        if: matrix.language == 'javascript'
        uses: actions/setup-node@v4
        with:
          node-version: '18'

      - name: Install Node.js Dependencies
        if: matrix.language == 'javascript'
        run: npm ci

      - name: Run JavaScript Linters
        if: matrix.language == 'javascript'
        run: |
          npx eslint .
          npx prettier --check .
```

### Ejemplo 4: Integración en CI/CD (Original)

```yaml
# .github/workflows/static-analysis.yml
name: Static Analysis Suite

on: [push, pull_request]

jobs:
  dart-analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: dart-lang/setup-dart@v1
      - run: dart pub get
      - run: dart format --set-exit-if-changed .
      - run: dart analyze --fatal-infos

  datadog-sast:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: datadog/static-analysis-action@v1
        with:
          api-key: ${{ secrets.DATADOG_API_KEY }}

  coderabbit-review:
    runs-on: ubuntu-latest
    if: github.event_name == 'pull_request'
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: actions/setup-node@v4
      - run: npm install -g @coderabbitai/cli
      - run: |
          coderabbit review \
            --range ${{ github.event.pull_request.base.sha }}..${{ github.event.pull_request.head.sha }}
```

---

**Última actualización:** Diciembre 2025
**Versión:** 2.0.0
**Cambios v2.0.0:** Agregado soporte completo para linting multi-lenguaje (Python, Go, Bash, PowerShell, Rust, JavaScript/Node.js)
