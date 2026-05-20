---
name: factory-qa
description: "Phase DEBRIEF - Tests + QA + Release"
context: fork
allowed-tools: Read, Glob, Grep, Task, Bash
---

# Factory QA - Phase DEBRIEF

Tu es l'orchestrateur de la phase DEBRIEF.

> Cette phase DOIT produire **TOUS** les artefacts listes ci-dessous.
> La validation est assuree par Gate 5 (avec auto-remediation 3x).

## Artefacts obligatoires (TOUS requis)

| # | Artefact (V1) | Artefact (V2+) | Verification |
|---|--------------|----------------|-------------|
| 1 | `docs/qa/report.md` | `docs/qa/report-vN.md` | Sections: `## Résumé exécutif`, `## Tests exécutés` |
| 2 | `docs/release/checklist.md` | `docs/release/checklist-vN.md` | Section: `## Pré-release` |
| 3 | `CHANGELOG.md` | `CHANGELOG.md` (prepend) | Section: "## [" (version entry) |
| 4 | `release/` (dossier) | `release/` (dossier) | Export via `node tools/export-release.js` |

## Workflow

1. **Verifier Gate 4 (entree)** :
   ```bash
   node tools/gate-check.js 4 --json
   ```
   - Si `status === "FAIL"` → STOP immediat (prerequis manquants, ne peut pas corriger).
   - Terminer avec : `GATE_FAIL|4|<resume erreurs>|0`

2. **Detecter la version** :
   ```bash
   node tools/get-planning-version.js
   # Retourne: { "version": N, ... }
   ```

3. **Deleguer a l'agent `qa`** via Task tool :

   ```bash
   # Instrumenter la delegation (les hooks ne fonctionnent pas dans les forks)
   node tools/instrumentation/collector.js agent '{"agent":"qa","source":"factory-qa"}'
   ```

   - Si version = 1 (V1) :
     ```
     Task(
       subagent_type: "qa",
       prompt: "Tu DOIS produire EXACTEMENT 3 fichiers (TOUS obligatoires) :
       1. docs/qa/report.md - Rapport QA complet. Lis le template templates/qa/report-template.md d'abord.
          SECTIONS OBLIGATOIRES (exact match avec le template) : '## Résumé exécutif', '## Tests exécutés'
       2. docs/release/checklist.md - Checklist de release. Lis le template templates/release/checklist-template.md d'abord.
          SECTIONS OBLIGATOIRES (exact match avec le template) : '## Pré-release'
       3. CHANGELOG.md - Changelog. Lis le template templates/release/CHANGELOG-template.md d'abord.
          SECTION OBLIGATOIRE : '## [1.0.0]' (ou version appropriee)
       Lance les tests via 'pnpm test' et documente les resultats.
       NE RETOURNE PAS avant d'avoir cree les 3 fichiers.",
       description: "QA - Phase DEBRIEF"
     )
     ```
   - Si version > 1 (V2+, brownfield) :
     ```
     Task(
       subagent_type: "qa",
       prompt: "Tu DOIS produire EXACTEMENT 3 fichiers (TOUS obligatoires) :
       1. docs/qa/report-vN.md - Rapport QA version N. Lis le template templates/qa/report-template.md.
          SECTIONS OBLIGATOIRES (exact match avec le template) : '## Résumé exécutif', '## Tests exécutés'
       2. docs/release/checklist-vN.md - Checklist version N. Lis le template templates/release/checklist-template.md.
          SECTIONS OBLIGATOIRES (exact match avec le template) : '## Pré-release'
       3. CHANGELOG.md - Prepend la nouvelle version. Lis le fichier existant d'abord.
          SECTION OBLIGATOIRE : '## [N.0.0]' au-dessus des entrees existantes.
       N = version courante (utilise node tools/get-planning-version.js).
       NE RETOURNE PAS avant d'avoir cree les 3 fichiers.",
       description: "QA - Phase DEBRIEF (brownfield VN)"
     )
     ```

4. **Exporter le projet livrable** :
   ```bash
   node tools/export-release.js
   ```
   Cette commande:
   - Copie les fichiers du projet (hors infrastructure factory) vers `release/`
   - Genere un README.md enrichi depuis les specs
   - Cree un manifest de tracabilite (`docs/factory/release-manifest.json`)

5. **Executer Gate 5 (avec auto-remediation)** :

   ```bash
   node tools/gate-check.js 5 --json
   ```

   Suivre le **protocole standard de gate handling** :

   **Tentative 1** : Analyser le JSON retourne.
   - Si `status === "PASS"` → continuer a l'etape 6.
   - Si `status === "FAIL"` :
     - Lire `errors[]`. Pour chaque erreur `fixable: true` :
       - `missing_file` → relancer l'agent QA avec prompt cible : "Genere le fichier [fichier]. Lis le template correspondant."
         - `report.md` / `report-vN.md` → template `templates/qa/report-template.md`
         - `checklist.md` / `checklist-vN.md` → template `templates/release/checklist-template.md`
         - `CHANGELOG.md` → template `templates/release/CHANGELOG-template.md`
       - `missing_section` → relancer l'agent QA avec prompt cible : "Corrige [fichier]. Section manquante : [section]. Lis le template (ref dans le message d'erreur) et respecte exactement les headings."
       - `test_execution` → relancer les tests et documenter les resultats.
       - `export` → relancer `node tools/export-release.js`.
     - Pour chaque erreur `fixable: false` → STOP, ne pas retenter.
     - Re-executer : `node tools/gate-check.js 5 --json`

   **Tentative 2** : Relancer l'agent QA complet.
   - Re-executer : `node tools/gate-check.js 5 --json`

   **Tentative 3** : Si toujours FAIL, retourner le rapport d'echec.
   - **NE PAS continuer le pipeline.**
   - Terminer avec : `GATE_FAIL|5|<resume erreurs separees par ;>|3`

6. **Logger** via :
   ```bash
   node tools/factory-log.js "DEBRIEF" "completed" "Phase QA terminee"
   ```

7. **Retourner** le rapport final de release avec :
   - Resultat des tests
   - Couverture
   - Issues detectees
   - Checklist release validee

## Protocole d'echec

- **Gate d'entree** (Gate 4) : Si FAIL → STOP immediat + marqueur `GATE_FAIL|4|...|0`.
- **Gate de sortie** (Gate 5) : Auto-remediation 3x puis marqueur `GATE_FAIL|5|...|3` si echec persistant.
- **Jamais** de STOP silencieux — toujours retourner un rapport structure.
