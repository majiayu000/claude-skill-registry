---
name: power-automate
description: Expert guidance for Power Automate development including cloud flows, desktop flows, Dataverse connector, expression functions, custom connectors, error handling, and child flow patterns. Use when building automated workflows, writing flow expressions, creating custom connectors from OpenAPI, or implementing error handling patterns.
---

# Power Automate Development

Expert guidance for cloud flows, desktop flows, expressions, custom connectors, and error handling patterns.

## Triggers

Use this skill when you see:
- power automate, cloud flow, desktop flow
- flow expression, trigger outputs, compose action
- custom connector, openapi connector
- dataverse connector, flow trigger
- child flow, environment variable, connection reference
- run after, scope try catch, error handling flow

## Instructions

### Flow Types

| Type | Description | Use Case |
|------|-------------|----------|
| **Automated** | Triggered by an event | Dataverse row created, email received |
| **Instant** | Triggered manually | Button press, Power Apps call |
| **Scheduled** | Runs on a schedule | Daily report, hourly sync |
| **Desktop** | RPA for desktop apps | Legacy app automation, file processing |

### Dataverse Connector Actions

```
Trigger: "When a row is added, modified or deleted"
- Change type: Added / Modified / Deleted / Added or Modified
- Table name: Accounts, Contacts, etc.
- Scope: User / Business Unit / Parent-Child BU / Organization
- Filter rows: statecode eq 0
- Select columns: name,revenue,accountid

Actions:
- List rows:
  Table name: Accounts
  Filter rows: revenue gt 1000000 and statecode eq 0
  Select columns: name,revenue,primarycontactid
  Order by: revenue desc
  Row count: 50

- Get a row by ID:
  Table name: Accounts
  Row ID: triggerOutputs()?['body/accountid']
  Select columns: name,revenue

- Add a new row:
  Table name: Tasks
  Body: { "subject": "Follow up", "regardingobjectid_account@odata.bind": "/accounts(ID)" }

- Update a row:
  Table name: Accounts
  Row ID: triggerOutputs()?['body/accountid']
  Body: { "revenue": 5000000 }

- Delete a row:
  Table name: Accounts
  Row ID: triggerOutputs()?['body/accountid']
```

### Expression Functions

```
// Trigger and action outputs
triggerOutputs()?['body/accountid']
triggerBody()?['name']
outputs('Get_Account')?['body/revenue']
body('HTTP_Request')?['value']
items('Apply_to_each')?['name']

// String functions
concat('Hello, ', triggerBody()?['name'])
substring('Hello World', 0, 5)                    // "Hello"
replace(triggerBody()?['description'], '\n', ' ')
toLower(triggerBody()?['email'])
split('a,b,c', ',')                               // ["a","b","c"]
trim(triggerBody()?['name'])

// Date/time functions
utcNow()
addDays(utcNow(), 7)
formatDateTime(utcNow(), 'yyyy-MM-dd')
convertTimeZone(utcNow(), 'UTC', 'Eastern Standard Time')
ticks(utcNow())

// Conditional and null handling
if(equals(triggerBody()?['status'], 'Active'), 'Yes', 'No')
coalesce(triggerBody()?['phone'], triggerBody()?['mobile'], 'No phone')
if(empty(triggerBody()?['email']), 'No email', triggerBody()?['email'])

// Collection functions
length(body('List_rows')?['value'])
first(body('List_rows')?['value'])
last(body('List_rows')?['value'])
union(variables('arrayA'), variables('arrayB'))
intersection(variables('arrayA'), variables('arrayB'))

// Type conversion
int(triggerBody()?['quantity'])
float(triggerBody()?['price'])
string(triggerBody()?['accountid'])
json(body('HTTP_Request'))
base64(body('Get_File_Content'))

// Variables
variables('myVariable')
// Set via "Initialize variable" and "Set variable" actions
```

### Custom Connectors from OpenAPI

```yaml
# OpenAPI spec for custom connector
openapi: 3.0.0
info:
  title: Contoso API
  version: 1.0.0
servers:
  - url: https://api.contoso.com/v1
paths:
  /orders/{orderId}:
    get:
      operationId: GetOrder
      summary: Get order by ID
      parameters:
        - name: orderId
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Order details
          content:
            application/json:
              schema:
                type: object
                properties:
                  id:
                    type: string
                  status:
                    type: string
                  total:
                    type: number
  /orders:
    post:
      operationId: CreateOrder
      summary: Create new order
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                customerId:
                  type: string
                items:
                  type: array
                  items:
                    type: object
                    properties:
                      productId:
                        type: string
                      quantity:
                        type: integer
      responses:
        '201':
          description: Order created
```

```bash
# Create custom connector from OpenAPI
pac connector create --api-definition ./openapi.yaml --environment "https://myorg.crm.dynamics.com"

# Or import via Power Platform maker portal:
# Data > Custom Connectors > New > Import from OpenAPI file
```

### Error Handling Patterns

#### Configure Run After

```
Action: "Send notification email"
Configure run after:
  ✓ Is successful
  ✗ Has failed        → Route to error handler
  ✗ Is skipped
  ✗ Has timed out     → Route to error handler
```

#### Scope Try/Catch Pattern

```
Flow Structure:
├── Scope: Try
│   ├── Action 1: Get data from API
│   ├── Action 2: Process data
│   └── Action 3: Update Dataverse
│
├── Scope: Catch (Configure run after: "Try" has failed)
│   ├── Compose: Error Details
│   │   Expression: result('Try')
│   ├── Action: Log error to table
│   │   Body: {
│   │     "error": outputs('Compose_Error_Details'),
│   │     "flowRunId": workflow()?['run']?['name'],
│   │     "timestamp": utcNow()
│   │   }
│   └── Action: Send alert email
│
└── Scope: Finally (Configure run after: "Catch" is successful OR skipped)
    └── Action: Cleanup / audit log
```

### Child Flows Pattern

```
Parent Flow:
├── Initialize variable: Results (Array)
├── Apply to each: Items
│   └── Run a Child Flow: "Process Single Item"
│       Input: Current item
│       Output: Processing result
│       → Append result to Results array
├── Compose: Summary of results
└── Send notification with summary

Child Flow (separate flow):
├── Trigger: "Manually trigger a flow" (with input parameters)
├── Process item logic
├── Error handling (Scope try/catch)
└── Respond to a PowerApp or flow (output parameters)
```

### Environment Variables and Connection References

```
Environment Variables:
- Use for: API URLs, feature flags, email addresses, lookup IDs
- Types: String, Number, Boolean, JSON, Data Source
- Stored in Dataverse solution; values differ per environment
- Access in flow: Look up environment variable value dynamically

Connection References:
- Abstract connections from flows for ALM portability
- Each reference maps to a concrete connection per environment
- Created automatically when you add connectors to a solution
- Configure target connections during solution import
```

## Best Practices

| Practice | Description |
|----------|-------------|
| **Error handling** | Always use Scope try/catch pattern for critical flows |
| **Pagination** | Use "List rows" with pagination settings for large datasets |
| **Concurrency** | Set Apply to each concurrency (1-50) based on API limits |
| **Child flows** | Break complex flows into reusable child flows |
| **Environment variables** | Store environment-specific config, not hardcoded values |
| **Connection references** | Use solution connection references for portability |
| **Expression readability** | Use Compose actions to name intermediate expressions |
| **Run history** | Add tracked properties to actions for debugging |
| **Throttling** | Implement retry policies for HTTP actions (429/503) |
| **Naming** | Prefix actions descriptively: "Get_Account_Details" not "Get_a_row" |

## Common Workflows

### Dataverse Event Processing
1. Trigger on Dataverse row change (filter to specific columns)
2. Get related records if needed
3. Apply business logic with conditions
4. Update records or send notifications
5. Handle errors with Scope try/catch

### API Integration Flow
1. Trigger (scheduled or event-based)
2. Authenticate to external API (HTTP action with OAuth)
3. Retrieve data with pagination loop
4. Transform data with Compose/Select actions
5. Upsert to Dataverse
6. Log results and handle errors

### Custom Connector Development
1. Author or obtain OpenAPI spec
2. Import via maker portal or `pac connector create`
3. Configure authentication (API key, OAuth 2.0, etc.)
4. Test actions in connector test pane
5. Use in flows and canvas apps
6. Add to solution for ALM
