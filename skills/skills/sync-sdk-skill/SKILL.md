---
name: sync-sdk-skill
description: Synchronize the base44-sdk skill with the latest SDK source code from the Base44 SDK repository
disable-model-invocation: true
---

# Sync SDK Skill

Synchronize the `skills/base44-sdk/` skill with the latest SDK source code from the Base44 SDK repository.

## Usage

When activated, this command will ask for:
1. **SDK source folder path** (required) - The local path to the Base44 SDK source code
2. **Documentation URL** (optional) - URL to fetch additional documentation

## Steps

### Step 1: Gather Input

Ask the user for the required inputs using the AskQuestion tool if available, otherwise ask conversationally:

**Required:**
- SDK source folder path (e.g., `~/projects/base44-sdk` or `/Users/me/base44-sdk`)

**Optional:**
- Documentation URL (e.g., `https://docs.base44.com/sdk`)

If the user provided these in the initial prompt, use those values.

### Step 2: Validate Source Folder

1. Check that the provided path exists and contains SDK source code
2. Look for these key indicators:
   - `package.json` with `@base44/sdk` or similar SDK-related content
   - `src/` directory with module implementations
   - TypeScript/JavaScript files with SDK module exports (e.g., `entities.ts`, `auth.ts`, `client.ts`)

If validation fails, ask the user to verify the path.

### Step 3: Discover SDK Modules

Scan the SDK source folder to find all available modules. Look for:

1. **Module files** in directories like:
   - `src/`
   - `src/modules/`
   - `lib/`

2. **For each module, extract:**
   - Module name and exports
   - Available methods and their signatures
   - Method parameters and types
   - Return types
   - Usage examples (if present in source or JSDoc)
   - Submodules (e.g., `integrations.Core`, `integrations.custom`)

3. **Parse module definitions** from:
   - TypeScript interfaces and types
   - Class definitions and methods
   - JSDoc comments and annotations
   - Export statements

4. **Key modules to look for:**
   - `entities` - CRUD operations on data models
   - `auth` - Login, register, user management
   - `agents` - AI conversations and messages
   - `functions` - Backend function invocation
   - `integrations` - AI, email, file uploads, custom APIs
   - `connectors` - OAuth tokens (service role only)
   - `analytics` - Track custom events
   - `appLogs` - Log user activity
   - `users` - User invitations
   - `client` - Client creation and configuration

### Step 4: Read Existing Skill

Read the current skill files to understand what needs updating:

```
skills/base44-sdk/
├── SKILL.md
└── references/
    ├── analytics.md
    ├── app-logs.md
    ├── auth.md
    ├── base44-agents.md
    ├── client.md
    ├── connectors.md
    ├── entities.md
    ├── functions.md
    ├── integrations.md
    └── users.md
```

### Step 5: Compare and Identify Changes

Compare discovered SDK modules with existing skill documentation:

1. **New modules**: Modules in source but not in skill references
2. **New methods**: Methods added to existing modules
3. **Updated methods**: Methods with changed signatures, parameters, or return types
4. **Deprecated methods**: Methods marked as deprecated
5. **Removed methods**: Methods in skill but not in source (verify before removing)
6. **New parameters**: New options added to existing methods

Create a summary of changes to show the user before applying.

### Step 6: Fetch External Documentation (Optional)

If a documentation URL was provided:

1. Fetch the documentation page
2. Extract relevant module and method documentation
3. Use this to supplement information from source code
4. Cross-reference for accuracy

### Step 7: Update Skill Files

For each change identified:

#### Update Reference Files

For each module, update or create `references/{module-name}.md`:

```markdown
# {ModuleName} Module

{Description from source}

## Overview

{Brief explanation of what the module does}

## Methods

### `{methodName}(params)`

{Method description}

**Parameters:**

| Parameter | Type | Description | Required |
|-----------|------|-------------|----------|
| `param1` | `string` | {description} | Yes |
| `options` | `object` | {description} | No |

**Returns:** `Promise<{ReturnType}>`

**Example:**

```javascript
const result = await base44.{module}.{methodName}({
  param1: "value"
});
```

## Notes

{Any important behavioral notes, frontend/backend availability, etc.}
```

#### Update SKILL.md

1. Update the **SDK Modules** table if modules changed
2. Update **Quick Start** if core patterns changed
3. Update **Module Selection** section with new capabilities
4. Update **Common Patterns** with new usage examples
5. Update **Frontend vs Backend** table if availability changed
6. Keep the existing structure and formatting
7. Do NOT change the frontmatter description unless explicitly asked

### Step 8: Present Summary

After updates, present a summary to the user:

```
## Sync Summary

### Files Updated
- references/new-module.md (created)
- references/entities.md (updated methods)
- SKILL.md (updated module table)

### Changes Made
- Added new module: `newModule`
- Updated `entities` module: added `bulkCreate()` method
- Added new parameter `options.cache` to `auth.me()`
- Deprecated `integrations.legacyMethod()`

### Manual Review Recommended
- [List any changes that need verification]
```

## Important Notes

- **Preserve existing content**: Don't remove detailed explanations, examples, or warnings unless they're outdated
- **Keep formatting consistent**: Match the existing style of SKILL.md and reference files
- **Maintain progressive disclosure**: Keep detailed docs in references, summaries in SKILL.md
- **Flag uncertainties**: If source code is unclear, flag it for manual review
- **Document frontend/backend availability**: Always note if a method is backend-only (e.g., `connectors`, `asServiceRole`)
- **Preserve type information**: Include TypeScript types in method signatures
- **Keep examples practical**: Examples should reflect real-world usage patterns

## Module-Specific Guidelines

### entities.md
- Document CRUD methods: `create`, `get`, `list`, `filter`, `update`, `delete`
- Include query filter syntax and operators
- Document `subscribe()` for real-time updates
- Note RLS/FLS security implications if applicable

### auth.md
- Cover all authentication methods (email/password, OAuth, etc.)
- Document `me()`, `updateMe()`, `logout()`
- Include redirect flow examples
- Note token handling

### integrations.md
- Document `Core` submodule methods (InvokeLLM, SendEmail, UploadFile, GenerateImage)
- Document `custom.call()` for custom integrations
- Include AI prompt examples

### connectors.md
- Note this is service role / backend only
- Document `getAccessToken()` for OAuth providers

### functions.md
- Show both frontend invocation and backend implementation
- Include `createClientFromRequest()` usage
- Document `asServiceRole` access patterns

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Can't find module files | Try searching for `export class` or `export function` patterns |
| Types not detected | Look for `.d.ts` files or inline TypeScript annotations |
| Missing method descriptions | Check for JSDoc comments (`/** ... */`) above methods |
| Submodule structure | Modules like `integrations.Core` may be in nested files |
| Return types unclear | Check TypeScript generics and Promise wrappers |
