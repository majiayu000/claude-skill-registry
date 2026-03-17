---
id: cyfrin-findings
title: Cyfrin/Solodit Findings Database Integration
category: data-source
difficulty: intermediate
triggers:
  - cyfrin findings
  - solodit
  - historical findings
  - audit database
  - past vulnerabilities
  - similar findings
related_skills:
  - variant-analysis/SKILL.md
  - patterns/SKILL.md
tags:
  - cyfrin
  - solodit
  - findings
  - database
version: 1.0.0
last_updated: 2026-02-26
api_base: https://api.solodit.xyz
description: >-
  Query the Cyfrin/Solodit findings database (50,530+ findings from 30+
  audit firms) for vulnerability research, pattern extraction, and audit
  enhancement. Use when searching for historical findings by vulnerability
  type, protocol category, or severity, or when looking for similar bugs
  found in comparable protocols.
---

# Cyfrin/Solodit Findings Database Skill

## Purpose

Query and leverage the Cyfrin/Solodit findings database — the largest aggregated repository of smart contract audit findings — for vulnerability research, pattern extraction, and audit enhancement. This skill provides structured access to historical audit data across the entire Web3 ecosystem.

## Database Statistics

| Metric | Value |
|--------|-------|
| Total findings indexed | 50,530+ |
| Audit firms represented | 30+ (Code4rena, Sherlock, Spearbit, Trail of Bits, OpenZeppelin, ConsenSys Diligence, Cyfrin, Sigma Prime, MixBytes, Cantina, etc.) |
| Protocols covered | 2,844+ |
| Vulnerability categories/tags | 207 |
| Protocol categories | 33 (Lending, DEX, Bridge, Yield, Governance, NFT, Stablecoin, Derivatives, Insurance, etc.) |
| Chains covered | Ethereum, Arbitrum, Optimism, Polygon, BSC, Avalanche, Solana, and more |

## Severity Distribution (Approximate)

Based on the indexed findings:

| Severity | Percentage | Approximate Count |
|----------|------------|-------------------|
| Critical | ~5% | ~2,500 |
| High | ~25% | ~12,600 |
| Medium | ~40% | ~20,200 |
| Low | ~20% | ~10,100 |
| Informational/Gas | ~10% | ~5,050 |

## Top Vulnerability Categories

Ranked by frequency across the entire database:

1. **Access Control** — Unprotected functions, missing role checks, privilege escalation
2. **Input Validation** — Unchecked parameters, missing bounds, zero-address checks
3. **Reentrancy** — Cross-function, cross-contract, read-only reentrancy
4. **Oracle Manipulation** — Price feed manipulation, stale prices, TWAP attacks
5. **Rounding/Precision** — Integer division truncation, share price inflation, dust amounts
6. **Flash Loan Attacks** — Governance manipulation, price oracle attacks, liquidity draining
7. **Front-running/MEV** — Sandwich attacks, transaction ordering dependence
8. **Denial of Service** — Gas griefing, unbounded loops, block stuffing
9. **Logic Errors** — Incorrect state transitions, wrong comparison operators, off-by-one
10. **Token Integration** — Fee-on-transfer, rebasing tokens, non-standard ERC20 behavior

## Capabilities

### Core Query Operations
- **Search by vulnerability type**: Query findings by category tag (e.g., `reentrancy`, `oracle-manipulation`, `access-control`)
- **Search by protocol type**: Filter by protocol category (e.g., lending, DEX, bridge, yield aggregator)
- **Search by severity**: Filter Critical/High/Medium/Low findings
- **Search by chain**: Target chain-specific vulnerabilities (Ethereum, Arbitrum, Optimism, etc.)
- **Search by auditor**: Filter by specific audit firm (Code4rena, Sherlock, Spearbit, etc.)
- **Get specific finding**: Retrieve full details of a finding by its unique ID

### Research Operations
- **Pattern extraction**: Group findings by category to identify recurring vulnerability patterns
- **Protocol benchmarking**: Compare finding density across similar protocols
- **Trend analysis**: Track vulnerability type frequency over time
- **Auditor comparison**: Compare finding distributions across audit firms
- **Historical research**: Study how specific vulnerability classes have evolved

### Audit Enhancement
- **Pre-audit intelligence**: Build targeted checklists from historical findings for the protocol type under review
- **Live code review support**: Query relevant past findings when encountering suspicious patterns during review
- **Report enrichment**: Reference similar historical findings to add credibility and context to audit reports
- **Mitigation validation**: Check whether proposed fixes align with successful remediations in past findings

## API Reference

| Property | Value |
|----------|-------|
| Base URL | `https://api.solodit.xyz` |
| Auth | API key in `X-API-Key` header |
| Rate limit | 100 requests/minute, 10,000 requests/day |
| Response format | JSON |
| Pagination | `page` (default: 1), `per_page` (default: 50, max: 100) |

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/findings` | Search findings with filters (severity, category, chain, protocol) |
| GET | `/findings/:id` | Get a specific finding by ID |
| GET | `/protocols` | List all audited protocols |
| GET | `/categories` | List all vulnerability categories |

See [API Reference](resources/api-reference.md) for full parameter documentation and response schemas.

## Workflows

| Workflow | When to Use |
|----------|-------------|
| [Audit Preparation](workflows/audit-preparation.md) | Before starting an audit — build threat model from historical findings for the protocol type |
| [Code Review Enhancement](workflows/code-review-enhancement.md) | During code review — query past findings when encountering suspicious patterns |
| [Vulnerability Learning](workflows/vulnerability-learning.md) | Study sessions — deep-dive into a vulnerability category with 10+ real examples |
| [Pre-Development Research](workflows/pre-development-research.md) | Before writing smart contract code — learn what goes wrong in similar protocols |

## Resources

| Resource | Purpose |
|----------|---------|
| [API Reference](resources/api-reference.md) | Full endpoint documentation, parameters, response schemas, error codes |
| [Query Templates](resources/query-templates.md) | Ready-to-use query patterns for common research scenarios |
| [Rate Limiting](resources/rate-limiting.md) | Rate limit details, caching strategies, backoff implementation |
| [Response Parsing](resources/response-parsing.md) | How to extract, normalize, and categorize findings from API responses |

## Integration with Other Skills

This skill feeds data into multiple other skills in the system:

| Skill | Integration |
|-------|-------------|
| `patterns/` | Findings data populates vulnerability pattern files (e.g., reentrancy-patterns.md, erc4626-patterns.md) |
| `exploit-forensics/` | Past findings provide forensic case studies for exploit analysis |
| `protocol-playbooks/` | Historical findings for specific protocol types inform playbook checklists |
| `attack-trees/` | Finding severity and frequency data shapes attack tree probability nodes |
| `checklists/` | Top vulnerability categories from findings become checklist items |
| `scoring/` | Finding density by category informs risk scoring weights |

## Quick Start Example

To research vulnerabilities for a **lending protocol** audit:

1. Query: `GET /findings?category=lending&severity=critical&per_page=50`
2. Extract top attack vectors from results (oracle manipulation, liquidation logic, interest rate calculation)
3. Cross-reference with `patterns/oracle-patterns.md` and `patterns/lending-patterns.md`
4. Build targeted checklist using `checklists/` templates
5. During review, query specific patterns: `GET /findings?category=reentrancy&protocol_type=lending`
6. Reference relevant historical findings in audit report

## Data Quality Notes

- Findings are sourced from public audit reports and contest results
- Severity levels are preserved as assigned by the original auditor/judge
- Some findings may be marked as invalid or duplicate in contest platforms — filter accordingly
- Protocol names are normalized but may have variations across different audit firms
- Not all findings include code snippets — some only have descriptions and recommendations
