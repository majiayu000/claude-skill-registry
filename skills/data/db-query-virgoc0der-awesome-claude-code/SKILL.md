---
name: db-query
description: This skill enables querying Spanner databases through the AfterShip DSP API. It uses the go-admin-automizely-cli library to obtain authentication tokens and execute SQL queries against Spanner databases in different environments.
---

# Database Query Skill

## Overview
This skill enables querying Spanner databases through the Automizely DBP API. It uses the go-admin-automizely-cli library to obtain authentication tokens and execute SQL queries against Spanner databases in different environments.

**Main Production Instances:**
- `p-connectors-usce1` - Connectors instance
- `aftership-pro-1` - Main AfterShip instance

The script automatically retrieves the database_id by querying the database list API before executing queries.

**Production Databases:**

| Instance | Database | Tables |
| :--- | :--- | :--- |
| `aftership-pro-1` | `af-p-core` | `combinable_orders`, `competitor_migrate_records`, `competitor_synced_orders`, `couriers`, `crons`, `events`, `feature_canary_rules`, `feature_status`, `feed_fulfillment_orders`, `feed_order_items`, `feed_orders`, `feed_returns`, `feeds`, `fulfillment_order_routings`, `hub_orders`, `hub_returns`, `order_actions`, `order_routings`, `reconciliations`, `return_routings`, `settings`, `tasks`, `web_storages` |
| `p-connectors-usce1` | `connectors-p-core` | `action_execution_records`, `amazon_sp_jobs_20250115094545`, `app_connections`, `app_events`, `app_platforms`, `blog_posts`, `blog_tags`, `blogs`, `carrier_services`, `category_rules`, `connection_associations`, `count_stats`, `coupons`, `credentials`, `cron_tasks`, `custom_warehouses`, `discounts`, `discounts_codes`, `error_codes`, `event_notifications`, `events`, `exchange_rates`, `exchange_rates_latest`, `fulfillment_services`, `gdpr_requests`, `gift_cards`, `idempotent_requests`, `image_upload_records`, `kv_config`, `merchant_configs`, `metafield_definitions`, `metafields`, `pages`, `partner_connections`, `partners`, `price_rules`, `product_categories`, `publications`, `sales_channels`, `scheduler_workflow_instances`, `scheduler_workflows`, `scripts`, `sessions`, `state_pipelines`, `storefront_access_tokens`, `stores`, `tasks`, `theme_assets`, `themes`, `unauthorized_tasks`, `warehouses`, `weaver_rules`, `webpixels` |
| `p-connectors-usce1` | `connectors-p-order` | `checkouts`, `draft_orders`, `fulfillment_orders`, `order_cancellations`, `order_fulfillments`, `order_refunds`, `order_restocks`, `order_return_calculations`, `order_tracking_events`, `order_transactions`, `orders`, `orders_items`, `orders_trackings`, `payment_refunds`, `payments`, `returns`, `warehouse_returns` |
| `p-connectors-usce1` | `products-p-listings` | `organization_settings`, `product_listing_audit_versions`, `product_listing_relations`, `product_listings`, `settings` |
| `p-connectors-usce1` | `products-p-core` | `bundled_listing_variant_relations`, `bundled_listings`, `collection_product_relations`, `collections`, `combined_listing_product_relations`, `combined_listings`, `products` |
| `p-connectors-usce1` | `connectors-p-jobs` | `jobs`, `job_groups` |



## When to Use This Skill
Use this skill when Billy needs to:
- Query Spanner database records
- Investigate data issues or verify data states
- Fetch specific records for debugging or analysis
- Profile query performance

## Prerequisites
- Go environment set up
- Access to https://github.com/AfterShip/go-admin-automizely-cli library
- Appropriate permissions to access the databases

## Implementation Steps

### Step 1: Install and Setup
First, install the go-admin-automizely-cli library:

```bash
go get -u github.com/AfterShip/go-admin-automizely-cli
```

### Step 2: Get Token
Create a Go script that uses the client.GetToken method to obtain an authentication token:

```go
package main

import (
	"context"
	"fmt"
	"log"
	
	"github.com/AfterShip/go-admin-automizely-cli/client"
)

func main() {
	// Use "testing" for test environment or "production" for production
	token, err := client.GetToken(context.Background(), "production")
	if err != nil {
		log.Fatalf("Failed to get token: %v", err)
	}
	fmt.Println(token)
}
```

**Environment Options:**
- `"testing"` - For test environment (aftership-test)
- `"production"` - For production environment (aftership-pro)

### Step 2: Get Database ID (if needed)
If you don't know the database_id, first query the database list API to get it:

**API Endpoint:**
```
https://api.automizely.org/dbp/v2/instances/${instance_name}/databases?database_name=${database_name}&db_type=spanner&gcp_project=${gcp_project}&instance=${instance_name}&limit=20&page=1
```

**Common Production Instances:**
- `p-connectors-usce1` - Connectors instance
- `aftership-pro-1` - Main AfterShip instance

**Example Response:**
```json
{
    "meta": {
        "code": 20000,
        "type": "OK",
        "message": "The request was successfully processed by AfterShip."
    },
    "data": {
        "databases": [
            {
                "instance_name": "aftership-pro-1",
                "database_name": "af-p-core",
                "database_id": 170,
                "gcp_project": "aftership-pro",
                "env": "production",
                "product_id": 98,
                "product_name": "AfterShip Feed",
                "backend_owner": "xq.yan@aftership.com",
                "db_type": "spanner",
                "modules": ["Feed Internal", "Automizely Feed"]
            }
        ],
        "pagination": {
            "total": 1,
            "page": 1,
            "next_cursor": null,
            "limit": 20,
            "has_next_page": false
        }
    }
}
```

Extract the `database_id` from `data.databases[0].database_id`.

### Step 3: Execute Query Against DBP API
Once you have the token and database_id, use them to query the database through the API:

**API Endpoint:**
```
https://api.automizely.org/dbp/v2/instances/${instance_name}/databases/${database_id}/query-result
```

**Request Format:**
```json
{
  "db_type": "spanner",
  "gcp_project": "aftership-test",  // or "aftership-pro" for production
  "query": "SELECT * FROM orders WHERE order_id='xxx' LIMIT 10;",
  "query_mode": "profile"
}
```

### Step 4: Complete Go Script
Here's a complete Go script that handles token retrieval, database_id lookup, and database querying:

```go
package main

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	
	"github.com/AfterShip/go-admin-automizely-cli/client"
)

type QueryRequest struct {
	DBType     string `json:"db_type"`
	GCPProject string `json:"gcp_project"`
	Query      string `json:"query"`
	QueryMode  string `json:"query_mode"`
}

type DatabaseInfo struct {
	InstanceName string `json:"instance_name"`
	DatabaseName string `json:"database_name"`
	DatabaseID   int    `json:"database_id"`
	GCPProject   string `json:"gcp_project"`
	Env          string `json:"env"`
}

type DatabaseListResponse struct {
	Meta struct {
		Code    int    `json:"code"`
		Type    string `json:"type"`
		Message string `json:"message"`
	} `json:"meta"`
	Data struct {
		Databases []DatabaseInfo `json:"databases"`
	} `json:"data"`
}

func main() {
	if len(os.Args) < 5 {
		log.Fatal("Usage: go run script.go <instance_name> <database_name> <environment> <sql_query>\n" +
			"  instance_name: p-connectors-usce1, aftership-pro-1, etc.\n" +
			"  database_name: af-p-core, af-p-feed, etc.\n" +
			"  environment: testing or production\n" +
			"  sql_query: SQL query with LIMIT (max 1000)")
	}

	instanceName := os.Args[1]
	databaseName := os.Args[2]
	environment := os.Args[3] // "testing" or "production"
	sqlQuery := os.Args[4]

	// Get authentication token using client.GetToken
	token, err := client.GetToken(context.Background(), environment)
	if err != nil {
		log.Fatalf("Failed to get token: %v", err)
	}

	// Determine GCP project based on environment
	gcpProject := "aftership-test"
	if environment == "production" {
		gcpProject = "aftership-pro"
	}

	// Step 1: Get database_id by querying database list
	databaseID, err := getDatabaseID(token, instanceName, databaseName, gcpProject)
	if err != nil {
		log.Fatalf("Failed to get database ID: %v", err)
	}

	fmt.Printf("Found database_id: %d for %s/%s\n", databaseID, instanceName, databaseName)

	// Step 2: Execute query
	result, err := executeQuery(token, instanceName, databaseID, gcpProject, sqlQuery)
	if err != nil {
		log.Fatalf("Failed to execute query: %v", err)
	}

	fmt.Println("\nQuery Result:")
	fmt.Println(result)
}

func getDatabaseID(token, instanceName, databaseName, gcpProject string) (int, error) {
	url := fmt.Sprintf("https://api.automizely.org/dbp/v2/instances/%s/databases?database_name=%s&db_type=spanner&gcp_project=%s&instance=%s&limit=20&page=1",
		instanceName, databaseName, gcpProject, instanceName)

	req, err := http.NewRequest("GET", url, nil)
	if err != nil {
		return 0, fmt.Errorf("failed to create request: %w", err)
	}

	req.Header.Set("Authorization", fmt.Sprintf("Bearer %s", token))

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		return 0, fmt.Errorf("failed to execute request: %w", err)
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return 0, fmt.Errorf("failed to read response: %w", err)
	}

	if resp.StatusCode != http.StatusOK {
		return 0, fmt.Errorf("API request failed with status %d: %s", resp.StatusCode, string(body))
	}

	var dbResponse DatabaseListResponse
	if err := json.Unmarshal(body, &dbResponse); err != nil {
		return 0, fmt.Errorf("failed to unmarshal response: %w", err)
	}

	if len(dbResponse.Data.Databases) == 0 {
		return 0, fmt.Errorf("no database found with name %s in instance %s", databaseName, instanceName)
	}

	return dbResponse.Data.Databases[0].DatabaseID, nil
}

func executeQuery(token, instanceName string, databaseID int, gcpProject, sqlQuery string) (string, error) {
	// Prepare request
	reqBody := QueryRequest{
		DBType:     "spanner",
		GCPProject: gcpProject,
		Query:      sqlQuery,
		QueryMode:  "profile",
	}

	jsonData, err := json.Marshal(reqBody)
	if err != nil {
		return "", fmt.Errorf("failed to marshal request: %w", err)
	}

	// Make API request
	url := fmt.Sprintf("https://api.automizely.org/dbp/v2/instances/%s/databases/%d/query-result", instanceName, databaseID)
	req, err := http.NewRequest("POST", url, bytes.NewBuffer(jsonData))
	if err != nil {
		return "", fmt.Errorf("failed to create request: %w", err)
	}

	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("Authorization", fmt.Sprintf("Bearer %s", token))

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		return "", fmt.Errorf("failed to execute request: %w", err)
	}
	defer resp.Body.Close()

	// Read response
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return "", fmt.Errorf("failed to read response: %w", err)
	}

	if resp.StatusCode != http.StatusOK {
		return "", fmt.Errorf("API request failed with status %d: %s", resp.StatusCode, string(body))
	}

	return string(body), nil
}
```

## Important Constraints

### Instance and Database Parameters
- **instance_name**: The Spanner instance name (e.g., `p-connectors-usce1`, `aftership-pro-1`)
- **database_name**: The logical database name (e.g., `af-p-core`, `af-p-feed`)
- **database_id**: Automatically retrieved from the database list API
- The script first queries the database list API to get the database_id, then uses it to execute the query
- **DDL**: When you do not know the DDL of a table, write a go script to call API `https://api.automizely.org/dbp/v2/instances/${instance_name}/databases/${database_id}/tables/${table_name}/ddl?db_type=spanner&gcp_project=aftership-pro&mode=Schemas&table_name=${table_name}`. And you can get the ddl from the response. 
response example: 
```json
{
    "meta": {
        "code": 20000,
        "type": "OK",
        "message": "The request was successfully processed by AfterShip."
    },
    "data": "CREATE TABLE job_groups (\n  group_id STRING(32) NOT NULL,\n  namespace STRING(256) NOT NULL,\n  project STRING(256) NOT NULL,\n  name STRING(256) NOT NULL,\n  job_topic_name STRING(256) NOT NULL,\n  notification_topic_name STRING(256),\n  concurrency INT64,\n  retry_config STRING(MAX) NOT NULL,\n  created_at TIMESTAMP NOT NULL OPTIONS (\n    allow_commit_timestamp = true\n  ),\n  updated_at TIMESTAMP NOT NULL OPTIONS (\n    allow_commit_timestamp = true\n  ),\n) PRIMARY KEY(group_id)"
}
```

### Query Requirements
- **LIMIT is MANDATORY**: Every SQL query MUST include a LIMIT clause
- **Maximum LIMIT**: The LIMIT value cannot exceed 1000
- **Query Validation**: Always validate that the query includes LIMIT before execution

Example valid queries:
```sql
SELECT * FROM orders WHERE order_id='xxx' LIMIT 10;
SELECT order_id, status FROM orders WHERE created_at > '2024-01-01' LIMIT 100;
SELECT COUNT(*) as count FROM orders LIMIT 1;
```

### Environment Configuration
- **Test Environment**: Use environment `"testing"` with `gcp_project: "aftership-test"`
- **Production Environment**: Use environment `"production"` with `gcp_project: "aftership-pro"`

### Query Modes
- **profile**: Returns query results with execution statistics and performance metrics
- Use "profile" mode by default for better debugging insights

## Usage Examples

### Example 1: Query Single Order from Feed Database (Production)
```bash
go run query_db.go "aftership-pro-1" "af-p-core" "production" "SELECT * FROM orders WHERE order_id='6f851c942e604330b7165aa2408047d3' LIMIT 10;"
```

### Example 2: Query from Connectors Instance (Production)
```bash
go run query_db.go "p-connectors-usce1" "af-p-connectors" "production" "SELECT order_id, status, created_at FROM orders WHERE created_at > TIMESTAMP('2024-11-01') ORDER BY created_at DESC LIMIT 100;"
```

### Example 3: Count Orders by Status (Test Environment)
```bash
go run query_db.go "aftership-test-1" "af-t-core" "testing" "SELECT status, COUNT(*) as count FROM orders GROUP BY status LIMIT 1000;"
```

### Example 4: Check Inventory Records
```bash
go run query_db.go "aftership-pro-1" "af-p-core" "production" "SELECT * FROM inventory WHERE sku='ABC123' LIMIT 50;"
```

## Error Handling

Common errors and solutions:

1. **Authentication Failed**: Ensure go-admin-automizely-cli is properly configured
2. **Database Not Found**: Verify the instance_name and database_name are correct
3. **Missing LIMIT**: Add LIMIT clause to your SQL query (required)
4. **LIMIT Too Large**: Reduce LIMIT to 1000 or less
5. **Invalid Instance Name**: Use correct instance names (p-connectors-usce1, aftership-pro-1, etc.)
6. **Query Timeout**: Optimize query or reduce LIMIT value
7. **Empty Database List**: Check if the database exists in the specified instance

## Best Practices

1. Always start with a small LIMIT (e.g., 10) for exploratory queries
2. Use specific WHERE clauses to reduce query scope
3. Use indexes when available for better performance
4. Review query execution statistics from profile mode
5. Test queries in test environment before running in production
6. Keep sensitive data secure - don't log tokens or credentials

## Response Format

The API returns JSON with the following structure:
- Query results as an array of records
- Execution statistics (when using profile mode)
- Column metadata
- Row count information

## Notes

- This tool is primarily for Spanner databases but the structure can be adapted for other database types
- Always respect data privacy and security policies when querying production data
- Use appropriate LIMIT values to avoid performance impact on production systems
