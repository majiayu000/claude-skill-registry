---
name: mcp-tool-generator
description: Generate new MCP tools for GitLab operations following the project's standardized pattern. Creates complete TypeScript files with imports, registration functions, Zod schemas, error handling, and format options. Supports simple CRUD operations, complex multi-action tools, and advanced patterns like discussion management. Use when "create mcp tool", "generate gitlab tool", "new tool for", "add tool to gitlab", or building new GitLab integration features.
allowed-tools: Read, Write, Glob, Grep
---

# MCP Tool Generator

Generate new MCP tools following the standardized patterns from the project. Creates complete tool files with proper imports, Zod schemas, error handling, and GitLab API integration.

## Activation Triggers

- "create an mcp tool for..."
- "generate a gitlab tool to..."
- "I need a new tool that..."
- "add a tool for [operation]"
- "create tool to [action] [resource]"

## Tool Types Supported

### 1. Simple CRUD Tools
Basic get/list/create/update/delete operations with standard patterns:
- Get single resource (issue, MR, milestone, etc.)
- List multiple resources with filtering and pagination
- Create new resources
- Update existing resources
- Delete resources

**Pattern**: `gitlab-[action]-[resource]` (e.g., `gitlab-get-issue`, `gitlab-list-pipelines`)

### 2. Multi-Action Tools
Comprehensive tools that handle multiple related operations in one tool:
- Multiple actions via `action` enum parameter
- Conditional logic based on action type
- Structured responses with status/action/message format
- More efficient than multiple separate tools

**Pattern**: `gitlab-[resource]-[operation]` (e.g., `gitlab-manage-issue`)

### 3. Complex Operation Tools
Tools with advanced logic:
- Discussion/comment management with update detection
- Multi-step workflows
- Direct API calls using fetch for specific needs
- Position-based operations (code reviews, inline comments)

**Pattern**: Based on specific operation (e.g., `gitlab-review-merge-request-code`)

## Autonomous Generation Process

### Step 1: Analyze User Request

Extract key information:
1. **Tool Type**: Simple CRUD, multi-action, or complex?
2. **Tool Purpose**: What GitLab operation? (e.g., "get merge request details", "manage issues", "review code")
3. **Resource Type**: What GitLab entity? (issue, MR, branch, milestone, pipeline, label, etc.)
4. **Action Type**: What operation? (get, list, create, update, delete, search, manage, review, etc.)
5. **Required Parameters**: What inputs needed? (projectname, IID, branch name, action, etc.)
6. **Optional Parameters**: What's optional? (format, labels, assignee, filters, etc.)
7. **Special Features**: Multi-action? Position-based? Discussion management?

### Step 2: Auto-Generate Names

**Tool Name** (kebab-case):
- Simple CRUD: `gitlab-[action]-[resource]`
  - Examples: `gitlab-get-merge-request`, `gitlab-list-pipelines`, `gitlab-create-branch`
- Multi-action: `gitlab-[manage|handle]-[resource]`
  - Examples: `gitlab-manage-issue`, `gitlab-handle-milestone`
- Complex: `gitlab-[specific-operation]`
  - Examples: `gitlab-review-merge-request-code`, `gitlab-find-related-issues`

**Function Name** (PascalCase):
- Pattern: `register[Action][Resource]`
- Examples:
  - `gitlab-get-merge-request` → `registerGetMergeRequest`
  - `gitlab-manage-issue` → `registerManageIssue`
  - `gitlab-review-merge-request-code` → `registerReviewMergeRequestCode`

**File Name** (kebab-case):
- Pattern: `gitlab-[tool-name].ts`
- Location: `src/tools/gitlab/`

### Step 3: Select Tool Pattern

#### Pattern A: Simple CRUD Tool

**Use when**: Single operation (get, list, create, update, delete)

**Standard features**:
- `projectname` parameter (optional, with prompt fallback)
- `format` parameter (detailed/concise) for get/list operations
- HTML content cleaning with `cleanGitLabHtmlContent()`
- Project validation before API calls
- Descriptive error messages
- Emojis in concise format

**Template structure**:
```typescript
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp';
import { z } from 'zod';
import { cleanGitLabHtmlContent } from '../../core/utils';
import { getGitLabService, getProjectNameFromUser } from './gitlab-shared';

export function register{FunctionName}(server: McpServer) {
    server.registerTool(
        "{tool-name}",
        {
            title: "{Human Readable Title}",
            description: "{Detailed description}",
            inputSchema: {
                {param1}: z.{type}().describe("{description}"),
                projectname: z.string().optional().describe("GitLab project name (if not provided, you'll be prompted to select)"),
                format: z.enum(["detailed", "concise"]).optional().describe("Response format - 'detailed' includes all metadata, 'concise' includes only key information")
            }
        },
        async ({ {params}, projectname, format = "detailed" }) => {
            try {
                // Standard workflow
            } catch (e) {
                return { content: [{ type: "text", text: JSON.stringify({ type: "error", error: String(e) }) }] };
            }
        }
    );
}
```

#### Pattern B: Multi-Action Tool

**Use when**: Multiple related operations on same resource type

**Standard features**:
- `action` parameter with enum of actions
- Switch/case logic for each action
- Structured responses: `{ status: "success"/"failure", action: "...", message: "...", [resource]: {...} }`
- Direct API calls using fetch when needed
- Conditional parameters based on action
- No format parameter (uses structured JSON)

**Template structure**:
```typescript
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp';
import fetch from 'node-fetch';
import { z } from 'zod';
import { cleanGitLabHtmlContent } from '../../core/utils';
import { getGitLabService, getProjectNameFromUser } from './gitlab-shared';

export function register{FunctionName}(server: McpServer) {
    server.registerTool(
        "{tool-name}",
        {
            title: "{Human Readable Title}",
            description: "{Comprehensive description covering all actions}",
            inputSchema: {
                {resourceId}: z.number().describe("The ID/IID of the resource"),
                projectname: z.string().optional().describe("GitLab project name (if not provided, you'll be prompted to select)"),
                action: z.enum(["action1", "action2", "action3"]).describe("Action to perform"),
                // Conditional parameters for different actions
                param1: z.{type}().optional().describe("For action1: description"),
                param2: z.{type}().optional().describe("For action2: description")
            }
        },
        async ({ {resourceId}, projectname, action, {params} }) => {
            try {
                // Get project and resource
                const projectName = projectname || await getProjectNameFromUser(server, false, "prompt");
                if (!projectName) {
                    return { content: [{ type: "text", text: JSON.stringify({ type: "error", error: "Project not found" }) }] };
                }

                const service = await getGitLabService(server);
                const projectId = await service.getProjectId(projectName);
                if (!projectId) {
                    return { content: [{ type: "text", text: JSON.stringify({ type: "error", error: `Project "${projectName}" not found` }) }] };
                }

                // Get resource first
                const rawResource = await service.get{Resource}(projectId, {resourceId});
                if (!rawResource) {
                    return { content: [{ type: "text", text: JSON.stringify({ type: "error", error: `Resource not found` }) }] };
                }

                const resource = cleanGitLabHtmlContent(rawResource, ['description', 'title']);

                // Handle actions
                switch (action) {
                    case "action1":
                        // Implementation
                        return { content: [{ type: "text", text: JSON.stringify({
                            status: 'success',
                            action: 'action1',
                            message: 'Action completed',
                            {resource}: { /* key fields */ }
                        }, null, 2) }] };

                    case "action2":
                        // Implementation
                        break;

                    default:
                        return { content: [{ type: "text", text: JSON.stringify({
                            status: 'failure',
                            error: `Unknown action "${action}"`
                        }, null, 2) }] };
                }
            } catch (e) {
                return { content: [{ type: "text", text: JSON.stringify({
                    status: 'failure',
                    error: String(e)
                }, null, 2) }] };
            }
        }
    );
}
```

#### Pattern C: Complex Operation Tool

**Use when**: Advanced logic like discussion management, position-based operations, multi-step workflows

**Standard features**:
- Specialized parameters (may not include projectname if using projectId directly)
- Custom logic for specific use cases
- May use direct API calls
- May fetch and update existing data
- Structured responses appropriate to operation

**Template structure**: Highly variable based on specific needs

### Step 4: Generate Zod Schema

**Common Parameter Patterns**:

```typescript
// IDs (internal issue/MR number)
{name}Iid: z.number().describe("The internal ID (IID) of the {resource} to {action}")

// Project ID (for tools that need direct ID)
projectId: z.number().describe("The project ID")

// Names/identifiers
{name}: z.string().describe("{Resource} name (e.g., 'feature/user-auth')")

// Action enums (for multi-action tools)
action: z.enum(["action1", "action2", "action3"]).describe("Action to perform on the {resource}")

// Optional filters
state: z.enum(["opened", "closed", "all"]).optional().describe("Filter by state (default: 'opened')")
labels: z.string().optional().describe("Comma-separated list of label names to filter by")
// OR for multi-action tools:
labels: z.array(z.string()).optional().describe("For add-labels action: labels to add")

// Pagination
page: z.number().optional().describe("Page number for pagination (default: 1)")
perPage: z.number().optional().describe("Number of items per page (default: 20, max: 100)")

// Dates
dueDate: z.string().optional().describe("Due date in ISO 8601 format (YYYY-MM-DD)")

// Position-based parameters (for code review tools)
baseSha: z.string().describe("Base SHA for the diff")
startSha: z.string().describe("Start SHA for the diff")
headSha: z.string().describe("Head SHA for the diff")
newPath: z.string().describe("Path to the file being reviewed")
newLine: z.number().optional().describe("Line number in the new file")

// Project (standard for simple CRUD, optional for complex tools)
projectname: z.string().optional().describe("GitLab project name (if not provided, you'll be prompted to select)")

// Format (only for simple get/list operations)
format: z.enum(["detailed", "concise"]).optional().describe("Response format - 'detailed' includes all metadata, 'concise' includes only key information")
```

**Important notes**:
- Add `.describe()` with clear examples for all parameters
- Use `z.array(z.string())` for arrays in multi-action tools
- Note when square brackets `[]` are allowed in descriptions for paths/labels/markdown
- Make parameters optional when sensible defaults exist

### Step 5: Generate Response Formats

#### Simple CRUD Tools (Pattern A)

**Concise format** (with emojis):
```typescript
if (format === "concise") {
    return { content: [{ type: "text", text:
        `{emoji} {Resource} #{id}: {title}\n` +
        `📊 Status: {state}\n` +
        `👤 {role}: {user}\n` +
        `🏷️ Labels: {labels}\n` +
        `🎯 Milestone: {milestone}\n` +
        `📅 Due: {due_date}\n` +
        `🔗 URL: {web_url}`
    }] };
}
```

**Detailed format** (full JSON):
```typescript
return { content: [{ type: "text", text: JSON.stringify({resource}, null, 2) }] };
```

**Emoji Guide**:
- 🔍 - Get/View operations
- 📋 - List operations
- ✨ - Create operations
- 🔄 - Update operations
- 🗑️ - Delete operations
- 📊 - Status/State
- 👤 - User/Assignee
- 🏷️ - Labels
- 🎯 - Milestone
- 📅 - Dates
- 🔗 - URLs
- ✅ - Success/Completed
- ❌ - Error/Failed

#### Multi-Action Tools (Pattern B)

**Structured JSON format**:
```typescript
// Success response
{
    status: 'success',
    action: 'action-name',
    message: 'Human-readable success message',
    {resource}: {
        id: resource.id,
        iid: resource.iid,
        title: resource.title,
        webUrl: resource.web_url,
        // Other key fields relevant to the action
    }
}

// Failure response
{
    status: 'failure',
    action: 'action-name',
    error: 'Detailed error message with context',
    {resource}: {
        id: resource.id,
        iid: resource.iid,
        title: resource.title,
        webUrl: resource.web_url
    }
}
```

#### Complex Tools (Pattern C)

Custom format based on operation needs. Examples:
```typescript
// Discussion update/create
{
    action: "updated" | "created",
    discussion_id: "...",
    note_id: "...",
    updated_note: {...}
}
```

### Step 6: Add Error Handling

**Standard Error Patterns**:

```typescript
// Project not selected (for tools with projectname parameter)
if (!projectName) {
    return { content: [{ type: "text", text: JSON.stringify({
        type: "error",
        error: "Project not found or not selected. Please provide a valid project name."
    }) }] };
}

// Project not found
if (!projectId) {
    return { content: [{ type: "text", text: JSON.stringify({
        type: "error",
        error: `Could not find project "${projectName}". Please verify the project name is correct and you have access to it.`
    }) }] };
}

// Resource not found
if (!resource) {
    return { content: [{ type: "text", text: JSON.stringify({
        type: "error",
        error: `{Resource} not found. Please verify the {parameters} are correct.`
    }) }] };
}

// Missing required parameters (for multi-action tools)
if (!requiredParam) {
    return { content: [{ type: "text", text: JSON.stringify({
        status: 'failure',
        action: action,
        error: "Required parameter missing. Please specify...",
        {resource}: { /* minimal info */ }
    }, null, 2) }] };
}

// API call failure (for multi-action tools using fetch)
if (!response.ok) {
    return { content: [{ type: "text", text: JSON.stringify({
        status: 'failure',
        action: action,
        error: `Failed to {action}. Status: ${response.status}`,
        {resource}: { /* minimal info */ }
    }, null, 2) }] };
}

// General error (catch block)
catch (e) {
    // For simple CRUD tools:
    return { content: [{ type: "text", text: JSON.stringify({
        type: "error",
        error: `Error {operation}: ${String(e)}. Please check your GitLab connection and permissions.`
    }) }] };

    // For multi-action tools:
    return { content: [{ type: "text", text: JSON.stringify({
        status: 'failure',
        error: `Error {operation}: ${String(e)}`
    }, null, 2) }] };
}
```

### Step 7: Register in gitlab-tool.ts

After creating the tool file, add registration:

```typescript
// In src/tools/gitlab-tool.ts

// Add import at top
import { register{FunctionName} } from './gitlab/gitlab-{tool-name}';

// Add registration in registerGitlabTools function
export function registerGitlabTools(server: McpServer) {
    // ... other registrations
    register{FunctionName}(server);
}
```

## Interactive Generation Workflow

### Ask User (Only if unclear):

1. **Tool Type**:
   - "Is this a simple CRUD operation, multi-action tool, or complex operation?"
   - Clarify if multiple actions should be combined in one tool

2. **Tool Purpose**:
   - "What GitLab operation should this tool perform?"
   - Examples: "Get merge request details", "Manage issues (get, update, close)", "Review code inline"

3. **Required Parameters**:
   - "What parameters are required?"
   - Examples: "merge request IID", "issue IID and action type", "project ID and position data"

4. **Optional Parameters**:
   - "Any optional filters or options?"
   - Examples: "state filter", "label filter", "format option"

5. **API Method** (if not obvious):
   - "Which GitLab service method to use?"
   - Check `src/services/gitlab-client.ts` for available methods
   - Note if direct fetch API calls are needed

### Generate Files:

1. **Create tool file**: `src/tools/gitlab/gitlab-{tool-name}.ts`
2. **Show registration code** for `src/tools/gitlab-tool.ts`
3. **Provide usage examples** based on tool type

## Output Format

After generating the tool:

```markdown
✅ MCP Tool Created: {tool-name}

📁 Files Created:
- `src/tools/gitlab/gitlab-{tool-name}.ts`

🔧 Type: {Simple CRUD | Multi-Action | Complex Operation}
🔧 Function: register{FunctionName}

📝 Next Steps:
1. Add registration to `src/tools/gitlab-tool.ts`:
   ```typescript
   import { register{FunctionName} } from './gitlab/gitlab-{tool-name}';
   // In registerGitlabTools:
   register{FunctionName}(server);
   ```

2. Rebuild the project:
   ```bash
   npm run build
   ```

3. Test the tool:
   ```bash
   npm run dev
   ```

🎯 Usage Examples:
{Type-specific examples}

📖 Tool registered as: "{tool-name}"
```

## GitLab Service Methods Reference

Common methods available in `gitlab-client.ts`. Latest update 31/10/2025:

**Issues**:
- `getIssue(projectId, iid)`
- `getIssues(projectId, options)`
- `createIssue(projectId, data)`
- `updateIssue(projectId, iid, data)`

**Merge Requests**:
- `getMergeRequest(projectId, iid)`
- `getMergeRequests(projectId, options)`
- `createMergeRequest(projectId, data)`
- `updateMergeRequest(projectId, iid, data)`
- `approveMergeRequest(projectId, iid)`
- `getMrDiscussions(projectId, iid)`
- `addMrComments(projectId, iid, data)`
- `updateMrDiscussionNote(projectId, iid, discussionId, noteId, body)`

**Branches**:
- `getBranches(projectId, options)`
- `createBranch(projectId, branchName, ref)`
- `deleteBranch(projectId, branchName)`

**Pipelines**:
- `getPipelines(projectId, options)`
- `getPipeline(projectId, pipelineId)`
- `createPipeline(projectId, ref)`

**Milestones**:
- `getMilestone(projectId, milestoneId)`
- `getMilestones(projectId, options)`
- `createMilestone(projectId, data)`
- `updateMilestone(projectId, milestoneId, data)`

**Projects**:
- `getProjectId(projectName)`
- `getProject(projectId)`
- `searchProjects(search)`

**Users**:
- `getUserIdByUsername(username)`

**Direct Fetch API**:
For operations not covered by service methods, use direct fetch:
```typescript
const response = await fetch(`${service.gitlabUrl}/api/v4/projects/${projectId}/{endpoint}`, {
    method: 'PUT' | 'POST' | 'GET' | 'DELETE',
    headers: service['getHeaders'](),
    body: JSON.stringify({...})
});
```

## Key Patterns to Follow

1. **Always use appropriate tool pattern** based on operation type
2. **Simple CRUD tools**: Include `projectname` and `format` parameters
3. **Multi-action tools**: Use `action` enum and structured responses
4. **Always clean HTML content** with `cleanGitLabHtmlContent()` where applicable
5. **Always validate project exists** before API calls (if using projectname)
6. **Always use descriptive error messages** with context
7. **Always use emojis in concise format** for simple CRUD tools
8. **Always follow kebab-case** for file and tool names
9. **Always follow PascalCase** for function names
10. **Always provide detailed Zod descriptions** with examples
11. **Always handle null/undefined responses** gracefully
12. **Multi-action tools**: Return structured JSON with status/action/message
13. **Direct API calls**: Use fetch and check response.ok
14. **Note square bracket support**: Add notes about `[]` support in descriptions where relevant (file paths, labels, markdown)

## Quality Checklist

Before presenting the generated tool:

- ✅ File name is kebab-case
- ✅ Function name is PascalCase with "register" prefix
- ✅ All imports are correct
- ✅ Zod schema has detailed descriptions
- ✅ Appropriate tool pattern selected (Simple CRUD / Multi-Action / Complex)
- ✅ For simple CRUD: projectname optional, format parameter included
- ✅ For multi-action: action enum, structured responses, conditional params
- ✅ HTML content cleaned where applicable
- ✅ Error messages are descriptive and actionable
- ✅ Response format matches tool type
- ✅ Try-catch wraps the entire handler
- ✅ All responses follow `{ content: [{ type: "text", text: ... }] }` format
- ✅ Tool follows MCP SDK patterns
- ✅ Code matches project conventions from CLAUDE.md

---

**Ready to generate MCP tools!** Tell me what GitLab operation you want to create a tool for.
