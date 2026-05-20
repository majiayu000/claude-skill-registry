---
name: documenting-dbt-models
description: |
  Documents dbt models and columns in schema.yml. Use when working with dbt documentation for:
  (1) Adding model descriptions or column definitions to schema.yml
  (2) Task mentions "document", "describe", "description", "dbt docs", or "schema.yml"
  (3) Explaining business context, grain, meaning of data, or business rules
  (4) Preparing dbt docs generate or improving model discoverability
  Matches existing project documentation style and conventions before writing.
---

# dbt Documentation

**Document the WHY, not just the WHAT. Include grain, business rules, and caveats.**

## Workflow

### 1. Study Existing Documentation Patterns

**CRITICAL: Match the project's documentation style before adding new docs.**

```bash
# Find all schema.yml files with documentation
find . -name "schema.yml" | head -5

# Read well-documented models to learn patterns
cat models/marts/schema.yml | head -150
cat models/staging/schema.yml | head -150
```

**Extract from existing documentation:**
- Description length (brief vs detailed)
- Formatting style (plain text vs markdown with headers)
- Information included (grain? business rules? caveats?)
- Column description depth (all columns vs key columns)
- Use of meta tags or custom properties

### 2. Read Model SQL

```bash
cat models/<path>/<model_name>.sql
```

Understand: transformations, business logic, joins, filters.

### 3. Check Existing Documentation for This Model

```bash
# Find existing schema.yml
find . -name "schema.yml" -exec grep -l "<model_name>" {} \;

# Read existing docs
cat models/<path>/schema.yml | grep -A 100 "<model_name>"
```

### 4. Identify Documentation Needs

For each model, document:
- **Model description**: Purpose, grain, key business rules
- **Column descriptions**: Business meaning, not just data type

For each column, consider:
- What business concept does this represent?
- Are there any caveats or special values?
- What is the source of this data?

### 5. Write Documentation

**Match the style discovered in step 1. Example format (adapt to project):**

```yaml
version: 2

models:
  - name: orders
    description: |
      Order transactions at the order line item grain.
      Each row represents one product in one order.

      **Business Rules:**
      - Revenue recognized on ship_date, not order_date
      - Cancelled orders excluded (status != 'cancelled')
      - Returns processed as negative line items

      **Grain:** One row per order_id + product_id combination

    columns:
      - name: order_id
        description: |
          Unique identifier for the order.
          Source: orders.id from Stripe webhook

      - name: customer_id
        description: |
          Foreign key to customers table.
          NULL for guest checkouts (pre-2023 only)

      - name: revenue
        description: |
          Net revenue for this line item in USD.
          Calculation: unit_price * quantity - discount_amount
          Excludes tax and shipping

      - name: order_status
        description: |
          Current status of the order.
          Values: pending, processing, shipped, delivered, cancelled, returned
```

### 6. Generate Docs

```bash
dbt docs generate
dbt docs serve  # Optional: preview locally
```

## Documentation Patterns

**Note: These are default templates. Always adapt to match project's existing style.**

### Model Description Template

```yaml
description: |
  [One sentence: what this model contains]

  **Grain:** [What does one row represent?]

  **Business Rules:**
  - [Key rule 1]
  - [Key rule 2]

  **Caveats:**
  - [Important limitation or edge case]
```

### Column Description Patterns

| Column Type | Documentation Focus |
|-------------|---------------------|
| Primary key | Source system, uniqueness guarantee |
| Foreign key | What it joins to, NULL handling |
| Metric | Calculation formula, units, exclusions |
| Date | Timezone, what event it represents |
| Status/Category | All possible values, business meaning |
| Boolean/Flag | What true/false means in business terms |

### Documenting Calculated Fields

```yaml
- name: gross_margin
  description: |
    Gross margin percentage.
    Calculation: (revenue - cogs) / revenue * 100
    NULL when revenue = 0 to avoid division by zero
```

## Anti-Patterns

- Adding documentation without checking existing project patterns
- Using different formatting style than existing documentation
- Describing WHAT (e.g., "The order ID") instead of WHY/context
- Missing grain documentation
- Not documenting NULL handling
- Leaving columns undocumented
- Copy-pasting column names as descriptions

