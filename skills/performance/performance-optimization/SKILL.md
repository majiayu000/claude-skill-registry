---
name: performance-optimization
description: Master perceived performance through optimistic UI, skeleton screens, and latency strategies. Learn the difference between actual and perceived latency. Use when optimizing load times, designing loading states, or improving user confidence during operations.
---

# Performance Optimization: Perceived vs Actual Latency

## Overview

**Perceived latency is more important than actual latency.** A 3-second operation that feels instant is better than a 1-second operation that feels slow. This skill teaches you to optimize how fast your interface *feels*, not just how fast it actually is.

## Core Principle: The Linear Method

The "Linear Method" popularized by Linear.com prioritizes a steady cadence of quality over frantic sprints. Applied to performance, this means:

**Speed is a feature, but perceived speed is the ultimate UX.**

When a user creates a task, the UI should show it as created *instantly*. The network request happens in the background. If it fails, the UI gracefully rolls back. This pattern builds trust—users know the system will handle the details.

## Actual vs Perceived Latency

### Actual Latency

The real time it takes for an operation to complete (measured in milliseconds).

```javascript
// Actual latency: 2000ms
const startTime = performance.now();
const result = await fetch('/api/data');
const endTime = performance.now();
console.log(`Actual latency: ${endTime - startTime}ms`);
```

### Perceived Latency

How fast the operation *feels* to the user. This is what matters.

**Factors that affect perceived latency:**
- Visual feedback (does something happen immediately?)
- Progress indication (is the user informed of progress?)
- Anticipation (does the UI predict what's coming?)
- Momentum (does the interface feel responsive?)

## The Latency Spectrum

### < 100ms: Instant

No feedback needed. The user perceives this as instant.

```javascript
// Instant - no loading state needed
const handleClick = () => {
  updateLocalState();  // Instant
  // Network request in background
  fetch('/api/update').catch(() => rollback());
};
```

### 100ms - 1s: Subtle Feedback

Show a subtle indicator. A loading spinner is overkill; a slight opacity change or color shift is enough.

```css
/* Subtle feedback for 100-1000ms operations */
.button.loading {
  opacity: 0.7;
  cursor: wait;
}

/* Or a subtle pulse */
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}

.button.loading {
  animation: pulse 1s ease-in-out infinite;
}
```

### 1s - 10s: Skeleton or Spinner

Show a skeleton screen (if layout is known) or spinner (if layout is unknown).

```html
<!-- Skeleton for known layout -->
<div class="card-skeleton">
  <div class="skeleton skeleton-image"></div>
  <div class="skeleton skeleton-text"></div>
  <div class="skeleton skeleton-text"></div>
</div>

<!-- Spinner for unknown layout -->
<div class="spinner"></div>
```

### > 10s: Progress Bar

Show a progress bar with time estimate.

```html
<div class="progress-container">
  <div class="progress-bar" style="width: 65%"></div>
  <span class="progress-text">Uploading... 2 of 3 files</span>
</div>
```

## Optimistic UI: The Gold Standard

Optimistic UI shows changes immediately, then syncs with the server.

### Pattern: Optimistic Update

```javascript
// 1. Update UI immediately (optimistic)
const newItem = { id: Date.now(), text: input.value };
setItems([...items, newItem]);
clearInput();

// 2. Send to server
const response = await fetch('/api/items', {
  method: 'POST',
  body: JSON.stringify(newItem)
});

// 3. Handle failure - rollback
if (!response.ok) {
  setItems(items);  // Remove the optimistic item
  showError('Failed to save');
}
```

### Pattern: Optimistic Delete

```javascript
// 1. Remove from UI immediately
const updatedItems = items.filter(item => item.id !== id);
setItems(updatedItems);

// 2. Send delete request
const response = await fetch(`/api/items/${id}`, {
  method: 'DELETE'
});

// 3. Handle failure - restore
if (!response.ok) {
  setItems(items);  // Restore the item
  showError('Failed to delete');
}
```

### Pattern: Optimistic Like/Vote

```javascript
// 1. Update like count immediately
const newLikeCount = isLiked ? count - 1 : count + 1;
setLikeCount(newLikeCount);
setIsLiked(!isLiked);

// 2. Send to server
const response = await fetch(`/api/items/${id}/like`, {
  method: 'POST',
  body: JSON.stringify({ liked: !isLiked })
});

// 3. Handle failure - rollback
if (!response.ok) {
  setLikeCount(count);  // Restore original count
  setIsLiked(isLiked);  // Restore original state
  showError('Failed to update');
}
```

## Perceived Performance Strategies

### 1. Instant Feedback

Show that something happened immediately, even if the operation isn't complete.

```javascript
// Bad - Wait for server response
const handleSubmit = async () => {
  const response = await fetch('/api/submit', { body });
  showSuccess('Saved!');
};

// Good - Show feedback immediately
const handleSubmit = async () => {
  showSuccess('Saving...');  // Instant feedback
  const response = await fetch('/api/submit', { body });
  if (!response.ok) showError('Failed to save');
};
```

### 2. Progress Indication

Show progress for long operations. Even fake progress (that doesn't go to 100%) feels better than nothing.

```javascript
// Fake progress for unknown duration
const startFakeProgress = () => {
  let progress = 10;
  const interval = setInterval(() => {
    progress += Math.random() * 20;
    if (progress > 90) progress = 90;  // Never reach 100%
    setProgress(progress);
  }, 500);
  return interval;
};

// Real progress for known duration
const startRealProgress = (total) => {
  let completed = 0;
  const interval = setInterval(() => {
    completed++;
    setProgress((completed / total) * 100);
    if (completed === total) clearInterval(interval);
  }, 100);
  return interval;
};
```

### 3. Anticipatory Design

Preload content before the user asks for it.

```javascript
// Preload next page when user scrolls near bottom
const handleScroll = () => {
  if (isNearBottom()) {
    preloadNextPage();  // Load before user clicks
  }
};

// Preload hover targets
const handleMouseEnter = () => {
  preloadUserProfile(userId);  // Load on hover
};
```

### 4. Momentum Conservation

Respect the user's gesture velocity. If they swipe fast, the animation should feel fast.

```javascript
// Respect gesture velocity
const handleSwipe = (velocity) => {
  const distance = Math.abs(velocity) * 100;  // Distance based on velocity
  const duration = Math.max(300, distance / 500);  // Duration based on distance
  
  animate({
    from: currentPosition,
    to: currentPosition + distance,
    duration: duration,
    easing: 'ease-out'
  });
};
```

## Latency Masking Techniques

### 1. Skeleton Screens

Show a placeholder that matches the content structure.

```html
<!-- Skeleton that matches actual content -->
<div class="card-skeleton">
  <div class="skeleton skeleton-image" style="height: 200px;"></div>
  <div class="skeleton skeleton-text" style="width: 80%;"></div>
  <div class="skeleton skeleton-text" style="width: 60%;"></div>
  <div class="skeleton skeleton-text" style="width: 40%;"></div>
</div>
```

**Why it works:** The brain constructs a spatial map while waiting. When real content arrives, it feels like a natural transition, not a sudden appearance.

### 2. Blur-Up Technique

Load a low-quality image first, then replace with high-quality.

```html
<img 
  src="image-low-quality.jpg" 
  srcset="image-high-quality.jpg 1x"
  loading="lazy"
/>

<!-- Or with CSS -->
<div class="image-container">
  <img class="image-blur" src="image-low.jpg" />
  <img class="image-sharp" src="image-high.jpg" />
</div>
```

```css
.image-blur {
  filter: blur(20px);
  opacity: 1;
  transition: opacity 300ms;
}

.image-sharp {
  opacity: 0;
  transition: opacity 300ms;
}

.image-sharp.loaded {
  opacity: 1;
}
```

### 3. Progressive Enhancement

Show basic content immediately, enhance as data loads.

```html
<!-- Show immediately -->
<article class="post">
  <h1>Post Title</h1>
  <p>First paragraph (server-rendered)</p>
</article>

<!-- Load additional content -->
<div id="comments-container">
  <!-- Comments load via JavaScript -->
</div>
```

### 4. Staggered Animations

Animate elements in sequence to make loading feel faster.

```css
/* Stagger animations */
.list-item {
  animation: slideIn 300ms ease-out;
  animation-fill-mode: both;
}

.list-item:nth-child(1) { animation-delay: 0ms; }
.list-item:nth-child(2) { animation-delay: 50ms; }
.list-item:nth-child(3) { animation-delay: 100ms; }
.list-item:nth-child(4) { animation-delay: 150ms; }

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

**Why it works:** Staggered animations create the illusion of faster loading. Content appears to cascade in, which feels more natural than everything appearing at once.

## Network Optimization

### 1. Request Batching

Combine multiple requests into one.

```javascript
// Bad - 5 separate requests
await fetch('/api/user');
await fetch('/api/posts');
await fetch('/api/comments');
await fetch('/api/likes');
await fetch('/api/followers');

// Good - 1 batched request
const data = await fetch('/api/batch', {
  method: 'POST',
  body: JSON.stringify({
    requests: ['user', 'posts', 'comments', 'likes', 'followers']
  })
});
```

### 2. Request Deduplication

Prevent duplicate requests for the same data.

```javascript
const requestCache = new Map();

const fetchData = async (url) => {
  // Return cached promise if request is in flight
  if (requestCache.has(url)) {
    return requestCache.get(url);
  }

  const promise = fetch(url).then(r => r.json());
  requestCache.set(url, promise);

  try {
    return await promise;
  } finally {
    requestCache.delete(url);  // Clear after completion
  }
};
```

### 3. Connection Pooling

Reuse HTTP connections.

```javascript
// Use HTTP/2 or HTTP/3 (automatic in modern browsers)
// Or manually manage connection pool
const connectionPool = [];
const MAX_CONNECTIONS = 6;

const getConnection = () => {
  if (connectionPool.length < MAX_CONNECTIONS) {
    return new Connection();
  }
  return connectionPool.shift();
};
```

## Measuring Perceived Performance

### Core Web Vitals

1. **LCP (Largest Contentful Paint)** — When main content is visible
2. **FID (First Input Delay)** — Time to respond to user input
3. **CLS (Cumulative Layout Shift)** — Visual stability

```javascript
// Measure LCP
const observer = new PerformanceObserver((list) => {
  const entries = list.getEntries();
  const lastEntry = entries[entries.length - 1];
  console.log('LCP:', lastEntry.renderTime || lastEntry.loadTime);
});
observer.observe({ entryTypes: ['largest-contentful-paint'] });

// Measure FID
const fidObserver = new PerformanceObserver((list) => {
  list.getEntries().forEach((entry) => {
    console.log('FID:', entry.processingDuration);
  });
});
fidObserver.observe({ entryTypes: ['first-input'] });
```

## How to Use This Skill with Claude Code

### Optimize Perceived Performance

```
"I'm using the performance-optimization skill. Can you help me:
- Implement optimistic UI for my form
- Add skeleton screens for loading states
- Measure Core Web Vitals
- Identify perceived latency issues"
```

### Create Loading State Strategy

```
"Can you create a loading state strategy for my app?
- < 100ms: No feedback
- 100ms-1s: Subtle feedback
- 1s-10s: Skeleton screen
- > 10s: Progress bar"
```

### Implement Staggered Animations

```
"Can you add staggered animations to my list?
- Animate items in sequence
- 50ms delay between items
- Smooth slide-in effect
- Respect prefers-reduced-motion"
```

## Integration with Other Skills

- **loading-states** — Loading state design
- **interaction-physics** — Smooth animations
- **accessibility-excellence** — Respect motion preferences
- **component-architecture** — Optimistic components

## Key Principles

**1. Perceived > Actual**
How fast it feels matters more than how fast it is.

**2. Instant Feedback**
Show something happened immediately.

**3. Progress Indication**
Keep users informed during long operations.

**4. Anticipation**
Preload before the user asks.

**5. Momentum**
Respect user gesture velocity.

## Checklist: Is Your Performance Ready?

- [ ] Optimistic UI for mutations
- [ ] Skeleton screens for 1-10s loads
- [ ] Progress bars for >10s operations
- [ ] Instant feedback for all actions
- [ ] Staggered animations for lists
- [ ] Preloading for anticipated actions
- [ ] Request batching and deduplication
- [ ] LCP < 2.5s
- [ ] FID < 100ms
- [ ] CLS < 0.1

Optimized perceived performance transforms interfaces from sluggish to snappy.
