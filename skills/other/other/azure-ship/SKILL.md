---
name: azure-ship
description: Azure shipping gate for App Service, Functions, Container Apps, AKS, slots, managed identity, Key Vault, app settings, ingress, and rollout safety. Use when releasing to Azure and you want a provider-specific read on config drift, identity failures, swap risk, or rollback realism.
user-invocable: true
argument-hint: "[App Service, Function App, Container App, AKS deploy, or Azure release]"
---

Read `../_house-style/house-style.md` before starting.

## Anchor phrases

- Slot swap confidence without config discipline is fantasy.
- Managed identity mistakes fail at runtime, not in meeting notes.
- If Key Vault access is wrong, deployment success is meaningless.
- Azure rollout safety is mostly config truth, not YAML poetry.

## What to interrogate

### 1. Release surface

State what is shipping:
- App Service
- Function App
- Container App
- AKS workload
- slot swap
- identity, settings, secrets, ingress, or scaling changes

### 2. Identity and config realism

Check:
- managed identity assumptions
- Key Vault references and permissions
- slot setting correctness
- environment/app setting drift
- ingress and auth expectations

### 3. Runtime behavior

Review:
- startup and health probe assumptions
- background job or queue behavior
- function cold start or trigger assumptions
- scaling thresholds
- what happens when dependencies are slow or unavailable

### 4. Rollout and rollback

Ask:
- is there a slot, revision, or staged rollout?
- can traffic move back safely?
- are schema/config changes backward-compatible?
- what is the real blast radius if the deploy is bad?

## Output format

### Azure release surface

What is actually being deployed or swapped.

### Platform blockers

Identity, settings, slot, startup, ingress, or scaling blockers.

### Rollout and rollback risk

What can go wrong during promotion or recovery.

### Safer release plan

Concrete mitigations, staging, and rollback steps.

### Verdict

- **Safe to release**
- **Fix before release**
- **Azure release red flag**
