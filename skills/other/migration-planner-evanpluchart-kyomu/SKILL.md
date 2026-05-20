---
name: migration-planner
description: "Skill de planification et execution de migrations de stack. Analyse un projet pour identifier les breaking changes, genere un plan de migration progressif par lots avec rollback possible, et execute la migration etape par etape. Supporte les montees de version majeures (Chakra v2 -> v3, Next 15 -> 16, Symfony 6 -> 7, etc.). Ce skill devrait etre utilise avant toute montee de version majeure d'une dependance structurante."
---

# migration-planner

## But

Planifier une migration de stack (ex: Chakra v2 -> v3, Next 15 -> 16, Symfony 6 -> 7).

## Modes

### Mode A : `--analyze {source} {target}`
Scanner le projet et identifier tous les breaking changes, fichiers impactes, effort estime.

### Mode B : `--plan {source} {target}`
Generer un plan de migration progressif (par lots, avec rollback possible).

### Mode C : `--execute {source} {target}`
Implementer la migration lot par lot avec verification a chaque etape.

## Workflow Mode A (Analyze)

### 1. Identifier la migration
- Determiner la stack concernee (source -> target)
- Identifier la version actuelle dans les fichiers de configuration (`package.json`, `composer.json`, etc.)
- Confirmer la version cible

### 2. Lire la documentation officielle de migration
- Consulter le guide de migration officiel (via Context7 MCP si disponible)
- Lister tous les breaking changes documentes
- Identifier les deprecations qui deviennent des erreurs dans la version cible

### 3. Scanner tous les fichiers impactes dans le projet
- Rechercher les imports, API, composants et patterns affectes par les breaking changes
- Lister chaque fichier impacte avec le(s) changement(s) concerne(s)
- Compter le nombre d'occurrences par type de changement

### 4. Classifier les changements
Chaque changement identifie est classe dans une des categories suivantes :

| Categorie | Description | Exemple |
|---|---|---|
| **Automatique** | Remplacement par regex/codemod | Renommage d'import, changement de prop |
| **Semi-automatique** | Pattern matching + adaptation manuelle | Changement de signature d'API |
| **Manuel** | Necessite une comprehension du contexte | Changement d'architecture, logique metier |

### 5. Estimer l'effort
- Nombre total de fichiers impactes
- Repartition par categorie (auto / semi-auto / manuel)
- Effort estime en jours-homme (S/M/L/XL)

## Workflow Mode B (Plan)

### 1. Lire l'analyse
Si aucune analyse n'existe, en generer une automatiquement (Mode A).

### 2. Organiser les changements par lots
Decouper la migration en lots ordonnes par dependance :
- **Lot 0** : Preparation (mise a jour des outils, configuration, CI)
- **Lot 1-N** : Changements fonctionnels, du plus fondamental au plus peripherique
- **Lot final** : Nettoyage (suppression des shims, compat layers, deprecations)

### 3. Definir chaque lot
Pour chaque lot :
```
Lot: [Numero] - [Titre]
Dependances: [Lots prerequis]
Fichiers: [Liste des fichiers concernes]
Type: [automatique / semi-automatique / manuel]
Effort: [S/M/L/XL]
Rollback: [Strategie de retour arriere]
Verification: [Tests, build, types a verifier]
```

### 4. Definir la strategie de rollback globale
- Point de sauvegarde (branche, tag) avant chaque lot
- Criteres de go/no-go entre chaque lot
- Plan de retour arriere si un lot echoue

## Workflow Mode C (Execute)

### 1. Lire le plan
Si aucun plan n'existe, en generer un automatiquement (Mode B).

### 2. Pour chaque lot, executer le cycle suivant

#### a. Implementer
- Appliquer les changements du lot (regex pour les automatiques, modifications guidees pour les autres)
- Respecter les patterns evan-workflow du stack cible

#### b. Verifier
- Verification des types (TypeScript, PHPStan)
- Execution des tests existants
- Verification du build
- Verification visuelle si applicable (composants UI)

#### c. Commit atomique
- Un commit par lot avec un message explicite : `migration({stack}): lot {N} - {description}`
- Permet un revert propre si necessaire

### 3. Validation finale
- Tous les tests passent
- Le build est fonctionnel
- Aucune deprecation warning residuelle
- Les performances ne sont pas degradees

## Principe fondamental

Migration progressive, jamais de big bang. Chaque lot laisse le projet dans un etat fonctionnel. Si un lot echoue, on peut revenir au lot precedent sans perte. Toujours commiter entre chaque lot pour garder un historique propre.
