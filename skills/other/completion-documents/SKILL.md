---
name: completion-documents
description: >
  Ce skill doit être utilisé quand l'utilisateur demande à "compléter un cahier des charges",
  "remplir une offre de services", "créer un document à partir du gabarit", "préparer une
  proposition", ou a besoin de générer un cahier des charges ou une offre de services à partir
  d'un gabarit Word (.docx). Aussi déclenché par "gabarit", "template", "cahier des charges",
  "offre de services", "proposition commerciale", "CDC".
version: 0.1.0
---

# Complétion de Documents — Cahier des Charges et Offre de Services

Guider l'utilisateur dans la complétion de cahiers des charges et d'offres de services à partir de gabarits Word (.docx) existants.

## Prérequis

1. Le **gabarit Word** (.docx) — inclus dans le plugin sous `templates/`
2. Les **informations du projet** — soit via un brief, soit interactivement
3. (Optionnel) Le **contrat cadre** du client pour la vérification de cohérence

## Détection Automatique du Contrat Cadre

**IMPORTANT** — Avant de commencer la collecte d'informations, toujours scanner le répertoire de travail (workspace) pour détecter un contrat cadre existant. Les conventions de nommage sont :

- `CONTRAT-CADRE_ET_OFFRE_DE_SERVICES_(CCS)*` (ancien format)
- `CONTRAT_CADRE*` (nouveau format)

Patterns de recherche :
```
Glob: **/CONTRAT-CADRE_ET_OFFRE_DE_SERVICES_(CCS)*
Glob: **/CONTRAT_CADRE*
```

Si un contrat cadre est détecté, il **doit** être utilisé comme référence pour :
- Informer la rédaction du contenu (périmètre, conditions, terminologie du client)
- Pré-remplir les sections juridiques et conditions générales
- Déclencher automatiquement une vérification de cohérence à la fin de la génération

## Processus de Complétion

### Étape 1 : Analyse du Gabarit

1. Lire le gabarit Word fourni en utilisant le skill docx (unpack → lire XML ou pandoc)
2. Identifier toutes les sections et sous-sections du gabarit
3. Repérer les champs à compléter (texte entre crochets, placeholders, zones vides)
4. Dresser la liste des informations nécessaires pour compléter chaque section

### Étape 2 : Collecte des Informations

**Mode interactif (par défaut) :**
Poser des questions à l'utilisateur section par section en utilisant AskUserQuestion :
- Commencer par les informations générales (client, projet, dates)
- Progresser vers les détails techniques et fonctionnels
- Terminer par les conditions commerciales et juridiques

**Mode lot (si l'utilisateur fournit un brief) :**
1. Analyser le document ou texte fourni par l'utilisateur
2. Extraire les informations pertinentes pour chaque section
3. Identifier les lacunes et poser uniquement les questions manquantes

### Étape 3 : Génération du Document

1. Créer le document .docx final en utilisant le skill docx et la bibliothèque docx-js
2. Respecter fidèlement la mise en forme du gabarit original :
   - Polices, tailles, couleurs
   - En-têtes et pieds de page
   - Logo et images existantes
   - Styles de titres et paragraphes
3. Remplir chaque section avec le contenu collecté
4. Sauvegarder le document complété dans le dossier workspace

**CRITIQUE — Préservation des espaces dans les en-têtes et pieds de page** :
Lors de la manipulation des fichiers .docx (unpack/edit/repack), les en-têtes (`word/header*.xml`) et pieds de page (`word/footer*.xml`) sont particulièrement sensibles aux problèmes d'espacement :
- Les textes sont souvent fragmentés en plusieurs éléments `<w:t>` avec l'attribut `xml:space="preserve"` — cet attribut est **essentiel** pour conserver les espaces
- **NE JAMAIS** fusionner ou réassembler les éléments `<w:t>` dans les headers/footers
- **NE JAMAIS** supprimer `xml:space="preserve"` des éléments `<w:t>`
- Lors du remplacement de placeholders dans les headers/footers, s'assurer que les espaces adjacents ne sont pas supprimés
- Si un outil comme docx-js regénère le XML, vérifier explicitement que chaque `<w:t>` contenant un espace en début ou fin conserve `xml:space="preserve"`
- **Vérification obligatoire** : Après chaque génération de document, extraire le texte brut des headers et footers du fichier produit et le comparer au gabarit original pour détecter tout mot collé ou espace manquant

**CRITIQUE — Énumérations autonomes par section** :
Les listes numérotées (1, 2, 3... ou a, b, c...) dans un document Word utilisent des définitions de numérotation dans `word/numbering.xml`. Un problème fréquent est que les énumérations de différentes sections partagent le même `<w:numId>`, ce qui fait que la numérotation **continue** d'une section à l'autre au lieu de recommencer.
- Chaque énumération appartenant à une clause ou section différente doit avoir son propre `<w:numId>` dans `word/numbering.xml`, ou utiliser `<w:lvlOverride>` avec `<w:startOverride w:val="1"/>` pour forcer le redémarrage
- **NE JAMAIS** réutiliser le même identifiant de numérotation pour des listes de sections/clauses différentes
- Exemple concret : si la clause 6.1 a une énumération (a, b, c, d, e) et la clause 8 a sa propre énumération, elles doivent être indépendantes — la clause 8 doit recommencer à (a) et non continuer à (f)
- Si tu utilises docx-js : créer une nouvelle instance de numérotation avec `restart` pour chaque liste dans une nouvelle section
- Si tu fais du unpack/edit/repack : inspecter `word/numbering.xml` et s'assurer que chaque liste a son propre `<w:num w:numId="...">` séparé
- **Vérification obligatoire** : Après génération, parcourir le document et vérifier que chaque énumération recommence à 1 (ou a) dans sa section respective

### Étape 4 : Revue et Ajustements

1. Présenter un résumé des sections complétées
2. Demander à l'utilisateur s'il souhaite modifier ou ajuster du contenu
3. Appliquer les corrections demandées
4. Proposer la vérification de cohérence avec le contrat cadre si disponible

## Sections Typiques — Cahier des Charges

Voici les sections courantes dans un CDC de développement logiciel :

1. **Page de garde** : Titre du projet, client, date, version, auteur
2. **Contexte et objectifs** : Description du besoin, problématique actuelle, objectifs visés
3. **Périmètre du projet** : Inclusions et exclusions, modules concernés
4. **Exigences fonctionnelles** : User stories, cas d'utilisation, workflows
5. **Exigences non-fonctionnelles** : Performance, sécurité, accessibilité, compatibilité
6. **Architecture technique** : Stack technologique, intégrations, environnements
7. **Livrables attendus** : Code, documentation, formation, environnements
8. **Calendrier et jalons** : Phases, dates clés, critères de passage
9. **Critères d'acceptation** : Tests, validation, recette
10. **Annexes** : Maquettes, diagrammes, glossaire

## Sections Typiques — Offre de Services

1. **Page de garde** : Titre, client, prestataire, date, validité de l'offre
2. **Présentation de l'entreprise** : Somtech, compétences, références
3. **Compréhension du besoin** : Reformulation du besoin client
4. **Solution proposée** : Approche technique, architecture, choix technologiques
5. **Méthodologie** : Agile/Scrum, phases, livrables par phase
6. **Équipe projet** : Rôles, profils, disponibilité
7. **Calendrier de réalisation** : Planning, jalons, dépendances
8. **Proposition financière** : Estimation, ventilation, conditions de paiement
9. **Conditions générales** : Clauses juridiques, propriété intellectuelle, confidentialité
10. **Annexes** : CV de l'équipe, références clients, certifications

## Règles de Rédaction

- Adopter un ton professionnel et clair
- Utiliser la terminologie du client quand disponible
- Éviter le jargon technique excessif dans les sections destinées aux décideurs
- Être précis et quantifiable dans les engagements (délais, volumes, métriques)
- Inclure des réserves appropriées (hypothèses, dépendances, limites)

## Ressources

- **`references/guide-gabarits.md`** — Guide de bonnes pratiques pour la complétion des gabarits
