# Function Calling

Function calling lets you connect models to external tools and APIs. Instead of generating text responses, the model determines when to call specific functions and provides the necessary parameters to execute real-world actions.

## Table of Contents

- [Overview](#overview)
- [Basic Usage](#basic-usage)
- [How It Works](#how-it-works)
- [Function Declarations](#function-declarations)
- [Execution Modes](#execution-modes)
- [Automatic Function Calling](#automatic-function-calling)
- [Compositional Function Calling](#compositional-function-calling)
- [Multimodal Function Responses](#multimodal-function-responses)
- [Thinking Models](#thinking-models)
- [MCP Integration](#mcp-integration)
- [Best Practices](#best-practices)

---

## Overview

### Use Cases

| Use Case | Description | Example |
|----------|-------------|---------|
| **Augment Knowledge** | Access external data sources | Databases, APIs, knowledge bases |
| **Extend Capabilities** | Perform computations | Calculators, chart creation, data analysis |
| **Take Actions** | Interact with external systems | Schedule meetings, send emails, control devices |

---

## Basic Usage

### Python

```python
from google import genai
from google.genai import types

# Define the function declaration
schedule_meeting_function = {
    "name": "schedule_meeting",
    "description": "Schedules a meeting with specified attendees at a given time and date.",
    "parameters": {
        "type": "object",
        "properties": {
            "attendees": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of people attending the meeting.",
            },
            "date": {
                "type": "string",
                "description": "Date of the meeting (e.g., '2024-07-29')",
            },
            "time": {
                "type": "string",
                "description": "Time of the meeting (e.g., '15:00')",
            },
            "topic": {
                "type": "string",
                "description": "The subject or topic of the meeting.",
            },
        },
        "required": ["attendees", "date", "time", "topic"],
    },
}

# Configure the client and tools
client = genai.Client()
tools = types.Tool(function_declarations=[schedule_meeting_function])
config = types.GenerateContentConfig(tools=[tools])

# Send request with function declarations
response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="Schedule a meeting with Bob and Alice for 03/14/2025 at 10:00 AM about Q3 planning.",
    config=config,
)

# Check for a function call
if response.candidates[0].content.parts[0].function_call:
    function_call = response.candidates[0].content.parts[0].function_call
    print(f"Function to call: {function_call.name}")
    print(f"Arguments: {function_call.args}")
    # Execute your function here with function_call.args
```

### JavaScript

```javascript
import { GoogleGenAI, Type } from '@google/genai';

const ai = new GoogleGenAI({});

const scheduleMeetingFunction = {
    name: 'schedule_meeting',
    description: 'Schedules a meeting with specified attendees at a given time and date.',
    parameters: {
        type: Type.OBJECT,
        properties: {
            attendees: {
                type: Type.ARRAY,
                items: { type: Type.STRING },
                description: 'List of people attending the meeting.',
            },
            date: {
                type: Type.STRING,
                description: "Date of the meeting (e.g., '2024-07-29')",
            },
            time: {
                type: Type.STRING,
                description: "Time of the meeting (e.g., '15:00')",
            },
            topic: {
                type: Type.STRING,
                description: 'The subject or topic of the meeting.',
            },
        },
        required: ['attendees', 'date', 'time', 'topic'],
    },
};

const response = await ai.models.generateContent({
    model: 'gemini-3-flash-preview',
    contents: 'Schedule a meeting with Bob and Alice for 03/27/2025 at 10:00 AM about Q3 planning.',
    config: {
        tools: [{ functionDeclarations: [scheduleMeetingFunction] }],
    },
});

if (response.functionCalls && response.functionCalls.length > 0) {
    const functionCall = response.functionCalls[0];
    console.log(`Function to call: ${functionCall.name}`);
    console.log(`Arguments: ${JSON.stringify(functionCall.args)}`);
}
```

### REST

```bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "contents": [{
      "role": "user",
      "parts": [{"text": "Schedule a meeting with Bob and Alice for 03/27/2025 at 10:00 AM about Q3 planning."}]
    }],
    "tools": [{
      "functionDeclarations": [{
        "name": "schedule_meeting",
        "description": "Schedules a meeting with specified attendees at a given time and date.",
        "parameters": {
          "type": "object",
          "properties": {
            "attendees": {"type": "array", "items": {"type": "string"}, "description": "List of attendees."},
            "date": {"type": "string", "description": "Date (e.g., 2024-07-29)"},
            "time": {"type": "string", "description": "Time (e.g., 15:00)"},
            "topic": {"type": "string", "description": "Meeting topic"}
          },
          "required": ["attendees", "date", "time", "topic"]
        }
      }]
    }]
  }'
```

---

## How It Works

1. **Define Function Declaration**: Describe the function's name, parameters, and purpose
2. **Call LLM with declarations**: Send user prompt + function declarations to model
3. **Model returns function call**: Model analyzes request and returns structured JSON with function name and args
4. **Execute function (your code)**: Your application executes the function with provided args
5. **Send result back**: Return function result to model for final response

---

## Function Declarations

Define functions using JSON with OpenAPI schema format:

```python
function_declaration = {
    "name": "get_weather",                    # Unique name (use underscores/camelCase)
    "description": "Gets weather for a city", # Clear explanation of purpose
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",             # string, integer, boolean, array
                "description": "City and state, e.g., 'San Francisco, CA'",
            },
            "unit": {
                "type": "string",
                "enum": ["celsius", "fahrenheit"],  # Fixed set of values
                "description": "Temperature unit",
            },
        },
        "required": ["location"],             # Mandatory parameters
    },
}
```

### Parameter Types

| Type | Description |
|------|-------------|
| `string` | Text values |
| `integer` | Whole numbers |
| `number` | Decimal numbers |
| `boolean` | true/false |
| `array` | Lists with `items` type |
| `object` | Nested objects |

### From Python Functions

```python
from google.genai import types

def get_weather(location: str, unit: str = "celsius") -> dict:
    """Gets weather for a location.

    Args:
        location: City and state, e.g., 'San Francisco, CA'
        unit: Temperature unit (celsius or fahrenheit)

    Returns:
        Dictionary with temperature and conditions
    """
    return {"temperature": 22, "conditions": "sunny"}

# Convert Python function to declaration
fn_decl = types.FunctionDeclaration.from_callable(
    callable=get_weather,
    client=client
)
```

---

## Execution Modes

Control when the model calls functions using `tool_config`:

### AUTO (Default)

Model decides whether to call functions or respond directly.

```python
config = types.GenerateContentConfig(
    tools=[tools],
    tool_config=types.ToolConfig(
        function_calling_config=types.FunctionCallingConfig(mode="auto")
    ),
)
```

### ANY

Force the model to always call a function.

```python
config = types.GenerateContentConfig(
    tools=[tools],
    tool_config=types.ToolConfig(
        function_calling_config=types.FunctionCallingConfig(mode="any")
    ),
)
```

### NONE

Disable function calling entirely.

```python
config = types.GenerateContentConfig(
    tools=[tools],
    tool_config=types.ToolConfig(
        function_calling_config=types.FunctionCallingConfig(mode="none")
    ),
)
```

### Allowed Functions

Restrict which functions can be called:

```python
config = types.GenerateContentConfig(
    tools=[tools],
    tool_config=types.ToolConfig(
        function_calling_config=types.FunctionCallingConfig(
            mode="any",
            allowed_function_names=["get_weather", "get_forecast"]
        )
    ),
)
```

---

## Automatic Function Calling

**Python SDK only.** Pass Python functions directly as tools for automatic execution.

```python
from google import genai
from google.genai import types

def set_light_values(brightness: int, color_temp: str) -> dict:
    """Set the brightness and color temperature of a room light.

    Args:
        brightness: Light level from 0 to 100
        color_temp: Color temperature ('daylight', 'cool', 'warm')

    Returns:
        Dictionary with the set values
    """
    return {"brightness": brightness, "color_temp": color_temp}

client = genai.Client()

# Pass function directly - SDK handles execution automatically
response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="Turn the lights down to a romantic level",
    config=types.GenerateContentConfig(
        tools=[set_light_values]  # Pass function directly
    ),
)

print(response.text)
# "I've set the lights to 25% brightness with a warm color temperature."
```

---

## Compositional Function Calling

Chain multiple function calls to fulfill complex requests.

### Python (Manual Loop)

```python
def get_weather_forecast(location: str) -> dict:
    """Gets current weather temperature."""
    print(f"Tool Call: get_weather_forecast(location={location})")
    return {"temperature": 15, "unit": "celsius"}

def set_thermostat_temperature(temperature: int) -> dict:
    """Sets the thermostat."""
    print(f"Tool Call: set_thermostat_temperature(temperature={temperature})")
    return {"status": "success"}

client = genai.Client()
config = types.GenerateContentConfig(
    tools=[get_weather_forecast, set_thermostat_temperature]
)

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="If it's warmer than 20°C in London, set thermostat to 20°C, otherwise 18°C.",
    config=config,
)

print(response.text)
```

### JavaScript (Manual Loop)

```javascript
const toolFunctions = {
    get_weather_forecast: ({ location }) => {
        console.log(`Tool Call: get_weather_forecast(location=${location})`);
        return { temperature: 15, unit: "celsius" };
    },
    set_thermostat_temperature: ({ temperature }) => {
        console.log(`Tool Call: set_thermostat_temperature(temperature=${temperature})`);
        return { status: "success" };
    },
};

let contents = [
    { role: "user", parts: [{ text: "If it's warmer than 20°C in London, set thermostat to 20°C, otherwise 18°C." }] },
];

while (true) {
    const result = await ai.models.generateContent({
        model: "gemini-3-flash-preview",
        contents,
        config: { tools },
    });

    if (result.functionCalls && result.functionCalls.length > 0) {
        const { name, args } = result.functionCalls[0];
        const toolResponse = toolFunctions[name](args);

        // Add model's function call and our response to history
        contents.push({ role: "model", parts: [{ functionCall: result.functionCalls[0] }] });
        contents.push({
            role: "user",
            parts: [{ functionResponse: { name, response: { result: toolResponse } } }],
        });
    } else {
        console.log(result.text);
        break;
    }
}
```

---

## Multimodal Function Responses

Return images or other media in function responses.

### Python

```python
import requests
from google.genai import types

# After receiving functionCall for "get_image"
image_bytes = requests.get("https://example.com/image.jpg").content

function_response_multimodal = types.FunctionResponsePart(
    inline_data=types.FunctionResponseBlob(
        mime_type="image/jpeg",
        display_name="instrument.jpg",
        data=image_bytes,
    )
)

# Include in history
history = [
    types.Content(role="user", parts=[types.Part(text="Show me the instrument I ordered")]),
    response_1.candidates[0].content,
    types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name="get_image",
                response={"image_ref": {"$ref": "instrument.jpg"}},
                parts=[function_response_multimodal]
            )
        ],
    )
]

response_2 = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=history,
    config=types.GenerateContentConfig(tools=[tool_config]),
)
```

---

## Thinking Models

Gemini 3 and 2.5 models use internal "thinking" to improve function calling. They use [thought signatures](https://ai.google.dev/gemini-api/docs/thought-signatures) to maintain context.

**SDK users**: Signatures are handled automatically.

**Manual REST/history management**: Always send `thought_signature` back in its original `Part`.

```json
{
  "role": "model",
  "parts": [{
    "functionCall": {"name": "get_weather", "args": {"location": "London"}},
    "thoughtSignature": "<signature_string>"
  }]
}
```

Rules:
- Always include `thought_signature` in the Part where it appeared
- Don't merge Parts with signatures with Parts without
- Don't merge two Parts that both have signatures

---

## MCP Integration

Model Context Protocol (MCP) provides a standard for connecting to external tools.

### Python

```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from google import genai

client = genai.Client()

server_params = StdioServerParameters(
    command="npx",
    args=["-y", "@philschmid/weather-mcp"],
)

async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            response = await client.aio.models.generate_content(
                model="gemini-2.5-flash",
                contents="What is the weather in London today?",
                config=genai.types.GenerateContentConfig(
                    tools=[session],  # MCP session as tool
                ),
            )
            print(response.text)

asyncio.run(run())
```

### JavaScript

```javascript
import { GoogleGenAI, mcpToTool } from '@google/genai';
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

const transport = new StdioClientTransport({
    command: "npx",
    args: ["-y", "@philschmid/weather-mcp"]
});

const mcpClient = new Client({ name: "example-client", version: "1.0.0" });
await mcpClient.connect(transport);

const ai = new GoogleGenAI({});
const tools = mcpToTool(mcpClient);

const response = await ai.models.generateContent({
    model: "gemini-2.5-flash",
    contents: "What is the weather in London today?",
    config: { tools: [tools] },
});
```

---

## Multi-Tool Use (Live API)

Combine native tools with function calling in Live API:

```python
tools = [
    {'google_search': {}},
    {'code_execution': {}},
    {'function_declarations': [turn_on_lights_schema]}
]

# Use with Live API
await run(prompt, tools=tools, modality="AUDIO")
```

---

## Best Practices

### Function Design

- **Clear descriptions**: Detailed explanations of purpose and parameters
- **Use enums**: For fixed value sets instead of open strings
- **Specific types**: Use appropriate data types for parameters
- **Required vs optional**: Clearly mark required parameters

### Prompt Design

- **Provide context**: Include relevant information in system instructions
- **Handle edge cases**: Guide model behavior for ambiguous requests
- **Low temperature**: Use temperature=0 for deterministic calls (but keep 1.0 for Gemini 3)

### Error Handling

- **Validate calls**: Check `finishReason` for valid function calls
- **Graceful failures**: Return informative error messages
- **User confirmation**: Validate significant actions before executing

### Security

- **Authentication**: Use proper auth for external APIs
- **Avoid sensitive data**: Don't expose credentials in function calls
- **Rate limiting**: Implement limits on function execution

### Token Management

- **Limit functions**: Fewer functions = more tokens for conversation
- **Concise descriptions**: Keep descriptions focused
- **Simplify schemas**: Reduce nesting and property count

---

## Limitations

- Only a subset of OpenAPI schema is supported
- `ANY` mode may reject large/deeply nested schemas
- Automatic function calling is Python SDK only
- Supported Python parameter types are limited

---

## Resources

- [Function Calling Guide](https://ai.google.dev/gemini-api/docs/function-calling)
- [Thought Signatures](https://ai.google.dev/gemini-api/docs/thought-signatures)
- [MCP Documentation](https://modelcontextprotocol.io/introduction)
- [Live API](https://ai.google.dev/gemini-api/docs/live)
