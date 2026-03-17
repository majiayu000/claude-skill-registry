---
name: auction-catalog
description: Reference guide for Swedish auction cataloging conventions and Auctionet FAQ compliance. Use when working on title formatting, description rules, condition reports, or quality validation logic.
argument-hint: [category or topic]
---

# Auction Cataloging Reference

Use this skill to look up or apply correct cataloging conventions when modifying quality rules, AI prompts, or validation logic in the extension.

If an argument is provided, focus on that category or topic: `$ARGUMENTS`

## Title Formatting Rules (by category)

### Furniture (Möbler)
```
BYRÅ, gustaviansk, sent 1700-tal.
FÅTÖLJ, "Karin", Bruno Mathsson, Dux.
```
- NEVER include wood type in title (put in description)
- Include: style, period, designer if known
- Signed furniture: include maker in title

### Small Items (Småsaker)
```
VAS, majolika, nyrenässans, Gustafsberg, sent 1800-tal.
SKÅL, glas, Bertil Vallien, Kosta Boda, sign.
```
- NEVER combine material+object ("MAJOLIKAVAS" is WRONG → "VAS, majolika")
- NEVER "KERAMIKTOMTE" → "TOMTE, keramik"

### Services (Serviser)
```
MATSERVIS, 89 delar, porslin, "Maria Björnbär", Rosenthal.
MAT- OCH KAFFESERVIS, 38 delar, flintgods, rokokostil, Rörstrand, tidigt 1900-tal.
```
- Always: type, piece count, material, pattern name, manufacturer, period

### Rugs (Mattor)
```
MATTA, orientalisk, semiantik, ca 320 x 230 cm.
```
- Dimensions ALWAYS in title (exception to normal rule)
- Priority category at intake — catalog fully at intake

### Silver
```
BÄGARE, 2 st, silver, rokokostil, CG Hallberg, Stockholm, 1942-56, ca 450 gram.
```
- Always research hallmarks
- Weight always LAST in title
- No weight for filled-base items (candelabras with weighted base)

### Art (Konst)
```
BENGT LINDSTRÖM, färglitografier, 2 st, signerade och daterade 76 och numrerade 120/310.
BRUNO LILJEFORS, "Enkelbeckasin i höstskog", olja på duk, signerad B.L och daterad -28.
```
- Artist name in artist field (auto-prepended in UPPERCASE)
- Quoted titles ONLY for artist-given titles
- Write signatures/dates exactly as on the work: distinguish "1832" vs "-32" vs "32"
- "sign. a tergo" for reverse signatures
- Piece count after technique, not after artist
- "Ej sign." in description for unsigned works

### Unidentified Artist
```
OIDENTIFIERAD KONSTNÄR, Rådjur, skulptur, brons, otydligt signerad, 18/1900-tal.
```
- Use when signature is clear but artist cannot be identified
- Always take a detail photo of the signature
- Droit de suite still applies

## Description Rules

### General
- Be thorough — especially things hard to see in photos
- Write out full words, no abbreviations (for Google SEO)
- Always include: creator, material, manufacturer, measurements, weight (where applicable)
- Provenance, exhibitions, literature: write before measurements

### Measurements
- Format: `Höjd 84, bredd 47 cm` or `Längd 84, bredd 47, höjd 92 cm`
- Art: `45 x 78 cm` (height × width, without frame)
- Always last in description (except rugs/ceiling lamps → in title)
- Use "ca" for approximate measurements
- Graphics: clarify "bladstorlek" vs "bildstorlek"
- Rings: only ring size, no measurements

### Services Description
- No measurements needed
- List all pieces: `34 mattallrikar, 25 djupa tallrikar, såsskål samt tillbringare`
- Single items NOT preceded by "1" — just name them
- No "st" after single items

## Condition Report Rules

### Dos
- Be thorough when possible, vague when necessary
- Always use "Ej examinerad ur ram" for framed art
- Always mention engravings/monograms on silver
- Use "Ej genomgånget" for books and similar
- Always photograph visible damage

### Don'ts
- NEVER use "bruksslitage" as standalone condition — specify damage type
- NEVER use "Ej funktionstestad" — implies we test items
- AVOID "Ingen anmärkning" — leads to complaints
- NEVER comment on frame condition (unless the frame IS the item)
- Avoid abbreviations: mm, bl a, osv
- Paintings don't have "bruksslitage" — they're not "used"

### Preferred Specific Terms
| Instead of "Bruksslitage" | Use |
|---------------------------|-----|
| Furniture | Smärre ytslitage, repor, märken, fläckar, ringmärken |
| Glass/Ceramics | Smärre nagg, ytslitage, hårspricka |
| Textiles/Rugs | Slitage fransar, fläckar, färgförändringar |
| Paintings | Sedvanligt slitage, ramslitage, krakelyrer |
| Silver | Bucklor, repor, lagningar, monogram |

## Forbidden Language
Never use subjective/selling language:
`fin, vacker, värdefull, stor, elegant, karakteristisk, typisk, klassisk, traditionell, autentisk, raffinerad, stilren, harmonisk, genomarbetad, påkostad, exklusiv, förnäm, gedigen, kvalitativ, förstklassig, exemplarisk, representativ`

## Photography Guidelines
- Minimum 3 photos per item
- Always: front, back, important details
- Specific: stamps, signatures, damages, maker marks
- Silver/gold: always show hallmarks
- Art: signature detail + back of frame for older works
- Rugs: full view + corner + back
