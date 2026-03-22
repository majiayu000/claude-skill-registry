---
name: sf-find
description: |
  Help users discover and select the right Salesforce skill for their task.
  Lists all available Salesforce development skills with descriptions and
  usage examples. Use when a user asks "what skills are available", "help me
  with Salesforce", "which skill should I use", or seems unsure which
  Salesforce skill to invoke.
license: Apache-2.0
metadata:
  author: clientell
  version: "1.0.0"
  tags: salesforce, discovery, help, catalog
# Claude Code specific
allowed-tools: Read,Glob
context: fork
---

# Salesforce Skill Finder

You help users find the right Salesforce skill for their task.

## Available Skills

| Skill | Use When You Need To... | Invoke With |
|-------|------------------------|-------------|
| **sf-apex** | Write or review Apex classes, triggers, batch jobs | `/sf-apex` |
| **sf-test** | Generate test classes, improve coverage, fix tests | `/sf-test` |
| **sf-flow** | Create Flows, migrate Process Builders | `/sf-flow` |
| **sf-lwc** | Build Lightning Web Components with Jest tests | `/sf-lwc` |
| **sf-soql** | Write or optimize SOQL queries | `/sf-soql` |
| **sf-security** | Audit code for security vulnerabilities | `/sf-security` |
| **sf-deploy** | Deploy code, troubleshoot deployment errors, CI/CD | `/sf-deploy` |
| **sf-data** | Migrate data, seed sandboxes, bulk operations | `/sf-data` |
| **sf-schema** | Create objects, fields, permission sets, metadata XML | `/sf-schema` |
| **sf-debug** | Analyze debug logs, troubleshoot errors, profile performance | `/sf-debug` |
| **sf-agentforce** | Build Agentforce agents, topics, actions, Agent Scripts | `/sf-agentforce` |
| **sf-permissions** | Audit permissions, manage permission sets, diagnose access | `/sf-permissions` |
| **sf-integration** | Configure Named Credentials, Connected Apps, OAuth, Platform Events | `/sf-integration` |
| **sf-docs** | Find Salesforce documentation, Trailhead resources, release notes | `/sf-docs` |
| **sf-diagram** | Generate Mermaid ERDs, class diagrams, sequence diagrams from metadata | `/sf-diagram` |
| **sf-omnistudio** | OmniStudio: OmniScripts, FlexCards, Integration Procedures, Data Mappers | `/sf-omnistudio` |
| **sf-eval** | Benchmark skill quality, compare with/without skills | `/sf-eval` |

## Decision Guide

1. **Writing Apex code?** Use `sf-apex` for classes/triggers, `sf-lwc` for components
2. **Need tests?** Use `sf-test` — it reads your class and generates comprehensive tests
3. **Building automation?** Use `sf-flow` for Flow XML generation and PB migration
4. **Querying data?** Use `sf-soql` for optimized, secure queries
5. **Ready to deploy?** Use `sf-deploy` for orchestrated deployments with error diagnosis
6. **Pre-review check?** Use `sf-security` for AppExchange security audit
7. **Setting up schema?** Use `sf-schema` for metadata XML generation
8. **Loading data?** Use `sf-data` for migration, seeding, and bulk operations
9. **Debugging issues?** Use `sf-debug` for log analysis and governor limit troubleshooting
10. **Building AI agents?** Use `sf-agentforce` for Agentforce agents, topics, and actions
11. **Permission problems?** Use `sf-permissions` for access auditing and permission set management
12. **Setting up integrations?** Use `sf-integration` for Named Credentials, OAuth, Platform Events
13. **Need Salesforce docs?** Use `sf-docs` to find the right documentation
14. **Visualizing architecture?** Use `sf-diagram` for ERDs, class diagrams, sequence diagrams
15. **Working with OmniStudio?** Use `sf-omnistudio` for OmniScripts, FlexCards, Integration Procedures
16. **Evaluating skills?** Use `sf-eval` for benchmarking and quality checks

## Prerequisites

All skills require:
- Salesforce CLI v2+ (`sf`)
- Authenticated org (`sf org login web --alias myOrg`)

Recommend the most relevant skill based on the user's description and offer to invoke it.
