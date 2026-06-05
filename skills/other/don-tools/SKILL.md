---
name: don-tools
description: "Ontwerpen en bouwen van REST APIs voor de Nederlandse overheid (design-first): OAS genereren met oas-generator, valideren met don-checker, schemakeuze uit het schema-register, codegen. Gebruik dit voor de praktische bouw-workflow."
model: sonnet
allowed-tools:
  - AskUserQuestion
  - Read
  - Bash(curl -s *)
  - Bash(npx github:developer-overheid-nl/oas-generator *)
  - Bash(npx @developer-overheid-nl/don-checker *)
  - Bash(npx @stoplight/spectral-cli *)
  - Bash(npx @redocly/cli *)
  - Bash(npx @openapitools/openapi-generator-cli *)
  - Bash(git clone *)
  - WebFetch(*)
metadata:
  source: manual
  created-with-ai: "true"
  created-with-model: claude-opus-4-7
  created-date: "2026-06-02"
---

# DON Tools

**Agent-instructie:** Deze skill bevat de praktische DON-tools voor API-ontwikkeling op [developer.overheid.nl](https://developer.overheid.nl). Bij het ontwerpen of bouwen van een REST API: volg de [API design-first werkwijze](#api-design-first-werkwijze) hieronder. Voor de normatieve regels uit de NL GOV API Design Rules (ADR) — naming, problem+json, transport security, etc. — zie de `ls-api` skill in [developer-overheid-nl/skills-standaarden](https://github.com/developer-overheid-nl/skills-standaarden).

## API design-first werkwijze

Volg de [Bouw een API-tutorial](../don-apis/references/aan-de-slag/bouw-een-api.md) (lokaal beschikbaar via de gesynchroniseerde `don-apis` kennisbank — de bron is [developer.overheid.nl](https://developer.overheid.nl/kennisbank/api-ontwikkeling/tutorials/bouw-een-api/)): eerst de OpenAPI Specification (OAS) als contract, daarna pas code. Doorloop deze flow in volgorde; gebruik `AskUserQuestion` voor elke vraag aan de gebruiker en valideer **altijd** (stap 6 en 10) voordat je een OAS oplevert. Lees de lokale referenties (zie [Bronnen](#bronnen)) voor diepere context wanneer nodig.

1. **Onderwerp & titel** — vraag waarover de API gaat en stel op basis daarvan een `title` en `description` voor.
2. **Contactgegevens** — vraag `name`, `email` en `url`. Dit moet het **beheerteam** zijn, nooit een individu (wisselt van rol) of een algemene helpdesk (`info@…`); gebruik als `url` bij voorkeur een **issuetracker** waar consumenten problemen kunnen melden, niet een homepage. Stuur de gebruiker hier actief op bij twijfel. (Normatieve regel: [`/core/doc-openapi-contact`](../don-apis/references/api-design-rules/hoe-te-voldoen/doc-openapi-contact.md).)
3. **Resources** — vraag welke resources de API bevat. Bepaal per resource:
   1. **`readonly` of niet** — `readonly: true` genereert enkel `GET`; anders ook `POST` (collectie) en `PUT`/`DELETE` (item).
   2. **Naam** — bepaal zelf enkelvoud (`name`) en meervoud (`plural`) op basis van de input.
   3. **Schema** — zoek eerst in het schema-register (zie [Schema's kiezen uit het register](#schemas-kiezen-uit-het-register)) en **leg de treffers ALTIJD ter keuze voor aan de gebruiker via `AskUserQuestion`**. Kies nooit zelf zonder bevestiging; voeg ook altijd een optie *"Zelf een schema voorstellen"* toe. Bied aan een voorbeeld te tonen, desnoods via de register-link in de console.
4. **Bevestig de `input.json`** — toon de samengestelde input en laat de gebruiker bevestigen vóór je genereert.
5. **Genereer de OAS** (CLI; de [web-tool](https://developer-overheid-nl.github.io/oas-generator) is het handmatige alternatief):

   ```bash
   npx github:developer-overheid-nl/oas-generator input.json -o openapi.json
   ```

6. **Valideer de OAS** met de DON Checker (zie [OAS valideren](#oas-valideren)):

   ```bash
   npx @developer-overheid-nl/don-checker@latest validate --ruleset adr-21 --input openapi.json
   ```

7. **Server-URL invullen** — de boilerplate bevat een `@TODO`-server-URL, dus stap 6 faalt sowieso op `include-major-version-in-uri`. Vraag de gebruiker om de server-URL **mét major versie** (bijv. `https://api.example.com/v1`) en zet die in `servers`. Geen URL? Default dan naar `http://localhost:8080/v1` — validatie is dan schoon op één `servers-use-https`-waarschuwing na (acceptabel voor lokale ontwikkeling).
8. **Extra functionaliteit** — vraag per operatie naar extra functionaliteit zoals filtering en zoeken. Query- en padparameters zijn **altijd lowerCamelCase**, óók in de OAS (bijv. `?sorteerOp=naam`, niet `?sorteer_op`).
9. **Voeg de functionaliteit toe** aan de OAS (parameters, query's, schema's). Hergebruik standaard headers/foutresponses via externe `$ref`s naar `https://static.developer.overheid.nl/adr/components.yaml` — zie de [`ls-api` Standaardcomponenten-sectie](https://github.com/developer-overheid-nl/skills-standaarden/blob/main/skills/ls-api/SKILL.md#standaardcomponenten-hergebruiken) voor het patroon.
10. **Valideer opnieuw** (herhaal stap 6) tot er geen errors meer zijn; documenteer bewuste afwijkingen.
11. **Oplevering & vervolg** — toon de definitieve OAS en stel een vervolgstap voor: opslaan en bekijken in [editor.swagger.io](https://editor.swagger.io), of doorgaan met servercode-generatie (zie [Code genereren](#code-genereren)).

> **ALTIJD valideren:** elke OAS die je genereert of wijzigt MOET stap 6/10 doorlopen vóórdat je hem aan de gebruiker presenteert.

## Schema's kiezen uit het register

In **OAS 3.1** kun je per resource direct een JSON Schema koppelen via het `schema`-veld in de generator-input (alleen toegestaan bij `oasVersion: "3.1"`). Bepaal per resource een schema en **laat de gebruiker ALTIJD zelf kiezen** — sla deze stap niet over en pak nooit autonoom een schema:

1. **Zoek in het DON-schema-register** op een trefwoord uit de resource-naam/context:

   ```bash
   curl -s 'https://schemas.don.projects.digilab.network/self/v1/api/schemas/search?q=adres'
   # → [{ "path": "/api-register/.../adresuitgebreid", "title": "AdresUitgebreid", "description": "..." }, ...]
   ```

2. **Leg de treffers ALTIJD ter keuze voor** met `AskUserQuestion` — kies nooit zelf zonder de gebruiker hierin te laten beslissen. Maak per treffer een optie met de `title` als label en de `description` als toelichting, plus altijd een optie **"Zelf een schema voorstellen"**. (Max 4 opties per vraag — toon de relevantste treffers; via "Other" kan de gebruiker een specifiek schema benoemen.) Vind je geen treffers? Vraag dan eerst aan de gebruiker of die zelf een schema wil voorstellen of een ander zoektrefwoord wil proberen.
3. **Verwerk de keuze:**
   - **Bestaand schema** → gebruik de resolvebare URL `https://schemas.don.projects.digilab.network{path}` als waarde van het `schema`-veld (externe verwijzing, JSON Schema draft 2020-12). Bladeren kan ook in de [register-UI](https://schemas.don.projects.digilab.network).
   - **Zelf voorstellen** → stel op basis van de resource-naam en context een **human-readable** inline JSON Schema-object voor en bevestig het bij de gebruiker.

Voorbeeld-input voor de generator met beide varianten (URL-schema én inline schema):

```json
{
  "oasVersion": "3.1",
  "title": "Bier API",
  "description": "API voor het beheren van bieren en adressen van brouwerijen.",
  "contact": { "name": "API Team", "email": "api@example.com", "url": "https://github.com/example/api/issues" },
  "resources": [
    {
      "name": "adres",
      "plural": "adressen",
      "readonly": true,
      "schema": "https://schemas.don.projects.digilab.network/api-register/dienst-voor-het-kadaster-en-de-openbare-registers/imbag-api-van-de-lvbag-7fnzbuehg/adresuitgebreid"
    },
    {
      "name": "bier",
      "plural": "bieren",
      "schema": {
        "type": "object",
        "properties": {
          "naam": { "type": "string" },
          "stijl": { "type": "string" },
          "alcoholpercentage": { "type": "number" }
        },
        "required": ["naam"]
      }
    }
  ]
}
```

`adres` is hier alleen-lezen (`readonly: true` → enkel `GET`); `bier` krijgt de volledige set operaties (`GET`/`POST` op de collectie, `GET`/`PUT`/`DELETE` op het item). Een URL-schema wordt direct met een `$ref` aangehaald; een inline schema komt onder `components/schemas` te staan en wordt lokaal gerefereerd.

## OAS valideren

Valideer elke OpenAPI-spec tegen de ADR met de **DON Checker**. De online [OAS Checker](https://developer-overheid-nl.github.io/oas-checker) gebruikt dezelfde ruleset; onder de motorkap draait de Spectral ADR-ruleset.

```bash
# Aanbevolen: DON Checker (lokaal/CI); --input accepteert een bestandspad of URL
npx @developer-overheid-nl/don-checker@latest validate \
  --ruleset adr-21 \
  --input ./openapi.json

# Voorbeeld tegen een live spec
npx @developer-overheid-nl/don-checker@latest validate \
  --ruleset adr-21 \
  --input https://api.developer.overheid.nl/api-register/v1/openapi.json
```

### Alternatief: Spectral CLI direct

Wanneer je de ruleset zelf wilt inspecteren of een specifieke variant wilt draaien:

```bash
npx @stoplight/spectral-cli lint <jouw-spec.yaml> \
  --ruleset https://static.developer.overheid.nl/adr/ruleset.yaml
```

Voor het overzicht van regels (DON-versie: 11 regels; GitHub-versie: 22 regels) zie de `ls-api` skill in [skills-standaarden](https://github.com/developer-overheid-nl/skills-standaarden/blob/main/skills/ls-api/SKILL.md#oas-valideren).

## Code genereren

Optionele vervolgstap (flow-stap 11) na een goedgekeurde OAS: bundel de spec en genereer een server uit de officiële templates.

```bash
npx @redocly/cli bundle ./openapi.json --output openapi.bundled.json --ext json
git clone https://github.com/developer-overheid-nl/codegen-templates.git
npx @openapitools/openapi-generator-cli generate \
  -i ./openapi.bundled.json -g nodejs-express-server \
  -o ./api -t ./codegen-templates/nodejs-express-server
```

Vereist Node.js 22+ en Java 11+. Start een mock met `npm install && npm run start-mock`.

## Bronnen

De relevante kennisbank-content uit [developer.overheid.nl](https://developer.overheid.nl) staat al lokaal als gesynchroniseerde markdown in de `don-apis` skill. Gebruik deze lokale bronnen i.p.v. online links wanneer je extra context nodig hebt — ze worden bijgewerkt via `scripts/sync.py`:

- [Aan de slag → Bouw een API](../don-apis/references/aan-de-slag/bouw-een-api.md) — de tutorial die deze flow operationaliseert
- [Aan de slag → Maak een OAS](../don-apis/references/aan-de-slag/maak-een-oas.md) — OAS-basis
- [API Design Rules → Linter](../don-apis/references/api-design-rules/api-design-rules-linter.md) — Spectral-ruleset details
- [API Design Rules → Validator](../don-apis/references/api-design-rules/api-design-rules-validator.md) — DON Checker / OAS Checker
- [API Design Rules → Cheat sheet](../don-apis/references/api-design-rules/cheat-sheet.md) — compacte regel-overzicht
- [API Design Rules → `/core/doc-openapi-contact`](../don-apis/references/api-design-rules/hoe-te-voldoen/doc-openapi-contact.md) — contactinformatie-eis

Voor de **normatieve samenvatting** van de NL GOV API Design Rules (ADR) — naming, problem+json, transport security, signing, encryption, geo — zie de `ls-api` skill in [developer-overheid-nl/skills-standaarden](https://github.com/developer-overheid-nl/skills-standaarden) (andere plugin).
