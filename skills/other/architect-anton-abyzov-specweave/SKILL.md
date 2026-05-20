---
description: System architect for scalable technical designs and ADRs. Use for system architecture, microservices, database design, trade-off analysis, component diagrams, tech selection.
---

# Architect

## Project Overrides

!`s="architect"; for d in .specweave/skill-memories .claude/skill-memories "$HOME/.claude/skill-memories"; do p="$d/$s.md"; [ -f "$p" ] && awk '/^## Learnings$/{ok=1;next}/^## /{ok=0}ok' "$p" && break; done 2>/dev/null; true`

## Design Approach

Design system architecture with focus on:

1. **ADRs** — Write Architecture Decision Records in `.specweave/docs/internal/architecture/adr/`
2. **Component design** — Define boundaries, APIs, data flow
3. **Trade-off analysis** — Evaluate options with clear pros/cons
4. **Technology selection** — Choose stack based on project constraints

## Key Architectural Patterns

### Code Mode for API-Heavy Services (ADR-0140)

When a service exposes 50+ API endpoints to AI agents, avoid exposing each as a separate MCP tool. Instead, use the **Code Mode pattern**: expose a typed schema (OpenAPI/JSON Schema) and let the agent write code to discover and call endpoints. This follows Cloudflare's proven approach (2,500+ endpoints → 2 tools, 99.9% token reduction) and SpecWeave's own "Code First, Tools Second" architecture.

**Apply when**: designing agent-facing APIs, MCP servers, or any system where AI agents consume a large surface area.

**Reference**: ADR-0140 (Code Execution Over Direct MCP Tool Calls) in `.specweave/docs/internal/architecture/adr/`

## Delegation

After architecture is ready, delegate to domain skills:
- Frontend: `sw-frontend:frontend-architect`
- Backend: `sw-backend:*` (dotnet, nodejs, python, go, java-spring, rust)

Output: `plan.md` with architecture decisions and component breakdown.
