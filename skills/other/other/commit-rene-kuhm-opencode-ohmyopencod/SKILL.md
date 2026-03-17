---
description: "Crear commits siguiendo Conventional Commits. Analiza cambios y genera mensajes descriptivos."
user-invocable: true
argument-hint: "[--amend] [mensaje opcional]"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
---

# Commit Skill

Eres un experto en git y Conventional Commits. Tu rol es crear commits bien estructurados, descriptivos y siguiendo las mejores prácticas.

## Conventional Commits Format

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

### Types

| Type | Descripción | Ejemplo |
|------|-------------|---------|
| `feat` | Nueva funcionalidad | `feat(auth): add Google OAuth login` |
| `fix` | Bug fix | `fix(cart): resolve quantity calculation error` |
| `docs` | Documentación | `docs(readme): update installation steps` |
| `style` | Formato (no afecta código) | `style(components): format with Biome` |
| `refactor` | Refactoring | `refactor(api): extract validation logic` |
| `perf` | Performance | `perf(images): add lazy loading` |
| `test` | Tests | `test(auth): add unit tests for login` |
| `build` | Build/dependencies | `build(deps): upgrade React to v19` |
| `ci` | CI/CD | `ci(github): add deploy workflow` |
| `chore` | Mantenimiento | `chore(scripts): update dev scripts` |
| `revert` | Revert commit | `revert: feat(auth): add Google OAuth` |

### Scopes Comunes

```
auth, api, ui, db, config, deps, docs, test, ci, build
components, hooks, services, utils, types, styles
```

## Flujo de Trabajo

### 1. Analizar Cambios

```bash
# Ver estado
git status

# Ver cambios unstaged
git diff

# Ver cambios staged
git diff --cached

# Ver archivos modificados
git diff --name-only

# Ver commits recientes (para estilo)
git log --oneline -10
```

### 2. Clasificar Cambios

Analizar los cambios y determinar:
- **Type**: ¿Qué tipo de cambio es?
- **Scope**: ¿Qué área del código afecta?
- **Breaking Change**: ¿Rompe compatibilidad?

### 3. Generar Mensaje

#### Commit Simple
```bash
git commit -m "feat(auth): add password reset functionality"
```

#### Commit con Body
```bash
git commit -m "$(cat <<'EOF'
feat(auth): add password reset functionality

- Add forgot password page
- Implement email sending service
- Add password reset token validation
- Create new password form

Closes #123
EOF
)"
```

#### Breaking Change
```bash
git commit -m "$(cat <<'EOF'
feat(api)!: change response format for user endpoints

BREAKING CHANGE: User API now returns nested objects instead of flat structure.

Before: { id, name, email }
After: { id, profile: { name, email } }

Migration: Update all clients to access user.profile.name instead of user.name
EOF
)"
```

## Reglas de Mensajes

### DO ✅

```bash
# Específico y descriptivo
feat(products): add price filtering by range

# Incluye contexto cuando es útil
fix(checkout): resolve race condition in payment processing

# Breaking changes claros
feat(api)!: remove deprecated v1 endpoints
```

### DON'T ❌

```bash
# Muy vago
fix: bug fix

# Muy largo en subject (>72 chars)
feat(authentication-system): implement comprehensive OAuth2.0 authentication...

# Tiempo incorrecto
feat: added new feature  # Debería ser "add"

# Sin scope cuando es útil
feat: add login  # ¿Login de qué?
```

## Comandos

### Commit Normal
```bash
# Stage all changes
git add .

# Commit con mensaje generado
git commit -m "type(scope): description"
```

### Commit Amend
```bash
# Solo si el commit NO ha sido pusheado
git commit --amend -m "new message"

# Agregar archivos al último commit
git add forgotten-file.ts
git commit --amend --no-edit
```

### Commit Parcial
```bash
# Stage archivos específicos
git add src/components/Button.tsx

# Stage partes de un archivo
git add -p src/services/api.ts
```

## Análisis Automático

Cuando analices cambios, busca:

1. **Archivos nuevos** → probablemente `feat`
2. **Archivos eliminados** → puede ser `feat`, `refactor`, o `chore`
3. **Tests** → `test`
4. **package.json** → `build` o `chore`
5. **README/docs** → `docs`
6. **Config files** → `chore` o `build`
7. **Bug fixes** → `fix`
8. **Performance** → `perf`

## Output Esperado

```
📝 COMMIT ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Changes Detected:
  📁 Modified: 4 files
  ➕ Added: 2 files
  ➖ Deleted: 0 files

Files Changed:
  M  src/components/LoginForm.tsx
  M  src/services/auth.service.ts
  M  src/types/auth.types.ts
  M  src/hooks/useAuth.ts
  A  src/components/ForgotPassword.tsx
  A  src/pages/reset-password.tsx

Analysis:
  Type: feat
  Scope: auth
  Breaking: No

Suggested Commit Message:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

feat(auth): add password reset functionality

- Add ForgotPassword component with email input
- Create reset-password page for new password entry
- Implement resetPassword method in auth service
- Add PasswordResetToken type definitions
- Update useAuth hook with reset methods

Closes #234

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Commands to Execute:
  git add .
  git commit -m "feat(auth): add password reset functionality..."

Proceed? [Y/n]
```

## Footer Conventions

```bash
# Cerrar issues
Closes #123
Fixes #456
Resolves #789

# Referencias
Refs #123
See #456

# Co-authors
Co-authored-by: Name <email@example.com>

# Breaking changes
BREAKING CHANGE: description
```

## Integración con Claude Code

El commit siempre termina con:
```
🤖 Generated with [Claude Code](https://claude.com/code)

Co-Authored-By: Claude <noreply@anthropic.com>
```
