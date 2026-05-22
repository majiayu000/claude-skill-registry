---
name: write-rfc
description: Write RFCs for the ToolHive ecosystem. Use when the user wants to create a new RFC, proposal, or design document for toolhive, toolhive-studio, toolhive-registry, toolhive-registry-server, toolhive-cloud-ui, or dockyard projects.
allowed-tools: Read, Glob, Grep, Bash(git:*), mcp__github__*, mcp__fetch__fetch, WebFetch, Task, Edit, Write, AskUserQuestion
---

# Write RFC Skill

This skill helps you write high-quality RFCs for the ToolHive ecosystem following established patterns and conventions.

## Overview

ToolHive RFCs follow a specific format with the naming convention `THV-{NUMBER}-{descriptive-name}.md`. The NUMBER must match the PR number and be zero-padded to 4 digits.

## Workflow

### Step 1: Gather Requirements

Before writing an RFC, ask the user about:

1. **Problem Statement**: What problem are they trying to solve?
2. **Target Repository**: Which repo does this affect?
   - `toolhive` - Core runtime, CLI (`thv`), operator (`thv-operator`), proxy-runner (`thv-proxyrunner`), virtual MCP (`vmcp`)
   - `toolhive-studio` - Desktop UI application (Electron/TypeScript)
   - `toolhive-registry` - MCP server registry data
   - `toolhive-registry-server` - Registry API server (`thv-registry-api`)
   - `toolhive-cloud-ui` - Cloud/Enterprise web UI (Next.js)
   - `dockyard` - Container packaging for MCP servers
   - `multiple` - Cross-cutting changes
3. **Scope**: What are the goals and explicit non-goals?

### Step 2: Research the Ecosystem

Before drafting, research the relevant codebase:

#### 2.1 Fetch Architectural Documentation

Use `mcp__github__get_file_contents` to read from `stacklok/toolhive` repo's `docs/arch/` directory:

| Document | Content |
|----------|---------|
| `00-overview.md` | Platform overview, key components |
| `01-deployment-modes.md` | Local vs Kubernetes modes |
| `02-core-concepts.md` | Nouns (Workloads, Transports, Proxy, etc.) and Verbs |
| `03-transport-architecture.md` | stdio, SSE, streamable-http transports |
| `04-secrets-management.md` | Secrets handling, providers |
| `05-runconfig-and-permissions.md` | Configuration format, permission profiles |
| `06-registry-system.md` | Registry architecture, MCPRegistry CRD |
| `07-groups.md` | Server grouping concepts |
| `08-workloads-lifecycle.md` | Lifecycle management |
| `09-operator-architecture.md` | K8s operator, CRDs |
| `10-virtual-mcp-architecture.md` | Virtual MCP aggregation |

#### 2.2 Review Existing RFCs

Read `rfcs/` directory in this repository to understand patterns and check for related proposals.

#### 2.3 Search Relevant Codebases

Use `mcp__github__search_code` or `mcp__github__get_file_contents` to explore:

| Repository | Purpose |
|------------|---------|
| `stacklok/toolhive` | Core platform, CLI, operator, proxy |
| `stacklok/toolhive-studio` | Desktop UI |
| `stacklok/toolhive-registry-server` | Registry API server |
| `stacklok/toolhive-registry` | Registry data |
| `stacklok/toolhive-cloud-ui` | Cloud/Enterprise UI |
| `stacklok/dockyard` | Container packaging |

### Step 3: Draft the RFC

Create the RFC following the template structure from `rfcs/0000-template.md`.

#### Required Metadata

```markdown
# RFC-XXXX: Title

- **Status**: Draft
- **Author(s)**: Name (@github-handle)
- **Created**: YYYY-MM-DD
- **Last Updated**: YYYY-MM-DD
- **Target Repository**: [from step 1]
- **Related Issues**: [links if applicable]
```

#### Core Sections

1. **Summary** - 2-3 sentences capturing the essence
2. **Problem Statement** - Current limitation, who's affected, why it matters
3. **Goals** - Specific objectives (bulleted)
4. **Non-Goals** - Explicit scope boundaries
5. **Proposed Solution**
   - High-Level Design (with Mermaid diagrams)
   - Detailed Design: Component changes, API changes, configuration changes, data model changes
6. **Security Considerations** (REQUIRED) - See security checklist below
7. **Alternatives Considered** - Other approaches evaluated
8. **Compatibility** - Backward and forward compatibility
9. **Implementation Plan** - Phased approach with tasks
10. **Testing Strategy** - Unit, integration, E2E, performance, security tests
11. **Documentation** - What needs documenting
12. **Open Questions** - Unresolved items
13. **References** - Related links

#### Security Considerations Checklist (REQUIRED)

Every RFC MUST address:

- [ ] **Threat Model** - Potential threats, attacker capabilities
- [ ] **Authentication and Authorization** - Auth changes, permission models
- [ ] **Data Security** - Sensitive data handling, encryption
- [ ] **Input Validation** - User input, injection vectors
- [ ] **Secrets Management** - Credentials storage, rotation
- [ ] **Audit and Logging** - Security events, compliance
- [ ] **Mitigations** - Security controls implemented

### Step 4: Use Proper Conventions

#### Code Examples

- Use **Go** for API changes in toolhive, toolhive-registry-server
- Use **TypeScript** for toolhive-studio, toolhive-cloud-ui changes
- Use **YAML** for configuration examples
- Use **Mermaid** for diagrams (flowcharts, sequence diagrams)

#### Kubernetes CRDs

If the RFC involves Kubernetes, include CRD examples:

```yaml
apiVersion: toolhive.stacklok.dev/v1alpha1
kind: MCPServer
metadata:
  name: example
spec:
  # ...
```

CRD types: `MCPServer`, `MCPRegistry`, `MCPToolConfig`, `MCPExternalAuthConfig`, `MCPGroup`, `VirtualMCPServer`

### Step 5: File Naming

The RFC file should be named `THV-XXXX-{descriptive-name}.md` where XXXX is the PR number. Since you don't know the PR number yet, use a placeholder like `THV-XXXX-{name}.md` and remind the user to rename it to match the PR number after creating the PR.

### Step 6: Review Checklist

Before finalizing, verify:

- [ ] Problem is clearly stated
- [ ] Goals and non-goals are explicit
- [ ] Security section is complete (all 7 areas addressed)
- [ ] Alternatives are discussed
- [ ] Diagrams illustrate complex flows
- [ ] Code examples are concrete and in the correct language
- [ ] Implementation phases are defined
- [ ] Testing strategy covers all levels
- [ ] File follows naming convention

## ToolHive Architecture Summary

### Platform Overview

ToolHive is a **platform** for MCP server management (not just a container runner):

- **Proxy layer** with middleware (auth, authz, audit, rate limiting)
- **Security** by default (network isolation, permission profiles)
- **Aggregation** via Virtual MCP Server
- **Registry** for curated MCP servers
- **Multi-deployment**: Local (CLI/UI) and Kubernetes (operator)

### Key Binaries

| Binary | Location | Purpose |
|--------|----------|---------|
| `thv` | toolhive | Main CLI |
| `thv-operator` | toolhive | Kubernetes operator |
| `thv-proxyrunner` | toolhive | K8s proxy container |
| `vmcp` | toolhive | Virtual MCP server (aggregation) |
| `thv-registry-api` | toolhive-registry-server | Registry API server |

### Transport Types

- **stdio** - Standard input/output (requires protocol translation)
- **SSE** - Server-Sent Events (HTTP, transparent proxy)
- **streamable-http** - HTTP streaming (transparent proxy)

### Design Principles

1. Platform abstraction over direct execution
2. Security by default (network isolation, permissions)
3. Extensibility through middleware
4. Cloud-native (K8s operators, containers)
5. RunConfig as portable API contract

## Reference Files

- Template: `rfcs/0000-template.md`
- Contributing guide: `CONTRIBUTING.md`
- Existing RFCs: `rfcs/THV-*.md`
