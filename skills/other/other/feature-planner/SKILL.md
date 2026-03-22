---
name: feature-planner
description: Planification de features avec discovery, generation de plan, review adversarial et synthese
---

# Feature Planner

## Objectif

Transformer une demande fonctionnelle en plan de developpement structure, avec stories decoupees, priorisees et validees par review adversarial.

## Modes d'execution

Le skill s'invoque avec `/feature-planner` suivi d'un mode :

| Mode | Declencheur | Description |
|------|------------|-------------|
| A | `--new <nom>` | Nouveau plan depuis une demande |
| B | `--iterate <nom>` | Nouvelle version du plan apres feedback |
| C | `--review <nom>` | Review adversarial du plan courant |
| D | `--finalize <nom>` | Generation du plan final valide |
| E | `--summary <nom>` | Synthese executive du plan |

## Structure generee

```
{docs-dir}/features/{nom}/plan/
  plan-v1.md          # Plan initial (puis v2, v3...)
  decisions.md        # Log des decisions prises
  review-critique.md  # Resultats des reviews adversariales
  summary.md          # Synthese executive (mode E)
```

## Workflow detaille

### Phase 1 : Discovery (Mode A uniquement)

1. **Scale-adaptive planning** : Evaluer la complexite de la demande
   - Si la feature est triviale (1-2 fichiers, < 1h de dev), suggerer `/quick-dev` au lieu d'un plan complet
   - Si la feature est petite (3-5 stories max), proposer un plan simplifie sans epics
   - Si la feature est moyenne a grande, continuer le workflow complet
2. **Comprendre le contexte** : Lire la demande, poser des questions de clarification si necessaire
3. **Scanner le code existant** : Identifier les fichiers, patterns et composants concernes
4. **Lire les conventions** : Lire `~/evan-workflow/common/manifest.yaml` et charger les fichiers des scopes `always` + scopes pertinents, puis `~/evan-workflow/technos/{stack}/patterns/` pertinents pour le domaine
5. **Identifier les contraintes** : Dependances, limitations techniques, risques

### Phase 2 : Generation du plan

1. **Decouper en epics** : Regroupements logiques de stories
2. **Definir les stories** selon les regles de qualite (voir ci-dessous)
3. **Ordonner par dependance** : Stories prerequises en premier
4. **Estimer les tailles** : S / M / L / XL
5. **Ecrire le plan** en suivant le template `references/plan-template.md`
6. **Logger les decisions** dans `decisions.md`

### Phase 3 : Review adversarial (Mode C)

1. **Adopter une posture critique** : Chercher les failles, pas les confirmations
2. **Verifier la completude** : Toutes les fonctionnalites sont couvertes ?
3. **Verifier la faisabilite** : Les patterns techniques sont corrects ?
4. **Verifier le decoupage** : Stories atomiques, pas de couplage cache ?
5. **Identifier les risques** : Dependances fragiles, edge cases, performance
6. **Rediger la review** en suivant `references/review-template.md`
7. **Verification explicite** : Relire la demande originale et confirmer que chaque exigence est tracee vers au moins une story

### Phase 4 : Iteration (Mode B)

1. **Lire le feedback** : Retours utilisateur ou review adversarial
2. **Identifier les changements** : Ce qui doit etre modifie
3. **Generer une nouvelle version** : plan-v{N+1}.md
4. **Logger les decisions** : Pourquoi chaque changement a ete fait

### Phase 5 : Plan final (Mode D)

1. **Verifier que la review adversarial a ete faite** (au moins une)
2. **Consolider** : Integrer tous les retours
3. **Valider la coherence** : Ordre des stories, dependances, estimations
4. **Marquer comme final** : Le plan est pret pour le sprint-planner

### Phase 6 : Synthese (Mode E)

1. **Resume executif** : Objectif, scope, nombre de stories
2. **Risques identifies** : Liste priorisee
3. **Estimations** : Effort total, repartition par epic
4. **Dependances externes** : APIs, services, equipes

## Regles de qualite des stories

Chaque story DOIT contenir :

| Champ | Regle |
|-------|-------|
| Titre | Verbe a l'imperatif (ex: "Implementer le formulaire de creation") |
| Description | Contexte + objectif + criteres d'acceptation |
| Fichiers cibles | Liste des fichiers a creer/modifier |
| Patterns | References vers `~/evan-workflow/technos/{stack}/patterns/` |
| Taille | S (< 30min), M (30min-2h), L (2-4h), XL (4h+, a redecouper) |
| Dependances | Stories prerequises par numero |

## Regles de qualite du plan

- Chaque story doit etre implementable independamment (une fois ses dependances resolues)
- Les stories XL doivent etre signalees pour redecoupe
- Les patterns techniques doivent correspondre a ceux documentes dans `~/evan-workflow/technos/{stack}/`
- Les fichiers cibles doivent etre realistes (verifier l'arborescence existante)
- Le plan doit respecter les conventions evan-workflow (chargees via le manifeste)

## Sortie attendue

A la fin de chaque mode, afficher :
- Le fichier genere/mis a jour
- Un resume des decisions prises
- La prochaine action recommandee (ex: "Lancer `--review` pour valider le plan")
