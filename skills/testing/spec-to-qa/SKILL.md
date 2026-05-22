---
name: spec-to-qa
description: |
  Reads any PRD, spec, or requirements document and generates comprehensive QA
  test scenarios. Covers happy paths, edge cases, error handling, and accessibility.
  Use when you have a spec and need a testing checklist.
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Glob
---

# Spec to QA

Generate comprehensive test scenarios from any specification document.

---

## Quick Start

1. **Point it at a spec.** Run `/spec-to-qa path/to/prd.md` or paste requirements text directly.
2. **Review the output.** The skill writes a prioritized QA checklist to `tasks/qa-[feature-name].md` with happy paths, edge cases, error handling, and accessibility checks in Given/When/Then format.
3. **Use the checklist.** Run through it manually, convert scenarios to automated tests, or hand it to your QA team. Update later with `/spec-to-qa update` when the spec changes.

---

## Overview

Takes a PRD, spec, or requirements document and produces a structured QA checklist covering:

- Happy path scenarios
- Edge cases
- Error handling
- Accessibility checks
- Performance considerations
- Security checks (where applicable)

---

## The Job

### Input

Any of:
- Path to a PRD/spec markdown file
- Pasted requirements text
- A feature description

### Output

A QA checklist saved to `tasks/qa-[feature-name].md`.

---

## Commands

### `/spec-to-qa [path-or-text]`

Generate QA scenarios from the given spec.

### `/spec-to-qa update [qa-path] [spec-path]`

Update an existing QA checklist when the spec changes. Adds new scenarios, marks removed ones.

---

## Process

### Step 1: Parse the Spec

Read the document and identify:

1. **Screens/Pages**: Each distinct view or page
2. **User Actions**: What can users do? (click, type, submit, navigate)
3. **Data Flows**: What data moves where? (input -> API -> database -> display)
4. **State Changes**: What state transitions exist? (loading, error, success, empty)
5. **Roles**: Who interacts? (user, admin, anonymous)
6. **Integrations**: External dependencies (APIs, services, auth)

### Step 2: Generate Scenarios Per Screen

For each screen/feature, generate scenarios in 5 categories.

### Step 3: Cross-Cutting Concerns

Add scenarios for concerns that span multiple screens.

### Step 4: Prioritize

Mark each scenario with priority:
- **P0**: Must pass before release (happy path, data integrity)
- **P1**: Should pass (common edge cases, error handling)
- **P2**: Nice to have (uncommon edge cases, polish)

---

## Output Format

Use the template at `templates/qa-template.md` as the base structure.

```markdown
# QA Test Plan: [Feature Name]

**Source Spec**: [path or link]
**Generated**: [date]
**Total Scenarios**: [N]
**Coverage**: [screens/features covered]

---

## Screen: [Screen Name]

### Happy Path (P0)
- [ ] **[ID]** [Scenario description]
  - Given: [precondition]
  - When: [action]
  - Then: [expected result]

### Edge Cases (P1)
- [ ] **[ID]** [Scenario description]
  - Given: [precondition]
  - When: [action]
  - Then: [expected result]

### Error Handling (P1)
- [ ] **[ID]** [Scenario description]
  - Given: [precondition]
  - When: [action]
  - Then: [expected result]

### Accessibility (P1)
- [ ] **[ID]** [Check description]

### Security (P0)
- [ ] **[ID]** [Check description]

---

## Cross-Cutting Concerns

### Performance
- [ ] **[ID]** [Scenario]

### Data Integrity
- [ ] **[ID]** [Scenario]

### Browser/Device Compatibility
- [ ] **[ID]** [Scenario]
```

---

## Scenario Generation Rules

### Happy Path

For each user story or functional requirement, create at least one happy path scenario:

- User completes the primary action successfully
- Data is saved/displayed correctly
- Correct feedback is shown (toast, redirect, update)

### Edge Cases

Think about boundaries and unusual-but-valid inputs:

| Area | Edge Cases to Consider |
|---|---|
| Text inputs | Empty, very long, special characters, unicode, emoji, HTML/script tags |
| Numbers | Zero, negative, decimals, very large, NaN |
| Lists | Empty list, single item, many items (100+), pagination boundary |
| Dates | Past, future, today, timezone differences, invalid formats |
| Files | Empty file, large file, wrong format, multiple files |
| State | Loading, error, empty, first-time, returning user |
| Network | Slow connection, timeout, offline, retry |

### Error Handling

For each action that can fail:

- API returns 400 (bad request)
- API returns 401/403 (unauthorized)
- API returns 404 (not found)
- API returns 500 (server error)
- Network timeout
- Validation failure (client-side)
- Concurrent modification conflict

### Accessibility

For each screen:

- [ ] All interactive elements reachable via keyboard (Tab, Enter, Escape)
- [ ] Screen reader announces content correctly
- [ ] Color is not the only means of conveying information
- [ ] Focus management on modal open/close
- [ ] Error messages associated with form fields
- [ ] Sufficient color contrast (WCAG AA: 4.5:1 for text)
- [ ] Touch targets at least 44x44px on mobile

### Security

Where applicable:

- [ ] Input sanitization (XSS prevention)
- [ ] Authorization checks (can't access others' data)
- [ ] Rate limiting on sensitive endpoints
- [ ] CSRF protection on state-changing requests
- [ ] Sensitive data not exposed in URLs or logs

---

## Important Notes

- Generate scenario IDs as `[Screen]-[Category]-[Number]`: e.g., `LOGIN-HP-001`
- Be specific in Given/When/Then. Avoid vague language.
- Prioritize every scenario (P0/P1/P2).
- Group by screen/feature, then by category.
- Include both manual and automatable scenarios.

---

## API Testing

When the spec describes REST or GraphQL endpoints, generate scenarios specific to API behavior. These go in a dedicated `## API Endpoints` section in the output.

### REST Endpoint Scenarios

For each endpoint, generate scenarios covering:

| Category | Scenarios |
|---|---|
| Status codes | 200/201 on success, 400 on bad input, 401 without auth, 403 with wrong role, 404 on missing resource, 409 on conflict, 422 on validation failure, 429 on rate limit, 500 on server fault |
| Pagination | First page returns correct count, last page returns remainder, page beyond max returns empty array (not error), `page=0` and `page=-1` handled, default page size applied when omitted |
| Rate limiting | Requests under limit succeed, request at limit returns 429, rate limit headers present (`X-RateLimit-Remaining`, `Retry-After`), limit resets after window |
| Authentication | Valid token accepted, expired token returns 401, malformed token returns 401, missing token returns 401, token with wrong scope returns 403 |
| Request body | Required fields missing returns 400 with field-level errors, extra fields ignored (or rejected, per spec), empty body handled, content-type mismatch returns 415 |
| Response shape | All documented fields present, field types match spec (string vs number vs null), nested objects have correct structure, empty collections return `[]` not `null` |
| Idempotency | POST with same idempotency key returns same response, PUT is idempotent on retry, DELETE on already-deleted returns 404 (or 204, per spec) |

### GraphQL-Specific Scenarios

| Category | Scenarios |
|---|---|
| Query depth | Nested query within allowed depth succeeds, query exceeding max depth returns error |
| N+1 | List query with nested relation does not cause N+1 (check with query complexity analysis or response time) |
| Partial errors | Query with one valid field and one unauthorized field returns data + errors array |
| Mutations | Mutation returns updated object, mutation with invalid input returns `errors` with path |
| Subscriptions | Subscription receives event after mutation, subscription disconnects cleanly on client close |

### Scenario ID Format for APIs

Use `API-[ENDPOINT]-[CATEGORY]-[NUMBER]`, e.g., `API-USERS-AUTH-001`.

---

## Mobile-Specific Testing

When the spec targets a mobile app (iOS, Android, or cross-platform), add a `## Mobile` section with these scenarios.

### Device and OS

- [ ] App works on minimum supported OS version
- [ ] App works on latest OS version
- [ ] App works on smallest supported screen size (e.g., iPhone SE, 4-inch Android)
- [ ] App works on tablet if tablet is a target
- [ ] App handles orientation change without losing state (form inputs, scroll position)
- [ ] App handles split-screen / multitasking mode (iPad, Android foldables)

### Gestures and Interaction

- [ ] Swipe-to-delete works and shows undo option
- [ ] Pull-to-refresh triggers data reload
- [ ] Long press shows context menu (if applicable)
- [ ] Back gesture/button navigates correctly (does not exit app unexpectedly)
- [ ] Pinch-to-zoom works on zoomable content, is disabled on non-zoomable content
- [ ] Scroll position preserved on back navigation

### Push Notifications

- [ ] Notification received when app is in foreground (banner or in-app alert, per spec)
- [ ] Notification received when app is in background
- [ ] Tapping notification opens correct screen (deep link target)
- [ ] Notification with expired/invalid deep link shows fallback gracefully
- [ ] User with notifications disabled sees no errors

### Offline Mode

- [ ] App shows meaningful state when offline (cached data, offline banner)
- [ ] Queued actions sync when connectivity returns
- [ ] Conflict resolution works when offline edit conflicts with server state
- [ ] App does not crash on network timeout during a write operation
- [ ] Airplane mode toggle mid-request is handled

### Deep Links

- [ ] Deep link to existing content opens correct screen
- [ ] Deep link to non-existent content shows 404 or fallback
- [ ] Deep link while logged out redirects to login, then to target after auth
- [ ] Universal links / App Links open in app (not browser) when app is installed
- [ ] Deep link with query parameters passes them correctly

### Scenario ID Format for Mobile

Use `MOB-[SCREEN]-[CATEGORY]-[NUMBER]`, e.g., `MOB-PROFILE-OFFLINE-001`.

---

## Automation Hooks

Generated scenarios follow Given/When/Then format intentionally. Here is how to convert them into executable test code for common frameworks.

### Jest / Vitest (Unit and Integration)

Map each scenario directly to a `describe` + `it` block:

```typescript
// From: LOGIN-HP-001
// Given: User is on login page with valid credentials
// When: User submits the login form
// Then: User is redirected to dashboard

describe('Login Page', () => {
  it('LOGIN-HP-001: redirects to dashboard on valid login', async () => {
    // Given
    render(<LoginPage />);
    await userEvent.type(screen.getByLabelText('Email'), 'user@test.com');
    await userEvent.type(screen.getByLabelText('Password'), 'validpass');

    // When
    await userEvent.click(screen.getByRole('button', { name: 'Log in' }));

    // Then
    expect(mockRouter.push).toHaveBeenCalledWith('/dashboard');
  });
});
```

### Playwright (E2E)

```typescript
// From: LOGIN-ERR-002
// Given: User is on login page
// When: User submits with wrong password
// Then: Error message "Invalid credentials" is shown

test('LOGIN-ERR-002: shows error on wrong password', async ({ page }) => {
  // Given
  await page.goto('/login');

  // When
  await page.fill('[name="email"]', 'user@test.com');
  await page.fill('[name="password"]', 'wrongpass');
  await page.click('button[type="submit"]');

  // Then
  await expect(page.locator('[role="alert"]')).toContainText('Invalid credentials');
});
```

### Cypress

```typescript
// From: DASH-HP-001
// Given: Authenticated user
// When: User visits dashboard
// Then: KPI cards display current data

describe('Dashboard', () => {
  it('DASH-HP-001: displays KPI cards for authenticated user', () => {
    // Given
    cy.login('user@test.com', 'validpass');

    // When
    cy.visit('/dashboard');

    // Then
    cy.get('[data-testid="kpi-card"]').should('have.length.at.least', 1);
    cy.get('[data-testid="kpi-card"]').first().should('not.contain', 'Loading');
  });
});
```

### Conversion Tips

- Keep the scenario ID as the test name prefix. This links test failures back to the QA checklist.
- The "Given" maps to test setup (rendering, navigation, seeding data).
- The "When" maps to user actions (clicks, typing, API calls).
- The "Then" maps to assertions.
- P0 scenarios are your first automation targets. P2 scenarios may not justify automation cost.

---

## Templates

See `templates/qa-template.md` for the full output template.
