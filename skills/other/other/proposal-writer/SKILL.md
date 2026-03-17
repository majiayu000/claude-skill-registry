---
name: proposal-writer
description: "Write technical project proposals or specific sections of proposals for research grants, technology development, and innovation projects. Use when the user asks to write, draft, or create a project proposal, grant proposal, research proposal, technical proposal, or any section thereof (e.g., abstract, objectives, methodology, work packages, budget justification, impact statement, Gantt chart). Also triggers on requests mentioning proposal-related terms like 'deliverables', 'milestones', 'work plan', 'state of the art', or 'expected outcomes'. Supports EU Horizon, NSF, TUBITAK, ERC, and generic proposal formats. Outputs via docx or pdf skills. Does NOT handle market research reports or business plans."
---

# Technical Project Proposal Writer

Write technical project proposals for research, technology development, and innovation funding calls. Produce either complete proposals or individual sections based on user request.

## Workflow

### 1. Understand Scope

Determine what the user needs:

**Full proposal?** → Follow "Full Proposal Workflow" below
**Specific section(s)?** → Follow "Section Workflow" below

Ask the user to clarify if ambiguous:
- Target funding body / call (e.g., Horizon Europe, NSF, TUBITAK, ERC, internal)
- Project topic and domain
- Consortium partners (if any)
- Duration and approximate budget
- Output format preference (docx or pdf) — default to **docx**

### 2. Research the Topic

Before writing, conduct complementary research to strengthen the proposal. Prioritize user-provided information, but augment with:

- **State of the art**: Search for recent publications from top venues (CVPR, ICCV, ECCV, ICRA, RSS, SIGGRAPH, ICML, ICLR, NeurIPS, etc.) using the `citation-management` skill
- **Competing/related projects**: Search for funded projects in the same domain
- **Technology readiness**: Identify TRL levels of relevant technologies
- **Market context**: Brief landscape if the call requires innovation/exploitation plans

Use web search and citation-management to gather reliable sources. Record key references for the bibliography.

### 3. Write Content

Follow the structure in [references/proposal_structure.md](references/proposal_structure.md) for full proposals. For individual sections, use the appropriate section guidance from that reference.

**Writing principles:**
- Be specific and quantitative — avoid vague claims
- Ground claims in citations from reputable venues
- Use active voice and direct language
- Match the tone to the funding body (EU calls: formal and structured; NSF: narrative and compelling)
- Clearly distinguish what is novel from what is state of the art
- Every objective must map to measurable deliverables
- Include risk mitigation — do not present an overly optimistic picture

### 4. Generate Output

Use the `docx` skill (default) or `pdf` skill based on user preference to produce the final document.

**Output location:** `data/output/` unless the user specifies otherwise.

**Naming convention:** `proposal_<short_topic>_<section_or_full>_<YYYYMMDD>.docx`

Example: `proposal_robot_perception_full_20260216.docx`

### 5. Self-Review Before Delivery

Before delivering the final output, perform a quick self-review using the checklist in [references/review_checklist.md](references/review_checklist.md). Fix any issues found. For a deeper review, invoke the `proposal-reviewer` skill.

---

## Full Proposal Workflow

1. Clarify scope, funding body, and format with the user
2. Research the topic (state of the art, related projects, key references)
3. Draft all sections per [references/proposal_structure.md](references/proposal_structure.md)
4. Ensure consistency across sections (objectives ↔ work packages ↔ deliverables ↔ budget)
5. Run self-review checklist
6. Generate output document

## Section Workflow

1. Identify which section(s) the user needs
2. Ask for any missing context required for that section
3. Research if the section demands it (e.g., state of the art, impact)
4. Draft the section(s)
5. Run relevant items from the review checklist
6. Generate output document

---

## Integration with Other Skills

- **docx**: Primary output format for proposals
- **pdf**: Alternative output format
- **citation-management**: Find and validate references for state-of-the-art sections
- **read-arxiv-paper**: Deep-read specific papers for literature review
- **proposal-reviewer**: Post-writing review for overpromises and legal risk

---

## Reference Files

- **[references/proposal_structure.md](references/proposal_structure.md)**: Complete section-by-section structure guide with content requirements for each section
- **[references/review_checklist.md](references/review_checklist.md)**: Quick self-review checklist to run before delivery
