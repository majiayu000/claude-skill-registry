---
name: LLM Function Calling
description: Implementing function calling (tool use) with LLMs for structured outputs and external integrations.
---

# LLM Function Calling

## Overview

LLM function calling (also known as tool use) enables Large Language Models to interact with external systems by calling predefined functions. Instead of just generating text, the LLM can request to execute specific functions with structured parameters, receive results, and continue reasoning based on those results.

## What is Function Calling (Tool Use)

Function calling allows LLMs to:

1. **Understand Intent**: Recognize when a user request requires external action
2. **Select Tools**: Choose appropriate function(s) to call
3. **Generate Parameters**: Create properly formatted function arguments
4. **Execute Functions**: Run the functions and get results
5. **Process Results**: Use function outputs to answer the user

### Example Flow

```
User: "What's the weather in Tokyo?"
         ↓
LLM: I need to call get_weather function with parameters:
       {"location": "Tokyo"}
         ↓
System: Execute get_weather("Tokyo")
         ↓
Result: {"temperature": 22, "condition": "sunny"}
         ↓
LLM: The weather in Tokyo is sunny with a temperature of 22°C.
```

## OpenAI Function Calling API

### Basic Function Definition

```python
from openai import OpenAI

client = OpenAI()

# Define function
functions = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g., San Francisco, CA"
                    }
                },
                "required": ["location"]
            }
        }
    }
]

# Make request with function calling
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": "What's the weather in Tokyo?"}
    ],
    functions=functions
)

# Check if LLM wants to call a function
if response.choices[0].finish_reason == "function_calls":
    function_call = response.choices[0].message.function_calls[0]
    
    # Execute the function
    if function_call.name == "get_weather":
        args = json.loads(function_call.arguments)
        weather_data = get_weather(args["location"])
        
        # Send result back to LLM
        second_response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": "What's the weather in Tokyo?"},
                response.choices[0].message,  # Assistant message with function call
                {
                    "role": "function",
                    "name": "get_weather",
                    "content": json.dumps(weather_data)
                }
            ]
        )
        
        print(second_response.choices[0].message.content)
```

### Multiple Functions

```python
functions = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string"}
                },
                "required": ["location"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_time",
            "description": "Get the current time",
            "parameters": {
                "type": "object",
                "properties": {
                    "timezone": {
                        "type": "string",
                        "description": "Timezone, e.g., America/New_York"
                    }
                },
                "required": []
            }
        }
    }
]

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": "What's the weather and time in Tokyo?"}
    ],
    functions=functions
)
```

### Streaming with Function Calls

```python
from openai import OpenAI

client = OpenAI()

stream = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": "Calculate 25 * 47"}
    ],
    functions=[{
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Perform mathematical calculations",
            "parameters": {
                "type": "object",
                "properties": {
                    "operation": {
                        "type": "string",
                        "enum": ["add", "subtract", "multiply", "divide"]
                    },
                    "a": {"type": "number"},
                    "b": {"type": "number"}
                },
                "required": ["operation", "a", "b"]
            }
        }
    }],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].finish_reason == "function_calls":
        function_call = chunk.choices[0].delta.function_calls[0]
        # Execute function
        result = execute_function(function_call)
        
        # Continue stream with result
        stream = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": "Calculate 25 * 47"},
                {"role": "assistant", "content": None, "function_calls": [function_call]},
                {"role": "function", "name": function_call.name, "content": json.dumps(result)}
            ],
            stream=True
        )
        for response_chunk in stream:
            print(response_chunk.choices[0].delta.content)
```

## Anthropic Tool Use API

### Basic Tool Definition

```python
import anthropic

client = anthropic.Anthropic()

# Define tools
tools = [
    {
        "name": "get_weather",
        "description": "Get the current weather for a location",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state"
                }
            },
            "required": ["location"]
        }
    }
]

# Make request
message = client.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=1024,
    tools=tools,
    messages=[
        {"role": "user", "content": "What's the weather in Tokyo?"}
    ]
)

# Check for tool use
if message.stop_reason == "tool_use":
    for tool_use in message.content:
        if tool_use.type == "tool_use":
            tool_name = tool_use.name
            tool_input = tool_use.input
            
            # Execute tool
            if tool_name == "get_weather":
                result = get_weather(tool_input["location"])
                
                # Send result back
                response = client.messages.create(
                    model="claude-3-opus-20240229",
                    max_tokens=1024,
                    messages=[
                        {"role": "user", "content": "What's the weather in Tokyo?"},
                        message,  # Assistant message with tool use
                        {
                            "role": "user",
                            "content": f"Tool result: {json.dumps(result)}"
                        }
                    ]
                )
                
                print(response.content[0].text)
```

### Multiple Tools

```python
tools = [
    {
        "name": "search_database",
        "description": "Search the product database",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "category": {"type": "string"}
            },
            "required": ["query"]
        }
    },
    {
        "name": "get_user_profile",
        "description": "Get user profile information",
        "input_schema": {
            "type": "object",
            "properties": {
                "user_id": {"type": "string"}
            },
            "required": ["user_id"]
        }
    }
]

response = client.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=1024,
    tools=tools,
    messages=[
        {"role": "user", "content": "Find running shoes for user 123"}
    ]
)

# Handle multiple tool calls
for content in response.content:
    if content.type == "tool_use":
        tool_name = content.name
        tool_input = content.input
        
        if tool_name == "search_database":
            results = search_products(tool_input["query"], tool_input.get("category"))
        elif tool_name == "get_user_profile":
            results = get_user_profile(tool_input["user_id"])
        
        # Send all results back
        tool_results = [{"type": "tool_result", "tool_use_id": content.id, "content": json.dumps(results)}]
        
        final_response = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": "Find running shoes for user 123"},
                response.content,
                *tool_results
            ]
        )
```

## Function Definition Schemas

### JSON Schema

```python
functions = [
    {
        "type": "function",
        "function": {
            "name": "create_user",
            "description": "Create a new user account",
            "parameters": {
                "type": "object",
                "properties": {
                    "email": {
                        "type": "string",
                        "format": "email",
                        "description": "User's email address"
                    },
                    "password": {
                        "type": "string",
                        "minLength": 8,
                        "description": "User's password (min 8 characters)"
                    },
                    "name": {
                        "type": "string",
                        "minLength": 2,
                        "description": "User's display name"
                    },
                    "age": {
                        "type": "integer",
                        "minimum": 13,
                        "maximum": 120,
                        "description": "User's age"
                    },
                    "subscribe_newsletter": {
                        "type": "boolean",
                        "default": False,
                        "description": "Whether to subscribe to newsletter"
                    }
                },
                "required": ["email", "password", "name"],
                "additionalProperties": False
            }
        }
    }
]
```

### Parameter Descriptions

```python
functions = [
    {
        "type": "function",
        "function": {
            "name": "search_products",
            "description": "Search for products in the catalog",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query - can include product name, category, or keywords"
                    },
                    "category": {
                        "type": "string",
                        "description": "Filter by specific category (optional)",
                        "enum": ["Electronics", "Clothing", "Sports", "Home"]
                    },
                    "min_price": {
                        "type": "number",
                        "description": "Minimum price filter (optional)"
                    },
                    "max_price": {
                        "type": "number",
                        "description": "Maximum price filter (optional)"
                    },
                    "sort_by": {
                        "type": "string",
                        "description": "Sort results by field",
                        "enum": ["price", "name", "rating", "relevance"]
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results to return",
                        "default": 10,
                        "minimum": 1,
                        "maximum": 50
                    }
                },
                "required": ["query"]
            }
        }
    }
]
```

### Required vs Optional

```python
functions = [
    {
        "type": "function",
        "function": {
            "name": "book_flight",
            "description": "Book a flight ticket",
            "parameters": {
                "type": "object",
                "properties": {
                    "origin": {
                        "type": "string",
                        "description": "Departure airport code (e.g., JFK, LAX)"
                    },
                    "destination": {
                        "type": "string",
                        "description": "Destination airport code"
                    },
                    "date": {
                        "type": "string",
                        "description": "Departure date in YYYY-MM-DD format"
                    },
                    "passengers": {
                        "type": "integer",
                        "description": "Number of passengers",
                        "default": 1
                    },
                    "class": {
                        "type": "string",
                        "description": "Flight class",
                        "enum": ["economy", "business", "first"],
                        "default": "economy"
                    }
                },
                "required": ["origin", "destination", "date"]
            }
        }
    }
]
```

## Structured Output Extraction

### Extracting Structured Data

```python
functions = [
    {
        "type": "function",
        "function": {
            "name": "extract_order_info",
            "description": "Extract order information from user message",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_name": {
                        "type": "string",
                        "description": "Name of the product"
                    },
                    "quantity": {
                        "type": "integer",
                        "description": "Quantity to order"
                    },
                    "address": {
                        "type": "string",
                        "description": "Shipping address"
                    },
                    "payment_method": {
                        "type": "string",
                        "description": "Payment method",
                        "enum": ["credit_card", "debit_card", "paypal", "bank_transfer"]
                    }
                },
                "required": []
            }
        }
    }
]

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "Extract order information from the user's message."},
        {"role": "user", "content": "I'd like to order 2 pairs of Nike running shoes to 123 Main St, New York, NY 10001 using my credit card"}
    ],
    functions=functions
)

# Check if function was called
if response.choices[0].finish_reason == "function_calls":
    function_call = response.choices[0].message.function_calls[0]
    args = json.loads(function_call.arguments)
    
    # Process extracted data
    print(f"Product: {args['product_name']}")
    print(f"Quantity: {args['quantity']}")
    print(f"Address: {args['address']}")
    print(f"Payment: {args['payment_method']}")
```

### Data Validation

```python
from pydantic import BaseModel, EmailStr, validator
from typing import Optional

class OrderInfo(BaseModel):
    product_name: str
    quantity: int = 1
    address: str
    payment_method: str
    email: Optional[EmailStr] = None
    notes: Optional[str] = None
    
    @validator('quantity')
    def validate_quantity(cls, v):
        if v < 1 or v > 100:
            raise ValueError('Quantity must be between 1 and 100')
        return v

# Use with function calling
functions = [
    {
        "type": "function",
        "function": {
            "name": "create_order",
            "description": "Create a new order",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_name": {"type": "string"},
                    "quantity": {"type": "integer"},
                    "address": {"type": "string"},
                    "payment_method": {"type": "string"},
                    "email": {"type": "string"},
                    "notes": {"type": "string"}
                },
                "required": ["product_name", "address", "payment_method"]
            }
        }
    }
]

# Validate and process
def process_order(args):
    try:
        order = OrderInfo(**args)
        # Process order
        return {"success": True, "order_id": "12345"}
    except ValueError as e:
        return {"success": False, "error": str(e)}
```

## Multi-Function Calls

### Sequential Function Calls

```python
functions = [
    {
        "type": "function",
        "function": {
            "name": "get_user_balance",
            "description": "Get user's account balance",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string"}
                },
                "required": ["user_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "transfer_money",
            "description": "Transfer money between accounts",
            "parameters": {
                "type": "object",
                "properties": {
                    "from_user_id": {"type": "string"},
                    "to_user_id": {"type": "string"},
                    "amount": {"type": "number"}
                },
                "required": ["from_user_id", "to_user_id", "amount"]
            }
        }
    }
]

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": "Transfer $50 from user 123 to user 456"}
    ],
    functions=functions
)

# Handle multiple function calls
if response.choices[0].finish_reason == "function_calls":
    function_calls = response.choices[0].message.function_calls
    
    # Execute sequentially
    results = []
    for fc in function_calls:
        if fc.name == "get_user_balance":
            balance = get_user_balance(fc.arguments)
            results.append({"function": "get_user_balance", "result": balance})
        elif fc.name == "transfer_money":
            transfer_result = transfer_money(fc.arguments)
            results.append({"function": "transfer_money", "result": transfer_result})
    
    # Send results back
    second_response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": "Transfer $50 from user 123 to user 456"},
            response.choices[0].message,
            *[{
                "role": "function",
                "name": r["function"],
                "content": json.dumps(r["result"])
            } for r in results]
        ]
    )
```

### Parallel Function Calls

```python
functions = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get weather for a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string"}
                },
                "required": ["location"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_time",
            "description": "Get current time",
            "parameters": {
                "type": "object",
                "properties": {
                    "timezone": {"type": "string"}
                },
                "required": []
            }
        }
    }
]

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": "What's the weather and time in Tokyo and New York?"}
    ],
    functions=functions
)

# Handle parallel function calls
if response.choices[0].finish_reason == "function_calls":
    function_calls = response.choices[0].message.function_calls
    
    # Execute in parallel
    import asyncio
    
    async def execute_all(calls):
        tasks = []
        for fc in calls:
            if fc.name == "get_weather":
                task = asyncio.create_task(get_weather(fc.arguments))
            elif fc.name == "get_time":
                task = asyncio.create_task(get_time(fc.arguments))
            tasks.append(task)
        
        results = await asyncio.gather(*tasks)
        return results
    
    results = asyncio.run(execute_all(function_calls))
    
    # Send results back
    second_response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": "What's the weather and time in Tokyo and New York?"},
            response.choices[0].message,
            *[{
                "role": "function",
                "name": fc.name,
                "content": json.dumps(r)
            } for fc, r in zip(function_calls, results)]
        ]
    )
```

## Function Call Routing

### Intelligent Routing

```python
class FunctionRouter:
    def __init__(self):
        self.functions = {
            "weather": self.get_weather,
            "time": self.get_time,
            "database": self.search_database,
            "user": self.get_user,
        }
    
    def route(self, function_name, arguments):
        if function_name in self.functions:
            return self.functions[function_name](arguments)
        else:
            raise ValueError(f"Unknown function: {function_name}")
    
    def get_weather(self, args):
        location = args.get("location")
        return {"temperature": 22, "condition": "sunny"}
    
    def get_time(self, args):
        timezone = args.get("timezone", "UTC")
        return {"time": "2024-01-16 12:00:00", "timezone": timezone}
    
    def search_database(self, args):
        query = args.get("query")
        return {"results": [{"id": 1, "name": "Product 1"}]}
    
    def get_user(self, args):
        user_id = args.get("user_id")
        return {"id": user_id, "name": "John Doe"}

router = FunctionRouter()

# Use with LLM
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": "What's the weather in Tokyo?"}
    ],
    functions=[{
        "type": "function",
        "function": {
            "name": "weather",
            "description": "Get weather",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string"}
                },
                "required": ["location"]
            }
        }
    }]
)

if response.choices[0].finish_reason == "function_calls":
    fc = response.choices[0].message.function_calls[0]
    result = router.route(fc.name, json.loads(fc.arguments))
```

### Dynamic Function Loading

```python
import importlib
import os

class DynamicFunctionLoader:
    def __init__(self, functions_dir="functions"):
        self.functions_dir = functions_dir
        self.loaded_functions = {}
        self.load_functions()
    
    def load_functions(self):
        for filename in os.listdir(self.functions_dir):
            if filename.endswith('.py') and not filename.startswith('_'):
                module_name = filename[:-3]
                try:
                    module = importlib.import_module(f"functions.{module_name}")
                    for attr_name in dir(module):
                        attr = getattr(module, attr_name)
                        if callable(attr) and hasattr(attr, 'tool_definition'):
                            self.loaded_functions[attr.tool_definition['name']] = attr
                except Exception as e:
                    print(f"Failed to load {module_name}: {e}")
    
    def get_function_definitions(self):
        definitions = []
        for name, func in self.loaded_functions.items():
            definitions.append(func.tool_definition)
        return definitions
    
    def execute_function(self, name, arguments):
        if name in self.loaded_functions:
            return self.loaded_functions[name](**arguments)
        else:
            raise ValueError(f"Function not found: {name}")

# Example function module
# functions/weather.py
def get_weather(location: str) -> dict:
    """Get weather for a location"""
    return {"temperature": 22, "condition": "sunny", "location": location}

get_weather.tool_definition = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get the current weather for a location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state"
                }
            },
            "required": ["location"]
        }
    }
}

# Usage
loader = DynamicFunctionLoader()
functions = loader.get_function_definitions()

response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "What's the weather in Tokyo?"}],
    functions=functions
)
```

## Error Handling

### Invalid Function Calls

```python
def safe_execute_function(name, arguments):
    try:
        # Validate function name
        if name not in available_functions:
            return {
                "error": f"Unknown function: {name}",
                "available_functions": list(available_functions.keys())
            }
        
        # Validate arguments
        func_schema = available_functions[name]
        for param in func_schema.get("required", []):
            if param not in arguments:
                return {
                    "error": f"Missing required parameter: {param}",
                    "function": name
                }
        
        # Execute function
        result = available_functions[name]["handler"](**arguments)
        return {"success": True, "result": result}
        
    except Exception as e:
        return {
            "error": str(e),
            "function": name
        }

# Use with LLM response
if response.choices[0].finish_reason == "function_calls":
    fc = response.choices[0].message.function_calls[0]
    args = json.loads(fc.arguments)
    result = safe_execute_function(fc.name, args)
    
    # Send error back to LLM
    if "error" in result:
        second_response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": original_user_message},
                response.choices[0].message,
                {
                    "role": "function",
                    "name": fc.name,
                    "content": json.dumps(result)
                }
            ]
        )
```

### Retry Strategies

```python
import time
from functools import wraps

def retry_on_failure(max_retries=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        time.sleep(delay * (attempt + 1))
            
            raise last_exception
        return wrapper
    return decorator

# Apply to function
@retry_on_failure(max_retries=3, delay=2)
def get_weather(location):
    # May fail occasionally
    return call_weather_api(location)
```

### Fallback Mechanisms

```python
class RobustFunctionExecutor:
    def __init__(self):
        self.functions = {}
        self.fallbacks = {}
    
    def register_function(self, name, handler, fallback=None):
        self.functions[name] = handler
        if fallback:
            self.fallbacks[name] = fallback
    
    def execute(self, name, arguments):
        try:
            return {"success": True, "result": self.functions[name](**arguments)}
        except Exception as e:
            if name in self.fallbacks:
                try:
                    fallback_result = self.fallbacks[name](**arguments)
                    return {
                        "success": True,
                        "result": fallback_result,
                        "warning": f"Primary function failed, used fallback: {str(e)}"
                    }
                except Exception as fe:
                    return {
                        "success": False,
                        "error": f"Both primary and fallback failed: {str(e)}"
                    }
            else:
                return {
                    "success": False,
                    "error": str(e)
                }

# Usage
executor = RobustFunctionExecutor()

executor.register_function(
    "get_weather",
    lambda location: call_weather_api(location),
    lambda location: {"temperature": 20, "condition": "unknown"}  # Fallback
)
```

## Validation and Sanitization

### Input Validation

```python
from pydantic import BaseModel, validator

class WeatherQuery(BaseModel):
    location: str
    
    @validator('location')
    def validate_location(cls, v):
        if len(v) < 2 or len(v) > 100:
            raise ValueError('Location must be 2-100 characters')
        # Sanitize input
        return v.strip().lower()

def safe_weather_handler(args):
    try:
        validated = WeatherQuery(**args)
        return get_weather(validated.location)
    except ValueError as e:
        return {"error": str(e)}
```

### Output Sanitization

```python
def sanitize_output(data):
    """Remove sensitive information from function output"""
    sensitive_keys = ['password', 'ssn', 'credit_card', 'api_key']
    
    sanitized = data.copy()
    for key in sensitive_keys:
        if key in sanitized:
            sanitized[key] = "***REDACTED***"
    
    return sanitized

# Use with function calls
def get_user_profile(user_id):
    user_data = fetch_user_from_db(user_id)
    return sanitize_output(user_data)
```

### Schema Validation

```python
import jsonschema

# Define schema
function_schema = {
    "type": "object",
    "properties": {
        "email": {"type": "string", "format": "email"},
        "age": {"type": "integer", "minimum": 0, "maximum": 120}
    },
    "required": ["email"]
}

def validate_arguments(args, schema):
    try:
        jsonschema.validate(instance=args, schema=schema)
        return {"valid": True}
    except jsonschema.ValidationError as e:
        return {"valid": False, "errors": e.message}

# Use with function calls
if response.choices[0].finish_reason == "function_calls":
    fc = response.choices[0].message.function_calls[0]
    args = json.loads(fc.arguments)
    validation = validate_arguments(args, function_schema)
    
    if not validation["valid"]:
        # Send error back to LLM
        second_response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": original_message},
                response.choices[0].message,
                {
                    "role": "function",
                    "name": fc.name,
                    "content": json.dumps({"error": validation["errors"]})
                }
            ]
        )
```

## Security Considerations

### Input Validation

```python
def validate_function_input(function_name, arguments):
    # Check for SQL injection
    for value in arguments.values():
        if isinstance(value, str):
            dangerous_patterns = ["'", ";", "--", "/*", "xp_"]
            if any(pattern in value.lower() for pattern in dangerous_patterns):
                raise ValueError(f"Potentially dangerous input detected")
    
    # Check for command injection
    dangerous_commands = ["eval(", "exec(", "system(", "__import__"]
    for value in arguments.values():
        if isinstance(value, str):
            if any(cmd in value for cmd in dangerous_commands):
                raise ValueError(f"Command injection attempt detected")
    
    return True
```

### Permission Checks

```python
class SecureFunctionExecutor:
    def __init__(self):
        self.function_permissions = {
            "get_user_data": ["read:users"],
            "update_user": ["write:users"],
            "delete_user": ["delete:users"],
            "admin_functions": ["admin:access"]
        }
        self.user_permissions = set()
    
    def set_user_permissions(self, permissions):
        self.user_permissions = set(permissions)
    
    def check_permission(self, function_name):
        required = self.function_permissions.get(function_name, [])
        if not required:
            return True
        return all(perm in self.user_permissions for perm in required)
    
    def execute(self, function_name, arguments):
        if not self.check_permission(function_name):
            return {
                "error": "Permission denied",
                "required_permissions": self.function_permissions.get(function_name, [])
            }
        
        return execute_function(function_name, arguments)

# Usage
executor = SecureFunctionExecutor()
executor.set_user_permissions(["read:users", "write:users"])

result = executor.execute("get_user_data", {"user_id": "123"})  # Success
result = executor.execute("delete_user", {"user_id": "123"})  # Permission denied
```

### Rate Limiting

```python
from collections import defaultdict
from datetime import datetime, timedelta
import threading

class RateLimiter:
    def __init__(self, max_calls=100, window=timedelta(minutes=1)):
        self.max_calls = max_calls
        self.window = window
        self.calls = defaultdict(list)
        self.lock = threading.Lock()
    
    def check_rate_limit(self, user_id, function_name):
        now = datetime.now()
        key = f"{user_id}:{function_name}"
        
        with self.lock:
            # Remove old calls outside window
            self.calls[key] = [
                call_time for call_time in self.calls[key]
                if now - call_time < self.window
            ]
            
            # Check if limit exceeded
            if len(self.calls[key]) >= self.max_calls:
                return False
            
            # Record this call
            self.calls[key].append(now)
            return True
    
    def record_call(self, user_id, function_name):
        self.check_rate_limit(user_id, function_name)

# Usage
limiter = RateLimiter(max_calls=10, window=timedelta(minutes=1))

def execute_with_rate_limit(user_id, function_name, arguments):
    if not limiter.check_rate_limit(user_id, function_name):
        return {
            "error": "Rate limit exceeded. Please try again later."
        }
    
    return execute_function(function_name, arguments)
```

## Common Patterns

### Database Queries

```python
functions = [
    {
        "type": "function",
        "function": {
            "name": "query_database",
            "description": "Execute a SQL query on the database",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "SQL query to execute"
                    },
                    "params": {
                        "type": "array",
                        "description": "Query parameters"
                    }
                },
                "required": ["query"]
            }
        }
    }
]

def execute_sql_query(query, params):
    # Validate query (only allow SELECT)
    if not query.strip().upper().startswith("SELECT"):
        raise ValueError("Only SELECT queries are allowed")
    
    # Execute with parameterized query
    cursor.execute(query, params)
    return cursor.fetchall()
```

### API Integrations

```python
functions = [
    {
        "type": "function",
        "function": {
            "name": "call_external_api",
            "description": "Make a request to an external API",
            "parameters": {
                "type": "object",
                "properties": {
                    "endpoint": {
                        "type": "string",
                        "description": "API endpoint to call"
                    },
                    "method": {
                        "type": "string",
                        "enum": ["GET", "POST", "PUT", "DELETE"],
                        "default": "GET"
                    },
                    "headers": {
                        "type": "object",
                        "description": "Request headers"
                    },
                    "body": {
                        "type": "object",
                        "description": "Request body (for POST/PUT)"
                    }
                },
                "required": ["endpoint"]
            }
        }
    }
]

def call_external_api(endpoint, method="GET", headers=None, body=None):
    # Whitelist allowed endpoints
    allowed_endpoints = [
        "/api/weather",
        "/api/products",
        "/api/users"
    ]
    
    if not any(endpoint.startswith(prefix) for prefix in allowed_endpoints):
        raise ValueError(f"Endpoint not allowed: {endpoint}")
    
    # Make request
    if method == "GET":
        response = requests.get(endpoint, headers=headers)
    elif method == "POST":
        response = requests.post(endpoint, headers=headers, json=body)
    
    return response.json()
```

### Code Execution

```python
import subprocess
import tempfile
import os

functions = [
    {
        "type": "function",
        "function": {
            "name": "execute_code",
            "description": "Execute Python code in a sandboxed environment",
            "parameters": {
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "Python code to execute"
                    }
                },
                "required": ["code"]
            }
        }
    }
]

def execute_code_safely(code):
    # Validate code
    dangerous_keywords = ["import os", "import subprocess", "exec(", "eval("]
    if any(keyword in code.lower() for keyword in dangerous_keywords):
        raise ValueError("Code contains dangerous keywords")
    
    # Execute in temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(code)
        temp_file = f.name
    
    try:
        # Execute with timeout
        result = subprocess.run(
            ['python', temp_file],
            capture_output=True,
            text=True,
            timeout=10  # 10 second timeout
        )
        
        # Clean up
        os.unlink(temp_file)
        
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }
    except subprocess.TimeoutExpired:
        os.unlink(temp_file)
        return {"error": "Code execution timed out"}
```

### File Operations

```python
import os
import shutil

functions = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read contents of a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "File path to read"
                    },
                    "max_lines": {
                        "type": "integer",
                        "description": "Maximum number of lines to read"
                    }
                },
                "required": ["path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write content to a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "File path to write"
                    },
                    "content": {
                        "type": "string",
                        "description": "Content to write"
                    },
                    "mode": {
                        "type": "string",
                        "enum": ["append", "overwrite"],
                        "default": "overwrite"
                    }
                },
                "required": ["path", "content"]
            }
        }
    }
]

def safe_read_file(path, max_lines=None):
    # Validate path is within allowed directory
    allowed_dir = "/safe/files"
    full_path = os.path.abspath(path)
    
    if not full_path.startswith(os.path.abspath(allowed_dir)):
        raise ValueError("Path outside allowed directory")
    
    # Read file
    with open(full_path, 'r') as f:
        if max_lines:
            lines = []
            for i, line in enumerate(f):
                if i >= max_lines:
                    break
                lines.append(line.rstrip())
            return {"content": "\n".join(lines)}
        else:
            content = f.read()
            return {"content": content}

def safe_write_file(path, content, mode="overwrite"):
    allowed_dir = "/safe/files"
    full_path = os.path.abspath(path)
    
    if not full_path.startswith(os.path.abspath(allowed_dir)):
        raise ValueError("Path outside allowed directory")
    
    if mode == "append":
        with open(full_path, 'a') as f:
            f.write(content + "\n")
    else:
        with open(full_path, 'w') as f:
            f.write(content)
    
    return {"success": True, "path": full_path}
```

## Building AI Agents with Tools

### Tool-Aware Agent

```python
class ToolAwareAgent:
    def __init__(self, llm_client, tools):
        self.client = llm_client
        self.tools = tools
        self.tool_registry = {tool["name"]: tool for tool in tools}
        self.conversation_history = []
    
    def process(self, user_message):
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # Get LLM response
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=self.conversation_history,
            tools=self.tools
        )
        
        assistant_message = response.choices[0].message
        self.conversation_history.append(assistant_message)
        
        # Handle function calls
        if assistant_message.function_calls:
            tool_results = []
            
            for fc in assistant_message.function_calls:
                tool_name = fc.name
                tool_args = json.loads(fc.arguments)
                
                # Execute tool
                tool_result = self.execute_tool(tool_name, tool_args)
                tool_results.append({
                    "role": "tool",
                    "tool_use_id": fc.id,
                    "name": tool_name,
                    "content": json.dumps(tool_result)
                })
            
            # Get final response
            final_response = self.client.chat.completions.create(
                model="gpt-4",
                messages=self.conversation_history + tool_results
            )
            
            self.conversation_history.append(final_response.choices[0].message)
            return final_response.choices[0].message.content
        
        return assistant_message.content
    
    def execute_tool(self, tool_name, arguments):
        tool = self.tool_registry.get(tool_name)
        if not tool:
            raise ValueError(f"Tool not found: {tool_name}")
        
        # Execute tool
        handler = tool.get("handler")
        return handler(**arguments)
```

### Multi-Step Reasoning

```python
class MultiStepAgent:
    def __init__(self, llm_client):
        self.client = llm_client
        self.max_steps = 5
        self.current_step = 0
    
    def process(self, user_message):
        self.current_step = 0
        conversation = [{"role": "user", "content": user_message}]
        
        while self.current_step < self.max_steps:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=conversation,
                tools=self.get_tools()
            )
            
            assistant_message = response.choices[0].message
            conversation.append(assistant_message)
            
            # Check if function calls
            if assistant_message.function_calls:
                # Execute tools
                for fc in assistant_message.function_calls:
                    tool_result = self.execute_tool(fc.name, fc.arguments)
                    conversation.append({
                        "role": "tool",
                        "name": fc.name,
                        "content": json.dumps(tool_result)
                    })
                
                self.current_step += 1
            else:
                # No more function calls, we're done
                break
        
        return conversation[-1]["content"]
    
    def get_tools(self):
        return [
            {
                "type": "function",
                "function": {
                    "name": "search",
                    "description": "Search for information"
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "analyze",
                    "description": "Analyze found information"
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "summarize",
                    "description": "Summarize the analysis"
                }
            }
        ]
```

## Tool Orchestration

### Sequential Orchestration

```python
class ToolOrchestrator:
    def __init__(self):
        self.tools = {}
        self.workflows = {
            "data_analysis": ["search", "analyze", "summarize"],
            "user_lookup": ["get_user", "get_profile", "get_orders"],
            "order_processing": ["check_inventory", "calculate_price", "create_order"]
        }
    
    def register_tool(self, name, handler):
        self.tools[name] = handler
    
    def execute_workflow(self, workflow_name, context):
        if workflow_name not in self.workflows:
            raise ValueError(f"Unknown workflow: {workflow_name}")
        
        workflow = self.workflows[workflow_name]
        results = {}
        
        for tool_name in workflow:
            if tool_name in self.tools:
                results[tool_name] = self.tools[tool_name](context)
        
        return results

# Usage
orchestrator = ToolOrchestrator()
orchestrator.register_tool("search", search_tool)
orchestrator.register_tool("analyze", analyze_tool)
orchestrator.register_tool("summarize", summarize_tool)

results = orchestrator.execute_workflow("data_analysis", {"query": "market trends"})
```

### Parallel Orchestration

```python
import asyncio

class ParallelOrchestrator:
    def __init__(self):
        self.tools = {}
    
    def register_tool(self, name, handler):
        self.tools[name] = handler
    
    async def execute_parallel(self, tool_calls):
        tasks = []
        
        for call in tool_calls:
            if call["name"] in self.tools:
                task = asyncio.create_task(
                    self.tools[call["name"]](**call["arguments"])
                )
                tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        return [
            {
                "name": call["name"],
                "success": not isinstance(result, Exception),
                "result": result if not isinstance(result, Exception) else str(result)
            }
            for call, result in zip(tool_calls, results)
        ]

# Usage
orchestrator = ParallelOrchestrator()
orchestrator.register_tool("get_weather", get_weather)
orchestrator.register_tool("get_time", get_time)

tool_calls = [
    {"name": "get_weather", "arguments": {"location": "Tokyo"}},
    {"name": "get_time", "arguments": {"timezone": "Asia/Tokyo"}}
]

results = asyncio.run(orchestrator.execute_parallel(tool_calls))
```

## Streaming with Function Calls

### Real-Time Tool Execution

```python
from openai import OpenAI

client = OpenAI()

async def streaming_function_call():
    stream = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": "Calculate the sum of 1 through 100"}
        ],
        functions=[{
            "type": "function",
            "function": {
                "name": "calculate_sum",
                "description": "Calculate sum of numbers",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "numbers": {
                            "type": "array",
                            "items": {"type": "integer"},
                            "description": "List of numbers to sum"
                        }
                    },
                    "required": ["numbers"]
                }
            }
        }],
        stream=True
    )
    
    async for chunk in stream:
        if chunk.choices[0].finish_reason == "function_calls":
            fc = chunk.choices[0].delta.function_calls[0]
            
            # Execute function
            args = json.loads(fc.arguments)
            result = calculate_sum(args["numbers"])
            
            # Stream result back
            result_stream = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "user", "content": "Calculate the sum of 1 through 100"},
                    {"role": "assistant", "content": None, "function_calls": [fc]},
                    {
                        "role": "function",
                        "name": fc.name,
                        "content": json.dumps(result)
                    }
                ],
                stream=True
            )
            
            async for result_chunk in result_stream:
                if result_chunk.choices[0].delta.content:
                    print(result_chunk.choices[0].delta.content, end='', flush=True)
```

## Cost Optimization

### Token Usage Monitoring

```python
class TokenTracker:
    def __init__(self):
        self.usage = {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0
        }
    
    def track(self, response):
        if hasattr(response, 'usage'):
            self.usage["prompt_tokens"] += response.usage.prompt_tokens
            self.usage["completion_tokens"] += response.usage.completion_tokens
            self.usage["total_tokens"] += response.usage.total_tokens
    
    def get_stats(self):
        return self.usage

# Usage
tracker = TokenTracker()
tracker.track(response)
print(f"Total tokens used: {tracker.get_stats()['total_tokens']}")
```

### Caching Function Results

```python
from functools import lru_cache
import hashlib

class FunctionCache:
    def __init__(self, ttl=300):
        self.cache = {}
        self.ttl = ttl  # Time to live in seconds
    
    def get_cache_key(self, function_name, arguments):
        key_str = f"{function_name}:{json.dumps(arguments, sort_keys=True)}"
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def get(self, function_name, arguments):
        key = self.get_cache_key(function_name, arguments)
        
        if key in self.cache:
            entry = self.cache[key]
            if time.time() - entry["timestamp"] < self.ttl:
                return {"cached": True, "result": entry["result"]}
            else:
                del self.cache[key]
        
        return None
    
    def set(self, function_name, arguments, result):
        key = self.get_cache_key(function_name, arguments)
        self.cache[key] = {
            "result": result,
            "timestamp": time.time()
        }

# Usage
cache = FunctionCache(ttl=300)

def cached_function_call(function_name, arguments):
    # Check cache
    cached = cache.get(function_name, arguments)
    if cached:
        return cached
    
    # Execute function
    result = execute_function(function_name, arguments)
    
    # Store in cache
    cache.set(function_name, arguments, result)
    
    return {"cached": False, "result": result}
```

### Minimizing Function Calls

```python
def smart_function_selection(user_query, available_functions):
    """Select the most relevant function based on query"""
    query_lower = user_query.lower()
    
    # Score functions based on keyword matching
    scored_functions = []
    for func in available_functions:
        score = 0
        description = func.get("description", "").lower()
        
        # Check for keyword matches
        for keyword in ["weather", "temperature", "forecast"]:
            if keyword in query_lower and keyword in description:
                score += 2
        
        scored_functions.append((score, func))
    
    # Sort by score and return top function
    scored_functions.sort(key=lambda x: x[0], reverse=True)
    
    # Only use top-scoring function
    if scored_functions and scored_functions[0][0] > 0:
        return [scored_functions[0][1]]
    
    return available_functions
```

## Testing Function Calling

### Unit Testing

```python
import pytest
from unittest.mock import Mock, patch

def test_function_calling():
    # Mock the LLM response
    with patch('openai.OpenAI') as mock_openai:
        mock_client = Mock()
        mock_openai.return_value = mock_client
        
        # Mock function call response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message = Mock()
        mock_response.choices[0].message.function_calls = [
            Mock(name="get_weather", arguments='{"location": "Tokyo"}')
        ]
        mock_client.chat.completions.create.return_value = mock_response
        
        # Test
        client = mock_openai()
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": "What's the weather in Tokyo?"}],
            functions=functions
        )
        
        # Assert function call was made
        assert response.choices[0].message.function_calls is not None
        assert response.choices[0].message.function_calls[0].name == "get_weather"
```

### Integration Testing

```python
def test_end_to_end_function_calling():
    # Simulate user interaction
    user_message = "What's the weather in Tokyo?"
    
    # Get LLM response
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": user_message}],
        functions=functions
    )
    
    # Check if function was called
    assert response.choices[0].finish_reason == "function_calls"
    
    # Execute function
    fc = response.choices[0].message.function_calls[0]
    args = json.loads(fc.arguments)
    weather_data = get_weather(args["location"])
    
    # Send result back
    final_response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": user_message},
            response.choices[0].message,
            {
                "role": "function",
                "name": fc.name,
                "content": json.dumps(weather_data)
            }
        ]
    )
    
    # Verify final response
    assert "sunny" in final_response.choices[0].message.content.lower()
```

## Monitoring and Logging

### Function Call Logging

```python
import logging

class FunctionCallLogger:
    def __init__(self):
        self.logger = logging.getLogger('function_calls')
        self.logger.setLevel(logging.INFO)
        
        handler = logging.FileHandler('function_calls.log')
        handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        self.logger.addHandler(handler)
    
    def log_call(self, function_name, arguments, result, duration_ms):
        self.logger.info(
            f"Function: {function_name}, "
            f"Arguments: {arguments}, "
            f"Result: {result}, "
            f"Duration: {duration_ms}ms"
        )
    
    def log_error(self, function_name, arguments, error):
        self.logger.error(
            f"Function: {function_name}, "
            f"Arguments: {arguments}, "
            f"Error: {error}"
        )

# Usage
logger = FunctionCallLogger()

import time
start = time.time()
try:
    result = get_weather("Tokyo")
    logger.log_call("get_weather", {"location": "Tokyo"}, result, (time.time() - start) * 1000)
except Exception as e:
    logger.log_error("get_weather", {"location": "Tokyo"}, str(e))
```

## Best Practices

1. **Function Design**
   - Keep functions focused and single-purpose
   - Use clear, descriptive names
   - Provide detailed parameter descriptions
   - Define required vs optional parameters clearly

2. **Error Handling**
   - Validate all inputs before execution
   - Provide clear error messages
   - Implement retry logic for transient failures
   - Use fallback mechanisms when possible

3. **Security**
   - Validate and sanitize all inputs
   - Implement permission checks
   - Use rate limiting
   - Never expose sensitive data in outputs

4. **Performance**
   - Cache function results when appropriate
   - Use parallel execution when possible
   - Monitor token usage
   - Optimize function execution time

5. **Testing**
   - Unit test individual functions
   - Integration test end-to-end flows
   - Test error scenarios
   - Monitor function call patterns in production

## Related Skills

- `06-ai-ml-production/llm-integration`
- `06-ai-ml-production/prompt-engineering`
- `06-ai-ml-production/agent-patterns`
