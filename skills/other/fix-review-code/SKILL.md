---
name: fix-review-code
description: Corriger automatiquement les problemes identifies par /code-review en se basant sur les regles et conventions evan-workflow.
---

# Fix Review Code

## Objectif

Corriger automatiquement les problemes identifies par `/code-review`. Peut travailler a partir d'un rapport existant ou lancer sa propre review en interne avant de corriger.

## Input

- **Rapport existant** : `/fix-review-code path/to/review-report.md` ou le rapport est dans le contexte de conversation
- **Memes parametres que /code-review** : `/fix-review-code --commit abc123`, `/fix-review-code --branch feature/xxx`, etc. (lance une review interne puis corrige)

## Parametres

- `--auto` : Mode B — corriger tout ce qui est non-ambigu, skip les ambigus
- `--dry-run` : Mode C — montrer ce qui serait corrige sans modifier aucun fichier

Sans parametre, le mode par defaut est le Mode A (correction interactive).

## Workflow

### Etape 1 — Obtenir le rapport

- Si un rapport de code-review est fourni (fichier ou contexte) : le lire et parser les problemes
- Sinon : lancer `/code-review` en interne avec les parametres fournis pour obtenir le rapport

### Etape 2 — Trier les problemes

Trier les problemes par severite, du plus critique au moins critique :
1. CRITIQUE
2. HAUTE
3. MOYENNE
4. BASSE

### Etape 3 — Corriger chaque probleme

Pour chaque probleme, dans l'ordre de severite :

1. **Lire le fichier concerne** a la ligne indiquee
2. **Lire la regle evan-workflow applicable** pour comprendre la correction attendue
3. **Determiner la strategie de fix** selon `references/fix-strategies.md`
4. **Evaluer l'ambiguite** :
   - **Non-ambigu** : la correction est evidente et sans risque → appliquer directement
   - **Ambigu** : plusieurs corrections possibles ou risque d'effet de bord → selon le mode :
     - Mode A : demander confirmation au user
     - Mode B : skip le probleme
     - Mode C : mentionner l'ambiguite dans le rapport dry-run
5. **Appliquer la correction** avec l'outil Edit
6. **Verifier** que la correction ne casse pas les imports, les types ou les tests

### Etape 4 — Resume des corrections

Produire un resume :
- Nombre de corrections appliquees
- Nombre de problemes skipes (ambigus)
- Liste des fichiers modifies
- Problemes restants a traiter manuellement

### Etape 5 — Proposer le commit

- Mode A : proposer un ou plusieurs commits au user
- Mode B : creer le(s) commit(s) automatiquement
- Mode C : aucun commit

Le message de commit doit suivre le scope `commit` du manifeste evan-workflow (`~/evan-workflow/common/git-conventions.md`). Si les corrections couvrent plusieurs categories, proposer un commit par categorie (ex: un commit pour le style, un pour les fixes de bugs).

## Securite

- **Ne corriger que les violations claires.** Si une correction est ambigue, demander au user (Mode A) ou skipper (Mode B).
- **Ne jamais supprimer de code fonctionnel.** Un fix ne doit pas changer le comportement metier.
- **Verifier apres chaque correction** que les imports et les types restent coherents.
- **En cas de doute, ne pas corriger.** Mieux vaut laisser un probleme signale que d'introduire une regression.

## Modes

| Mode | Comportement | Ambiguite | Commit |
|------|-------------|-----------|--------|
| A (defaut) | Correction interactive | Demande confirmation | Propose au user |
| B (`--auto`) | Correction automatique | Skip | Commit auto |
| C (`--dry-run`) | Aucune modification | Signale | Aucun |
