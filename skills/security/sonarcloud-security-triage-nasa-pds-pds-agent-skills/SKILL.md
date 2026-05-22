---
name: sonarcloud-security-triage
description: Apply triage decisions to SonarCloud security issues by reading a CSV with review decisions and updating issue/hotspot statuses via the SonarCloud API. Use when the user has reviewed security issues and wants to bulk-update SonarCloud with their triage decisions.
---

# SonarCloud Security Triage Skill

This skill applies triage decisions to SonarCloud security issues (vulnerabilities and hotspots) by reading a CSV file with review decisions and updating the statuses in SonarCloud via the API.

## Prerequisites

- Node.js v18 or higher
- SonarCloud API token with **Administer Security Hotspots** and **Administer Issues** permissions
- CSV file with triage decisions (output from `sonarcloud-security-audit` skill with added columns)

## Workflow

This skill complements the **sonarcloud-security-audit** skill:

1. **Export** security issues → `sonarcloud-security-audit` skill generates CSV
2. **Review** in spreadsheet → User adds triage columns (Action, Resolution, Comment, Reviewer)
3. **Apply** decisions → This skill updates SonarCloud with the triage decisions

## CSV Format Required

The input CSV must have these columns (typically the output of `sonarcloud-security-audit` plus 4 additional columns):

**Original columns from audit:**
- Project, Type, Severity, Status, Rule, Message, Component, Line, Created, URL

**Added triage columns:**
- **Action** - For SECURITY_HOTSPOT: `REVIEWED` | For VULNERABILITY: `confirm`, `falsepositive`, `wontfix`, `resolve`
- **Resolution** - For SECURITY_HOTSPOT only: `SAFE` or `FIXED`
- **Comment** - Review explanation (optional but recommended)
- **Reviewer** - Email or name of reviewer (optional, for tracking)

**Example rows:**
```csv
Project,Type,Severity,Status,Rule,Message,Component,Line,Created,URL,Action,Resolution,Comment,Reviewer
NASA-PDS_doi-ui,SECURITY_HOTSPOT,,TO_REVIEW,,Using http protocol...,src/file.jsx,119,2021-01-28T19:38:04+0000,https://sonarcloud.io/project/security_hotspots?id=NASA-PDS_doi-ui&hotspots=AZPV1fTprahIrD-njDRb,REVIEWED,SAFE,"False positive. This is a URI not a URL.",jordan@jpl.nasa.gov
NASA-PDS_data-upload,VULNERABILITY,MAJOR,OPEN,python:S7608,Add ExpectedBucketOwner...,src/sync.py,134,2025-10-10T20:33:50+0000,https://sonarcloud.io/project/issues?open=AZnP1S0b_yFrdYV3Iu6e&id=NASA-PDS_data-upload,wontfix,,"Scheduled for future sprint",jane@jpl.nasa.gov
```

## Execution Steps

### Step 1: Check Prerequisites

Verify the SonarCloud token is set:
```bash
env | grep SONARCLOUD_TOKEN
```

If not set, prompt the user to set it (same token used for audit skill).

### Step 2: Validate CSV

Check that the CSV file exists and has the required columns:
- Must have URL column (to extract issue/hotspot keys)
- Must have Action column (identifies rows to process)
- For SECURITY_HOTSPOT rows with Action=REVIEWED, must have Resolution column

### Step 3: Run the Triage Script

Execute the script:
```bash
cd sonarcloud-security-triage
node scripts/apply-triage.mjs <path-to-csv> [--dry-run]
```

**Parameters:**
- `<path-to-csv>` (required): Path to CSV file with triage decisions
- `--dry-run` (optional): Preview changes without actually updating SonarCloud

**The script will:**
1. Parse the CSV file
2. Filter rows where Action column is not empty
3. Extract issue/hotspot key from the URL column
4. For each row:
   - **SECURITY_HOTSPOT** → Call `POST /api/hotspots/change_status`
     - Parameters: `hotspot`, `status=REVIEWED`, `resolution` (SAFE/FIXED), `comment`
   - **VULNERABILITY** → Call `POST /api/issues/do_transition`
     - Parameters: `issue`, `transition` (confirm/falsepositive/wontfix/resolve), `comment`
5. Log success/failure for each update
6. Generate summary report

### Step 4: Review Results

The script outputs:
- **Success count**: Number of issues successfully updated
- **Failed count**: Number of issues that failed to update (with error messages)
- **Skipped count**: Number of rows skipped (empty Action or already in target status)
- **Summary CSV**: Optional output file with status of each update

### Step 5: Verify in SonarCloud

After running, verify a few updates in the SonarCloud UI:
- Navigate to the project's Security Hotspots or Issues page
- Check that statuses were updated correctly
- Verify comments were added

## API Endpoints Used

### For Security Hotspots (TO_REVIEW → REVIEWED)

**Endpoint:** `POST /api/hotspots/change_status`

**Parameters:**
- `hotspot` (required): Hotspot key extracted from URL (e.g., `AZPV1fTprahIrD-njDRb`)
- `status` (required): Always `REVIEWED`
- `resolution` (required): `SAFE` or `FIXED`
- `comment` (optional): Review explanation

**Example:**
```bash
curl -X POST 'https://sonarcloud.io/api/hotspots/change_status' \
  -H 'Authorization: Bearer <token>' \
  -d 'hotspot=AZPV1fTprahIrD-njDRb' \
  -d 'status=REVIEWED' \
  -d 'resolution=SAFE' \
  -d 'comment=False positive. This is a URI not a URL.'
```

### For Vulnerabilities (OPEN → Other statuses)

**Endpoint:** `POST /api/issues/do_transition`

**Parameters:**
- `issue` (required): Issue key extracted from URL (e.g., `AZnP1S0b_yFrdYV3Iu6e`)
- `transition` (required): One of `confirm`, `falsepositive`, `wontfix`, `resolve`
- `comment` (optional): Explanation for the transition

**Example:**
```bash
curl -X POST 'https://sonarcloud.io/api/issues/do_transition' \
  -H 'Authorization: Bearer <token>' \
  -d 'issue=AZnP1S0b_yFrdYV3Iu6e' \
  -d 'transition=wontfix' \
  -d 'comment=Scheduled for future sprint'
```

## Extracting Keys from URLs

The script extracts issue/hotspot keys from the URL column:

**Security Hotspot URL:**
```
https://sonarcloud.io/project/security_hotspots?id=NASA-PDS_doi-ui&hotspots=AZPV1fTprahIrD-njDRb
                                                                              ^^^^^^^^^^^^^^^^^^^^^^
                                                                              Extract this part
```

**Vulnerability URL:**
```
https://sonarcloud.io/project/issues?open=AZnP1S0b_yFrdYV3Iu6e&id=NASA-PDS_data-upload
                                           ^^^^^^^^^^^^^^^^^^^^^
                                           Extract this part
```

## Error Handling

### Authentication Errors (401)
- Token is invalid or expired
- Token doesn't have required permissions
- Regenerate token with correct permissions

### Permission Errors (403)
- Token doesn't have **Administer Security Hotspots** permission for hotspots
- Token doesn't have **Administer Issues** permission for vulnerabilities
- Check token scopes in SonarCloud settings

### Not Found Errors (404)
- Issue/hotspot key is invalid or was deleted
- Skip and continue with next item

### Invalid Transition Errors (400)
- Transition not allowed from current status
- Resolution required but not provided
- Log error and skip item

### Rate Limiting (429)
- Script automatically waits 60 seconds and retries
- If persistent, reduce batch size or run during off-peak hours

## Dry Run Mode

Before applying changes, use `--dry-run` to preview:

```bash
node scripts/apply-triage.mjs triage.csv --dry-run
```

**Dry run output:**
```
[DRY RUN] Would update hotspot AZPV1fTprahIrD-njDRb:
  Project: NASA-PDS_doi-ui
  Type: SECURITY_HOTSPOT
  Action: Change status to REVIEWED (SAFE)
  Comment: "False positive. This is a URI not a URL."

[DRY RUN] Would update issue AZnP1S0b_yFrdYV3Iu6e:
  Project: NASA-PDS_data-upload
  Type: VULNERABILITY
  Action: Transition to wontfix
  Comment: "Scheduled for future sprint"

Summary: 2 updates would be applied (0 errors)
```

## Best Practices

1. **Always run dry-run first** to preview changes
2. **Add meaningful comments** to explain triage decisions (helps future reviewers)
3. **Start small** - test with 5-10 issues before processing thousands
4. **Track reviewer** - include email/name in Reviewer column for accountability
5. **Backup CSV** - keep original audit CSV before adding triage columns
6. **Verify sample** - Check a few issues in SonarCloud UI after bulk update

## Troubleshooting

**"Column 'Action' not found"**
- CSV is missing the Action column
- Ensure you added the 4 triage columns: Action, Resolution, Comment, Reviewer

**"Could not extract hotspot key from URL"**
- URL format may have changed
- Verify URL column contains valid SonarCloud URLs
- Check if URL contains `hotspots=` or `open=` parameter

**"No rows to process"**
- All Action columns are empty
- Add triage decisions to at least one row

**"Invalid resolution: must be SAFE or FIXED"**
- For SECURITY_HOTSPOT with Action=REVIEWED, Resolution must be `SAFE` or `FIXED`
- Check spelling and capitalization

## Example Workflow

### 1. Export security issues
```bash
cd sonarcloud-security-audit
node scripts/fetch-security-issues.mjs nasa-pds security-audit.csv
```

### 2. Review and add triage columns

Open `security-audit.csv` in Excel/Google Sheets and add 4 columns:

| Action | Resolution | Comment | Reviewer |
|--------|------------|---------|----------|
| REVIEWED | SAFE | False positive. Uses URI not URL. | jordan@jpl.nasa.gov |
| wontfix | | Low priority. Scheduled for Q2. | jane@jpl.nasa.gov |

Save as `security-triage.csv`

### 3. Dry run to preview
```bash
cd sonarcloud-security-triage
node scripts/apply-triage.mjs ../security-triage.csv --dry-run
```

### 4. Apply triage decisions
```bash
node scripts/apply-triage.mjs ../security-triage.csv
```

### 5. Verify in SonarCloud
- Open a few updated issues in SonarCloud UI
- Confirm status changes and comments appear correctly

## Output

**Console output:**
```
🔧 SonarCloud Security Triage

Input file: security-triage.csv
Dry run: NO
Total rows: 4647
Rows with triage decisions: 127

Processing...
[1/127] ✅ Hotspot AZPV1fTprahIrD-njDRb → REVIEWED (SAFE)
[2/127] ✅ Issue AZnP1S0b_yFrdYV3Iu6e → wontfix
[3/127] ⚠️  Hotspot ABC123 → 404 Not Found (skipped)
...

📊 Summary:
   ✅ Successfully updated: 125
   ❌ Failed: 1
   ⏭️  Skipped: 1

Failed updates:
- Row 45: Hotspot XYZ789 - 403 Forbidden (insufficient permissions)

All done!
```

## Notes

- Only rows with non-empty **Action** column are processed
- Empty Action = no update (useful for keeping already-reviewed items in the CSV)
- The **Reviewer** column is for tracking purposes only (not sent to SonarCloud)
- Comments in SonarCloud will show timestamp and API user (token owner), not the Reviewer value
- Updates are applied sequentially with small delays to respect rate limits
- Script is idempotent: running twice won't cause issues (SonarCloud will reject invalid transitions)
