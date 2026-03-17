---
name: dataverse
description: Expert guidance for Microsoft Dataverse development including Web API (OData), C# plugin development, custom APIs, security model, early-bound types, and FetchXML queries. Use when working with Dataverse tables, writing plugins, building custom APIs, configuring security roles, or querying data via the Web API.
---

# Dataverse Development

Expert guidance for Dataverse Web API, C# plugin development, custom APIs, security model, and data operations.

## Triggers

Use this skill when you see:
- dataverse, common data service, cds
- dataverse web api, odata, fetchxml
- dataverse plugin, iplugin, iorganizationservice
- custom api, dataverse security, security role
- early bound, modelbuilder, dataverse sdk

## Instructions

### Web API (OData) Patterns

```http
# Retrieve records with select and filter
GET [org]/api/data/v9.2/accounts?$select=name,revenue&$filter=revenue gt 1000000&$top=10
Authorization: Bearer {token}
Prefer: odata.include-annotations="*"

# Retrieve with expand (related records)
GET [org]/api/data/v9.2/accounts(00000000-0000-0000-0000-000000000001)?$select=name&$expand=contact_customer_accounts($select=fullname,emailaddress1;$top=5)

# Create a record
POST [org]/api/data/v9.2/accounts
Content-Type: application/json
{
    "name": "Contoso Ltd",
    "revenue": 5000000,
    "primarycontactid@odata.bind": "/contacts(00000000-0000-0000-0000-000000000002)"
}

# Update a record
PATCH [org]/api/data/v9.2/accounts(00000000-0000-0000-0000-000000000001)
Content-Type: application/json
If-Match: *
{
    "name": "Contoso Ltd (Updated)",
    "revenue": 6000000
}

# Delete a record
DELETE [org]/api/data/v9.2/accounts(00000000-0000-0000-0000-000000000001)

# Batch request
POST [org]/api/data/v9.2/$batch
Content-Type: multipart/mixed;boundary=batch_boundary

--batch_boundary
Content-Type: application/http
Content-Transfer-Encoding: binary

GET accounts?$select=name&$top=5 HTTP/1.1
Accept: application/json

--batch_boundary--
```

### FetchXML Queries

```xml
<!-- Aggregation query -->
<fetch aggregate="true">
  <entity name="opportunity">
    <attribute name="estimatedvalue" alias="total_value" aggregate="sum" />
    <attribute name="ownerid" alias="owner" groupby="true" />
    <filter>
      <condition attribute="statecode" operator="eq" value="0" />
      <condition attribute="estimatedclosedate" operator="this-year" />
    </filter>
  </entity>
</fetch>

<!-- Linked entities with outer join -->
<fetch>
  <entity name="account">
    <attribute name="name" />
    <attribute name="revenue" />
    <link-entity name="contact" from="parentcustomerid" to="accountid" link-type="outer" alias="c">
      <attribute name="fullname" />
      <attribute name="emailaddress1" />
    </link-entity>
    <filter>
      <condition attribute="statecode" operator="eq" value="0" />
    </filter>
    <order attribute="name" />
  </entity>
</fetch>
```

### Plugin Development (C#)

```csharp
// Plugin class implementing IPlugin
using Microsoft.Xrm.Sdk;
using Microsoft.Xrm.Sdk.Query;
using System;

namespace Contoso.Plugins
{
    public class AccountPreCreate : IPlugin
    {
        public void Execute(IServiceProvider serviceProvider)
        {
            // Obtain services from the service provider
            var context = (IPluginExecutionContext)serviceProvider.GetService(typeof(IPluginExecutionContext));
            var serviceFactory = (IOrganizationServiceFactory)serviceProvider.GetService(typeof(IOrganizationServiceFactory));
            var service = serviceFactory.CreateOrganizationService(context.UserId);
            var tracingService = (ITracingService)serviceProvider.GetService(typeof(ITracingService));

            try
            {
                // Validate the target entity
                if (context.InputParameters.Contains("Target") &&
                    context.InputParameters["Target"] is Entity target)
                {
                    tracingService.Trace("AccountPreCreate: Processing {0}", target.LogicalName);

                    // Business logic: auto-set account number
                    if (!target.Contains("accountnumber"))
                    {
                        var query = new QueryExpression("account")
                        {
                            ColumnSet = new ColumnSet("accountnumber"),
                            TopCount = 1,
                            Orders = { new OrderExpression("createdon", OrderType.Descending) }
                        };

                        var results = service.RetrieveMultiple(query);
                        var nextNumber = results.Entities.Count > 0
                            ? int.Parse(results.Entities[0].GetAttributeValue<string>("accountnumber") ?? "0") + 1
                            : 1001;

                        target["accountnumber"] = nextNumber.ToString();
                        tracingService.Trace("Set account number to {0}", nextNumber);
                    }
                }
            }
            catch (Exception ex)
            {
                tracingService.Trace("AccountPreCreate Error: {0}", ex.ToString());
                throw new InvalidPluginExecutionException(
                    "An error occurred in the Account Pre-Create plugin.", ex);
            }
        }
    }
}
```

### Plugin Registration

```bash
# Initialize plugin project
pac plugin init

# Project structure:
# MyPlugin/
# ├── MyPlugin.csproj
# ├── Plugin1.cs         # IPlugin implementation
# └── PluginBase.cs      # Optional base class

# Build and register
dotnet build
# Use Plugin Registration Tool or pac CLI to register steps

# Plugin Registration Tool steps:
# 1. Register assembly (DLL)
# 2. Register step (message, entity, stage, mode)
# 3. Register image (pre/post entity images if needed)
```

### Custom APIs

```csharp
// Custom API plugin
namespace Contoso.Plugins
{
    public class CalculateDiscount : IPlugin
    {
        public void Execute(IServiceProvider serviceProvider)
        {
            var context = (IPluginExecutionContext)serviceProvider.GetService(typeof(IPluginExecutionContext));

            // Read request parameters
            var accountId = (string)context.InputParameters["AccountId"];
            var orderTotal = (decimal)context.InputParameters["OrderTotal"];

            // Business logic
            decimal discountRate = orderTotal > 10000 ? 0.15m : 0.05m;
            decimal discountedTotal = orderTotal * (1 - discountRate);

            // Set response parameters
            context.OutputParameters["DiscountRate"] = discountRate;
            context.OutputParameters["DiscountedTotal"] = discountedTotal;
        }
    }
}
```

```http
# Call custom API via Web API
POST [org]/api/data/v9.2/contoso_CalculateDiscount
Content-Type: application/json
{
    "AccountId": "00000000-0000-0000-0000-000000000001",
    "OrderTotal": 15000.00
}
```

### Early-Bound Types

```bash
# Generate early-bound entity classes
pac modelbuilder build

# Configuration in builderSettings.json:
# {
#   "entities": ["account", "contact", "opportunity"],
#   "generateActions": true,
#   "namespaces": { "account": "Contoso.DataModel" }
# }
```

### Security Model

```
Security Layers:
1. Security Roles     - Define table-level CRUD privileges
2. Privilege Depth    - User / Business Unit / Parent-Child BU / Organization
3. Column Security    - Restrict access to specific columns
4. Row-Level Sharing  - Share individual records with users/teams
5. Teams              - Owner teams, Access teams, AAD group teams
6. Field Masking      - Mask sensitive data in columns

Role Privilege Matrix:
┌───────────────┬────────┬──────┬────────┬────────┬────────┐
│ Entity        │ Create │ Read │ Update │ Delete │ Append │
├───────────────┼────────┼──────┼────────┼────────┼────────┤
│ Account       │ BU     │ Org  │ BU     │ User   │ BU     │
│ Contact       │ BU     │ Org  │ BU     │ User   │ BU     │
│ Opportunity   │ User   │ BU   │ User   │ None   │ User   │
└───────────────┴────────┴──────┴────────┴────────┴────────┘
Depth: User < BU < Parent-Child BU < Organization
```

## Best Practices

| Practice | Description |
|----------|-------------|
| **Web API pagination** | Use `@odata.nextLink` for large result sets; default page size is 5000 |
| **Select columns** | Always use `$select` to retrieve only needed columns |
| **Plugin idempotency** | Design plugins to produce the same result if executed multiple times |
| **Tracing** | Use `ITracingService` extensively for debugging in plugin trace logs |
| **Pre vs Post** | Use pre-operation for validation/modification, post-operation for side effects |
| **Async plugins** | Register long-running logic as async to avoid blocking the user |
| **Early-bound** | Use `pac modelbuilder build` for type-safe entity access in plugins |
| **Least privilege** | Grant minimum required security role privileges |

## Common Workflows

### New Plugin Development
1. `pac plugin init` to scaffold project
2. Implement `IPlugin.Execute` with business logic
3. Build and test locally
4. Register assembly with Plugin Registration Tool
5. Register step (message, entity, stage)
6. Test in Dataverse environment
7. Add to solution for ALM

### Web API Integration
1. Register Azure AD app with Dataverse permissions
2. Obtain OAuth 2.0 token (client credentials or auth code)
3. Use `$select`, `$filter`, `$expand` for efficient queries
4. Handle pagination with `@odata.nextLink`
5. Use batch operations for bulk operations
6. Implement retry logic for throttling (429 responses)
