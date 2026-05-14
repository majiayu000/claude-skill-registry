# Examples and prompt recipes

## Minimal app card config shape

Use this as a shape reference, not as a guaranteed complete file. Check current docs and generated CLI output before final code.

```json
{
  "uid": "customer-health-card",
  "type": "card",
  "config": {
    "name": "Customer Health",
    "description": "Shows external customer health status for the current record.",
    "location": "crm.record.tab",
    "entrypoint": "/app/cards/CustomerHealthCard.tsx",
    "objectTypes": ["companies"]
  }
}
```

## Minimal extension entrypoint shape

```tsx
import React from "react";
import { hubspot, Text, Button, Flex, LoadingSpinner, Alert } from "@hubspot/ui-extensions";

hubspot.extend(({ context, actions }) => (
  <CustomerHealthCard context={context} actions={actions} />
));

function CustomerHealthCard({ context, actions }) {
  const recordId = context?.crm?.objectId;

  if (!recordId) {
    return <Alert title="Record unavailable">Open this card from a supported CRM record.</Alert>;
  }

  return (
    <Flex direction="column" gap="sm">
      <Text format={{ fontWeight: "bold" }}>Customer health</Text>
      <Text>Use CRM hooks or hubspot.fetch() to load contextual data.</Text>
      <Button onClick={() => actions.addAlert({ message: "Action started", type: "success" })}>
        Start action
      </Button>
    </Flex>
  );
}
```

## Prompt recipe: create a new app card

Use this with Claude Code, Codex, or another coding agent:

```text
Use the hubspot-developer-platform skill. In this existing HubSpot developer platform project, add a modern UI extension app card for [object type] at [location]. The card should [user workflow]. Inspect the current project files first, use the generated CLI structure where possible, keep scopes minimal, use TypeScript and @hubspot/ui-extensions components, include loading/empty/error states, and document manual HubSpot testing steps.
```

## Prompt recipe: review an existing app

```text
Use the hubspot-developer-platform skill. Review this HubSpot developer platform app for modern platform correctness. Check extension metadata, platform version assumptions, use of hubspot.extend(), UI component usage, hubspot.fetch() limits, sensitive data scope risks, permissions, local dev workflow, and Marketplace-readiness issues. Return specific file-level findings and fixes.
```

## Prompt recipe: migrate a legacy card

```text
Use the hubspot-developer-platform skill. Migrate this legacy HubSpot CRM card concept to a modern developer platform UI extension app card. Identify the old data flow, required scopes, target object types, card location, external service calls, and the modern file structure. Produce code changes plus a migration checklist.
```

## Prompt recipe: design before coding

```text
Use the hubspot-developer-platform skill. Design a modern HubSpot app for [business process]. Choose whether it needs app cards, app pages, settings pages, OAuth/API setup, serverless functions, or external fetch calls. Explain the recommended extension points, data flow, security constraints, scopes, and implementation phases before writing code.
```

