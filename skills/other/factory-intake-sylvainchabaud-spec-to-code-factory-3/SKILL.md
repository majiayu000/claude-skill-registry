---
name: factory-intake
description: "Phase BREAK - Normalise les requirements en brief/scope/acceptance"
allowed-tools: Read, Glob, Grep, Task, Bash, AskUserQuestion
---

# Factory Intake - Phase BREAK

Tu es l'orchestrateur de la phase BREAK.

> **Phase CRITIQUE** : Le cadrage du besoin determine la qualite de tout le projet.
> L'interaction avec l'utilisateur pour clarifier les ambiguites est ESSENTIELLE.

## Workflow

0. **Lire le state** :
   ```bash
   node tools/factory-state.js get
   # Retourne: { "evolutionMode": "greenfield|brownfield", "evolutionVersion": N, "requirementsFile": "input/requirements-N.md", ... }
   ```
   Extraire : `evolutionMode`, `evolutionVersion`, `requirementsFile`.

1. **Verifier Gate 0 (entree)** : Valider le fichier requirements
   ```bash
   node tools/gate-check.js 0 --json
   ```
   - Si `status === "FAIL"` → STOP immediat (prerequis manquants, ne peut pas corriger).
   - Les erreurs de type `requirements` sont `fixable: false` — l'utilisateur DOIT completer les sections.
   - Terminer avec : `GATE_FAIL|0|<resume erreurs>|0`

2. **Informer l'utilisateur** :
   ```
   "Phase BREAK - Cadrage du besoin

   Je vais analyser vos requirements et vous poser des questions de clarification.
   Vos reponses seront stockees dans docs/factory/questions.md

   Vous pouvez repondre :
   - Directement dans le terminal (recommande)
   - Ou en editant docs/factory/questions.md puis relancer /factory-intake"
   ```

3a. **Phase ANALYSE** - Deleguer a l'agent `analyst` (analyse seule) :
   ```bash
   # Instrumenter la delegation (pas de hooks dans le skill inline non plus)
   node tools/instrumentation/collector.js agent '{"agent":"analyst","source":"factory-intake","phase":"analyse"}'
   ```
   ```
   Task(
     subagent_type: "analyst",
     prompt: "MODE DELEGATION - PHASE ANALYSE UNIQUEMENT.
     Fichier requirements: <requirementsFile>. Mode: <evolutionMode>. Version: <evolutionVersion>.
     Analyse le requirements, identifie les ambiguites et questions.
     Lis le template templates/break/questions-template.md AVANT de generer le fichier questions.
     Ecris le fichier questions : docs/factory/questions.md (V1) ou questions-v<evolutionVersion>.md (V2+).
     IMPORTANT: Respecte EXACTEMENT le format du template (colonnes, statuts).
     - NE PAS utiliser AskUserQuestion (le skill s'en charge)
     - NE PAS generer brief.md, scope.md, acceptance.md
     - NE PAS inventer de numeros de version pour les librairies.
       Ecrire uniquement le nom de la lib (ex: 'Tailwind CSS', pas 'Tailwind CSS v3' ou 'Tailwind CSS 4+').
       Les versions seront verifiees automatiquement en phase MODEL via WebSearch.
     - Retourne dans ta reponse la LISTE des questions identifiees avec leur priorite (bloquante/optionnelle) et les hypotheses proposees.",
     description: "Analyst - Phase ANALYSE (delegation)"
   )
   ```

3b. **Poser les questions a l'utilisateur** (fait par le skill, PAS par le subagent) :
   1. Lire le fichier questions genere par l'analyst (`docs/factory/questions.md` ou `docs/factory/questions-vN.md`)
   2. Extraire les questions identifiees (depuis le fichier ou la reponse de l'analyst)
   3. Poser les questions **bloquantes en premier** via `AskUserQuestion` :
      - Regrouper par lot de 1 a 4 questions (limite du tool)
      - Proposer les hypotheses de l'analyst comme options par defaut
      - Ajouter toujours une option pour que l'utilisateur precise sa reponse
   4. Pour les questions optionnelles, poser egalement via `AskUserQuestion`
      mais accepter l'hypothese si l'utilisateur ne precise pas
   5. Mettre a jour le fichier questions avec les reponses recues :
      - Statut → `REPONDU` avec la reponse
      - Ou statut → `HYPOTHESE` si l'utilisateur accepte l'hypothese par defaut

   > **IMPORTANT** : Cette etape est executee par le skill lui-meme (pas un subagent)
   > car les subagents ne posent pas les questions de maniere fiable.

3c. **Phase GENERATION** - Deleguer a l'agent `analyst` (generation des documents) :
   ```bash
   node tools/instrumentation/collector.js agent '{"agent":"analyst","source":"factory-intake","phase":"generation"}'
   ```
   ```
   Task(
     subagent_type: "analyst",
     prompt: "MODE DELEGATION - PHASE GENERATION.
     Fichier requirements: <requirementsFile>. Mode: <evolutionMode>. Version: <evolutionVersion>.
     Lis le fichier questions mis a jour avec les reponses utilisateur :
     docs/factory/questions.md (V1) ou docs/factory/questions-v<evolutionVersion>.md (V2+).
     Les reponses de l'utilisateur sont dans la colonne 'Reponse' du tableau.
     Si mode=greenfield: CREATE docs/brief.md, scope.md, acceptance.md.
     Si mode=brownfield: EDIT les docs existants pour les enrichir.
     Lis les templates AVANT de generer les documents :
     - templates/break/brief-template.md
     - templates/break/scope-template.md
     - templates/break/acceptance-template.md
     IMPORTANT: Respecte EXACTEMENT les headings des templates (##).
     Integre les reponses de l'utilisateur dans les documents generes.
     IMPORTANT:
     - NE PAS utiliser AskUserQuestion (les reponses sont deja dans le fichier questions)
     - Lire le fichier questions AVANT de generer les documents
     - Les hypotheses acceptees doivent etre marquees comme telles dans brief.md
     - NE PAS inventer de numeros de version pour les librairies.
       Ecrire uniquement le nom de la lib (ex: 'Tailwind CSS', pas 'Tailwind CSS v3').
       Les versions seront verifiees automatiquement en phase MODEL via WebSearch.",
     description: "Analyst - Phase GENERATION (delegation)"
   )
   ```

4. **Executer Gate 1 (avec auto-remediation)** :

   ```bash
   node tools/gate-check.js 1 --json
   ```

   Suivre le **protocole standard de gate handling** :

   **Tentative 1** : Analyser le JSON retourne.
   - Si `status === "PASS"` → continuer a l'etape 5.
   - Si `status === "FAIL"` :
     - Lire `errors[]`. Pour chaque erreur `fixable: true` :
       - `missing_file` → relancer l'agent analyst en phase GENERATION avec prompt cible : "Genere le fichier [fichier]. Lis le template [template] et respecte exactement les headings."
         - `brief.md` → template `templates/break/brief-template.md`
         - `scope.md` → template `templates/break/scope-template.md`
         - `acceptance.md` → template `templates/break/acceptance-template.md`
       - `missing_section` → relancer l'agent analyst en phase GENERATION avec prompt cible : "Corrige [fichier]. Section manquante : [section]. Lis le template (ref dans le message d'erreur) et respecte exactement les headings."
       - `structure` → creer les repertoires manquants directement (`mkdir -p`).
     - Pour chaque erreur `fixable: false` → STOP, ne pas retenter.
     - Re-executer : `node tools/gate-check.js 1 --json`

   **Tentative 2** : Relancer l'agent analyst complet (phase GENERATION).
   - Re-executer : `node tools/gate-check.js 1 --json`

   **Tentative 3** : Si toujours FAIL apres 3 tentatives, retourner le rapport d'echec.
   - **NE PAS continuer le pipeline.**
   - Terminer avec ce message EXACT en fin de reponse :
     ```
     GATE_FAIL|1|<resume des erreurs separees par ;>|3
     ```
     Exemple : `GATE_FAIL|1|Fichier manquant: docs/brief.md;Section manquante: ## IN|3`

5. **Logger** via :
   ```bash
   node tools/factory-log.js "BREAK" "completed" "Phase BREAK terminee - X questions posees, Y repondues"
   ```

6. **Retourner** un resume avec :
   - Liste des artefacts crees
   - Nombre de questions posees/repondues
   - Hypotheses generees (si applicable)

## Gestion des questions

| Situation | Action |
|-----------|--------|
| Questions bloquantes non repondues | STOP - Demander reponse |
| Questions optionnelles non repondues | Continuer avec hypothese explicite |
| Utilisateur veut repondre plus tard | Pause - Expliquer comment reprendre |

## Protocole d'echec

- **Gate d'entree** (Gate 0) : Si FAIL → STOP immediat (prerequis manquants, ne peut pas corriger).
- **Gate de sortie** (Gate 1) : Auto-remediation 3x puis marqueur `GATE_FAIL` si echec persistant.
- **Jamais** de STOP silencieux — toujours retourner un rapport structure.
