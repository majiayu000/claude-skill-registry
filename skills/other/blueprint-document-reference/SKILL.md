---
name: blueprint-document-reference
description: Référence pour la création et la modification de documents de plan directeur d’expérience digitale Adobe. À utiliser lors de la création de plans directeurs, de l’ajout de pages de plan directeur ou lorsque l’utilisateur pose des questions sur la structure, les sections, les modèles de plan directeur ou le référencement d’Adobe Experience League.
source-git-commit: a632042b3a7434dd88f52804e15e30fa06057e3b
workflow-type: tm+mt
source-wordcount: '445'
ht-degree: 1%

---


# Référence du document de plan directeur

Utilisez ces compétences lors de la création ou de la modification de documents de plan directeur dans ce référentiel. Les plans directeurs sont des implémentations reproductibles qui répondent à des problèmes commerciaux établis et incluent des diagrammes d’architecture, des considérations techniques et des liens vers la documentation Adobe Experience League associée.

## Quand appliquer

- Création d’un document de plan directeur ou d’une page d’aperçu de plan directeur
- Ajout ou restructuration de sections dans un plan directeur existant
- Lier ou citer la documentation d’Adobe Experience League
- Alignement du nouveau contenu sur les conventions de plans directeurs (frontaux, titres, diagrammes)

## Référence rapide

1. **Objectif du document** : les plans directeurs fournissent une architecture du système et du flux de données pour montrer comment Adobe Experience Platform et les applications sont intégrés. Elles sont visuelles et techniques, et non marketing.
2. **Sections** : utilisez les sections standard du modèle ; omettez uniquement lorsque cela n’est pas applicable (voir [reference.md](reference.md)).
3. **Experience League** : préférez la liaison à Experience League pour obtenir des documents sur les produits, des API, des mécanismes de sécurisation et des tutoriels. Utiliser des URL complètes ; voir [reference.md](reference.md) pour les modèles et la mise en forme d’URL.
4. **Structure de référentiel** : les plans directeurs sont actifs sous `help/blueprints/`. Mettez à jour les `help/blueprints/TOC.md` lors de l’ajout ou du déplacement de pages de plan directeur.

## Modèle de document

Chaque page de plan directeur doit suivre cette structure. Inclure uniquement les sections qui s’appliquent.

```markdown
---
title: [Short descriptive title]
description: "[One sentence: what this blueprint shows and why it matters.]"
solution: [Product name, e.g. Real-Time Customer Data Platform, Journey Optimizer]
exl-id: [UUID - leave blank if new, this will be auto-generated as part of the Experience League publishing flow]
---
# [H1 - same as title or expanded]

[1–3 paragraphs: what the blueprint covers, key capabilities, and who it’s for.]

## Applications

* [Product 1]
* [Product 2]

## Use cases

* [Use case 1]
* [Use case 2]

## Prerequisites

[Bullets or short paragraphs: required products, config, or setup.]

## Architecture Diagram

<img src="[path to SVG/image]" alt="[Descriptive alt]" style="width:90%; border:1px solid #4a4a4a" class="modal-image" />

## Guardrails

[Link to Experience League guardrails and any blueprint-specific limits.]

## Implementation patterns

[Optional: named patterns with bullets.]

## Implementation steps

1. [Step with link to Experience League where relevant]
2. ...

## Implementation considerations

[Optional: identity, performance, security, etc.]

## Related documentation

[Grouped links to Experience League: product docs, APIs, tutorials.]
```

Pour les pages de présentation ou de hub, utilisez une structure plus courte : introduction, cas d’utilisation (ou onglets), image d’architecture, tableau de scénarios/modèles, conditions préalables, mécanismes de sécurisation, documentation connexe. Consultez les présentations existantes dans `help/blueprints/` pour obtenir des exemples.

## Matière Première

| Champ | Obligatoire | Remarques |
|-------|----------|--------|
| `title` | Oui | Court ; utilisez `[!DNL Product Name]` pour les noms de produit selon le style Adobe. |
| `description` | Oui | Une phrase ; utilisée dans les recherches et les cartes |
| `solution` | Oui | Produit en Principal (par exemple Real-Time Customer Data Platform, Journey Optimizer) |
| `exl-id` | Oui | UUID ; laisser vide pour les nouvelles pages |
| `doc-type` | Pour les vues d’ensemble | Utiliser des `overview-page` pour les pages d’aperçu de plan directeur principales |
| `kt` | Facultatif | ID de l’article de la base de connaissances s’il est lié |

## Référencer Adobe Experience League

- **Quand créer un lien** : créez un lien vers Experience League pour accéder à la documentation du produit, aux références d’API, aux mécanismes de sécurisation, aux tutoriels et aux étapes de configuration. Ne dupliquez pas les longues procédures ; résumez et liez.
- **Format d’URL** : utilisez des URL complètes. Préférez `https://experienceleague.adobe.com/docs/?lang=fr...` ou `https://experienceleague.adobe.com/fr/docs/...`. Pour les documents destinés aux développeurs, `https://developer.adobe.com/...` est également valide.
- **Texte du lien** : utilisez un texte descriptif (par exemple, « [Créer des schémas] (url) » et non « Cliquer ici »). Pour les noms de produit dans le texte du lien, utilisez `[!DNL Product Name]` le cas échéant.
- **Section de documentation connexe** : terminez les plans directeurs par une section « Documentation connexe » regroupant les liens par catégorie (par exemple, configurations de destination, documentation de SDK, profil et segmentation, tutoriels).

Pour obtenir des modèles d’URL détaillés, un regroupement de liens et des exemples, voir [reference.md](reference.md).

## Liste de contrôle avant envoi

- [ ] FrontMATTER a `title`, `description`, `solution`, `exl-id`
- [ ] H1 correspond au titre ou le développe de manière appropriée
- [ Diagramme d’architecture ] présent et texte secondaire descriptif
- [ Lien des étapes d’implémentation ] vers Experience League où se trouvent les procédures
- [ ] section Mécanismes de sécurisation : liens vers les documents officiels sur les mécanismes de sécurisation Experience League.
- [ ] section Documentation connexe comprend des liens Experience League pertinents
- [ ] les pages nouvelles ou déplacées sont reflétées dans les `help/blueprints/TOC.md`

## Ressources supplémentaires

- Modèle complet et notes de section : [reference.md](reference.md)
- Plans directeurs existants : `help/blueprints/` (par exemple, `audience-activation/real-time-lookup.md`, `customer-journeys/journey-optimizer/journey-optimizer-overview.md`)
- Table des matières et navigation : `help/blueprints/TOC.md`
