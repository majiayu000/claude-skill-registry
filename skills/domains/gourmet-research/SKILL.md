---
name: gourmet-research
description: Use when creating or updating evidence-based gourmet research outputs for cities (restaurants/cafes/desserts) that require multi-source evidence, standardized scoring, and structured city folders.
---

# Gourmet Research

## Overview
Template-first workflow for traceable, comparable, auditable food recommendations across cities. Keep evidence, scores, and decisions synchronized.

## Core Rules (Non-Negotiable)
- If the user has not specified an **output language**, ask once at project start and record it in `overview.md`.
- Use **gourmet/<city-slug>/** with 6 files: `overview.md`, `inbox.md`, `candidates.md`, `notes.md`, `top-places.md`, `excluded.md`.
- **Never fabricate** sources, ratings, or claims. Use `unknown` when missing.
- Prefer **original-language place names** (not translated) unless the user requests otherwise.
- **Preserve audit trail**: never delete candidates; mark `rejected` and record why in `excluded.md`.
- Default **minimum sources = 4**. If the locale is information-sparse, allow **3** only when you record `evidence: limited` with the reason and attempted sources.

## Template-First Workflow (Summary)
1. **Initialize**: Ask for output language + city, then copy templates from `assets/templates/` into the city folder.
2. **Normalize**: Update language/city placeholders in the copied files before research begins.
2. **Discovery**: Capture raw ideas in `inbox.md`, then move top candidates into `candidates.md` with `status: inbox`.
3. **Evidence**: For each candidate, write a full evidence block in `notes.md` with sources + practical constraints.
4. **Score**: Apply the 50-point rubric and justify each component in `notes.md`.
5. **Decide**: Promote to Top Picks (>=35), Backups (30-34), or reject (<30).
6. **Publish**: Update `top-places.md` and `excluded.md` to match decisions.
7. **Verify**: Ensure no `inbox` statuses remain and required sections exist.

## Ranking Retrieval (When user asks for “highest score”)
Before extracting any “top N” list, **confirm the scope**:
- **Geography**: Okinawa *prefecture* vs *main island only* vs *specific subarea*.
- **Category**: overall vs cuisine category.
- **Source URL**: must match the user’s intent exactly.

**Checklist (must pass):**
1. URL matches the requested scope (prefecture vs category).
2. If “main island only” is required, exclude island subareas (A4705/A4706).
3. Page title confirms the intended ranking.
4. Language modal handled so list items actually render.

If static scraping fails or content is blocked, **use Playwright** to load the page, close the language modal (日本語), and then extract items.

## Evidence & Negative Review Rules
- Sources must include: **Maps + local reviews + guide/editorial + official channel** (where available).
- **Negative review analysis is conditional**: perform a focused negative review pass when risk signals appear in any source.
  - **Risk signals**: repeated service complaints, hygiene/safety concerns, tourist-trap claims, extreme queue issues, inconsistent ratings, unclear hours/reservations.
  - If triggered: add a **Negative reviews** subsection in `notes.md`, adjust Risk/Consistency/Value as needed, and sync scores/status across files.

## Locale-Specific Source Suggestions (Optional)
| Locale | Local reviews | Aggregator | Guides/editorial |
| --- | --- | --- | --- |
| Japan | Tabelog, Retty | Google Maps | Michelin, local food media |
| Korea | Naver Map, Kakao Map | Google Maps | Michelin, local food media |
| Taiwan | Google Maps, iPeen | OpenRice | Local food media |
| Hong Kong | OpenRice | Google Maps | Michelin, local food media |
| Singapore | OpenRice | Google Maps | Michelin, local food media |
| Europe | Google Maps | Tripadvisor | Michelin, local city guides |
| North America | Google Maps, Yelp | Tripadvisor | Eater, local food media |
| Latin America | Google Maps | Tripadvisor | Local city guides |
| SEA (general) | Google Maps | Tripadvisor | Local food media |

## Scoring (50-Point Rubric)
- Taste/Quality (0-10)
- Value (0-10)
- Convenience (0-10)
- Consistency (0-10)
- Risk (0-10, higher = lower risk)

Thresholds:
- **Top Picks**: >=35
- **Backups**: 30-34
- **Reject**: <30 (or hard exclusion: hygiene/safety/tourist-trap evidence)

## Roles (Optional, Compact)
- **Research**: find sources + capture evidence.
- **Verify**: resolve conflicts, confirm practical constraints.
- **Score**: apply rubric + justify.
- **Synthesize**: finalize top-places + dining strategy.

## Quick Reference
| Item | Rule |
| --- | --- |
| City path | `gourmet/<city-slug>/` |
| Files | overview/inbox/candidates/notes/top-places/excluded |
| Min sources | 4 (3 only with `evidence: limited`) |
| Output language | Ask if not specified |
| Place names | Prefer original language |
| Score tiers | >=35 Top, 30-34 Backup, <30 Reject |

## Example (Evidence Block)
```markdown
### Sakura Teahouse
**Official**: https://example.com
**Maps**: 4.4/5 (820 reviews) - https://maps.app.goo.gl/...
**Local reviews**: 3.7/5 (420 reviews) - https://tabelog.com/...
**Guide/editorial**: https://guide.example.com/...
**Notes**: quiet seating, popular seasonal desserts
**Practical**: reservations recommended, closed Tue
**Score**: Taste 8 / Value 7 / Convenience 6 / Consistency 7 / Risk 7 = **35/50**
```

## Common Mistakes
- Skipping templates and mixing content across files.
- Skipping `inbox.md` and dumping raw ideas into candidates.
- Translating place names instead of using the original language.
- Using only one review platform.
- Pulling the wrong ranking scope (category vs overall, islands included).
- Changing scores without updating candidates/top-places/excluded.
- Ignoring unclear hours or reservation policies.

## Rationalization Table
| Excuse | Reality |
| --- | --- |
| "It’s just one city; I can skip templates." | Templates prevent drift and keep outputs comparable. |
| "Inbox is optional; I can put everything in candidates." | `inbox.md` keeps raw capture separate and reduces noise. |
| "There aren’t 4 sources; I’ll guess." | Use `unknown` and mark `evidence: limited`. Never guess. |
| "I’ll translate names for clarity." | Keep original-language names unless the user asks. |
| "This ranking page is close enough." | Scope mismatch invalidates the answer. Confirm URL and geography. |
| "Negative reviews are optional." | Required when risk signals appear. |

## Red Flags — Stop and Fix
- Candidates deleted instead of rejected.
- Scores updated in notes but not in candidates/top-places.
- Missing output language decision.
- Uncited claims or ratings.

## References
- `references/repo-spec.md`
- `assets/templates/`
