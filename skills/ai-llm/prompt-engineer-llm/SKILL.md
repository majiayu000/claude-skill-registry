---
name: prompt-engineer-llm
description: World-class expert in prompt engineering, LLM fine-tuning, RAG systems, and AI/ML workflows. Use when crafting prompts, designing AI agents, building knowledge bases, implementing retrieval systems, or optimizing LLM performance at production scale.
---

# Prompt Engineer & LLM Specialist - World-Class Edition

## Project Context: DriverConnect (eddication.io)

**IMPORTANT**: This project integrates AI/ML for various features including geocoding, route optimization, and potential driver assistance features.

### AI/ML Integration Points

| Feature | AI Technology | Status |
|---------|---------------|--------|
| **Geocoding** | Nominatim/Photon API (future: LLM-enhanced) | Active |
| **Route Optimization** | Algorithmic (future: ML models) | Planned |
| **Driver Assist** | LLM-based chatbot | Planned |
| **Document Processing** | OCR + LLM extraction | Planned |
| **Voice Commands** | STT + LLM | Planned |

### Project Files

- **AI Prompts**: [PTGLG/driverconnect/admin/js/prompts.js](../PTGLG/driverconnect/admin/js/prompts.js) (if exists)
- **LLM Integration**: [backend/lib/llm-service.js](../backend/lib/llm-service.js) (if exists)

---

## Overview

You are a world-class expert in prompt engineering, LLM architecture, and AI/ML systems. You understand how to craft effective prompts, design retrieval-augmented generation (RAG) systems, fine-tune models, build AI agents, and optimize for cost and performance. You excel at bridging the gap between raw model capabilities and production-ready AI features.

---

# Philosophy & Principles

## Core Principles

1. **Clarity Over Cleverness** - Explicit instructions beat implicit hints
2. **Context is King** - Provide relevant information, minimize noise
3. **Test and Iterate** - Prompt engineering is empirical
4. **Cost Awareness** - Optimize for token usage and latency
5. **Safety First** - Guardrails, filtering, and monitoring
6. **Human-in-the-Loop** - AI augments, not replaces, human judgment

## Prompt Engineering Decision Tree

```
Task → Is it simple or complex?
    ├─ Simple → Direct prompt with clear instructions
    │
    └─ Complex → Needs strategy?
        ├─ Yes → Chain of Thought, Few-shot, or Decomposition
        └─ No → Needs external knowledge?
            ├─ Yes → RAG (Retrieval Augmented Generation)
            └─ No → Zero/Few-shot with examples
```

---

# Prompt Engineering Fundamentals

## The Anatomy of a Perfect Prompt

```
┌─────────────────────────────────────────────────────────────┐
│                     SYSTEM MESSAGE                          │
│  Role, personality, constraints, output format, safety      │
├─────────────────────────────────────────────────────────────┤
│                     USER MESSAGE                            │
│  Context + Task + Examples + Constraints + Output Format    │
└─────────────────────────────────────────────────────────────┘
```

### Essential Components

| Component | Purpose | Example |
|-----------|---------|---------|
| **Role** | Set persona and expertise level | "You are an expert logistics coordinator..." |
| **Context** | Provide background information | "DriverConnect is a fuel delivery system..." |
| **Task** | Clear, specific instruction | "Extract delivery addresses from this text..." |
| **Examples** | Few-shot learning | "Input: X → Output: Y" |
| **Constraints** | What NOT to do | "Do not make up information..." |
| **Format** | Expected output structure | "Return JSON with keys: address, city, province" |
| **Thinking** | Chain-of-thought | "Think step by step..." |

## Prompt Templates

### Zero-Shot Template

```
You are a world-class {domain} expert.

Task: {task_description}

Input: {input_data}

Constraints:
- {constraint_1}
- {constraint_2}

Output Format: {format_specification}
```

### Few-Shot Template

```
You are a world-class {domain} expert.

Your task is to {task_description}.

Here are some examples:

Example 1:
Input: {example_1_input}
Output: {example_1_output}

Example 2:
Input: {example_2_input}
Output: {example_2_output}

Example 3:
Input: {example_3_input}
Output: {example_3_output}

Now, process this input:
Input: {actual_input}

Output:
```

### Chain-of-Thought Template

```
You are a world-class {domain} expert.

Task: {task_description}

Let's think step by step:

1. First, {step_1_instruction}
2. Then, {step_2_instruction}
3. Finally, {step_3_instruction}

Input: {input_data}

Step-by-step reasoning:
[Your reasoning here]

Final Answer:
[Your final answer here]
```

---

# Advanced Prompt Techniques

## Chain-of-Thought (CoT)

### When to Use

| Scenario | Why CoT Helps |
|----------|---------------|
| Multi-step reasoning | Breaks complex problems |
| Math/Logic problems | Shows work, reduces errors |
| Debugging | Systematic elimination |
| Planning | Sequential consideration |

### Examples

```
// Basic CoT
A truck has 22 delivery stops. At stop 1-5, 50 liters each. Stop 6-15, 30 liters each.
Stop 16-22, 20 liters each. How much total fuel?

Let's think step by step:
1. First, calculate stops 1-5: 5 stops × 50 liters = 250 liters
2. Then, calculate stops 6-15: 10 stops × 30 liters = 300 liters
3. Then, calculate stops 16-22: 7 stops × 20 liters = 140 liters
4. Finally, add them all: 250 + 300 + 140 = 690 liters

Answer: 690 liters
```

## Self-Consistency

```
Task: Solve this complex logistics problem

Please solve this problem three different ways and compare your answers:
1. Method 1: [Approach description]
2. Method 2: [Approach description]
3. Method 3: [Approach description]

After getting three answers, determine which is most likely correct and explain why.
```

## Tree of Thoughts

```
You are a strategic logistics planner.

For this delivery challenge, explore multiple solution paths:

Path A: [Option A description]
  - Pros: [List]
  - Cons: [List]
  - Outcome prediction: [Analysis]

Path B: [Option B description]
  - Pros: [List]
  - Cons: [List]
  - Outcome prediction: [Analysis]

Path C: [Option C description]
  - Pros: [List]
  - Cons: [List]
  - Outcome prediction: [Analysis]

After evaluating all paths, recommend the best option with justification.
```

## ReAct Pattern (Reason + Act)

```
You are a logistics assistant with access to tools.

For each step, think then act:

Thought: [What you want to do]
Action: [Which tool to use]
Observation: [What the tool returned]
Thought: [What to do next based on observation]
Action: [Next tool]
... (repeat until done)

Final Answer: [The result]
```

---

# Retrieval Augmented Generation (RAG)

## RAG Architecture

```
┌─────────────┐
│ User Query  │
└──────┬──────┘
       │
       ▼
┌──────────────┐     ┌─────────────┐
│  Embedding   │────►│ Vector DB   │
│   Model      │     │ (pgvector)  │
└──────────────┘     └──────┬──────┘
                            │
                            ▼
                       ┌─────────┐
                       │Context  │
                       │+ Query  │
                       └────┬────┘
                            │
                            ▼
                       ┌─────────┐
                       │   LLM   │
                       └────┬────┘
                            │
                            ▼
                       ┌─────────┐
                       │ Answer  │
                       └─────────┘
```

## RAG Implementation

```typescript
// Vector database schema (PostgreSQL + pgvector)
CREATE TABLE documents (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  content TEXT NOT NULL,
  embedding vector(1536),  // OpenAI dimension
  metadata JSONB DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX docs_embedding_idx
  ON documents USING hnsw (embedding vector_cosine_ops);

// Matching function
CREATE OR REPLACE FUNCTION match_documents(
  query_embedding vector(1536),
  match_threshold float DEFAULT 0.8,
  match_count int DEFAULT 10
)
RETURNS TABLE (
  id UUID,
  content TEXT,
  similarity float
)
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN QUERY
  SELECT
    d.id,
    d.content,
    1 - (d.embedding <=> query_embedding) as similarity
  FROM documents d
  WHERE d.embedding <=> query_embedding < 1 - match_threshold
  ORDER BY d.embedding <=> query_embedding
  LIMIT match_count;
END;
$$;

// RAG pipeline
import { OpenAI } from 'openai';

const openai = new OpenAI();

async function ragAnswer(query: string) {
  // 1. Embed query
  const embedding = await openai.embeddings.create({
    model: 'text-embedding-3-small',
    input: query
  });

  // 2. Retrieve relevant documents
  const { data: docs } = await supabase.rpc('match_documents', {
    query_embedding: embedding.data[0].embedding,
    match_threshold: 0.8,
    match_count: 5
  });

  // 3. Build prompt with context
  const context = docs.map(d => d.content).join('\n\n');

  const prompt = `
You are a DriverConnect logistics expert. Answer the user's question using the context below.

Context:
${context}

Question: ${query}

If the context doesn't contain the answer, say "I don't have enough information to answer this."

Answer:
  `.trim();

  // 4. Generate response
  const completion = await openai.chat.completions.create({
    model: 'gpt-4o',
    messages: [{ role: 'user', content: prompt }],
    temperature: 0.3
  });

  return completion.choices[0].message.content;
}
```

## Chunking Strategies

```typescript
// Fixed-size chunking
function chunkBySize(text: string, chunkSize: number = 500, overlap: number = 50) {
  const chunks: string[] = [];
  let start = 0;

  while (start < text.length) {
    const end = Math.min(start + chunkSize, text.length);
    chunks.push(text.slice(start, end));
    start = end - overlap;
  }

  return chunks;
}

// Semantic chunking (by paragraph/sentence)
function chunkSemantic(text: string) {
  return text
    .split(/\n\n+/)  // Split by paragraphs
    .filter(p => p.trim().length > 50)  // Filter too short
    .map(p => p.trim());
}

// Recursive chunking (preserves structure)
function chunkRecursive(
  text: string,
  separators: string[] = ['\n\n', '\n', '. ', ' '],
  maxSize: number = 500
): string[] {
  for (const sep of separators) {
    const parts = text.split(sep);
    if (parts.every(p => p.length <= maxSize)) {
      return parts.filter(p => p.trim());
    }
  }
  // Fallback to fixed size
  return chunkBySize(text, maxSize);
}
```

---

# LLM Fine-Tuning

## When to Fine-Tune

| Scenario | Base Model | Fine-Tuned |
|----------|------------|------------|
| General tasks | Good enough | Overkill |
| Domain-specific jargon | Struggles | Excels |
| Specific output format | Inconsistent | Reliable |
| Cost optimization | Large prompts | Compact prompts |
| Privacy | External API | Self-hosted |

## Fine-Tuning Process

```python
# Prepare training data
training_data = [
    {
        "messages": [
            {"role": "system", "content": "You are a DriverConnect logistics assistant."},
            {"role": "user", "content": "What's the status of trip TRIP-001?"},
            {"role": "assistant", "content": "Trip TRIP-001 is currently in progress. Driver Somchai is at stop 2 of 5."}
        ]
    },
    # ... more examples
]

# Save as JSONL
import json

with open('driverconnect_train.jsonl', 'w') as f:
    for entry in training_data:
        f.write(json.dumps(entry) + '\n')

# Upload and fine-tune (OpenAI)
from openai import OpenAI

client = OpenAI()

# Upload file
response = client.files.create(
    file=open('driverconnect_train.jsonl', 'rb'),
    purpose='fine-tune'
)
file_id = response.id

# Start fine-tuning
fine_tune = client.fine_tuning.jobs.create(
    training_file=file_id,
    model='gpt-4o-mini',
    hyperparameters={
        'n_epochs': 3,
        'learning_rate_multiplier': 0.1,
        'batch_size': 4
    }
)

# Monitor progress
job = client.fine_tuning.jobs.retrieve(fine_tune.id)
print(f"Status: {job.status}")

# Use fine-tuned model
completion = client.chat.completions.create(
    model=fine_tune.fine_tuned_model,
    messages=[...]
)
```

---

# Agent Design Patterns

## ReAct Agent

```typescript
interface Tool {
  name: string;
  description: string;
  parameters: Record<string, any>;
  execute: (params: any) => Promise<string>;
}

class ReActAgent {
  private tools: Map<string, Tool> = new Map();

  registerTool(tool: Tool) {
    this.tools.set(tool.name, tool);
  }

  async run(query: string, maxSteps: number = 10) {
    let thought = `I need to answer: ${query}`;
    const steps: string[] = [];

    for (let i = 0; i < maxSteps; i++) {
      // Decide next action
      const prompt = `
Thought: ${thought}

Available tools:
${Array.from(this.tools.values()).map(t =>
  `- ${t.name}: ${t.description}`
).join('\n')}

Respond in this format:
Thought: [your reasoning]
Action: [tool name]
Action Input: [JSON parameters]

Or if you have the final answer:
Thought: [reasoning]
Final Answer: [answer]
      `.trim();

      const response = await this.llm(prompt);

      // Parse response
      const actionMatch = response.match(/Action: (\w+)/);
      const inputMatch = response.match(/Action Input: ({.*})/s);
      const finalMatch = response.match(/Final Answer: (.*)/s);

      if (finalMatch) {
        return finalMatch[1];
      }

      if (actionMatch && inputMatch) {
        const tool = this.tools.get(actionMatch[1]);
        if (tool) {
          const result = await tool.execute(JSON.parse(inputMatch[1]));
          thought = `Action ${actionMatch[1]} returned: ${result}`;
          steps.push(`${actionMatch[1]}: ${result}`);
        }
      }
    }

    return 'Could not complete task';
  }

  private async llm(prompt: string): Promise<string> {
    // LLM call implementation
    return '';
  }
}
```

## Multi-Agent System

```
┌─────────────────────────────────────────────────────────┐
│                    Coordinator Agent                     │
│  - Receives user request                                │
│  - Decomposes into sub-tasks                            │
│  - Routes to specialist agents                          │
│  - Aggregates results                                   │
└──────┬────────┬────────┬────────┬────────┬──────────────┘
       │        │        │        │        │
       ▼        ▼        ▼        ▼        ▼
┌──────────┐┌────────┐┌───────┐┌──────┐┌─────────┐
│Routing   ││Status  ││Geocode││Alert ││Report   │
│Agent     ││Agent   ││Agent  ││Agent ││Agent    │
└──────────┘└────────┘└───────┘└──────┘└─────────┘
```

---

# Prompt Evaluation & Testing

## Evaluation Metrics

```typescript
interface PromptEvaluation {
  // Accuracy
  correctness: number;  // 0-1, factual correctness
  completeness: number;  // 0-1, covered all aspects

  // Quality
  coherence: number;  // 0-1, logical flow
  conciseness: number;  // 0-1, not verbose

  // Safety
  hallucination: boolean;  // Made up information
  policyViolation: boolean;  // Broke guidelines

  // Performance
  latency: number;  // milliseconds
  tokenUsage: number;  // total tokens
  cost: number;  // USD
}

async function evaluatePrompt(
  prompt: string,
  testCases: Array<{input: string, expected: string}>
): Promise<PromptEvaluation> {
  const results = await Promise.all(
    testCases.map(async ({input, expected}) => {
      const start = Date.now();
      const output = await llm(prompt + '\n\nInput: ' + input);
      const latency = Date.now() - start;

      return {
        output,
        latency,
        similarity: cosineSimilarity(embed(expected), embed(output))
      };
    })
  );

  return {
    correctness: results.reduce((s, r) => s + r.similarity, 0) / results.length,
    latency: results.reduce((s, r) => s + r.latency, 0) / results.length,
    // ... other metrics
  };
}
```

---

# World-Class Resources

## Official Documentation
- OpenAI Docs: https://platform.openai.com/docs
- Anthropic Docs: https://docs.anthropic.com
- LangChain Docs: https://python.langchain.com

## Prompt Engineering Guides
- OpenAI Prompt Engineering Guide: https://platform.openai.com/docs/guides/prompt-engineering
- Anthropic Prompt Library: https://docs.anthropic.com/claude/prompt-library

## RAG Resources
- LangChain RAG Tutorial: https://python.langchain.com/docs/tutorials/rag
- LlamaIndex Documentation: https://docs.llamaindex.ai

## Fine-Tuning
- OpenAI Fine-Tuning Guide: https://platform.openai.com/docs/guides/fine-tuning
- HuggingFace PEFT: https://huggingface.co/docs/peft

## Tools & Frameworks
- LangChain: https://github.com/langchain-ai/langchain
- LlamaIndex: https://github.com/run-llama/llama_index
- AutoGPT: https://github.com/Significant-Gravitas/AutoGPT
- Vector DBs: Pinecone, Weaviate, Qdrant, pgvector
