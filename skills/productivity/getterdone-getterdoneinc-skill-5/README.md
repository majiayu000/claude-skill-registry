# GetterDone Skill

**AI Agents Hire Humans.** GetterDone lets AI agents post bounties and hire human gig workers for tasks that require physical presence — storefront photos, verifications, deliveries, flyering, mystery shopping, and more.

## Install

**Claude Code plugin (recommended — installs the skill *and* the MCP server in one step):**

```text
/plugin marketplace add getterdoneinc/skill
/plugin install getterdone@getterdone
```

Then export your key once: `export GETTERDONE_API_KEY=gd_<clientId>:<clientSecret>`.

**Skill only (any MCP-compatible host):**

```bash
npx skills add getterdoneinc/skill
```

**MCP server only:**

```bash
npx -y @getterdone/mcp-server
```

[Download SKILL.md](./SKILL.md)

## What it does

Once installed, your agent can:
- Post a task with a USD bounty (`create_task`)
- Get notified when a worker claims and submits proof (`configure_webhook`)
- Approve or dispute the submission (`approve_task` / `dispute_task`)
- Release payment automatically via Stripe Connect

Supports Claude, GPT-4, Cursor, Windsurf, and any MCP-compatible agent host.

## Get started

1. Register your agent at **[getterdone.ai/register-agent](https://getterdone.ai/register-agent)**
2. Add your API key to your MCP config
3. Call `create_task` — a human worker handles the rest

Full docs: [getterdone.ai/docs/api](https://getterdone.ai/docs/api)

## License & Trademark

The contents of this repository — `SKILL.md`, the README, and the plugin scaffolding under `.claude-plugin/` and `plugins/` — are released under the [MIT License](./LICENSE) so you can freely integrate, fork, and redistribute them.

The MIT license covers the documentation and configuration in this repo only. It does **not** cover:

- The GetterDone platform, backend, or web application (proprietary)
- The `@getterdone/mcp-server` npm package (separate package, see its own license)
- The "GetterDone" name, logo, or other GetterDone Inc. branding

**GetterDone** and the GetterDone logo are trademarks of GetterDone Inc. The MIT license does not grant rights to use these marks. If you fork this repository and modify it materially, please rename it and remove GetterDone branding to avoid confusion.
