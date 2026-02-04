---
name: test-webhook
description: Generate and send test GitHub webhook payloads to the local webhook server.
user-invocable: true
---

You are a webhook testing tool for the claude-code-reviewer project. You generate realistic GitHub webhook payloads and send them to the local server for testing.

## Step 1: Read Configuration

Read `config.yaml` to determine:
- `webhook.port` (default: 3000)
- `webhook.path` (default: /webhook)
- `webhook.secret` (for HMAC signature)
- First repo in `repos[]` (for owner/repo in payloads)

## Step 2: Ask Which Event

Ask the user which webhook event to simulate:

### pull_request events
- **opened** — new PR opened (triggers review)
- **synchronize** — new commits pushed (triggers review)
- **reopened** — closed PR reopened (triggers review)
- **ready_for_review** — draft PR marked ready (triggers review)
- **closed (merged)** — PR merged (lifecycle → merged status)
- **closed (unmerged)** — PR closed without merge (lifecycle → closed status)
- **converted_to_draft** — PR converted to draft (lifecycle → skipped if skipDrafts)
- **edited** — PR title changed (conditional — only triggers if title changed)

### issue_comment events
- **/review trigger** — comment matching the `commentTrigger` regex on a PR (triggers forced re-review). The trigger pattern is configurable in `config.yaml` under `review.commentTrigger` (default: `^\s*/review\s*$`). Read the config to use the actual pattern; default to `/review` as the comment body.

Also ask for a PR number (default: 1).

## Step 3: Generate Payload

Build a JSON payload matching the GitHub webhook format. The payload must match the field access patterns in `src/webhook/server.ts`:

### pull_request event payload structure:
```json
{
  "action": "<action>",
  "pull_request": {
    "number": <N>,
    "title": "Test PR #<N>",
    "draft": false,
    "merged": false,
    "head": { "sha": "<random-hex-40>" },
    "base": { "ref": "main" }
  },
  "repository": {
    "full_name": "<owner>/<repo>"
  }
}
```

Adjust fields per event:
- **closed (merged)**: set `"merged": true` in pull_request
- **converted_to_draft**: set `"draft": true`
- **edited**: add `"changes": { "title": { "from": "Old Title" } }`

### issue_comment event payload structure:
```json
{
  "action": "created",
  "issue": {
    "number": <N>,
    "pull_request": { "url": "https://api.github.com/repos/<owner>/<repo>/pulls/<N>" }
  },
  "comment": {
    "body": "/review",
    "user": { "login": "test-user", "type": "User" }
  },
  "repository": {
    "full_name": "<owner>/<repo>"
  }
}
```

Generate a random 40-character hex string for `head.sha`.

## Step 4: Compute Signature

If `webhook.secret` is configured (non-empty), compute the HMAC-SHA256 signature:

```bash
echo -n '<payload>' | openssl dgst -sha256 -hmac '<secret>'
```

The signature header value is `sha256=<hex-digest>`.

If no secret is configured, skip the signature header.

## Step 5: Send Request

Use curl to send the webhook:

```bash
curl -s -o /dev/null -w "%{http_code}" \
  -X POST \
  -H "Content-Type: application/json" \
  -H "X-GitHub-Event: <event>" \
  -H "X-Hub-Signature-256: sha256=<hmac>" \
  "http://localhost:<port><path>" \
  -d '<payload>'
```

Omit the `X-Hub-Signature-256` header if no secret is configured.

## Step 6: Report Results

Report the HTTP status code and interpret it:
- **202** — Accepted, webhook processed successfully
- **200** — OK, event was received but ignored (untracked repo, ignored action, etc.)
- **401** — Invalid signature (check webhook secret)
- **400** — Bad request (malformed payload)
- **413** — Payload too large
- **404** — Not found (wrong path — verify `webhook.path` in config)
- **Connection refused** — Server not running

## Step 7: (Optional) Verify State

For lifecycle events (closed, merged, converted_to_draft), offer to read `data/state.json` after sending to verify the state was updated correctly. Show the PR's new status.

## Notes

- Always use `localhost` — webhooks are for the local dev server
- Generate a fresh random SHA for each synchronize event to simulate new commits
- The `/review` trigger requires the PR to exist in state (or the server will fetch it via gh CLI)
