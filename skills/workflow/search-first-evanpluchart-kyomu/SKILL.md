---
name: search-first
description: Workflow de recherche systematique avant de coder. Cherche les solutions existantes (libs, MCP, skills, code interne) avant d'ecrire du code custom.
---

# Search-First — Rechercher avant de coder

## Quand activer ce skill

- Avant d'implementer une fonctionnalite non-triviale
- Quand on s'apprete a ecrire un utilitaire, un helper, ou une abstraction
- Quand on a besoin d'une lib pour une tache specifique (validation, date, parsing, etc.)
- Quand l'utilisateur demande "comment faire X" et que X est un probleme courant

## Posture

Tu es un developpeur senior qui sait que le meilleur code est celui qu'on n'ecrit pas. Avant de coder, tu cherches systematiquement si une solution existe deja — dans le projet, dans l'ecosysteme, ou dans les outils disponibles.

## Workflow en 5 etapes

### Etape 1 : Chercher dans le projet

Avant tout, verifier si le code existe deja dans le projet :

1. **Grep semantique** : chercher des fonctions/classes/composants similaires
2. **Patterns koulia** : verifier si un pattern documente dans `~/koulia/technos/` couvre le besoin
3. **Utils existants** : chercher dans les dossiers `utils/`, `helpers/`, `lib/`, `shared/`

Si trouve → **Reutiliser** (adapter si necessaire)

### Etape 2 : Chercher dans l'ecosysteme

Si rien dans le projet :

1. **Registry de packages** : npm (npmjs.com), PyPI, Packagist, crates.io selon le stack
2. **Context7** : verifier si la lib du framework couvre le besoin nativement
3. **GitHub** : chercher des implementations de reference

Criteres de selection d'une lib :
- Maintenance active (commits recents, issues traitees)
- Taille raisonnable (pas de mega-dependance pour un besoin simple)
- Types TypeScript inclus (pour les projets TS)
- Compatibilite avec le stack du projet

### Etape 3 : Chercher dans les outils MCP/Skills

Verifier si un outil disponible couvre le besoin :

1. **MCP servers** : un MCP installe peut-il resoudre le probleme ?
2. **Skills koulia** : un skill existant couvre-t-il une partie du workflow ?
3. **CLI disponibles** : `gh`, `docker`, `bruno`, etc.

### Etape 4 : Matrice de decision

| Situation | Action |
|---|---|
| Solution exacte trouvee dans le projet | **Reutiliser** directement |
| Lib mature et bien maintenue | **Adopter** (proposer l'ajout de dependance) |
| Lib proche mais pas exacte | **Etendre** (wrapper autour de la lib) |
| Plusieurs petites solutions a combiner | **Composer** (assembler les pieces) |
| Rien de satisfaisant | **Construire** (coder from scratch) |

### Etape 5 : Rapport de recherche

Avant de coder, presenter un resume court :

```
## Recherche effectuee
- Projet : [ce qui a ete trouve ou "rien de pertinent"]
- Ecosysteme : [libs candidates ou "rien de pertinent"]
- Outils : [MCP/skills/CLI ou "rien de pertinent"]

## Decision : [Reutiliser|Adopter|Etendre|Composer|Construire]
## Justification : [1 phrase]
```

## Regles

- Ne JAMAIS proposer de coder un utilitaire sans avoir d'abord cherche
- Ne JAMAIS ajouter une dependance sans verifier sa maintenance et sa taille
- Preferer les solutions natives du framework (ex: `Array.from()` plutot qu'une lib)
- Si "Construire" est choisi, expliquer pourquoi les autres options ne conviennent pas
- Le rapport de recherche peut etre court (3 lignes) pour les cas evidents
