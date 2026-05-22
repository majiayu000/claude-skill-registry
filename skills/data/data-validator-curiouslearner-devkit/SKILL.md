---
name: data-validator
description: Validate data against schemas, business rules, and data quality standards.
---

# Data Validator Skill

Validate data against schemas, business rules, and data quality standards.

## Instructions

You are a data validation expert. When invoked:

1. **Schema Validation**:
   - Validate against JSON Schema
   - Check database schema compliance
   - Validate API request/response formats
   - Ensure data type correctness
   - Verify required fields

2. **Business Rules Validation**:
   - Apply domain-specific rules
   - Validate data ranges and constraints
   - Check referential integrity
   - Verify business logic constraints
   - Validate calculated fields

3. **Data Quality Checks**:
   - Check for completeness
   - Detect duplicates
   - Identify outliers and anomalies
   - Validate format patterns (email, phone, etc.)
   - Check data consistency

4. **Generate Validation Reports**:
   - Detailed error messages
   - Validation statistics
   - Data quality scores
   - Fix suggestions
   - Compliance summaries

## Usage Examples

```
@data-validator data.json --schema schema.json
@data-validator --check-duplicates
@data-validator --rules business-rules.yaml
@data-validator --quality-report
@data-validator --fix-errors
```

## Schema Validation

### JSON Schema Validation

#### Python (jsonschema)
```python
from jsonschema import validate, ValidationError, Draft7Validator
import json

def validate_json_schema(data, schema):
    """
    Validate data against JSON Schema
    """
    try:
        validate(instance=data, schema=schema)
        return {
            'valid': True,
            'errors': []
        }
    except ValidationError as e:
        return {
            'valid': False,
            'errors': [{
                'path': list(e.path),
                'message': e.message,
                'validator': e.validator,
                'validator_value': e.validator_value
            }]
        }

def validate_with_detailed_errors(data, schema):
    """
    Validate and collect all errors
    """
    validator = Draft7Validator(schema)
    errors = []

    for error in validator.iter_errors(data):
        errors.append({
            'path': '.'.join(str(p) for p in error.path),
            'message': error.message,
            'validator': error.validator,
            'failed_value': error.instance
        })

    return {
        'valid': len(errors) == 0,
        'errors': errors,
        'error_count': len(errors)
    }

# Example schema
user_schema = {
    "type": "object",
    "properties": {
        "id": {
            "type": "integer",
            "minimum": 1
        },
        "email": {
            "type": "string",
            "format": "email",
            "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
        },
        "age": {
            "type": "integer",
            "minimum": 0,
            "maximum": 150
        },
        "phone": {
            "type": "string",
            "pattern": "^\\+?[1-9]\\d{1,14}$"
        },
        "status": {
            "type": "string",
            "enum": ["active", "inactive", "suspended"]
        },
        "created_at": {
            "type": "string",
            "format": "date-time"
        },
        "tags": {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 1,
            "uniqueItems": True
        },
        "address": {
            "type": "object",
            "properties": {
                "street": {"type": "string"},
                "city": {"type": "string"},
                "zip": {"type": "string", "pattern": "^\\d{5}(-\\d{4})?$"}
            },
            "required": ["street", "city"]
        }
    },
    "required": ["id", "email", "status"],
    "additionalProperties": False
}

# Validate data
user_data = {
    "id": 1,
    "email": "user@example.com",
    "age": 30,
    "status": "active",
    "tags": ["developer", "admin"]
}

result = validate_with_detailed_errors(user_data, user_schema)

if result['valid']:
    print("✅ Data is valid")
else:
    print(f"❌ Found {result['error_count']} errors:")
    for error in result['errors']:
        print(f"  - {error['path']}: {error['message']}")
```

#### JavaScript (AJV)
```javascript
const Ajv = require('ajv');
const addFormats = require('ajv-formats');

const ajv = new Ajv({ allErrors: true });
addFormats(ajv);

const schema = {
  type: 'object',
  properties: {
    id: { type: 'integer', minimum: 1 },
    email: { type: 'string', format: 'email' },
    age: { type: 'integer', minimum: 0, maximum: 150 },
    status: { type: 'string', enum: ['active', 'inactive', 'suspended'] }
  },
  required: ['id', 'email', 'status'],
  additionalProperties: false
};

function validateData(data) {
  const validate = ajv.compile(schema);
  const valid = validate(data);

  return {
    valid,
    errors: validate.errors || []
  };
}

// Usage
const userData = {
  id: 1,
  email: 'user@example.com',
  status: 'active'
};

const result = validateData(userData);
console.log(result);
```

### Database Schema Validation

```python
import pandas as pd
from sqlalchemy import inspect

def validate_dataframe_schema(df, expected_schema):
    """
    Validate DataFrame against expected schema

    expected_schema = {
        'column_name': {
            'type': 'int64',
            'nullable': False,
            'unique': False,
            'min': 0,
            'max': 100
        }
    }
    """
    errors = []

    # Check columns exist
    expected_columns = set(expected_schema.keys())
    actual_columns = set(df.columns)

    missing_columns = expected_columns - actual_columns
    extra_columns = actual_columns - expected_columns

    if missing_columns:
        errors.append({
            'type': 'missing_columns',
            'columns': list(missing_columns)
        })

    if extra_columns:
        errors.append({
            'type': 'extra_columns',
            'columns': list(extra_columns)
        })

    # Validate each column
    for col_name, col_schema in expected_schema.items():
        if col_name not in df.columns:
            continue

        col = df[col_name]

        # Check data type
        expected_type = col_schema.get('type')
        if expected_type and str(col.dtype) != expected_type:
            errors.append({
                'type': 'wrong_type',
                'column': col_name,
                'expected': expected_type,
                'actual': str(col.dtype)
            })

        # Check nullable
        if not col_schema.get('nullable', True):
            null_count = col.isnull().sum()
            if null_count > 0:
                errors.append({
                    'type': 'null_values',
                    'column': col_name,
                    'count': int(null_count)
                })

        # Check unique
        if col_schema.get('unique', False):
            dup_count = col.duplicated().sum()
            if dup_count > 0:
                errors.append({
                    'type': 'duplicate_values',
                    'column': col_name,
                    'count': int(dup_count)
                })

        # Check range
        if 'min' in col_schema and pd.api.types.is_numeric_dtype(col):
            min_val = col.min()
            if min_val < col_schema['min']:
                errors.append({
                    'type': 'below_minimum',
                    'column': col_name,
                    'min_allowed': col_schema['min'],
                    'min_found': float(min_val)
                })

        if 'max' in col_schema and pd.api.types.is_numeric_dtype(col):
            max_val = col.max()
            if max_val > col_schema['max']:
                errors.append({
                    'type': 'above_maximum',
                    'column': col_name,
                    'max_allowed': col_schema['max'],
                    'max_found': float(max_val)
                })

        # Check pattern
        if 'pattern' in col_schema and col.dtype == 'object':
            import re
            pattern = re.compile(col_schema['pattern'])
            invalid = ~col.dropna().astype(str).str.match(pattern)
            invalid_count = invalid.sum()

            if invalid_count > 0:
                errors.append({
                    'type': 'pattern_mismatch',
                    'column': col_name,
                    'pattern': col_schema['pattern'],
                    'count': int(invalid_count)
                })

    return {
        'valid': len(errors) == 0,
        'errors': errors
    }

# Example usage
expected_schema = {
    'user_id': {
        'type': 'int64',
        'nullable': False,
        'unique': True,
        'min': 1
    },
    'email': {
        'type': 'object',
        'nullable': False,
        'pattern': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    },
    'age': {
        'type': 'int64',
        'nullable': True,
        'min': 0,
        'max': 150
    },
    'score': {
        'type': 'float64',
        'nullable': False,
        'min': 0.0,
        'max': 100.0
    }
}

df = pd.DataFrame({
    'user_id': [1, 2, 3],
    'email': ['user1@example.com', 'user2@example.com', 'invalid'],
    'age': [25, 30, 200],
    'score': [85.5, 92.0, 78.5]
})

result = validate_dataframe_schema(df, expected_schema)
```

## Business Rules Validation

```python
class DataValidator:
    """
    Flexible data validator with custom rules
    """

    def __init__(self):
        self.rules = []
        self.errors = []

    def add_rule(self, name, validator_func, error_message):
        """
        Add validation rule

        validator_func: function that takes data and returns bool
        """
        self.rules.append({
            'name': name,
            'validator': validator_func,
            'error_message': error_message
        })

    def validate(self, data):
        """Validate data against all rules"""
        self.errors = []

        for rule in self.rules:
            try:
                is_valid = rule['validator'](data)
                if not is_valid:
                    self.errors.append({
                        'rule': rule['name'],
                        'message': rule['error_message']
                    })
            except Exception as e:
                self.errors.append({
                    'rule': rule['name'],
                    'message': f"Validation error: {str(e)}"
                })

        return {
            'valid': len(self.errors) == 0,
            'errors': self.errors
        }

# Example: E-commerce order validation
validator = DataValidator()

# Rule: Order total must match sum of line items
validator.add_rule(
    'order_total_matches',
    lambda data: abs(data['total'] - sum(item['price'] * item['quantity']
                                         for item in data['items'])) < 0.01,
    "Order total does not match sum of line items"
)

# Rule: Shipping address required for physical items
validator.add_rule(
    'shipping_address_required',
    lambda data: not any(item['type'] == 'physical' for item in data['items'])
                 or 'shipping_address' in data,
    "Shipping address required for physical items"
)

# Rule: Discount cannot exceed order subtotal
validator.add_rule(
    'discount_valid',
    lambda data: data.get('discount', 0) <= data.get('subtotal', 0),
    "Discount cannot exceed order subtotal"
)

# Rule: Email required for digital items
validator.add_rule(
    'email_for_digital',
    lambda data: not any(item['type'] == 'digital' for item in data['items'])
                 or ('email' in data and '@' in data['email']),
    "Valid email required for digital items"
)

# Validate order
order = {
    'total': 150.00,
    'subtotal': 150.00,
    'discount': 10.00,
    'items': [
        {'name': 'Product A', 'type': 'physical', 'price': 50.00, 'quantity': 2},
        {'name': 'Product B', 'type': 'digital', 'price': 50.00, 'quantity': 1}
    ],
    'email': 'user@example.com'
}

result = validator.validate(order)

if not result['valid']:
    for error in result['errors']:
        print(f"❌ {error['rule']}: {error['message']}")
```

### Complex Business Rules

```python
def validate_user_registration(data):
    """
    Comprehensive user registration validation
    """
    errors = []

    # Required fields
    required = ['username', 'email', 'password', 'terms_accepted']
    for field in required:
        if field not in data or not data[field]:
            errors.append(f"Field '{field}' is required")

    # Username validation
    if 'username' in data:
        username = data['username']

        if len(username) < 3:
            errors.append("Username must be at least 3 characters")

        if len(username) > 20:
            errors.append("Username must not exceed 20 characters")

        if not username.isalnum():
            errors.append("Username must contain only letters and numbers")

    # Email validation
    if 'email' in data:
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, data['email']):
            errors.append("Invalid email format")

    # Password validation
    if 'password' in data:
        password = data['password']

        if len(password) < 8:
            errors.append("Password must be at least 8 characters")

        if not any(c.isupper() for c in password):
            errors.append("Password must contain at least one uppercase letter")

        if not any(c.islower() for c in password):
            errors.append("Password must contain at least one lowercase letter")

        if not any(c.isdigit() for c in password):
            errors.append("Password must contain at least one digit")

        if not any(c in '!@#$%^&*()_+-=' for c in password):
            errors.append("Password must contain at least one special character")

    # Password confirmation
    if 'password' in data and 'password_confirm' in data:
        if data['password'] != data['password_confirm']:
            errors.append("Passwords do not match")

    # Age validation
    if 'birthdate' in data:
        from datetime import datetime
        try:
            birthdate = datetime.fromisoformat(data['birthdate'])
            age = (datetime.now() - birthdate).days / 365.25

            if age < 13:
                errors.append("Must be at least 13 years old")

            if age > 150:
                errors.append("Invalid birthdate")
        except:
            errors.append("Invalid birthdate format")

    # Terms acceptance
    if not data.get('terms_accepted'):
        errors.append("Must accept terms and conditions")

    return {
        'valid': len(errors) == 0,
        'errors': errors
    }
```

## Data Quality Validation

### Completeness Check

```python
def check_completeness(df):
    """
    Check data completeness
    """
    report = {
        'total_cells': len(df) * len(df.columns),
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'columns': {}
    }

    for col in df.columns:
        null_count = df[col].isnull().sum()
        completeness = (1 - null_count / len(df)) * 100

        report['columns'][col] = {
            'total': len(df),
            'null_count': int(null_count),
            'non_null_count': int(len(df) - null_count),
            'completeness_percent': round(completeness, 2)
        }

    # Overall completeness
    total_nulls = df.isnull().sum().sum()
    report['overall_completeness'] = round(
        (1 - total_nulls / report['total_cells']) * 100,
        2
    )

    return report

def check_duplicates(df, subset=None):
    """
    Check for duplicate rows
    """
    dup_mask = df.duplicated(subset=subset, keep=False)
    duplicates = df[dup_mask]

    return {
        'has_duplicates': dup_mask.any(),
        'duplicate_count': int(dup_mask.sum()),
        'duplicate_percent': round(dup_mask.sum() / len(df) * 100, 2),
        'duplicate_rows': duplicates.to_dict('records') if len(duplicates) < 100 else []
    }

def check_outliers(df, column, method='iqr'):
    """
    Detect outliers in numeric column
    """
    if method == 'iqr':
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1

        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]

    elif method == 'zscore':
        from scipy import stats
        z_scores = np.abs(stats.zscore(df[column].dropna()))
        outliers = df[z_scores > 3]

    return {
        'method': method,
        'lower_bound': float(lower_bound) if method == 'iqr' else None,
        'upper_bound': float(upper_bound) if method == 'iqr' else None,
        'outlier_count': len(outliers),
        'outlier_percent': round(len(outliers) / len(df) * 100, 2),
        'outliers': outliers[column].tolist()[:100]  # Limit to 100
    }
```

### Format Validation

```python
import re

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_phone(phone, country='US'):
    """Validate phone number"""
    patterns = {
        'US': r'^\+?1?\d{10}$',
        'UK': r'^\+?44\d{10}$',
        'international': r'^\+?[1-9]\d{1,14}$'
    }

    phone_clean = re.sub(r'[^\d+]', '', phone)
    pattern = patterns.get(country, patterns['international'])

    return bool(re.match(pattern, phone_clean))

def validate_url(url):
    """Validate URL format"""
    pattern = r'^https?://[a-zA-Z0-9-._~:/?#\[\]@!$&\'()*+,;=]+$'
    return bool(re.match(pattern, url))

def validate_date(date_string, format='%Y-%m-%d'):
    """Validate date format"""
    from datetime import datetime

    try:
        datetime.strptime(date_string, format)
        return True
    except:
        return False

def validate_credit_card(card_number):
    """Validate credit card using Luhn algorithm"""
    card_number = re.sub(r'[\s-]', '', card_number)

    if not card_number.isdigit():
        return False

    if len(card_number) < 13 or len(card_number) > 19:
        return False

    # Luhn algorithm
    def luhn_checksum(card_num):
        def digits_of(n):
            return [int(d) for d in str(n)]

        digits = digits_of(card_num)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]

        checksum = sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits_of(d * 2))

        return checksum % 10

    return luhn_checksum(card_number) == 0

def validate_formats_in_dataframe(df):
    """
    Validate common formats in DataFrame
    """
    results = {}

    for col in df.columns:
        col_lower = col.lower()

        # Email validation
        if 'email' in col_lower:
            invalid = df[~df[col].apply(validate_email)]
            results[col] = {
                'type': 'email',
                'valid_count': len(df) - len(invalid),
                'invalid_count': len(invalid),
                'invalid_samples': invalid[col].head(5).tolist()
            }

        # Phone validation
        elif 'phone' in col_lower:
            invalid = df[~df[col].apply(validate_phone)]
            results[col] = {
                'type': 'phone',
                'valid_count': len(df) - len(invalid),
                'invalid_count': len(invalid),
                'invalid_samples': invalid[col].head(5).tolist()
            }

        # URL validation
        elif 'url' in col_lower or 'link' in col_lower:
            invalid = df[~df[col].apply(validate_url)]
            results[col] = {
                'type': 'url',
                'valid_count': len(df) - len(invalid),
                'invalid_count': len(invalid),
                'invalid_samples': invalid[col].head(5).tolist()
            }

    return results
```

## Validation Report Generation

```python
def generate_validation_report(df, schema=None, business_rules=None):
    """
    Generate comprehensive validation report
    """
    from datetime import datetime

    report = f"""# Data Validation Report
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Dataset:** {len(df):,} rows × {len(df.columns)} columns

---

## Summary

"""

    # Completeness check
    completeness = check_completeness(df)
    report += f"- **Overall Completeness:** {completeness['overall_completeness']}%\n"

    # Duplicates check
    duplicates = check_duplicates(df)
    report += f"- **Duplicate Rows:** {duplicates['duplicate_count']:,} ({duplicates['duplicate_percent']}%)\n"

    # Schema validation
    if schema:
        schema_result = validate_dataframe_schema(df, schema)
        status = "✅ Pass" if schema_result['valid'] else f"❌ Fail ({len(schema_result['errors'])} errors)"
        report += f"- **Schema Validation:** {status}\n"

    report += "\n---\n\n## Completeness Analysis\n\n"

    report += "| Column | Non-Null | Null Count | Completeness |\n"
    report += "|--------|----------|------------|-------------|\n"

    for col, stats in completeness['columns'].items():
        report += f"| {col} | {stats['non_null_count']:,} | {stats['null_count']:,} | {stats['completeness_percent']}% |\n"

    # Schema validation details
    if schema and not schema_result['valid']:
        report += "\n---\n\n## Schema Validation Errors\n\n"

        for error in schema_result['errors']:
            report += f"### {error['type'].replace('_', ' ').title()}\n\n"

            if error['type'] == 'wrong_type':
                report += f"- **Column:** {error['column']}\n"
                report += f"- **Expected:** {error['expected']}\n"
                report += f"- **Actual:** {error['actual']}\n\n"

            elif error['type'] in ['null_values', 'duplicate_values']:
                report += f"- **Column:** {error['column']}\n"
                report += f"- **Count:** {error['count']:,}\n\n"

            elif error['type'] == 'pattern_mismatch':
                report += f"- **Column:** {error['column']}\n"
                report += f"- **Pattern:** `{error['pattern']}`\n"
                report += f"- **Invalid Count:** {error['count']:,}\n\n"

    # Format validation
    format_results = validate_formats_in_dataframe(df)

    if format_results:
        report += "\n---\n\n## Format Validation\n\n"

        for col, result in format_results.items():
            report += f"### {col} ({result['type']})\n\n"
            report += f"- **Valid:** {result['valid_count']:,}\n"
            report += f"- **Invalid:** {result['invalid_count']:,}\n"

            if result['invalid_samples']:
                report += f"\n**Invalid Samples:**\n"
                for sample in result['invalid_samples']:
                    report += f"- `{sample}`\n"

            report += "\n"

    # Data quality score
    quality_score = calculate_quality_score(df, schema, duplicates, completeness)

    report += f"\n---\n\n## Data Quality Score\n\n"
    report += f"### Overall Score: {quality_score['overall']}/100\n\n"

    for dimension, score in quality_score['dimensions'].items():
        report += f"- **{dimension}:** {score}/100\n"

    return report

def calculate_quality_score(df, schema, duplicates, completeness):
    """Calculate data quality score"""

    scores = {}

    # Completeness score
    scores['Completeness'] = completeness['overall_completeness']

    # Uniqueness score
    scores['Uniqueness'] = 100 - duplicates['duplicate_percent']

    # Validity score (if schema provided)
    if schema:
        schema_result = validate_dataframe_schema(df, schema)
        error_rate = len(schema_result['errors']) / (len(df) * len(df.columns))
        scores['Validity'] = max(0, 100 - (error_rate * 100))
    else:
        scores['Validity'] = 100

    # Overall score
    overall = sum(scores.values()) / len(scores)

    return {
        'overall': round(overall, 1),
        'dimensions': {k: round(v, 1) for k, v in scores.items()}
    }
```

## Best Practices

1. **Define clear validation rules** before implementation
2. **Validate early** in the data pipeline
3. **Provide detailed error messages** for debugging
4. **Use schema validation** for API contracts
5. **Implement business rule validation** separately from schema
6. **Log validation failures** for monitoring
7. **Generate validation reports** for auditing
8. **Handle validation errors gracefully**
9. **Test validation rules** with edge cases
10. **Version control** validation schemas and rules

## Common Validation Patterns

### API Request Validation
```python
def validate_api_request(request_data, endpoint):
    """Validate API request data"""

    schemas = {
        '/users': user_schema,
        '/orders': order_schema,
        '/products': product_schema
    }

    schema = schemas.get(endpoint)
    if not schema:
        return {'valid': False, 'error': 'Unknown endpoint'}

    return validate_json_schema(request_data, schema)
```

### Batch Data Validation
```python
def validate_batch(records, validator):
    """Validate batch of records"""

    results = []

    for i, record in enumerate(records):
        result = validator.validate(record)
        result['record_index'] = i

        if not result['valid']:
            results.append(result)

    return {
        'total_records': len(records),
        'valid_records': len(records) - len(results),
        'invalid_records': len(results),
        'failures': results
    }
```

## Notes

- Always validate at system boundaries
- Use appropriate validation levels (syntax, semantic, business)
- Cache validation results for performance
- Provide clear error messages for users
- Log validation metrics for monitoring
- Consider validation performance for large datasets
- Use streaming validation for big data
- Keep validation rules maintainable and testable
