---
skill: 'ai-terminology'
version: '2.0.0'
updated: '2025-12-31'
category: 'documentation'
complexity: 'foundational'
prerequisite_skills: []
composable_with: ['technical-writing', 'document-structure']
---

# AI Terminology Skill

## Overview
This skill ensures consistent, accurate usage of AI/ML terminology throughout the FTE+AI documentation, making content accessible to R&D audiences with varying AI expertise.

## Core Terminology

### AI/ML Fundamentals

**Artificial Intelligence (AI)**
- **Definition:** Computer systems that can perform tasks typically requiring human intelligence
- **Usage:** Use when discussing broad capabilities (reasoning, learning, problem-solving)
- **Context for R&D:** "AI can automate repetitive coding tasks and augment developer productivity"

**Machine Learning (ML)**
- **Definition:** Subset of AI where systems learn from data without explicit programming
- **Usage:** Use when discussing models trained on data
- **Context:** "ML models can predict code defects based on historical patterns"

**Large Language Models (LLMs)**
- **Definition:** AI models trained on vast text data to understand and generate human language
- **Examples:** GPT-4/5, Claude, Gemini, Qwen-Next, GLM-4.6, MiniMax-M2
- **Usage:** Use when discussing text generation, code completion, or conversational AI
- **Context:** "LLMs like GPT-4 can generate documentation from code comments"

**Generative AI**
- **Definition:** AI systems that create new content (text, code, images)
- **Usage:** Use when discussing content creation capabilities
- **Context:** "Generative AI can create test cases and mock data for QA"

### Model Types & Architectures

**Foundation Models**
- Pre-trained models that can be adapted for multiple tasks
- Examples: GPT, BERT, T5
- Usage: When discussing base models before fine-tuning

**Fine-tuned Models**
- Models adapted for specific tasks or domains
- Usage: "A fine-tuned model trained on your codebase"

**Multimodal Models**
- Models that handle multiple input types (text, image, audio)
- Examples: GPT-4V, Gemini
- Usage: When discussing vision + language capabilities

### AI Agents & Systems

**AI Agent**
- **Definition:** Autonomous system that perceives, decides, and acts to achieve goals
- **Usage:** Use for systems with agency and decision-making
- **Context:** "Deploy an AI agent to automatically triage customer support tickets"

**Prompt**
- **Definition:** Instructions or input given to an AI model
- **Usage:** Describe user input to LLMs
- **Context:** "Craft clear prompts to get accurate code generation"

**Prompt Engineering**
- **Definition:** The practice of designing effective prompts to get desired outputs
- **Usage:** When discussing optimization of AI interactions
- **Context:** "Effective prompt engineering increases AI output quality by 40%"

**Context Window**
- **Definition:** The amount of text an LLM can process at once
- **Usage:** When discussing model limitations
- **Context:** "GPT-4 has a 128K token context window, enough for large codebases"

**Token**
- **Definition:** Basic unit of text processing (roughly 4 characters or 0.75 words)
- **Usage:** When discussing model capacity or costs
- **Context:** "Processing 1M tokens costs approximately $10 with GPT-4"

### Training & Learning

**Training**
- Process of teaching an ML model using data
- Usage: "Training a model on your company's documentation"

**Fine-tuning**
- Adapting a pre-trained model for specific tasks
- Usage: "Fine-tune GPT-4 on your API documentation"

**Retrieval-Augmented Generation (RAG)**
- **Definition:** Technique where AI retrieves relevant info before generating responses
- **Usage:** When discussing knowledge-enhanced AI systems
- **Context:** "RAG enables AI to access your latest documentation without retraining"

**Embeddings**
- **Definition:** Numerical representations of text that capture semantic meaning
- **Usage:** When discussing semantic search or similarity
- **Context:** "Use embeddings to find similar code snippets in your repository"

**Vector Database**
- **Definition:** Database optimized for storing and searching embeddings
- **Examples:** Pinecone, Weaviate, Qdrant
- **Usage:** When discussing RAG implementations

### Model Performance

**Hallucination**
- **Definition:** When AI generates false or fabricated information
- **Usage:** Address reliability concerns
- **Context:** "Implement verification steps to catch AI hallucinations"

**Accuracy**
- Percentage of correct predictions
- Usage: "The model achieves 95% accuracy on code classification"

**Latency**
- Response time from input to output
- Usage: "Sub-second latency is critical for code completion"

**Throughput**
- Number of requests processed per unit time
- Usage: "The system handles 1000 API calls per minute"

### Common AI Tasks

**Classification**
- Categorizing inputs into predefined categories
- Example: "Bug triage: critical, high, medium, low"

**Generation**
- Creating new content
- Example: "Generate unit tests from function signatures"

**Summarization**
- Condensing long text into key points
- Example: "Summarize meeting notes into action items"

**Translation**
- Converting between languages or formats
- Example: "Translate Python to TypeScript"

**Sentiment Analysis**
- Determining emotional tone
- Example: "Analyze customer feedback sentiment"

### Enterprise AI Terms

**API (Application Programming Interface)**
- How to interact with AI services programmatically
- Usage: "Integrate AI via REST API calls"

**SDK (Software Development Kit)**
- Pre-built libraries for AI integration
- Usage: "Use OpenAI's Python SDK for faster development"

**Inference**
- Running a trained model to get predictions
- Usage: "Real-time inference on production data"

**Model Deployment**
- Making a trained model available for use
- Usage: "Deploy the model to AWS Lambda"

### Cost & Resource Terms

**API Cost**
- Pay-per-use pricing for AI services
- Usage: "GPT-4 costs $30 per 1M input tokens"

**Self-hosted vs. Cloud-hosted**
- **Self-hosted:** Run models on your own infrastructure
- **Cloud-hosted:** Use third-party AI services
- Usage: Compare deployment options

**Vendor Lock-in**
- Dependency on specific AI provider
- Usage: Risk assessment discussions

## Terminology Guidelines

### Consistency Rules
1. **First use:** Always define acronyms: "Large Language Model (LLM)"
2. **Subsequent uses:** Use short form: "The LLM generates..."
3. **Product names:** Keep official capitalization: "GitHub Copilot", "OpenAI GPT-4"
4. **Avoid mixing:** Don't alternate between "AI agent" and "intelligent agent"

### Simplification for Non-Technical Audiences
| Technical Term | Simplified Alternative |
|----------------|------------------------|
| "Fine-tuning" | "Customizing the AI for your needs" |
| "Context window" | "How much information the AI can read at once" |
| "Embeddings" | "AI's understanding of text meaning" |
| "Inference" | "Getting predictions from the AI" |
| "Hallucination" | "When AI makes up incorrect information" |

### Common Mistakes to Avoid
❌ "Artificial intelligence (AI)" → ✓ "Artificial Intelligence (AI)"  
❌ "GPT-4 model" → ✓ "GPT-4" (GPT already means model)  
❌ "AI/ML agent" → ✓ "AI agent" (ML is subset of AI)  
❌ "Machine learning algorithm" → ✓ "Machine learning model" (in context of LLMs)  

## Glossary Template
Maintain a project-wide glossary with:
- **Term:** Official name
- **Definition:** Clear explanation
- **Example:** Real-world usage in FTE+AI context
- **Related terms:** Cross-references
- **See also:** Links to detailed docs

## When to Use Technical vs. Business Language

**Technical Documentation (Developers):**
- Use precise terms: "tokens", "context window", "embeddings"
- Include specifications: "8K context window", "gpt-4-0125-preview"
- Reference APIs and SDKs directly

**Business Documentation (Executives):**
- Use analogies: "AI's memory" instead of "context window"
- Focus on outcomes: "reduces time by 50%" vs. "processes 100K tokens/sec"
- Minimize acronyms

**Hybrid Documentation (R&D Managers):**
- Define terms inline: "The context window (AI's working memory) limits..."
- Balance: Technical accuracy + business value
- Use sidebars for deeper technical details
