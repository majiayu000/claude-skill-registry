---
name: domain-name-finder
description: Find, validate, and register domain names through requirements gathering, brainstorming, trademark screening, availability checking, and registration guidance.
category: business
license: MIT
---

# Domain Name Finder Skill

Find, validate, and register domain names through a structured 7-phase workflow.

## Utility Scripts

Available in the `scripts/` directory:

| Script                        | Purpose                                     | When to Use                |
| ----------------------------- | ------------------------------------------- | -------------------------- |
| `scripts/check-all.ts`        | **Comprehensive** - All checks with scoring | **Default recommendation** |
| `scripts/check-dns.ts`        | DNS availability only                       | Quick availability check   |
| `scripts/check-whois.ts`      | WHOIS registration details                  | Get registrar/dates info   |
| `scripts/check-trademarks.ts` | Trademark conflicts                         | Legal risk assessment      |
| `scripts/check-social.ts`     | Social handle availability                  | Brand consistency check    |

## 7-Phase Workflow

### Phase 1: Requirements Gathering

Understand project context and constraints.

**Gather these details:**

- **Project type**: SaaS, consumer app, e-commerce, personal brand, etc.
- **Budget range**: $10-15 (budget) to $5000+ (premium domains)
- **TLD preferences**: .com only, .io/.ai (tech), country-specific, open to
  alternatives
- **Naming style**: Descriptive, brandable, compound, playful, keyword-focused
- **Length preference**: Short (4-6 letters), medium (7-10), longer (11+)
- **Keywords**: Core terms related to the project

**Output**: User requirements document summarizing preferences.

### Phase 2: Brainstorm Domain Ideas

Generate 20-30 domain names using multiple techniques.

**Brainstorming techniques:**

1. **Keyword combinations**: Combine 2-3 relevant words (e.g., TaskFlow,
   ProjectMate)
2. **Prefixes/Suffixes**: Add get-, go-, my-, -ify, -ly, -able, -io
3. **Compound mashups**: Blend words (e.g., Pinterest = pin + interest)
4. **Creative spellings**: Drop letters, use double letters (e.g., Flickr,
   Tumblr)
5. **Latin/Greek roots**: Use meaningful prefixes/suffixes (e.g., Nova, Zen,
   Vel)
6. **Industry metaphors**: Relate to field (e.g., Anchor for stability, Bolt for
   speed)

**Example output:**

```
Descriptive: TaskFlow.com, ProjectManager.com
Brandable: Velora.io, Zenify.app
Compound: Notionly.com, ClickFlow.io
Creative: Kreato.com, Desqgn.com
```

### Phase 3: Trademark Screening

Check for potential conflicts using a combination of web signals and **assisted
manual verification**.

**Run trademark check:**

```bash
npx -y bun run scripts/check-trademarks.ts velora zenify taskflow
```

**Interpret results:**

- **Web Activity**: High activity suggests the name is in use, though not
  necessarily trademarked.
- **Agent Action (REQUIRED)**: The script outputs an "AGENT HINT" with direct
  links.
  - **Action**: Use your `read_web_page` or `search_web` tool to visit these
    links.
  - **Goal**: Confirm if an exact match exists in the trademark database.
  - **Fallback**: If the direct link fails, perform a web search for "USPTO
    trademark search [name]" and browse manually.

> [!IMPORTANT] **AGENTS**: You must not rely solely on the "Web Activity" score.
> You are required to use your browser capabilities to verify the legal status
> using the provided links.

**Output**: Web presence assessment + list of direct links for manual clearance.

### Phase 4: Domain Availability Checking

Identify which domains are available for registration.

**Run availability check:**

```bash
# Quick DNS check (fast)
npx -y bun run scripts/check-dns.ts velora.io zenify.app taskflow.com

# Detailed WHOIS check (slower, more info)
npx -y bun run scripts/check-whois.ts velora.io zenify.app taskflow.com
```

**Interpret results:**

- ✅ **Available**: No DNS/WHOIS records found
- ❌ **Registered**: Domain has active records
- ⚠️ **Error**: Check manually at registrar

**Output**: Availability table with status and registration details.

### Phase 5: Analysis and Scoring

Rank domains by overall fit using a scoring framework.

**Score each domain 1-10 across:**

1. **Brandability** (memorable, pronounceable, spellable)
2. **Trademark risk** (based on Phase 3)
3. **SEO potential** (keyword relevance, .com advantage)
4. **Budget fit** (aligned with price range)
5. **Marketing potential** (social handles, logo-friendly)
6. **User preference** (matches style criteria)

**Weighted scoring:**

```
Total = (Brandability × 2) + Trademark Risk + SEO + Budget + Marketing + Style
```

**Output**: Ranked domain list with scores and rationale.

### Phase 6: Deep Dive on Finalists

Comprehensive analysis of top 3-5 domains.

**For each finalist, provide:**

- Name breakdown (pronunciation, meaning, associations)
- Trademark risk summary
- Domain history (Wayback Machine: https://web.archive.org/)
- Social handle availability: `npx -y bun run scripts/check-social.ts velora`
- Competitive landscape (similar domains in use)
- Marketing angles and tagline suggestions
- Registration recommendation

**Output**: Detailed dossier for each finalist domain.

### Phase 7: Registration and Next Steps

Guide through registration process and setup.

**See references:**

- `references/registrars-comparison-2025.md` - Compare pricing and features
- `references/registration-guide.md` - Step-by-step registration walkthrough
- `references/dns-setup-guide.md` - Configure A/CNAME/MX records

**Key considerations:**

- **Registrar choice**: Cloudflare (free WHOIS privacy), Porkbun (low prices),
  Namecheap (support)
- **Defensive registrations**: Consider .com + primary TLD + typos
- **Trademark filing**: Consult attorney before significant investment
- **DNS setup**: Point to hosting provider, configure email
- **Social profiles**: Secure matching handles on key platforms

**Output**: Actionable registration checklist.

## Quick Reference

**Project type examples:**

- SaaS: .com, .io, .ai - brandable, compound words
- Consumer app: .com, .app - short, memorable
- E-commerce: .com, .shop - descriptive, keyword-rich
- Personal brand: .com, .me - name-based, professional

**TLD pricing (2025):**

- .com: $10-15/year (standard), $100+ (premium)
- .io: $35-50/year
- .ai: $80-100/year
- .app: $15-20/year

**Common pitfalls:**

- Numbers (hard to remember)
- Hyphens (confusing, seen as spammy)
- Double letters (typos: Flicker vs Flickr)
- Trendy misspellings (may age poorly)
- Long names (>15 characters)

## References

- `references/trademark-search-guide.md` - USPTO/EUIPO/UKIPO database links
- `references/registrars-comparison-2025.md` - Pricing, features, pros/cons
- `references/registration-guide.md` - Step-by-step registration
- `references/dns-setup-guide.md` - A/CNAME/MX records

## Examples

See `examples/EXAMPLES.md` for real-world walkthroughs.

## Sources

- [ICANN Lookup](https://lookup.icann.org/en)
- [IANA Root Zone Database](https://www.iana.org/domains/root/db)
- [Create DNS Records | Cloudflare Docs](https://developers.cloudflare.com/dns/manage-dns-records/how-to/create-dns-records/)
- [Search Trademarks | USPTO](https://www.uspto.gov/trademarks/search)
- [Global Brand Database | WIPO](https://branddb.wipo.int/)
- [Search for a Trademark | GOV.UK](https://www.gov.uk/search-for-trademark)
