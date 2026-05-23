---
name: factory-run
description: "Pipeline complet requirements → release"
allowed-tools: Read, Glob, Grep, Bash, Task, Skill
---

# Factory Run - Pipeline Complet

Tu es l'orchestrateur master du pipeline complet requirements → release.

## Workflow

Exécuter les 5 phases **séquentiellement** en invoquant chaque skill directement.
Chaque skill a son propre `context: fork` et gère sa délégation d'agent.

### Initialisation
```bash
# Reset instrumentation pour un timeline propre
node tools/instrumentation/collector.js reset

# Instrumentation (si activée)
node tools/instrumentation/collector.js skill "{\"skill\":\"factory-run\"}"

# Log démarrage
node tools/factory-log.js "PIPELINE" "started" "Demarrage du pipeline"
```

### Phase 1 - BREAK
Invoque `/factory-intake` et attends le résultat.
Si Gate 1 échoue → STOP et rapport d'erreur.

### Phase 2 - MODEL
Invoque `/factory-spec` et attends le résultat.
Si Gate 2 échoue → STOP et rapport d'erreur.

### Phase 3 - ACT (planning)
Invoque `/factory-plan` et attends le résultat.
Si Gate 3 échoue → STOP et rapport d'erreur.

### Phase 4 - ACT (build)
Invoque `/factory-build` et attends le résultat.
Si Gate 4 échoue → STOP et rapport d'erreur.

### Phase 5 - DEBRIEF
Invoque `/factory-qa` et attends le résultat.
Si Gate 5 échoue → STOP et rapport d'erreur.

### Finalisation
```bash
node tools/factory-log.js "PIPELINE" "completed" "Pipeline terminé avec succès"
```

## Règles critiques

- **Séquentiel strict** : Chaque phase DOIT réussir (gate OK) avant la suivante
- **Si un gate échoue** → STOP immédiat, logger l'erreur, retourner rapport
- **Pas de nesting** : Invoquer les skills directement, ils gèrent leur propre fork

## Rapport final

À la fin du pipeline, produire un résumé complet :
- Phases complétées avec statuts
- Artefacts générés (liste des fichiers créés)
- Issues détectées (si applicable)
- Prochaines étapes recommandées :

### Projet livrable
Informer l'utilisateur que :
- Le projet livrable se trouve dans **`release/`**
- Le code existe en double (racine + `release/`) — c'est **intentionnel** :
  - **Racine** : environnement de travail avec l'infrastructure factory
  - **`release/`** : projet livrable propre, prêt à être copié
- Commandes pour récupérer le projet :
```bash
# Option 1 : Copier vers un nouveau repo
cp -r release/ ../mon-projet/
cd ../mon-projet && git init && npm install

# Option 2 : Tester localement
cd release && npm install && npm test && npm run build
```

### Commandes post-pipeline (à suggérer à l'utilisateur)
```bash
# Vérification complète du pipeline (38 checks)
node tools/verify-pipeline.js

# Couverture de l'instrumentation
node tools/instrumentation/coverage.js

# Rapport détaillé instrumentation (markdown)
node tools/instrumentation/reporter.js
```
