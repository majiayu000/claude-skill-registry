---
name: ai-agent-builder
description: "Build AI agents with tools, memory, and multi-step reasoning - ChatGPT, Claude, Gemini integration patterns"
version: "1.0.0"
author: claude-office-skills
license: MIT

category: ai
tags:
  - ai-agent
  - chatgpt
  - openai
  - langchain
  - automation
department: Engineering

models:
  recommended:
    - claude-opus-4
    - claude-sonnet-4

capabilities:
  - agent_design
  - tool_integration
  - memory_management
  - multi_step_reasoning
  - conversation_flow

languages:
  - en
  - zh

related_skills:
  - deep-research
  - n8n-workflow
  - slack-workflows
---

# AI Agent Builder

Design and build AI agents with tools, memory, and multi-step reasoning capabilities. Covers ChatGPT, Claude, Gemini integration patterns based on n8n's 5,000+ AI workflow templates.

## Overview

This skill covers:
- AI agent architecture design
- Tool/function calling patterns
- Memory and context management
- Multi-step reasoning workflows
- Platform integrations (Slack, Telegram, Web)

---

## AI Agent Architecture

### Core Components

```
┌─────────────────────────────────────────────────────────────────┐
│                      AI AGENT ARCHITECTURE                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐       │
│  │   Input     │────▶│   Agent     │────▶│   Output    │       │
│  │  (Query)    │     │   (LLM)     │     │  (Response) │       │
│  └─────────────┘     └──────┬──────┘     └─────────────┘       │
│                             │                                   │
│         ┌───────────────────┼───────────────────┐              │
│         │                   │                   │              │
│         ▼                   ▼                   ▼              │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐       │
│  │   Tools     │     │   Memory    │     │  Knowledge  │       │
│  │ (Functions) │     │  (Context)  │     │   (RAG)     │       │
│  └─────────────┘     └─────────────┘     └─────────────┘       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Agent Types

```yaml
agent_types:
  reactive_agent:
    description: "Single-turn response, no memory"
    use_case: simple_qa, classification
    complexity: low
    
  conversational_agent:
    description: "Multi-turn with conversation memory"
    use_case: chatbots, support
    complexity: medium
    
  tool_using_agent:
    description: "Can call external tools/APIs"
    use_case: data_lookup, actions
    complexity: medium
    
  reasoning_agent:
    description: "Multi-step planning and execution"
    use_case: complex_tasks, research
    complexity: high
    
  multi_agent:
    description: "Multiple specialized agents collaborating"
    use_case: complex_workflows
    complexity: very_high
```

---

## Tool Calling Pattern

### Tool Definition

```yaml
tool_definition:
  name: "get_weather"
  description: "Get current weather for a location"
  parameters:
    type: object
    properties:
      location:
        type: string
        description: "City name or coordinates"
      units:
        type: string
        enum: ["celsius", "fahrenheit"]
        default: "celsius"
    required: ["location"]
    
  implementation:
    type: api_call
    endpoint: "https://api.weather.com/v1/current"
    method: GET
    params:
      q: "{location}"
      units: "{units}"
```

### Common Tool Categories

```yaml
tool_categories:
  data_retrieval:
    - web_search: search the internet
    - database_query: query SQL/NoSQL
    - api_lookup: call external APIs
    - file_read: read documents
    
  actions:
    - send_email: send emails
    - create_calendar: schedule events
    - update_crm: modify CRM records
    - post_slack: send Slack messages
    
  computation:
    - calculator: math operations
    - code_interpreter: run Python
    - data_analysis: analyze datasets
    
  generation:
    - image_generation: create images
    - document_creation: generate docs
    - chart_creation: create visualizations
```

### n8n Tool Integration

```yaml
n8n_agent_workflow:
  nodes:
    - trigger:
        type: webhook
        path: "/ai-agent"
        
    - ai_agent:
        type: "@n8n/n8n-nodes-langchain.agent"
        model: openai_gpt4
        system_prompt: |
          You are a helpful assistant that can:
          1. Search the web for information
          2. Query our customer database
          3. Send emails on behalf of the user
          
        tools:
          - web_search
          - database_query
          - send_email
          
    - respond:
        type: respond_to_webhook
        data: "{{ $json.output }}"
```

---

## Memory Patterns

### Memory Types

```yaml
memory_types:
  buffer_memory:
    description: "Store last N messages"
    implementation: |
      messages = []
      def add_message(role, content):
          messages.append({"role": role, "content": content})
          if len(messages) > MAX_MESSAGES:
              messages.pop(0)
    use_case: simple_chatbots
    
  summary_memory:
    description: "Summarize conversation periodically"
    implementation: |
      When messages > threshold:
          summary = llm.summarize(messages[:-5])
          messages = [summary_message] + messages[-5:]
    use_case: long_conversations
    
  vector_memory:
    description: "Store in vector DB for semantic retrieval"
    implementation: |
      # Store
      embedding = embed(message)
      vector_db.insert(embedding, message)
      
      # Retrieve
      relevant = vector_db.search(query_embedding, k=5)
    use_case: knowledge_retrieval
    
  entity_memory:
    description: "Track entities mentioned in conversation"
    implementation: |
      entities = {}
      def update_entities(message):
          extracted = llm.extract_entities(message)
          entities.update(extracted)
    use_case: personalized_assistants
```

### Context Window Management

```yaml
context_management:
  strategies:
    sliding_window:
      keep: last_n_messages
      n: 10
      
    relevance_based:
      method: embed_and_rank
      keep: top_k_relevant
      k: 5
      
    hierarchical:
      levels:
        - immediate: last_3_messages
        - recent: summary_of_last_10
        - long_term: key_facts_from_all
        
  token_budget:
    total: 8000
    system_prompt: 1000
    tools: 1000
    memory: 4000
    current_query: 1000
    response: 1000
```

---

## Multi-Step Reasoning

### ReAct Pattern

```
Thought: I need to find information about X
Action: web_search("X")
Observation: [search results]
Thought: Based on the results, I should also check Y
Action: database_query("SELECT * FROM Y")
Observation: [database results]
Thought: Now I have enough information to answer
Action: respond("Final answer based on X and Y")
```

### Planning Agent

```yaml
planning_workflow:
  step_1_plan:
    prompt: |
      Task: {user_request}
      
      Create a step-by-step plan to complete this task.
      Each step should be specific and actionable.
      
    output: numbered_steps
    
  step_2_execute:
    for_each: step
    actions:
      - execute_step
      - validate_result
      - adjust_if_needed
      
  step_3_synthesize:
    prompt: |
      Steps completed: {executed_steps}
      Results: {results}
      
      Synthesize a final response for the user.
```

---

## Platform Integrations

### Slack Bot Agent

```yaml
slack_agent:
  trigger: slack_message
  
  workflow:
    1. receive_message:
        extract: [user, channel, text, thread_ts]
        
    2. get_context:
        if: thread_ts
        action: fetch_thread_history
        
    3. process_with_agent:
        model: gpt-4
        system: "You are a helpful Slack assistant"
        tools: [web_search, jira_lookup, calendar_check]
        
    4. respond:
        action: post_to_slack
        channel: "{channel}"
        thread_ts: "{thread_ts}"
        text: "{agent_response}"
```

### Telegram Bot Agent

```yaml
telegram_agent:
  trigger: telegram_message
  
  handlers:
    text_message:
      - extract_text
      - process_with_ai
      - send_response
      
    voice_message:
      - transcribe_with_whisper
      - process_with_ai
      - send_text_or_voice_response
      
    image:
      - analyze_with_vision
      - process_with_ai
      - send_response
      
    document:
      - extract_content
      - process_with_ai
      - send_response
```

### Web Chat Interface

```yaml
web_chat_agent:
  frontend:
    type: react_component
    features:
      - message_input
      - message_history
      - typing_indicator
      - file_upload
      
  backend:
    endpoint: "/api/chat"
    method: POST
    streaming: true
    
  session_management:
    method: jwt_token
    storage: redis
    ttl: 24_hours
```

---

## Agent Templates

### Customer Support Agent

```yaml
support_agent:
  name: "Customer Support AI"
  model: gpt-4
  
  system_prompt: |
    You are a customer support agent for {company}.
    
    Guidelines:
    - Be helpful, professional, and empathetic
    - Use the knowledge base to answer questions
    - Escalate to human if you cannot help
    - Never make up information
    
    Available actions:
    - Search knowledge base
    - Look up customer account
    - Create support ticket
    - Escalate to human agent
    
  tools:
    - knowledge_search:
        description: "Search help articles"
    - customer_lookup:
        description: "Get customer account info"
    - create_ticket:
        description: "Create support ticket"
    - escalate:
        description: "Transfer to human agent"
        
  escalation_triggers:
    - sentiment: very_negative
    - keywords: ["speak to human", "manager", "complaint"]
    - failed_resolution: after_3_attempts
```

### Research Agent

```yaml
research_agent:
  name: "Research Assistant"
  model: claude-opus
  
  system_prompt: |
    You are a research assistant that helps users find 
    and synthesize information on any topic.
    
    Process:
    1. Understand the research question
    2. Plan search strategy
    3. Execute searches across multiple sources
    4. Synthesize findings
    5. Present with citations
    
  tools:
    - web_search
    - academic_search
    - news_search
    - wikipedia_lookup
    
  output_format:
    - executive_summary
    - key_findings
    - detailed_analysis
    - sources_cited
```

---

## Output Example

**Request**: "Design an AI agent for appointment scheduling"

**Output**:

```markdown
# Appointment Scheduling Agent Design

## Architecture

```yaml
agent:
  name: "Scheduling Assistant"
  model: gpt-4
  
  capabilities:
    - Check calendar availability
    - Book appointments
    - Send confirmations
    - Handle rescheduling
    - Answer FAQs
```

## Tools Required

1. **calendar_check**
   - Input: date_range, duration
   - Output: available_slots[]

2. **book_appointment**
   - Input: datetime, customer_info, service_type
   - Output: confirmation_id

3. **send_notification**
   - Input: type, recipient, details
   - Output: success/failure

4. **customer_lookup**
   - Input: email or phone
   - Output: customer_record

## Conversation Flow

```
User: "I'd like to book an appointment"
Agent: [Thought: Need to know service type and preferred time]
Agent: "I'd be happy to help! What service are you looking for, 
        and do you have a preferred date/time?"

User: "Haircut, next Tuesday afternoon"
Agent: [Action: calendar_check(date="next Tuesday", time="afternoon")]
Agent: "I have availability at 2pm, 3pm, and 4:30pm next Tuesday. 
        Which works best for you?"

User: "3pm please"
Agent: [Action: book_appointment(datetime="Tuesday 3pm", service="haircut")]
Agent: [Action: send_notification(type="confirmation", ...)]
Agent: "You're all set for a haircut at 3pm next Tuesday. 
        I've sent a confirmation to your email. See you then!"
```

## n8n Implementation

```yaml
workflow:
  - webhook_trigger: /schedule-chat
  - ai_agent:
      tools: [calendar, booking, notification]
  - respond_to_user
```
```

---

*AI Agent Builder Skill - Part of Claude Office Skills*
