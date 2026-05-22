---
name: htmx
description: |
  htmx gives you access to AJAX, CSS transitions, WebSockets, and Server-Sent Events
  directly in HTML using attributes. It enables dynamic web UIs without writing JavaScript
  by letting any element issue HTTP requests and swap content into the DOM.
license: Apache-2.0
compatibility: 'any web server, html'
metadata:
  author: terminal-skills
  version: 1.0.0
  category: development
  tags:
    - html
    - hypermedia
    - ajax
    - sse
    - websocket
    - no-javascript
---

# htmx

htmx extends HTML with attributes like `hx-get`, `hx-post`, `hx-swap`, and `hx-trigger` to make any element capable of issuing HTTP requests and updating the DOM. The server returns HTML fragments, not JSON.

## Installation

```html
<!-- index.html — add htmx via CDN or npm -->
<script src="https://unpkg.com/htmx.org@2.0.4"></script>
<!-- Or: npm install htmx.org -->
```

## Core Attributes

```html
<!-- templates/core-demo.html — fundamental htmx attributes -->

<!-- GET request, replace inner HTML of target -->
<button hx-get="/api/articles" hx-target="#article-list" hx-swap="innerHTML">
  Load Articles
</button>
<div id="article-list"></div>

<!-- POST form without page reload -->
<form hx-post="/api/articles" hx-target="#article-list" hx-swap="afterbegin">
  <input name="title" placeholder="Title" required />
  <textarea name="body" placeholder="Body" required></textarea>
  <button type="submit">Create</button>
</form>

<!-- DELETE with confirmation -->
<button hx-delete="/api/articles/42" hx-confirm="Are you sure?" hx-target="closest article" hx-swap="outerHTML swap:500ms">
  Delete
</button>
```

## Swap Strategies

```html
<!-- templates/swap-strategies.html — different ways to insert content -->

<!-- Replace inner content (default) -->
<div hx-get="/fragment" hx-swap="innerHTML">Replace my contents</div>

<!-- Replace entire element -->
<div hx-get="/fragment" hx-swap="outerHTML">Replace me entirely</div>

<!-- Append/prepend to list -->
<div id="list">
  <button hx-get="/more" hx-target="#list" hx-swap="beforeend">Load More</button>
</div>

<!-- Swap with transition delay -->
<div hx-get="/fragment" hx-swap="innerHTML settle:300ms">With transition</div>

<!-- Out-of-band swaps (update multiple elements) -->
<!-- Server returns: -->
<!-- <div id="notification" hx-swap-oob="innerHTML">New notification!</div> -->
<!-- <div id="count" hx-swap-oob="innerHTML">43</div> -->
```

## Triggers

```html
<!-- templates/triggers.html — custom event triggers -->

<!-- Trigger on input change with debounce -->
<input type="search" name="q"
  hx-get="/search"
  hx-trigger="input changed delay:300ms"
  hx-target="#results" />
<div id="results"></div>

<!-- Trigger on intersection (lazy loading) -->
<div hx-get="/more-articles"
  hx-trigger="intersect once"
  hx-swap="afterend">
  Loading...
</div>

<!-- Trigger on custom event -->
<div hx-get="/notifications" hx-trigger="newMessage from:body">
  Notifications
</div>

<!-- Polling -->
<div hx-get="/api/status" hx-trigger="every 5s">
  Status: checking...
</div>
```

## Server Responses (Python/Django Example)

```python
# views.py — server returns HTML fragments, not JSON
from django.shortcuts import render
from django.http import HttpResponse

def article_list(request):
    articles = Article.objects.filter(published=True)[:20]
    return render(request, "partials/article_list.html", {"articles": articles})

def create_article(request):
    form = ArticleForm(request.POST)
    if form.is_valid():
        article = form.save()
        return render(request, "partials/article_card.html", {"article": article})
    return render(request, "partials/article_form.html", {"form": form}, status=422)

def delete_article(request, pk):
    Article.objects.filter(pk=pk).delete()
    return HttpResponse("")  # Empty response removes element with outerHTML swap
```

```html
<!-- templates/partials/article_card.html — HTML fragment returned by server -->
<article id="article-{{ article.id }}">
  <h2>{{ article.title }}</h2>
  <p>{{ article.body|truncatewords:30 }}</p>
  <button hx-delete="/api/articles/{{ article.id }}"
    hx-target="#article-{{ article.id }}"
    hx-swap="outerHTML swap:300ms"
    hx-confirm="Delete this article?">
    Delete
  </button>
</article>
```

## Indicators

```html
<!-- templates/indicators.html — loading indicators -->

<!-- Show spinner during request -->
<button hx-get="/slow-endpoint" hx-indicator="#spinner">
  Load Data
</button>
<span id="spinner" class="htmx-indicator">Loading...</span>

<!-- CSS (htmx adds .htmx-request class during requests) -->
<style>
  .htmx-indicator { display: none; }
  .htmx-request .htmx-indicator { display: inline; }
  .htmx-request.htmx-indicator { display: inline; }
</style>
```

## Headers and Request Config

```html
<!-- templates/request-config.html — request customization -->

<!-- Include extra values -->
<button hx-post="/api/vote" hx-vals='{"article_id": 42, "vote": "up"}'>
  Upvote
</button>

<!-- Include values from other elements -->
<input id="search-input" name="q" />
<button hx-get="/search" hx-include="#search-input">Search</button>

<!-- Push URL to browser history -->
<a hx-get="/articles/my-article" hx-push-url="true" hx-target="#content">
  My Article
</a>
```

## Server-Sent Events

```html
<!-- templates/sse.html — real-time updates with SSE -->
<div hx-ext="sse" sse-connect="/events/articles">
  <div sse-swap="newArticle" hx-swap="afterbegin">
    <!-- New articles appear here in real-time -->
  </div>
</div>
```

```python
# views.py — SSE endpoint
import json
from django.http import StreamingHttpResponse

def article_events(request):
    def event_stream():
        for article in listen_for_new_articles():
            html = render_to_string("partials/article_card.html", {"article": article})
            yield f"event: newArticle\ndata: {html}\n\n"
    return StreamingHttpResponse(event_stream(), content_type="text/event-stream")
```

## WebSocket

```html
<!-- templates/ws.html — WebSocket integration -->
<div hx-ext="ws" ws-connect="/ws/chat">
  <div id="messages"></div>
  <form ws-send>
    <input name="message" placeholder="Type a message..." />
    <button type="submit">Send</button>
  </form>
</div>
```

## Boosting (Progressive Enhancement)

```html
<!-- templates/boost.html — make regular links/forms use AJAX -->
<body hx-boost="true">
  <!-- All links and forms in this body now use AJAX -->
  <nav>
    <a href="/articles">Articles</a>  <!-- AJAX navigation -->
    <a href="/about">About</a>
  </nav>
  <main id="content">
    <!-- Content swapped here -->
  </main>
</body>
```

## Key Patterns

- Server returns HTML fragments, not JSON — this is hypermedia, not REST
- Use `hx-target` to control where responses are inserted; `hx-swap` controls how
- Use `hx-trigger` with modifiers (`delay`, `throttle`, `changed`, `once`) for precise control
- Use `hx-boost="true"` on `<body>` for easy progressive enhancement of existing sites
- Use `hx-swap-oob` for updating multiple page sections from a single response
- Use `hx-indicator` for loading states — htmx manages the CSS class automatically
- Use `hx-push-url` to update browser URL for back-button support
