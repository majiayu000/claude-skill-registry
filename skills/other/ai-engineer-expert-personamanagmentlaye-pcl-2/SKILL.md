---
name: ai-engineer-expert
version: 1.0.0
description: Expert-level AI implementation, deployment, LLM integration, and production AI systems
category: ai
tags: [ai-engineering, llm, deployment, production-ai, integration]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash(python:*)
---

# AI Engineer Expert

Expert guidance for implementing AI systems, LLM integration, prompt engineering, and deploying production AI applications.

## Core Concepts

### AI Engineering
- LLM integration and orchestration
- Prompt engineering and optimization
- RAG (Retrieval-Augmented Generation)
- Vector databases and embeddings
- Fine-tuning and adaptation
- AI agent systems

### Production AI
- Model deployment strategies
- API design for AI services
- Rate limiting and cost control
- Error handling and fallbacks
- Monitoring and logging
- Security and safety

### LLM Patterns
- Chain-of-thought prompting
- Few-shot learning
- System/user message design
- Function calling and tools
- Streaming responses
- Context window management

## LLM Integration

```python
from openai import AsyncOpenAI
from anthropic import Anthropic
from typing import List, Dict, Optional
import asyncio

class LLMClient:
    """Unified LLM client with fallback"""

    def __init__(self, primary: str = "openai", fallback: str = "anthropic"):
        self.openai_client = AsyncOpenAI()
        self.anthropic_client = Anthropic()
        self.primary = primary
        self.fallback = fallback

    async def chat_completion(self, messages: List[Dict],
                              model: str = "gpt-4-turbo",
                              temperature: float = 0.7,
                              max_tokens: int = 1000) -> str:
        """Chat completion with fallback"""
        try:
            if self.primary == "openai":
                response = await self.openai_client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                return response.choices[0].message.content

        except Exception as e:
            print(f"Primary provider failed: {e}, trying fallback")

            if self.fallback == "anthropic":
                response = self.anthropic_client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                return response.content[0].text

    async def chat_completion_streaming(self, messages: List[Dict],
                                       model: str = "gpt-4-turbo"):
        """Streaming chat completion"""
        stream = await self.openai_client.chat.completions.create(
            model=model,
            messages=messages,
            stream=True
        )

        async for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    async def function_calling(self, messages: List[Dict],
                              tools: List[Dict]) -> Dict:
        """Function calling with tools"""
        response = await self.openai_client.chat.completions.create(
            model="gpt-4-turbo",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        message = response.choices[0].message

        if message.tool_calls:
            return {
                "type": "function_call",
                "function": message.tool_calls[0].function.name,
                "arguments": message.tool_calls[0].function.arguments
            }
        else:
            return {
                "type": "message",
                "content": message.content
            }
```

## RAG Implementation

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI

class RAGSystem:
    """Retrieval-Augmented Generation system"""

    def __init__(self, persist_directory: str = "./chroma_db"):
        self.embeddings = OpenAIEmbeddings()
        self.vectorstore = None
        self.persist_directory = persist_directory
        self.llm = ChatOpenAI(model="gpt-4-turbo", temperature=0)

    def ingest_documents(self, documents: List[str]):
        """Ingest and index documents"""
        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        chunks = text_splitter.create_documents(documents)

        # Create vector store
        self.vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory=self.persist_directory
        )

    def query(self, question: str, k: int = 4) -> Dict:
        """Query with RAG"""
        if not self.vectorstore:
            raise ValueError("No documents ingested")

        # Retrieve relevant documents
        retriever = self.vectorstore.as_retriever(
            search_kwargs={"k": k}
        )

        # Create QA chain
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True
        )

        # Get answer
        result = qa_chain({"query": question})

        return {
            "answer": result["result"],
            "sources": [doc.page_content for doc in result["source_documents"]]
        }

    def similarity_search(self, query: str, k: int = 4) -> List[Dict]:
        """Similarity search in vector database"""
        results = self.vectorstore.similarity_search_with_score(query, k=k)

        return [
            {
                "content": doc.page_content,
                "score": score,
                "metadata": doc.metadata
            }
            for doc, score in results
        ]
```

## Prompt Engineering

```python
class PromptTemplate:
    """Advanced prompt templates"""

    @staticmethod
    def chain_of_thought(question: str) -> str:
        """Chain-of-thought prompting"""
        return f"""Let's solve this step by step:

Question: {question}

Please think through this problem carefully:
1. First, identify what we need to find
2. Then, break down the problem into smaller steps
3. Solve each step
4. Finally, combine the results

Your step-by-step solution:"""

    @staticmethod
    def few_shot(task: str, examples: List[Dict], query: str) -> str:
        """Few-shot learning prompt"""
        examples_text = "\n\n".join([
            f"Input: {ex['input']}\nOutput: {ex['output']}"
            for ex in examples
        ])

        return f"""Task: {task}

Here are some examples:

{examples_text}

Now, please solve this:

Input: {query}
Output:"""

    @staticmethod
    def system_message(role: str, constraints: List[str],
                       format_instructions: str) -> str:
        """System message template"""
        constraints_text = "\n".join([f"- {c}" for c in constraints])

        return f"""You are a {role}.

Constraints:
{constraints_text}

Output Format:
{format_instructions}

Remember to follow these guidelines strictly."""
```

## AI Agent System

```python
from typing import Callable
import json

class Tool:
    """Tool that agents can use"""

    def __init__(self, name: str, description: str, function: Callable):
        self.name = name
        self.description = description
        self.function = function

    def to_openai_function(self) -> Dict:
        """Convert to OpenAI function format"""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.get_parameters()
            }
        }

class AIAgent:
    """AI agent with tools"""

    def __init__(self, llm_client: LLMClient, tools: List[Tool]):
        self.llm = llm_client
        self.tools = {tool.name: tool for tool in tools}
        self.conversation_history = []

    async def run(self, user_input: str, max_iterations: int = 10) -> str:
        """Run agent with tool use"""
        self.conversation_history.append({
            "role": "user",
            "content": user_input
        })

        for i in range(max_iterations):
            # Get LLM response with function calling
            response = await self.llm.function_calling(
                messages=self.conversation_history,
                tools=[tool.to_openai_function() for tool in self.tools.values()]
            )

            if response["type"] == "message":
                # Agent is done
                return response["content"]

            # Execute tool
            tool_name = response["function"]
            arguments = json.loads(response["arguments"])

            tool_result = await self.execute_tool(tool_name, arguments)

            # Add tool result to conversation
            self.conversation_history.append({
                "role": "function",
                "name": tool_name,
                "content": str(tool_result)
            })

        return "Max iterations reached"

    async def execute_tool(self, tool_name: str, arguments: Dict) -> any:
        """Execute a tool"""
        if tool_name not in self.tools:
            raise ValueError(f"Tool {tool_name} not found")

        tool = self.tools[tool_name]
        return await tool.function(**arguments)
```

## Production Deployment

```python
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from circuitbreaker import circuit
import asyncio

app = FastAPI()

class ChatRequest(BaseModel):
    messages: List[Dict]
    model: str = "gpt-4-turbo"
    stream: bool = False

class RateLimiter:
    """Rate limiter for API"""

    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = {}

    async def check_limit(self, user_id: str) -> bool:
        """Check if user is within rate limit"""
        import time
        now = time.time()

        if user_id not in self.requests:
            self.requests[user_id] = []

        # Remove old requests
        self.requests[user_id] = [
            req_time for req_time in self.requests[user_id]
            if now - req_time < self.window_seconds
        ]

        if len(self.requests[user_id]) >= self.max_requests:
            return False

        self.requests[user_id].append(now)
        return True

rate_limiter = RateLimiter(max_requests=100, window_seconds=60)
llm_client = LLMClient()

@circuit(failure_threshold=5, recovery_timeout=60)
async def call_llm(messages: List[Dict]) -> str:
    """LLM call with circuit breaker"""
    return await llm_client.chat_completion(messages)

@app.post("/chat")
async def chat(request: ChatRequest, user_id: str = Depends(get_user_id)):
    """Chat endpoint with rate limiting"""
    # Check rate limit
    if not await rate_limiter.check_limit(user_id):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    try:
        if request.stream:
            async def generate():
                async for chunk in llm_client.chat_completion_streaming(request.messages):
                    yield chunk

            return StreamingResponse(generate(), media_type="text/event-stream")
        else:
            response = await call_llm(request.messages)
            return {"response": response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

## Best Practices

### LLM Integration
- Implement fallback providers
- Use streaming for better UX
- Cache responses where appropriate
- Handle rate limits gracefully
- Monitor token usage and costs
- Version prompts and track changes

### Production Systems
- Implement circuit breakers
- Add comprehensive logging
- Monitor latency and errors
- Use rate limiting
- Implement retry logic with backoff
- Test edge cases thoroughly

### Security
- Validate and sanitize inputs
- Implement authentication/authorization
- Never expose API keys in logs
- Use environment variables for secrets
- Implement content filtering
- Monitor for prompt injection

## Anti-Patterns

❌ No error handling or fallbacks
❌ Exposing raw LLM outputs without validation
❌ No rate limiting or cost controls
❌ Storing API keys in code
❌ No monitoring or logging
❌ Ignoring token limits
❌ No testing of prompts

## Resources

- OpenAI API: https://platform.openai.com/docs
- Anthropic Claude: https://docs.anthropic.com/
- LangChain: https://python.langchain.com/
- LlamaIndex: https://www.llamaindex.ai/
- Weights & Biases Prompts: https://wandb.ai/site/prompts
