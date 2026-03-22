---
name: trello
description: "Manage Trello boards, lists, and cards via the REST API."
metadata: {"thinkfleetbot":{"emoji":"📝","requires":{"bins":["curl","jq"],"env":["TRELLO_API_KEY","TRELLO_TOKEN"]}}}
---

# Trello

Manage Trello boards, lists, and cards via the REST API.

## Environment Variables

- `TRELLO_API_KEY` - API key (get at https://trello.com/power-ups/admin)
- `TRELLO_TOKEN` - User token

## List boards

```bash
curl -s "https://api.trello.com/1/members/me/boards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq '.[] | {id, name, url}'
```

## List lists

```bash
curl -s "https://api.trello.com/1/boards/BOARD_ID/lists?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq '.[] | {id, name}'
```

## List cards

```bash
curl -s "https://api.trello.com/1/lists/LIST_ID/cards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq '.[] | {id, name, url, due}'
```

## Create card

```bash
curl -s -X POST "https://api.trello.com/1/cards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"idList":"LIST_ID","name":"New card","desc":"Card description","due":"2025-12-31T12:00:00.000Z"}' | jq '{id, name, url}'
```

## Move card

```bash
curl -s -X PUT "https://api.trello.com/1/cards/CARD_ID?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"idList":"TARGET_LIST_ID"}' | jq '{id, name, idList}'
```

## Add comment

```bash
curl -s -X POST "https://api.trello.com/1/cards/CARD_ID/actions/comments?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"text":"This is a comment."}' | jq '{id, data: .data.text}'
```

## Get board members

```bash
curl -s "https://api.trello.com/1/boards/BOARD_ID/members?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq '.[] | {id, fullName, username}'
```

## Create list

```bash
curl -s -X POST "https://api.trello.com/1/lists?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"New List","idBoard":"BOARD_ID"}' | jq '{id, name}'
```
