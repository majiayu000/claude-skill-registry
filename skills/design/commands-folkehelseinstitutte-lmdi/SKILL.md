---
name: commands
description: Generer en komplett SKILL.md dokumentasjon fra denne FHIR Implementation
  Guide.
---

# Generate FHIR Profile Skill

Generer en komplett SKILL.md dokumentasjon fra denne FHIR Implementation Guide.

## Instruksjoner

### 1. Finn og les alle FSH-filer

Les alle `.fsh`-filer fra `LMDI/input/fsh/` med undermapper:
- `LMDI/input/fsh/aliases.fsh`
- `LMDI/input/fsh/profiles/*.fsh`
- `LMDI/input/fsh/extensions/*.fsh`
- `LMDI/input/fsh/valuesets/*.fsh`
- `LMDI/input/fsh/namingsystems/*.fsh`
- `LMDI/input/fsh/examples/*.fsh` (for referanse, men ikke inkluder i skill)

### 2. For hver fil, ekstraher og dokumenter

**Profiles** - Ekstraher:
- Navn, Id, Title, Description
- Parent (base-ressurs)
- Alle rules: kardinalitet, must-support, fixed values, bindings
- Slicing-definisjoner med discriminator
- Invariant-referanser

**Extensions** - Ekstraher:
- Navn, Id, URL, Title, Description
- Context (hvor den kan brukes)
- Value[x] type og constraints

**ValueSets** - Ekstraher:
- Navn, Id, URL, Title, Description
- Alle inkluderte koder med system og display

**NamingSystems** - Ekstraher:
- Navn, uniqueId verdier

**Aliases** - Inkluder alle aliases for referanse

### 3. Hent FHIR R4 base-ressurs kontekst

For hver Profile, slå opp base-ressursen på `https://hl7.org/fhir/R4/[resourcetype].html` og inkluder:
- Alle elementer som profilen refererer til
- Elementer med kardinalitet 1..* i base som ikke er eksplisitt nevnt
- Datatyper for hvert element

### 4. Generer SKILL.md

Lag filen med denne strukturen:

```markdown
---
name: lmdi-fhir-profiles
description: Komplett dokumentasjon for LMDI (Legemiddelregisteret Data Inn) FHIR Implementation Guide. Bruk denne når du skal svare på spørsmål om LMDI-profiler, extensions, valuesets, kardinaliteter, constraints, slicing, eller andre detaljer i LMDI FHIR-profilene. Dekker MedicationAdministration, Medication, Patient, Encounter, Condition, Organization, Practitioner, Substance og tilhørende extensions.
---

# LMDI FHIR Implementation Guide

## Oversikt
[Beskriv formålet med LMDI - innrapportering av legemiddeldata til Legemiddelregisteret]

## Aliases
[List opp alle aliases fra aliases.fsh for referanse]

---

## Profiler

### [ProfilNavn]
- **Id**: `[id]`
- **Base**: [FHIR R4 ressurs med lenke]
- **Title**: [title]
- **Description**: [description]

#### Elementer

| Element | Kard. | Type | MS | Binding/Fixed | Beskrivelse |
|---------|-------|------|-----|---------------|-------------|
| [path] | [0..1] | [type] | ✓/- | [valueset/fixed] | [kort beskrivelse] |

#### Slicing
[Hvis profilen har slicing, dokumenter:
- Element som slices
- Discriminator type og path
- Slice-navn og regler for hver slice]

#### Constraints/Invarianter
[List invarianter som gjelder denne profilen]

---

## Extensions

### [ExtensionNavn]
- **Id**: `[id]`
- **URL**: `[canonical url]`
- **Context**: [ressurs.element hvor den kan brukes]
- **Type**: [value[x] datatype]
- **Description**: [beskrivelse]

---

## ValueSets

### [ValueSetNavn]
- **Id**: `[id]`
- **URL**: `[canonical url]`

| System | Code | Display |
|--------|------|---------|
| [system] | `[code]` | [display] |

---

## NamingSystems

### [Navn]
- **UniqueId**: `[oid/uri]`
- **Type**: [oid/uri]

---

## Relasjoner

[Beskriv hvordan ressursene henger sammen:
- MedicationAdministration -> Medication (reference)
- MedicationAdministration -> Patient (subject)
- MedicationAdministration -> Encounter (context)
- osv.]
```

### 5. Lagre output

Lagre til: `~/.claude/skills/lmdi-fhir/SKILL.md`

Opprett mappen hvis den ikke finnes:
```bash
mkdir -p ~/.claude/skills/lmdi-fhir
```

På Windows tilsvarer `~` brukerens hjemmemappe, typisk `C:\Users\[brukernavn]`.

### 6. Bekreft og vis opplastingsinstruksjoner

Fortell brukeren at skillen er generert og klar til bruk i alle Claude Code-prosjekter.

Vis deretter følgende instruksjoner for opplasting til Claude.ai:

---

**Skillen er nå tilgjengelig i Claude Code / VS Code extension.**

Hvis du også vil bruke den i Claude.ai (web/app), gjør følgende:

1. **Åpne Claude.ai** i nettleseren (claude.ai)

2. **Start en ny samtale** og skriv:
   ```
   Jeg vil laste opp en SKILL.md fil til /mnt/skills/user/lmdi-fhir/
   ```

3. **Last opp filen** ved å dra `SKILL.md` inn i chat-vinduet, eller klikk på 📎 og velg filen fra:
   ```
   C:\Users\[ditt-brukernavn]\.claude\skills\lmdi-fhir\SKILL.md
   ```

4. **Be Claude lagre den**:
   ```
   Lagre denne filen til /mnt/skills/user/lmdi-fhir/SKILL.md
   ```

5. **Verifiser** ved å spørre:
   ```
   Kan du lese /mnt/skills/user/lmdi-fhir/SKILL.md og bekrefte at den er lagret?
   ```

Etter dette vil LMDI FHIR-skillen være tilgjengelig både i Claude Code og i Claude.ai/appen.

---

## Viktig

- Vær KOMPLETT - ta med alle detaljer
- Behold norske beskrivelser
- Inkluder alle koder i valuesets (ikke forkort)
- Marker tydelig hva som er must-support
- Dokumenter alle slicing-regler nøyaktig