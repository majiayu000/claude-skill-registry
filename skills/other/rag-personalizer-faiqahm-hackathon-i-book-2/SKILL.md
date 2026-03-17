---
name: rag-personalizer
description: |
  Transform textbook content based on the 10-dimension user profile to provide personalized learning experiences.
  Agent: AIEngineer
version: 1.0.0
inputs:
  openai_api_key:
    description: OpenAI API key for content transformation
    required: true
    example: "sk-..."
  qdrant_url:
    description: Qdrant Cloud cluster URL (for RAG retrieval)
    required: false
    example: "https://xxx.qdrant.io"
  qdrant_api_key:
    description: Qdrant API key
    required: false
    example: "your-api-key"
  model:
    description: OpenAI model for personalization
    required: false
    default: "gpt-4o-mini"
    example: "gpt-4o"
---

# RAG Personalizer

**Agent:** AIEngineer

Transform textbook content based on a 10-dimension user profile to provide personalized learning experiences. This skill takes RAG-retrieved content and adapts it to match individual learner preferences, knowledge level, and learning style.

## Quick Setup

```bash
# Set environment variables
export OPENAI_API_KEY="sk-..."
export QDRANT_URL="https://xxx.qdrant.io"  # Optional
export QDRANT_API_KEY="your-api-key"       # Optional

# Create a user profile
.claude/skills/rag-personalizer/scripts/setup.sh --create-profile user123

# Personalize content for a query
.claude/skills/rag-personalizer/scripts/setup.sh --personalize "What is ROS 2?" --profile user123

# Update profile dimensions
.claude/skills/rag-personalizer/scripts/setup.sh --update-profile user123 --dimension learning_style --value visual
```

## The 10-Dimension User Profile

| # | Dimension | Options | Default |
|---|-----------|---------|---------|
| 1 | `learning_style` | visual, auditory, kinesthetic, reading | reading |
| 2 | `knowledge_level` | beginner, intermediate, advanced | beginner |
| 3 | `learning_pace` | slow, moderate, fast | moderate |
| 4 | `language` | en, ur | en |
| 5 | `content_depth` | overview, standard, deep-dive | standard |
| 6 | `example_preference` | theoretical, practical, code-heavy | practical |
| 7 | `difficulty_tolerance` | easy, moderate, challenging | moderate |
| 8 | `interaction_style` | passive, interactive, hands-on | interactive |
| 9 | `time_availability` | limited, moderate, extensive | moderate |
| 10 | `goal_orientation` | certification, understanding, application | understanding |

## Command Options

| Option | Description | Default |
|--------|-------------|---------|
| `--create-profile ID` | Create a new user profile | - |
| `--update-profile ID` | Update an existing profile | - |
| `--get-profile ID` | Get profile details | - |
| `--delete-profile ID` | Delete a profile | - |
| `--list-profiles` | List all profiles | - |
| `--personalize QUERY` | Personalize content for query | - |
| `--profile ID` | Profile ID to use | `default` |
| `--dimension DIM` | Dimension to update | - |
| `--value VAL` | Value for dimension | - |
| `--content TEXT` | Direct content to personalize | - |
| `--model MODEL` | OpenAI model | `gpt-4o-mini` |
| `--output FORMAT` | Output format (text, json, markdown) | `markdown` |
| `-h, --help` | Show help message | - |

## What It Does

### 1. Profile Management

Creates and manages learner profiles with 10 configurable dimensions:

```json
{
  "id": "user123",
  "created_at": "2026-01-02T12:00:00Z",
  "dimensions": {
    "learning_style": "visual",
    "knowledge_level": "beginner",
    "learning_pace": "moderate",
    "language": "en",
    "content_depth": "standard",
    "example_preference": "practical",
    "difficulty_tolerance": "easy",
    "interaction_style": "interactive",
    "time_availability": "moderate",
    "goal_orientation": "understanding"
  }
}
```

### 2. Content Personalization

Transforms RAG-retrieved content based on profile dimensions:

```python
# Example transformation for visual learner
Original: "ROS 2 uses a publish-subscribe pattern..."
Personalized: "ROS 2 uses a publish-subscribe pattern...

📊 **Visual Diagram:**
┌─────────┐    publish    ┌─────────┐    subscribe    ┌─────────┐
│ Node A  │ ─────────────▶│  Topic  │◀─────────────── │ Node B  │
└─────────┘               └─────────┘                 └─────────┘
"
```

### 3. Adaptive Strategies by Dimension

| Dimension | Adaptation Strategy |
|-----------|---------------------|
| **learning_style=visual** | Add diagrams, flowcharts, color coding |
| **learning_style=auditory** | Add pronunciation guides, verbal explanations |
| **learning_style=kinesthetic** | Add hands-on exercises, step-by-step tutorials |
| **knowledge_level=beginner** | Simplify jargon, add definitions, more examples |
| **knowledge_level=advanced** | Skip basics, add edge cases, performance tips |
| **content_depth=overview** | Summarize, bullet points, key takeaways |
| **content_depth=deep-dive** | Add technical details, internals, references |
| **example_preference=code-heavy** | Add code snippets, implementations |
| **language=ur** | Translate content, use RTL formatting |

### 4. Integration with RAG

Works with `qdrant-manager` for end-to-end personalized retrieval:

```python
from rag_personalizer import Personalizer
from vectorize import QdrantManager

# Retrieve relevant content
qdrant = QdrantManager()
results = qdrant.query("What is ROS 2?", language="en")

# Personalize for user
personalizer = Personalizer()
profile = personalizer.get_profile("user123")
personalized = personalizer.personalize(
    content=results[0]['content'],
    profile=profile
)
```

## Bundled Resources

### 1. Python Dependencies

**File**: `requirements.txt`

```
openai>=1.0.0
pydantic>=2.0.0
python-dotenv>=1.0.0
rich>=13.0.0
```

### 2. Profile Schema

**File**: `assets/profile_schema.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["id", "dimensions"],
  "properties": {
    "id": { "type": "string" },
    "created_at": { "type": "string", "format": "date-time" },
    "updated_at": { "type": "string", "format": "date-time" },
    "dimensions": {
      "type": "object",
      "properties": {
        "learning_style": { "enum": ["visual", "auditory", "kinesthetic", "reading"] },
        "knowledge_level": { "enum": ["beginner", "intermediate", "advanced"] },
        "learning_pace": { "enum": ["slow", "moderate", "fast"] },
        "language": { "enum": ["en", "ur"] },
        "content_depth": { "enum": ["overview", "standard", "deep-dive"] },
        "example_preference": { "enum": ["theoretical", "practical", "code-heavy"] },
        "difficulty_tolerance": { "enum": ["easy", "moderate", "challenging"] },
        "interaction_style": { "enum": ["passive", "interactive", "hands-on"] },
        "time_availability": { "enum": ["limited", "moderate", "extensive"] },
        "goal_orientation": { "enum": ["certification", "understanding", "application"] }
      }
    }
  }
}
```

### 3. Personalization Prompts

**File**: `assets/prompts.json`

```json
{
  "base_system": "You are an expert educational content adapter. Transform the given content to match the learner's profile while preserving accuracy.",
  "dimension_instructions": {
    "learning_style": {
      "visual": "Add diagrams, flowcharts, and visual representations using ASCII art or markdown.",
      "auditory": "Add phonetic guides, emphasize rhythm in explanations, suggest audio resources.",
      "kinesthetic": "Add hands-on exercises, physical analogies, and step-by-step activities.",
      "reading": "Maintain text-based format, add references, use clear paragraph structure."
    },
    "knowledge_level": {
      "beginner": "Define all technical terms, use simple analogies, provide foundational context.",
      "intermediate": "Assume basic knowledge, focus on application, add moderate complexity.",
      "advanced": "Skip fundamentals, discuss edge cases, performance implications, best practices."
    },
    "content_depth": {
      "overview": "Provide a concise summary with bullet points and key takeaways only.",
      "standard": "Balance detail and brevity, include examples and explanations.",
      "deep-dive": "Include technical internals, implementation details, and references."
    }
  }
}
```

### 4. Personalizer Module

**File**: `scripts/personalizer.py`

A Python module for profile management and content personalization.

```python
from rag_personalizer import Personalizer

# Initialize
personalizer = Personalizer()

# Create profile
profile = personalizer.create_profile("user123", {
    "learning_style": "visual",
    "knowledge_level": "beginner"
})

# Personalize content
result = personalizer.personalize(
    content="ROS 2 is a robotics middleware...",
    profile=profile,
    query="What is ROS 2?"
)

print(result.personalized_content)
print(result.adaptations_applied)
```

### 5. Test Suite

**File**: `scripts/test.sh` - Bash test runner
**File**: `scripts/test_personalizer.py` - Python unit tests

```bash
# Run tests
.claude/skills/rag-personalizer/scripts/test.sh
```

## Usage Instructions

### Step 1: Set Environment Variables

```bash
# Add to .env file
OPENAI_API_KEY=sk-...

# Optional: For RAG integration
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=your-api-key
```

### Step 2: Create User Profile

```bash
# Create with defaults
.claude/skills/rag-personalizer/scripts/setup.sh --create-profile student1

# Create with specific dimensions
.claude/skills/rag-personalizer/scripts/setup.sh --create-profile student1 \
  --dimension learning_style --value visual \
  --dimension knowledge_level --value beginner
```

### Step 3: Update Profile

```bash
# Update single dimension
.claude/skills/rag-personalizer/scripts/setup.sh --update-profile student1 \
  --dimension knowledge_level --value intermediate

# View profile
.claude/skills/rag-personalizer/scripts/setup.sh --get-profile student1
```

### Step 4: Personalize Content

```bash
# Personalize from RAG query
.claude/skills/rag-personalizer/scripts/setup.sh --personalize "What is ROS 2?" \
  --profile student1

# Personalize direct content
.claude/skills/rag-personalizer/scripts/setup.sh --content "ROS 2 uses DDS..." \
  --profile student1 --output markdown
```

### Step 5: Integrate with RAG Chatbot

```python
# In FastAPI backend
from rag_personalizer import Personalizer
from vectorize import QdrantManager

@app.post("/chat")
async def chat(query: str, user_id: str):
    # Get user profile
    personalizer = Personalizer()
    profile = personalizer.get_profile(user_id)

    # Retrieve content
    qdrant = QdrantManager()
    results = qdrant.query(query, language=profile.dimensions.language)

    # Personalize
    context = "\n".join([r['content'] for r in results[:3]])
    personalized = personalizer.personalize(context, profile, query)

    return {"response": personalized.content}
```

## Verification Checklist

- [ ] `OPENAI_API_KEY` environment variable set
- [ ] Profile created successfully
- [ ] Profile dimensions update correctly
- [ ] Content personalization returns adapted content
- [ ] Language switching works (en/ur)
- [ ] RAG integration functions properly

## API Reference

### Personalizer Class

```python
class Personalizer:
    def create_profile(id: str, dimensions: dict = None) -> Profile
    def get_profile(id: str) -> Profile
    def update_profile(id: str, dimension: str, value: str) -> Profile
    def delete_profile(id: str) -> bool
    def list_profiles() -> List[Profile]
    def personalize(content: str, profile: Profile, query: str = None) -> PersonalizedContent
```

### Profile Model

```python
class Profile:
    id: str
    created_at: datetime
    updated_at: datetime
    dimensions: ProfileDimensions

class ProfileDimensions:
    learning_style: Literal["visual", "auditory", "kinesthetic", "reading"]
    knowledge_level: Literal["beginner", "intermediate", "advanced"]
    learning_pace: Literal["slow", "moderate", "fast"]
    language: Literal["en", "ur"]
    content_depth: Literal["overview", "standard", "deep-dive"]
    example_preference: Literal["theoretical", "practical", "code-heavy"]
    difficulty_tolerance: Literal["easy", "moderate", "challenging"]
    interaction_style: Literal["passive", "interactive", "hands-on"]
    time_availability: Literal["limited", "moderate", "extensive"]
    goal_orientation: Literal["certification", "understanding", "application"]
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| **API rate limit** | Reduce request frequency or upgrade OpenAI plan |
| **Profile not found** | Create profile first with `--create-profile` |
| **Invalid dimension** | Check spelling, use exact enum values |
| **Translation issues** | Ensure `language` dimension is set correctly |
| **Slow response** | Use `gpt-4o-mini` instead of `gpt-4o` |

## Requirements

- Python 3.9+
- OpenAI API key
- pip packages: openai, pydantic, python-dotenv

## Cost Considerations

| Resource | Cost |
|----------|------|
| **GPT-4o-mini** | $0.15 / 1M input tokens |
| **GPT-4o** | $2.50 / 1M input tokens |
| **Estimated per query** | ~$0.001 (gpt-4o-mini) |

## Related

- Skill: `qdrant-manager` - Vector storage for RAG retrieval
- Feature: `004-personalization` - Personalization specification
- Feature: `002-rag-chatbot` - RAG chatbot integration

## Changelog

### v1.0.0 (2026-01-02)
**Initial Release**

- 10-dimension user profile system
- Profile CRUD operations (create, read, update, delete)
- Content personalization via OpenAI
- Support for English and Urdu languages
- Integration with qdrant-manager for RAG
- Adaptive strategies for all dimensions
- JSON and Markdown output formats
