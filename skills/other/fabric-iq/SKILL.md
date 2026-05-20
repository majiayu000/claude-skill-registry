---
name: fabric-iq
description: Guide for working with Microsoft Fabric IQ (preview), the semantic intelligence workload for unified data and business vocabulary. Use when creating or managing ontology items, defining entity types, binding data to ontologies, creating relationship types, configuring data agents with ontology sources, working with Graph in Microsoft Fabric, managing Fabric IQ tenant settings, querying ontology graphs, generating ontologies from Power BI semantic models, or remediate Fabric IQ preview features. Covers ontology, graph, data agent, operations agent, and semantic model items.
license: Complete terms in LICENSE.txt
---

# Microsoft Fabric IQ

Fabric IQ (preview) is a Fabric workload for unifying data across OneLake and organizing it according to your business vocabulary. It exposes data to analytics, AI agents, and applications with consistent semantic meaning and context.

## When to Use This Skill

- Creating or managing **ontology** items in Fabric IQ
- Defining **entity types**, **properties**, and **relationship types**
- **Binding data** from lakehouses, eventhouses, or semantic models to ontologies
- **Generating ontologies** from Power BI semantic models
- Configuring **Fabric data agents** with ontology as a source
- Working with **Graph in Microsoft Fabric** for traversals and graph queries
- Enabling **Fabric IQ tenant settings** in the admin portal
- Querying ontology graphs using the **preview experience**
- Building **operations agents** that reason across business concepts
- remediate ontology creation, data binding, or agent integration issues
- Automating Fabric IQ items via **REST API** or **PowerShell**

## Prerequisites

1. A Fabric workspace with a Microsoft Fabric-enabled capacity (F2+ or P1+)
2. Required tenant settings enabled (see [tenant-settings.md](./references/tenant-settings.md))
3. Data in OneLake (lakehouse tables), an eventhouse, or Power BI semantic models

## Fabric IQ Items Overview

Fabric IQ contains five items that work together:

| Item | Purpose | Shared With |
|------|---------|-------------|
| **Ontology (preview)** | Enterprise vocabulary and semantic layer — entity types, relationships, properties, data bindings | IQ only |
| **Graph in Microsoft Fabric (preview)** | Native graph storage/compute for nodes, edges, traversals, path finding | Real-Time Intelligence |
| **Fabric data agent (preview)** | Conversational Q&A using generative AI, grounded in ontology | Data Science |
| **Operations agent (preview)** | AI agent to monitor real-time data and recommend actions | Real-Time Intelligence |
| **Power BI semantic model** | Curated analytics model for reporting and DAX | Power BI |

### Choosing the Right Item

| Scenario | Use |
|----------|-----|
| Cross-domain consistency, governance, AI agent grounding | **Ontology** |
| Relationship-heavy questions (impact chains, shortest paths) | **Graph** |
| Trusted KPIs and fast visuals with dimensional modeling | **Power BI semantic model** |
| Operational context, stateful twins, what-if simulation | **Digital twin builder** (Real-Time Intelligence) |

## Step-by-Step Workflows

### Workflow 1: Create an Ontology from OneLake

For the complete walkthrough with all field mappings, see [ontology-workflows.md](./references/ontology-workflows.md#from-onelake).

1. Navigate to your Fabric workspace and select **+ New item > Ontology (preview)**
2. Name the ontology (letters, numbers, underscores only — no spaces or dashes)
3. Add entity types from the ribbon or canvas
4. Bind static or time series data from OneLake sources
5. Set entity type keys (unique identifier properties)
6. Create relationship types between entity types and bind them to source data
7. Use the **preview experience** to explore entity instances and the ontology graph

### Workflow 2: Generate an Ontology from a Semantic Model

For the complete walkthrough, see [ontology-workflows.md](./references/ontology-workflows.md#from-semantic-model).

1. Navigate to your Power BI semantic model in Fabric
2. Select **Generate Ontology** from the ribbon
3. Choose workspace and name the ontology
4. Verify generated entity types, bindings, and relationship types
5. Configure any incomplete relationship bindings manually

### Workflow 3: Connect an Ontology to a Data Agent

For the complete walkthrough, see [ontology-workflows.md](./references/ontology-workflows.md#data-agent).

1. Create a **Data agent** item in your workspace
2. Add the ontology as a **knowledge source**
3. Add agent instructions (e.g., `Support group by in GQL`)
4. Test queries in the agent chat to validate semantic grounding

### Workflow 4: Validate Tenant Prerequisites

Run the [prereq validation script](./scripts/Validate-FabricIQPrereqs.ps1) to check your environment:

```powershell
./scripts/Validate-FabricIQPrereqs.ps1 -TenantId "your-tenant-id"
```

## Key Concepts

### Ontology Core Concepts

| Concept | Description |
|---------|-------------|
| **Entity type** | Represents a real-world concept (e.g., Customer, Truck, Sensor) |
| **Property** | A fact about an entity type (e.g., name, email, temperature) |
| **Entity type key** | Unique identifier property for entity instances |
| **Relationship type** | Semantic connection between entity types (e.g., "drives", "has", "soldIn") |
| **Data binding** | Connects ontology definitions to concrete OneLake data sources |
| **Ontology graph** | Queryable instance graph built from data bindings and relationships |

### Data Binding Types

| Type | Use Case | Example |
|------|----------|---------|
| **Static** | Descriptive attributes that change infrequently | Store locations, product catalog |
| **Time series** | Timestamped observations in columnar format | Sensor telemetry, temperature readings |

### Naming Constraints

| Element | Rules |
|---------|-------|
| Ontology name | Letters, numbers, underscores. No spaces or dashes |
| Entity type name | 1-26 chars, alphanumeric + hyphens + underscores, start/end alphanumeric |
| Property name | 1-26 chars, alphanumeric + hyphens + underscores, unique across entity types for same type |

## REST API Support

The Fabric REST API supports ontology CRUD operations:

| Operation | Supported |
|-----------|-----------|
| Create (without definition) | Yes |
| Create (with payload/definition) | Yes |
| Service principal support | Yes |
| Get | Yes |
| Update | Yes |
| Delete | Yes |
| List | Yes |

Use the Fabric CLI for command-line operations:

```bash
pip install ms-fabric-cli
fab auth login
```

## remediate

For the full remediate guide, see [remediate.md](./references/remediate.md).

| Issue | Quick Fix |
|-------|-----------|
| Unable to create ontology item | Enable all required tenant settings |
| Graph errors on new ontology | Enable **User can create Graph (preview)** tenant setting |
| Data agent 403 Forbidden | Enable Copilot and Azure OpenAI tenant settings |
| Generated ontology has no entity types | Ensure semantic model tables are visible (not hidden) |
| Generated ontology has no data bindings | Check semantic model mode — Import mode not supported |
| Decimal properties return null | Recreate property as Double type |
| Aggregation queries fail in data agent | Add instruction: `Support group by in GQL` |

## References

- [Tenant Settings & Prerequisites](./references/tenant-settings.md)
- [Ontology Workflows (Detailed)](./references/ontology-workflows.md)
- [remediate Guide](./references/remediate.md)
- [Prereq Validation Script](./scripts/Validate-FabricIQPrereqs.ps1)
- [Ontology Template](./templates/ontology-design-template.md)
- [Microsoft Learn: Fabric IQ Overview](https://learn.microsoft.com/en-us/fabric/iq/overview)
- [Microsoft Learn: Ontology Overview](https://learn.microsoft.com/en-us/fabric/iq/ontology/overview)
- [Sample Data: IQ Samples on GitHub](https://github.com/microsoft/fabric-samples/tree/main/docs-samples/iq)
