---
name: elephant-build
description: Build multi-file features with unstoppable momentum. Trumpet the vision, gather materials, construct with strength, test thoroughly, and celebrate completion. Use when implementing features that span multiple files or systems.
---

# Elephant Build 🐘

The elephant doesn't hesitate. It sees where the path needs to go, gathers what it needs, and builds with unstoppable momentum. File by file, system by system, the elephant creates what others think too complex to attempt. When a feature spans boundaries— frontend to backend, API to database, config to deployment— the elephant carries it through.

## When to Activate

- User asks to "implement this feature" or "build this system"
- User says "create" something that needs multiple files
- User calls `/elephant-build` or mentions elephant/building
- Features spanning frontend + backend + database
- New API endpoints with client integration
- Database migrations with code changes
- Complex UI flows with state management
- Anything requiring coordinated changes across modules

**Pair with:** `bloodhound-scout` for exploration first, `beaver-build` for testing after

---

## The Build

```
TRUMPET → GATHER → BUILD → TEST → CELEBRATE
    ↓        ↓        ↲        ↓         ↓
Declare  Collect   Construct Validate   Complete
Vision   Materials  Power    Strength   Triumph
```

### Phase 1: TRUMPET

_The elephant lifts its trunk and sounds the beginning..._

Declare what we're building:

**The Vision Statement:**
In one sentence: What does this feature DO for users?

```
"Users can reset their password via email with a secure token link"
"The dashboard shows real-time analytics with filterable date ranges"
```

**Scope Boundaries:**
What's IN:

- Password reset email flow
- Token generation and validation
- UI for requesting reset
- UI for entering new password

What's OUT (for now):

- SMS reset option
- Admin password override
- Password history enforcement

**File Inventory:**
What needs to change?

```
NEW FILES:
- src/lib/services/password-reset.ts
- src/routes/reset-password/+page.svelte
- src/routes/api/auth/reset-request/+server.ts
- src/routes/api/auth/reset-confirm/+server.ts

MODIFIED FILES:
- src/lib/services/email.ts (add reset template)
- src/lib/db/schema.ts (add reset_tokens table)
- src/routes/login/+page.svelte (add "Forgot password?" link)

CONFIG CHANGES:
- .env.example (add RESET_TOKEN_SECRET)
```

**Build Sequence:**

```
1. Database schema
2. Backend services/APIs
3. Frontend components
4. Integration points
5. Tests
```

**Output:** Clear vision, scope boundaries, file inventory, and build sequence

---

### Phase 2: GATHER

_The elephant collects stones and branches, preparing the foundation..._

Collect everything needed before building:

**Dependencies Check:**

```bash
# What do we need?
npm list @sveltejs/kit  # Verify SvelteKit version
npm list zod            # Validation library present?

# Install what's missing
npm install crypto-random-string  # For secure tokens
```

**Pattern Research:**

Use Grove Find to understand existing patterns before building:

```bash
gf --agent impact "src/lib/services/email.ts"  # What depends on the email service?
gf --agent usage "EmailService"                 # Where is this pattern used?
gf --agent func "sendEmail"                     # Find the function's shape
```

Find similar implementations:

```typescript
// Look at: src/lib/services/email.ts
// How do other services send emails?
// What patterns do they follow?

// Look at: src/routes/api/auth/login/+server.ts
// How are API endpoints structured?
// What error handling patterns?

// Look at: src/lib/db/schema.ts
// How are migrations handled?
// What naming conventions?
```

**Environment Setup:**

```bash
# Add required env vars
cat >> .env.local << 'EOF'
RESET_TOKEN_SECRET=$(openssl rand -hex 32)
RESET_TOKEN_EXPIRY=3600
EOF

# Update example file
cat >> .env.example << 'EOF'
RESET_TOKEN_SECRET=generate_with_openssl_rand_hex_32
RESET_TOKEN_EXPIRY=3600
EOF
```

**Documentation Reference:**

- API documentation for external services
- Database schema conventions
- Testing patterns used in this codebase

**Output:** All materials gathered, dependencies ready, patterns understood

---

### Phase 3: BUILD

_The elephant places each stone with precision, building what will last..._

Construct the feature file by file:

**Build Order:**

1. **Database/Foundation** (schema, types, constants)
2. **Backend Services** (business logic, data access)
3. **API Layer** (endpoints, validation, error handling)
4. **Frontend Components** (UI, state management)
5. **Integration** (wiring it all together)

**Example Build Sequence:**

```typescript
// 1. SCHEMA (src/lib/db/schema.ts)
export const passwordResetTokens = sqliteTable('password_reset_tokens', {
  id: integer('id').primaryKey(),
  userId: integer('user_id').references(() => users.id),
  token: text('token').notNull().unique(),
  expiresAt: integer('expires_at', { mode: 'timestamp' }).notNull(),
  createdAt: integer('created_at', { mode: 'timestamp' }).notNull().$defaultFn(() => new Date()),
});

// 2. SERVICE (src/lib/services/password-reset.ts)
export async function createResetToken(userId: number): Promise<string> {
  const token = generateSecureToken(32);
  const expiresAt = new Date(Date.now() + RESET_TOKEN_EXPIRY * 1000);

  await db.insert(passwordResetTokens).values({
    userId,
    token,
    expiresAt,
  });

  return token;
}

export async function validateResetToken(token: string): Promise<number | null> {
  const record = await db.query.passwordResetTokens.findFirst({
    where: eq(passwordResetTokens.token, token),
  });

  if (!record || record.expiresAt < new Date()) {
    return null;
  }

  return record.userId;
}

// 3. API ENDPOINTS (src/routes/api/auth/reset-request/+server.ts)
export const POST: RequestHandler = async ({ request }) => {
  const { email } = await request.json();

  const user = await getUserByEmail(email);
  if (user) {
    // Always return success to prevent email enumeration
    const token = await createResetToken(user.id);
    await sendResetEmail(email, token);
  }

  return json({ success: true });
};

// 4. FRONTEND (src/routes/reset-password/+page.svelte)
<script>
  let email = $state('');
  let submitted = $state(false);
  let loading = $state(false);

  async function handleSubmit() {
    loading = true;
    await fetch('/api/auth/reset-request', {
      method: 'POST',
      body: JSON.stringify({ email }),
    });
    submitted = true;
    loading = false;
  }
</script>

{#if submitted}
  <p>Check your email for reset instructions.</p>
{:else}
  <form on:submit|preventDefault={handleSubmit}>
    <input bind:value={email} type="email" required />
    <button disabled={loading}>
      {loading ? 'Sending...' : 'Send Reset Link'}
    </button>
  </form>
{/if}

// 5. INTEGRATION (src/routes/login/+page.svelte - add link)
<a href="/reset-password">Forgot password?</a>
```

**Track your progress as you build:**

```bash
gw context   # Where are we? What's changed? Stay oriented mid-build
```

**Construction Principles:**

- **One file at a time** — Finish it before moving on
- **Follow existing patterns** — Match the codebase style
- **Use Signpost error codes** — Every error uses a code from the appropriate catalog
- **Validate inputs** — Never trust user data
- **Add types** — TypeScript is your friend

**Error Handling (Signpost Standard):**

API routes return structured errors:

```typescript
import {
  API_ERRORS,
  buildErrorJson,
  logGroveError,
} from "@autumnsgrove/groveengine/errors";

// In +server.ts
if (!locals.user) {
  logGroveError("Engine", API_ERRORS.UNAUTHORIZED, { path: "/api/resource" });
  return json(buildErrorJson(API_ERRORS.UNAUTHORIZED), { status: 401 });
}
```

Client actions show toast feedback:

```typescript
import { toast } from "@autumnsgrove/groveengine/ui";

try {
  await apiRequest("/api/resource", { method: "POST", body });
  toast.success("Created successfully!");
} catch (err) {
  toast.error(err instanceof Error ? err.message : "Something went wrong");
}
```

See `AgentUsage/error_handling.md` for the full Signpost reference.

**Output:** Complete implementation across all required files

---

### Phase 4: TEST

_The elephant tests each stone, ensuring the structure holds..._

**MANDATORY: Verify the build before committing. The elephant does not ship broken structures.**

```bash
# Step 1: Sync dependencies (catches new/changed packages)
pnpm install

# Step 2: Run affected-only CI — lint, check, test, build on ONLY the packages the elephant touched
gw ci --affected --fail-fast --diagnose
```

**If verification fails:** Read the diagnostics. Fix the errors. Re-run verification. The elephant does not move forward on a cracked foundation. Repeat until the structure holds.

**Only when CI passes**, proceed to manual verification:

**Manual Testing Checklist:**

- [ ] Happy path works end-to-end
- [ ] Invalid email handled gracefully
- [ ] Expired token rejected
- [ ] Used token invalidated
- [ ] Error messages clear and helpful
- [ ] Loading states work
- [ ] Mobile layout correct
- [ ] Accessibility (keyboard nav, screen reader)

**Integration Testing:**

```typescript
// Test the full flow
test("password reset flow", async () => {
  // 1. Request reset
  const response = await fetch("/api/auth/reset-request", {
    method: "POST",
    body: JSON.stringify({ email: "user@example.com" }),
  });
  expect(response.ok).toBe(true);

  // 2. Get token from database (test helper)
  const token = await getLatestResetToken("user@example.com");

  // 3. Confirm reset
  const confirm = await fetch("/api/auth/reset-confirm", {
    method: "POST",
    body: JSON.stringify({ token, newPassword: "newpass123" }),
  });
  expect(confirm.ok).toBe(true);

  // 4. Verify can login with new password
  const login = await loginWith("user@example.com", "newpass123");
  expect(login.success).toBe(true);
});
```

**Edge Cases:**

- Network failures
- Database errors
- Invalid/expired tokens
- Concurrent requests
- XSS attempts in inputs

**Output:** All tests passing, manual verification complete, edge cases handled

---

### Phase 5: CELEBRATE

_The elephant raises its trunk in triumph, the build complete..._

Ship the build and document:

```bash
gw git ship --write -a -m "feat(component): brief description of feature"
```

**Completion Summary:**

```markdown
## 🐘 ELEPHANT BUILD COMPLETE

### Feature: Password Reset Flow

#### Files Created (4)

- `src/lib/services/password-reset.ts` — Token generation/validation
- `src/routes/reset-password/+page.svelte` — Request form UI
- `src/routes/api/auth/reset-request/+server.ts` — Request endpoint
- `src/routes/api/auth/reset-confirm/+server.ts` — Confirmation endpoint

#### Files Modified (3)

- `src/lib/db/schema.ts` — Added password_reset_tokens table
- `src/lib/services/email.ts` — Added reset email template
- `src/routes/login/+page.svelte` — Added forgot password link

#### Configuration

- Added RESET_TOKEN_SECRET and RESET_TOKEN_EXPIRY to env

#### Tests Added

- Unit: Token generation/validation
- Integration: Full reset flow
- Edge cases: Expired tokens, invalid emails

### Verification

- ✅ All tests passing (23 tests)
- ✅ TypeScript types valid
- ✅ Linting clean
- ✅ Manual testing complete
- ✅ Security review passed
```

**Documentation Update:**

```markdown
### Password Reset Feature

**How it works:**

1. User enters email on /reset-password
2. System generates secure token (expires in 1 hour)
3. Email sent with reset link
4. User clicks link, enters new password
5. Token invalidated, password updated

**Security considerations:**

- Tokens are single-use
- Same response for valid/invalid emails (prevents enumeration)
- Rate limited to 3 requests per email per hour
- All tokens expire after 1 hour

**Environment variables:**

- `RESET_TOKEN_SECRET` — Cryptographic secret (generate with openssl)
- `RESET_TOKEN_EXPIRY` — Token lifetime in seconds (default: 3600)
```

**Next Steps:**

```markdown
### Recommended Follow-ups

1. [ ] Add rate limiting middleware
2. [ ] Monitor reset email delivery rates
3. [ ] Add analytics for reset success rate
4. [ ] Consider SMS as secondary option
```

**Output:** Feature complete, tested, documented, and ready for production

---

## Elephant Rules

### Momentum

Keep moving forward. Don't get stuck on one file for hours. If blocked, make a TODO and move on. The elephant doesn't stop.

### Completeness

Build the whole feature. Half-built features don't help users. If the scope is too big, scope down—but finish what you start.

### Quality

Build it right the first time. Tests, error handling, types—these aren't extras, they're part of the build.

### Communication

Use building metaphors:

- "Sounding the trumpet..." (declaring the vision)
- "Gathering materials..." (preparation)
- "Placing each stone..." (construction)
- "Testing the structure..." (validation)
- "Build complete!" (celebration)

---

## Anti-Patterns

**The elephant does NOT:**

- Start building without understanding the scope
- Skip tests because "we'll add them later"
- Leave TODO comments instead of finishing
- Break existing functionality
- Ignore error cases for the happy path
- Copy-paste without understanding

---

## Example Build

**User:** "Add a comments system to blog posts"

**Elephant flow:**

1. 🐘 **TRUMPET** — "Users can leave threaded comments on blog posts. Scope: basic CRUD, threaded replies, moderation. Out: real-time updates, reactions."

2. 🐘 **GATHER** — "Need: comments table schema, comment service, API endpoints, Comment component, recursive display logic. Check: existing auth patterns, how posts work."

3. 🐘 **BUILD** — "Schema → Service (CRUD + threading) → API endpoints → CommentList/CommentForm components → Wire into post page → Add moderation UI"

4. 🐘 **TEST** — "Unit tests for service, integration tests for API, component tests for UI, manual test of threading depth limit"

5. 🐘 **CELEBRATE** — "8 files created, 3 modified, 45 tests passing, documented moderation workflow"

---

## Quick Decision Guide

| Situation        | Approach                                           |
| ---------------- | -------------------------------------------------- |
| New API endpoint | Schema → Handler → Tests → Client integration      |
| UI feature       | Component → State management → API wiring          |
| Database change  | Migration → Schema update → Code changes → Tests   |
| Integration      | Bloodhound scout first, then Elephant build        |
| Large feature    | Break into smaller builds, coordinate dependencies |

---

## Integration with Other Skills

**Before Building:**

- `bloodhound-scout` — Explore existing patterns
- `eagle-architect` — For complex system design
- `swan-design` — If detailed specs needed

**During Building:**

- `chameleon-adapt` — For UI polish
- `beaver-build` — For testing strategy

**After Building:**

- `raccoon-audit` — Security review
- `fox-optimize` — If performance issues found
- `deer-sense` — Accessibility audit

---

_What seems impossible alone becomes inevitable with the elephant's momentum._ 🐘
