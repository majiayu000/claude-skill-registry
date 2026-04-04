---
name: vkc-regulation-knowledge-updater
description: Build the regulation/knowledge update pipeline (official sources -> snapshots -> structured rulesets/templates -> admin approval -> active). Use for keeping visa rules and document requirements up-to-date without code hardcoding. (키워드= 규정 최신화, 공식 정보, 스냅샷, 검수/승인, 룰셋/템플릿 업데이트)
metadata:
  short-description: Regulation knowledge updater (admin-approved)
---

# VKC Regulation / Knowledge Updater (P2)

## Goal

Keep “규정/서류 요구사항/공식 공지” up-to-date as **data**, not code:

- fetch or ingest updates into snapshots
- detect changes
- require admin approval to activate
- feed active rulesets into visa assessment + doc templates

## Core model (minimum)

- `immigration_sources` (allowlist)
- `immigration_source_snapshots` (hash + fetchedAt + raw text / attachment path)
- `immigration_rulesets` (structured JSON + version + status)

## Admin workflow (required)

- `sync` job writes `pending` snapshots/rulesets
- admin reviews diffs and activates the new version

## Implementation notes (practical)

- Treat “no official API” sources as best-effort:
  - low frequency + caching + allowlist
  - immediate fallback to manual admin upload if unstable
- Scheduler: external cron hits `/api/admin/immigration/sync` (authenticated)

## STEP3 official sources (SoT)

- Source list (A/B/C) and update cadence: `docs/STEP3_SOT_RESOURCES.md`
