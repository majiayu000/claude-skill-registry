---
name: docs-seeker
description: Discovers and researches authoritative documentation with version-specific,
  context-aware search. Auto-activates when user asks "find documentation", "API docs",
  "how to use", "integration guide", "be
---

---
name: docs-seeker
description: Discovers and researches authoritative documentation with version-specific, context-aware search. Auto-activates when user asks "find documentation", "API docs", "how to use", "integration guide", "best practices", "design pattern", or when running /ccpm:plan or /ccpm:plan. Fetches latest docs from official sources via Context7 MCP. Uses progressive discovery (overview → API reference → integration → best practices). Prioritizes: Official docs → Framework guides → API references → Community resources. Provides version-specific recommendations and code examples from documentation. Flags important caveats and performance considerations. Surfaces migration guides when upgrading frameworks.
---

# Documentation Seeker

Intelligent documentation discovery and research for technical implementation.

## When to Use

This skill auto-activates when:

- User asks: **"find documentation"**, **"API docs"**, **"how to use"**, **"integration guide"**
- Running **`/ccpm:plan`** (needs library docs)
- Running **`/ccpm:plan`** (technical research phase)
- Implementing features requiring framework knowledge
- Researching best practices or design patterns

## What It Does

### Documentation Discovery

**Finds relevant documentation for**:
- Libraries and frameworks (React, Next.js, Express, etc.)
- APIs and SDKs (Stripe, AWS, Google Cloud, etc.)
- Design patterns and best practices
- Integration guides
- Technical specifications

**Search strategies**:
1. Official documentation first
2. Framework-specific guides
3. API references
4. Community resources (if official docs insufficient)
5. Code examples and tutorials

### Integration with Context7 MCP

Works seamlessly with Context7 to fetch latest documentation:

```
User: "Find React 19 documentation for Server Components"

Claude: [docs-seeker activates]

Searching for React 19 Server Components documentation...

Using Context7 to fetch latest docs:
1. Official React docs (react.dev)
2. Server Components RFC
3. Next.js App Router integration guide

Found:
- React 19 Server Components: https://react.dev/reference/rsc/server-components
- Key features: Async components, data fetching, streaming
- Best practices: Use for data-heavy components, avoid client-side state
- Integration: Works with Next.js 15 App Router

Summary available for /ccpm:plan architecture section.
```

## Integration with CCPM

### Planning Phase Research

**Use with `/ccpm:plan`**:

When planning a task, docs-seeker helps gather technical context:

```
User: "/ccpm:plan AUTH-123 JIRA-456"

Claude: [docs-seeker activates during research phase]

Researching technical requirements for AUTH-123...

Finding relevant documentation:
1. JWT authentication best practices
2. OAuth 2.0 specification
3. Passport.js integration guide
4. Express.js security middleware

Key findings:
- JWT: Use RS256 for production (not HS256)
- Refresh tokens: Store in httpOnly cookies
- OAuth: Implement PKCE flow for SPAs
- Rate limiting: 5 login attempts per 15 minutes

Documentation links saved to Linear task for implementation reference.
```

### Spec Writing Research

**Use with `/ccpm:plan`**:

When writing specs, docs-seeker finds authoritative sources:

```
User: "/ccpm:plan DOC-789 api-design"

Claude: [docs-seeker activates]

Researching API design best practices...

Finding documentation:
1. RESTful API design guide (Microsoft)
2. GraphQL schema design (Apollo)
3. OpenAPI 3.1 specification
4. API versioning strategies

Recommendations based on docs:
- Endpoints: Use nouns, not verbs (/users not /getUsers)
- Versioning: URL path (/v1/) or Accept header
- Pagination: Cursor-based for scalability
- Error handling: RFC 7807 Problem Details
- Documentation: OpenAPI spec + Swagger UI

Writing API design section with these guidelines...
```

### Implementation Guidance

**During feature implementation**:

```
User: "How do I implement file uploads with NextJS 15?"

Claude: [docs-seeker activates]

Searching Next.js 15 file upload documentation...

Found official guides:
1. Next.js App Router: Route Handlers
2. FormData API usage
3. File upload best practices
4. Streaming uploads for large files

Implementation approach:
```typescript
// app/api/upload/route.ts
export async function POST(request: Request) {
  const formData = await request.formData();
  const file = formData.get('file') as File;

  // Process file
  const bytes = await file.arrayBuffer();
  const buffer = Buffer.from(bytes);

  // Save to storage
  await saveFile(buffer, file.name);

  return Response.json({ success: true });
}
```

Documentation: https://nextjs.org/docs/app/building-your-application/routing/route-handlers

Would you like me to add this to the implementation plan?
```

## Documentation Sources

### Official Sources (Highest Priority)

**Always check official docs first**:
- Framework documentation (React, Next.js, Vue, Angular)
- Library docs (Lodash, Axios, Moment.js)
- Cloud provider docs (AWS, GCP, Azure)
- API specifications (Stripe, Twilio, SendGrid)

### Technical Specifications

**For standards and protocols**:
- W3C specifications
- IETF RFCs
- ECMA standards
- OpenAPI/Swagger specs

### Community Resources

**When official docs are insufficient**:
- MDN Web Docs (JavaScript, CSS, HTML)
- Stack Overflow discussions
- GitHub repositories and READMEs
- Technical blogs (reputable sources only)

## Search Strategies

### Strategy 1: Version-Specific Search

Always search for the specific version in use:

```
❌ Generic: "React hooks documentation"
✅ Specific: "React 19 hooks documentation"

❌ Generic: "Node.js async/await"
✅ Specific: "Node.js 20 async/await best practices"
```

### Strategy 2: Context-Aware Search

Include the context of what you're building:

```
❌ Vague: "authentication docs"
✅ Context: "JWT authentication with Express.js and Passport"

❌ Vague: "database queries"
✅ Context: "PostgreSQL complex joins with Prisma ORM"
```

### Strategy 3: Progressive Discovery

Start broad, then narrow down:

1. **Overview**: "What is Server Components in React?"
2. **API Reference**: "Server Component API methods"
3. **Integration**: "Server Components with Next.js App Router"
4. **Best Practices**: "Server Components performance optimization"

## Examples

### Example 1: Research for Spec Writing

```
User: "/ccpm:plan DOC-456 architecture"

Claude: [docs-seeker activates]

Researching architecture patterns for payment processing...

Finding documentation:
1. Stripe API documentation
   - Payment Intents API
   - Webhook handling
   - Idempotency keys

2. PCI compliance requirements
   - Never store full card numbers
   - Use tokenization
   - Secure data transmission

3. Architecture patterns
   - Adapter pattern for multiple providers
   - Event-driven webhooks
   - Retry mechanisms with exponential backoff

4. Error handling
   - Stripe error types
   - Declined payments flow
   - Network timeout handling

Documentation summary:
- Use Payment Intents (not legacy Charges API)
- Implement webhook signature verification
- Store payment status in database
- Handle idempotency for retries
- Support multiple payment providers via adapters

Writing architecture section with these patterns...
```

### Example 2: Quick Implementation Help

```
User: "How do I use React useEffect with async functions?"

Claude: [docs-seeker activates]

Searching React useEffect async documentation...

Found: React 19 documentation on useEffect

Official recommendation:
```javascript
// ✅ Correct approach
useEffect(() => {
  async function fetchData() {
    const response = await fetch('/api/data');
    const data = await response.json();
    setData(data);
  }
  fetchData();
}, []);

// ❌ Wrong - useEffect cannot be async directly
useEffect(async () => {
  // This won't work!
}, []);
```

Key points from docs:
- useEffect callback cannot be async
- Create async function inside useEffect
- Handle cleanup with AbortController
- Avoid race conditions with cleanup

Documentation: https://react.dev/reference/react/useEffect#fetching-data-with-effects

Would you like me to show the full pattern with cleanup?
```

### Example 3: API Integration Research

```
User: "Find Stripe webhook documentation"

Claude: [docs-seeker activates]

Searching Stripe webhook documentation...

Found official Stripe docs:

1. **Webhook Events**
   - payment_intent.succeeded
   - payment_intent.payment_failed
   - customer.subscription.updated
   - Full event reference: https://stripe.com/docs/api/events/types

2. **Webhook Security**
   - Signature verification required
   - Use Stripe-Signature header
   - Verify with webhook secret
   - Code example:
   ```javascript
   const sig = request.headers['stripe-signature'];
   const event = stripe.webhooks.constructEvent(
     request.body,
     sig,
     process.env.STRIPE_WEBHOOK_SECRET
   );
   ```

3. **Best Practices**
   - Return 200 immediately
   - Process events asynchronously
   - Handle duplicate events (idempotency)
   - Log all webhook events
   - Monitor webhook failures in Stripe dashboard

4. **Testing**
   - Use Stripe CLI for local testing
   - Test with Stripe's test events
   - Verify all event types your app handles

Documentation: https://stripe.com/docs/webhooks

This should be added to the implementation plan under "Webhook Handler" section.
```

## Integration with CCPM Workflows

### Workflow 1: Spec Writing

```
1. User runs: /ccpm:plan DOC-123 architecture
2. docs-seeker activates automatically
3. Finds relevant documentation
4. Summarizes key patterns and best practices
5. Claude writes spec section using authoritative sources
6. Documentation links added to spec for reference
```

### Workflow 2: Planning Phase

```
1. User runs: /ccpm:plan TASK-456
2. Task description: "Implement real-time notifications"
3. docs-seeker activates for research
4. Finds WebSocket, Server-Sent Events, and polling docs
5. Compares approaches based on documentation
6. Recommends approach with rationale
7. Plan includes documentation links
```

### Workflow 3: Implementation Support

```
1. Developer starts implementing feature
2. Asks: "How do I handle file uploads?"
3. docs-seeker finds Next.js/Express/Multer docs
4. Provides implementation example from docs
5. Highlights important caveats (file size limits, validation)
6. Links to official documentation
```

## Works With Context7 MCP

**Context7 integration provides**:
- Latest documentation (always up-to-date)
- Version-specific information
- Framework changelog and migration guides
- API reference with examples

**Example Context7 usage**:
```
docs-seeker: "Find Next.js 15 App Router documentation"
       ↓
Context7 MCP: Fetches latest from nextjs.org
       ↓
Returns: App Router architecture, routing, data fetching, caching
       ↓
docs-seeker: Summarizes key points relevant to task
```

## Tips for Better Results

### Be Specific

**Good requests**:
- "Find Prisma migration documentation for PostgreSQL"
- "Get Tailwind CSS v4 documentation for dark mode"
- "Show GraphQL schema stitching with Apollo Federation"

**Vague requests** (harder to help):
- "Find docs"
- "How does this work?"
- "Give me information about React"

### Include Version Information

Always mention versions when known:
- "Next.js 15" not just "Next.js"
- "React 19" not just "React"
- "Node.js 20 LTS" not just "Node.js"

### Specify Your Stack

Help docs-seeker find the right integration docs:
- "React with TypeScript"
- "Express.js with Prisma ORM"
- "Next.js with Auth.js (NextAuth v5)"

## Common Use Cases

### Use Case 1: Starting New Feature

```
Before implementation:
1. Ask docs-seeker for library documentation
2. Review API reference
3. Check best practices
4. See code examples
5. Then start coding with solid foundation
```

### Use Case 2: Troubleshooting

```
When stuck:
1. Ask docs-seeker for specific API documentation
2. Check if using correct method/approach
3. Review error handling documentation
4. Find related examples
5. Apply documented solution
```

### Use Case 3: Architecture Decisions

```
When designing:
1. Ask docs-seeker for pattern documentation
2. Compare multiple approaches
3. Review trade-offs from official sources
4. Choose approach backed by documentation
5. Document decision with references
```

## Integration with Other Skills

**Works alongside**:

- **sequential-thinking**: Use docs-seeker to research each step
- **pm-workflow-guide**: Suggests when documentation research needed
- **ccpm-debugging**: Find debugging guides when issues arise
- **Context7 MCP**: Fetches actual documentation content

**Example combined activation**:
```
User: "Break down this complex GraphQL federation task"
       ↓
sequential-thinking: Structure the problem breakdown
       ↓
docs-seeker: Find Apollo Federation documentation
       ↓
Together: Create informed, well-researched plan
```

## Summary

This skill provides:

- ✅ Intelligent documentation discovery
- ✅ Version-specific search results
- ✅ Integration with Context7 MCP
- ✅ Support for CCPM planning and spec writing
- ✅ Implementation guidance from authoritative sources

**Philosophy**: Research first, implement with confidence. Use authoritative sources, always check official documentation, and stay current with latest versions.

---

**Source**: From [claudekit-skills/docs-seeker](https://github.com/mrgoonie/claudekit-skills)
**License**: MIT
**CCPM Integration**: `/ccpm:plan`, `/ccpm:plan`, Context7 MCP
