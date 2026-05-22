---
name: azure-deploy
description: "Execute Azure deployments after preparation and validation are complete. USE FOR: azd up, azd deploy, push to Azure, publish to Azure, ship to production, launch on Azure, go live, release to Azure, deploy web app, deploy container app, deploy static site, deploy Azure Functions, azd provision, infrastructure deployment, bicep deploy, terraform apply. DO NOT USE FOR: preparing new apps (use azure-prepare), validating before deploy (use azure-validate)."
---

# Azure Deploy

> **AUTHORITATIVE GUIDANCE — MANDATORY COMPLIANCE**
>
> **PREREQUISITE**: The **azure-validate** skill **MUST** be invoked and completed with status `Validated` BEFORE executing this skill.

## Triggers

Activate this skill when user wants to:
- Deploy their application to Azure
- Publish, host, or launch their app
- Push updates to existing deployment
- Run `azd up` or `az deployment`
- Ship code to production
- Deploy Azure Functions to the cloud

## Rules

1. Run after azure-prepare and azure-validate
2. Manifest must exist with status `Validated`
3. **Pre-deploy checklist required** — [pre-deploy-checklist](references/pre-deploy-checklist.md)
4. ⛔ **Destructive actions require `ask_user`** — [global-rules](references/global-rules.md)

---

## Steps

| # | Action | Reference |
|---|--------|-----------|
| 1 | **Check Manifest** — Verify status = `Validated` | — |
| 2 | **Pre-Deploy Checklist** — MUST complete ALL steps | [pre-deploy-checklist](references/pre-deploy-checklist.md) |
| 3 | **Load Recipe** — Based on `recipe.type` in manifest | [recipes/](references/recipes/) |
| 4 | **Execute Deploy** — Follow recipe steps | Recipe README |
| 5 | **Handle Errors** — See recipe's `errors.md` | — |
| 6 | **Verify Success** — Confirm deployment completed and endpoints are accessible | — |

## Recipes

| Recipe | Reference |
|--------|-----------|
| AZD | [recipes/azd/](references/recipes/azd/) |
| AZCLI | [recipes/azcli/](references/recipes/azcli/) |
| Bicep | [recipes/bicep/](references/recipes/bicep/) |
| Terraform | [recipes/terraform/](references/recipes/terraform/) |

## MCP Tools

| Tool | Purpose |
|------|---------|
| `mcp_azure_mcp_subscription_list` | List available subscriptions |
| `mcp_azure_mcp_group_list` | List resource groups in subscription |
| `mcp_azure_mcp_azd` | Execute AZD commands |
