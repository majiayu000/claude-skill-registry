---
name: factory-plan
description: "Phase ACT (planning) - Génère epics/US/tasks"
context: fork
allowed-tools: Read, Glob, Grep, Task, Bash
---

# Factory Plan - Phase ACT (Planning)

Tu es l'orchestrateur de la phase planning.

## Workflow

0. **Obtenir la version** :
   ```bash
   # Obtenir la version courante
   node tools/get-planning-version.js
   # Retourne: { "dir": "docs/planning/vN", "version": N, ... }

   # Creer le repertoire si necessaire (evolution)
   mkdir -p docs/planning/v<N>/us
   mkdir -p docs/planning/v<N>/tasks
   ```

1. **Verifier Gate 2 (entree)** :
   ```bash
   node tools/gate-check.js 2 --json
   ```
   - Si `status === "FAIL"` → STOP immediat (prerequis manquants, ne peut pas corriger).
   - Terminer avec : `GATE_FAIL|2|<resume erreurs>|0`

2. **Deleguer a l'agent `scrum-master`** via Task tool :
   ```bash
   # Pre-filtrage : lister uniquement les ADR actifs (exclut SUPERSEDED)
   node tools/list-active-adrs.js --summary
   # Retourne les paths des ADR actifs, a passer dans le prompt ci-dessous

   # Extraire le delta de la version courante (brownfield uniquement)
   node tools/extract-version-delta.js -f system -f domain -f api
   # Retourne les ajouts/modifications de la version courante — passer dans le prompt

   # Instrumenter la delegation (les hooks ne fonctionnent pas dans les forks)
   node tools/instrumentation/collector.js agent '{"agent":"scrum-master","source":"factory-plan"}'
   ```
   ```
   Task(
     subagent_type: "scrum-master",
     prompt: "Decompose les specs en epics/US/tasks.
     ADR ACTIFS : <liste des paths retournes par list-active-adrs.js --summary>
     DELTA VERSION COURANTE : <output de extract-version-delta.js ci-dessus>
     IMPORTANT : NE PAS charger les ADR au statut SUPERSEDED.

     Lis les templates de planning AVANT de generer les documents :
     - templates/planning/epics-template.md (pour docs/planning/vN/epics.md)
     - templates/planning/US-template.md (pour chaque US-*.md)
     - templates/planning/task-template.md (pour chaque TASK-*.md)
     - templates/planning/task-assembly-template.md (pour la task app-assembly)
     IMPORTANT: Respecte EXACTEMENT les headings et le format des templates.

     IMPORTANT - Tasks auto-suffisantes (principe BMAD):
     Chaque TASK doit etre 100% independante avec:
     - Template: templates/planning/task-template.md
     - Contexte complet: references specs avec resumes
     - Code existant pertinent: extraits avec lignes
     - Aucune dependance a la task precedente

     Le developpeur doit pouvoir implementer la task
     SANS connaitre les autres tasks.

     IMPORTANT - TASK DE SETUP PROJET (OBLIGATOIRE) :
     La PREMIERE task generee DOIT etre une task de setup projet :
     - Nom : TASK-XXXX-project-config.md (ou XXXX est le premier numero disponible)
     - Contenu : Initialiser le projet (installer les deps, creer les configs).
     - Lire docs/specs/stack-reference.md pour les versions et configs exactes.
     - DoD :
       1. Installer EXACTEMENT les packages listes dans stack-reference.md (versions exactes)
       2. Creer les fichiers de configuration EXACTEMENT comme les snippets de reference
       3. Verifier que le build passe (pnpm build sans erreur)
       4. Verifier que les tests passent (pnpm test sans erreur)
     - Cette task reference docs/specs/stack-reference.md comme source de verite.
     - NE PAS inventer de versions — utiliser UNIQUEMENT celles de stack-reference.md.",
     description: "Scrum Master - Planning BMAD"
   )
   ```

3. **Executer Gate 3 (avec auto-remediation)** :

   ```bash
   node tools/gate-check.js 3 --json
   ```

   Suivre le **protocole standard de gate handling** :

   **Tentative 1** : Analyser le JSON retourne.
   - Si `status === "PASS"` → continuer a l'etape 4.
   - Si `status === "FAIL"` :
     - Lire `errors[]`. Pour chaque erreur `fixable: true` :
       - `missing_file` → relancer le scrum-master avec prompt cible : "Genere le fichier [fichier]. Lis le template correspondant."
         - `epics.md` → template `templates/planning/epics-template.md`
         - `US-*.md` → template `templates/planning/US-template.md`
         - `TASK-*.md` → template `templates/planning/task-template.md`
       - `missing_pattern` → relancer le scrum-master avec prompt cible sur le pattern manquant.
       - `task_incomplete` → relancer le scrum-master pour completer les DoD/Tests. Prompt : "Lis le template templates/planning/task-template.md et complete les sections manquantes."
       - `task_references` → corriger les references US directement dans les fichiers task.
     - Pour chaque erreur `fixable: false` → STOP, ne pas retenter.
     - Re-executer : `node tools/gate-check.js 3 --json`

   **Tentative 2** : Relancer le scrum-master complet.
   - Re-executer : `node tools/gate-check.js 3 --json`

   **Tentative 3** : Si toujours FAIL, retourner le rapport d'echec.
   - **NE PAS continuer le pipeline.**
   - Terminer avec : `GATE_FAIL|3|<resume erreurs separees par ;>|3`

4. **Logger** via :
   ```bash
   node tools/factory-log.js "ACT_PLAN" "completed" "Phase planning terminee"
   ```

5. **Retourner** un resume avec liste des tasks creees (numerotees)

## Protocole d'echec

- **Gate d'entree** (Gate 2) : Si FAIL → STOP immediat + marqueur `GATE_FAIL|2|...|0`.
- **Gate de sortie** (Gate 3) : Auto-remediation 3x puis marqueur `GATE_FAIL|3|...|3` si echec persistant.
- **Jamais** de STOP silencieux — toujours retourner un rapport structure.
