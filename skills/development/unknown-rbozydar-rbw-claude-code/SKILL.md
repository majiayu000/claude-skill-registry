---
name: agent-native-architecture
description: This skill should be used when building AI agents using prompt-native architecture where features are defined in prompts, not code. It covers creating autonomous agents, designing MCP servers, implementing self-modifying systems, and adopting the "trust the agent's intelligence" philosophy.
---

<essential_principles>

## The Prompt-Native Philosophy

Agent native engineering inverts traditional software architecture. Instead of writing code that the agent executes, define outcomes in prompts and let the agent figure out HOW to achieve them.

### The Foundational Principle

**Whatever the user can do, the agent can do.**

Avoid artificially limiting the agent. If a user can read files, write code, browse the web, deploy an app -- the agent should be able to do those things too.

### Features Are Prompts

Each feature is a prompt that defines an outcome and gives the agent the tools it needs.

**Traditional:** Feature = function in codebase that agent calls
**Prompt-native:** Feature = prompt defining desired outcome + primitive tools

### Tools Provide Capability, Not Behavior

Tools should be primitives that enable capability. The prompt defines what to do with that capability.

**Wrong:** `generate_dashboard(data, layout, filters)` -- agent executes a predefined workflow
**Right:** `read_file`, `write_file`, `list_files` -- agent figures out how to build a dashboard

### The Development Lifecycle

1. **Start in the prompt** -- new features begin as natural language defining outcomes
2. **Iterate rapidly** -- change behavior by editing prose, not refactoring code
3. **Graduate when stable** -- harden to code when requirements stabilize AND speed/reliability matter
4. **Many features stay as prompts** -- not everything needs to become code

### When NOT to Use This Approach

- High-frequency operations (thousands of calls per second)
- Deterministic requirements (exact same output every time)
- Cost-sensitive scenarios (when API costs would be prohibitive)

</essential_principles>

<intake>

What aspect of agent native architecture is needed?

1. **Design architecture** -- plan a new prompt-native agent system
2. **Create MCP tools** -- build primitive tools following the philosophy
3. **Write system prompts** -- define agent behavior in prompts
4. **Self-modification** -- enable agents to safely evolve themselves
5. **Review/refactor** -- make existing code more prompt-native
6. **Context injection** -- inject runtime app state into agent prompts
7. **Action parity** -- ensure agents can do everything users can do
8. **Shared workspace** -- set up agents and users in the same data space
9. **Testing** -- test agent-native apps for capability and parity
10. **Mobile patterns** -- handle background execution, permissions, cost

Wait for response before proceeding.

</intake>

<routing>

| Response | Action |
|----------|--------|
| 1, "design", "architecture" | Read [architecture-patterns.md](./references/architecture-patterns.md), apply Architecture Checklist |
| 2, "tool", "mcp", "primitive" | Read [mcp-tool-design.md](./references/mcp-tool-design.md) |
| 3, "prompt", "system prompt" | Read [system-prompt-design.md](./references/system-prompt-design.md) |
| 4, "self-modify", "evolve" | Read [self-modification.md](./references/self-modification.md) |
| 5, "review", "refactor" | Read [refactoring-to-prompt-native.md](./references/refactoring-to-prompt-native.md) |
| 6, "context", "inject" | Read [dynamic-context-injection.md](./references/dynamic-context-injection.md) |
| 7, "parity", "capability" | Read [action-parity-discipline.md](./references/action-parity-discipline.md) |
| 8, "workspace", "shared" | Read [shared-workspace-architecture.md](./references/shared-workspace-architecture.md) |
| 9, "test", "testing" | Read [agent-native-testing.md](./references/agent-native-testing.md) |
| 10, "mobile", "ios" | Read [mobile-patterns.md](./references/mobile-patterns.md) |

After reading the reference, apply those patterns to the specific context.

</routing>

<architecture_checklist>

## Architecture Review Checklist

When designing an agent-native system, verify before implementation:

### Tool Design
- [ ] External APIs with full agent access use Dynamic Capability Discovery
- [ ] Every entity has full CRUD tools
- [ ] Tools are primitives, not workflows
- [ ] API validates inputs (use `z.string()` not `z.enum()` when API validates)

### Action Parity
- [ ] Every UI action has a corresponding agent tool
- [ ] Edit and delete operations are available, not just create/read
- [ ] The "write something to [app location]" test passes for all locations

### UI Integration
- [ ] Agent changes reflect in UI immediately (shared service, file watching, or event bus)
- [ ] Users can discover what the agent can do (onboarding, capability hints)

### Context Injection
- [ ] System prompt includes available resources and capabilities
- [ ] Context refreshes for long sessions (or `refresh_context` tool exists)

### Mobile (if applicable)
- [ ] Background execution uses checkpoint/resume pattern
- [ ] Just-in-time permission requests in tools
- [ ] Cost-aware model tier selection

</architecture_checklist>

<anti_patterns>

## Common Anti-Patterns

| Anti-Pattern | Problem | Fix | Reference |
|---|---|---|---|
| **Cardinal Sin** | Agent executes predefined workflow code instead of figuring things out | Define outcomes in prompts, provide primitive tools | architecture-patterns.md |
| **Context Starvation** | Agent doesn't know what resources exist | Inject available resources into system prompt at runtime | [dynamic-context-injection.md](./references/dynamic-context-injection.md) |
| **Orphan Features** | UI action with no agent equivalent | Add tool + document in system prompt for every UI action | [action-parity-discipline.md](./references/action-parity-discipline.md) |
| **Sandbox Isolation** | Agent works in separate data space from user | Use shared workspace | [shared-workspace-architecture.md](./references/shared-workspace-architecture.md) |
| **Silent Actions** | Agent changes state but UI doesn't update | Use shared data stores with reactive binding | [architecture-patterns.md](./references/architecture-patterns.md) |
| **Capability Hiding** | Users can't discover what agents can do | Include capability hints, provide onboarding | [action-parity-discipline.md](./references/action-parity-discipline.md) |
| **Static Tool Mapping** | Individual tools for each API endpoint | Use Dynamic Capability Discovery (`list_*` + generic access tool) | [mcp-tool-design.md](./references/mcp-tool-design.md) |
| **Incomplete CRUD** | Agent can create but not update/delete | Every entity needs all four CRUD operations | [mcp-tool-design.md](./references/mcp-tool-design.md) |

See the referenced files for detailed examples and solutions.

</anti_patterns>

<reference_index>

## References

All in `references/`:

**Core Patterns:**
- [architecture-patterns.md](./references/architecture-patterns.md) -- system architecture
- [mcp-tool-design.md](./references/mcp-tool-design.md) -- Dynamic Capability Discovery, CRUD Completeness
- [system-prompt-design.md](./references/system-prompt-design.md) -- prompt structure
- [self-modification.md](./references/self-modification.md) -- safe self-evolution
- [refactoring-to-prompt-native.md](./references/refactoring-to-prompt-native.md) -- migration guide

**Agent-Native Disciplines:**
- [dynamic-context-injection.md](./references/dynamic-context-injection.md)
- [action-parity-discipline.md](./references/action-parity-discipline.md)
- [shared-workspace-architecture.md](./references/shared-workspace-architecture.md)
- [agent-native-testing.md](./references/agent-native-testing.md)
- [mobile-patterns.md](./references/mobile-patterns.md)

</reference_index>

<success_criteria>

## Success Criteria

A prompt-native agent is complete when:

- [ ] The agent figures out HOW to achieve outcomes, not just calls predefined functions
- [ ] Features are prompts defining outcomes, not code defining workflows
- [ ] Tools are primitives enabling capability, not encoding logic
- [ ] Changing behavior means editing prose, not refactoring code
- [ ] Every UI action has a corresponding agent tool (action parity)
- [ ] Agent and user operate in the same data space (shared workspace)
- [ ] System prompt includes dynamic context about app state

</success_criteria>
