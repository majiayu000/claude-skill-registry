---
name: json-transformer
description: Transform, manipulate, and analyze JSON data structures with advanced operations.
---

# JSON Transformer Skill

Transform, manipulate, and analyze JSON data structures with advanced operations.

## Instructions

You are a JSON transformation expert. When invoked:

1. **Parse and Validate JSON**:
   - Parse JSON from files, strings, or APIs
   - Validate JSON structure and schema
   - Handle malformed JSON gracefully
   - Pretty-print and format JSON
   - Detect and fix common JSON issues

2. **Transform Data Structures**:
   - Reshape nested objects and arrays
   - Flatten and unflatten structures
   - Extract specific paths (JSONPath, JMESPath)
   - Merge and combine JSON documents
   - Filter and map data

3. **Advanced Operations**:
   - Convert between JSON and other formats (CSV, YAML, XML)
   - Apply transformations (jq-style operations)
   - Query and search JSON data
   - Diff and compare JSON documents
   - Generate JSON from schemas

4. **Data Manipulation**:
   - Add, update, delete properties
   - Rename keys
   - Convert data types
   - Sort and deduplicate
   - Calculate aggregate values

## Usage Examples

```
@json-transformer data.json
@json-transformer --flatten
@json-transformer --path "users[*].email"
@json-transformer --merge file1.json file2.json
@json-transformer --to-csv data.json
@json-transformer --validate schema.json
```

## Basic JSON Operations

### Parsing and Writing

#### Python
```python
import json

# Parse JSON string
data = json.loads('{"name": "John", "age": 30}')

# Parse from file
with open('data.json', 'r') as f:
    data = json.load(f)

# Write JSON to file
with open('output.json', 'w') as f:
    json.dump(data, f, indent=2)

# Pretty print
print(json.dumps(data, indent=2, sort_keys=True))

# Compact output
compact = json.dumps(data, separators=(',', ':'))

# Handle special types
from datetime import datetime
import decimal

def json_encoder(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError(f"Type {type(obj)} not serializable")

json.dumps(data, default=json_encoder)
```

#### JavaScript
```javascript
// Parse JSON string
const data = JSON.parse('{"name": "John", "age": 30}');

// Parse from file (Node.js)
const fs = require('fs');
const data = JSON.parse(fs.readFileSync('data.json', 'utf8'));

// Write JSON to file
fs.writeFileSync('output.json', JSON.stringify(data, null, 2));

// Pretty print
console.log(JSON.stringify(data, null, 2));

// Custom serialization
const json = JSON.stringify(data, (key, value) => {
  if (value instanceof Date) {
    return value.toISOString();
  }
  return value;
}, 2);
```

#### jq (Command Line)
```bash
# Pretty print
cat data.json | jq '.'

# Compact output
cat data.json | jq -c '.'

# Sort keys
cat data.json | jq -S '.'

# Read from file, write to file
jq '.' input.json > output.json
```

### Validation

#### Python (jsonschema)
```python
from jsonschema import validate, ValidationError

# Define schema
schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "number", "minimum": 0},
        "email": {"type": "string", "format": "email"}
    },
    "required": ["name", "email"]
}

# Validate data
data = {"name": "John", "email": "john@example.com", "age": 30}

try:
    validate(instance=data, schema=schema)
    print("Valid JSON")
except ValidationError as e:
    print(f"Invalid: {e.message}")

# Validate against JSON Schema draft
from jsonschema import Draft7Validator

validator = Draft7Validator(schema)
errors = list(validator.iter_errors(data))
for error in errors:
    print(f"Error at {'.'.join(str(p) for p in error.path)}: {error.message}")
```

#### JavaScript (ajv)
```javascript
const Ajv = require('ajv');
const ajv = new Ajv();

const schema = {
  type: 'object',
  properties: {
    name: { type: 'string' },
    age: { type: 'number', minimum: 0 },
    email: { type: 'string', format: 'email' }
  },
  required: ['name', 'email']
};

const validate = ajv.compile(schema);

const data = { name: 'John', email: 'john@example.com', age: 30 };

if (validate(data)) {
  console.log('Valid JSON');
} else {
  console.log('Invalid:', validate.errors);
}
```

## Data Extraction and Querying

### JSONPath Queries

#### Python (jsonpath-ng)
```python
from jsonpath_ng import jsonpath, parse

data = {
    "users": [
        {"name": "John", "age": 30, "email": "john@example.com"},
        {"name": "Jane", "age": 25, "email": "jane@example.com"}
    ]
}

# Extract all user names
jsonpath_expr = parse('users[*].name')
names = [match.value for match in jsonpath_expr.find(data)]
# Result: ['John', 'Jane']

# Extract emails of users over 25
jsonpath_expr = parse('users[?(@.age > 25)].email')
emails = [match.value for match in jsonpath_expr.find(data)]

# Nested extraction
data = {
    "company": {
        "departments": [
            {
                "name": "Engineering",
                "employees": [
                    {"name": "Alice", "salary": 100000},
                    {"name": "Bob", "salary": 90000}
                ]
            }
        ]
    }
}

jsonpath_expr = parse('company.departments[*].employees[*].name')
names = [match.value for match in jsonpath_expr.find(data)]
```

#### jq
```bash
# Extract field
echo '{"name": "John", "age": 30}' | jq '.name'

# Extract from array
echo '[{"name": "John"}, {"name": "Jane"}]' | jq '.[].name'

# Filter array
echo '[{"name": "John", "age": 30}, {"name": "Jane", "age": 25}]' | \
  jq '.[] | select(.age > 25)'

# Extract nested fields
cat data.json | jq '.users[].email'

# Multiple fields
cat data.json | jq '.users[] | {name: .name, email: .email}'

# Conditional extraction
cat data.json | jq '.users[] | select(.age > 25) | .email'
```

### JMESPath Queries

#### Python (jmespath)
```python
import jmespath

data = {
    "users": [
        {"name": "John", "age": 30, "tags": ["admin", "developer"]},
        {"name": "Jane", "age": 25, "tags": ["developer"]},
        {"name": "Bob", "age": 35, "tags": ["manager"]}
    ]
}

# Simple extraction
names = jmespath.search('users[*].name', data)
# Result: ['John', 'Jane', 'Bob']

# Filtering
admins = jmespath.search('users[?contains(tags, `admin`)]', data)

# Multiple conditions
senior_devs = jmespath.search(
    'users[?age > `28` && contains(tags, `developer`)]',
    data
)

# Projections
result = jmespath.search('users[*].{name: name, age: age}', data)

# Nested queries
data = {
    "departments": [
        {
            "name": "Engineering",
            "employees": [
                {"name": "Alice", "skills": ["Python", "Go"]},
                {"name": "Bob", "skills": ["JavaScript", "Python"]}
            ]
        }
    ]
}

python_devs = jmespath.search(
    'departments[*].employees[?contains(skills, `Python`)].name',
    data
)
```

## Data Transformation

### Flattening Nested JSON

#### Python
```python
def flatten_json(nested_json, parent_key='', sep='.'):
    """
    Flatten nested JSON structure
    """
    items = []

    for key, value in nested_json.items():
        new_key = f"{parent_key}{sep}{key}" if parent_key else key

        if isinstance(value, dict):
            items.extend(flatten_json(value, new_key, sep=sep).items())
        elif isinstance(value, list):
            for i, item in enumerate(value):
                if isinstance(item, dict):
                    items.extend(flatten_json(item, f"{new_key}[{i}]", sep=sep).items())
                else:
                    items.append((f"{new_key}[{i}]", item))
        else:
            items.append((new_key, value))

    return dict(items)

# Example
nested = {
    "user": {
        "name": "John",
        "address": {
            "city": "New York",
            "zip": "10001"
        },
        "tags": ["admin", "developer"]
    }
}

flat = flatten_json(nested)
# Result: {
#     'user.name': 'John',
#     'user.address.city': 'New York',
#     'user.address.zip': '10001',
#     'user.tags[0]': 'admin',
#     'user.tags[1]': 'developer'
# }
```

#### JavaScript
```javascript
function flattenJSON(obj, prefix = '', result = {}) {
  for (const [key, value] of Object.entries(obj)) {
    const newKey = prefix ? `${prefix}.${key}` : key;

    if (value && typeof value === 'object' && !Array.isArray(value)) {
      flattenJSON(value, newKey, result);
    } else if (Array.isArray(value)) {
      value.forEach((item, index) => {
        if (typeof item === 'object') {
          flattenJSON(item, `${newKey}[${index}]`, result);
        } else {
          result[`${newKey}[${index}]`] = item;
        }
      });
    } else {
      result[newKey] = value;
    }
  }

  return result;
}
```

### Unflattening JSON

```python
def unflatten_json(flat_json, sep='.'):
    """
    Unflatten a flattened JSON structure
    """
    result = {}

    for key, value in flat_json.items():
        parts = key.split(sep)
        current = result

        for i, part in enumerate(parts[:-1]):
            # Handle array notation
            if '[' in part:
                array_key, index = part.split('[')
                index = int(index.rstrip(']'))

                if array_key not in current:
                    current[array_key] = []

                # Extend array if needed
                while len(current[array_key]) <= index:
                    current[array_key].append({})

                current = current[array_key][index]
            else:
                if part not in current:
                    current[part] = {}
                current = current[part]

        # Set the final value
        final_key = parts[-1]
        if '[' in final_key:
            array_key, index = final_key.split('[')
            index = int(index.rstrip(']'))

            if array_key not in current:
                current[array_key] = []

            while len(current[array_key]) <= index:
                current[array_key].append(None)

            current[array_key][index] = value
        else:
            current[final_key] = value

    return result
```

### Merging JSON

#### Python
```python
def deep_merge(dict1, dict2):
    """
    Deep merge two dictionaries
    """
    result = dict1.copy()

    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value

    return result

# Example
base = {
    "user": {"name": "John", "age": 30},
    "settings": {"theme": "dark"}
}

override = {
    "user": {"age": 31, "email": "john@example.com"},
    "settings": {"language": "en"}
}

merged = deep_merge(base, override)
# Result: {
#     'user': {'name': 'John', 'age': 31, 'email': 'john@example.com'},
#     'settings': {'theme': 'dark', 'language': 'en'}
# }
```

#### jq
```bash
# Merge two JSON files
jq -s '.[0] * .[1]' file1.json file2.json

# Deep merge
jq -s 'reduce .[] as $item ({}; . * $item)' file1.json file2.json
```

### Transforming Keys

```python
def transform_keys(obj, transform_fn):
    """
    Transform all keys in JSON structure
    """
    if isinstance(obj, dict):
        return {transform_fn(k): transform_keys(v, transform_fn) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [transform_keys(item, transform_fn) for item in obj]
    else:
        return obj

# Convert to snake_case
import re

def to_snake_case(text):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', text)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

data = {
    "firstName": "John",
    "lastName": "Doe",
    "userInfo": {
        "emailAddress": "john@example.com"
    }
}

snake_case_data = transform_keys(data, to_snake_case)
# Result: {
#     'first_name': 'John',
#     'last_name': 'Doe',
#     'user_info': {'email_address': 'john@example.com'}
# }

# Convert to camelCase
def to_camel_case(text):
    components = text.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])
```

## Format Conversion

### JSON to CSV

#### Python
```python
import json
import csv
import pandas as pd

# Using pandas (recommended)
data = [
    {"name": "John", "age": 30, "email": "john@example.com"},
    {"name": "Jane", "age": 25, "email": "jane@example.com"}
]

df = pd.DataFrame(data)
df.to_csv('output.csv', index=False)

# Using csv module
with open('output.csv', 'w', newline='') as csvfile:
    if data:
        writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

# Handle nested JSON
def flatten_for_csv(data):
    """Flatten nested JSON for CSV export"""
    if isinstance(data, list):
        return [flatten_json(item) for item in data]
    return flatten_json(data)

flattened = flatten_for_csv(data)
pd.DataFrame(flattened).to_csv('output.csv', index=False)
```

#### jq
```bash
# Convert JSON array to CSV
cat data.json | jq -r '.[] | [.name, .age, .email] | @csv'

# With headers
cat data.json | jq -r '["name", "age", "email"], (.[] | [.name, .age, .email]) | @csv'
```

### JSON to YAML

#### Python
```python
import json
import yaml

# JSON to YAML
with open('data.json', 'r') as json_file:
    data = json.load(json_file)

with open('data.yaml', 'w') as yaml_file:
    yaml.dump(data, yaml_file, default_flow_style=False)

# YAML to JSON
with open('data.yaml', 'r') as yaml_file:
    data = yaml.safe_load(yaml_file)

with open('data.json', 'w') as json_file:
    json.dump(data, json_file, indent=2)
```

### JSON to XML

#### Python
```python
import json
import xml.etree.ElementTree as ET

def json_to_xml(json_obj, root_name='root'):
    """Convert JSON to XML"""

    def build_xml(parent, obj):
        if isinstance(obj, dict):
            for key, val in obj.items():
                elem = ET.SubElement(parent, key)
                build_xml(elem, val)
        elif isinstance(obj, list):
            for item in obj:
                elem = ET.SubElement(parent, 'item')
                build_xml(elem, item)
        else:
            parent.text = str(obj)

    root = ET.Element(root_name)
    build_xml(root, json_obj)

    return ET.tostring(root, encoding='unicode')

# Example
data = {"user": {"name": "John", "age": 30}}
xml_string = json_to_xml(data)
```

## Advanced Transformations

### jq-Style Transformations

#### Python (pyjq)
```python
import pyjq

data = {
    "users": [
        {"name": "John", "age": 30, "city": "New York"},
        {"name": "Jane", "age": 25, "city": "San Francisco"},
        {"name": "Bob", "age": 35, "city": "New York"}
    ]
}

# Select and transform
result = pyjq.all('.users[] | {name, age}', data)

# Filter and group
result = pyjq.all('group_by(.city) | map({city: .[0].city, count: length})', data)

# Complex transformation
result = pyjq.all('''
    .users
    | map(select(.age > 25))
    | sort_by(.age)
    | reverse
''', data)
```

#### jq Examples
```bash
# Map over array
echo '[1,2,3,4,5]' | jq 'map(. * 2)'

# Filter and transform
cat users.json | jq '.users | map(select(.age > 25) | {name, email})'

# Group by field
cat data.json | jq 'group_by(.category) | map({category: .[0].category, count: length})'

# Calculate sum
cat orders.json | jq '[.[] | .amount] | add'

# Create new structure
cat users.json | jq '{
  total: length,
  users: [.[] | {name, email}],
  avgAge: ([.[] | .age] | add / length)
}'

# Conditional logic
cat data.json | jq '.[] | if .status == "active" then .name else empty end'
```

### Complex Restructuring

```python
def restructure_json(data):
    """
    Example: Transform flat user records into hierarchical structure
    """
    # Input: [
    #   {"userId": 1, "name": "John", "orderId": 101, "product": "A"},
    #   {"userId": 1, "name": "John", "orderId": 102, "product": "B"},
    #   {"userId": 2, "name": "Jane", "orderId": 103, "product": "C"}
    # ]

    # Output: [
    #   {
    #     "userId": 1,
    #     "name": "John",
    #     "orders": [
    #       {"orderId": 101, "product": "A"},
    #       {"orderId": 102, "product": "B"}
    #     ]
    #   },
    #   {
    #     "userId": 2,
    #     "name": "Jane",
    #     "orders": [{"orderId": 103, "product": "C"}]
    #   }
    # ]

    from collections import defaultdict

    users = defaultdict(lambda: {"orders": []})

    for record in data:
        user_id = record["userId"]

        if "name" not in users[user_id]:
            users[user_id]["userId"] = user_id
            users[user_id]["name"] = record["name"]

        users[user_id]["orders"].append({
            "orderId": record["orderId"],
            "product": record["product"]
        })

    return list(users.values())
```

### Array Operations

```python
import json

def unique_by_key(array, key):
    """Remove duplicates based on key"""
    seen = set()
    result = []

    for item in array:
        value = item.get(key)
        if value not in seen:
            seen.add(value)
            result.append(item)

    return result

def sort_by_key(array, key, reverse=False):
    """Sort array by key"""
    return sorted(array, key=lambda x: x.get(key, ''), reverse=reverse)

def group_by_key(array, key):
    """Group array elements by key"""
    from collections import defaultdict

    groups = defaultdict(list)
    for item in array:
        groups[item.get(key)].append(item)

    return dict(groups)

# Example usage
users = [
    {"name": "John", "age": 30, "city": "New York"},
    {"name": "Jane", "age": 25, "city": "San Francisco"},
    {"name": "Bob", "age": 35, "city": "New York"},
    {"name": "Alice", "age": 28, "city": "San Francisco"}
]

# Sort by age
sorted_users = sort_by_key(users, 'age')

# Group by city
by_city = group_by_key(users, 'city')
```

## JSON Diff and Comparison

```python
import json
from deepdiff import DeepDiff

def json_diff(obj1, obj2):
    """Compare two JSON objects and return differences"""
    diff = DeepDiff(obj1, obj2, ignore_order=True)
    return diff

# Example
old = {
    "name": "John",
    "age": 30,
    "addresses": [{"city": "New York"}]
}

new = {
    "name": "John",
    "age": 31,
    "addresses": [{"city": "San Francisco"}]
}

diff = json_diff(old, new)
print(json.dumps(diff, indent=2))

# Manual diff
def simple_diff(obj1, obj2, path=""):
    """Simple diff implementation"""
    diffs = []

    if type(obj1) != type(obj2):
        diffs.append(f"{path}: type changed from {type(obj1)} to {type(obj2)}")
        return diffs

    if isinstance(obj1, dict):
        all_keys = set(obj1.keys()) | set(obj2.keys())

        for key in all_keys:
            new_path = f"{path}.{key}" if path else key

            if key not in obj1:
                diffs.append(f"{new_path}: added")
            elif key not in obj2:
                diffs.append(f"{new_path}: removed")
            elif obj1[key] != obj2[key]:
                diffs.extend(simple_diff(obj1[key], obj2[key], new_path))

    elif isinstance(obj1, list):
        if len(obj1) != len(obj2):
            diffs.append(f"{path}: length changed from {len(obj1)} to {len(obj2)}")

        for i, (item1, item2) in enumerate(zip(obj1, obj2)):
            diffs.extend(simple_diff(item1, item2, f"{path}[{i}]"))

    elif obj1 != obj2:
        diffs.append(f"{path}: changed from {obj1} to {obj2}")

    return diffs
```

## Schema Generation

```python
def generate_schema(data, name="root"):
    """
    Generate JSON Schema from data
    """
    if isinstance(data, dict):
        properties = {}
        required = []

        for key, value in data.items():
            properties[key] = generate_schema(value, key)
            if value is not None:
                required.append(key)

        schema = {
            "type": "object",
            "properties": properties
        }

        if required:
            schema["required"] = required

        return schema

    elif isinstance(data, list):
        if data:
            return {
                "type": "array",
                "items": generate_schema(data[0], name)
            }
        return {"type": "array"}

    elif isinstance(data, bool):
        return {"type": "boolean"}

    elif isinstance(data, int):
        return {"type": "integer"}

    elif isinstance(data, float):
        return {"type": "number"}

    elif isinstance(data, str):
        return {"type": "string"}

    elif data is None:
        return {"type": "null"}

    return {}

# Example
sample_data = {
    "name": "John",
    "age": 30,
    "email": "john@example.com",
    "active": True,
    "tags": ["developer", "admin"],
    "address": {
        "city": "New York",
        "zip": "10001"
    }
}

schema = generate_schema(sample_data)
print(json.dumps(schema, indent=2))
```

## Utility Functions

### Pretty Print with Colors

```python
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter

def pretty_print_json(data):
    """Print JSON with syntax highlighting"""
    json_str = json.dumps(data, indent=2, sort_keys=True)
    print(highlight(json_str, JsonLexer(), TerminalFormatter()))
```

### Safe Access with Default Values

```python
def safe_get(data, path, default=None):
    """
    Safely get nested value from JSON
    path: "user.address.city" or ["user", "address", "city"]
    """
    if isinstance(path, str):
        path = path.split('.')

    current = data
    for key in path:
        if isinstance(current, dict):
            current = current.get(key)
        elif isinstance(current, list) and key.isdigit():
            index = int(key)
            current = current[index] if 0 <= index < len(current) else None
        else:
            return default

        if current is None:
            return default

    return current

# Example
data = {"user": {"address": {"city": "New York"}}}
city = safe_get(data, "user.address.city")  # "New York"
country = safe_get(data, "user.address.country", "Unknown")  # "Unknown"
```

## Command Line Tools

### Using jq
```bash
# Format JSON
cat messy.json | jq '.'

# Extract specific fields
cat data.json | jq '.users[] | {name, email}'

# Filter arrays
cat data.json | jq '.[] | select(.age > 30)'

# Transform keys to lowercase
cat data.json | jq 'with_entries(.key |= ascii_downcase)'

# Merge multiple JSON files
jq -s 'add' file1.json file2.json file3.json

# Convert to CSV
cat data.json | jq -r '.[] | [.name, .age, .email] | @csv'
```

### Using Python (command line)
```bash
# Pretty print
python -m json.tool input.json

# Compact output
python -c "import json; print(json.dumps(json.load(open('data.json')), separators=(',',':')))"

# Extract field
python -c "import json; data=json.load(open('data.json')); print(data['users'][0]['name'])"
```

## Best Practices

1. **Always validate JSON** before processing
2. **Use schema validation** for API contracts
3. **Handle errors gracefully** (malformed JSON)
4. **Use appropriate libraries** (jq, jmespath, jsonpath)
5. **Preserve data types** during transformations
6. **Document complex transformations**
7. **Use version control** for schema definitions
8. **Test transformations** with edge cases
9. **Consider memory usage** for large files
10. **Use streaming parsers** for very large JSON

## Common Patterns

### API Response Transformation
```python
def transform_api_response(response):
    """Transform API response to application format"""
    return {
        "users": [
            {
                "id": user["userId"],
                "name": f"{user['firstName']} {user['lastName']}",
                "email": user["emailAddress"],
                "active": user["status"] == "active"
            }
            for user in response.get("data", {}).get("users", [])
        ],
        "pagination": {
            "page": response.get("page", 1),
            "total": response.get("totalResults", 0)
        }
    }
```

### Configuration Merging
```python
def merge_configs(base_config, user_config):
    """Merge user configuration with base configuration"""
    result = deep_merge(base_config, user_config)

    # Validate required fields
    required = ["database", "api_key"]
    for field in required:
        if field not in result:
            raise ValueError(f"Missing required field: {field}")

    return result
```

## Notes

- Always handle edge cases (null, empty arrays, missing keys)
- Use appropriate tools for the job (jq for CLI, pandas for data science)
- Consider performance for large JSON files
- Validate schemas in production environments
- Keep transformations idempotent when possible
- Document expected JSON structure
- Use TypeScript/JSON Schema for type safety
