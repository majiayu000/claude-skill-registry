---
name: dependency-audit
description: "Skill d'audit des dependances d'un projet. Verifie les packages outdated, les vulnerabilites connues, les licences incompatibles, et le poids des dependances. Supporte npm/pnpm (package.json) et Composer (composer.json). Ce skill devrait etre utilise periodiquement pour la maintenance ou avant une release."
---

# dependency-audit

## But

Verifier les dependances d'un projet (outdated, vulnerabilites, licences, poids).

## Modes

### Mode A : `--full`
Audit complet (outdated + vulnerabilites + licences + poids).

### Mode B : `--security`
Vulnerabilites uniquement.

### Mode C : `--outdated`
Packages desactualises uniquement.

### Mode D : `--unused`
Detecter les dependances installees mais non utilisees.

## Workflow

### 1. Detection des package managers
Identifier les gestionnaires de dependances presents :
- `pnpm-lock.yaml` -> pnpm
- `package-lock.json` -> npm
- `yarn.lock` -> yarn
- `composer.lock` -> composer

### 2. Execution des audits
Pour chaque package manager detecte :
- Lancer les commandes d'audit (`pnpm audit`, `composer audit`, `npm audit`)
- Lancer les commandes outdated (`pnpm outdated`, `composer outdated`, `npm outdated`)
- Parser les resultats
- Classer par severite (critical, high, moderate, low)

### 3. Generation du rapport

#### Vulnerabilites critiques/hautes (action immediate)
- CVE, package affecte, version installee, version corrigee
- Impact potentiel et recommandation

#### Packages majeurs en retard (planifier la mise a jour)
- Version actuelle vs derniere version
- Changelog des breaking changes
- Effort estime de migration

#### Licences a verifier
- Lister toutes les licences utilisees
- Alerter sur les licences GPL dans un projet commercial
- Signaler les packages sans licence explicite

#### Packages lourds (alternatives plus legeres)
- Taille du package dans le bundle
- Alternatives recommandees (ex: moment.js -> dayjs)
- Impact sur le temps de build / taille du bundle

### 4. Plan de mise a jour priorise
1. Corriger les vulnerabilites critiques/hautes
2. Mettre a jour les packages avec des patch/minor disponibles
3. Planifier les montees de version majeures
4. Remplacer les packages deprecies ou abandonnes
