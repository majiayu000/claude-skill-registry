---
name: firebase
description: "Manage Firebase — Firestore documents, Realtime Database, and Auth users via the REST API."
metadata: {"thinkfleetbot":{"emoji":"🔥","requires":{"bins":["curl","jq"],"env":["FIREBASE_PROJECT_ID","GOOGLE_ACCESS_TOKEN"]}}}
---

# Firebase

Manage Firestore, Realtime Database, and Auth.

## Environment Variables

- `FIREBASE_PROJECT_ID` - Firebase project ID
- `GOOGLE_ACCESS_TOKEN` - OAuth access token

## List Firestore documents

```bash
curl -s -H "Authorization: Bearer $GOOGLE_ACCESS_TOKEN" \
  "https://firestore.googleapis.com/v1/projects/$FIREBASE_PROJECT_ID/databases/(default)/documents/COLLECTION?pageSize=10" | jq '.documents[] | {name, fields}'
```

## Get Firestore document

```bash
curl -s -H "Authorization: Bearer $GOOGLE_ACCESS_TOKEN" \
  "https://firestore.googleapis.com/v1/projects/$FIREBASE_PROJECT_ID/databases/(default)/documents/COLLECTION/DOC_ID" | jq '{name, fields}'
```

## List Auth users

```bash
curl -s -X POST -H "Authorization: Bearer $GOOGLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "https://identitytoolkit.googleapis.com/v1/projects/$FIREBASE_PROJECT_ID/accounts:batchGet?maxResults=10" | jq '.users[] | {localId, email, displayName}'
```

## Read Realtime Database

```bash
curl -s "$FIREBASE_PROJECT_ID.firebaseio.com/path.json?auth=$GOOGLE_ACCESS_TOKEN" | jq '.'
```

## Notes

- Always confirm before writing or deleting data.
