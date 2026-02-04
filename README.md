# Claude Skills Registry

<p align="center">
  <img src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fskills-registry-web.vercel.app%2Fstats.json&query=%24.total_skills&label=Skills&color=purple&style=flat-square" alt="Skills">
  <img src="https://img.shields.io/badge/Updated-Daily-green?style=flat-square" alt="Updated">
  <img src="https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square" alt="License">
  <a href="https://skills-registry-web.vercel.app"><img src="https://img.shields.io/badge/Web-Search-blue?style=flat-square" alt="Web Search"></a>
</p>

> The most comprehensive Claude Code skills registry — updated daily with the latest skills

## What is this?

The largest searchable index of Claude Code skills, aggregated from GitHub and community sources.

**Three ways to use:**
1. **[Web Search](https://skills-registry-web.vercel.app/)** - Fast browser-based search
2. **[sk CLI](https://github.com/majiayu000/caude-skill-manager)** - Terminal package manager
3. **API** - Direct JSON access

**Repo layout note:** the browsable `skills/**` archive is designed to live in a separate **data repo** (Scheme 2). See `SCHEME2_SPLIT.md`.

## Highlights

- **Massive Skill Index** - Deduplicated, quality collection (see badge for live count)
- **12 Categories** - Development, Testing, DevOps, Design, and more
- **Daily Updates** - Automated crawling and validation
- **Quality Indexed** - Metadata, descriptions, and star counts
- **Lightweight Search** - ~1MB index for fast client-side search

## Quick Start

### Option 1: Web Search

Visit [https://skills-registry-web.vercel.app/](https://skills-registry-web.vercel.app/)

### Option 2: CLI (sk)

```bash
# Install sk
go install github.com/majiayu000/caude-skill-manager@latest

# Search skills
sk search testing
sk search pdf
sk search --popular

# Install a skill
sk install anthropics/skills/docx
```

### Option 3: Direct API

```bash
# Lightweight search index (~1MB gzip)
curl https://skills-registry-web.vercel.app/search-index.json

# Full registry
curl https://raw.githubusercontent.com/majiayu000/claude-skill-registry/main/registry.json

# Specific category
curl https://skills-registry-web.vercel.app/categories/development.json
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

## Directory Structure

```
claude-skill-registry/
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
└── skills/                 # Skill archive (moved to registry-data repo)
```

---

## Categories

| Category | Code | Count | Description |
|----------|------|-------|-------------|
| `development` | `dev` | 15,000+ | Development tools, frameworks |
| `data` | `dat` | 8,000+ | Data processing, analysis |
| `design` | `des` | 5,000+ | UI/UX design, frontend |
| `testing` | `tst` | 4,000+ | Testing, QA, automation |
| `devops` | `ops` | 3,000+ | DevOps, CI/CD, infrastructure |
| `documents` | `doc` | 2,000+ | Document creation (docx, pdf) |
| `productivity` | `pro` | 1,500+ | Productivity and automation |
| `product` | `prd` | 1,000+ | Product management |
| `security` | `sec` | 800+ | Security, auditing |
| `marketing` | `mkt` | 500+ | Marketing, content, SEO |

---

## Roadmap

### Current Status

- [x] **90,000+ unique skills indexed** (deduplicated, growing daily)
- [x] **Daily auto-update** via GitHub Actions
- [x] **Security scanning** for all skills
- [x] **sk CLI** for installation

### In Progress

- [x] **Lightweight search index** (~1MB vs 17MB)
- [x] **Web search UI** (GitHub Pages)
- [ ] **GitHub Pages deployment** (pending)

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
1. Open an [issue](https://github.com/majiayu000/claude-skill-registry/issues/new)
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

👉 [Open an Issue](https://github.com/majiayu000/claude-skill-registry/issues/new)

### Contribute Code

```bash
# Clone the repo (recommended: partial + sparse checkout to avoid 200k+ files)
git clone --filter=blob:none --sparse https://github.com/majiayu000/claude-skill-registry.git
cd claude-skill-registry

# Pull only what you need (add more paths later if needed, e.g. skills/development)
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

MIT License - see [LICENSE](LICENSE) for details.

---

<p align="center">
  Made with ❤️ for the Claude Code community
</p>
