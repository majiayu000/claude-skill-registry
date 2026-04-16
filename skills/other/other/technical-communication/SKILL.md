---
name: technical-communication
description: Technical writing, engineering specifications, reports, presentations, and documentation standards for engineering practice. Covers document types (requirements documents, test reports, design rationale, operations manuals), writing style, data visualization, engineering drawing standards, and oral presentation techniques. Use when writing engineering documents, presenting technical results, creating specifications, or learning documentation best practices.
type: skill
category: engineering
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/engineering/technical-communication/SKILL.md
superseded_by: null
---
# Technical Communication

Engineering that cannot be communicated is engineering that does not exist. The finest analysis is useless if the reader cannot follow it. The most thorough test is wasted if the report does not document what was tested, how, and what was found. Technical communication is not a soft skill appended to engineering -- it is a core engineering competency. This skill covers the full range of engineering communication: written documents, visual presentations, engineering drawings, and oral delivery.

**Agent affinity:** polya-e (pedagogical communication, scaffolded explanation), johnson-k (technical precision, NASA documentation standards)

**Concept IDs:** engr-design-communication, engr-testing-methodology, engr-data-from-experiments, engr-codes-of-ethics

## Principles of Engineering Writing

### Clarity

Engineering writing serves one purpose: to transfer technical information from the writer's mind to the reader's mind with minimum distortion. Every sentence should advance this transfer. Sentences that do not transfer information are noise.

**Bad:** "It is important to note that the utilization of advanced computational methodologies was employed in the determination of stress distribution."

**Good:** "We computed stress distribution using finite element analysis."

The good version says the same thing in half the words with double the clarity.

### Precision

Engineering writing is precise. Numbers have units. Claims have evidence. Conclusions follow from data.

**Imprecise:** "The beam was strong enough."

**Precise:** "The beam sustained a 50 kN point load at midspan with 12 mm deflection, within the L/360 serviceability limit of 14 mm."

### Structure

Engineering documents follow predictable structures because readers need to find information quickly. An engineer reviewing a test report at 2 AM during an integration crisis does not want a narrative -- they want the result in a predictable location.

### Audience Awareness

The same technical result is communicated differently to different audiences:

| Audience | What they need | How to write |
|---|---|---|
| Fellow engineers | Full technical detail, assumptions, limitations | Formal, precise, equations and data tables |
| Management | Summary, implications, decisions needed | Executive summary, key findings, recommendations |
| Regulators | Compliance evidence, traceability | Structured by regulation section, explicit requirement mapping |
| Public | What it means for them, safety implications | Plain language, analogies, no jargon |

## Document Types

### Requirements Document

**Purpose:** Define what the system must do.

**Structure:**
1. Scope and purpose
2. Applicable documents and standards
3. Requirements (numbered, each with rationale, verification method, and priority)
4. Traceability matrix (if not a separate document)
5. TBD/TBR list (items to be determined/resolved)

**Style rule:** Each requirement is a single sentence. "The system shall..." format. One requirement per numbered item. No compound requirements ("shall do A and B" -- split into two requirements).

### Test Report

**Purpose:** Document what was tested, how, and what was found.

**Structure:**
1. Test objective
2. Test article description
3. Test setup (including photographs and diagrams)
4. Instrumentation and calibration records
5. Test procedure (step-by-step)
6. Raw data
7. Data analysis
8. Results vs. requirements (pass/fail table)
9. Anomalies and observations
10. Conclusions and recommendations

**Style rule:** The reader should be able to reproduce the test from the report alone. If they cannot, the report is incomplete.

### Design Rationale Document

**Purpose:** Explain why this design was chosen.

**Structure:**
1. Problem statement
2. Alternatives considered
3. Evaluation criteria and weights
4. Trade study results (Pugh matrix or weighted scoring)
5. Selected design and rationale
6. Risks and mitigations

**Why it matters:** Design rationale documents prevent future engineers from re-fighting settled decisions. When someone asks "why did we choose a cable-stayed bridge instead of an arch?" five years later, the design rationale document provides the answer.

### Operations and Maintenance Manual

**Purpose:** How to use, maintain, troubleshoot, and repair the system.

**Structure:**
1. System description and specifications
2. Operating procedures (normal, abnormal, emergency)
3. Maintenance schedule (preventive and corrective)
4. Troubleshooting guide (symptom-cause-remedy tables)
5. Parts list and ordering information
6. Safety warnings and precautions

**Style rule:** Written for the operator, not the designer. Use the operator's vocabulary. Include illustrations. Never assume the reader has engineering background.

### Engineering Drawing

Engineering drawings are the legal definition of a part or assembly. They must conform to standards (ASME Y14.5 in the US, ISO 128 internationally).

**Key elements:**
- **Title block:** Part name, number, material, revision, approval signatures
- **Views:** Sufficient orthographic views to define the geometry completely
- **Dimensions:** All dimensions necessary for fabrication, no more
- **Tolerances:** Geometric Dimensioning and Tolerancing (GD&T) for critical features; general tolerance note for others
- **Notes:** Material specification, finish, special processes, inspection requirements

**The drawing rule:** A competent machinist with only the drawing (no verbal explanation) should be able to produce a conforming part. If they cannot, the drawing is incomplete.

## Data Visualization

### Tables vs. Figures

| Use a table when | Use a figure when |
|---|---|
| Exact values matter | Trends and patterns matter |
| Few data points | Many data points |
| Comparison across categories | Relationships between variables |
| Reference lookup | Spatial or temporal relationships |

### Figure Best Practices

1. **Label both axes** with quantity and units.
2. **Include a legend** if multiple data series are plotted.
3. **Use consistent scales.** Do not truncate axes to exaggerate trends.
4. **Title the figure** with what it shows, not what it is. "Deflection vs. Load for Specimen A" not "Figure 3."
5. **Include error bars** when data has uncertainty.
6. **Cite the source** if data is not original.

### The Tufte Principles

Edward Tufte's guidelines for data visualization:

- **Maximize the data-ink ratio.** Every drop of ink should convey data. Remove gridlines, borders, and decoration that do not serve communication.
- **Avoid chartjunk.** 3D effects, excessive color, gradient fills, and decorative elements distract from data.
- **Show the data.** Prefer scatter plots over bar charts when individual data points matter. Show distributions, not just averages.

## Oral Presentations

### Structure

| Section | Time allocation | Content |
|---|---|---|
| Introduction | 10% | Problem, scope, why it matters |
| Body | 75% | Approach, results, analysis |
| Conclusion | 10% | Key findings, recommendations, next steps |
| Q&A | 5%+ | Prepared for likely questions |

### Slide Design

- **One idea per slide.** If a slide needs a paragraph of text, it needs to be two slides.
- **Minimize text.** The slide supports your spoken words; it does not replace them.
- **Use figures.** A well-labeled diagram communicates more than a paragraph.
- **Consistent formatting.** Same font, same color scheme, same layout grid throughout.

### Delivery

- **Know your material.** Do not read slides. The slides are prompts; you are the presenter.
- **Make eye contact.** Scan the room. Do not stare at the screen.
- **Handle questions honestly.** "I don't know, but I'll find out" is always better than guessing.
- **Practice.** A dry run to a friendly audience catches structural problems and timing issues.

## NASA Technical Standards

NASA documentation standards (NPR 7120.5, NPR 7123.1) provide a reference framework for technical communication in complex systems:

- **Technical memoranda (TMs):** Formal documentation of analyses and results.
- **Technical papers (TPs):** Peer-reviewed publications.
- **Conference papers (CPs):** Presentations at professional conferences.
- **Contractor reports (CRs):** Work performed under contract.

These standards enforce structure, peer review, and traceability -- the same principles that apply to all engineering communication, formalized for the highest-stakes environment.

## Writing Process

1. **Outline first.** Structure the document before writing prose. The outline is the load-bearing structure; the prose is the cladding.
2. **Write the results section first.** You know what you found. Work backward to explain how you found it.
3. **Draft without editing.** Get the content down, then revise for clarity and precision.
4. **Review.** Have someone else read it. If they misunderstand something, the writing is at fault, not the reader.
5. **Revise.** Cut unnecessary words. Simplify sentences. Check units and calculations.

## Cross-References

- **polya-e agent:** Pedagogical communication -- adapting technical content for different learning levels.
- **johnson-k agent:** NASA documentation standards and precision in technical writing.
- **brunel agent:** Design review presentations and design rationale documentation.
- **design-process skill:** Phase 9 (Communicate) of the design cycle.
- **systems-engineering skill:** Requirements documentation and verification reports.
- **engineering-ethics skill:** Risk communication and the obligation to present data clearly and honestly.

## References

- Beer, D. F., & McMurrey, D. A. (2019). *A Guide to Writing as an Engineer*. 5th edition. Wiley.
- Tufte, E. R. (2001). *The Visual Display of Quantitative Information*. 2nd edition. Graphics Press.
- ASME. (2019). *ASME Y14.5-2018: Dimensioning and Tolerancing*. American Society of Mechanical Engineers.
- NASA. (2020). *NASA Technical Reports Server (NTRS) Style Guide*. National Aeronautics and Space Administration.
- Alley, M. (2018). *The Craft of Scientific Presentations*. 2nd edition. Springer.
- Paradis, J. G., & Zimmerman, M. L. (2002). *The MIT Guide to Science and Engineering Communication*. 2nd edition. MIT Press.
