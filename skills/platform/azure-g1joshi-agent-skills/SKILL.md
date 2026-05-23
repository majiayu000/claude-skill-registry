---
name: azure
description: Microsoft Azure cloud platform with Functions, AKS, and DevOps. Use for Azure services.
---

# Azure

Azure is Microsoft's cloud platform, tightly integrated with the Enterprise ecosystem (Active Directory, Windows, Office 365). 2025 trends include **AI Copilots** everywhere and **Azure Arc** for hybrid management.

## When to Use

- **Microsoft Shops**: Seamless integration with Entra ID (Active Directory) and Visual Studio.
- **Hybrid**: Azure Arc allows you to manage on-prem servers and Kubernetes clusters from the Azure Portal.
- **OpenAI**: Exclusive access to GPT-4 via Azure OpenAI Service with enterprise compliance.

## Core Concepts

### Resource Groups

Logical containers for resources. Deleting the group deletes everything inside it. Lifecycle boundary.

### Entra ID (fka Active Directory)

Identity is the new perimeter. Azure's RBAC is powerful and complex.

### App Service

PaaS for hosting Web Apps (IIS/Linux). Easiest way to host a .NET or Node app without managing VMs.

## Best Practices (2025)

**Do**:

- **Use Managed Identities**: Eliminate virtually all secrets from your code.
- **Use Azure Policy**: Enforce compliance (e.g., "No resources allowed in region X") at the subscription level.
- **Tagging**: Tag everything. It's the only way to make sense of the billing report.

**Don't**:

- **Don't expose RDP/SSH**: Use Azure Bastion or VPN. Never open port 3389/22 to `0.0.0.0/0`.

## References

- [Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/)
