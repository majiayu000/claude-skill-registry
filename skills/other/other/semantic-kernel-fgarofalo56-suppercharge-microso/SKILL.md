---
name: semantic-kernel
description: Build AI applications with Microsoft Semantic Kernel. Create plugins, planners, memory systems, and AI orchestration. Use for enterprise AI integration, .NET/Python AI development, and LLM application frameworks.
---

# Semantic Kernel

Expert guidance for Microsoft's AI orchestration framework.

## Installation

```bash
# Python
pip install semantic-kernel

# .NET
dotnet add package Microsoft.SemanticKernel
```

## Quick Start

### Python

```python
import asyncio
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion

async def main():
    # Create kernel
    kernel = Kernel()

    # Add AI service
    kernel.add_service(OpenAIChatCompletion(
        service_id="chat",
        ai_model_id="gpt-4o",
        api_key="your-api-key"
    ))

    # Simple completion
    result = await kernel.invoke_prompt("What is the capital of France?")
    print(result)

asyncio.run(main())
```

### .NET

```csharp
using Microsoft.SemanticKernel;

var kernel = Kernel.CreateBuilder()
    .AddOpenAIChatCompletion("gpt-4o", "your-api-key")
    .Build();

var result = await kernel.InvokePromptAsync("What is the capital of France?");
Console.WriteLine(result);
```

## Plugins

### Native Functions (Python)

```python
from semantic_kernel.functions import kernel_function

class MathPlugin:
    @kernel_function(name="add", description="Add two numbers")
    def add(self, a: float, b: float) -> float:
        return a + b

    @kernel_function(name="multiply", description="Multiply two numbers")
    def multiply(self, a: float, b: float) -> float:
        return a * b

    @kernel_function(name="calculate_compound_interest")
    def compound_interest(
        self,
        principal: float,
        rate: float,
        time: float,
        n: int = 12
    ) -> str:
        """Calculate compound interest.

        Args:
            principal: Initial amount
            rate: Annual interest rate (as decimal)
            time: Time in years
            n: Compounding frequency per year
        """
        amount = principal * (1 + rate/n) ** (n * time)
        return f"Final amount: ${amount:.2f}"

# Register plugin
kernel.add_plugin(MathPlugin(), plugin_name="math")

# Invoke
result = await kernel.invoke(
    plugin_name="math",
    function_name="add",
    a=5,
    b=3
)
```

### Native Functions (.NET)

```csharp
public class MathPlugin
{
    [KernelFunction, Description("Add two numbers")]
    public double Add(double a, double b) => a + b;

    [KernelFunction, Description("Multiply two numbers")]
    public double Multiply(double a, double b) => a * b;
}

// Register
kernel.ImportPluginFromType<MathPlugin>();

// Invoke
var result = await kernel.InvokeAsync("MathPlugin", "Add",
    new() { ["a"] = 5, ["b"] = 3 });
```

### Prompt Functions

```python
# Inline prompt
summarize = kernel.add_function(
    plugin_name="text",
    function_name="summarize",
    prompt="""Summarize the following text in 3 sentences:

{{$input}}

Summary:""",
    description="Summarize text"
)

result = await kernel.invoke(summarize, input="Long text here...")
```

```yaml
# prompts/summarize/config.json
{
  "schema": 1,
  "name": "summarize",
  "description": "Summarize text",
  "input_variables": [
    {
      "name": "input",
      "description": "Text to summarize",
      "required": true
    }
  ],
  "execution_settings": {
    "default": {
      "max_tokens": 500,
      "temperature": 0.3
    }
  }
}
```

```
# prompts/summarize/skprompt.txt
Summarize the following text in 3 sentences:

{{$input}}

Summary:
```

```python
# Load from directory
kernel.add_plugin(parent_directory="./prompts", plugin_name="text")
```

## Chat Completion

```python
from semantic_kernel.contents import ChatHistory

chat_history = ChatHistory()
chat_history.add_system_message("You are a helpful assistant.")

async def chat(user_input: str):
    chat_history.add_user_message(user_input)

    result = await kernel.invoke_prompt(
        prompt="{{$chat_history}}{{$user_input}}",
        chat_history=chat_history,
        user_input=user_input
    )

    chat_history.add_assistant_message(str(result))
    return result

response = await chat("Hello, how are you?")
```

## Function Calling

```python
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior

# Enable auto function calling
execution_settings = OpenAIChatPromptExecutionSettings(
    function_choice_behavior=FunctionChoiceBehavior.Auto()
)

# Kernel will automatically call functions when needed
result = await kernel.invoke_prompt(
    "What is 25 multiplied by 4?",
    settings=execution_settings
)
```

## Planners

### Function Calling Stepwise Planner

```python
from semantic_kernel.planners.function_calling_stepwise_planner import (
    FunctionCallingStepwisePlanner,
    FunctionCallingStepwisePlannerOptions
)

planner = FunctionCallingStepwisePlanner(
    service_id="chat",
    options=FunctionCallingStepwisePlannerOptions(
        max_iterations=10,
        max_tokens=4000
    )
)

result = await planner.invoke(
    kernel,
    "Send an email to John about the meeting tomorrow at 3pm"
)
```

### Handlebars Planner

```python
from semantic_kernel.planners.handlebars_planner import HandlebarsPlannerOptions, HandlebarsPlanner

planner = HandlebarsPlanner(
    service_id="chat",
    options=HandlebarsPlannerOptions(
        allow_loops=True
    )
)

plan = await planner.create_plan(kernel, "Research and summarize AI trends")
result = await plan.invoke(kernel)
```

## Memory

### Semantic Memory

```python
from semantic_kernel.memory import SemanticTextMemory
from semantic_kernel.connectors.memory.azure_cognitive_search import AzureCognitiveSearchMemoryStore

# Create memory store
memory_store = AzureCognitiveSearchMemoryStore(
    endpoint="https://search.search.windows.net",
    admin_key="your-key"
)

memory = SemanticTextMemory(
    storage=memory_store,
    embeddings_generator=kernel.get_service("embeddings")
)

# Save memory
await memory.save_information(
    collection="documents",
    id="doc1",
    text="Semantic Kernel is an AI orchestration framework",
    description="SK overview"
)

# Search memory
results = await memory.search(
    collection="documents",
    query="What is Semantic Kernel?",
    limit=5
)
```

### Vector Store

```python
from semantic_kernel.connectors.memory.azure_ai_search import AzureAISearchCollection
from semantic_kernel.data import VectorStoreRecordDefinition

# Define record
@vectorstoremodel
class Document:
    id: Annotated[str, VectorStoreRecordKeyField()]
    content: Annotated[str, VectorStoreRecordDataField()]
    embedding: Annotated[list[float], VectorStoreRecordVectorField(dimensions=1536)]

# Create collection
collection = AzureAISearchCollection(
    record_type=Document,
    collection_name="documents"
)

# Upsert
await collection.upsert(Document(
    id="1",
    content="Important information",
    embedding=await get_embedding("Important information")
))

# Search
results = await collection.vectorized_search(
    vector=query_embedding,
    options=VectorSearchOptions(top=5)
)
```

## Filters

```python
from semantic_kernel.filters import FunctionInvocationContext

@kernel.filter(FilterTypes.FUNCTION_INVOCATION)
async def log_function_calls(
    context: FunctionInvocationContext,
    next: Callable
):
    print(f"Calling: {context.function.name}")
    await next(context)
    print(f"Result: {context.result}")

@kernel.filter(FilterTypes.PROMPT_RENDERING)
async def modify_prompt(context: PromptRenderContext, next: Callable):
    await next(context)
    # Modify rendered prompt if needed
    context.rendered_prompt = context.rendered_prompt.strip()
```

## Azure Services

```python
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion

kernel.add_service(AzureChatCompletion(
    service_id="azure-chat",
    deployment_name="gpt-4o",
    endpoint="https://your-resource.openai.azure.com/",
    api_key="your-key"
))

# Or with Managed Identity
from azure.identity import DefaultAzureCredential

kernel.add_service(AzureChatCompletion(
    service_id="azure-chat",
    deployment_name="gpt-4o",
    endpoint="https://your-resource.openai.azure.com/",
    ad_token_provider=DefaultAzureCredential()
))
```

## Resources

- [Semantic Kernel Documentation](https://learn.microsoft.com/semantic-kernel/)
- [Semantic Kernel GitHub](https://github.com/microsoft/semantic-kernel)
- [SK Samples](https://github.com/microsoft/semantic-kernel/tree/main/samples)
