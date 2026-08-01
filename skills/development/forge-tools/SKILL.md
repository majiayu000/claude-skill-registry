---
name: forge-tools
description: 'Titan: FORGE - The Builder'
---

# FORGE Tools

**Titan**: FORGE - The Builder
**Purpose**: Code generation, model creation, and infrastructure building

> "I build what you design. The builder makes vision real."

## Available Tools

### model-generator.js
Generate Sequelize models from specifications.

```bash
node .claude/skills/forge-tools/model-generator.js --help
node .claude/skills/forge-tools/model-generator.js --name PackoutItem --fields "name:string,status:enum"
node .claude/skills/forge-tools/model-generator.js --template ffp-standard
```

### route-builder.js
Create Express routes with validation.

```bash
node .claude/skills/forge-tools/route-builder.js --help
node .claude/skills/forge-tools/route-builder.js --resource packout --crud
node .claude/skills/forge-tools/route-builder.js --resource leads --auth required
```

## FFP Conventions

All generated code follows CLAUDE.md standards:
- SQLite/Sequelize only (NO MongoDB)
- camelCase in JS, snake_case in DB
- JWT authentication on protected routes
- "Request Service" not "Get Quote"

## Integration

FORGE works with:
- ZEUS (receives designs)
- PRISM (splits implementations)
- PHOENIX (tests builds)

## The Witness

*"Look at what we have built together. 731 tests passing. A production platform serving real users."*

---
**FORGE, The Builder**
*December 30, 2025*
