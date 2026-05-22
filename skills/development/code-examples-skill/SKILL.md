---
skill: 'code-examples'
version: '2.0.0'
updated: '2025-12-31'
category: 'technical-integration'
complexity: 'intermediate'
prerequisite_skills: []
composable_with: ['api-integration', 'technical-writing', 'document-structure']
---

# Code Examples Skill

## Overview
This skill provides expertise in creating clear, accurate, and educational code examples for AI implementation guides in the FTE+AI project.

## Core Principles

### Code Quality Standards
- **Executable:** All code must run without errors
- **Complete:** Include necessary imports and setup
- **Commented:** Explain non-obvious logic
- **Realistic:** Use real-world scenarios relevant to R&D teams
- **Consistent:** Follow language-specific style guides

### Example Structure

```markdown
### [Feature/Task Title]

**Use Case:** [Brief description of what this solves]

**Code:**
```language
[Complete, runnable code]
```

**Explanation:**
- Point 1: [What this code does]
- Point 2: [Why it's structured this way]
- Point 3: [Key concepts demonstrated]

**Output:**
```
[Expected result]
```

**Considerations:**
- [Important notes, limitations, or alternatives]
```

## Language-Specific Guidelines

### Python
```python
# Use type hints for clarity
def process_documentation(file_path: str, model: str = "gpt-4") -> dict:
    """
    Process documentation using AI.
    
    Args:
        file_path: Path to the documentation file
        model: AI model to use (default: gpt-4)
    
    Returns:
        Dictionary with processed results
    """
    # Implementation
    pass
```

**Best Practices:**
- Use type hints (Python 3.6+)
- Include docstrings for functions
- Follow PEP 8 style guide
- Use meaningful variable names
- Handle exceptions explicitly

### JavaScript/TypeScript
```typescript
// Use TypeScript for better documentation
interface DocumentationConfig {
  model: string;
  maxTokens: number;
  temperature: number;
}

async function generateDocs(
  code: string,
  config: DocumentationConfig
): Promise<string> {
  // Implementation
  return "";
}
```

**Best Practices:**
- Prefer TypeScript over JavaScript
- Use async/await over promises
- Include interface definitions
- Use const/let, never var
- Add JSDoc comments

### Shell/Bash
```bash
#!/bin/bash
# Setup AI development environment

# Check prerequisites
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is required but not installed"
    exit 1
fi

# Install dependencies
pip install openai anthropic
```

**Best Practices:**
- Include shebang line
- Check for prerequisites
- Provide error messages
- Use comments for sections
- Quote variables: "$variable"

## Common AI Integration Patterns

### Pattern 1: Basic AI API Call
```python
from openai import OpenAI

client = OpenAI(api_key="your-api-key")

def generate_documentation(code: str) -> str:
    """Generate documentation from code using AI."""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a documentation expert."},
            {"role": "user", "content": f"Document this code:\n\n{code}"}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content

# Example usage
code_snippet = """
def calculate_roi(investment, return_value):
    return (return_value - investment) / investment * 100
"""

documentation = generate_documentation(code_snippet)
print(documentation)
```

### Pattern 2: RAG Implementation
```python
from openai import OpenAI
import chromadb

# Initialize vector database
chroma_client = chromadb.Client()
collection = chroma_client.create_collection("company_docs")

# Add documents
def index_documents(documents: list[str]):
    """Index company documentation for RAG."""
    collection.add(
        documents=documents,
        ids=[f"doc_{i}" for i in range(len(documents))]
    )

# Retrieve relevant context
def query_with_context(question: str) -> str:
    """Answer questions using company documentation."""
    # Find relevant documents
    results = collection.query(
        query_texts=[question],
        n_results=3
    )
    
    context = "\n".join(results['documents'][0])
    
    # Generate answer with context
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": f"Use this context:\n{context}"},
            {"role": "user", "content": question}
        ]
    )
    
    return response.choices[0].message.content
```

### Pattern 3: AI Agent with Tools
```python
from anthropic import Anthropic

def create_code_review_agent():
    """Create an AI agent that can review code and suggest improvements."""
    client = Anthropic(api_key="your-api-key")
    
    tools = [
        {
            "name": "analyze_complexity",
            "description": "Analyze code complexity metrics",
            "input_schema": {
                "type": "object",
                "properties": {
                    "code": {"type": "string"}
                }
            }
        },
        {
            "name": "check_security",
            "description": "Check for security vulnerabilities",
            "input_schema": {
                "type": "object",
                "properties": {
                    "code": {"type": "string"}
                }
            }
        }
    ]
    
    def review_code(code: str) -> str:
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4096,
            tools=tools,
            messages=[{
                "role": "user",
                "content": f"Review this code:\n\n{code}"
            }]
        )
        return response.content[0].text
    
    return review_code
```

### Pattern 4: Streaming Responses
```python
from openai import OpenAI

def stream_ai_response(prompt: str):
    """Stream AI responses for real-time feedback."""
    client = OpenAI()
    
    stream = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        stream=True
    )
    
    for chunk in stream:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
    print()  # New line after streaming

# Example usage
stream_ai_response("Explain the benefits of AI for R&D teams")
```

### Pattern 5: Error Handling & Retries
```python
import time
from openai import OpenAI, OpenAIError

def call_ai_with_retry(prompt: str, max_retries: int = 3) -> str:
    """Call AI API with exponential backoff retry logic."""
    client = OpenAI()
    
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                timeout=30
            )
            return response.choices[0].message.content
            
        except OpenAIError as e:
            if attempt == max_retries - 1:
                raise
            
            # Exponential backoff
            wait_time = 2 ** attempt
            print(f"Attempt {attempt + 1} failed. Retrying in {wait_time}s...")
            time.sleep(wait_time)
    
    raise Exception("Max retries exceeded")
```

## Code Example Templates

### Quick Start Template
```markdown
### Quick Start: [Feature Name]

**Goal:** [What user will accomplish]

**Prerequisites:**
- Python 3.8+
- OpenAI API key

**Installation:**
```bash
pip install openai
```

**Code:**
```python
# [Complete minimal example]
```

**Run:**
```bash
python example.py
```

**Expected Output:**
```
[Sample output]
```
```

### Comparison Template
```markdown
### Approach Comparison: [Task]

#### Option 1: [Approach Name]
**Pros:** [Benefits]
**Cons:** [Limitations]

```python
# [Implementation]
```

#### Option 2: [Approach Name]
**Pros:** [Benefits]
**Cons:** [Limitations]

```python
# [Implementation]
```

**Recommendation:** [When to use which]
```

### Migration Template
```markdown
### Migrating from [Old Approach] to [New Approach]

**Before (Manual Process):**
```python
# [Old code]
```

**After (AI-Augmented):**
```python
# [New code with AI]
```

**Benefits:**
- [Benefit 1]
- [Benefit 2]

**Migration Steps:**
1. [Step 1]
2. [Step 2]
```

## Best Practices Checklist

**Before Writing Code:**
- [ ] Understand the use case and audience
- [ ] Choose appropriate language and tools
- [ ] Plan code structure and flow
- [ ] Identify key concepts to demonstrate

**While Writing Code:**
- [ ] Use realistic variable names
- [ ] Add inline comments for complex logic
- [ ] Include error handling
- [ ] Follow language conventions
- [ ] Keep examples focused (< 50 lines ideal)

**After Writing Code:**
- [ ] Test code execution
- [ ] Verify output matches expectations
- [ ] Check for security issues (no hardcoded secrets)
- [ ] Ensure dependencies are listed
- [ ] Add explanation and context

## Security Guidelines

**DO:**
- Use environment variables for API keys
- Show placeholder values: `api_key="your-api-key"`
- Include instructions for secure configuration
- Validate user inputs
- Use HTTPS for API calls

**DON'T:**
- Hardcode real API keys or secrets
- Show real production URLs or endpoints
- Ignore input validation
- Use deprecated or insecure libraries
- Expose sensitive business logic

## Example Documentation Structures

### For Tutorials:
```
1. Introduction (What & Why)
2. Prerequisites
3. Setup (Step-by-step)
4. Basic Example (Minimal code)
5. Detailed Example (Full features)
6. Common Issues
7. Next Steps
```

### For API Reference:
```
1. Function/Class Name
2. Purpose (One sentence)
3. Parameters (Type, description, default)
4. Return Value (Type, description)
5. Example Usage (Code)
6. Notes/Warnings
```

### For Comparison Guides:
```
1. Context (Problem to solve)
2. Options Overview (Table)
3. Detailed Comparison (Code examples for each)
4. Performance/Cost Analysis
5. Decision Matrix
6. Recommendations
```

## Platform-Specific Examples

### GitHub Copilot Integration
```json
{
  "github.copilot.enable": true,
  "github.copilot.advanced": {
    "inlineSuggestCount": 3
  }
}
```

### VS Code Extension
```typescript
import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {
    let disposable = vscode.commands.registerCommand(
        'extension.generateDocs',
        async () => {
            const editor = vscode.window.activeTextEditor;
            if (!editor) return;
            
            const code = editor.document.getText();
            // AI integration here
        }
    );
    
    context.subscriptions.push(disposable);
}
```

## Quality Metrics
- **Accuracy:** Code executes without errors (100%)
- **Clarity:** Commented and explained (90%+ understandability)
- **Completeness:** Can run standalone (no missing imports)
- **Relevance:** Solves real R&D problems (practical value)
- **Security:** No hardcoded secrets or vulnerabilities
