---
name: nushell
description: Guide for using Nushell for structured data pipelines and scripting. Use when writing shell scripts, processing structured data, or working with cross-platform automation.
---

# Nushell - Modern Structured Shell

This skill activates when working with Nushell (Nu), writing Nu scripts, working with structured data pipelines, or configuring the Nu environment.

## When to Use This Skill

Activate when:
- Writing Nushell scripts or commands
- Working with structured data in pipelines
- Converting from bash/zsh to Nushell
- Configuring Nushell environment
- Processing JSON, CSV, YAML, or other structured data
- Creating custom commands or modules

## What is Nushell?

Nushell is a modern shell that:
- Treats **data as structured** (not just text streams)
- Works **cross-platform** (Windows, macOS, Linux)
- Provides **clear error messages** and IDE support
- Combines **shell and programming language** features
- Has **built-in data format support** (JSON, CSV, YAML, TOML, XML, etc.)

## Installation

```bash
# macOS
brew install nushell

# Linux (cargo)
cargo install nu

# Windows
winget install nushell

# Or download from https://www.nushell.sh/
```

## Basic Concepts

### Everything is Data

Unlike traditional shells where everything is text, Nu works with structured data:

```nu
# Traditional shell (text output)
ls | grep ".txt"

# Nushell (structured data)
ls | where name =~ ".txt"
```

### Pipeline Philosophy

Data flows through pipelines as structured tables/records:

```nu
# Each command outputs structured data
ls | where size > 1kb | sort-by modified | reverse
```

## Data Types

### Basic Types

```nu
# Integers
42
-10

# Floats
3.14
-2.5

# Strings
"hello"
'world'

# Booleans
true
false

# Null
null
```

### Collections

```nu
# Lists
[1 2 3 4 5]
["apple" "banana" "cherry"]

# Records (like objects/dicts)
{name: "Alice", age: 30, city: "NYC"}

# Tables (list of records)
[
  {name: "Alice", age: 30}
  {name: "Bob", age: 25}
]
```

### Ranges

```nu
# Number ranges
1..10
1..2..10  # Step by 2

# Use in commands
1..5 | each { |i| $i * 2 }
```

## Working with Files and Directories

### Navigation

```nu
# Change directory
cd /path/to/dir

# List files (returns structured table)
ls

# List with details
ls | select name size modified

# Filter files
ls | where type == file
ls | where size > 1mb
ls | where name =~ "\.txt$"
```

### File Operations

```nu
# Create file
"hello" | save hello.txt

# Read file
open hello.txt

# Append to file
"world" | save -a hello.txt

# Copy
cp source.txt dest.txt

# Move/rename
mv old.txt new.txt

# Remove
rm file.txt
rm -r directory/

# Create directory
mkdir new-dir
```

### File Content

```nu
# Read as string
open file.txt

# Read structured data
open data.json
open config.toml
open data.csv

# Write structured data
{name: "Alice", age: 30} | to json | save user.json
[{a: 1} {a: 2}] | to csv | save data.csv
```

## Pipeline Operations

### Filtering

```nu
# Filter with where
ls | where size > 1mb
ls | where type == dir
ls | where name =~ "test"

# Multiple conditions
ls | where size > 1kb and type == file
```

### Selecting Columns

```nu
# Select specific columns
ls | select name size

# Rename columns
ls | select name size | rename file bytes
```

### Sorting

```nu
# Sort by column
ls | sort-by size
ls | sort-by modified

# Reverse sort
ls | sort-by size | reverse

# Multiple columns
ls | sort-by type size
```

### Transforming Data

```nu
# Map over items with each
1..5 | each { |i| $i * 2 }

# Update column
ls | update name { |row| $row.name | str upcase }

# Insert column
ls | insert size_kb { |row| $row.size / 1000 }

# Upsert (update or insert)
ls | upsert type_upper { |row| $row.type | str upcase }
```

### Aggregation

```nu
# Count items
ls | length

# Sum
[1 2 3 4 5] | math sum

# Average
[1 2 3 4 5] | math avg

# Min/Max
ls | get size | math max
ls | get size | math min

# Group by
ls | group-by type
```

## Variables

### Variable Assignment

```nu
# Let (immutable by default)
let name = "Alice"
let age = 30
let colors = ["red" "green" "blue"]

# Mut (mutable)
mut counter = 0
$counter = $counter + 1
```

### Using Variables

```nu
# Reference with $
let name = "Alice"
print $"Hello, ($name)!"

# In pipelines
let threshold = 1mb
ls | where size > $threshold
```

### Environment Variables

```nu
# Get environment variable
$env.PATH
$env.HOME

# Set environment variable
$env.MY_VAR = "value"

# Load from file
load-env { API_KEY: "secret" }
```

## String Operations

### String Interpolation

```nu
# String interpolation with ()
let name = "Alice"
print $"Hello, ($name)!"

# With expressions
let x = 5
print $"Result: (5 * $x)"
```

### String Methods

```nu
# Case conversion
"hello" | str upcase  # HELLO
"WORLD" | str downcase  # world

# Trimming
"  spaces  " | str trim

# Replace
"hello world" | str replace "world" "nu"

# Contains
"hello world" | str contains "world"  # true

# Split
"a,b,c" | split row ","
```

## Conditionals

### If Expressions

```nu
# If-else
if $age >= 18 {
  print "Adult"
} else {
  print "Minor"
}

# If-else if-else
if $score >= 90 {
  "A"
} else if $score >= 80 {
  "B"
} else {
  "C"
}

# Ternary-style with match
let status = if $is_active { "active" } else { "inactive" }
```

### Match (Pattern Matching)

```nu
# Match expression
match $value {
  1 => "one"
  2 => "two"
  _ => "other"
}

# With conditions
match $age {
  0..17 => "minor"
  18..64 => "adult"
  _ => "senior"
}
```

## Loops

### For Loop

```nu
# Loop over range
for i in 1..5 {
  print $i
}

# Loop over list
for name in ["Alice" "Bob" "Charlie"] {
  print $"Hello, ($name)"
}

# Loop over files
for file in (ls | where type == file) {
  print $file.name
}
```

### While Loop

```nu
# While loop
mut i = 0
while $i < 5 {
  print $i
  $i = $i + 1
}
```

### Each (Functional)

```nu
# Transform each item
1..5 | each { |i| $i * 2 }

# With index
["a" "b" "c"] | enumerate | each { |item|
  print $"($item.index): ($item.item)"
}
```

## Custom Commands

### Defining Commands

```nu
# Simple command
def greet [name: string] {
  print $"Hello, ($name)!"
}

greet "Alice"

# With return value
def add [a: int, b: int] {
  $a + $b
}

let result = add 5 3

# With default values
def greet [name: string = "World"] {
  print $"Hello, ($name)!"
}
```

### Command Parameters

```nu
# Required parameters
def copy [source: path, dest: path] {
  cp $source $dest
}

# Optional parameters
def greet [
  name: string
  --loud (-l)  # Flag
  --repeat (-r): int = 1  # Named parameter with default
] {
  let message = if $loud {
    $name | str upcase
  } else {
    $name
  }

  1..$repeat | each { print $"Hello, ($message)!" }
}

# Usage
greet "Alice"
greet "Bob" --loud
greet "Charlie" --repeat 3
```

### Pipeline Commands

```nu
# Accept pipeline input
def filter-large [] {
  where size > 1mb
}

# Usage
ls | filter-large

# Accept and transform pipeline
def double [] {
  each { |value| $value * 2 }
}

[1 2 3] | double
```

## Working with Structured Data

### JSON

```nu
# Read JSON
let data = open data.json

# Parse JSON string
let obj = '{"name": "Alice", "age": 30}' | from json

# Write JSON
{name: "Alice", age: 30} | to json | save user.json

# Pretty print JSON
{name: "Alice", age: 30} | to json -i 2
```

### CSV

```nu
# Read CSV
let data = open data.csv

# Convert to CSV
[{a: 1, b: 2} {a: 3, b: 4}] | to csv

# Save CSV
ls | select name size | to csv | save files.csv
```

### YAML/TOML

```nu
# Read YAML
let config = open config.yaml

# Read TOML
let config = open config.toml

# Write YAML
{key: "value"} | to yaml | save config.yaml

# Write TOML
{key: "value"} | to toml | save config.toml
```

### Working with Tables

```nu
# Create table
let users = [
  {name: "Alice", age: 30, city: "NYC"}
  {name: "Bob", age: 25, city: "LA"}
  {name: "Charlie", age: 35, city: "NYC"}
]

# Query table
$users | where age > 25
$users | where city == "NYC"
$users | select name age

# Add column
$users | insert country { "USA" }

# Group and count
$users | group-by city | transpose city users
```

## Modules

### Creating Modules

```nu
# utils.nu
export def greet [name: string] {
  print $"Hello, ($name)!"
}

export def add [a: int, b: int] {
  $a + $b
}
```

### Using Modules

```nu
# Import module
use utils.nu

# Use exported commands
utils greet "Alice"
utils add 5 3

# Import specific commands
use utils.nu [greet add]

greet "Alice"
add 5 3

# Import with alias
use utils.nu *
```

## Configuration

### Config File Location

```nu
# View config
config nu

# Edit config
config nu | open

# Config location
$nu.config-path
```

### Common Configurations

```nu
# config.nu
$env.config = {
  show_banner: false

  ls: {
    use_ls_colors: true
    clickable_links: true
  }

  table: {
    mode: rounded
    index_mode: auto
  }

  completions: {
    quick: true
    partial: true
  }

  history: {
    max_size: 10000
    sync_on_enter: true
    file_format: "sqlite"
  }
}
```

### Environment Setup

```nu
# env.nu
$env.PATH = ($env.PATH | split row (char esep) | append '/custom/bin')
$env.EDITOR = "nvim"

# Load completions
use completions/git.nu *
```

## Common Patterns

### File Processing

```nu
# Process all JSON files
ls *.json | each { |file|
  let data = open $file.name
  print $"Processing ($file.name): ($data | length) items"
}

# Batch rename files
ls *.txt | each { |file|
  let new_name = ($file.name | str replace ".txt" ".md")
  mv $file.name $new_name
}
```

### Data Transformation

```nu
# CSV to JSON
open data.csv | to json | save data.json

# Filter and transform
open users.json
| where active == true
| select name email
| to csv
| save active_users.csv

# Merge data
let users = open users.json
let orders = open orders.json
$users | merge $orders
```

### HTTP Requests

```nu
# GET request
http get https://api.example.com/users

# POST request
http post https://api.example.com/users {
  name: "Alice"
  email: "alice@example.com"
}

# With headers
http get -H [Authorization "Bearer token"] https://api.example.com/data
```

### System Commands

```nu
# Run external command
^ls -la

# Capture output
let output = (^git status)

# Check if command exists
which git

# Get command path
which git | get path
```

## Error Handling

### Try-Catch

```nu
# Try expression
try {
  open missing.txt
} catch {
  print "File not found"
}

# With error value
try {
  open missing.txt
} catch { |err|
  print $"Error: ($err)"
}
```

### Null Handling

```nu
# Default value
let value = ($env.MY_VAR? | default "default_value")

# Null propagation
let length = ($value | get name? | str length)
```

## Scripting

### Script Files

```nu
#!/usr/bin/env nu

# Script: process_logs.nu
# Description: Process log files and generate report

def main [log_dir: path] {
  let errors = (
    ls $"($log_dir)/*.log"
    | each { |file| open $file.name | lines }
    | flatten
    | where $it =~ "ERROR"
  )

  print $"Found ($errors | length) errors"
  $errors | save error_report.txt
}
```

Make executable:
```bash
chmod +x process_logs.nu
./process_logs.nu /var/log
```

### Script Parameters

```nu
# With parameters
def main [
  input: path
  --output (-o): path = "output.txt"
  --verbose (-v)
] {
  if $verbose {
    print $"Processing ($input)..."
  }

  let data = open $input
  $data | save $output

  if $verbose {
    print "Done!"
  }
}
```

## Comparison with Bash

### Common Operations

```bash
# Bash
find . -name "*.txt" | wc -l

# Nushell
ls **/*.txt | length
```

```bash
# Bash
cat file.json | jq '.users[] | select(.age > 25) | .name'

# Nushell
open file.json | get users | where age > 25 | get name
```

```bash
# Bash
for file in *.txt; do
  mv "$file" "${file%.txt}.md"
done

# Nushell
ls *.txt | each { |f| mv $f.name ($f.name | str replace ".txt" ".md") }
```

## Best Practices

- **Use structured data**: Leverage Nu's strength in handling structured data
- **Pipeline composition**: Build complex operations from simple pipeline stages
- **Type annotations**: Add types to custom command parameters for clarity
- **Error handling**: Use try-catch for operations that might fail
- **Modules for reuse**: Organize reusable commands in modules
- **Configuration**: Customize Nu to fit your workflow
- **External commands**: Use `^` prefix when calling external commands explicitly

## Common Pitfalls

### String vs Bare Words

```nu
# Bare word (interpreted as string in some contexts)
echo hello

# Explicit string (clearer)
echo "hello"
```

### External Commands

```nu
# Wrong - Nu tries to parse as Nu command
ls -la

# Right - Explicitly call external command
^ls -la
```

### Variable Scope

```nu
# Variables are scoped to blocks
if true {
  let x = 5
}
# $x not available here

# Use mut outside for wider scope
mut x = 0
if true {
  $x = 5
}
print $x  # Works
```

## Key Principles

- **Structured data first**: Think in terms of tables and records, not text
- **Pipeline composition**: Chain simple operations to build complex workflows
- **Type safety**: Leverage Nu's type system for reliable scripts
- **Cross-platform**: Write scripts that work on all platforms
- **Interactive and scriptable**: Same syntax works in REPL and scripts
- **Clear errors**: Nu provides helpful error messages for debugging
