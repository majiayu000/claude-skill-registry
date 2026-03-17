---
name: data-flow
description: Rooms as pipeline nodes, exits as edges, objects as messages
allowed-tools:
  - read_file
  - write_file
  - run_terminal_cmd
tier: 2
protocol: DATA-FLOW
tags: [moollm, pipeline, processing, kilroy, messaging]
related: [room, card, sister-script, coherence-engine]
---

# Data Flow

> *"Rooms are nodes. Exits are edges. Thrown objects are messages."*

MOOLLM's approach to building processing pipelines using rooms and objects. The filesystem IS the data flow network.

## The Pattern

- **Rooms** are processing stages (nodes)
- **Exits** connect stages (edges)
- **Objects** flow through as messages
- **THROW** sends objects through exits
- **INBOX** receives incoming objects
- **OUTBOX** stages outgoing objects

## Commands

| Command | Effect |
|---------|--------|
| `THROW obj exit` | Send object through exit to destination |
| `INBOX` | List items waiting to be processed |
| `NEXT` | Get next item from inbox (FIFO) |
| `PEEK` | Look at next item without removing |
| `STAGE obj exit` | Add object to outbox for later throw |
| `FLUSH` | Throw all staged objects |
| `FLUSH exit` | Throw staged objects for specific exit |

## Room Structure

```
stage/
├── ROOM.yml       # Config and processor definition
├── inbox/         # Incoming queue (FIFO)
├── outbox/        # Staged for batch throwing
└── door-next/     # Exit to next stage
```

## Processor Types

### Script (Deterministic)

```yaml
processor:
  type: script
  command: "python parse.py ${input}"
```

### LLM (Semantic)

```yaml
processor:
  type: llm
  prompt: |
    Analyze this document:
    - Extract key entities
    - Summarize in 3 sentences
```

### Hybrid

```yaml
processor:
  type: hybrid
  pre_process: "extract.py ${input}"
  llm_prompt: "Analyze extracted data"
  post_process: "format.py ${output}"
```

**Mix and match.** LLM for reasoning, scripts for transformation.

## Example Pipeline

```
uploads/              # Raw files land here
├── inbox/
│   ├── doc-001.pdf
│   └── doc-002.pdf
└── door-parser/

parser/               # Extract text
├── script: parse.py
└── door-analyzer/

analyzer/             # LLM analyzes
├── prompt: "Summarize..."
├── door-output/
└── door-errors/

output/               # Final results
└── inbox/
    ├── doc-001-summary.yml
    └── doc-002-summary.yml
```

## Processing Loop

```
> ENTER parser
Inbox: 2 items waiting.

> NEXT
Processing doc-001.pdf...
Text extracted.

> STAGE doc-001.txt door-analyzer
Staged.

> FLUSH
Throwing 2 items through door-analyzer...
```

## Fan-Out (one-to-many)

```yaml
routing_rules:
  - if: "priority == 'high'"
    throw_to: door-fast-track
  - if: "type == 'archive'"
    throw_to: door-archive
  - default: door-standard
```

## Fan-In (many-to-one)

```yaml
batch_size: 10
on_batch_complete: |
  Combine all results
  Generate summary report
  THROW report.yml door-output
```

## Kilroy Mapping

| MOOLLM | Kilroy |
|--------|--------|
| Room | Node |
| Exit | Edge |
| THROW | Message passing |
| inbox/ | Input queue |
| Script processor | Deterministic module |
| LLM processor | LLM node |
