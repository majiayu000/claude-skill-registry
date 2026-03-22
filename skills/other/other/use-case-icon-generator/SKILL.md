---
name: use-case-icon-generator
description: Générez des spécifications d’icône et des invites d’image pour les icônes de cas d’utilisation dans le référentiel de blueprints Adobe Experience Platform. Utilisez cette compétence lors de la création d’icônes pour de nouveaux cas d’utilisation du secteur, lorsque la compétence du créateur de cas d’utilisation du secteur a besoin d’une icône ou lorsque l’utilisateur demande comment créer ou mettre à jour des icônes de cas d’utilisation. Génère une invite de génération d’images détaillée que l’utilisateur peut utiliser avec les outils Midjourney, DALL-E, Adobe Firefly ou similaires, ainsi que le nom et l’emplacement corrects des fichiers.
source-git-commit: ef1c207922c1079117d8bd255dbfa32a1527b014
workflow-type: tm+mt
source-wordcount: '875'
ht-degree: 0%

---


# Générateur d’icônes de cas d’utilisation

Générez des spécifications détaillées d’icônes et des invites d’image AI pour les icônes de cas d’utilisation dans le référentiel de blueprints.

## Quand utiliser cette compétence

- Création d’un cas pratique nécessitant une icône
- Appelé par la compétence du créateur de cas d’utilisation du secteur pour générer une spécification d’icône
- L’utilisateur demande comment créer, mettre à jour ou remplacer une icône de cas d’utilisation
- L’utilisateur souhaite générer un lot d’icônes pour un nouveau secteur industriel vertical

## Étape 1 : Collecter les entrées

Rassemblez les informations suivantes auprès de l’utilisateur ou de la compétence appelante :

**Obligatoire :**
- **Nom du cas d’utilisation** — Nom lisible par l’utilisateur du cas d’utilisation (par exemple, « Panier abandonné », « Notation des leads »)
- **Secteur vertical** — L’un des secteurs suivants : automobile, b2b, services financiers, soins de santé, assurance, médias-divertissement, vente au détail, télécommunications, voyages-hébergement
- **Brève description** — 1 à 2 phrases décrivant la fonction du cas d’utilisation

**Facultatif:**
- **Métaphore visuelle préférée ou sujet préféré** — Si l&#39;utilisateur a une idée précise de ce que l&#39;icône doit représenter

Si une entrée requise est manquante, demandez à l’utilisateur avant de continuer.

## Étape 2 : lire le guide de style

Lisez le `references/icon-style-guide.md` du fichier (relatif au répertoire de cette compétence) pour charger le guide de style complet, y compris :

- Spécifications techniques
- Instructions de style visuel
- Exemples de métaphore visuelle par secteur
- Modèle d’invite
- Inventaire des icônes existantes

Utilisez le guide de style pour garantir la cohérence avec les icônes existantes.

## Étape 3 : générer la spécification de l’icône

Produisez les trois parties de la spécification de l’icône :

### A. Spécification du fichier

Déduisez le nom de fichier et le chemin d’accès à partir du nom et du secteur du cas d’utilisation :

- **Filename:** `icon-{kebab-case-name}.png`
   - Convertir le nom du cas d’utilisation en majuscules (minuscules, tirets pour les espaces)
   - Exemples : « Panier abandonné » devient `icon-abandoned-cart.png`, « Vente croisée » devient `icon-cross-sell-upsell.png`
- **Chemin:** `/help/blueprints/industry-use-cases/assets/use-case-icons/{industry}/`
- **Dimensions :** 1 024 x 1 024 pixels
- **Format :** PNG, RGB 8 bits ou RGBA
- **Taille de fichier cible :** 900KB - 1,4 Mo

### B. Invite de génération d’images

Créez une invite détaillée et prête pour la copie pour les outils de génération d’images de l’IA. L’invite doit :

1. **Décrivez une métaphore visuelle claire** — Choisissez une métaphore visuelle unique et puissante qui communique immédiatement le concept de cas d’utilisation. Si l’utilisateur ou l’utilisatrice a fourni une métaphore préférée, utilisez-la. Sinon, sélectionnez-en un en fonction des exemples du guide de style et de la description du cas d’utilisation.

2. **Spécifier le style artistique** — Inclure ces directives de style :
   - Style d’illustration d’icône moderne et épuré.
   - Esthétique professionnelle du design d&#39;entreprise
   - Formes en gras et lignes nettes
   - Finition polie et rendue (non photoréaliste)
   - Cohérent avec un système de conception unifié

3. **Inclure les spécifications techniques :**
   - Format carré, 1 024 x 1 024 pixels
   - Sujet unique centré
   - Arrière-plan de dégradé uni ou subtil
   - Contraste élevé entre le sujet et le fond

4. **Appliquer la lisibilité en petite taille :**
   - Aucun texte ni aucune lettre
   - Pas de détails fins ni de motifs complexes
   - Aucun arrière-plan complexe ni scène à plusieurs éléments
   - Silhouette en gras qui lit clairement à 40px
   - Forte reconnaissance de forme même sans couleur

5. **Guide de la palette de couleurs :**
   - Des couleurs professionnelles et adaptées à l’entreprise
   - Vibrant mais raffiné (pas de néon ou trop saturé)
   - Contraste élevé pour l’accessibilité
   - Cohérent avec d’autres icônes du même secteur vertical

Structurez l’invite en un seul paragraphe, prêt à être collé dans n’importe quel outil de génération d’images.

### C. Fragment de code de référence de catalogue

Générez le fragment de code HTML à utiliser dans la table de catalogue :

```
<img src="assets/use-case-icons/{industry}/icon-{name}.png" alt="{Alt Text}" width="40">
```

Où `{Alt Text}` est le nom du cas d’utilisation lisible.

## Étape 4 : répertorier les icônes existantes dans le même secteur d’activité

Vérifiez la section d’inventaire des icônes existantes du guide de style et répertoriez toutes les icônes actuelles du même secteur d’activité. Cela permet à l’utilisateur :
- Assurer la cohérence visuelle lors de la génération de la nouvelle icône
- Évitez de dupliquer une icône qui existe déjà
- Référencer les icônes existantes en tant qu’exemples de style

## Étape 5 : présentation de la sortie

Mettez en forme la sortie de manière claire avec les sections suivantes :

&#x200B;---

### Spécification d’icône : &lbrace;Use Case Name&rbrace;

**Industrie:** {Industry}

**Détails du fichier :**
- Nom de fichier : `icon-{kebab-case-name}.png`
- Chemin : `/help/blueprints/industry-use-cases/assets/use-case-icons/{industry}/`
- Dimensions : 1 024 x 1 024 pixels
- Format : PNG (RGB 8 bits/RGBA)

**Invite de génération d’images :**

> {L’invite complète et détaillée — formatée sous la forme d’un guillemet simple à copier}

**Catalog HTML:**

```html
<img src="assets/use-case-icons/{industry}/icon-{name}.png" alt="{Use Case Name}" width="40">
```

**Icônes existantes dans {Industry}:**
- {list of existing icon names}

**Étapes suivantes :**
1. Copiez l’invite de génération d’image ci-dessus.
2. Collez-le dans l’outil de génération d’images de votre choix (Adobe Firefly, Midjourney, DALL-E ou similaire).
3. Générez l’image et sélectionnez le meilleur résultat.
4. Redimensionnez/exportez-les exactement à 1 024 x 1 024 pixels si nécessaire.
5. Enregistrez sous `{filename}` dans le chemin indiqué ci-dessus.
6. Vérifiez que l’icône est claire et reconnaissable au format d’affichage de 40 pixels.
7. Utilisez le fragment de code HTML de catalogue lors de l’ajout de ce cas d’utilisation au tableau de catalogue.

&#x200B;---

## l’enquête

- **Ne jamais générer l’image réelle** — Cette compétence produit uniquement la spécification et l’invite. L’utilisateur doit utiliser un outil de génération d’images externe.
- **Une icône par cas d’utilisation** — Chaque cas d’utilisation reçoit exactement une icône.
- **Rechercher les doublons** — Si une icône portant le même nom ou un nom très similaire existe déjà dans l&#39;inventaire, avertissez l&#39;utilisateur.
- **Donner la priorité à la lisibilité** — En cas de doute entre une métaphore détaillée et une simple, choisissez toujours l&#39;option la plus simple qui se lit bien à 40px.
- **Soyez précis dans les invites** — Les invites vagues produisent des résultats incohérents. Inclure des détails visuels concrets (p. ex., « un panier contenant deux boîtes colorées » plutôt qu&#39;un « concept d&#39;achat »).
- **Évitez les clichés lorsque cela est possible** — Essayez de trouver des métaphores visuelles fraîches mais immédiatement reconnaissables. Une ampoule pour chaque cas d’utilisation « intelligent » devient répétitive.
