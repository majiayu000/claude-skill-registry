---
name: mongodb-atlas
description: MongoDB Atlas cloud database management including clusters, schemas, aggregation pipelines, and Prisma ORM integration. Activate for MongoDB queries, schema design, indexing, and Atlas administration.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - WebFetch
---

# MongoDB Atlas Skill

Provides comprehensive MongoDB and MongoDB Atlas capabilities for the Alpha Members Platform.

## When to Use This Skill

Activate this skill when working with:
- MongoDB query development
- Schema design and modeling
- Aggregation pipelines
- Index optimization
- Prisma MongoDB integration
- Atlas cluster management
- Database performance tuning

## Quick Reference

### Docker Commands
```bash
# Start local MongoDB
docker-compose up mongodb -d

# Connect to MongoDB shell
docker exec -it mongodb mongosh -u root -p rootpassword

# Check MongoDB logs
docker logs mongodb -f --tail=100
```

### MongoDB Shell Commands
```javascript
// Switch to database
use member_db

// List collections
show collections

// Find documents
db.members.find({ status: "ACTIVE" }).limit(10)

// Insert document
db.members.insertOne({ email: "test@example.com", status: "PENDING" })

// Update document
db.members.updateOne(
  { email: "test@example.com" },
  { $set: { status: "ACTIVE" } }
)

// Aggregation
db.members.aggregate([
  { $match: { status: "ACTIVE" } },
  { $group: { _id: "$profile.company", count: { $sum: 1 } } }
])
```

### Connection Strings
```bash
# Local Docker
mongodb://root:rootpassword@localhost:27017/member_db?authSource=admin

# Atlas (example)
mongodb+srv://user:password@cluster.mongodb.net/member_db?retryWrites=true&w=majority
```

## Schema Design

### Prisma MongoDB Schema
```prisma
datasource db {
  provider = "mongodb"
  url      = env("DATABASE_URL")
}

model Member {
  id              String          @id @default(auto()) @map("_id") @db.ObjectId
  keycloakUserId  String          @unique
  email           String          @unique
  firstName       String
  lastName        String
  status          MemberStatus    @default(PENDING)
  profile         MemberProfile?  // Embedded
  addresses       MemberAddress[] // Embedded array
  memberships     Membership[]    // Relation
  createdAt       DateTime        @default(now())
  updatedAt       DateTime        @updatedAt

  @@index([status])
  @@index([email])
}

type MemberProfile {
  jobTitle    String?
  company     String?
  timezone    String  @default("UTC")
}

type MemberAddress {
  type        AddressType
  street1     String
  city        String
  state       String
  postalCode  String
}
```

## Collections

### members
```javascript
{
  _id: ObjectId("..."),
  keycloakUserId: "uuid",
  email: "user@example.com",
  firstName: "John",
  lastName: "Doe",
  status: "ACTIVE",
  profile: {
    jobTitle: "Engineer",
    company: "Acme Corp"
  },
  addresses: [
    { type: "HOME", street1: "123 Main St", ... }
  ],
  createdAt: ISODate("..."),
  updatedAt: ISODate("...")
}
```

### memberships
```javascript
{
  _id: ObjectId("..."),
  memberId: ObjectId("..."),
  type: "INDIVIDUAL",
  level: "PREMIUM",
  status: "ACTIVE",
  startDate: ISODate("..."),
  payment: {
    method: "card",
    amount: 99.99,
    currency: "USD"
  }
}
```

### member_activities
```javascript
{
  _id: ObjectId("..."),
  memberId: ObjectId("..."),
  action: "LOGIN",
  category: "AUTH",
  ipAddress: "192.168.1.1",
  createdAt: ISODate("...")
}
```

## Indexing

### Recommended Indexes
```javascript
// Members collection
db.members.createIndex({ keycloakUserId: 1 }, { unique: true })
db.members.createIndex({ email: 1 }, { unique: true })
db.members.createIndex({ status: 1, createdAt: -1 })
db.members.createIndex({ "profile.company": 1 })

// Text search
db.members.createIndex({
  firstName: "text",
  lastName: "text",
  email: "text",
  "profile.company": "text"
})

// Memberships
db.memberships.createIndex({ memberId: 1 })
db.memberships.createIndex({ status: 1, endDate: 1 })

// Activities (with TTL)
db.member_activities.createIndex({ memberId: 1, createdAt: -1 })
db.member_activities.createIndex(
  { createdAt: 1 },
  { expireAfterSeconds: 31536000 } // 1 year TTL
)
```

## Aggregation Pipelines

### Member Statistics
```javascript
db.members.aggregate([
  { $facet: {
      byStatus: [
        { $group: { _id: "$status", count: { $sum: 1 } } }
      ],
      byMonth: [
        { $group: {
            _id: { $dateToString: { format: "%Y-%m", date: "$createdAt" } },
            count: { $sum: 1 }
          }
        },
        { $sort: { _id: 1 } }
      ],
      total: [{ $count: "count" }]
    }
  }
])
```

### Member with Memberships
```javascript
db.members.aggregate([
  { $match: { _id: ObjectId("...") } },
  { $lookup: {
      from: "memberships",
      localField: "_id",
      foreignField: "memberId",
      as: "memberships"
    }
  }
])
```

## Prisma Operations

```typescript
// Find member
const member = await prisma.member.findUnique({
  where: { email: "user@example.com" },
  include: { memberships: true }
});

// Create member with embedded profile
const newMember = await prisma.member.create({
  data: {
    email: "new@example.com",
    firstName: "Jane",
    lastName: "Doe",
    keycloakUserId: "uuid",
    profile: {
      jobTitle: "Manager",
      company: "Acme"
    }
  }
});

// Update with push to array
const updated = await prisma.member.update({
  where: { id: "..." },
  data: {
    addresses: {
      push: {
        type: "WORK",
        street1: "456 Office Blvd",
        city: "Boston",
        state: "MA",
        postalCode: "02102"
      }
    }
  }
});

// Aggregation with Prisma
const stats = await prisma.member.groupBy({
  by: ['status'],
  _count: true
});
```

## Performance Optimization

### Query Optimization
```javascript
// Use projection to limit returned fields
db.members.find(
  { status: "ACTIVE" },
  { firstName: 1, lastName: 1, email: 1 }
)

// Use covered queries
db.members.find(
  { email: "user@example.com" },
  { _id: 0, email: 1, status: 1 }
).hint({ email: 1, status: 1 })

// Explain query plan
db.members.find({ status: "ACTIVE" }).explain("executionStats")
```

### Index Analysis
```javascript
// Get index usage stats
db.members.aggregate([{ $indexStats: {} }])

// Find unused indexes
db.members.aggregate([
  { $indexStats: {} },
  { $match: { "accesses.ops": 0 } }
])
```

## Atlas CLI Commands

```bash
# Login to Atlas
atlas auth login

# List clusters
atlas clusters list --projectId <projectId>

# Create cluster
atlas clusters create alpha-dev \
  --projectId <projectId> \
  --provider AWS \
  --region US_EAST_1 \
  --tier M10

# Get connection string
atlas clusters connectionStrings describe alpha-dev
```

## Project Files

- Prisma Schema: `prisma/schema.prisma`
- MongoDB Init: `infrastructure/mongo-init/01-init-db.js`
- Docker: `docker/docker-compose.yml` (mongodb service)

## Related Agents

- **mongodb-atlas-admin** - Cluster management
- **mongodb-schema-designer** - Schema design
- **mongodb-query-optimizer** - Performance tuning
- **mongodb-aggregation-specialist** - Complex queries

## Troubleshooting

```bash
# Check MongoDB connection
docker exec mongodb mongosh --eval "db.adminCommand('ping')"

# Check replication status
docker exec mongodb mongosh --eval "rs.status()"

# Analyze slow queries
db.setProfilingLevel(1, { slowms: 100 })
db.system.profile.find().sort({ millis: -1 }).limit(10)
```
