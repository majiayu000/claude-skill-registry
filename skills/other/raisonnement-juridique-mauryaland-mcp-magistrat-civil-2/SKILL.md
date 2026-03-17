---
name: "raisonnement-juridique"
description: "Modélise le raisonnement juridique d'un magistrat français pour l'analyse de dossiers civils. Utiliser ce skill pour analyser un litige et identifier les questions juridiques, construire un raisonnement juridique structuré (syllogisme), rédiger une motivation de jugement civil, rechercher la jurisprudence et les textes applicables via Judilibre et Légifrance, qualifier juridiquement des faits et actes, distinguer prétentions, moyens et arguments. Basé sur les Fiches méthodologiques de rédaction du jugement civil (ENM/Cour de cassation, 2023)."
---

# Raisonnement Juridique - Méthodologie du Magistrat Civil

Ce skill guide Claude pour analyser des dossiers juridiques civils en appliquant la méthodologie du magistrat français, basée sur les fiches méthodologiques de l'ENM/Cour de cassation (2023).

## Capacités

- **Analyser un litige** : identifier les questions juridiques, qualifier les faits
- **Construire un raisonnement juridique** : syllogisme majeure/mineure/conclusion
- **Rédiger une motivation** : motivation complète, fidèle, impartiale, précise
- **Rechercher les sources** : jurisprudence (Judilibre) et textes (Légifrance)
- **Distinguer prétentions/moyens/arguments** : répondre correctement à chaque élément
- **Évaluer la hiérarchie des décisions** : pondérer les arrêts selon leur formation et publication

## Outils MCP disponibles

### Judilibre (jurisprudence)
- `judilibre_search` : rechercher des décisions par mots-clés, chambre, date
- `judilibre_get_decision` : récupérer le texte intégral d'une décision
- `judilibre_get_taxonomy` : obtenir les listes de référence (chambres, solutions, formations, publications)

### Légifrance (textes légaux)
- `rechercher_code` : rechercher dans les codes (Code civil, Code du travail...)
- `rechercher_dans_texte_legal` : rechercher dans les lois et décrets
- `recherche_journal_officiel` : rechercher dans le JORF
- `recuperer_article` : récupérer le texte intégral et les métadonnées d'un article par son ID

## Hiérarchie des Décisions de la Cour de cassation

### Formations de jugement (par ordre d'autorité décroissant)

| Formation | Magistrats | Coefficient | Cas de saisine |
|-----------|------------|-------------|----------------|
| **Assemblée plénière** | 19 | 10/10 | Question de principe, second pourvoi, résistance |
| **Chambres mixtes** | ≥13 | 9/10 | Divergences entre chambres, partage des voix |
| **Formation plénière chambre** | Variable | 7/10 | Revirement possible, question sensible |
| **Formation de section** | ≥5 | 5/10 | Affaires courantes complexes |
| **Formation restreinte** | 3 | 3/10 | Pourvoi irrecevable ou manifestement infondé |

### Publications (par ordre d'importance)

| Code | Publication | Coefficient | Signification |
|------|-------------|-------------|---------------|
| `b` | Publié au Bulletin | 10/10 | Arrêt de principe |
| `c` | Communiqué | 9/10 | Importance majeure |
| `r` | Publié au Rapport | 8/10 | Sélectionné pour le rapport annuel |
| `l` | Publié aux Lettres de chambre | 6/10 | Intérêt doctrinal |
| `n` | Non publié | 3/10 | Application jurisprudence établie |

### Règles de recherche OBLIGATOIRES

⚠️ **NE JAMAIS limiter la recherche à une seule chambre** sans vérifier les formations solennelles.

**Stratégie de recherche en 3 étapes** :

1. **D'abord : Formations solennelles**
   ```
   chamber: ["pl", "mi"]
   publication: ["b", "c"]
   ```
   
2. **Ensuite : Chambres pertinentes avec Bulletin**
   ```
   chamber: ["civ1", "civ2", "civ3", "comm", "soc", "cr"]  # selon la matière
   publication: ["b"]
   ```
   
3. **Enfin : Recherche exhaustive sans filtre de chambre**
   ```
   sort: "scorepub"  # Tri pertinence + publication
   ```

### Principe d'articulation

- **Un arrêt d'assemblée plénière > tout arrêt de chambre** (même récent)
- **Un arrêt publié au Bulletin > un arrêt non publié**
- **Entre deux arrêts de même niveau, le plus récent prévaut**
- **Effet contraignant** : après cassation par l'assemblée plénière, la juridiction de renvoi **doit** se conformer à la décision (art. L.431-4 COJ)

### Codes des chambres (taxonomie Judilibre)

| Code | Chambre |
|------|---------|
| `pl` | Assemblée plénière |
| `mi` | Chambre mixte |
| `civ1` | Première chambre civile |
| `civ2` | Deuxième chambre civile |
| `civ3` | Troisième chambre civile |
| `comm` | Chambre commerciale, financière et économique |
| `soc` | Chambre sociale |
| `cr` | Chambre criminelle |
| `creun` | Chambres réunies (historique, avant 1967) |
| `ordo` | Première présidence (Ordonnances) |
| `allciv` | Toutes les chambres civiles |

### Codes des formations (taxonomie Judilibre)

| Code | Formation | Magistrats |
|------|-----------|------------|
| `fp` | Formation plénière de chambre | Variable |
| `fs` | Formation de section | ≥5 |
| `f` | Formation restreinte | 3 |
| `frh` | Formation restreinte hors RNSM/NA | 3 |
| `frr` | Formation restreinte RNSM/NA | 3 |

### Codes de publication (taxonomie Judilibre)

| Code | Publication | Coefficient |
|------|-------------|-------------|
| `b` | Publié au Bulletin | 10/10 |
| `c` | Communiqué | 9/10 |
| `r` | Publié au Rapport | 8/10 |
| `l` | Publié aux Lettres de chambre | 6/10 |
| `n` | Non publié | 3/10 |

## Points de vigilance pour la recherche de jurisprudence de la Cour de cassation

✅ **À faire** :
- Toujours commencer par les formations solennelles (`pl`, `mi`)
- Vérifier la publication de chaque arrêt cité (`b`, `r`, `c`, `l`, `n`)
- Citer les arrêts publiés au Bulletin (`b`) de préférence
- Vérifier qu'un arrêt ancien n'a pas été infirmé

❌ **À éviter** :
- Se limiter à une seule chambre sans vérifier `pl`/`mi`
- Citer un arrêt non publié (`n`) comme fondement principal
- Ignorer un arrêt d'assemblée plénière au profit d'un arrêt de chambre récent

## Processus d'analyse

### 1. Prise en main du dossier

1. **Identifier les parties** : demandeur, défendeur, qualités
2. **Comprendre l'objet du litige** : quelle est la demande principale ?
3. **Situer chronologiquement** : faits, procédure antérieure
4. **Recenser les pièces** : preuves disponibles

### 2. Distinction prétentions / moyens / arguments

| Élément | Définition | Exemple | Réponse du juge |
|---------|-----------|---------|-----------------|
| **Prétention** | Objet de la demande (dispositif conclusions) | "Condamnation à 10 000€" | Statuer dans le dispositif |
| **Moyen de droit** | Règle juridique invoquée | "Art. 1240 C.civ." | Y répondre dans la motivation |
| **Moyen de fait** | Élément factuel au soutien | "Le défendeur a renversé le demandeur" | Analyser les preuves |
| **Argument** | Discussion sans effet juridique propre | "Le défendeur était pressé" | Ne pas y répondre |

**Règle fondamentale** : Le juge doit répondre à tous les moyens, jamais aux arguments.

### 3. Construction du syllogisme juridique

Le raisonnement juridique s'articule en trois temps :

#### MAJEURE (règle de droit)
- Énoncer la règle applicable (texte + jurisprudence)
- Préciser les conditions d'application
- Indiquer le régime probatoire
- **Utiliser Légifrance** pour citer le texte exact (voir workflow ci-dessous)
- **Utiliser Judilibre** pour l'interprétation jurisprudentielle

**Structure** : "Aux termes de l'article X du code Y, [règle]. Il en résulte que [conditions]."

**Sources à utiliser** :
- `rechercher_code` pour les articles de loi
- `judilibre_search` pour la jurisprudence interprétative

#### MINEURE (application aux faits)
- Commencer par "En l'espèce..."
- Exposer les faits établis
- Analyser les preuves
- Répondre aux moyens des parties
- Qualifier juridiquement les faits

**Structure** : "En l'espèce, il résulte des pièces que [faits établis]. Or, [qualification juridique]."

#### CONCLUSION
- Commencer par "En conséquence..."
- Tirer la conséquence juridique de la mineure
- Doit être en cohérence avec majeure et mineure
- Reproduire au dispositif du jugement

**Structure** : "En conséquence, [décision sur la prétention]."

### 4. Office du juge

#### Dans le domaine des faits
- **Art. 6 CPC** : Allégation par les parties
- **Art. 7 al.1** : Faits dans le débat uniquement
- **Art. 7 al.2** : Faits adventices (avec contradictoire)
- **Art. 9 CPC** : Charge de la preuve aux parties

#### Dans le domaine du droit
- **Art. 12 CPC** : Obligation de qualifier/requalifier
- Peut changer le fondement juridique
- **Art. 16 CPC** : Respecter le contradictoire

#### Limites
- Ne peut modifier l'objet du litige (art. 4 CPC)
- Respecter les prétentions hiérarchisées
- Ne peut relever d'office la prescription (art. 2247 C.civ.)

## Structure du jugement

1. **Chapeau** : mentions obligatoires (art. 454 CPC)
2. **Faits constants** : non contestés + pertinents
3. **Procédure** : saisine, clôture, audiences
4. **Prétentions et moyens** : chaque partie
5. **Motivation** : syllogisme pour chaque chef de demande
6. **Dispositif** : décision (art. 480 CPC - autorité chose jugée)

## Fichiers de référence

Pour approfondir, consultez :
- `references/hierarchie-decisions.md` : hiérarchie des formations et publications
- `references/syllogisme-juridique.md` : construction détaillée du syllogisme
- `references/office-du-juge.md` : pouvoirs et devoirs du juge
- `references/structure-jugement.md` : structure complète du jugement
- `references/exemples-motivations.md` : exemples par domaine juridique

## Utilisation des outils MCP

### Recherche de jurisprudence (Judilibre)

```
# Rechercher hiérarchiquement des arrêts sur un sujet
judilibre_search(query="responsabilité du fait des choses gardien", chamber=["pl", "mi"], publication=["b"])
→ Vérification des arrêts de principe (formations solennelles)

judilibre_search: query="responsabilité gardien chose chute", chamber=["civ2"], publication=["b"]
→ Jurisprudence de la chambre spécialisée (2e civile = responsabilité délictuelle)

# Obtenir une décision complète
judilibre_get_decision(id="...", resolve_references=true)
```

### Recherche de textes (Légifrance)

```
# Rechercher dans le Code civil
rechercher_code(code_name="Code civil", search="responsabilité contractuelle")

# Rechercher une loi spécifique
rechercher_dans_texte_legal(search="bail habitation", text_id="89-462")
```

### Récupération du texte intégral d'un article

**⚠️ RÈGLE IMPÉRATIVE** : Ne jamais citer un article de loi dans le syllogisme juridique sans avoir préalablement récupéré son texte intégral via `recuperer_article`. Les extraits tronqués des résultats de recherche ne suffisent pas pour une citation juridique fiable.

#### Workflow en deux étapes

**Étape 1 : Identifier l'article** via `rechercher_code` ou `rechercher_dans_texte_legal`

```
# Exemple : rechercher l'article sur les victimes de terrorisme
rechercher_code(code_name="Code des assurances", search="victimes terrorisme indemnisation")
```

→ Dans les résultats, repérer l'identifiant LEGIARTI de l'article pertinent (ex: `LEGIARTI000038312684`)

**Étape 2 : Récupérer le texte complet** via `recuperer_article`

```
# Récupérer le texte intégral avec toutes les métadonnées
recuperer_article(article_id="LEGIARTI000038312684")
```

→ Retourne :
- Texte intégral de l'article
- Métadonnées : numéro, titre, état (en vigueur/abrogé), dates
- Nota et observations
- Lien officiel Légifrance

#### Exemple complet

```
# 1. Recherche initiale
rechercher_code(code_name="Code civil", search="responsabilité fait personnel")
# → Trouve article 1240, ID: LEGIARTI000032041571

# 2. Récupération du texte complet
recuperer_article(article_id="LEGIARTI000032041571")
# → "Tout fait quelconque de l'homme, qui cause à autrui un dommage, 
#    oblige celui par la faute duquel il est arrivé à le réparer."
```

#### Format de citation dans le syllogisme

```
**MAJEURE**

Aux termes de l'article 1240 du code civil :

> « Tout fait quelconque de l'homme, qui cause à autrui un dommage, oblige celui par la faute duquel il est arrivé à le réparer. »

Lien : https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000032041571

Il résulte de ce texte que la responsabilité délictuelle suppose la réunion de trois conditions...
```

#### Recours à la recherche web

Utiliser `web_search` **uniquement en dernier recours** dans les cas suivants :
- L'API Légifrance retourne une erreur technique
- L'article n'est pas trouvé dans la base (texte très récent ou spécifique)
- Des informations complémentaires sont nécessaires (doctrine, travaux préparatoires)

Dans ce cas :
```
web_search("article L126-1 code des assurances legifrance texte intégral")
```

## Bonnes pratiques

1. **Toujours récupérer le texte intégral** via `recuperer_article` avant de citer un article
2. **Vérifier l'état de l'article** : en vigueur, abrogé, modifié
3. **Rechercher la jurisprudence récente** via Judilibre pour les questions d'interprétation
4. **Structurer le raisonnement** avec des titres apparents
5. **Répondre à tous les moyens** pertinents des parties
6. **Assurer la cohérence** entre motivation et dispositif
7. **Éviter** les motifs hypothétiques ("il semble"), dubitatifs ("vraisemblablement")
8. **Citer précisément** les pièces (nature, date, auteur)
9. **Inclure le lien Légifrance** officiel pour chaque article cité