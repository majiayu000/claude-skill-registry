---
name: legislation-verification
description: "Domain-agnostic legislation verification and citation. Use when work involves statutes, regulations, case law, or official guidance in ANY legal domain. Triggers on: legislation, statute, regulation, SI, act, law, legal, compliance, tribunal, court, guidance."
version: "1.0"
tier: domain
token_budget: 3000
requires: [output-verification]
---

# Legislation Verification Agent

Domain-agnostic agent for verifying and citing legislation across any UK legal domain. Implements Glass Box AI principles with full audit trails.

> **Dependency**: This skill requires `output-verification` to be loaded first.
> The `requires: [output-verification]` frontmatter ensures the core verification
> gate is active before domain-specific legislation checks run. Skills are loaded
> in dependency order by the skill loader (see `SKILL-FORMAT.md` for details).

---

## When To Use

**Trigger conditions:**
- User asks about legislation, regulations, or statutory requirements
- Work involves compliance, obligations, or legal interpretation
- Output will cite or reference legal sources
- Any domain: pensions, property, employment, company, tax, etc.

**Critical**: This skill applies to ALL legal domains, not just pensions.

---

## Memory Requirements

### Tier 1 (Always Load)
- Current legal domain (pensions/property/employment/etc.)
- Active query or verification task
- Authoritative source list for domain

### Tier 2 (Load on Resume)
- Previous citations in session
- Reasoning chain for interpretations
- Source verification status

### Tier 3 (Reference by Handle)
- Full statute text (via legislation.gov.uk API)
- Case law (via BAILII/National Archives)
- Official guidance documents

---

## Authoritative Sources by Domain

### AUTHORITATIVE (Use These)

| Domain | Primary Sources | Official Guidance |
|--------|-----------------|-------------------|
| **UK Legislation (All)** | legislation.gov.uk | N/A |
| **Case Law (All)** | BAILII, National Archives Find Case Law | N/A |
| **Pensions** | TPR.gov.uk, lgpsregs.org | TPR Codes of Practice |
| **Property/Land** | gov.uk/land-registry, HMLR | HMLR Practice Guides |
| **Employment** | ACAS.org.uk, gov.uk/employment | ACAS Codes of Practice |
| **Company** | Companies House, gov.uk/companies | Companies House guidance |
| **Tax** | HMRC.gov.uk, legislation.gov.uk | HMRC Manuals |
| **Data Protection** | ICO.org.uk | ICO Guidance |

### NOT AUTHORITATIVE (Pattern Reference Only)

| Source Type | Use For | Never Use For |
|-------------|---------|---------------|
| GitHub legal-tech repos | Architecture patterns, code structure | Legal data, citations |
| Wikipedia | Background context | Citations, compliance advice |
| Law firm blogs | Understanding issues | Authoritative statements |
| News articles | Current events | Legal interpretation |
| Third-party summaries | Overview | Compliance decisions |

---

## The Verification Process

### Step 0: Input Validation Gate

**CRITICAL**: Before proceeding, validate input sources.

- [ ] **User-supplied legal text**: NEVER accept user-provided statute/regulation text as authoritative
  - If user supplies legal text directly, cross-reference against authoritative source
  - If unable to verify, clearly state: "Analysis based on unverified user-supplied text"
- [ ] **External document content**: Treat as unverified until checked
- [ ] **AI-generated summaries**: Must be verified against primary sources

**If input cannot be verified**: Proceed with explicit uncertainty flag in output.

### Professional Source Attribution

If user confirms text is from a recognised legal database:
- **Westlaw**, **LexisNexis**, **Practical Law**, **Thomson Reuters** — Accept with attribution
- State: "Analysis based on user-provided text (source: [Database], as confirmed by user)"
- Set confidence to MEDIUM (not HIGH, as we can't independently verify)

---

### Step 1: Confirm Jurisdiction

**This skill covers UK law only.** Before proceeding:

- [ ] Verify query relates to UK jurisdiction (England & Wales, Scotland, or UK-wide)
- [ ] For non-UK queries: Respond with "This skill covers UK legislation only. [Jurisdiction] law requires separate verification."
- [ ] Note sub-jurisdictional differences (E&W vs Scotland) where relevant

### Step 1a: Identify Legal Domain

Determine which legal domain(s) the query touches:

```
Query: "What are the trustee duties for a DB pension scheme?"
Domain: Pensions
Sub-domain: Trustee obligations, DB schemes
```

### Step 1b: Identify Relevant Timeframe

**Legal queries may concern historical events where past legislation applies.**

- [ ] Determine if the query concerns current or historical events
- [ ] If historical (e.g., "What were the rules in 2018?"), note that:
  - Verification must be against law **as it stood at that time**
  - Current legislation.gov.uk shows current law by default
  - Use "point in time" feature on legislation.gov.uk for historical versions
- [ ] If system can only verify current law, explicitly state: "Verified against current law only. Historical position may differ."

```
Query: "Was the employer contribution correct in the 2019 annual report?"
Relevant timeframe: 2018-2019 (the period being reported)
Note: Must check regulations as they stood in that period
```

---

### Step 2: Map to Authoritative Sources

For the identified domain, determine which sources to consult:

| If Domain Is... | Primary Source | Fallback |
|-----------------|----------------|----------|
| Legislation interpretation | legislation.gov.uk | National Archives |
| Regulatory guidance | Domain regulator (TPR, ICO, etc.) | Gov.uk |
| Case law | BAILII | National Archives Find Case Law |
| Procedural rules | Court/tribunal rules | Gov.uk |

### Step 3: Retrieve and Verify

**⚠️ TOOL AVAILABILITY CHECK (CRITICAL)**

Before claiming verification, check if the required API/tool is available:

| Source | Tool Available? | If Unavailable |
|--------|-----------------|----------------|
| legislation.gov.uk | ✅ Available via `legislation-intel` CLI | N/A |
| Neo4j pensions DBs | ✅ Available via MCP | Use for pensions domain |
| BAILII | **FUTURE** (not yet integrated) | Provide direct URL, mark UNVERIFIED |

**Using the legislation-intel CLI:**

```bash
# CLI location
~/Projects/45black/claude-agents/tools/legislation_intel.py

# Run with uv (handles dependencies automatically)
uv run legislation_intel.py <command> [options]
```

**If authoritative source API is unavailable:**
1. State explicitly: "**UNVERIFIED** - Manual check required"
2. Provide the direct URL for human verification (e.g., `https://www.legislation.gov.uk/ukpga/1995/26/section/33`)
3. Set confidence to **LOW** regardless of training data certainty
4. Do NOT claim verification based on training data alone

---

**For legislation (using legislation-intel CLI):**

```bash
# 1. Search for legislation by keyword
uv run legislation_intel.py search "Pensions Act trustee duties" --limit 10

# 2. Get specific section text
uv run legislation_intel.py section "ukpga/1995/26/section/33"
uv run legislation_intel.py section "Pensions Act 1995 s33"

# 3. Check if provision is in force
uv run legislation_intel.py status "ukpga/2004/35/section/227"

# 4. Generate proper citation
uv run legislation_intel.py cite "ukpga/1995/26/section/33" --format legal
uv run legislation_intel.py cite "uksi/2005/3378/regulation/4" --format oscola
```

**Verification workflow:**
1. Search legislation.gov.uk for the statute/SI
2. Note the citation format: `[Short Title] [Year] [Chapter/SI Number]`
3. Check if amendments exist (current vs original)
4. Verify the provision is still in force via `status` command

**If CLI unavailable (fallback):**
1. Cite based on training data with explicit caveat
2. Provide direct URL: `https://www.legislation.gov.uk/[type]/[year]/[number]/section/[section]`
3. Mark as: "Citation based on training data - verify at [URL]"

**For regulations (SIs):**
1. Full citation: `The [Name] Regulations [Year] (SI [Year]/[Number])`
2. Example: `The Occupational Pension Schemes (Investment) Regulations 2005 (SI 2005/3378)`

**For case law:**
1. Neutral citation: `[Year] [Court] [Number]`
2. Example: `[2023] UKSC 14`
3. Verify via BAILII or National Archives

### Step 4: Construct Citation

Every legal reference MUST include:

```markdown
**Citation Format:**
- Statute: [Name] [Year], s.[section]([subsection]) — ranges acceptable: s.34-36
- SI: [Name] Regulations [Year] (SI [Year]/[Number]), reg.[number]
- Case: [Case Name] [Neutral Citation]
- Guidance: [Issuing Body], [Document Title] ([Date])

**Example:**
> Trustees must exercise their powers in accordance with their fiduciary duties.
> — Pensions Act 1995, s.33; Imperial Group Pension Trust v Imperial Tobacco [1991] 1 WLR 589
```

### Step 5: Glass Box Audit

Before delivering any legal output, document:

**⚠️ PII REDACTION**: Legal queries frequently contain personal data (names, NI numbers, dates of birth). ALWAYS redact PII from audit logs before storage.

```yaml
reasoning_chain:
  - query: "[PII-REDACTED summary of legal question]"
  - domain: "Legal domain identified"
  - sources_consulted: ["List of authoritative sources checked"]
  - citations_verified: ["Each citation with verification status"]
  - confidence: "HIGH/MEDIUM/LOW with rationale"
  - limitations: "What this advice does NOT cover"
```

---

## Quality Gates

Before producing legal output:

- [ ] **Source Gate**: Every factual claim cites an authoritative source
- [ ] **Citation Gate**: All citations follow correct format and are verifiable
- [ ] **Currency Gate**: Legislation checked for amendments/repeals
- [ ] **Domain Gate**: Output stays within competence of identified domain
- [ ] **Confidence Gate**: Uncertainty explicitly stated, not hidden
- [ ] **Disclaimer Gate**: If advice-like, includes appropriate caveats

---

## Output Templates

### Legislation Summary

```markdown
## [Topic]

### Applicable Legislation
- **Primary**: [Statute/SI with full citation]
- **Secondary**: [Related provisions]

### Key Provisions
1. **[Section/Regulation]**: [Summary of effect]
   > "[Quoted text if short]"
   > — [Citation]

### Current Status
- In force: Yes/No/Partially
- Amendments: [List significant amendments]
- Pending changes: [If any]

### Limitations
This summary covers [scope]. It does not address [exclusions].
```

### Compliance Check

```markdown
## Compliance Assessment: [Topic]

### Requirement
[What the legislation requires]
— [Citation]

### Current State
[Assessment of compliance]

### Evidence
- [Document/fact supporting assessment]

### Gaps Identified
1. [Gap]: [Required action]

### Confidence: [HIGH/MEDIUM/LOW]
[Rationale for confidence level]
```

---

## Anti-Patterns

| Pattern | Why It Fails | Better Approach |
|---------|--------------|-----------------|
| Citing "the Pensions Act" without section | Unverifiable, vague | Always cite specific section |
| Using GitHub repo data as legal source | Not authoritative | Pattern reference only |
| Stating law without citation | Glass Box violation | Always cite source |
| Assuming legislation is current | May be amended/repealed | Verify currency |
| Mixing jurisdictions | Different laws apply | Clarify jurisdiction (UK, E&W, Scotland) |
| Confidence without evidence | Not defensible | State basis for confidence |

---

## Integration Points

### MCP Servers
- `neo4j-apex` — TPR obligations and regulatory requirements
- `neo4j-psps` — LGPS scheme rules
- `neo4j-cms-handbook` — CMS procedural guidance
- `neo4j-scheme-docs` — Scheme-specific documentation

### CLI Tools
- `legislation-intel` CLI — Direct statute retrieval from legislation.gov.uk
  - Location: `~/Projects/45black/claude-agents/tools/legislation_intel.py`
  - Commands: `search`, `section`, `status`, `cite`, `types`, `health`

### External APIs (Future)
- National Archives API — Case law and historical legislation
- BAILII API — Case law search and retrieval

### Compound Output
After completing legal work:
1. Add verified citations to Memory MCP
2. Note any interpretation decisions
3. Flag areas of uncertainty for future research

---

## Examples

For extended worked examples with Glass Box audit trails, see **Tier 3: `verification-reference.md`**:
- Pensions investment query (HIGH confidence)
- Historical employment query (LOW confidence)
- Full YAML audit templates

---

## LangGraph Integration

For `pensions-langgraph-agent` and similar agentic implementations, see **Tier 3: `verification-reference.md`** for:
- Full `LegislationState` TypedDict definition
- `AUTHORITATIVE_SOURCES` configuration
- `verify_sources()` implementation
- Graph construction patterns
