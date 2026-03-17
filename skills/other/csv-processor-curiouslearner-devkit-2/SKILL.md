---
name: csv-processor
description: Parse, transform, and analyze CSV files with advanced data manipulation capabilities.
---

# CSV Processor Skill

Parse, transform, and analyze CSV files with advanced data manipulation capabilities.

## Instructions

You are a CSV processing expert. When invoked:

1. **Parse CSV Files**:
   - Auto-detect delimiters (comma, tab, semicolon, pipe)
   - Handle different encodings (UTF-8, Latin-1, Windows-1252)
   - Process quoted fields and escaped characters
   - Handle multi-line fields correctly
   - Detect and use header rows

2. **Transform Data**:
   - Filter rows based on conditions
   - Select specific columns
   - Sort and group data
   - Merge multiple CSV files
   - Split large files into smaller chunks
   - Pivot and unpivot data

3. **Clean Data**:
   - Remove duplicates
   - Handle missing values
   - Trim whitespace
   - Normalize data formats
   - Fix encoding issues
   - Validate data types

4. **Analyze Data**:
   - Generate statistics (sum, average, min, max, count)
   - Identify data quality issues
   - Detect outliers
   - Profile column data types
   - Calculate distributions

## Usage Examples

```
@csv-processor data.csv
@csv-processor --filter "age > 30"
@csv-processor --select "name,email,age"
@csv-processor --merge file1.csv file2.csv
@csv-processor --stats
@csv-processor --clean --remove-duplicates
```

## Basic CSV Operations

### Reading CSV Files

#### Python (pandas)
```python
import pandas as pd

# Basic read
df = pd.read_csv('data.csv')

# Custom delimiter
df = pd.read_csv('data.tsv', delimiter='\t')

# Specify encoding
df = pd.read_csv('data.csv', encoding='latin-1')

# Skip rows
df = pd.read_csv('data.csv', skiprows=2)

# Select specific columns
df = pd.read_csv('data.csv', usecols=['name', 'email', 'age'])

# Parse dates
df = pd.read_csv('data.csv', parse_dates=['created_at', 'updated_at'])

# Handle missing values
df = pd.read_csv('data.csv', na_values=['NA', 'N/A', 'null', ''])

# Specify data types
df = pd.read_csv('data.csv', dtype={
    'user_id': int,
    'age': int,
    'score': float,
    'active': bool
})
```

#### JavaScript (csv-parser)
```javascript
const fs = require('fs');
const csv = require('csv-parser');

// Basic parsing
const results = [];
fs.createReadStream('data.csv')
  .pipe(csv())
  .on('data', (row) => {
    results.push(row);
  })
  .on('end', () => {
    console.log(`Processed ${results.length} rows`);
  });

// With custom options
const Papa = require('papaparse');

Papa.parse(fs.createReadStream('data.csv'), {
  header: true,
  delimiter: ',',
  skipEmptyLines: true,
  transformHeader: (header) => header.trim().toLowerCase(),
  complete: (results) => {
    console.log('Parsed:', results.data);
  }
});
```

#### Python (csv module)
```python
import csv

# Basic reading
with open('data.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        print(row['name'], row['age'])

# Custom delimiter
with open('data.csv', 'r') as file:
    reader = csv.reader(file, delimiter='\t')
    for row in reader:
        print(row)

# Handle different dialects
with open('data.csv', 'r') as file:
    dialect = csv.Sniffer().sniff(file.read(1024))
    file.seek(0)
    reader = csv.reader(file, dialect)
    for row in reader:
        print(row)
```

### Writing CSV Files

#### Python (pandas)
```python
# Basic write
df.to_csv('output.csv', index=False)

# Custom delimiter
df.to_csv('output.tsv', sep='\t', index=False)

# Specify encoding
df.to_csv('output.csv', encoding='utf-8-sig', index=False)

# Write only specific columns
df[['name', 'email']].to_csv('output.csv', index=False)

# Append to existing file
df.to_csv('output.csv', mode='a', header=False, index=False)

# Quote all fields
df.to_csv('output.csv', quoting=csv.QUOTE_ALL, index=False)
```

#### JavaScript (csv-writer)
```javascript
const createCsvWriter = require('csv-writer').createObjectCsvWriter;

const csvWriter = createCsvWriter({
  path: 'output.csv',
  header: [
    {id: 'name', title: 'Name'},
    {id: 'email', title: 'Email'},
    {id: 'age', title: 'Age'}
  ]
});

const records = [
  {name: 'John Doe', email: 'john@example.com', age: 30},
  {name: 'Jane Smith', email: 'jane@example.com', age: 25}
];

csvWriter.writeRecords(records)
  .then(() => console.log('CSV file written successfully'));
```

## Data Transformation Patterns

### Filtering Rows

#### Python (pandas)
```python
# Single condition
filtered = df[df['age'] > 30]

# Multiple conditions (AND)
filtered = df[(df['age'] > 30) & (df['country'] == 'USA')]

# Multiple conditions (OR)
filtered = df[(df['age'] < 18) | (df['age'] > 65)]

# String operations
filtered = df[df['email'].str.contains('@gmail.com')]
filtered = df[df['name'].str.startswith('John')]

# Is in list
filtered = df[df['country'].isin(['USA', 'Canada', 'Mexico'])]

# Not null values
filtered = df[df['email'].notna()]

# Complex conditions
filtered = df.query('age > 30 and country == "USA" and active == True')
```

#### JavaScript
```javascript
// Filter with arrow function
const filtered = data.filter(row => row.age > 30);

// Multiple conditions
const filtered = data.filter(row =>
  row.age > 30 && row.country === 'USA'
);

// String operations
const filtered = data.filter(row =>
  row.email.includes('@gmail.com')
);

// Complex filtering
const filtered = data.filter(row => {
  const age = parseInt(row.age);
  return age >= 18 && age <= 65 && row.active === 'true';
});
```

### Selecting Columns

#### Python (pandas)
```python
# Select single column
names = df['name']

# Select multiple columns
subset = df[['name', 'email', 'age']]

# Select by column type
numeric_cols = df.select_dtypes(include=['int64', 'float64'])
string_cols = df.select_dtypes(include=['object'])

# Select columns matching pattern
email_cols = df.filter(regex='.*email.*')

# Drop columns
df_without = df.drop(['temporary', 'unused'], axis=1)

# Rename columns
df_renamed = df.rename(columns={
    'old_name': 'new_name',
    'email_address': 'email'
})
```

#### JavaScript
```javascript
// Map to select columns
const subset = data.map(row => ({
  name: row.name,
  email: row.email,
  age: row.age
}));

// Destructuring
const subset = data.map(({name, email, age}) => ({name, email, age}));

// Dynamic column selection
const columns = ['name', 'email', 'age'];
const subset = data.map(row =>
  Object.fromEntries(
    columns.map(col => [col, row[col]])
  )
);
```

### Sorting Data

#### Python (pandas)
```python
# Sort by single column
sorted_df = df.sort_values('age')

# Sort descending
sorted_df = df.sort_values('age', ascending=False)

# Sort by multiple columns
sorted_df = df.sort_values(['country', 'age'], ascending=[True, False])

# Sort by index
sorted_df = df.sort_index()
```

#### JavaScript
```javascript
// Sort by single field
const sorted = data.sort((a, b) => a.age - b.age);

// Sort descending
const sorted = data.sort((a, b) => b.age - a.age);

// Sort by string
const sorted = data.sort((a, b) => a.name.localeCompare(b.name));

// Sort by multiple fields
const sorted = data.sort((a, b) => {
  if (a.country !== b.country) {
    return a.country.localeCompare(b.country);
  }
  return b.age - a.age;
});
```

### Grouping and Aggregation

#### Python (pandas)
```python
# Group by single column
grouped = df.groupby('country')

# Count by group
counts = df.groupby('country').size()

# Multiple aggregations
stats = df.groupby('country').agg({
    'age': ['mean', 'min', 'max'],
    'salary': ['sum', 'mean'],
    'user_id': 'count'
})

# Group by multiple columns
grouped = df.groupby(['country', 'city']).agg({
    'revenue': 'sum',
    'user_id': 'count'
})

# Custom aggregation
df.groupby('country').apply(lambda x: x['salary'].max() - x['salary'].min())

# Pivot table
pivot = df.pivot_table(
    values='revenue',
    index='country',
    columns='year',
    aggfunc='sum',
    fill_value=0
)
```

#### JavaScript (lodash)
```javascript
const _ = require('lodash');

// Group by field
const grouped = _.groupBy(data, 'country');

// Count by group
const counts = _.mapValues(
  _.groupBy(data, 'country'),
  group => group.length
);

// Sum by group
const sums = _.mapValues(
  _.groupBy(data, 'country'),
  group => _.sumBy(group, row => parseFloat(row.salary))
);

// Multiple aggregations
const stats = Object.entries(_.groupBy(data, 'country')).map(([country, rows]) => ({
  country,
  count: rows.length,
  avgAge: _.meanBy(rows, row => parseInt(row.age)),
  totalSalary: _.sumBy(rows, row => parseFloat(row.salary))
}));
```

### Merging CSV Files

#### Python (pandas)
```python
# Concatenate vertically (stack rows)
df1 = pd.read_csv('file1.csv')
df2 = pd.read_csv('file2.csv')
combined = pd.concat([df1, df2], ignore_index=True)

# Join (SQL-like merge)
users = pd.read_csv('users.csv')
orders = pd.read_csv('orders.csv')

# Inner join
merged = pd.merge(users, orders, on='user_id', how='inner')

# Left join
merged = pd.merge(users, orders, on='user_id', how='left')

# Multiple keys
merged = pd.merge(
    users, orders,
    left_on='id',
    right_on='user_id',
    how='left'
)

# Merge with different column names
merged = pd.merge(
    users, orders,
    left_on='user_id',
    right_on='customer_id',
    how='inner'
)
```

#### JavaScript
```javascript
// Concatenate arrays
const file1 = parseCSV('file1.csv');
const file2 = parseCSV('file2.csv');
const combined = [...file1, ...file2];

// Join arrays (like SQL)
function leftJoin(left, right, leftKey, rightKey) {
  return left.map(leftRow => {
    const rightRow = right.find(r => r[rightKey] === leftRow[leftKey]);
    return {...leftRow, ...rightRow};
  });
}

const merged = leftJoin(users, orders, 'id', 'user_id');
```

## Data Cleaning Operations

### Remove Duplicates

#### Python (pandas)
```python
# Remove duplicate rows
df_unique = df.drop_duplicates()

# Based on specific columns
df_unique = df.drop_duplicates(subset=['email'])

# Keep first or last occurrence
df_unique = df.drop_duplicates(subset=['email'], keep='first')
df_unique = df.drop_duplicates(subset=['email'], keep='last')

# Identify duplicates
duplicates = df[df.duplicated()]
duplicate_emails = df[df.duplicated(subset=['email'])]
```

### Handle Missing Values

#### Python (pandas)
```python
# Check for missing values
missing_count = df.isnull().sum()
missing_percent = (df.isnull().sum() / len(df)) * 100

# Drop rows with any missing values
df_clean = df.dropna()

# Drop rows where specific column is missing
df_clean = df.dropna(subset=['email'])

# Drop columns with too many missing values
df_clean = df.dropna(axis=1, thresh=len(df)*0.7)

# Fill missing values
df_filled = df.fillna(0)
df_filled = df.fillna({'age': 0, 'country': 'Unknown'})

# Forward fill
df_filled = df.fillna(method='ffill')

# Fill with mean/median
df['age'].fillna(df['age'].mean(), inplace=True)
df['age'].fillna(df['age'].median(), inplace=True)

# Interpolate
df['value'].interpolate(method='linear', inplace=True)
```

#### JavaScript
```javascript
// Filter out rows with missing values
const cleaned = data.filter(row =>
  row.email && row.name && row.age
);

// Fill missing values
const filled = data.map(row => ({
  ...row,
  age: row.age || 0,
  country: row.country || 'Unknown'
}));
```

### Data Validation

#### Python (pandas)
```python
# Validate email format
import re
email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
df['email_valid'] = df['email'].str.match(email_pattern)

# Validate age range
df['age_valid'] = df['age'].between(0, 120)

# Validate required fields
df['valid'] = df[['name', 'email', 'age']].notna().all(axis=1)

# Check data types
def validate_types(df):
    errors = []

    # Check numeric columns
    for col in ['age', 'salary', 'score']:
        if col in df.columns:
            if not pd.api.types.is_numeric_dtype(df[col]):
                errors.append(f"{col} should be numeric")

    # Check date columns
    for col in ['created_at', 'updated_at']:
        if col in df.columns:
            try:
                pd.to_datetime(df[col])
            except:
                errors.append(f"{col} has invalid dates")

    return errors

# Remove invalid rows
df_valid = df[df['email_valid'] & df['age_valid']]
```

### Data Normalization

#### Python (pandas)
```python
# Trim whitespace
df['name'] = df['name'].str.strip()
df['email'] = df['email'].str.strip()

# Convert to lowercase
df['email'] = df['email'].str.lower()

# Standardize phone numbers
df['phone'] = df['phone'].str.replace(r'[^0-9]', '', regex=True)

# Standardize dates
df['created_at'] = pd.to_datetime(df['created_at'])

# Standardize country names
country_mapping = {
    'USA': 'United States',
    'US': 'United States',
    'United States of America': 'United States',
    'UK': 'United Kingdom'
}
df['country'] = df['country'].replace(country_mapping)

# Convert data types
df['age'] = pd.to_numeric(df['age'], errors='coerce')
df['active'] = df['active'].astype(bool)
df['score'] = df['score'].astype(float)
```

## Data Analysis Operations

### Statistical Summary

#### Python (pandas)
```python
# Basic statistics
print(df.describe())

# Statistics for all columns (including non-numeric)
print(df.describe(include='all'))

# Specific statistics
print(f"Mean age: {df['age'].mean()}")
print(f"Median age: {df['age'].median()}")
print(f"Std dev: {df['age'].std()}")
print(f"Min: {df['age'].min()}")
print(f"Max: {df['age'].max()}")

# Count values
print(df['country'].value_counts())

# Percentage distribution
print(df['country'].value_counts(normalize=True) * 100)

# Cross-tabulation
cross_tab = pd.crosstab(df['country'], df['active'])

# Correlation matrix
correlation = df[['age', 'salary', 'score']].corr()
```

### Data Profiling

#### Python (pandas)
```python
def profile_dataframe(df):
    """Generate comprehensive data profile"""

    profile = {
        'shape': df.shape,
        'columns': list(df.columns),
        'dtypes': df.dtypes.to_dict(),
        'memory_usage': df.memory_usage(deep=True).sum() / 1024**2,  # MB
        'missing_values': df.isnull().sum().to_dict(),
        'missing_percent': (df.isnull().sum() / len(df) * 100).to_dict(),
        'duplicates': df.duplicated().sum(),
        'numeric_summary': df.describe().to_dict(),
        'unique_counts': df.nunique().to_dict()
    }

    # Column-specific analysis
    for col in df.columns:
        profile[f'{col}_sample'] = df[col].head(5).tolist()

        if df[col].dtype == 'object':
            profile[f'{col}_top_values'] = df[col].value_counts().head(10).to_dict()

        if pd.api.types.is_numeric_dtype(df[col]):
            profile[f'{col}_outliers'] = detect_outliers(df[col])

    return profile

def detect_outliers(series):
    """Detect outliers using IQR method"""
    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outliers = series[(series < lower_bound) | (series > upper_bound)]
    return {
        'count': len(outliers),
        'percent': (len(outliers) / len(series)) * 100,
        'values': outliers.tolist()
    }
```

### Generate Report

```python
def generate_csv_report(df, filename='report.md'):
    """Generate comprehensive analysis report"""

    report = f"""# CSV Analysis Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Dataset Overview
- **Rows**: {len(df):,}
- **Columns**: {len(df.columns)}
- **Memory Usage**: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB
- **Duplicates**: {df.duplicated().sum():,}

## Column Summary

| Column | Type | Non-Null | Unique | Missing % |
|--------|------|----------|--------|-----------|
"""

    for col in df.columns:
        dtype = str(df[col].dtype)
        non_null = df[col].count()
        unique = df[col].nunique()
        missing_pct = (df[col].isnull().sum() / len(df)) * 100

        report += f"| {col} | {dtype} | {non_null:,} | {unique:,} | {missing_pct:.1f}% |\n"

    report += "\n## Numeric Columns Statistics\n\n"
    report += df.describe().to_markdown()

    report += "\n\n## Data Quality Issues\n\n"

    # Missing values
    missing = df.isnull().sum()
    if missing.sum() > 0:
        report += "### Missing Values\n"
        for col, count in missing[missing > 0].items():
            pct = (count / len(df)) * 100
            report += f"- **{col}**: {count:,} ({pct:.1f}%)\n"

    # Duplicates
    if df.duplicated().sum() > 0:
        report += f"\n### Duplicates\n"
        report += f"- Found {df.duplicated().sum():,} duplicate rows\n"

    # Write report
    with open(filename, 'w') as f:
        f.write(report)

    print(f"Report generated: {filename}")
```

## Advanced Operations

### Splitting Large CSV Files

```python
def split_csv(input_file, rows_per_file=10000):
    """Split large CSV into smaller chunks"""

    chunk_num = 0

    for chunk in pd.read_csv(input_file, chunksize=rows_per_file):
        output_file = f"{input_file.rsplit('.', 1)[0]}_part{chunk_num}.csv"
        chunk.to_csv(output_file, index=False)
        print(f"Created {output_file} with {len(chunk)} rows")
        chunk_num += 1
```

### Pivot and Unpivot

```python
# Pivot (wide format)
pivot = df.pivot_table(
    values='revenue',
    index='product',
    columns='month',
    aggfunc='sum'
)

# Unpivot (long format)
melted = df.melt(
    id_vars=['product', 'category'],
    value_vars=['jan', 'feb', 'mar'],
    var_name='month',
    value_name='revenue'
)
```

### Data Type Conversion

```python
# Convert columns
df['age'] = pd.to_numeric(df['age'], errors='coerce')
df['created_at'] = pd.to_datetime(df['created_at'])
df['active'] = df['active'].astype(bool)

# Parse custom date formats
df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')

# Handle mixed types
df['mixed'] = df['mixed'].astype(str)
```

## Performance Optimization

### Reading Large Files Efficiently

```python
# Read in chunks
chunk_size = 10000
chunks = []

for chunk in pd.read_csv('large_file.csv', chunksize=chunk_size):
    # Process chunk
    processed = chunk[chunk['active'] == True]
    chunks.append(processed)

result = pd.concat(chunks, ignore_index=True)

# Read only needed columns
df = pd.read_csv('large_file.csv', usecols=['name', 'email', 'age'])

# Use appropriate dtypes
df = pd.read_csv('large_file.csv', dtype={
    'id': 'int32',  # instead of int64
    'age': 'int8',  # small integers
    'category': 'category'  # categorical data
})
```

### Writing Large Files

```python
# Write in chunks
chunk_size = 10000

for i in range(0, len(df), chunk_size):
    chunk = df.iloc[i:i+chunk_size]
    mode = 'w' if i == 0 else 'a'
    header = i == 0
    chunk.to_csv('output.csv', mode=mode, header=header, index=False)
```

## Command Line Tools

### Using csvkit
```bash
# View CSV structure
csvcut -n data.csv

# Filter columns
csvcut -c name,email,age data.csv > subset.csv

# Filter rows
csvgrep -c age -r "^[3-9][0-9]$" data.csv > age_30plus.csv

# Convert to JSON
csvjson data.csv > data.json

# Statistics
csvstat data.csv

# SQL queries on CSV
csvsql --query "SELECT country, COUNT(*) FROM data GROUP BY country" data.csv
```

### Using awk
```bash
# Print specific columns
awk -F',' '{print $1, $3}' data.csv

# Filter rows
awk -F',' '$3 > 30' data.csv

# Sum column
awk -F',' '{sum+=$3} END {print sum}' data.csv
```

## Best Practices

1. **Always validate data** before processing
2. **Use appropriate data types** to save memory
3. **Handle encoding issues** early in the process
4. **Profile data first** to understand structure
5. **Use chunks** for large files
6. **Back up original files** before transformations
7. **Document transformations** for reproducibility
8. **Validate output** after processing
9. **Use version control** for CSV processing scripts
10. **Test with sample data** before processing full datasets

## Common Issues and Solutions

### Issue: Encoding Errors
```python
# Try different encodings
for encoding in ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']:
    try:
        df = pd.read_csv('data.csv', encoding=encoding)
        print(f"Success with encoding: {encoding}")
        break
    except UnicodeDecodeError:
        continue
```

### Issue: Delimiter Detection
```python
# Auto-detect delimiter
with open('data.csv', 'r') as file:
    sample = file.read(1024)
    sniffer = csv.Sniffer()
    delimiter = sniffer.sniff(sample).delimiter

df = pd.read_csv('data.csv', delimiter=delimiter)
```

### Issue: Memory Errors
```python
# Use chunking
chunks = []
for chunk in pd.read_csv('large.csv', chunksize=10000):
    # Process and filter
    processed = chunk[chunk['keep'] == True]
    chunks.append(processed)

df = pd.concat(chunks, ignore_index=True)
```

## Notes

- Always inspect CSV structure before processing
- Test transformations on a small sample first
- Consider using databases for very large datasets
- Document column meanings and data types
- Use consistent date and number formats
- Validate data quality regularly
- Keep processing scripts version controlled
