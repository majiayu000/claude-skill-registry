---
name: fabric-data-agent-remediate
description: Diagnose and resolve Microsoft Fabric Data Agent issues including tenant settings, data source configuration, query generation failures, cross-region capacity errors, XMLA endpoint setup, Power BI semantic model integration, lakehouse/warehouse/KQL connectivity, example query validation, publishing/sharing problems, and Azure AI Foundry integration. Use when asked to troubleshoot data agent, fix Fabric AI agent, debug NL2SQL/NL2DAX/NL2KQL, resolve Copilot tenant settings, or diagnose Fabric data agent errors.
license: Complete terms in LICENSE.txt
---
# Fabric Data Agent remediate

Structured remediate guide for diagnosing and resolving issues with Microsoft Fabric Data Agent (preview). Covers the full lifecycle from tenant configuration through data source setup, query tuning, publishing, and external integration.

## When to Use This Skill

- Fabric data agent cannot be created or is missing from the workspace
- Data agent returns errors, empty results, or inaccurate queries
- Tenant settings are misconfigured for Copilot and Azure OpenAI
- Power BI semantic model data source fails to connect (XMLA)
- Cross-region capacity errors prevent query execution
- Example queries fail validation or are ignored by the agent
- Published data agent is inaccessible to shared users
- Azure AI Foundry or Copilot Studio integration issues
- Agent generates incorrect SQL, DAX, or KQL queries
- Conversation history is lost or not persisting

## Prerequisites

- Microsoft Fabric capacity: F2 or higher (or Power BI Premium P1+ with Fabric enabled)
- Fabric Admin Portal access (for tenant settings)
- At least one data source with data: lakehouse, warehouse, Power BI semantic model, KQL database, or ontology
- Workspace Contributor (or higher) permissions
- PowerShell 7+ recommended for diagnostic scripts

## Quick Diagnosis Workflow

Follow this decision tree to rapidly identify your issue category:

1. **Cannot create data agent?** → See [Tenant Settings Checklist](./references/tenant-settings-checklist.md)
2. **Data agent created but queries fail?** → See [Query remediate](./references/query-remediate.md)
3. **Data source not appearing or erroring?** → See [Data Source Connectivity](./references/data-source-connectivity.md)
4. **Published agent inaccessible?** → See [Publishing and Sharing](./references/publishing-and-sharing.md)
5. **Integration with Foundry/Teams failing?** → See [External Integration](./references/external-integration.md)

## Known Limitations (Preview)

These are product limitations, not configuration errors. Do not troubleshoot these as bugs:

| Limitation              | Detail                                                                 |
| ----------------------- | ---------------------------------------------------------------------- |
| Read-only queries       | Agent generates only SELECT/read queries; no INSERT, UPDATE, or DELETE |
| English only            | Non-English questions, instructions, and examples are not supported    |
| No unstructured data    | PDF, DOCX, TXT files cannot be used as data sources                    |
| Lakehouse files         | Agent reads lakehouse tables only, not standalone CSV/JSON files       |
| Fixed LLM               | The underlying LLM model cannot be changed                             |
| Max 5 data sources      | Up to five data sources in any combination per agent                   |
| Max 100 example queries | Per data source limit for example query pairs                          |
| Cross-region blocked    | Data source and agent capacities must be in the same region            |
| Conversation history    | May reset during backend updates or model upgrades                     |
| No PBI example queries  | Power BI semantic models do not support sample query/question pairs    |

## Common Error Patterns

| Symptom                           | Likely Cause                                | Quick Fix                                                                 |
| --------------------------------- | ------------------------------------------- | ------------------------------------------------------------------------- |
| "Data agent" item type missing    | Tenant setting disabled                     | Enable "Fabric data agent" in Admin Portal                                |
| Agent created but no response     | Copilot tenant switch off                   | Enable "Users can use Copilot and other features powered by Azure OpenAI" |
| Cross-geo processing error        | Cross-geo settings disabled                 | Enable both cross-geo processing AND storing settings                     |
| XMLA connection failure           | XMLA endpoints not enabled                  | Enable "Allow XMLA endpoints" in Integration settings                     |
| Query returns empty/wrong results | Poor table/column names or missing examples | Add descriptive names and example query pairs                             |
| "Cannot execute query" error      | Capacity region mismatch                    | Move agent or data source to same region capacity                         |
| First queries fail after creation | Agent initialization delay                  | Wait 2-3 minutes after creation before querying                           |
| Example queries ignored           | Invalid SQL/KQL syntax                      | Validate all example queries match schema exactly                         |
| Published agent not visible       | Permissions not shared                      | Share agent with Read permission to target users                          |
| 403 Forbidden on data source      | User lacks data access                      | Grant workspace Contributor or data Read permissions                      |

## Diagnostic Script

Run the [Fabric Data Agent Diagnostic](./scripts/Test-FabricDataAgentConfig.ps1) PowerShell script to validate tenant settings and connectivity prerequisites programmatically.

```powershell
./scripts/Test-FabricDataAgentConfig.ps1 -WorkspaceId "<guid>" -Verbose
```

## Configuration Validation Template

Use the [Configuration Checklist](./templates/data-agent-config-checklist.md) template to document and track your data agent configuration for team handoff or support tickets.

## References

- [Tenant Settings Checklist](./references/tenant-settings-checklist.md) - Complete tenant configuration walkthrough
- [Query remediate](./references/query-remediate.md) - NL2SQL/NL2DAX/NL2KQL diagnosis
- [Data Source Connectivity](./references/data-source-connectivity.md) - Lakehouse, warehouse, KQL, PBI, ontology issues
- [Publishing and Sharing](./references/publishing-and-sharing.md) - Publish, share, and consume data agents
- [External Integration](./references/external-integration.md) - Azure AI Foundry, Copilot Studio, Teams integration
- [Microsoft Learn: Create a Fabric data agent](https://learn.microsoft.com/en-us/fabric/data-science/how-to-create-data-agent)
- [Microsoft Learn: Data agent concepts](https://learn.microsoft.com/en-us/fabric/data-science/concept-data-agent)
- [Microsoft Learn: Tenant settings](https://learn.microsoft.com/en-us/fabric/data-science/data-agent-tenant-settings)
- [Microsoft Learn: Data agent SDK](https://learn.microsoft.com/en-us/fabric/data-science/fabric-data-agent-sdk)
- [Microsoft Learn: Evaluate your data agent](https://learn.microsoft.com/en-us/fabric/data-science/evaluate-data-agent)
