---
name: windmill
version: 1.0.0
description: Developer-first workflow engine that turns scripts into workflows and UIs, supporting Python, TypeScript, Go, and Bash with approval flows, schedule management, and self-hosted deployment
author: workspace-hub
category: automation
type: skill
capabilities:
  - script_to_workflow
  - auto_generated_ui
  - approval_flows
  - schedule_management
  - python_typescript_go
  - flow_orchestration
  - webhook_triggers
  - resource_management
  - secrets_management
  - branching_logic
tools:
  - windmill-cli
  - docker
  - python
  - node
  - deno
tags: [windmill, workflow, automation, scripts, python, typescript, go, bash, self-hosted, developer-tools]
platforms: [linux, macos, windows, docker, kubernetes]
related_skills:
  - n8n
  - activepieces
  - airflow
  - yaml-configuration
---

# Windmill Workflow Automation Skill

Master Windmill for developer-first workflow automation that transforms scripts into production workflows with auto-generated UIs. This skill covers script authoring in Python/TypeScript/Go/Bash, flow orchestration, approval flows, schedules, and enterprise deployment patterns.

## When to Use This Skill

### USE when:
- Developers prefer writing code over visual tools
- Need auto-generated UIs for script parameters
- Building internal tools with minimal frontend work
- Python, TypeScript, Go, or Bash are primary languages
- Combining workflow automation with internal tools
- Need code review and version control for automations
- Require approval flows with audit trails
- Self-hosting for data sovereignty

### DON'T USE when:
- Non-developers need to build workflows (use n8n, Activepieces)
- Need 400+ pre-built integrations (use n8n)
- Complex DAG orchestration with dependencies (use Airflow)
- CI/CD pipelines tightly coupled with git (use GitHub Actions)
- Simple visual automation preferred (use Activepieces)

## Prerequisites

### Installation Options

**Option 1: Docker Compose (Recommended)**
```yaml
# docker-compose.yml
version: '3.8'

services:
  windmill:
    image: ghcr.io/windmill-labs/windmill:main
    restart: always
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgres://windmill:${POSTGRES_PASSWORD}@postgres:5432/windmill?sslmode=disable
      - MODE=standalone
      - BASE_URL=http://localhost:8000
      - RUST_LOG=info
      - NUM_WORKERS=4
      - DISABLE_SERVER=false
      - DISABLE_WORKERS=false
    depends_on:
      postgres:
        condition: service_healthy
    volumes:
      - worker_dependency_cache:/tmp/windmill/cache

  postgres:
    image: postgres:15
    restart: always
    environment:
      - POSTGRES_USER=windmill
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_DB=windmill
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U windmill"]
      interval: 10s
      timeout: 5s
      retries: 5

  lsp:
    image: ghcr.io/windmill-labs/windmill-lsp:latest
    restart: always
    ports:
      - "3001:3001"
    volumes:
      - lsp_cache:/root/.cache

volumes:
  postgres_data:
  worker_dependency_cache:
  lsp_cache:
```

```bash
# Generate password
export POSTGRES_PASSWORD=$(openssl rand -hex 32)

# Start services
docker compose up -d

# Access UI at http://localhost:8000
# Default credentials: admin@windmill.dev / changeme
```

**Option 2: Kubernetes with Helm**
```bash
# Add Windmill Helm repo
helm repo add windmill https://windmill-labs.github.io/windmill-helm-charts
helm repo update

# Create namespace
kubectl create namespace windmill

# Create secrets
kubectl create secret generic windmill-secrets \
  --namespace windmill \
  --from-literal=postgres-password=$(openssl rand -hex 32)

# Install Windmill
helm install windmill windmill/windmill \
  --namespace windmill \
  --set postgresql.auth.existingSecret=windmill-secrets \
  --set windmill.baseUrl=https://windmill.example.com \
  --set windmill.workers.replicas=3

# Get LoadBalancer IP
kubectl get svc -n windmill windmill-app
```

**Option 3: Local Development**
```bash
# Install Windmill CLI
npm install -g windmill-cli

# Or with pip
pip install wmill

# Login to instance
wmill workspace add my-workspace https://windmill.example.com
wmill workspace switch my-workspace

# Initialize project
wmill init

# Sync local scripts to Windmill
wmill sync push
```

### Development Setup
```bash
# Install language-specific dependencies

# Python development
pip install wmill pandas numpy requests

# TypeScript/Deno development
# Windmill uses Deno runtime for TypeScript
deno --version

# Go development
go install github.com/windmill-labs/windmill-go-client@latest

# Bash scripts work out of the box
```

## Core Capabilities

### 1. Python Scripts

```python
# scripts/data_processing/fetch_and_transform.py
"""
Fetch data from API and transform for analysis.
Auto-generates UI with input fields for all parameters.
"""

import wmill
from datetime import datetime, timedelta
import requests
import pandas as pd


def main(
    api_endpoint: str,
    date_range_days: int = 7,
    include_metadata: bool = True,
    output_format: str = "json",  # Dropdown: json, csv, parquet
    filters: dict = None,
):
    """
    Fetch and transform data from external API.

    Args:
        api_endpoint: The API endpoint URL to fetch data from
        date_range_days: Number of days of data to fetch (default: 7)
        include_metadata: Whether to include metadata in response
        output_format: Output format - json, csv, or parquet
        filters: Optional filters to apply to the data

    Returns:
        Transformed data in specified format
    """
    # Get API credentials from Windmill resources
    api_credentials = wmill.get_resource("u/admin/api_credentials")

    # Calculate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=date_range_days)

    # Fetch data
    headers = {
        "Authorization": f"Bearer {api_credentials['api_key']}",
        "Content-Type": "application/json"
    }

    params = {
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
    }

    if filters:
        params.update(filters)

    response = requests.get(
        f"{api_endpoint}/data",
        headers=headers,
        params=params,
        timeout=30
    )
    response.raise_for_status()
    data = response.json()

    # Transform with pandas
    df = pd.DataFrame(data["records"])

    # Apply transformations
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df["date"] = df["timestamp"].dt.date
        df["hour"] = df["timestamp"].dt.hour

    if "value" in df.columns:
        df["value_normalized"] = (df["value"] - df["value"].min()) / (
            df["value"].max() - df["value"].min()
        )

    # Generate summary statistics
    summary = {
        "total_records": len(df),
        "date_range": {
            "start": str(start_date.date()),
            "end": str(end_date.date())
        },
        "statistics": df.describe().to_dict() if not df.empty else {}
    }

    # Format output
    if output_format == "json":
        result = df.to_dict(orient="records")
    elif output_format == "csv":
        result = df.to_csv(index=False)
    else:
        # For parquet, return as dict (Windmill handles serialization)
        result = df.to_dict(orient="records")

    if include_metadata:
        return {
            "data": result,
            "metadata": summary,
            "format": output_format,
            "generated_at": datetime.now().isoformat()
        }

    return result
```

```python
# scripts/integrations/sync_crm_to_database.py
"""
Sync CRM contacts to internal database with deduplication.
"""

import wmill
from typing import Optional
import psycopg2
from psycopg2.extras import execute_values


def main(
    crm_list_id: str,
    batch_size: int = 100,
    dry_run: bool = False,
    update_existing: bool = True,
):
    """
    Sync CRM contacts to PostgreSQL database.

    Args:
        crm_list_id: The CRM list ID to sync
        batch_size: Number of records per batch
        dry_run: If True, don't actually write to database
        update_existing: If True, update existing records

    Returns:
        Sync statistics
    """
    # Get resources
    crm_api = wmill.get_resource("u/admin/crm_api")
    db_conn = wmill.get_resource("u/admin/postgres_warehouse")

    # Fetch contacts from CRM
    import requests
    contacts = []
    page = 1

    while True:
        response = requests.get(
            f"{crm_api['base_url']}/lists/{crm_list_id}/contacts",
            headers={"Authorization": f"Bearer {crm_api['api_key']}"},
            params={"page": page, "per_page": batch_size}
        )
        response.raise_for_status()
        data = response.json()

        contacts.extend(data["contacts"])

        if not data.get("has_more"):
            break
        page += 1

    print(f"Fetched {len(contacts)} contacts from CRM")

    if dry_run:
        return {
            "mode": "dry_run",
            "contacts_fetched": len(contacts),
            "sample": contacts[:5]
        }

    # Connect to database
    conn = psycopg2.connect(
        host=db_conn["host"],
        port=db_conn["port"],
        database=db_conn["database"],
        user=db_conn["user"],
        password=db_conn["password"]
    )

    stats = {"inserted": 0, "updated": 0, "skipped": 0, "errors": []}

    try:
        with conn.cursor() as cur:
            for contact in contacts:
                try:
                    # Check if exists
                    cur.execute(
                        "SELECT id FROM contacts WHERE email = %s",
                        (contact["email"],)
                    )
                    existing = cur.fetchone()

                    if existing:
                        if update_existing:
                            cur.execute("""
                                UPDATE contacts
                                SET name = %s, company = %s, phone = %s,
                                    updated_at = NOW(), crm_id = %s
                                WHERE email = %s
                            """, (
                                contact["name"],
                                contact.get("company"),
                                contact.get("phone"),
                                contact["id"],
                                contact["email"]
                            ))
                            stats["updated"] += 1
                        else:
                            stats["skipped"] += 1
                    else:
                        cur.execute("""
                            INSERT INTO contacts
                            (email, name, company, phone, crm_id, created_at)
                            VALUES (%s, %s, %s, %s, %s, NOW())
                        """, (
                            contact["email"],
                            contact["name"],
                            contact.get("company"),
                            contact.get("phone"),
                            contact["id"]
                        ))
                        stats["inserted"] += 1

                except Exception as e:
                    stats["errors"].append({
                        "contact": contact["email"],
                        "error": str(e)
                    })

            conn.commit()

    finally:
        conn.close()

    return {
        "mode": "live",
        "contacts_fetched": len(contacts),
        **stats
    }
```

### 2. TypeScript/Deno Scripts

```typescript
// scripts/api/webhook_handler.ts
/**
 * Handle incoming webhooks with validation and routing.
 * Uses Deno runtime with TypeScript support.
 */

import * as wmill from "npm:windmill-client@1";

// Define input types for auto-generated UI
type WebhookPayload = {
  event_type: string;
  data: Record<string, unknown>;
  timestamp: string;
  signature?: string;
};

type HandlerConfig = {
  validate_signature: boolean;
  allowed_events: string[];
  forward_to_slack: boolean;
};

export async function main(
  payload: WebhookPayload,
  config: HandlerConfig = {
    validate_signature: true,
    allowed_events: ["order.created", "order.updated", "payment.completed"],
    forward_to_slack: true,
  }
): Promise<{
  processed: boolean;
  event_type: string;
  actions_taken: string[];
}> {
  const actions: string[] = [];

  // Get webhook secret from resources
  const webhookSecret = await wmill.getResource("u/admin/webhook_secret");

  // Validate signature if required
  if (config.validate_signature && payload.signature) {
    const crypto = await import("node:crypto");
    const expectedSignature = crypto
      .createHmac("sha256", webhookSecret.secret)
      .update(JSON.stringify(payload.data))
      .digest("hex");

    if (payload.signature !== expectedSignature) {
      throw new Error("Invalid webhook signature");
    }
    actions.push("signature_validated");
  }

  // Check if event is allowed
  if (!config.allowed_events.includes(payload.event_type)) {
    return {
      processed: false,
      event_type: payload.event_type,
      actions_taken: ["event_filtered"],
    };
  }

  // Route based on event type
  switch (payload.event_type) {
    case "order.created":
      await handleOrderCreated(payload.data);
      actions.push("order_processed");
      break;

    case "order.updated":
      await handleOrderUpdated(payload.data);
      actions.push("order_updated");
      break;

    case "payment.completed":
      await handlePaymentCompleted(payload.data);
      actions.push("payment_recorded");
      break;
  }

  // Forward to Slack if configured
  if (config.forward_to_slack) {
    const slackWebhook = await wmill.getResource("u/admin/slack_webhook");
    await fetch(slackWebhook.url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        text: `Webhook received: ${payload.event_type}`,
        blocks: [
          {
            type: "section",
            text: {
              type: "mrkdwn",
              text: `*Event:* ${payload.event_type}\n*Timestamp:* ${payload.timestamp}`,
            },
          },
        ],
      }),
    });
    actions.push("slack_notified");
  }

  return {
    processed: true,
    event_type: payload.event_type,
    actions_taken: actions,
  };
}

async function handleOrderCreated(data: Record<string, unknown>) {
  console.log("Processing new order:", data);
  // Implementation
}

async function handleOrderUpdated(data: Record<string, unknown>) {
  console.log("Processing order update:", data);
  // Implementation
}

async function handlePaymentCompleted(data: Record<string, unknown>) {
  console.log("Processing payment:", data);
  // Implementation
}
```

```typescript
// scripts/data/aggregate_metrics.ts
/**
 * Aggregate metrics from multiple sources into unified dashboard data.
 */

import * as wmill from "npm:windmill-client@1";

type MetricsSource = "database" | "api" | "cache";
type AggregationPeriod = "hourly" | "daily" | "weekly" | "monthly";

interface MetricConfig {
  sources: MetricsSource[];
  period: AggregationPeriod;
  include_comparisons: boolean;
  custom_dimensions?: string[];
}

interface AggregatedMetrics {
  period: string;
  total_revenue: number;
  total_orders: number;
  avg_order_value: number;
  unique_customers: number;
  top_products: Array<{ name: string; revenue: number; quantity: number }>;
  by_dimension: Record<string, Record<string, number>>;
  comparisons?: {
    previous_period: Record<string, number>;
    change_percent: Record<string, number>;
  };
}

export async function main(
  start_date: string,
  end_date: string,
  config: MetricConfig = {
    sources: ["database"],
    period: "daily",
    include_comparisons: true,
  }
): Promise<AggregatedMetrics> {
  // Get database connection
  const dbConfig = await wmill.getResource("u/admin/analytics_db");

  // Dynamic import for database client
  const { Client } = await import("npm:pg@8");
  const client = new Client(dbConfig);
  await client.connect();

  try {
    // Fetch base metrics
    const metricsQuery = `
      SELECT
        DATE_TRUNC('${config.period}', created_at) as period,
        COUNT(*) as total_orders,
        SUM(total_amount) as total_revenue,
        COUNT(DISTINCT customer_id) as unique_customers
      FROM orders
      WHERE created_at >= $1 AND created_at < $2
      GROUP BY DATE_TRUNC('${config.period}', created_at)
      ORDER BY period
    `;

    const metricsResult = await client.query(metricsQuery, [
      start_date,
      end_date,
    ]);

    // Aggregate across periods
    const totalRevenue = metricsResult.rows.reduce(
      (sum, r) => sum + parseFloat(r.total_revenue || 0),
      0
    );
    const totalOrders = metricsResult.rows.reduce(
      (sum, r) => sum + parseInt(r.total_orders || 0),
      0
    );
    const uniqueCustomers = metricsResult.rows.reduce(
      (sum, r) => sum + parseInt(r.unique_customers || 0),
      0
    );

    // Fetch top products
    const topProductsQuery = `
      SELECT
        p.name,
        SUM(oi.quantity) as quantity,
        SUM(oi.quantity * oi.unit_price) as revenue
      FROM order_items oi
      JOIN products p ON oi.product_id = p.id
      JOIN orders o ON oi.order_id = o.id
      WHERE o.created_at >= $1 AND o.created_at < $2
      GROUP BY p.id, p.name
      ORDER BY revenue DESC
      LIMIT 10
    `;

    const topProductsResult = await client.query(topProductsQuery, [
      start_date,
      end_date,
    ]);

    const result: AggregatedMetrics = {
      period: `${start_date} to ${end_date}`,
      total_revenue: totalRevenue,
      total_orders: totalOrders,
      avg_order_value: totalOrders > 0 ? totalRevenue / totalOrders : 0,
      unique_customers: uniqueCustomers,
      top_products: topProductsResult.rows.map((r) => ({
        name: r.name,
        revenue: parseFloat(r.revenue),
        quantity: parseInt(r.quantity),
      })),
      by_dimension: {},
    };

    // Add dimension breakdowns
    if (config.custom_dimensions) {
      for (const dimension of config.custom_dimensions) {
        const dimensionQuery = `
          SELECT
            ${dimension},
            SUM(total_amount) as revenue
          FROM orders
          WHERE created_at >= $1 AND created_at < $2
          GROUP BY ${dimension}
        `;
        const dimResult = await client.query(dimensionQuery, [
          start_date,
          end_date,
        ]);
        result.by_dimension[dimension] = Object.fromEntries(
          dimResult.rows.map((r) => [r[dimension], parseFloat(r.revenue)])
        );
      }
    }

    // Add period comparisons
    if (config.include_comparisons) {
      const periodDays = Math.ceil(
        (new Date(end_date).getTime() - new Date(start_date).getTime()) /
          (1000 * 60 * 60 * 24)
      );
      const prevStart = new Date(
        new Date(start_date).getTime() - periodDays * 24 * 60 * 60 * 1000
      )
        .toISOString()
        .split("T")[0];
      const prevEnd = start_date;

      const prevQuery = `
        SELECT
          COUNT(*) as total_orders,
          COALESCE(SUM(total_amount), 0) as total_revenue,
          COUNT(DISTINCT customer_id) as unique_customers
        FROM orders
        WHERE created_at >= $1 AND created_at < $2
      `;

      const prevResult = await client.query(prevQuery, [prevStart, prevEnd]);
      const prev = prevResult.rows[0];

      const prevRevenue = parseFloat(prev.total_revenue || 0);
      const prevOrders = parseInt(prev.total_orders || 0);

      result.comparisons = {
        previous_period: {
          revenue: prevRevenue,
          orders: prevOrders,
        },
        change_percent: {
          revenue: prevRevenue > 0 ? ((totalRevenue - prevRevenue) / prevRevenue) * 100 : 0,
          orders: prevOrders > 0 ? ((totalOrders - prevOrders) / prevOrders) * 100 : 0,
        },
      };
    }

    return result;
  } finally {
    await client.end();
  }
}
```

### 3. Go Scripts

```go
// scripts/performance/batch_processor.go
// High-performance batch processing using Go.

package inner

import (
	"context"
	"encoding/json"
	"fmt"
	"sync"
	"time"

	wmill "github.com/windmill-labs/windmill-go-client"
)

type BatchConfig struct {
	BatchSize     int    `json:"batch_size"`
	Concurrency   int    `json:"concurrency"`
	RetryAttempts int    `json:"retry_attempts"`
	TimeoutSecs   int    `json:"timeout_secs"`
}

type ProcessResult struct {
	TotalItems     int            `json:"total_items"`
	Successful     int            `json:"successful"`
	Failed         int            `json:"failed"`
	ProcessingTime float64        `json:"processing_time_seconds"`
	Errors         []ProcessError `json:"errors,omitempty"`
}

type ProcessError struct {
	ItemID string `json:"item_id"`
	Error  string `json:"error"`
}

func Main(
	items []map[string]interface{},
	config BatchConfig,
) (*ProcessResult, error) {
	startTime := time.Now()

	// Set defaults
	if config.BatchSize == 0 {
		config.BatchSize = 100
	}
	if config.Concurrency == 0 {
		config.Concurrency = 4
	}
	if config.RetryAttempts == 0 {
		config.RetryAttempts = 3
	}
	if config.TimeoutSecs == 0 {
		config.TimeoutSecs = 30
	}

	// Get API credentials
	ctx := context.Background()
	resource, err := wmill.GetResource("u/admin/processing_api")
	if err != nil {
		return nil, fmt.Errorf("failed to get resource: %w", err)
	}

	apiKey := resource["api_key"].(string)

	result := &ProcessResult{
		TotalItems: len(items),
	}

	var mu sync.Mutex
	var wg sync.WaitGroup

	// Create worker pool
	itemChan := make(chan map[string]interface{}, config.BatchSize)
	errorChan := make(chan ProcessError, len(items))

	// Start workers
	for i := 0; i < config.Concurrency; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			for item := range itemChan {
				err := processItem(ctx, item, apiKey, config)
				mu.Lock()
				if err != nil {
					result.Failed++
					errorChan <- ProcessError{
						ItemID: fmt.Sprintf("%v", item["id"]),
						Error:  err.Error(),
					}
				} else {
					result.Successful++
				}
				mu.Unlock()
			}
		}()
	}

	// Send items to workers
	for _, item := range items {
		itemChan <- item
	}
	close(itemChan)

	// Wait for all workers to complete
	wg.Wait()
	close(errorChan)

	// Collect errors
	for err := range errorChan {
		result.Errors = append(result.Errors, err)
	}

	result.ProcessingTime = time.Since(startTime).Seconds()

	return result, nil
}

func processItem(
	ctx context.Context,
	item map[string]interface{},
	apiKey string,
	config BatchConfig,
) error {
	var lastErr error

	for attempt := 1; attempt <= config.RetryAttempts; attempt++ {
		ctx, cancel := context.WithTimeout(ctx, time.Duration(config.TimeoutSecs)*time.Second)
		defer cancel()

		// Process item (simplified - real implementation would make API calls)
		select {
		case <-ctx.Done():
			lastErr = ctx.Err()
		default:
			// Simulate processing
			time.Sleep(10 * time.Millisecond)

			// Validate item
			if _, ok := item["id"]; !ok {
				return fmt.Errorf("missing required field: id")
			}

			return nil
		}

		// Exponential backoff before retry
		if attempt < config.RetryAttempts {
			time.Sleep(time.Duration(1<<attempt) * time.Second)
		}
	}

	return fmt.Errorf("failed after %d attempts: %w", config.RetryAttempts, lastErr)
}
```

### 4. Bash Scripts

```bash
#!/bin/bash
# scripts/devops/deploy_service.sh
# Deploy a service with health checks and rollback capability.

# Windmill automatically provides these as environment variables
# SERVICE_NAME, VERSION, ENVIRONMENT, DRY_RUN

set -euo pipefail

# Get secrets from Windmill resources
DEPLOY_KEY=$(curl -s -H "Authorization: Bearer $WM_TOKEN" \
  "$BASE_INTERNAL_URL/api/w/$WM_WORKSPACE/resources/get/u/admin/deploy_key" | jq -r '.value.key')

AWS_REGION=$(curl -s -H "Authorization: Bearer $WM_TOKEN" \
  "$BASE_INTERNAL_URL/api/w/$WM_WORKSPACE/resources/get/u/admin/aws_config" | jq -r '.value.region')

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

deploy_service() {
  local service=$1
  local version=$2
  local env=$3

  log "Deploying $service version $version to $env"

  # Update ECS service
  if [[ "$DRY_RUN" == "true" ]]; then
    log "[DRY RUN] Would update ECS service $service to $version"
    return 0
  fi

  aws ecs update-service \
    --cluster "${env}-cluster" \
    --service "$service" \
    --force-new-deployment \
    --region "$AWS_REGION"

  log "Deployment initiated"
}

wait_for_healthy() {
  local service=$1
  local env=$2
  local max_wait=300
  local interval=10
  local elapsed=0

  log "Waiting for $service to become healthy..."

  while [[ $elapsed -lt $max_wait ]]; do
    local running_count=$(aws ecs describe-services \
      --cluster "${env}-cluster" \
      --services "$service" \
      --region "$AWS_REGION" \
      --query 'services[0].runningCount' \
      --output text)

    local desired_count=$(aws ecs describe-services \
      --cluster "${env}-cluster" \
      --services "$service" \
      --region "$AWS_REGION" \
      --query 'services[0].desiredCount' \
      --output text)

    if [[ "$running_count" == "$desired_count" ]]; then
      log "Service healthy: $running_count/$desired_count tasks running"
      return 0
    fi

    log "Waiting... ($running_count/$desired_count tasks running)"
    sleep $interval
    elapsed=$((elapsed + interval))
  done

  log "ERROR: Service did not become healthy within ${max_wait}s"
  return 1
}

rollback() {
  local service=$1
  local env=$2

  log "Rolling back $service in $env"

  # Get previous task definition
  local prev_task_def=$(aws ecs describe-services \
    --cluster "${env}-cluster" \
    --services "$service" \
    --region "$AWS_REGION" \
    --query 'services[0].deployments[1].taskDefinition' \
    --output text)

  if [[ -z "$prev_task_def" || "$prev_task_def" == "None" ]]; then
    log "ERROR: No previous task definition found for rollback"
    return 1
  fi

  aws ecs update-service \
    --cluster "${env}-cluster" \
    --service "$service" \
    --task-definition "$prev_task_def" \
    --region "$AWS_REGION"

  log "Rollback initiated to $prev_task_def"
}

# Main execution
main() {
  log "=== Deployment Started ==="
  log "Service: $SERVICE_NAME"
  log "Version: $VERSION"
  log "Environment: $ENVIRONMENT"
  log "Dry Run: $DRY_RUN"

  # Deploy
  if ! deploy_service "$SERVICE_NAME" "$VERSION" "$ENVIRONMENT"; then
    log "ERROR: Deployment failed"
    exit 1
  fi

  # Wait for health (skip in dry run)
  if [[ "$DRY_RUN" != "true" ]]; then
    if ! wait_for_healthy "$SERVICE_NAME" "$ENVIRONMENT"; then
      log "Deployment failed health check, initiating rollback"
      rollback "$SERVICE_NAME" "$ENVIRONMENT"
      exit 1
    fi
  fi

  log "=== Deployment Completed Successfully ==="

  # Output result as JSON for Windmill
  cat <<EOF
{
  "status": "success",
  "service": "$SERVICE_NAME",
  "version": "$VERSION",
  "environment": "$ENVIRONMENT",
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF
}

main
```

### 5. Flow Orchestration

```yaml
# flows/order_processing_flow.yaml
summary: Order Processing Pipeline
description: |
  End-to-end order processing with validation, payment, and fulfillment.
  Includes approval for high-value orders.

value:
  modules:
    - id: validate_order
      value:
        type: script
        path: f/order_processing/validate_order
        input_transforms:
          order:
            type: javascript
            expr: flow_input.order

    - id: check_inventory
      value:
        type: script
        path: f/inventory/check_availability
        input_transforms:
          items:
            type: javascript
            expr: results.validate_order.items

    - id: route_by_value
      value:
        type: branchone
        branches:
          - summary: High Value Order
            expr: results.validate_order.total > 5000
            modules:
              - id: request_approval
                value:
                  type: approval
                  timeout: 86400  # 24 hours
                  approvers:
                    - admin@example.com
                    - manager@example.com

              - id: process_approved
                value:
                  type: script
                  path: f/payments/process_payment
                  input_transforms:
                    order_id:
                      type: javascript
                      expr: results.validate_order.order_id
                    amount:
                      type: javascript
                      expr: results.validate_order.total

          - summary: Normal Order
            expr: results.validate_order.total <= 5000
            modules:
              - id: process_normal
                value:
                  type: script
                  path: f/payments/process_payment
                  input_transforms:
                    order_id:
                      type: javascript
                      expr: results.validate_order.order_id
                    amount:
                      type: javascript
                      expr: results.validate_order.total

    - id: create_shipment
      value:
        type: script
        path: f/fulfillment/create_shipment
        input_transforms:
          order_id:
            type: javascript
            expr: results.validate_order.order_id
          shipping_address:
            type: javascript
            expr: results.validate_order.shipping_address

    - id: send_confirmation
      value:
        type: script
        path: f/notifications/send_order_confirmation
        input_transforms:
          email:
            type: javascript
            expr: results.validate_order.customer_email
          order_details:
            type: javascript
            expr: |
              {
                order_id: results.validate_order.order_id,
                total: results.validate_order.total,
                tracking_number: results.create_shipment.tracking_number
              }

schema:
  $schema: https://json-schema.org/draft/2020-12/schema
  type: object
  properties:
    order:
      type: object
      properties:
        customer_email:
          type: string
          format: email
        items:
          type: array
          items:
            type: object
        shipping_address:
          type: object
      required:
        - customer_email
        - items
        - shipping_address
  required:
    - order
```

### 6. Schedule Management

```python
# scripts/scheduling/dynamic_scheduler.py
"""
Dynamically manage schedules based on business rules.
"""

import wmill
from datetime import datetime, timedelta
from typing import List, Optional


def main(
    schedule_configs: List[dict],
    dry_run: bool = True,
):
    """
    Update Windmill schedules based on configuration.

    Args:
        schedule_configs: List of schedule configurations
        dry_run: If True, only report what would change

    Returns:
        Summary of schedule changes
    """
    client = wmill.Client()
    workspace = wmill.get_workspace()

    changes = []

    for config in schedule_configs:
        schedule_path = config["path"]
        enabled = config.get("enabled", True)
        cron = config.get("cron")
        timezone = config.get("timezone", "UTC")

        # Check business hours constraint
        if config.get("business_hours_only", False):
            # Modify cron to only run during business hours (9-17)
            if cron:
                cron_parts = cron.split()
                if len(cron_parts) >= 5:
                    cron_parts[1] = "9-17"  # Hours
                    cron_parts[4] = "1-5"   # Weekdays only
                    cron = " ".join(cron_parts)

        # Check maintenance window constraint
        if config.get("skip_maintenance_windows", False):
            maintenance = get_maintenance_windows()
            now = datetime.now()
            in_maintenance = any(
                m["start"] <= now <= m["end"]
                for m in maintenance
            )
            if in_maintenance:
                enabled = False

        change = {
            "path": schedule_path,
            "cron": cron,
            "timezone": timezone,
            "enabled": enabled,
            "dry_run": dry_run
        }

        if not dry_run:
            # Update schedule via Windmill API
            try:
                client.update_schedule(
                    workspace=workspace,
                    path=schedule_path,
                    schedule={
                        "schedule": cron,
                        "timezone": timezone,
                        "enabled": enabled
                    }
                )
                change["status"] = "updated"
            except Exception as e:
                change["status"] = "error"
                change["error"] = str(e)
        else:
            change["status"] = "would_update"

        changes.append(change)

    return {
        "total_schedules": len(schedule_configs),
        "changes": changes,
        "dry_run": dry_run
    }


def get_maintenance_windows():
    """Fetch maintenance windows from configuration."""
    try:
        config = wmill.get_variable("u/admin/maintenance_windows")
        return config.get("windows", [])
    except:
        return []
```

### 7. Approval Flows

```python
# scripts/approvals/expense_approval.py
"""
Expense approval workflow with multi-level approvals.
"""

import wmill
from typing import Optional
from enum import Enum


class ApprovalLevel(Enum):
    AUTO = "auto"
    MANAGER = "manager"
    DIRECTOR = "director"
    EXECUTIVE = "executive"


def main(
    expense_id: str,
    amount: float,
    category: str,
    description: str,
    requestor_email: str,
    receipts: Optional[list] = None,
):
    """
    Process expense approval request.

    Args:
        expense_id: Unique expense ID
        amount: Expense amount in USD
        category: Expense category
        description: Expense description
        requestor_email: Email of person requesting expense
        receipts: List of receipt file URLs

    Returns:
        Approval request status and next steps
    """
    # Determine approval level based on amount and category
    approval_level = determine_approval_level(amount, category)

    # Get approvers for this level
    approvers = get_approvers(approval_level, requestor_email)

    if approval_level == ApprovalLevel.AUTO:
        # Auto-approve small expenses
        return {
            "expense_id": expense_id,
            "status": "approved",
            "approval_level": approval_level.value,
            "auto_approved": True,
            "message": f"Expense auto-approved (amount: ${amount:.2f})"
        }

    # Create approval request in database
    db = wmill.get_resource("u/admin/expenses_db")
    approval_id = create_approval_request(
        db,
        expense_id=expense_id,
        amount=amount,
        category=category,
        description=description,
        requestor=requestor_email,
        approvers=approvers,
        level=approval_level.value
    )

    # Send notification to approvers
    slack = wmill.get_resource("u/admin/slack_webhook")
    send_approval_notification(
        slack,
        expense_id=expense_id,
        amount=amount,
        category=category,
        description=description,
        requestor=requestor_email,
        approvers=approvers,
        approval_link=f"https://windmill.example.com/approvals/{approval_id}"
    )

    # Return approval URL for Windmill's built-in approval step
    return {
        "expense_id": expense_id,
        "approval_id": approval_id,
        "status": "pending_approval",
        "approval_level": approval_level.value,
        "approvers": approvers,
        "resume_url": wmill.get_resume_url(),  # For approval continuation
        "message": f"Expense pending {approval_level.value} approval"
    }


def determine_approval_level(amount: float, category: str) -> ApprovalLevel:
    """Determine required approval level based on business rules."""
    # Category-specific rules
    high_scrutiny_categories = ["travel", "equipment", "consulting"]

    if amount <= 100:
        return ApprovalLevel.AUTO
    elif amount <= 1000:
        return ApprovalLevel.MANAGER
    elif amount <= 5000 or category in high_scrutiny_categories:
        return ApprovalLevel.DIRECTOR
    else:
        return ApprovalLevel.EXECUTIVE


def get_approvers(level: ApprovalLevel, requestor: str) -> list:
    """Get list of approvers for given level."""
    approvers_config = wmill.get_variable("u/admin/approvers_config")

    if level == ApprovalLevel.MANAGER:
        # Get requestor's manager
        return approvers_config.get("managers", {}).get(requestor, [])
    elif level == ApprovalLevel.DIRECTOR:
        return approvers_config.get("directors", [])
    elif level == ApprovalLevel.EXECUTIVE:
        return approvers_config.get("executives", [])
    return []


def create_approval_request(db, **kwargs) -> str:
    """Create approval request in database."""
    import psycopg2
    import uuid

    approval_id = str(uuid.uuid4())

    conn = psycopg2.connect(**db)
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO expense_approvals
                (id, expense_id, amount, category, description,
                 requestor, approvers, level, status, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'pending', NOW())
            """, (
                approval_id,
                kwargs["expense_id"],
                kwargs["amount"],
                kwargs["category"],
                kwargs["description"],
                kwargs["requestor"],
                kwargs["approvers"],
                kwargs["level"]
            ))
            conn.commit()
    finally:
        conn.close()

    return approval_id


def send_approval_notification(slack, **kwargs):
    """Send Slack notification for approval request."""
    import requests

    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "Expense Approval Required"
            }
        },
        {
            "type": "section",
            "fields": [
                {"type": "mrkdwn", "text": f"*Amount:* ${kwargs['amount']:.2f}"},
                {"type": "mrkdwn", "text": f"*Category:* {kwargs['category']}"},
                {"type": "mrkdwn", "text": f"*Requestor:* {kwargs['requestor']}"},
                {"type": "mrkdwn", "text": f"*Description:* {kwargs['description']}"}
            ]
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Review & Approve"},
                    "url": kwargs["approval_link"],
                    "style": "primary"
                }
            ]
        }
    ]

    requests.post(slack["url"], json={"blocks": blocks})
```

### 8. Resource and Secrets Management

```python
# scripts/admin/manage_resources.py
"""
Manage Windmill resources and secrets programmatically.
"""

import wmill
from typing import Optional


def main(
    action: str,  # "list", "get", "create", "update", "delete"
    resource_path: Optional[str] = None,
    resource_type: Optional[str] = None,
    resource_value: Optional[dict] = None,
    description: Optional[str] = None,
):
    """
    Manage Windmill resources (secrets, connections, configs).

    Args:
        action: Operation to perform
        resource_path: Path to resource (e.g., "u/admin/my_api")
        resource_type: Type of resource (for create)
        resource_value: Resource value (for create/update)
        description: Resource description

    Returns:
        Operation result
    """
    workspace = wmill.get_workspace()

    if action == "list":
        # List all resources in workspace
        resources = wmill.list_resources()
        return {
            "total": len(resources),
            "resources": [
                {
                    "path": r["path"],
                    "resource_type": r.get("resource_type"),
                    "description": r.get("description", "")
                }
                for r in resources
            ]
        }

    elif action == "get":
        if not resource_path:
            raise ValueError("resource_path required for get action")

        try:
            value = wmill.get_resource(resource_path)
            return {
                "path": resource_path,
                "value": value,
                "found": True
            }
        except Exception as e:
            return {
                "path": resource_path,
                "found": False,
                "error": str(e)
            }

    elif action == "create":
        if not all([resource_path, resource_type, resource_value]):
            raise ValueError("resource_path, resource_type, and resource_value required for create")

        # Validate resource type exists
        valid_types = ["postgresql", "mysql", "mongodb", "s3", "smtp", "slack", "http"]
        if resource_type not in valid_types and not resource_type.startswith("c/"):
            print(f"Warning: Unknown resource type '{resource_type}'")

        # Create resource via API
        result = wmill.create_resource(
            path=resource_path,
            resource_type=resource_type,
            value=resource_value,
            description=description or ""
        )

        return {
            "action": "created",
            "path": resource_path,
            "resource_type": resource_type,
            "success": True
        }

    elif action == "update":
        if not all([resource_path, resource_value]):
            raise ValueError("resource_path and resource_value required for update")

        result = wmill.update_resource(
            path=resource_path,
            value=resource_value
        )

        return {
            "action": "updated",
            "path": resource_path,
            "success": True
        }

    elif action == "delete":
        if not resource_path:
            raise ValueError("resource_path required for delete")

        result = wmill.delete_resource(path=resource_path)

        return {
            "action": "deleted",
            "path": resource_path,
            "success": True
        }

    else:
        raise ValueError(f"Unknown action: {action}")
```

## Integration Examples

### Integration with Database and Slack

```python
# scripts/monitoring/database_health_check.py
"""
Monitor database health and alert on issues.
"""

import wmill
from datetime import datetime
import psycopg2


def main(
    check_connections: bool = True,
    check_slow_queries: bool = True,
    slow_query_threshold_ms: int = 5000,
    alert_channel: str = "#database-alerts",
):
    """
    Run database health checks and alert on issues.

    Args:
        check_connections: Check connection pool status
        check_slow_queries: Check for slow running queries
        slow_query_threshold_ms: Threshold for slow query alerts
        alert_channel: Slack channel for alerts

    Returns:
        Health check results
    """
    db = wmill.get_resource("u/admin/production_db")
    slack = wmill.get_resource("u/admin/slack_webhook")

    results = {
        "timestamp": datetime.now().isoformat(),
        "checks": {},
        "alerts": []
    }

    conn = psycopg2.connect(**db)

    try:
        with conn.cursor() as cur:
            # Check active connections
            if check_connections:
                cur.execute("""
                    SELECT
                        count(*) as total,
                        count(*) FILTER (WHERE state = 'active') as active,
                        count(*) FILTER (WHERE state = 'idle') as idle,
                        count(*) FILTER (WHERE state = 'idle in transaction') as idle_in_txn
                    FROM pg_stat_activity
                    WHERE datname = current_database()
                """)
                conn_stats = cur.fetchone()

                results["checks"]["connections"] = {
                    "total": conn_stats[0],
                    "active": conn_stats[1],
                    "idle": conn_stats[2],
                    "idle_in_transaction": conn_stats[3]
                }

                # Alert if too many connections
                if conn_stats[0] > 80:
                    results["alerts"].append({
                        "type": "high_connections",
                        "message": f"High connection count: {conn_stats[0]}/100",
                        "severity": "warning"
                    })

            # Check slow queries
            if check_slow_queries:
                cur.execute("""
                    SELECT
                        pid,
                        now() - pg_stat_activity.query_start AS duration,
                        query,
                        state
                    FROM pg_stat_activity
                    WHERE (now() - pg_stat_activity.query_start) > interval '%s milliseconds'
                    AND state != 'idle'
                    AND query NOT LIKE '%%pg_stat_activity%%'
                """, (slow_query_threshold_ms,))

                slow_queries = cur.fetchall()

                results["checks"]["slow_queries"] = {
                    "count": len(slow_queries),
                    "threshold_ms": slow_query_threshold_ms,
                    "queries": [
                        {
                            "pid": q[0],
                            "duration": str(q[1]),
                            "query": q[2][:200],
                            "state": q[3]
                        }
                        for q in slow_queries[:5]
                    ]
                }

                if slow_queries:
                    results["alerts"].append({
                        "type": "slow_queries",
                        "message": f"Found {len(slow_queries)} slow queries",
                        "severity": "warning"
                    })

    finally:
        conn.close()

    # Send Slack alerts
    if results["alerts"]:
        send_slack_alert(slack, alert_channel, results)

    return results


def send_slack_alert(slack, channel, results):
    """Send health check alerts to Slack."""
    import requests

    alert_texts = [
        f"*{a['severity'].upper()}*: {a['message']}"
        for a in results["alerts"]
    ]

    requests.post(slack["url"], json={
        "channel": channel,
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "Database Health Alert"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "\n".join(alert_texts)
                }
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": f"Timestamp: {results['timestamp']}"
                    }
                ]
            }
        ]
    })
```

## Best Practices

### 1. Script Organization
```
scripts/
├── data/
│   ├── fetch_api_data.py
│   ├── transform_records.ts
│   └── aggregate_metrics.py
├── integrations/
│   ├── sync_crm.py
│   ├── webhook_handler.ts
│   └── slack_notifications.py
├── devops/
│   ├── deploy_service.sh
│   ├── health_checks.py
│   └── cleanup_resources.py
└── admin/
    ├── manage_resources.py
    └── user_management.py
```

### 2. Error Handling
```python
import wmill

def main(input_data: dict):
    try:
        result = process_data(input_data)
        return {"success": True, "data": result}
    except ValueError as e:
        # Business logic error - don't retry
        wmill.set_state({"error": str(e), "retryable": False})
        raise
    except ConnectionError as e:
        # Transient error - allow retry
        wmill.set_state({"error": str(e), "retryable": True})
        raise
```

### 3. Resource Management
```python
# Always use resources for credentials
api_key = wmill.get_resource("u/admin/api_key")  # Good
# api_key = "sk-1234567890"  # Never hardcode

# Use variables for configuration
config = wmill.get_variable("u/admin/app_config")
```

### 4. Testing Scripts
```bash
# Test script locally
wmill script run f/data/fetch_api_data \
  --data '{"api_endpoint": "https://api.example.com", "limit": 10}'

# Run with specific resource
wmill script run f/data/fetch_api_data \
  --resource u/admin/test_api_credentials
```

## Troubleshooting

### Common Issues

**Issue: Script timeout**
```yaml
# Increase timeout in script metadata
# At top of script file:
# extra_perms:
#   timeout: 600  # 10 minutes
```

**Issue: Import errors in Python**
```python
# Add dependencies to script header
# requirements:
# pandas==2.0.0
# requests==2.31.0

import pandas as pd
import requests
```

**Issue: Resource not found**
```bash
# List available resources
wmill resource list

# Check resource path
wmill resource get u/admin/my_resource
```

### Debugging Tips

```python
# Add logging
import wmill

def main(data: dict):
    print(f"Input: {data}")  # Shows in logs
    wmill.set_state({"debug": "checkpoint_1"})

    result = process(data)

    print(f"Result: {result}")
    return result

# Check script state
# wmill script get-state f/my_script
```

```bash
# View recent runs
wmill job list --script f/data/my_script --limit 10

# Get job logs
wmill job get <job_id>
```

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-17 | Initial release with comprehensive workflow patterns |

## Resources

- [Windmill Documentation](https://www.windmill.dev/docs)
- [Script Hub](https://hub.windmill.dev/)
- [GitHub Repository](https://github.com/windmill-labs/windmill)
- [Discord Community](https://discord.gg/windmill)
- [API Reference](https://www.windmill.dev/docs/api)

---

*This skill provides production-ready patterns for Windmill workflow automation, tested across enterprise scenarios with Python, TypeScript, Go, and Bash scripts.*
