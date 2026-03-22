---
name: toggle-memory
description: Active ou desactive la session memory sur le projet courant. Si active, desactive et supprime le fichier. Si inactive, active la feature.
---

# Toggle Memory — Activer/desactiver la session memory

## Quand activer ce skill

- Quand l'utilisateur invoque `/toggle-memory`

## Mecanisme

Le fichier marqueur `.claude/.session-memory-enabled` indique si la feature est active.

- **Fichier present** → session memory active
- **Fichier absent** → session memory inactive

## Workflow

### Etape 1 : Detecter l'etat actuel

Verifier si `.claude/.session-memory-enabled` existe dans le projet courant.

### Etape 2A : Si active → Desactiver

1. Supprimer `.claude/.session-memory-enabled`
2. Si `.claude/session-memory.md` existe :
   - Afficher un resume du contenu (titres de sections, nombre de lignes)
   - Si `--save` passe en argument → Copier vers `.claude/session-memory-{date}.md` avant suppression
   - Supprimer `.claude/session-memory.md`
3. Afficher :
   ```
   Session memory desactivee. Le fichier de memoire a ete supprime.
   ```

### Etape 2B : Si inactive → Activer

1. Creer le dossier `.claude/` s'il n'existe pas
2. Creer `.claude/.session-memory-enabled` avec le contenu :
   ```
   # Session memory activee
   # Voir ~/koulia/common/session-memory.md pour la documentation
   ```
3. Verifier que `.claude/.session-memory-enabled` est dans `.gitignore` (sinon avertir)
4. Afficher :
   ```
   Session memory activee.
   En fin de session ou avant un /clear, je sauvegarderai automatiquement
   le contexte dans .claude/session-memory.md

   Pour desactiver : /toggle-memory
   ```

## Comment les skills detectent la feature

Les skills qui supportent la session memory (dev-story, feature-planner, etc.) peuvent verifier :

```
Si .claude/.session-memory-enabled existe → Proposer de sauvegarder le contexte en fin de workflow
```

Ce n'est pas bloquant — un skill fonctionne normalement meme sans session memory.

## Modes

| Etat actuel | Invocation | Resultat |
|---|---|---|
| Inactive | `/toggle-memory` | Active la feature |
| Active | `/toggle-memory` | Desactive + supprime la memoire |
| Active | `/toggle-memory --save` | Desactive + archive la memoire avant suppression |
