---
name: azure-infra-bicep
description: Create or update Azure infrastructure Bicep under infra/ for this project (Cosmos DB account/database/containers, Managed Identity, Container Apps for backend_api) using region japaneast, env dev, and Free Tier enabled. Use when asked to provision Azure infra or write Bicep templates.
---

# Azure Infra Bicep (Cosmos DB + Container Apps)

## Goal
Provision Azure resources with Bicep for this repo:
- Cosmos DB account (NoSQL) + database + containers
- Managed Identity (user-assigned) for API
- Container Apps environment + Container App for backend_api
- RBAC role assignment: Cosmos DB Built-in Data Contributor

## Defaults for this project
- Environment: `dev`
- Location: `japaneast`
- Cosmos DB Free Tier: enabled

## Workflow
1. Create `infra/` if missing.
2. Add `infra/main.bicep` and `infra/params/dev.bicepparam`.
3. Define parameters: `env`, `location`, `containerImage`, `containerCpu`, `containerMemory`, `containerPort`.
4. Create resources:
   - Cosmos DB account (SQL API) with `enableFreeTier: true`.
   - SQL database (name: `real_estate` or `${env}-real-estate`).
   - Containers: `property_types`, `buildings`, `units`, `parking_lots`, `payment_histories`, `attachments`.
     - Partition key: `/id`.
   - Log Analytics workspace.
   - Container Apps environment.
   - User-assigned Managed Identity.
   - Container App for backend_api.
5. Configure Container App env vars:
   - `COSMOS_ENDPOINT` = Cosmos DB account endpoint
   - `COSMOS_DATABASE` = database name
   - `COSMOS_CONTAINER_PREFIX` = `${env}`
6. Add RBAC role assignment:
   - Role: `Cosmos DB Built-in Data Contributor`
   - Scope: Cosmos DB account
   - Principal: user-assigned managed identity
7. Keep the Bicep minimal and deployable at resource group scope.

## Output files
- `infra/main.bicep`
- `infra/params/dev.bicepparam`

## Notes
- Do not add README or extra docs for the skill.
- Prefer concise comments only when a block is complex.
