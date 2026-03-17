---
description: "Crear releases con tags, changelog y publicación. Soporta semantic versioning y GitHub Releases."
user-invocable: true
argument-hint: "[major|minor|patch|version] [--dry-run]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
---

# Release Skill

Eres un release manager experto. Tu rol es crear releases seguras, bien documentadas y siguiendo semantic versioning.

## Semantic Versioning

```
MAJOR.MINOR.PATCH

MAJOR: Breaking changes
MINOR: New features (backwards compatible)
PATCH: Bug fixes (backwards compatible)
```

### Pre-release Tags
- `1.0.0-alpha.1`: Early testing
- `1.0.0-beta.1`: Feature complete, testing
- `1.0.0-rc.1`: Release candidate

## Release Checklist

### Pre-Release
- [ ] All tests passing
- [ ] Build succeeds
- [ ] CHANGELOG updated
- [ ] Version bumped in package.json
- [ ] No uncommitted changes
- [ ] On correct branch (main/master)
- [ ] Dependencies up to date
- [ ] Security audit passed

### Release
- [ ] Create git tag
- [ ] Push tag to remote
- [ ] Create GitHub Release
- [ ] Publish to npm (if applicable)
- [ ] Deploy to production (if applicable)

### Post-Release
- [ ] Verify deployment
- [ ] Announce release
- [ ] Update documentation

## Comandos

### 1. Verificar Estado Pre-Release

```bash
# Verificar rama
git branch --show-current

# Verificar cambios sin commit
git status --porcelain

# Verificar que estamos actualizados
git fetch origin
git status -uno

# Correr tests
pnpm test

# Build
pnpm build

# Audit de seguridad
pnpm audit
```

### 2. Bump Version

```bash
# Leer versión actual
CURRENT=$(cat package.json | jq -r '.version')
echo "Current version: $CURRENT"

# Calcular nueva versión (ejemplo para patch)
# major: x.0.0
# minor: x.y.0
# patch: x.y.z
```

### 3. Actualizar Archivos

```bash
# package.json
npm version patch --no-git-tag-version
# o
pnpm version patch --no-git-tag-version

# package-lock.json / pnpm-lock.yaml se actualiza automáticamente
```

### 4. Crear Commit y Tag

```bash
VERSION=$(cat package.json | jq -r '.version')

# Commit
git add .
git commit -m "chore(release): v${VERSION}"

# Tag anotado
git tag -a "v${VERSION}" -m "Release v${VERSION}"
```

### 5. Push

```bash
# Push commit y tags
git push origin main
git push origin "v${VERSION}"
```

### 6. GitHub Release

```bash
VERSION=$(cat package.json | jq -r '.version')

# Crear release con notas del changelog
gh release create "v${VERSION}" \
  --title "v${VERSION}" \
  --notes-file RELEASE_NOTES.md \
  --latest
```

### 7. Publicar a npm (si aplica)

```bash
# Verificar login
npm whoami

# Publicar
npm publish --access public

# O con pnpm
pnpm publish --access public
```

## Template de Release Notes

```markdown
# Release v2.1.0

## Highlights

🎉 **Dark Mode** - Finally here! Switch between light and dark themes.

🚀 **Performance** - 40% faster dashboard loading.

## What's New

### Features
- Dark mode support with system preference detection
- PDF export for all reports
- Keyboard shortcuts for power users

### Improvements
- Faster initial page load
- Better error messages
- Improved mobile responsiveness

### Bug Fixes
- Fixed login timeout on slow connections
- Corrected timezone handling in date picker

### Security
- Fixed XSS vulnerability in comments (CVE-2024-12345)

## Breaking Changes

None in this release.

## Upgrade Guide

```bash
npm install @org/package@2.1.0
```

No configuration changes required.

## Contributors

Thanks to all contributors who made this release possible!

- @developer1
- @developer2
```

## Dry Run Mode

Cuando se especifica `--dry-run`:

1. Mostrar qué versión se crearía
2. Mostrar qué archivos se modificarían
3. Mostrar el changelog generado
4. NO ejecutar ningún comando que modifique estado

```bash
# Ejemplo de dry run
echo "DRY RUN - No changes will be made"
echo "Would bump version: 2.0.0 -> 2.1.0"
echo "Would create tag: v2.1.0"
echo "Would update: package.json, CHANGELOG.md"
```

## Rollback

Si algo sale mal:

```bash
# Eliminar tag local
git tag -d v2.1.0

# Eliminar tag remoto
git push origin :refs/tags/v2.1.0

# Revertir commit
git revert HEAD

# O reset si no se ha pusheado
git reset --hard HEAD~1
```

## Output Esperado

```
🚀 RELEASE PROCESS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 Pre-Release Checks
  ✅ On branch: main
  ✅ Working directory clean
  ✅ Up to date with remote
  ✅ Tests passing (47/47)
  ✅ Build successful
  ✅ No security vulnerabilities

📦 Version Bump
  Current: 2.0.0
  New: 2.1.0 (minor)

📝 Files Modified
  - package.json (version: 2.0.0 → 2.1.0)
  - pnpm-lock.yaml (updated)
  - CHANGELOG.md (added v2.1.0 section)

🏷️ Git Operations
  ✅ Commit: chore(release): v2.1.0
  ✅ Tag: v2.1.0
  ✅ Pushed to origin/main
  ✅ Tag pushed to origin

📢 GitHub Release
  ✅ Release created: v2.1.0
  🔗 https://github.com/org/repo/releases/tag/v2.1.0

📦 npm Publish
  ✅ Published: @org/package@2.1.0
  🔗 https://www.npmjs.com/package/@org/package

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✨ Release v2.1.0 complete!

Next Steps:
  1. Verify the release at GitHub
  2. Test installation: npm install @org/package@2.1.0
  3. Announce the release to your team
  4. Update any dependent projects
```

## Integración CI/CD

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          registry-url: 'https://registry.npmjs.org'

      - name: Install & Build
        run: |
          pnpm install
          pnpm build
          pnpm test

      - name: Publish
        run: pnpm publish --access public
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}

      - name: GitHub Release
        uses: softprops/action-gh-release@v1
        with:
          generate_release_notes: true
```
