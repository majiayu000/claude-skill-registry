---
name: af-amplify-expertise
description: |
  Use when developing features with AWS Amplify Gen 2. Covers the four-tier architecture
  (Frontend, BFF, AppSync, Lambda), Lambda-first business logic principle, AppSync wiring
  patterns, and implementation pitfalls. Essential for anyone building on the GainInsight
  Standard stack.

title: Amplify Development Expertise
created: 2026-01-06
updated: 2026-01-06
last_checked: 2026-01-06
tags: [skill, expertise, amplify, lambda, appsync, architecture]
parent: ../README.md
related:
  - ../af-gaininsight-standard/SKILL.md
  - ../af-testing-expertise/SKILL.md
---

# Amplify Development Expertise

Development patterns and best practices for AWS Amplify Gen 2 applications.

## When to Use This Skill

Load this skill when you need to:
- Decide where to place new functionality (Lambda vs API route vs frontend)
- Wire Lambda functions to AppSync mutations/queries
- Implement business logic that calls AWS services
- Debug deployment or runtime issues with Amplify
- Review code for architectural compliance

**Common triggers:**
- Implementing new features in GainInsight Standard projects
- Code review of Amplify-based changes
- Debugging "why isn't this working in deployed environments?"

---

## Core Principle

> **Managed services handle infrastructure. Lambda handles decisions. Frontend handles presentation.**

Or more specifically for Amplify:

> **Cognito handles identity. Lambda handles business logic. AppSync handles data access. Frontend handles UI.**

---

## Four-Tier Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  FRONTEND (React/Next.js Client)                            │
│  Presentation Layer                                          │
├─────────────────────────────────────────────────────────────┤
│  - Render UI components                                      │
│  - Collect user input                                        │
│  - Call mutations/queries via Amplify client                 │
│  - Display results and handle loading/error states           │
│  ❌ NO business logic                                        │
│  ❌ NO data transformation beyond display formatting         │
│  ❌ NO direct AWS service calls                              │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  NEXT.JS API ROUTES (SSR)                                    │
│  Backend for Frontend (BFF) Pattern                          │
├─────────────────────────────────────────────────────────────┤
│  - Session/auth context extraction                           │
│  - Data formatting for frontend consumption                  │
│  - Simple proxying to AppSync                                │
│  ❌ NO business logic                                        │
│  ❌ NO direct AWS service calls (SES, Cognito Admin, etc.)   │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  APPSYNC (GraphQL API)                                       │
│  Data Access Layer                                           │
├─────────────────────────────────────────────────────────────┤
│  - CRUD operations on DynamoDB models                        │
│  - Authorization rules (allow.authenticated, etc.)           │
│  - Real-time subscriptions                                   │
│  - Custom resolvers → Lambda functions                       │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  LAMBDA FUNCTIONS (amplify/functions/)                       │
│  Business Logic Layer                                        │
├─────────────────────────────────────────────────────────────┤
│  - Complex business logic and workflows                      │
│  - AWS service calls (SES, S3, Cognito Admin)                │
│  - Multi-step orchestration                                  │
│  - Batch data processing (import/export)                     │
│  - Auth triggers (post-confirmation, pre-signup)             │
│  - Audit logging                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Rules

### Critical Rules (MUST)

1. **MUST place business logic in Lambda functions.** Any code that makes decisions, enforces rules, or orchestrates workflows belongs in Lambda, not frontend or API routes.

2. **MUST use AppSync mutations for write operations.** Don't call Lambda directly from frontend; wire Lambdas as AppSync resolver handlers.

3. **MUST grant explicit IAM permissions.** Lambda functions need IAM policies in `backend.ts` for AWS service access (SES, Cognito, S3).

4. **MUST include `__typename` when writing directly to DynamoDB.** Amplify Data Client requires this field to recognize records. See Pitfall #1.

5. **MUST use `resourceGroupName: "data"` for resolver Lambdas.** Prevents circular dependency between function and data stacks. See Pitfall #2.

6. **MUST avoid auto-generated mutation name conflicts.** Don't name custom mutations `createModelName`, `updateModelName`, etc. See Pitfall #3.

### Process Rules (SHOULD)

7. **SHOULD keep API routes as thin BFF wrappers.** Extract session, call AppSync, format response. No business logic.

8. **SHOULD test Lambdas in isolation.** Unit tests for handlers with mocked AWS SDK, integration tests against sandbox.

9. **SHOULD use the same sender identity across Cognito and custom emails.** Prevents DKIM/deliverability issues.

### Quality Rules (MAY)

10. **MAY use API routes for simple read-only data aggregation.** If it's just formatting data from AppSync for the frontend, BFF is acceptable.

---

## Tier Placement Guide

Use this table to decide where code belongs:

| Responsibility | Correct Tier | Example |
|----------------|--------------|---------|
| Render UI | Frontend | React components |
| Collect user input | Frontend | Forms, buttons |
| Display loading/error states | Frontend | Spinners, toasts |
| Extract session claims | API Route (BFF) | Reading JWT |
| Format data for frontend | API Route (BFF) | Aggregating responses |
| CRUD on DynamoDB models | AppSync | `client.models.Tenant.get()` |
| Authorization rules | AppSync | `allow.authenticated()` |
| Send emails (SES) | Lambda | Invitation emails |
| Cognito admin operations | Lambda | User attribute updates |
| Complex business logic | Lambda | Multi-step workflows |
| Batch data import | Lambda | CSV processing |
| Data export generation | Lambda | Report generation → S3 |
| Auth triggers | Lambda | Post-confirmation |
| Scheduled jobs | Lambda | Cleanup tasks |

### Decision Flowchart

```
Does it make a business decision?
  └─ Yes → Lambda
  └─ No  → Does it call AWS services (SES, Cognito Admin, S3)?
            └─ Yes → Lambda
            └─ No  → Does it need audit/logging?
                      └─ Yes → Lambda
                      └─ No  → Could a malicious client exploit it?
                                └─ Yes → Lambda
                                └─ No  → Frontend or BFF is acceptable
```

---

## Workflows

### Workflow: Wiring a Lambda to AppSync

**When:** Adding a new mutation or query backed by Lambda

**Procedure:**

1. **Create Lambda function** in `amplify/functions/`:
```typescript
// amplify/functions/my-function/resource.ts
import { defineFunction } from "@aws-amplify/backend";

export const myFunction = defineFunction({
  name: "project-my-function",
  entry: "./handler.ts",
  timeoutSeconds: 30,
  memoryMB: 256,
  resourceGroupName: "data",  // Required for AppSync resolvers
});
```

2. **Implement handler** with AppSync event format:
```typescript
// amplify/functions/my-function/handler.ts
import type { AppSyncResolverHandler } from "aws-lambda";

interface Args { email: string; }
interface Result { id: string; status: string; }

export const handler: AppSyncResolverHandler<Args, Result> = async (event) => {
  const { email } = event.arguments;
  const claims = (event.identity as { claims?: Record<string, string> })?.claims;

  // Business logic here

  return { id: "...", status: "success" };
};
```

3. **Wire to AppSync** in `amplify/data/resource.ts`:
```typescript
import { myFunction } from "../functions/my-function/resource";

const schema = a.schema({
  // Models...

  myMutation: a
    .mutation()
    .arguments({ email: a.string().required() })
    .returns(a.customType({
      id: a.string(),
      status: a.string(),
    }))
    .handler(a.handler.function(myFunction))
    .authorization((allow) => [allow.authenticated()]),
});
```

4. **Grant IAM permissions** in `amplify/backend.ts`:
```typescript
import { PolicyStatement, Effect } from "aws-cdk-lib/aws-iam";

backend.myFunction.resources.lambda.addToRolePolicy(
  new PolicyStatement({
    effect: Effect.ALLOW,
    actions: ["ses:SendEmail"],
    resources: ["arn:aws:ses:eu-west-2:*:identity/*"],
  })
);
```

5. **Export function** in `amplify/backend.ts`:
```typescript
import { myFunction } from "./functions/my-function/resource";
// Add to backend definition
```

6. **Call from frontend**:
```typescript
const { data, errors } = await client.mutations.myMutation({
  email: userEmail,
});
```

### Workflow: Direct DynamoDB Writes from Lambda

**When:** Lambda needs to write to DynamoDB directly (not via AppSync)

**Critical:** Include `__typename` and `updatedAt` fields:

```typescript
const item = {
  __typename: "ModelName",  // Must match your model name exactly
  id: uuid(),
  // ... other fields
  createdAt: new Date().toISOString(),
  updatedAt: new Date().toISOString(),
};

await dynamoClient.send(new PutCommand({
  TableName: TABLE_NAME,
  Item: item,
}));
```

Without `__typename`, Amplify Data Client's `.get()` returns `null` even though the record exists in DynamoDB.

---

## Common Pitfalls

### 1. Missing `__typename` in Direct DynamoDB Writes

**Problem:** Lambda writes to DynamoDB succeed, but `client.models.Model.get()` returns `null`.

**Root cause:** Amplify Data Client expects `__typename: "ModelName"` field. Records created via `client.models.create()` include this automatically. Direct DynamoDB writes don't.

**Solution:**
```typescript
const invitation = {
  __typename: "TenantInvitation",  // Required!
  id: invitationId,
  email: email.toLowerCase(),
  // ... other fields
  createdAt: now.toISOString(),
  updatedAt: now.toISOString(),  // Also expected by Amplify
};
```

### 2. Circular Dependency Between Function and Data Stacks

**Problem:** Sandbox deployment fails with circular dependency error.

**Root cause:** Lambda functions used as AppSync resolvers are in a separate CloudFormation stack from data resources by default.

**Solution:** Add `resourceGroupName: "data"` to Lambda definition:
```typescript
export const myFunction = defineFunction({
  name: "project-my-function",
  entry: "./handler.ts",
  resourceGroupName: "data",  // Places in same stack as data resources
});
```

### 3. Mutation Name Conflicts with Auto-Generated CRUD

**Problem:** Deployment fails with `Object type extension 'Mutation' cannot redeclare field createTenant`.

**Root cause:** Amplify auto-generates `create`, `update`, `delete` mutations for models defined with `a.model()`. Custom mutations with same names conflict.

**Solution:** Use prefixed names:
```typescript
// ❌ Conflicts with auto-generated createTenant
createTenant: a.mutation()...

// ✅ Unique name, no conflict
adminCreateTenant: a.mutation()...
```

### 4. SSR/API Routes Can't Access AWS Services

**Problem:** SES emails work locally but fail in deployed environments with permission errors.

**Root cause:** Next.js SSR compute (Lambda@Edge) doesn't have explicit IAM policies. Only custom Lambda functions defined in `amplify/functions/` have manageable IAM.

**Solution:** Move AWS service calls to Lambda functions, wire via AppSync.

### 5. Environment URL Mismatch in Emails

**Problem:** Email links point to wrong environment (e.g., production URL in sandbox emails).

**Root cause:** Lambda `APP_URL` environment variable set to production/staging, but test data only exists in sandbox.

**Solution for E2E tests:** Extract path from email, navigate to test server's path:
```typescript
// Extract /invite/abc-123 from full URL
const path = emailBody.match(/\/invite\/([a-zA-Z0-9-]+)/)?.[0];
await page.goto(path);  // Goes to localhost/invite/abc-123
```

### 6. Sandbox vs Deployed Environment Parity

**Context:** Sandboxes run in the dev AWS account with `doppler run --config dev` credentials.

**Implication:** If something works in deployed dev but not sandbox, it's likely a code/config difference, not AWS permissions. Both use the same AWS account and SES configuration.

---

## Examples

### Good: Lambda for Business Logic

```typescript
// ✅ Invitation logic in Lambda
// amplify/functions/org-invite-user/handler.ts
export const handler: AppSyncResolverHandler<Args, Result> = async (event) => {
  // 1. Authorization check
  const claims = event.identity?.claims;
  if (claims?.["custom:role"] !== "owner" && claims?.["custom:role"] !== "admin") {
    throw new Error("Forbidden");
  }

  // 2. Business validation
  const existingUser = await checkUserExists(email);
  if (existingUser) throw new Error("User already exists");

  // 3. Create invitation record
  await dynamoClient.send(new PutCommand({ ... }));

  // 4. Send email
  await sesClient.send(new SendEmailCommand({ ... }));

  return { id: invitationId, status: "pending" };
};
```

### Bad: Business Logic in API Route

```typescript
// ❌ Business logic in Next.js API route
// src/app/api/org/invite/route.ts
export async function POST(request: NextRequest) {
  // Authorization, validation, DynamoDB, SES all in one place
  // - No explicit IAM permissions
  // - Harder to test
  // - Mixed responsibilities
}
```

### Good: Thin BFF Route

```typescript
// ✅ BFF pattern - session extraction and formatting only
// src/app/api/org/users/route.ts
export async function GET() {
  const session = await getSession();
  const tenantId = session.claims["custom:tenant_id"];

  // Delegate to AppSync
  const { data } = await client.models.User.list({
    filter: { tenantId: { eq: tenantId } },
  });

  // Format for frontend
  return NextResponse.json(data.map(u => ({
    id: u.id,
    email: u.email,
    role: u.role,
  })));
}
```

---

## Essential Reading

- [Amplify Gen 2: Functions](https://docs.amplify.aws/react/build-a-backend/functions/)
- [Amplify Gen 2: Custom Business Logic](https://docs.amplify.aws/react/build-a-backend/data/custom-business-logic/)
- [af-gaininsight-standard](../af-gaininsight-standard/SKILL.md) - Infrastructure setup
- [af-testing-expertise](../af-testing-expertise/SKILL.md) - Testing Lambda functions

---

**Remember:**
1. Business logic → Lambda
2. AWS service calls → Lambda
3. Frontend → UI only
4. Include `__typename` in direct DynamoDB writes
5. Use `resourceGroupName: "data"` for resolver Lambdas
