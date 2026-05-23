---
description: "LangChain & AI Agent Frameworks expert. Covers LCEL chains, ReAct/Plan-and-Execute/Multi-Agent architectures, tool calling, memory systems, LangGraph, CrewAI, prompt engineering, streaming, LangSmith tracing, RAG integration, and production deployment patterns."
model: opus
context: fork
---

# LangChain & AI Agent Frameworks

Expert guidance for building LLM-powered applications using LangChain, LangGraph, CrewAI, and related agent frameworks. Covers chain composition, agent architectures, tool integration, memory management, and production deployment.

## LCEL (LangChain Expression Language)

### Chain Composition with Runnables

LCEL is the declarative way to compose LangChain components. Every component implements the Runnable interface.

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

# Basic chain: prompt | model | parser
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant specialized in {domain}."),
    ("human", "{question}")
])

model = ChatOpenAI(model="gpt-4o", temperature=0)
parser = StrOutputParser()

chain = prompt | model | parser

# Invoke synchronously
result = chain.invoke({"domain": "Python", "question": "Explain decorators"})

# Async invoke
result = await chain.ainvoke({"domain": "Python", "question": "Explain decorators"})

# Batch processing
results = chain.batch([
    {"domain": "Python", "question": "Explain decorators"},
    {"domain": "Rust", "question": "Explain ownership"},
], config={"max_concurrency": 5})
```

### Parallel and Branching Chains

```python
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

# Parallel execution
parallel_chain = RunnableParallel(
    summary=summary_chain,
    keywords=keyword_chain,
    sentiment=sentiment_chain,
)
result = parallel_chain.invoke({"text": document})
# result = {"summary": "...", "keywords": [...], "sentiment": "positive"}

# Passthrough for forwarding input alongside transformations
chain = RunnableParallel(
    context=retriever,
    question=RunnablePassthrough(),
) | prompt | model | parser
```

### Fallback Chains

```python
from langchain_openai import ChatOpenAI

primary = ChatOpenAI(model="gpt-4o", temperature=0)
fallback = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Automatic fallback on failure
robust_model = primary.with_fallbacks([fallback])

chain = prompt | robust_model | parser
```

### Routing

```python
from langchain_core.runnables import RunnableLambda

def route_by_topic(input_dict: dict) -> Runnable:
    topic = input_dict.get("topic", "general")
    if topic == "technical":
        return technical_chain
    elif topic == "creative":
        return creative_chain
    return general_chain

routed_chain = RunnableLambda(route_by_topic)
```

## Agent Architectures

### ReAct Agent (Reasoning + Acting)

The standard agent pattern: the LLM reasons about what to do, takes an action via a tool, observes the result, and repeats.

```python
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.tools import tool
from langchain import hub

@tool
def search_database(query: str) -> str:
    """Search the product database for items matching the query."""
    # Implementation here
    return f"Found 3 results for '{query}'"

@tool
def calculate_price(item_id: str, quantity: int) -> float:
    """Calculate the total price for a given item and quantity."""
    prices = {"SKU001": 29.99, "SKU002": 49.99}
    return prices.get(item_id, 0) * quantity

tools = [search_database, calculate_price]
llm = ChatOpenAI(model="gpt-4o", temperature=0)
prompt = hub.pull("hwchase17/react")

agent = create_react_agent(llm, tools, prompt)
executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=10,
    handle_parsing_errors=True,
)

result = executor.invoke({"input": "Find laptops under $500 and calculate price for 3 units"})
```

### Tool Calling Agent (Preferred for Modern Models)

```python
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful shopping assistant."),
    MessagesPlaceholder("chat_history", optional=True),
    ("human", "{input}"),
    MessagesPlaceholder("agent_scratchpad"),
])

agent = create_tool_calling_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
```

### Plan-and-Execute Agent

Separates planning from execution for complex multi-step tasks.

```python
from langchain_experimental.plan_and_execute import (
    PlanAndExecute, load_agent_executor, load_chat_planner,
)

planner = load_chat_planner(ChatOpenAI(model="gpt-4o", temperature=0))
executor_agent = load_agent_executor(
    ChatOpenAI(model="gpt-4o-mini", temperature=0),
    tools=tools,
    verbose=True,
)

agent = PlanAndExecute(
    planner=planner,
    executor=executor_agent,
    verbose=True,
)

result = agent.invoke({"input": "Research competitor pricing and create a report"})
```

## Tool Calling and Function Calling

### Defining Tools

```python
from langchain_core.tools import tool, StructuredTool
from pydantic import BaseModel, Field

# Decorator approach (simplest)
@tool
def get_weather(city: str, unit: str = "celsius") -> str:
    """Get the current weather for a city.

    Args:
        city: The city name to look up weather for.
        unit: Temperature unit, either 'celsius' or 'fahrenheit'.
    """
    return f"Weather in {city}: 22 {unit}"

# Pydantic schema approach (most control)
class SearchInput(BaseModel):
    query: str = Field(description="The search query")
    max_results: int = Field(default=5, description="Maximum results to return")
    include_metadata: bool = Field(default=False)

@tool(args_schema=SearchInput)
def search(query: str, max_results: int = 5, include_metadata: bool = False) -> str:
    """Search the knowledge base."""
    return f"Results for '{query}'"

# StructuredTool for dynamic creation
def _run_query(sql: str) -> str:
    return f"Executed: {sql}"

sql_tool = StructuredTool.from_function(
    func=_run_query,
    name="sql_query",
    description="Execute a read-only SQL query",
)
```

### Binding Tools to Models

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o")

# Bind tools for function calling
llm_with_tools = llm.bind_tools(tools)

# Force a specific tool
llm_forced = llm.bind_tools(tools, tool_choice="get_weather")

# Parallel tool calling
response = llm_with_tools.invoke("What's the weather in Paris and London?")
for tool_call in response.tool_calls:
    print(f"Tool: {tool_call['name']}, Args: {tool_call['args']}")
```

## Memory Systems

### Conversation Memory

```python
from langchain.memory import (
    ConversationBufferMemory,
    ConversationSummaryMemory,
    ConversationBufferWindowMemory,
    ConversationSummaryBufferMemory,
)

# Full conversation history (simple, grows unbounded)
buffer_memory = ConversationBufferMemory(return_messages=True)

# Sliding window (last k exchanges)
window_memory = ConversationBufferWindowMemory(k=10, return_messages=True)

# Summarize older messages (saves tokens)
summary_memory = ConversationSummaryMemory(
    llm=ChatOpenAI(model="gpt-4o-mini"),
    return_messages=True,
)

# Hybrid: recent messages verbatim + older messages summarized
hybrid_memory = ConversationSummaryBufferMemory(
    llm=ChatOpenAI(model="gpt-4o-mini"),
    max_token_limit=2000,
    return_messages=True,
)
```

### Long-Term Memory with Vector Stores

```python
from langchain.memory import VectorStoreRetrieverMemory
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

vectorstore = Chroma(
    collection_name="memory",
    embedding_function=OpenAIEmbeddings(),
)

memory = VectorStoreRetrieverMemory(
    retriever=vectorstore.as_retriever(search_kwargs={"k": 5}),
    memory_key="relevant_history",
)

# Saves conversation turns as searchable documents
memory.save_context(
    {"input": "My favorite color is blue"},
    {"output": "I'll remember that!"},
)
```

## Structured Output Parsing

```python
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

class ProductReview(BaseModel):
    sentiment: str = Field(description="positive, negative, or neutral")
    confidence: float = Field(ge=0.0, le=1.0)
    key_points: list[str] = Field(description="Main points from the review")
    recommendation: bool = Field(description="Whether the reviewer recommends the product")

# Method 1: with_structured_output (preferred, uses tool calling)
structured_llm = llm.with_structured_output(ProductReview)
result: ProductReview = structured_llm.invoke("Review: This laptop is amazing...")

# Method 2: PydanticOutputParser (works with any model)
parser = PydanticOutputParser(pydantic_object=ProductReview)
prompt = ChatPromptTemplate.from_messages([
    ("system", "Analyze the review.\n{format_instructions}"),
    ("human", "{review}"),
]).partial(format_instructions=parser.get_format_instructions())

chain = prompt | model | parser
result: ProductReview = chain.invoke({"review": "This laptop is amazing..."})
```

## LangGraph for Stateful Multi-Agent Workflows

### Basic Graph

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator

class AgentState(TypedDict):
    messages: Annotated[list, operator.add]
    next_step: str
    iteration: int

def researcher(state: AgentState) -> dict:
    """Research node: gathers information."""
    messages = state["messages"]
    response = research_chain.invoke({"messages": messages})
    return {
        "messages": [response],
        "next_step": "analyzer",
        "iteration": state["iteration"] + 1,
    }

def analyzer(state: AgentState) -> dict:
    """Analyzer node: processes research results."""
    response = analysis_chain.invoke({"messages": state["messages"]})
    return {"messages": [response], "next_step": "writer"}

def writer(state: AgentState) -> dict:
    """Writer node: produces final output."""
    response = writing_chain.invoke({"messages": state["messages"]})
    return {"messages": [response], "next_step": "end"}

def should_continue(state: AgentState) -> str:
    if state["iteration"] > 3:
        return "writer"  # Force completion after 3 iterations
    return state["next_step"]

# Build the graph
graph = StateGraph(AgentState)
graph.add_node("researcher", researcher)
graph.add_node("analyzer", analyzer)
graph.add_node("writer", writer)

graph.set_entry_point("researcher")
graph.add_conditional_edges("researcher", should_continue)
graph.add_edge("analyzer", "researcher")
graph.add_edge("writer", END)

app = graph.compile()
result = app.invoke({
    "messages": ["Research the impact of AI on healthcare"],
    "next_step": "researcher",
    "iteration": 0,
})
```

### Human-in-the-Loop with LangGraph

```python
from langgraph.checkpoint.memory import MemorySaver

checkpointer = MemorySaver()

graph = StateGraph(AgentState)
# ... add nodes ...

# Compile with interrupt
app = graph.compile(
    checkpointer=checkpointer,
    interrupt_before=["critical_action"],  # Pause before this node
)

config = {"configurable": {"thread_id": "user-123"}}
result = app.invoke(initial_state, config)
# Execution pauses at "critical_action"

# After human approval, resume
result = app.invoke(None, config)
```

## CrewAI for Team-Based Orchestration

```python
from crewai import Agent, Task, Crew, Process

researcher = Agent(
    role="Senior Research Analyst",
    goal="Uncover cutting-edge developments in AI",
    backstory="You are an expert analyst at a leading tech think tank.",
    tools=[search_tool, scrape_tool],
    llm="gpt-4o",
    verbose=True,
)

writer = Agent(
    role="Tech Content Strategist",
    goal="Craft compelling content about tech advancements",
    backstory="You are a content strategist known for insightful articles.",
    llm="gpt-4o",
)

research_task = Task(
    description="Research the latest AI agent frameworks in 2026.",
    expected_output="A detailed report with key findings and trends.",
    agent=researcher,
)

writing_task = Task(
    description="Write a blog post based on the research report.",
    expected_output="A 1000-word blog post in markdown.",
    agent=writer,
    context=[research_task],  # Receives output from research
)

crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, writing_task],
    process=Process.sequential,
    verbose=True,
)

result = crew.kickoff()
```

## Streaming Responses and Callbacks

```python
# Streaming with LCEL
async for chunk in chain.astream({"question": "Explain quantum computing"}):
    print(chunk, end="", flush=True)

# Streaming events (detailed)
async for event in chain.astream_events(
    {"question": "Explain quantum computing"},
    version="v2",
):
    if event["event"] == "on_chat_model_stream":
        print(event["data"]["chunk"].content, end="")
    elif event["event"] == "on_tool_start":
        print(f"\nUsing tool: {event['name']}")

# Custom callback handler
from langchain_core.callbacks import BaseCallbackHandler

class CostTracker(BaseCallbackHandler):
    def __init__(self):
        self.total_tokens = 0
        self.total_cost = 0.0

    def on_llm_end(self, response, **kwargs):
        usage = response.llm_output.get("token_usage", {})
        self.total_tokens += usage.get("total_tokens", 0)
        # Calculate cost based on model pricing
```

## LangSmith for Tracing and Evaluation

```python
import os

# Enable tracing (set environment variables)
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "ls__..."
os.environ["LANGCHAIN_PROJECT"] = "my-project"

# All chain invocations are now traced automatically

# Programmatic evaluation
from langsmith import Client
from langsmith.evaluation import evaluate

client = Client()

def correctness_evaluator(run, example):
    prediction = run.outputs["output"]
    reference = example.outputs["answer"]
    score = 1.0 if prediction.strip() == reference.strip() else 0.0
    return {"key": "correctness", "score": score}

results = evaluate(
    lambda inputs: chain.invoke(inputs),
    data="my-dataset",
    evaluators=[correctness_evaluator],
    experiment_prefix="v1",
)
```

## Production Deployment Patterns

### Rate Limiting and Retry

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-4o",
    max_retries=3,
    request_timeout=30,
    max_tokens=4096,
)

# Rate limiting with asyncio semaphore
import asyncio

semaphore = asyncio.Semaphore(10)  # Max 10 concurrent requests

async def rate_limited_invoke(input_data):
    async with semaphore:
        return await chain.ainvoke(input_data)
```

### Caching

```python
from langchain_core.globals import set_llm_cache
from langchain_community.cache import RedisCache, SQLiteCache
import redis

# SQLite cache (development)
set_llm_cache(SQLiteCache(database_path=".langchain_cache.db"))

# Redis cache (production)
set_llm_cache(RedisCache(redis_=redis.Redis(host="localhost", port=6379)))
```

## Cost Optimization

### Decision Framework

| Approach | Use When | Cost |
|----------|----------|------|
| GPT-4o-mini / Claude Haiku | Simple tasks, classification, extraction | Low |
| GPT-4o / Claude Sonnet | Complex reasoning, code generation | Medium |
| GPT-4o + tools / Claude Opus | Multi-step planning, agent workflows | High |
| Fine-tuned small model | Repetitive domain-specific tasks | Lowest per-call |

### Token Reduction Strategies

```python
# 1. Trim conversation history
from langchain_core.messages import trim_messages

trimmed = trim_messages(
    messages,
    max_tokens=4000,
    strategy="last",
    token_counter=ChatOpenAI(model="gpt-4o"),
    include_system=True,
)

# 2. Use structured output to avoid verbose responses
# 3. Cache repeated queries (see caching section above)
# 4. Batch similar requests
results = await chain.abatch(inputs, config={"max_concurrency": 10})
```

## Security Best Practices

### Prompt Injection Defense

```python
# 1. Input sanitization
def sanitize_input(user_input: str) -> str:
    # Remove common injection patterns
    dangerous_patterns = [
        "ignore previous instructions",
        "you are now",
        "system prompt:",
    ]
    sanitized = user_input
    for pattern in dangerous_patterns:
        if pattern.lower() in sanitized.lower():
            sanitized = sanitized.replace(pattern, "[FILTERED]")
    return sanitized

# 2. Output validation
class SafeOutput(BaseModel):
    content: str
    contains_code: bool
    risk_level: str = Field(pattern="^(low|medium|high)$")

safe_llm = llm.with_structured_output(SafeOutput)

# 3. Tool permission scoping
@tool
def read_file(path: str) -> str:
    """Read a file from the allowed directory only."""
    allowed_dir = "/data/public/"
    resolved = os.path.realpath(path)
    if not resolved.startswith(allowed_dir):
        raise ValueError("Access denied: path outside allowed directory")
    with open(resolved) as f:
        return f.read()
```

### Guardrails

```python
# Use LangChain's built-in moderation
from langchain.chains import OpenAIModerationChain

moderation = OpenAIModerationChain(error=True)

safe_chain = (
    {"input": RunnablePassthrough()}
    | moderation
    | main_chain
)
```

## Error Handling and Fallback Patterns

```python
from langchain_core.runnables import RunnableLambda

# Retry with exponential backoff (built into LangChain)
llm = ChatOpenAI(model="gpt-4o", max_retries=3)

# Fallback chain with different providers
from langchain_anthropic import ChatAnthropic

primary = ChatOpenAI(model="gpt-4o")
secondary = ChatAnthropic(model="claude-sonnet-4-20250514")
tertiary = ChatOpenAI(model="gpt-4o-mini")

robust = primary.with_fallbacks([secondary, tertiary])

# Custom error handler
def handle_error(error: Exception) -> str:
    if "rate_limit" in str(error).lower():
        return "System is busy. Please try again in a moment."
    return f"An error occurred: {type(error).__name__}"

chain_with_fallback = chain.with_fallbacks(
    [fallback_chain],
    exceptions_to_handle=(Exception,),
) | RunnableLambda(lambda x: x).with_retry(stop_after_attempt=3)
```

## Decision Framework: When to Use What

| Need | Solution |
|------|----------|
| Simple Q&A | Single LCEL chain |
| Multi-step reasoning | ReAct agent or tool-calling agent |
| Complex workflow with state | LangGraph |
| Team of specialists | CrewAI or LangGraph multi-agent |
| Production reliability | Fallback chains + caching + rate limiting |
| Debugging and evaluation | LangSmith tracing |
| Long conversations | Summary memory + vector store memory |
| Structured data extraction | `with_structured_output` + Pydantic |
