---
name: retool
description: >-
  Build internal tools with Retool, the low-code platform. Use when a user asks to create admin panels, connect to databases or APIs, build CRUD interfaces with drag-and-drop components, or deploy Retool apps.
license: Apache-2.0
compatibility: "No special requirements"
metadata:
  author: terminal-skills
  version: "1.0.0"
  category: development
  tags: ["internal-tools", "low-code", "admin-panel", "dashboard", "crud"]
---
# Retool — Build Internal Tools Fast

## Overview

You are an expert in Retool, the low-code platform for building internal tools, admin panels, and dashboards. You help developers connect to databases and APIs, build CRUD interfaces with drag-and-drop components, write custom JavaScript for business logic, and deploy tools that would take weeks to code from scratch.

## Instructions

### Connect Data Sources

```javascript
// Retool connects to databases, APIs, and services natively:
// - PostgreSQL, MySQL, MongoDB, Redis, BigQuery, Snowflake
// - REST API, GraphQL, gRPC
// - Stripe, Twilio, SendGrid, Slack, Google Sheets
// - S3, Firebase, Supabase

// SQL Query (runs server-side, results available as {{ query1.data }})
SELECT
  u.id, u.email, u.name, u.plan, u.created_at,
  COUNT(o.id) as order_count,
  SUM(o.amount) as total_spent
FROM users u
LEFT JOIN orders o ON o.user_id = u.id
WHERE u.plan = {{ planFilter.value }}
  AND u.created_at >= {{ dateRange.start }}
GROUP BY u.id
ORDER BY total_spent DESC
LIMIT {{ pagination.pageSize }}
OFFSET {{ pagination.offset }}

// REST API query
// Method: POST
// URL: https://api.stripe.com/v1/refunds
// Headers: Authorization: Bearer {{ STRIPE_KEY }}
// Body: { "charge": {{ table1.selectedRow.stripe_charge_id }}, "amount": {{ refundAmount.value * 100 }} }
```

### Components and Bindings

```javascript
// Table component displays query results
// Columns auto-detect from query. Customize:
table1.columns = [
  { key: "email", label: "Email", type: "link" },
  { key: "plan", label: "Plan", type: "tag",
    colors: { free: "gray", pro: "blue", enterprise: "purple" } },
  { key: "total_spent", label: "Revenue", type: "currency" },
  { key: "created_at", label: "Joined", type: "date" },
];

// Button click handler (JavaScript)
// Runs when "Process Refund" button is clicked
async function handleRefund() {
  const row = table1.selectedRow;
  if (!row) return utils.showNotification({ title: "Select a row first" });

  const confirmed = await utils.openConfirmDialog({
    title: "Process Refund",
    body: `Refund $${refundAmount.value} to ${row.email}?`,
  });
  if (!confirmed) return;

  await refundQuery.trigger();  // Runs the Stripe API query

  if (refundQuery.error) {
    utils.showNotification({ title: "Refund Failed", description: refundQuery.error });
  } else {
    utils.showNotification({ title: "Refund Processed", type: "success" });
    await usersQuery.trigger();  // Refresh the table
  }
}

// Conditional visibility
// Show refund panel only for paid users
refundPanel.hidden = {{ table1.selectedRow?.plan === 'free' }}

// Dynamic form validation
submitButton.disabled = {{
  !emailInput.value ||
  !emailInput.value.includes('@') ||
  amountInput.value <= 0
}}
```

### Custom Components

```javascript
// Retool supports custom React components for advanced use cases
const CustomChart = ({ data, height }) => {
  return (
    <ResponsiveContainer width="100%" height={height}>
      <BarChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="month" />
        <YAxis />
        <Tooltip />
        <Bar dataKey="revenue" fill="#4f46e5" />
        <Bar dataKey="costs" fill="#ef4444" />
      </BarChart>
    </ResponsiveContainer>
  );
};
```

### Workflows (Backend Automation)

```javascript
// Retool Workflows — serverless backend logic
// Trigger: webhook, schedule, or manual

// Step 1: Query database for expiring trials
const expiringTrials = await query("SELECT * FROM users WHERE trial_ends_at < NOW() + INTERVAL '3 days' AND plan = 'trial'");

// Step 2: For each user, send reminder email
for (const user of expiringTrials) {
  await sendgrid.send({
    to: user.email,
    template_id: "trial-expiring",
    data: { name: user.name, days_left: daysUntil(user.trial_ends_at) },
  });
}

// Step 3: Log results
await query("INSERT INTO email_logs (type, count, sent_at) VALUES ('trial_expiring', $1, NOW())", [expiringTrials.length]);

return { sent: expiringTrials.length };
```

## Examples

**Example 1: User asks to set up retool**

User: "Help me set up retool for my project"

The agent should:
1. Check system requirements and prerequisites
2. Install or configure retool
3. Set up initial project structure
4. Verify the setup works correctly

**Example 2: User asks to build a feature with retool**

User: "Create a dashboard using retool"

The agent should:
1. Scaffold the component or configuration
2. Connect to the appropriate data source
3. Implement the requested feature
4. Test and validate the output

## Guidelines

1. **Start with the query** — Write the SQL/API query first, then build the UI around the data; Retool auto-generates table columns
2. **Use transformers** — Process query results with JavaScript transformers instead of complex SQL; easier to debug and maintain
3. **Staged actions** — For destructive operations (delete, refund), use confirmation dialogs and audit logging
4. **Row-level permissions** — Use Retool's permission groups to control who can view/edit/delete; don't rely on hiding buttons
5. **Version control** — Use Retool's built-in git sync to version your apps; review changes in PRs
6. **Reusable modules** — Extract common patterns (user lookup, audit log) into Retool modules; share across apps
7. **Workflows for automation** — Use Retool Workflows for scheduled tasks and webhooks; keep app-level logic in the UI
8. **Self-hosted for sensitive data** — Retool offers self-hosted deployment; use it when data can't leave your infrastructure
