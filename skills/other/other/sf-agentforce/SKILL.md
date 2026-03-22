---
name: sf-agentforce
description: |
  Build, configure, and test Agentforce agents on Salesforce. Covers agent setup,
  topics, actions (Flow, Apex, PromptTemplate, External Service), Agent Scripts
  for deterministic FSM-based agents, PromptTemplate authoring, GenAI Models API,
  metadata structure, and agent testing via the Testing Center and CLI.
  Activate on Agentforce agents, .agent files, .agent-meta.xml, .agentTopic-meta.xml,
  .agentAction-meta.xml, GenAiFunction, GenAiPlugin, PromptTemplate, Agent Script,
  or agent testing workflows.
license: Apache-2.0
compatibility: Requires Salesforce CLI (sf) v2+, API v66.0+ for Agentforce features, Agentforce license.
metadata:
  author: clientell
  version: "1.0.0"
  tags: salesforce, agentforce, agents, topics, actions, prompt-template, agent-script, testing
# Claude Code specific
allowed-tools: Read,Write,Edit,Bash(sf *),Glob,Grep
context: fork
---

# Agentforce Development Guide

You are a Salesforce Agentforce specialist. Build production-ready autonomous and deterministic agents following Salesforce best practices. API version 66.0 for all Agentforce features.

## Agent Setup

### Creating an Agent

Agents are created in **Setup > Agentforce > Agents** or via metadata deployment.

Two agent types:

| Agent Type | API Name | Use Case |
|---|---|---|
| Service Agent | `AgentforceServiceAgent` | Customer-facing, runs as Agent User, deployed to channels |
| Employee Agent | `AgentforceEmployeeAgent` | Internal-facing, runs as logged-in user, embedded in apps |

### Agent User Configuration (Service Agents Only)

Service Agents require a dedicated **Einstein Agent User**:
1. Create a user with the `Salesforce Integration` license
2. Assign the `AgentforceServiceAgent` permission set
3. Grant object/field permissions the agent needs via permission sets
4. Set as `default_agent_user` in agent configuration

Employee Agents run as the logged-in user and do not need a dedicated agent user.

### Channel Configuration

Agents can be deployed to:
- **Messaging channels** (web chat, SMS, WhatsApp)
- **Embedded Service deployments** (Lightning Web Runtime)
- **Slack** (Employee Agent)
- **API** (Agent Runtime API for programmatic access)

Configure channels in **Setup > Messaging Settings** or **Embedded Service Deployments**.

---

## Topics

Topics define the scope of what an agent can handle. Each topic is a logical domain with its own instructions, actions, and scope boundaries.

### Topic Design Principles

- **Specific scope**: Each topic should have a clear, non-overlapping domain
- **Natural language description**: The description is the routing signal — the planner uses it to match user utterances
- **Focused instructions**: Tell the agent how to behave within this topic
- **Bounded actions**: Only attach actions relevant to the topic

### Topic Structure

A topic consists of:
- **Label and API Name**: Human-readable name and developer reference
- **Description**: Natural language explanation of what this topic covers (this drives routing)
- **Scope**: Define what is in-scope and out-of-scope explicitly
- **Instructions**: Step-by-step guidance for agent behavior within this topic
- **Actions**: The tools available to the agent when this topic is active

### Topic Routing

The planner matches user utterances to topics based on:
1. Topic description similarity to the utterance
2. Scope definitions (in-scope vs out-of-scope)
3. Instruction context

**Avoid scope overlap** between sibling topics. If two topics could match the same utterance, the planner may misroute. Use explicit scope boundaries:

```text
In scope: Order status inquiries, order tracking, delivery estimates
Out of scope: Order creation, order cancellation (handled by Order Management topic)
```

---

## Agent Actions

Actions are the tools an agent can invoke. Each action wraps a target implementation.

### Action Types

| Action Type | Target | Best For | Registered Via |
|---|---|---|---|
| Flow Action | Screen Flow or Autolaunched Flow | Declarative logic, guided interactions, multi-step processes | `GenAiFunction` |
| Apex Action | `@InvocableMethod` class | Complex business logic, callouts, calculations | `GenAiFunction` |
| PromptTemplate Action | PromptTemplate metadata | Generated text, summaries, recommendations, drafts | `GenAiFunction` |
| External Service Action | External Service registration | Third-party API calls via OpenAPI spec | `GenAiFunction` |

### When to Use Each

- **Flow**: Default choice. Safest, most maintainable, supports guided user interaction
- **Apex**: When you need complex logic, external callouts, or custom data processing
- **PromptTemplate**: When the output is generated text (summaries, emails, recommendations)
- **External Service**: When calling external APIs registered via External Services

### Action Configuration

Every action requires:
- **Capability description**: Natural language explaining when the agent should invoke this action
- **Input parameters**: Mapped from conversation context or user input
- **Output parameters**: Returned to the agent for response generation

Input/output parameter names must match the target contract exactly:
- For Flows: match Flow input/output variable API names
- For Apex: match `@InvocableVariable` field names
- For PromptTemplates: match template input/output variable names

### Action Grouping with GenAiPlugin

Group related `GenAiFunction` entries into a `GenAiPlugin` for logical organization. A plugin represents a capability domain (e.g., "Order Management" containing lookup, status, and cancel actions).

---

## PromptTemplate

PromptTemplate metadata defines reusable prompt configurations for agent grounding, text generation, and structured responses.

### Template Types

| Type | Use Case |
|---|---|
| `einstein_gpt__fieldCompletion` | Single-field generation |
| `einstein_gpt__salesEmail` | Email drafting |
| `einstein_gpt__flex` | General-purpose flex templates |
| `einstein_gpt__chat` | Conversational agent grounding |

### Template Components

- **Input variables**: Data passed into the template (record fields, user input, context)
- **Output variable**: The generated result
- **Resolution steps**: Ordered prompt fragments, grounding data, and instructions
- **Model configuration**: Which model to use and parameters

### PromptTemplate as Agent Action

When used as an agent action:
1. Create the PromptTemplate metadata
2. **Activate the template** (Draft templates cause publish errors)
3. Register it as a `GenAiFunction`
4. Attach to a topic
5. Map inputs from conversation context

### Models API Integration

Use the Models API from Apex for custom model routing beyond PromptTemplates:

```apex
public with sharing class ModelService {
    @InvocableMethod(label='Generate Summary')
    public static List<String> generateSummary(List<String> inputs) {
        ConnectApi.EinsteinLlmGenerateParams params =
            new ConnectApi.EinsteinLlmGenerateParams();
        params.promptTextorId = 'Summarize: ' + inputs[0];
        ConnectApi.EinsteinLlmGenerationOutput output =
            ConnectApi.EinsteinAI.generateMessages(params);
        return new List<String>{ output.generatedMessages[0].text };
    }
}
```

---

## Agent Scripts (Deterministic Agents)

Agent Scripts provide a **code-first, FSM-based** approach for building deterministic agents. Use `.agent` files with a declarative DSL.

### When to Use Agent Scripts vs Setup UI

| Criteria | Agent Script | Setup UI / Agent Builder |
|---|---|---|
| Routing control | Deterministic (state machine) | LLM-directed (planner) |
| Version control | `.agent` files in source | Metadata XML retrieved from org |
| Repeatability | Identical behavior every time | May vary with planner interpretation |
| Complexity ceiling | High (FSM + guards + transitions) | Moderate (topic + actions) |
| Best for | Strict compliance flows, regulated processes | General customer service, flexible Q&A |

### Agent Script DSL Structure

```yaml
config:
  developer_name: MyServiceAgent
  master_label: My Service Agent
  agent_description: Handles customer service inquiries
  agent_type: AgentforceServiceAgent
  default_agent_user: einstein_agent_user@company.com

variables:
  caseNumber:
    type: string
    description: The case number provided by the customer
  customerVerified:
    type: boolean
    description: Whether the customer has been verified
    default: False

system:
  greeting: Hello! I am your service agent. How can I help you today?

start_agent:
  topic: Greeting

topic: Greeting
  description: Initial greeting and intent identification
  instructions: ->
    Greet the customer and ask how you can help.
    Identify their intent and route to the appropriate topic.
  actions:
    identifyIntent:
      target: flow://Identify_Customer_Intent
      inputs:
        utterance: $input
      outputs:
        detectedIntent: intent
  transitions:
    - when: detectedIntent == "case_status"
      go_to: CaseStatus
    - when: detectedIntent == "new_case"
      go_to: NewCase
```

### Key DSL Rules

1. **Exactly one `start_agent` block** per file
2. **No mixed tabs and spaces** — pick one and be consistent
3. **Booleans**: `True` / `False` (capitalized)
4. **No `else if`** — use separate conditions or transitions
5. **No nested `if` blocks**
6. **`linked` variables** cannot have defaults and cannot use `object`/`list` types
7. **Actions use `@actions.` prefix** when referenced in instructions
8. **`run @actions.X`** only for topic-level actions with a `target:` definition

### Agent Script CLI

```bash
# Validate an agent script
sf agent validate authoring-bundle --api-name MyAgent -o TARGET_ORG --json

# Publish an agent script
sf agent publish authoring-bundle --api-name MyAgent -o TARGET_ORG --json

# Activate the agent
sf agent activate --api-name MyAgent -o TARGET_ORG
```

Publishing does **not** activate — always run `sf agent activate` separately.

---

## Metadata Structure

Key metadata types for Agentforce:

| Metadata Type | File Suffix | Purpose |
|---|---|---|
| Bot | `.agent-meta.xml` | Agent definition, versions, context variables |
| GenAiTopic | `.agentTopic-meta.xml` | Topic with description, scope, instructions, actions |
| GenAiFunction | `.genAiFunction-meta.xml` | Single action wrapping a Flow, Apex, or PromptTemplate target |
| GenAiPlugin | `.genAiPlugin-meta.xml` | Logical grouping of related GenAiFunctions |
| PromptTemplate | `.promptTemplate-meta.xml` | Prompt configuration with inputs, outputs, and model settings |

Each GenAiFunction must specify:
- `targetType` (Flow, Apex, PromptTemplate, ExternalService)
- `targetName` (API name of the target)
- `capabilityDescription` (when the agent should use this action)
- `inputs` and `outputs` with names matching the target contract exactly

Full XML templates for all metadata types: [references/agentforce-reference.md](references/agentforce-reference.md)

---

## Testing Agents

### Agentforce Testing Center

The Testing Center (Setup > Agentforce > Testing Center) provides UI-based testing with multi-turn conversation validation.

### CLI Testing Commands

```bash
sf agent test run --api-name MyAgent -o TARGET_ORG --json
sf agent test run --spec-file tests/order-status.yaml -o TARGET_ORG --json
sf agent test results --test-run-id 0Atxx0000000001 -o TARGET_ORG --json
```

Test spec YAML format and multi-turn examples: [references/agentforce-reference.md](references/agentforce-reference.md)

### Test Coverage Categories

Ensure tests cover:
1. **Topic routing**: Correct topic matched for each utterance
2. **Action invocation**: Expected actions called with correct parameters
3. **Context preservation**: Multi-turn conversations maintain state
4. **Guardrails**: Off-topic, harmful, or out-of-scope inputs handled
5. **Escalation**: Agent escalates to human when appropriate
6. **Phrasing variation**: Multiple ways of asking the same question

### Test-Fix Loop

1. Run tests and capture failures
2. Classify failures (topic mismatch, action failure, context loss, guardrail failure)
3. Fix the agent (topic descriptions, action configs, instructions)
4. Re-publish and re-activate
5. Re-run focused tests before full regression

---

## Agent Observability

Monitor agent behavior in production using the Session Tracing Data Model (STDM) and EventLogFile.

### Session Tracing Data Model (STDM)

STDM captures structured telemetry for every agent session: sessions, interactions (turns), interaction steps, moments, and messages. Enable tracing in **Setup > Einstein AI > Session Tracing**. Data flows into Data Cloud for analysis.

Key STDM entities: `Session`, `Interaction`, `InteractionStep`, `Moment`, `Message`. Each interaction maps to a single user turn and the agent's response chain (topic match, action invocations, LLM calls).

### Session Transcripts

Query session transcripts via the Agent Runtime API or Data Cloud. Use transcripts to debug topic routing failures, inspect action parameters, and verify context preservation across turns.

### EventLogFile for Agent Events

`EventLogFile` captures agent-related platform events. Query with:
```soql
SELECT Id, EventType, LogDate, LogFileLength
FROM EventLogFile
WHERE EventType IN ('AIInteraction', 'AIInsightAction')
ORDER BY LogDate DESC
```

Use EventLogFile data for aggregate monitoring: invocation counts, error rates, and latency trends.

---

## Agent Persona Design

Design a consistent agent personality by defining voice attributes and encoding them into agent configuration.

### Voice Attributes

Define: **register** (formal to casual), **warmth** (neutral to empathetic), **brevity** (concise to detailed), **humor** (none to light). Align these with brand guidelines and audience expectations.

### System Instructions for Persona

Encode persona in the agent's system instructions or topic-level instructions. Include: identity statement, tone directives, a phrase book (preferred phrases), and a never-say list (banned phrases or topics). Keep instructions specific and testable.

### Guardrails for Persona

Define tone boundaries: how the agent adjusts tone for frustrated users vs happy-path conversations. Set hard limits (never use slang, never promise timelines) and soft guidelines (prefer active voice, use customer's name).

---

## GenAI Models API

The Models API provides programmatic access to LLMs through Apex via `ConnectApi.EinsteinAI.generateMessages()`. All calls are automatically protected by the Einstein Trust Layer (prompt defense, toxicity detection, PII masking, audit trail, data grounding, zero data retention).

Configure model routing in **Setup > Einstein AI > Model Management**. Override at the PromptTemplate level for per-template model selection.

See [references/agentforce-reference.md](references/agentforce-reference.md) for Apex usage examples and Trust Layer details.

---

## Gotchas

### Agent User License
Service Agents require an Einstein Agent User license. Without it, publish succeeds but the agent cannot execute actions at runtime. Verify the user has `AgentforceServiceAgent` permission set.

### Topic Scope Overlap
Overlapping topic descriptions cause routing ambiguity. The planner may match the wrong topic or oscillate between topics. Fix by making scope boundaries explicit and non-overlapping.

### Action Parameter Mapping
Input/output parameter names in `GenAiFunction` must exactly match the target contract. Mismatched names cause silent failures where the action is invoked but receives null inputs.

### PromptTemplate Draft Status
A PromptTemplate in Draft status causes `invalid input/output parameters` errors during agent publish. Always activate templates before publishing the agent.

### API Version Requirement
Agentforce features require API version **66.0 or higher**. Metadata deployed at lower API versions will be rejected or ignored.

### Publish vs Activate
Publishing an agent does not activate it. After `sf agent publish`, you must separately run `sf agent activate`. Forgetting this step means the agent is deployed but unreachable.

### Agent Script Syntax Pitfalls
- `else if` is not supported — use separate conditions
- Nested `if` blocks are not allowed
- `linked` variables cannot have default values
- Booleans must be `True`/`False` (case-sensitive)
- Top-level `actions:` block is invalid — actions belong inside topics

### Deploy Order Matters
Supporting metadata must be deployed before the agent:
1. Custom objects/fields
2. Apex classes (InvocableMethod)
3. Flows
4. PromptTemplates (and activate them)
5. GenAiFunction / GenAiPlugin
6. Agent metadata
7. Publish, then activate

### Test Coverage
While there is no enforced minimum test percentage for agents (unlike Apex), untested agents are risky. Cover at minimum: each topic, each action, off-topic handling, and escalation paths.

---

## Workflow

### Step-by-Step Agent Development

1. **Define the agent purpose**: Identify whether this is a Service Agent or Employee Agent. Determine the channels and use cases.

2. **Design topics**: Map out the conversation domains. Each topic should be distinct with clear scope boundaries.

3. **Choose the authoring path**:
   - **Setup UI / Agent Builder**: For declarative, LLM-directed agents
   - **Agent Script DSL**: For deterministic, state-machine-driven agents

4. **Build supporting components**:
   - Create Flows for declarative actions
   - Create Apex `@InvocableMethod` classes for complex logic
   - Create PromptTemplates for generated content
   - Register External Services for third-party APIs

5. **Configure actions**: Create `GenAiFunction` metadata for each action. Ensure input/output mappings match targets exactly.

6. **Wire topics to actions**: Attach actions to topics. Write clear capability descriptions so the planner knows when to invoke each action.

7. **Deploy metadata**: Deploy in dependency order (objects, Apex, Flows, templates, functions, agent).

8. **Publish and activate**:
   ```bash
   sf agent publish authoring-bundle --api-name MyAgent -o TARGET_ORG --json
   sf agent activate --api-name MyAgent -o TARGET_ORG
   ```

9. **Test**: Run test specs covering topic routing, action invocation, guardrails, and multi-turn context.

10. **Iterate**: Fix failures, re-publish, re-activate, re-test.

---

## Review Checklist

When reviewing an Agentforce agent, verify:
1. Agent type matches use case (Service vs Employee)
2. Service Agent has a valid Einstein Agent User configured
3. Topic descriptions are specific and non-overlapping
4. Scope boundaries are explicitly defined for each topic
5. Action capability descriptions clearly state invocation criteria
6. Input/output parameter names match target contracts
7. PromptTemplates are in Active status
8. Deploy order is correct (dependencies before agent)
9. Agent is both published and activated
10. Tests cover all topics, actions, guardrails, and escalation paths

---

## References
- [Agentforce Reference](references/agentforce-reference.md) — metadata templates, Agent Script DSL, testing specs, patterns, Trust Layer, debugging
