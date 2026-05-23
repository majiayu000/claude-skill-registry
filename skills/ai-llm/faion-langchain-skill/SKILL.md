---
name: faion-langchain-skill
user-invocable: false
description: ""
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(python:*), Bash(pip:*)
---

# LangChain Skill

**Communication: User's language. Docs/code: English.**

## Purpose

Orchestrate multi-step AI workflows using LangChain and LangGraph. Build production-ready chains, agents, and multi-agent systems.

## When to Use

- Building conversational AI with memory
- Creating multi-step reasoning pipelines
- Implementing agent architectures (ReAct, Plan-and-Execute)
- Orchestrating tool use with LLMs
- Building multi-agent systems
- Creating RAG pipelines with retrieval

---

# Section 1: Core Concepts

## LangChain vs LangGraph

| Component | Purpose | Use When |
|-----------|---------|----------|
| **LangChain** | Chains, prompts, memory | Simple sequential pipelines |
| **LangGraph** | State machines, agents | Complex control flow, agents |

**Recommendation:** Use LangGraph for new projects. LangChain for simple chains.

## Installation

```bash
# Core packages
pip install langchain langchain-core langchain-community

# LangGraph for agents
pip install langgraph

# Provider-specific
pip install langchain-openai langchain-anthropic langchain-google-genai

# Observability
pip install langsmith
```

## Environment Setup

```python
import os

# LLM API keys
os.environ["OPENAI_API_KEY"] = "sk-..."
os.environ["ANTHROPIC_API_KEY"] = "sk-ant-..."

# LangSmith tracing (optional but recommended)
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "ls__..."
os.environ["LANGCHAIN_PROJECT"] = "my-project"
```

---

# Section 2: Chain Patterns

## Pattern 1: Sequential Chain

Simple A → B → C pipeline.

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

# Define components
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("human", "{input}")
])
model = ChatOpenAI(model="gpt-4o-mini")
parser = StrOutputParser()

# Chain using LCEL (LangChain Expression Language)
chain = prompt | model | parser

# Invoke
result = chain.invoke({"input": "What is LangChain?"})
```

## Pattern 2: Router Chain

Route to different chains based on input.

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableBranch, RunnableLambda

# Define specialized chains
math_prompt = ChatPromptTemplate.from_template("Solve this math problem: {input}")
code_prompt = ChatPromptTemplate.from_template("Write code for: {input}")
general_prompt = ChatPromptTemplate.from_template("Answer: {input}")

math_chain = math_prompt | model | parser
code_chain = code_prompt | model | parser
general_chain = general_prompt | model | parser

# Router function
def route(info: dict) -> str:
    topic = info.get("topic", "").lower()
    if "math" in topic:
        return "math"
    elif "code" in topic:
        return "code"
    return "general"

# Create router
branch = RunnableBranch(
    (lambda x: route(x) == "math", math_chain),
    (lambda x: route(x) == "code", code_chain),
    general_chain  # Default
)

# Use
result = branch.invoke({"input": "2 + 2", "topic": "math"})
```

## Pattern 3: MapReduce Chain

Process multiple items in parallel, then combine.

```python
from langchain_core.runnables import RunnableParallel

# Map: process each document
summarize_prompt = ChatPromptTemplate.from_template(
    "Summarize this document in 2 sentences:\n\n{document}"
)
summarize_chain = summarize_prompt | model | parser

# Reduce: combine summaries
combine_prompt = ChatPromptTemplate.from_template(
    "Combine these summaries into a coherent overview:\n\n{summaries}"
)
combine_chain = combine_prompt | model | parser

# MapReduce function
def map_reduce(documents: list[str]) -> str:
    # Map phase
    summaries = [summarize_chain.invoke({"document": doc}) for doc in documents]

    # Reduce phase
    combined = combine_chain.invoke({"summaries": "\n\n".join(summaries)})
    return combined

# With parallel execution
from langchain_core.runnables import RunnableParallel

def parallel_map(documents: list[str]) -> list[str]:
    parallel = RunnableParallel({
        f"doc_{i}": summarize_chain for i, _ in enumerate(documents)
    })
    inputs = {f"doc_{i}": {"document": doc} for i, doc in enumerate(documents)}
    results = parallel.invoke(inputs)
    return list(results.values())
```

## Pattern 4: Fallback Chain

Try primary, fall back to secondary on failure.

```python
from langchain_core.runnables import RunnableWithFallbacks

# Primary (expensive, high quality)
primary = ChatOpenAI(model="gpt-4o") | parser

# Fallback (cheaper, faster)
fallback = ChatOpenAI(model="gpt-4o-mini") | parser

# Chain with fallback
robust_chain = primary.with_fallbacks([fallback])

# Will try gpt-4o first, then gpt-4o-mini if it fails
result = robust_chain.invoke("Complex question...")
```

---

# Section 3: Agent Architectures

## Architecture 1: ReAct (Reasoning + Acting)

Think step-by-step, use tools, observe results, repeat.

```python
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool

# Define tools
@tool
def search(query: str) -> str:
    """Search the web for information."""
    # Implementation
    return f"Results for: {query}"

@tool
def calculator(expression: str) -> str:
    """Calculate a mathematical expression."""
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error: {e}"

# Create ReAct agent
model = ChatOpenAI(model="gpt-4o")
tools = [search, calculator]

agent = create_react_agent(model, tools)

# Run
result = agent.invoke({
    "messages": [("human", "What is 25 * 4 and who invented calculus?")]
})
```

## Architecture 2: Plan-and-Execute

Plan all steps first, then execute each.

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, List
import operator

class PlanExecuteState(TypedDict):
    input: str
    plan: List[str]
    current_step: int
    results: Annotated[List[str], operator.add]
    final_answer: str

def planner(state: PlanExecuteState) -> PlanExecuteState:
    """Create a plan of steps."""
    prompt = f"""Create a step-by-step plan to answer: {state['input']}
    Return a numbered list of steps."""

    response = model.invoke(prompt)
    steps = parse_steps(response.content)

    return {"plan": steps, "current_step": 0}

def executor(state: PlanExecuteState) -> PlanExecuteState:
    """Execute current step."""
    step = state["plan"][state["current_step"]]

    result = model.invoke(f"Execute this step: {step}")

    return {
        "results": [result.content],
        "current_step": state["current_step"] + 1
    }

def should_continue(state: PlanExecuteState) -> str:
    if state["current_step"] >= len(state["plan"]):
        return "synthesize"
    return "execute"

def synthesizer(state: PlanExecuteState) -> PlanExecuteState:
    """Combine results into final answer."""
    all_results = "\n".join(state["results"])
    prompt = f"Synthesize these results into a final answer:\n{all_results}"

    response = model.invoke(prompt)
    return {"final_answer": response.content}

# Build graph
graph = StateGraph(PlanExecuteState)
graph.add_node("plan", planner)
graph.add_node("execute", executor)
graph.add_node("synthesize", synthesizer)

graph.set_entry_point("plan")
graph.add_edge("plan", "execute")
graph.add_conditional_edges("execute", should_continue)
graph.add_edge("synthesize", END)

agent = graph.compile()
```

## Architecture 3: LATS (Language Agent Tree Search)

Tree search with backtracking for complex problems.

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Optional
import random

class LATSState(TypedDict):
    problem: str
    thoughts: List[dict]  # Tree of thoughts
    current_path: List[int]  # Path through tree
    best_solution: Optional[str]
    best_score: float

def generate_thoughts(state: LATSState) -> LATSState:
    """Generate multiple candidate thoughts."""
    current_context = get_current_context(state)

    prompt = f"""Given this problem and context, generate 3 different approaches:
    Problem: {state['problem']}
    Context: {current_context}

    Return 3 distinct approaches."""

    response = model.invoke(prompt)
    new_thoughts = parse_thoughts(response.content)

    # Add to tree
    parent_idx = state["current_path"][-1] if state["current_path"] else -1
    for thought in new_thoughts:
        state["thoughts"].append({
            "content": thought,
            "parent": parent_idx,
            "score": None,
            "children": []
        })

    return state

def evaluate_thoughts(state: LATSState) -> LATSState:
    """Score each thought for promise."""
    for i, thought in enumerate(state["thoughts"]):
        if thought["score"] is None:
            prompt = f"""Rate this approach (0-10):
            Problem: {state['problem']}
            Approach: {thought['content']}
            """
            response = model.invoke(prompt)
            thought["score"] = parse_score(response.content)

    return state

def select_thought(state: LATSState) -> LATSState:
    """Select most promising unexplored thought."""
    unexplored = [
        (i, t) for i, t in enumerate(state["thoughts"])
        if not t["children"] and t["score"] is not None
    ]

    if not unexplored:
        return state

    # UCB-like selection
    best_idx = max(unexplored, key=lambda x: x[1]["score"])[0]
    state["current_path"].append(best_idx)

    return state

def should_continue_lats(state: LATSState) -> str:
    if state["best_score"] and state["best_score"] > 8:
        return END
    if len(state["thoughts"]) > 20:  # Max nodes
        return END
    return "generate"

# Build LATS graph
lats = StateGraph(LATSState)
lats.add_node("generate", generate_thoughts)
lats.add_node("evaluate", evaluate_thoughts)
lats.add_node("select", select_thought)

lats.set_entry_point("generate")
lats.add_edge("generate", "evaluate")
lats.add_edge("evaluate", "select")
lats.add_conditional_edges("select", should_continue_lats)
```

---

# Section 4: Memory Types

## Type 1: Conversation Buffer Memory

Store full conversation history.

```python
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# Create store
store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

# Wrap chain with memory
chain_with_memory = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history"
)

# Use with session
result = chain_with_memory.invoke(
    {"input": "My name is Alice"},
    config={"configurable": {"session_id": "user-123"}}
)

# Later in same session
result = chain_with_memory.invoke(
    {"input": "What's my name?"},
    config={"configurable": {"session_id": "user-123"}}
)
# Returns: "Your name is Alice"
```

## Type 2: Conversation Summary Memory

Summarize old messages to save tokens.

```python
from langchain.memory import ConversationSummaryMemory
from langchain_openai import ChatOpenAI

summary_llm = ChatOpenAI(model="gpt-4o-mini")

class SummaryMemory:
    def __init__(self, llm, max_messages: int = 10):
        self.llm = llm
        self.max_messages = max_messages
        self.messages = []
        self.summary = ""

    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})

        if len(self.messages) > self.max_messages:
            self._summarize()

    def _summarize(self):
        # Summarize oldest half
        to_summarize = self.messages[:len(self.messages)//2]
        remaining = self.messages[len(self.messages)//2:]

        messages_text = "\n".join(
            f"{m['role']}: {m['content']}" for m in to_summarize
        )

        prompt = f"""Summarize this conversation:
        Previous summary: {self.summary}

        New messages:
        {messages_text}
        """

        response = self.llm.invoke(prompt)
        self.summary = response.content
        self.messages = remaining

    def get_context(self) -> str:
        recent = "\n".join(
            f"{m['role']}: {m['content']}" for m in self.messages
        )
        return f"Summary: {self.summary}\n\nRecent:\n{recent}"
```

## Type 3: Vector Store Memory

Retrieve relevant past interactions via semantic search.

```python
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

class VectorMemory:
    def __init__(self, collection_name: str = "memory"):
        self.embeddings = OpenAIEmbeddings()
        self.vectorstore = Chroma(
            collection_name=collection_name,
            embedding_function=self.embeddings
        )

    def add_interaction(self, human: str, assistant: str, metadata: dict = None):
        """Store a conversation turn."""
        text = f"Human: {human}\nAssistant: {assistant}"
        self.vectorstore.add_texts(
            texts=[text],
            metadatas=[metadata or {}]
        )

    def get_relevant(self, query: str, k: int = 3) -> list[str]:
        """Retrieve relevant past interactions."""
        docs = self.vectorstore.similarity_search(query, k=k)
        return [doc.page_content for doc in docs]

    def get_context(self, current_query: str) -> str:
        """Get memory context for prompt."""
        relevant = self.get_relevant(current_query)
        if not relevant:
            return ""
        return "Relevant past interactions:\n" + "\n---\n".join(relevant)

# Usage
memory = VectorMemory()
memory.add_interaction(
    "What's the capital of France?",
    "The capital of France is Paris."
)

# Later
context = memory.get_context("Tell me about French cities")
# Returns relevant past interaction about Paris
```

## Type 4: Entity Memory

Track entities mentioned in conversation.

```python
from langchain_openai import ChatOpenAI

class EntityMemory:
    def __init__(self, llm):
        self.llm = llm
        self.entities = {}

    def extract_entities(self, text: str) -> dict:
        """Extract entities from text."""
        prompt = f"""Extract named entities from this text.
        Return as JSON: {{"entity_name": "entity_info"}}

        Text: {text}
        """
        response = self.llm.invoke(prompt)
        return parse_json(response.content)

    def update(self, text: str):
        """Update entity store with new information."""
        new_entities = self.extract_entities(text)
        for name, info in new_entities.items():
            if name in self.entities:
                # Merge information
                self.entities[name] = self._merge(self.entities[name], info)
            else:
                self.entities[name] = info

    def get_context(self, entities: list[str]) -> str:
        """Get context for specific entities."""
        relevant = {k: v for k, v in self.entities.items() if k in entities}
        return f"Known entities: {relevant}"
```

---

# Section 5: Prompt Templates

## Basic Templates

```python
from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder
)

# Simple template
simple = ChatPromptTemplate.from_template("Translate to French: {text}")

# With system message
chat = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful translator."),
    ("human", "Translate to {language}: {text}")
])

# With message history placeholder
with_history = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])
```

## Few-Shot Templates

```python
from langchain_core.prompts import FewShotChatMessagePromptTemplate

examples = [
    {"input": "2 + 2", "output": "4"},
    {"input": "5 * 3", "output": "15"},
]

example_prompt = ChatPromptTemplate.from_messages([
    ("human", "{input}"),
    ("ai", "{output}")
])

few_shot = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=examples
)

final_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a calculator."),
    few_shot,
    ("human", "{input}")
])
```

## Dynamic Few-Shot Selection

```python
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

examples = [
    {"input": "happy", "output": "sad"},
    {"input": "tall", "output": "short"},
    {"input": "fast", "output": "slow"},
    {"input": "rich", "output": "poor"},
]

selector = SemanticSimilarityExampleSelector.from_examples(
    examples,
    OpenAIEmbeddings(),
    Chroma,
    k=2  # Select 2 most relevant examples
)

dynamic_few_shot = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    example_selector=selector
)

# Will select most relevant examples for "big"
result = dynamic_few_shot.invoke({"input": "big"})
```

---

# Section 6: Output Parsers

## String Parser

```python
from langchain_core.output_parsers import StrOutputParser

parser = StrOutputParser()
chain = prompt | model | parser
```

## JSON Parser

```python
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

class Answer(BaseModel):
    answer: str = Field(description="The answer")
    confidence: float = Field(description="Confidence 0-1")

parser = JsonOutputParser(pydantic_object=Answer)

prompt = ChatPromptTemplate.from_messages([
    ("system", "Answer questions with confidence score."),
    ("human", "{question}\n\n{format_instructions}")
])

chain = prompt.partial(format_instructions=parser.get_format_instructions()) | model | parser
```

## Structured Output (Recommended)

```python
from langchain_core.pydantic_v1 import BaseModel, Field

class SearchQuery(BaseModel):
    """Search query parameters."""
    query: str = Field(description="The search query")
    filters: list[str] = Field(default=[], description="Filters to apply")
    limit: int = Field(default=10, description="Max results")

# Use with_structured_output for reliable parsing
structured_model = model.with_structured_output(SearchQuery)

result = structured_model.invoke("Find Python tutorials, limit 5")
# Returns: SearchQuery(query="Python tutorials", filters=[], limit=5)
```

## Streaming Parser

```python
from langchain_core.output_parsers import JsonOutputParser

parser = JsonOutputParser()

chain = prompt | model | parser

# Stream partial results
for chunk in chain.stream({"input": "Generate a complex JSON"}):
    print(chunk)  # Partial JSON as it's generated
```

---

# Section 7: Tool Integration

## Defining Tools

```python
from langchain_core.tools import tool, StructuredTool
from pydantic import BaseModel, Field

# Simple tool with decorator
@tool
def search(query: str) -> str:
    """Search the web for information about a topic."""
    return f"Search results for: {query}"

# Tool with complex input
class CalculatorInput(BaseModel):
    expression: str = Field(description="Mathematical expression")
    precision: int = Field(default=2, description="Decimal places")

@tool(args_schema=CalculatorInput)
def calculate(expression: str, precision: int = 2) -> str:
    """Calculate a mathematical expression."""
    result = eval(expression)
    return f"{result:.{precision}f}"

# Dynamic tool creation
def create_api_tool(api_name: str, base_url: str):
    @tool(name=f"{api_name}_api")
    def api_tool(endpoint: str, params: dict = None) -> str:
        f"""Call the {api_name} API."""
        # Implementation
        return f"API response from {base_url}/{endpoint}"
    return api_tool
```

## Tool Error Handling

```python
from langchain_core.tools import ToolException

@tool(handle_tool_error=True)
def risky_tool(input: str) -> str:
    """A tool that might fail."""
    if not input:
        raise ToolException("Input cannot be empty")
    return f"Processed: {input}"

# Custom error handler
def handle_error(error: ToolException) -> str:
    return f"Tool failed: {error}. Please try again with valid input."

@tool(handle_tool_error=handle_error)
def custom_error_tool(input: str) -> str:
    """Tool with custom error handling."""
    if "bad" in input:
        raise ToolException("Bad input detected")
    return input
```

## Tool Binding

```python
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4o")
tools = [search, calculate]

# Bind tools to model
model_with_tools = model.bind_tools(tools)

# Invoke
response = model_with_tools.invoke("What is 25 * 4?")

# Check for tool calls
if response.tool_calls:
    for call in response.tool_calls:
        print(f"Tool: {call['name']}, Args: {call['args']}")
```

---

# Section 8: LangGraph Workflows

## State Definition

```python
from typing import TypedDict, Annotated, List
import operator

class WorkflowState(TypedDict):
    # Simple fields
    input: str
    output: str

    # Accumulating field (appends instead of replaces)
    messages: Annotated[List[str], operator.add]

    # Optional field
    error: str | None

# Usage: {"messages": ["new"]} adds to existing messages
```

## Node Functions

```python
from langgraph.graph import StateGraph, END

def process_node(state: WorkflowState) -> WorkflowState:
    """Process the input."""
    result = f"Processed: {state['input']}"
    return {
        "output": result,
        "messages": [f"Processed input: {state['input']}"]
    }

def validate_node(state: WorkflowState) -> WorkflowState:
    """Validate the output."""
    if "error" in state["output"].lower():
        return {"error": "Validation failed"}
    return {"messages": ["Validation passed"]}

def finalize_node(state: WorkflowState) -> WorkflowState:
    """Finalize the workflow."""
    return {"messages": ["Workflow complete"]}
```

## Conditional Edges

```python
def should_continue(state: WorkflowState) -> str:
    """Determine next node based on state."""
    if state.get("error"):
        return "error_handler"
    if len(state.get("messages", [])) > 10:
        return END
    return "process"

# Build graph
graph = StateGraph(WorkflowState)

graph.add_node("process", process_node)
graph.add_node("validate", validate_node)
graph.add_node("finalize", finalize_node)
graph.add_node("error_handler", error_handler)

graph.set_entry_point("process")
graph.add_edge("process", "validate")
graph.add_conditional_edges(
    "validate",
    should_continue,
    {
        "process": "process",
        "error_handler": "error_handler",
        END: END
    }
)
graph.add_edge("finalize", END)
graph.add_edge("error_handler", END)

workflow = graph.compile()
```

## Human-in-the-Loop

```python
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, END

# Create checkpointer for persistence
memory = MemorySaver()

def get_approval(state: WorkflowState) -> WorkflowState:
    """Node that requires human approval."""
    return {"messages": ["Waiting for approval..."]}

def execute_action(state: WorkflowState) -> WorkflowState:
    """Execute after approval."""
    return {"output": "Action executed", "messages": ["Done"]}

# Build graph with interrupt
graph = StateGraph(WorkflowState)
graph.add_node("get_approval", get_approval)
graph.add_node("execute", execute_action)

graph.set_entry_point("get_approval")
graph.add_edge("get_approval", "execute")
graph.add_edge("execute", END)

# Compile with interrupt before execute
workflow = graph.compile(
    checkpointer=memory,
    interrupt_before=["execute"]
)

# First run - stops at interrupt
config = {"configurable": {"thread_id": "1"}}
result = workflow.invoke({"input": "Do something"}, config)

# Resume after approval
result = workflow.invoke(None, config)  # Continues from checkpoint
```

## Subgraphs

```python
from langgraph.graph import StateGraph

# Define subgraph
def create_research_subgraph():
    graph = StateGraph(WorkflowState)
    graph.add_node("search", search_node)
    graph.add_node("analyze", analyze_node)
    graph.set_entry_point("search")
    graph.add_edge("search", "analyze")
    return graph.compile()

research_subgraph = create_research_subgraph()

# Use in main graph
main = StateGraph(WorkflowState)
main.add_node("research", research_subgraph)
main.add_node("synthesize", synthesize_node)

main.set_entry_point("research")
main.add_edge("research", "synthesize")
main.add_edge("synthesize", END)

main_workflow = main.compile()
```

---

# Section 9: Multi-Agent Systems

## Pattern 1: Supervisor Architecture

One agent routes to specialized workers.

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Literal

class TeamState(TypedDict):
    input: str
    next_agent: str
    messages: list
    final_answer: str

def supervisor(state: TeamState) -> TeamState:
    """Route to appropriate specialist."""
    prompt = f"""You are a supervisor. Route this query to the right agent.
    Options: researcher, coder, writer

    Query: {state['input']}

    Respond with just the agent name."""

    response = model.invoke(prompt)
    return {"next_agent": response.content.strip().lower()}

def researcher(state: TeamState) -> TeamState:
    """Research specialist."""
    response = model.invoke(f"Research this: {state['input']}")
    return {"messages": [f"Researcher: {response.content}"]}

def coder(state: TeamState) -> TeamState:
    """Coding specialist."""
    response = model.invoke(f"Write code for: {state['input']}")
    return {"messages": [f"Coder: {response.content}"]}

def writer(state: TeamState) -> TeamState:
    """Writing specialist."""
    response = model.invoke(f"Write content for: {state['input']}")
    return {"messages": [f"Writer: {response.content}"]}

def route_to_agent(state: TeamState) -> str:
    return state["next_agent"]

# Build
graph = StateGraph(TeamState)
graph.add_node("supervisor", supervisor)
graph.add_node("researcher", researcher)
graph.add_node("coder", coder)
graph.add_node("writer", writer)

graph.set_entry_point("supervisor")
graph.add_conditional_edges(
    "supervisor",
    route_to_agent,
    {"researcher": "researcher", "coder": "coder", "writer": "writer"}
)
graph.add_edge("researcher", END)
graph.add_edge("coder", END)
graph.add_edge("writer", END)

team = graph.compile()
```

## Pattern 2: Debate Architecture

Agents debate to reach consensus.

```python
class DebateState(TypedDict):
    topic: str
    positions: list[dict]
    round: int
    consensus: str | None

def agent_a(state: DebateState) -> DebateState:
    """First debater."""
    context = "\n".join([f"{p['agent']}: {p['argument']}" for p in state["positions"]])

    prompt = f"""You are Agent A in a debate.
    Topic: {state['topic']}
    Previous arguments: {context}

    Present your position."""

    response = model.invoke(prompt)
    return {
        "positions": [{"agent": "A", "argument": response.content}],
        "round": state["round"] + 1
    }

def agent_b(state: DebateState) -> DebateState:
    """Second debater."""
    context = "\n".join([f"{p['agent']}: {p['argument']}" for p in state["positions"]])

    prompt = f"""You are Agent B in a debate.
    Topic: {state['topic']}
    Previous arguments: {context}

    Present your counterargument."""

    response = model.invoke(prompt)
    return {"positions": [{"agent": "B", "argument": response.content}]}

def judge(state: DebateState) -> DebateState:
    """Judge the debate."""
    context = "\n".join([f"{p['agent']}: {p['argument']}" for p in state["positions"]])

    prompt = f"""You are a judge.
    Topic: {state['topic']}
    Arguments: {context}

    Determine if consensus is reached. If yes, summarize it.
    If no, say "No consensus"."""

    response = model.invoke(prompt)
    consensus = None if "No consensus" in response.content else response.content
    return {"consensus": consensus}

def should_continue_debate(state: DebateState) -> str:
    if state.get("consensus"):
        return END
    if state["round"] >= 5:
        return END
    return "agent_a"

# Build
graph = StateGraph(DebateState)
graph.add_node("agent_a", agent_a)
graph.add_node("agent_b", agent_b)
graph.add_node("judge", judge)

graph.set_entry_point("agent_a")
graph.add_edge("agent_a", "agent_b")
graph.add_edge("agent_b", "judge")
graph.add_conditional_edges("judge", should_continue_debate)

debate = graph.compile()
```

## Pattern 3: Hierarchical Teams

Teams of teams with delegation.

```python
class HierarchicalState(TypedDict):
    task: str
    team: str
    subtasks: list[str]
    results: list[str]
    final_output: str

# Research team
def research_lead(state: HierarchicalState) -> HierarchicalState:
    """Research team lead - delegates to researchers."""
    return {"subtasks": ["search web", "analyze papers", "summarize"]}

research_team = StateGraph(HierarchicalState)
research_team.add_node("lead", research_lead)
research_team.add_node("searcher", searcher_node)
research_team.add_node("analyzer", analyzer_node)
# ... build team

# Engineering team
def eng_lead(state: HierarchicalState) -> HierarchicalState:
    """Engineering team lead."""
    return {"subtasks": ["design", "implement", "test"]}

eng_team = StateGraph(HierarchicalState)
eng_team.add_node("lead", eng_lead)
# ... build team

# Top-level coordinator
def coordinator(state: HierarchicalState) -> HierarchicalState:
    """Coordinate between teams."""
    prompt = f"Which team should handle: {state['task']}? research or engineering"
    response = model.invoke(prompt)
    return {"team": response.content.strip().lower()}

def route_team(state: HierarchicalState) -> str:
    return state["team"]

main = StateGraph(HierarchicalState)
main.add_node("coordinator", coordinator)
main.add_node("research", research_team.compile())
main.add_node("engineering", eng_team.compile())

main.set_entry_point("coordinator")
main.add_conditional_edges(
    "coordinator",
    route_team,
    {"research": "research", "engineering": "engineering"}
)

organization = main.compile()
```

---

# Section 10: Streaming

## Basic Streaming

```python
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4o", streaming=True)

# Stream tokens
for chunk in model.stream("Tell me a story"):
    print(chunk.content, end="", flush=True)
```

## Chain Streaming

```python
chain = prompt | model | parser

# Stream final output
for chunk in chain.stream({"input": "Hello"}):
    print(chunk, end="", flush=True)

# Stream events (more detailed)
async for event in chain.astream_events({"input": "Hello"}, version="v2"):
    if event["event"] == "on_chat_model_stream":
        print(event["data"]["chunk"].content, end="")
```

## LangGraph Streaming

```python
from langgraph.graph import StateGraph

# Stream node outputs
for state in workflow.stream({"input": "Hello"}):
    print(f"Node: {list(state.keys())[0]}")
    print(f"Output: {list(state.values())[0]}")

# Stream with mode
for chunk in workflow.stream(
    {"input": "Hello"},
    stream_mode="values"  # or "updates", "debug"
):
    print(chunk)
```

---

# Section 11: Error Handling

## Retry Logic

```python
from langchain_core.runnables import RunnableRetry
from tenacity import retry, stop_after_attempt, wait_exponential

# Built-in retry
chain_with_retry = chain.with_retry(
    stop_after_attempt=3,
    wait_exponential_jitter=True
)

# Custom retry with tenacity
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10)
)
def robust_invoke(chain, input):
    return chain.invoke(input)
```

## Fallback Chains

```python
from langchain_core.runnables import RunnableWithFallbacks

primary = ChatOpenAI(model="gpt-4o")
fallback_1 = ChatOpenAI(model="gpt-4o-mini")
fallback_2 = ChatOpenAI(model="gpt-3.5-turbo")

robust_model = primary.with_fallbacks([fallback_1, fallback_2])
```

## Exception Handling in Graphs

```python
from langgraph.graph import StateGraph, END

class SafeState(TypedDict):
    input: str
    output: str
    error: str | None

def safe_node(state: SafeState) -> SafeState:
    try:
        result = risky_operation(state["input"])
        return {"output": result}
    except Exception as e:
        return {"error": str(e)}

def error_handler(state: SafeState) -> SafeState:
    """Handle errors gracefully."""
    return {"output": f"Error occurred: {state['error']}"}

def route_on_error(state: SafeState) -> str:
    if state.get("error"):
        return "error_handler"
    return "next_node"

graph = StateGraph(SafeState)
graph.add_node("risky", safe_node)
graph.add_node("error_handler", error_handler)
graph.add_node("next_node", next_node)

graph.add_conditional_edges("risky", route_on_error)
```

---

# Section 12: Best Practices

## Debugging with LangSmith

```python
import os

# Enable tracing
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "ls__..."
os.environ["LANGCHAIN_PROJECT"] = "my-project"

# Add metadata for filtering
chain = prompt | model | parser

result = chain.invoke(
    {"input": "Hello"},
    config={
        "metadata": {"user_id": "123", "feature": "chat"},
        "tags": ["production", "v2"]
    }
)
```

## Cost Optimization

```python
from langchain_community.callbacks import get_openai_callback

# Track costs
with get_openai_callback() as cb:
    result = chain.invoke({"input": "Hello"})
    print(f"Tokens: {cb.total_tokens}")
    print(f"Cost: ${cb.total_cost:.4f}")

# Use cheaper models for simple tasks
cheap_model = ChatOpenAI(model="gpt-4o-mini")
expensive_model = ChatOpenAI(model="gpt-4o")

def select_model(complexity: str):
    if complexity == "simple":
        return cheap_model
    return expensive_model
```

## Testing Agents

```python
import pytest
from unittest.mock import Mock, patch

def test_agent_tool_selection():
    """Test that agent selects correct tool."""
    with patch("langchain_openai.ChatOpenAI") as mock_llm:
        mock_llm.return_value.invoke.return_value = Mock(
            tool_calls=[{"name": "search", "args": {"query": "test"}}]
        )

        result = agent.invoke({"messages": [("human", "Search for test")]})

        assert "search" in str(result)

def test_chain_output_format():
    """Test chain returns expected format."""
    result = chain.invoke({"input": "test"})

    assert isinstance(result, str)
    assert len(result) > 0

# Integration test with real LLM
@pytest.mark.integration
def test_full_workflow():
    """Test complete workflow end-to-end."""
    result = workflow.invoke({"input": "Analyze this data"})

    assert result["final_answer"] is not None
    assert "error" not in result
```

## Latency Reduction

```python
from langchain_core.runnables import RunnableParallel

# Parallel execution
parallel = RunnableParallel({
    "summary": summarize_chain,
    "keywords": extract_keywords_chain,
    "sentiment": sentiment_chain
})

# All three run in parallel
result = parallel.invoke({"text": "Long document..."})

# Caching
from langchain.cache import InMemoryCache
from langchain.globals import set_llm_cache

set_llm_cache(InMemoryCache())

# Use streaming for perceived speed
for chunk in chain.stream({"input": "Hello"}):
    yield chunk
```

---

# Quick Reference

## Chain Types

| Pattern | Use Case | Example |
|---------|----------|---------|
| Sequential | A then B | prompt \| model \| parser |
| Router | Dynamic routing | RunnableBranch |
| MapReduce | Process + combine | Parallel map, then reduce |
| Fallback | Resilience | with_fallbacks() |

## Agent Architectures

| Architecture | Strengths | Use When |
|--------------|-----------|----------|
| ReAct | Simple, debuggable | Basic tool use |
| Plan-and-Execute | Structured | Multi-step tasks |
| LATS | Handles uncertainty | Complex reasoning |

## Memory Types

| Type | Token Cost | Best For |
|------|-----------|----------|
| Buffer | High | Short conversations |
| Summary | Medium | Long conversations |
| Vector | Low per query | Large history |
| Entity | Medium | Entity-focused |

---

# Agents Called

| Agent | Purpose |
|-------|---------|
| faion-autonomous-agent-builder-agent | Build custom LangGraph agents |
| faion-llm-cli-agent | CLI interactions with LangChain |
| faion-rag-agent | RAG with LangChain/LlamaIndex |

---

*faion-langchain-skill v1.0*
*LangChain 0.3.x / LangGraph 0.2.x*
*Covers: chains, agents, memory, tools, multi-agent systems*


---

## Methodologies

| ID | Name | File |
|----|------|------|
| M-LLM-001-prompt-engineering | M-LLM-001-prompt-engineering | [methodologies/M-LLM-001-prompt-engineering.md](methodologies/M-LLM-001-prompt-engineering.md) |
| M-LLM-002-llm-chain-patterns | M-LLM-002-llm-chain-patterns | [methodologies/M-LLM-002-llm-chain-patterns.md](methodologies/M-LLM-002-llm-chain-patterns.md) |
| M-LLM-003-agent-architecture | M-LLM-003-agent-architecture | [methodologies/M-LLM-003-agent-architecture.md](methodologies/M-LLM-003-agent-architecture.md) |
| M-LLM-004-multi-agent-systems | M-LLM-004-multi-agent-systems | [methodologies/M-LLM-004-multi-agent-systems.md](methodologies/M-LLM-004-multi-agent-systems.md) |
| M-LLM-005-function-calling | M-LLM-005-function-calling | [methodologies/M-LLM-005-function-calling.md](methodologies/M-LLM-005-function-calling.md) |
| M-LLM-006-context-window-optimization | M-LLM-006-context-window-optimization | [methodologies/M-LLM-006-context-window-optimization.md](methodologies/M-LLM-006-context-window-optimization.md) |
| M-LLM-007-llm-evaluation | M-LLM-007-llm-evaluation | [methodologies/M-LLM-007-llm-evaluation.md](methodologies/M-LLM-007-llm-evaluation.md) |
| M-LLM-008-cost-optimization | M-LLM-008-cost-optimization | [methodologies/M-LLM-008-cost-optimization.md](methodologies/M-LLM-008-cost-optimization.md) |
