---
name: n8n-syntax-node-types
description: >
  Use when creating custom n8n nodes, defining node properties, implementing
  execute methods, or building declarative nodes. Prevents incorrect
  INodeProperties types and malformed displayOptions conditions. Covers
  INodeType interface, INodeTypeDescription, INodeProperties (22 types),
  displayOptions with rich conditions, execute() method with IExecuteFunctions,
  Node base class alternative, versioned nodes, declarative routing, and methods
  (loadOptions, listSearch, credentialTest, resourceMapping).
  Keywords: n8n, custom nodes, INodeType, INodeProperties, execute,
  displayOptions, declarative routing, versioned nodes, credentialTest.
license: MIT
compatibility: "Designed for Claude Code. Requires n8n v1.x."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# n8n-syntax-node-types

## Quick Reference

### INodeType Interface Members

| Member | Signature | Required | Purpose |
|--------|-----------|----------|---------|
| `description` | `INodeTypeDescription` | YES | Node metadata, properties, credentials |
| `execute` | `(this: IExecuteFunctions) => Promise<INodeExecutionData[][]>` | For regular nodes | Process input items |
| `trigger` | `(this: ITriggerFunctions) => Promise<ITriggerResponse>` | For event triggers | Emit data on events |
| `poll` | `(this: IPollFunctions) => Promise<INodeExecutionData[][] \| null>` | For polling triggers | Periodically check for data |
| `webhook` | `(this: IWebhookFunctions) => Promise<IWebhookResponseData>` | For webhook nodes | Handle HTTP requests |
| `supplyData` | `(this: ISupplyDataFunctions, itemIndex: number) => Promise<SupplyData>` | For AI sub-nodes | Provide data to AI agents |
| `methods` | `{ loadOptions, listSearch, credentialTest, resourceMapping, actionHandler }` | No | Dynamic methods |
| `webhookMethods` | `{ [name]: { checkExists, create, delete } }` | No | External webhook lifecycle |

### INodeTypeDescription Key Fields

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `displayName` | `string` | YES | Human-readable name in UI |
| `name` | `string` | YES | Internal identifier (e.g., `'myNode'`) |
| `icon` | `string \| { light, dark }` | No | `'fa:icon-name'` or `'file:icon.svg'` |
| `group` | `NodeGroupType[]` | YES | `'input'`, `'output'`, `'transform'`, `'trigger'`, `'schedule'` |
| `version` | `number \| number[]` | YES | Supported versions |
| `description` | `string` | YES | Short description |
| `defaults` | `{ name: string }` | YES | Default node name |
| `inputs` | `NodeConnectionType[] \| ExpressionString` | YES | Input connections |
| `outputs` | `NodeConnectionType[] \| ExpressionString` | YES | Output connections |
| `credentials` | `INodeCredentialDescription[]` | No | Required credential types |
| `properties` | `INodeProperties[]` | YES | Node parameters |
| `polling` | `true` | No | Marks node as polling trigger |
| `webhooks` | `IWebhookDescription[]` | No | Webhook registrations |
| `requestDefaults` | `HttpRequestOptions` | No | Declarative base URL/headers |
| `usableAsTool` | `true` | No | Enable as AI agent tool |
| `subtitle` | `string` | No | Dynamic expression for UI subtitle |

### All 22 Property Types (NodePropertyTypes)

| Type | UI Element | Default Value Type |
|------|-----------|-------------------|
| `'boolean'` | Toggle switch | `boolean` |
| `'button'` | Action button | `string` |
| `'collection'` | Group of optional fields | `{}` |
| `'color'` | Color picker | `string` |
| `'dateTime'` | Date/time picker | `string` |
| `'fixedCollection'` | Group with fixed structure | `{}` |
| `'hidden'` | Hidden value | `string` |
| `'icon'` | Icon selector | `string` |
| `'json'` | JSON editor | `string` |
| `'callout'` | Info/warning callout | `string` |
| `'notice'` | Notice/info text | `string` |
| `'multiOptions'` | Multi-select dropdown | `string[]` |
| `'number'` | Number input | `number` |
| `'options'` | Single-select dropdown | `string` |
| `'string'` | Text input | `string` |
| `'credentialsSelect'` | Credential selector | `string` |
| `'resourceLocator'` | Resource locator (ID/URL/list) | `object` |
| `'curlImport'` | cURL import | `string` |
| `'resourceMapper'` | Resource field mapper | `object` |
| `'filter'` | Filter/condition builder | `object` |
| `'assignmentCollection'` | Field assignment collection | `object` |
| `'workflowSelector'` | Workflow selector | `string` |
| `'credentials'` | Credentials property | `string` |

### IExecuteFunctions Key Methods

| Method | Signature | Purpose |
|--------|-----------|---------|
| `getInputData` | `(inputIndex?: number) => INodeExecutionData[]` | Get input items |
| `getNodeParameter` | `(name: string, itemIndex: number) => any` | Read parameter value |
| `getCredentials` | `(type: string) => Promise<ICredentialDataDecryptedObject>` | Get decrypted credentials |
| `continueOnFail` | `() => boolean` | Check continue-on-fail setting |
| `executeWorkflow` | `(workflowInfo, inputData?) => Promise<ExecuteWorkflowData>` | Call sub-workflow |
| `putExecutionToWait` | `(waitTill: Date) => Promise<void>` | Pause execution until date |
| `sendMessageToUI` | `(message: any) => void` | Send message to editor UI |
| `helpers.httpRequest` | `(options) => Promise<any>` | Make HTTP requests |
| `helpers.getBinaryDataBuffer` | `(itemIndex, propertyName) => Promise<Buffer>` | Read binary data |
| `helpers.prepareBinaryData` | `(buffer, fileName?, mimeType?) => Promise<IBinaryData>` | Create binary data |
| `helpers.normalizeItems` | `(items) => INodeExecutionData[]` | Normalize item format |

### Critical Warnings

**ALWAYS** return `INodeExecutionData[][]` from `execute()` -- the outer array represents output indices (for multi-output nodes like IF/Switch), the inner array contains items. Single-output nodes return `[returnData]`.

**ALWAYS** iterate over input items using `this.getInputData()` and call `getNodeParameter(name, i)` with the item index `i` -- parameters can contain expressions that resolve differently per item.

**ALWAYS** handle `continueOnFail()` in the catch block of your item loop -- when enabled, push an error item with `pairedItem` instead of throwing.

**NEVER** use `&str` or borrowed types in node parameters -- n8n uses `IDataObject` (plain objects) for all parameter values. Cast with `as string`, `as number`, etc.

**NEVER** create an `execute()` method in declarative nodes -- n8n handles HTTP requests automatically based on `routing` configuration in properties.

**NEVER** define `inputs` on trigger nodes -- trigger nodes ALWAYS have `inputs: []` (empty array) because they start workflow execution.

**NEVER** use `this` binding in the `Node` base class -- the `Node` class passes `context` as a parameter. Use `context.getInputData()` instead of `this.getInputData()`.

**ALWAYS** set `noDataExpression: true` on resource and operation selector properties -- these properties control node behavior and MUST NOT be expression-dependent.

---

## Decision Trees

### Which Node Pattern to Use?

```
Is this a trigger/starting node?
├── YES: Does it respond to HTTP requests?
│   ├── YES → Webhook pattern (webhook() + webhooks config)
│   └── NO: Does it poll an external service?
│       ├── YES → Poll pattern (poll() + polling: true)
│       └── NO → Trigger pattern (trigger() + emit())
└── NO: Is this a simple REST API wrapper?
    ├── YES → Declarative pattern (routing in properties, NO execute())
    └── NO → Programmatic pattern (execute() with custom logic)
```

### Which Property Type to Use?

```
What data does the user provide?
├── True/false → 'boolean'
├── Free text → 'string' (add rows for textarea, editor for code)
├── A number → 'number' (set minValue/maxValue in typeOptions)
├── One choice from list → 'options'
├── Multiple choices from list → 'multiOptions'
├── A set of optional fields → 'collection'
├── A structured group of fields → 'fixedCollection'
├── Raw JSON → 'json'
├── Date/time → 'dateTime'
├── A color → 'color'
├── Filter conditions → 'filter'
├── Field mapping → 'resourceMapper'
├── Field assignments → 'assignmentCollection'
├── Resource ID/URL/name → 'resourceLocator'
├── Another workflow → 'workflowSelector'
└── Display-only info → 'notice' or 'callout'
```

---

## Essential Patterns

### Pattern 1: Programmatic Node (implements INodeType)

```typescript
import type {
    IExecuteFunctions,
    INodeExecutionData,
    INodeType,
    INodeTypeDescription,
} from 'n8n-workflow';
import { NodeConnectionTypes } from 'n8n-workflow';

export class MyNode implements INodeType {
    description: INodeTypeDescription = {
        displayName: 'My Node',
        name: 'myNode',
        icon: 'file:myIcon.svg',
        group: ['transform'],
        version: 1,
        description: 'Processes data',
        defaults: { name: 'My Node' },
        inputs: [NodeConnectionTypes.Main],
        outputs: [NodeConnectionTypes.Main],
        properties: [/* see references/methods.md */],
    };

    async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
        const items = this.getInputData();
        const returnData: INodeExecutionData[] = [];

        for (let i = 0; i < items.length; i++) {
            try {
                const value = this.getNodeParameter('myParam', i) as string;
                returnData.push({ json: { result: value } });
            } catch (error) {
                if (this.continueOnFail()) {
                    returnData.push({
                        json: { error: (error as Error).message },
                        pairedItem: { item: i },
                    });
                    continue;
                }
                throw error;
            }
        }

        return [returnData]; // Single output
    }
}
```

### Pattern 2: Node Base Class (context parameter)

```typescript
import { Node } from 'n8n-workflow';
import type {
    IExecuteFunctions,
    INodeExecutionData,
    INodeTypeDescription,
} from 'n8n-workflow';

export class MyNode extends Node {
    description: INodeTypeDescription = { /* same as above */ };

    async execute(
        context: IExecuteFunctions  // context parameter, NOT this
    ): Promise<INodeExecutionData[][]> {
        const items = context.getInputData();  // Use context, not this
        const returnData: INodeExecutionData[] = [];

        for (let i = 0; i < items.length; i++) {
            const value = context.getNodeParameter('myParam', i) as string;
            returnData.push({ json: { result: value } });
        }

        return [returnData];
    }
}
```

### Pattern 3: Declarative Node (routing, NO execute)

```typescript
export class ApiNode implements INodeType {
    description: INodeTypeDescription = {
        displayName: 'API Node',
        name: 'apiNode',
        group: ['input'],
        version: 1,
        description: 'Interacts with an API',
        defaults: { name: 'API Node' },
        inputs: [NodeConnectionTypes.Main],
        outputs: [NodeConnectionTypes.Main],
        credentials: [{ name: 'myApi', required: true }],
        requestDefaults: {
            baseURL: 'https://api.example.com',
            headers: { Accept: 'application/json' },
        },
        properties: [
            {
                displayName: 'Operation',
                name: 'operation',
                type: 'options',
                noDataExpression: true,
                options: [
                    {
                        name: 'Get Many',
                        value: 'getAll',
                        action: 'Get many items',
                        routing: {
                            request: { method: 'GET', url: '/items' },
                        },
                    },
                ],
                default: 'getAll',
            },
        ],
    };
    // NO execute() method -- n8n handles requests via routing
}
```

### Pattern 4: displayOptions (Conditional Properties)

```typescript
// Show 'limit' only when operation is 'getAll' AND returnAll is false
{
    displayName: 'Limit',
    name: 'limit',
    type: 'number',
    default: 50,
    typeOptions: { minValue: 1 },
    displayOptions: {
        show: {
            operation: ['getAll'],
            returnAll: [false],
        },
    },
}

// Rich conditions with operators
{
    displayName: 'Advanced Field',
    name: 'advancedField',
    type: 'string',
    default: '',
    displayOptions: {
        show: {
            '@version': [{ _cnd: { gte: 2 } }],      // Version 2+
            status: [{ _cnd: { not: 'archived' } }],  // Not archived
        },
    },
}
```

### Pattern 5: Versioned Node

```typescript
import type { IVersionedNodeType, INodeType } from 'n8n-workflow';

export class MyNodeVersioned implements IVersionedNodeType {
    currentVersion = 2;
    description = { /* INodeTypeBaseDescription */ };
    nodeVersions: { [key: number]: INodeType } = {
        1: new MyNodeV1(),
        2: new MyNodeV2(),
    };

    getNodeType(version?: number): INodeType {
        return this.nodeVersions[version ?? this.currentVersion];
    }
}
```

### Pattern 6: methods Object (Dynamic Loading)

```typescript
methods = {
    loadOptions: {
        async getUsers(this: ILoadOptionsFunctions): Promise<INodePropertyOptions[]> {
            const credentials = await this.getCredentials('myApi');
            const users = await this.helpers.httpRequest({ /* ... */ });
            return users.map((u: any) => ({ name: u.name, value: u.id }));
        },
    },
    listSearch: {
        async searchUsers(
            this: ILoadOptionsFunctions,
            filter?: string,
            paginationToken?: string,
        ): Promise<INodeListSearchResult> {
            // Return { results: [...], paginationToken?: string }
        },
    },
    credentialTest: {
        async testMyApi(this: ICredentialTestFunctions): Promise<INodeCredentialTestResult> {
            // Return { status: 'OK', message: 'Success' }
            // or { status: 'Error', message: 'Invalid credentials' }
        },
    },
    resourceMapping: {
        async getFields(this: ILoadOptionsFunctions): Promise<ResourceMapperFields> {
            // Return field definitions for resource mapper
        },
    },
};
```

---

## INodeExecutionData Structure

```typescript
interface INodeExecutionData {
    json: IDataObject;                     // REQUIRED -- the main data payload
    binary?: IBinaryKeyData;               // Optional binary/file data
    error?: NodeApiError;                  // Error info if item errored
    pairedItem?: IPairedItemData | number; // Source item linking
}

// Binary data keyed by property name
interface IBinaryKeyData {
    [key: string]: IBinaryData;  // e.g., { data: {...}, attachment: {...} }
}
```

**ALWAYS** include a `json` property on every output item -- it is the only required field. Binary data is ALWAYS secondary.

---

## execute() Return Type

The return type `INodeExecutionData[][]` is a 2D array:
- **Outer array**: One entry per output connector (index 0 = first output, index 1 = second output)
- **Inner array**: Items for that output

```typescript
// Single output (most nodes):
return [returnData];

// Two outputs (like IF node):
return [trueItems, falseItems];

// Three outputs:
return [output1Items, output2Items, output3Items];

// Empty output (no items):
return [[]];
```

---

## Reference Links

- [references/methods.md](references/methods.md) -- INodeType, INodeTypeDescription, INodeProperties (all 22 types), IDisplayOptions, IExecuteFunctions
- [references/examples.md](references/examples.md) -- Complete node implementation, property definitions, displayOptions, declarative node
- [references/anti-patterns.md](references/anti-patterns.md) -- Node type mistakes, property configuration errors

### Official Sources

- https://docs.n8n.io/integrations/creating-nodes/
- https://docs.n8n.io/integrations/creating-nodes/build/reference/node-type-description/
- https://docs.n8n.io/integrations/creating-nodes/build/reference/node-base-files/
- https://github.com/n8n-io/n8n (packages/workflow/src/interfaces.ts)
