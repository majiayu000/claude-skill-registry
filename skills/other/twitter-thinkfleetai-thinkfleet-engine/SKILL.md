---
name: twitter
description: "Query Twitter/X — search tweets, get user profiles, timelines, and followers via the API v2."
metadata: {"thinkfleetbot":{"emoji":"🐦","requires":{"bins":["curl","jq"],"env":["TWITTER_BEARER_TOKEN"]}}}
---

# Twitter / X

Search tweets, get user profiles, and query timelines via the Twitter API v2.

## Environment Variables

- `TWITTER_BEARER_TOKEN` - Bearer token

## Search tweets

```bash
curl -s -H "Authorization: Bearer $TWITTER_BEARER_TOKEN" \
  "https://api.twitter.com/2/tweets/search/recent?query=SEARCH_QUERY&max_results=10&tweet.fields=created_at,public_metrics" | jq '.data[] | {id, text, created_at, metrics: .public_metrics}'
```

## Get user profile

```bash
curl -s -H "Authorization: Bearer $TWITTER_BEARER_TOKEN" \
  "https://api.twitter.com/2/users/by/username/USERNAME?user.fields=public_metrics,description" | jq '.data | {id, name, username, description, metrics: .public_metrics}'
```

## Get user timeline

```bash
curl -s -H "Authorization: Bearer $TWITTER_BEARER_TOKEN" \
  "https://api.twitter.com/2/users/USER_ID/tweets?max_results=10&tweet.fields=created_at,public_metrics" | jq '.data[] | {id, text, created_at}'
```

## Notes

- Rate limits apply per endpoint. Check Twitter API docs.
- Read-only with bearer token; posting requires OAuth 1.0a user context.
