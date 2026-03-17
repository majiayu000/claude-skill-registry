---
name: microsoft-365-agents-toolkit
description: Expert guidance for Microsoft 365 and Copilot development using the Teams Toolkit MCP server. Access manifest schemas, knowledge base, code snippets for Teams AI/JS/botbuilder SDKs, and troubleshooting. Use when building Microsoft 365 agents, Teams apps, Copilot extensions, or working with Teams development SDKs.
---

# Microsoft 365 Agents Toolkit Expert

Expert guidance for building Microsoft 365 agents, Teams applications, and Copilot extensions using the Microsoft 365 Agents Toolkit MCP server. Access schemas, documentation, code samples, and troubleshooting resources.

## Core Capabilities

1. **Schema Access** - Retrieve manifest schemas for apps and agents
2. **Knowledge Retrieval** - Access Microsoft 365 and Copilot documentation
3. **Code Snippets** - Get templates and SDK examples
4. **Troubleshooting** - Solutions for common development issues

## Quick Reference - MCP Tools

| Tool | Purpose | Parameters |
|------|---------|------------|
| `get_schema` | Get manifest schemas | schema_name, schema_version |
| `get_knowledge` | Access M365 documentation | question |
| `get_code_snippets` | Get SDK code examples | question |
| `troubleshoot` | Get problem solutions | question |

---

## Instructions

### Tool 1: get_schema

Access manifest and schema definitions for Microsoft 365 development.

**Purpose:** Retrieve JSON schemas for validating and understanding manifest structures.

**When to use:**
- Creating or validating app manifests
- Building declarative agents
- Developing API plugins
- Working with Teams Toolkit YAML files

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| schema_name | enum | Yes | Schema type to retrieve |
| schema_version | string | Yes | Version (e.g., "v1.4") or "latest" |

**Schema Types:**
- `App manifest` - Teams app manifest schema
- `Declarative agent manifest` - Copilot declarative agent schema
- `API plugin manifest` - API plugin manifest schema
- `M365 agents yaml` - Teams Toolkit YAML schema

**Example Usage:**

```
Get latest Teams app manifest schema:
  schema_name: "App manifest"
  schema_
Get specific declarative agent   schema_
Get API plugin schema:
  schema_name: "API plugin manifest"
  schema_```

**Schema Versions:**
- App manifest: v1.23 (latest)
- Declarative agent manifest: v1.4 (latest)
- API plugin manifest: v2.3 (latest)
- M365 agents yaml: v1.9 (latest)

---

### Tool 2: get_knowledge

Search Microsoft 365 and Copilot development documentation.

**Purpose:** Access comprehensive knowledge base for M365 development topics.

**When to use:**
- Understanding Microsoft 365 concepts
- Learning Copilot extension development
- Researching Teams platform capabilities
- Finding best practices and guidelines

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| question | string | Yes | Search query or question |

**Topics Covered:**
- Microsoft 365 Copilot development
- Teams app development
- Declarative agents
- Message extensions
- Adaptive cards
- Authentication and SSO
- Bot framework integration
- Microsoft Graph API
- Deployment and distribution

**Example Queries:**

```
"How do I create a declarative agent for Copilot?"
"What are the authentication options for Teams apps?"
"How to implement SSO in a Teams tab?"
"What is a message extension and how does it work?"
"Best practices for Adaptive Card design"
"How to call Microsoft Graph API from a Teams app?"
```

**Query Tips:**
- Be specific about the technology or feature
- Include the platform (Teams, Copilot, M365)
- Ask about "how to" for implementation guidance
- Use "what is" for conceptual understanding
- Mention specific SDKs when relevant

---

### Tool 3: get_code_snippets

Access templates and SDK code examples.

**Purpose:** Retrieve implementation examples and starter code for Microsoft 365 development.

**When to use:**
- Implementing Teams AI SDK features
- Using Teams JavaScript SDK
- Working with Bot Builder SDK
- Creating message extensions
- Building adaptive cards
- Implementing authentication flows

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| question | string | Yes | Query for code examples |

**SDK Coverage:**
- **@microsoft/teams-ai** - Teams AI Library
- **@microsoft/teams-js** - Teams JavaScript SDK
- **botbuilder** - Bot Framework SDK
- Related SDKs and libraries

**Example Queries:**

```
"Teams AI SDK: How to create a simple bot?"
"Teams JS SDK: Implementing tab authentication"
"Bot Builder: Creating a dialog flow"
"Message extension with action commands"
"Adaptive Card with input validation"
"Teams AI: Using AI prompts and actions"
"SSO implementation example for Teams tab"
"Bot Builder: Handling conversation updates"
```

**Code Snippet Categories:**
- Bot creation and configuration
- Tab development
- Message extensions
- Authentication (SSO)
- Adaptive Cards
- AI integration
- Graph API calls
- Conversation handling

---

### Tool 4: troubleshoot

Get solutions for common development issues.

**Purpose:** Access troubleshooting guidance for Microsoft 365 development problems.

**When to use:**
- Encountering errors during development
- Debugging Teams app issues
- Resolving authentication problems
- Fixing manifest validation errors
- Solving deployment issues

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| question | string | Yes | Description of the issue |

**Common Issue Categories:**
- Manifest validation errors
- Authentication failures
- Bot not responding
- Tab loading issues
- Message extension errors
- Deployment failures
- Teams Toolkit errors
- Azure configuration problems
- Graph API errors
- SSO issues

**Example Queries:**

```
"Teams app manifest validation fails with error X"
"Bot returns 500 error when invoked"
"SSO authentication not working in Teams tab"
"Cannot sideload app in Teams"
"Message extension not appearing in compose box"
"Azure deployment fails with error"
"Graph API returns 403 Forbidden"
"Teams Toolkit provision fails"
```

**Troubleshooting Tips:**
- Include the specific error message
- Mention the component having issues (bot, tab, etc.)
- Specify the SDK or tool version if known
- Describe what you were trying to do
- Include relevant error codes

---

## Development Workflows

### Creating a Teams App

**Workflow:**
```
1. get_knowledge: "How to create a Teams app with Teams Toolkit?"
2. get_schema: App manifest (latest) - understand required fields
3. get_code_snippets: "Teams app starter template"
4. Implement app based on guidance
5. troubleshoot: Any issues encountered
```

### Building a Declarative Agent

**Workflow:**
```
1. get_knowledge: "What is a declarative agent for Copilot?"
2. get_schema: Declarative agent manifest (latest)
3. get_code_snippets: "Declarative agent example"
4. Create agent manifest
5. get_knowledge: "How to test declarative agents?"
6. troubleshoot: Issues during testing
```

### Implementing Bot Functionality

**Workflow:**
```
1. get_code_snippets: "Bot Builder basic bot example"
2. get_knowledge: "Bot Framework best practices"
3. get_code_snippets: "Handling conversation updates"
4. Implement bot logic
5. get_code_snippets: "Adaptive Card examples"
6. troubleshoot: Bot errors or unexpected behavior
```

### Adding Authentication

**Workflow:**
```
1. get_knowledge: "SSO authentication in Teams apps"
2. get_code_snippets: "Teams tab SSO implementation"
3. get_knowledge: "Microsoft Graph API authentication"
4. Implement auth flow
5. troubleshoot: "SSO not working" (if issues)
```

### Creating a Message Extension

**Workflow:**
```
1. get_knowledge: "What are message extensions?"
2. get_schema: App manifest (check message extension properties)
3. get_code_snippets: "Message extension with search command"
4. Implement extension
5. get_code_snippets: "Adaptive Card for search results"
6. troubleshoot: "Message extension not appearing"
```

---

## Best Practices

### Schema Usage
1. **Always use "latest"** for new projects unless specific version required
2. **Validate manifests** against schemas before deployment
3. **Check schema updates** when upgrading SDK versions
4. **Reference schemas** in IDEs for autocomplete and validation

### Knowledge Queries
1. **Be specific** - Include platform and technology name
2. **Start broad** - Get overview before deep-diving
3. **Follow up** - Ask related questions for complete understanding
4. **Verify versions** - Check if guidance applies to your SDK version

### Code Snippets
1. **Understand before copying** - Review code carefully
2. **Adapt to context** - Modify examples for your use case
3. **Check dependencies** - Ensure required packages installed
4. **Test thoroughly** - Validate examples work as expected
5. **Combine snippets** - Use multiple examples together

### Troubleshooting
1. **Include error details** - Provide complete error messages
2. **Describe context** - What were you doing when error occurred?
3. **Check logs** - Review console and debug output
4. **Isolate issue** - Narrow down to specific component
5. **Try solutions incrementally** - Test one fix at a time

---

## Manifest Types Reference

### App Manifest (Teams App)

**Purpose:** Defines Teams app package structure, capabilities, and metadata.

**Key Sections:**
- `$schema` - Schema URL for validation
- `manifestVersion` - Version of manifest format
- `id` - Unique app identifier (GUID)
- `version` - App version (semantic versioning)
- `packageName` - Reverse domain name identifier
- `developer` - Developer information
- `name` - App names (short and full)
- `description` - App descriptions
- `icons` - App icon URLs
- `accentColor` - App theme color
- `bots` - Bot capabilities
- `composeExtensions` - Message extensions
- `staticTabs` - Tab configurations
- `configurableTabs` - Configurable tabs
- `permissions` - Required permissions
- `validDomains` - Allowed domains

**Use get_schema to explore complete structure.**

---

### Declarative Agent Manifest

**Purpose:** Defines Copilot declarative agent configuration and capabilities.

**Key Sections:**
- `$schema` - Schema validation URL
- `id` - Unique agent identifier
- `version` - Agent version
- `name` - Agent name
- `description` - Agent purpose
- `instructions` - System prompt and behavior
- `conversation_starters` - Suggested prompts
- `actions` - API actions agent can perform
- `capabilities` - Agent capabilities (web_search, etc.)

**Use get_schema to see full specification.**

---

### API Plugin Manifest

**Purpose:** Defines API plugins for Copilot extensions.

**Key Sections:**
- `$schema` - Schema URL
- `schema_version` - Version of schema
- `name_for_human` - Human-readable name
- `name_for_model` - Model-facing name
- `description_for_human` - User-facing description
- `description_for_model` - Model instruction
- `auth` - Authentication configuration
- `api` - OpenAPI specification reference
- `logo_url` - Plugin logo
- `contact_email` - Support contact
- `legal_info_url` - Legal information

**Use get_schema for complete details.**

---

### M365 Agents YAML

**Purpose:** Teams Toolkit project configuration file.

**Key Sections:**
- `version` - YAML schema version
- `environmentFolderPath` - Environment configs location
- `provision` - Provisioning steps
- `deploy` - Deployment steps
- `publish` - Publishing configuration
- `projectId` - Unique project identifier

**Use get_schema for full YAML structure.**

---

## SDK Reference

### @microsoft/teams-ai

**Purpose:** AI-powered Teams app development library.

**Key Features:**
- AI prompt management
- Action planning
- Conversation handling
- State management
- Authentication

**Use get_code_snippets for:**
- "Teams AI bot setup"
- "AI action handlers"
- "Prompt templates"
- "State management"

---

### @microsoft/teams-js

**Purpose:** Teams JavaScript SDK for client-side development.

**Key Features:**
- Teams context access
- Authentication flows
- Deep linking
- Task modules
- Navigation

**Use get_code_snippets for:**
- "Teams context initialization"
- "SSO authentication"
- "Task module usage"
- "Deep linking"

---

### botbuilder

**Purpose:** Microsoft Bot Framework SDK.

**Key Features:**
- Dialog management
- Activity handling
- Middleware
- State management
- Adaptive Cards

**Use get_code_snippets for:**
- "Bot initialization"
- "Dialog flows"
- "Message handling"
- "Adaptive Card responses"

---

## Common Scenarios

### Scenario 1: Validating App Manifest

```
1. get_schema
   schema_name: "App manifest"
   schema_
2. Review schema structure
3. Validate your manifest.json
4. Fix any validation errors
```

### Scenario 2: Learning About Copilot Extensions

```
1. get_knowledge
   question: "How do Copilot extensions work?"

2. get_knowledge
   question: "Declarative agents vs API plugins"

3. get_schema
   schema_name: "Declarative agent manifest"
   schema_```

### Scenario 3: Implementing a Feature

```
1. get_knowledge
   question: "How to implement [feature]?"

2. get_code_snippets
   question: "[feature] implementation example"

3. Adapt code to your project
4. troubleshoot (if issues arise)
```

### Scenario 4: Debugging an Error

```
1. troubleshoot
   question: "[Error message and context]"

2. Apply suggested solutions
3. get_code_snippets (for corrected implementation)
4. Test fix
```

---

## When to Use This Skill

- Building Microsoft 365 agents and Copilot extensions
- Developing Teams applications (bots, tabs, message extensions)
- Working with Teams AI, Teams JS, or Bot Builder SDKs
- Creating declarative agents for Copilot
- Implementing API plugins
- Troubleshooting Teams development issues
- Validating app manifests
- Learning Microsoft 365 development concepts

## Keywords

microsoft 365, teams, copilot, agents, teams toolkit, bot framework, teams ai sdk, teams js sdk, bot builder, declarative agent, message extension, adaptive cards, manifest, api plugin, sso, authentication, microsoft graph, teams app, copilot extension, m365 development
