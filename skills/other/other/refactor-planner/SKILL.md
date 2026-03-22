---
name: refactor-planner
description: "Skill de planification de refactoring. Analyse un codebase ou un domaine specifique pour identifier la dette technique, les violations de patterns evan-workflow, les duplications, et les complexites excessives. Produit un plan de refactoring priorise et progressif (pas de big bang). Ce skill devrait etre utilise quand l'utilisateur veut ameliorer la qualite du code, avant un gros chantier, ou periodiquement pour la maintenance."
---

# refactor-planner

## But

Planifier un refactoring progressif en identifiant la dette technique et en priorisant les actions.

## Modes

### Mode A : `--scan {chemin}`
Analyser et produire un rapport de dette technique.

### Mode B : `--plan {chemin}`
Produire un plan de refactoring priorise (stories).

### Mode C : `--compare`
Comparer le code avec les conventions evan-workflow et lister les ecarts.

## Workflow Mode A (Scan)

### 1. Scanner le code
Identifier les problemes suivants :
- **Duplications de code** : copier-coller entre fichiers, logique dupliquee
- **Complexite cyclomatique elevee** : fichiers/fonctions trop longs, imbrications profondes
- **Violations des patterns evan-workflow** : charger les conventions du stack et verifier la conformite
- **Inconsistances de nommage** : melange de conventions (camelCase/snake_case), noms peu explicites
- **Dead code** : imports non utilises, fonctions jamais appelees, variables inutilisees
- **Couplage fort entre modules** : dependances circulaires, modules trop interconnectes

### 2. Classer chaque probleme
Matrice impact / effort :

| | Effort S | Effort M | Effort L | Effort XL |
|---|---|---|---|---|
| **Impact haut** | Priorite 1 | Priorite 2 | Priorite 3 | Priorite 4 |
| **Impact moyen** | Priorite 2 | Priorite 3 | Priorite 4 | Priorite 5 |
| **Impact bas** | Priorite 3 | Priorite 4 | Priorite 5 | Backlog |

### 3. Generer le rapport
- Resume executif (etat general du code)
- Liste des problemes tries par priorite
- Metriques cles (nombre de fichiers, lignes, complexite moyenne)

## Workflow Mode B (Plan)

### 1. Lire le rapport de scan
Si aucun rapport n'existe, en generer un automatiquement (Mode A).

### 2. Prioriser
- Haut impact + faible effort en premier (quick wins)
- Regrouper les changements lies dans la meme story
- Separer les changements structurels des changements cosmetiques

### 3. Decouper en stories de refactoring
Chaque story doit etre :
- **Atomique** : un seul objectif clair
- **Non-cassante** : le code fonctionne apres chaque story
- **Testable** : les tests existants passent toujours
- **Compatible sprint-planner** : peut etre integree dans un sprint

Format de story :
```
Story: [Titre]
Priorite: [1-5]
Effort: [S/M/L/XL]
Impact: [haut/moyen/bas]
Description: [Ce qui doit etre fait]
Fichiers concernes: [Liste]
Criteres de validation: [Comment verifier]
```

### 4. Estimer l'effort total
- Nombre de stories par priorite
- Effort cumule
- Calendrier suggere (ex: 2 stories S par sprint)

## Principe fondamental

Refactoring progressif, jamais de big bang. Chaque etape laisse le code dans un etat meilleur et fonctionnel. Le refactoring ne doit jamais bloquer les developpements en cours.
