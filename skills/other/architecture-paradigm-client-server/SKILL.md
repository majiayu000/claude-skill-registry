---
name: architecture-paradigm-client-server
description: Applies client-server architecture for web/mobile apps. Use when designing systems with centralized backend services, trust boundaries, or offline-first sync.
alwaysApply: false
category: architectural-pattern
tags:
- architecture
- client-server
- peer-to-peer
- distributed-systems
dependencies: []
tools: []
usage_patterns:
- paradigm-implementation
- distributed-system-design
- offline-first
complexity: low
model_hint: fast
estimated_tokens: 600
---
# The Client-Server and Peer-to-Peer Paradigms

## When to Employ This Paradigm
- For traditional applications that have centralized services, such as web or mobile clients communicating with backend APIs.
- For systems exploring decentralized or "offline-first" capabilities that rely on peer-to-peer synchronization.
- To formally document trust boundaries, client-server version negotiation, and API evolution strategies.

## Adoption Steps
1. **Define Responsibilities**: Clearly delineate which logic and data reside on the client versus the server, with the goal of minimizing duplication.
2. **Document the Contracts**: Formally document all APIs, data schemas, authentication flows, and any capability negotiation required for handling different client versions.
3. **Plan for Version Skew**: Implement a strategy to manage different client and server versions, such as using feature flags, `Accept` headers for content negotiation, or semantic versioning for APIs.
4. **Address Connectivity Issues**: If the application is not purely client-server, design for intermittent connectivity. This may involve implementing offline caching, data synchronization protocols, or peer discovery and membership services.
5. **Secure All Communications**: Enforce the use of TLS for all data in transit. Implement authorization policies, rate limiting, and detailed telemetry for every endpoint.

## Key Deliverables
- An Architecture Decision Record (ADR) that covers the roles of clients, servers, and peers, defines the trust boundaries, and outlines deployment assumptions.
- Formal API or protocol specifications, along with a suite of compatibility tests.
- Runbooks detailing the coordination required for rollouts, such as client release waves, backward-compatibility support, or operational procedures for a peer-to-peer network.

## Risks & Mitigations
- **"Chatty" Clients**:
  - **Mitigation**: A client making too many small requests can lead to poor performance. Consolidate API calls using patterns like the Façade or Gateway, and implement caching strategies on the client or at the network edge.
- **"Thick" Clients with Duplicated Logic**:
  - **Mitigation**: When clients contain too much business logic, it often becomes duplicated and out-of-sync with the server. Share validation logic by packaging it in a common library or move the rules definitively to the server.
- **Peer-to-Peer Data Conflicts**:
  - **Mitigation**: In a peer-to-peer model, data conflicts are inevitable. Design formal conflict resolution strategies (e.g., CRDTs, last-write-wins) and consensus mechanisms from the beginning.

## Concrete Components

These vocabulary items name the concrete tools and abstractions
that show up when the paradigm is implemented. They are not
required dependencies and they are not part of the skill's
``tools:`` frontmatter (which is reserved for Claude Code tool
restrictions). Use this list to disambiguate during architecture
discussions.

- ``api-contract-generator`` -- produces machine-readable OpenAPI/RPC contracts the client and server share
- ``networking-debugger`` -- captures request/response traces for diagnosing latency, retries, and timeout issues
