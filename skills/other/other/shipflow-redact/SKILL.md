---
name: shipflow-redact
description: Rédiger du contenu original long format — articles de blog, guides informationnels, éditoriaux — adapté à la marque, l'audience et la voix de l'auteur du projet
disable-model-invocation: true
argument-hint: <nombre> <format> [sujet] (ex: "3 blog", "1 editorial IA en éducation", "2 informational")
---

## Context

- Current directory: !`pwd`
- Project CLAUDE.md: !`head -120 CLAUDE.md 2>/dev/null || echo "no CLAUDE.md"`
- Branding: !`head -80 BRANDING.md 2>/dev/null || echo "no BRANDING.md"`
- Business: !`head -80 BUSINESS.md 2>/dev/null || echo "no BUSINESS.md"`
- Inspiration: !`head -60 INSPIRATION.md 2>/dev/null || echo "no INSPIRATION.md"`
- Source: !`head -60 SOURCE.md 2>/dev/null || echo "no SOURCE.md"`
- Guidelines: !`head -60 GUIDELINES.md 2>/dev/null || echo "no GUIDELINES.md"`
- Author identity: !`head -80 FOUNDER.md 2>/dev/null || head -80 AUTHOR.md 2>/dev/null || echo "no FOUNDER.md or AUTHOR.md"`
- Content language: !`grep -ri "lang=" src/layouts/*.astro src/app/layout.tsx 2>/dev/null | head -3 || echo "detect from content"`
- Existing content: !`find src/content content posts -name "*.md" -o -name "*.mdx" 2>/dev/null | head -20 || echo "no content dir found"`
- Content schema: !`cat src/content/config.ts src/content.config.ts 2>/dev/null | head -40 || echo "no content config"`
- Sample frontmatter: !`ls src/content/blog/*.md src/content/blog/*.mdx src/content/articles/*.md content/blog/*.md content/posts/*.md 2>/dev/null | head -1 | xargs head -30 2>/dev/null || echo "no sample found"`

## Your task

Write original, high-quality long-form content from scratch. Each article must read as if written by the project's founder/author — informed by brand identity, audience needs, and real web research. The reader should leave knowing more AND knowing exactly what to do next.

---

### MODE DETECTION

Parse `$ARGUMENTS` to extract:
- **Count**: number of articles to write (default: 1)
- **Format**: `blog` | `informational` | `editorial` (default: blog)
- **Topic**: optional topic hint (remaining words after count and format)

Examples:
- `3 blog` → 3 blog articles, topics to be determined in Phase 2
- `1 editorial IA en éducation` → 1 editorial piece on AI in education
- `2 informational` → 2 informational guides, topics to be determined
- `react server components` → 1 blog article (default) on React Server Components
- *(empty)* → use **AskUserQuestion**:
  - Question: "Quel contenu dois-je rédiger ?"
  - Options:
    - **1 article de blog** — "Un article sur un sujet pertinent au projet"
    - **3 articles de blog** — "Batch de 3 articles (recommandé)"
    - **1 guide informationnel** — "Guide éducatif approfondi (2000-3500+ mots)"
    - **1 éditorial** — "Prise de position / thought leadership du fondateur"
    - **Personnalisé** — "Préciser nombre, format et sujet"

**Définitions des formats** :
- **blog** : 1500-2500 mots. Pratique, actionnable. Enseigne quelque chose de spécifique. Ton d'expert accessible. Structure claire avec takeaways.
- **informational** : 2000-3500 mots. Guide complet. Profondeur éducative. Couvre un sujet de manière exhaustive. Contenu de référence.
- **editorial** : 1500-2500 mots. Axé opinion. Première personne. Le fondateur partage une perspective, une leçon apprise ou un point de vue contrarian. La voix personnelle domine.

---

### PHASE 1 : ABSORBER L'IDENTITÉ DU PROJET

Lire INTÉGRALEMENT tous les fichiers de documentation disponibles (pas seulement les previews du Context) :

1. **CLAUDE.md** — vue d'ensemble, stack, architecture, utilisateurs cibles
2. **BRANDING.md** — voix de marque, ton, identité visuelle, tagline, valeurs
3. **BUSINESS.md** — mission, proposition de valeur, audience cible, business model, distribution
4. **GUIDELINES.md** — conventions techniques (utile pour l'exactitude technique)
5. **INSPIRATION.md** — références, concurrents, philosophie design
6. **SOURCE.md** — fondements de recherche, sources de données, frameworks académiques
7. **FOUNDER.md** ou **AUTHOR.md** — qui est le "je" quand on écrit (parcours, expertise, style, histoire personnelle)

Construire un modèle mental :

| Dimension | Extraire |
|-----------|----------|
| **Voix de marque** | Formelle/informelle ? Experte/accessible ? Sérieuse/ludique ? |
| **Persona auteur** | Qui est le "je" ? Son expertise, son histoire, ses signaux de crédibilité |
| **Lecteur cible** | Qui lit ? Niveau, pain points, objectifs, langue |
| **Style d'adresse** | tu / vous (FR), formal/casual (EN) |
| **Langue du contenu** | Français ou anglais (depuis `lang=`, contenu existant, ou CLAUDE.md) |
| **Angle unique** | Ce que ce projet/cette marque apporte que les concurrents n'ont pas |
| **Thèmes clés** | Sujets récurrents, valeurs, principes issus de la documentation |

Si **FOUNDER.md / AUTHOR.md est absent** : chercher des indices dans BUSINESS.md et BRANDING.md. Si toujours insuffisant, utiliser **AskUserQuestion** :
- Question : "J'ai besoin de connaître l'auteur des articles. Peux-tu décrire brièvement qui écrit ?"
- Type : texte libre

---

### PHASE 2 : PLANIFIER LE CONTENU

Pour chaque article à rédiger :

1. **Si aucun sujet fourni** : Proposer des sujets basés sur le contexte projet.
   - Analyser : que chercherait l'audience cible ? Quels problèmes le produit résout-il ? Quelle expertise le fondateur a-t-il ?
   - Utiliser **WebSearch** et **mcp__exa__web_search_exa** pour identifier les sous-sujets tendance, les lacunes de contenu dans la niche, les questions fréquentes.
   - Utiliser **AskUserQuestion** pour présenter les options :
     - Question : "Sur quels sujets dois-je écrire ?"
     - `multiSelect: true` (si count > 1)
     - Une option par sujet proposé : label = titre de travail, description = angle + pourquoi c'est pertinent
     - Proposer 2-3 options de plus que nécessaire pour laisser le choix

2. **Pour chaque sujet confirmé**, définir :
   - **Titre de travail** — accrocheur, spécifique, orienté bénéfice
   - **Mot-clé cible** — le terme de recherche principal visé
   - **Intent lecteur** — quel problème résout-il ? Quel résultat cherche-t-il ?
   - **Angle** — ce qui rend CET article différent des 10 autres sur le même sujet
   - **Plan** — structure H2/H3 avec points clés par section (5-8 sections)
   - **Objectif mots** — selon le format (blog: 1500-2500, informational: 2000-3500, editorial: 1500-2500)

---

### PHASE 3 : RECHERCHE

Pour chaque article, mener une recherche web approfondie. Chercher dans la **même langue** que le contenu ET en anglais pour la profondeur technique.

1. **Données et statistiques actuelles** — Utiliser **mcp__exa__web_search_exa** et **WebSearch** :
   - Derniers chiffres, benchmarks, études (2024-2026)
   - Rapports d'industrie, enquêtes, analyses d'experts
   - Noter chaque source avec son URL pour citation inline

2. **Perspectives d'experts** — Utiliser **mcp__firecrawl__firecrawl_search** :
   - Leaders d'opinion sur le sujet
   - Points de vue contrarian intéressants à référencer
   - Frameworks ou modèles mentaux pertinents

3. **Analyse de la concurrence** — Utiliser **WebSearch** :
   - Top 3-5 articles existants sur le même sujet
   - Ce qu'ils couvrent bien (pour égaler ou dépasser)
   - Ce qu'ils ratent (pour se différencier)

4. **Exemples réels et études de cas** — Utiliser **mcp__exa__web_search_exa** :
   - Histoires d'entreprises concrètes, résultats réels, implémentations spécifiques
   - Données avant/après, histoires de transformation
   - Éviter les exemples génériques ; trouver des cas nommés, spécifiques, vérifiables

5. **Exactitude technique** (sujets techniques) — Utiliser **mcp__exa__get_code_context_exa** et **mcp__context7__resolve-library-id** + **mcp__context7__query-docs** :
   - Références API, versions d'outils, fonctionnalités de frameworks
   - Exemples de code actuels et corrects

**Minimum 5 sources uniques par article.** Compiler un brief de recherche par article avant la rédaction.

---

### PHASE 4 : RÉDIGER

Produire l'article complet pour chaque pièce.

#### Détection du répertoire de contenu

Avant d'écrire, détecter où créer les fichiers :
- Astro : `src/content/blog/`, `src/content/articles/`, `src/content/posts/`
- Next.js : `content/blog/`, `content/posts/`, `app/blog/`
- Hugo : `content/posts/`, `content/blog/`
- Générique : `content/`, `blog/`, `posts/`

Utiliser le même répertoire que le contenu existant. Si plusieurs répertoires existent, utiliser **AskUserQuestion** pour confirmer. Respecter l'extension existante (`.md` ou `.mdx`).

#### Frontmatter

Respecter le schéma de contenu du projet (depuis `content/config.ts`). Si pas de schéma, utiliser :

```yaml
---
title: "[Titre accrocheur, spécifique — 50-70 caractères]"
description: "[Meta description — 150-160 caractères, inclut la proposition de valeur]"
date: [date du jour, format ISO]
author: "[depuis FOUNDER.md ou convention du projet]"
tags: [tags pertinents, taxonomie existante]
category: "[catégories existantes]"
readingTime: "[estimé : word count / 200]"
image: "[placeholder : /images/blog/slug.webp — signaler dans le rapport que l'image est nécessaire]"
draft: false
---
```

#### Écrire en tant que l'auteur

- **Première personne quand approprié** : "je" pour les éditoriaux toujours. "Nous" ou "je" pour blog si la marque l'utilise. Troisième personne si la marque est institutionnelle.
- **Anecdotes personnelles** : Puiser dans FOUNDER.md — expériences réelles, leçons, pivots. Ne JAMAIS inventer d'histoires personnelles.
- **Signaux de crédibilité** : Tisser l'expertise naturellement ("Après 10 ans à construire X...", "Quand j'ai lancé Y...").
- **Voix authentique** : Respecter le ton du BRANDING.md. Si la marque est ludique, être ludique. Si académique, être rigoureux.

#### Principes de rédaction

**Hook en 2 phrases.** Énoncer le problème, un fait surprenant, ou le résultat. Pas d'intro bateau ("Dans le monde d'aujourd'hui...", "Il est indéniable que...").

**Chaque section mérite sa place.** Supprimer tout paragraphe qui dit seulement "X est important" sans montrer POURQUOI. Pas de remplissage. Pas de blabla.

**Expert ami du lecteur.** Écrire comme si on expliquait à un collègue intelligent qui a besoin de concret, pas de platitudes. Anticiper ses questions. Répondre avant qu'il ne les pose.

**Données > adjectifs.** "Réduit le temps de chargement de 40%" bat "améliore significativement les performances." Chiffres spécifiques issus de la Phase 3. Chaque stat liée à sa source.

**Structure scannable :**
- Sous-titres qui racontent une histoire (parcourir les titres = 80% de la valeur)
- Paragraphes courts (2-3 phrases max)
- Listes à puces pour les étapes, comparaisons, checklists
- **Gras sur les phrases clés** pour le lecteur pressé
- TL;DR en haut pour les articles de plus de 1500 mots

**Pousse à l'action.** Terminer chaque section majeure par une prochaine étape concrète ou un takeaway. La conclusion est un tremplin, pas un résumé : "Voici quoi faire maintenant."

**Vivant et actuel.** Exemples 2024-2026. Outils réels, entreprises réelles, chiffres réels. Pas de conseil générique.

**Zéro cliché IA.** Interdits : "game-changer", "unlock your potential", "in today's digital landscape", "plongeons dans", "il est indéniable", "incontournable", "révolutionner", "leveraging", "at the end of the day".

#### Spécificités par format

**Blog** : Conversationnel mais expert. Enseigner une chose bien. Inclure exemples pratiques, code (si technique), ou instructions étape par étape. Terminer par un CTA clair.

**Informational** : Complet et structuré. Inclure tables de comparaison, pour/contre, frameworks de décision. Penser "le guide définitif." Ajouter une table des matières si plus de 2500 mots.

**Editorial** : Personnel et opinioné. Commencer par une thèse. Utiliser l'expérience personnelle comme preuve. Reconnaître les contre-arguments. Être vulnérable sur les leçons apprises. Terminer par un appel à la réflexion ou à l'action.

---

### PHASE 5 : OPTIMISER

Pour chaque article :

1. **SEO** :
   - [ ] Mot-clé cible dans : titre, premier paragraphe, 1-2 sous-titres, meta description
   - [ ] Densité de mot-clé naturelle (1-2%, jamais de bourrage)
   - [ ] Mots-clés associés/LSI intégrés naturellement
   - [ ] Slug URL propre et pertinent

2. **Liens internes** :
   - [ ] Lier vers 2-3 autres pages/articles du même site (s'ils existent)
   - [ ] Lier vers les pages produit/fonctionnalité pertinentes si naturel

3. **Liens externes** :
   - [ ] Toutes les stats et affirmations ont un lien source inline
   - [ ] Liens vers des références faisant autorité (docs officielles, études, articles d'experts)
   - [ ] Minimum 3 liens sources externes par article

4. **CTAs** :
   - [ ] Un CTA contextuel par article (lié à ce que le lecteur vient d'apprendre)
   - [ ] Le CTA est une extension naturelle du contenu, pas un pitch de vente
   - [ ] Pour éditorial : le CTA peut être "partagez votre perspective" ou "essayez cette approche"

5. **Enrichissements** (si approprié) :
   - [ ] Tables de comparaison pour outils/approches
   - [ ] Snippets de code (fonctionnels, prêts à copier-coller, commentés)
   - [ ] Encadrés pour astuces, avertissements, erreurs fréquentes
   - [ ] Section FAQ (2-4 questions que les gens cherchent réellement)

---

### PHASE 6 : CONTRÔLE QUALITÉ

Avant de finaliser, vérifier chaque article :

- [ ] **Word count** atteint l'objectif du format (blog: 1500-2500, informational: 2000-3500, editorial: 1500-2500)
- [ ] **Toutes les stats ont un lien source** — aucune affirmation non attribuée
- [ ] **Pas de texte placeholder** — pas de `[TODO]`, `[INSÉRER]`, `Lorem ipsum`
- [ ] **Frontmatter complet** — tous les champs requis remplis, conforme au schéma projet
- [ ] **Cohérence de ton** — la voix respecte la marque du début à la fin, pas de changement de style abrupt
- [ ] **Voix auteur authentique** — sonne comme le fondateur, pas comme un article IA générique
- [ ] **Langue correcte** — français OU anglais, jamais mélangé (sauf citations)
- [ ] **Flux de lecture** — fluide du début à la fin, chaque section s'appuie sur la précédente
- [ ] **Test "et alors ?"** — chaque section répond à pourquoi le lecteur devrait s'en soucier
- [ ] **Test "je partagerais ?"** — le contenu est-il assez utile pour que le lecteur l'envoie à un collègue ?
- [ ] **Pas de clichés IA** — aucun des termes interdits listés dans les principes de rédaction
- [ ] **Images notées** — le rapport liste où des images/illustrations amélioreraient l'article (avec descriptions suggérées)

---

### PHASE 7 : RAPPORT

Pour un seul article :
```
RÉDIGÉ : [titre de l'article]
─────────────────────────────────────
Format :         [blog / informational / editorial]
Sujet :          [sujet]
Mot-clé cible :  [keyword]
Langue :         [FR / EN]
Word count :     [nombre] mots
Sources citées : [nombre] (depuis [nombre] recherches web)
Liens internes : [nombre]
Liens externes : [nombre]
Fichier :        [chemin du fichier créé]
─────────────────────────────────────
Sections :
  1. [titre H2]
  2. [titre H2]
  3. ...

Images nécessaires :
  • [section] — [description image suggérée]
  • ...

Contexte manquant (pour amélioration) :
  • [ce qui était difficile à écrire sans plus d'info projet]
```

Pour batch (plusieurs articles) :
```
CONTENU RÉDIGÉ : [nombre] articles
═══════════════════════════════════════
  1. [titre]     [format]  [word count] mots  →  [chemin]
  2. [titre]     [format]  [word count] mots  →  [chemin]
  3. [titre]     [format]  [word count] mots  →  [chemin]
═══════════════════════════════════════
Total mots :         [somme]
Total sources :      [somme] depuis [nombre] recherches
Total images :       [nombre] nécessaires
Langue :             [FR / EN]

CALENDRIER DE PUBLICATION SUGGÉRÉ :
  Semaine 1 : Publier "[titre 1]" — [pourquoi en premier]
  Semaine 2 : Publier "[titre 2]" — [pourquoi ensuite]
  ...
═══════════════════════════════════════
```

---

### IMPORTANT

- **La langue est sacrée.** Détecter depuis le contenu existant, `<html lang>`, ou CLAUDE.md. Projet français = articles français. Anglais = anglais. Rechercher dans les deux langues pour la profondeur, mais rédiger dans la langue du projet.
- **Jamais inventer de stats.** Si pas de source trouvée, dire "selon les benchmarks de l'industrie" ou ne pas faire l'affirmation. Un chiffre faux détruit la confiance définitivement.
- **Jamais inventer d'histoires personnelles.** Si FOUNDER.md ne mentionne pas une expérience spécifique, ne pas en fabriquer. Utiliser les valeurs et la perspective de la marque à la place.
- **Jamais écrire de remplissage.** Si un article est trop court, ajouter plus de recherche et d'exemples spécifiques — pas de phrases creuses. Chaque mot doit mériter sa place.
- **Nommage fichiers** : slug en kebab-case dérivé du titre. Respecter la convention de nommage existante dans le répertoire de contenu.
- **Statut draft** : `draft: false` par défaut sauf si l'utilisateur demande explicitement des brouillons.
- **Ordre de publication** : quand on rédige plusieurs articles, suggérer un calendrier de publication dans le rapport basé sur l'actualité du sujet et la valeur stratégique.
- **Accents français obligatoires.** Lors de toute création ou modification de contenu en français, vérifier systématiquement que TOUS les accents sont présents et corrects (é, è, ê, à, â, ù, û, ô, î, ï, ç, œ, æ). Les accents manquants sont une faute d'orthographe. Relire chaque texte produit pour s'assurer qu'aucun accent n'a été oublié — c'est une erreur très fréquente à corriger impérativement.
