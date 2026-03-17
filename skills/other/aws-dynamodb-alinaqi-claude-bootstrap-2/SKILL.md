---
name: aws-dynamodb
description: AWS DynamoDB single-table design, GSI patterns, SDK v3 TypeScript/Python
---

# AWS DynamoDB Skill

*Load with: base.md + [typescript.md | python.md]*

DynamoDB is a fully managed NoSQL database designed for single-digit millisecond performance at any scale. Master single-table design and access pattern modeling.

**Sources:** [DynamoDB Docs](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/) | [SDK v3](https://docs.aws.amazon.com/AWSJavaScriptSDK/v3/latest/client/dynamodb/) | [Best Practices](https://aws.amazon.com/blogs/database/single-table-vs-multi-table-design-in-amazon-dynamodb/)

---

## Core Principle

**Design for access patterns, not entities. Think access-pattern-first.**

DynamoDB requires you to know your queries before designing your schema. Model around how you'll access data, not how data relates. Single-table design stores multiple entity types in one table using generic key attributes.

---

## Key Concepts

| Concept | Description |
|---------|-------------|
| **Partition Key (PK)** | Primary key attribute - determines data distribution |
| **Sort Key (SK)** | Optional secondary key for range queries within partition |
| **GSI** | Global Secondary Index - alternate partition/sort keys |
| **LSI** | Local Secondary Index - same partition, different sort |
| **Item** | Single record (max 400 KB) |
| **Attribute** | Field within an item |

---

## Single-Table Design

### Why Single Table?
- Fetch related data in single query
- Reduce round trips and costs
- Enable transactions across entity types
- Simplify operations (backup, restore, IAM)

### Generic Key Pattern
```typescript
// Instead of entity-specific keys:
// userId, orderId, productId

// Use generic keys that work for all entities:
interface BaseItem {
  PK: string;   // Partition Key
  SK: string;   // Sort Key
  GSI1PK?: string;  // First GSI partition key
  GSI1SK?: string;  // First GSI sort key
  EntityType: string;
  // ... entity-specific attributes
}
```

### Example: E-commerce Schema
```typescript
// Users
{ PK: 'USER#123', SK: 'PROFILE', EntityType: 'User', name: 'John', email: 'john@test.com' }
{ PK: 'USER#123', SK: 'ADDRESS#1', EntityType: 'Address', street: '123 Main', city: 'NYC' }

// Orders for user (1:N relationship)
{ PK: 'USER#123', SK: 'ORDER#2024-001', EntityType: 'Order', total: 99.99, status: 'shipped' }
{ PK: 'USER#123', SK: 'ORDER#2024-002', EntityType: 'Order', total: 49.99, status: 'pending' }

// Order details (query by order ID using GSI)
{ PK: 'USER#123', SK: 'ORDER#2024-001', GSI1PK: 'ORDER#2024-001', GSI1SK: 'ORDER', ... }
{ PK: 'ORDER#2024-001', SK: 'ITEM#1', GSI1PK: 'ORDER#2024-001', GSI1SK: 'ITEM#1', productId: 'PROD#456', qty: 2 }

// Products
{ PK: 'PROD#456', SK: 'PRODUCT', EntityType: 'Product', name: 'Widget', price: 29.99 }
```

### Access Patterns Covered
```
1. Get user profile          → Query PK='USER#123', SK='PROFILE'
2. Get user with addresses   → Query PK='USER#123', SK begins_with 'ADDRESS'
3. Get all user orders       → Query PK='USER#123', SK begins_with 'ORDER'
4. Get order by ID           → Query GSI1, PK='ORDER#2024-001'
5. Get order with items      → Query GSI1, PK='ORDER#2024-001'
6. Get product details       → Query PK='PROD#456', SK='PRODUCT'
```

---

## SDK v3 Setup (TypeScript)

### Install Dependencies
```bash
npm install @aws-sdk/client-dynamodb @aws-sdk/lib-dynamodb
```

### Client Configuration
```typescript
// lib/dynamodb.ts
import { DynamoDBClient } from '@aws-sdk/client-dynamodb';
import { DynamoDBDocumentClient } from '@aws-sdk/lib-dynamodb';

const client = new DynamoDBClient({
  region: process.env.AWS_REGION || 'us-east-1',
  // For local development with DynamoDB Local
  ...(process.env.DYNAMODB_LOCAL && {
    endpoint: 'http://localhost:8000',
    credentials: { accessKeyId: 'local', secretAccessKey: 'local' }
  })
});

// Document client for simplified operations
export const docClient = DynamoDBDocumentClient.from(client, {
  marshallOptions: {
    removeUndefinedValues: true,  // Important: match v2 behavior
    convertClassInstanceToMap: true
  },
  unmarshallOptions: {
    wrapNumbers: false
  }
});

export const TABLE_NAME = process.env.DYNAMODB_TABLE || 'MyTable';
```

### Type Definitions
```typescript
// types/dynamodb.ts
export interface BaseItem {
  PK: string;
  SK: string;
  GSI1PK?: string;
  GSI1SK?: string;
  EntityType: string;
  createdAt: string;
  updatedAt: string;
}

export interface User extends BaseItem {
  EntityType: 'User';
  userId: string;
  email: string;
  name: string;
}

export interface Order extends BaseItem {
  EntityType: 'Order';
  orderId: string;
  userId: string;
  total: number;
  status: 'pending' | 'paid' | 'shipped' | 'delivered';
}

// Key builders
export const keys = {
  user: (userId: string) => ({
    PK: `USER#${userId}`,
    SK: 'PROFILE'
  }),
  userOrders: (userId: string) => ({
    PK: `USER#${userId}`,
    SKPrefix: 'ORDER#'
  }),
  order: (userId: string, orderId: string) => ({
    PK: `USER#${userId}`,
    SK: `ORDER#${orderId}`,
    GSI1PK: `ORDER#${orderId}`,
    GSI1SK: 'ORDER'
  })
};
```

---

## CRUD Operations

### Put Item (Create/Update)
```typescript
import { PutCommand } from '@aws-sdk/lib-dynamodb';
import { docClient, TABLE_NAME } from './dynamodb';
import { User, keys } from './types';

async function createUser(userId: string, data: { email: string; name: string }): Promise<User> {
  const now = new Date().toISOString();
  const item: User = {
    ...keys.user(userId),
    EntityType: 'User',
    userId,
    email: data.email,
    name: data.name,
    createdAt: now,
    updatedAt: now
  };

  await docClient.send(new PutCommand({
    TableName: TABLE_NAME,
    Item: item,
    ConditionExpression: 'attribute_not_exists(PK)'  // Prevent overwrite
  }));

  return item;
}
```

### Get Item (Read)
```typescript
import { GetCommand } from '@aws-sdk/lib-dynamodb';

async function getUser(userId: string): Promise<User | null> {
  const result = await docClient.send(new GetCommand({
    TableName: TABLE_NAME,
    Key: keys.user(userId)
  }));

  return (result.Item as User) || null;
}
```

### Query (List/Search)
```typescript
import { QueryCommand } from '@aws-sdk/lib-dynamodb';

// Get all orders for a user
async function getUserOrders(userId: string): Promise<Order[]> {
  const result = await docClient.send(new QueryCommand({
    TableName: TABLE_NAME,
    KeyConditionExpression: 'PK = :pk AND begins_with(SK, :sk)',
    ExpressionAttributeValues: {
      ':pk': `USER#${userId}`,
      ':sk': 'ORDER#'
    },
    ScanIndexForward: false  // Newest first
  }));

  return (result.Items as Order[]) || [];
}

// Query GSI by order ID
async function getOrderById(orderId: string): Promise<Order | null> {
  const result = await docClient.send(new QueryCommand({
    TableName: TABLE_NAME,
    IndexName: 'GSI1',
    KeyConditionExpression: 'GSI1PK = :pk',
    ExpressionAttributeValues: {
      ':pk': `ORDER#${orderId}`
    }
  }));

  return (result.Items?.[0] as Order) || null;
}

// Paginated query
async function getUserOrdersPaginated(
  userId: string,
  pageSize: number = 20,
  lastKey?: Record<string, any>
): Promise<{ items: Order[]; lastKey?: Record<string, any> }> {
  const result = await docClient.send(new QueryCommand({
    TableName: TABLE_NAME,
    KeyConditionExpression: 'PK = :pk AND begins_with(SK, :sk)',
    ExpressionAttributeValues: {
      ':pk': `USER#${userId}`,
      ':sk': 'ORDER#'
    },
    Limit: pageSize,
    ExclusiveStartKey: lastKey
  }));

  return {
    items: (result.Items as Order[]) || [],
    lastKey: result.LastEvaluatedKey
  };
}
```

### Update Item
```typescript
import { UpdateCommand } from '@aws-sdk/lib-dynamodb';

async function updateUser(userId: string, updates: Partial<Pick<User, 'name' | 'email'>>): Promise<User> {
  // Build update expression dynamically
  const updateParts: string[] = ['#updatedAt = :updatedAt'];
  const names: Record<string, string> = { '#updatedAt': 'updatedAt' };
  const values: Record<string, any> = { ':updatedAt': new Date().toISOString() };

  if (updates.name !== undefined) {
    updateParts.push('#name = :name');
    names['#name'] = 'name';
    values[':name'] = updates.name;
  }

  if (updates.email !== undefined) {
    updateParts.push('#email = :email');
    names['#email'] = 'email';
    values[':email'] = updates.email;
  }

  const result = await docClient.send(new UpdateCommand({
    TableName: TABLE_NAME,
    Key: keys.user(userId),
    UpdateExpression: `SET ${updateParts.join(', ')}`,
    ExpressionAttributeNames: names,
    ExpressionAttributeValues: values,
    ReturnValues: 'ALL_NEW',
    ConditionExpression: 'attribute_exists(PK)'  // Must exist
  }));

  return result.Attributes as User;
}

// Atomic counter increment
async function incrementOrderCount(userId: string): Promise<void> {
  await docClient.send(new UpdateCommand({
    TableName: TABLE_NAME,
    Key: keys.user(userId),
    UpdateExpression: 'SET orderCount = if_not_exists(orderCount, :zero) + :inc',
    ExpressionAttributeValues: {
      ':zero': 0,
      ':inc': 1
    }
  }));
}
```

### Delete Item
```typescript
import { DeleteCommand } from '@aws-sdk/lib-dynamodb';

async function deleteUser(userId: string): Promise<void> {
  await docClient.send(new DeleteCommand({
    TableName: TABLE_NAME,
    Key: keys.user(userId),
    ConditionExpression: 'attribute_exists(PK)'
  }));
}
```

---

## Batch Operations

### Batch Write (Up to 25 items)
```typescript
import { BatchWriteCommand } from '@aws-sdk/lib-dynamodb';

async function batchCreateItems(items: BaseItem[]): Promise<void> {
  // DynamoDB allows max 25 items per batch
  const chunks = [];
  for (let i = 0; i < items.length; i += 25) {
    chunks.push(items.slice(i, i + 25));
  }

  for (const chunk of chunks) {
    await docClient.send(new BatchWriteCommand({
      RequestItems: {
        [TABLE_NAME]: chunk.map(item => ({
          PutRequest: { Item: item }
        }))
      }
    }));
  }
}
```

### Batch Get (Up to 100 items)
```typescript
import { BatchGetCommand } from '@aws-sdk/lib-dynamodb';

async function batchGetUsers(userIds: string[]): Promise<User[]> {
  const result = await docClient.send(new BatchGetCommand({
    RequestItems: {
      [TABLE_NAME]: {
        Keys: userIds.map(id => keys.user(id))
      }
    }
  }));

  return (result.Responses?.[TABLE_NAME] as User[]) || [];
}
```

---

## Transactions

### TransactWrite (Atomic Multi-Item)
```typescript
import { TransactWriteCommand } from '@aws-sdk/lib-dynamodb';

async function createOrderWithItems(
  userId: string,
  orderId: string,
  orderData: { total: number },
  items: { productId: string; quantity: number }[]
): Promise<void> {
  const now = new Date().toISOString();

  const transactItems = [
    // Create order
    {
      Put: {
        TableName: TABLE_NAME,
        Item: {
          ...keys.order(userId, orderId),
          EntityType: 'Order',
          orderId,
          userId,
          total: orderData.total,
          status: 'pending',
          createdAt: now,
          updatedAt: now
        },
        ConditionExpression: 'attribute_not_exists(PK)'
      }
    },
    // Update user's order count
    {
      Update: {
        TableName: TABLE_NAME,
        Key: keys.user(userId),
        UpdateExpression: 'SET orderCount = if_not_exists(orderCount, :zero) + :inc',
        ExpressionAttributeValues: { ':zero': 0, ':inc': 1 }
      }
    },
    // Add order items
    ...items.map((item, index) => ({
      Put: {
        TableName: TABLE_NAME,
        Item: {
          PK: `ORDER#${orderId}`,
          SK: `ITEM#${index}`,
          GSI1PK: `ORDER#${orderId}`,
          GSI1SK: `ITEM#${index}`,
          EntityType: 'OrderItem',
          productId: item.productId,
          quantity: item.quantity,
          createdAt: now
        }
      }
    }))
  ];

  await docClient.send(new TransactWriteCommand({
    TransactItems: transactItems
  }));
}
```

---

## GSI Patterns

### Sparse Index
```typescript
// Only items with GSI1PK attribute appear in the index
// Useful for "featured" or "flagged" items

// Featured products (only some products have GSI1PK)
{ PK: 'PROD#1', SK: 'PRODUCT', GSI1PK: 'FEATURED', GSI1SK: 'PROD#1', ... }  // In index
{ PK: 'PROD#2', SK: 'PRODUCT', ... }  // Not in index (no GSI1PK)

// Query featured products
const featured = await docClient.send(new QueryCommand({
  TableName: TABLE_NAME,
  IndexName: 'GSI1',
  KeyConditionExpression: 'GSI1PK = :pk',
  ExpressionAttributeValues: { ':pk': 'FEATURED' }
}));
```

### Inverted Index (GSI)
```typescript
// Main table: User -> Orders (PK=USER#, SK=ORDER#)
// GSI: Orders by status (GSI1PK=STATUS#, GSI1SK=ORDER#)

{ PK: 'USER#123', SK: 'ORDER#001', GSI1PK: 'STATUS#pending', GSI1SK: 'ORDER#001', ... }
{ PK: 'USER#456', SK: 'ORDER#002', GSI1PK: 'STATUS#shipped', GSI1SK: 'ORDER#002', ... }

// Get all pending orders across all users
const pending = await docClient.send(new QueryCommand({
  TableName: TABLE_NAME,
  IndexName: 'GSI1',
  KeyConditionExpression: 'GSI1PK = :pk',
  ExpressionAttributeValues: { ':pk': 'STATUS#pending' }
}));
```

### Multi-Attribute Composite Keys (Nov 2025+)
```typescript
// New feature: Up to 4 attributes per partition/sort key
// No more synthetic keys like "TOURNAMENT#WINTER2024#REGION#NA-EAST"

// Table definition (IaC)
const table = {
  AttributeDefinitions: [
    { AttributeName: 'tournament', AttributeType: 'S' },
    { AttributeName: 'region', AttributeType: 'S' },
    { AttributeName: 'score', AttributeType: 'N' }
  ],
  GlobalSecondaryIndexes: [{
    IndexName: 'TournamentRegionIndex',
    KeySchema: [
      { AttributeName: 'tournament', KeyType: 'HASH' },  // Composite PK part 1
      { AttributeName: 'region', KeyType: 'HASH' },      // Composite PK part 2
      { AttributeName: 'score', KeyType: 'RANGE' }
    ]
  }]
};
```

---

## Python (boto3)

### Setup
```python
# requirements.txt
boto3>=1.34.0

# db.py
import boto3
from boto3.dynamodb.conditions import Key, Attr
import os

dynamodb = boto3.resource(
    'dynamodb',
    region_name=os.getenv('AWS_REGION', 'us-east-1'),
    endpoint_url=os.getenv('DYNAMODB_LOCAL_ENDPOINT')  # For local dev
)

table = dynamodb.Table(os.getenv('DYNAMODB_TABLE', 'MyTable'))
```

### Operations
```python
from datetime import datetime
from typing import Optional, List
from decimal import Decimal

def create_user(user_id: str, email: str, name: str) -> dict:
    now = datetime.utcnow().isoformat()
    item = {
        'PK': f'USER#{user_id}',
        'SK': 'PROFILE',
        'EntityType': 'User',
        'userId': user_id,
        'email': email,
        'name': name,
        'createdAt': now,
        'updatedAt': now
    }

    table.put_item(
        Item=item,
        ConditionExpression='attribute_not_exists(PK)'
    )
    return item


def get_user(user_id: str) -> Optional[dict]:
    response = table.get_item(
        Key={'PK': f'USER#{user_id}', 'SK': 'PROFILE'}
    )
    return response.get('Item')


def get_user_orders(user_id: str) -> List[dict]:
    response = table.query(
        KeyConditionExpression=Key('PK').eq(f'USER#{user_id}') & Key('SK').begins_with('ORDER#'),
        ScanIndexForward=False
    )
    return response.get('Items', [])


def update_user(user_id: str, **updates) -> dict:
    update_parts = ['#updatedAt = :updatedAt']
    names = {'#updatedAt': 'updatedAt'}
    values = {':updatedAt': datetime.utcnow().isoformat()}

    for key, value in updates.items():
        update_parts.append(f'#{key} = :{key}')
        names[f'#{key}'] = key
        values[f':{key}'] = value

    response = table.update_item(
        Key={'PK': f'USER#{user_id}', 'SK': 'PROFILE'},
        UpdateExpression=f'SET {", ".join(update_parts)}',
        ExpressionAttributeNames=names,
        ExpressionAttributeValues=values,
        ReturnValues='ALL_NEW'
    )
    return response['Attributes']


def delete_user(user_id: str) -> None:
    table.delete_item(
        Key={'PK': f'USER#{user_id}', 'SK': 'PROFILE'}
    )
```

---

## Local Development

### DynamoDB Local
```bash
# Docker
docker run -d -p 8000:8000 amazon/dynamodb-local

# Create table locally
aws dynamodb create-table \
  --endpoint-url http://localhost:8000 \
  --table-name MyTable \
  --attribute-definitions \
    AttributeName=PK,AttributeType=S \
    AttributeName=SK,AttributeType=S \
    AttributeName=GSI1PK,AttributeType=S \
    AttributeName=GSI1SK,AttributeType=S \
  --key-schema \
    AttributeName=PK,KeyType=HASH \
    AttributeName=SK,KeyType=RANGE \
  --global-secondary-indexes \
    'IndexName=GSI1,KeySchema=[{AttributeName=GSI1PK,KeyType=HASH},{AttributeName=GSI1SK,KeyType=RANGE}],Projection={ProjectionType=ALL}' \
  --billing-mode PAY_PER_REQUEST
```

### NoSQL Workbench
AWS provides [NoSQL Workbench](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/workbench.html) for visual data modeling and querying.

---

## CLI Quick Reference

```bash
# Table operations
aws dynamodb create-table --cli-input-json file://table.json
aws dynamodb describe-table --table-name MyTable
aws dynamodb delete-table --table-name MyTable

# Item operations
aws dynamodb put-item --table-name MyTable --item '{"PK":{"S":"USER#1"},"SK":{"S":"PROFILE"}}'
aws dynamodb get-item --table-name MyTable --key '{"PK":{"S":"USER#1"},"SK":{"S":"PROFILE"}}'
aws dynamodb delete-item --table-name MyTable --key '{"PK":{"S":"USER#1"},"SK":{"S":"PROFILE"}}'

# Query
aws dynamodb query --table-name MyTable \
  --key-condition-expression "PK = :pk" \
  --expression-attribute-values '{":pk":{"S":"USER#1"}}'

# Scan (avoid in production)
aws dynamodb scan --table-name MyTable --limit 10
```

---

## Anti-Patterns

- **Scan operations** - Always use Query with proper key conditions
- **Hot partitions** - Distribute writes with high-cardinality partition keys
- **Large items** - Keep items under 400KB; use S3 for large data
- **Too many GSIs** - Each GSI duplicates data; design carefully
- **Ignoring capacity** - Monitor consumed capacity, use on-demand for variable loads
- **No condition expressions** - Always validate with ConditionExpression
- **Fetching all attributes** - Use ProjectionExpression to limit data
- **Multi-table design without reason** - Single-table is preferred unless access patterns don't overlap
