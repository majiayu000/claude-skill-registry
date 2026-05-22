---
name: langchain
description: "Build LLM applications with LangChain. Create chains, agents, memory systems, and tool integrations. Use for conversational AI, document QA, and complex LLM orchestration."
---

# LangChain Skill

Complete guide for LangChain - framework for LLM applications.

## Quick Reference

### Core Components
| Component | Description |
|-----------|-------------|
| **LLMs/Chat Models** | Language model interfaces |
| **Prompts** | Template management |
| **Chains** | Composable pipelines |
| **Agents** | Autonomous reasoning |
| **Memory** | Conversation state |
| **Retrievers** | Document retrieval |

---

## 1. Installation

```bash
# Core
pip install langchain langchain-core langchain-community

# LLM providers
pip install langchain-openai
pip install langchain-anthropic
pip install langchain-google-genai

# Vector stores
pip install langchain-chroma
pip install langchain-pinecone

# All common dependencies
pip install langchain[all]
```

---

## 2. Chat Models

### OpenAI
```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.7,
    api_key="your-key"  # or OPENAI_API_KEY env
)

response = llm.invoke("What is LangChain?")
print(response.content)
```

### Anthropic
```python
from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(
    model="claude-3-5-sonnet-20241022",
    temperature=0.7
)

response = llm.invoke("Explain RAG in simple terms")
print(response.content)
```

### Streaming
```python
for chunk in llm.stream("Write a poem about coding"):
    print(chunk.content, end="", flush=True)
```

### Async
```python
import asyncio

async def main():
    response = await llm.ainvoke("Hello!")
    print(response.content)

asyncio.run(main())
```

---

## 3. Prompts

### Basic Templates
```python
from langchain_core.prompts import ChatPromptTemplate

# Simple template
prompt = ChatPromptTemplate.from_template(
    "You are a helpful assistant. Answer this question: {question}"
)

# With messages
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a {role} expert."),
    ("human", "{question}")
])

# Format and invoke
messages = prompt.format_messages(role="Python", question="What is a decorator?")
response = llm.invoke(messages)
```

### Few-Shot Prompts
```python
from langchain_core.prompts import FewShotChatMessagePromptTemplate

examples = [
    {"input": "2+2", "output": "4"},
    {"input": "3*4", "output": "12"},
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

---

## 4. Chains (LCEL)

### Basic Chain
```python
from langchain_core.output_parsers import StrOutputParser

# Chain with pipe operator
chain = prompt | llm | StrOutputParser()

result = chain.invoke({"question": "What is Python?"})
print(result)
```

### Runnable Sequences
```python
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

result = chain.invoke("What is RAG?")
```

### Parallel Execution
```python
from langchain_core.runnables import RunnableParallel

parallel_chain = RunnableParallel(
    summary=prompt1 | llm | StrOutputParser(),
    translation=prompt2 | llm | StrOutputParser()
)

results = parallel_chain.invoke({"text": "Hello world"})
# {'summary': '...', 'translation': '...'}
```

### Branching
```python
from langchain_core.runnables import RunnableBranch

branch = RunnableBranch(
    (lambda x: "code" in x["topic"], code_chain),
    (lambda x: "math" in x["topic"], math_chain),
    default_chain
)
```

---

## 5. Output Parsers

### String Parser
```python
from langchain_core.output_parsers import StrOutputParser

chain = prompt | llm | StrOutputParser()
result = chain.invoke({"question": "Hi"})  # Returns string
```

### JSON Parser
```python
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel

class Answer(BaseModel):
    answer: str
    confidence: float

parser = JsonOutputParser(pydantic_object=Answer)

prompt = ChatPromptTemplate.from_messages([
    ("system", "Answer in JSON format: {format_instructions}"),
    ("human", "{question}")
]).partial(format_instructions=parser.get_format_instructions())

chain = prompt | llm | parser
result = chain.invoke({"question": "What is 2+2?"})
# {'answer': '4', 'confidence': 1.0}
```

### Structured Output
```python
from langchain_core.pydantic_v1 import BaseModel, Field

class MovieReview(BaseModel):
    title: str = Field(description="Movie title")
    rating: int = Field(description="Rating 1-10")
    summary: str = Field(description="Brief summary")

structured_llm = llm.with_structured_output(MovieReview)
result = structured_llm.invoke("Review the movie Inception")
# MovieReview(title='Inception', rating=9, summary='...')
```

---

## 6. RAG (Retrieval-Augmented Generation)

### Document Loading
```python
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    WebBaseLoader,
    DirectoryLoader
)

# PDF
loader = PyPDFLoader("document.pdf")
docs = loader.load()

# Web page
loader = WebBaseLoader("https://example.com")
docs = loader.load()

# Directory
loader = DirectoryLoader("./docs", glob="**/*.md")
docs = loader.load()
```

### Text Splitting
```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\n\n", "\n", " ", ""]
)

chunks = splitter.split_documents(docs)
```

### Vector Store
```python
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

embeddings = OpenAIEmbeddings()

# Create from documents
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db"
)

# Load existing
vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings
)

# Create retriever
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 4}
)
```

### RAG Chain
```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

template = """Answer based on the context:

Context: {context}

Question: {question}

Answer:"""

prompt = ChatPromptTemplate.from_template(template)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

answer = rag_chain.invoke("What is the main topic?")
```

---

## 7. Memory

### Conversation Buffer
```python
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

memory = ConversationBufferMemory()

conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True
)

response1 = conversation.predict(input="Hi, I'm Alice")
response2 = conversation.predict(input="What's my name?")
```

### Message History (LCEL)
```python
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("placeholder", "{history}"),
    ("human", "{input}")
])

chain = prompt | llm

with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history"
)

# Use with session
config = {"configurable": {"session_id": "user123"}}
response = with_history.invoke({"input": "Hi, I'm Bob"}, config=config)
response = with_history.invoke({"input": "What's my name?"}, config=config)
```

---

## 8. Agents

### Tool Definition
```python
from langchain_core.tools import tool

@tool
def search_web(query: str) -> str:
    """Search the web for information."""
    # Implementation
    return f"Results for: {query}"

@tool
def calculator(expression: str) -> str:
    """Calculate mathematical expressions."""
    return str(eval(expression))

tools = [search_web, calculator]
```

### Create Agent
```python
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub

# Get ReAct prompt
prompt = hub.pull("hwchase17/react")

# Create agent
agent = create_react_agent(llm, tools, prompt)

# Create executor
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=5
)

# Run
result = agent_executor.invoke({"input": "What is 25 * 4?"})
```

### Tool Calling Agent
```python
from langchain.agents import create_tool_calling_agent

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("placeholder", "{chat_history}"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])

agent = create_tool_calling_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools)

result = executor.invoke({"input": "Search for LangChain tutorials"})
```

---

## 9. LangGraph

### Basic Graph
```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator

class State(TypedDict):
    messages: Annotated[list, operator.add]
    next: str

def chatbot(state: State):
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

def should_continue(state: State):
    if "DONE" in state["messages"][-1].content:
        return "end"
    return "continue"

# Build graph
workflow = StateGraph(State)
workflow.add_node("chatbot", chatbot)
workflow.set_entry_point("chatbot")
workflow.add_conditional_edges(
    "chatbot",
    should_continue,
    {"continue": "chatbot", "end": END}
)

app = workflow.compile()
result = app.invoke({"messages": [HumanMessage(content="Hello")]})
```

---

## 10. Callbacks & Tracing

### Custom Callbacks
```python
from langchain_core.callbacks import BaseCallbackHandler

class MyHandler(BaseCallbackHandler):
    def on_llm_start(self, serialized, prompts, **kwargs):
        print(f"LLM started with: {prompts}")

    def on_llm_end(self, response, **kwargs):
        print(f"LLM ended with: {response}")

    def on_chain_start(self, serialized, inputs, **kwargs):
        print(f"Chain started")

# Use handler
result = chain.invoke({"question": "Hi"}, config={"callbacks": [MyHandler()]})
```

### LangSmith Tracing
```python
import os
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "your-langsmith-key"
os.environ["LANGCHAIN_PROJECT"] = "my-project"

# All chains now traced automatically
result = chain.invoke({"question": "Hello"})
```

---

## 11. Common Patterns

### Self-Query Retriever
```python
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.chains.query_constructor.base import AttributeInfo

metadata_field_info = [
    AttributeInfo(name="author", description="Author name", type="string"),
    AttributeInfo(name="year", description="Publication year", type="integer"),
]

retriever = SelfQueryRetriever.from_llm(
    llm=llm,
    vectorstore=vectorstore,
    document_contents="Research papers",
    metadata_field_info=metadata_field_info
)

# Natural language query with filtering
docs = retriever.invoke("Papers by Smith from 2023")
```

### Multi-Query Retriever
```python
from langchain.retrievers.multi_query import MultiQueryRetriever

retriever = MultiQueryRetriever.from_llm(
    retriever=vectorstore.as_retriever(),
    llm=llm
)

# Generates multiple query variations
docs = retriever.invoke("What is machine learning?")
```

### Conversational RAG
```python
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

# Contextualize question
contextualize_prompt = ChatPromptTemplate.from_messages([
    ("system", "Reformulate the question given chat history."),
    ("placeholder", "{chat_history}"),
    ("human", "{input}")
])

history_aware_retriever = create_history_aware_retriever(
    llm, retriever, contextualize_prompt
)

# Answer with context
qa_prompt = ChatPromptTemplate.from_messages([
    ("system", "Answer using context:\n\n{context}"),
    ("placeholder", "{chat_history}"),
    ("human", "{input}")
])

qa_chain = create_stuff_documents_chain(llm, qa_prompt)
rag_chain = create_retrieval_chain(history_aware_retriever, qa_chain)

# Use
result = rag_chain.invoke({
    "input": "What is RAG?",
    "chat_history": []
})
```

---

## Best Practices

1. **Use LCEL** - Modern chain composition
2. **Structured output** - Pydantic for reliability
3. **Chunk wisely** - Overlap for context
4. **Test prompts** - Iterate on templates
5. **Handle errors** - Graceful fallbacks
6. **Monitor costs** - Track token usage
7. **Cache embeddings** - Avoid recomputation
8. **Use streaming** - Better UX
9. **Trace with LangSmith** - Debug effectively
10. **Version prompts** - Track changes
