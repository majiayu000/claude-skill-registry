---
name: sonar-graphql
description: |
  Execute GraphQL queries against Sonar ISP API.
  Use when querying customer data, services, billing, invoices, payments, tickets, jobs, or network info from Sonar.
  Supports live mode via fetch_customer_live(). Reference: src/apis/sonar_client.py
---

# Sonar GraphQL API

Execute GraphQL queries against Sonar ISP software.

## Authentication

```python
# Bearer token authentication
headers = {
    "Authorization": f"Bearer {SONAR_API_KEY}",
    "Content-Type": "application/json"
}
```

**Environment variables:**
- `SONAR_URL` - Base URL (e.g., `https://your-sonar.com`)
- `SONAR_API_KEY` - API key for Bearer token auth

**Endpoint:** `{SONAR_URL}/api/graphql`

## Using the Client

```python
from src.apis.sonar_client import SonarGraphQLClient
from src.config.settings import config

client = SonarGraphQLClient(config)

# Test connection
if client.test_connection():
    print("Connected!")

# Execute custom query
response = client.execute_query(query_string, variables={})
if response.success and response.data:
    entities = response.data.get("accounts", {}).get("entities", [])
```

## Query Patterns

### Single Entity by ID
```graphql
query {
    accounts(id: 123) {
        entities {
            id
            name
            account_status_id
        }
    }
}
```

### Paginated List
```graphql
query {
    accounts(paginator: {page: 1, records_per_page: 100}) {
        entities {
            id
            name
        }
        page_info {
            page
            total_pages
            total_count
        }
    }
}
```

### With Filter
```graphql
query {
    accounts(
        account_status_id: 1,
        paginator: {page: 1, records_per_page: 100}
    ) {
        entities { id, name }
    }
}
```

### Nested Relationships
```graphql
query {
    accounts(id: 123) {
        entities {
            id
            name
            contacts {
                entities {
                    id
                    name
                    email_address
                }
            }
            addresses {
                entities {
                    id
                    line1
                    city
                }
            }
        }
    }
}
```

### Polymorphic Union Types
```graphql
query {
    credits(account_id: 123) {
        entities {
            id
            amount
            creditable {
                ... on Payment {
                    description
                    payment_type
                }
                ... on Discount {
                    description
                    type
                }
            }
        }
    }
}
```

### Aliased Batch Query (25 items per request)
```graphql
query GetTaxesBatch {
    d0: tax_transactions(taxtransactionable_id: 100, taxtransactionable_type: Debit) {
        entities { id, amount }
    }
    d1: tax_transactions(taxtransactionable_id: 101, taxtransactionable_type: Debit) {
        entities { id, amount }
    }
    # ... up to d24
}
```

## Common Entities

| Entity | Query | Key Fields |
|--------|-------|------------|
| Customers | `accounts` | id, name, account_status_id, account_type_id |
| Services | `account_services` | id, account_id, service, package |
| Invoices | `invoices` | id, date, due_date, total_debits, remaining_due |
| Payments | `payments` | id, amount, payment_datetime, payment_type, successful |
| Debits | `debits` | id, amount, description, invoice_id, type |
| Credits | `credits` | id, amount, creditable_type, creditable_id |
| Tickets | `tickets` | id, subject, description, priority, status |
| Jobs | `jobs` | id, job_type_id, scheduled_datetime, complete |
| Contacts | `contacts` | id, name, email_address, phone_numbers |
| Addresses | `addresses` | id, line1, city, zip, country |
| IP Assignments | `account_ip_assignments` | account_id, subnet |
| RADIUS | `radius_accounts` | id, username, password, ip_assignments |

## Live Mode Fetch

Fetch complete customer data in one call:

```python
# Returns dict with all customer data: profile, services, billing, tickets, etc.
customer_data = client.fetch_customer_live(customer_id)

# Access nested data
services = customer_data.get("account_services", {}).get("entities", [])
invoices = customer_data.get("invoices", [])
payments = customer_data.get("payments", [])
tickets = customer_data.get("tickets", [])
```

## Pagination Loop

```python
page = 1
all_records = []

while True:
    query = f"""
    query {{
        accounts(paginator: {{page: {page}, records_per_page: 500}}) {{
            entities {{ id, name }}
            page_info {{ total_pages }}
        }}
    }}
    """

    response = client.execute_query(query)
    if not response.success:
        break

    entities = response.data.get("accounts", {}).get("entities", [])
    all_records.extend(entities)

    total_pages = response.data.get("accounts", {}).get("page_info", {}).get("total_pages", 1)
    if page >= total_pages:
        break
    page += 1
```

## Error Handling

```python
response = client.execute_query(query)

if response.success and response.data:
    # Process data
    entities = response.data.get("accounts", {}).get("entities", [])
else:
    # Handle error
    print(f"Error: {response.errors}")
```

## Response Structure

```python
@dataclass
class GraphQLResponse:
    data: Optional[Dict[str, Any]]      # Query result
    errors: Optional[List[Dict]]        # GraphQL errors
    success: bool                        # Overall success
```

## Reference

- Client implementation: `src/apis/sonar_client.py`
- Config: `src/config/settings.py`
- Test: `python -c "from src.apis.sonar_client import SonarGraphQLClient; from src.config.settings import config; print(SonarGraphQLClient(config).test_connection())"`
