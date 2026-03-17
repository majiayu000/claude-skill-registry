---
name: sap-fiori-url-generator
description: Generate SAP Fiori Launchpad URLs from app names using AppList.json. Looks up app information by name and constructs proper FLP URLs with required parameters like sap-client and sap-language.
license: MIT
---

# SAP Fiori URL Generator Skill

This skill enables you to generate SAP Fiori Launchpad (FLP) URLs based on app names from the AppList.json file.

## References

When you need to look up SAP Fiori app information:

**App List Database**: Read `@skills/sap-fiori-apps-reference/references/AppList.json` - contains all SAP Fiori apps with their Semantic Object-Action mappings, App IDs, descriptions, and technical details.

Use this reference to:
- Search for apps by name (partial match, case-insensitive)
- Extract the "Semantic Object - Action" field for URL generation
- Provide app details (ID, description, component) to users
- Suggest similar apps when exact match is not found

### Updating AppList.json

The AppList.json data can be obtained from SAP's Fiori Apps Library:

1. Go to https://pr.alm.me.sap.com/launchpad#FALApp-display
2. Export the app list to Excel
3. Convert the Excel file to JSON format

This ensures the app list stays current with the latest SAP Fiori applications.

## Overview

When a user provides:
1. A base SAP Fiori URL (e.g., `https://myserver.com:44300`)
2. An app name (e.g., "Create Maintenance Request")

You will:
1. Search the AppList.json file for the app
2. Extract the "Semantic Object - Action" field
3. Construct the complete FLP URL with proper parameters

## URL Structure

The complete SAP Fiori Launchpad URL follows this pattern:

```
{BASE_URL}/sap/bc/ui2/flp?sap-client={CLIENT}&sap-language={LANGUAGE}#{SEMANTIC_OBJECT}-{ACTION}
```

### Required Parameters (MUST be provided by user)

- **BASE_URL**: The SAP system base URL (e.g., `https://myserver.com:44300`)
  - MUST be provided by user
  - No default value
  
- **sap-client**: The SAP client number (e.g., `100`)
  - MUST be provided by user
  - No default value
  - Required for all SAP Fiori Launchpad URLs

### Optional Parameters

- **sap-language**: Language code (e.g., `EN`, `DE`, `FR`)
  - Default: `EN` if not specified by user
  - Can be customized per request
  
### Auto-Generated Parameters

- **SEMANTIC_OBJECT-ACTION**: Automatically extracted from the "Semantic Object - Action" field in AppList.json
  - No user input required
  - Looked up based on app name

## Implementation Steps

### Step 1: Read AppList.json

First, read the AppList.json file to access the app data:

```javascript
const fs = require('fs');
const appList = JSON.parse(fs.readFileSync('AppList.json', 'utf8'));
```

### Step 2: Search for the App

Search for the app by name (case-insensitive, partial match):

```javascript
function findAppByName(appName) {
  const normalizedSearch = appName.toLowerCase().trim();
  
  return appList.find(app => 
    app['App Name'] && 
    app['App Name'].toLowerCase().includes(normalizedSearch)
  );
}
```

### Step 3: Extract Semantic Object-Action

Get the "Semantic Object - Action" field:

```javascript
function getSemanticObjectAction(app) {
  const semanticAction = app['Semantic Object - Action'];
  
  if (!semanticAction || semanticAction === 'NaN' || semanticAction === null) {
    throw new Error('No Semantic Object-Action found for this app');
  }
  
  return semanticAction;
}
```

### Step 4: Construct the URL

Build the complete FLP URL:

```javascript
function generateFioriUrl(baseUrl, client, semanticAction, language = 'EN') {
  // Validate required parameters
  if (!baseUrl) {
    throw new Error('BASE_URL is required and must be provided by user');
  }
  if (!client) {
    throw new Error('sap-client is required and must be provided by user');
  }
  
  // Remove trailing slash from base URL if present
  const cleanBaseUrl = baseUrl.replace(/\/$/, '');
  
  return `${cleanBaseUrl}/sap/bc/ui2/flp?sap-client=${client}&sap-language=${language}#${semanticAction}`;
}
```

## Complete Example

### Input (ALL required parameters must be provided by user)
- Base URL: `https://myserver.com:44300` (**USER MUST PROVIDE**)
- SAP Client: `100` (**USER MUST PROVIDE**)
- App Name: `Create Maintenance Request` (**USER MUST PROVIDE**)
- Language: `EN` (optional - defaults to EN if not specified)

### Process
1. Read AppList.json
2. Search for "Create Maintenance Request"
3. Find entry with "Semantic Object - Action": `MaintenanceWorkRequest-create`
4. Construct URL using user-provided base URL and client

### Output
```
https://myserver.com:44300/sap/bc/ui2/flp?sap-client=100&sap-language=EN#MaintenanceWorkRequest-create
```

## Error Handling

### App Not Found
If the app name is not found in AppList.json:
```
Error: App "{app_name}" not found in AppList.json
Suggestion: Check spelling or try searching with partial name
```

### Missing Semantic Object-Action
If the app exists but has no Semantic Object-Action:
```
Error: App "{app_name}" (ID: {app_id}) does not have a Semantic Object-Action defined
Note: This app may not be launchable via FLP URL
```

### Multiple Matches
If multiple apps match the search term:
```
Found multiple apps matching "{search_term}":
1. App Name 1 (ID: F1234)
2. App Name 2 (ID: F5678)
Please specify which app you want
```

## Additional Features

### List Similar Apps
When an exact match isn't found, suggest similar apps:

```javascript
function findSimilarApps(searchTerm, limit = 5) {
  const normalized = searchTerm.toLowerCase();
  
  return appList
    .filter(app => 
      app['App Name'] && 
      app['App Name'].toLowerCase().includes(normalized)
    )
    .slice(0, limit)
    .map(app => ({
      name: app['App Name'],
      id: app['App ID'],
      semanticAction: app['Semantic Object - Action']
    }));
}
```

### Extract App Details
Provide additional app information:

```javascript
function getAppDetails(app) {
  return {
    name: app['App Name'],
    id: app['App ID'],
    description: app['App Description'],
    semanticAction: app['Semantic Object - Action'],
    technicalCatalog: app['Technical Catalog'],
    transactionCode: app['Transaction Codes'],
    component: app['Application Component']
  };
}
```

## User Interaction Examples

### Example 1: Basic URL Generation
**User:** "Generate URL for Create Maintenance Request app with base URL https://myserver.com:44300 and client 100"

**Response:**
```
App Found: Create Maintenance Request (F1511A)
Semantic Object-Action: MaintenanceWorkRequest-create

Generated URL:
https://myserver.com:44300/sap/bc/ui2/flp?sap-client=100&sap-language=EN#MaintenanceWorkRequest-create
```

### Example 2: Custom Language
**User:** "Generate URL for Create Maintenance Request in German, base URL https://myserver.com:44300, client 100"

**Response:**
```
App Found: Create Maintenance Request (F1511A)
Semantic Object-Action: MaintenanceWorkRequest-create

Generated URL:
https://myserver.com:44300/sap/bc/ui2/flp?sap-client=100&sap-language=DE#MaintenanceWorkRequest-create
```

### Example 3: Missing Required Parameters
**User:** "Generate URL for Create Maintenance Request"

**Response:**
```
Error: Missing required parameters
Please provide:
  - Base URL (e.g., https://myserver.com:44300)
  - SAP Client (e.g., 100)
  - App Name (provided: Create Maintenance Request)
  - Language (optional, defaults to EN)

Example: Generate URL for "Create Maintenance Request" with base URL https://myserver.com:44300 and client 100
```

### Example 3: Search by Partial Name
**User:** "Find apps related to 'Workflow'"

**Response:**
```
Found 8 apps matching "Workflow":

1. Manage Workflows (F2190)
   Action: Workflow-showList

2. Workflow Component (F2506)
   Action: Not available

3. Manage Workflow Templates (F2787)
   Action: WorkflowTemplate-showList

4. Manage Workflows - For Bank Accounts (F2796)
   Action: BankAccount-workflowShowList

5. Manage Workflow Scenarios (F3067)
   Action: WorkflowScenario-showList

To generate a URL, please provide:
  - Base URL (e.g., https://myserver.com:44300)
  - SAP Client (e.g., 100)
  - Which app you want from the list above
```

## Language Codes Reference

Common SAP language codes:
- `EN` - English
- `DE` - German (Deutsch)
- `ES` - Spanish (Español)
- `FR` - French (Français)
- `IT` - Italian (Italiano)
- `PT` - Portuguese (Português)
- `ZH` - Chinese (中文)
- `JA` - Japanese (日本語)
- `KO` - Korean (한국어)

## Technical Notes

### AppList.json Structure
Each app entry contains:
- **App Name**: Display name of the application
- **App ID**: SAP Fiori app identifier (e.g., F1511A)
- **Semantic Object - Action**: FLP navigation target (e.g., MaintenanceWorkRequest-create)
- **UI Technology**: Technology used (SAP Fiori elements, SAPUI5, etc.)
- **Application Component**: SAP component abbreviation
- **App Description**: Detailed description of functionality
- **Technical Catalog**: Catalog assignment
- **Transaction Codes**: Classic SAP transaction (if applicable)
- **OData Service**: Backend service name

### Handling Missing Data
Some apps may have `NaN` or `null` values for certain fields. Always check:
- Semantic Object - Action must exist to generate FLP URL
- App Name should exist for search functionality
- Other fields are optional for URL generation

## Best Practices

1. **Always request required parameters**: Ask user for base URL and sap-client if not provided
2. **Validate parameters**: Ensure base URL format is valid (starts with `http://` or `https://`)
3. **Strip trailing slashes**: Clean the base URL before concatenation
4. **Case-insensitive search**: Make searches user-friendly
5. **Provide app details**: Show App ID and description for confirmation
6. **Handle multiple matches gracefully**: Let users choose when ambiguous
7. **Default language**: Use `sap-language=EN` as default if not specified
8. **Escape special characters**: If app names contain special characters in URLs
9. **Prompt for missing info**: Never assume base URL or client - always ask user

## Complete Implementation Example

```javascript
const fs = require('fs');

class FioriUrlGenerator {
  constructor(appListPath) {
    this.apps = JSON.parse(fs.readFileSync(appListPath, 'utf8'));
  }

  findApp(appName) {
    const normalized = appName.toLowerCase().trim();
    return this.apps.find(app => 
      app['App Name'] && 
      app['App Name'].toLowerCase().includes(normalized)
    );
  }

  generateUrl(baseUrl, client, appName, options = {}) {
    const { language = 'EN' } = options;
    
    // Validate required parameters
    if (!baseUrl) {
      throw new Error('Base URL is required - must be provided by user');
    }
    if (!client) {
      throw new Error('SAP Client is required - must be provided by user');
    }
    
    // Find the app
    const app = this.findApp(appName);
    if (!app) {
      throw new Error(`App "${appName}" not found`);
    }

    // Extract semantic action
    const semanticAction = app['Semantic Object - Action'];
    if (!semanticAction || semanticAction === 'NaN') {
      throw new Error(`App "${app['App Name']}" has no Semantic Object-Action`);
    }

    // Clean base URL
    const cleanBaseUrl = baseUrl.replace(/\/$/, '');

    // Construct URL
    return {
      url: `${cleanBaseUrl}/sap/bc/ui2/flp?sap-client=${client}&sap-language=${language}#${semanticAction}`,
      appDetails: {
        name: app['App Name'],
        id: app['App ID'],
        description: app['App Description'],
        semanticAction: semanticAction
      }
    };
  }
}

// Usage - User MUST provide base URL and client
const generator = new FioriUrlGenerator('./AppList.json');
const result = generator.generateUrl(
  'https://myserver.com:44300',  // User provided
  '100',                                    // User provided
  'Create Maintenance Request',            // User provided
  { language: 'EN' }                       // Optional - defaults to EN
);

console.log(result.url);
```

## Summary

This skill enables seamless SAP Fiori URL generation by:
1. Reading and parsing AppList.json
2. Searching for apps by name
3. Extracting semantic object-action mappings
4. Constructing properly formatted FLP URLs
5. Handling errors and edge cases gracefully
6. Supporting multiple languages and customization

The generated URLs can be directly used to launch SAP Fiori apps in the Fiori Launchpad.
