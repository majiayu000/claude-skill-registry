---
name: "mongodb-production-query"
description: "Query Ballee production MongoDB (Meteor app) using .env.local credentials; use when debugging Meteor data, verifying MongoDB documents, investigating sync issues, or exploring legacy data for migration"
version: "1.0.0"
last_updated: "2025-12-07"
---

# MongoDB Production Query Skill

Query the Ballee production MongoDB database (Meteor application) safely using credentials from `.env.local` (with 1Password reference).

## When to Use This Skill

Use this skill when:
- Debugging Meteor/MongoDB data issues
- Verifying MongoDB documents exist before sync
- Investigating Meteor-to-Supabase sync issues
- Exploring legacy data structure for migration planning
- Counting documents in MongoDB collections
- Comparing MongoDB data with Supabase data

## MongoDB Server Reference

| Environment | Host | Database | Auth |
|-------------|------|----------|------|
| **Production** | `mdb-p-{0,1,2}.ballee.db-eu2.zcloud.ws` | `meteor` | `authSource=admin` |

### Connection Details

- **Replica Set**: `mdb-p` (3 nodes)
- **Ports**: 60601, 60602, 60603
- **SSL**: Required (`ssl=true&tlsInsecure=true`)
- **CA Certificate**: `.claude/skills/mongodb-production-query/ca-eu-2.pem`

## Credential Management

### Environment Variable (Primary)

Credentials stored in `apps/web/.env.local`:

```bash
METEOR_MONGO_URL="op://Ballee/MongoDB Production (zCloud)/connection string"
```

### 1Password Reference

| Credential | 1Password Item | Field |
|------------|----------------|-------|
| Connection String | `MongoDB Production (zCloud)` | `connection string` |
| Username | `MongoDB Production (zCloud)` | `username` |
| Password | `MongoDB Production (zCloud)` | `password` |

## Prerequisites

- Node.js with `mongodb` package installed
- Credentials in `.env.local` OR 1Password CLI authenticated (`op whoami`)

## Quick Reference Commands

### Connect via Node.js

```javascript
const { MongoClient } = require('mongodb');

const url = process.env.METEOR_MONGO_URL ||
  'mongodb://root:<password>@mdb-p-0.ballee.db-eu2.zcloud.ws:60601,mdb-p-1.ballee.db-eu2.zcloud.ws:60602,mdb-p-2.ballee.db-eu2.zcloud.ws:60603/meteor?authSource=admin&ssl=true&tlsInsecure=true&replicaSet=mdb-p';

async function connect() {
  const client = new MongoClient(url);
  await client.connect();
  return client.db('meteor');
}
```

### List Collections

```javascript
const db = await connect();
const collections = await db.listCollections().toArray();
console.log(collections.map(c => c.name));
```

### Count Documents

```javascript
const db = await connect();
const count = await db.collection('Organizations').countDocuments();
console.log('Organizations:', count);
```

### Quick Connection Test

```bash
cd /Users/antoineschaller/GitHub/ballee-community-app && node -e "
const { MongoClient } = require('mongodb');
const url = process.env.METEOR_MONGO_URL;
async function test() {
  const client = new MongoClient(url, { serverSelectionTimeoutMS: 10000 });
  await client.connect();
  const db = client.db('meteor');
  const collections = await db.listCollections().toArray();
  console.log('Collections:', collections.map(c => c.name).join(', '));
  await client.close();
}
test().catch(console.error);
"
```

## Available Collections

| Collection | Description | Approx Count |
|------------|-------------|--------------|
| `Organizations` | Dance schools, companies | ~428 |
| `Candidates` | Dancer profiles | ~20,018 |
| `Posts` | Social posts | ~1,492 |
| `Experiences` | Work/education history | varies |
| `Media` | Photos, videos, headshots | varies |
| `Comments` | Post comments | varies |
| `Likes` | Post/comment likes | varies |
| `Follow` | User follows | varies |
| `users` | Meteor auth users | varies |

## Common Queries

### Find Organization by Name

```javascript
const org = await db.collection('Organizations')
  .findOne({ name: /fever/i });
console.log(org);
```

### Find Candidate by Email

```javascript
const candidate = await db.collection('Candidates')
  .findOne({ 'emails.address': 'user@example.com' });
console.log(candidate);
```

### Count Documents by Type

```javascript
const collections = ['Organizations', 'Candidates', 'Posts', 'Experiences', 'Media', 'Comments', 'Likes', 'Follow'];
for (const coll of collections) {
  const count = await db.collection(coll).countDocuments();
  console.log(`${coll}: ${count}`);
}
```

### Sample Document Structure

```javascript
// Get sample document to understand schema
const sample = await db.collection('Candidates').findOne();
console.log(JSON.stringify(sample, null, 2));
```

### Find Recent Documents

```javascript
const recent = await db.collection('Posts')
  .find()
  .sort({ 'meta.createdAt': -1 })
  .limit(10)
  .toArray();
console.log(recent);
```

## Meteor to Supabase Field Mapping

| Meteor Field | Supabase Field | Notes |
|--------------|----------------|-------|
| `_id` | `meteor_id` | Store original ID |
| `meta.createdAt` | `created_at` | Timestamp |
| `meta.modifiedAt` | `updated_at` | Timestamp |
| `name` | `name` | Direct mapping |
| camelCase | snake_case | Transform field names |

## Related Documentation

- Meteor Sync Service: `apps/web/app/admin/sync/meteor/`
- Sync Plan: `.claude/plans/dreamy-wiggling-emerson.md`
- Migration Scripts: `scripts/migration/`
- Airtable Sync Specialist: `.claude/skills/airtable-sync-specialist/SKILL.md`
