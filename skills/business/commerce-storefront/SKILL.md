---
name: commerce-storefront
description: Build and adapt storefront templates and Agentic Commerce Protocol flows. Use when designing storefront pages, checkout UI, or ACP flows.
---

# Commerce Storefront

Scaffold storefronts and add commerce features using StateSet tools.

## How It Works

1. Choose a template (Next.js, Remix, Vite, Astro).
2. Generate the project scaffold.
3. Add pages, components, and API routes.
4. Seed demo data and run the dev server.

## Usage

- CLI: `stateset-create <name> --template nextjs`
- Use `stateset` or the scaffold MCP server for adding pages/components.
- Keep database path in `.env` and use `@stateset/embedded` on the server.

## Output

```json
{"status":"created","project":"my-storefront","template":"nextjs"}
```

## Present Results to User

- Project path and template used.
- Pages/components added.
- How to run the dev server.

## Troubleshooting

- Missing Node dependencies: run `npm install` in the project.
- Database errors: confirm `.env` path and file permissions.

## References
- references/storefront-templates.md
- /home/dom/stateset-icommerce/cli/.claude/skills/commerce-storefront/SKILL.md
- /home/dom/stateset-icommerce/cli/src/scaffold-server.js
