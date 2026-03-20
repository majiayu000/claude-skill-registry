---
name: midea-recall-diagnose-playwright
description: Diagnose or 排查 why a `/rag-recall/api/search/keyword` request did not recall an expected doc or FAQ in sit, uat, or prod. Use when the user wants to 排查 keyword 检索漏召回, provides a full keyword request or an existing requestId plus target docId/faqId values, and expects end-to-end troubleshooting through a Playwright-attached browser session, `trace/recordInfo`, ELK `traceTargetIds` logs, and ES ranking or `_explain` checks. Also use when the user asks to fabricate a live keyword request with `traceTargetIds` and then investigate the resulting requestId.
---

# Recall Diagnose Playwright

## Start

- Prefer `playwright-ext` for platform operations.
- Use environment split strategy by default:
  - `sit` / `uat`: local startup evidence first (replay + local execution logs), then `trace/recordInfo` + ELK + ES for cross-check.
  - `prod`: platform evidence first (`trace/recordInfo` + ELK), then ES only when retrieval root cause still needs proof.
- Work against browser sessions that are already logged into the target environment.
- If login is required (for example password/MFA), pause and wait for the user to complete login in the current browser tab, then continue from the same tab.
- Only after the browser session is confirmed logged in and still inaccessible (for example persistent `403`/network denial), allow direct terminal `curl` for `keyword` replay and `trace/recordInfo` fetch with user-provided headers, then continue ELK/ES checks in Playwright.
- For `sit` / `uat`, prefer the ES console entry configured in `references/env-config.example.yaml` (or your local override file).
- Normalize the user input first with `scripts/prepare_diagnosis.py`.
- Read `references/diagnosis-rules.md` before interpreting any stage outcome.
- Read `references/platform-playbooks.md` before opening ELK or the ES console.
- Read `references/env-config.example.yaml` to understand the expected environment resource layout. Prefer a local copy with real URLs when available.

## Accept Inputs

- Accept `env`, `targetType`, and one or more `targetIds`.
- Accept either:
  - a full live request with `headers + body`, or
  - an existing `requestId`.
- Treat `targetType` as `doc` or `faq` only in V1.
- Reject more than 10 target IDs because `traceTargetIds` only supports 10.
- If live request headers are missing, do not infer or guess `appId` / `appChannel`. Mark them as unknown and require user-supplied headers or local-log extraction evidence.

Normalize the input before touching any platform:

```bash
python3 scripts/prepare_diagnosis.py --json '{
  "env": "prod",
  "targetType": "doc",
  "targetIds": ["<targetId>"],
  "request": {
    "headers": {
      "appId": "<required-appId>",
      "appChannel": "<optional-channel>"
    },
    "body": {
      "query": "<query>",
      "topk": 10,
      "conditionFilter": {
        "threshold": 0.45
      }
    }
  }
}'
```

## Run The Workflow

1. Normalize the input.
2. If the user gave a live request, inject a unique `requestId` when missing and always merge `targetIds` into `traceTargetIds` when `conditionFilter` is present.
3. Choose workflow by `env`:
   - `sit` / `uat`: replay request on local startup first and capture local phase evidence (`requestId`, cmp stage, hit/miss, key filters).
   - `prod` or no local runtime available: send live request through logged-in browser session (or use given `requestId`) and continue with trace-first flow.
4. Fetch `trace/recordInfo` and compact immediately with `scripts/compact_trace.py`. Never read the whole payload into context.
5. Use local evidence (`sit` / `uat`) plus compacted `stepList` + ELK (`targetId` first) to identify the **first phase where target is lost**.
6. Report this phase-level conclusion first with minimal key evidence. Do not expand downstream phases by default.
7. If first-lost phase is `full_range_faqTxtRecall` / `full_range_docTxtRecall`, go to ES and replay the real text DSL only.
8. In text-recall ES diagnosis, follow this shortest sequence:
   - check target existence by `targetId` (`knowledge_base_id`/`doc_id`) in the same index alias
   - replay original DSL
   - run contrast replay: `keep filter + remove text must` vs `keep filter + keep text must`
9. If target appears when text must is removed, conclude **query-text match miss (analyzer/minimum_should_match/field scope)**, then use `_explain` only for this target doc.
10. `_explain` and `_analyze` are single-index operations. Never run them on multi-index aliases. Always:
   - find target `_index` first via `_search`
   - run `_explain` / `_analyze` on that concrete `_index`
11. If the user asks "why query did not match", run `_analyze` overlap evidence **on demand** and report:
   - query tokens per analyzer
   - required match threshold per analyzer
   - `max_hit` and `hitAtLeastRequired`
   - `max_hit_items` (`knowledge_point_id` + question text)
12. Enter vector recall diagnosis only when:
   - first-lost phase is vector recall, or
   - text-stage evidence is inconsistent and user explicitly asks for deeper checks.
13. For FAQ retrieval misses, run a simplified-query contrast (`knowTypeList=["FAQ"]`) only when steps above are still insufficient.
14. If user asks for complete text-recall storage for target FAQ/doc, export text fields only (exclude vectors) and present as:
   - common fields
   - deduplicated content block
   - question/variant list with IDs

## ELK Time Window

- Default ELK time window is `now-3d` to `now`.
- Do not expand beyond 3 days unless the user explicitly asks.
- When results are empty, adjust query first, then check whether the request was actually replayed with trace targets.

## Missing Trace Evidence

- If there is no `trace/recordInfo` data or no `TRACE_TARGET_ES` log for the target within 3 days, treat it as **not reproduced with trace**.
- In this case, either:
  - fabricate a replay request that includes `traceTargetIds` and a fresh `requestId`, then send it through the logged-in browser session, or
  - explicitly ask the user to send one replay request and return the required payload.
- For `sit` / `uat`, if local replay already produced stable phase evidence, continue diagnosis with local evidence + ES cross-check even when trace evidence is missing.

## Control Token Usage

- Never dump the raw `trace/recordInfo` response into the conversation.
- Use `scripts/compact_trace.py` in summary mode first.
- Expand only the suspect `cmpId`.
- Strip or summarize vectors, embeddings, large arrays, and large response bodies.
- Prefer `operateMsg`, `cmpId`, `targetUrl`, `hit`, `returnedHitCount`, `totalHitCount`, `threshold`, and rank evidence over full JSON blobs.

Compact the trace before reading details:

```bash
python3 scripts/compact_trace.py --json '<trace record json>'
```

Expand a suspect stage only when needed:

```bash
python3 scripts/compact_trace.py \
  --json '<trace record json>' \
  --expand-step full_range_docTxtRecall
```

## Use Platform Priorities

- `sit` / `uat`: prefer local runtime evidence first, then `trace/recordInfo`, then ELK `traceTargetIds` logs.
- `prod`: prefer `trace/recordInfo` for the first structured read, then ELK `traceTargetIds` logs.
- Default delivery is phase diagnosis plus retrieval root cause when the target is lost in text/vector recall.
- Prefer ES only for retrieval-stage diagnosis:
  - raw recall miss
  - raw recall rank too low
  - score filter or topN suspicion
- Do not query ES when the target is already proven to be lost in `full_range_rerank` or a later final filter.

## Apply Retrieval Rules

- Treat `TRACE_TARGET_ES phase=response hit=false` as the strongest proof that a target is absent from that ES query's returned set.
- In ES console operations, clear `input` and `output` before each DSL run to avoid mixed requests/responses.
- Do not treat `targetBefore=[] targetAfter=[]` alone as proof that the raw ES query missed the target. Those logs can appear after score filtering.
- Always stop at the first proven lost phase. Do not continue to later phases for default diagnosis.
- `_explain` / `_analyze` must run on a concrete `_index`, not on a multi-index alias.
- When the problem is in a retrieval phase, reproduce the original DSL, then check:
  - total hits
  - returned hits
  - target rank
  - target score
  - threshold score
  - `_explain` only if ranking still needs explanation
- If text DSL with target filter returns `0`, do not classify as "low score". It is a **query-match miss** unless evidence shows post-score filtering.
- If `keep filter + remove text must` returns target while `keep filter + keep text must` does not, root cause is text query/analyzer/field scope mismatch.
- Token-overlap (`_analyze`) evidence is optional by default and runs only when user asks for deeper textual mismatch reasons.
- When the problem is in a rerank phase, stay in trace and ELK evidence and report the exact step.

## Report Findings

Return the result in this order:

1. Final phase where the target was lost
2. Short rationale
3. Key evidence from trace or ELK
4. ES ranking evidence only if retrieval was the issue
5. Next action tied to the proven phase

## Resources

- Use `scripts/prepare_diagnosis.py` to normalize live-request and requestId-only inputs.
- Use `scripts/compact_trace.py` to summarize `trace/recordInfo` safely.
- Use `references/diagnosis-rules.md` for the `cmpId -> phase -> action` mapping.
- Use `references/platform-playbooks.md` for Playwright, ELK, and ES operating notes.
- Use `references/env-config.example.yaml` as the environment resource template.
