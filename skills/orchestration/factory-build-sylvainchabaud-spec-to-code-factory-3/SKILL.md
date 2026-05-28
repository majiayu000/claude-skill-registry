---
name: factory-build
description: "Phase ACT (build) - Implémente tasks par batch (layer)"
context: fork
allowed-tools: Read, Glob, Grep, Task, Bash
---

# Factory Build - Phase ACT (Build)

Tu es l'orchestrateur de la phase build.

## Workflow

1. **Verifier Gate 3 (entree)** :
   ```bash
   node tools/gate-check.js 3 --json
   ```
   - Si `status === "FAIL"` → STOP immediat (prerequis manquants, ne peut pas corriger).
   - Terminer avec : `GATE_FAIL|3|<resume erreurs>|0`

2. **Obtenir le repertoire planning actif** :
   ```bash
   node tools/get-planning-version.js
   # Retourne: { "tasksDir": "docs/planning/v1/tasks", ... }
   ```

3. **Lister et grouper les tasks par layer (batching)** :

   Glob `<tasksDir>/TASK-*.md`, trier par numero.

   **Algorithme de grouping** : Regrouper les tasks consecutives par layer, en se basant sur le nom du fichier :

   | Pattern dans le nom de fichier | Layer / Batch |
   |-------------------------------|---------------|
   | `*-project-config*` | **setup** |
   | `*-value-objects*`, `*-entity-*`, `*-entities-*`, `*-service*`, `*-events*` | **domain** |
   | `*-ports-*`, `*-dtos-*`, `*-usecase*`, `*-use-case*` | **application** |
   | `*-localstorage*`, `*-csv*`, `*-adapter*`, `*-repository*` | **infrastructure** |
   | `*-hook*` | **ui-hooks** |
   | `*-component*`, `*-page*`, `*-view*` | **ui-components** |
   | `*-app-assembly*` | **assembly** |
   | (aucun match) | **other** |

   **Limite de taille** : Si un batch contient **plus de 5 tasks**, le subdiviser en sous-batches de 5 max.
   Exemple : 7 tasks UI-components → batch "ui-components-1" (5 tasks) + batch "ui-components-2" (2 tasks).

   **Modele** : Tous les batches utilisent le **modele par defaut** (herite du parent, pas de parametre `model`).

4. **Pour chaque batch** (dans l'ordre : **setup → domain → application → infrastructure → ui-hooks → ui-components → assembly → other**) :

   > **SEQUENTIEL OBLIGATOIRE** : Executer UN SEUL batch a la fois. Attendre sa completion avant le suivant.
   > **SETUP EN PREMIER** : Le batch `setup` (project-config) DOIT toujours etre execute en premier.
   > Il installe les dependances et cree les fichiers de configuration necessaires aux autres batches.
   > **ASSEMBLY EN DERNIER** : Le batch `assembly` (app-assembly) DOIT toujours etre execute en dernier.
   > Il assemble tous les composants/hooks dans App.tsx.

   a. **Instrumenter la delegation** (les hooks ne fonctionnent pas dans les forks) :
      Remplacer `LAYER_NAME` par le nom reel du batch (ex: "setup", "domain", "ui-components-1", "assembly").
      ```bash
      node tools/instrumentation/collector.js agent '{"agent":"developer","source":"factory-build","batch":"LAYER_NAME"}'
      ```
      Exemple concret :
      ```bash
      node tools/instrumentation/collector.js agent '{"agent":"developer","source":"factory-build","batch":"setup"}'
      ```

   b. **Definir la task courante** (premiere task du batch, pour instrumentation) :
      ```bash
      node tools/set-current-task.js set <tasksDir>/TASK-XXXX-first.md
      ```

   c. **Deleguer le batch entier a 1 agent `developer`** via Task tool :

      **Pour le batch `setup`** (project-config) :
      ```
      Task(
        subagent_type: "developer",
        prompt: "Implemente la task de setup projet.
        Task : <path vers TASK-XXXX-project-config.md>

        1. Lis la task complete
        2. Lis docs/specs/stack-reference.md — c'est la SOURCE DE VERITE pour les versions et configs
        3. Installe EXACTEMENT les packages listes (versions exactes)
        4. Cree les fichiers de configuration EXACTEMENT comme les snippets de reference
        5. Verifie que le build passe (pnpm build)
        6. Verifie que les tests passent (pnpm test)

        TRACKING OBLIGATOIRE :
        - Appelle `node tools/set-current-task.js set <path>` AVANT de commencer
        - Appelle `node tools/set-current-task.js clear` APRES avoir termine

        REGLE ABSOLUE : NE PAS inventer de versions ou de configs.
        Utiliser UNIQUEMENT ce qui est ecrit dans stack-reference.md.",
        description: "Developer batch - setup (1 task)"
      )
      ```

      **Pour tous les autres batches** :
      ```
      Task(
        subagent_type: "developer",
        prompt: "Implemente les N tasks suivantes SEQUENTIELLEMENT, dans l'ordre.
        Tasks : <liste des paths TASK-*.md du batch>

        Pour CHAQUE task :
        1. Appelle `node tools/set-current-task.js set <path>` AVANT de commencer
        2. Lis la task complete
        3. Implemente le code + tests conformement a la DoD
        4. Appelle `node tools/set-current-task.js clear` APRES avoir termine

        TRACKING OBLIGATOIRE :
        - JAMAIS sauter set-current-task.js, meme sous pression de contexte
        - Chaque task DOIT avoir son appel set + clear

        REGLES QUALITE STRICTES :
        - Composants/fichiers : MAX 150 lignes. Si un fichier depasse, extraire des sous-composants.
        - Fonctions : MAX 30 lignes.
        - Tests : MINIMUM 3 tests par fichier source (happy path, edge case, erreur).
          Pour les composants UI : tester le rendu, l'interaction utilisateur, et au moins 1 cas limite.
        - TypeScript strict : zero `any`, zero `as` sauf cast justifie.
        - Imports : respecter les boundaries architecturales (domain n'importe jamais infra/UI).

        TESTING PLAN :
        Si docs/testing/plan.md n'existe pas encore, le creer en lisant le template
        templates/testing/plan.md. Respecter EXACTEMENT les headings du template.",
        description: "Developer batch - LAYER_NAME (N tasks)"
      )
      ```

      **IMPORTANT** : Remplacer `LAYER_NAME` par le nom reel du batch dans `description` aussi.

   d. **Effacer la task courante** :
      ```bash
      node tools/set-current-task.js clear
      ```

   e. **Logger le batch** :
      ```bash
      node tools/factory-log.js "ACT_BUILD" "batch-done" "Batch LAYER_NAME termine - N tasks implementees"
      ```

5. **Executer Gate 4 (avec auto-remediation, MAX 2 retries)** :

   ```bash
   node tools/gate-check.js 4 --json
   ```

   **Tentative 1** : Analyser le JSON retourne.
   - Si `status === "PASS"` → continuer a l'etape 6.
   - Si `status === "FAIL"` :
     - Lire `errors[]`. Pour chaque erreur `fixable: true` :
       - `test_failure` → relancer le developer sur les tests en echec.
       - `quality` → relancer le developer pour corriger la qualite.
       - `assembly` → relancer le developer sur la task app-assembly (template `templates/planning/task-assembly-template.md`).
       - `boundary` → relancer le developer pour corriger les imports inter-couches.
       - `project_health` → installer les dependances manquantes (`pnpm add ...`), corriger le build.
       - `testing_plan` → completer docs/testing/plan.md en lisant le template `templates/testing/plan.md`.
     - Pour chaque erreur `fixable: false` → STOP, ne pas retenter.
     - Re-executer : `node tools/gate-check.js 4 --json`

   **Tentative 2** : Relancer le developer sur les erreurs restantes (meme routage par categorie que Tentative 1).
   - Re-executer : `node tools/gate-check.js 4 --json`

   **Tentative 3 (dernier)** : Si toujours FAIL, retourner le rapport d'echec.
   - **NE PAS relancer. NE PAS faire de Tentative 4.**
   - Terminer avec : `GATE_FAIL|4|<resume erreurs separees par ;>|3`

   > **STRICTEMENT 3 checks max (1 initial + 2 retries). Ne JAMAIS depasser.**

6. **Logger** via :
   ```bash
   node tools/factory-log.js "ACT_BUILD" "completed" "Phase BUILD terminee - N tasks implementees en B batches"
   ```

7. **Retourner** un resume des batches executes avec nombre de tasks par batch et statuts

## Protocole d'echec

- **Gate d'entree** (Gate 3) : Si FAIL → STOP immediat + marqueur `GATE_FAIL|3|...|0`.
- **Gate de sortie** (Gate 4) : Auto-remediation **2x max** puis marqueur `GATE_FAIL|4|...|3` si echec persistant.
- **Erreur non-fixable** (`fixable: false`) → STOP immediat + `GATE_FAIL`.
- **Jamais** de STOP silencieux — toujours retourner un rapport structure.
