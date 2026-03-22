---
name: doc-client
description: "Generer une documentation client professionnelle a partir de la doc technique. Transforme la doc dev (generee par /feature-doc ou autre) en document metier sans jargon technique, pret pour import Google Docs et export PDF. Ce skill devrait etre utilise quand l'utilisateur veut creer une doc client, un livrable fonctionnel, une doc utilisateur, ou preparer un document de recette/presentation pour un client non-technique."
---

# Doc Client

## Objectif

Transformer une documentation technique en document client professionnel. Le document produit doit etre comprehensible par une personne sans aucune connaissance technique — un dirigeant, un chef de projet, un utilisateur final.

Le principe fondamental : le client ne se soucie pas de comment c'est construit, mais de ce que ca fait pour lui et pourquoi c'est utile.

## Input

- `/doc-client {domaine}` — Genere la doc client pour un domaine/feature
- `/doc-client --from {chemin}` — Genere depuis un ou plusieurs fichiers de doc technique specifiques
- `/doc-client --list` — Liste les domaines documentes disponibles (scan de `{docs-dir}/features/`)

## Parametres optionnels

- `--ton formel` | `--ton accessible` — Choisir le registre de langue (defaut : demander au user)
- `--longueur courte` | `--longueur standard` | `--longueur detaillee` — Choisir la densite (defaut : demander au user)

## Workflow

### Etape 1 — Configuration

Si le ton ou la longueur ne sont pas specifies en parametre, poser ces deux questions au user :

**Ton :**
- **Formel** — Registre corporate, phrases impersonnelles ("La fonctionnalite permet de...", "Le systeme offre...")
- **Accessible** — Registre direct, adresse au lecteur ("Vous pouvez desormais...", "Retrouvez facilement...")

**Longueur :**
- **Courte** — Synthese executive, 1-2 pages. L'essentiel en un coup d'oeil.
- **Standard** — Document complet, 3-5 pages. Couvre tous les cas d'usage.
- **Detaillee** — Documentation exhaustive, 5-10 pages. Chaque fonctionnalite expliquee en detail avec exemples.

### Etape 2 — Localiser la doc technique

Selon le mode :

- **Par domaine** : Scanner `{docs-dir}/features/{domaine}/` pour trouver les fichiers de doc technique (overview.md, architecture.md, api.md, data-model.md, workflows.md, components.md)
- **Par chemin** : Lire directement le(s) fichier(s) pointes
- **Mode --list** : Lister les sous-dossiers de `{docs-dir}/features/` et afficher les domaines disponibles, puis s'arreter

Si aucune doc technique n'est trouvee, proposer au user :
1. Lancer `/feature-doc --full {domaine}` d'abord pour generer la doc technique
2. Ou pointer vers des fichiers existants avec `--from`

### Etape 3 — Charger le contexte evan-workflow

1. Lire `~/evan-workflow/common/manifest.yaml` et charger les fichiers du scope `always`
2. En particulier respecter `~/evan-workflow/common/french-content.md` pour les regles d'ecriture francaise

### Etape 4 — Analyser la doc technique

Lire l'ensemble de la documentation technique et en extraire :
- Les fonctionnalites offertes a l'utilisateur final
- Les workflows metier (parcours utilisateur, pas flux de donnees)
- Les regles de gestion et contraintes metier
- Les cas d'usage concrets
- Les gains et la valeur apportee

Ignorer completement :
- L'architecture technique (services, controllers, composants)
- Les noms de fichiers, classes, fonctions, variables
- Les choix technologiques (framework, librairie, ORM)
- Les details d'implementation (requetes, types, interfaces)

### Etape 5 — Structurer le document

Adapter la structure au domaine et au contenu. Ne pas forcer un plan rigide — le plan doit refleter naturellement les cas d'usage du domaine.

Exemples de structures possibles (a adapter) :

**Pour une feature utilisateur :**
1. Presentation generale
2. Ce qui change pour vous (avant/apres)
3. Comment ca fonctionne (parcours pas a pas)
4. Questions frequentes

**Pour un module metier complexe :**
1. Objectif et contexte
2. Fonctionnalites principales
3. Cas d'usage detailles
4. Regles de gestion
5. Points d'attention

**Pour une mise a jour / evolution :**
1. Resume des nouveautes
2. Detail des ameliorations
3. Impact sur vos usages actuels

Consulter `references/writing-guide.md` pour les regles de redaction et le glossaire de traduction technique → metier.

### Etape 6 — Rediger le document

Produire un fichier markdown propre en suivant ces regles de formatage (pensees pour l'import Google Docs) :

- **Titre H1** unique en haut du document
- **Sections H2** pour les grandes parties, **H3** pour les sous-parties
- **Listes a puces** pour les fonctionnalites et enumerations
- **Tableaux** quand une comparaison ou une synthese s'y prete
- **Texte en gras** pour les termes cles et les noms de fonctionnalites
- **Jamais** de blocs de code, de backticks, de noms de fichiers
- **Jamais** de liens markdown (pas cliquables dans un PDF)
- Ajouter un en-tete avec la date de generation et le nom du projet

### Etape 7 — Generer le fichier

Ecrire le document dans :
```
docs/features/{domaine}/client/{domaine}-{dd-mm-yyyy-hh-min-ss}.md
```

Le timestamp utilise l'heure courante au format `dd-mm-yyyy-hh-min-ss`.

Creer les dossiers intermediaires si necessaire.

Afficher un resume :
- Chemin du fichier genere
- Nombre de sections
- Ton et longueur utilises
- Suggestion : "Vous pouvez importer ce fichier dans Google Docs pour le finaliser"

## Principes de redaction

La qualite du document repose sur la capacite a traduire le technique en metier. Ce n'est pas un exercice de simplification — c'est un exercice de reformulation ou l'on change completement d'angle.

- **Penser valeur, pas implementation.** "L'utilisateur peut filtrer par date" plutot que "Un filtre date a ete ajoute au state provider".
- **Penser parcours, pas architecture.** "Quand vous creez une fiche, le systeme verifie automatiquement..." plutot que "Le validator verifie les contraintes avant la persistence".
- **Penser impact, pas fonctionnalite.** "Vous gagnez du temps sur la saisie grace au remplissage automatique" plutot que "Un autocomplete a ete implemente".
- **Utiliser le vocabulaire du client.** Si la doc technique parle d'"entite Adherent", le document client parle d'"adherent" ou de "fiche adherent" — jamais d'"entite".
