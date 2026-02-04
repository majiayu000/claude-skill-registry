---
name: semantic-kernel
description: Build AI applications with Microsoft Semantic Kernel. Create plugins, planners, and memory systems. Use for enterprise AI, copilot development, and Microsoft ecosystem integrations.
---

# Semantic Kernel

Expert guidance for building AI applications with Microsoft's SDK.

## Triggers

Use this skill when:
- Building enterprise AI applications with Microsoft technologies
- Creating copilot-style AI assistants
- Working with Semantic Kernel plugins, planners, or memory
- Integrating AI into Microsoft ecosystem (Azure, Office, etc.)
- Building modular AI applications with plugin architecture
- Keywords: semantic kernel, microsoft, plugin, planner, memory, copilot, azure ai

## Installation

### Python

```bash
pip install semantic-kernel
```

### .NET

```bash
dotnet add package Microsoft.SemanticKernel
```

## Quick Start (Python)

```python
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion

# Create kernel
kernel = sk.Kernel()

# Add AI service
kernel.add_service(
    OpenAIChatCompletion(
        service_id="chat",
        ai_model_id="gpt-4o",
        api_key="your-key"
    )
)

# Create and invoke prompt
result = await kernel.invoke_prompt("What is the capital of France?")
print(result)
```

## Quick Start (.NET)

```csharp
using Microsoft.SemanticKernel;

var builder = Kernel.CreateBuilder();
builder.AddOpenAIChatCompletion(
    modelId: "gpt-4o",
    apiKey: "your-key"
);

var kernel = builder.Build();

var result = await kernel.InvokePromptAsync("What is the capital of France?");
Console.WriteLine(result);
```

## Plugins

### Semantic Functions (Prompts)

```python
# Python
from semantic_kernel.functions import KernelFunction

summarize = KernelFunction.from_prompt(
    prompt="""Summarize the following text in {{$style}} style:
    {{$input}}

    Summary:""",
    function_name="summarize",
    plugin_name="TextPlugin"
)

kernel.add_function(plugin_name="TextPlugin", function=summarize)

result = await kernel.invoke(
    summarize,
    input="Long text here...",
    style="professional"
)
```

```csharp
// C#
var summarize = kernel.CreateFunctionFromPrompt(
    @"Summarize the following text in {{$style}} style:
    {{$input}}

    Summary:"
);

var result = await kernel.InvokeAsync(summarize, new() {
    ["input"] = "Long text here...",
    ["style"] = "professional"
});
```

### Native Functions

```python
# Python
from semantic_kernel.functions import kernel_function

class MathPlugin:
    @kernel_function(
        name="add",
        description="Add two numbers"
    )
    def add(self, a: int, b: int) -> int:
        return a + b

    @kernel_function(
        name="multiply",
        description="Multiply two numbers"
    )
    def multiply(self, a: int, b: int) -> int:
        return a * b

kernel.add_plugin(MathPlugin(), plugin_name="Math")
result = await kernel.invoke("Math", "add", a=5, b=3)
```

```csharp
// C#
public class MathPlugin
{
    [KernelFunction, Description("Add two numbers")]
    public int Add(int a, int b) => a + b;

    [KernelFunction, Description("Multiply two numbers")]
    public int Multiply(int a, int b) => a * b;
}

kernel.Plugins.AddFromType<MathPlugin>("Math");
var result = await kernel.InvokeAsync("Math", "Add", new() { ["a"] = 5, ["b"] = 3 });
```

### Plugin from Directory

```python
# plugins/WriterPlugin/Summarize/config.json
{
    "schema": 1,
    "description": "Summarize text",
    "execution_settings": {
        "default": {
            "max_tokens": 500,
            "temperature": 0.5
        }
    }
}

# plugins/WriterPlugin/Summarize/skprompt.txt
Summarize: {{$input}}

# Load plugin
kernel.add_plugin(parent_directory="./plugins", plugin_name="WriterPlugin")
```

## Planners

### Function Calling Stepwise Planner

```python
from semantic_kernel.planners import FunctionCallingStepwisePlanner

planner = FunctionCallingStepwisePlanner(service_id="chat")

result = await planner.invoke(
    kernel,
    question="What is 25 * 4 and then add 10?"
)
print(result.final_answer)
```

### Handlebars Planner

```python
from semantic_kernel.planners.handlebars_planner import HandlebarsPlannerOptions, HandlebarsPlanner

planner = HandlebarsPlanner(
    options=HandlebarsPlannerOptions(
        allow_loops=True
    )
)

plan = await planner.create_plan(kernel, goal="Research AI and write summary")
result = await plan.invoke(kernel)
```

## Memory

### Semantic Memory

```python
from semantic_kernel.memory import SemanticTextMemory
from semantic_kernel.connectors.memory.azure_cognitive_search import AzureCognitiveSearchMemoryStore
from semantic_kernel.connectors.ai.open_ai import OpenAITextEmbedding

# Setup embedding
embedding = OpenAITextEmbedding(
    ai_model_id="text-embedding-3-small",
    api_key="your-key"
)

# Setup memory store
memory_store = AzureCognitiveSearchMemoryStore(
    vector_size=1536,
    search_endpoint="https://your-service.search.windows.net",
    admin_key="your-key"
)

memory = SemanticTextMemory(storage=memory_store, embeddings_generator=embedding)

# Save memory
await memory.save_information(
    collection="documents",
    id="doc1",
    text="Important information here",
    description="Description of the information"
)

# Search memory
results = await memory.search(
    collection="documents",
    query="What is important?",
    limit=5
)
```

### Vector Store

```python
from semantic_kernel.connectors.memory.chroma import ChromaMemoryStore

memory_store = ChromaMemoryStore(persist_directory="./chroma_db")
```

## Chat Completion

### Basic Chat

```python
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.contents import ChatHistory

chat_service = kernel.get_service(type=OpenAIChatCompletion)

history = ChatHistory()
history.add_system_message("You are a helpful assistant.")
history.add_user_message("What is Python?")

result = await chat_service.get_chat_message_contents(
    chat_history=history,
    settings=OpenAIChatPromptExecutionSettings(
        max_tokens=500,
        temperature=0.7
    )
)
```

### Streaming

```python
async for chunk in chat_service.get_streaming_chat_message_contents(
    chat_history=history,
    settings=settings
):
    print(chunk[0].content, end="")
```

## Filters

```python
from semantic_kernel.filters import FunctionInvocationContext

@kernel.filter(filter_type=FilterTypes.FUNCTION_INVOCATION)
async def log_filter(context: FunctionInvocationContext, next):
    print(f"Calling: {context.function.name}")
    await next(context)
    print(f"Result: {context.result}")
```

## Azure OpenAI

```python
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion

kernel.add_service(
    AzureChatCompletion(
        service_id="azure-chat",
        deployment_name="gpt-4o",
        endpoint="https://your-resource.openai.azure.com",
        api_key="your-key"
    )
)
```

## Example: Research Assistant

```python
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.functions import kernel_function

# Setup
kernel = sk.Kernel()
kernel.add_service(OpenAIChatCompletion(
    service_id="chat",
    ai_model_id="gpt-4o",
    api_key="your-key"
))

# Define plugins
class ResearchPlugin:
    @kernel_function(description="Search for information")
    def search(self, query: str) -> str:
        return f"Search results for: {query}"

    @kernel_function(description="Summarize text")
    async def summarize(self, text: str, kernel: sk.Kernel) -> str:
        result = await kernel.invoke_prompt(
            f"Summarize this: {text}"
        )
        return str(result)

kernel.add_plugin(ResearchPlugin(), "Research")

# Use with planner
planner = FunctionCallingStepwisePlanner(service_id="chat")
result = await planner.invoke(
    kernel,
    question="Research and summarize AI trends"
)
```

## Resources

- [Semantic Kernel Documentation](https://learn.microsoft.com/semantic-kernel/)
- [Semantic Kernel GitHub](https://github.com/microsoft/semantic-kernel)
- [Samples](https://github.com/microsoft/semantic-kernel/tree/main/samples)
