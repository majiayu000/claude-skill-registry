---
name: context-compression
description: "Compress selected context to a target token budget while preserving decisions, evidence, constraints, and unresolved questions. Use when relevant material is already selected but too long; use context-optimization when selection, deduplication, and ordering are also required."
license: MIT
metadata:
  author: awesome-ai-agent-skills
  version: "1.0.0"
---

# Context Compression

Context compression is the process of reducing the size of textual context provided to a language model while retaining the information most essential to the task. As conversations grow longer and retrieved documents grow larger, compression becomes critical for staying within token limits and keeping inference costs manageable without sacrificing answer quality.

## Workflow

1. **Measure the Token Budget**: Determine the model's total context window (e.g., 4K, 32K, 128K tokens) and subtract the tokens reserved for the system prompt, instructions, and the model's generation output. The remainder is your available context budget. If the raw context already fits, compression may be unnecessary.

2. **Score Information Density**: Analyze each paragraph, sentence, or chunk of the raw context and assign an information-density score based on how many task-relevant facts it contains per token. Sentences that are purely stylistic, redundant, or off-topic receive low scores. This can be done heuristically (keyword overlap with the query) or via a lightweight classifier.

3. **Select a Compression Strategy**: Choose the most appropriate technique based on the compression ratio needed and the nature of the content:
   - *Extractive summarization* — select the most important sentences verbatim.
   - *Abstractive summarization* — rewrite content in fewer words while preserving meaning.
   - *Key-point extraction* — pull out only named entities, facts, and figures.
   - *Selective pruning* — remove low-density sentences, boilerplate, and repeated information.

4. **Apply Compression**: Execute the chosen strategy. For aggressive compression (>80% reduction), combine techniques — for example, first prune boilerplate, then abstractively summarize the remainder. For moderate compression (40–60%), extractive selection is often sufficient and avoids introducing paraphrasing errors.

5. **Validate Information Retention**: Compare the compressed output against the original to ensure no critical facts were lost. A quick validation pass can check that key entities, numbers, and conclusions from the original are still present in the compressed version.

6. **Assemble the Final Context**: Insert the compressed text into the prompt in place of the raw context. Include a note to the model indicating the context has been summarized, so it can calibrate its confidence accordingly.

## Techniques

- **Extractive Summarization**: Selects the top-n most important sentences from the source text based on relevance scoring. Preserves exact wording, which is important when precision matters (legal, medical, code). Tools: TextRank, LexRank, or LLM-based extraction.
- **Abstractive Summarization**: Generates a new, shorter version of the text that captures the same meaning. Produces more natural and concise output but risks introducing inaccuracies. Best used with a reliable LLM and a validation step.
- **Key-Point Extraction**: Reduces text to a structured list of facts, entities, and data points. Extremely space-efficient (often 90%+ compression) but loses narrative flow and nuance.
- **Selective Pruning**: Removes filler sentences, repeated explanations, greetings, and boilerplate while keeping substantive content intact. Low risk of information loss and easy to implement with rule-based heuristics.
- **Token Budget Management**: Dynamically allocate token budgets across multiple context sources. For example, in a RAG pipeline with 5 retrieved chunks, allocate more tokens to higher-relevance chunks and aggressively compress lower-relevance ones.

## Usage

Provide the raw context text and a target token budget. The skill returns a compressed version of the text that fits within the budget. Optionally specify the compression strategy (extractive, abstractive, key-points, or auto) and a list of must-retain keywords or entities.

## Examples

### Example 1: Compressing a Document for a Q&A Task

**Input (excerpt, ~800 tokens):**
> The Acme Corporation was founded in 1987 by Jane Doe in Austin, Texas. It started as a small consulting firm specializing in environmental compliance. Over the years, the company expanded into waste management technology, receiving its first patent in 1994 for an automated sorting system. By 2005, Acme had grown to 500 employees across 12 offices nationwide. The company went public in 2010 with an IPO price of $18 per share. In 2018, Acme acquired GreenTech Solutions for $240 million, adding recycling automation to its portfolio. As of 2024, Acme reports annual revenue of $1.2 billion and employs 3,400 people. The CEO since 2020 is Michael Chen, who previously served as CTO. Acme's headquarters relocated to Denver, Colorado in 2021. The company's mission statement emphasizes sustainable industrial practices and carbon-neutral operations by 2030.

**Compressed Output (key-point extraction, ~150 tokens):**
> - Acme Corporation: founded 1987 by Jane Doe, Austin TX; now HQ in Denver CO (relocated 2021)
> - Business: environmental compliance consulting → waste management tech → recycling automation
> - Key milestones: first patent 1994 (automated sorting), IPO 2010 ($18/share), acquired GreenTech Solutions 2018 ($240M)
> - Current: CEO Michael Chen (since 2020), 3,400 employees, $1.2B annual revenue
> - Goal: carbon-neutral operations by 2030

### Example 2: Compressing Conversation History

**Input (long-running chat, ~3,000 tokens across 18 messages):**
> User asks about setting up a Python virtual environment. Agent explains venv creation, pip usage, and requirements.txt. User then asks about Docker containerization. Agent explains Dockerfiles, docker-compose, and volume mounts. User encounters a port-binding error. Agent helps debug by checking for conflicting processes. User resolves the issue. User then asks about deploying to AWS ECS.

**Compressed Output (abstractive summary, ~400 tokens):**
> **Conversation summary:** The user is setting up a Python application with Docker and deploying to AWS. Key context:
> 1. Python environment is configured with venv and requirements.txt (resolved).
> 2. Docker setup uses a Dockerfile and docker-compose with volume mounts (resolved).
> 3. A port-binding conflict on port 8080 was resolved by killing a conflicting process.
> 4. **Current topic:** User is now asking about deploying the Dockerized Python app to AWS ECS. They have a working Docker setup locally and need guidance on ECS task definitions, service configuration, and load balancing.

## Best Practices

- **Compress progressively** — apply light pruning first, measure the result, then apply heavier techniques only if you still exceed the budget. This minimizes unnecessary information loss.
- **Preserve numbers and names** — quantitative data, proper nouns, dates, and code identifiers are disproportionately important and should be retained even in aggressive compression.
- **Tag compressed context** — always indicate to the model that the context has been compressed so it can appropriately hedge when details might have been lost.
- **Prefer extractive methods for code** — abstractive summarization can introduce subtle errors in code snippets. Use extractive selection or selective pruning for technical content.
- **Keep the most recent turns** — when compressing conversation history, preserve the last 2–3 turns verbatim and summarize earlier turns. Recency is a strong signal for relevance.
- **Measure information loss** — after compression, check that answers to key questions about the content remain correct. If a fact is lost that the task depends on, the compression was too aggressive.

## Edge Cases

- **Context already within budget**: Skip compression entirely — unnecessary compression always loses some information. Only compress when the raw context exceeds available tokens.
- **Highly technical or structured content**: Tables, JSON, and code blocks compress poorly with abstractive methods. Use selective pruning or extract only the relevant rows/fields rather than summarizing.
- **Multiple languages in context**: Compression models may perform unevenly across languages. Compress each language segment independently or use a multilingual summarization model.
- **Critical safety information**: Never compress away safety warnings, legal disclaimers, or medical dosage information. Mark these as must-retain before applying any compression.
- **Near-budget context**: If the context is only 10–15% over budget, simple pruning of whitespace, boilerplate headers, and duplicate sentences is safer than full summarization.
