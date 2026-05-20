---
name: libingest
description: >
  libingest - Document ingestion pipeline. IngestPipeline orchestrates
  configurable transformation steps. IngestStep defines individual processors
  like pdf-to-images, images-to-html, extract-context, annotate-html. Converts
  PDF, PowerPoint, images to Schema.org annotated HTML. Use for document
  processing, knowledge extraction, and content transformation.
---

# libingest Skill

## When to Use

- Converting PDF documents to structured HTML
- Processing PowerPoint presentations for indexing
- Extracting semantic content from images via OCR
- Building document ingestion pipelines

## Key Concepts

**IngestPipeline**: Orchestrates a sequence of transformation steps defined in
config/ingest.yml.

**IngestStep**: Individual processing step (pdf-to-images, images-to-html,
extract-context, annotate-html, normalize-html).

## Usage Patterns

### Pattern 1: Run ingestion via CLI

```bash
# Drop files in data/ingest/in/
cp document.pdf data/ingest/in/

# Run pipeline
make ingest
```

### Pattern 2: Programmatic ingestion

```javascript
import { IngestPipeline } from "@copilot-ld/libingest";

const pipeline = new IngestPipeline(config, storage, llmClient);
const result = await pipeline.process("document.pdf");
// result.output points to final HTML
```

## Integration

Configured via config/ingest.yml. Uses libllm for vision processing. Output
stored in data/ingest/pipeline/.
