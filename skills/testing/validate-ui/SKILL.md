---
name: validate-ui
description: |
  Valider l'interface et capturer les erreurs console.
  TRIGGERS : validate-ui, vérifier console, 0 erreur, validation UI, test UI
disable-model-invocation: false
---

# Validate UI

## Procédure

### 1. Naviguer vers la page modifiée

Ouvrir la page concernée dans le navigateur.

### 2. Interagir avec les éléments

Si applicable, reproduire le scénario utilisateur :
- Clics
- Saisie de formulaires
- Navigation

### 3. Capturer les logs console

Capturer les erreurs console (type: "error").

### 4. Analyser

Pour chaque erreur :
- Identifier la source (stack trace)
- Comprendre la cause
- Proposer une correction

## Si erreurs détectées

```
1. Identifier la cause (stack trace)
2. Corriger le code
3. Recharger la page
4. RE-CAPTURER les logs console
5. Répéter jusqu'à 0 erreur
```

**⚠️ NE PAS terminer tant qu'il y a des erreurs console.**

## Output attendu

### ✅ Succès
```
✅ Validation UI terminée
   Page : /chemin/vers/page
   Erreurs console : 0
   Status : OK
```

### ❌ Échec
```
❌ Validation UI échouée
   Page : /chemin/vers/page
   Erreurs console : N

   Erreur 1:
   - Message : [message d'erreur]
   - Source : [fichier:ligne]
   - Cause probable : [analyse]

   Action : Corriger et revalider
```
