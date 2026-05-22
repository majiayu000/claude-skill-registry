---
name: chrome-ext
description: Chrome Extensions (Manifest V3) performance optimization guidelines (formerly chrome-extensions). This skill should be used when writing, reviewing, or refactoring Chrome extension code to ensure optimal performance patterns. Triggers on tasks involving service workers, content scripts, message passing, storage APIs, or extension development.
---

# Chrome Developer Relations Chrome Extensions Best Practices

Comprehensive performance optimization guide for Chrome Extensions (Manifest V3), maintained by Chrome Developer Relations. Contains 40+ rules across 8 categories, prioritized by impact to guide automated refactoring and code generation.

## When to Apply

Reference these guidelines when:
- Writing new Chrome extension code
- Migrating from Manifest V2 to Manifest V3
- Optimizing service worker lifecycle and state management
- Implementing content scripts for page interaction
- Debugging performance issues in extensions

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Service Worker Lifecycle | CRITICAL | `sw-` |
| 2 | Content Script Optimization | CRITICAL | `content-` |
| 3 | Message Passing Efficiency | HIGH | `msg-` |
| 4 | Storage Operations | HIGH | `storage-` |
| 5 | Network & Permissions | MEDIUM-HIGH | `net-` |
| 6 | Memory Management | MEDIUM | `mem-` |
| 7 | UI Performance | MEDIUM | `ui-` |
| 8 | API Usage Patterns | LOW-MEDIUM | `api-` |

## Quick Reference

### 1. Service Worker Lifecycle (CRITICAL)

- [`sw-persist-state-storage`](references/sw-persist-state-storage.md) - Persist state with chrome.storage instead of global variables
- [`sw-avoid-keepalive`](references/sw-avoid-keepalive.md) - Avoid artificial service worker keep-alive patterns
- [`sw-use-alarms-api`](references/sw-use-alarms-api.md) - Use chrome.alarms instead of setTimeout/setInterval
- [`sw-return-true-async`](references/sw-return-true-async.md) - Return true from message listeners for async responses
- [`sw-register-listeners-toplevel`](references/sw-register-listeners-toplevel.md) - Register event listeners at top level
- [`sw-use-offscreen-for-dom`](references/sw-use-offscreen-for-dom.md) - Use offscreen documents for DOM APIs

### 2. Content Script Optimization (CRITICAL)

- [`content-use-specific-matches`](references/content-use-specific-matches.md) - Use specific URL match patterns
- [`content-use-document-idle`](references/content-use-document-idle.md) - Use document_idle for content script injection
- [`content-programmatic-injection`](references/content-programmatic-injection.md) - Prefer programmatic injection over manifest declaration
- [`content-minimize-script-size`](references/content-minimize-script-size.md) - Minimize content script bundle size
- [`content-batch-dom-operations`](references/content-batch-dom-operations.md) - Batch DOM operations to minimize reflows
- [`content-use-mutation-observer`](references/content-use-mutation-observer.md) - Use MutationObserver instead of polling

### 3. Message Passing Efficiency (HIGH)

- [`msg-use-ports-for-frequent`](references/msg-use-ports-for-frequent.md) - Use port connections for frequent message exchange
- [`msg-minimize-payload-size`](references/msg-minimize-payload-size.md) - Minimize message payload size
- [`msg-debounce-frequent-events`](references/msg-debounce-frequent-events.md) - Debounce high-frequency events before messaging
- [`msg-check-lasterror`](references/msg-check-lasterror.md) - Always check chrome.runtime.lastError
- [`msg-avoid-broadcast-to-all-tabs`](references/msg-avoid-broadcast-to-all-tabs.md) - Avoid broadcasting messages to all tabs

### 4. Storage Operations (HIGH)

- [`storage-batch-operations`](references/storage-batch-operations.md) - Batch storage operations instead of individual calls
- [`storage-choose-correct-type`](references/storage-choose-correct-type.md) - Choose the correct storage type for your use case
- [`storage-cache-frequently-accessed`](references/storage-cache-frequently-accessed.md) - Cache frequently accessed storage values
- [`storage-use-session-for-temp`](references/storage-use-session-for-temp.md) - Use storage.session for temporary runtime data
- [`storage-avoid-storing-large-blobs`](references/storage-avoid-storing-large-blobs.md) - Avoid storing large binary blobs

### 5. Network & Permissions (MEDIUM-HIGH)

- [`net-use-declarativenetrequest`](references/net-use-declarativenetrequest.md) - Use declarativeNetRequest instead of webRequest
- [`net-request-minimal-permissions`](references/net-request-minimal-permissions.md) - Request minimal required permissions
- [`net-use-activetab`](references/net-use-activetab.md) - Use activeTab permission instead of broad host permissions
- [`net-limit-csp-modifications`](references/net-limit-csp-modifications.md) - Avoid modifying Content Security Policy headers

### 6. Memory Management (MEDIUM)

- [`mem-cleanup-event-listeners`](references/mem-cleanup-event-listeners.md) - Clean up event listeners when content script unloads
- [`mem-avoid-detached-dom`](references/mem-avoid-detached-dom.md) - Avoid holding references to detached DOM nodes
- [`mem-avoid-closure-leaks`](references/mem-avoid-closure-leaks.md) - Avoid accidental closure memory leaks
- [`mem-clear-intervals-timeouts`](references/mem-clear-intervals-timeouts.md) - Clear intervals and timeouts on cleanup
- [`mem-use-weak-collections`](references/mem-use-weak-collections.md) - Use WeakMap and WeakSet for DOM element references

### 7. UI Performance (MEDIUM)

- [`ui-minimize-popup-bundle`](references/ui-minimize-popup-bundle.md) - Minimize popup bundle size for fast startup
- [`ui-render-with-cached-data`](references/ui-render-with-cached-data.md) - Render popup UI with cached data first
- [`ui-batch-badge-updates`](references/ui-batch-badge-updates.md) - Batch badge updates to avoid flicker
- [`ui-use-options-page-lazy`](references/ui-use-options-page-lazy.md) - Lazy load options page sections

### 8. API Usage Patterns (LOW-MEDIUM)

- [`api-use-promises-over-callbacks`](references/api-use-promises-over-callbacks.md) - Use promise-based API calls over callbacks
- [`api-query-tabs-efficiently`](references/api-query-tabs-efficiently.md) - Query tabs with specific filters
- [`api-avoid-redundant-api-calls`](references/api-avoid-redundant-api-calls.md) - Avoid redundant API calls in loops
- [`api-use-alarms-minperiod`](references/api-use-alarms-minperiod.md) - Respect alarms API minimum period
- [`api-handle-context-invalidated`](references/api-handle-context-invalidated.md) - Handle extension context invalidated errors
- [`api-use-declarative-content`](references/api-use-declarative-content.md) - Use declarative content API for page actions

## How to Use

Read individual reference files for detailed explanations and code examples:

- [Section definitions](references/_sections.md) - Category structure and impact levels
- [Rule template](assets/templates/_template.md) - Template for adding new rules

## Full Compiled Document

For a complete guide with all rules in a single document, see [AGENTS.md](AGENTS.md).

## Reference Files

| File | Description |
|------|-------------|
| [AGENTS.md](AGENTS.md) | Complete compiled guide with all rules |
| [references/_sections.md](references/_sections.md) | Category definitions and ordering |
| [assets/templates/_template.md](assets/templates/_template.md) | Template for new rules |
| [metadata.json](metadata.json) | Version and reference information |
