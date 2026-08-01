---
name: qa-audit
description: App-specific QA audit skill for the Claude Code Cloud web app. Contains
  flow map, test cases, known issues, and mobile-specific tests.
---

# QA Audit: Claude Code Cloud

App-specific QA audit skill for the Claude Code Cloud web app. Contains flow map, test cases, known issues, and mobile-specific tests.

## Activation

Triggers on: "run QA", "audit the app", "regression test", "check for regressions", "mobile QA"

## App Metadata

- **Base URL**: http://localhost:3072 (or configured port)
- **Tech Stack**: Next.js 15, Clerk auth, Hono API
- **Test Credentials**: User's Clerk account
- **Last Full Audit**: 2026-01-02
- **Last QA Run**: 2026-01-02

## Quick Commands

- `/qa-audit` - Run all test cases
- `/qa-audit regression` - Run P0 tests only
- `/qa-audit mobile` - Run mobile-specific tests
- `/qa-audit [flow-name]` - Run specific flow tests

## Flow Map

### Screens Inventory

| ID  | Screen           | URL                       | Purpose          | Key Elements                           |
| --- | ---------------- | ------------------------- | ---------------- | -------------------------------------- |
| S01 | Landing          | /                         | Marketing page   | Hero, CTA, feature grid                |
| S02 | Sign In          | /sign-in                  | Clerk auth       | Clerk component                        |
| S03 | Sign Up          | /sign-up                  | Registration     | Clerk component                        |
| S04 | Dashboard        | /dashboard                | Workspace list   | Header, workspace cards, new button    |
| S05 | Setup            | /dashboard/setup          | VM provisioning  | Progress indicator                     |
| S06 | New Workspace    | /dashboard/new            | Create workspace | Form fields                            |
| S07 | Workspace Detail | /dashboard/workspace/[id] | Terminal view    | Header, breadcrumb, terminal, settings |

### Navigation Graph

```
Landing (/)
  ├── Sign In → Dashboard
  └── Sign Up → Dashboard/Setup

Dashboard (/dashboard)
  ├── New Workspace → Dashboard (after creation)
  └── Workspace Card → Workspace Detail

Workspace Detail (/dashboard/workspace/[id])
  ├── ← WORKSPACES breadcrumb → Dashboard
  ├── Logo click → Dashboard
  └── Workspaces button → Dashboard
```

### User Journeys

1. **J01 - New User**: Landing → Sign Up → Setup → Dashboard
2. **J02 - Returning User**: Landing → Sign In → Dashboard
3. **J03 - Create Workspace**: Dashboard → New → Form → Dashboard
4. **J04 - Access Terminal**: Dashboard → Workspace Card → Terminal
5. **J05 - Return to Dashboard**: Terminal → (breadcrumb/logo/button) → Dashboard

## Test Case Library

### P0 - Critical (Every Release)

| ID     | Title                          | Category   | Steps                                                       |
| ------ | ------------------------------ | ---------- | ----------------------------------------------------------- |
| TC-001 | Landing page loads             | Happy Path | Navigate to /, verify hero visible                          |
| TC-002 | Sign in redirects to dashboard | Happy Path | Click Sign In, complete auth, verify /dashboard             |
| TC-003 | Dashboard shows workspaces     | Happy Path | Go to /dashboard, verify workspace list                     |
| TC-004 | Workspace detail loads         | Happy Path | Click workspace card, verify terminal section               |
| TC-005 | Navigation back to dashboard   | Happy Path | From workspace, click logo or breadcrumb, verify /dashboard |

### P1 - Important (Mobile-Specific)

| ID     | Title                          | Category | Steps                                                             |
| ------ | ------------------------------ | -------- | ----------------------------------------------------------------- |
| TC-010 | Header visible on mobile       | Mobile   | Set 375px viewport, verify all header elements visible or in menu |
| TC-011 | Nav items accessible on mobile | Mobile   | Verify all nav functionality works at 375px                       |
| TC-012 | Touch targets 44px minimum     | Mobile   | Verify buttons/links have adequate touch area                     |
| TC-013 | No horizontal overflow         | Mobile   | Check no horizontal scroll at 375px                               |
| TC-014 | Terminal usable on mobile      | Mobile   | Verify terminal section fills available space                     |

### P2 - Standard

| ID     | Title                | Category   | Steps                                |
| ------ | -------------------- | ---------- | ------------------------------------ |
| TC-020 | Create new workspace | Happy Path | Dashboard → New → Fill form → Submit |
| TC-021 | Fullscreen terminal  | Feature    | Click MAXIMIZE, verify fullscreen    |
| TC-022 | Settings toggle      | Feature    | Toggle network mode                  |

## Known Issues & Workarounds

| Issue                     | Severity | Status | Description                                       |
| ------------------------- | -------- | ------ | ------------------------------------------------- |
| Header overflow on mobile | Major    | Open   | Nav items cut off at 375px - email/signout hidden |
| Button overlap            | Minor    | Open   | "+ NEW WORKSPACE" overlaps "Workspaces" heading   |
| Small breadcrumb          | Minor    | Open   | "← WORKSPACES" is 0.75rem, not touch-optimized    |

## Mobile Breakpoints to Test

| Viewport | Device            | Priority |
| -------- | ----------------- | -------- |
| 375x812  | iPhone 13/14      | P0       |
| 390x844  | iPhone 14 Pro     | P1       |
| 428x926  | iPhone 14 Pro Max | P1       |
| 768x1024 | iPad              | P1       |
| 1024x768 | iPad Landscape    | P2       |

## App-Specific Heuristics

### What Typically Breaks

- Header at narrow viewports (no responsive handling)
- Terminal height calculation on small screens
- Long email addresses overflow nav

### Patterns to Watch

- Inline styles with fixed values (no media queries)
- `display: flex; gap: X` without wrap
- `calc(100vh - Xpx)` height calculations

### Known Fragile Areas

- `apps/web/src/components/Header.tsx` - no mobile breakpoints
- `apps/web/src/components/TerminalSection.tsx` - fixed height calc
- `apps/web/src/app/globals.css` - only one @media query at 768px

## Screenshot Archive

| Date       | Directory                     | Notes                |
| ---------- | ----------------------------- | -------------------- |
| 2026-01-02 | /tmp/ux-qa/claude-code-cloud/ | Initial mobile audit |

## Last Run Results

| Date       | Tests        | Passed | Failed | Notes                                           |
| ---------- | ------------ | ------ | ------ | ----------------------------------------------- |
| 2026-01-02 | Visual Audit | -      | -      | Initial discovery, found header overflow issues |

## Dev Browser Setup

```bash
# Start server
cd skills/dev-browser && ./server.sh &

# Mobile viewport test
cd skills/dev-browser && npx tsx <<'EOF'
import { connect, waitForPageLoad } from "@/client.js";
const client = await connect();
const page = await client.page("mobile-test");
await page.setViewportSize({ width: 375, height: 812 });
await page.goto("http://localhost:3072");
await waitForPageLoad(page);
await page.screenshot({ path: "/tmp/qa-test.png" });
await client.disconnect();
EOF
```
