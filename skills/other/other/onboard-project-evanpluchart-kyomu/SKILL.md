---
name: onboard-project
description: "Skill d'onboarding sur un projet existant. Scanne un codebase, identifie le stack, l'architecture, les domaines metier, les patterns, et genere un briefing complet. Produit un CLAUDE.md adapte, un PROJECT_CONTEXT.md, et des recommendations. Ce skill devrait etre utilise quand un dev rejoint un nouveau projet, quand l'IA doit comprendre un projet inconnu, ou pour bootstrapper les fichiers de contexte evan-workflow sur un projet existant."
---

# onboard-project

## But

Analyser un projet inconnu et generer un briefing complet pour qu'un dev (ou l'IA) puisse travailler dessus rapidement.

## Modes

### Mode A : `--full {chemin}`
Analyse complete + generation de tous les fichiers.

### Mode B : `--quick {chemin}`
Analyse rapide, resume en 1 page.

### Mode C : `--claude-md {chemin}`
Generer uniquement le CLAUDE.md.

## Workflow Mode A (Full)

### 1. Detection stack
Identifier les technologies via les fichiers de configuration :
- `package.json` (Node.js, Next.js, React)
- `composer.json` (PHP, Symfony)
- `Cargo.toml` (Rust)
- `go.mod` (Go)
- `requirements.txt` / `pyproject.toml` (Python)

### 2. Scan structure
Analyser l'arborescence et l'organisation des dossiers :
- Identifier le type d'architecture (monorepo, monolithe, microservices)
- Reperer les dossiers cles (src, app, lib, tests, config)

### 3. Scan code
Explorer les elements structurants :
- Entites / modeles
- Routes / endpoints
- Pages / composants
- Services / providers

### 4. Analyse patterns
Identifier les conventions en place :
- Nommage (camelCase, snake_case, PascalCase)
- Structure des fichiers (barrel exports, co-location)
- Imports (absolus, relatifs, aliases)
- Gestion d'erreurs

### 5. Detection domaines
Regrouper les entites/pages par domaine metier :
- Identifier les bounded contexts
- Cartographier les relations entre domaines

### 6. Lecture CLAUDE.md existant
Si un CLAUDE.md est deja present, integrer les regles existantes.

### 7. Generation
Produire les fichiers suivants :
- **CLAUDE.md** adapte au projet (base sur `~/evan-workflow/templates/CLAUDE.template.md`)
- **PROJECT_CONTEXT.md** (base sur `~/evan-workflow/templates/PROJECT_CONTEXT.template.md`)
- **Briefing de synthese** : resume en 1 page du projet

### 8. Recommendations
- Skills evan-workflow recommandes pour le projet
- Patterns manquants a mettre en place
- Points d'attention (dette technique, risques)

## Combinaison avec evan-workflow-extractor

`onboard-project` genere le contexte projet, `evan-workflow-extractor` extrait les conventions techniques. Les deux sont complementaires :
- **onboard-project** : "Qu'est-ce que ce projet ?" (stack, domaines, architecture)
- **evan-workflow-extractor** : "Comment code-t-on dans ce projet ?" (conventions, patterns, regles)
