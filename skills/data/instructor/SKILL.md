---
name: instructor
description: Structured outputs with Instructor. Extract typed data from LLMs using Pydantic models and validation. Use for data extraction, structured generation, and type-safe LLM responses.
---

# Instructor

Expert guidance for structured LLM outputs with Pydantic validation.

## Triggers

Use this skill when:
- Extracting structured data from LLM responses
- Building type-safe LLM applications
- Validating LLM outputs with Pydantic
- Implementing data extraction pipelines
- Working with structured generation
- Keywords: instructor, structured output, pydantic, data extraction, validation, typed responses

## Installation

```bash
pip install instructor
```

## Quick Start

```python
import instructor
from pydantic import BaseModel
from openai import OpenAI

# Patch OpenAI client
client = instructor.from_openai(OpenAI())

class User(BaseModel):
    name: str
    age: int

# Extract structured data
user = client.chat.completions.create(
    model="gpt-4o",
    response_model=User,
    messages=[
        {"role": "user", "content": "John is 25 years old"}
    ]
)

print(user)  # User(name='John', age=25)
```

## Pydantic Models

### Basic Models

```python
from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Task(BaseModel):
    title: str = Field(description="Task title")
    description: str = Field(description="Detailed description")
    priority: Priority = Field(description="Task priority level")
    due_date: Optional[str] = Field(None, description="Due date in YYYY-MM-DD format")
    tags: List[str] = Field(default_factory=list, description="Related tags")

task = client.chat.completions.create(
    model="gpt-4o",
    response_model=Task,
    messages=[
        {"role": "user", "content": "Create a task for reviewing the Q4 report, high priority, due next Friday"}
    ]
)
```

### Nested Models

```python
from pydantic import BaseModel
from typing import List

class Address(BaseModel):
    street: str
    city: str
    country: str
    postal_code: str

class Person(BaseModel):
    name: str
    email: str
    address: Address
    phone_numbers: List[str]

person = client.chat.completions.create(
    model="gpt-4o",
    response_model=Person,
    messages=[
        {"role": "user", "content": """
        Extract: John Smith, john@email.com, lives at 123 Main St,
        New York, USA 10001. Phone: 555-1234, 555-5678
        """}
    ]
)
```

## Validation

### Field Validators

```python
from pydantic import BaseModel, field_validator
from typing import List

class SearchQuery(BaseModel):
    query: str
    filters: List[str]

    @field_validator('query')
    @classmethod
    def query_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Query cannot be empty")
        return v.strip()

    @field_validator('filters')
    @classmethod
    def validate_filters(cls, v):
        valid = ["date", "author", "category"]
        for f in v:
            if f not in valid:
                raise ValueError(f"Invalid filter: {f}")
        return v
```

### Model Validators

```python
from pydantic import BaseModel, model_validator

class DateRange(BaseModel):
    start_date: str
    end_date: str

    @model_validator(mode='after')
    def validate_dates(self):
        if self.start_date > self.end_date:
            raise ValueError("Start date must be before end date")
        return self
```

## Retries

```python
from instructor import from_openai
from tenacity import retry, stop_after_attempt

client = from_openai(
    OpenAI(),
    mode=instructor.Mode.TOOLS
)

# Automatic retries on validation failure
user = client.chat.completions.create(
    model="gpt-4o",
    response_model=User,
    max_retries=3,
    messages=[{"role": "user", "content": "Extract user info"}]
)
```

## Streaming

```python
from instructor import from_openai, Partial
from pydantic import BaseModel
from typing import List

class Report(BaseModel):
    title: str
    sections: List[str]
    summary: str

client = from_openai(OpenAI())

# Stream partial results
for partial in client.chat.completions.create_partial(
    model="gpt-4o",
    response_model=Report,
    messages=[{"role": "user", "content": "Write a report on AI trends"}],
):
    print(partial)  # Partial[Report] with available fields
```

## Iterable Extraction

```python
from instructor import from_openai
from pydantic import BaseModel
from typing import Iterable

class Product(BaseModel):
    name: str
    price: float
    category: str

client = from_openai(OpenAI())

products: Iterable[Product] = client.chat.completions.create_iterable(
    model="gpt-4o",
    response_model=Product,
    messages=[
        {"role": "user", "content": """
        Extract products:
        - iPhone 15 Pro: $999, Electronics
        - Nike Air Max: $150, Footwear
        - MacBook Pro: $2499, Electronics
        """}
    ]
)

for product in products:
    print(product)
```

## Multiple Providers

### Anthropic

```python
import instructor
from anthropic import Anthropic

client = instructor.from_anthropic(Anthropic())

user = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    response_model=User,
    messages=[{"role": "user", "content": "John is 25"}]
)
```

### Ollama

```python
import instructor
from openai import OpenAI

client = instructor.from_openai(
    OpenAI(base_url="http://localhost:11434/v1", api_key="ollama"),
    mode=instructor.Mode.JSON
)

user = client.chat.completions.create(
    model="llama3.1",
    response_model=User,
    messages=[{"role": "user", "content": "John is 25"}]
)
```

### LiteLLM

```python
import instructor
import litellm

client = instructor.from_litellm(litellm.completion)

user = client(
    model="gpt-4o",
    response_model=User,
    messages=[{"role": "user", "content": "John is 25"}]
)
```

## Advanced Patterns

### Chain of Thought

```python
from pydantic import BaseModel, Field

class Reasoning(BaseModel):
    chain_of_thought: str = Field(
        description="Step by step reasoning before the answer"
    )
    answer: str = Field(description="Final answer")

result = client.chat.completions.create(
    model="gpt-4o",
    response_model=Reasoning,
    messages=[
        {"role": "user", "content": "What is 25 * 47?"}
    ]
)
print(result.chain_of_thought)
print(result.answer)
```

### Classification

```python
from enum import Enum, auto

class Sentiment(str, Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"

class SentimentAnalysis(BaseModel):
    text: str
    sentiment: Sentiment
    confidence: float = Field(ge=0, le=1)

analysis = client.chat.completions.create(
    model="gpt-4o",
    response_model=SentimentAnalysis,
    messages=[
        {"role": "user", "content": "Analyze: 'I love this product!'"}
    ]
)
```

## Resources

- [Instructor Documentation](https://python.useinstructor.com/)
- [Instructor GitHub](https://github.com/jxnl/instructor)
- [Examples](https://python.useinstructor.com/examples/)
