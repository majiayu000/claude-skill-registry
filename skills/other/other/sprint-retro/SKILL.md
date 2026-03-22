---
name: sprint-retro
description: Retrospective de sprint avec analyse des metriques, patterns, calibration des tailles et plan d'amelioration
---

# Sprint Retro

## Objectif

Analyser un sprint termine pour en extraire des metriques, identifier les patterns de succes et d'echec, calibrer les estimations et produire un plan d'amelioration.

## Declencheur

`/sprint-retro --sprint <chemin>`

## Workflow en 6 etapes

### Etape 1 : Collecte des donnees

1. Lire `sprint-status.yaml`
2. Collecter pour chaque story :
   - Taille estimee vs duree reelle
   - Difficulte declaree
   - Lecons apprises (lessons_learned)
   - Statut final

### Etape 2 : Metriques

Calculer :
- **Velocity** : Nombre de stories completees
- **Temps total** : Somme des durees reelles
- **Taux de completion** : done / total
- **Taux de blocage** : blocked / total
- **Precision des estimations** : Ecart moyen taille estimee vs duree reelle

### Etape 3 : Analyse des patterns

1. **Patterns de succes** : Qu'est-ce qui a bien fonctionne ?
   - Stories completees rapidement
   - Patterns techniques efficaces
   - Bonnes pratiques observees

2. **Patterns d'echec** : Qu'est-ce qui a pose probleme ?
   - Stories bloquees et raisons
   - Difficultes recurrentes
   - Sous-estimations systematiques

3. **Analyse des retours d'experience** : Agreger les lessons_learned
   - Regrouper par theme (patterns, outils, architecture, processus)
   - Identifier les lecons qui se repetent

### Etape 4 : Performance insights

1. **Par epic** : Quel epic a ete le plus fluide/difficile ?
2. **Par taille** : Quelle taille est la plus fiable en estimation ?
3. **Par type** : Frontend vs backend vs fullstack, lequel pose le plus de problemes ?

### Etape 5 : Calibration des tailles

Comparer les estimations aux durees reelles :

```
Calibration des tailles :
  S (estime < 30min) : reel moyen = {N}min  -> {OK | SOUS-ESTIME | SUR-ESTIME}
  M (estime 30-120min) : reel moyen = {N}min -> {OK | SOUS-ESTIME | SUR-ESTIME}
  L (estime 2-4h) : reel moyen = {N}min      -> {OK | SOUS-ESTIME | SUR-ESTIME}
  XL (estime 4h+) : reel moyen = {N}min      -> {OK | SOUS-ESTIME | SUR-ESTIME}

Recommandation : {ajuster les seuils si necessaire}
```

### Etape 6 : Plan d'action et sauvegarde

1. Generer un plan d'amelioration :

```markdown
## Plan d'amelioration

### Process
- {amelioration 1}

### Estimations
- {ajustement de calibration}

### Patterns techniques
- {pattern a adopter / abandonner}

### Par skill
- feature-planner : {amelioration}
- sprint-planner : {amelioration}
- dev-story : {amelioration}
- feature-doc : {amelioration}
```

2. Sauvegarder le rapport dans :
```
{docs-dir}/features/{nom}/sprint/retro-report.md
```

## Sortie attendue

- Rapport complet affiche dans le terminal
- Fichier `retro-report.md` sauvegarde
- Recommandations actionnables pour le prochain sprint
