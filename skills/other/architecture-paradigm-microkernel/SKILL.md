---
name: architecture-paradigm-microkernel
description: Applies microkernel architecture with minimal core and plugin extensibility. Use when building platforms where third parties extend core functionality.
alwaysApply: false
category: architectural-pattern
tags:
- architecture
- microkernel
- plugin
- extensibility
- platform-design
dependencies: []
tools: []
usage_patterns:
- paradigm-implementation
- platform-development
- extensibility-design
complexity: high
model_hint: deep
estimated_tokens: 900
---
# The Microkernel (Plugin) Architecture Paradigm


## When To Use

- Building extensible systems with plugin architectures
- Products requiring customer-specific customizations

## When NOT To Use

- Monolithic applications without plugin extensibility needs
- Systems where all features are core and tightly coupled by design

## When to Employ This Paradigm
- When building platforms, Integrated Development Environments (IDEs), data ingestion pipelines, or marketplaces where third parties need to extend core functionality.
- When the core system requires extreme stability, while extensions and features must evolve and change rapidly.
- When isolating optional dependencies and sandboxing untrusted code provided by plugins is critical.

## Adoption Steps
1. **Define Core Services**: Clearly delineate the minimal responsibilities of the microkernel, such as scheduling, component lifecycle management, core domain primitives, and messaging.
2. **Specify the Plugin Contract**: Design and document the formal contract for all plugins, including registration procedures, capability descriptors, lifecycle hooks (e.g., start, stop), and the permission model.
3. **Build the Extension Loader and Sandbox**: Implement the mechanisms for loading extensions, performing version compatibility checks, negotiating capabilities, and isolating plugins to prevent failures from cascading.
4. **Provide a Software Development Kit (SDK)**: To facilitate plugin development, provide an SDK with project templates, testing harnesses, and compatibility-checking tools.
5. **Govern the Release Process**: Maintain a clear compatibility matrix between core and plugin versions. Implement an automated regression test suite that validates core functionality against a variety of plugins.

## Key Deliverables
- An Architecture Decision Record (ADR) describing the division of responsibilities between the core and plugins, along with the governance model for plugin development and certification.
- Formal documentation for the security and permission model, detailing what capabilities are available to plugins.
- An automated plugin validation pipeline that performs linting, runs tests, and executes the plugin within a sandbox environment.

## Risks & Mitigations
- **Uncontrolled Plugin Proliferation**:
  - **Mitigation**: Without a curation process, the maintenance cost of supporting numerous plugins can become unsustainable. Enforce a formal certification process or a marketplace-style review for all third-party plugins.
- **Version Skew Between Core and Plugins**:
  - **Mitigation**: Use semantic versioning (SemVer) rigorously for both the core and the plugins. Where necessary, provide abstraction layers or "shims" to maintain backward compatibility with older plugins.
- **Core System Bloat**:
  - **Mitigation**: There is often pressure to add feature logic to the stable core. Aggressively resist this temptation. The core should remain minimal, with new features implemented as plugins whenever possible.

## Concrete Components

These vocabulary items name the concrete tools and abstractions
that show up when the paradigm is implemented. They are not
required dependencies and they are not part of the skill's
``tools:`` frontmatter (which is reserved for Claude Code tool
restrictions). Use this list to disambiguate during architecture
discussions.

- ``plugin-loader`` — discovers, validates, and activates plugins at runtime
- ``sandbox-executor`` — runs each plugin in an isolated context with a constrained capability set
- ``sdk-generator`` — produces language-specific SDKs from the kernel's stable interface
