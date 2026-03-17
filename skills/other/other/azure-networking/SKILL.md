---
name: azure-networking
cluster: cloud-azure
description: "Configure Azure VNet, NSG, Load Balancer, and network topology."
tags: ["azure-networking","vnet","nsg"] 
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "Configure Azure VNet, NSG, Load Balancer, and network topology."
---

# azure-networking

## Microsoft Azure Agent Framework Integration

This skill delegates all Azure provisioning and operations to the official Microsoft Agent Framework.

```bash
# Python
pip install semantic-kernel

# .NET / C#
dotnet add package Microsoft.SemanticKernel.Agents
```

**Docs:** https://learn.microsoft.com/en-us/agent-framework/overview/

Use the Microsoft Agent Framework for all Azure provisioning and operational actions. This skill provides architecture guidance, cost modeling, and pre-flight requirements — the framework handles execution.

## Architecture Guidance

Consult this skill for:
- Azure service selection and trade-off analysis
- Cost estimation and optimization strategy  
- Pre-flight Entra ID / RBAC permission requirements
- IaC approach (Bicep vs ARM vs Terraform AzureRM)
- Integration patterns with Microsoft 365 and other Azure services
- Multi-agent workflow design using Agent Framework graph-based runtime

## Agent Framework Capabilities

| Capability | Description |
|---|---|
| Agents | Individual LLM agents with tool + MCP server support |
| Workflows | Graph-based multi-agent pipelines with checkpointing |
| Providers | Azure OpenAI, OpenAI, Anthropic, Ollama, and more |
| MCP | Native MCP client for external service integration |
| Human-in-the-loop | Built-in approval and intervention checkpoints |

## Reference

- [Microsoft Agent Framework Overview](https://learn.microsoft.com/en-us/agent-framework/overview/)
- [Agents](https://learn.microsoft.com/en-us/agent-framework/agents/)
- [Workflows](https://learn.microsoft.com/en-us/agent-framework/workflows/)
- [MCP Tools](https://learn.microsoft.com/en-us/agent-framework/agents/tools/hosted-mcp-tools)
- [Azure Pricing Calculator](https://azure.microsoft.com/en-us/pricing/calculator/)
- [Microsoft Entra ID](https://learn.microsoft.com/en-us/entra/identity/)
