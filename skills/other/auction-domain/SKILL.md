---
name: auction-domain
description: Background knowledge about online auctions, Swedish auction cataloging conventions, Auctionet platform rules, and auction house terminology. Use this context whenever working on code that handles item cataloging, condition reports, titles, descriptions, artist fields, valuations, or market analysis.
user-invocable: false
---

# Auctionet Auction Domain Knowledge

This codebase is a Chrome extension for **Auctionet** — Sweden's leading online auction platform with 3.65M+ historical auction results across 60+ auction houses. The extension augments the admin cataloging interface with AI assistance.

## Swedish Auction Cataloging Conventions

### Title Structure (by category)
- **Furniture**: `BYRÅ, gustaviansk, sent 1700-tal.` — NEVER include wood type in title
- **Small items**: `VAS, majolika, nyrenässans, Gustafsberg, sent 1800-tal.` — never "MAJOLIKAVAS", always separate material
- **Services**: `MATSERVIS, 89 delar, porslin, "Maria Björnbär", Rosenthal.`
- **Rugs**: `MATTA, orientalisk, semiantik, ca 320 x 230 cm.` — dimensions ALWAYS in title
- **Silver**: `BÄGARE, 2 st, silver, CG Hallberg, Stockholm, 1942, ca 450 gram.` — weight last in title
- **Art**: `OIDENTIFIERAD KONSTNÄR, Rådjur, skulptur, brons, otydligt signerad, 18/1900-tal.`
- **Art (known artist)**: Artist name goes in the dedicated artist field (auto-prepended to title in UPPERCASE). Title contains: motif description, technique, signed/dated info.

### Key Rules
- Object type in UPPERCASE at start of title
- Artist names: `Förnamn Efternamn` in the artist field, displayed UPPERCASE
- "Oidentifierad konstnär" for signed but unidentified artists
- Measurements: `Höjd 84, bredd 47 cm` or `45 x 78 cm` for art (height first, without frame)
- Never use abbreviations — full words for Google SEO ("nysilver" not "NS", "Josef Frank" not "Frank")
- No subjective words: "fin", "vacker", "värdefull", "stor" are forbidden
- Condition terms: avoid vague "bruksslitage" / "bruksskick" — specify actual damage type
- Art titles in quotes ONLY if given by the artist themselves
- "Ej examinerad ur ram" — standard phrase for framed art not examined out of frame
- Never say "Ej funktionstestad" — implies we test items
- Avoid "Ingen anmärkning" — leads to complaints

### Condition Field Quality Problem
31.7% of Auctionet listings use vague condition language. The extension's quality analyzer flags these and suggests specific alternatives:
- Furniture: `Smärre ytslitage`, `Repor`, `Märken`, `Fläckar`, `Ringmärken`
- Glass/Ceramics: `Smärre nagg`, `Ytslitage`, `Hårspricka`
- Textiles: `Slitage fransar`, `Fläckar`, `Färgförändringar`

### Auctionet Platform Specifics
- Items are published by Auctionet staff after cataloging by auction houses
- Auction duration: ~10 days (configurable)
- Minimum reserve: 400 SEK
- Standard reserve: 60–80% of estimate
- Items re-listed automatically up to 3 times before manual intervention
- Transport cataloging: box size, number of parts, fragility rating
- Droit de suite (Följerätt) applies to identified and unidentified artists

### Anti-Hallucination Rules
The extension enforces strict rules to prevent AI-invented information:
- NEVER fabricate artist dates, materials, or dimensions
- NEVER add historical context not explicitly in source data
- NEVER replace specific condition terms with vaguer ones
- Temperature kept low (0.15) for corrections, not creative rewriting
- Category-specific extra caution for: weapons/militaria, jewelry, historical items, watches

### Swedish Auction Terminology
| Swedish | English | Context |
|---------|---------|---------|
| Bruksslitage | General wear | VAGUE — flag for specifics |
| Bruksskick | Used condition | VAGUE — flag for specifics |
| Smärre nagg | Minor chips | Glass/ceramics |
| Hårspricka | Hairline crack | Ceramics |
| Lagning | Repair | General |
| Signerad | Signed | Art |
| A tergo | On the reverse | Art signatures |
| Ej sign. | Not signed | Art |
| Fanerad | Veneered | Furniture |
| Intarsia | Inlay work | Furniture |
| Beslag | Fittings/mounts | Metal hardware |
| Proveniens | Provenance | Ownership history |
| Utropspris | Reserve price | Minimum bid |
| Bevakningspris | Watch price | Seller's reserve |
| Klubbat pris | Hammer price | Final sale price |
| Köpare | Buyer | Customer type |
| Säljare | Seller | Customer type |
| Föremål | Item/object | Auction lot |
| Reklamation | Complaint/claim | Customer dispute |
| Ångerrätt | Right of withdrawal | Consumer right |
| Snabbkatalogisering | Quick cataloging | Extension feature |
| Flytta | Move (artist name) | Extension action |

### Auctionet API
- Public API: `https://auctionet.com/api/v2/items.json`
- Search: `https://auctionet.com/sv/search`
- Artists: `https://auctionet.com/sv/artists`
- Image CDN: `https://images.auctionet.com/`
