---
name: factory-quick
description: "Quick fix/tweak sans pipeline complet (BMAD Quick Flow)"
allowed-tools: Read, Glob, Grep, Bash, Task, Skill, AskUserQuestion
---

# Factory Quick - Quick Flow (BMAD)

Tu es l'orchestrateur du Quick Flow pour les modifications mineures.

> **Principe BMAD** : Quick Flow pour bug fixes, tweaks UI, refactors internes.
> Si la modification impacte les specs → basculer vers `/factory`.

## Prerequis

- Un projet V1+ existe (code fonctionnel dans `src/`)
- Les specs existent (`docs/specs/`)
- La modification est **mineure** (ne change pas le modele metier)

## Workflow

### 1. Recevoir la demande

L'utilisateur decrit sa modification en langage naturel.

```
Exemple: "Ajouter un bouton de confirmation avant suppression"
Exemple: "Fixer le bug de validation email"
Exemple: "Refactorer le hook useAuth pour plus de clarte"
```

### 2. Analyser la conformite specs

Lire les specs existantes et verifier si la demande est conforme :

```bash
# Charger le delta de la version courante (léger, ~5-10% du volume total)
node tools/extract-version-delta.js -f system -f domain -f api -f brief

# Si le delta est insuffisant pour juger la conformité, charger les specs complètes :
# cat docs/specs/system.md
# cat docs/specs/domain.md
# cat docs/specs/api.md
# cat docs/brief.md
```

**Criteres de NON-conformite (→ basculer vers Evolve) :**

| Signal | Impact |
|--------|--------|
| Nouveau concept/entite metier | `domain.md` obsolete |
| Nouvelle regle business | Rules impactees |
| Changement signature API | `api.md` desynchronise |
| Nouvelle contrainte non-fonctionnelle | `system.md` + ADR |
| Modification acceptance criteria | `acceptance.md` obsolete |
| Plus de 3 fichiers impactes | Scope trop large |

### 3. Decision

#### SI CONFORME (Quick OK)

```
"Modification compatible avec les specs existantes.
Mode Quick Flow active.

Je vais:
1. Creer une TASK directe (TASK-XXXX)
2. Implementer la modification
3. Valider (Gate 4 light)
4. Mettre a jour CHANGELOG

Confirmer pour continuer."
```

→ Aller a l'etape 4 (Implementation Quick)

#### SI NON-CONFORME (Basculement requis)

Presenter le rapport de non-conformite :

```
"Cette modification necessite une mise a jour des specs.

## Impacts detectes

| Element | Spec impactee | Raison |
|---------|---------------|--------|
| Nouvelle entite 'PaymentMethod' | domain.md | Concept metier absent |
| Endpoint POST /payments | api.md | Non documente |
| Regle validation montant | rules/ | Nouvelle contrainte |

## Options

[A] Generer requirements-N.md automatiquement (Recommande)
    → Je cree le fichier pre-rempli base sur votre demande
    → Vous validez/completez les 12 sections
    → Puis /factory s'execute

[B] Creer requirements-N.md manuellement
    → Template: input/requirements.md
    → Completez les sections impactees
    → Puis lancez /factory

[C] Forcer Quick (NON RECOMMANDE)
    → Risque de derive specs/code
    → Dette technique garantie
    → A vos risques"
```

Utiliser `AskUserQuestion` pour obtenir le choix.

### 4. Traitement selon choix

#### Option A : Generation automatique requirements

1. Detecter la prochaine version :
   ```bash
   node tools/detect-requirements.js
   # Retourne: { "version": N, "nextVersion": N+1, ... }
   # Utiliser nextVersion pour le nouveau fichier
   ```

2. Generer `input/requirements-{nextVersion}.md` pre-rempli :
   - Sections impactees completees depuis la demande utilisateur
   - Sections non-impactees marquees "Inchange - voir V1"
   - Section "Contexte evolution" ajoutee

3. **Valider Gate 0** sur le fichier genere :
   ```bash
   node tools/validate-requirements.js input/requirements-{nextVersion}.md
   ```
   - Si echec → corriger les sections manquantes avant de continuer
   - Si succes → continuer

4. Demander validation utilisateur :
   ```
   "J'ai genere input/requirements-{nextVersion}.md (Gate 0 valide)

   Sections pre-remplies:
   - Fonctionnalites: [resume]
   - Contraintes: [resume]

   Veuillez:
   1. Relire et completer si necessaire
   2. Confirmer pour lancer /factory"
   ```

5. Si confirme → Invoquer `/factory`

#### Option B : Creation manuelle

```
"Pour creer requirements-N.md manuellement:

1. Copier le template:
   cp input/requirements.md input/requirements-N.md

2. Completer les sections impactees:
   - ## Fonctionnalites cles
   - ## Contraintes techniques
   - [autres sections selon impacts]

3. Lancer:
   /factory

Le pipeline detectera automatiquement requirements-N.md"
```

#### Option C : Forcer Quick (avec warning)

```
"MODE QUICK FORCE - Vous acceptez les risques suivants:
- Specs desynchronisees du code
- Gate 4 peut echouer sur conformite
- Dette technique a rembourser

Continuation..."
```

→ Aller a Implementation Quick (etape 5)

### 5. Implementation Quick

Si Quick OK ou force :

1. **Creer la TASK** :
   ```bash
   # Obtenir le prochain numero
   node tools/factory-state.js counter task next
   # Creer dans la version courante
   node tools/get-planning-version.js
   ```

2. **Generer TASK-XXXX-quick-fix.md** dans `docs/planning/vN/tasks/` :
   - Template simplifie (pas besoin de US/EPIC pour quick)
   - **US Parent** : `N/A (Quick Fix)` — JAMAIS de reference cross-version
   - **EPIC** : `N/A (Quick Fix)`
   - Objectif clair
   - Fichiers concernes (max 3)
   - DoD minimale
   - Tests attendus

3. **Activer le tracking instrumentation** :
   ```bash
   node tools/set-current-task.js set docs/planning/vN/tasks/TASK-XXXX-quick-fix.md
   ```

4. **Deleguer a l'agent `developer`** :
   ```
   Task(
     subagent_type: "developer",
     prompt: "Implementer TASK-XXXX-quick-fix.md.
     Mode Quick: modification mineure, pas de nouveaux concepts.
     Respecter boundaries architecturales.",
     description: "Developer - Quick Fix"
   )
   ```

5. **Desactiver le tracking instrumentation** :
   ```bash
   node tools/set-current-task.js clear
   ```

6. **Validation Gate 4 light** :
   - Tests passent
   - Boundaries respectees
   - Pas de secrets/PII

7. **Mettre a jour CHANGELOG** :
   - Prepend section "Fixed" ou "Changed"
   - Format: `- [Quick] Description (#TASK-XXXX)`

### 6. Finalisation

```bash
node tools/factory-log.js "QUICK" "completed" "Quick fix TASK-XXXX termine"
```

Rapport final :
```
"Quick Fix termine

TASK: TASK-XXXX-quick-fix.md
Fichiers modifies: [liste]
Tests: OK
CHANGELOG: Mis a jour

Note: Cette modification n'a pas mis a jour les specs.
Si d'autres modifications similaires s'accumulent,
considerez un /factory pour synchroniser."
```

## Template requirements pre-rempli (Option A)

Quand on genere automatiquement :

```markdown
# Requirements - Evolution V{{N}}

> Genere automatiquement par /factory-quick
> A valider et completer avant /factory

## Contexte evolution

**Origine**: Quick fix qui necessite mise a jour specs
**Demande initiale**: {{DEMANDE_UTILISATEUR}}
**Impacts detectes**: {{LISTE_IMPACTS}}

## Objectif

{{DESCRIPTION_OBJECTIF}}

## Fonctionnalites cles

### Nouvelles fonctionnalites
- {{FONCTIONNALITE_EXTRAITE}}

### Fonctionnalites existantes (inchangees)
- Voir requirements.md (V1)

## Contraintes techniques

{{SI_NOUVELLES_CONTRAINTES}}
- Sinon: Inchangees - voir V1

## Stack technique

Inchange - voir V1

## Personas

Inchange - voir V1

## User Stories

### US ajoutees
- En tant que {{PERSONA}}, je veux {{ACTION}} afin de {{BENEFICE}}

## Regles metier

{{NOUVELLES_REGLES_SI_DETECTEES}}
- Sinon: Inchangees - voir V1

## API

{{NOUVEAUX_ENDPOINTS_SI_DETECTES}}
- Sinon: Inchange - voir V1

## Securite

Inchange - voir V1

## Performance

Inchange - voir V1

## Livrables

- Code source mis a jour
- Tests mis a jour
- CHANGELOG mis a jour
- Specs synchronisees
```

