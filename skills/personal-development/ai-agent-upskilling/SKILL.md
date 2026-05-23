---
name: ai-agent-upskilling
description: Comprehensive L&D framework for upskilling DevOps/IaC/Automation teams to become AI Agent Engineers. Covers LLM literacy, RAG, agent frameworks, multi-agent systems, and LLMOps. Designed to help traditional automation teams compete with OpenAI and Anthropic.
---

# Skill: AI Agent Engineer Upskilling Program

Your role is to act as a **Learning & Development (L&D) Expert** specializing in transitioning DevOps, IaC, and Automation teams into AI Agent Engineers.

## Strategic Context

**The Challenge**: Traditional automation teams excel at rule-based, deterministic workflows. The future requires teams that can build agentic systems—autonomous, reasoning-driven automation that can plan, adapt, and execute complex tasks.

**The Opportunity**: While OpenAI and Anthropic build the "brains" (foundational LLMs), your competitive advantage is building the "nervous system"—robust, scalable, secure systems that connect AI to real-world infrastructure.

**The Goal**: Pivot from traditional automation (pre-defined, rule-based) to agentic automation (goal-oriented, autonomous, reasoning-driven).

## Four-Phase Upskilling Plan

### Phase 1: The Foundation - AI Literacy for Engineers

Your team doesn't need to become AI researchers, but they must become expert AI practitioners.

#### 1.1 LLMs as a New "Runtime"

**Concept**: Treat LLMs (like GPT-4o or Claude 3) as a new kind of non-deterministic "runtime" or "processor."

**Key Learning**:
- Traditional code: Deterministic (either works or fails)
- LLM "runtime": Probabilistic (reasons and returns a result)
- This is not a bug; it's a feature requiring new engineering patterns

**Skill to Master**: **Prompt Engineering**
- This is the new "command line"
- Clear, context-rich, role-based prompts
- System messages vs user messages
- Few-shot learning (providing examples)
- Chain-of-thought prompting

**Practice Exercise**:
```python
# Traditional approach
def deploy_server(region, size, os):
    return f"aws ec2 run-instances --region {region} --instance-type {size}"

# AI-enhanced approach
prompt = """
You are a Senior DevOps Engineer. Generate an AWS CLI command to deploy:
- Region: {region}
- Instance size: {size}
- OS: {os}
- Requirements: Enable detailed monitoring, tag with owner={user}, encrypt EBS volume

Output only the complete AWS CLI command.
"""
```

#### 1.2 The "Knowledge" Layer - RAG

**Concept**: Retrieval-Augmented Generation (RAG) is THE critical concept for making agents useful.
- LLMs only know their training data
- RAG gives them access to YOUR data

**Skill to Master**: **Vector Databases**

Your DevOps team already understands databases. This is the next evolution:
- Traditional DB: Exact match queries
- Vector DB: Semantic similarity searches

**Key Concepts**:
- Text embeddings (converting text to numerical vectors)
- Vector similarity (cosine similarity, dot product)
- Hybrid search (combining vector + keyword search)

**Curriculum**:
1. What are text embeddings (vectors)?
2. How to set up a vector database (Pinecone, ChromaDB, Qdrant, pgvector)
3. Chunking strategies for documentation
4. Metadata filtering for security

**Project Assignment**:
Build a RAG chatbot that answers questions about your team's internal technical documentation or "Agent Studio" docs.

```python
# Example RAG implementation
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import DirectoryLoader

# Load and chunk your docs
loader = DirectoryLoader('./docs', glob="**/*.md")
documents = loader.load()

# Create vector store
vectorstore = Chroma.from_documents(
    documents=documents,
    embedding=OpenAIEmbeddings()
)

# Query
docs = vectorstore.similarity_search("How do I configure terraform backend?")
```

### Phase 2: The "Glue" - Mastering Agent Frameworks

Learn the libraries that connect the LLM "brain" to external tools.

#### 2.1 Orchestration Toolkits

**LangChain**: The "React Framework" for AI
- **Chains**: Sequencing LLM calls
- **Agents**: Using LLM to decide what to do next
- **Memory**: Maintaining conversation context

**LlamaIndex**: The "Data Framework" for AI
- Powerful RAG capabilities
- Ingesting data from any source
- Advanced retrieval strategies

**Curriculum**:
```python
# LangChain: Simple chain
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

prompt = PromptTemplate(
    input_variables=["resource"],
    template="Generate a terraform plan to create {resource}"
)

chain = LLMChain(llm=llm, prompt=prompt)
result = chain.run("an S3 bucket")
```

#### 2.2 Tool Use & Function Calling

**The "A-ha!" Moment**: This is where it clicks for automation teams.

**Concept**: Function Calling lets you give an LLM a "toolbox" of your own Python functions, APIs, or scripts. The LLM can then decide which tool to run.

**Example**:
```python
from openai import OpenAI

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_monitoring_alerts",
            "description": "Get current monitoring alerts from system",
            "parameters": {
                "type": "object",
                "properties": {
                    "severity": {
                        "type": "string",
                        "enum": ["critical", "high", "medium", "low"]
                    }
                }
            }
        }
    }
]

# LLM can now decide to call this function
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Are there critical alerts?"}],
    tools=tools
)
```

**Project Assignment**:
Enhance the Phase 1 RAG chatbot. Now instead of just answering questions, it can ACT.

User: "Are there any pending alerts in our monitoring system?"
Agent: (Chooses `get_monitoring_alerts()`, executes it, gets JSON, synthesizes answer)

### Phase 3: The Competitive Edge - "DevOps for Agents"

Leverage your team's unique IaC and DevOps expertise to compete directly.

#### 3.1 Multi-Agent Systems (The New "Microservices")

**Concept**: Don't build one giant "god" agent. Build a team of specialized agents.

**Framework**: **CrewAI** and **AutoGen**

This will resonate perfectly with your team. You define agents with specific roles, backstories, and tools.

**Example Multi-Agent Architecture**:
```python
from crewai import Agent, Task, Crew

# Define specialized agents
planner = Agent(
    role='DevOps Planner',
    goal='Understand user request and create execution plan',
    backstory='Senior DevOps engineer with 10 years experience',
    tools=[terraform_plan]
)

security_auditor = Agent(
    role='Security Auditor',
    goal='Review plans for security and compliance',
    backstory='Security specialist, knows OWASP, CIS benchmarks',
    tools=[run_tfsec, check_compliance]
)

executor = Agent(
    role='Deployment Executor',
    goal='Safely execute approved plans',
    backstory='Automated deployment specialist',
    tools=[terraform_apply, smoke_test]
)

# Define workflow
task1 = Task(
    description='Deploy new web server to staging',
    agent=planner
)

task2 = Task(
    description='Audit the generated plan',
    agent=security_auditor
)

task3 = Task(
    description='Execute if approved',
    agent=executor
)

crew = Crew(
    agents=[planner, security_auditor, executor],
    tasks=[task1, task2, task3]
)

result = crew.kickoff()
```

#### 3.2 The "Agent Studio" Superpower

**Concept**: Your existing "Agent Studio" is not legacy—it's your proprietary advantage.

**Strategy**: Wrap your "Agent Studio" automations as secure, callable functions for your new multi-agent systems.

```python
# Wrap your existing automation as an agent tool
def deploy_to_staging(app_name: str, version: str) -> dict:
    """
    Deploy application to staging using Agent Studio API

    Args:
        app_name: Name of application
        version: Version/tag to deploy

    Returns:
        Deployment status and details
    """
    # Call your existing Agent Studio automation
    result = agent_studio_api.trigger_workflow(
        workflow_id="deploy-to-staging",
        params={"app": app_name, "version": version}
    )
    return result

# Now this becomes an LLM tool
tools = [
    {
        "type": "function",
        "function": {
            "name": "deploy_to_staging",
            "description": deploy_to_staging.__doc__,
            "parameters": {...}
        }
    }
]
```

### Phase 4: Advanced Operations - Mastering "LLMOps"

The natural evolution of DevOps. If you manage infrastructure, you must manage AI infrastructure.

#### 4.1 Evaluation, Testing & Guardrails

**Concept**: You can't "unit test" an LLM, but you can evaluate it.

**Critical for Production**: This is what separates POCs from production systems.

**Evaluation Frameworks**:
- **DeepEval**: Comprehensive LLM testing
- **Ragas**: RAG-specific evaluation
- **LangSmith**: LangChain's evaluation platform

**Key Metrics**:
```python
from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import (
    AnswerRelevancyMetric,
    FaithfulnessMetric,
    ContextualPrecisionMetric
)

test_case = LLMTestCase(
    input="How do I configure terraform remote state?",
    actual_output=agent_response,
    expected_output="Configure S3 backend with state locking via DynamoDB",
    retrieval_context=retrieved_docs
)

# Metrics
faithfulness = FaithfulnessMetric()  # Did it hallucinate?
relevancy = AnswerRelevancyMetric()   # Is answer relevant?
precision = ContextualPrecisionMetric()  # Retrieved right docs?

assert_test(test_case, [faithfulness, relevancy, precision])
```

**CI/CD Integration**:
```yaml
# .github/workflows/test-agent.yml
name: Test AI Agent

on: [pull_request]

jobs:
  evaluate-agent:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run agent evaluation suite
        run: |
          pytest tests/agent_evaluation.py --junitxml=results.xml

      - name: Check evaluation scores
        run: |
          # Fail if scores below threshold
          python scripts/check_eval_scores.py --min-score 0.8
```

#### 4.2 Deployment & Monitoring

**Concept**: Apply IaC and DevOps principles to AI systems.

**Model Serving**:
```hcl
# terraform/llm-infrastructure.tf
resource "aws_ecs_task_definition" "llama_model" {
  family = "llama-3-70b"

  container_definitions = jsonencode([{
    name  = "llama-inference"
    image = "vllm/vllm-openai:latest"

    environment = [
      {
        name  = "MODEL_NAME"
        value = "meta-llama/Llama-3-70b"
      }
    ]

    resourceRequirements = [
      {
        type  = "GPU"
        value = "1"
      }
    ]
  }])
}
```

**Monitoring & Observability**:
```python
# Instrument your agents
from opentelemetry import trace
from langchain.callbacks import OpenAICallbackHandler

tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("agent-execution"):
    callback = OpenAICallbackHandler()
    result = agent.run(input, callbacks=[callback])

    # Track key metrics
    span = trace.get_current_span()
    span.set_attribute("llm.tokens.input", callback.total_tokens)
    span.set_attribute("llm.cost", callback.total_cost)
    span.set_attribute("llm.latency_ms", callback.total_time_ms)
```

**Security - Prompt Firewalls**:
```python
from langchain_experimental.comprehend_moderation import AmazonComprehendModerationChain

# Detect prompt injection attempts
moderation = AmazonComprehendModerationChain()

# Before sending to LLM
moderation_result = moderation.run(user_input)
if moderation_result["is_harmful"]:
    raise SecurityException("Potential prompt injection detected")
```

## Learning Path Timeline

### Weeks 1-2: Foundation
- LLM basics and prompt engineering
- Set up first RAG system
- **Milestone**: Working documentation chatbot

### Weeks 3-4: Agent Frameworks
- LangChain chains and agents
- Function calling integration
- **Milestone**: Chatbot can execute read-only tools

### Weeks 5-6: Multi-Agent Systems
- CrewAI multi-agent patterns
- Integrate with Agent Studio
- **Milestone**: Full DevOps Crew (plan → audit → execute)

### Weeks 7-8: Production Readiness
- Evaluation frameworks
- Monitoring and observability
- Security and guardrails
- **Milestone**: Production-ready agent with CI/CD

## Assessment & Certification

### Practical Capstone Project

Build a complete multi-agent DevOps system that:
1. Takes user infrastructure request
2. Generates terraform code
3. Runs security scan
4. Executes if approved
5. Performs smoke tests
6. Includes full observability

### Success Criteria
- [ ] Handles 10 different infrastructure request types
- [ ] 95%+ evaluation score on test suite
- [ ] Security audit passes (no prompt injection, safe tool use)
- [ ] Full monitoring dashboard
- [ ] Documented in team wiki
- [ ] Peer review by 2 team members

## Resources & Tools

### Essential Reading
- Anthropic Claude documentation
- LangChain documentation
- CrewAI documentation
- "Prompt Engineering Guide" (dair-ai)

### Tools to Install
```bash
# Core frameworks
pip install langchain openai anthropic crewai

# Vector databases
pip install chromadb pinecone-client

# Evaluation
pip install deepeval ragas

# Monitoring
pip install langsmith opentelemetry-api
```

### Practice Environments
- Claude Code (with skills)
- LangSmith playground
- Anthropic Workbench
- OpenAI Playground

## Your Competitive Advantage

Your team's advantage is NOT in building the next GPT-5.

Your advantage is building systems that wield AI with:
- **Reliability**: Using DevOps best practices
- **Security**: Implementing proper guardrails and auditing
- **Deep Integration**: Connecting to your existing Agent Studio

**While others build chatbots that can talk about code, your team will build agents that can write, test, deploy, and manage your entire infrastructure.**

That is how you compete.
