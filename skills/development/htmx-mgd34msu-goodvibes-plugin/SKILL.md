---
name: htmx
description: Adds AJAX, CSS Transitions, WebSockets, and Server Sent Events to HTML using attributes. Use when building hypermedia-driven applications, adding interactivity without JavaScript frameworks, or when user mentions HTMX, hx-boost, or HTML-first development.
---

# HTMX

High-power tools for HTML - access AJAX, CSS Transitions, WebSockets and Server Sent Events directly from HTML.

## Quick Start

```html
<!-- Include htmx -->
<script src="https://unpkg.com/htmx.org@2.0.8"></script>

<!-- Basic AJAX request -->
<button hx-get="/api/data" hx-target="#result">
  Load Data
</button>
<div id="result"></div>
```

## Core Attributes

### Request Types

```html
<!-- GET request -->
<button hx-get="/api/users">Load Users</button>

<!-- POST request -->
<form hx-post="/api/users">
  <input name="name" required>
  <button type="submit">Create User</button>
</form>

<!-- PUT request -->
<button hx-put="/api/users/123" hx-vals='{"name": "Updated"}'>
  Update User
</button>

<!-- PATCH request -->
<button hx-patch="/api/users/123" hx-vals='{"status": "active"}'>
  Activate User
</button>

<!-- DELETE request -->
<button hx-delete="/api/users/123" hx-confirm="Are you sure?">
  Delete User
</button>
```

### Targeting

```html
<!-- Target by ID -->
<button hx-get="/content" hx-target="#container">Load</button>
<div id="container"></div>

<!-- Target closest parent matching selector -->
<button hx-get="/row" hx-target="closest tr">Update Row</button>

<!-- Target next sibling -->
<input hx-get="/search" hx-target="next .results" hx-trigger="keyup">
<div class="results"></div>

<!-- Target previous sibling -->
<button hx-get="/status" hx-target="previous .status">Check</button>

<!-- Target find within -->
<div hx-get="/content" hx-target="find .inner">
  <div class="inner"></div>
</div>

<!-- Target this element -->
<button hx-get="/self-update" hx-target="this">
  Click to Update
</button>
```

### Swap Strategies

```html
<!-- Replace inner HTML (default) -->
<div hx-get="/content" hx-swap="innerHTML">Loading...</div>

<!-- Replace entire element -->
<div hx-get="/content" hx-swap="outerHTML">Replace me</div>

<!-- Insert before element -->
<ul hx-get="/item" hx-swap="beforebegin">
  <li>Existing item</li>
</ul>

<!-- Insert after element -->
<ul hx-get="/item" hx-swap="afterend">
  <li>Existing item</li>
</ul>

<!-- Prepend to element -->
<ul hx-get="/item" hx-swap="afterbegin">
  <li>Existing item</li>
</ul>

<!-- Append to element -->
<ul hx-get="/item" hx-swap="beforeend" hx-trigger="click from:button">
  <li>Existing item</li>
</ul>

<!-- Delete target element -->
<button hx-delete="/item/1" hx-target="closest li" hx-swap="delete">
  Remove
</button>

<!-- No swap, just trigger events -->
<button hx-post="/action" hx-swap="none">
  Trigger Action
</button>
```

### Swap Modifiers

```html
<!-- Swap with transition delay -->
<div hx-get="/content" hx-swap="innerHTML swap:500ms">
  Fades out, waits 500ms, then swaps
</div>

<!-- Settle delay (after swap) -->
<div hx-get="/content" hx-swap="innerHTML settle:300ms">
  Swaps, then waits 300ms before settling
</div>

<!-- Scroll to element -->
<div hx-get="/content" hx-swap="innerHTML scroll:top">
  Scrolls to top after swap
</div>

<!-- Show element in viewport -->
<div hx-get="/content" hx-swap="innerHTML show:bottom">
  Shows bottom of element
</div>

<!-- Focus scroll control -->
<div hx-get="/content" hx-swap="innerHTML focus-scroll:false">
  Prevents scroll to focused input
</div>

<!-- View Transitions API -->
<div hx-get="/content" hx-swap="innerHTML transition:true">
  Uses View Transitions API
</div>
```

## Triggers

### Event Triggers

```html
<!-- Click (default for buttons) -->
<button hx-get="/data" hx-trigger="click">Click Me</button>

<!-- Change (default for inputs) -->
<select hx-get="/filter" hx-trigger="change">
  <option value="1">Option 1</option>
</select>

<!-- Submit (default for forms) -->
<form hx-post="/submit" hx-trigger="submit">
  <button type="submit">Submit</button>
</form>

<!-- Keyboard events -->
<input hx-get="/search" hx-trigger="keyup">

<!-- Mouse events -->
<div hx-get="/preview" hx-trigger="mouseenter">
  Hover for preview
</div>

<!-- Custom events -->
<div hx-get="/data" hx-trigger="customEvent from:body">
  Listens for custom event
</div>
```

### Trigger Modifiers

```html
<!-- Delay trigger -->
<input hx-get="/search" hx-trigger="keyup delay:500ms">

<!-- Throttle trigger -->
<div hx-get="/position" hx-trigger="mousemove throttle:100ms">
  Track mouse
</div>

<!-- Only once -->
<button hx-get="/init" hx-trigger="click once">
  Initialize (only works once)
</button>

<!-- Changed filter (only if value changed) -->
<input hx-get="/search" hx-trigger="keyup changed delay:300ms">

<!-- From another element -->
<input id="search" type="text">
<div hx-get="/results" hx-trigger="keyup from:#search delay:300ms">
  Results appear here
</div>

<!-- Multiple triggers -->
<div hx-get="/data" hx-trigger="click, keyup from:body[key='Enter']">
  Multiple triggers
</div>

<!-- Polling -->
<div hx-get="/status" hx-trigger="every 5s">
  Auto-refreshes every 5 seconds
</div>

<!-- Load on page load -->
<div hx-get="/initial" hx-trigger="load">
  Loads on page load
</div>

<!-- Load when revealed (lazy loading) -->
<div hx-get="/lazy" hx-trigger="revealed">
  Loads when scrolled into view
</div>

<!-- Intersect (Intersection Observer) -->
<div hx-get="/more" hx-trigger="intersect threshold:0.5">
  Loads when 50% visible
</div>
```

## hx-boost

```html
<!-- Boost all links and forms in a container -->
<div hx-boost="true">
  <!-- These become AJAX requests -->
  <a href="/page1">Page 1</a>
  <a href="/page2">Page 2</a>

  <form action="/submit" method="post">
    <input name="data">
    <button type="submit">Submit</button>
  </form>

  <!-- Opt out specific elements -->
  <a href="/external" hx-boost="false">External Link</a>
</div>

<!-- Boost with target -->
<body hx-boost="true" hx-target="#main" hx-swap="innerHTML">
  <nav>
    <a href="/">Home</a>
    <a href="/about">About</a>
  </nav>
  <main id="main">
    <!-- Content swaps here -->
  </main>
</body>
```

## Form Handling

### Basic Forms

```html
<!-- Standard form -->
<form hx-post="/api/users" hx-target="#result">
  <input name="name" required>
  <input name="email" type="email" required>
  <button type="submit">Create</button>
</form>
<div id="result"></div>

<!-- Form with JSON encoding -->
<form hx-post="/api/users" hx-ext="json-enc" hx-target="#result">
  <input name="name">
  <button type="submit">Create</button>
</form>
```

### Including Values

```html
<!-- Include values from other elements -->
<input id="filter" name="filter" value="active">
<button hx-get="/users" hx-include="#filter">
  Filter Users
</button>

<!-- Include closest form -->
<form>
  <input name="query">
  <button hx-get="/search" hx-include="closest form">
    Search
  </button>
</form>

<!-- Include all inputs in parent -->
<div>
  <input name="a" value="1">
  <input name="b" value="2">
  <button hx-get="/data" hx-include="this">
    Include both inputs
  </button>
</div>

<!-- Add inline values -->
<button hx-post="/action" hx-vals='{"key": "value", "count": 42}'>
  With Values
</button>

<!-- Dynamic values with JavaScript -->
<button hx-post="/action" hx-vals='js:{timestamp: Date.now()}'>
  Dynamic Value
</button>
```

### Form Validation

```html
<form hx-post="/api/register"
      hx-target="#result"
      hx-indicator=".spinner">

  <label>
    Email
    <input name="email" type="email" required
           hx-get="/api/validate-email"
           hx-trigger="blur"
           hx-target="next .error">
    <span class="error"></span>
  </label>

  <label>
    Password
    <input name="password" type="password" required minlength="8">
  </label>

  <button type="submit">Register</button>
  <span class="spinner htmx-indicator">Loading...</span>
</form>
<div id="result"></div>
```

## Out-of-Band Swaps

```html
<!-- Server can return multiple elements to swap -->
<!-- Response from server: -->
<div id="main-content">
  Main content here
</div>

<div id="notification" hx-swap-oob="true">
  Notification updated!
</div>

<div id="sidebar" hx-swap-oob="innerHTML">
  Sidebar content updated
</div>

<!-- Swap strategy in oob -->
<tr id="row-5" hx-swap-oob="outerHTML">
  Updated row content
</tr>
```

## Indicators

```html
<!-- Show spinner during request -->
<button hx-get="/slow"
        hx-indicator="#spinner">
  Load Data
</button>
<span id="spinner" class="htmx-indicator">Loading...</span>

<!-- Indicator on parent -->
<div hx-indicator=".spinner">
  <button hx-get="/data">Load</button>
  <span class="spinner htmx-indicator">...</span>
</div>

<style>
  /* Default htmx indicator styles */
  .htmx-indicator {
    opacity: 0;
    transition: opacity 200ms ease-in;
  }
  .htmx-request .htmx-indicator {
    opacity: 1;
  }
  .htmx-request.htmx-indicator {
    opacity: 1;
  }
</style>
```

## CSS Transitions

```html
<!-- Swapping classes for transitions -->
<style>
  .fade-me-in.htmx-added {
    opacity: 0;
  }
  .fade-me-in {
    opacity: 1;
    transition: opacity 1s ease-out;
  }
</style>

<button hx-get="/content" hx-swap="innerHTML" hx-target="#container">
  Load
</button>
<div id="container">
  <!-- Content with class="fade-me-in" will animate -->
</div>

<!-- Settling classes -->
<style>
  .my-content.htmx-settling {
    opacity: 0;
  }
  .my-content {
    transition: opacity 0.5s ease-in;
  }
</style>
```

## WebSockets

```html
<!-- Connect to WebSocket -->
<div hx-ext="ws" ws-connect="/ws/chat">
  <div id="messages">
    <!-- Messages appear here via ws-send -->
  </div>

  <form ws-send>
    <input name="message">
    <button type="submit">Send</button>
  </form>
</div>
```

## Server-Sent Events

```html
<!-- Connect to SSE endpoint -->
<div hx-ext="sse" sse-connect="/events">
  <!-- Swap content on specific event -->
  <div sse-swap="message">
    Waiting for messages...
  </div>

  <!-- Trigger htmx request on event -->
  <div hx-get="/data" hx-trigger="sse:update">
    Refreshes on 'update' event
  </div>
</div>
```

## Request Headers

```html
<!-- Add custom headers -->
<button hx-get="/api/data"
        hx-headers='{"X-Custom-Header": "value"}'>
  With Headers
</button>

<!-- HTMX automatically sends these headers: -->
<!-- HX-Request: true -->
<!-- HX-Trigger: <element id> -->
<!-- HX-Trigger-Name: <element name> -->
<!-- HX-Target: <target element id> -->
<!-- HX-Current-URL: <current url> -->
```

## Response Headers

```python
# Server can control htmx behavior via headers

# Redirect
response.headers['HX-Redirect'] = '/new-page'

# Refresh page
response.headers['HX-Refresh'] = 'true'

# Push URL to history
response.headers['HX-Push-Url'] = '/new-url'

# Replace URL without history
response.headers['HX-Replace-Url'] = '/new-url'

# Retarget the swap
response.headers['HX-Retarget'] = '#other-element'

# Change swap strategy
response.headers['HX-Reswap'] = 'outerHTML'

# Trigger client-side events
response.headers['HX-Trigger'] = 'myEvent'
response.headers['HX-Trigger'] = '{"myEvent": {"key": "value"}}'

# Trigger after settle
response.headers['HX-Trigger-After-Settle'] = 'settled'

# Trigger after swap
response.headers['HX-Trigger-After-Swap'] = 'swapped'
```

## Events

```javascript
// Listen for htmx events
document.body.addEventListener('htmx:beforeRequest', function(evt) {
  console.log('Request starting:', evt.detail);
});

document.body.addEventListener('htmx:afterSwap', function(evt) {
  console.log('Swap complete:', evt.detail);
});

document.body.addEventListener('htmx:responseError', function(evt) {
  console.error('Request failed:', evt.detail);
});

// Common events:
// htmx:configRequest - modify request before sending
// htmx:beforeRequest - request about to be made
// htmx:afterRequest - request completed
// htmx:beforeSwap - about to swap content
// htmx:afterSwap - swap completed
// htmx:afterSettle - settling completed
// htmx:responseError - non-2xx response
// htmx:sendError - network error
```

## Configuration

```html
<head>
  <meta name="htmx-config" content='{
    "defaultSwapStyle": "outerHTML",
    "defaultSettleDelay": 100,
    "historyCacheSize": 20,
    "scrollBehavior": "smooth",
    "allowEval": false,
    "globalViewTransitions": true
  }'>
</head>

<script>
  // Or configure via JavaScript
  htmx.config.defaultSwapStyle = 'outerHTML';
  htmx.config.useTemplateFragments = true;
</script>
```

## Extensions

```html
<!-- Load extensions -->
<script src="https://unpkg.com/htmx-ext-json-enc@2.0.0/json-enc.js"></script>
<script src="https://unpkg.com/htmx-ext-loading-states@2.0.0/loading-states.js"></script>

<!-- Use extensions -->
<form hx-ext="json-enc" hx-post="/api/data">
  <input name="field">
  <button>Submit as JSON</button>
</form>

<!-- Loading states -->
<button hx-get="/slow"
        hx-ext="loading-states"
        data-loading-class="is-loading"
        data-loading-disable>
  Click Me
</button>
```

## Preserve Elements

```html
<!-- Preserve element across swaps -->
<div hx-preserve="true" id="video-player">
  <!-- Won't be replaced when parent swaps -->
  <video src="/video.mp4" autoplay></video>
</div>
```

## Reference Files

- [patterns.md](references/patterns.md) - Common HTMX patterns and recipes
- [server-integration.md](references/server-integration.md) - Backend integration examples
