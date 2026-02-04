---
name: dataset-generator
description: Generate evaluation datasets with adjustable difficulty levels from PDF documents for RAG system testing and benchmarking
version: 1.0.0
author: lana.dominkovic
disable-model-invocation: false
tags:
  - datasets
  - evaluation
  - benchmarking
  - RAG
  - testing
  - pdf
---

# Dataset Generator Skill

Generate high-quality benchmark evaluation datasets with adjustable difficulty levels from custom PDF documents. Perfect for testing RAG systems, knowledge graphs, and Q&A models.

## Usage

Invoke this skill with:
```
/dataset-generator <pdf_directory> [output_file] [num_questions] [difficulty]
```

**Arguments:**
- `$1` (required) - Path to PDF directory containing source documents
- `$2` (optional) - Output JSON file path (default: `benchmark_dataset.json`)
- `$3` (optional) - Number of questions to generate (default: 20)
- `$4` (optional) - Difficulty level: `easy`, `medium`, `hard`, or `mixed` (default: `mixed`)

## Examples

```bash
# Generate 20 mixed-difficulty questions
/dataset-generator ./pdfs

# Generate 30 hard questions
/dataset-generator ./pdfs hard_benchmark.json 30 hard

# Generate 15 easy questions for testing retrieval
/dataset-generator ./pdfs easy_test.json 15 easy
```

## What This Skill Does

1. **Extract Content**: Reads all PDFs from specified directory using pypdf
2. **Analyze Topics**: Uses Claude to identify key concepts, entities, dates, and relationships
3. **Generate Questions**: Creates questions across 5 types:
   - **Fact Retrieval**: Direct facts extractable from single passages
   - **Multi-hop Reasoning**: Requires connecting 2-3 pieces of information
   - **Comparative Analysis**: Compare concepts, approaches, or entities
   - **Contextual Summarization**: Broad understanding across multiple sections
   - **Creative Generation**: Application/scenario-based questions
4. **Difficulty Calibration**: Adjusts question complexity and required reasoning depth
5. **Format Output**: Standard benchmark JSON format with:
   - Question and ground truth answer
   - Question type classification
   - Difficulty level
   - 2-5 supporting evidence passages
   - Evidence relationship explanations

## Difficulty Levels

### Easy (Single-hop, Direct)
- **Reasoning**: Answerable from a single chunk/passage
- **Evidence**: Direct quotes sufficient
- **Chunk Size**: 300-500 chars
- **Examples**:
  - "What is [Product/Service] described in the document?"
  - "Who is mentioned as the CEO in [Year]?"
  - "What is the duration/cost/size of [Feature]?"

### Medium (Multi-hop, Inference)
- **Reasoning**: Requires 2-3 pieces of information
- **Evidence**: Light inference and connection needed
- **Chunk Size**: 800-1000 chars
- **Examples**:
  - "How does [Concept A] affect [Concept B]?"
  - "What are the requirements for [Process/System]?"

### Hard (Synthesis, Cross-document)
- **Reasoning**: Requires synthesizing info across multiple documents
- **Evidence**: Implicit relationships, complex inference
- **Chunk Size**: 1200-1500 chars
- **Examples**:
  - "Compare [Company's] approach in [Document A] vs [Document B]"
  - "Summarize how [System] addresses [Challenge] across all documents"

### Mixed (Balanced Distribution)
- **Distribution**: 40% easy, 40% medium, 20% hard
- **Purpose**: Comprehensive testing across difficulty spectrum
- **Chunk Size**: Adaptive (1000 chars average)

## Output Format

Standard evaluation JSON format:
```json
[
  {
    "id": "unique-hash-id",
    "question": "What is the main product described?",
    "answer": "The main product is a cloud-based solution that provides...",
    "question_type": "Fact Retrieval",
    "difficulty": "easy",
    "evidence": [
      "The product is a cloud-based solution that provides enterprise-grade features...",
      "Key capabilities include real-time processing and analytics..."
    ],
    "evidence_relations": "Evidence 1 defines the product, evidence 2 details key capabilities."
  }
]
```

## Implementation Details

When invoked, execute Python script `generate_benchmark_with_difficulty.py` which:

1. **Load PDFs**: Extract text from all PDFs in directory
2. **Adaptive Chunking**:
   - Easy: 300-500 char chunks
   - Medium: 800-1000 char chunks
   - Hard: 1200-1500 char chunks with 25% overlap
3. **Topic Analysis**: Use Claude to identify:
   - Key entities (companies, products, people, dates)
   - Main concepts and themes
   - Relationships and connections
4. **Question Generation** (Claude-powered):
   - Generate questions matching difficulty requirements
   - Ensure diverse question types
   - Create comprehensive ground truth answers
   - Extract supporting evidence passages
5. **Validation**:
   - Verify evidence supports answer
   - Check answer completeness
   - Validate JSON structure
6. **Output**: Save to specified file with statistics

## Statistics Reported

After generation:
- Total questions generated
- Questions per type breakdown
- Questions per difficulty
- Average answer length
- Average evidence passages per question
- Processing time

## Requirements

- Python 3.8+
- pypdf library (auto-installed if missing)
- Anthropic API key (from environment)
- PDF files in specified directory

## Notes

- For **hard** questions, ensures cross-document synthesis by analyzing multiple PDFs
- For **easy** questions, uses direct extraction with minimal inference
- Always includes 2-5 evidence passages per question
- Validates that evidence actually supports the answer
- Uses unique hash IDs for question tracking
- Compatible with RAGAs and other evaluation frameworks
