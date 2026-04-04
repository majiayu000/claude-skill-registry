---
name: spec-writer
description: CSI outline specification writer — takes a materials or products list and generates structured specs with MasterFormat divisions, performance criteria, and acceptable manufacturers.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# /spec-writer — CSI Outline Specification Writer

Takes a materials list, product schedule, or project description and produces outline specifications organized by CSI MasterFormat 2020 divisions. Output is a structured `.md` file ready for review by a senior specifier.

## Input

The user provides materials/products in one of these ways:

1. **Pasted text** — a materials list, product schedule, or finish legend copied into the conversation
2. **File path** — path to a CSV, Excel export, schedule PDF, or markdown file containing materials/products
3. **Verbal description** — project type and general materials ("ground-up office with curtain wall, porcelain tile, ACT ceilings, painted gypsum board")

If the user invokes the skill without input, ask:

1. **What is the project type?** (e.g., commercial office, multifamily residential, retail, healthcare, education)
2. **What materials or products should be specified?** (paste a list, provide a file path, or describe them)

## CSI MasterFormat Divisions Covered

Map every material/product to the correct division and section number using MasterFormat 2020:

| Division | Title | Common Sections |
|----------|-------|-----------------|
| 03 | Concrete | 03 30 00 Cast-in-Place Concrete, 03 45 00 Precast Architectural Concrete |
| 04 | Masonry | 04 20 00 Unit Masonry, 04 40 00 Stone Assemblies |
| 05 | Metals | 05 12 00 Structural Steel Framing, 05 50 00 Metal Fabrications, 05 51 00 Metal Stairs |
| 06 | Wood, Plastics, and Composites | 06 10 00 Rough Carpentry, 06 20 00 Finish Carpentry, 06 40 00 Architectural Woodwork |
| 07 | Thermal and Moisture Protection | 07 21 00 Thermal Insulation, 07 27 00 Air Barriers, 07 46 00 Siding, 07 54 00 Thermoplastic Membrane Roofing, 07 84 00 Firestopping, 07 92 00 Joint Sealants |
| 08 | Openings | 08 11 00 Metal Doors and Frames, 08 14 00 Wood Doors, 08 44 00 Curtain Wall, 08 80 00 Glazing |
| 09 | Finishes | 09 21 00 Plaster and Gypsum Board, 09 30 00 Tiling, 09 51 00 Acoustical Ceilings, 09 65 00 Resilient Flooring, 09 68 00 Carpeting, 09 91 00 Painting |
| 10 | Specialties | 10 14 00 Signage, 10 21 00 Compartments and Cubicles, 10 28 00 Toilet Accessories |
| 12 | Furnishings | 12 24 00 Window Shading, 12 36 00 Countertops, 12 48 00 Rugs and Mats |
| 22 | Plumbing (fixtures only) | 22 40 00 Plumbing Fixtures |
| 26 | Electrical (fixtures only) | 26 50 00 Lighting |

If a material does not fit these divisions, assign the closest match and note the limitation.

## Spec Generation Workflow

### Step 1: Parse and classify materials

Read the user's input and build an inventory:

- **Material/product name** — as provided
- **CSI division and section number** — mapped from the material type
- **Section title** — per MasterFormat conventions

Sort by division number, then section number. Group related items under the same section where appropriate (e.g., two paint types both go under 09 91 00).

Report the mapping to the user:

```
Identified X materials across Y divisions:
- 07 92 00 Joint Sealants: silicone sealant, urethane sealant
- 09 30 00 Tiling: porcelain floor tile, ceramic wall tile
- 09 91 00 Painting: latex paint, epoxy coating
```

Ask: **"Does this mapping look correct? Any items to add or reassign?"**

### Step 2: Generate outline specifications

For each section, write a three-part outline spec following CSI SectionFormat:

#### Part 1 — General

- **1.01 Section Includes**: Scope of work covered by this section.
- **1.02 Related Sections**: Cross-references to other specification sections (e.g., "Section 07 92 00 — Joint Sealants" from a tiling section).
- **1.03 References**: Applicable standards — ASTM, ANSI, ADA, NFPA, UL, or other testing/certification standards relevant to the product. Cite specific standard numbers where known (e.g., ASTM C150 for portland cement, ASTM E84 for surface burning characteristics).
- **1.04 Submittals**: Product data sheets, samples, shop drawings, certifications, LEED/sustainability documentation as applicable.
- **1.05 Quality Assurance**: Installer qualifications, mock-up requirements (where relevant — typically for exposed finishes, masonry, curtain wall, architectural woodwork).
- **1.06 Delivery, Storage, and Handling**: Standard requirements for the product type.
- **1.07 Warranty**: Manufacturer warranty period. Use industry-standard minimums if not specified.

#### Part 2 — Products

- **2.01 Manufacturers**: List a minimum of three acceptable manufacturers with "or approved equal" language. Select manufacturers appropriate to the project type and product category. Use well-known, nationally available manufacturers.
- **2.02 Materials/Products**: Material composition, grade, class, or type. Reference applicable ASTM or industry standards.
- **2.03 Performance Criteria**: Fire rating, slip resistance (DCOF for tile), sound transmission (STC/NRC for acoustical products), thermal resistance (R-value for insulation), load capacity, or other measurable criteria relevant to the product.
- **2.04 Finishes**: Color, texture, pattern, sheen level, or surface treatment. Use "as selected by Architect from manufacturer's full range" for color selections unless the user specifies.
- **2.05 Accessories**: Ancillary items required for a complete installation (trim, adhesives, grout, fasteners, sealants).

#### Part 3 — Execution

- **3.01 Examination**: Substrate conditions to verify before installation. Moisture testing, levelness tolerances, etc.
- **3.02 Preparation**: Surface preparation, priming, layout requirements.
- **3.03 Installation**: Method of installation per manufacturer's written instructions and referenced standards. Include key installation requirements specific to the product.
- **3.04 Quality Assurance**: Field quality control — inspection, testing, tolerances.
- **3.05 Cleaning and Protection**: Post-installation cleaning, temporary protection during construction.

### Step 3: Add spec notes

Include these where relevant:

- **Substitution Procedures**: "Substitution requests shall be submitted in writing to the Architect a minimum of 10 days prior to bid date. Include product data, samples, and a point-by-point comparison with the specified product."
- **Mock-Up Requirements**: For exposed finishes (masonry, architectural woodwork, tile, curtain wall), require a mock-up panel of specified size for Architect approval before proceeding with production work.
- **Generic Spec Flags**: If a section is generic and lacks project-specific detail, append a note:

  > **[REVIEW REQUIRED]** This section contains generic outline specifications. A senior specifier shall review and supplement with project-specific requirements, local code references, and coordination with the design intent.

Apply the `[REVIEW REQUIRED]` flag when:
- No specific product or manufacturer was provided by the user
- The material is in a life-safety-related section (firestopping, fire-rated assemblies, glazing)
- Performance criteria are assumed rather than confirmed

### Step 4: Write output

Compile all sections into a single `.md` file organized by division number.

**Default output path**: `~/Documents/outline-specs-[project-slug].md`

- Derive `[project-slug]` from the project name or type provided by the user (lowercase, hyphenated — e.g., `outline-specs-brannan-office.md`)
- If no project name is given, use `outline-specs-draft.md`
- Ask the user if they want a different path

**File structure:**

```markdown
# Outline Specifications — [Project Name]

Generated: [date]
Project Type: [type]
Divisions: [count]
Sections: [count]

---

## Division 07 — Thermal and Moisture Protection

### Section 07 92 00 — Joint Sealants

#### Part 1 — General

**1.01 Section Includes**
...

#### Part 2 — Products

**2.01 Manufacturers**
...

#### Part 3 — Execution

**3.01 Examination**
...

---

## Division 09 — Finishes

### Section 09 30 00 — Tiling
...
```

### Step 5: Summary

After writing the file, report:

```
Specifications written: X sections across Y divisions
Output: [file path]
Sections flagged for review: [count]
- [list flagged sections]
```

## Writing Style

- Use specification language throughout: "shall", "provide", "verify", "submit", "conform to"
- Write in imperative mood, third person
- Do not use contractions
- Do not use first person ("we", "our")
- Capitalize "Architect", "Owner", "Contractor", "Installer" when referring to project roles
- Reference standards by full designation on first use (e.g., "ASTM C150/C150M, Standard Specification for Portland Cement"), abbreviated thereafter
- Use "approved equal" rather than "or equal"
- Measurements in imperial units unless the user specifies metric

## Edge Cases

- **Single material input**: Generate one section. Still include the full three-part structure.
- **Ambiguous materials**: Ask the user to clarify. Example: "tile" could be ceramic wall tile (09 30 00), quarry tile (09 30 00), or ceiling tile (09 51 00).
- **Materials outside covered divisions**: Note the limitation and provide the best-fit section. Example: "Elevator cab finishes are typically specified under Division 14 — Conveying Equipment, which is outside the scope of this skill. Consider coordinating with the elevator vendor."
- **Duplicate materials**: Consolidate under one section. Do not create separate sections for "latex paint — walls" and "latex paint — ceilings" — combine under 09 91 00 with both applications noted.
- **Very long lists (20+ materials)**: Process all of them. Give a progress update after every 5 sections written.
