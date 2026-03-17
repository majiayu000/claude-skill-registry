---
name: backend-agent
description: Handles backend/API/database work for Unite-Hub. Implements Next.js API routes, Supabase database operations, RLS policies, authentication, and third-party integrations (Gmail, Stripe).
---

# Backend Agent Skill

## Overview

The Backend Agent is responsible for all server-side work in Unite-Hub:
1. **Next.js API route development** (serverless functions)
2. **Supabase database operations** (queries, mutations, RLS)
3. **Authentication and authorization** (NextAuth.js, Supabase Auth)
4. **Third-party integrations** (Gmail API, Stripe, Claude AI)
5. **Database schema management** (migrations, indexes)
6. **API security and performance** (rate limiting, caching)

## How to Use This Agent

### Trigger

User says: "Create new API endpoint", "Fix database query", "Update RLS policies", "Implement Gmail integration"

### What the Agent Does

#### 1. Understand the Request

**Questions to Ask**:
- What's the API endpoint purpose?
- What database tables are involved?
- What's the expected input/output format?
- What authentication is required?
- What's the priority (P0/P1/P2)?

#### 2. Analyze Current Implementation

**Step A: Locate Files**
```bash
# Find API routes
find src/app/api -name "route.ts" | grep -i "contacts"

# Find database utilities
find src/lib -name "*.ts" | grep -i "db"
```

**Step B: Read Current Code**
```typescript
// Use text_editor tool
text_editor.view("src/app/api/contacts/route.ts")
text_editor.view("src/lib/db.ts")
```

**Step C: Identify Dependencies**
- What database tables are queried?
- What authentication is required?
- What external APIs are called?
- What error handling exists?

#### 3. Implement Changes

**Step A: Create API Route**

All API routes in Unite-Hub follow this pattern:

```typescript
// src/app/api/example/route.ts
import { NextRequest, NextResponse } from "next/server";
import { createClient } from "@/lib/supabase";

export async function POST(request: NextRequest) {
  try {
    // 1. Parse request body
    const body = await request.json();
    const { workspaceId, action, ...params } = body;

    // 2. Validate input
    if (!workspaceId) {
      return NextResponse.json(
        { error: "workspaceId is required" },
        { status: 400 }
      );
    }

    // 3. Get Supabase client
    const supabase = createClient();

    // 4. Check authentication (if needed)
    const { data: { user }, error: authError } = await supabase.auth.getUser();
    if (authError || !user) {
      return NextResponse.json(
        { error: "Unauthorized" },
        { status: 401 }
      );
    }

    // 5. Perform database operation
    const { data, error } = await supabase
      .from("contacts")
      .select("*")
      .eq("workspace_id", workspaceId)  // CRITICAL: Workspace filter
      .eq("organization_id", user.organization_id);  // CRITICAL: Org filter

    if (error) {
      console.error("Database error:", error);
      return NextResponse.json(
        { error: "Database query failed" },
        { status: 500 }
      );
    }

    // 6. Return success response
    return NextResponse.json({
      success: true,
      data,
      count: data.length
    });

  } catch (error) {
    console.error("API error:", error);
    return NextResponse.json(
      { error: "Internal server error" },
      { status: 500 }
    );
  }
}

// Support OPTIONS for CORS
export async function OPTIONS(request: NextRequest) {
  return NextResponse.json({}, { status: 200 });
}
```

**Step B: Database Operations**

All database operations MUST use workspace filtering:

```typescript
// ❌ BAD - No workspace filter
const { data } = await supabase
  .from("contacts")
  .select("*");

// ✅ GOOD - Workspace filtered
const { data } = await supabase
  .from("contacts")
  .select("*")
  .eq("workspace_id", workspaceId)
  .eq("organization_id", orgId);
```

**Required filters for data isolation**:
- `.eq("workspace_id", workspaceId)` - Workspace scope
- `.eq("organization_id", orgId)` - Organization scope (top-level)

**Step C: Update `src/lib/db.ts` Wrapper**

The `db.ts` wrapper provides consistent database access:

```typescript
// src/lib/db.ts
import { createClient } from "@/lib/supabase";

export const db = {
  contacts: {
    async listByWorkspace(workspaceId: string) {
      const supabase = createClient();
      const { data, error } = await supabase
        .from("contacts")
        .select("*")
        .eq("workspace_id", workspaceId)
        .order("created_at", { ascending: false });

      if (error) throw error;
      return data || [];
    },

    async getById(contactId: string, workspaceId: string) {
      const supabase = createClient();
      const { data, error } = await supabase
        .from("contacts")
        .select("*")
        .eq("id", contactId)
        .eq("workspace_id", workspaceId)
        .single();

      if (error) throw error;
      return data;
    },

    async create(contact: ContactInput, workspaceId: string) {
      const supabase = createClient();
      const { data, error } = await supabase
        .from("contacts")
        .insert([{ ...contact, workspace_id: workspaceId }])
        .select()
        .single();

      if (error) throw error;
      return data;
    },

    async update(contactId: string, updates: Partial<ContactInput>, workspaceId: string) {
      const supabase = createClient();
      const { data, error } = await supabase
        .from("contacts")
        .update(updates)
        .eq("id", contactId)
        .eq("workspace_id", workspaceId)
        .select()
        .single();

      if (error) throw error;
      return data;
    }
  },

  // Similar patterns for campaigns, emails, etc.
};
```

**CRITICAL FIX for V1**: Add missing import in `src/lib/db.ts:58`

```typescript
// Line 1 - Add import
import { createClient, getSupabaseServer } from "./supabase";

// Line 58 - Fix usage
const supabaseServer = getSupabaseServer();
const { data: workspace, error } = await supabaseServer
  .from("workspaces")
  .select("*")
  .eq("id", workspaceId)
  .single();
```

#### 4. Implement Authentication

**Pattern 1: Client-Side Auth (Browser)**

```typescript
import { createClient } from "@/lib/supabase";

export async function GET(request: NextRequest) {
  const supabase = createClient();

  const { data: { user }, error } = await supabase.auth.getUser();

  if (error || !user) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  // User is authenticated, proceed
}
```

**Pattern 2: Server-Side Auth (API Routes)**

```typescript
import { getSupabaseServer } from "@/lib/supabase";

export async function POST(request: NextRequest) {
  const supabase = getSupabaseServer();

  const { data: { session }, error } = await supabase.auth.getSession();

  if (error || !session) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  // Session is valid, proceed
}
```

**CRITICAL for V1**: Re-enable authentication on all API routes

Many routes currently have:
```typescript
// TODO: Re-enable authentication in production
// const { auth } = await import("@/lib/auth");
// const session = await auth();
```

**Action Required**: Remove TODO comments and re-enable auth checks.

#### 5. Row Level Security (RLS) Policies

All Supabase tables MUST have RLS policies:

```sql
-- Enable RLS on table
ALTER TABLE contacts ENABLE ROW LEVEL SECURITY;

-- Policy: Users can only see contacts in their workspace
CREATE POLICY "Users can view workspace contacts"
ON contacts
FOR SELECT
USING (
  workspace_id IN (
    SELECT w.id
    FROM workspaces w
    JOIN user_organizations uo ON uo.organization_id = w.organization_id
    WHERE uo.user_id = auth.uid()
  )
);

-- Policy: Users can insert contacts in their workspace
CREATE POLICY "Users can create workspace contacts"
ON contacts
FOR INSERT
WITH CHECK (
  workspace_id IN (
    SELECT w.id
    FROM workspaces w
    JOIN user_organizations uo ON uo.organization_id = w.organization_id
    WHERE uo.user_id = auth.uid()
  )
);

-- Policy: Users can update contacts in their workspace
CREATE POLICY "Users can update workspace contacts"
ON contacts
FOR UPDATE
USING (
  workspace_id IN (
    SELECT w.id
    FROM workspaces w
    JOIN user_organizations uo ON uo.organization_id = w.organization_id
    WHERE uo.user_id = auth.uid()
  )
);
```

**CRITICAL for V1**: Verify RLS policies exist for:
- `contacts`
- `campaigns`
- `drip_campaigns`
- `emails`
- `generated_content`
- `campaign_enrollments`

#### 6. Third-Party Integrations

**Gmail API Integration**

```typescript
// src/lib/integrations/gmail.ts
import { google } from "googleapis";

export async function getGmailClient(accessToken: string) {
  const oauth2Client = new google.auth.OAuth2(
    process.env.GOOGLE_CLIENT_ID,
    process.env.GOOGLE_CLIENT_SECRET,
    process.env.GOOGLE_CALLBACK_URL
  );

  oauth2Client.setCredentials({ access_token: accessToken });

  return google.gmail({ version: "v1", auth: oauth2Client });
}

export async function fetchEmails(gmail: any, maxResults = 50) {
  const res = await gmail.users.messages.list({
    userId: "me",
    maxResults,
    q: "is:unread", // Only unread emails
  });

  const messages = res.data.messages || [];
  const emails = [];

  for (const message of messages) {
    const email = await gmail.users.messages.get({
      userId: "me",
      id: message.id,
    });
    emails.push(email.data);
  }

  return emails;
}
```

**Claude AI Integration**

```typescript
// src/lib/integrations/claude.ts
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

export async function generateContent({
  contactName,
  contactCompany,
  interactionHistory,
  contentType,
}: {
  contactName: string;
  contactCompany: string;
  interactionHistory: string;
  contentType: "followup" | "proposal" | "case_study";
}) {
  const message = await client.messages.create({
    model: "claude-opus-4-5-20251101",
    max_tokens: 2000,
    thinking: {
      type: "enabled",
      budget_tokens: 7500,
    },
    messages: [
      {
        role: "user",
        content: `Generate a personalized ${contentType} email for ${contactName} at ${contactCompany}.

Interaction history:
${interactionHistory}

Generate a professional, personalized email that references their previous interactions.`,
      },
    ],
  });

  return message.content[0].type === "text" ? message.content[0].text : null;
}
```

#### 7. Error Handling and Logging

**Structured Error Responses**:

```typescript
// Error response format
return NextResponse.json(
  {
    error: "Error message for user",
    code: "ERROR_CODE",
    details: isDev ? error.message : undefined, // Only in development
  },
  { status: 500 }
);
```

**Audit Logging**:

```typescript
// Log all important actions
await supabase.from("auditLogs").insert({
  organization_id: orgId,
  user_id: userId,
  action: "contact_created",
  resource_type: "contact",
  resource_id: contact.id,
  context: {
    contact_email: contact.email,
    source: "api",
  },
  ip_address: request.headers.get("x-forwarded-for"),
  user_agent: request.headers.get("user-agent"),
  created_at: new Date().toISOString(),
});
```

## Common Tasks

### Task 1: Fix Missing Workspace Filter in API

**Example**: `/api/agents/contact-intelligence` missing workspace filter

**Steps**:
1. Read `src/app/api/agents/contact-intelligence/route.ts`
2. Find database queries
3. Add `.eq("workspace_id", workspaceId)`
4. Add null check for workspaceId
5. Test with multiple workspaces

**Code**:
```typescript
// Before
const { data: contacts } = await supabase.from("contacts").select("*");

// After
if (!workspaceId) {
  return NextResponse.json(
    { error: "workspaceId is required" },
    { status: 400 }
  );
}

const { data: contacts, error } = await supabase
  .from("contacts")
  .select("*")
  .eq("workspace_id", workspaceId);

if (error) {
  console.error("Database error:", error);
  return NextResponse.json(
    { error: "Failed to fetch contacts" },
    { status: 500 }
  );
}
```

### Task 2: Create New API Endpoint

**Example**: Create `/api/contacts/bulk-update` endpoint

**Steps**:
1. Create `src/app/api/contacts/bulk-update/route.ts`
2. Implement POST handler
3. Add authentication check
4. Validate input
5. Perform bulk update with workspace filter
6. Test endpoint

**Code**:
```typescript
// src/app/api/contacts/bulk-update/route.ts
import { NextRequest, NextResponse } from "next/server";
import { createClient } from "@/lib/supabase";

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { workspaceId, contactIds, updates } = body;

    // Validate input
    if (!workspaceId || !contactIds || !Array.isArray(contactIds)) {
      return NextResponse.json(
        { error: "Invalid input" },
        { status: 400 }
      );
    }

    // Get authenticated user
    const supabase = createClient();
    const { data: { user }, error: authError } = await supabase.auth.getUser();

    if (authError || !user) {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
    }

    // Perform bulk update
    const { data, error } = await supabase
      .from("contacts")
      .update(updates)
      .in("id", contactIds)
      .eq("workspace_id", workspaceId)  // CRITICAL: Workspace filter
      .select();

    if (error) {
      console.error("Bulk update error:", error);
      return NextResponse.json(
        { error: "Bulk update failed" },
        { status: 500 }
      );
    }

    // Log audit event
    await supabase.from("auditLogs").insert({
      organization_id: user.organization_id,
      user_id: user.id,
      action: "contacts_bulk_updated",
      resource_type: "contact",
      context: {
        updated_count: data.length,
        contact_ids: contactIds,
        updates,
      },
    });

    return NextResponse.json({
      success: true,
      updated: data.length,
      contacts: data,
    });

  } catch (error) {
    console.error("API error:", error);
    return NextResponse.json(
      { error: "Internal server error" },
      { status: 500 }
    );
  }
}
```

### Task 3: Update RLS Policies

**Example**: Add RLS policy for new table

**Steps**:
1. Connect to Supabase SQL Editor
2. Enable RLS on table
3. Create SELECT policy
4. Create INSERT policy
5. Create UPDATE policy
6. Create DELETE policy (if needed)
7. Test policies

**Code**:
```sql
-- Enable RLS
ALTER TABLE new_table ENABLE ROW LEVEL SECURITY;

-- SELECT policy
CREATE POLICY "Users can view workspace records"
ON new_table
FOR SELECT
USING (
  workspace_id IN (
    SELECT w.id
    FROM workspaces w
    JOIN user_organizations uo ON uo.organization_id = w.organization_id
    WHERE uo.user_id = auth.uid()
  )
);

-- INSERT policy
CREATE POLICY "Users can create workspace records"
ON new_table
FOR INSERT
WITH CHECK (
  workspace_id IN (
    SELECT w.id
    FROM workspaces w
    JOIN user_organizations uo ON uo.organization_id = w.organization_id
    WHERE uo.user_id = auth.uid()
  )
);

-- UPDATE policy
CREATE POLICY "Users can update workspace records"
ON new_table
FOR UPDATE
USING (
  workspace_id IN (
    SELECT w.id
    FROM workspaces w
    JOIN user_organizations uo ON uo.organization_id = w.organization_id
    WHERE uo.user_id = auth.uid()
  )
);

-- Test policy
SELECT * FROM new_table; -- Should only return user's workspace records
```

## Database Best Practices

### Query Optimization

```typescript
// ❌ BAD - N+1 query problem
const contacts = await db.contacts.listByWorkspace(workspaceId);
for (const contact of contacts) {
  const emails = await db.emails.listByContact(contact.id); // N queries!
}

// ✅ GOOD - Single query with join
const { data } = await supabase
  .from("contacts")
  .select(`
    *,
    emails (*)
  `)
  .eq("workspace_id", workspaceId);
```

### Indexing

```sql
-- Create indexes for frequently queried columns
CREATE INDEX idx_contacts_workspace_id ON contacts(workspace_id);
CREATE INDEX idx_contacts_ai_score ON contacts(ai_score DESC);
CREATE INDEX idx_emails_contact_id ON emails(contact_id);
CREATE INDEX idx_campaign_enrollments_contact ON campaign_enrollments(contact_id);
```

### Pagination

```typescript
const PAGE_SIZE = 20;

const { data, error, count } = await supabase
  .from("contacts")
  .select("*", { count: "exact" })
  .eq("workspace_id", workspaceId)
  .order("created_at", { ascending: false })
  .range(page * PAGE_SIZE, (page + 1) * PAGE_SIZE - 1);

return {
  contacts: data,
  totalCount: count,
  page,
  pageSize: PAGE_SIZE,
  totalPages: Math.ceil(count / PAGE_SIZE),
};
```

## API Security Checklist

✅ **Authentication**:
- [ ] User is authenticated (Supabase Auth)
- [ ] Session is valid
- [ ] User has access to requested workspace

✅ **Authorization**:
- [ ] User belongs to organization
- [ ] User has required role (owner/admin/member)
- [ ] Workspace belongs to user's organization

✅ **Input Validation**:
- [ ] Required fields present
- [ ] Data types correct
- [ ] Values within acceptable ranges
- [ ] SQL injection prevented (Supabase parameterized queries)
- [ ] XSS prevented (sanitize user input)

✅ **Data Isolation**:
- [ ] Workspace filtering on ALL queries
- [ ] Organization filtering on ALL queries
- [ ] RLS policies enabled on ALL tables

✅ **Error Handling**:
- [ ] Try/catch blocks
- [ ] Structured error responses
- [ ] No sensitive data in error messages
- [ ] Errors logged to console/monitoring

✅ **Audit Logging**:
- [ ] All mutations logged to auditLogs
- [ ] User ID, action, resource captured
- [ ] Timestamp recorded

## Version 1 Constraints

**What We Fix for V1**:
- ✅ Add workspace filtering to ALL API endpoints
- ✅ Re-enable authentication on ALL routes
- ✅ Fix `src/lib/db.ts` missing import
- ✅ Verify RLS policies on ALL tables
- ✅ Test ALL 104 API endpoints

**What We Do NOT Build for V1**:
- ❌ Advanced rate limiting
- ❌ GraphQL API
- ❌ Webhook infrastructure
- ❌ Background job queue
- ❌ Caching layer (Redis)

## Key Points

- **Always filter by workspace** - Data isolation is critical
- **Always check authentication** - No public endpoints without explicit reason
- **Use RLS policies** - Defense in depth
- **Log all mutations** - Audit trail for compliance
- **Handle errors gracefully** - Return structured error responses
- **Test with multiple workspaces** - Verify data isolation

---

## Integration with Other Agents

The Backend Agent works with:
- **Frontend Agent** - Provides API endpoints
- **Email Agent** - Processes email data
- **Content Agent** - Stores generated content
- **Orchestrator** - Coordinates workflows
- **Docs Agent** - Updates API documentation
