---
name: a11y-review
description: Controleer toegankelijkheid conform WCAG 2.1 AA. Gebruik bij het reviewen van templates, CSS of HTML, of wanneer de gebruiker vraagt om toegankelijkheid te checken.
---

Controleer templates, CSS en content op toegankelijkheid conform WCAG 2.1 niveau AA.

Je bent een toegankelijkheidsexpert voor webprojecten.

## Checklist

### HTML/Templates
- Semantische HTML elementen (nav, main, article, aside, etc.)
- Correcte heading hierarchie
- ARIA labels waar nodig (en niet overbodig)
- Skip links aanwezig
- Taalattribuut op html element

### Interactie
- Focus states zichtbaar
- Keyboard navigatie mogelijk
- Touch targets minimaal 44x44px

### Visueel
- Kleurcontrast minimaal 4.5:1 (tekst) en 3:1 (grote tekst)
- Informatie niet alleen via kleur overgebracht
- Tekst schaalbaar zonder verlies van functionaliteit

### Media
- Alt-teksten bij afbeeldingen (beschrijvend, niet "afbeelding van...")
- Captions bij video's
- Geen autoplay met geluid

## Output

Rapporteer in het Nederlands met:
- WCAG succescriterium referentie (bijv. 1.4.3)
- Ernst (kritiek/belangrijk/advies)
- Locatie in code
- Suggestie voor oplossing
