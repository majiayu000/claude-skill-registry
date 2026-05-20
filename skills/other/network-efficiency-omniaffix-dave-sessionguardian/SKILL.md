---
name: network-efficiency
description: Batch API requests when possible Use when optimizing code performance. Performance category skill.
metadata:
  category: Performance
  priority: medium
  is-built-in: true
  session-guardian-id: builtin_network_efficiency
---

# Network Efficiency

Batch API requests when possible. Use compression for large payloads. Implement pagination instead of fetching all data at once. Consider GraphQL or sparse fieldsets to fetch only needed data. Use appropriate HTTP caching headers. For real-time data, consider WebSockets over polling. Optimize asset delivery with CDNs and appropriate cache headers.