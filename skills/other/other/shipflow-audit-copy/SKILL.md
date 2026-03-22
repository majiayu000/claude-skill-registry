---
name: shipflow-audit-copy
description: Professional copywriting review — single page (with argument) or full project audit (no argument)
disable-model-invocation: true
argument-hint: [file-path | "global"] (omit for full project)
---

## Context

- Current directory: !`pwd`
- Project CLAUDE.md: !`head -100 CLAUDE.md 2>/dev/null || echo "no CLAUDE.md"`
- Content language: !`grep -ri "lang=" src/layouts/*.astro src/app/layout.tsx 2>/dev/null | head -5 || echo "unknown"`
- All pages: !`find src/pages src/app -name "*.astro" -o -name "*.tsx" -o -name "*.vue" 2>/dev/null | grep -v node_modules | sort`
- i18n/translations: !`find src -path "*/i18n/*" -o -path "*/locales/*" -o -path "*/messages/*" 2>/dev/null | head -10 || echo "none"`
- Content collections: !`find src/content -type f 2>/dev/null | head -20 || echo "no content dir"`

## Mode detection

- **`$ARGUMENTS` is "global"** → GLOBAL MODE: audit ALL projects in the workspace.
- **`$ARGUMENTS` is a file path** → PAGE MODE: review that single page.
- **`$ARGUMENTS` is empty** → PROJECT MODE: full copywriting audit of the entire project.

---

## GLOBAL MODE

Audit ALL web projects in the workspace for copywriting quality.

1. Read `/home/claude/shipflow_data/PROJECTS.md` — check the **Domain Applicability** table. Identify projects with ✓ in the Copy column.

2. Use **AskUserQuestion** to let the user choose:
   - Question: "Which projects should I audit for copywriting?"
   - `multiSelect: true`
   - One option per applicable project: label = project name, description = stack from PROJECTS.md
   - All applicable projects pre-listed as options

3. Use the **Task tool** to launch one agent per **selected** project — ALL IN A SINGLE MESSAGE (parallel). Each agent: `subagent_type: "general-purpose"`.

   Agent prompt must include:
   - `cd [path]` then read `CLAUDE.md` for project context
   - The complete **PROJECT MODE** section from this skill (all 6 phases: Voice & Tone Inventory → Messaging Hierarchy → Page-by-Page Copy Scan → Conversion Copy Check → Fix → Report)
   - The **Tracking** section from this skill
   - Rule: **read-only analysis** — no code fixes, only update AUDIT_LOG.md and TASKS.md

4. After all agents return, compile a **cross-project copy report**:

   ```
   GLOBAL COPY AUDIT — [date]
   ═══════════════════════════════════════
   PROJECT SCORES
     [project]    [A/B/C/D]  —  summary
     ...
   CROSS-PROJECT PATTERNS
     [Systemic copy issues in 2+ projects]
   ALL ISSUES BY SEVERITY
     🔴 [project] file:line — description
     🟠 [project] file:line — description
     🟡 [project] file:line — description
   Total: X critical, Y high, Z medium across N projects
   ═══════════════════════════════════════
   ```

5. Update `/home/claude/shipflow_data/AUDIT_LOG.md` (one row per project, Copy column) and `/home/claude/shipflow_data/TASKS.md` (each project's `### Audit: Copy` subsection).

6. Ask: **"Which projects should I fix?"** — list projects with scores. Fix only approved projects, one at a time.

---

## PAGE MODE

### Step 1: Gather the page

1. Read the target file (`$ARGUMENTS`).
2. Read layout/wrapper components for shared copy (nav, footer, CTAs).
3. Read i18n/translation files if the project uses them.
4. Identify the page's role in the user journey (landing, feature, pricing, blog, docs, etc.).

### Step 2: Audit against this checklist

Score each category **A/B/C/D**. Be strict — professional copywriter standard.

#### 1. Value Proposition & Messaging
- [ ] Primary benefit is clear within 5 seconds of reading
- [ ] Headline answers "what's in it for me?" not "what is this?"
- [ ] Subheadline adds specificity (numbers, outcomes, timeframe)
- [ ] Copy speaks to a specific audience, not everyone
- [ ] Features are framed as benefits (not just feature lists)

#### 2. Clarity & Readability
- [ ] Sentences average under 20 words
- [ ] Paragraphs are 2-3 sentences max
- [ ] No jargon without context (or jargon is intentional for the audience)
- [ ] Active voice dominant (passive < 10%)
- [ ] Flesch-Kincaid grade level appropriate for audience (typically 6-8)
- [ ] No filler words ("very", "really", "just", "actually", "basically")

#### 3. Persuasion & Psychology
- [ ] Social proof present where claims are made (testimonials, numbers, logos)
- [ ] Urgency/scarcity used authentically (not fake countdown timers)
- [ ] Objections addressed before they arise
- [ ] Risk reversal present (guarantee, free trial, no credit card)
- [ ] Emotional trigger matches audience's primary motivation

#### 4. Calls to Action
- [ ] Primary CTA uses action verb + benefit ("Start free trial" not "Submit")
- [ ] One clear primary CTA per section (no competing CTAs)
- [ ] CTA copy matches what actually happens next
- [ ] Button text works standalone (makes sense without surrounding context)
- [ ] Secondary CTAs provide a lower-commitment alternative

#### 5. Microcopy & UX Writing
- [ ] Form labels are clear, not clever
- [ ] Error messages explain what went wrong AND how to fix it
- [ ] Success messages confirm what happened
- [ ] Empty states guide the user to take action
- [ ] Loading states set expectations
- [ ] Navigation labels are predictable (no creative menu names)

#### 6. Tone & Voice Consistency
- [ ] Tone is consistent across the page (no formal → casual switches)
- [ ] Voice matches brand personality throughout
- [ ] Humor (if used) doesn't undermine trust
- [ ] Address style is consistent (tu/vous in French, you/we in English)
- [ ] Technical level is consistent

#### 7. Grammar & Polish
- [ ] Zero spelling errors
- [ ] Zero grammar errors
- [ ] Consistent capitalization (title case vs sentence case)
- [ ] Consistent punctuation
- [ ] No broken interpolation or placeholder text (`{name}`, `Lorem ipsum`)

### Step 3: Rewrite and fix

For each issue rated B or worse:
1. Quote the problematic copy.
2. Explain why it's weak.
3. Provide a rewritten version directly in the code.
4. For subjective tone choices, propose 2 options and ask the user.

### Step 4: Report

```
COPY REVIEW: [page name]
─────────────────────────────────────
Value Proposition  [A/B/C/D] — one-line summary
Clarity            [A/B/C/D] — one-line summary
Persuasion         [A/B/C/D] — one-line summary
Calls to Action    [A/B/C/D] — one-line summary
Microcopy          [A/B/C/D] — one-line summary
Tone & Voice       [A/B/C/D] — one-line summary
Grammar & Polish   [A/B/C/D] — one-line summary
─────────────────────────────────────
OVERALL            [A/B/C/D]

Rewrites applied: X | Needs decision: Y
```

---

## PROJECT MODE

### Workspace root detection

If the current directory has no project markers (no `package.json`, no `src/` dir) BUT contains multiple project subdirectories — you are at the **workspace root**, not inside a project.

Use **AskUserQuestion**:
- Question: "You're at the workspace root. Which project(s) should I audit for copy?"
- `multiSelect: true`
- Options:
  - **All projects** — "Run copy audit across every applicable project" (Recommended)
  - One option per content project from `/home/claude/shipflow_data/PROJECTS.md`: label = project name, description = stack

Then proceed to **GLOBAL MODE** with the selected projects.

### Phase 1: Voice & Tone Inventory

Read the homepage, about page, and 3-5 key pages. Document:

1. **Brand voice profile**: Is the voice consistent? Describe it.
2. **Address style**: tu/vous (FR) or formal/informal (EN) — consistent everywhere?
3. **Terminology**: List key terms. Flag synonyms used inconsistently (e.g., "dashboard" vs "panel" vs "interface").
4. **Tone range**: Where does tone shift? Intentional or accidental?

### Phase 2: Messaging Hierarchy

Map the entire site's messaging:

1. **Homepage**: What's the primary message? Strongest possible version?
2. **Feature/product pages**: Reinforce or contradict the homepage?
3. **Blog/content**: Support core positioning?
4. **Pricing**: Value framing consistent with feature pages?
5. **About/team**: Build credibility for claims made elsewhere?

Flag messaging contradictions or gaps.

### Phase 3: Page-by-Page Copy Scan

For each page, check:
- [ ] Headline is benefit-driven
- [ ] Body copy is scannable
- [ ] CTAs use action verbs + benefit
- [ ] No filler words or corporate jargon
- [ ] No spelling/grammar errors
- [ ] No placeholder text or broken interpolation
- [ ] Microcopy is helpful

### Phase 4: Conversion Copy Check

- [ ] Landing pages have a clear single message
- [ ] Pricing page frames value before cost
- [ ] Signup/onboarding copy reduces anxiety
- [ ] Error messages are human and actionable
- [ ] Success messages reinforce value
- [ ] 404 page is helpful

### Phase 5: Fix

Rewrite and fix all issues directly in code. Prioritize:
1. **Homepage and pricing** (highest traffic/impact)
2. **CTAs across the site** (direct conversion impact)
3. **Inconsistent terminology** (fix at source: i18n files or shared constants)
4. **Grammar/spelling errors** (zero tolerance)
5. **Microcopy** (error messages, empty states, confirmations)

### Phase 6: Report

```
COPY AUDIT: [project name]
═══════════════════════════════════════

VOICE & TONE
  Brand voice:  [description]
  Consistency:  [A/B/C/D]
  Terminology:  X inconsistencies found

MESSAGING HIERARCHY
  Core message clarity:    [A/B/C/D]
  Cross-page coherence:    [A/B/C/D]

PAGE SCORES
  /                  [A/B/C/D] — "[current headline]"
  /pricing           [A/B/C/D] — "[current headline]"
  ...

CONVERSION COPY        [A/B/C/D]
MICROCOPY              [A/B/C/D]
GRAMMAR & POLISH       [A/B/C/D]
═══════════════════════════════════════
OVERALL                [A/B/C/D]

Rewrites applied: X across Y files
Terminology standardized: Z terms
Needs decision: W items
```

---

## Tracking (all modes)

After generating the report and applying fixes:

### Log the audit

Append a row to two files:

1. **Global `/home/claude/shipflow_data/AUDIT_LOG.md`**: append a row filling only the Copy column, `—` for others.
2. **Project-local `./AUDIT_LOG.md`**: same without the Project column.

Create either file if missing.

### Update TASKS.md

1. **Local TASKS.md** (project root): add/replace an `### Audit: Copy` subsection with critical (🔴), high (🟠), and medium (🟡) issues as task rows.
2. **Master `/home/claude/shipflow_data/TASKS.md`**: find the project's section, add/replace an `### Audit: Copy` subsection with the same tasks.

---

## Important (all modes)

- Detect content language automatically. Review in that language.
- For French sites: check tutoiement/vouvoiement consistency, French typographic rules (espaces insécables before : ; ! ?), avoid anglicisms when French alternatives exist.
- Preserve the author's voice — elevate, don't replace.
- Never use clichés ("leverage", "empower", "seamless", "révolutionner", "unique").
- All rewrites must fit UI constraints (button width, card height, etc.).
- Never change copy that's clearly a direct quote or testimonial.
- In project mode, build a mini style guide from findings. Standardize terminology at the source.
- **Accents français obligatoires.** Lors de toute création ou modification de contenu en français, vérifier systématiquement que TOUS les accents sont présents et corrects (é, è, ê, à, â, ù, û, ô, î, ï, ç, œ, æ). Les accents manquants sont une faute d'orthographe. Relire chaque texte produit pour s'assurer qu'aucun accent n'a été oublié — c'est une erreur très fréquente à corriger impérativement.
