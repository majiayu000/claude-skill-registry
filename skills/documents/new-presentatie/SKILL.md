---
name: new-presentatie
description: Maak een nieuwe Reveal.js presentatie aan. Gebruik wanneer de gebruiker een nieuwe presentatie wil maken.
---

Help bij het maken van een nieuwe Reveal.js presentatie.

## Stappen

1. Vraag naar de naam van de presentatie (in kebab-case)
2. Run: `hugo new content presentaties/naam-van-presentatie`
3. Leg uit hoe de slide syntax werkt

## Slide syntax

Elke slide is een `<section>` element:

```html
<section>
  <h2>Slide titel</h2>
  <p>Inhoud van de slide</p>
</section>
```

Geneste sections maken verticale slides (navigeer met pijltje omlaag).

## Afbeeldingen

Plaats afbeeldingen in de `images/` submap van de presentatie en verwijs ernaar met:

```html
<img src="images/voorbeeld.png" alt="Beschrijving">
```

## Output

Toon het pad naar de aangemaakte presentatie en bied aan om te helpen met de eerste slides.
