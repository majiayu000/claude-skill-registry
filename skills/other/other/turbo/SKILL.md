---
name: turbo
description: Hotwire Turbo for Symfony UX. Use when building SPA-like navigation without JS, partial page updates with frames, real-time updates with streams, or integrating with Mercure for broadcasts. Triggers - turbo drive, turbo-frame, turbo-stream, partial page update, SPA feel, ajax navigation, real-time update, Mercure broadcast, Symfony UX Turbo, inline edit, lazy load section, pagination frame, modal from server, flash message stream, multi-section update, TurboStreamResponse, twig:Turbo:Stream, data-turbo, turbo-stream-source, SSE. Also trigger when the user wants to update part of a page without a full reload, or wants real-time server-to-browser updates.
license: MIT
metadata:
  author: Simon Andre
  email: smn.andre@gmail.com
  url: https://smnandre.dev
  version: "1.0"
---

# Turbo

Hotwire Turbo provides SPA-like speed with server-rendered HTML. No JavaScript to write. Three components work together:

- **Drive** -- Automatic AJAX navigation for all links and forms (zero config)
- **Frames** -- Scoped navigation that updates only one section of the page
- **Streams** -- Server-pushed DOM mutations (append, replace, remove, etc.)

## Decision Tree

```
Need to update the page?
+-- Full page navigation          -> Turbo Drive (automatic, already active)
+-- Single section from user click -> Turbo Frame
+-- Multiple sections from action  -> Turbo Stream (HTTP response)
+-- Real-time from server/others   -> Turbo Stream (Mercure / SSE)
```

## Installation

```bash
composer require symfony/ux-turbo
```

That's it. Turbo Drive is active immediately -- all links and forms become AJAX.

## Turbo Drive

Automatic SPA-like navigation. Every `<a>` click and `<form>` submit is intercepted, fetched via AJAX, and the `<body>` is swapped. The browser URL and history update normally.

### Disabling for Specific Elements

```html
<!-- Disable on link/form -->
<a href="/external" data-turbo="false">External Link</a>

<!-- Disable for entire section -->
<div data-turbo="false">
    <a href="/normal">Normal link (no Turbo)</a>
</div>
```

### History and Caching

```html
<!-- Replace history instead of push -->
<a href="/page" data-turbo-action="replace">Replace History</a>

<!-- Force full reload when asset changes -->
<link rel="stylesheet" href="/app.css" data-turbo-track="reload">
<script src="/app.js" data-turbo-track="reload"></script>
```

## Turbo Frames

Scope navigation to a section of the page. Links and forms inside a frame update only that frame's content. The rest of the page stays untouched.

### Basic Frame

```html
<!-- Page with frame -->
<turbo-frame id="messages">
    <h2>Messages</h2>
    <a href="/messages/1">View Message 1</a>  <!-- Updates only this frame -->
</turbo-frame>

<!-- /messages/1 response must contain a matching frame ID -->
<turbo-frame id="messages">
    <h2>Message 1</h2>
    <p>Content here...</p>
    <a href="/messages">Back to list</a>
</turbo-frame>
```

The server response is a full HTML page, but Turbo extracts only the matching `<turbo-frame>` and swaps it in.

### Lazy Loading

Load frame content asynchronously after the page renders:

```html
<turbo-frame id="notifications" src="/notifications" loading="lazy">
    <p>Loading...</p>
</turbo-frame>
```

### Target Another Frame

A link inside one frame can update a different frame:

```html
<turbo-frame id="sidebar">
    <a href="/item/1" data-turbo-frame="main-content">View Item</a>
</turbo-frame>

<turbo-frame id="main-content">
    <!-- Content replaced here -->
</turbo-frame>
```

### Break Out of Frame

Navigate the entire page from within a frame:

```html
<turbo-frame id="modal">
    <a href="/dashboard" data-turbo-frame="_top">Go to Dashboard</a>
</turbo-frame>
```

### Frame with Form

Forms inside frames submit and update within that frame:

```html
<turbo-frame id="search-results">
    <form action="/search" method="get">
        <input type="search" name="q">
        <button>Search</button>
    </form>
    <ul>
        {% for item in results %}
            <li>{{ item.name }}</li>
        {% endfor %}
    </ul>
</turbo-frame>
```

### URL Sync

Update the browser URL when a frame navigates (useful for bookmarkable state):

```html
<turbo-frame id="products" data-turbo-action="advance">
    <!-- Browser URL updates when this frame navigates -->
</turbo-frame>
```

## Turbo Streams

Update multiple DOM elements from a single server response. Eight actions available, each targeting elements by ID or CSS selector.

### Stream Actions

```html
<turbo-stream action="append" target="messages">
    <template><div id="msg_1">New message</div></template>
</turbo-stream>

<turbo-stream action="prepend" target="messages">
    <template><div id="msg_0">First!</div></template>
</turbo-stream>

<turbo-stream action="replace" target="notification">
    <template><div id="notification">Updated!</div></template>
</turbo-stream>

<turbo-stream action="update" target="counter">
    <template>42</template>
</turbo-stream>

<turbo-stream action="remove" target="msg_5"></turbo-stream>

<turbo-stream action="before" target="msg_3">
    <template><div id="msg_2">Inserted before</div></template>
</turbo-stream>

<turbo-stream action="after" target="msg_3">
    <template><div id="msg_4">Inserted after</div></template>
</turbo-stream>

<turbo-stream action="morph" target="user-card">
    <template><div id="user-card">Updated content</div></template>
</turbo-stream>
```

### Target Multiple Elements (CSS Selector)

Use `targets` (plural) with a CSS selector to affect multiple elements:

```html
<turbo-stream action="remove" targets=".notification.read"></turbo-stream>

<turbo-stream action="update" targets=".price">
    <template>99.00 EUR</template>
</turbo-stream>
```

### Twig Component Syntax for Streams

Since Symfony UX 2.22+, you can use `<twig:Turbo:Stream:*>` components instead of raw HTML:

```twig
<twig:Turbo:Stream:Append target="comments">
    {{ include('comment/_comment.html.twig') }}
</twig:Turbo:Stream:Append>

<twig:Turbo:Stream:Update target="comment-count">
    {{ count }}
</twig:Turbo:Stream:Update>

<twig:Turbo:Stream:Remove target="msg_5" />
```

## Symfony Integration

### Stream Response from Controller

```php
use Symfony\UX\Turbo\TurboBundle;

#[Route('/messages', name: 'message_create', methods: ['POST'])]
public function create(Request $request): Response
{
    $message = new Message();
    // ... handle form

    $this->em->persist($message);
    $this->em->flush();

    // Return stream response for Turbo requests
    $request->setRequestFormat(TurboBundle::STREAM_FORMAT);

    return $this->render('message/create.stream.html.twig', [
        'message' => $message,
        'count' => $count,
    ]);
}
```

You can also use the `TurboStreamResponse` helper or `TurboStream` helper methods for programmatic stream building.

### Stream Template

```twig
{# templates/message/create.stream.html.twig #}
<turbo-stream action="append" target="messages">
    <template>
        {{ include('message/_message.html.twig', {message: message}) }}
    </template>
</turbo-stream>
<turbo-stream action="update" target="message-count">
    <template>{{ count }}</template>
</turbo-stream>
<turbo-stream action="replace" target="new-message-form">
    <template>
        {{ include('message/_form.html.twig', {message: null}) }}
    </template>
</turbo-stream>
```

### Detect Frame Request

```php
public function show(Request $request, int $id): Response
{
    if ($request->headers->has('Turbo-Frame')) {
        $frameId = $request->headers->get('Turbo-Frame');
        // Return only the frame content (or a full page -- Turbo extracts the frame)
    }

    return $this->render('page/show.html.twig');
}
```

### Mercure Broadcasts (Real-time)

Push changes to all connected browsers via SSE:

```php
use Symfony\UX\Turbo\Attribute\Broadcast;

#[Broadcast]
class Message
{
    // Entity changes broadcast automatically to subscribed clients
}
```

```twig
{# Subscribe to Mercure topic #}
<turbo-stream-source src="{{ mercure('chat-room-1')|escape('html_attr') }}">
</turbo-stream-source>

<div id="messages">
    {# Messages appear here in real-time #}
</div>
```

## Common Patterns

### Inline Edit

```html
<!-- Display mode -->
<turbo-frame id="task_{{ task.id }}">
    <span>{{ task.title }}</span>
    <a href="/tasks/{{ task.id }}/edit">Edit</a>
</turbo-frame>

<!-- Edit mode (response from /tasks/1/edit) -->
<turbo-frame id="task_1">
    <form action="/tasks/1" method="post">
        <input name="title" value="Task title">
        <button>Save</button>
        <a href="/tasks/1">Cancel</a>
    </form>
</turbo-frame>
```

### Modal in Frame

```html
<turbo-frame id="modal"><!-- Empty by default --></turbo-frame>

<a href="/items/1/delete" data-turbo-frame="modal">Delete</a>

<!-- /items/1/delete response -->
<turbo-frame id="modal">
    <dialog open>
        <p>Confirm delete?</p>
        <form method="post">
            <button>Delete</button>
        </form>
        <a href="/items" data-turbo-frame="modal">Cancel</a>
    </dialog>
</turbo-frame>
```

### Flash Messages with Stream

```twig
<turbo-stream action="prepend" target="flash-messages">
    <template>
        <div class="alert alert-success" role="alert">
            Item saved successfully!
        </div>
    </template>
</turbo-stream>
```

## Key Principles

**Server returns full HTML pages.** Turbo works best when the server always returns a complete, valid HTML page. Turbo Drive replaces the body, Turbo Frames extract the matching frame. Don't try to return partial HTML snippets (except for Stream templates).

**Frame IDs must match.** The frame in the response must have the same `id` as the frame on the page. If they don't match, Turbo shows an error.

**Streams are for side effects.** Use Streams when a single action needs to update multiple unrelated parts of the page. If you're only updating one section, a Frame is simpler.

**Stimulus complements Turbo.** Turbo handles navigation and server communication. Stimulus handles client-side behavior (animations, toggles, clipboard). They work together -- Stimulus controllers survive Turbo Frame swaps within their scope, and reconnect properly on Drive navigation.

## References

- **Full API** (Drive events, Frame attributes, Stream actions, Mercure): [references/api.md](references/api.md)
- **Patterns** (forms, modals, search, pagination, infinite scroll): [references/patterns.md](references/patterns.md)
- **Gotchas** (caching issues, form handling, Stimulus integration): [references/gotchas.md](references/gotchas.md)
