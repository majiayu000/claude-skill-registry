---
name: tech-docs-kb
description: Search internal technical documentation, ADRs, RFCs, runbooks, architecture guides, and deployment procedures. Use when the user asks about how services work, project architecture, incident procedures, or development guidelines.
metadata:
  category: knowledge
---

# Tech Docs KB Search

Search technical and architectural documentation using AWS Bedrock Knowledge Base. Provides semantic and hybrid search over the `lightspeed-hospitality/tech-docs` corpus without needing a local clone.

## Trigger

Use this skill when the user asks to:
- Find technical documentation, ADRs, RFCs, runbooks
- Understand service architecture or data flows
- Look up development guidelines or deployment procedures
- Run `/tech-docs`

## Prerequisites & Authentication

- AWS CLI v2 (`brew install awscli`)
- granted CLI (`brew install common-fate/granted/granted`)
- Access to the `lsk/dev/admin/eu-central-1` role

For prerequisite checks and SSO login flow, see `references/auth.md`.

**IMPORTANT:** Do NOT proceed with KB queries until credentials are confirmed working.

## Configuration

| Parameter | Value |
| --- | --- |
| Knowledge Base ID | `S3WJX83IGW` |
| Data Source ID | `5OM2Q7H4CV` |
| Region | `eu-central-1` |
| AWS Profile | `lsk/dev/admin/eu-central-1` |
| S3 Bucket | `s3://tech-docs-knowledge-base` |

**IMPORTANT:** All `aws` commands must include `--profile "lsk/dev/admin/eu-central-1" --region eu-central-1`.

### Indexed Content

| Area | Content |
| --- | --- |
| `Architecture/` | System architecture, fiscalization, data flows, service diagrams |
| `Decision-Records/` | ADRs (0001-0018) and RFCs (0001-0079) |
| `Development/` | Dev workflows, CI/CD, Signadot, deployment tooling, code quality |
| `How-We-Work/` | Team processes, AI PR guidelines, on-call, service ownership |
| `Incidents/` | Incident management, rollback procedures, debugging guides |
| `Infrastructure/` | Kafka, Kubernetes, Elasticsearch, AWS, GCP, DR runbooks |
| `Projects/` | POS, KDS, Fiscalization, AI Assistant, and 20+ other projects |
| `Tutorials/` | How-to guides, datastore selection, and 15+ tutorial topics |
| `Onboarding/` | New employee guides |
| `Learning/` | Learning resources |

**Not indexed:** `/blog` content is intentionally excluded.

## Search the Knowledge Base

### Reformulate the Query

Do NOT pass the user's question verbatim. Extract key nouns and technical terms for HYBRID search:

| User question | Good query |
| --- | --- |
| How does the POS blockchain work? | `POS blockchain device registration key generation block chaining signature verification` |
| Why was GraphQL deprecated? | `GraphQL deprecation ADR REST migration Apollo Federation schema registry` |
| What's the rollback procedure? | `ArgoCD rollback procedure SEV-0 incident revert PR` |

**Strategy:** Include the topic, specific service/tool names, and 2-3 terms you'd expect in the answer document.

### Run the Search

Always default to **HYBRID** search. It outperforms SEMANTIC-only in both precision and token efficiency.

```bash
aws bedrock-agent-runtime retrieve \
  --knowledge-base-id S3WJX83IGW \
  --retrieval-query '{"text": "QUERY"}' \
  --retrieval-configuration '{"vectorSearchConfiguration": {"numberOfResults": 5, "overrideSearchType": "HYBRID"}}' \
  --profile "lsk/dev/admin/eu-central-1" \
  --region eu-central-1 \
  --output json \
  --no-cli-pager
```

| Query type | Search type | Results | When |
| --- | --- | --- | --- |
| Default | `HYBRID` | 5 | Start here |
| Broad/cross-cutting | `HYBRID` | 8 | Answer spans multiple docs |
| Exact doc lookup | `HYBRID` | 3 | "Show me RFC-0063" |
| Fallback (scores < 0.3) | `SEMANTIC` | 8 | Only if HYBRID returns weak results |

For metadata filters and advanced search patterns, see `references/advanced-search.md`.

### Handle Errors

- **ExpiredTokenException / Invalid credentials**: Re-run auth (see `references/auth.md`), then retry
- **AccessDeniedException**: User may not have the required role
- **ThrottlingException**: Wait 3 seconds and retry once

## Parse and Present Results

### Evaluate Result Quality

| Top score | Confidence | Action |
| --- | --- | --- |
| > 0.7 | High | 3-5 results sufficient |
| 0.4 - 0.7 | Medium | Use all results, consider fetching full docs |
| < 0.4 | Low | Reformulate and retry |
| < 0.3 (all) | Very low | KB may not cover this topic |

### Process Results

1. Read chunks from `retrievalResults[].content.text`
2. Extract source paths from `retrievalResults[].location.s3Location.uri` — strip bucket prefix to get repo-relative path
3. For high-relevance results (score >= 0.4), fetch the full document from S3 — see `references/advanced-search.md`
4. Synthesize an answer — do NOT dump raw JSON or chunk text
5. Cite sources with repo-relative file paths

### Presentation Format

```
## [Topic]

[Synthesized answer from retrieved chunks and full documents]

**Sources:**
- `docs/path/to/file.md` — [what this doc covers]
```

## Checklist

- [ ] Verified AWS CLI v2 and active credentials before searching
- [ ] Reformulated the query (extracted key terms, not verbatim)
- [ ] Used HYBRID search as default
- [ ] Actually ran the `aws` command using the Bash tool
- [ ] Evaluated result scores and retried if top score < 0.4
- [ ] Fetched full documents from S3 for high-relevance results
- [ ] Synthesized an answer (not raw dump)
- [ ] Cited source document paths
