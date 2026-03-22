---
name: industry-use-case-builder
description: 'Guidez la création de nouveaux cas d’utilisation du secteur pour le référentiel de plans directeurs Adobe Experience Platform. Utilisez cette compétence lors de l’ajout d’un nouveau cas d’utilisation à un secteur vertical (vente au détail, automobile, soins de santé, services financiers, assurance, médias et divertissement, télécommunications, voyages et hébergement, B2B), lorsque l’utilisateur souhaite ajouter des scénarios commerciaux aux pages du secteur ou lors de la mise à jour du catalogue de cas d’utilisation. Gère l’ensemble du workflow : collecte des détails du cas d’utilisation, évaluation du niveau de maturité, génération de contenu, mise à jour de la page de présentation du secteur et du catalogue de cas d’utilisation, et appel de la compétence use-case-icon-generator pour la création d’icônes.'
source-git-commit: ed8928687806b619e95d8d320478d27c13722a80
workflow-type: tm+mt
source-wordcount: '783'
ht-degree: 1%

---


# Créateur de cas d’utilisation du secteur

Cette compétence guide la création de cas d’utilisation du secteur pour le référentiel de plans directeurs Adobe Experience Platform. Suivez chaque phase de manière séquentielle. Lisez les fichiers de référence avant de commencer :

- `references/use-case-template.md` : modèle exact pour les sections de cas d’utilisation
- `references/catalog-row-template.md` — format exact des lignes de la table du catalogue
- `references/maturity-criteria.md` — rubrique détaillée pour l&#39;évaluation de l&#39;échéance

## Phase 1 : Collecte d&#39;informations

Interrogez l’utilisateur ou l’utilisatrice pour collecter tous les détails requis avant de générer du contenu.

### Champs obligatoires

1. **Secteur vertical** — Doit être l&#39;un des suivants :
   - automobile
   - b2b
   - services financiers
   - santé
   - assurance
   - média-divertissement
   - vente au détail
   - télécommunications
   - voyage-accueil

2. **Nom du cas d’utilisation** — Titre clair et descriptif (par exemple, « Récupération d’e-mails de panier abandonné », « Campagnes d’observance des médicaments »).

3. **Description** — 1 à 2 phrases décrivant le scénario commercial et son importance.

4. **Impact commercial** — Résultats quantifiés avec des mesures spécifiques (p. ex., « augmentation de 20 à 30 % des taux de clics publicitaires », « amélioration de 15 à 25 % des taux de renouvellement »).

5. **Modèle de cas d’utilisation** — Doit correspondre exactement à l’un de ces modèles existants :
   - Audience Activation vers les destinations
   - Audience Collaboration avec correspondance de segments
   - Transfert d’événement
   - Audience Activation B2B
   - Personalization Web de visiteur anonyme
   - Personalization Web/App Connu Des Visiteurs
   - Offer Decisioning
   - Recommandation comportementale
   - Activation des messages sortants par lots
   - Messagerie déclenchée par événement
   - Parcours Orchestré À Plusieurs Étapes
   - Parcours cross-canal avec prise de décision
   - Marketing et gestion de Parcours par groupe d&#39;achats
   - Génération de Customer Analytics et d’Insight
   - Analyses B2B
   - Expérience de conversation Brand Concierge

6. **Considérations techniques** — 4 à 8 puces couvrant les exigences en matière de données, les intégrations, les besoins en matière de réglementation/conformité, les considérations de performances et les notes architecturales.

Demandez tous les champs manquants avant de continuer. Ne présumez pas et ne fabriquez pas de détails.

## Phase 2 : évaluation de la maturité

Lisez `references/maturity-criteria.md` pour la rubrique complète. Attribuez l&#39;un des trois niveaux de maturité suivants :

- **Fondamentaux** `[!BADGE Foundational]{type=Neutral}` : modèles à une seule étape ou déclenchés par un événement (messagerie déclenchée par un événement, diffusion par lots), exigences simples en matière de données, IA/ML minimale, intégrations standard.
- **Émergent** `[!BADGE Emerging]{type=Informative}` : parcours à plusieurs étapes, données comportementales, modèles de recommandation, personnalisation des visiteurs connus, complexité d’intégration modérée.
- **Avancé** `[!BADGE Advanced]{type=Caution}` : prise de décision cross-canal, prédiction optimisée par l’IA, Offer Decisioning, orchestration complexe, intégrations système multiples.

### Workflow d’évaluation

1. Identifier le modèle de cas d’utilisation auquel le cas d’utilisation correspond.
2. Consultez la liste des « modèles standard » dans les critères de maturité pour une correspondance rapide.
3. Si le modèle n’indique pas clairement la maturité, évaluez la complexité des données, les exigences en matière d’IA/ML et la portée de l’intégration.
4. Présentez l&#39;évaluation à l&#39;utilisateur avec le raisonnement suivant : « Sur la base de la cartographie des motifs ({pattern}) et {key factors}, je classifierais ceci comme {level} parce que {reasoning}. »
5. Attendez que l’utilisateur confirme ou remplace avant de passer à la génération du contenu.

## Phase 3 : génération de contenu

Générer ou mettre à jour le contenu de deux fichiers.

### A. Fichier de présentation du secteur

**Chemin du fichier :** `/help/blueprints/industry-use-cases/{industry}/{industry}-overview.md`

Lisez d’abord le fichier existant pour comprendre la structure et le contenu actuels. Ajoutez ensuite une nouvelle section suivant le modèle exact de `references/use-case-template.md` :

```markdown
## {Use Case Title}

{1-2 sentence description of the business scenario and why it matters}

### Business impact

{Quantified business outcomes, e.g., "Retailers typically see a 20-30% increase in click-through rates..."}

### How to implement

Use the [{Pattern Name}](/help/blueprints/use-case-patterns/{category}/{pattern-file}.md) pattern. {1-2 sentence explanation of why this pattern applies}

### Technical considerations

- {4-8 bullet points covering data integration, regulatory, performance, or architectural considerations}
```

Placez la nouvelle section après les sections de cas d’utilisation existantes, en conservant une mise en forme cohérente.

### B. Catalogue des cas d’utilisation

**Chemin du fichier :** `/help/blueprints/industry-use-cases/use-case-catalog.md`

Lisez d’abord le fichier catalogue existant. Ajoutez une nouvelle ligne à l’onglet secteur approprié. Le catalogue utilise une structure à onglets avec des marqueurs `>[!TAB {Industry}]`. Chaque onglet contient un tableau avec les colonnes suivantes :

| Colonne | Contenu |
| --- | --- |
| Icon | `<img src="assets/use-case-icons/{industry}/icon-{kebab-name}.png" alt="{Alt Text}" width="40">` (laisser vide si aucune icône n’a encore été sélectionnée) |
| Cas d’utilisation | `[{Use Case Title}]({industry}/{industry}-overview.md#{anchor})` où anchor est le titre dans kebab-case |
| Description | Résumé en une phrase |
| Maturité | Syntaxe du badge pour le niveau attribué |
| Modèle | `[{Pattern Name}](/help/blueprints/use-case-patterns/{category}/{pattern-file}.md)` |

**Règle d’emplacement :** dans chaque onglet secteur d’activité, les lignes sont regroupées par maturité dans l’ordre suivant : Fondamental d’abord, Émergent ensuite, puis Avancé. Placez la nouvelle ligne à la fin du groupe de maturité approprié.

Les chemins d’accès aux fichiers de motifs sont les suivants :
- `audience-building-activation/audience-activation-to-destinations.md`
- `audience-building-activation/audience-collaboration-segment-match.md`
- `audience-building-activation/event-forwarding.md`
- `audience-building-activation/b2b-audience-activation.md`
- `personalization/anonymous-visitor-web-personalization.md`
- `personalization/known-visitor-web-app-personalization.md`
- `personalization/offer-decisioning.md`
- `personalization/behavioral-recommendation.md`
- `campaign-management-orchestration/batch-outbound-message-activation.md`
- `campaign-management-orchestration/event-triggered-messaging.md`
- `campaign-management-orchestration/multi-step-orchestrated-journey.md`
- `campaign-management-orchestration/cross-channel-journey-with-decisioning.md`
- `campaign-management-orchestration/buying-group-based-marketing.md`
- `analysis/customer-analytics-insight-generation.md`
- `analysis/b2b-analytics.md`
- `conversational-experience/brand-concierge-conversational-experience.md`

## Phase 4 : génération d’icônes

Une fois le contenu créé, appelez la compétence `use-case-icon-generator` pour générer une spécification d’icône pour le nouveau cas d’utilisation. Fournir à la compétence :
- Nom du cas d’utilisation
- Secteur vertical
- Brève description du cas d’utilisation

Une fois que l’utilisateur dispose du fichier d’icône généré, mettez à jour la ligne du catalogue pour inclure la référence d’icône :

```
<img src="assets/use-case-icons/{industry}/icon-{kebab-name}.png" alt="{Alt Text}" width="40">
```

## Phase 5 : validation

Avant de terminer, vérifiez tous les éléments suivants :

1. **Conformité des modèles** — La section de présentation du secteur suit exactement le modèle (en-tête ##, description, ### Impact commercial, ### Comment mettre en œuvre, ### Considérations techniques).
2. **Emplacement du catalogue** — La ligne du catalogue se trouve dans l&#39;onglet secteur approprié et dans le groupe de maturité approprié (Fondamental, puis Émergent, puis Avancé).
3. **Validité du lien de modèle** — Le lien de modèle dans la présentation et le catalogue utilise un chemin d&#39;accès au fichier de modèle valide de la liste ci-dessus.
4. **Cohérence de l’ancre** — L’ancre dans le lien du catalogue (par exemple, `#abandoned-cart-email-recovery`) correspond à l’en-tête `##` dans le fichier d’aperçu converti en kebab-case.
5. **Conventions relatives au chemin des icônes** — Le chemin des icônes suit `assets/use-case-icons/{industry}/icon-{kebab-name}.png`.

Signalez tout problème détecté lors de la validation et corrigez-le avant de terminer.
