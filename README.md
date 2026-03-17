# Claude Skills Registry

> **Core repo:** logic + index + site.  
> **Main repo (merged artifact):** https://github.com/majiayu000/claude-skill-registry  
> **Data repo (skills archive):** https://github.com/majiayu000/claude-skill-registry-data  
> **Authority:** core workflows are canonical; main is a publish mirror.  
<p align="center">
  <img src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fmajiayu000.github.io%2Fclaude-skill-registry-core%2Fstats.json&query=%24.dedup_skill_count&label=Skills%20(dedup)&color=purple&style=flat-square" alt="Skills (dedup)">
  <img src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fmajiayu000.github.io%2Fclaude-skill-registry-core%2Fstats.json&query=%24.raw_skill_count&label=SKILL.md%20files&color=blueviolet&style=flat-square" alt="SKILL.md files">
  <img src="https://img.shields.io/badge/Updated-Daily-green?style=flat-square" alt="Updated">
  <img src="https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square" alt="License">
  <a href="https://majiayu000.github.io/claude-skill-registry-core/"><img src="https://img.shields.io/badge/Web-Search-blue?style=flat-square" alt="Web Search"></a>
</p>

> The most comprehensive Claude Code skills registry — updated daily with the latest skills

## What is this?

The largest searchable index of Claude Code skills, aggregated from GitHub and community sources.

**Three ways to use:**
1. **[Web Search](https://majiayu000.github.io/claude-skill-registry-core/)** - Fast browser-based search
2. **[sk CLI](https://github.com/majiayu000/caude-skill-manager)** - Terminal package manager
3. **API** - Direct JSON access

**Repo layout note:** `core` owns workflows/pipeline logic, `data` stores `skills/**`, and `main` is generated from `core + data`. See `SCHEME2_SPLIT.md`.

## Highlights

- **Massive Skill Index** - Deduplicated, quality collection (see badge for live count)
- **Rich Categories** - Development, Testing, DevOps, Design, and more
- **Daily Updates** - Automated crawling/validation by core scheduled workflows
- **Quality Indexed** - Metadata, descriptions, and star counts
- **Lightweight Search** - Gzip-compressed index for fast client-side search

## Operational Ownership

- **Core**: source of truth for workflows, crawling, scanning, and index/site generation
- **Data**: canonical archived skill tree (`skills/**`)
- **Main**: publish artifact for merged browsing/compatibility consumers
- **Publish contract**: core dispatches main publish with pinned `core_sha` + `data_sha`

## Quick Start

### Option 1: Web Search

Visit [https://majiayu000.github.io/claude-skill-registry-core/](https://majiayu000.github.io/claude-skill-registry-core/)

### Option 2: CLI (sk)

```bash
# Install sk
go install github.com/majiayu000/caude-skill-manager@latest

# Search skills
sk search testing
sk search pdf
sk search --popular

# Install a skill
sk install anthropics/skills/skills/docx
```

### Option 3: Direct API

```bash
# Lightweight search index (gzip-compressed)
curl https://majiayu000.github.io/claude-skill-registry-core/search-index.json

# Full registry
curl https://raw.githubusercontent.com/majiayu000/claude-skill-registry-core/main/registry.json

# Specific category
curl https://majiayu000.github.io/claude-skill-registry-core/categories/development.json
```

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│  Layer 1: Data Collection                                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ GitHub Crawl │→ │ Download     │→ │ Security     │          │
│  │ (discover)   │  │ (sync)       │  │ (scanner)    │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  Layer 2: Index Generation                                      │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐    │
│  │ search-index   │  │ categories/    │  │ featured.json  │    │
│  │ .json (~1MB)   │  │ *.json         │  │ (top 100)      │    │
│  └────────────────┘  └────────────────┘  └────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  Layer 3: Consumption                                           │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐    │
│  │ Web UI         │  │ sk CLI         │  │ API            │    │
│  │ (GitHub Pages) │  │ (Go)           │  │ (JSON)         │    │
│  └────────────────┘  └────────────────┘  └────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

### Search Index Schema

```typescript
// Lightweight index for fast search (~1MB gzip)
interface SearchIndex {
  v: string;           // Version (date)
  t: number;           // Total count
  s: SkillMini[];      // Skills array
}

interface SkillMini {
  n: string;           // name
  d: string;           // description (truncated 80 chars)
  c: string;           // category code (dev, ops, sec, etc.)
  g: string[];         // tags (max 5)
  r: number;           // stars
  i: string;           // install path
}
```

---

## Directory Structure (Core)

```
claude-skill-registry-core/
├── registry.json           # Full registry (all skills)
├── docs/                   # GitHub Pages
│   ├── index.html          # Web search UI
│   ├── search-index.json   # Lightweight search index
│   ├── featured.json       # Top 100 skills
│   └── categories/         # Category indexes
├── sources/                # Data sources
│   ├── anthropic.json
│   ├── community.json
│   └── skillsmp.json
├── scripts/                # Build scripts
│   ├── build_search_index.py
│   ├── discover_by_topic.py
│   ├── security_scanner.py
│   └── ...
└── (no committed skills/)  # skills/** lives in registry-data; mounted in CI when needed
```

---

## Categories

Category counts are published in the index (`categories/*.json`). Here are the standard codes:

| Category | Code | Description |
|----------|------|-------------|
| `development` | `dev` | Development tools, frameworks |
| `data` | `dat` | Data processing, analysis |
| `design` | `des` | UI/UX design, frontend |
| `testing` | `tst` | Testing, QA, automation |
| `devops` | `ops` | DevOps, CI/CD, infrastructure |
| `documents` | `doc` | Document creation (docx, pdf) |
| `productivity` | `pro` | Productivity and automation |
| `product` | `prd` | Product management |
| `security` | `sec` | Security, auditing |
| `marketing` | `mkt` | Marketing, content, SEO |

---

## Roadmap

### Current Status

- [x] **Index count** tracked by the badge (core `registry.json`)
- [x] **Archive size:** tracked by badge (raw `SKILL.md` count from `stats.json`)
- [x] **Daily auto-update** via GitHub Actions
- [x] **Security scanning** for all skills
- [x] **sk CLI** for installation

### In Progress

- [x] **Lightweight search index** (gzip-compressed; see stats.json)
- [x] **Web search UI** (GitHub Pages)
- [x] **GitHub Pages deployment** (https://majiayu000.github.io/claude-skill-registry-core/)

### Planned

- [ ] **AI semantic search** (vector similarity)
- [ ] **Skill recommendations** (based on usage)
- [ ] **Version tracking** for skills
- [ ] **Skill quality scoring**
- [ ] **API rate limiting** and caching

---

## Contributing

### Add Your Skill

**Option 1: Submit via Issue**
1. Open an [issue](https://github.com/majiayu000/claude-skill-registry-core/issues/new)
2. Use the "Add Skill" template
3. Provide: repo URL, name, description, category

**Option 2: Submit via PR**
1. Fork this repo
2. Add your skill to `sources/community.json`:

```json
{
  "name": "your-skill-name",
  "repo": "your-username/your-repo",
  "path": "optional/path/to/skill",
  "description": "What your skill does",
  "category": "development",
  "tags": ["testing", "automation"]
}
```

3. Submit a PR

### Report Issues

We welcome feedback! Please open an issue for:
- **Bugs** - Search not working, incorrect data
- **Feature requests** - New categories, better search
- **UX improvements** - Web UI, CLI enhancements
- **Data quality** - Duplicate skills, wrong categories

👉 [Open an Issue](https://github.com/majiayu000/claude-skill-registry-core/issues/new)

### Contribute Code

```bash
# Clone the core repo (authoritative pipeline repo)
git clone --filter=blob:none --sparse https://github.com/majiayu000/claude-skill-registry-core.git
cd claude-skill-registry-core

# Pull only what you need (add more paths later as needed)
git sparse-checkout set --cone docs scripts sources schema

# Install dependencies
pip install -r requirements.txt

# Build search index locally
python scripts/build_search_index.py --registry registry.json --output docs

# Test web UI
cd docs && python -m http.server 8000
# Visit http://localhost:8000
```

See `docs/FAST_CLONE.md` for more options (existing clones, getting full checkout, Windows notes).

---

## Related Projects

| Project | Description |
|---------|-------------|
| [caude-skill-manager](https://github.com/majiayu000/caude-skill-manager) | CLI tool for installing skills (`sk`) |
| [anthropics/skills](https://github.com/anthropics/skills) | Official Anthropic skills |
| [SkillsMP](https://skillsmp.com) | Web-based skill marketplace |
| [awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills) | Curated skill list |

---

## License

MIT License applies to the registry code/pipeline only - see [LICENSE](LICENSE) for details.

## Third-Party License & Attribution

Third-party skills under `skills/**` keep their original licenses and copyright ownership.

- Repository-level MIT does **not** relicense third-party skill content.
- Every imported skill metadata file should include:
  - `author`
  - `source_url`
  - `license`
  - `copyright`
  - `permission_note`
  - `distribution` (`compatible` or `restricted`)
- `restricted` entries are not MIT-compatible by default and require explicit upstream permission before redistribution/use.
- Notices are generated by compliance checks into `THIRD_PARTY_NOTICES.md`.
- Metadata compliance runs in advisory mode by default to avoid blocking collection; strict blocking can be enabled when needed.

---

<p align="center">
  Made with ❤️ for the Claude Code community
</p>
