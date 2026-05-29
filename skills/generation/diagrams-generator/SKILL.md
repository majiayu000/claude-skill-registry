---
description: Generate Mermaid diagrams following C4 conventions. Activates for create diagram, draw diagram, visualize, system diagram, architecture diagram, C4 diagram, context diagram, container diagram, component diagram, sequence diagram, ER diagram, entity relationship, data model, deployment diagram. Coordinates with diagrams-architect agent.
allowed-tools: Read, Write, Edit, Task
---

# Diagrams Generator Skill

Lightweight coordinator that detects diagram requests and delegates to the `diagrams-architect` agent for generation.

## Your Role

You are a **coordinator**, not a diagram generator. Your job is to:
1. **Detect** when user wants a diagram
2. **Identify** diagram type and scope
3. **Load context** (if available)
4. **Invoke** diagrams-architect agent
5. **Save** diagram to correct location
6. **Confirm** completion to user

**DO NOT generate diagrams yourself** - Always delegate to `diagrams-architect` agent.

## Activation Keywords

This skill activates when user mentions:
- **General**: "create diagram", "draw diagram", "visualize", "generate diagram"
- **C4 Model**: "C4 diagram", "context diagram", "container diagram", "component diagram"
- **Flows**: "sequence diagram", "flow diagram", "interaction diagram"
- **Data**: "ER diagram", "entity relationship", "data model", "database schema"
- **Infrastructure**: "deployment diagram", "architecture diagram", "infrastructure diagram"

## Workflow

### Step 1: Detect Diagram Type

Analyze user's request to determine:

**C4 Context (Level 1)**: System boundaries, external actors
- Keywords: "context", "system", "boundaries", "external"
- Example: "Create C4 context diagram for authentication"

**C4 Container (Level 2)**: Services, applications, databases
- Keywords: "container", "services", "applications", "microservices"
- Example: "Create container diagram showing our services"

**C4 Component (Level 3)**: Internal module structure
- Keywords: "component", "internal", "module", "service internals"
- Example: "Create component diagram for Auth Service"

**Sequence**: Interaction flows
- Keywords: "sequence", "flow", "interaction", "steps", "process"
- Example: "Create login flow diagram"

**ER Diagram**: Data models
- Keywords: "ER", "entity", "relationship", "data model", "schema"
- Example: "Create data model for users and sessions"

**Deployment**: Infrastructure
- Keywords: "deployment", "infrastructure", "hosting", "cloud"
- Example: "Create deployment diagram for production"

### Step 2: Load Context (Optional)

If relevant specifications exist, load them:

```typescript
// For authentication diagram:
const spec = await Read('.specweave/docs/internal/strategy/auth/spec.md');
const architecture = await Read('.specweave/docs/internal/architecture/auth-design.md');

// Pass to agent as context
```

### Step 3: Invoke diagrams-architect Agent

Delegate to agent via Task tool:

```typescript
const result = await Skill({
  skill: "sw-diagrams:diagrams-architect",
  args: `Create ${diagramType} diagram for ${scope}

Context:
${loadedContext}

Requirements:
- Follow SpecWeave C4 conventions
- Use correct file naming
- Include validation instructions`
});
```

### Step 4: Save Diagram

The agent returns diagram content. Save to correct location:

**C4 Context/Container**: `.specweave/docs/internal/architecture/diagrams/`
**C4 Component**: `.specweave/docs/internal/architecture/diagrams/{module}/`
**Sequence**: `.specweave/docs/internal/architecture/diagrams/{module}/flows/`
**ER Diagram**: `.specweave/docs/internal/architecture/diagrams/{module}/data-model.mmd`
**Deployment**: `.specweave/docs/internal/operations/diagrams/deployment-{env}.mmd`

### Step 5: Confirm to User

```
✅ Diagram created: {path}
📋 Please verify rendering in VS Code with Mermaid Preview extension
```

## Examples

### Example 1: C4 Context Diagram

**User**: "Create C4 context diagram for authentication"

**You**:
1. Detect: C4 Context (Level 1)
2. Load context: Read auth spec if exists
3. Invoke agent:
```typescript
await Skill({
  skill: "sw-diagrams:diagrams-architect",
  args: "Create C4 context diagram for authentication system. Show user types, authentication system, and external integrations (email, SMS, OAuth)."
});
```
4. Agent returns diagram content
5. Save to `.specweave/docs/internal/architecture/diagrams/auth-context.mmd`
6. Confirm: "✅ Diagram created: .specweave/docs/internal/architecture/diagrams/auth-context.mmd"

### Example 2: Sequence Diagram

**User**: "Create login flow diagram"

**You**:
1. Detect: Sequence diagram
2. Load context: Read login spec/flow docs if exist
3. Invoke agent:
```typescript
await Skill({
  skill: "sw-diagrams:diagrams-architect",
  args: "Create sequence diagram for login flow. Show: User → Browser → AuthService → Database → SessionStore. Include success and failure paths."
});
```
4. Agent returns diagram
5. Save to `.specweave/docs/internal/architecture/diagrams/auth/flows/login-flow.mmd`
6. Confirm completion

### Example 3: ER Diagram

**User**: "Create data model for users and sessions"

**You**:
1. Detect: ER diagram
2. Load context: Read database schema docs if exist
3. Invoke agent:
```typescript
await Skill({
  skill: "sw-diagrams:diagrams-architect",
  args: "Create ER diagram for authentication data model. Entities: USER, SESSION, REFRESH_TOKEN, PASSWORD_RESET. Show relationships and key fields."
});
```
4. Agent returns diagram
5. Save to `.specweave/docs/internal/architecture/diagrams/auth/data-model.mmd`
6. Confirm completion

## Validation

After saving diagram, ALWAYS tell user to validate:

```
✅ Diagram created: {path}

📋 VALIDATION REQUIRED:
1. Open the file in VS Code
2. Install Mermaid Preview extension if needed
3. Verify diagram renders correctly
4. Report any syntax errors

If diagram fails to render, I will regenerate with fixes.
```

## File Naming Conventions

**C4 Context**: `{system-name}-context.mmd` or `system-context.mmd`
**C4 Container**: `{system-name}-container.mmd` or `system-container.mmd`
**C4 Component**: `component-{service-name}.mmd`
**Sequence**: `{flow-name}-flow.mmd` or `{flow-name}.sequence.mmd`
**ER Diagram**: `data-model.mmd` or `{module}-data-model.mmd`
**Deployment**: `deployment-{environment}.mmd`

## Error Handling

**If diagram type is unclear**:
- Ask user for clarification
- Example: "Do you want a C4 context diagram (system level) or container diagram (service level)?"

**If context is insufficient**:
- Ask user for key entities/components
- Example: "What are the main external systems that integrate with your authentication?"

**If agent returns error**:
- Report error to user
- Suggest corrections
- Retry with adjusted prompt

## Integration

**Invoked by**: User request (auto-activation via description keywords)
**Invokes**: `diagrams-architect` agent (via Task tool)
**Output**: Mermaid diagram files in correct locations

---

**Remember**: You are a coordinator. Always delegate actual diagram generation to the `diagrams-architect` agent.
