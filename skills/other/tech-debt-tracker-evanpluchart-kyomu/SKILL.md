---
name: tech-debt-tracker
description: "Skill d'identification et de priorisation de la dette technique dans un projet. Scanne les patterns de dette (TODO/FIXME, code duplique, fichiers trop longs, dependances outdated, types manquants, etc.), classifie par categorie et severite, et genere un rapport avec matrice de priorisation. Compatible avec /refactor-planner pour la remediation. Ce skill devrait etre utilise periodiquement ou avant un audit qualite."
---

# tech-debt-tracker

## But

Identifier et prioriser la dette technique dans un projet.

## Modes

### Mode A : `--scan`
Analyse globale du projet (scan complet).

### Mode B : `--focus {domaine}`
Analyse d'un domaine specifique (ex: securite, performance, un dossier).

### Mode C : `--report`
Generer un rapport markdown structure.

## Workflow Mode A (Scan complet)

### 1. Scanner les patterns de dette

Rechercher les indicateurs suivants dans tout le projet :

#### Commentaires signalant de la dette
- `TODO`, `FIXME`, `HACK`, `WORKAROUND`, `XXX`, `TEMPORARY`
- Anciennete du commentaire (via git blame si possible)

#### Code duplique
- Blocs de code identiques ou tres similaires entre fichiers
- Logique copiee-collee avec de legeres variations

#### Fichiers trop longs ou complexes
- Fichiers depassant 300 lignes (composants, services)
- Fonctions depassant 50 lignes
- Complexite cyclomatique elevee (imbrications profondes)

#### Dependances problematiques
- Packages outdated (majeurs en retard)
- Packages deprecies ou abandonnes
- Packages avec vulnerabilites connues

#### Typage manquant ou faible
- `any` en TypeScript (explicites et implicites)
- `@SuppressWarnings` en PHP
- `mixed` excessif en PHP
- Absence de types de retour

#### Couverture de tests faible
- Fichiers de logique metier sans test correspondant
- Endpoints API sans test d'integration
- Validators et voters sans test unitaire

#### Autres indicateurs
- Fichiers de configuration dupliques ou incoherents
- Variables d'environnement non documentees
- Imports non utilises
- Code mort (fonctions jamais appelees)

### 2. Classifier par categorie

Chaque item de dette est classe dans une des categories suivantes :

| Categorie | Description | Exemples |
|---|---|---|
| **Securite** | Risque de vulnerabilite | Dependances avec CVE, auth non testee, secrets en dur |
| **Performance** | Impact sur les performances | Packages lourds, requetes N+1, absence de cache |
| **Maintenabilite** | Difficulte a faire evoluer le code | Code duplique, fichiers trop longs, nommage incoherent |
| **Obsolescence** | Technologies ou patterns depasses | Dependances majeures en retard, API deprecees |

### 3. Scorer chaque item

Chaque item recoit deux scores :

- **Impact** (1-5) : consequence si la dette n'est pas traitee
  - 5 = critique (securite, perte de donnees)
  - 4 = haut (bugs en prod, performance degradee)
  - 3 = moyen (experience developpeur, maintenabilite)
  - 2 = bas (cosmetique, conventions)
  - 1 = negligeable

- **Effort** (1-5) : cout de remediation
  - 1 = trivial (< 1h)
  - 2 = faible (< 1 jour)
  - 3 = moyen (1-3 jours)
  - 4 = important (1 semaine)
  - 5 = majeur (> 1 semaine)

**Priorite = Impact x Effort inverse** : les items a haut impact et faible effort sont traites en premier.

| | Effort 1 | Effort 2 | Effort 3 | Effort 4 | Effort 5 |
|---|---|---|---|---|---|
| **Impact 5** | P1 | P1 | P2 | P3 | P4 |
| **Impact 4** | P1 | P2 | P3 | P4 | P5 |
| **Impact 3** | P2 | P3 | P4 | P5 | P5 |
| **Impact 2** | P3 | P4 | P5 | P5 | Backlog |
| **Impact 1** | P4 | P5 | Backlog | Backlog | Backlog |

## Workflow Mode B (Focused)

### 1. Identifier le domaine cible
- Un dossier specifique, une categorie (securite, performance...), ou un type de dette

### 2. Appliquer les memes regles de scan
Mais uniquement sur le perimetre defini.

### 3. Approfondir l'analyse
- Plus de detail sur chaque item
- Suggestions de correction concretes

## Workflow Mode C (Report)

### 1. Collecter les donnees
Si aucun scan n'existe, en generer un automatiquement (Mode A).

### 2. Generer le rapport markdown

Structure du rapport :
```
# Rapport de dette technique - {projet}
## Date : {date}

## Resume executif
- Score global de sante : {X}/100
- Nombre total d'items : {N}
- Repartition par categorie et priorite

## Items critiques (P1-P2)
[Detail de chaque item avec recommandation]

## Matrice de priorisation
[Tableau impact x effort]

## Tendance
[Evolution depuis le dernier scan si disponible]

## Plan de remediation suggere
[Compatible avec /refactor-planner]
```

### 3. Proposer un plan de remediation
- Quick wins (P1) : a traiter immediatement
- Court terme (P2-P3) : a planifier dans les prochains sprints
- Moyen terme (P4-P5) : a integrer dans la roadmap
- Backlog : a traiter quand l'opportunite se presente

## Compatibilite

Ce skill est concu pour fonctionner en complement de :
- `/refactor-planner` : pour la planification detaillee de la remediation
- `/dependency-audit` : pour l'analyse approfondie des dependances
- `/test-coverage-analyzer` : pour l'analyse de la couverture de tests

## Principe fondamental

La dette technique n'est pas inheremment mauvaise — c'est un choix conscient. L'objectif n'est pas de tout corriger mais de rendre la dette visible, mesuree et priorisee. Traiter en priorite ce qui a le plus d'impact avec le moins d'effort.
