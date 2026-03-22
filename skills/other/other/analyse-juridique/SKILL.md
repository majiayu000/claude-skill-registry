---
name: analyse-juridique
description: >
  Ce skill doit être utilisé quand l'utilisateur demande à "vérifier les clauses",
  "comparer le contrat cadre", "analyser la cohérence juridique", "valider les clauses
  de l'offre", ou a besoin d'extraire et comparer des clauses entre un contrat cadre PDF
  et une offre de services. Aussi déclenché par "contrat cadre", "clauses juridiques",
  "cohérence contractuelle", "vérification légale".
version: 0.1.0
---

# Analyse Juridique — Contrat Cadre vs Documents Produits

Extraire les clauses d'un contrat cadre PDF fourni par le client, puis les comparer aux clauses mentionnées dans l'offre de services pour détecter les incohérences.

## Détection Automatique du Contrat Cadre

**IMPORTANT** — Toujours scanner le répertoire de travail (workspace) pour détecter un contrat cadre existant avant de demander à l'utilisateur. Les conventions de nommage sont :

- `CONTRAT-CADRE_ET_OFFRE_DE_SERVICES_(CCS)*` (ancien format)
- `CONTRAT_CADRE*` (nouveau format)

Patterns de recherche :
```
Glob: **/CONTRAT-CADRE_ET_OFFRE_DE_SERVICES_(CCS)*
Glob: **/CONTRAT_CADRE*
```

Si un fichier est trouvé, l'utiliser automatiquement. Si plusieurs correspondent, demander à l'utilisateur lequel utiliser.

## Processus d'Analyse

### Étape 1 : Extraction du Contrat Cadre

1. Localiser le contrat cadre (détection automatique ou fourni par l'utilisateur via l'outil Read ou le skill PDF)
2. Identifier et extraire chaque clause juridique significative
3. Classifier chaque clause par catégorie (voir référence `references/clauses-types.md`)
4. Produire un résumé structuré des clauses extraites

### Étape 2 : Extraction des Clauses de l'Offre

1. Lire le document d'offre de services (.docx) — soit le gabarit complété, soit un brouillon
2. Identifier toutes les mentions de clauses, conditions et engagements
3. Classifier par catégorie correspondante

### Étape 3 : Comparaison et Détection d'Incohérences

Comparer clause par clause en vérifiant :

**Cohérence directe :**
- Les obligations mentionnées dans l'offre correspondent-elles aux termes du contrat cadre ?
- Les limites de responsabilité sont-elles alignées ?
- Les conditions de propriété intellectuelle sont-elles compatibles ?

**Omissions :**
- Y a-t-il des clauses du contrat cadre qui ne sont pas reflétées dans l'offre ?
- Y a-t-il des engagements dans l'offre qui ne sont pas couverts par le contrat cadre ?

**Contradictions :**
- Des termes dans l'offre contredisent-ils directement le contrat cadre ?
- Des délais, conditions de paiement ou pénalités divergent-ils ?

### Étape 4 : Rapport de Cohérence

Produire un rapport structuré avec :

1. **Résumé exécutif** : Nombre de clauses analysées, nombre d'incohérences trouvées, niveau de risque global
2. **Clauses alignées** : Liste des clauses cohérentes entre les deux documents
3. **Incohérences détectées** : Pour chaque incohérence :
   - Catégorie de clause
   - Ce que dit le contrat cadre (citation)
   - Ce que dit l'offre de services (citation)
   - Nature de l'incohérence (contradiction, omission, divergence)
   - Niveau de risque (élevé, moyen, faible)
   - Recommandation d'action
4. **Clauses manquantes** : Clauses du contrat cadre non couvertes dans l'offre

## Modes de Fonctionnement

### Mode interactif
Poser des questions à l'utilisateur pour clarifier les ambiguïtés trouvées avant de finaliser le rapport.

### Mode automatique
Produire le rapport complet avec toutes les incohérences détectées, en marquant les cas ambigus pour revue humaine.

## Règles Importantes

- Ne JAMAIS fournir de conseil juridique formel — toujours préciser que l'analyse est un outil d'aide et qu'un juriste devrait valider les points critiques
- Citer textuellement les passages pertinents des deux documents
- En cas de doute sur l'interprétation d'une clause, signaler l'ambiguïté plutôt que de trancher
- Toujours recommander une revue humaine pour les incohérences de niveau "élevé"

## Ressources

- **`references/clauses-types.md`** — Taxonomie des clauses juridiques courantes dans les contrats de développement logiciel
