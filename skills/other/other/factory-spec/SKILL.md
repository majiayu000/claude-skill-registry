---
name: factory-spec
description: "Phase MODEL - Génère specs + ADR + rules"
context: fork
allowed-tools: Read, Glob, Grep, Task, Bash, WebSearch, WebFetch
---

# Factory Spec - Phase MODEL

Tu es l'orchestrateur de la phase MODEL.

## Workflow

1. **Verifier Gate 1 (entree)** :
   ```bash
   node tools/gate-check.js 1 --json
   ```
   - Si `status === "FAIL"` → STOP immediat (prerequis manquants, ne peut pas corriger).
   - Terminer avec : `GATE_FAIL|1|<resume erreurs>|0`

2. **Lire le state** :
   ```bash
   node tools/factory-state.js get
   # Retourne: { "evolutionMode": "greenfield|brownfield", "evolutionVersion": N, "requirementsFile": "...", ... }

   # Lister les ADR actifs (brownfield : exclut SUPERSEDED)
   node tools/list-active-adrs.js --summary

   # Extraire le delta de la version courante (brownfield uniquement)
   node tools/extract-version-delta.js -f brief -f scope
   ```
   Extraire : `evolutionMode`, `evolutionVersion`.

3. **Deleguer aux agents** (sequentiel strict, UN A LA FOIS) :

   **3a. Agent PM** (specs fonctionnelles) :
   ```bash
   # Instrumenter la delegation (les hooks ne fonctionnent pas dans les forks)
   node tools/instrumentation/collector.js agent '{"agent":"pm","source":"factory-spec"}'
   ```
   ```
   Task(
     subagent_type: "pm",
     prompt: "Genere les specs fonctionnelles du projet.
     Mode: <evolutionMode>. Version: <evolutionVersion>.
     Si mode=greenfield: CREATE docs/specs/system.md et docs/specs/domain.md.
     Si mode=brownfield: EDIT les specs existantes pour les mettre a jour.
     DELTA VERSION COURANTE: <output de extract-version-delta.js>
     Lis les fichiers BREAK: docs/brief.md, docs/scope.md, docs/acceptance.md.
     Lis les templates: templates/specs/system.md, templates/specs/domain.md.
     IMPORTANT: Respecte EXACTEMENT les headings des templates (##).
     IMPORTANT: NE PAS inventer de numeros de version pour les librairies.
     Ecrire uniquement le nom de la lib (ex: 'Tailwind CSS', pas 'Tailwind CSS 3+').",
     description: "MODEL - PM specs"
   )
   ```

   **3b. Verification web des dependances et generation de stack-reference.md** (fait par le fork, AVANT l'architect) :

   > **OBLIGATOIRE** : Verifier les dependances de la stack sur internet AVANT de deleguer a l'architect.
   > Les LLMs ont souvent des connaissances obsoletes sur les versions recentes des libs.
   > L'architect n'a pas acces a WebSearch/WebFetch — c'est le fork qui fournit les infos verifiees.

   **Etape 1 : Identifier la stack dans le brief/scope**

   Lire `docs/brief.md` et `docs/scope.md` pour extraire la liste des dependances prevues (framework, CSS lib, bundler, test runner, linter, chart lib, etc.).
   Constituer une liste : `[ "react", "tailwindcss", "vite", "vitest", ... ]`.

   **Etape 2 : Verifier les versions via npm registry** (source canonique)

   Pour **chaque dependance** identifiee :
   ```bash
   npm view <package> version
   # Retourne la derniere version stable (ex: "19.1.0")
   ```
   Si le nom npm n'est pas evident (ex: Tailwind CSS → `tailwindcss`), utiliser :
   ```bash
   npm search <lib> --json | head -5
   ```

   > **C'est la source la plus fiable** pour les numeros de version.
   > Ne JAMAIS utiliser une version extraite d'une page web si elle contredit npm registry.

   Compteur : noter le nombre de deps verifiees via npm (`verified_count`).

   **Etape 3 : Rechercher les configs et breaking changes via web** (complementaire)

   Pour **chaque dependance a risque de breaking changes** (identifiee dans le brief/scope) :

   a. **Trouver la doc officielle** :
      - `WebSearch` : `"<lib> getting started"` ou `"<lib> installation guide"`
      - Privilegier les domaines officiels (npmjs.com, github.com/<org>, docs officiels)

   b. **Extraire la configuration** :
      - `WebFetch` sur la page d'installation officielle
      - Extraire : packages a installer, fichiers de config requis, snippets de reference
      - Copier le snippet EXACT depuis la doc (pas de memoire LLM)

   c. **Identifier les breaking changes** :
      - `WebSearch` : `"<lib> migration guide"` ou `"<lib> upgrade from v<N-1>"`
      - Documenter : ancien pattern (a eviter) vs nouveau pattern (a utiliser)

   > **Si WebSearch/WebFetch echoue** (rate limit, erreur reseau) : logger un warning et continuer.
   > La verification configs/breaking changes est best-effort. Les versions npm sont obligatoires.

   **Etape 4 : Seuil de fiabilite**

   Calculer : `ratio = verified_count / total_deps`.
   - Si `ratio >= 0.5` (50%+) → continuer normalement.
   - Si `ratio < 0.5` → logger un warning :
     ```bash
     node tools/factory-log.js "MODEL" "stack-warning" "Seuil de fiabilite non atteint: X/Y deps verifiees via npm. Risque de versions incorrectes."
     ```
     Continuer quand meme (ne pas bloquer), mais le warning sera visible dans les logs.

   **Etape 5 : Generer `docs/specs/stack-reference.md`**

   Lire le template `templates/specs/stack-reference.md`.
   Creer le fichier `docs/specs/stack-reference.md` en remplissant :
   - **Dependencies runtime** : tableau avec package, version exacte (depuis npm), commande install, URL source
   - **Dependencies dev** : idem pour les deps de dev
   - **Configurations de reference** : pour chaque lib necessitant un fichier de config, inclure le snippet EXACT copie depuis la doc officielle (pas de memoire LLM)
   - **Compatibilite** : notes inter-dependances (ex: "Tailwind v4 necessite @tailwindcss/vite")
   - **Breaking changes connus** : tableau ancien vs nouveau pour chaque lib avec breaking change

   > **Ce fichier est la source de verite** pour toutes les etapes suivantes.
   > L'architect et le developer doivent s'y referer, pas inventer de versions.

   **Etape 6 : Logger**
   ```bash
   node tools/factory-log.js "MODEL" "stack-verified" "Verification stack: X/Y deps verifiees via npm, Z configs web → docs/specs/stack-reference.md"
   ```

   **3c. Agent Architect** (specs techniques + ADR, avec stack verifiee) :
   ```bash
   # Extraire le delta depuis les specs PM (disponibles apres 3a)
   node tools/extract-version-delta.js -f system -f domain

   # Instrumenter la delegation
   node tools/instrumentation/collector.js agent '{"agent":"architect","source":"factory-spec"}'
   ```
   ```
   Task(
     subagent_type: "architect",
     prompt: "Genere les specs techniques et ADR.
     Mode: <evolutionMode>. Version: <evolutionVersion>.
     Si mode=greenfield: CREATE docs/specs/api.md, ADR-0001-stack.md, project-config.json.
     Si mode=brownfield: EDIT api.md + CREATE nouveaux ADR + marquer anciens SUPERSEDED.
     DELTA VERSION COURANTE: <output de extract-version-delta.js>
     Lis les fichiers BREAK: docs/brief.md, docs/scope.md, docs/acceptance.md.
     Lis les specs PM: docs/specs/system.md, docs/specs/domain.md.
     Lis le fichier stack de reference: docs/specs/stack-reference.md.
     Lis les templates: templates/specs/api.md, templates/adr/ADR-template.md, templates/specs/project-config.json.
     IMPORTANT: Respecte EXACTEMENT les headings des templates (##).

     STACK REFERENCE (source de verite - UTILISE CES VERSIONS ET CONFIGS, PAS TA MEMOIRE) :
     Lis docs/specs/stack-reference.md pour toutes les versions, packages et configs.

     Pour chaque dependance dans l'ADR :
     - Utilise la version exacte et les packages indiques dans stack-reference.md
     - Inclus les snippets de configuration de reference dans une section '## Configuration de reference' de l'ADR
     - Si une lib a un setup specifique (ex: plugin Vite au lieu de PostCSS), documente-le
     - NE PAS inventer de config : utilise UNIQUEMENT les infos de stack-reference.md",
     description: "MODEL - Architect specs"
   )
   ```

   **3d. Agent Rules-Memory** (rules Claude Code) :
   ```bash
   # Extraire le delta depuis toutes les specs (disponibles apres 3a+3c)
   node tools/extract-version-delta.js -f system -f domain -f api

   # Instrumenter la delegation
   node tools/instrumentation/collector.js agent '{"agent":"rules-memory","source":"factory-spec"}'
   ```
   ```
   Task(
     subagent_type: "rules-memory",
     prompt: "Genere les rules Claude Code pour le projet.
     Mode: <evolutionMode>. Version: <evolutionVersion>.
     Si mode=greenfield: CREATE les rules dans .claude/rules/.
     Si mode=brownfield: mettre a jour les rules existantes, supprimer les obsoletes.
     ADR ACTIFS: <liste des paths retournes par list-active-adrs.js --summary>
     DELTA VERSION COURANTE: <output de extract-version-delta.js>
     IMPORTANT: NE PAS charger les ADR au statut SUPERSEDED.
     Lis les specs: docs/specs/system.md, docs/specs/domain.md, docs/specs/api.md.
     Lis le template: templates/rule.md.",
     description: "MODEL - Rules generation"
   )
   ```

4. **Executer Gate 2 (sortie avec auto-remediation)** :

   ```bash
   node tools/gate-check.js 2 --json
   ```

   Suivre le **protocole standard de gate handling** :

   **Tentative 1** : Analyser le JSON retourne.
   - Si `status === "PASS"` → continuer a l'etape 5.
   - Si `status === "FAIL"` :
     - Lire `errors[]`. Pour chaque erreur `fixable: true` :
       - `missing_section` → identifier le fichier et le template de reference dans le message d'erreur (`ref: templates/...`). Relancer l'agent responsable avec prompt : "Corrige [fichier]. Section manquante : [section]. Lis le template [template] et respecte exactement les headings."
       - `missing_file` → identifier le fichier manquant :
         - `stack-reference.md` → re-executer l'etape 3b (verification web + generation du fichier). C'est le fork qui le fait, pas un agent.
         - `system.md` / `domain.md` → relancer l'agent PM (step 3a).
         - `api.md` → relancer l'agent architect (step 3c).
         - Autre → relancer l'agent responsable.
       - `missing_pattern` → identifier le pattern manquant :
         - `.claude/rules/*.md` → relancer l'agent rules-memory (step 3d).
         - `docs/adr/ADR-*` → relancer l'agent architect (step 3c).
       - `config` → relancer l'architect pour corriger project-config.json.
       - `security` → corriger les secrets/PII directement.
     - Pour chaque erreur `fixable: false` → STOP, ne pas retenter.
     - Re-executer : `node tools/gate-check.js 2 --json`

   **Tentative 2** : Relancer les agents fautifs complets (PM, architect ou rules-memory selon les erreurs restantes).
   - Re-executer : `node tools/gate-check.js 2 --json`

   **Tentative 3** : Si toujours FAIL, retourner le rapport d'echec.
   - **NE PAS continuer le pipeline.**
   - Terminer avec : `GATE_FAIL|2|<resume erreurs separees par ;>|3`

5. **Sync ADR** (brownfield) :
   ```bash
   node tools/list-active-adrs.js --summary
   ```

6. **Logger** via :
   ```bash
   node tools/factory-log.js "MODEL" "completed" "Phase MODEL terminee"
   ```

7. **Retourner** un resume avec liste des fichiers generes (chemins complets).

## Protocole d'echec

- **Gate d'entree** (Gate 1) : Si FAIL → STOP immediat + marqueur `GATE_FAIL|1|...|0`.
- **Gate de sortie** (Gate 2) : Auto-remediation 3x puis marqueur `GATE_FAIL|2|...|3` si echec persistant.
- **Jamais** de STOP silencieux — toujours retourner un rapport structure.
