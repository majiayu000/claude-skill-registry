---
name: dst-subjects
description: Browse Danmarks Statistik subject hierarchy to explore available data topics and categories. Use when user wants to discover what data is available or explore DST's organizational structure.
---

# DST Subjects Skill

## Purpose

Browse DST's subject hierarchy to discover available data topics and understand how Statistics Denmark organizes its data. This is the starting point for exploring what data is available in the DST database.

## When to Use

- User wants to explore available data categories
- User asks "what data is available?"
- User needs to find relevant subjects for their analysis
- User wants to understand DST's organizational structure
- Starting point for data discovery workflow

## How to Use

### Basic Usage

Get all top-level subjects:
```bash
python scripts/api/get_subjects.py
```

### Get Complete Hierarchy

Get all subject levels recursively:
```bash
python scripts/api/get_subjects.py --recursive
```

### Save to File

Save results to a JSON file:
```bash
python scripts/api/get_subjects.py --output subjects.json
```

## Expected Output

The script returns a JSON array of subject objects. Each subject contains:

- **id**: Subject identifier (needed for finding tables)
- **description**: Human-readable topic name
- **active**: Whether subject is currently active
- **hasSubjects**: Indicates if there are sub-subjects
- **subjects**: Nested array of sub-subjects (if using --recursive)
- **tables**: Array of tables in this subject (if DST API called with includeTables)

Example output (basic):
```json
[
  {
    "id": "02",
    "description": "Population and elections",
    "active": true,
    "hasSubjects": true
  },
  {
    "id": "03",
    "description": "Labour, income and wealth",
    "active": true,
    "hasSubjects": true
  }
]
```

Example output (recursive):
```json
[
  {
    "id": "02",
    "description": "Population and elections",
    "active": true,
    "hasSubjects": true,
    "subjects": [
      {
        "id": "02.01",
        "description": "Population",
        "active": true,
        "hasSubjects": false
      }
    ]
  }
]
```

## Key Information to Extract

When browsing subjects, note:

1. **Subject ID**: You'll need this to find tables in that subject area
2. **Description**: The topic or category name
3. **Hierarchy**: How subjects are organized (when using --recursive)
4. **Active status**: Whether the subject is currently maintained

### Subject Hierarchy Structure

DST organizes data in up to 3 levels:
- **Level 1**: Top-level subjects (IDs: 1-9, 19) - 10 total
- **Level 2**: Sub-subjects within each topic
- **Level 3**: Detailed categories

Total catalog size:
- 10 top-level subjects
- ~100+ sub-subjects
- 5,542 total tables across all subjects
- Full recursive response: ~1.3 MB

## Next Steps

After identifying a relevant subject:

1. Note the subject ID (e.g., "02" for Labour)
2. Use the **dst-tables** skill to find tables within that subject
3. Example: `python scripts/api/get_tables.py --subject 02`

## Examples

### Example 1: Browse top-level subjects
```bash
python scripts/api/get_subjects.py
```
Output: 10 top-level categories with IDs and descriptions

### Example 2: Get complete hierarchy (all 3 levels)
```bash
python scripts/api/get_subjects.py --recursive
```
Output: Full tree structure with all sub-subjects (1.3 MB response)

### Example 3: Save to file for offline reference
```bash
python scripts/api/get_subjects.py --recursive --output subjects.json
```
Recommended: Cache locally to avoid repeated API calls

### Example 4: Quick lookup workflow
```bash
# Step 1: Get overview
python scripts/api/get_subjects.py

# Step 2: Identify relevant subject (e.g., subject "2" for labour)
# Step 3: Find tables in that subject
python scripts/api/get_tables.py --subject 2
```

## Troubleshooting

### Slow Response
- Full recursive call takes 500+ ms
- Expected for complete catalog (1.3 MB)
- Use non-recursive mode for faster results
- Cache results locally to avoid repeated calls

### Understanding Hierarchy
- Top level gives broad categories
- Use --recursive to see detailed breakdown
- Not all subjects have sub-subjects
- Check `"hasSubjects"` field to know if deeper levels exist

### Subject Not Found
- Verify subject ID format
- Check if using active subjects only
- Some subjects may be inactive/discontinued
- API returns empty array if no matching subjects

## Tips

### Navigation Strategy
- **Start simple**: Use non-recursive mode first to see top-level subjects
- **Use recursive**: When you need to understand the complete organizational structure
- **Browse by topic**: Look at descriptions to find relevant area
- **Note the IDs**: Subject IDs needed for next step (finding tables)

### Understanding Subject IDs
- **Top-level**: Single digit or two-digit (1-9, 19)
- **Sub-level**: Dotted notation like "02.01" (though DST uses various formats)
- **Consistent**: IDs remain stable over time
- **Language-independent**: Same IDs work for Danish and English

### Performance & Caching
- **Response time**: 106ms (basic) to 542ms (full recursive)
- **Response size**:
  - Basic (top-level): ~900 bytes
  - Full recursive: ~1.3 MB
- **Cacheable**: Subject structure rarely changes, cache for 24 hours
- **Save for reference**: Use `--output` to cache hierarchy locally

### Browsing Tips
- Start with top-level to get overview
- Use recursive when you need complete picture
- Subject descriptions available in both Danish and English
- Look for relevant keywords in descriptions

## Common Subjects (Reference)

Top-level DST subject categories (verified from API):
- **1**: Population and elections
- **2**: Labour and income
- **3**: Social services and justice
- **4**: Education and knowledge
- **5**: Culture and Church
- **6**: Housing and construction
- **7**: Elections
- **8**: Prices and consumption
- **9**: National accounts and business
- **19**: Various/Cross-cutting topics

Note: Exact subject IDs and descriptions retrieved via API may vary by language (Danish vs English).

### Finding Specific Topics

Common topic mappings:
- **Population data**: Subject 1 (Population and elections)
- **Employment/Labour**: Subject 2 (Labour and income)
- **Housing**: Subject 6 (Housing and construction)
- **Prices/Inflation**: Subject 8 (Prices and consumption)
- **Business/Economy**: Subject 9 (National accounts)
- **Education**: Subject 4 (Education and knowledge)

Use recursive mode to see detailed sub-categories within each top-level subject.
