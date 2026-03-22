---
name: segment
description: >-
  Collect and route customer data with Segment — customer data platform (CDP)
  that sends events to any destination. Use when someone asks to "track user
  events across tools", "Segment", "customer data platform", "send events to
  multiple analytics tools", "CDP", or "unify analytics across Mixpanel/
  Amplitude/BigQuery". Covers identify, track, page, group, and destination
  routing.
license: Apache-2.0
compatibility: "JavaScript, Node.js, Python, iOS, Android. 400+ integrations."
metadata:
  author: terminal-skills
  version: "1.0.0"
  category: data-ai
  tags: ["analytics", "segment", "cdp", "events", "tracking"]
---

# Segment

## Overview

Segment is a customer data platform — collect events once, route them to every tool in your stack. Instead of adding SDKs for Mixpanel, Amplitude, Google Analytics, Intercom, and BigQuery separately (each with their own tracking code), send events to Segment and it forwards them to all destinations. One API, one event schema, 400+ integrations. Toggle destinations on/off without code changes.

## When to Use

- Sending analytics events to multiple tools (Mixpanel + BigQuery + Intercom)
- Don't want to add/remove tracking SDKs when switching tools
- Need a single source of truth for customer events
- Unifying web + mobile + server-side event tracking
- Building a data warehouse pipeline (events → BigQuery/Snowflake)

## Instructions

### Setup

```bash
# Browser (Analytics.js)
# Add to your site:
```

```html
<script>
  !function(){var analytics=window.analytics=window.analytics||[];if(!analytics.initialize)if(analytics.invoked)window.console&&console.error&&console.error("Segment snippet included twice.");else{analytics.invoked=!0;analytics.methods=["trackSubmit","trackClick","trackLink","trackForm","pageview","identify","reset","group","track","ready","alias","debug","page","screen","once","off","on","addSourceMiddleware","addIntegrationMiddleware","setAnonymousId","addDestinationMiddleware","register"];analytics.factory=function(e){return function(){if(window.analytics.initialized)return window.analytics[e].apply(window.analytics,arguments);var i=Array.prototype.slice.call(arguments);if(["track","screen","alias","group","page","identify"].indexOf(e)>-1){var c=document.querySelector("link[rel='canonical']");i.push({__t:"bpc",c:c&&c.getAttribute("href")||void 0,p:location.pathname,u:location.href,s:location.search,t:document.title,r:document.referrer})}i.unshift(e);analytics.push(i);return analytics}};for(var i=0;i<analytics.methods.length;i++){var key=analytics.methods[i];analytics[key]=analytics.factory(key)}analytics.load=function(key,i){var t=document.createElement("script");t.type="text/javascript";t.async=!0;t.setAttribute("data-global-segment-analytics-key","analytics");t.src="https://cdn.segment.com/analytics.js/v1/" + key + "/analytics.min.js";var n=document.getElementsByTagName("script")[0];n.parentNode.insertBefore(t,n);analytics._loadOptions=i};analytics._writeKey="YOUR_WRITE_KEY";analytics.SNIPPET_VERSION="5.2.1";analytics.load("YOUR_WRITE_KEY");analytics.page();}}();
</script>
```

```bash
# Node.js
npm install @segment/analytics-node
```

### Core API Calls

```typescript
// tracking.ts — The 5 Segment API calls
import { Analytics } from "@segment/analytics-node";

const analytics = new Analytics({ writeKey: process.env.SEGMENT_WRITE_KEY! });

// 1. IDENTIFY — Who is the user?
analytics.identify({
  userId: "user_123",
  traits: {
    email: "kai@example.com",
    name: "Kai",
    plan: "pro",
    company: "Acme",
    createdAt: "2026-01-15T00:00:00Z",
  },
});

// 2. TRACK — What did they do?
analytics.track({
  userId: "user_123",
  event: "Order Completed",
  properties: {
    orderId: "ord_456",
    total: 99.99,
    currency: "USD",
    products: [
      { id: "prod_1", name: "Widget", price: 49.99, quantity: 2 },
    ],
  },
});

// 3. PAGE — What page are they on? (browser-side)
analytics.page({
  userId: "user_123",
  name: "Pricing",
  properties: { url: "https://myapp.com/pricing", referrer: "https://google.com" },
});

// 4. GROUP — What company/team are they part of?
analytics.group({
  userId: "user_123",
  groupId: "company_789",
  traits: { name: "Acme Corp", industry: "Technology", employees: 50, plan: "enterprise" },
});

// 5. ALIAS — Link anonymous to known user (on signup)
analytics.alias({ userId: "user_123", previousId: "anon_abc" });
```

### React Integration

```tsx
// hooks/useTracking.ts — React hook for Segment tracking
export function useTracking() {
  const track = (event: string, properties?: Record<string, any>) => {
    window.analytics?.track(event, properties);
  };

  const identify = (userId: string, traits?: Record<string, any>) => {
    window.analytics?.identify(userId, traits);
  };

  const page = (name?: string, properties?: Record<string, any>) => {
    window.analytics?.page(name, properties);
  };

  return { track, identify, page };
}

// Usage
function PricingPage() {
  const { track, page } = useTracking();

  useEffect(() => { page("Pricing"); }, []);

  return (
    <button onClick={() => track("Plan Selected", { plan: "pro", price: 49 })}>
      Choose Pro
    </button>
  );
}
```

## Examples

### Example 1: Set up tracking for a SaaS product

**User prompt:** "Track user signups, feature usage, and purchases — send to Mixpanel, BigQuery, and Intercom."

The agent will set up Segment with identify on signup, track events for key actions, and configure destinations in the Segment dashboard.

### Example 2: Migrate from multiple tracking SDKs

**User prompt:** "We have separate Mixpanel, Amplitude, and GA4 SDKs. Consolidate into one."

The agent will replace individual SDKs with Segment's single tracking code, map existing events to Segment's schema, and enable destinations.

## Guidelines

- **Identify first, then track** — always identify users before tracking events
- **Event naming convention** — "Object Action" format: "Order Completed", "Page Viewed"
- **Traits for user properties** — email, plan, company go in identify traits
- **Properties for event data** — order total, product ID go in track properties
- **Server-side for sensitive events** — payments, subscriptions tracked from backend
- **Client-side for UI events** — clicks, page views, form interactions
- **Destinations via dashboard** — toggle integrations without code changes
- **Tracking plan** — document events before implementing; prevents data sprawl
- **Anonymous → identified** — use alias() when anonymous user signs up
- **Free tier: 1,000 visitors/month** — or self-host with Segment's open-source alternatives
