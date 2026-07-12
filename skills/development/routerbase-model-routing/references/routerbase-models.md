# RouterBase Model Routing Notes

Use this reference when selecting model IDs, checking availability, or documenting routing tradeoffs.

## Source Of Truth

RouterBase docs describe the model list as a snapshot and point users to the live model catalog for the current source of truth. Query the catalog when credentials are available.

```bash
curl "https://routerbase.com/api/v1/models?task=chat" \
  -H "Authorization: Bearer $ROUTERBASE_API_KEY"
```

Useful query params:

- `task`: repeatable modality filter; documented options include `video`, `image`, `audio`, and `chat`.
- `provider`: repeatable provider filter.
- `search`: full-text search across model names and descriptions.
- `page`: one-indexed page number.
- `per_page`: results per page.

Pricing:

```bash
curl "https://routerbase.com/api/v1/models/{model_id}/pricing" \
  -H "Authorization: Bearer $ROUTERBASE_API_KEY"

curl "https://routerbase.com/api/v1/pricing" \
  -H "Authorization: Bearer $ROUTERBASE_API_KEY"
```

## Publicly Documented Model Examples

These examples came from RouterBase docs and should be rechecked before production use:

Chat:

- `openai/gpt-5-2`
- `openai/gpt-5-4`
- `anthropic/claude-haiku-4-5`
- `anthropic/claude-sonnet-4-6`
- `anthropic/claude-opus-4-8`
- `google/gemini-2.5-flash`
- `google/gemini-3-flash-preview`
- `openai/gpt-codex`

Image:

- `google/imagen-4`
- `google/imagen-4-fast`
- `blackforestlabs/flux-2-pro`
- `blackforestlabs/flux-2-pro-i2i`
- `ideogram/ideogram-3-0`

Video:

- `google/veo-3-1-quality`
- `google/veo-3-1-fast`
- `openai/sora-2`
- `xai/grok-imagine`
- `kuaishou/kling-v3-4k-t2v`
- `alibaba/wan-2-7-t2v`

Audio:

- `suno/suno-v5`
- `elevenlabs/tts-turbo`
- `elevenlabs/tts-multilingual`

## Decision Template

Use this table when returning recommendations:

| Use case | Primary model | Fallback | Why | Validate |
| --- | --- | --- | --- | --- |
| Fast chat answer | `google/gemini-2.5-flash` | TBD from catalog | Low-latency starting point | Run 10 representative prompts |
| Tool-using agent | TBD from catalog | TBD from catalog | Needs tool-calling support | Run exact tool schema |
| High-quality long answer | TBD from catalog | TBD from catalog | Needs quality/context over speed | Compare output quality and cost |

## Fallback Rules

- Retry transient network errors, timeouts, `429`, and `5xx` responses with backoff.
- Do not retry invalid keys, invalid model IDs, malformed requests, or policy failures without a code/configuration fix.
- Log model ID, request ID, status code, latency, and token/media cost where available.
- Keep fallback models compatible with the same request shape. A fallback that lacks vision, tools, or JSON mode can break user-visible behavior.

## Prompt Caching Notes

RouterBase docs describe automatic prompt caching for upstream models that support it. To improve cache usefulness:

- Put stable system prompts and tool definitions at the start.
- Put variable user content near the end.
- Use `prompt_cache_key` only when the app intentionally wants to override RouterBase's default partitioning behavior for supported models.
