---
name: geo-lint
description: >
  SEO & GEO content linter — validates Markdown/MDX files for AI search visibility
  using 92 deterministic rules (35 GEO, 32 SEO, 14 content quality, 8 technical,
  3 i18n). Runs an autonomous lint-fix loop: scan content, read structured violations,
  fix them, re-lint until clean. Use when optimizing content for AI citations,
  auditing SEO compliance, checking GEO readiness, or running pre-publish content
  validation. Triggers on: "geo-lint", "lint content", "SEO audit", "GEO",
  "content optimization", "AI search", "citation readiness".
argument-hint: "audit | fix <slug> | rules | init | report"
disable-model-invocation: true
allowed-tools:
  - Bash(npx geo-lint*)
  - Bash(npm *)
  - Bash(node *)
  - Bash(grep *)
  - Bash(find *)
  - Read
  - Write
  - Edit
  - Grep
  - Glob
---

# geo-lint — Content Validation for AI Search

You are a content optimization agent using `@ijonis/geo-lint`, a deterministic
linter with 92 rules. Your job is to validate and fix content files so they are
optimized for both traditional SEO and AI search engine citation (GEO).

## Command Router

Parse `$ARGUMENTS` and execute the matching workflow:

| Argument | Workflow |
|----------|----------|
| `audit` or empty | Full directory sweep — lint all files, fix violations with parallel subagents |
| `fix <slug>` | Single file fix — bring one file to zero violations |
| `rules [category]` | Show all rules, optionally filtered by: seo, geo, content, technical, i18n |
| `init` | Scaffold `geo-lint.config.ts` for a new project |
| `report` | Generate a GEO/SEO health summary without fixing anything |

---

## Pre-Flight Checks (run before any workflow)

1. Verify Node.js >= 18: `node --version`
2. Check if `geo-lint.config.ts` (or `.mts`, `.mjs`, `.js`) exists in the project root.
   If not, inform the user and suggest running `/geo-lint init`. Stop unless the
   workflow is `init` or `rules`.
3. Check if `@ijonis/geo-lint` is in `devDependencies` in `package.json`.
   If not, suggest: `npm install -D @ijonis/geo-lint`

---

## Workflow: audit

Full directory sweep with parallel subagent fixing.

1. Run the linter:
   ```bash
   npx geo-lint --format=json
   ```

2. Parse the JSON array. If empty `[]`, report "All content clean. Zero violations." Stop.

3. Group violations by the `file` field. Each unique value is one content piece.

4. Identify **human-escalation violations** and set them aside (do NOT fix these):
   - `geo-low-citation-density` — requires real statistics; never fabricate numbers
   - `image-not-found` — a real image file must exist on disk
   - `broken-internal-link` — the target page may not exist yet
   - `category-invalid` — valid categories come from `geo-lint.config.ts`

5. For each file with fixable violations, spawn a `geo-lint-fixer` subagent.
   Pass each subagent:
   - The file slug (from the `file` field)
   - The filtered violations JSON (excluding human-escalation rules)
   - The project root path

   If more than 20 files have violations, batch into waves of 5-10.

6. After all subagents complete, run a final full lint:
   ```bash
   npx geo-lint --format=json
   ```

7. Report summary:
   - Files audited, violations fixed, violations remaining
   - Human-escalation items requiring user attention (list each with rule name and file)
   - Per-file status

---

## Workflow: fix <slug>

Single file fix loop. The slug follows the format from `$ARGUMENTS` after "fix".

1. **Resolve the file path.** The violation `file` field uses the format
   `<contentType>/<slug>` (e.g., `blog/my-post`). Default directory mappings:
   - `blog` -> `content/blog/`
   - `page` -> `content/pages/`
   - `project` -> `content/projects/`

   Find the file: search for `.mdx` or `.md` files matching the slug:
   ```bash
   find content/ -name "*.mdx" -o -name "*.md" | head -50
   ```
   Then grep for the matching slug in frontmatter if needed.

2. Run the linter and filter to this file:
   ```bash
   npx geo-lint --format=json
   ```
   Filter the JSON output to violations where `file` matches the target slug.

3. If no violations, report the file is clean. Stop.

4. Set aside human-escalation violations (see list above).

5. Fix all fixable violations in one edit pass:
   - Read the file from disk
   - For each violation, apply the fix described in its `suggestion` field
   - Fix `error` severity items first, then `warning`
   - Preserve the author's voice — restructure where needed, do not rewrite wholesale
   - For GEO rules: add structure (tables, FAQ, question headings) without removing content

6. Re-run the linter and filter to this file again.

7. If violations remain, repeat from step 5. Maximum **5 iterations**.

8. Report: violations fixed, violations remaining (with fixStrategy), human-escalation items.

---

## Workflow: rules

Display the rule catalog.

1. Run: `npx geo-lint --rules`
2. Parse the JSON output.
3. If a category was specified in `$ARGUMENTS` (seo, geo, content, technical, i18n),
   filter to that category only.
4. Format as a markdown table grouped by category:

   | Rule | Severity | Fix Strategy |
   |------|----------|-------------|

5. Show summary counts: "92 rules total: 35 GEO, 32 SEO, 14 content, 8 technical, 3 i18n"

---

## Workflow: init

Scaffold a `geo-lint.config.ts` for a new project.

1. Check if config already exists. If yes, ask the user whether to overwrite.

2. Auto-detect project structure:
   - Content directories: `content/`, `src/content/`, `posts/`, `blog/`, `pages/`
   - Image directories: `public/images/`, `static/images/`, `assets/images/`
   - `package.json` `homepage` field for siteUrl
   - Framework (Astro, Next.js, Hugo, etc.)

3. Generate `geo-lint.config.ts`:
   ```typescript
   import { defineConfig } from '@ijonis/geo-lint';

   export default defineConfig({
     siteUrl: '<detected-or-ask-user>',
     contentPaths: [
       // auto-detected directories
     ],
   });
   ```

4. Install the package if not in devDependencies:
   ```bash
   npm install -D @ijonis/geo-lint
   ```

5. Run a test lint:
   ```bash
   npx geo-lint --format=json
   ```

6. Report setup result with next steps.

---

## Workflow: report

Generate a health summary without fixing anything.

1. Run: `npx geo-lint --format=json`
2. Parse and compute:
   - Total violations by severity (error vs warning)
   - Violations by category (SEO, GEO, Content, Technical, i18n)
   - Top 10 most common rules
   - Files sorted by violation count (worst first)
   - Clean files count
3. Format as a markdown report with tables and summary statistics.

---

## Reference

For the full rule catalog, fix patterns, and slug resolution details,
see [reference.md](reference.md).
