---
name: cube
description: Expert guidance for Cube, the headless BI and semantic layer that sits between your data warehouse and analytics applications. Helps developers define data models, create metrics APIs, and build analytics features in applications with consistent, governed access to business metrics.
license: Apache-2.0
compatibility: No special requirements
metadata:
  author: terminal-skills
  version: 1.0.0
  category: data-ai
  tags:
  - semantic-layer
  - analytics
  - api
  - sql
  - metrics
---

# Cube — Semantic Layer for Analytics


## Overview


Cube, the headless BI and semantic layer that sits between your data warehouse and analytics applications. Helps developers define data models, create metrics APIs, and build analytics features in applications with consistent, governed access to business metrics.


## Instructions

### Data Modeling

Define your business metrics as code:

```javascript
// model/cubes/Orders.js — Orders cube with measures and dimensions
cube(`Orders`, {
  sql_table: `public.orders`,

  // Pre-aggregations for performance (materialized rollups)
  pre_aggregations: {
    daily_revenue: {
      measures: [revenue, count],
      dimensions: [status, product_category],
      time_dimension: created_at,
      granularity: `day`,
      refresh_key: {
        every: `1 hour`,          // Refresh hourly
      },
    },
  },

  joins: {
    Users: {
      relationship: `many_to_one`,
      sql: `${CUBE}.user_id = ${Users}.id`,
    },
    Products: {
      relationship: `many_to_one`,
      sql: `${CUBE}.product_id = ${Products}.id`,
    },
  },

  measures: {
    count: {
      type: `count`,
    },
    revenue: {
      type: `sum`,
      sql: `amount`,
      format: `currency`,
    },
    avg_order_value: {
      type: `avg`,
      sql: `amount`,
      format: `currency`,
    },
    // Derived measure: revenue per user
    revenue_per_user: {
      type: `number`,
      sql: `${revenue} / NULLIF(${Users.count}, 0)`,
      format: `currency`,
    },
    // Rolling window: 7-day moving average
    revenue_7d_avg: {
      type: `avg`,
      sql: `amount`,
      rolling_window: {
        trailing: `7 day`,
      },
    },
  },

  dimensions: {
    id: {
      type: `number`,
      sql: `id`,
      primary_key: true,
    },
    status: {
      type: `string`,
      sql: `status`,
    },
    product_category: {
      type: `string`,
      sql: `${Products}.category`,
    },
    amount: {
      type: `number`,
      sql: `amount`,
    },
    created_at: {
      type: `time`,
      sql: `created_at`,
    },
  },

  // Row-level security
  segments: {
    completed: {
      sql: `${CUBE}.status = 'completed'`,
    },
    high_value: {
      sql: `${CUBE}.amount > 100`,
    },
  },
});
```

```javascript
// model/cubes/Users.js — Users cube
cube(`Users`, {
  sql_table: `public.users`,

  measures: {
    count: {
      type: `count`,
    },
    active_count: {
      type: `count`,
      filters: [{ sql: `${CUBE}.last_login_at > NOW() - INTERVAL '30 days'` }],
    },
    retention_rate: {
      type: `number`,
      sql: `${active_count}::float / NULLIF(${count}, 0) * 100`,
      format: `percent`,
    },
  },

  dimensions: {
    id: {
      type: `number`,
      sql: `id`,
      primary_key: true,
    },
    email: {
      type: `string`,
      sql: `email`,
    },
    plan: {
      type: `string`,
      sql: `plan`,
    },
    created_at: {
      type: `time`,
      sql: `created_at`,
    },
    country: {
      type: `string`,
      sql: `country`,
    },
  },
});
```

### REST API

Query Cube's API from any application:

```typescript
// src/analytics/cube-client.ts — Query the Cube REST API
const CUBE_API_URL = process.env.CUBE_API_URL!;
const CUBE_API_TOKEN = process.env.CUBE_API_TOKEN!;

interface CubeQuery {
  measures?: string[];
  dimensions?: string[];
  timeDimensions?: {
    dimension: string;
    granularity?: string;
    dateRange?: string | string[];
  }[];
  filters?: {
    member: string;
    operator: string;
    values?: string[];
  }[];
  order?: Record<string, "asc" | "desc">;
  limit?: number;
}

async function cubeQuery(query: CubeQuery) {
  const response = await fetch(`${CUBE_API_URL}/v1/load`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${CUBE_API_TOKEN}`,
    },
    body: JSON.stringify({ query }),
  });

  const result = await response.json();
  return result.data;
}

// Example: Get monthly revenue by product category
const monthlyRevenue = await cubeQuery({
  measures: ["Orders.revenue", "Orders.count"],
  dimensions: ["Orders.product_category"],
  timeDimensions: [{
    dimension: "Orders.created_at",
    granularity: "month",
    dateRange: "Last 6 months",
  }],
  order: { "Orders.revenue": "desc" },
  limit: 100,
});

// Example: Retention by plan
const retention = await cubeQuery({
  measures: ["Users.retention_rate", "Users.active_count"],
  dimensions: ["Users.plan"],
  filters: [
    { member: "Users.plan", operator: "equals", values: ["free", "pro", "enterprise"] },
  ],
});
```

### JavaScript SDK (React)

Build analytics UIs with the Cube React SDK:

```tsx
// src/components/RevenueChart.tsx — React component using Cube
import { useCubeQuery } from "@cubejs-client/react";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

export function RevenueChart({ dateRange = "Last 6 months" }) {
  const { resultSet, isLoading, error } = useCubeQuery({
    measures: ["Orders.revenue"],
    timeDimensions: [{
      dimension: "Orders.created_at",
      granularity: "month",
      dateRange,
    }],
  });

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  const data = resultSet?.chartPivot() ?? [];

  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={data}>
        <XAxis dataKey="x" />
        <YAxis />
        <Tooltip formatter={(value: number) => `$${value.toLocaleString()}`} />
        <Line type="monotone" dataKey="Orders.revenue" stroke="#6366f1" strokeWidth={2} />
      </LineChart>
    </ResponsiveContainer>
  );
}
```

### Access Control

Define who can see what data:

```javascript
// cube.js — Security context configuration
module.exports = {
  contextToAppId: ({ securityContext }) => {
    return `CUBE_APP_${securityContext.tenant_id}`;
  },

  // Query rewriting based on user context
  queryRewrite: (query, { securityContext }) => {
    // Multi-tenant: filter all queries by tenant
    if (securityContext.tenant_id) {
      query.filters.push({
        member: "Orders.tenant_id",
        operator: "equals",
        values: [securityContext.tenant_id],
      });
    }

    // Role-based: restrict measures for non-admin users
    if (securityContext.role !== "admin") {
      query.measures = query.measures?.filter(
        (m) => !["Orders.revenue", "Orders.avg_order_value"].includes(m)
      );
    }

    return query;
  },
};
```

## Installation

```bash
# Create a new Cube project
npx cubejs-cli create my-analytics -d postgres

# Or with Docker
docker run -d -p 4000:4000 \
  -e CUBEJS_DB_TYPE=postgres \
  -e CUBEJS_DB_HOST=localhost \
  -e CUBEJS_DB_NAME=mydb \
  cubejs/cube

# Development
npm run dev
# Cube Playground at http://localhost:4000
```


## Examples


### Example 1: Setting up an evaluation pipeline for a RAG application

**User request:**

```
I have a RAG chatbot that answers questions from our docs. Set up Cube to evaluate answer quality.
```

The agent creates an evaluation suite with appropriate metrics (faithfulness, relevance, answer correctness), configures test datasets from real user questions, runs baseline evaluations, and sets up CI integration so evaluations run on every prompt or retrieval change.

### Example 2: Comparing model performance across prompts

**User request:**

```
We're testing GPT-4o vs Claude on our customer support prompts. Set up a comparison with Cube.
```

The agent creates a structured experiment with the existing prompt set, configures both model providers, defines scoring criteria specific to customer support (accuracy, tone, completeness), runs the comparison, and generates a summary report with statistical significance indicators.


## Guidelines

1. **Semantic layer = single source of truth** — Define metrics once in Cube; all apps query the same definitions
2. **Pre-aggregations for performance** — Materialize common queries; Cube auto-selects the best pre-aggregation
3. **Use the Playground for exploration** — Build queries visually in Cube Playground before coding them into your app
4. **Security context for multi-tenancy** — Use `queryRewrite` to automatically filter queries by tenant/user role
5. **Measures over raw SQL** — Define `revenue_per_user` as a Cube measure, not as raw SQL in your app
6. **Time dimensions for trends** — Use `timeDimensions` with `granularity` for consistent time-series queries
7. **Cache aggressively** — Cube caches query results; configure `refresh_key` based on your data update frequency
8. **Version your models** — Cube models are code; store in Git, review changes, deploy via CI/CD
