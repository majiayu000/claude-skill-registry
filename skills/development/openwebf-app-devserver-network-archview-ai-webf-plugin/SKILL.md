---
name: openwebf-app-devserver-network
description: 'Troubleshoot dev server reachability and HMR for WebF apps on real devices
  (Vite/Webpack): LAN IP vs localhost, 0.0.0.0/--host binding, firewall/ports, and
  websocket/HMR (ws://) issues. Use when the u'
---

---
name: openwebf-app-devserver-network
description: Troubleshoot dev server reachability and HMR for WebF apps on real devices (Vite/Webpack): LAN IP vs localhost, 0.0.0.0/--host binding, firewall/ports, and websocket/HMR (ws://) issues. Use when the user mentions HMR, websocket, ws://, --host, 0.0.0.0, LAN IP, firewall, or a device that can load HTML but not assets/HMR.
allowed-tools: Read, Grep, Glob, Bash, Edit, Write, mcp__openwebf__docs_search, mcp__openwebf__docs_get_section, mcp__openwebf__docs_related
---

# OpenWebF App: Dev Server & Network Troubleshooting

## Instructions

1. Collect the minimum facts: platform (desktop/iOS/Android), dev server URL, framework (Vite/Webpack), and exact error/symptom.
2. Prioritize network reachability before app-level debugging:
   - LAN IP vs `localhost`
   - binding to interfaces (e.g. `--host`)
   - firewall/port rules
3. If hot reload (HMR) is the issue, confirm the dev server is configured for network access and HMR websocket is reachable.
4. Use MCP docs for authoritative steps and known pitfalls; keep changes minimal.

More:
- [reference.md](reference.md)
- [doc-queries.md](doc-queries.md)
- [examples.md](examples.md)
