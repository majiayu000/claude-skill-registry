---
name: data-quality-planning
description: Define data quality rules, profiling strategies, validation frameworks, and quality metrics.
allowed-tools: Read, Write, Glob, Grep, Task
---

# Data Quality Planning

## When to Use This Skill

Use this skill when:

- **Data Quality Planning tasks** - Working on define data quality rules, profiling strategies, validation frameworks, and quality metrics
- **Planning or design** - Need guidance on Data Quality Planning approaches
- **Best practices** - Want to follow established patterns and standards

## Overview

Data quality planning establishes rules, processes, and metrics to ensure data is fit for its intended purpose. Quality dimensions help categorize and measure data health.

## Data Quality Dimensions

### Six Core Dimensions

| Dimension | Definition | Example Metric |
|-----------|------------|----------------|
| Accuracy | Data correctly represents reality | % records matching source of truth |
| Completeness | All required data is present | % non-null required fields |
| Consistency | Data agrees across systems | % matching cross-system values |
| Timeliness | Data is available when needed | Avg latency from source to target |
| Uniqueness | No duplicate records | % unique on key columns |
| Validity | Data conforms to rules | % records passing validation |

### Quality Dimension Matrix

```markdown
# Quality Assessment: Customer Domain

| Dimension | Weight | Target | Current | Gap |
|-----------|--------|--------|---------|-----|
| Accuracy | 25% | 99% | 97% | -2% |
| Completeness | 25% | 98% | 95% | -3% |
| Consistency | 20% | 99% | 94% | -5% |
| Timeliness | 10% | 99% | 99% | 0% |
| Uniqueness | 15% | 100% | 98% | -2% |
| Validity | 5% | 99% | 96% | -3% |
| **Overall** | 100% | 98.6% | 96.2% | -2.4% |
```

## Data Profiling

### Profiling Types

| Type | Purpose | Output |
|------|---------|--------|
| Column | Understand data distribution | Min, Max, Null %, Distinct count |
| Cross-column | Find relationships | Correlations, functional dependencies |
| Cross-table | Validate referential integrity | Orphan records, FK violations |
| Cross-system | Compare across sources | Discrepancies, sync issues |

### Profiling Template

```markdown
# Column Profile: customers.email

## Statistics
| Metric | Value |
|--------|-------|
| Total Rows | 1,250,000 |
| Distinct Values | 1,180,000 |
| Null Count | 12,500 (1%) |
| Empty String | 2,340 (0.2%) |
| Min Length | 5 |
| Max Length | 254 |
| Avg Length | 24.3 |

## Pattern Analysis
| Pattern | Count | Example |
|---------|-------|---------|
| \w+@\w+\.\w+ | 1,185,000 | user@domain.com |
| NULL | 12,500 | NULL |
| Invalid format | 50,160 | user@domain, @domain.com |

## Value Distribution
| Domain | Count | % |
|--------|-------|---|
| gmail.com | 312,000 | 26% |
| outlook.com | 187,500 | 15% |
| company.com | 125,000 | 10% |
| Other | 612,500 | 49% |

## Issues Found
- 4% invalid email format
- 1% null values (required field)
- 5.6% duplicate emails
```

## Validation Rules

### Rule Categories

| Category | Description | Example |
|----------|-------------|---------|
| Format | Pattern matching | Email regex, phone format |
| Range | Value boundaries | Age 0-120, price > 0 |
| Referential | FK constraints | Order.customer_id exists |
| Business | Domain logic | Discount <= 50% |
| Cross-field | Field relationships | End date >= Start date |
| Aggregate | Group-level | Daily sales > $1000 |

### Rule Definition Template

```markdown
# Validation Rule: VR-CUST-001

## Metadata
- Name: Valid Email Format
- Domain: Customer
- Severity: Error
- Owner: Customer Data Steward

## Rule Definition
- Field: email
- Type: Format
- Pattern: ^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$

## Threshold
- Error: < 99% compliance
- Warning: < 99.5% compliance
- Target: 99.9% compliance

## Remediation
1. Flag invalid emails for review
2. Attempt auto-correction (lowercase, trim)
3. Queue for customer contact if unresolvable
```

### SQL Validation Examples

```sql
-- Completeness check
SELECT
    'email' AS column_name,
    COUNT(*) AS total_rows,
    COUNT(email) AS non_null_rows,
    CAST(COUNT(email) * 100.0 / COUNT(*) AS DECIMAL(5,2)) AS completeness_pct
FROM customers;

-- Uniqueness check
SELECT
    'customer_id' AS column_name,
    COUNT(*) AS total_rows,
    COUNT(DISTINCT customer_id) AS unique_values,
    CAST(COUNT(DISTINCT customer_id) * 100.0 / COUNT(*) AS DECIMAL(5,2)) AS uniqueness_pct
FROM customers;

-- Format validation
SELECT
    COUNT(*) AS total_rows,
    SUM(CASE WHEN email LIKE '%_@_%.__%' THEN 1 ELSE 0 END) AS valid_format,
    SUM(CASE WHEN email NOT LIKE '%_@_%.__%' THEN 1 ELSE 0 END) AS invalid_format
FROM customers;

-- Referential integrity
SELECT
    o.order_id,
    o.customer_id
FROM orders o
LEFT JOIN customers c ON o.customer_id = c.customer_id
WHERE c.customer_id IS NULL;

-- Business rule
SELECT *
FROM orders
WHERE discount_percentage > 50
   OR total_amount < 0
   OR order_date > GETDATE();
```

## C# Validation Framework

```csharp
public interface IValidationRule<T>
{
    string RuleName { get; }
    ValidationSeverity Severity { get; }
    ValidationResult Validate(T entity);
}

public class EmailFormatRule : IValidationRule<Customer>
{
    private static readonly Regex EmailPattern = new(
        @"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
        RegexOptions.Compiled);

    public string RuleName => "VR-CUST-001";
    public ValidationSeverity Severity => ValidationSeverity.Error;

    public ValidationResult Validate(Customer entity)
    {
        if (string.IsNullOrEmpty(entity.Email))
        {
            return ValidationResult.Fail(RuleName, "Email is required");
        }

        if (!EmailPattern.IsMatch(entity.Email))
        {
            return ValidationResult.Fail(RuleName,
                $"Invalid email format: {entity.Email}");
        }

        return ValidationResult.Pass(RuleName);
    }
}

public class DataQualityValidator<T>
{
    private readonly IEnumerable<IValidationRule<T>> _rules;
    private readonly ILogger _logger;

    public async Task<QualityReport> ValidateAsync(
        IEnumerable<T> records,
        CancellationToken ct)
    {
        var report = new QualityReport
        {
            StartTime = DateTime.UtcNow,
            TotalRecords = 0
        };

        var ruleResults = _rules.ToDictionary(
            r => r.RuleName,
            r => new RuleResult { RuleName = r.RuleName });

        foreach (var record in records)
        {
            report.TotalRecords++;

            foreach (var rule in _rules)
            {
                var result = rule.Validate(record);
                var ruleResult = ruleResults[rule.RuleName];

                if (result.IsValid)
                {
                    ruleResult.PassCount++;
                }
                else
                {
                    ruleResult.FailCount++;
                    ruleResult.Failures.Add(result);
                }
            }
        }

        report.RuleResults = ruleResults.Values.ToList();
        report.EndTime = DateTime.UtcNow;
        report.OverallScore = CalculateOverallScore(ruleResults.Values);

        return report;
    }
}
```

## Quality Metrics Dashboard

### KPIs Template

```markdown
# Data Quality Dashboard

## Overall Score
| Domain | Score | Trend | Status |
|--------|-------|-------|--------|
| Customer | 96.2% | ↑ +0.5% | 🟡 Warning |
| Product | 98.5% | ↑ +0.1% | 🟢 Healthy |
| Order | 99.1% | → 0% | 🟢 Healthy |
| Inventory | 94.8% | ↓ -1.2% | 🔴 Critical |

## Rule Compliance
| Rule ID | Rule Name | Target | Actual | Status |
|---------|-----------|--------|--------|--------|
| VR-CUST-001 | Valid Email | 99% | 95.4% | 🔴 |
| VR-CUST-002 | Unique SSN | 100% | 99.9% | 🟢 |
| VR-ORD-001 | Valid Total | 100% | 100% | 🟢 |
| VR-INV-001 | Positive Qty | 100% | 97.2% | 🔴 |

## Trend (Last 30 Days)
| Week | Customer | Product | Order | Inventory |
|------|----------|---------|-------|-----------|
| W1 | 95.7% | 98.4% | 99.1% | 96.0% |
| W2 | 95.9% | 98.5% | 99.1% | 95.5% |
| W3 | 96.0% | 98.5% | 99.1% | 95.0% |
| W4 | 96.2% | 98.5% | 99.1% | 94.8% |
```

## Data Cleansing Patterns

### Cleansing Operations

| Operation | Description | Example |
|-----------|-------------|---------|
| Standardization | Consistent format | "USA" → "United States" |
| Deduplication | Remove duplicates | Merge customer records |
| Enrichment | Add missing data | Append geocodes |
| Correction | Fix known errors | Typo correction |
| Imputation | Fill missing values | Mean/median substitution |

### Cleansing Pipeline

```csharp
public class CustomerCleansingPipeline
{
    public Customer Cleanse(Customer raw)
    {
        var cleansed = new Customer
        {
            CustomerId = raw.CustomerId,

            // Standardization
            Email = raw.Email?.Trim().ToLowerInvariant(),
            Phone = StandardizePhone(raw.Phone),

            // Formatting
            FirstName = ToTitleCase(raw.FirstName?.Trim()),
            LastName = ToTitleCase(raw.LastName?.Trim()),

            // Enrichment
            State = LookupStateFromZip(raw.PostalCode) ?? raw.State,

            // Validation
            PostalCode = ValidatePostalCode(raw.PostalCode)
                ? raw.PostalCode
                : null  // Mark for review
        };

        return cleansed;
    }

    private string StandardizePhone(string phone)
    {
        if (string.IsNullOrEmpty(phone)) return null;

        var digits = new string(phone.Where(char.IsDigit).ToArray());

        return digits.Length switch
        {
            10 => $"+1-{digits[..3]}-{digits[3..6]}-{digits[6..]}",
            11 when digits[0] == '1' => $"+{digits[0]}-{digits[1..4]}-{digits[4..7]}-{digits[7..]}",
            _ => phone  // Return original if non-standard
        };
    }
}
```

## Quality Monitoring

### Alerting Rules

```markdown
# Quality Alert Configuration

## Critical Alerts (Immediate)
| Condition | Action |
|-----------|--------|
| Overall score < 90% | Page on-call, Slack #data-critical |
| Rule failure > 10% | Email data steward, create incident |
| New duplicate rate > 1% | Slack #data-ops |

## Warning Alerts (Daily Digest)
| Condition | Action |
|-----------|--------|
| Score decrease > 2% | Include in daily report |
| Approaching threshold | Email data steward |
| Trend declining 3+ days | Escalate to owner |

## Informational (Weekly Report)
| Condition | Action |
|-----------|--------|
| All scores stable | Include in weekly summary |
| Improvements noted | Celebrate in report |
```

## Validation Checklist

- [ ] Quality dimensions defined and weighted
- [ ] Data profiling completed for critical fields
- [ ] Validation rules documented with thresholds
- [ ] Severity levels assigned to rules
- [ ] Remediation procedures defined
- [ ] Quality metrics and KPIs established
- [ ] Monitoring and alerting configured
- [ ] Cleansing procedures documented
- [ ] Data stewards assigned for remediation

## Integration Points

**Inputs from**:

- `data-governance` skill → Quality standards
- `conceptual-modeling` skill → Business rules
- `er-modeling` skill → Constraints and relationships

**Outputs to**:

- `migration-planning` skill → Validation steps
- ETL/ELT pipelines → Quality gates
- Data catalog → Quality metadata
- Dashboards → Quality metrics
