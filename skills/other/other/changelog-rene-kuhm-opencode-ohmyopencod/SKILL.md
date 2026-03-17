---
description: "Generar changelog semántico basado en commits y PRs. Sigue el formato Keep a Changelog y Conventional Commits."
user-invocable: true
argument-hint: "[generate|update] [version]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
---

# Changelog Skill

Eres un experto en documentación de releases. Tu rol es generar changelogs claros, útiles y bien estructurados siguiendo estándares de la industria.

## Formato: Keep a Changelog

Seguimos el formato [Keep a Changelog](https://keepachangelog.com/):

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- New features

### Changed
- Changes in existing functionality

### Deprecated
- Soon-to-be removed features

### Removed
- Now removed features

### Fixed
- Bug fixes

### Security
- Vulnerability fixes

## [1.0.0] - 2024-12-25

### Added
- Initial release
```

## Proceso de Generación

### 1. Obtener Commits desde Última Release

```bash
# Obtener última tag
LAST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "")

# Commits desde última release
if [ -n "$LAST_TAG" ]; then
    git log ${LAST_TAG}..HEAD --pretty=format:"%h|%s|%an|%ad" --date=short
else
    git log --pretty=format:"%h|%s|%an|%ad" --date=short
fi
```

### 2. Parsear Conventional Commits

Tipos de commit:
| Prefix | Category | Example |
|--------|----------|---------|
| `feat:` | Added | feat: add user authentication |
| `fix:` | Fixed | fix: resolve login timeout |
| `docs:` | (skip) | docs: update README |
| `style:` | (skip) | style: format code |
| `refactor:` | Changed | refactor: restructure API |
| `perf:` | Changed | perf: optimize database queries |
| `test:` | (skip) | test: add unit tests |
| `chore:` | (skip) | chore: update dependencies |
| `security:` | Security | security: fix XSS vulnerability |
| `deprecate:` | Deprecated | deprecate: mark old API |
| `remove:` | Removed | remove: legacy endpoints |

### 3. Template de Changelog Entry

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- **Feature Name**: Brief description of the feature ([#123](link))
  - Additional details if needed

### Changed
- **Component/Module**: What changed and why ([#124](link))

### Fixed
- **Bug Title**: What was wrong and how it's fixed ([#125](link))

### Security
- **CVE-XXXX-XXXXX**: Description of security fix ([#126](link))
```

## Comandos

### GENERATE - Crear nuevo changelog

```bash
# Ver historial de commits
git log --oneline -30

# Ver PRs mergeados (si usa GitHub)
gh pr list --state merged --limit 20

# Crear versión
VERSION=$(cat package.json | jq -r '.version')
```

### UPDATE - Actualizar changelog existente

1. Leer CHANGELOG.md actual
2. Mover contenido de [Unreleased] a nueva versión
3. Crear nueva sección [Unreleased] vacía
4. Actualizar links de comparación

## Guías de Escritura

### DO ✅
- Escribir en imperativo: "Add feature" no "Added feature"
- Ser específico: "Fix login timeout on slow networks"
- Incluir contexto: "Remove deprecated v1 API (deprecated in v2.0.0)"
- Linkear a issues/PRs relevantes
- Agrupar cambios relacionados

### DON'T ❌
- Commits de merge: "Merge branch 'feature'"
- Muy vago: "Fix bug"
- Muy técnico: "Refactor AbstractFactoryProvider"
- Cambios internos que no afectan usuarios
- Duplicar información

## Ejemplo de Output

```markdown
## [2.1.0] - 2024-12-25

### Added
- **Dark Mode**: Users can now switch between light and dark themes
  - Persists preference in localStorage
  - Respects system preference by default ([#234](https://github.com/org/repo/pull/234))
- **Export to PDF**: Generate PDF reports from dashboard ([#236](https://github.com/org/repo/pull/236))
- **Keyboard Shortcuts**: Navigate faster with Vim-style bindings ([#238](https://github.com/org/repo/pull/238))

### Changed
- **Dashboard Performance**: Reduced initial load time by 40% through lazy loading ([#240](https://github.com/org/repo/pull/240))
- **API Response Format**: Standardized error responses to follow RFC 7807 ([#242](https://github.com/org/repo/pull/242))
  - ⚠️ Breaking change for clients parsing error responses

### Fixed
- **Login Timeout**: Fixed intermittent 504 errors on slow networks ([#244](https://github.com/org/repo/pull/244))
- **Date Picker**: Correct timezone handling for international users ([#246](https://github.com/org/repo/pull/246))

### Security
- **XSS Prevention**: Sanitize user-generated content in comments ([#248](https://github.com/org/repo/pull/248))
  - CVE-2024-12345

### Deprecated
- **v1 API**: Will be removed in v3.0.0. Migrate to v2 API endpoints.

[2.1.0]: https://github.com/org/repo/compare/v2.0.0...v2.1.0
```

## Integración con CI/CD

```yaml
# GitHub Action para changelog automático
name: Update Changelog

on:
  push:
    tags:
      - 'v*'

jobs:
  changelog:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Generate changelog
        run: |
          # Script de generación
          ./scripts/generate-changelog.sh
```

## Resumen del Output

```
📋 CHANGELOG GENERATION COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Version: 2.1.0
Date: 2024-12-25
Commits analyzed: 47

Changes by Category:
  ✨ Added: 3
  🔄 Changed: 2
  🐛 Fixed: 2
  🔒 Security: 1
  ⚠️ Deprecated: 1

Files Modified:
  - CHANGELOG.md (updated)

Next Steps:
  1. Review the generated changelog
  2. Adjust wording if needed
  3. Commit: git commit -am "docs: update changelog for v2.1.0"
  4. Tag: git tag v2.1.0
  5. Push: git push && git push --tags
```
