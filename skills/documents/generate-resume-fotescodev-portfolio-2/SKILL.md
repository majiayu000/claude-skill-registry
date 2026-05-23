---
name: generate-resume
description: Generate a print-optimized, ATS-friendly single-page resume PDF from portfolio content. Use when user wants to create or regenerate their resume. (project)
---

# Resume Generator

<purpose>
Generate a single-page PDF resume using Puppeteer to render the `/resume` React page. Optimized for ATS (Applicant Tracking Systems) and print.
</purpose>

<when_to_activate>
Activate when the user:
- Asks to generate, create, or update their resume
- Says "create my resume", "make a resume", "export resume PDF"
- Wants to refresh the resume after updating portfolio content
- Asks about resume format or PDF generation

**Trigger phrases:** "resume", "generate resume", "PDF", "export resume", "make resume"
</when_to_activate>

## Critical Files

| File | Purpose |
|------|---------|
| `src/pages/ResumePage.tsx` | React component for print-optimized layout |
| `src/pages/ResumePage.css` | Print/screen styles with theme isolation |
| `scripts/generate-resume.ts` | Puppeteer PDF generation script |
| `content/profile.yaml` | Name, email, location, tagline, stats |
| `content/experience/index.yaml` | Jobs with highlights |
| `content/skills/index.yaml` | Categorized skills |
| `public/resume.pdf` | Default output file |

---

## Design Principles

### 1. Never Cut Experience

**Critical:** Include ALL jobs from `content/experience/index.yaml`. Missing experience (especially major companies) damages credibility more than a slightly longer resume.

- If page is too long → reduce highlights per job, NOT number of jobs
- Set `MAX_JOBS` to match total jobs in experience file
- Every role adds signal; cutting roles removes career trajectory

### 2. Metrics Over Descriptions

Highlights should follow **Action → Outcome** format with quantified results:

```
❌ "Managed product development"
✅ "Shipped Advanced API from 0→1: 17 methods serving 1M+ daily requests"
```

### 3. ATS-First Design

- Plain text (no images, icons, or complex layouts)
- Standard fonts: Georgia, Times New Roman (serif) or Arial, Helvetica (sans)
- Clear section headers: Header, Summary, Experience, Skills
- All text must be selectable/copyable

### 4. Single Page Target

One-page resumes get 2x more callbacks. Fit content by:
1. Reducing highlights per job (2-3 is sufficient)
2. Tightening typography (9-10pt base)
3. Never by cutting jobs

---

## Format Guidelines

### Layout Constants (ResumePage.tsx)

```typescript
const RESUME_CONFIG = {
  SUMMARY_SKILL_CATEGORIES: 2,   // Categories in impact summary
  SKILLS_PER_CATEGORY: 3,        // Skills per category in summary
  SUMMARY_COMPANIES: 4,          // Companies to list in summary
  MAX_JOBS: 6,                   // Include ALL jobs - adjust to match your experience
  MAX_HIGHLIGHTS_PER_JOB: 3,     // Bullets per job (action → outcome format)
};
```

**Adjust `MAX_JOBS` to match the total number of jobs in your experience file.**

### Resume Structure

1. **Header**: Name / Current Role + contact info (email, location)
2. **Impact Summary**: One-liner tagline + top skills + notable companies + key stats
3. **Professional Experience**: Each job with company, role, period, location, and bullets
4. **Skills**: 2-column grid organized by category

### Skills Section Layout

Skills are displayed in a **2-column grid** with category names in bold:

```
Category A: skill1, skill2, skill3...    | Category B: skill1, skill2...
Category C: skill1, skill2, skill3...    | Category D: skill1, skill2...
```

Categories are pulled from `content/skills/index.yaml`. Common category structures:

**For Engineers:**
- Languages & Frameworks, Infrastructure, Databases, Tools

**For Product Managers:**
- Domain Expertise, Product Leadership, Technical Execution, Tools

**For Designers:**
- Design Tools, Research Methods, Platforms, Collaboration

### Typography (ResumePage.css)

- **Font**: Georgia / Times New Roman (ATS-safe serif)
- **Base size**: 9.5pt
- **Line height**: 1.35
- **Page**: Letter size (8.5in × 11in)
- **Margins**: 0.4in top/bottom, 0.5in left/right

---

## Known Issues & Fixes

### 1. Black Box at Bottom of PDF

**Cause:** ThemeProvider applies dark background (#08080a) to body/#root, which bleeds into the PDF outside the `.resume-page` container.

**Fix:** CSS must override parent elements in `@media print`:

```css
@media print {
  html,
  body,
  #root {
    background: white !important;
    min-height: auto !important;
    padding: 0 !important;
    margin: 0 !important;
  }
}
```

### 2. PDF Exceeds One Page

**Fix:** Reduce `MAX_HIGHLIGHTS_PER_JOB` in ResumePage.tsx. **Do NOT reduce MAX_JOBS** - missing experience is worse than a slightly longer resume.

### 3. Missing Experience/Jobs

**Cause:** `MAX_JOBS` was set too low, cutting off important companies.

**Fix:** Always set `MAX_JOBS` to the total number of jobs in `content/experience/index.yaml`. Count your jobs and update the config.

### 4. Yellow/Colored Underline on Role Title

**Fix:** Ensure `.resume-role-highlight` has no border-bottom or background-color.

### 5. Theme Colors Bleeding Through

**Fix:** Reset all children with:

```css
.resume-page * {
  background: transparent;
  color: inherit;
}
```

### 6. Fonts Not Loading in PDF

**Fix:** The script waits for `document.fonts.ready` + 500ms buffer. If fonts still don't load, increase `POST_FONT_BUFFER_MS` in `generate-resume.ts`.

---

## Generation Workflow

### Prerequisites

1. **Dev server running**: `npm run dev`
2. **Content files populated**:
   - `content/profile.yaml` (name, email, location, tagline, stats)
   - `content/experience/index.yaml` (jobs with highlights)
   - `content/skills/index.yaml` (categorized skills)

### Steps

1. **Validate content**: `npm run validate`
2. **Preview** at http://localhost:5173/resume
3. **Verify** single-page fit (no vertical scrollbar)
4. **Check** all experience is included
5. **Generate**:

```bash
npm run generate:resume
```

6. **Verify** output at `public/resume.pdf`

### Custom Filename

```bash
npm run generate:resume -- --name "Jane Smith"
# Output: public/jane-smith.pdf
```

### Custom URL

```bash
npm run generate:resume -- --url http://localhost:3000
# Uses different dev server port
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "net::ERR_CONNECTION_REFUSED" | Start dev server: `npm run dev` |
| PDF is blank | Check browser console at /resume for React errors |
| Wrong content displayed | Verify YAML files, run `npm run validate` |
| Fonts look wrong | Increase `POST_FONT_BUFFER_MS` in script |
| Two pages instead of one | Reduce `MAX_HIGHLIGHTS_PER_JOB`, NOT `MAX_JOBS` |
| Dark background in PDF | Verify print CSS overrides html/body/#root |
| Jobs missing | Increase `MAX_JOBS` to match total in experience file |
| Skills look cramped | Reduce number of skills per category or categories |

---

## After Generation

Update hero CTA in `content/profile.yaml` to link to the resume:

```yaml
hero:
  cta:
    secondary:
      label: "Download Resume"
      href: "/resume.pdf"
```

---

## Technical Details

### Puppeteer Configuration (generate-resume.ts)

```typescript
const PAGE_DIMENSIONS = {
  LETTER: {
    WIDTH_PX: 816,   // 8.5" at 96dpi
    HEIGHT_PX: 1056, // 11" at 96dpi
  },
};

const TIMING = {
  POST_FONT_BUFFER_MS: 500,    // Wait after fonts.ready
  PAGE_LOAD_TIMEOUT_MS: 30000, // Navigation timeout
};
```

### PDF Export Settings

```typescript
await page.pdf({
  path: output,
  format: 'letter',
  printBackground: true,
  margin: {
    top: '0.4in',
    right: '0.5in',
    bottom: '0.4in',
    left: '0.5in',
  },
  preferCSSPageSize: true,
});
```

---

## Content Sources

The resume pulls data from these content files:

| Data | Source | Field |
|------|--------|-------|
| Name | `profile.yaml` | `name` |
| Email | `profile.yaml` | `email` |
| Location | `profile.yaml` | `location` |
| Tagline | `profile.yaml` | `about.tagline` |
| Stats | `profile.yaml` | `about.stats[]` |
| Jobs | `experience/index.yaml` | `jobs[]` |
| Skills | `skills/index.yaml` | `categories[].skills[]` |

---

## Quality Checklist

### Before Generating

- [ ] Content YAML files pass validation (`npm run validate`)
- [ ] Preview at /resume shows correct info
- [ ] ALL jobs are included (count them!)
- [ ] Resume fits on single page (no scrollbar)
- [ ] All highlights follow "Action → Outcome" format
- [ ] Metrics are quantified (%, $, numbers)

### After Generating

- [ ] Open PDF and verify visual appearance
- [ ] Check all text is selectable (ATS-friendly)
- [ ] Verify no dark backgrounds or visual artifacts
- [ ] Confirm all companies/roles are present
- [ ] Test PDF in an ATS simulator if available
