---
name: openmetadata-dq
description: Configure and manage data quality tests, profiling, alerts, and incidents in OpenMetadata. Use when setting up quality tests, configuring profiler workflows, creating observability alerts, or triaging data quality incidents.
---

# OpenMetadata Data Quality & Observability

Guide for configuring data quality tests, profiling, alerts, and incident management in OpenMetadata.

## When to Use This Skill

- Creating and managing data quality tests
- Configuring data profiler workflows
- Setting up observability alerts
- Triaging and resolving data incidents
- Exploring lineage for impact analysis
- Running quality tests programmatically

## This Skill Does NOT Cover

- General data discovery and UI navigation (see `openmetadata-user`)
- Using SDKs for non-quality tasks (see `openmetadata-dev`)
- Administering users and policies (see `openmetadata-ops`)
- Contributing quality features to core (see `openmetadata-sdk-dev`)

---

## Data Quality Overview

OpenMetadata provides comprehensive data quality capabilities:

```
┌─────────────────────────────────────────────────────────────┐
│                 Data Quality Framework                       │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   Profiler  │  │   Tests     │  │   Incident Manager  │  │
│  │  (Metrics)  │→ │ (Assertions)│→ │   (Resolution)      │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
│         ↓                ↓                    ↓              │
│  ┌─────────────────────────────────────────────────────────┐│
│  │                 Alerts & Notifications                  ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

---

## Data Profiler

### What the Profiler Does

The profiler captures descriptive statistics to:
- Understand data shape and distribution
- Validate assumptions (nulls, duplicates, ranges)
- Detect anomalies over time
- Power data quality tests

### Profiler Metrics

#### Table-Level Metrics

| Metric | Description |
|--------|-------------|
| **Row Count** | Total rows in table |
| **Column Count** | Number of columns |
| **Size Bytes** | Table size in bytes |
| **Create DateTime** | When table was created |

#### Column-Level Metrics

| Metric | Description |
|--------|-------------|
| **Null Count** | Number of null values |
| **Null Ratio** | Percentage of nulls |
| **Unique Count** | Distinct values |
| **Unique Ratio** | Percentage unique |
| **Duplicate Count** | Non-unique values |
| **Min/Max** | Range for numeric/date |
| **Mean/Median** | Central tendency |
| **Std Dev** | Value distribution spread |
| **Histogram** | Value distribution buckets |

### Configuring Profiler Workflow

#### Via UI

1. Navigate to **Settings → Services → Database Services**
2. Select your database service
3. Click **Ingestion → Add Ingestion**
4. Select **Profiler** as ingestion type
5. Configure:
   - Schedule (cron expression)
   - Sample size percentage
   - Tables to include/exclude
   - Metrics to compute

#### Via YAML

```yaml
source:
  type: profiler
  serviceName: my-database
  sourceConfig:
    config:
      type: Profiler
      generateSampleData: true
      profileSampleType: PERCENTAGE
      profileSample: 50  # Sample 50% of rows
      tableFilterPattern:
        includes:
          - "prod.*"
        excludes:
          - ".*_staging"
      columnFilterPattern:
        includes:
          - ".*"

processor:
  type: orm-profiler
  config: {}

sink:
  type: metadata-rest
  config: {}

workflowConfig:
  openMetadataServerConfig:
    hostPort: http://localhost:8585/api
    authProvider: openmetadata
    securityConfig:
      jwtToken: ${OM_JWT_TOKEN}
```

### Sample Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `profileSampleType` | PERCENTAGE or ROWS | PERCENTAGE |
| `profileSample` | Sample size | 50 |
| `generateSampleData` | Store sample rows | true |
| `sampleDataCount` | Rows to store | 50 |
| `threadCount` | Parallel threads | 5 |
| `timeoutSeconds` | Per-table timeout | 43200 |

### Viewing Profiler Results

1. Navigate to table's **Profiler** tab
2. View **Table Profile**:
   - Row count over time
   - Size trends
3. View **Column Profile**:
   - Null percentages
   - Unique values
   - Distribution histograms

---

## Data Quality Tests

### Test Categories

#### Table-Level Tests

| Test | Description |
|------|-------------|
| **tableRowCountToBeBetween** | Row count within range |
| **tableRowCountToEqual** | Row count equals value |
| **tableColumnCountToBeBetween** | Column count within range |
| **tableColumnCountToEqual** | Column count equals value |
| **tableRowInsertedCountToBeBetween** | New rows within range |
| **tableCustomSQLQuery** | Custom SQL returns expected result |

#### Column-Level Tests

| Test | Description |
|------|-------------|
| **columnValuesToBeNotNull** | No null values |
| **columnValuesToBeUnique** | All values unique |
| **columnValuesToBeBetween** | Values within range |
| **columnValuesToMatchRegex** | Values match pattern |
| **columnValuesToBeInSet** | Values in allowed list |
| **columnValueLengthsToBeBetween** | String lengths in range |
| **columnValuesMissingCount** | Missing values below threshold |
| **columnValueMaxToBeBetween** | Max value in range |
| **columnValueMinToBeBetween** | Min value in range |
| **columnValueMeanToBeBetween** | Mean in range |
| **columnValueMedianToBeBetween** | Median in range |
| **columnValueStdDevToBeBetween** | Std dev in range |
| **columnValuesLengthsToMatch** | Exact string length |

### Creating Tests via UI

1. Navigate to table's **Data Quality** tab
2. Click **+ Add Test**
3. Select test type (Table or Column level)
4. Choose test definition
5. Configure parameters:
   - Column (for column tests)
   - Thresholds/values
   - Description
6. Save test

### Creating Tests via YAML

```yaml
source:
  type: TestSuite
  serviceName: my-database
  sourceConfig:
    config:
      type: TestSuite
      entityFullyQualifiedName: my-database.schema.table

processor:
  type: orm-test-runner
  config:
    testCases:
      - name: orders_row_count_check
        testDefinitionName: tableRowCountToBeBetween
        parameterValues:
          - name: minValue
            value: 1000
          - name: maxValue
            value: 1000000

      - name: customer_id_not_null
        testDefinitionName: columnValuesToBeNotNull
        columnName: customer_id

      - name: status_in_valid_set
        testDefinitionName: columnValuesToBeInSet
        columnName: status
        parameterValues:
          - name: allowedValues
            value: "['pending', 'completed', 'cancelled']"

sink:
  type: metadata-rest
  config: {}

workflowConfig:
  openMetadataServerConfig:
    hostPort: http://localhost:8585/api
    authProvider: openmetadata
    securityConfig:
      jwtToken: ${OM_JWT_TOKEN}
```

### Test Suites

Group related tests into test suites:

```yaml
testSuites:
  - name: orders_table_suite
    description: Quality tests for orders table
    testCases:
      - orders_row_count_check
      - customer_id_not_null
      - status_in_valid_set
```

### Custom SQL Tests

Write custom validation queries:

```yaml
- name: custom_business_rule
  testDefinitionName: tableCustomSQLQuery
  parameterValues:
    - name: sqlExpression
      value: "SELECT COUNT(*) FROM orders WHERE total < 0"
    - name: strategy
      value: "COUNT"
    - name: threshold
      value: 0
```

**Strategy Options:**
- `COUNT` - Result should equal threshold
- `ROWS` - Should return no rows
- `VALUE` - Single value comparison

### Dimensional Testing

Test data quality by business dimensions:

```yaml
- name: quality_by_region
  testDefinitionName: columnValuesToBeBetween
  columnName: revenue
  parameterValues:
    - name: minValue
      value: 0
    - name: partitionColumnName
      value: region
    - name: partitionValues
      value: "['US', 'EU', 'APAC']"
```

---

## Running Tests Programmatically

### Python SDK

```python
from metadata.ingestion.ometa.ometa_api import OpenMetadata
from metadata.generated.schema.tests.testCase import TestCase
from metadata.generated.schema.tests.testDefinition import TestDefinition
from metadata.generated.schema.type.entityReference import EntityReference

# Initialize client
metadata = OpenMetadata(server_config)

# Get test definition
null_test = metadata.get_by_name(
    entity=TestDefinition,
    fqn="columnValuesToBeNotNull",
)

# Create test case
test_case = TestCase(
    name="customer_id_not_null",
    testDefinition=EntityReference(
        id=null_test.id,
        type="testDefinition",
    ),
    entityLink="<#E::table::my-db.schema.orders::columns::customer_id>",
    parameterValues=[],
)

created = metadata.create_or_update(test_case)
print(f"Created test: {created.name}")
```

### Run from ETL Pipeline

```python
from metadata.workflow.data_quality import TestSuiteWorkflow

config = {
    "source": {
        "type": "TestSuite",
        "serviceName": "my-database",
        "sourceConfig": {
            "config": {
                "type": "TestSuite",
                "entityFullyQualifiedName": "my-database.schema.orders"
            }
        }
    },
    # ... rest of config
}

workflow = TestSuiteWorkflow.create(config)
workflow.execute()
workflow.print_status()
```

---

## Alerts and Notifications

### Alert Types

| Trigger | Description |
|---------|-------------|
| **Test Failure** | When data quality test fails |
| **Pipeline Failure** | When ingestion pipeline fails |
| **Schema Change** | When table schema changes |
| **Ownership Change** | When asset owner changes |
| **New Asset** | When new asset is created |

### Creating Alerts

1. Navigate to **Settings → Notifications**
2. Click **+ Add Alert**
3. Configure:
   - Alert name and description
   - Trigger type
   - Filter conditions
   - Notification destinations

### Notification Destinations

| Destination | Setup Required |
|-------------|----------------|
| **Email** | SMTP configuration |
| **Slack** | Webhook URL |
| **Microsoft Teams** | Webhook URL |
| **Webhook** | Custom endpoint URL |

### Alert Filters

Filter which events trigger alerts:

```yaml
filters:
  - field: entityType
    condition: equals
    value: table
  - field: testResult
    condition: equals
    value: Failed
  - field: tier
    condition: in
    values: [Tier1, Tier2]
```

### Slack Integration

```yaml
destinations:
  - type: Slack
    config:
      webhookUrl: https://hooks.slack.com/services/XXX/YYY/ZZZ
      channel: "#data-quality-alerts"
```

---

## Incident Manager

### Incident Lifecycle

```
Test Failure
    ↓
New Incident Created
    ↓
Acknowledged (ack)
    ↓
Assigned to Owner
    ↓
Investigation
    ↓
Root Cause Documented
    ↓
Resolved (with reason)
```

### Incident States

| State | Description |
|-------|-------------|
| **New** | Incident just created |
| **Ack** | Acknowledged, under review |
| **Assigned** | Assigned to specific person/team |
| **Resolved** | Issue fixed, incident closed |

### Managing Incidents

#### Acknowledge

1. Navigate to **Incident Manager**
2. Find new incident
3. Click **Ack** to acknowledge
4. Incident moves to acknowledged state

#### Assign

1. Select acknowledged incident
2. Click **Assign**
3. Search for user or team
4. Add assignment notes
5. Task created for assignee

#### Document Root Cause

1. Open incident details
2. Click **Root Cause**
3. Document:
   - What went wrong
   - Why it happened
   - How it was discovered
4. Save for future reference

#### Resolve

1. Open incident
2. Click **Resolve**
3. Select resolution reason:
   - **Fixed** - Issue corrected
   - **False Positive** - Test was wrong
   - **Duplicate** - Same as another incident
   - **Won't Fix** - Accepted as-is
4. Add resolution comments
5. Confirm resolution

### Resolution Workflow

```
1. Failure Notification → System alerts on test failure
2. Acknowledgment → Team member confirms awareness
3. Assignment → Routes to knowledgeable person
4. Status Updates → Assigned team communicates progress
5. Resolution → All stakeholders notified of fix
```

### Historical Analysis

Past incidents serve as a troubleshooting handbook:
- Review similar scenarios
- Access previous resolutions
- Learn from patterns
- Improve test coverage

---

## Lineage for Impact Analysis

### Lineage in Data Quality Context

Use lineage to understand:
- Which downstream tables are affected by issues
- Which upstream sources might be the root cause
- Impact radius of data quality problems

### Exploring Lineage

1. Navigate to table's **Lineage** tab
2. View upstream sources (data origins)
3. View downstream targets (data consumers)
4. Click nodes for quality status

### Lineage Configuration

| Setting | Range | Purpose |
|---------|-------|---------|
| Upstream Depth | 1-3 | How far back to trace |
| Downstream Depth | 1-3 | How far forward to trace |
| Nodes per Layer | 5-50 | Max nodes displayed |

### Lineage Layers

| Layer | Quality Use Case |
|-------|------------------|
| **Column** | Track field transformations |
| **Observability** | See test results on each node |
| **Service** | Cross-system impact analysis |

### Observability Layer

Enabling the observability layer shows:
- Test pass/fail status on each node
- Failing tests propagate visual indicators
- Quick identification of problem sources

---

## Profiler and Test Scheduling

### Cron Expressions

| Expression | Schedule |
|------------|----------|
| `0 0 * * *` | Daily at midnight |
| `0 */6 * * *` | Every 6 hours |
| `0 0 * * 0` | Weekly on Sunday |
| `0 0 1 * *` | Monthly on 1st |
| `*/30 * * * *` | Every 30 minutes |

### Recommended Schedules

| Workload Type | Profiler | Tests |
|---------------|----------|-------|
| **Batch (Daily)** | Daily after load | Daily after load |
| **Streaming** | Every 6 hours | Every hour |
| **Critical** | Hourly | Every 15 minutes |
| **Archive** | Weekly | Weekly |

### Managing Schedules

1. Navigate to **Settings → Services → [Service]**
2. Go to **Ingestion** tab
3. View/edit scheduled workflows:
   - Metadata ingestion
   - Profiler
   - Test suites

---

## Best Practices

### Test Coverage

1. **Start with critical tables** - Tier1 assets first
2. **Cover basics first**:
   - Null checks on required columns
   - Uniqueness on primary keys
   - Range checks on numeric fields
3. **Add business rules** - Custom SQL for domain logic
4. **Test incrementally** - New rows, not full table

### Profiler Configuration

1. **Sample appropriately** - 10-50% usually sufficient
2. **Exclude large columns** - Skip LOBs and JSON
3. **Schedule off-peak** - Avoid production impact
4. **Timeout appropriately** - Set realistic limits

### Alert Management

1. **Avoid alert fatigue** - Start with critical tests
2. **Route appropriately** - Right team for right issues
3. **Include context** - Link to asset and test details
4. **Set severity levels** - Not all failures are equal

### Incident Response

1. **Acknowledge quickly** - Show awareness
2. **Document thoroughly** - Future you will thank you
3. **Communicate status** - Keep stakeholders informed
4. **Learn from incidents** - Improve tests and processes

---

## Troubleshooting

### Profiler Not Running

| Symptom | Check |
|---------|-------|
| No metrics | Verify ingestion is scheduled |
| Missing columns | Check column filter patterns |
| Slow execution | Reduce sample size |
| Timeouts | Increase timeout or reduce scope |

### Tests Failing Unexpectedly

| Symptom | Check |
|---------|-------|
| False positives | Review test thresholds |
| Intermittent failures | Check for race conditions |
| All tests failing | Verify database connectivity |
| No test results | Check test suite is scheduled |

### Alerts Not Sending

| Symptom | Check |
|---------|-------|
| No emails | Verify SMTP configuration |
| No Slack messages | Check webhook URL |
| Wrong recipients | Review alert filters |
| Too many alerts | Tighten filter conditions |

---

## Integration with CI/CD

### GitHub Actions Example

```yaml
name: Data Quality Check
on:
  schedule:
    - cron: '0 6 * * *'
  workflow_dispatch:

jobs:
  quality-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: pip install openmetadata-ingestion

      - name: Run quality tests
        env:
          OM_HOST: ${{ secrets.OM_HOST }}
          OM_TOKEN: ${{ secrets.OM_TOKEN }}
        run: |
          metadata_openmetadata test-suite run \
            --config quality-tests.yaml

      - name: Check results
        run: |
          # Fail pipeline if critical tests failed
          metadata_openmetadata test-suite status \
            --suite critical-tests \
            --fail-on-failure
```

---

## References

- [Data Quality Guide](https://docs.open-metadata.org/latest/how-to-guides/data-quality-observability)
- [Profiler Configuration](https://docs.open-metadata.org/latest/how-to-guides/data-quality-observability/profiler)
- [Test Definitions](https://docs.open-metadata.org/latest/how-to-guides/data-quality-observability/quality)
- [Incident Manager](https://docs.open-metadata.org/latest/how-to-guides/data-quality-observability/incident-manager)
- [Data Lineage](https://docs.open-metadata.org/latest/how-to-guides/data-lineage)
- `openmetadata-dev` - SDK for programmatic quality tests
- `openmetadata-user` - UI navigation and discovery
- `openmetadata-ops` - Platform administration
