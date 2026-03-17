---
name: hugging-face-dataset-creator
description: Create and manage datasets on Hugging Face Hub. Supports initializing repos, defining configs/system prompts, and streaming row updates. Designed to work alongside HF MCP server for comprehensive dataset workflows.
---

# Overview
This skill provides tools to manage datasets on the Hugging Face Hub with a focus on creation, configuration, and content management. It is designed to complement the existing Hugging Face MCP server by providing dataset editing capabilities that the MCP server doesn't offer.

## Integration with HF MCP Server
- **Use HF MCP Server for**: Dataset discovery, search, and metadata retrieval
- **Use This Skill for**: Dataset creation, content editing, configuration management, and structured data formatting

# Version
2.0.0

# Dependencies
- huggingface_hub
- json (built-in)
- time (built-in)

# Core Capabilities

## 1. Dataset Lifecycle Management
- **Initialize**: Create new dataset repositories with proper structure
- **Configure**: Store detailed configuration including system prompts and metadata
- **Stream Updates**: Add rows efficiently without downloading entire datasets

## 2. Multi-Format Dataset Support
Supports diverse dataset types through template system:
- **Chat/Conversational**: Chat templating, multi-turn dialogues, tool usage examples
- **Text Classification**: Sentiment analysis, intent detection, topic classification
- **Question-Answering**: Reading comprehension, factual QA, knowledge bases
- **Text Completion**: Language modeling, code completion, creative writing
- **Tabular Data**: Structured data for regression/classification tasks
- **Custom Formats**: Flexible schema definition for specialized needs

## 3. Quality Assurance Features
- **JSON Validation**: Ensures data integrity during uploads
- **Batch Processing**: Efficient handling of large datasets
- **Error Recovery**: Graceful handling of upload failures and conflicts

# Usage Instructions

The skill includes a Python script `scripts/dataset_manager.py` to perform operations.

### Prerequisites
- `huggingface_hub` library must be installed via `uv add huggingface_hub`
- `HF_TOKEN` environment variable must be set with a Write-access token
- Activate virtual environment: `source .venv/bin/activate`

### Recommended Workflow

**1. Discovery (Use HF MCP Server):**
```python
# Use HF MCP tools to find existing datasets
search_datasets("conversational AI training")
get_dataset_details("username/dataset-name")
```

**2. Creation (Use This Skill):**
```bash
# Initialize new dataset
python scripts/dataset_manager.py init --repo_id "your-username/dataset-name" [--private]

# Configure with detailed system prompt
python scripts/dataset_manager.py config --repo_id "your-username/dataset-name" --system_prompt "$(cat system_prompt.txt)"
```

**3. Content Management (Use This Skill):**
```bash
# Quick setup with any template
python scripts/dataset_manager.py quick_setup \
  --repo_id "your-username/dataset-name" \
  --template classification

# Add data with template validation
python scripts/dataset_manager.py add_rows \
  --repo_id "your-username/dataset-name" \
  --template qa \
  --rows_json "$(cat your_qa_data.json)"
```

### Template-Based Data Structures

**1. Chat Template (`--template chat`)**
```json
{
  "messages": [
    {"role": "user", "content": "Natural user request"},
    {"role": "assistant", "content": "Response with tool usage"},
    {"role": "tool", "content": "Tool response", "tool_call_id": "call_123"}
  ],
  "scenario": "Description of use case",
  "complexity": "simple|intermediate|advanced"
}
```

**2. Classification Template (`--template classification`)**
```json
{
  "text": "Input text to be classified",
  "label": "classification_label",
  "confidence": 0.95,
  "metadata": {"domain": "technology", "language": "en"}
}
```

**3. QA Template (`--template qa`)**
```json
{
  "question": "What is the question being asked?",
  "answer": "The complete answer",
  "context": "Additional context if needed",
  "answer_type": "factual|explanatory|opinion",
  "difficulty": "easy|medium|hard"
}
```

**4. Completion Template (`--template completion`)**
```json
{
  "prompt": "The beginning text or context",
  "completion": "The expected continuation",
  "domain": "code|creative|technical|conversational",
  "style": "description of writing style"
}
```

**5. Tabular Template (`--template tabular`)**
```json
{
  "columns": [
    {"name": "feature1", "type": "numeric", "description": "First feature"},
    {"name": "target", "type": "categorical", "description": "Target variable"}
  ],
  "data": [
    {"feature1": 123, "target": "class_a"},
    {"feature1": 456, "target": "class_b"}
  ]
}
```

### Advanced System Prompt Template

For high-quality training data generation:
```text
You are an AI assistant expert at using MCP tools effectively.

## MCP SERVER DEFINITIONS
[Define available servers and tools]

## TRAINING EXAMPLE STRUCTURE
[Specify exact JSON schema for chat templating]

## QUALITY GUIDELINES
[Detail requirements for realistic scenarios, progressive complexity, proper tool usage]

## EXAMPLE CATEGORIES
[List development workflows, debugging scenarios, data management tasks]
```

### Example Categories & Templates

The skill includes diverse training examples beyond just MCP usage:

**Available Example Sets:**
- `training_examples.json` - MCP tool usage examples (debugging, project setup, database analysis)
- `diverse_training_examples.json` - Broader scenarios including:
  - **Educational Chat** - Explaining programming concepts, tutorials
  - **Git Workflows** - Feature branches, version control guidance
  - **Code Analysis** - Performance optimization, architecture review
  - **Content Generation** - Professional writing, creative brainstorming
  - **Codebase Navigation** - Legacy code exploration, systematic analysis
  - **Conversational Support** - Problem-solving, technical discussions

**Using Different Example Sets:**
```bash
# Add MCP-focused examples
python scripts/dataset_manager.py add_rows --repo_id "your-username/dataset-name" \
  --rows_json "$(cat examples/training_examples.json)"

# Add diverse conversational examples
python scripts/dataset_manager.py add_rows --repo_id "your-username/dataset-name" \
  --rows_json "$(cat examples/diverse_training_examples.json)"

# Mix both for comprehensive training data
python scripts/dataset_manager.py add_rows --repo_id "your-username/dataset-name" \
  --rows_json "$(jq -s '.[0] + .[1]' examples/training_examples.json examples/diverse_training_examples.json)"
```

### Commands Reference

**List Available Templates:**
```bash
python scripts/dataset_manager.py list_templates
```

**Quick Setup (Recommended):**
```bash
python scripts/dataset_manager.py quick_setup --repo_id "your-username/dataset-name" --template classification
```

**Manual Setup:**
```bash
# Initialize repository
python scripts/dataset_manager.py init --repo_id "your-username/dataset-name" [--private]

# Configure with system prompt
python scripts/dataset_manager.py config --repo_id "your-username/dataset-name" --system_prompt "Your prompt here"

# Add data with validation
python scripts/dataset_manager.py add_rows \
  --repo_id "your-username/dataset-name" \
  --template qa \
  --rows_json '[{"question": "What is AI?", "answer": "Artificial Intelligence..."}]'
```

**View Dataset Statistics:**
```bash
python scripts/dataset_manager.py stats --repo_id "your-username/dataset-name"
```

### Error Handling
- **Repository exists**: Script will notify and continue with configuration
- **Invalid JSON**: Clear error message with parsing details
- **Network issues**: Automatic retry for transient failures
- **Token permissions**: Validation before operations begin
