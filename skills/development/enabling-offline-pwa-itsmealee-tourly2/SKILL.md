---
name: enabling-offline-pwa
description: Implements PWA features and service workers for offline access. Use to cache itineraries and critical travel info for users on the go.
---

# Offline Capabilities (PWA)

## When to use this skill
- When users need access to their "My Bookings" or "Itinerary" without a signal.
- To improve load times via aggressive caching.

## Workflow
- [ ] Configure `next-pwa` or a manual service worker (`sw.js`).
- [ ] Define the `manifest.json` for "Add to Home Screen" support.
- [ ] Cache Appwrite API responses for routes like `/my-trips`.

## Strategy (Service Worker)
- **Stale-While-Revalidate**: Show the cached data immediately, then update it in the background.
- **Cache-First**: Use for static assets (icons, fonts, localized tour descriptions).

## Instructions
- **Safety**: Ensure the service worker doesn't cache auth tokens or sensitive personal data indefinitely.
- **Feedback**: Show an "Offline Mode" banner when the user loses connection.
