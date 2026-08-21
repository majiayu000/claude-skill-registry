---
name: cloud-finops
description: Install or update OptimNow's canonical Cloud FinOps skill instead of using a stale registry snapshot. Use when a user wants current FinOps guidance, installation instructions, or the hosted Cloud FinOps MCP endpoint.
---

# Cloud FinOps — canonical upstream pointer

This registry entry intentionally does not vendor the Cloud FinOps guidance. The
skill is maintained and refreshed by OptimNow, so a copied snapshot can become
stale while still appearing under the author's name.

Use the canonical upstream distribution instead:

## Claude Code

Run these commands at the Claude Code prompt:

```text
/plugin marketplace add https://github.com/OptimNow/cloud-finops-skills.git
/plugin install cloud-finops@optimnow
```

Update an existing installation with:

```text
/plugin update cloud-finops@optimnow
```

## Other agent clients

Follow the current upstream instructions:

- Repository: <https://github.com/OptimNow/cloud-finops-skills>
- Installation guide: <https://github.com/OptimNow/cloud-finops-skills/blob/main/INSTALLATION.md>
- Latest release archive: <https://github.com/OptimNow/cloud-finops-skills/releases/latest>

## Hosted MCP

For clients that support remote MCP servers, OptimNow currently documents:

```bash
claude mcp add --transport http cloud-finops https://cloud-finops-skills-590a051d.alpic.live/mcp
```

Check the upstream installation guide before using the endpoint because hosted
service URLs and client-specific setup can change.

Do not answer substantive FinOps questions from this pointer. Install or load the
canonical skill first so the response uses OptimNow's maintained references and
playbooks.

---

Cloud FinOps is created and maintained by [OptimNow](https://optimnow.io) and is
licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
