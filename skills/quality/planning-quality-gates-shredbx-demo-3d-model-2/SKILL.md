---
description: Mandatory quality gates and checklists for planning phase - ensures comprehensive planning
tags: [planning, quality, checklist, SDLC, architecture]
related_skills: [dev-philosophy, dev-code-quality, frontend-network-resilience]
applies_to: [Plan]
mandatory: true
---

# Planning Quality Gates

Mandatory checklist for Plan agents to verify before completing planning phase.

**Usage:** Plan agents MUST reference this skill and verify all applicable checks before delivering planning artifacts.

---

## Overview

This skill ensures that planning phase produces comprehensive, production-ready specifications that consider:
- Network resilience
- Error handling
- SSR/UX implications
- Testing requirements
- Deployment safety

---

## Quality Gate 1: Network Operations

**Applies When:** Plan involves:
- External SDK loading (Clerk, Stripe, Google Maps, etc.)
- API calls to backend services
- Third-party API integrations
- CDN resource loading
- WebSocket connections

**Mandatory Checks:**

### Retry Logic
- [ ] Retry strategy is specified (number of attempts, timing)
- [ ] Exponential backoff pattern is used (or justified why not)
- [ ] Total wait time is reasonable (typically 10-40s)
- [ ] Justification provided for retry parameters

**Examples:**
- ✅ "4 attempts with 2s, 4s, 8s backoff (total ~24s)"
- ✅ "No retry - idempotent payment operation, user must confirm"
- ❌ "Use retry logic" (too vague)

### Error Handling
- [ ] Error types are differentiated (offline, timeout, blocked, server_error, etc.)
- [ ] User-friendly error messages defined for each type
- [ ] Manual retry option provided (button)
- [ ] Auto-retry vs manual retry decision is documented

**Example:**
```typescript
Errors to handle:
- offline: "No internet connection. Please check your network."
- timeout: "Connection is very slow. Retrying automatically..."
- blocked: "Resource blocked. Please disable ad blockers."
- server_error: "Server error. We're working on it."
```

### Timeout Strategy
- [ ] Timeout values specified (e.g., 5s per attempt)
- [ ] Total timeout justified (e.g., 4 × 5s = 20s total)
- [ ] Per-attempt vs total timeout clarified
- [ ] Timeout behavior specified (fail vs retry)

### Offline Detection
- [ ] Offline state detection planned (`navigator.onLine`)
- [ ] Offline behavior specified (show banner, disable actions, etc.)
- [ ] Online/offline event listeners planned

### Loading States
- [ ] Loading states defined for all time ranges:
  - 0-1s: Immediate feedback (spinner visible)
  - 1-3s: Basic loading indicator
  - 3-10s: Progress message ("Taking longer than expected...")
  - 10s+: Error state or extended wait message
- [ ] Loading time tracking implemented
- [ ] Progress indicators visible to user

---

## Quality Gate 2: Frontend SSR/UX

**Applies When:** Plan involves:
- SvelteKit pages/routes
- Components that load data
- Client-side only operations
- Progressive enhancement

**Mandatory Checks:**

### SSR Compatibility
- [ ] Network operations only in `onMount` or client-side code
- [ ] Initial loading state present in SSR HTML
- [ ] No server-side `fetch` unless in `+page.server.ts` load function
- [ ] Browser-only APIs guarded (`window`, `document`, `localStorage`)

**Example:**
```typescript
// ✅ SSR-safe
let data = $state(null);
let isLoading = $state(true); // Renders in SSR HTML

onMount(async () => {
  data = await fetch('/api/data');
  isLoading = false;
});
```

### Hydration Transition
- [ ] No flash of incorrect content (FOUC)
- [ ] Loading state visible during hydration
- [ ] Smooth transition from SSR to hydrated state
- [ ] No layout shifts during hydration

### Progressive Enhancement
- [ ] Core content visible without JavaScript (where possible)
- [ ] Graceful degradation if JS disabled
- [ ] Critical actions work without JavaScript (where possible)
- [ ] `<noscript>` fallback provided (if applicable)

### User Feedback
- [ ] User sees feedback within 1 second
- [ ] Loading indicators are visible and clear
- [ ] Error messages are user-friendly and actionable
- [ ] Success states are communicated clearly

---

## Quality Gate 3: Testing Requirements

**Applies When:** All plans (mandatory)

**Mandatory Checks:**

### Test Coverage
- [ ] Unit tests specified (if new functions/utilities)
- [ ] E2E tests specified for user-facing features
- [ ] Test scenarios cover happy path and error cases
- [ ] Performance benchmarks defined (if applicable)

### Error Scenario Testing
- [ ] Success scenario tested
- [ ] Slow network scenario tested (3G simulation)
- [ ] Offline scenario tested
- [ ] Timeout scenario tested
- [ ] Error recovery tested (retry logic)
- [ ] Persistent failure tested (all retries exhausted)

### Browser Compatibility
- [ ] Target browsers specified (Chrome, Firefox, Safari, Edge)
- [ ] Browser-specific issues considered
- [ ] Polyfills identified (if needed)
- [ ] Mobile browsers tested

---

## Quality Gate 4: Deployment Safety

**Applies When:** Plan involves code changes (always)

**Mandatory Checks:**

### Risk Assessment
- [ ] Risk level assessed (low, medium, high)
- [ ] Blast radius identified (which features affected)
- [ ] Rollback plan specified
- [ ] Deployment window identified (low-traffic time)

### Feature Flags
- [ ] Feature flag considered (for high-risk changes)
- [ ] Gradual rollout strategy (if applicable)
- [ ] A/B testing strategy (if applicable)

### Monitoring
- [ ] Success metrics defined
- [ ] Error tracking configured (Sentry, etc.)
- [ ] Performance monitoring (if applicable)
- [ ] User analytics (if applicable)

### Documentation
- [ ] API changes documented
- [ ] User-facing changes documented
- [ ] Team notified of changes
- [ ] Runbook updated (for operations)

---

## Quality Gate 5: Acceptance Criteria

**Applies When:** All plans (mandatory)

**Mandatory Checks:**

### Technical Criteria
- [ ] All technical requirements have acceptance criteria
- [ ] Success metrics are measurable
- [ ] Quality gates are defined (TypeScript, ESLint, tests, etc.)
- [ ] Performance benchmarks specified (if applicable)

### User Story Mapping
- [ ] All user story acceptance criteria addressed
- [ ] Edge cases identified and handled
- [ ] Error scenarios covered
- [ ] Accessibility requirements met

### Definition of Done
- [ ] Code complete
- [ ] Tests passing (unit, integration, E2E)
- [ ] Code reviewed
- [ ] Documentation updated
- [ ] Deployed to staging
- [ ] User acceptance testing complete

---

## Quality Gate 6: Dependencies and Prerequisites

**Applies When:** All plans (mandatory)

**Mandatory Checks:**

### External Dependencies
- [ ] Third-party libraries identified and versions specified
- [ ] API dependencies documented
- [ ] Environment variables required
- [ ] Infrastructure requirements (if any)

### Internal Dependencies
- [ ] Dependent tasks/stories identified
- [ ] Blocking issues documented
- [ ] Team coordination needs specified

### Technical Debt
- [ ] Technical debt created is documented
- [ ] Future improvements identified
- [ ] Workarounds are justified

---

## Quality Gate 7: Official Documentation Validation

**Applies When:** All frontend/backend planning (mandatory)

**Purpose:** Ensure solution follows official framework documentation and web standards

**Mandatory Checks:**

### Framework Documentation (Svelte/SvelteKit)
- [ ] Relevant official documentation sections identified
- [ ] Used `mcp__svelte__list-sections` to find applicable docs
- [ ] Used `mcp__svelte__get-documentation` to fetch official guidance
- [ ] Solution validated against official Svelte 5 patterns
- [ ] Solution validated against official SvelteKit patterns
- [ ] Patterns match official examples and recommendations
- [ ] Any deviations from official patterns are justified

**Required Tools:**
```typescript
// Step 1: List available documentation
mcp__svelte__list-sections()

// Step 2: Identify relevant sections by analyzing use_cases
// Example: For SDK integration, look for:
// - "$effect" (side effects, third-party libraries)
// - "Lifecycle hooks" (onMount, onDestroy)
// - "State management" (SSR considerations)

// Step 3: Fetch relevant documentation
mcp__svelte__get-documentation({
  section: ["$effect", "Lifecycle hooks", "State management"]
})
```

**Validation Checklist:**
- [ ] Reactive patterns (Use `$state`/`$derived`/`$effect` correctly?)
- [ ] Lifecycle (Use `onMount`/`onDestroy` vs `$effect` appropriately?)
- [ ] SSR compatibility (Does code work with server-side rendering?)
- [ ] Component patterns (Follow official component structure?)
- [ ] State management (Use recommended patterns for shared state?)

### Web Standards Documentation
- [ ] Network operations validated against Fetch API standards
- [ ] Browser APIs validated against MDN documentation
- [ ] HTTP patterns validated against RFC specifications
- [ ] Web API usage verified (navigator, FormData, URL, etc.)

**Examples:**
```
Fetch API:
- MDN: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API
- Verify: credentials, headers, CORS, request/response patterns

navigator.onLine:
- MDN: https://developer.mozilla.org/en-US/docs/Web/API/Navigator/onLine
- Verify: event listeners (online/offline), state detection

Web Crypto API:
- MDN: https://developer.mozilla.org/en-US/docs/Web/API/Web_Crypto_API
- Verify: randomUUID, subtle crypto operations
```

### Third-Party Library Documentation
- [ ] External library usage validated against official docs
- [ ] API integration patterns validated against provider documentation
- [ ] SDK initialization patterns follow official examples
- [ ] Error handling follows library recommendations

**Examples:**
```
Clerk SDK:
- Official docs: https://clerk.com/docs
- Verify: initialization, mounting patterns, error handling

Stripe SDK:
- Official docs: https://stripe.com/docs
- Verify: Elements mounting, payment intents, webhooks
```

### Industry Best Practices
- [ ] Retry strategies validated against cloud provider standards (AWS, Google Cloud)
- [ ] Exponential backoff follows industry patterns
- [ ] HTTP status code handling follows RFC 7231
- [ ] Error classification follows HTTP standards

**Standards References:**
```
AWS Retry Strategy:
- https://docs.aws.amazon.com/general/latest/gr/api-retries.html
- Exponential backoff with jitter

Google Cloud Retry:
- https://cloud.google.com/iot/docs/how-tos/exponential-backoff
- Truncated exponential backoff

HTTP Status Codes:
- RFC 7231: https://tools.ietf.org/html/rfc7231
- 4xx client errors, 5xx server errors
```

### Documentation Artifacts

Create validation document in task planning folder:
```
.claude/tasks/TASK-XXX/planning/official-docs-validation.md

Contents:
1. Documentation sources used
2. Validation results (pattern matches)
3. Any deviations with justification
4. References to official docs
```

**Template:**
```markdown
# Official Documentation Validation

## Framework Validation (Svelte 5)

### Pattern: Using onMount for SDK initialization
**Official Guidance:** [quote from docs]
**Our Solution:** [description]
**Validation:** ✅ MATCHES / ❌ DEVIATES
**Justification:** [if deviates, explain why]

## Web Standards Validation

### Pattern: Offline detection
**Standard:** navigator.onLine API
**MDN Reference:** [URL]
**Our Solution:** [description]
**Validation:** ✅ MATCHES

## Third-Party Documentation

### Library: Clerk SDK
**Official Docs:** [URL]
**Pattern Validated:** Mounting pattern
**Validation:** ✅ MATCHES official examples
```

### Common Validation Scenarios

**Scenario 1: External SDK Integration**
```
Must validate:
- ✅ onMount vs $effect decision (Svelte 5 docs)
- ✅ Client-side only execution (SvelteKit SSR docs)
- ✅ Cleanup patterns (Svelte lifecycle hooks docs)
- ✅ Error handling (SDK official docs)
```

**Scenario 2: Data Loading**
```
Must validate:
- ✅ load function patterns (SvelteKit load docs)
- ✅ SSR vs client-side data fetching (SvelteKit docs)
- ✅ Streaming with promises (SvelteKit load docs)
- ✅ Error handling (SvelteKit errors docs)
```

**Scenario 3: Form Handling**
```
Must validate:
- ✅ Form actions (SvelteKit form-actions docs)
- ✅ Progressive enhancement (SvelteKit docs)
- ✅ Validation patterns (Svelte bind docs)
- ✅ FormData usage (Web standards docs)
```

---

## Planning Phase Completion Checklist

Before submitting planning artifacts, verify:

### Artifacts Complete
- [ ] solution-architecture.md created
- [ ] implementation-spec.md created with file-by-file details
- [ ] test-plan.md created with all test scenarios
- [ ] acceptance-criteria.md created with DoD
- [ ] planning-summary.md created for user review

### Quality Gates Passed
- [ ] Network Operations quality gate passed (if applicable)
- [ ] Frontend SSR/UX quality gate passed (if applicable)
- [ ] Testing Requirements quality gate passed
- [ ] Deployment Safety quality gate passed
- [ ] Acceptance Criteria quality gate passed
- [ ] Dependencies quality gate passed
- [ ] Official Documentation Validation quality gate passed

### Reviewability
- [ ] Plan is clear and comprehensive
- [ ] Code examples provided (before/after)
- [ ] Diagrams included (text-based)
- [ ] Rationale explained for key decisions
- [ ] Alternatives considered and documented

### Implementability
- [ ] Implementation agents can execute without additional design decisions
- [ ] File paths and line numbers specified
- [ ] Edge cases and error scenarios covered
- [ ] Testing instructions are clear

---

## When to Skip Quality Gates

Some quality gates may not apply to all tasks. Document exemptions:

**Example:**
```
Quality Gate: Network Operations
Status: SKIPPED
Reason: This task only adds static content (no network operations)
```

**Mandatory Gates (Never Skip):**
- Testing Requirements
- Acceptance Criteria
- Dependencies
- Official Documentation Validation

**Conditional Gates (Skip if Not Applicable):**
- Network Operations (only if no network calls)
- Frontend SSR/UX (only for backend-only tasks)

---

## References

- frontend-network-resilience skill
- dev-philosophy skill
- dev-code-quality skill
- CLAUDE.md Core Directives

---

**Last Updated:** 2025-11-06
**Mandatory:** YES
**Applies To:** All Plan agent tasks
