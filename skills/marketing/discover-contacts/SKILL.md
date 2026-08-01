---
name: discover-contacts
description: Research and enrich professional contacts and marketing prospects. Takes
  a contact
---

---
name: discover-contacts
description: >
  Research and enrich professional contacts and marketing prospects.
  Uses /dogpile to find current company, role, recent news, and company intelligence.
  Ingests CSV contact lists and outputs enriched profiles to /memory.
allowed-tools: ["Bash", "Read", "Write", "Task"]
triggers:
  - research contacts
  - enrich contacts
  - discover contacts
  - look up contacts
  - research prospects
  - find out about this person
  - who is this contact
  - company research
  - prospect research
  - enrich this CSV
  - research this company
  - what does their company do
  - marketing research
metadata:
  short-description: "Contact and prospect research via /dogpile enrichment"
  author: "Graham"
  version: "0.1.0"

provides:
  - discover-contacts
composes: [, task-monitor]
---

# discover-contacts

Research and enrich professional contacts and marketing prospects. Takes a contact
list (CSV, YAML, or individual names) and uses `/dogpile` to build comprehensive
profiles with current company info, role, recent news, and company intelligence.

## Why This Exists

Contact lists go stale fast. People change jobs, companies get acquired, divisions
restructure. A CSV from a DARPA conference 6 months ago is already outdated. This
skill uses deep multi-source research to answer: **"Who is this person NOW, and
what is their company doing?"**

## Architecture

```
┌──────────────────────────────────────────────────────┐
│              discover-contacts                        │
│  - Ingest contact list (CSV/YAML/name)               │
│  - Batch or single-contact research                  │
│  - Rate-limited concurrent /dogpile calls            │
│  - Enrichment pipeline                               │
└──────────────────────────────────────────────────────┘
         │                              │
    ┌────┴──────┐                 ┌─────┴─────────┐
    │ Person    │                 │ Company        │
    │ Research  │                 │ Research       │
    ├───────────┤                 ├────────────────┤
    │ - LinkedIn│                 │ - Website      │
    │ - Papers  │                 │ - News         │
    │ - GitHub  │                 │ - Funding      │
    │ - News    │                 │ - Contracts    │
    │ - Patents │                 │ - Key hires    │
    └───────────┘                 └────────────────┘
         │                              │
         └──────────┬───────────────────┘
                    │
    ┌───────────────┴────────────────────┐
    │         Enriched Profile           │
    │  - Current role + company          │
    │  - Company summary + sector        │
    │  - Recent news (last 6 months)     │
    │  - Publications / patents          │
    │  - Social links                    │
    │  - Confidence + staleness score    │
    │  → Stored to /memory               │
    │  → Written to enriched CSV/YAML    │
    └────────────────────────────────────┘
```

## Commands

```bash
# Research a single contact
./run.sh research "John Rushby" --org "SRI International"

# Research a company
./run.sh company "Galois, Inc."

# Enrich a CSV contact list (batch)
./run.sh enrich /mnt/storage12tb/media/personas/references/darpa_arcos_contacts.csv

# Enrich with concurrency limit
./run.sh enrich contacts.csv --concurrency 3 --delay 5

# Research a specific contact from the CSV
./run.sh research --csv contacts.csv --row 5

# Check enrichment freshness
./run.sh freshness contacts.csv

# Export enriched profiles
./run.sh export contacts.csv --format yaml --output enriched_contacts.yaml
```

## Input Formats

### CSV (primary)
```csv
first_name,last_name,organization,email
John,Rushby,SRI International,rushby@csl.sri.com
```

### YAML
```yaml
contacts:
  - name: John Rushby
    org: SRI International
    email: rushby@csl.sri.com
```

### Single contact (CLI)
```bash
./run.sh research "John Rushby" --org "SRI International"
```

## Enrichment Pipeline

For each contact, the skill runs a structured research pipeline:

### 1. Person Research
```
/dogpile "{first_name} {last_name} {organization} current role"
```
Extracts:
- **Current role and company** (may have changed from CSV)
- **LinkedIn profile** (via Brave search)
- **Recent publications** (ArXiv, Google Scholar)
- **GitHub activity** (if technical)
- **Recent news mentions**
- **Conference talks** (YouTube)

### 2. Company Research
```
/dogpile "{organization} recent news funding contracts"
```
Extracts:
- **Company summary** — what they do, sector, size
- **Recent news** — last 6 months of significant events
- **Government contracts** — via /ops-sam-gov if relevant
- **DARPA programs** — via /ops-darpa if relevant
- **Key hires/departures** — leadership changes
- **Funding/acquisitions** — financial events

### 3. Profile Assembly
Merges person + company research into enriched profile:

```yaml
contact:
  name: John Rushby
  current_role: Senior Computer Scientist
  current_org: SRI International
  previous_org: null  # or previous if changed
  email: rushby@csl.sri.com
  email_status: likely_valid  # or stale, bounced
  linkedin: null
  github: null
  research:
    publications: 3  # recent papers found
    patents: 0
    talks: 1
  company:
    name: SRI International
    sector: Defense/Research
    size: 2000+
    recent_news:
      - "SRI awarded $X contract for..."
    darpa_programs:
      - ARCOS
      - PROOFS
    sam_gov_active: true
  enriched_at: "2026-02-12T12:00:00Z"
  confidence: 0.85  # how confident in current info
  staleness_days: 0
```

## Rate Limiting

Batch enrichment is rate-limited to avoid burning through API quotas:

| Setting | Default | Description |
|---------|---------|-------------|
| `--concurrency` | 2 | Parallel /dogpile calls |
| `--delay` | 10 | Seconds between batches |
| `--budget` | 20 | Max /dogpile calls per run |
| `--skip-enriched` | true | Skip contacts enriched within 30 days |

## Storage

```
/mnt/storage12tb/media/personas/references/
├── darpa_arcos_contacts.csv          # Original CSV
├── darpa_arcos_enriched.yaml         # Enriched profiles
├── company_profiles/
│   ├── sri_international.yaml
│   ├── galois_inc.yaml
│   └── ...
└── enrichment_log.json               # Audit trail
```

## Memory + Taxonomy Integration

The skill integrates with the shared memory and taxonomy systems via
`memory_integration.py` for cross-session contact intelligence:

- **Pre-hook (`recall_prior_research`)**: Before researching a contact, recalls
  prior enrichment data for that person. Avoids redundant /dogpile calls and
  surfaces previously gathered intelligence.
- **Post-hook (`learn_contact`)**: After enrichment, stores the contact profile
  (name, company, role, sources, enrichment data) to memory with taxonomy
  bridge tags for cross-skill recall.
- **Bridge keywords**: Precision, Resilience, Fragility, Corruption, Loyalty, Stealth
  (tuned to contact research domain).
- **Tags**: `["discover_contacts", person_name] + bridges`

Gracefully degrades if `common.memory_client` or `taxonomy/taxonomy.py` are unavailable.

Enriched profiles are also stored to `/memory` for cross-skill access:

```bash
# After enrichment, profiles available via:
/memory recall "John Rushby SRI International"
/memory recall "DARPA ARCOS contacts"
/memory recall "defense contractors formal verification"
```

## File Structure

```
discover-contacts/
  SKILL.md                   # This file
  run.sh                     # Shell entry point
  sanity.sh                  # Sanity checks
  config.py                  # Paths, constants, skill references
  memory_integration.py      # Memory + Taxonomy hooks
```

## Leveraged Skills

| Skill | Purpose |
|-------|---------|
| `/dogpile` | Multi-source deep research per contact |
| `/memory` | Store enriched profiles for recall |
| `/ops-sam-gov` | Government contract lookup |
| `/ops-darpa` | DARPA program participation |
| `/brave-search` | Free web search for current info |
| `/perplexity` | Deep research for high-value contacts |

## Persona Generation

Enriched contacts can seed `/create-persona` for fictional personas:

```bash
# Research a contact, then create an inspired-by persona
./run.sh research "Natasha Neogi" --org NASA
/create-persona --inspired-by /mnt/storage12tb/media/personas/references/company_profiles/nasa.yaml
```

This bridges the gap between real-world contacts and the persona system.

## Privacy & Ethics

- Contact data is stored locally only (12TB drive)
- No data is sent to external services beyond search queries
- Research uses only publicly available information
- Email validation does NOT send emails
- Enrichment log tracks all research for audit
