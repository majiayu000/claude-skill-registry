---
name: skill-creator-agent
description: Creates Claude Code skills where each skill is tied to a specialist agent optimized with evidence-based prompting techniques. Use this skill when users need to create reusable skills that leverage specialized agents for consistent high-quality performance. The skill ensures that each created skill spawns an appropriately crafted agent that communicates effectively with the parent Claude Code instance using best practices.
---

# Skill Creator with Agent Specialization

This skill extends the standard skill creation process by tying each skill to a specialist agent that is invoked when the skill is triggered. Rather than having Claude Code directly execute skill instructions, this approach spawns a specialized agent configured with optimal prompting patterns, domain expertise, and communication protocols. The result is more consistent, higher-quality outputs and better separation of concerns.

## When to Use This Skill

Use the skill-creator-agent skill when creating skills for complex domains where specialist expertise significantly improves outcomes, when building skills that require consistent behavior across many invocations, when creating skills for team use where quality consistency matters, or when the skill involves multi-step processes that benefit from structured cognitive frameworks. This skill is particularly valuable when building professional-grade tools rather than simple helper scripts.

## Core Concept: Skills as Agent Spawners

Traditional skills provide instructions and resources that Claude Code follows directly. The skill-creator-agent approach instead treats skills as agent spawning mechanisms. When a skill triggers, it instantiates a specialist agent configured specifically for that domain. This architecture provides several advantages that make it worth the additional complexity.

**Separation of Concerns**: The skill itself handles detection, resource management, and context preparation. The specialist agent handles task execution using domain-specific expertise. This clean separation makes both components easier to maintain and test. Changes to how the skill detects when to activate do not affect the agent's execution logic and vice versa.

**Consistent Expertise**: Each invocation of the skill spawns the same specialist agent with the same expertise model, cognitive framework, and quality standards. This consistency is difficult to achieve when Claude Code interprets skill instructions directly because interpretation can vary based on context, recent conversation history, and other factors. Specialist agents maintain their identity and approach more reliably.

**Optimal Prompting Patterns**: Specialist agents can be configured with evidence-based prompting techniques tailored to their domain. A data analysis agent might use program-of-thought decomposition while a content generation agent uses plan-and-solve frameworks. These techniques can be deeply integrated into the agent's system prompt rather than applied ad hoc during task execution.

**Better Error Handling**: Specialist agents can implement sophisticated error detection, recovery, and escalation logic specific to their domain. They can recognize when tasks fall outside their expertise and escalate appropriately rather than producing suboptimal results. This failure mode awareness is harder to encode in general skill instructions.

**Communication Protocol Optimization**: The agent knows exactly how to communicate with the parent Claude Code instance, including progress reporting, intermediate result formatting, and final deliverable packaging. This protocol standardization makes multi-skill workflows more reliable and reduces integration friction.

## Architecture of Agent-Based Skills

Skills created with this framework follow a specific architectural pattern that coordinates between the skill definition and the specialist agent.

### Skill Layer Responsibilities

The skill layer handles trigger detection through the description field that tells Claude Code when this skill is relevant. It manages resource preparation by making scripts, references, and assets available to the agent. It performs context gathering by collecting relevant information from the environment, user input, and related files. Finally, it executes agent spawning by invoking the specialist agent with properly formatted context and awaiting results.

The skill's SKILL.md file should be relatively concise because most execution logic lives in the agent. The skill primarily serves as an interface between Claude Code and the specialized agent, handling the logistics of invocation rather than detailed task execution.

### Agent Layer Responsibilities

The specialist agent handles task execution using its domain-specific methodology and expertise. It manages internal state and reasoning using appropriate cognitive frameworks for its domain. It implements error detection and recovery specific to the types of failures common in its domain. It formats results according to the communication protocol established with the parent. Finally, it provides status reporting through progress updates and completion signals.

The agent's system prompt should be comprehensive and detailed, encoding deep expertise in the domain. This is where evidence-based prompting techniques, failure mode awareness, and quality standards are implemented. The agent should feel like a domain expert rather than a general-purpose assistant.

### Communication Protocol Between Layers

The skill and agent communicate through a well-defined protocol. The skill sends a context package to the agent that includes the task description, relevant files or data references, constraints and requirements, and any skill-specific configuration. The agent sends back progress reports for long-running tasks, formatted results according to specification, error notifications if issues arise, and metadata about the execution such as confidence levels or caveats.

This bidirectional communication should be explicitly defined in both the skill's SKILL.md and the agent's system prompt so both parties understand the contract. Consistency in communication format makes the skills more reliable and easier to debug.

## Creating Skills with Specialist Agents

Follow this systematic process when creating agent-based skills. This extends the standard skill creation process with agent design and integration steps.

### Step 1: Define Skill Scope and Agent Role

Begin by defining what the skill should detect and when it should activate. This becomes the skill's description field. Then define what the specialist agent should do when spawned. The agent's role should be narrower and more focused than the skill's scope because the skill handles triggering while the agent handles execution.

For example, a skill might trigger on "working with API documentation" while the specialist agent is "an API documentation generator that creates comprehensive, standards-compliant API reference documentation." The skill activates broadly while the agent executes narrowly but deeply.

### Step 2: Design Agent Using Agent-Creator Skill

Use the agent-creator skill to design the specialist agent's system prompt. This involves defining the agent's identity and expertise, structuring its task approach and methodology, specifying communication guidelines with the parent, encoding domain-specific knowledge, implementing guardrails and failure mode prevention, and defining output specifications.

The agent-creator skill applies evidence-based prompting techniques automatically and ensures the agent follows best practices for its domain. Invest significant effort here because the agent's quality determines the skill's output quality.

### Step 3: Define Context Handoff Protocol

Specify exactly what information the skill should pass to the agent and in what format. This typically includes the original user request or trigger event, relevant file paths or data that the agent needs to access, constraints such as output format requirements or quality standards, and any skill-specific configuration parameters.

Document this protocol in both the skill's SKILL.md and the agent's system prompt so both components understand the contract. Include examples of actual context packages to make the protocol concrete and testable.

### Step 4: Create Skill Resources

Develop any scripts, references, or assets that either the skill or the agent needs to function optimally. Scripts might include utilities for data processing or file manipulation that the agent can invoke. References might include detailed specifications, schemas, or domain knowledge that the agent should consult. Assets might include templates or boilerplate that the agent uses in its outputs.

**Create Process Visualization Diagram**: Generate a GraphViz .dot file showing both the skill layer and agent layer workflows, their interaction points, and SDK implementation patterns. Follow semantic GraphViz best practices from https://blog.fsck.com/2025/09/29/using-graphviz-for-claudemd/:

- Use **ellipse** for start/end points
- Use **diamond** for decisions (e.g., "Agent spawned successfully?")
- Use **octagon** for critical checkpoints or warnings
- Use **cylinder** for external references (agent-creator skill, SDK libraries)
- Use **folder** for architecture concepts or principles
- Use **subgraph cluster_*** for grouping skill vs agent layers
- Color code: red for stops, orange for warnings, yellow for decisions, green for success
- Use quoted labels and dashed edges for conditional flows

Name the file `<skill-name>-process.dot` in the skill's root directory. The diagram should visualize the two-layer architecture, context handoff protocol, and SDK implementation integration points.

Organize these resources following the standard skill structure with scripts, references, and assets directories. Document in both the skill and agent descriptions which resources are available and how to use them.

### Step 5: Implement Agent Spawning Logic

In the skill's SKILL.md, describe how Claude Code should spawn the specialist agent. This includes instructions for gathering context information, formatting the context package, invoking the agent with the context, awaiting agent results, and processing results before returning to the user.

The spawning logic should be clear and procedural so Claude Code can follow it consistently. Include error handling for cases where the agent cannot be spawned or fails during execution.

### Step 6: Define Result Processing

Specify how Claude Code should process the agent's results before presenting them to the user. This might involve extracting specific fields from structured output, formatting results for readability, combining results with additional context, or validating that the agent completed the task successfully.

Result processing bridges between the agent's technical output format and the user-facing presentation. It ensures that users receive information in an appropriate format even if the agent produces structured data internally.

### Step 7: Test Integration

Test the complete skill-agent integration by simulating realistic use cases, verifying that the skill activates at appropriate times, confirming that context handoff works correctly, checking that the agent executes tasks properly, and validating that results are processed and presented correctly.

Integration testing often reveals assumptions or edge cases that were not apparent during design. Iterate based on test results to refine both the skill and the agent until the integration works smoothly.

### Step 8: Package and Document

Create comprehensive documentation that explains how the skill works, what the specialist agent does, how to use the skill effectively, what outputs to expect, and how to troubleshoot issues. Package both the skill and the agent specification together so they can be deployed as a unit.

Good documentation is especially important for agent-based skills because the two-layer architecture is less transparent than traditional skills. Users should understand that a specialist agent is being spawned and what that agent's capabilities and limitations are.

## Agent System Prompt Template for Skills

When creating the specialist agent for a skill, follow this template structure optimized for skills integration. This extends the general agent system prompt structure with skill-specific elements.

### Identity and Skill Context Section

Begin the agent's system prompt by establishing its identity and its relationship to the parent skill. For example, "I am a specialist API documentation generator agent. I am spawned by the api-documentation skill when Claude Code needs to create comprehensive API reference documentation. My role is to take API specifications or code and transform them into clear, standards-compliant documentation."

This section grounds the agent in its operational context. The agent understands that it is not operating independently but as part of a skill-based workflow with a parent Claude Code instance that invoked it.

### Task Execution Methodology Section

Describe the agent's step-by-step approach to executing tasks in its domain. Incorporate appropriate evidence-based techniques such as plan-and-solve for complex multi-stage tasks, program-of-thought for analytical or computational work, or self-consistency for fact-heavy outputs.

Frame this methodology from the agent's first-person perspective to create a strong procedural identity. The agent should internalize this methodology and apply it consistently across invocations.

### Communication Protocol Section

Explicitly specify how the agent communicates with the parent Claude Code instance. This includes how the agent receives context with field descriptions and format requirements, how it reports progress with checkpoint definitions and update frequency, how it handles errors with error types and escalation criteria, and how it formats results with structure specifications and metadata requirements.

Be very explicit about the communication protocol because this is where integration issues most commonly arise. Provide examples of actual messages in each category.

### Resource Utilization Section

Document what scripts, references, and assets are available to the agent and how to use them effectively. This connects the agent to the skill's bundled resources. For each resource type, specify when to use it, how to invoke or access it, and what to do if the resource is not available or fails.

Resource utilization guidance helps the agent make effective use of the tools provided by the skill layer rather than reinventing functionality or struggling with tasks that could be handled by existing scripts.

### Domain Expertise and Guardrails Section

Encode the agent's deep domain knowledge including patterns, heuristics, and best practices specific to its area of expertise. Include explicit awareness of common failure modes and how to avoid them. Frame guardrails as expert judgment rather than external constraints.

This section transforms the agent from a general assistant into a domain specialist. The depth and specificity of domain knowledge directly impacts output quality.

### Output Specification Section

Define exactly what the agent should produce, including format and structure requirements, completeness criteria, quality standards, and metadata or annotations to include. Be very specific because the parent Claude Code instance will process this output programmatically.

If the output will be parsed, provide exact schemas or format specifications. If the output will be presented to users, specify how to make it clear and actionable.

## Best Practices for Agent-Based Skills

Follow these best practices when creating skills with specialist agents to ensure high quality and reliability.

### Keep Skill Layer Lightweight

The skill's SKILL.md should be relatively concise, focused on triggering, context gathering, agent invocation, and result processing. Resist the temptation to include detailed execution logic in the skill. That logic belongs in the agent's system prompt. A lightweight skill layer is easier to maintain and test.

### Make Agent Layer Comprehensive

Invest effort in creating a comprehensive, detailed agent system prompt that encodes deep domain expertise. The agent should feel like a specialist who has internalized best practices and can handle complex cases independently. A well-designed agent provides consistent high-quality results across diverse inputs.

### Establish Clear Contracts

The communication protocol between skill and agent should be explicitly documented in both components. Include examples of actual messages or data structures. Clear contracts prevent integration issues and make debugging much easier when problems arise. Ambiguous contracts lead to inconsistent behavior and mysterious failures.

### Test Integration Thoroughly

Test the complete skill-agent integration with realistic use cases and edge cases. Verify that context handoff works, that the agent executes correctly, that results are processed properly, and that errors are handled gracefully. Integration issues are common in two-layer architectures so thorough testing is essential.

### Provide Comprehensive Documentation

Document how the skill works, what the agent does, and how they interact. Include examples of typical use cases and expected outputs. Good documentation makes the skill usable by others and maintainable over time. For agent-based skills, documentation is especially important because the architecture is more complex than traditional skills.

### Iterate Based on Real Use

After initial development, use the skill on real tasks and refine based on experience. Pay attention to where the agent struggles or produces suboptimal results. Strengthen the agent's system prompt in those areas. Iteration based on real use is where agent-based skills really shine because improvements to the agent's expertise directly enhance output quality.

## Implementing Agent-Based Skills with Claude Agent SDK

Transform skill concepts into production-ready implementations using the Claude Agent SDK. The SDK enables programmatic agent spawning, configuration, and lifecycle management within skills.

### TypeScript Implementation for Skills

**Skill-Spawned Agent Pattern**: Create skills that spawn SDK-configured agents:

```typescript
// In your skill's implementation file
import { query, AgentDefinition } from '@anthropic-ai/claude-agent-sdk';

// Define the specialist agent for this skill
const specialistAgent: AgentDefinition = {
  name: 'api-documentation-specialist',
  description: 'Expert in generating comprehensive API documentation',
  systemPrompt: `I am an API documentation specialist. When spawned by the api-documentation skill,
I analyze API code and specifications to generate clear, standards-compliant documentation.

My methodology:
1. Parse API endpoints and data structures
2. Extract parameter types, validation rules, and response formats
3. Generate OpenAPI/Swagger specifications
4. Create human-readable documentation with examples
5. Validate completeness and accuracy

I communicate results in structured format for the parent skill to process and present to users.`,
  allowedTools: ['Read', 'Grep', 'WebFetch'],
  permissionMode: 'acceptEdits'
};

// Skill execution function
export async function executeSkill(context: SkillContext) {
  const { userRequest, relevantFiles, outputFormat } = context;

  // Spawn specialist agent with skill context
  for await (const message of query(
    `Generate API documentation for: ${userRequest}\n\nRelevant files: ${relevantFiles.join(', ')}`,
    {
      systemPrompt: specialistAgent.systemPrompt,
      allowedTools: specialistAgent.allowedTools,
      permissionMode: specialistAgent.permissionMode,
      model: 'claude-sonnet-4-5'
    }
  )) {
    // Process agent messages
    if (message.type === 'assistant') {
      return formatResults(message.content, outputFormat);
    }
  }
}
```

**Multi-Agent Skill Orchestration**: Skills coordinating multiple specialist agents:

```typescript
import { query, AgentDefinition } from '@anthropic-ai/claude-agent-sdk';

const skillAgents: AgentDefinition[] = [
  {
    name: 'code-analyzer',
    description: 'Analyzes code structure and patterns',
    systemPrompt: codeAnalyzerPrompt,
    allowedTools: ['Read', 'Grep', 'Bash'],
    permissionMode: 'acceptEdits'
  },
  {
    name: 'documentation-generator',
    description: 'Generates documentation from analysis',
    systemPrompt: documentationGeneratorPrompt,
    allowedTools: ['Read', 'Write', 'WebFetch'],
    permissionMode: 'plan'
  },
  {
    name: 'quality-validator',
    description: 'Validates documentation quality',
    systemPrompt: qualityValidatorPrompt,
    allowedTools: ['Read'],
    permissionMode: 'default'
  }
];

async function executeMultiAgentSkill(task: string) {
  // Orchestrator spawns and coordinates specialists
  for await (const message of query(task, {
    systemPrompt: orchestratorPrompt,
    agents: skillAgents,
    permissionMode: 'plan',
    model: 'claude-sonnet-4-5'
  })) {
    console.log(message);
  }
}
```

**Custom Tools for Skill-Specific Operations**: Extend agents with domain tools:

```typescript
import { query, tool } from '@anthropic-ai/claude-agent-sdk';
import { z } from 'zod';

// Skill-specific custom tool
const extractApiEndpoints = tool({
  name: 'extractApiEndpoints',
  description: 'Extracts API endpoints from code files',
  parameters: z.object({
    sourceFiles: z.array(z.string()),
    framework: z.string()
  }),
  handler: async ({ sourceFiles, framework }) => {
    // Implementation specific to API extraction
    return { endpoints: [], schemas: [] };
  }
});

const validateDocumentation = tool({
  name: 'validateDocumentation',
  description: 'Validates documentation against OpenAPI spec',
  parameters: z.object({
    docPath: z.string(),
    specPath: z.string()
  }),
  handler: async ({ docPath, specPath }) => {
    // Validation implementation
    return { valid: true, issues: [] };
  }
});

// Skill agent with custom tools
for await (const message of query('Document the API', {
  systemPrompt: apiDocumentationAgentPrompt,
  allowedTools: ['Read', 'Write', extractApiEndpoints, validateDocumentation],
  permissionMode: 'acceptEdits'
})) {
  console.log(message);
}
```

### Python Implementation for Skills

**Stateful Skill Agent Pattern**: Skills maintaining context across operations:

```python
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
import asyncio

class ApiDocumentationSkill:
    def __init__(self):
        self.agent_prompt = """I am an API documentation specialist agent.

My role: Generate comprehensive API documentation from code analysis.

Methodology:
1. Analyze codebase structure and API patterns
2. Extract endpoint definitions and data models
3. Generate OpenAPI specifications
4. Create user-friendly documentation
5. Validate completeness

Communication: I report progress incrementally and format final
documentation as structured JSON for parent skill processing."""

        self.options = ClaudeAgentOptions(
            model='claude-sonnet-4-5',
            system_prompt=self.agent_prompt,
            permission_mode='acceptEdits',
            allowed_tools=['Read', 'Grep', 'Write', 'Bash'],
            setting_sources=['project']
        )

    async def execute(self, source_dir: str, output_format: str):
        client = ClaudeSDKClient(self.options)

        try:
            await client.connect()

            # Initial analysis request
            await client.query(f'Analyze API in {source_dir}')
            analysis_result = await self._collect_messages(client)

            # Documentation generation with context
            await client.query(f'Generate {output_format} documentation')
            doc_result = await self._collect_messages(client)

            return doc_result

        finally:
            await client.disconnect()

    async def _collect_messages(self, client):
        results = []
        async for message in client.receive_messages():
            if message.type == 'assistant':
                results.append(message.content)
        return results

# Usage
async def run_skill(source_dir: str):
    skill = ApiDocumentationSkill()
    documentation = await skill.execute(source_dir, 'openapi')
    print(documentation)

asyncio.run(run_skill('/path/to/api'))
```

**Multi-Agent Skill with Progress Tracking**: Coordinate specialists with monitoring:

```python
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, AgentDefinition
import asyncio

class MultiAgentAnalysisSkill:
    def __init__(self):
        self.specialist_agents = [
            AgentDefinition(
                name='security-analyst',
                description='Security vulnerability analysis',
                system_prompt=security_analyst_prompt,
                allowed_tools=['Read', 'Grep', 'Bash'],
                permission_mode='default'
            ),
            AgentDefinition(
                name='performance-analyst',
                description='Performance bottleneck identification',
                system_prompt=performance_analyst_prompt,
                allowed_tools=['Read', 'Bash'],
                permission_mode='acceptEdits'
            ),
            AgentDefinition(
                name='quality-analyst',
                description='Code quality and maintainability analysis',
                system_prompt=quality_analyst_prompt,
                allowed_tools=['Read', 'Grep'],
                permission_mode='acceptEdits'
            )
        ]

        self.orchestrator_options = ClaudeAgentOptions(
            system_prompt=orchestrator_prompt,
            agents=self.specialist_agents,
            permission_mode='plan',
            model='claude-sonnet-4-5'
        )

    async def analyze_codebase(self, repo_path: str):
        client = ClaudeSDKClient(self.orchestrator_options)

        try:
            await client.connect()

            task = f"""Perform comprehensive codebase analysis on {repo_path}.

Coordinate specialist agents to:
1. Security analysis - identify vulnerabilities
2. Performance analysis - find bottlenecks
3. Quality analysis - assess maintainability

Aggregate results and provide unified report."""

            await client.query(task)

            report = {'security': [], 'performance': [], 'quality': []}

            async for message in client.receive_messages():
                if message.type == 'assistant':
                    # Process and categorize specialist results
                    report = self._parse_agent_results(message.content, report)

            return report

        finally:
            await client.disconnect()

    def _parse_agent_results(self, content: str, report: dict):
        # Parse and categorize specialist agent outputs
        # Implementation details
        return report

asyncio.run(MultiAgentAnalysisSkill().analyze_codebase('/workspace/app'))
```

**Skill Hooks for Lifecycle Management**: Monitor and control agent execution:

```python
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, Hook

async def pre_agent_spawn_hook(agent_name: str, context: dict):
    """Executed before specialist agent spawns."""
    print(f"Spawning specialist: {agent_name}")
    # Validate context, prepare resources
    return context

async def post_agent_completion_hook(agent_name: str, results: dict):
    """Executed after specialist completes."""
    print(f"Agent {agent_name} completed")
    # Validate results, update metrics
    return results

async def agent_error_hook(agent_name: str, error: Exception):
    """Handle agent failures gracefully."""
    print(f"Agent {agent_name} failed: {error}")
    # Implement fallback or escalation
    return {'status': 'failed', 'fallback': True}

skill_options = ClaudeAgentOptions(
    system_prompt=skill_agent_prompt,
    hooks=[
        Hook(event='PreAgentSpawn', handler=pre_agent_spawn_hook),
        Hook(event='PostAgentCompletion', handler=post_agent_completion_hook),
        Hook(event='AgentError', handler=agent_error_hook)
    ],
    permission_mode='plan'
)
```

### Best Practices for SDK-Powered Skills

**1. Agent Lifecycle Management**: Properly manage agent connections and cleanup:

```python
class SkillWithProperLifecycle:
    async def execute(self, task: str):
        client = ClaudeSDKClient(self.options)
        try:
            await client.connect()
            await client.query(task)
            return await self._process_results(client)
        except Exception as e:
            await self._handle_error(e)
        finally:
            await client.disconnect()  # Always cleanup
```

**2. Context Optimization**: Minimize token usage with focused context:

```typescript
// Prepare minimal context for agent
const skillContext = {
  task: userRequest,
  relevantFiles: await filterRelevantFiles(allFiles),
  constraints: { maxTokens: 4000, outputFormat: 'json' }
};

for await (const message of query(JSON.stringify(skillContext), {
  systemPrompt: efficientAgentPrompt,
  permissionMode: 'acceptEdits'
})) {
  // Process streamlined results
}
```

**3. Permission Isolation**: Apply principle of least privilege:

```typescript
const readOnlyAnalyst: AgentDefinition = {
  name: 'read-only-analyst',
  systemPrompt: analystPrompt,
  allowedTools: ['Read', 'Grep'],  // No write/execute
  permissionMode: 'default'  // Safest mode
};

const trustedImplementer: AgentDefinition = {
  name: 'implementer',
  systemPrompt: implementerPrompt,
  allowedTools: ['Read', 'Write', 'Edit'],
  permissionMode: 'plan'  // Show intent before action
};
```

**4. Error Recovery and Fallbacks**: Handle agent failures gracefully:

```python
async def execute_with_fallback(self, task: str):
    try:
        # Primary specialist agent
        return await self.execute_specialist_agent(task)
    except AgentFailureException as e:
        # Fallback to simpler agent
        print(f"Specialist failed: {e}, using fallback")
        return await self.execute_fallback_agent(task)
    except Exception as e:
        # Escalate to user
        return {'error': str(e), 'requires_intervention': True}
```

**5. Result Validation**: Verify agent outputs meet skill requirements:

```typescript
async function executeSkillWithValidation(task: string) {
  for await (const message of query(task, skillOptions)) {
    if (message.type === 'assistant') {
      const result = parseAgentResult(message.content);

      if (validateResult(result)) {
        return formatForUser(result);
      } else {
        throw new Error('Agent output validation failed');
      }
    }
  }
}
```

### Deploying Skills with SDK Agents

**Packaging**: Bundle skills with agent configurations:

```
skill-name/
├── SKILL.md                    # Skill documentation
├── index.ts                    # SDK implementation
├── agents/
│   ├── specialist.prompt       # Agent system prompts
│   └── orchestrator.prompt
├── tools/
│   └── custom-tools.ts         # Skill-specific tools
└── tests/
    └── integration.test.ts     # Skill + agent tests
```

**Installation**: Deploy with dependencies:

```bash
# Install skill globally
cp -r skill-name ~/.claude/skills/

# Install SDK dependencies
cd ~/.claude/skills/skill-name
npm install @anthropic-ai/claude-agent-sdk
```

**Configuration**: Set up environment and permissions:

```typescript
// Load from skill config
const skillConfig = loadSkillConfig('.skill-config.json');

const options: ClaudeAgentOptions = {
  systemPrompt: await loadPrompt('agents/specialist.prompt'),
  allowedTools: skillConfig.tools,
  permissionMode: skillConfig.permissionMode,
  mcpServers: skillConfig.mcpServers
};
```

## Working with Skill-Creator-Agent

To use this skill effectively, provide information about the skill you want to create including its intended purpose and triggering conditions, what tasks the specialist agent should handle, what domain expertise the agent needs, any specific requirements or constraints, whether you need SDK implementation (TypeScript/Python), and whether the skill will integrate with other skills in a larger workflow.

The skill-creator-agent will guide you through designing both the skill layer and the specialist agent using Claude Agent SDK patterns. It will help you establish the communication protocol, create necessary resources including SDK implementations, configure proper agent lifecycle management, implement custom tools if needed, and test the complete integration.

The result is a professional-grade skill that leverages specialist agent expertise through production-ready Claude Agent SDK infrastructure. Skills created this way provide measurably better results than traditional skills for complex domains while maintaining reliability, security, and maintainability.

