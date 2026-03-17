---
name: nango-dry-run
description: Use when testing Nango syncs locally - runs dry-run command with proper parameters for integration testing without affecting production data
---

# Nango Dry Run Testing

## Overview

Test Nango sync jobs locally using the `nango dryrun` command to verify sync logic, data mapping, and API integration without persisting data to the database.

## When to Use

- Testing sync changes before deployment
- Debugging data mapping issues
- Verifying API integration works correctly
- Checking manager resolution or relationship logic
- Validating incremental sync behavior

## Quick Reference

| Task | Command |
|------|---------|
| Run sync locally | `npx nango dryrun <sync-name> <connection-id> --integration-id <provider> -e <env>` |
| Test employees sync | `npx nango dryrun employees <connection-id> --integration-id <provider> -e prod` |
| Short-circuit for faster testing | Add `if (page > 2) break;` in sync loop |

## Command Structure

```bash
cd nango-integrations
npx nango dryrun <sync-name> <connection-id> --integration-id <provider> -e <environment>
```

**Parameters:**
- `<sync-name>`: Name of sync endpoint (e.g., `employees`, `locations`, `departments`)
- `<connection-id>`: UUID of the Nango connection to test with
- `--integration-id`: Provider identifier (e.g., `workday`, `adp`, `gusto`)
- `-e <environment>`: Environment (e.g., `prod`, `dev`, `staging`)

**Example:**
```bash
npx nango dryrun employees <connection-id> \
  --integration-id workday -e prod
```

## Faster Testing with Short-Circuit

For large datasets, add temporary short-circuit to test faster:

```typescript
// ✅ GOOD - In sync loop before processing
do {
  await nango.log(`Fetching page ${page}`);

  // SHORT-CIRCUIT FOR TESTING - Remove before committing
  if (page > 2) {
    await nango.log(`Short-circuit: stopping after page ${page}`);
    break;
  }

  // ... rest of sync logic

  hasMoreData = res.Response_Results.Page < res.Response_Results.Total_Pages;
  page++;
} while (hasMoreData);
```

**Remember:** Remove short-circuit before committing!

## Common Patterns

### Testing Manager Resolution

```typescript
// Add detailed logging to verify manager data
await nango.log(`Manager resolution: ${managersResolved} resolved, ${managersNotFound} not found`);

// Log sample manager data
if (allMappedEmployees.length > 0) {
  const empWithManager = allMappedEmployees.find(e => e.manager);
  if (empWithManager) {
    await nango.log(`Sample manager: ${JSON.stringify(empWithManager.manager)}`);
  }
}
```

### Testing Data Mapping

```typescript
// Log first mapped employee to verify structure
if (mappedEmployees.length > 0) {
  await nango.log(`Sample employee: ${JSON.stringify(mappedEmployees[0], null, 2)}`);
}
```

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| "Connection not found" | Invalid connection ID | Verify connection exists in environment |
| "Sync not found" | Wrong sync name | Check sync export name in sync file |
| Timeout | Large dataset | Add short-circuit to limit pages |
| Missing data | Wrong Response_Group | Check API request includes needed data groups |
| Authentication error | Invalid credentials | Verify connection credentials in Nango dashboard |

## Workflow

1. **Make changes** to sync or mapper files
2. **Add short-circuit** if testing large dataset
3. **Run dry run** command
4. **Check logs** for errors or missing data
5. **Verify mapped data** structure is correct
6. **Remove short-circuit** before committing
7. **Run full dry run** to verify complete sync

## Best Practices

- Always test in the target environment (prod credentials may differ from dev)
- Use short-circuit for initial testing, then test full sync
- Add comprehensive logging for debugging
- Verify manager/relationship data populates correctly
- Check edge cases (missing fields, null values, empty arrays)
- Remove all debugging code before committing

## Example Output

```
Fetching page 1
Fetched batch of 100 workers. Total fetched: 100
Processed page 1 of 10 (1000 total)
Fetching page 2
Short-circuit: stopping after page 2
Resolving manager relationships for 200 employees...
Manager resolution complete: 180 resolved, 20 not found in employee list
Sample manager: {"id":"12345","firstName":"John","lastName":"Doe","email":"john.doe@company.com"}
Saved 200 employees with manager details
```

## Related

- **nango-integrations agent**: Expert guidance on Nango sync patterns
- Nango docs: https://docs.nango.dev/integrate/guides/dry-run
