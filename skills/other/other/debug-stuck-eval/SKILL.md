---
name: debug-stuck-eval
description: Debug stuck Hawk/Inspect AI evaluations. Use when user mentions "stuck eval", "eval not progressing", "eval hanging", "samples not completing", "eval set frozen", "runner stuck", "500 errors in eval", "retry loop", "eval timeout", or asks why an evaluation isn't finishing.
---

## Quick Checklist

1. **Verify auth**: `hawk auth access-token > /dev/null || echo "Run 'hawk login' first"`
2. **Get eval-set-id** from user
3. **Check status**: `hawk status <eval-set-id>` - JSON report with pod state, logs, metrics
4. **View logs**: `hawk logs <eval-set-id>` or `hawk logs -f` for follow mode
5. **List samples**: `hawk list samples <eval-set-id>` - see completion status
6. **Look for error patterns** (see below)
7. **Test API directly** if logs show retries without clear errors

## Error Patterns

| Log Pattern | Meaning | Resolution |
|-------------|---------|------------|
| `Retrying request to /responses` | OpenAI SDK hiding actual error | Test API directly with curl to see real error |
| `500 - Internal server error` | API issue | Download buffer, find failing request, test through middleman AND directly to provider |
| `400 - invalid_request_error` | Token/context limit exceeded | Check message count and model context window |
| `Pod UID mismatch` | Sandbox pod was killed and restarted | No fix needed—sample errored out, Inspect will retry |
| Empty output, `pending: true` | API returned malformed response | Restart eval (buffer resumes) |
| OOMKilled in pod status | Memory exhaustion | Increase pod memory limits |

## Key Techniques

1. **SDK hides errors by design** - The OpenAI SDK hides transient errors during retry backoff. "Retrying request" logs don't show the actual error. Use curl to see real errors.
2. **FAIL-OK patterns are fine** - Alternating failures and successes mean the eval IS progressing. Only worry about consistent FAIL-FAIL-FAIL patterns.
3. **Use S3 for buffer access** - Download `.buffer/` from S3 rather than accessing the runner pod directly.
4. **Read .eval files with inspect_ai** - Use `from inspect_ai.log import read_eval_log` instead of manually extracting zips.

## Test API Directly

Middleman is the auth proxy. If middleman fails but direct provider calls work, it's a middleman issue.

```bash
TOKEN=$(hawk auth access-token)

# Test through middleman
curl --max-time 300 -X POST https://middleman.internal.metr.org/anthropic/v1/messages \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"model": "claude-sonnet-4-20250514", "max_tokens": 100, "messages": [{"role": "user", "content": "Say hello"}]}'

# Test OpenAI-compatible
curl --max-time 300 -X POST https://middleman.internal.metr.org/openai/v1/chat/completions \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"model": "gpt-4o", "messages": [{"role": "user", "content": "Say hello"}], "max_tokens": 100}'
```

## Recovery

```bash
# Delete stuck eval and restart
hawk delete <eval-set-id>
hawk eval-set <config.yaml>
```

The sample buffer in S3 allows Inspect to resume from where it left off (unless you use `--no-resume`).

## HTTP Retry Count

Task progress logs include "HTTP retries: X". High retry counts indicate API instability even while tasks complete.

**Severity:** Retry count × wait time = stuck duration. E.g., 45 retries × 1800s = 22+ hours stuck.

## More Details

See `docs/debugging-stuck-evals.md` for:
- Sample buffer SQL queries
- Detailed API testing examples
- Escalation checklist

## References

- [Inspect AI Model Providers](https://inspect.aisi.org.uk/providers.html) - Model configuration
- [Inspect AI Eval Logs](https://inspect.aisi.org.uk/eval-logs.html) - .eval file format

## Filing Issues

- **Middleman**: https://github.com/metr-middleman/middleman-server/issues
- **Hawk**: Linear issue on Evals Execution team
- **Inspect AI**: https://github.com/UKGovernmentBEIS/inspect_ai/issues
