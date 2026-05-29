---
name: use-fullstackrecipes
description: Discover and follow recipes via MCP resources for setup guides, skills, and cookbooks. The meta-skill for using fullstackrecipes effectively.
---

# Building with fullstackrecipes

Discover and follow recipes via MCP resources for setup guides, skills, and cookbooks. The meta-skill for using fullstackrecipes effectively.

## How fullstackrecipes Works

fullstackrecipes provides setup instructions for building full-stack applications and skills to work with them. Content is organized into two types:

1. **Setup Recipes**: Step-by-step guides to configure tools and services (e.g., setting up authentication, database, payments)
2. **Skills**: Instructions for working with previously configured tools (e.g., writing queries, using auth, logging)

**Cookbooks** bundle related recipes together in sequence. For example, "Base App Setup" includes Next.js, Shadcn UI, Neon Postgres, Drizzle ORM, and AI SDK setup recipes and skills.

---

## Accessing Recipes via MCP

The fullstackrecipes MCP server exposes all recipes and cookbooks as resources. Resources are organized by type:

- `recipe://` - Individual setup guides and skills
- `cookbook://` - Bundled recipe sequences

### Set up MCP Server

If the MCP server is not already set up, add it to your coding agent's MCP configuration:

```json
{
  "mcpServers": {
    "fullstackrecipes": {
      "url": "https://fullstackrecipes.com/api/mcp"
    }
  }
}
```

### Read a Specific Recipe

Fetch the full content of any recipe by its resource URI:

```
Read the "neon-drizzle-setup" resource from fullstackrecipes
```

The recipe content includes all steps, code examples, and file paths needed to complete the setup.

---

## Best Practices for Following Recipes

### Follow Recipes Exactly

Recipes are tested instructions. Follow them step-by-step without modifications unless you have a specific reason to deviate.

### Complete Dependencies First

Some recipes depend on others. The MCP resource descriptions indicate prerequisites. Complete setup recipes before using their corresponding skills.

### Use Skills for Day-to-Day Work

Once a tool is configured, use the skill for ongoing development. Skills contain patterns, code examples, and API references that apply to the configured tools.

### Check for Updates

Recipes are updated as libraries evolve. When troubleshooting issues or starting new features, fetch the latest recipe content from the MCP server rather than relying on cached instructions.

---

## References

- [fullstackrecipes.com](https://fullstackrecipes.com) - Browse all recipes and cookbooks
- [MCP Resources](https://fullstackrecipes.com/api/mcp) - Direct MCP server endpoint
