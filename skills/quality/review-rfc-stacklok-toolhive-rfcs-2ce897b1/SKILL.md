---
name: review-rfc
description: Review RFCs for the ToolHive ecosystem. Use when the user wants to review, critique, or provide feedback on an RFC for toolhive, toolhive-studio, toolhive-registry, toolhive-registry-server, toolhive-cloud-ui, or dockyard projects.
allowed-tools: Read, Glob, Grep, Bash(git:*), mcp__github__*, mcp__fetch__fetch, WebFetch, Task
---

# Review RFC Skill

This skill helps you thoroughly review RFCs for the ToolHive ecosystem, ensuring they meet quality standards, architectural alignment, and security requirements.

## Overview

When reviewing an RFC, you should evaluate it against multiple dimensions: completeness, technical accuracy, architectural alignment, security considerations, and feasibility.

## Review Workflow

### Step 1: Read the RFC

First, read the RFC document completely. If provided a PR number or file path, fetch and read it.

### Step 2: Fetch Architectural Context

Before reviewing, gather context from the ToolHive architecture documentation. Use `mcp__github__get_file_contents` to read relevant docs from `stacklok/toolhive` repo's `docs/arch/` directory:

| Document | When to Read |
|----------|--------------|
| `00-overview.md` | Always - understand platform concepts |
| `01-deployment-modes.md` | RFCs affecting deployment, K8s, or local mode |
| `02-core-concepts.md` | RFCs introducing new concepts or terminology |
| `03-transport-architecture.md` | RFCs affecting MCP transports or proxy |
| `04-secrets-management.md` | RFCs involving secrets or credentials |
| `05-runconfig-and-permissions.md` | RFCs affecting configuration or permissions |
| `06-registry-system.md` | RFCs affecting registry functionality |
| `07-groups.md` | RFCs involving server grouping |
| `08-workloads-lifecycle.md` | RFCs affecting workload management |
| `09-operator-architecture.md` | RFCs affecting K8s operator or CRDs |
| `10-virtual-mcp-architecture.md` | RFCs involving aggregation or virtual MCP |

### Step 3: Check Related Existing RFCs

Search this repository for related RFCs that might:
- Conflict with the proposal
- Be superseded by the proposal
- Provide context or dependencies

### Step 4: Verify Against Target Repository

Search the target repository to verify:
- Proposed changes align with existing code patterns
- No conflicts with recent changes
- API changes are compatible with existing interfaces

## Review Checklist

### A. Structure and Completeness

- [ ] **Metadata present**: Status, Author, Created, Last Updated, Target Repository
- [ ] **Summary**: Clear 2-3 sentence description
- [ ] **Problem Statement**: Clearly articulates the problem, who's affected, why it matters
- [ ] **Goals**: Specific, measurable objectives listed
- [ ] **Non-Goals**: Explicit scope boundaries defined
- [ ] **Proposed Solution**: Detailed design with diagrams where appropriate
- [ ] **Security Considerations**: All required subsections present (see below)
- [ ] **Alternatives Considered**: At least one alternative evaluated
- [ ] **Compatibility**: Backward and forward compatibility addressed
- [ ] **Implementation Plan**: Phased approach with concrete tasks
- [ ] **Testing Strategy**: Multiple test levels covered
- [ ] **Open Questions**: Unresolved items listed (if any)

### B. Security Review (CRITICAL)

The Security Considerations section MUST address all of these:

| Section | Questions to Verify |
|---------|---------------------|
| **Threat Model** | Are potential threats identified? Are attacker capabilities considered? |
| **Authentication** | How does this affect auth? Are new auth requirements clear? |
| **Authorization** | What permission checks are needed? Any new permission models? |
| **Data Security** | Is sensitive data identified? Is encryption addressed? |
| **Input Validation** | What user input is accepted? How is it validated? |
| **Secrets Management** | Are secrets handled properly? Can they be rotated? |
| **Audit and Logging** | Are security events logged? Compliance considered? |
| **Mitigations** | Are concrete mitigations proposed for identified threats? |

**Red flags to watch for:**
- Missing or superficial security section
- "N/A" without justification for security subsections
- No threat model for network-exposed features
- Secrets in configuration examples
- Missing input validation for user-provided data
- No audit logging for security-relevant operations

### C. Technical Accuracy

- [ ] **Correct terminology**: Uses ToolHive concepts correctly (Workloads, Transports, Middleware, etc.)
- [ ] **Architecture alignment**: Follows established patterns and principles
- [ ] **Code examples**: Syntactically correct, idiomatic for the language
- [ ] **API design**: Consistent with existing APIs in the target repo
- [ ] **CRD design**: Follows Kubernetes conventions if applicable
- [ ] **Configuration format**: Matches existing RunConfig patterns

### D. Diagrams and Examples

- [ ] **Mermaid diagrams**: Complex flows illustrated clearly
- [ ] **Code examples**: Concrete, not abstract placeholders
- [ ] **Configuration examples**: Realistic YAML/JSON examples
- [ ] **Sequence diagrams**: For multi-component interactions

### E. Feasibility and Impact

- [ ] **Implementation complexity**: Is the phased approach realistic?
- [ ] **Dependencies**: Are external dependencies identified?
- [ ] **Breaking changes**: Are migration paths provided if needed?
- [ ] **Performance impact**: Considered where relevant?
- [ ] **Cross-repo impact**: If `multiple` repos, are all impacts identified?

## ToolHive Ecosystem Context

### Target Repositories

| Repository | Type | Key Considerations |
|------------|------|-------------------|
| `toolhive` | Go | Core platform, CLI, operator, proxy, virtual MCP |
| `toolhive-studio` | TypeScript | Desktop UI, Electron app |
| `toolhive-registry-server` | Go | Registry API, MCP Registry spec compliance |
| `toolhive-registry` | Go/JSON | Registry data, server definitions |
| `toolhive-cloud-ui` | TypeScript/Next.js | Cloud UI, OIDC integration |
| `dockyard` | Go | Container packaging, security scanning |

### Key Architecture Principles to Verify

1. **Platform, not runner**: Does this enhance the platform abstraction?
2. **Security by default**: Does this maintain or improve security posture?
3. **Middleware composability**: Can this be implemented as middleware if appropriate?
4. **RunConfig portability**: Does this preserve configuration portability?
5. **Cloud-native**: Is this Kubernetes-friendly where applicable?

### CRD Types (for K8s-related RFCs)

- `MCPServer` - Individual MCP server deployment
- `MCPRegistry` - Registry configuration
- `MCPToolConfig` - Tool filtering and configuration
- `MCPExternalAuthConfig` - External authentication
- `MCPGroup` - Server grouping
- `VirtualMCPServer` - Aggregation of multiple servers

## Review Output Format

Structure your review as follows:

```markdown
## RFC Review: [RFC Title]

### Summary
[1-2 sentence summary of your overall assessment]

### Strengths
- [What the RFC does well]

### Areas for Improvement

#### Critical Issues (Must Fix)
- [Issues that must be addressed before acceptance]

#### Suggestions (Should Consider)
- [Improvements that would strengthen the RFC]

#### Minor/Nitpicks (Optional)
- [Small improvements or style suggestions]

### Security Assessment
[Specific feedback on the security section]

### Architectural Alignment
[How well does this align with ToolHive architecture?]

### Questions for the Author
- [Clarifying questions that need answers]

### Recommendation
[ ] Ready to accept
[ ] Accept with minor changes
[ ] Needs revision (address critical issues)
[ ] Major rework needed
```

## Common Issues to Watch For

### Problem Statement Issues
- Too vague or abstract
- Doesn't explain who benefits
- Problem already solved elsewhere

### Design Issues
- Over-engineered for the problem
- Missing error handling considerations
- Doesn't consider edge cases
- Breaks existing functionality without migration path

### Security Issues
- Missing threat model
- Hardcoded credentials in examples
- No input validation
- Missing audit logging
- Overly permissive defaults

### Implementation Issues
- Unrealistic phasing
- Missing dependencies
- No rollback plan
- Insufficient testing strategy

## Reference Files

- Template: `rfcs/0000-template.md`
- Contributing guide: `CONTRIBUTING.md`
- Existing RFCs: `rfcs/THV-*.md`
