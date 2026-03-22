---
name: test-coverage-analyzer
description: "Skill d'analyse de la couverture de tests et de suggestion de tests a ecrire en priorite. Detecte le framework de test, analyse la couverture actuelle, identifie les zones critiques non couvertes, et peut generer les tests manquants en utilisant les patterns evan-workflow. Ce skill devrait etre utilise pour ameliorer la qualite des tests ou avant une release importante."
---

# test-coverage-analyzer

## But

Analyser la couverture de tests et suggerer quoi tester en priorite.

## Modes

### Mode A : `--analyze`
Analyser la couverture actuelle du projet.

### Mode B : `--suggest`
Suggerer les tests les plus importants a ecrire.

### Mode C : `--generate {fichier}`
Generer les tests sugeres pour un fichier ou un ensemble de fichiers.

## Workflow Mode A (Analyze)

### 1. Detecter le framework de test

Identifier les outils de test presents dans le projet :

| Indicateur | Framework |
|---|---|
| `jest.config.*` ou `jest` dans package.json | Jest |
| `vitest.config.*` ou `vitest` dans package.json | Vitest |
| `phpunit.xml*` ou `phpunit` dans composer.json | PHPUnit |
| `cypress.config.*` | Cypress |
| `playwright.config.*` | Playwright |

### 2. Analyser la couverture

#### Si un outil de couverture est disponible
- Lancer la commande de couverture (`pnpm test --coverage`, `phpunit --coverage-text`, etc.)
- Parser les resultats : couverture par fichier, par ligne, par branche

#### Si aucun outil de couverture n'est disponible
- Lister tous les fichiers de test existants
- Mapper les fichiers de test aux fichiers source (par convention de nommage)
- Identifier les fichiers source sans fichier de test correspondant

### 3. Cartographier la couverture

Produire une carte de couverture :
```
Couverture globale : {X}%

Par domaine :
- Logique metier (services, use cases) : {X}%
- Endpoints API (controllers, resolvers) : {X}%
- Validators / Guards / Voters : {X}%
- Composants UI : {X}%
- Utilitaires / Helpers : {X}%
```

### 4. Identifier les zones non couvertes critiques

Prioriser les zones non couvertes selon leur criticite :

| Zone | Criticite | Justification |
|---|---|---|
| **Authentification / Autorisation** | Critique | Risque securitaire |
| **Logique metier principale** | Critique | Coeur de l'application |
| **Endpoints API publics** | Haute | Surface d'attaque et contrat API |
| **Validators et contraintes** | Haute | Integrite des donnees |
| **Transformations de donnees** | Moyenne | Risque de regression |
| **Composants UI complexes** | Moyenne | Experience utilisateur |
| **Utilitaires et helpers** | Basse | Generalement simples |

## Workflow Mode B (Suggest)

### 1. Lire l'analyse
Si aucune analyse n'existe, en generer une automatiquement (Mode A).

### 2. Scorer chaque fichier non couvert par risque

Le score de risque combine plusieurs facteurs :

- **Complexite du code** : fichiers longs, fonctions complexes, nombreuses branches
- **Criticite du domaine** : auth > logique metier > API > UI > utils
- **Frequence de modification** : fichiers souvent modifies (via git log) = plus de risque de regression
- **Dependances** : fichiers dont beaucoup d'autres dependent = impact large en cas de bug

**Regle** : code complexe sans test > code simple sans test.

### 3. Generer la liste de suggestions ordonnee

Pour chaque fichier suggere :
```
Fichier: {chemin}
Score de risque: {X}/10
Raison: {pourquoi ce fichier est prioritaire}
Tests a ecrire:
  - {description du test 1}
  - {description du test 2}
Effort estime: {S/M/L}
```

### 4. Proposer un plan de test progressif
- **Sprint 1** : tests critiques (auth, logique metier principale)
- **Sprint 2** : tests hauts (API, validators)
- **Sprint 3+** : tests moyens et bas

## Workflow Mode C (Generate)

### 1. Lire les suggestions
Si aucune suggestion n'existe, en generer automatiquement (Mode B).

### 2. Charger les patterns de testing evan-workflow
- Lire `technos/{stack}/patterns/testing.md` pour le stack concerne
- Appliquer les conventions de nommage, structure et organisation des tests

### 3. Generer les tests pour le fichier cible

#### Pour chaque fichier :
- Analyser le code source (fonctions, classes, methodes publiques)
- Identifier les cas de test : happy path, edge cases, erreurs attendues
- Generer le fichier de test en respectant les patterns evan-workflow

#### Regles de generation :
- **Nommage** : suivre la convention du projet (`*.test.ts`, `*.spec.ts`, `*Test.php`)
- **Structure** : describe/it ou test classes selon le framework
- **Assertions** : couvrir les retours, les effets de bord, les erreurs
- **Mocks** : mocker les dependances externes (API, DB, services tiers)
- **Donnees de test** : utiliser des factories ou fixtures realistes

### 4. Verifier les tests generes
- S'assurer que les tests compilent (types corrects)
- Lancer les tests generes
- Corriger si necessaire

## Compatibilite

Ce skill est concu pour fonctionner en complement de :
- `/tech-debt-tracker` : la couverture de tests est un indicateur de dette
- `/refactor-planner` : ecrire des tests avant de refactorer pour securiser les changements

## Principe fondamental

Tous les fichiers n'ont pas besoin du meme niveau de couverture. L'objectif est de tester en priorite ce qui a le plus de risque et d'impact. Un test bien cible sur une zone critique vaut mieux que 100% de couverture sur des utilitaires triviaux.
