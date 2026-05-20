---
name: documentation-sync
description: >
  After any significant code change — new feature, API modification, config
  change, or architectural refactor — run this skill to identify which
  documentation files are now stale and update them. Keeps docs and code
  from drifting apart.
---

<!--
  TÜRKÇE AÇIKLAMA
  ───────────────
  Bu skill, kodda yapılan önemli değişikliklerden sonra hangi dokümantasyon dosyalarının
  eskidiğini tespit edip günceller. README, API docs, .env.example, CHANGELOG ve mimari
  diyagramlar incelenerek eski bilgiler düzeltilir. "Docs ile kod arasındaki uçurum"
  problemini kapatır.

  NE ZAMAN: API eklendiğinde/değiştiğinde, yeni env variable eklendiğinde,
            büyük refactor sonrası, merge öncesi veya sonrası.
  ÇIKTI:    Güncellenmiş doc dosyaları + değişim özet raporu.
-->

# Documentation Sync Skill

## When to Trigger

Run after:
- A public API endpoint is added, changed, or removed
- A CLI command or flag is modified
- A new environment variable or config key is introduced
- A major component or module is refactored
- A new npm/pip/etc. package is added or removed from dependencies
- Any `README.md` reference becomes inaccurate

## Step-by-Step Process

### 1. Identify What Changed

Review the git diff of the work just completed:

```bash
git diff main --name-only          # Files changed vs main
git diff HEAD~1 --name-only        # Files changed in last commit
```

Categorize changes:
- **API changes** → affects `docs/api/`, OpenAPI/Swagger specs, `README.md`
- **Config changes** → affects `.env.example`, `docs/configuration.md`
- **Dependency changes** → affects `README.md` (setup section), `docs/getting-started.md`
- **Architecture changes** → affects `docs/architecture.md`, diagrams
- **New features** → affects `docs/features/`, changelogs

### 2. Audit Existing Docs

For each affected category, check whether corresponding docs exist:

```
docs/
  api/             ← REST/GraphQL endpoint docs
  architecture.md  ← System design, component diagram
  configuration.md ← All env vars and config options
  getting-started.md ← Local setup guide
  features/        ← Per-feature descriptions
CHANGELOG.md       ← Version history
README.md          ← Project overview + quickstart
```

For each doc file that touches the changed area, read it and flag stale sections.

### 3. Update Docs — Priority Order

Update in this order (highest impact first):

#### A. README.md
- Setup instructions still accurate?
- Tech stack section reflects current stack?
- Any removed features still mentioned?

#### B. .env.example / Configuration Docs
For every new env variable added to code, add a corresponding entry:

```bash
# Description of what this does
NEW_VAR_NAME=example_value
```

Document in `docs/configuration.md`:
```markdown
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| NEW_VAR_NAME | Yes | — | What it controls |
```

#### C. API Docs
For every endpoint change, update the relevant doc:

```markdown
### POST /api/resource

**Changed in:** <date or version>
**Description:** ...
**Request Body:** ...
**Response:** ...
**Breaking Change:** Yes/No
```

#### D. CHANGELOG.md
Append an entry under `## [Unreleased]`:

```markdown
### Added
- <new feature description>

### Changed
- <what was modified and why>

### Fixed
- <bug fixed>

### Removed
- <what was removed>
```

Follow [Keep a Changelog](https://keepachangelog.com) format.

#### E. Architecture Docs
If a new service, module, or significant component was added:
- Update the component list in `docs/architecture.md`
- Note any new external dependencies or integrations
- If a diagram exists (Mermaid, Draw.io), update it

### 4. Verify Internal Links

After editing, do a quick check for broken internal references:

```bash
# Find markdown links pointing to non-existent files
grep -r "\[.*\](.*\.md)" docs/ README.md | grep -v "http"
```

Manually verify the top 5 most-used internal links still resolve.

### 5. Report Changes

Output a summary:

```
## Documentation Sync Complete

**Files Updated:**
- README.md — updated setup section
- docs/configuration.md — added NEW_VAR_NAME
- CHANGELOG.md — added unreleased entry

**Files That May Need Manual Review:**
- docs/architecture.md — diagram may be outdated (manual update needed)

**No changes needed:**
- docs/api/ — no endpoint changes detected
```

## Rules

- **Never delete documentation** without confirming with the user. Archive or mark as deprecated instead.
- **Don't invent information.** If you're unsure what a config variable does, write `# TODO: document this` and flag it.
- **Keep CHANGELOG.md under `[Unreleased]`** until an explicit version bump/release.
- **Every new env variable must appear in `.env.example`** — no exceptions.
- **Docs first is fine, but docs-never is not.** Even minimal docs are better than none.
