---
name: rules
description: Strict file creation rules. Loaded FIRST by orchestrator and all agents before any action. Prevents pollution with .md, .json, scripts. Only allows code files and .build/ docs.
allowed-tools: None
---

# Rules Skill - Règles Strictes Fichiers

> **Chargé EN PREMIER par orchestrator + tous agents AVANT toute action**

---

## 🛡️ .build/ PROTECTION (VIOLATION = ARRÊT IMMÉDIAT)

**RÈGLE ABSOLUE - NON NÉGOCIABLE:**

### ❌ INTERDICTION TOTALE d'écrire dans .build/

```
AUCUN fichier .md à créer dans .build/ (sauf orchestrator)
AUCUN log, tmp, test, guide, install
AUCUNE documentation technique
AUCUNE création de fichiers par AGENTS
```

**SEUL ORCHESTRATOR (Claude principal) peut écrire dans .build/**

### ✅ WHITELIST .build/ (EXHAUSTIVE - ORCHESTRATOR uniquement)

**Fichiers `.build/` orchestrator-only:**
- `context.md` - État actuel (routes, composants, models, stack)
- `timeline.md` - Historique append-only des actions
- `tasks.md` - Todo dynamique (in progress, blocked, next)
- `issues.md` - Bugs résolus + solutions documentées
- `specs.md` - Plan stratégique du projet
- `decisions/*.md` - ADRs numérotés (000-xxx.md, 001-xxx.md, etc)
- `templates/*.md` - Templates uniquement (si besoin)

**JAMAIS par agents (EXECUTOR, RESEARCHER, TESTER):**
- ❌ `.build/context.md` (orchestrator only)
- ❌ `.build/timeline.md` (orchestrator only)
- ❌ `.build/issues.md` (orchestrator only)
- ❌ `.build/decisions/*.md` (orchestrator only)
- ❌ Aucun nouveau .md dans .build/

### Où documenter CORRECTEMENT

**SI agent besoin documenter:**
```
✅ Utilise `/home/pilote/projet/primaire/BUILDER/docs/`
✅ Utilise `/tmp/builder-agents/` pour logs temporaires
✅ Utilise bin/README.md pour CLI docs
❌ JAMAIS dans .build/ (sauf orchestrator)
```

### SI violation détectée

**Pseudo-code vérification (EXECUTOR responsable):**
```
IF trying_to_write_in_build_dir:
  STOP IMMÉDIATEMENT

  IF .md file:
    RAISE ERROR "Violation: .build/ protection"
    RETURN info_structurée à orchestrator
    ORCHESTRATOR update .build/context.md après

  IF log/tmp/guide:
    REDIRECT à /tmp/builder-agents/ ou docs/
```

**Actions si violation détectée:**
1. **STOP** immédiatement (pas de création fichier .build/)
2. Return info structurée à ORCHESTRATOR
3. ORCHESTRATOR update .build/context.md après
4. Résultat: Info centralisée, ZÉRO pollution .build/

---

## ❌ INTERDIT de créer

### Fichiers Documentation
- ❌ `.md` files (sauf orchestrator dans `.build/`)
- ❌ AGENTS JAMAIS créer `.build/*.md` (violates .build/ protection)
- ❌ README, GUIDE, ARCHITECTURE, WORKFLOW fichiers hasardeux
- ❌ Documentation dispersée hors `.build/` (sauf orchestrator)
- ✅ Agents: Return info structurée à orchestrator (orchestrator update .build/ après)

### Fichiers Configuration Non-Standards
- `.json` SAUF package.json, tsconfig.json, components.json (standards projet)
- `.yaml/.yml` SAUF docker-compose.yml, .github/workflows/ (CI/CD standards)
- Fichiers config custom hasardeux

### Scripts Hasardeux
- `.sh` scripts inutiles (sauf si explicitement demandé user)
- Setup scripts pollués

---

## ✅ AUTORISÉ uniquement

### Code Source
- `.tsx, .ts, .jsx, .js` (React/TypeScript/JavaScript)
- `.py` (Python)
- `.css, .scss` (Styles - préférer Tailwind dans globals.css)
- `.prisma` (Prisma schema)
- `.sql` (Migrations SQL si besoin)

### Configuration Standards
- `package.json` (Node.js dependencies)
- `tsconfig.json` (TypeScript config)
- `tailwind.config.ts` (Tailwind config)
- `next.config.ts` (Next.js config)
- `components.json` (shadcn config)
- `.env, .env.local, .env.example` (Environment variables)
- `prisma/schema.prisma` (Database schema)

### Documentation Centralisée (.build/ uniquement)
- `.build/context.md` (état projet - routes, models, deployment, stack)
- `.build/timeline.md` (historique actions)
- `.build/tasks.md` (tâches en cours)
- `.build/issues.md` (bugs/solutions)
- `.build/decisions/*.md` (ADRs numérotés: 000-xxx.md, 001-xxx.md)

---

## 🔍 Vérification OBLIGATOIRE

**AVANT Write/Edit fichier:**

```
1. Check si path autorisé selon règles ci-dessus
2. SI path NON autorisé:
   - STOP immédiatement
   - Demander user: "Création [FICHIER] non-standard. Confirmes?"
3. SI user confirme: Procéder
4. SI user refuse: Abandonner
```

**Exemple vérification:**
```
User: "Crée dashboard"
Agent: Va créer app/dashboard/page.tsx
Check: .tsx → ✅ Autorisé (code source)
→ Procéder

User: "Crée feature"
Agent: Va créer FEATURE-GUIDE.md
Check: .md hors .build/ → ❌ Interdit
→ STOP + demander user
```

---

## 📁 Structure Fichiers Autorisée

### Projet Frontend (Next.js)
```
projet/
├── .build/              # Documentation centralisée (SEUL endroit .md)
│   ├── context.md       # Routes, models, deployment, stack
│   ├── timeline.md      # Historique actions
│   ├── tasks.md         # Tasks en cours
│   ├── issues.md        # Bugs + solutions
│   └── decisions/       # ADRs
│       └── 000-xxx.md
├── app/                 # Next.js pages
├── components/          # React components
├── lib/                 # Utilities
├── prisma/              # Database schema
├── public/              # Static assets
├── package.json         # Dependencies
├── tsconfig.json        # TypeScript config
└── tailwind.config.ts   # Tailwind config
```

### Projet Backend (Python)
```
backend/
├── .build/              # Documentation centralisée
├── api/                 # FastAPI routes
├── services/            # Business logic
├── models/              # Database models
├── config.py            # Configuration (1 seul fichier)
├── requirements.txt     # Dependencies
└── .env                 # Environment variables
```

### Projet Full-Stack (Next.js + Prisma)
```
projet/
├── .build/              # Documentation centralisée
├── app/                 # Next.js (frontend + Server Actions)
├── components/          # React components
├── prisma/              # Database schema + migrations
├── lib/                 # Utilities + Prisma client
└── package.json
```

---

## 📁 Dossiers Autorisés par Type

### Code Exécutable
- ✅ `bin/` - Scripts CLI (agent peut créer si demandé)
- ✅ `bin/lib/` - Helper scripts bash

### Documentation (Agent Doit Éviter)
- ✅ `/home/pilote/projet/primaire/BUILDER/docs/` - Docs techniques (si agent besoin documenter)
- ✅ `bin/README.md` - CLI reference uniquement
- ✅ `/tmp/builder-agents/` - Logs jetables temporaires

### INTERDITS Absolus
- ❌ `.build/` (orchectrator only - voir section protection ci-dessus)
- ❌ Racine projet (sauf scripts bin/, config standards)
- ❌ `.md` à la racine (sauf user demande explicitement README)

### Directive Agents Stricte
```
SI agent besoin documenter infos:
  ✅ Return info structurée (JSON/dict)
  ✅ ORCHESTRATOR update .build/ après
  ❌ JAMAIS créer .md agents
  ❌ JAMAIS écrire dans .build/
```

---

## 🚫 Exemples Interdictions

### ❌ Fichiers à NE JAMAIS créer (agents):
```
API_ROUTES.md                # ❌ Return info à orchestrator → orchestrator update .build/context.md
BACKEND_SETUP.md             # ❌ Return info à orchestrator → orchestrator update .build/
DEPLOYMENT.md                # ❌ Return info à orchestrator → orchestrator update .build/context.md
FRONTEND_README.md           # ❌ Return info à orchestrator → orchestrator update .build/
QUICK_START.md               # ❌ Return info à orchestrator → orchestrator update .build/
PROJECT_STATUS.md            # ❌ Orchestrator update .build/context.md uniquement
README.md                    # ❌ Sauf si user demande explicitement (validation user)
ARCHITECTURE.md              # ❌ Orchestrator create .build/decisions/xxx.md uniquement
WORKFLOW.md                  # ❌ Return info → orchestrator update
GUIDE.md                     # ❌ Return info → orchestrator update
SETUP.md                     # ❌ Return info → orchestrator update
setup-project.sh             # ❌ Sauf si user demande (validation user)
install.sh                   # ❌ Sauf si user demande (validation user)
deploy.sh                    # ❌ Sauf si user demande (validation user)
test-matrix.md               # ❌ Pollution - interdite
capabilities-guide.md        # ❌ Pollution - interdite
system-architecture.md       # ❌ Pollution - interdite
custom-config.json           # ❌ Non-standard - interdit
.build/context.md            # ❌ AGENTS JAMAIS - orchestrator only
.build/timeline.md           # ❌ AGENTS JAMAIS - orchestrator only
.build/issues.md             # ❌ AGENTS JAMAIS - orchestrator only
.build/decisions/*.md        # ❌ AGENTS JAMAIS - orchestrator only
```

### ✅ Fichiers autorisés:
```
.build/context.md                    # Documentation projet (routes, models, deployment)
.build/timeline.md                   # Historique actions
.build/decisions/001-use-prisma.md   # ADR
app/dashboard/page.tsx               # Code
components/ui/button.tsx             # Code
lib/utils.ts                         # Code
prisma/schema.prisma                 # Config standard
package.json                         # Config standard
```

---

## 🎯 Responsabilités

### Orchestrator (Claude principal)
- ✅ Créer/modifier `.build/*.md`
- ✅ Créer ADRs `.build/decisions/*.md`
- ❌ Créer autres fichiers .md

### Agents (executor, researcher, tester)
- ✅ Créer code source (.tsx, .ts, .py, etc)
- ✅ Créer configs standards (si nécessaire)
- ❌ Créer fichiers .md (jamais, même dans .build/)
- ❌ Créer documentation

### Skills
- Définissent conventions code
- Pas de création fichiers documentation
- Focus: patterns + anti-duplication

---

## ⚠️ Exceptions (validation user requise)

**SI user demande explicitement:**
- README.md projet
- Documentation technique spécifique
- Scripts deployment custom
- Configuration non-standard

**Workflow:**
```
User: "Crée README projet"
Agent: "Création README.md (hors règles standards). Confirmes?"
User: "oui" → Agent crée
```

---

## 🚨 ENFORCEMENT STRICT

**AVANT toute création fichier .md:**

```python
# Pseudo-code vérification obligatoire
file_to_create = "QUICK_START.md"

allowed_md_patterns = [
  r"^\.build/context\.md$",
  r"^\.build/timeline\.md$",
  r"^\.build/tasks\.md$",
  r"^\.build/issues\.md$",
  r"^\.build/decisions/\d{3}-.*\.md$"   # ADRs numérotés
]

if not matches_any_pattern(file_to_create, allowed_md_patterns):
  # ❌ VIOLATION DÉTECTÉE

  raise Error(f"""
  ❌ VIOLATION RULES SKILL

  Tentative création: {file_to_create}
  → Interdit (seul ORCHESTRATOR peut créer .md)

  ✅ SOLUTION:
  - Return info structurée à ORCHESTRATOR
  - ORCHESTRATOR update .build/context.md avec ces infos

  Format return:
  {{
    "routes": [...],
    "components": [...],
    "models": [...],
    "summary": "courte description"
  }}

  ⚠️ STOP création fichier .md
  """)
```

**Actions si violation:**
1. **STOP** immédiatement (pas de création .md)
2. Return info structurée à ORCHESTRATOR
3. ORCHESTRATOR update .build/context.md
4. Résultat: Info centralisée, zéro pollution

---

## 📌 Résumé Règle d'Or

**1 SEUL endroit documentation: `.build/`**
**Tout le reste: CODE SOURCE uniquement**

Si doute sur fichier → **Demander user AVANT créer**

**Rappel chemins autorisés .md:**
- `.build/context.md` (orchestrator uniquement)
- `.build/timeline.md` (orchestrator uniquement)
- `.build/tasks.md` (orchestrator uniquement)
- `.build/issues.md` (orchestrator uniquement)
- `.build/decisions/*.md` (orchestrator uniquement)

**Agents (executor, tester, research) = JAMAIS .md**

---

**Version:** 1.3.0
**Date:** 2025-11-11
**Application:** Obligatoire pour orchestrator + tous agents + tous skills
**Changelog:**
- v1.3.0: Add .build/ PROTECTION section (VIOLATION = ARRÊT IMMÉDIAT) - agents JAMAIS write .build/
- v1.3.0: Add "Dossiers Autorisés par Type" with strict directory rules
- v1.3.0: Clarify agent must return structured info, orchestrator update .build/ after
- v1.2.0: Suppression `.build/docs/` (context.md suffit)
- v1.2.0: Agents doivent return info structurée (pas créer .md)
- v1.1.0: Enforcement strict avec exemples violations
