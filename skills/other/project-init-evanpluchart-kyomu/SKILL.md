---
name: project-init
description: "Skill conversationnel interactif pour initialiser un nouveau projet ou onboarder un projet existant avec les standards evan-workflow. Guide l'utilisateur a travers des questions sur le stack, les technos, les conventions, puis genere tous les fichiers de configuration Claude Code (CLAUDE.md, settings.json, .claudeignore, .gitignore, structure). Propose intelligemment les technos documentees dans evan-workflow en priorite, avec des alternatives. Si une techno non documentee est choisie, propose de la documenter automatiquement. Ce skill devrait etre utilise quand l'utilisateur veut creer un nouveau projet, initialiser Claude Code sur un projet existant, ou configurer les standards evan-workflow."
---

# project-init

## But

Guider interactivement la creation d'un nouveau projet ou l'onboarding d'un projet existant avec les standards evan-workflow. Produire tous les fichiers de configuration Claude Code prets a l'emploi.

## Posture

Agir comme un **architecte technique bienveillant**. Poser des questions claires avec des choix numerotes. Ne jamais submerger l'utilisateur — maximum 3-4 questions par message. Proposer des defauts intelligents et expliquer brievement pourquoi.

Langue : **francais** pour toutes les interactions.

## REGLE CRITIQUE

**EXECUTER TOUTES LES ETAPES SANS EXCEPTION.** Ne jamais sauter une etape, meme si elle semble optionnelle. Chaque etape est obligatoire. En particulier :
- L'installation des skills via `~/evan-workflow/install.sh` est OBLIGATOIRE
- L'installation des hooks est OBLIGATOIRE (proposer le choix, mais toujours poser la question)
- Le resume final est OBLIGATOIRE
- Verifier a la fin que TOUS les fichiers ont ete generes et que les skills sont installes

---

## Modes

### Mode A — Nouveau projet (`/project-init`)

Creation d'un nouveau projet de zero avec questionnaire interactif.

### Mode B — Projet existant (`/project-init --existing {chemin}`)

Onboarding d'un projet existant : detection auto du stack, generation des fichiers de config Claude Code.

---

## Mode A — Nouveau projet

### Etape 1 : Identite du projet

Poser les questions suivantes :

```
Quel est le nom du projet ?
Decrivez-le en une phrase :
Quel type de projet ?
  1. Web app (SPA ou SSR)
  2. Site vitrine / landing page
  3. API backend seul
  4. App mobile (iOS/Android)
  5. App desktop
  6. CLI / outil en ligne de commande
  7. Outil IA / agent
  8. Autre (preciser)
```

### Etape 2 : Stack technique

Poser les questions par categorie. Pour chaque categorie :
1. Lister d'abord les technos documentees dans evan-workflow avec le tag `[doc]`
2. Puis proposer des alternatives pertinentes avec une courte explication
3. Adapter les propositions au type de projet choisi

**Consulter `references/tech-catalog.md`** pour la liste complete des technos a proposer par categorie.

Regles de proposition :
- Si le type est "App mobile" → proposer Expo/React Native, pas Next.js
- Si le type est "CLI" → proposer Node.js, Go, Rust, pas de framework frontend
- Si le type est "Site vitrine" → proposer Astro, Next.js static, pas de backend lourd
- Si le type est "API backend seul" → ne pas proposer de frontend framework

Poser les questions dans cet ordre (adapter selon le type de projet) :

**Frontend** (si applicable) :
```
Framework frontend ?
  1. Next.js 16        [doc] — SSR/SSG, App Router, React 19
  2. React SPA (Vite)         — SPA pur, leger, rapide
  3. Astro                    — Sites statiques, multi-framework
  4. Nuxt.js                  — Alternative Vue.js
  5. Pas de frontend
```

**Styling** (si frontend choisi) :
```
Systeme de styling ?
  1. Chakra UI v3      [doc] — Composants accessibles, theming puissant
  2. Chakra UI v2      [doc] — Version stable, large ecosystem
  3. Tailwind CSS      [placeholder] — Utility-first, tres flexible
  4. shadcn/ui         [placeholder] — Composants copiables + Tailwind
  5. Material UI              — Design system Google
  6. Mantine                  — Composants modernes, hooks utiles
```

**Backend** (si applicable) :
```
Framework backend ?
  1. Symfony + API Platform  [doc] — PHP, robuste, enterprise-ready
  2. Node.js (Express)       [placeholder] — Simple, ecosystem massif
  3. Node.js (Fastify)       [placeholder] — Rapide, schema-first
  4. Node.js (Hono)          [placeholder] — Ultra-leger, edge-ready
  5. tRPC (dans Next.js)     [placeholder] — API typesafe end-to-end, pas de backend separe
  6. Nest.js                        — Architecture Angular-like pour Node.js
  7. Django / FastAPI               — Python, bon pour ML/IA
  8. Pas de backend
```

**Base de donnees** (si backend choisi) :
```
Base de donnees ?
  1. PostgreSQL        [placeholder] — Robuste, features avancees (JSONB, full-text)
  2. SQLite                   — Zero config, embedded, bon pour dev/prototypage
  3. MySQL / MariaDB          — Populaire, performant en lecture
  4. MongoDB                  — NoSQL, flexible, documents JSON
  5. Supabase (PostgreSQL)    — BaaS avec auth et realtime inclus
  6. Turso (libSQL)           — SQLite distribue, edge-ready, tier gratuit
```

**ORM** (si base de donnees choisie) :
```
ORM ?
  1. Doctrine          [doc] — PHP, mature, migrations auto (si Symfony)
  2. Prisma            [placeholder] — TypeScript, schema declaratif, migrations
  3. Drizzle           [placeholder] — TypeScript, leger, SQL-like
  4. TypeORM                  — TypeScript, decorators, inspire de Doctrine
  5. Pas d'ORM (raw SQL)
```

**State management** (si frontend choisi) :
```
State management / data fetching ?
  1. RTK Query         [doc] — Cache API integre Redux, normalisation
  2. TanStack Query    [doc tanstack-table] — Cache API leger, flexible, populaire
  3. Zustand           [placeholder] — State simple sans boilerplate
  4. Jotai                    — Atoms pour state granulaire
  5. SWR                      — Data fetching par Vercel, minimaliste
  6. Aucun (fetch natif + state React)
```

**Tests** :
```
Framework de tests ?
  1. Vitest                   — Rapide, compatible Vite, ESM natif
  2. Jest              [doc patterns testing] — Populaire, mature
  3. PHPUnit           [doc patterns testing] — Standard PHP (si Symfony)
  4. Playwright        [MCP disponible] — Tests E2E navigateur
  5. Cypress                  — Tests E2E, bonne DX
```

**Gestion de tickets** :
```
Outil de gestion de tickets ?
  1. Jira — Quel prefix ? (ex: MAPP)
  2. Linear — Quel prefix ? (ex: DM)
  3. GitHub Issues
  4. GitLab Issues
  5. Pas de gestion de tickets
```

**Structure repo** :
```
Structure du repository ?
  1. Monorepo (frontend + backend dans le meme repo)
  2. Multi-repo (repos separes)
  3. Sous-projet (dans un repo existant)
  4. Repo unique (un seul projet)
```

### Etape 3 : Gestion des technos non documentees

Apres avoir collecte les choix, verifier pour chaque techno choisie si elle est documentee dans `~/evan-workflow/technos/`.

Pour chaque techno NON documentee :
1. Informer l'utilisateur : "La techno {nom} n'est pas encore documentee dans evan-workflow."
2. Proposer les options :
   ```
   Que faire pour {nom} ?
     1. Creer un placeholder minimal maintenant (recommande)
     2. Documenter en profondeur via /evan-workflow-builder --add-stack {nom}
     3. Ignorer pour l'instant
   ```
3. Si option 1 : creer le fichier `~/evan-workflow/technos/{nom}/index.md` avec un placeholder structure
4. Si option 2 : lancer la commande en arriere-plan via un sous-agent

### Etape 4 : Generation des fichiers

Generer tous les fichiers dans le dossier du projet.

**Fichiers a generer :**

1. **CLAUDE.md** — Base sur `~/evan-workflow/templates/CLAUDE.template.md`
   - Remplir les infos projet (nom, description, stack)
   - Decommenter les sections pertinentes selon le stack choisi
   - Ajouter les references vers les docs evan-workflow pour chaque techno
   - Remplir les conventions de branches/commits avec le prefix choisi
   - Recommander les skills pertinents
   - Consulter `references/claude-md-generation.md` pour les regles de generation

2. **.claude/settings.json** — Copier depuis `~/evan-workflow/templates/settings.json`

3. **.claudeignore** — Generer selon le stack. Consulter `references/claudeignore-templates.md`

4. **.gitignore** — Generer selon le stack

5. **Structure de dossiers** — Creer l'arborescence de base selon le type et le stack

### Etape 5 : Installation des skills et hooks

**CETTE ETAPE EST OBLIGATOIRE. NE JAMAIS LA SAUTER.**

Presenter les skills recommandes en fonction du stack choisi :

```
Skills recommandes pour votre projet :
  [x] feature-planner — Planification de features
  [x] sprint-planner — Decoupe en sprint
  [x] dev-story — Implementation de stories
  [x] quick-dev — Fix rapide
  [x] code-review — Review de code
  [x] fix-review-code — Correction auto des problemes
  [ ] dev-jira-ticket — Implementation de tickets Jira (si Jira choisi)
  [ ] api-test-gen — Generation de tests API (si backend avec API)
  [ ] migration-planner — Planification de migrations de stack
  [ ] dependency-audit — Audit des dependances
  [ ] tech-debt-tracker — Suivi de la dette technique
  [ ] test-coverage-analyzer — Analyse couverture de tests

Installer ces skills ? (y/N)
```

Si l'utilisateur accepte, executer le script d'installation evan-workflow :

```bash
~/evan-workflow/install.sh {chemin-projet} -y --no-hooks
```

Puis proposer le hook adapte au stack :
- Frontend Next.js → `nextjs`
- Backend Symfony → `symfony`
- Fullstack (front + back) → `fullstack`
- Autre → `biome` ou `eslint-prettier` selon le linter detecte

Si l'utilisateur accepte un hook, l'installer :

```bash
~/evan-workflow/install.sh {chemin-projet} -y --hooks {nom-du-hook}
```

Ou si les skills sont deja installes, installer uniquement le hook :

```bash
cp ~/evan-workflow/hooks/{nom}.sh ~/.claude/hooks/
chmod +x ~/.claude/hooks/{nom}.sh
```

### Etape 6 : Resume

Afficher un resume de tout ce qui a ete genere :

```
=== Projet {nom} initialise ===

Stack : {description du stack}
Fichiers generes :
  [+] CLAUDE.md
  [+] .claude/settings.json
  [+] .claudeignore
  [+] .gitignore
  [+] {structure de dossiers}

Skills installes : {liste}
Hook installe : {nom}

Prochaines etapes :
  1. Lire et ajuster le CLAUDE.md genere
  2. Lancer /feature-planner pour planifier la premiere feature
  3. Ou /quick-dev pour commencer a coder directement
```

---

## Mode B — Projet existant

### Etape 1 : Detection automatique

Scanner le projet pour identifier :
- `package.json` → Node.js, React, Next.js, libs installees
- `composer.json` → PHP, Symfony, API Platform
- `tsconfig.json` → TypeScript
- `biome.json` / `.eslintrc*` → Linter
- `tailwind.config.*` → Tailwind CSS
- `next.config.*` → Next.js
- `.env*` → Variables d'environnement
- `docker-compose.yml` → Docker
- `Makefile` → Commandes projet
- Structure de dossiers → monorepo, architecture

### Etape 2 : Presentation du scan

Afficher ce qui a ete detecte :

```
=== Scan de {chemin} ===

Stack detecte :
  Frontend : Next.js 16, React 19, TypeScript
  Styling : Tailwind CSS
  Backend : Pas detecte (ou integre)
  ORM : Prisma
  State : TanStack Query
  Tests : Vitest

Structure : Monorepo
Tickets : Pas detecte

Est-ce correct ? Voulez-vous ajuster quelque chose ?
```

### Etape 3 : Verification documentation evan-workflow

Pour chaque techno detectee, verifier si elle est documentee dans `~/evan-workflow/technos/`.
Signaler les technos non documentees et proposer de les documenter (meme logique que Mode A, Etape 3).

### Etape 4 : Generation des fichiers

Meme logique que Mode A Etape 4, mais adapter au projet existant :
- Si CLAUDE.md existe : proposer de le completer plutot que de le remplacer
- Si .gitignore existe : ne pas le remplacer
- Si .claude/settings.json existe : proposer un merge
- Si .claudeignore n'existe pas : le generer selon le stack detecte

### Etape 5 : Installation des skills et hooks

**CETTE ETAPE EST OBLIGATOIRE. NE JAMAIS LA SAUTER.**

Meme logique que Mode A Etape 5. Utiliser le script d'installation :

```bash
~/evan-workflow/install.sh {chemin-projet} -y --no-hooks
```

Puis proposer le hook adapte au stack detecte.

### Etape 6 : Resume

Afficher un resume complet de tout ce qui a ete fait :

```
=== Projet {nom} configure ===

Stack detecte : {description}
Fichiers generes/modifies :
  [+] CLAUDE.md (genere / complete)
  [+] .claude/settings.json (copie / merge)
  [+] .claudeignore (genere)

Skills installes : {nombre} dans {chemin}/.claude/skills/
Hook installe : {nom}

Technos non documentees dans evan-workflow :
  [!] {liste, si applicable}

Prochaines etapes :
  1. Relire et ajuster le CLAUDE.md genere
  2. Lancer /feature-planner pour planifier une feature
  3. Ou /quick-dev pour commencer a coder directement
```

---

## References

Consulter les fichiers de reference pour les details :
- `references/tech-catalog.md` — Catalogue complet des technos a proposer par categorie
- `references/claude-md-generation.md` — Regles de generation du CLAUDE.md
- `references/claudeignore-templates.md` — Templates .claudeignore par stack
