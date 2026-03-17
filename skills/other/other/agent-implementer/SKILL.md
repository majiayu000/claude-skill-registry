---
name: agent-implementer
description: Implementation guidance for creating individual agents in the Arcanea system with proper structure, capabilities, and integration.
version: 1.0.0
author: Arcanea Team
emoji: 🎭
tags: [agents, implementation, coding, templates]
---

# Agent Implementer Skill

## Purpose

Create individual agents for the Arcanea ecosystem with proper structure, capabilities, and integration points.

## When to Use

- Adding new agents to the registry
- Modifying existing agent capabilities
- Creating agent-specific prompts
- Implementing agent routing logic
- Testing agent performance

## Agent Structure

### Required Properties

```typescript
interface Agent {
  // Identity
  id: string;              // Unique kebab-case ID
  name: string;            // Display name
  command: string;         // Invocation command (/id)
  
  // Classification
  court: string;           // Guardian court name
  element: string;         // Fire/Water/Earth/Air/Void
  frequency: string;       // Operating frequency
  
  // Capabilities
  specialty: string;       // One-line description
  capabilities: string[];  // What they can do
  skills: string[];        // Available skills
  triggers: string[];      // Activation keywords
  
  // Configuration
  promptTemplate: string;  // System prompt template
  examples: string[];      // Example outputs
  parameters: ParamSchema; // Input parameters
  
  // Metadata
  version: string;         // Agent version
  author: string;          // Creator
  tier: 'free' | 'premium'; // Access level
}
```

## Implementation Steps

### Step 1: Define Agent Identity

**Questions to answer:**
1. What is the agent's core purpose?
2. Which court does it belong to?
3. What frequency does it operate at?
4. What makes it unique?

**Example:**
```typescript
const ignitionAgent = {
  id: "ignition",
  name: "Ignition",
  command: "/ignition",
  court: "Draconia",
  element: "fire",
  frequency: "528Hz",
  specialty: "Spark rapid creative ideas"
};
```

### Step 2: Define Capabilities

**List what the agent can do:**
- Generate ideas rapidly
- Break creative blocks
- Initiate projects
- Provide energetic momentum

**Map to skills:**
- `/fire ignite`
- `/fire intensify`
- `/foundation begin`

### Step 3: Create Prompt Template

**Template structure:**
```
You are {name} from the {court} Court.
Frequency: {frequency} | Element: {element}
Specialty: {specialty}

Your approach:
- {Characteristic 1}
- {Characteristic 2}
- {Characteristic 3}

Task: {{task}}
Context: {{context}}

Provide your contribution as {name}:
```

**Example for Ignition:**
```
You are Ignition from the Draconia Court.
Frequency: 528Hz | Element: Fire
Specialty: Spark rapid creative ideas

Your approach:
- High-energy, passionate
- Fast generation over perfection
- Bold, unconventional ideas
- Fearless creativity

Task: {{task}}
Context: {{context}}

Ignite creative fire. Generate 10 bold, energetic ideas rapidly.
Don't self-censor. Embrace wild possibilities.
```

### Step 4: Define Triggers

**Keywords that activate this agent:**
```typescript
triggers: [
  "stuck",
  "blocked", 
  "can't start",
  "ignite",
  "spark",
  "rapid",
  "brainstorm",
  "ideas"
]
```

### Step 5: Set Parameters

**What inputs does the agent need?**
```typescript
parameters: {
  task: {
    type: "string",
    required: true,
    description: "What to generate ideas for"
  },
  count: {
    type: "number",
    required: false,
    default: 10,
    description: "Number of ideas to generate"
  },
  temperature: {
    type: "number",
    required: false,
    default: 0.9,
    description: "Creativity level (0.1-1.0)"
  }
}
```

### Step 6: Register Agent

**Add to registry:**
```typescript
// In arcanea-agents/registry.js
const AGENT_REGISTRY = {
  courts: {
    elemental: {
      fire: {
        guardian: "Draconia",
        agents: [
          // ... other agents
          {
            id: "ignition",
            name: "Ignition",
            // ... all properties
          }
        ]
      }
    }
  }
};
```

### Step 7: Test Agent

**Create test cases:**
```typescript
// Test ignition agent
describe('Ignition Agent', () => {
  test('generates ideas for character', async () => {
    const result = await invokeAgent('ignition', {
      task: 'Create a cyberpunk character'
    });
    expect(result.output).toContain('character');
    expect(result.output.split('\n').length).toBeGreaterThan(5);
  });
});
```

## Agent Templates

### Fire Court Agent Template

```typescript
{
  id: "{kebab-name}",
  name: "{TitleCaseName}",
  command: "/{kebab-name}",
  court: "Draconia",
  element: "fire",
  frequency: "{396|528|639|741|852|963}Hz",
  specialty: "{One-line specialty}",
  personality: "{Fiery, passionate, transformative}",
  capabilities: ["{capability1}", "{capability2}"],
  skills: ["/fire {skill1}", "/fire {skill2}"],
  triggers: ["{keyword1}", "{keyword2}"],
  promptTemplate: `You are {name} from the Draconia Court...
  
Task: {{task}}

Approach with fire: intense, passionate, transformative.
{specific_instructions}`,
  examples: ["{example1}", "{example2}"]
}
```

### Water Court Agent Template

```typescript
{
  id: "{kebab-name}",
  name: "{TitleCaseName}",
  command: "/{kebab-name}",
  court: "Leyla",
  element: "water",
  frequency: "{396|528|639|741|852}Hz",
  specialty: "{One-line specialty}",
  personality: "{Fluid, emotional, nurturing}",
  capabilities: ["{capability1}", "{capability2}"],
  skills: ["/flow {skill1}", "/flow {skill2}"],
  triggers: ["{keyword1}", "{keyword2}"],
  promptTemplate: `You are {name} from the Leyla Court...
  
Task: {{task}}

Approach with water: flowing, emotional, adaptive.
{specific_instructions}`,
  examples: ["{example1}", "{example2}"]
}
```

## Common Patterns

### Agent with Sub-agents

For complex agents that need specialized modes:

```typescript
{
  id: "structure",
  name: "Structure",
  subModes: [
    { id: "structure-architect", name: "Architect Mode" },
    { id: "structure-foundation", name: "Foundation Mode" },
    { id: "structure-refinement", name: "Refinement Mode" }
  ]
}
```

### Agent with Parameters

For agents that need configuration:

```typescript
{
  id: "depth",
  name: "Depth",
  parameters: {
    depth: {
      type: "enum",
      options: ["surface", "shallow", "deep", "abyssal"],
      default: "deep"
    }
  }
}
```

### Agent with Context Memory

For agents that remember previous interactions:

```typescript
{
  id: "relationship",
  name: "Relationship",
  contextWindow: 5,  // Remember last 5 interactions
  memory: {
    type: "conversation",
    persistence: "session"
  }
}
```

## Best Practices

### Do's
✅ Give each agent a clear, single purpose
✅ Use consistent naming conventions
✅ Document all parameters
✅ Provide example outputs
✅ Test with real tasks
✅ Version your agents

### Don'ts
❌ Create agents that overlap too much
❌ Give agents vague or broad purposes
❌ Forget to add to registry
❌ Skip testing
❌ Hardcode without configuration options

## Validation Checklist

Before an agent is complete:

- [ ] ID is unique and kebab-case
- [ ] Name is clear and descriptive
- [ ] Court assignment is logical
- [ ] Frequency matches gate
- [ ] Specialty is one clear sentence
- [ ] At least 3 capabilities defined
- [ ] At least 3 skills mapped
- [ ] At least 5 trigger keywords
- [ ] Prompt template is complete
- [ ] Examples are provided
- [ ] Added to registry
- [ ] Tests written and passing
- [ ] Documentation complete

## Testing Strategy

### Unit Tests
```typescript
test('agent responds correctly', async () => {
  const agent = getAgent('ignition');
  const result = await agent.invoke('Brainstorm ideas');
  expect(result).toBeDefined();
  expect(result.output).toBeTruthy();
});
```

### Integration Tests
```typescript
test('agent integrates with conductor', async () => {
  const result = await conductor.orchestrate({
    agent: 'ignition',
    task: 'test'
  });
  expect(result.success).toBe(true);
});
```

### User Tests
- Real users try the agent
- Feedback collected
- Iterations made

## Conclusion

Implementing agents requires:
1. **Clear definition** - Know what the agent does
2. **Proper structure** - Follow the template
3. **Thorough testing** - Validate functionality
4. **Documentation** - Help users understand

Each agent is a specialized creative partner. Build them well.

---

*Use this skill when implementing or modifying agents in the Arcanea ecosystem.*
