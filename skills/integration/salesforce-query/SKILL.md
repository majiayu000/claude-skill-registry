---
name: salesforce-query
description: Query Salesforce data using natural language. Supports Accounts, Opportunities, Contacts, Leads, and Cases. Use when user asks to find, show, list, or retrieve Salesforce records.
argument-hint: [natural language query about Salesforce data]
allowed-tools: Bash(python:*), AskUserQuestion
---

# Salesforce Natural Language Query

Execute natural language queries against Salesforce and display results as formatted tables.

## Supported Objects
- **Account**: Companies and organizations
- **Opportunity**: Sales deals and opportunities
- **Contact**: Individual people
- **Lead**: Potential customers
- **Case**: Customer support cases

## How to Use This Skill

### Step 1: Get Credentials (First Query Only)
On the first query in a session, ask the user for:
1. **Instance URL**: Their Salesforce instance (e.g., `https://yourorg.my.salesforce.com`)
2. **Session ID**: Valid session token from Salesforce

**How to get Session ID**:
- Log into Salesforce
- Open Developer Console → Execute Anonymous
- Run: `System.debug(UserInfo.getSessionId());`
- Copy the session ID from debug logs

**Remember these credentials** for the entire chat session. Don't ask again unless they fail.

### Step 2: Understand the Query
Analyze the natural language query to:
- Identify which Salesforce object(s) are needed
- Determine filters, conditions, or relationships
- Identify if clarification is needed (ambiguous terms, missing context)

**If ambiguous**: Use AskUserQuestion to clarify before proceeding.

### Step 3: Fetch Object Schema
Use the describe.py script to fetch field metadata for needed objects.

**Command**:
```bash
python scripts/describe.py "<instance_url>" "<session_id>" "<ObjectName>"
```

**Intelligent field selection**: Only fetch schemas if you need to verify field names or understand relationships. For simple queries with common fields, you can skip this step.

**Common fields by object**:
- Account: Id, Name, Type, Industry, Phone, Website, BillingCity, BillingState, Owner.Name
- Opportunity: Id, Name, StageName, Amount, CloseDate, Probability, Account.Name, Owner.Name
- Contact: Id, Name, Email, Phone, Title, Account.Name, Department, Owner.Name
- Lead: Id, Name, Email, Status, Company, Phone, Industry, Owner.Name
- Case: Id, CaseNumber, Subject, Status, Priority, Origin, Account.Name, Contact.Name, Owner.Name

### Step 4: Generate SOQL Query
Translate the natural language query into SOQL using the schema information.

**SOQL Best Practices**:
- Always include `Id` in SELECT
- For related objects, use dot notation: `Account.Name`, `Owner.Name`
- Use proper WHERE clause syntax
- Date literals: `TODAY`, `THIS_WEEK`, `THIS_MONTH`, `THIS_QUARTER`, `THIS_YEAR`
- Comparison operators: `=`, `!=`, `>`, `<`, `>=`, `<=`, `LIKE`, `IN`
- Logical operators: `AND`, `OR`, `NOT`
- String values must be in single quotes: `'United Oil & Gas'`
- For partial matches use LIKE: `Name LIKE '%Oil%'`

**Common SOQL Patterns**:

*Find by name*:
```sql
SELECT Id, Name, Industry FROM Account WHERE Name LIKE '%Oil%'
```

*Find with related object*:
```sql
SELECT Id, Name, StageName, Amount, Account.Name
FROM Opportunity
WHERE Account.Name LIKE '%United Oil%'
```

*Date-based queries*:
```sql
SELECT Id, Name, CloseDate FROM Opportunity
WHERE CloseDate = THIS_QUARTER
```

*Multiple conditions*:
```sql
SELECT Id, Name, Amount FROM Opportunity
WHERE Amount > 100000 AND StageName = 'Negotiation'
```

*Order and limit*:
```sql
SELECT Id, Name, Amount FROM Opportunity
ORDER BY Amount DESC
LIMIT 10
```

### Step 5: Validate SOQL Syntax
Before executing, perform basic syntax validation:
- Check for balanced parentheses
- Verify SELECT, FROM are present
- Ensure field names look valid
- Check that string values are quoted

**If validation fails**: Fix the SOQL or ask for clarification.

### Step 6: Display SOQL to User
Show the generated SOQL to the user for transparency:

```
Generated SOQL:
SELECT Id, Name, StageName, Amount, CloseDate, Account.Name
FROM Opportunity
WHERE Account.Name LIKE '%United Oil & Gas%'
ORDER BY CloseDate DESC
```

### Step 7: Execute Query
Run the query using query.py script.

**Command**:
```bash
python scripts/query.py "<instance_url>" "<session_id>" "<SOQL_QUERY>"
```

**Important**: Make sure to properly escape the SOQL query string in the command line.

### Step 8: Format and Display Results
Parse the JSON response and format as a markdown table.

**For successful queries**:
- Show total count: `Found X records:`
- Create markdown table with relevant columns
- Always include Id and Name (if available)
- Include other fields from the SELECT clause
- Format numbers, dates appropriately
- Truncate long text fields if needed

**Example output**:
```markdown
Found 3 opportunities:

| Id | Name | Stage | Amount | Close Date | Account |
|---|---|---|---|---|---|
| 006xx01 | Platform Modernization | Prospecting | $250,000 | 2024-06-30 | United Oil & Gas |
| 006xx02 | Equipment Upgrade | Negotiation | $500,000 | 2024-08-15 | United Oil & Gas |
| 006xx03 | Safety System | Closed Won | $150,000 | 2024-03-01 | United Oil & Gas |
```

**For empty results**:
```
No records found matching your query.
```

**For errors**:
- Explain what went wrong
- Show the error message from Salesforce
- Suggest corrections if applicable

## Error Handling

### Authentication Errors (401)
- Session ID expired or invalid
- Ask user for new credentials

### SOQL Syntax Errors
- Show the error message
- Explain what's wrong
- Suggest corrected SOQL

### Field Not Found Errors
- The field doesn't exist on the object
- Fetch schema to verify available fields
- Regenerate SOQL with correct fields

### No Results
- Query is valid but returned no records
- Simply state "No records found"
- Don't auto-retry unless user asks

## Advanced Query Patterns

### Querying Related Records
```sql
-- Opportunities with Account details
SELECT Id, Name, Amount, Account.Name, Account.Industry
FROM Opportunity

-- Contacts with Account details
SELECT Id, Name, Email, Account.Name, Account.Type
FROM Contact
```

### Aggregations (if needed)
```sql
-- Count opportunities by stage
SELECT StageName, COUNT(Id)
FROM Opportunity
GROUP BY StageName

-- Sum of amounts
SELECT SUM(Amount)
FROM Opportunity
WHERE StageName = 'Closed Won'
```

### Subqueries
```sql
-- Opportunities for specific accounts
SELECT Id, Name, Amount
FROM Opportunity
WHERE AccountId IN (
  SELECT Id FROM Account WHERE Industry = 'Technology'
)
```

## Example Interactions

### Example 1: Simple Query
```
User: /salesforce-query show me all accounts in California

Claude: [If first query, asks for credentials]
Claude: Generated SOQL:
SELECT Id, Name, Type, Industry, Phone, BillingCity, BillingState
FROM Account
WHERE BillingState = 'CA'

Claude: [Executes and shows table]
```

### Example 2: Complex Query with Relationships
```
User: /salesforce-query show high-value opportunities closing this quarter

Claude: Generated SOQL:
SELECT Id, Name, StageName, Amount, CloseDate, Account.Name, Owner.Name
FROM Opportunity
WHERE Amount > 100000
AND CloseDate = THIS_QUARTER
ORDER BY Amount DESC

Claude: [Executes and shows table]
```

### Example 3: Ambiguous Query
```
User: /salesforce-query find John

Claude: I need clarification:
- Are you looking for a Contact, Lead, or Account named John?
- Should I search in the name field, or also email?
- Do you want exact match or partial match?
```

## Tips for Accurate Results

1. **Be specific**: "Show opportunities for United Oil & Gas" is better than "show opportunities"
2. **Use proper object names**: "accounts" not "companies", "opportunities" not "deals"
3. **Specify timeframes**: "this month", "this quarter", "last year"
4. **Include sorting/limits**: "top 10 by amount", "most recent cases"
5. **Clarify relationships**: "contacts from California accounts" vs "California contacts"

## Limitations

- Query timeout: 2 minutes maximum
- Result limit: 2000 records maximum (pagination handled automatically)
- Objects: Limited to Account, Opportunity, Contact, Lead, Case
- Custom fields: Supported but must exist in your org
- SOSL: Not supported (only SOQL)

## Troubleshooting

**Script not found errors**: Ensure Python scripts exist at:
- `scripts/describe.py`
- `scripts/query.py`

**Module not found errors**: Install dependencies:
```bash
pip install requests
```

**Permission errors**: Ensure user's profile has read access to the queried objects

---

**Ready to query Salesforce!** Provide your natural language query and I'll handle the rest.
