# Project Brief: `office` Skill

**Created**: 2026-01-12
**Status**: Ready for Planning

---

## Vision

A TypeScript-first skill for generating Office documents (DOCX, XLSX, PDF) that works everywhere - Claude Code CLI, Cloudflare Workers, and browsers. Simpler and more portable than Anthropic's official skills, installable via `/plugin install office`.

## Problem/Opportunity

Anthropic published official document skills (`docx`, `xlsx`, `pdf`, `pptx`) but they're:
- **Not installable as a plugin** - requires manual setup
- **Python-heavy** - relies on openpyxl, pypdf, pandoc, LibreOffice
- **Local execution only** - can't run in Cloudflare Workers
- **Comprehensive but complex** - covers every edge case, ~500+ lines each

**Opportunity**: Create a streamlined, TypeScript-first alternative that:
- Installs with one command
- Works on edge runtimes (Cloudflare Workers)
- Covers 80% of use cases with 20% of the complexity

## Target Audience

- **Primary users**: Developers building web apps that need document exports (invoices, reports, proposals)
- **Secondary**: Claude Code users wanting to create Office docs during development
- **Scale**: Part of claude-skills marketplace (60+ skills)
- **Context**: Production skill for our marketplace

## Core Functionality (MVP)

### 1. **DOCX Generation** - Create Word documents
- Create documents with headings, paragraphs, tables, images
- Basic formatting (bold, italic, fonts, colors)
- Export to buffer/blob for download or storage
- **Library**: `docx` npm package (v9.x)

### 2. **XLSX Generation** - Create Excel spreadsheets
- Create workbooks with multiple sheets
- Cell formatting, formulas, column widths
- Export to buffer for download
- **Library**: `xlsx` (SheetJS) or `exceljs` for richer features

### 3. **PDF Generation** - Create and modify PDFs
- Create PDFs from scratch (text, images, shapes)
- Fill existing PDF forms
- Merge/split PDF documents
- **Library**: `pdf-lib` (v1.17.x)

### 4. **HTML→PDF** (Cloudflare Workers bonus)
- Convert HTML/CSS to PDF using Browser Rendering API
- Template-based document generation
- **Requires**: Cloudflare Browser Rendering binding

**Out of Scope for MVP** (defer to Phase 2):
- PowerPoint (PPTX) - adds complexity, can add later
- Tracked changes / redlining in DOCX - requires OOXML manipulation
- Formula recalculation/validation - requires LibreOffice
- OCR for scanned PDFs - requires Python/pytesseract
- Reading/parsing existing Office files (focus on creation first)

## Tech Stack (Validated)

| Component | Choice | Rationale |
|-----------|--------|-----------|
| **DOCX** | `docx` npm v9.5+ | Pure JS, Workers-compatible, well-maintained |
| **XLSX** | `xlsx` (SheetJS) v0.18+ | Pure JS, universal runtime support |
| **PDF** | `pdf-lib` v1.17+ | Explicitly supports Workers + browser |
| **HTML→PDF** | Cloudflare Browser Rendering | Native Cloudflare solution |

**Key Dependencies** (all Workers-compatible):
- `docx` - 3.4 MB unpacked, ~1.2 MB minified
- `xlsx` - 7.5 MB unpacked, ~500 KB minified
- `pdf-lib` - 19.5 MB unpacked, ~500 KB minified

## Research Findings

### Similar Solutions Reviewed

| Solution | Strengths | Weaknesses | Our Differentiation |
|----------|-----------|------------|---------------------|
| **Anthropic's official skills** | Comprehensive, battle-tested | Python-heavy, not a plugin, local only | TS-first, plugin installable, Workers-compatible |
| **tfriedel/claude-office-skills** | Packages Anthropic's approach | Incomplete, attribution concerns | Original implementation, maintained |
| **Individual npm libraries** | Work well standalone | No Claude Code integration | Skill bundles with templates + patterns |

### Technical Validation

- **`docx` in Workers**: Confirmed compatible - pure JS, uses jszip internally
- **`pdf-lib` in Workers**: Explicitly documented as supporting Cloudflare Workers
- **`xlsx` in Workers**: Pure JS algorithms, no Node dependencies
- **Browser Rendering**: [Official Cloudflare docs](https://developers.cloudflare.com/browser-rendering/how-to/pdf-generation/) show HTML→PDF pattern
- **Working example**: [worker-generate-invoice-pdf](https://github.com/adamschwartz/worker-generate-invoice-pdf)

### Known Challenges

| Challenge | Mitigation |
|-----------|------------|
| Bundle size (~2-3MB total) | Tree-shaking, lazy loading, document which deps needed |
| No formula validation in XLSX | Document limitation, recommend manual verification |
| Complex DOCX editing | Out of scope for MVP, document as limitation |
| Browser Rendering requires paid plan | Document as optional enhancement |

## Scope Validation

**Why Build This?**
- Anthropic's skills aren't conveniently installable
- No existing skill covers server-side (Workers) document generation
- High demand use case (invoices, reports, exports)

**Why This Approach?**
- TypeScript aligns with our stack (Cloudflare, React, Vite)
- Pure JS libraries enable universal runtime support
- Focused scope = maintainable, high-quality skill

**What Could Go Wrong?**
1. **Bundle size concerns** - Mitigate with clear documentation on what to import
2. **Missing features users expect** - Clear scope documentation, Phase 2 roadmap
3. **Library updates breaking things** - Pin versions, test before updating

## Estimated Effort

- **MVP**: ~4-6 hours (~4-6 minutes human time with Claude Code)
- **Breakdown**:
  - Research/templates: 1h (done in this exploration)
  - DOCX patterns + templates: 1-1.5h
  - XLSX patterns + templates: 1-1.5h
  - PDF patterns + templates: 1-1.5h
  - Workers examples: 0.5-1h
  - Testing + polish: 0.5h

## Success Criteria (MVP)

- [ ] `/plugin install office` works from claude-skills marketplace
- [ ] Can create basic DOCX with headings, paragraphs, tables
- [ ] Can create basic XLSX with data, formulas, formatting
- [ ] Can create PDF with text, images, or fill forms
- [ ] All templates work in both Node.js AND Cloudflare Workers
- [ ] Documentation includes "Use when" scenarios and examples
- [ ] Skill follows claude-skills standards (YAML frontmatter, README, etc.)

## Skill Structure

```
skills/office/
├── SKILL.md              # Main skill with patterns for all 3 formats
├── README.md             # Auto-trigger keywords
├── rules/
│   └── office.md         # Correction rules for common mistakes
├── templates/
│   ├── docx-basic.ts     # Word document template
│   ├── xlsx-basic.ts     # Excel spreadsheet template
│   ├── pdf-basic.ts      # PDF generation template
│   └── workers-pdf.ts    # Cloudflare Workers HTML→PDF example
├── references/
│   ├── docx-api.md       # Quick reference for docx npm
│   ├── xlsx-api.md       # Quick reference for SheetJS
│   └── pdf-lib-api.md    # Quick reference for pdf-lib
└── scripts/
    └── verify-deps.sh    # Check library versions
```

## Next Steps

**If proceeding**:
1. Run `/plan-project` to generate IMPLEMENTATION_PHASES.md
2. Review phases and adjust
3. Start Phase 1 (skill scaffolding)

**Phase 2 Roadmap** (after MVP):
- Add PPTX generation
- Add template system (fill placeholders in existing docs)
- Add more complex DOCX features (headers/footers, TOC)
- Consider reading/parsing existing files

---

## Research References

- [Anthropic Skills Repository](https://github.com/anthropics/skills)
- [docx npm package](https://www.npmjs.com/package/docx)
- [pdf-lib](https://pdf-lib.js.org/)
- [SheetJS (xlsx)](https://sheetjs.com/)
- [Cloudflare Browser Rendering - PDF Generation](https://developers.cloudflare.com/browser-rendering/how-to/pdf-generation/)
- [worker-generate-invoice-pdf example](https://github.com/adamschwartz/worker-generate-invoice-pdf)
- [tfriedel/claude-office-skills](https://github.com/tfriedel/claude-office-skills)
- [pdfjs-serverless for Workers](https://github.com/johannschopplich/pdfjs-serverless)
