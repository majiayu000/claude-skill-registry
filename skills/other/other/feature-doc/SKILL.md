---
name: feature-doc
description: Generation et maintenance de documentation technique a partir du code, avec modes full, update et audit
---

# Feature Doc

## Objectif

Generer et maintenir une documentation technique synchronisee avec le code, en analysant l'implementation reelle pour produire des docs fiables.

## Modes d'execution

| Mode | Declencheur | Description |
|------|------------|-------------|
| Full | `--full <domaine>` | Creation complete de la doc pour un domaine |
| Update | `--update <domaine>` | Mise a jour incrementale apres des changements |
| Audit | `--audit <domaine>` | Verification de coherence code/doc |
| Story | (appel interne) | Appele depuis dev-story pour maj post-implementation |

## Structure generee

```
{docs-dir}/features/{domaine}/
  overview.md           # Vue d'ensemble du domaine
  architecture.md       # Architecture technique
  api.md                # Endpoints / interfaces (si applicable)
  data-model.md         # Modele de donnees (si applicable)
  workflows.md          # Flux metier
  components.md         # Composants UI (si applicable)
```

Les fichiers generes dependent du stack et du domaine. Tous ne sont pas toujours necessaires.

## Workflow : Mode full

### Etape 1 : Identifier le domaine

1. Determiner le perimetre du domaine (entites, composants, endpoints)
2. **Adaptive context loading** : Charger uniquement les docs evan-workflow pertinentes :
   - Lire `~/evan-workflow/common/manifest.yaml` et charger les fichiers des scopes `always` + scopes pertinents au projet (frontend, backend)
   - `~/evan-workflow/technos/{stack}/patterns/` pour les patterns du stack concerne
3. Identifier le stack concerne (backend, frontend, les deux)

### Etape 2 : Scanner le code

1. Utiliser une hierarchie de recherche pour trouver le code pertinent :
   - **Code direct** : Fichiers dans les dossiers du domaine (entites, controllers, composants...)
   - **Recherche par pattern** : Grep sur les noms de domaine, classes, fonctions
   - **Recherche large** : Glob sur les extensions et dossiers pertinents
2. Lire les fichiers identifies pour comprendre l'implementation

### Etape 3 : Analyser les workflows

1. Tracer les flux de donnees a travers le code
2. Identifier les points d'entree (routes, events, commandes)
3. Identifier les points de sortie (responses, notifications, side effects)
4. Documenter les cas nominaux et les cas d'erreur

### Etape 4 : Generer les fichiers

1. Utiliser la matrice de correspondance code vers doc :

| Type de code | Documentation generee |
|-------------|----------------------|
| Entites / Modeles | data-model.md |
| Controllers / Routes | api.md |
| Services / Processors | architecture.md, workflows.md |
| Composants UI | components.md |
| Configuration | architecture.md |

2. Pour chaque fichier doc, inclure :
   - Description fonctionnelle
   - Extraits de code pertinents (signatures, interfaces)
   - Relations et dependances
   - Exemples d'utilisation

### Etape 5 : Validation

1. Verifier que chaque fichier de code important est reference dans la doc
2. Verifier que les exemples de code sont corrects
3. Verifier la coherence entre les fichiers doc

## Workflow : Mode update

1. Identifier les fichiers modifies recemment (via git diff ou liste fournie)
2. Determiner quels fichiers doc sont impactes
3. Relire le code modifie
4. Mettre a jour uniquement les sections concernees
5. Ajouter une note de mise a jour avec la date

## Workflow : Mode audit

1. Lister tous les fichiers doc du domaine
2. Pour chaque fichier doc :
   - Verifier que les fichiers de code references existent encore
   - Verifier que les signatures/interfaces documentees correspondent au code actuel
   - Verifier que les workflows documentes sont encore valides
3. Generer un rapport d'audit :

```
Audit : {domaine}
Date : {date}

OK :
  - data-model.md : 12/12 entites a jour
  - api.md : 8/8 endpoints a jour

DESYNCHRONISE :
  - workflows.md : Le flux X a change (fichier Y modifie le {date})
  - components.md : Composant Z supprime

MANQUANT :
  - Nouveau service ServiceX non documente
```

## Appel depuis dev-story

Quand dev-story appelle feature-doc en mode story :
1. Recevoir la liste des fichiers modifies
2. Determiner le domaine concerne
3. Executer le mode update sur ce domaine
4. Retourner un resume des mises a jour effectuees

## Regles de documentation

- La doc doit refleter le code, pas l'inverse
- Privilegier les exemples concrets aux descriptions abstraites
- Les extraits de code doivent etre des copier-coller du code reel, pas des simplifications
- Chaque fichier doc doit etre lisible independamment
- Adapter le format de documentation au stack du projet (les patterns de doc varient selon le stack)

## Sortie attendue

- Liste des fichiers doc generes/mis a jour
- Statistiques de couverture (fichiers de code documentes / total)
- Alertes de desynchronisation (mode audit)
