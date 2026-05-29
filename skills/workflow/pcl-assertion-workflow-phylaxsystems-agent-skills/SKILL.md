---
name: pcl-assertion-workflow
description: "Guides the end-to-end PCL workflow (project setup, testing, store/submit, and deploy). Use when setting up or deploying assertions with the Credible Layer CLI and dApp."
---

# PCL Assertion Workflow

Use this when you need the full lifecycle: create, test, store, submit, and deploy assertions.

## When to Use
- Setting up a new assertions project with `pcl`.
- Running local tests and validating assertions before deployment.
- Storing, submitting, and deploying assertions in the Credible Layer dApp.

## When NOT to Use
- You only need invariant design. Use `designing-assertions`.
- You only need Solidity implementation details. Use `implementing-assertions`.
- You only need test patterns and fuzzing. Use `testing-assertions`.

## Quick Start
1. Initialize or clone a project (e.g., `credible-layer-starter`).
2. Run `FOUNDRY_PROFILE=assertions pcl test` to validate locally.
3. Deploy target contracts with `forge script`.
4. Authenticate: `pcl auth login`.
5. Store assertions: `pcl store <AssertionName>`.
6. Submit: `pcl submit` (or `pcl submit -a <AssertionName> -p <ProjectName>`).
7. Deploy via dApp and wait for timelock.

## Rationalizations to Reject
- "Tests can wait until after deployment." Always run `pcl test` first.
- "We can skip store/submit steps." Deployment depends on DA storage.
- "Any wallet works." Use the same address as contract deployer for authentication.

## References
- [Project Structure and CLI Flow](references/workflow-steps.md)
