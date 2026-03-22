---
name: git-commit-pr
description: Guide la création de commits bien formatés, push vers origin et création de Pull Requests documentées. Utilise ce skill lorsque l'utilisateur demande de commiter des changements, créer une PR, ou finaliser un travail. Suit les Conventional Commits et génère des descriptions de PR complètes.
license: MIT
metadata:
  author: somtech-pack
  version: "1.0.0"
  project: generic
---

# Git Commit & Pull Request

Ce skill guide la création de commits bien formatés, le push vers origin et la création de Pull Requests bien documentées.

## Quand utiliser ce skill

Utilisez ce skill lorsque :
- L'utilisateur demande de créer un commit
- Il faut pousser des changements vers origin
- L'utilisateur demande de créer une Pull Request (PR)
- Il faut finaliser un travail et le préparer pour review
- L'utilisateur demande de "commit et push"
- Il faut documenter des changements pour une PR

## Workflow Complet

### Étape 1 : Vérification pré-commit

Avant de commiter, **toujours** vérifier :

1. **État du dépôt**
```bash
git status
```

2. **Différences à commiter** (staged et unstaged)
```bash
git diff HEAD
```

3. **Commits récents** (pour suivre le style)
```bash
git log --oneline -10
```

### Étape 2 : Staging des fichiers

**Règle d'or** : Préférer ajouter des fichiers spécifiques plutôt que tout ajouter.

#### ✅ Bonnes pratiques

```bash
# Ajouter des fichiers spécifiques
git add src/components/Button.tsx
git add src/types/user.ts

# Ajouter un répertoire spécifique
git add .cursor/skills/new-skill/
```

#### ⚠️ À utiliser avec précaution

```bash
# Ajouter tous les fichiers modifiés (vérifier d'abord avec git status)
git add .

# Peut inclure des fichiers sensibles (.env, credentials, etc.)
git add -A
```

#### ❌ Fichiers à NE JAMAIS commiter

- `.env`, `.env.local` (variables d'environnement)
- `credentials.json`, `secrets.yaml` (credentials)
- `*.key`, `*.pem` (clés privées)
- `node_modules/` (dépendances)
- Fichiers temporaires (.DS_Store, *.log)

**Action** : Si un fichier sensible est staged, le retirer :
```bash
git reset HEAD .env
```

### Étape 3 : Création du commit

#### Format Conventional Commits

Utiliser le format [Conventional Commits](https://www.conventionalcommits.org/) :

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

#### Types de commits

| Type | Description | Exemple |
|------|-------------|---------|
| `feat` | Nouvelle fonctionnalité | `feat(auth): add OAuth2 login` |
| `fix` | Correction de bug | `fix(api): handle null response` |
| `docs` | Documentation seule | `docs(readme): update installation steps` |
| `style` | Formatage (pas de changement de code) | `style(button): fix indentation` |
| `refactor` | Refactoring (ni feat ni fix) | `refactor(utils): simplify date parsing` |
| `perf` | Amélioration de performance | `perf(db): add index on user_id` |
| `test` | Ajout/modification de tests | `test(auth): add login integration tests` |
| `build` | Système de build | `build(deps): upgrade to React 19` |
| `ci` | CI/CD | `ci(github): add test workflow` |
| `chore` | Maintenance | `chore(deps): update dependencies` |
| `revert` | Revert d'un commit | `revert: feat(auth): add OAuth2` |

#### Scopes (optionnels)

Le scope précise la partie du code affectée :
- `(auth)` : Authentification
- `(api)` : API
- `(ui)` : Interface utilisateur
- `(db)` : Base de données
- `(skills)` : Skills (pour ce repo)
- `(docs)` : Documentation

#### Description

- **Impératif** : "add", "fix", "update" (pas "added", "fixed")
- **Minuscule** : Commencer en minuscule (sauf noms propres)
- **Pas de point final**
- **Max 72 caractères**
- **Descriptif** : Dire QUOI, pas COMMENT

✅ **Bon** :
```
feat(skills): add git-commit-pr skill
fix(widget): handle empty data array
docs(versioning): add CHANGELOG guidelines
```

❌ **Mauvais** :
```
Added new feature
Fix bug
Updated files
WIP
```

#### Body (optionnel)

Le body explique le **pourquoi** et le **contexte**.

```
feat(skills): add git-commit-pr skill

This skill guides users through creating well-formatted commits,
pushing to origin, and creating documented Pull Requests.

It follows Conventional Commits and includes PR templates.
```

**Quand ajouter un body** :
- Changement complexe nécessitant explication
- Breaking change
- Contexte important pour comprendre le changement

#### Footer (optionnel)

Pour références et breaking changes :

```
feat(api): change user endpoint format

BREAKING CHANGE: User API now returns { data: User } instead of User directly

Refs: #123
```

**Footers communs** :
- `BREAKING CHANGE:` — Changement incompatible
- `Fixes #123` — Ferme l'issue #123
- `Refs #123` — Référence l'issue #123
- `Closes #123, #124` — Ferme plusieurs issues

#### Session URL (Claude Code)

Pour les commits créés par Claude Code, **toujours** ajouter l'URL de session à la fin :

```
feat(skills): add git-commit-pr skill

Guide la création de commits formatés et PRs documentées.

https://claude.ai/code/session_01PgdZKtpoXwTQw8WZzWKTU8
```

#### Commande de commit

Utiliser un **HEREDOC** pour les messages multi-lignes :

```bash
git commit -m "$(cat <<'EOF'
feat(skills): add git-commit-pr skill

This skill guides users through creating well-formatted commits,
pushing to origin, and creating documented Pull Requests.

https://claude.ai/code/session_01PgdZKtpoXwTQw8WZzWKTU8
EOF
)"
```

### Étape 4 : Push vers origin

#### Vérifier la branche

```bash
git branch --show-current
```

#### Push avec tracking

**Première fois** (nouvelle branche) :
```bash
git push -u origin nom-branche
```

**Fois suivantes** :
```bash
git push
```

#### Retry sur échec réseau

En cas d'échec réseau, **retry jusqu'à 4 fois** avec backoff exponentiel :

```bash
# Tentative 1
git push -u origin branch-name || sleep 2

# Tentative 2
git push -u origin branch-name || sleep 4

# Tentative 3
git push -u origin branch-name || sleep 8

# Tentative 4 (finale)
git push -u origin branch-name
```

### Étape 5 : Création de la Pull Request

#### Pré-requis

1. **Installer gh CLI** (si pas déjà fait)
2. **Authentification GitHub**

#### Authentification gh CLI

Avant de créer une PR, vous devez être authentifié avec GitHub.

##### Vérifier l'authentification

```bash
gh auth status
```

**Sortie attendue si authentifié** :
```
github.com
  ✓ Logged in to github.com as username (/root/.config/gh/hosts.yml)
  ✓ Git operations for github.com configured to use https protocol.
  ✓ Token: *******************
```

**Si non authentifié ou token invalide** :
```
X Failed to log in to github.com
- The token in /root/.config/gh/hosts.yml is invalid.
```

##### S'authentifier avec gh CLI

Si vous n'êtes pas authentifié, lancez :

```bash
gh auth login -h github.com --web
```

**Processus d'authentification** :

1. La commande affiche un **code à 6 caractères** (format : `XXXX-XXXX`)
   ```
   ! First copy your one-time code: 523C-8D88
   Open this URL to continue in your web browser: https://github.com/login/device
   ```

2. **Ouvrez** : https://github.com/login/device

3. **Entrez le code** affiché (ex: `523C-8D88`)

4. **Autorisez GitHub CLI** dans votre navigateur

5. **Attendez la confirmation** dans le terminal :
   ```
   ✓ Authentication complete.
   ✓ Logged in as username
   ```

⏱️ **Important** : Le code expire après quelques minutes. Si vous tardez :
```bash
# Le processus échouera, relancez simplement :
gh auth logout -h github.com  # Optionnel : nettoyer
gh auth login -h github.com --web
```

##### Troubleshooting Authentification

**Problème : "HTTP 401: Bad credentials"**
```bash
# Solution : Ré-authentifier
gh auth logout -h github.com
gh auth login -h github.com --web
```

**Problème : "none of the git remotes configured"**
```bash
# Solution : Spécifier le repo explicitement
gh pr create --repo owner/repo --head branch --base main --title "..." --body "..."
```

**Problème : "HTTP 503: Service Unavailable"**
```bash
# Solution : Attendre quelques secondes et réessayer
sleep 3
gh pr create --repo owner/repo --head branch --base main --title "..." --body "..."
```

#### Analyse des changements

Avant de créer la PR, **analyser TOUS les commits** depuis le point de divergence :

```bash
# Voir tous les commits de la branche
git log main..HEAD --oneline

# Voir tous les diffs depuis main
git diff main...HEAD
```

⚠️ **Important** : Ne pas se baser uniquement sur le dernier commit, mais sur **TOUS** les commits de la branche.

#### Format de la PR

Utiliser le template suivant :

```markdown
## Summary
[1-3 bullet points résumant les changements principaux]

## Changes
### Added
- [Liste des nouvelles fonctionnalités]

### Changed
- [Liste des modifications]

### Fixed
- [Liste des corrections]

### Removed (si applicable)
- [Liste des suppressions]

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Refactoring (no functional changes)

## Testing
- [ ] [Test effectué 1]
- [ ] [Test effectué 2]
- [ ] All tests pass
- [ ] No console errors

## Screenshots (si applicable)
[Ajouter des screenshots pour les changements UI]

## Additional Notes
[Contexte supplémentaire, décisions architecturales, etc.]

[URL de session Claude]
```

#### Commande gh pr create

```bash
gh pr create --title "feat(scope): description courte" --body "$(cat <<'EOF'
## Summary
- Ajout du skill git-commit-pr
- Templates pour PRs et commits
- Documentation complète du workflow

## Changes
### Added
- SKILL.md avec workflow complet Git
- Templates de PR dans references/
- Exemples de commits conventionnels
- Guide de retry sur échec réseau

## Type of Change
- [x] New feature (non-breaking change which adds functionality)
- [x] Documentation update

## Testing
- [x] Skill validé manuellement
- [x] Templates testés
- [x] Documentation revue

https://claude.ai/code/session_01PgdZKtpoXwTQw8WZzWKTU8
EOF
)"
```

#### Options supplémentaires

```bash
# Spécifier le repo explicitement (recommandé si remote non reconnu)
gh pr create --repo owner/repo --head branch-name --base main --title "..." --body "..."

# Créer PR en draft
gh pr create --draft --title "..." --body "..."

# Spécifier la branche de base
gh pr create --base develop --title "..." --body "..."

# Assigner des reviewers
gh pr create --reviewer user1,user2 --title "..." --body "..."

# Ajouter des labels
gh pr create --label bug,urgent --title "..." --body "..."
```

⚠️ **Important** : Si vous utilisez un proxy Git local ou si `gh` ne reconnaît pas votre remote, utilisez toujours l'option `--repo owner/repo --head branch-name --base main` pour spécifier explicitement le repository.

## Workflow Complet (Exemple)

Voici un workflow complet de bout en bout :

```bash
# 1. Vérifier l'état
git status
git diff HEAD
git log --oneline -10

# 2. Ajouter les fichiers spécifiques
git add .cursor/skills/git-commit-pr/

# 3. Commiter avec message formaté
git commit -m "$(cat <<'EOF'
feat(skills): add git-commit-pr skill

Guide complet pour créer des commits bien formatés,
pousser vers origin et créer des PRs documentées.

Inclut :
- Workflow Git complet
- Templates de PR
- Exemples Conventional Commits
- Gestion des retries réseau

https://claude.ai/code/session_01PgdZKtpoXwTQw8WZzWKTU8
EOF
)"

# 4. Pousser vers origin (avec retry si échec)
git push -u origin claude/git-commit-pr-skill || sleep 2 && \
git push -u origin claude/git-commit-pr-skill || sleep 4 && \
git push -u origin claude/git-commit-pr-skill || sleep 8 && \
git push -u origin claude/git-commit-pr-skill

# 5. Analyser les changements pour la PR
git log main..HEAD --oneline
git diff main...HEAD --stat

# 6. Créer la Pull Request
gh pr create --title "feat(skills): add git-commit-pr skill" --body "$(cat <<'EOF'
## Summary
- Nouveau skill pour gérer commits, push et création de PRs
- Suit Conventional Commits et bonnes pratiques Git
- Inclut templates et exemples réutilisables

## Changes
### Added
- SKILL.md avec workflow Git complet
- Templates de PR et exemples de commits
- Documentation retry réseau
- Guide Conventional Commits

## Type of Change
- [x] New feature (non-breaking change which adds functionality)
- [x] Documentation update

## Testing
- [x] Skill testé manuellement
- [x] Templates validés
- [x] Documentation complète

https://claude.ai/code/session_01PgdZKtpoXwTQw8WZzWKTU8
EOF
)"
```

## Bonnes Pratiques

### ✅ À FAIRE

1. **Commits atomiques** : Un commit = un changement logique
2. **Messages descriptifs** : Expliquer le QUOI et le POURQUOI
3. **Vérifier avant commit** : `git status`, `git diff`
4. **Ajouter fichiers spécifiques** : Éviter `git add .` sans vérification
5. **Suivre Conventional Commits** : Type, scope, description
6. **PRs documentées** : Summary, Changes, Testing
7. **Analyser TOUS les commits** : Pas seulement le dernier
8. **Session URL** : Toujours inclure l'URL Claude

### ❌ À ÉVITER

1. **Commits vagues** : "fix", "update", "WIP"
2. **Commits massifs** : 50 fichiers changés sans organisation
3. **Secrets commités** : .env, credentials
4. **Push force sur main** : `git push --force` sur branche principale
5. **PRs sans description** : Pas de contexte
6. **Oublier de tester** : Commit sans vérification
7. **Ignorer les hooks** : `--no-verify` sans raison

## Gestion des Hooks Git

### Pre-commit hooks

Si un hook pre-commit échoue :

1. **Corriger le problème** (linting, tests, etc.)
2. **Re-stage** les fichiers corrigés
3. **Créer un NOUVEAU commit** (pas `--amend` sauf si demandé)

❌ **Ne JAMAIS** :
```bash
git commit --no-verify  # Sauf demande explicite
git commit --amend      # Après échec de hook (risque de perte)
```

### Pre-push hooks

Si un hook pre-push échoue :

1. **Corriger localement**
2. **Créer un nouveau commit** avec la correction
3. **Re-push**

## Scénarios Spéciaux

### Multiple commits avant PR

Si la branche a plusieurs commits :

```bash
# Analyser TOUS les commits
git log main..HEAD --oneline

# La PR doit résumer TOUS les changements
git diff main...HEAD --stat
```

### Breaking changes

```bash
git commit -m "$(cat <<'EOF'
feat(api)!: change user endpoint response format

BREAKING CHANGE: The /api/users endpoint now returns
{ data: User[], meta: { total: number } } instead of User[].

Migration guide: Update all API calls to access response.data

https://claude.ai/code/session_01PgdZKtpoXwTQw8WZzWKTU8
EOF
)"
```

Note : Le `!` après le scope indique un breaking change.

### Revert de commit

```bash
git revert <commit-hash>

# Message auto-généré :
# revert: feat(auth): add OAuth2 login
#
# This reverts commit abc123.
```

## Références

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Keep a Changelog](https://keepachangelog.com/)
- [GitHub CLI Documentation](https://cli.github.com/manual/)
- [Git Best Practices](https://git-scm.com/book/en/v2)

## Templates

Voir les fichiers de référence :
- `references/PR_TEMPLATE.md` — Template complet de PR
- `references/COMMIT_EXAMPLES.md` — Exemples de commits
- `references/GIT_WORKFLOW.md` — Workflow Git détaillé

---

**Note** : Ce skill est générique et applicable à tout projet Git. Adaptez les scopes et conventions selon votre projet.
