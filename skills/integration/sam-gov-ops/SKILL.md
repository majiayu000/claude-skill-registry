---
name: sam-gov-ops
description: >
  Query SAM.gov for federal contracts, entity registrations, exclusions, and opportunities.
  Uses official GSA APIs for government contractor intelligence and OSINT research.
allowed-tools:
  - Bash
  - Read
  - Write
triggers:
  - sam.gov
  - federal contracts
  - government contractor
  - exclusions list
  - debarment
  - federal opportunities
  - uei lookup
  - cage code
metadata:
  short-description: SAM.gov federal contracts and entity lookup
---

# SAM.gov Operations Skill

Query the U.S. federal government's System for Award Management (SAM.gov) for:
- **Entity registrations** - Verify contractors, lookup UEI/CAGE codes
- **Exclusions** - Check debarment/suspension status
- **Opportunities** - Find active contract solicitations
- **Contract awards** - Research awarded contracts

## API Endpoints

| API | Purpose | Rate Limit |
|-----|---------|------------|
| Entity API | Contractor registrations, UEI/CAGE lookup | 1,000/day |
| Exclusions API | Debarred/suspended entities | 1,000/day |
| Opportunities API | Active solicitations | 1,000/day |
| Contract Awards API | Awarded contracts | 1,000/day |

## Quick Start

```bash
# Set API key (or use .env)
export SAMGOV_API_KEY="your_api_key"

# Lookup entity by name
./run.sh entity --name "Lockheed Martin"

# Lookup entity by UEI
./run.sh entity --uei "EXAMPLEUEI123"

# Check exclusions (debarment)
./run.sh exclusions --name "John Doe"

# Search opportunities
./run.sh opportunities --keyword "cybersecurity" --days 30

# Search contracts
./run.sh contracts --agency "DOD" --naics 541512
```

## Commands

### `entity` - Lookup Entity Registrations

Search for registered government contractors.

```bash
# By business name
./run.sh entity --name "Raytheon"

# By UEI (Unique Entity Identifier)
./run.sh entity --uei "ABC123DEF456"

# By CAGE code
./run.sh entity --cage "1ABC2"

# Filter by registration status
./run.sh entity --name "Boeing" --status active

# Output as JSON
./run.sh entity --name "Boeing" --json
```

**Response includes:**
- Legal business name
- UEI and CAGE codes
- Registration status (Active/Expired)
- Business types
- NAICS codes
- Address and POC info

### `exclusions` - Check Debarment/Suspension

Search the federal exclusions list.

```bash
# By name (individual or firm)
./run.sh exclusions --name "Smith"

# By classification
./run.sh exclusions --classification Firm
./run.sh exclusions --classification Individual

# By excluding agency
./run.sh exclusions --agency DOJ

# By state
./run.sh exclusions --state VA

# Active exclusions only
./run.sh exclusions --name "Corp" --active-only
```

**Exclusion types:**
- Ineligible (Proceedings Pending)
- Ineligible (Proceedings Completed)
- Prohibition/Restriction
- Voluntary Exclusion

### `opportunities` - Search Contract Solicitations

Find active federal contracting opportunities.

```bash
# Keyword search
./run.sh opportunities --keyword "artificial intelligence"

# By NAICS code
./run.sh opportunities --naics 541512

# By procurement type
./run.sh opportunities --type p  # Presolicitation
./run.sh opportunities --type o  # Solicitation
./run.sh opportunities --type a  # Award Notice

# By set-aside type
./run.sh opportunities --set-aside SBA

# Combine filters
./run.sh opportunities --keyword "cloud" --naics 541519 --days 60
```

**Procurement types:**
- `p` - Presolicitation
- `o` - Solicitation
- `k` - Combined Synopsis/Solicitation
- `r` - Sources Sought
- `s` - Special Notice
- `a` - Award Notice
- `u` - Justification and Approval

### `contracts` - Search Awarded Contracts

Research federal contract awards.

```bash
# By agency
./run.sh contracts --agency "DEPT OF DEFENSE"

# By contractor name
./run.sh contracts --contractor "Northrop Grumman"

# By NAICS
./run.sh contracts --naics 541330

# By date range
./run.sh contracts --from 2024-01-01 --to 2024-12-31

# By award type
./run.sh contracts --type "DEFINITIVE CONTRACT"
```

## Use Cases

### OSINT / Due Diligence
```bash
# Verify a contractor is registered and not excluded
./run.sh entity --name "Acme Corp" --status active
./run.sh exclusions --name "Acme Corp"
```

### Competitive Intelligence
```bash
# Find what contracts a competitor has won
./run.sh contracts --contractor "Palantir" --from 2024-01-01

# Find opportunities in a specific sector
./run.sh opportunities --naics 541512 --keyword "cloud migration"
```

### Compliance Verification
```bash
# Check if vendor is debarred before award
./run.sh exclusions --uei "ABC123DEF456" --json
```

### Market Research
```bash
# Find all cybersecurity solicitations
./run.sh opportunities --keyword "cybersecurity" --naics 541519 --days 90
```

## Environment Variables

```bash
# Required: SAM.gov API key
SAMGOV_API_KEY=your_public_api_key

# Optional: Use alpha/test environment
SAMGOV_USE_ALPHA=true
```

## Getting an API Key

1. Register at [SAM.gov](https://sam.gov)
2. Go to Account Details > Public API Key
3. Generate a new key
4. Add to `.env` as `SAMGOV_API_KEY`

## Rate Limits

| User Type | Daily Limit |
|-----------|-------------|
| Non-federal (no role) | 10 requests |
| Non-federal (with role) | 1,000 requests |
| Federal user | 1,000 requests |
| Federal system account | 10,000 requests |

## Integration with Dogpile

SAM.gov is available as an OSINT source in dogpile:

```bash
# Enable SAM.gov in OSINT preset
dogpile search "Contractor XYZ" --preset osint
```

## API Documentation

- [Entity API](https://open.gsa.gov/api/entity-api/)
- [Exclusions API](https://open.gsa.gov/api/exclusions-api/)
- [Opportunities API](https://open.gsa.gov/api/get-opportunities-public-api/)
- [Contract Awards API](https://open.gsa.gov/api/contract-awards/)
