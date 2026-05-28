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
node tools/factory-log.js "PIPELINE" "started" "Démarrage du pipeline"
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
- Prochaines étapes recommandées
