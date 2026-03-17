# LangChain Framework

---
progressive_disclosure:
  entry_point:
    summary: "LLM application framework with chains, agents, RAG, and memory"
    when_to_use:
      - "When building LLM-powered applications"
      - "When implementing RAG (Retrieval Augmented Generation)"
      - "When creating AI agents with tools"
      - "When chaining multiple LLM calls"
    quick_start:
      - "pip install langchain langchain-anthropic"
      - "Set up LLM (ChatAnthropic or ChatOpenAI)"
      - "Create chain with prompts and LLM"
      - "Invoke chain with input"
  token_estimate:
    entry: 85
    full: 5200
---

## Core Concepts

### LangChain Expression Language (LCEL)
Modern composable syntax for building chains with `|` operator.

**Basic Chain**:
```python
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Components
llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")
prompt = ChatPromptTemplate.from_template("Tell me a joke about {topic}")
output_parser = StrOutputParser()

# Compose with LCEL
chain = prompt | llm | output_parser

# Invoke
result = chain.invoke({"topic": "programming"})
```

**Why LCEL**:
- Type safety and auto-completion
- Streaming support built-in
- Async by default
- Observability with LangSmith
- Easier debugging

### Chain Components

**Prompts**:
```python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Simple template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("user", "{input}")
])

# With message history
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    MessagesPlaceholder(variable_name="history"),
    ("user", "{input}")
])

# Few-shot examples
from langchain_core.prompts import FewShotChatMessagePromptTemplate

examples = [
    {"input": "2+2", "output": "4"},
    {"input": "3*5", "output": "15"}
]

example_prompt = ChatPromptTemplate.from_messages([
    ("human", "{input}"),
    ("ai", "{output}")
])

few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=examples
)
```

**LLMs**:
```python
# Anthropic Claude
from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(
    model="claude-3-5-sonnet-20241022",
    temperature=0.7,
    max_tokens=1024,
    timeout=60.0
)

# OpenAI
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-4-turbo-preview",
    temperature=0.7
)

# Streaming
for chunk in llm.stream("Tell me a story"):
    print(chunk.content, end="", flush=True)
```

**Output Parsers**:
```python
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

# String parser
str_parser = StrOutputParser()

# JSON parser
json_parser = JsonOutputParser()

# Structured output
class Person(BaseModel):
    name: str = Field(description="Person's name")
    age: int = Field(description="Person's age")

parser = PydanticOutputParser(pydantic_object=Person)
prompt = ChatPromptTemplate.from_template(
    "Extract person info.\n{format_instructions}\n{query}"
)
chain = prompt | llm | parser
```

## RAG (Retrieval Augmented Generation)

### Document Loading
```python
from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    DirectoryLoader,
    WebBaseLoader
)

# Text files
loader = TextLoader("document.txt")
docs = loader.load()

# PDFs
loader = PyPDFLoader("document.pdf")
docs = loader.load()

# Directory of files
loader = DirectoryLoader(
    "./docs",
    glob="**/*.md",
    show_progress=True
)
docs = loader.load()

# Web pages
loader = WebBaseLoader("https://example.com")
docs = loader.load()
```

### Text Splitting
```python
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
    CharacterTextSplitter,
    TokenTextSplitter
)

# Recursive splitter (recommended)
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
    separators=["\n\n", "\n", " ", ""]
)

chunks = text_splitter.split_documents(docs)

# Token-aware splitting
from langchain.text_splitter import TokenTextSplitter

splitter = TokenTextSplitter(
    chunk_size=512,
    chunk_overlap=50
)
```

### Vector Stores
```python
from langchain_community.vectorstores import Chroma, FAISS, Pinecone
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings

# Embeddings
embeddings = OpenAIEmbeddings()

# Chroma (local, persistent)
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db"
)

# FAISS (local, in-memory)
vectorstore = FAISS.from_documents(
    documents=chunks,
    embedding=embeddings
)
vectorstore.save_local("./faiss_index")

# Pinecone (cloud)
from langchain_community.vectorstores import Pinecone
import pinecone

pinecone.init(api_key="your-key", environment="us-west1-gcp")
vectorstore = Pinecone.from_documents(
    documents=chunks,
    embedding=embeddings,
    index_name="langchain-index"
)
```

### RAG Chain
```python
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Create retriever
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 4}
)

# RAG prompt
template = """Answer based on context:

Context: {context}

Question: {question}

Answer:"""

prompt = ChatPromptTemplate.from_template(template)

# Format documents
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# RAG chain
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# Query
answer = rag_chain.invoke("What is LangChain?")
```

### Advanced RAG Patterns
```python
# Multi-query retrieval
from langchain.retrievers.multi_query import MultiQueryRetriever

retriever = MultiQueryRetriever.from_llm(
    retriever=vectorstore.as_retriever(),
    llm=llm
)

# Contextual compression
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor

compressor = LLMChainExtractor.from_llm(llm)
compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=vectorstore.as_retriever()
)

# Parent document retriever
from langchain.retrievers import ParentDocumentRetriever
from langchain.storage import InMemoryStore

store = InMemoryStore()
retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=store,
    child_splitter=text_splitter
)
```

## Agents and Tools

### Tool Creation
```python
from langchain.tools import tool
from langchain_core.tools import Tool

# Decorator approach
@tool
def search_wikipedia(query: str) -> str:
    """Search Wikipedia for information."""
    # Implementation
    return f"Results for: {query}"

# Class approach
from langchain.tools import BaseTool
from pydantic import BaseModel, Field

class CalculatorInput(BaseModel):
    expression: str = Field(description="Mathematical expression")

class CalculatorTool(BaseTool):
    name = "calculator"
    description = "Useful for math calculations"
    args_schema = CalculatorInput

    def _run(self, expression: str) -> str:
        return str(eval(expression))

# Pre-built tools
from langchain_community.tools import (
    DuckDuckGoSearchRun,
    WikipediaQueryRun,
    PythonREPLTool
)

search = DuckDuckGoSearchRun()
wikipedia = WikipediaQueryRun()
python_repl = PythonREPLTool()
```

### Agent Types
```python
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub

# ReAct agent (recommended)
prompt = hub.pull("hwchase17/react")
tools = [search_wikipedia, CalculatorTool()]

agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=3,
    handle_parsing_errors=True
)

result = agent_executor.invoke({"input": "What is 2+2 and who invented addition?"})

# Structured chat agent (function calling)
from langchain.agents import create_structured_chat_agent

agent = create_structured_chat_agent(llm, tools, prompt)

# OpenAI functions agent
from langchain.agents import create_openai_functions_agent

agent = create_openai_functions_agent(llm, tools, prompt)
```

### Agent with Memory
```python
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True
)

# Conversational loop
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    response = agent_executor.invoke({"input": user_input})
    print(f"Agent: {response['output']}")
```

## Memory Systems

### Memory Types
```python
from langchain.memory import (
    ConversationBufferMemory,
    ConversationBufferWindowMemory,
    ConversationSummaryMemory,
    ConversationSummaryBufferMemory
)

# Full conversation history
memory = ConversationBufferMemory(return_messages=True)

# Last K messages
memory = ConversationBufferWindowMemory(k=5, return_messages=True)

# Summarized history
memory = ConversationSummaryMemory(llm=llm, return_messages=True)

# Summary + recent buffer
memory = ConversationSummaryBufferMemory(
    llm=llm,
    max_token_limit=100,
    return_messages=True
)
```

### Conversation Chain with Memory
```python
from langchain.chains import ConversationChain

conversation = ConversationChain(
    llm=llm,
    memory=ConversationBufferMemory()
)

conversation.predict(input="Hi, I'm Alice")
conversation.predict(input="What's my name?")  # "Alice"

# Custom prompt with memory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

chain = prompt | llm | StrOutputParser()

# Manual memory management
from langchain_core.messages import HumanMessage, AIMessage

history = []

def chat(user_input):
    response = chain.invoke({"input": user_input, "history": history})
    history.append(HumanMessage(content=user_input))
    history.append(AIMessage(content=response))
    return response
```

## Advanced Chain Patterns

### Sequential Chains
```python
from langchain.chains import SequentialChain, LLMChain

# Step 1: Generate synopsis
synopsis_chain = LLMChain(
    llm=llm,
    prompt=ChatPromptTemplate.from_template("Write synopsis for: {title}"),
    output_key="synopsis"
)

# Step 2: Generate review
review_chain = LLMChain(
    llm=llm,
    prompt=ChatPromptTemplate.from_template("Review this synopsis: {synopsis}"),
    output_key="review"
)

# Combine
overall_chain = SequentialChain(
    chains=[synopsis_chain, review_chain],
    input_variables=["title"],
    output_variables=["synopsis", "review"],
    verbose=True
)

result = overall_chain({"title": "AI Revolution"})
```

### Router Chains
```python
from langchain.chains.router import MultiPromptChain
from langchain.chains.router.llm_router import LLMRouterChain, RouterOutputParser

# Define specialized prompts
physics_template = """You are a physics expert. Answer: {input}"""
math_template = """You are a math expert. Answer: {input}"""

prompt_infos = [
    {
        "name": "physics",
        "description": "Good for physics questions",
        "prompt_template": physics_template
    },
    {
        "name": "math",
        "description": "Good for math questions",
        "prompt_template": math_template
    }
]

# Create router
from langchain.chains.router.multi_prompt_prompt import MULTI_PROMPT_ROUTER_TEMPLATE

router_template = MULTI_PROMPT_ROUTER_TEMPLATE.format(destinations="\n".join(
    [f"{p['name']}: {p['description']}" for p in prompt_infos]
))

router_prompt = ChatPromptTemplate.from_template(router_template)
router_chain = LLMRouterChain.from_llm(llm, router_prompt)

# Build multi-prompt chain
chain = MultiPromptChain(
    router_chain=router_chain,
    destination_chains={
        "physics": LLMChain(llm=llm, prompt=ChatPromptTemplate.from_template(physics_template)),
        "math": LLMChain(llm=llm, prompt=ChatPromptTemplate.from_template(math_template))
    },
    default_chain=LLMChain(llm=llm, prompt=ChatPromptTemplate.from_template("{input}")),
    verbose=True
)
```

### Parallel Execution
```python
from langchain_core.runnables import RunnableParallel

# Execute multiple chains in parallel
parallel_chain = RunnableParallel(
    summary=summary_chain,
    translation=translation_chain,
    sentiment=sentiment_chain
)

result = parallel_chain.invoke({"text": "Long article text..."})
# Returns: {"summary": "...", "translation": "...", "sentiment": "..."}
```

## Async Patterns

### Async Chains
```python
import asyncio

# Async invoke
async def process():
    result = await chain.ainvoke({"input": "Hello"})
    return result

# Async streaming
async def stream():
    async for chunk in chain.astream({"input": "Tell me a story"}):
        print(chunk, end="", flush=True)

# Async batch
async def batch():
    results = await chain.abatch([
        {"input": "Question 1"},
        {"input": "Question 2"}
    ])
    return results

# Run
asyncio.run(process())
```

### Concurrent Processing
```python
from langchain_core.runnables import RunnablePassthrough

async def process_documents(docs):
    # Process multiple documents concurrently
    tasks = [chain.ainvoke({"doc": doc}) for doc in docs]
    results = await asyncio.gather(*tasks)
    return results

# With rate limiting
from langchain.callbacks import get_openai_callback

async def process_with_limits(docs, max_concurrent=5):
    semaphore = asyncio.Semaphore(max_concurrent)

    async def process_one(doc):
        async with semaphore:
            return await chain.ainvoke({"doc": doc})

    tasks = [process_one(doc) for doc in docs]
    return await asyncio.gather(*tasks)
```

## LangSmith Tracing

### Setup and Configuration
```python
import os

# Enable LangSmith
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "your-langsmith-key"
os.environ["LANGCHAIN_PROJECT"] = "my-project"

# Trace automatically captures all LangChain operations
result = chain.invoke({"input": "Hello"})
# View trace at: https://smith.langchain.com
```

### Custom Tracing
```python
from langsmith import trace

@trace
def my_function(input_text):
    # Custom function tracing
    result = chain.invoke({"input": input_text})
    return result

# Add metadata
from langchain.callbacks import LangChainTracer

tracer = LangChainTracer(
    project_name="my-project",
    metadata={"environment": "production", "version": "1.0"}
)

chain.invoke({"input": "Hello"}, config={"callbacks": [tracer]})
```

### Evaluation
```python
from langsmith import Client
from langchain.evaluation import load_evaluator

client = Client()

# Create dataset
dataset = client.create_dataset("my-dataset")
client.create_examples(
    inputs=[{"input": "What is AI?"}],
    outputs=[{"output": "Artificial Intelligence..."}],
    dataset_id=dataset.id
)

# Evaluate
def predict(input_dict):
    return chain.invoke(input_dict)

# Run evaluation
results = client.run_on_dataset(
    dataset_name="my-dataset",
    llm_or_chain_factory=lambda: chain,
    evaluation=load_evaluator("qa"),
    project_name="my-evaluation"
)
```

## Production Deployment

### Error Handling
```python
from langchain_core.runnables import RunnableWithFallbacks

# Fallback chain
primary_llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")
fallback_llm = ChatOpenAI(model="gpt-4-turbo-preview")

chain = (prompt | primary_llm).with_fallbacks([prompt | fallback_llm])

# Retry logic
from langchain_core.runnables import RunnableRetry

chain_with_retry = chain.with_retry(
    retry_if_exception_type=(RateLimitError,),
    wait_exponential_jitter=True,
    stop_after_attempt=3
)

# Error handling
try:
    result = chain.invoke({"input": "Hello"})
except Exception as e:
    logger.error(f"Chain failed: {e}")
    # Handle gracefully
```

### Caching
```python
from langchain.cache import InMemoryCache, SQLiteCache
from langchain.globals import set_llm_cache

# In-memory cache
set_llm_cache(InMemoryCache())

# Persistent cache
set_llm_cache(SQLiteCache(database_path=".langchain.db"))

# Redis cache
from langchain.cache import RedisCache
import redis

set_llm_cache(RedisCache(redis_=redis.Redis()))

# Semantic cache
from langchain.cache import RedisSemanticCache
from langchain_openai import OpenAIEmbeddings

set_llm_cache(RedisSemanticCache(
    redis_url="redis://localhost:6379",
    embedding=OpenAIEmbeddings(),
    score_threshold=0.8
))
```

### Rate Limiting
```python
from langchain.llms.base import BaseLLM
from ratelimit import limits, sleep_and_retry

class RateLimitedLLM(BaseLLM):
    @sleep_and_retry
    @limits(calls=50, period=60)  # 50 calls per minute
    def _call(self, prompt, stop=None, **kwargs):
        return self.llm._call(prompt, stop, **kwargs)

# Token budget tracking
from langchain.callbacks import get_openai_callback

with get_openai_callback() as cb:
    result = chain.invoke({"input": "Hello"})
    print(f"Tokens used: {cb.total_tokens}")
    print(f"Cost: ${cb.total_cost}")
```

### Monitoring
```python
from langchain.callbacks.base import BaseCallbackHandler

class MetricsCallback(BaseCallbackHandler):
    def on_llm_start(self, serialized, prompts, **kwargs):
        # Log LLM start
        logger.info(f"LLM started: {prompts}")

    def on_llm_end(self, response, **kwargs):
        # Log LLM completion
        logger.info(f"LLM completed: {response}")

    def on_llm_error(self, error, **kwargs):
        # Log errors
        logger.error(f"LLM error: {error}")

# Use callback
chain.invoke({"input": "Hello"}, config={"callbacks": [MetricsCallback()]})
```

## Best Practices

### Code Organization
```python
# chains.py
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate

def create_summarization_chain():
    llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")
    prompt = ChatPromptTemplate.from_template("Summarize: {text}")
    return prompt | llm

# main.py
from chains import create_summarization_chain

chain = create_summarization_chain()
```

### Environment Configuration
```python
# config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    anthropic_api_key: str
    langsmith_api_key: str | None = None
    langsmith_project: str = "default"
    model_name: str = "claude-3-5-sonnet-20241022"
    temperature: float = 0.7

    class Config:
        env_file = ".env"

settings = Settings()

# Use in chains
llm = ChatAnthropic(
    model=settings.model_name,
    temperature=settings.temperature,
    anthropic_api_key=settings.anthropic_api_key
)
```

### Testing
```python
import pytest
from langchain_core.prompts import ChatPromptTemplate

def test_chain_output():
    # Use mock LLM for testing
    from langchain.llms.fake import FakeListLLM

    llm = FakeListLLM(responses=["Mocked response"])
    prompt = ChatPromptTemplate.from_template("Test: {input}")
    chain = prompt | llm

    result = chain.invoke({"input": "test"})
    assert result == "Mocked response"

# Integration test
@pytest.mark.integration
def test_real_chain():
    chain = create_summarization_chain()
    result = chain.invoke({"text": "Long text..."})
    assert len(result) > 0
```

## Common Pitfalls

### Memory Leaks
```python
# ❌ WRONG: Memory grows unbounded
memory = ConversationBufferMemory()
while True:
    chain.invoke({"input": user_input})  # History never cleared

# ✅ CORRECT: Use windowed memory
memory = ConversationBufferWindowMemory(k=10)
# Or clear periodically
if len(memory.chat_memory.messages) > 100:
    memory.clear()
```

### Inefficient Retrieval
```python
# ❌ WRONG: Retrieving too many documents
retriever = vectorstore.as_retriever(search_kwargs={"k": 100})

# ✅ CORRECT: Optimize k value
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

# ✅ BETTER: Use MMR for diversity
retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 4, "fetch_k": 20}
)
```

### Blocking Async
```python
# ❌ WRONG: Blocking in async context
async def process():
    result = chain.invoke({"input": "test"})  # Blocks event loop

# ✅ CORRECT: Use async methods
async def process():
    result = await chain.ainvoke({"input": "test"})
```

### Unstructured Outputs
```python
# ❌ WRONG: Parsing string outputs
result = chain.invoke({"input": "Extract name and age"})
# Then: parse result string manually

# ✅ CORRECT: Use structured output
from langchain.output_parsers import PydanticOutputParser

parser = PydanticOutputParser(pydantic_object=Person)
chain = prompt | llm | parser
result = chain.invoke({"input": "Extract name and age"})
# Returns: Person(name="John", age=30)
```

### Token Waste
```python
# ❌ WRONG: Sending full context every time
for question in questions:
    chain.invoke({"context": long_document, "question": question})

# ✅ CORRECT: Use RAG retrieval
for question in questions:
    relevant_docs = retriever.get_relevant_documents(question)
    chain.invoke({"context": relevant_docs, "question": question})
```

## Quick Reference

**Installation**:
```bash
pip install langchain langchain-anthropic langchain-openai
pip install chromadb faiss-cpu  # Vector stores
pip install langsmith  # Observability
```

**Essential Imports**:
```python
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
```

**Basic Chain**: `prompt | llm | parser`

**RAG Chain**: `retriever | format_docs | prompt | llm`

**With Memory**: Use `MessagesPlaceholder` in prompt + memory object

**Async**: Replace `invoke` with `ainvoke`, `stream` with `astream`

**Debugging**: Set `verbose=True` or enable LangSmith tracing

**Production**: Add error handling, caching, rate limiting, monitoring