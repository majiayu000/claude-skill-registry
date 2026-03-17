---
name: json-and-csv-data-transformation
description: "Transform data between JSON, CSV, and other formats with filtering, mapping, and flattening. Use when: (1) Converting API responses to CSV, (2) Processing data pipelines, (3) Extracting specific fields, or (4) Flattening nested structures."
---

# JSON and CSV Data Transformation

Transform data between JSON, CSV, and other formats. Filter, map, flatten nested objects, and reshape data for analysis, reporting, and API integration.

## When to use

- Use case 1: When the user asks to convert data between JSON and CSV formats
- Use case 2: When you need to filter, extract, or transform specific fields from data
- Use case 3: For flattening nested JSON structures into tabular format
- Use case 4: When processing API responses for analysis or reporting

## Required tools / APIs

- **jq** — Command-line JSON processor (essential for JSON manipulation)
- **csvkit** — Suite of CSV tools (csvjson, csvcut, csvgrep, etc.)
- No external API required

Install options:

```bash
# Ubuntu/Debian
sudo apt-get install -y jq csvkit

# macOS
brew install jq csvkit

# Node.js (native support, no packages needed for basic operations)
# For advanced CSV parsing: npm install csv-parse csv-stringify
```

## Skills

### json_to_csv

Convert JSON array to CSV format.

```bash
# Simple JSON array to CSV
echo '[{"name":"Alice","age":30},{"name":"Bob","age":25}]' | jq -r '(.[0] | keys_unsorted) as $keys | $keys, (map([.[ $keys[] ]]) | .[] | @csv)'

# JSON file to CSV file
jq -r '(.[0] | keys_unsorted) as $keys | $keys, (map([.[ $keys[] ]]) | .[] | @csv)' data.json > output.csv

# JSON to CSV with specific fields
jq -r '.[] | [.id, .name, .email] | @csv' users.json

# Using csvkit (simpler syntax)
cat data.json | in2csv -f json > output.csv
```

**Node.js:**

```javascript
function jsonToCSV(jsonArray) {
  if (!Array.isArray(jsonArray) || jsonArray.length === 0) {
    return '';
  }
  
  // Get headers from first object
  const headers = Object.keys(jsonArray[0]);
  
  // Escape CSV values
  const escape = (val) => {
    if (val === null || val === undefined) return '';
    const str = String(val);
    if (str.includes(',') || str.includes('"') || str.includes('\n')) {
      return `"${str.replace(/"/g, '""')}"`;
    }
    return str;
  };
  
  // Build CSV
  const headerRow = headers.join(',');
  const dataRows = jsonArray.map(obj =>
    headers.map(header => escape(obj[header])).join(',')
  );
  
  return [headerRow, ...dataRows].join('\n');
}

// Usage
// const data = [
//   { name: 'Alice', age: 30, city: 'New York' },
//   { name: 'Bob', age: 25, city: 'San Francisco' }
// ];
// console.log(jsonToCSV(data));
```

### csv_to_json

Convert CSV to JSON array.

```bash
# CSV to JSON
csvjson data.csv

# CSV to JSON with pretty printing
csvjson data.csv | jq '.'

# CSV to JSON array of objects
csvjson --stream data.csv

# CSV file to JSON file
csvjson input.csv > output.json

# Using pure jq (if headers are in first row)
jq -Rsn '[inputs | split(",") | {name: .[0], age: .[1], city: .[2]}]' < data.csv
```

**Node.js:**

```javascript
function csvToJSON(csvString) {
  const lines = csvString.trim().split('\n');
  if (lines.length < 2) return [];
  
  // Parse CSV value (handle quotes)
  const parseCSVValue = (val) => {
    val = val.trim();
    if (val.startsWith('"') && val.endsWith('"')) {
      return val.slice(1, -1).replace(/""/g, '"');
    }
    return val;
  };
  
  // Split CSV line (basic implementation)
  const splitCSVLine = (line) => {
    const result = [];
    let current = '';
    let inQuotes = false;
    
    for (let i = 0; i < line.length; i++) {
      const char = line[i];
      
      if (char === '"') {
        inQuotes = !inQuotes;
        current += char;
      } else if (char === ',' && !inQuotes) {
        result.push(parseCSVValue(current));
        current = '';
      } else {
        current += char;
      }
    }
    result.push(parseCSVValue(current));
    return result;
  };
  
  const headers = splitCSVLine(lines[0]);
  const data = lines.slice(1).map(line => {
    const values = splitCSVLine(line);
    const obj = {};
    headers.forEach((header, i) => {
      obj[header] = values[i] || '';
    });
    return obj;
  });
  
  return data;
}

// Usage
// const csv = `name,age,city
// Alice,30,New York
// Bob,25,"San Francisco"`;
// console.log(JSON.stringify(csvToJSON(csv), null, 2));
```

### filter_and_extract_json

Filter and extract specific fields from JSON.

```bash
# Extract specific fields
jq '.[] | {name: .name, email: .email}' users.json

# Filter by condition
jq '.[] | select(.age > 25)' users.json

# Filter and extract
jq '[.[] | select(.active == true) | {id: .id, name: .name}]' data.json

# Extract nested fields
jq '.[] | {name: .name, street: .address.street, city: .address.city}' data.json

# Get array of single field
jq '.[].name' users.json

# Filter with multiple conditions
jq '.[] | select(.age > 20 and .country == "USA")' users.json

# Map and transform values
jq '.[] | .price = (.price * 1.1)' products.json
```

**Node.js:**

```javascript
function filterAndExtractJSON(data, options) {
  const { filter, extract } = options;
  
  let result = Array.isArray(data) ? data : [data];
  
  // Apply filter function
  if (filter) {
    result = result.filter(filter);
  }
  
  // Extract specific fields
  if (extract) {
    result = result.map(item => {
      const extracted = {};
      extract.forEach(field => {
        // Support nested fields with dot notation
        const value = field.split('.').reduce((obj, key) => obj?.[key], item);
        extracted[field] = value;
      });
      return extracted;
    });
  }
  
  return result;
}

// Usage
// const users = [
//   { id: 1, name: 'Alice', age: 30, address: { city: 'NYC' } },
//   { id: 2, name: 'Bob', age: 25, address: { city: 'SF' } },
//   { id: 3, name: 'Charlie', age: 35, address: { city: 'LA' } }
// ];
// 
// const result = filterAndExtractJSON(users, {
//   filter: user => user.age > 25,
//   extract: ['name', 'age', 'address.city']
// });
// console.log(result);
```

### flatten_nested_json

Flatten nested JSON objects into flat structure.

```bash
# Flatten nested JSON with jq
jq '[.[] | {id: .id, name: .name, street: .address.street, city: .address.city, zip: .address.zip}]' users.json

# Flatten all nested fields with custom separator
jq '[.[] | to_entries | map({key: .key, value: .value}) | from_entries]' data.json

# Flatten deeply nested structure
jq 'recurse | select(type != "object" and type != "array")' complex.json
```

**Node.js:**

```javascript
function flattenJSON(obj, prefix = '', separator = '.') {
  const flattened = {};
  
  for (const key in obj) {
    const value = obj[key];
    const newKey = prefix ? `${prefix}${separator}${key}` : key;
    
    if (value !== null && typeof value === 'object' && !Array.isArray(value)) {
      // Recursively flatten nested objects
      Object.assign(flattened, flattenJSON(value, newKey, separator));
    } else if (Array.isArray(value)) {
      // Convert arrays to string or flatten each item
      flattened[newKey] = JSON.stringify(value);
    } else {
      flattened[newKey] = value;
    }
  }
  
  return flattened;
}

// Usage
// const nested = {
//   id: 1,
//   name: 'Alice',
//   address: {
//     street: '123 Main St',
//     city: 'NYC',
//     coordinates: { lat: 40.7, lon: -74.0 }
//   },
//   tags: ['user', 'active']
// };
// console.log(flattenJSON(nested));
// Output: {
//   id: 1,
//   name: 'Alice',
//   'address.street': '123 Main St',
//   'address.city': 'NYC',
//   'address.coordinates.lat': 40.7,
//   'address.coordinates.lon': -74.0,
//   tags: '["user","active"]'
// }
```

### transform_csv_data

Transform and manipulate CSV data.

```bash
# Select specific columns
csvcut -c name,email,age users.csv

# Filter rows by value
csvgrep -c age -r "^[3-9][0-9]$" users.csv  # age >= 30

# Sort CSV
csvsort -c age -r users.csv  # reverse sort by age

# Remove duplicate rows
csvcut -c name,email users.csv | uniq

# Combine: filter, select columns, sort
csvgrep -c country -m "USA" users.csv | csvcut -c name,age | csvsort -c age

# Add calculated column (requires csvpy or awk)
awk -F',' 'BEGIN{OFS=","} NR==1{print $0,"total"} NR>1{print $0,$2*$3}' data.csv

# Merge two CSV files by column
csvjoin -c id users.csv orders.csv
```

**Node.js:**

```javascript
function transformCSV(csvData, transformations) {
  const { selectColumns, filterRows, sortBy } = transformations;
  
  // Parse CSV to objects
  const data = csvToJSON(csvData);
  
  let result = data;
  
  // Filter rows
  if (filterRows) {
    result = result.filter(filterRows);
  }
  
  // Select columns
  if (selectColumns) {
    result = result.map(row => {
      const selected = {};
      selectColumns.forEach(col => {
        selected[col] = row[col];
      });
      return selected;
    });
  }
  
  // Sort
  if (sortBy) {
    const { column, reverse } = sortBy;
    result.sort((a, b) => {
      const aVal = a[column];
      const bVal = b[column];
      const comparison = aVal > bVal ? 1 : aVal < bVal ? -1 : 0;
      return reverse ? -comparison : comparison;
    });
  }
  
  // Convert back to CSV
  return jsonToCSV(result);
}

// Usage
// const csv = `name,age,country
// Alice,30,USA
// Bob,25,Canada
// Charlie,35,USA`;
//
// const transformed = transformCSV(csv, {
//   filterRows: row => row.country === 'USA',
//   selectColumns: ['name', 'age'],
//   sortBy: { column: 'age', reverse: true }
// });
// console.log(transformed);
```

### aggregate_and_group_json

Aggregate and group JSON data (similar to SQL GROUP BY).

```bash
# Group by field and count
jq 'group_by(.country) | map({country: .[0].country, count: length})' users.json

# Sum values by group
jq 'group_by(.category) | map({category: .[0].category, total: map(.price) | add})' products.json

# Average by group
jq 'group_by(.department) | map({department: .[0].department, avg_salary: (map(.salary) | add / length)})' employees.json

# Multiple aggregations
jq 'group_by(.region) | map({
  region: .[0].region,
  count: length,
  total_sales: map(.sales) | add,
  avg_sales: (map(.sales) | add / length)
})' sales.json
```

**Node.js:**

```javascript
function groupAndAggregate(data, groupBy, aggregations) {
  // Group data
  const grouped = {};
  data.forEach(item => {
    const key = item[groupBy];
    if (!grouped[key]) grouped[key] = [];
    grouped[key].push(item);
  });
  
  // Apply aggregations
  return Object.entries(grouped).map(([key, items]) => {
    const result = { [groupBy]: key };
    
    aggregations.forEach(agg => {
      if (agg.type === 'count') {
        result[agg.name] = items.length;
      } else if (agg.type === 'sum') {
        result[agg.name] = items.reduce((sum, item) => sum + (item[agg.field] || 0), 0);
      } else if (agg.type === 'avg') {
        const sum = items.reduce((s, item) => s + (item[agg.field] || 0), 0);
        result[agg.name] = items.length > 0 ? sum / items.length : 0;
      } else if (agg.type === 'min') {
        result[agg.name] = Math.min(...items.map(item => item[agg.field] || Infinity));
      } else if (agg.type === 'max') {
        result[agg.name] = Math.max(...items.map(item => item[agg.field] || -Infinity));
      }
    });
    
    return result;
  });
}

// Usage
// const sales = [
//   { region: 'East', product: 'A', amount: 100 },
//   { region: 'East', product: 'B', amount: 200 },
//   { region: 'West', product: 'A', amount: 150 },
//   { region: 'West', product: 'B', amount: 250 }
// ];
//
// const result = groupAndAggregate(sales, 'region', [
//   { name: 'count', type: 'count' },
//   { name: 'total_amount', type: 'sum', field: 'amount' },
//   { name: 'avg_amount', type: 'avg', field: 'amount' }
// ]);
// console.log(result);
```

## Rate limits / Best practices

- ✅ **Stream large files** — Use jq with `-c` flag and process line by line for large datasets
- ✅ **Validate data** — Check JSON/CSV format before transformation
- ✅ **Handle missing fields** — Use default values for null/undefined fields
- ✅ **Memory management** — For files >100MB, use streaming parsers
- ✅ **Type conversion** — Be aware of number/string conversions in CSV
- ✅ **Preserve data types** — JSON maintains types, CSV converts everything to strings
- ⚠️ **Character encoding** — Ensure UTF-8 encoding for international characters
- ⚠️ **Quote escaping** — Properly escape quotes in CSV values

## Agent prompt

```text
You have JSON and CSV data transformation capability. When a user asks to transform data:

1. Identify the input format:
   - JSON: Look for {...} or [...]
   - CSV: Look for comma-separated values with headers

2. For JSON to CSV:
   - Use jq with @csv filter: `jq -r '... | @csv'`
   - Or csvkit: `in2csv -f json`
   - Node.js: Convert array of objects to CSV string

3. For CSV to JSON:
   - Use csvjson from csvkit: `csvjson file.csv`
   - Node.js: Parse CSV headers and data rows into objects

4. For filtering/extracting:
   - Use jq select(): `jq '.[] | select(.age > 25)'`
   - Use csvkit csvgrep: `csvgrep -c column -m value`
   - Node.js: Use Array.filter() and map()

5. For flattening:
   - Flatten nested JSON objects into dot notation
   - Convert nested structures to tabular format
   - Handle arrays by stringifying or creating separate rows

6. For aggregation:
   - Use jq group_by(): `jq 'group_by(.field) | map({...})'`
   - CSV: Convert to JSON, aggregate, convert back
   - Node.js: Implement grouping and aggregation functions

Always:
- Preserve data integrity (no data loss)
- Handle edge cases (empty values, special characters)
- Validate output format matches expected structure
- For large files (>100MB), recommend streaming approaches
```

## Troubleshooting

**Error: "parse error: Invalid numeric literal"**
- Symptom: jq fails to parse JSON
- Solution: Validate JSON format with `jq empty file.json`, fix syntax errors

**CSV columns not aligned:**
- Symptom: Data appears in wrong columns after transformation
- Solution: Check for unescaped commas in data, ensure quotes are properly escaped

**Empty output from jq:**
- Symptom: jq returns no results
- Solution: Check filter expression syntax, verify data structure matches filter

**Special characters broken in CSV:**
- Symptom: Non-ASCII characters appear garbled
- Solution: Ensure UTF-8 encoding: `iconv -f UTF-8 -t UTF-8 file.csv`

**Memory error with large files:**
- Symptom: Process runs out of memory
- Solution: Use streaming mode: `jq -c` or Node.js streams for line-by-line processing

**JSON doesn't convert to flat CSV:**
- Symptom: Nested objects create complex CSV structure
- Solution: Flatten JSON first before converting to CSV

## See also

- [../database-query-and-export/SKILL.md](../database-query-and-export/SKILL.md) — Export database results as JSON/CSV
- [../web-search-api/SKILL.md](../web-search-api/SKILL.md) — Transform API responses to desired format
- [../using-web-scraping/SKILL.md](../using-web-scraping/SKILL.md) — Process scraped data into structured formats
