---
version: 4.1.0-fractal
name: linkerd-patterns
description: Implement Linkerd service mesh patterns for lightweight, security-focused service mesh deployments. Use when setting up Linkerd, configuring traffic policies, or implementing zero-trust networking with minimal overhead.
---

# Linkerd Patterns

Production patterns for Linkerd service mesh - the lightweight, security-first service mesh for Kubernetes.

## Do not use this skill when

- The task is unrelated to linkerd patterns
- You need a different domain or tool outside this scope

## Instructions

- Clarify goals, constraints, and required inputs.
- Apply relevant best practices and validate outcomes.
- Provide actionable steps and verification.
- If detailed examples are required, open `resources/implementation-playbook.md`.

## Use this skill when

- Setting up a lightweight service mesh
- Implementing automatic mTLS
- Configuring traffic splits for canary deployments
- Setting up service profiles for per-route metrics
- Implementing retries and timeouts
- Multi-cluster service mesh

## Core Concepts

## 🧠 Knowledge Modules (Fractal Skills)

### 1. [1. Linkerd Architecture](./sub-skills/1-linkerd-architecture.md)
### 2. [2. Key Resources](./sub-skills/2-key-resources.md)
### 3. [Template 1: Mesh Installation](./sub-skills/template-1-mesh-installation.md)
### 4. [Template 2: Inject Namespace](./sub-skills/template-2-inject-namespace.md)
### 5. [Template 3: Service Profile with Retries](./sub-skills/template-3-service-profile-with-retries.md)
### 6. [Template 4: Traffic Split (Canary)](./sub-skills/template-4-traffic-split-canary.md)
### 7. [Template 5: Server Authorization Policy](./sub-skills/template-5-server-authorization-policy.md)
### 8. [Template 6: HTTPRoute for Advanced Routing](./sub-skills/template-6-httproute-for-advanced-routing.md)
### 9. [Template 7: Multi-cluster Setup](./sub-skills/template-7-multi-cluster-setup.md)
### 10. [Do's](./sub-skills/dos.md)
### 11. [Don'ts](./sub-skills/donts.md)
