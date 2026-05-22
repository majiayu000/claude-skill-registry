---
name: fabric-data-agent
description: Create, configure, and manage Microsoft Fabric Data Agents that enable natural language Q&A over lakehouses, warehouses, Power BI semantic models, KQL databases, and ontologies. Use when asked to build data agents, configure NL2SQL/NL2DAX/NL2KQL experiences, write agent instructions, create example queries, automate data agent provisioning via REST API or PowerShell, integrate Fabric data agents with Azure AI Foundry, or troubleshoot data agent configuration issues.
license: Complete terms in LICENSE.txt
---
# Microsoft Fabric Data Agents

Build conversational AI experiences that let users ask questions in plain English against structured data in Microsoft Fabric. Fabric Data Agents translate natural language into SQL, DAX, or KQL queries, execute them securely under the caller's identity, and return data-driven answers.

## When to Use This Skill

- Creating a new Fabric Data Agent from the portal or via REST API
- Configuring data sources (Lakehouse, Warehouse, Power BI Semantic Model, KQL Database, Ontology)
- Writing effective agent-level or data-source-level instructions
- Authoring example queries (few-shot examples) to improve NL2SQL/NL2DAX/NL2KQL accuracy
- Automating data agent provisioning with PowerShell and the Fabric REST API
- Integrating a published Fabric Data Agent with Azure AI Foundry agents
- Managing the Operations Agent definition (Configurations.json) programmatically
- Publishing, sharing, and versioning data agents
- remediate query generation, data source permissions, or tenant settings

## Prerequisites

| Requirement                    | Details                                                                                      |
| ------------------------------ | -------------------------------------------------------------------------------------------- |
| Fabric capacity                | Paid F2+ SKU, or Power BI Premium P1+ with Fabric enabled                                    |
| Tenant settings                | Fabric data agent, Cross-geo processing for AI, Cross-geo storing for AI all enabled         |
| XMLA endpoints                 | Enabled if using Power BI Semantic Model data sources                                        |
| Data source access             | At least Read permission on target lakehouses, warehouses, semantic models, or KQL databases |
| PowerShell (automation)        | PowerShell 7.4+, Az.Accounts module                                                          |
| Azure AI Foundry (integration) | Foundry Project endpoint, Fabric connection, model deployment                                |

## Step-by-Step Workflows

### Workflow 1: Create and Configure a Data Agent (Portal)

1. Navigate to your workspace and select **+ New Item > Fabric data agent**
2. Provide a descriptive name for the agent
3. Add up to 5 data sources from the OneLake catalog (any mix of Lakehouse, Warehouse, PBI Semantic Model, KQL DB, Ontology)
4. Select/deselect tables in the Explorer pane to control what the AI can query
5. Write agent instructions — see [instruction-best-practices.md](./references/instruction-best-practices.md)
6. Add example queries for each data source — see [example-query-guide.md](./references/example-query-guide.md)
7. Test the agent in the chat pane with representative questions
8. Select **Publish** and provide a description
9. Share the published version with colleagues via workspace permissions

### Workflow 2: Automate Data Agent via REST API (PowerShell)

1. Authenticate with `Connect-AzAccount` and obtain an access token
2. Create the agent item using the Fabric Items API — run [New-FabricDataAgent.ps1](./scripts/New-FabricDataAgent.ps1)
3. Configure the Operations Agent definition (Configurations.json) — see [operations-agent-schema.md](./references/operations-agent-schema.md)
4. Update the item definition using the Update Item Definition API
5. Validate deployment by listing items in the workspace

### Workflow 3: Integrate with Azure AI Foundry

1. Create and **publish** the Fabric Data Agent in the Fabric portal
2. Create a Foundry Agent in the Azure AI Foundry portal
3. Add a Microsoft Fabric connection to your Foundry project
4. Create the agent with the Fabric tool enabled — see [foundry-integration.md](./references/foundry-integration.md)
5. Create a thread, add a user question, run the thread, and retrieve the response
6. Update Foundry agent instructions to describe what data the Fabric tool can access

## remediate

| Symptom                                      | Cause                                     | Resolution                                                         |
| -------------------------------------------- | ----------------------------------------- | ------------------------------------------------------------------ |
| Data agent option not visible in New Item    | Tenant setting disabled                   | Admin enables "Fabric data agent" in Tenant Settings               |
| Agent can't see my tables                    | Tables not selected in Explorer           | Check table checkboxes in the data source Explorer                 |
| Queries return permission errors             | Insufficient data access                  | Grant at least Read on the underlying data source                  |
| Example queries show validation errors       | SQL/KQL syntax invalid or schema mismatch | Validate queries against the actual table schema                   |
| Agent misinterprets domain terms             | Missing definitions in instructions       | Add term definitions in Agent Instructions (up to 15,000 chars)    |
| Power BI semantic model won't add            | XMLA endpoints disabled                   | Enable "Power BI semantic models via XMLA endpoints" tenant switch |
| Published agent not accessible to colleagues | Workspace permissions not granted         | Share the workspace or agent item with appropriate roles           |

## References

- [Instruction Best Practices](./references/instruction-best-practices.md) — How to write effective agent and data-source instructions
- [Example Query Guide](./references/example-query-guide.md) — Authoring few-shot examples for NL2SQL/NL2DAX/NL2KQL
- [Operations Agent Schema](./references/operations-agent-schema.md) — REST API definition structure (Configurations.json)
- [Foundry Integration](./references/foundry-integration.md) — Connecting Fabric Data Agents with Azure AI Foundry
- [Microsoft Learn: Create a Fabric data agent](https://learn.microsoft.com/en-us/fabric/data-science/how-to-create-data-agent)
- [Microsoft Learn: Data agent configuration](https://learn.microsoft.com/en-us/fabric/data-science/data-agent-config)
