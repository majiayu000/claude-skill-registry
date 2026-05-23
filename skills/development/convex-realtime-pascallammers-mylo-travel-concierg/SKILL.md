---
name: convex-realtime
description: Implement real-time features using Convex reactive queries that automatically update when data changes, enabling live collaboration, instant updates, and reactive UIs without manual polling. Use when building live dashboards, implementing collaborative editing, creating chat applications, showing real-time notifications, building activity feeds, implementing presence indicators, creating reactive search, or any feature requiring instant data synchronization across clients.
---

# Convex Realtime - Live Data Subscriptions

## When to use this skill

- Building live dashboards that update instantly
- Implementing collaborative editing features
- Creating real-time chat applications
- Showing instant notifications to users
- Building activity feeds that update live
- Implementing user presence indicators
- Creating reactive search with live results
- Building multiplayer or collaborative features
- Showing real-time analytics and metrics
- Implementing live document collaboration
- Creating real-time forms with validation
- Building features requiring instant synchronization

## When to use this skill

- Building realtime features, live updates, collaborative apps.
- When working on related tasks or features
- During development that requires this expertise

**Use when**: Building realtime features, live updates, collaborative apps.

## Auto-Updating Queries
\`\`\`typescript
const messages = useQuery(api.messages.list, { channelId });
// Automatically updates when data changes!
\`\`\`

## Resources
- [Convex Reactivity](https://docs.convex.dev/using/reactivity)
