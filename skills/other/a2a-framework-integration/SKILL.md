---
name: a2a-framework-integration
description: Integrate A2A with agent frameworks — Google ADK, LangGraph, CrewAI, AutoGen, and AWS Bedrock AgentCore. Use when connecting framework-built agents to the A2A protocol for inter-agent communication.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# A2A Framework Integration

## Before writing code

**Fetch live docs**:
1. Fetch `https://a2a-protocol.org/latest/specification/` for the protocol spec
2. Web-search `site:github.com a2aproject a2a-samples` for framework integration examples
3. Web-search the specific framework's docs for A2A support:
   - `site:google.github.io adk a2a agent-to-agent` for Google ADK
   - `site:langchain-ai.github.io langgraph a2a` for LangGraph
   - `site:docs.crewai.com a2a` for CrewAI
   - `site:docs.aws.amazon.com bedrock agentcore a2a` for AWS Bedrock
4. Fetch SDK docs for framework adapter classes

## Conceptual Architecture

### Why Framework Integration

Most production agents are built using frameworks (LangGraph, CrewAI, ADK, etc.). A2A framework integration allows these agents to:
- **Expose themselves** as A2A servers (other agents can discover and call them)
- **Call other agents** as A2A clients (delegate work to specialist agents)
- **Participate in multi-agent systems** without rewriting framework-specific code

### Google ADK (Agent Development Kit)

Google ADK has **native A2A support** since it was co-developed alongside A2A:
- ADK agents can be directly exposed as A2A servers
- ADK provides A2A client utilities for calling other agents
- Agent Cards are generated from ADK agent configuration
- Supports streaming, multi-turn, and push notifications

**Integration approach**: Use ADK's built-in A2A server/client utilities.

### LangGraph / LangChain

LangGraph agents can be wrapped as A2A servers:
- The graph's invoke/stream methods map to `message/send` and `message/stream`
- Graph state maps to A2A task state
- Interrupts in LangGraph map to `input-required` in A2A

**Integration approach**: Use A2A SDK adapters or build a thin wrapper that translates between LangGraph's interface and A2A's JSON-RPC protocol.

### CrewAI

CrewAI's crew-based multi-agent model can integrate with A2A:
- Individual crew members can be exposed as A2A agents
- Entire crews can be wrapped as a single A2A agent
- A2A enables cross-crew communication

**Integration approach**: Wrap CrewAI agents/crews with an A2A server that translates tasks to crew kickoffs.

### AutoGen

Microsoft's AutoGen multi-agent framework:
- AutoGen agents can be wrapped as A2A servers
- AutoGen's conversation patterns map to A2A multi-turn
- Group chat can be exposed as a single A2A agent

**Integration approach**: Build adapters between AutoGen's message protocol and A2A.

### AWS Bedrock AgentCore

AWS Bedrock has added A2A support:
- Bedrock agents can communicate via A2A
- AgentCore provides infrastructure for hosting A2A-compatible agents
- Integration with AWS IAM for authentication

**Integration approach**: Use Bedrock's A2A-compatible agent hosting and client utilities.

### General Integration Pattern

Regardless of framework, the pattern is:

**Exposing a framework agent as A2A server:**
1. Create an Agent Card describing the framework agent's capabilities
2. Implement a thin A2A server that wraps the framework agent
3. Map incoming A2A messages to framework input format
4. Map framework output to A2A task results/artifacts
5. Handle state mapping (framework states → A2A task states)

**Using A2A agents from a framework:**
1. Fetch the target agent's Agent Card
2. Create an A2A client in the framework's tool/action layer
3. Map the framework's delegation pattern to A2A `message/send` or `message/stream`
4. Handle A2A responses within the framework's processing flow

### State Mapping Challenges

Different frameworks manage state differently:
- **LangGraph**: Graph state with checkpoints → A2A task state
- **CrewAI**: Crew execution state → A2A task state
- **AutoGen**: Conversation history → A2A message history
- **ADK**: Native A2A alignment (minimal mapping needed)

### Best Practices

- Use the simplest integration pattern that works — don't over-abstract
- Test framework-specific edge cases (timeouts, retries, error handling)
- Document the state mapping between the framework and A2A
- Keep the adapter layer as thin as possible
- Check for official A2A adapters before building custom ones
- Handle framework-specific features that don't map cleanly to A2A (e.g., LangGraph branching)
- Version your adapters alongside framework version upgrades

Fetch the latest framework documentation and A2A SDK adapters before implementing integrations.
