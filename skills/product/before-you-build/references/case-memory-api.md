# Case Memory API

Use this only when a remote beforeyoubuild case memory endpoint or an equivalent local case source is available.

Normal skill use does not require an API key. A bearer token is optional and only marks the caller as a verified integration with higher limits.

Before calling a remote endpoint, ask for the user's explicit agreement unless the user already asked to use the case database, case memory, or beforeyoubuild.fyi cases. Briefly tell the user that a minimal idea summary will be sent to beforeyoubuild.fyi to retrieve similar public cases. Do not send secrets, customer names, private financials, private user data, credentials, or confidential unreleased details.

Endpoint:

```text
POST https://api.beforeyoubuild.fyi/api/v1/case-memory/search
```

Request fields:

```json
{
  "idea": "Short idea summary",
  "target_user": "optional",
  "situation": "optional",
  "problem": "optional",
  "current_alternative": "optional",
  "product_type": "optional existing product type",
  "suspected_failure_patterns": ["optional_tag_key"],
  "pricing_model": "optional",
  "language": "en",
  "limit": 3,
  "declared_source": "skill"
}
```

Expected response shape:

```json
{
  "data": {
    "query_id": "uuid",
    "items": [],
    "no_match_reason": null,
    "took_ms": 16
  },
  "error": null
}
```

Expected `data` fields:

- `data.items`: 0 to 3 public cases.
- `data.items[].matched_on`: lightweight match buckets such as `failure_pattern`, `product_type`, `title_or_one_liner`, or `case_detail`.
- `data.items[].matched_terms`: terms that contributed to the match.
- `data.items[].summary`, `target_users`, `problem_statement`, `warnings_for_builders`, `takeaways`, `pre_build_tests`: public facts to use when explaining the analogy.
- `data.no_match_reason`: present when no similar public case is found.
- `data.took_ms`: endpoint processing time in milliseconds.

The endpoint does not generate `why_similar` or `why_different`. The skill must explain similarity and difference from the returned facts, and must still treat the case as historical analogy rather than proof of current market demand.

Use a short timeout and do not retry repeatedly. If the endpoint is unavailable, continue the review without retrieved cases and say so briefly.
