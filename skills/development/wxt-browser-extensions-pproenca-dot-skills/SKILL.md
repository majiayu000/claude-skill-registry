---
name: wxt-browser-extensions
description: WXT browser extension performance optimization guidelines. This skill should be used when writing, reviewing, or refactoring WXT browser extension code to ensure optimal performance patterns. Triggers on tasks involving WXT, browser extensions, content scripts, service workers, messaging, and extension APIs.
---

# Community WXT Browser Extensions Best Practices

Comprehensive performance optimization guide for WXT browser extension development. Contains 45 rules across 8 categories, prioritized by impact to guide automated refactoring and code generation.

## When to Apply

Reference these guidelines when:
- Writing new WXT browser extension code
- Implementing service worker background scripts
- Injecting content scripts into web pages
- Setting up messaging between extension contexts
- Configuring manifest permissions and resources

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Service Worker Lifecycle | CRITICAL | `svc-` |
| 2 | Content Script Injection | CRITICAL | `inject-` |
| 3 | Messaging Architecture | HIGH | `msg-` |
| 4 | Storage Patterns | HIGH | `store-` |
| 5 | Bundle Optimization | MEDIUM-HIGH | `bundle-` |
| 6 | Manifest Configuration | MEDIUM | `manifest-` |
| 7 | UI Performance | MEDIUM | `ui-` |
| 8 | TypeScript Patterns | LOW-MEDIUM | `ts-` |

## Quick Reference

### 1. Service Worker Lifecycle (CRITICAL)

- [`svc-register-listeners-synchronously`](references/svc-register-listeners-synchronously.md) - Register listeners synchronously to prevent missed events
- [`svc-avoid-global-state`](references/svc-avoid-global-state.md) - Use storage instead of in-memory state
- [`svc-keep-alive-patterns`](references/svc-keep-alive-patterns.md) - Keep service worker alive for long operations
- [`svc-handle-install-update`](references/svc-handle-install-update.md) - Handle install and update lifecycle events
- [`svc-offscreen-documents`](references/svc-offscreen-documents.md) - Use offscreen documents for DOM operations
- [`svc-declarative-net-request`](references/svc-declarative-net-request.md) - Use declarative rules for network blocking

### 2. Content Script Injection (CRITICAL)

- [`inject-use-main-function`](references/inject-use-main-function.md) - Place runtime code inside main() function
- [`inject-choose-correct-world`](references/inject-choose-correct-world.md) - Select ISOLATED or MAIN world appropriately
- [`inject-run-at-timing`](references/inject-run-at-timing.md) - Configure appropriate runAt timing
- [`inject-use-ctx-invalidated`](references/inject-use-ctx-invalidated.md) - Handle context invalidation on update
- [`inject-dynamic-registration`](references/inject-dynamic-registration.md) - Use runtime registration for conditional injection
- [`inject-all-frames`](references/inject-all-frames.md) - Configure allFrames for iframe handling

### 3. Messaging Architecture (HIGH)

- [`msg-return-true-for-async`](references/msg-return-true-for-async.md) - Return true for async message handlers
- [`msg-type-safe-messaging`](references/msg-type-safe-messaging.md) - Define type-safe message protocols
- [`msg-use-tabs-sendmessage`](references/msg-use-tabs-sendmessage.md) - Use tabs.sendMessage for content scripts
- [`msg-use-ports-for-streams`](references/msg-use-ports-for-streams.md) - Use ports for streaming communication
- [`msg-handle-no-receiver`](references/msg-handle-no-receiver.md) - Handle missing message receivers
- [`msg-avoid-circular-messages`](references/msg-avoid-circular-messages.md) - Prevent circular message loops

### 4. Storage Patterns (HIGH)

- [`store-use-define-item`](references/store-use-define-item.md) - Use storage.defineItem for type-safe access
- [`store-choose-storage-area`](references/store-choose-storage-area.md) - Select appropriate storage area
- [`store-batch-operations`](references/store-batch-operations.md) - Batch storage operations
- [`store-watch-for-changes`](references/store-watch-for-changes.md) - Use watch() for reactive updates
- [`store-handle-quota-errors`](references/store-handle-quota-errors.md) - Handle storage quota errors

### 5. Bundle Optimization (MEDIUM-HIGH)

- [`bundle-split-entrypoints`](references/bundle-split-entrypoints.md) - Split code by entrypoint
- [`bundle-analyze-size`](references/bundle-analyze-size.md) - Analyze and monitor bundle size
- [`bundle-tree-shake-icons`](references/bundle-tree-shake-icons.md) - Use direct imports for icon libraries
- [`bundle-externalize-wasm`](references/bundle-externalize-wasm.md) - Load WASM dynamically
- [`bundle-minify-content-scripts`](references/bundle-minify-content-scripts.md) - Minimize content script size

### 6. Manifest Configuration (MEDIUM)

- [`manifest-minimal-permissions`](references/manifest-minimal-permissions.md) - Request minimal permissions
- [`manifest-use-optional-permissions`](references/manifest-use-optional-permissions.md) - Use optional permissions progressively
- [`manifest-web-accessible-resources`](references/manifest-web-accessible-resources.md) - Scope web accessible resources
- [`manifest-content-security-policy`](references/manifest-content-security-policy.md) - Configure CSP correctly
- [`manifest-cross-browser-compatibility`](references/manifest-cross-browser-compatibility.md) - Support multiple browsers

### 7. UI Performance (MEDIUM)

- [`ui-use-shadow-dom`](references/ui-use-shadow-dom.md) - Use Shadow DOM for injected UI
- [`ui-defer-rendering`](references/ui-defer-rendering.md) - Defer popup rendering until needed
- [`ui-cleanup-on-unmount`](references/ui-cleanup-on-unmount.md) - Clean up UI on unmount
- [`ui-sidepanel-persistence`](references/ui-sidepanel-persistence.md) - Preserve sidepanel state
- [`ui-position-fixed-iframe`](references/ui-position-fixed-iframe.md) - Use iframe for complex UI
- [`ui-avoid-layout-thrashing`](references/ui-avoid-layout-thrashing.md) - Batch DOM reads and writes

### 8. TypeScript Patterns (LOW-MEDIUM)

- [`ts-use-browser-not-chrome`](references/ts-use-browser-not-chrome.md) - Use browser namespace over chrome
- [`ts-type-entrypoint-options`](references/ts-type-entrypoint-options.md) - Type entrypoint options explicitly
- [`ts-augment-browser-types`](references/ts-augment-browser-types.md) - Augment types for missing APIs
- [`ts-strict-null-checks`](references/ts-strict-null-checks.md) - Enable strict null checks
- [`ts-import-meta-env`](references/ts-import-meta-env.md) - Use import.meta for build info
- [`ts-avoid-any`](references/ts-avoid-any.md) - Avoid any type in handlers
- [`ts-path-aliases`](references/ts-path-aliases.md) - Use path aliases for imports

## How to Use

Read individual reference files for detailed explanations and code examples:

- [Section definitions](references/_sections.md) - Category structure and impact levels
- [Rule template](assets/templates/_template.md) - Template for adding new rules

## Reference Files

| File | Description |
|------|-------------|
| [references/_sections.md](references/_sections.md) | Category definitions and ordering |
| [assets/templates/_template.md](assets/templates/_template.md) | Template for new rules |
| [metadata.json](metadata.json) | Version and reference information |
