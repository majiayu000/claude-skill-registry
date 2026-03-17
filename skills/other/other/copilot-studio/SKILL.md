---
name: copilot-studio
description: Expert guidance for Microsoft Copilot Studio development including custom copilots, topic design, trigger phrases, actions, knowledge sources, generative AI answers, and channel publishing. Use when building conversational agents, designing topic flows, connecting knowledge bases, or publishing copilots to Teams and websites.
---

# Copilot Studio Development

Expert guidance for building custom copilots with Microsoft Copilot Studio, including topics, actions, knowledge sources, and channel publishing.

## Triggers

Use this skill when you see:
- copilot studio, custom copilot, power virtual agents
- topic design, trigger phrases, conversation flow
- knowledge source, generative answers, generative ai
- copilot actions, connector actions, ai builder
- copilot teams, copilot publish, direct line

## Instructions

### Copilot Architecture

```
┌─────────────────────────────────────────────────┐
│                 Custom Copilot                   │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐   │
│  │  Topics   │  │ Knowledge │  │  Actions   │   │
│  │ (Dialog   │  │ Sources   │  │ (Power     │   │
│  │  flows)   │  │ (Gen AI)  │  │  Automate) │   │
│  └───────────┘  └───────────┘  └───────────┘   │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐   │
│  │ Entities  │  │ Variables │  │  Channels  │   │
│  │ (Slot     │  │ (Global/  │  │ (Teams,    │   │
│  │  filling) │  │  Topic)   │  │  Web, etc.)│   │
│  └───────────┘  └───────────┘  └───────────┘   │
└─────────────────────────────────────────────────┘
```

### Topic Design

Topics are the building blocks of a copilot conversation. Each topic handles a specific user intent.

#### Topic Structure
- **Trigger phrases**: 5-10 example phrases that activate the topic
- **Question nodes**: Gather information from the user
- **Condition nodes**: Branch logic based on variable values
- **Message nodes**: Display responses to the user
- **Action nodes**: Call flows, connectors, or AI Builder prompts
- **Redirect nodes**: Transfer to another topic or escalate

#### Example Topic Flow: Order Status

```
Trigger Phrases:
- "Where is my order?"
- "Check order status"
- "Track my delivery"
- "Order tracking"
- "When will my order arrive?"

Flow:
1. Question: "What is your order number?" -> Save to Topic.OrderNumber
   - Entity: Custom regex pattern [A-Z]{2}\d{6}
   - Reprompt: "Please enter a valid order number (e.g., AB123456)"

2. Action: Call Power Automate flow "Get Order Status"
   - Input: Topic.OrderNumber
   - Output: Topic.OrderStatus, Topic.EstimatedDelivery

3. Condition: Topic.OrderStatus
   - "Shipped" ->
     Message: "Your order {Topic.OrderNumber} has shipped!
               Estimated delivery: {Topic.EstimatedDelivery}"
   - "Processing" ->
     Message: "Your order {Topic.OrderNumber} is being processed.
               You'll receive a tracking number once it ships."
   - "Delivered" ->
     Message: "Your order {Topic.OrderNumber} was delivered on {Topic.EstimatedDelivery}."
   - Else ->
     Message: "I couldn't find order {Topic.OrderNumber}. Let me connect you with support."
     Redirect: Escalate topic
```

### Knowledge Sources

Knowledge sources enable generative AI answers from your organizational content.

#### Supported Sources
- **SharePoint sites**: Point to site URLs; copilot indexes pages and documents
- **Public websites**: Crawl up to 4 levels deep from a URL
- **Uploaded files**: PDF, Word, Excel, PowerPoint, text files
- **Dataverse**: Tables configured as knowledge sources

#### Configuration

```
Knowledge Source Setup:
1. Navigate to copilot > Knowledge
2. Add source type (SharePoint, Website, Files)
3. Configure:
   - SharePoint: Enter site URL(s), select libraries
   - Website: Enter root URL, set crawl depth (1-4)
   - Files: Upload documents (max 3MB each, 100MB total)
4. Set description for AI to understand when to use this source
5. Test with sample questions in Test Copilot pane
```

#### Generative Answers Configuration
- **Content moderation**: Set strictness level (Low/Medium/High)
- **Citation style**: Inline or footnote citations
- **No-answer behavior**: Fallback to topic or escalate
- **Data sources**: Select which knowledge sources to query

### Actions

Actions extend copilot capabilities by connecting to external systems.

#### Power Automate Flow Actions

```
Action Setup:
1. Create a Power Automate cloud flow
2. Trigger: "When Power Virtual Agents calls a flow" (now "Run a flow from Copilot")
3. Define input parameters (from copilot variables)
4. Add flow logic (Dataverse, HTTP, connectors)
5. Return output parameters (back to copilot variables)
6. In Copilot Studio: Add Action node > select the flow
```

#### Connector Actions

```
1. In topic, add Action node > "Call a connector action"
2. Select connector (e.g., Outlook, SharePoint, Dataverse)
3. Map input parameters from topic variables
4. Map output to topic variables for use in messages
```

#### AI Builder Prompt Actions

```
1. Create an AI Builder custom prompt
2. Define prompt template with placeholders
3. In Copilot Studio: Add Action node > "AI Builder prompt"
4. Map topic variables to prompt placeholders
5. Use prompt output in subsequent message nodes
```

### ALM for Copilots

Copilots are Dataverse solution components and follow standard Power Platform ALM.

```bash
# Copilots live inside Dataverse solutions
pac solution export --name CopilotSolution --path ./copilot-solution.zip --managed false

# Unpack for source control
pac solution unpack --zipfile ./copilot-solution.zip --folder ./src/CopilotSolution

# Solution includes:
# - Chatbot component (copilot definition)
# - Chatbot subcomponents (topics, entities, variables)
# - Related Power Automate flows
# - Knowledge source configurations
```

### Channel Publishing

#### Microsoft Teams

```
1. Go to copilot > Channels > Microsoft Teams
2. Click "Turn on Teams"
3. Options:
   - Share link directly with users
   - Submit to Teams admin for org-wide deployment
   - Add to Teams app catalog
4. Users find copilot in Teams chat or app bar
```

#### Power Apps Embedding

```
1. Go to copilot > Channels > Custom website
2. Copy the embed snippet (iframe or webchat script)
3. Add to canvas app HTML text control or custom page
```

#### Website (Direct Line)

```html
<!-- Embed via Direct Line -->
<script src="https://cdn.botframework.com/botframework-webchat/latest/webchat.js"></script>
<script>
  window.WebChat.renderWebChat({
    directLine: window.WebChat.createDirectLine({
      token: 'YOUR_DIRECT_LINE_TOKEN'
    }),
    userID: 'user123'
  }, document.getElementById('webchat'));
</script>
<div id="webchat" role="main" style="height: 600px; width: 400px;"></div>
```

## Best Practices

| Practice | Description |
|----------|-------------|
| **Trigger phrases** | Use 5-10 diverse phrases per topic; avoid overlapping triggers |
| **Fallback topic** | Customize the fallback to gracefully handle unrecognized input |
| **Entity validation** | Use entity types and reprompt messages for data quality |
| **Knowledge scope** | Add descriptions to knowledge sources so AI picks the right one |
| **Testing** | Test every conversation path in the Test pane before publishing |
| **Topic naming** | Use descriptive names: "Order Status Lookup" not "Topic 1" |
| **Variables** | Prefer topic-scoped variables; use global only for cross-topic state |
| **Escalation** | Always provide a path to a human agent for complex issues |

## Common Workflows

### Build a New Copilot
1. Create copilot in Copilot Studio with description
2. Add knowledge sources (SharePoint, websites, files)
3. Create custom topics for specific intents
4. Connect Power Automate flows for data operations
5. Test in the Test Copilot pane
6. Publish to channels (Teams, website)

### Topic Design Process
1. Identify user intent and expected outcomes
2. Write 5-10 trigger phrases with natural variation
3. Design question flow with entity validation
4. Add conditions for branching logic
5. Connect actions for external data
6. Add message responses with variable interpolation
7. Test edge cases and fallback paths

### Copilot Deployment
1. Develop and test in Dev environment
2. Add copilot to Dataverse solution
3. Export solution (managed) for deployment
4. Import to Test environment, validate conversation flows
5. Import to Prod, publish to channels
6. Monitor analytics in Copilot Studio dashboard
