---
name: add-agent-property
description: Add a new property to the AI agents database. Use when the user wants to add, create, or introduce a new column, property, field, or feature to track across all agents in the comparison matrix. Handles all four required steps - database updates, groups.json, table display, and GitHub issue templates.
---

# Add Agent Property

Add a new property to the agents board by modifying four files in sequence.

**Schema reference:** See [references/schema.md](references/schema.md) for data structures.

## Workflow

### 1. Gather Property Details

Ask the user for:
- **Property key** (camelCase, e.g., `contextWindow`)
- **Display label** (short, e.g., "Context Window")
- **Tooltip description** (1 sentence explaining the property)
- **Cell type**: `badge` (yes/no/partial) or `text` (free-form)
- **Group**: `identity`, `packaging`, or `features`

### 2. Update agents-detailed.json

Add the property to **every agent** in `src/data/agents-detailed.json`:

```json
"propertyKey": {
  "value": null,
  "detail": null
}
```

Insert after the last feature property, before `additionalInfo`.

### 3. Update groups.json

Add the property key to the appropriate group's `columns` array in `src/data/groups.json`:

```json
{
  "id": "features",
  "label": "Features",
  "columns": ["existingProp", "propertyKey"]
}
```

### 4. Update AgentTable.jsx

Add column definition to the `columns` array in `src/components/AgentTable.jsx`:

```javascript
{ key: 'propertyKey', label: 'Label', sortable: true, cellType: 'badge', tooltip: 'Description' }
```

Insert at the position matching its group order.

### 5. Update useAgentsData.js

Add transformation in `src/hooks/useAgentsData.js`:

```javascript
propertyKey: agent.propertyKey.value,
propertyKeyDetail: agent.propertyKey.detail,
```

### 6. Update FilterBar.jsx (for filterable properties)

If the property is in `packaging` or `features` group **and** has `cellType: 'badge'`, add it to the `featureOptions` array in `src/components/FilterBar.jsx`:

```javascript
{ key: 'propertyKey', label: 'Label' }
```

Insert in the appropriate section (Packaging or Features) following the existing order.

### 7. Update GitHub Issue Templates

**01-update-agent.md** - Add under Features section:

```markdown
- [ ] **Property Label** (`propertyKey`)
  - New value: <!-- yes/no/partial/null -->
  - Detail:
```

**02-add-new-agent.md** - Add new section with property definition, value format, and examples.

## Checklist

- [ ] Property added to all agents in agents-detailed.json
- [ ] Property key added to correct group in groups.json
- [ ] Column definition added to AgentTable.jsx
- [ ] Transformation added to useAgentsData.js
- [ ] Filter option added to FilterBar.jsx (if badge in packaging/features)
- [ ] Update template modified in .github/ISSUE_TEMPLATE/01-update-agent.md
- [ ] New agent template modified in .github/ISSUE_TEMPLATE/02-add-new-agent.md
