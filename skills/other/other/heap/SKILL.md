---
name: heap
description: Analyze user behavior via Heap API. Query events, users, and funnels.
metadata: {"clawdbot":{"emoji":"📈","requires":{"env":["HEAP_APP_ID","HEAP_API_KEY"]}}}
---
# Heap
Product analytics.
## Environment
```bash
export HEAP_APP_ID="xxxxxxxxxx"
export HEAP_API_KEY="xxxxxxxxxx"
```
## Track Event (Server-side)
```bash
curl -X POST "https://heapanalytics.com/api/track" \
  -H "Content-Type: application/json" \
  -d '{"app_id": "'$HEAP_APP_ID'", "identity": "user@example.com", "event": "Purchase", "properties": {"amount": 99}}'
```
## Add User Properties
```bash
curl -X POST "https://heapanalytics.com/api/add_user_properties" \
  -H "Content-Type: application/json" \
  -d '{"app_id": "'$HEAP_APP_ID'", "identity": "user@example.com", "properties": {"plan": "premium"}}'
```
## Query API
```bash
curl "https://heapanalytics.com/api/partner/v1/events?app_id=$HEAP_APP_ID" \
  -H "Authorization: Bearer $HEAP_API_KEY"
```
## Links
- Dashboard: https://heapanalytics.com
- Docs: https://developers.heap.io
