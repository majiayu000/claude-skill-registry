---
name: epd-to-spec
description: Generate CSI-formatted specification sections requiring EPDs and setting maximum GWP thresholds — references ISO 14025, ISO 21930, EN 15804. Use when the user asks to write EPD requirements into a spec, set GWP limits, or "add embodied carbon requirements" to a specification.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - AskUserQuestion
  - mcp__google-sheets__get_sheet_data
  - mcp__google-sheets__list_sheets
---

# /epd-to-spec — EPD Specification Writer

Takes EPD data, GWP limits, or a materials list and generates CSI-formatted specification sections that require Environmental Product Declarations and set maximum Global Warming Potential thresholds. Output follows the same three-part CSI SectionFormat used by `/spec-writer`.

## Project Dossier

If `PROJECT.md` exists in the working directory, read it before fetching — the **Decisions** index may already hold GWP threshold or material choices the spec must reflect. After completing, append chosen thresholds to its **Code** section. Update values in place (the dossier holds current state, not history), every entry with a source and date. A GWP threshold is a decision — if one was set here, propose recording it with `/decision`. No `PROJECT.md`? Skip silently — or mention `/project-dossier init` if the user is clearly starting a project.

## Input

The user provides one or more of:

1. **Material list with GWP limits** — "concrete max 350 kg CO2e/m3, rebar max 1.0 kg CO2e/kg"
2. **EPD data from the sheet** — "use the EPDs I saved to set thresholds"
3. **Comparison report** — "use the lowest GWP from my last comparison as the max"
4. **LEED target** — "we're pursuing LEED v4.1 MRc2 Option 2"
5. **Verbal description** — "write EPD requirements for a ground-up office, concrete and steel structure, curtain wall"
6. **Project type** — helps determine which CSI divisions need EPD language

If the user invokes the skill without input, ask:

1. **What materials need EPD requirements?** (paste a list, reference the sheet, or describe the project)
2. **Do you have specific GWP thresholds, or should I use published industry baselines (cited with named source and publication year)?**

## CSI Divisions Where EPDs Are Most Common

Map materials to the correct division. EPD requirements are most relevant for structural, envelope, and interior finish materials:

| Division | Title | Common EPD Products |
|----------|-------|-------------------|
| 03 30 00 | Cast-in-Place Concrete | Ready-mix concrete |
| 03 40 00 | Precast Concrete | Precast panels, structural precast |
| 03 41 00 | Precast Structural Concrete | Precast beams, columns |
| 05 12 00 | Structural Steel Framing | Hot-rolled steel, HSS |
| 05 21 00 | Steel Joist Framing | Open web steel joists |
| 05 31 00 | Steel Decking | Composite floor deck, roof deck |
| 05 50 00 | Metal Fabrications | Miscellaneous metals, rebar |
| 06 10 00 | Rough Carpentry | Dimensional lumber, engineered wood |
| 06 17 00 | Shop-Fabricated Structural Wood | Glulam, CLT, LVL |
| 07 21 00 | Thermal Insulation | Mineral wool, XPS, EPS, spray foam |
| 07 27 00 | Air Barriers | Fluid-applied, sheet membranes |
| 07 42 00 | Wall Panels | Metal wall panels, ACM |
| 07 54 00 | Thermoplastic Membrane Roofing | TPO, PVC |
| 08 44 00 | Curtain Wall / Glazing | Aluminum curtain wall, IGUs |
| 09 21 00 | Plaster and Gypsum Board | Gypsum board, joint compound |
| 09 30 00 | Tiling | Porcelain, ceramic tile |
| 09 51 00 | Acoustical Ceilings | ACT, mineral fiber |
| 09 65 00 | Resilient Flooring | LVT, rubber, linoleum |
| 09 68 00 | Carpeting | Carpet tile, broadloom |
| 32 12 00 | Asphalt Paving | HMA, WMA |

## Spec Generation Workflow

### Step 1: Parse and classify materials

Read the user's input and build an inventory:

- **Material/product** — as provided
- **CSI division and section number** — mapped from the material type
- **GWP threshold** — user-provided limit, EPD sheet value, or industry baseline
- **Declared unit** — must match the unit used in the GWP threshold

If the user provided EPD sheet data or a comparison report, extract the GWP values and declared units from there.

If no GWP thresholds are specified, a published industry-average baseline may be used **only when you can cite its named source and publication year** (per the GWP Baseline Policy below) — always flag such thresholds `[VERIFY THRESHOLD]`. If no citable baseline is available, **do not use approximate from-memory numbers.** Instead, ask the user:

**"I need GWP thresholds to write the spec. You can provide them by:**
1. **Sharing an EPD** — I'll extract the GWP value and declared unit
2. **Using `/epd-research`** — I'll find EPDs for your material categories
3. **Using `/epd-compare`** — compare products and pick a threshold from the results
4. **Stating a number** — e.g., 'concrete max 350 kg CO2e/m3'

**We're working on EC3 API integration that will automate baseline lookups — for now, provide an EPD or a specific threshold."**

Do not fall back to uncited hardcoded numbers. Write the spec with `[THRESHOLD TBD]` placeholders if the user asks to proceed without data, and flag every placeholder clearly.

Report the mapping:

```
Identified X materials across Y divisions:
- 03 30 00 Cast-in-Place Concrete: GWP max 350 kg CO2e/m3 (user-provided)
- 05 12 00 Structural Steel Framing: GWP max 1.16 kg CO2e/kg (AISC Fabricated Hot-Rolled Structural Sections EPD, 2021) [VERIFY THRESHOLD]
- 07 21 00 Thermal Insulation: GWP max 1.2 kg CO2e/kg (NAIMA Mineral Wool Industry-Wide EPD, 2021) [VERIFY THRESHOLD]
```

Ask: **"Does this mapping look correct? Any thresholds to adjust?"**

### Step 2: Generate specification sections

For each material, write a three-part outline spec. The EPD-specific language is concentrated in Part 1 (submittals, quality assurance, sustainability) and Part 2 (environmental performance requirements).

#### Part 1 — General

**1.01 Section Includes**
Standard scope of work for the material. No EPD-specific changes.

**1.02 Related Sections**
Standard cross-references. Add:
- "Section 01 81 13 — Sustainable Design Requirements" (if the project has a sustainability section)

**1.03 References**
Standard material references PLUS:
- ISO 14025, Environmental labels and declarations — Type III environmental declarations — Principles and procedures
- ISO 21930, Sustainability in buildings and civil engineering works — Core rules for environmental product declarations of construction products and services (for North American EPDs)
- EN 15804+A2, Sustainability of construction works — Environmental product declarations — Core rules for the product category of construction products (for European EPDs, if applicable)
- ISO 14044, Environmental management — Life cycle assessment — Requirements and guidelines

**1.04 Submittals**
Add the following to standard submittal requirements:

```
D. Environmental Product Declarations:
   1. Submit product-specific Type III Environmental Product Declaration (EPD)
      conforming to ISO 14025 and ISO 21930.
   2. EPD shall be published by a program operator accredited per ISO 14025,
      including but not limited to: UL Environment, NSF International,
      SCS Global Services, Environdec (International EPD System), IBU, or
      ASTM International.
   3. EPD shall be current and valid at the time of submittal. Expired EPDs
      are not acceptable.
   4. EPD shall be third-party verified by an independent verifier approved
      by the program operator.
   5. Industry-average or sector EPDs are acceptable only when a product-specific
      EPD is not available for the specified product category. Submit documentation
      demonstrating unavailability.
   6. EPD shall report environmental impacts for life cycle stages A1 through A3
      (raw material supply, transport to manufacturer, manufacturing) at minimum.
```

**1.05 Quality Assurance**
Add:

```
C. Environmental Performance Verification:
   1. Manufacturer shall demonstrate that the supplied product meets the maximum
      GWP thresholds specified in Part 2.
   2. If the product is sourced from a different manufacturing plant than the one
      covered by the submitted EPD, provide documentation that the EPD is
      representative of the actual production facility.
```

**1.06 Sustainability Requirements** (new article — add if not already in the section)

```
A. Environmental Product Declaration Requirements:
   1. Provide products with Type III Environmental Product Declarations meeting
      the requirements of Article 1.04.D.
   2. Maximum Global Warming Potential (GWP):
      a. [Product]: [VALUE] kg CO2e per [DECLARED UNIT], measured for life cycle
         stages A1 through A3.
   3. GWP shall be calculated in accordance with ISO 21930 and reported using
      characterization factors from IPCC AR5 or later.

B. LEED Documentation (if applicable):
   1. Provide EPD documentation in format required for LEED v4.1 MRc2 credit
      submission.
   2. Coordinate with Owner's LEED consultant for documentation requirements.
```

**1.07 Delivery, Storage, and Handling**
Standard. No EPD-specific changes.

**1.08 Warranty**
Standard. No EPD-specific changes.

#### Part 2 — Products

**2.01 Manufacturers**
Standard manufacturer list with "or approved equal" language. Add:

```
B. All manufacturers shall provide a current, valid Type III EPD meeting the
   requirements of Article 1.04.D. Manufacturers unable to provide a conforming
   EPD are not acceptable.
```

**2.02 Materials/Products**
Standard material specifications. No EPD-specific changes.

**2.03 Environmental Performance Requirements** (new article)

```
A. Maximum Global Warming Potential (GWP):
   1. [Product]: Maximum [VALUE] kg CO2e per [DECLARED UNIT], for life cycle
      stages A1 through A3 (raw material supply, transport, manufacturing).
   2. GWP value shall be as reported in the product-specific EPD submitted
      under Article 1.04.D.

B. Additional Environmental Performance (if applicable):
   1. Recycled Content: Minimum [VALUE] percent by weight, post-consumer and
      pre-consumer combined.
   2. Regional Materials: Preference shall be given to products manufactured
      within [DISTANCE] miles of the project site.
```

**2.04 Finishes**
Standard. No EPD-specific changes.

**2.05 Accessories**
Standard. No EPD-specific changes.

#### Part 3 — Execution

Standard execution language for the material. No EPD-specific additions. Follow the same pattern as `/spec-writer`:

- 3.01 Examination
- 3.02 Preparation
- 3.03 Installation
- 3.04 Quality Assurance
- 3.05 Cleaning and Protection

### Step 3: Add LEED language (if applicable)

If the user mentions LEED v4.1, add a dedicated LEED section at the end of the specification:

```
## Appendix — LEED v4.1 MRc2: Building Product Disclosure and Optimization

### Option 1 — Environmental Product Disclosure (1 point)
Use at least 20 permanently installed products sourced from at least five different
manufacturers that have Type III EPDs conforming to ISO 14025.

Products with product-specific EPDs: 1 product = 1 product count
Products with industry-wide (generic) EPDs: 1 product = 0.5 product count

### Option 2 — Environmental Product Optimization (up to 2 points)
Products that demonstrate impact reduction below baseline:
- Products with EPDs showing impact reduction compared to industry average
  earn additional credit
- Third-party verified product-specific EPDs preferred
- Whole-building life cycle assessment (WBLCA) per ISO 14044 may be used
  as an alternative compliance path

### Documentation Requirements
1. Maintain a product EPD log tracking all qualifying products
2. For each product, document: manufacturer, product name, EPD registration
   number, program operator, GWP (A1-A3), and declared unit
3. Submit EPD log to LEED reviewer as part of MRc2 credit documentation
```

### Step 4: Add spec notes

Apply `[REVIEW REQUIRED]` flags when:

- GWP thresholds are based on industry baselines rather than project-specific targets
- The section covers life-safety materials (firestopping, fire-rated assemblies)
- Performance criteria are assumed

Apply `[VERIFY THRESHOLD]` flags when:

- GWP values are industry baselines that should be confirmed with current data
- Declared units need confirmation for the specific product being specified

### Step 5: Write output

Compile all sections into a single `.md` file organized by division number.

**Default output path**: `./epd-specs-[project-slug].md`

- Derive `[project-slug]` from the project name or type (lowercase, hyphenated)
- If no project name: `epd-specs-draft.md`
- If the user says it's final: `./deliverables/epd-specs-[project-slug].md`
- If no client context: keep it in the working directory (the default path above)
- Ask the user if they want a different path

**File structure:**

```markdown
# EPD Specifications — [Project Name]

Generated: [date]
Project Type: [type]
Divisions: [count]
Sections: [count]
LEED Target: [if applicable]

---

## Division 03 — Concrete

### Section 03 30 00 — Cast-in-Place Concrete

#### Part 1 — General
...

#### Part 2 — Products
...

#### Part 3 — Execution
...

---

## Division 05 — Metals

### Section 05 12 00 — Structural Steel Framing
...
```

### Step 6: Summary

After writing the file, report:

```
EPD specifications written: X sections across Y divisions
Output: [file path]
GWP thresholds set:
- 03 30 00 Concrete: 350 kg CO2e/m3 (user-provided)
- 05 12 00 Steel: 1.16 kg CO2e/kg (AISC Fabricated Hot-Rolled Structural Sections EPD, 2021) [VERIFY THRESHOLD]
Sections flagged for review: [count]
- [list flagged sections]
```

## Writing Style

- Use specification language throughout: "shall", "provide", "verify", "submit", "conform to"
- Write in imperative mood, third person
- Do not use contractions
- Do not use first person ("we", "our")
- Capitalize "Architect", "Owner", "Contractor", "Installer" when referring to project roles
- Reference standards by full designation on first use, abbreviated thereafter
- Use "approved equal" rather than "or equal"
- Measurements in imperial units unless the user specifies metric
- GWP values always include the unit (kg CO2e) and declared unit (per m3, per kg, per m2)

## Edge Cases

- **Single material**: Generate one section. Still include the full three-part structure.
- **No GWP threshold provided**: Use a published baseline only if you can cite named source + publication year (flag `[VERIFY THRESHOLD]`); otherwise ask the user to provide an EPD, run `/epd-research`, or state a specific threshold. If the user asks to proceed without data, use `[THRESHOLD TBD]` placeholders and flag every one.
- **Materials outside common EPD divisions**: Some materials (Division 10 specialties, Division 12 furnishings) rarely have EPDs. Note: "EPDs are uncommon for this product category. Consider requiring manufacturer environmental data sheets as an alternative submittal."
- **Mixed metric/imperial**: GWP declared units follow industry convention — concrete in kg CO2e/m3, steel in kg CO2e/kg. Don't convert these to imperial.
- **Multiple concrete mixes**: Create separate GWP thresholds per strength class (3000, 4000, 5000 PSI) if the user specifies different mixes.
- **LEED + non-LEED sections**: If some materials are for LEED credit and others aren't, include EPD submittal requirements for all but only add LEED documentation language where applicable.

## GWP Baseline Policy

This policy is shared by all four EPD skills (`epd-parser`, `epd-research`, `epd-compare`, `epd-to-spec`) and must read identically in each. Industry-average GWP baselines are allowed only when cited with a named source and publication year (e.g., "NRMCA Industry-Wide Member EPD v3.2, 2022" or "AISC Fabricated Hot-Rolled Structural Sections EPD, 2021"). Uncited baseline numbers recalled from memory or training data are banned. If no source-and-year citation is available, ask the user to provide a baseline EPD or find one with `/epd-research` — never guess a baseline.

## Notes

- **This skill generates spec language, not data.** It reads from the EPD sheet or conversation context but writes `.md` specification files.
- **Pair with `/spec-writer` for complete specs.** This skill adds EPD/sustainability requirements to specific sections. The general `/spec-writer` produces full outline specs without EPD language. For a complete specification package, use both.
- **Baselines follow the GWP Baseline Policy above.** Cited source + publication year required; uncited from-memory numbers banned. EC3 API integration is in progress and will automate baseline lookups.
- **Buy America / regional sourcing**: Some projects (federal, state-funded) require domestic materials. The regional materials preference in Part 2 can be strengthened to a requirement if needed.

## Final Step: Disclaimer + Marker (required)

This skill produces regulatory output. End every report this skill produces — printed in chat or saved to a file — with the canonical disclaimer block from `rules/professional-disclaimer.md`, followed by one blank line and the machine-readable marker, exactly as shown:

```markdown
> **Disclaimer:** This is an AI-generated analysis for preliminary planning purposes. All findings must be verified by a licensed professional before use in design, permitting, or regulatory submissions.

<!-- architecture-studio:requires-disclaimer -->
```

The marker is a single end-of-file sentinel — it appears exactly once, as the last line of the report. The `post-write-disclaimer-check` hook parses saved `.md` reports for the marker and blocks the write if the canonical disclaimer block is missing.
