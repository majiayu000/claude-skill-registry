---
name: recursive-decomposition
description: "Handle tasks that exceed the context window by decomposing them: size and filter the input, chunk it, run recursive sub-agents on independent parts, verify on small windows, and synthesise programmatically, following the Recursive Language Models (RLM) research by Zhang, Kraska and Khattab (2025). Use when a task spans 10+ files or 50k+ tokens, or when asked to analyze all files, process a large document, aggregate information from many sources, or search across a codebase. Triggers: long context, context rot, large codebase, many files, big document, multi-document, aggregate, summarize everything, codebase-wide, recursive, sub-agents, map-reduce."
license: MIT
metadata:
  author: massimodeluisa
  version: "1.1.0"
  paper: https://arxiv.org/abs/2512.24601
---

# Recursive Decomposition

Long inputs degrade model quality: details get missed, distant parts get linked by guesswork, reasoning drifts. The RLM paper calls it context rot. Instead of loading everything into the context window, treat the input as an environment you query with tools: size it, narrow it, split it, delegate independent parts to sub-agents, verify on small windows, and merge results programmatically. Based on [Recursive Language Models](https://arxiv.org/abs/2512.24601) (Zhang, Kraska, Khattab, 2025).

## How to use

- `/recursive-decomposition`: apply the protocol below to the current task.
- `/recursive-decomposition <path or question>`: size that input first, then run the protocol on it.

## When it applies

| Situation | Approach |
|-----------|----------|
| 10+ files, 50k+ tokens, or a multi-hop question across scattered sources | Decompose (this skill) |
| 30k to 50k tokens | Decompose when completeness matters; otherwise read directly |
| Under 30k tokens, one file, or a localized answer | Read directly |

## Protocol

1. **Size the input** before reading anything: count files (glob, `find`), lines (`wc -l`), bytes (`ls -lh`), pages for PDFs.
2. **Filter** the search space with searches (content search, file patterns, keywords, file types) before opening any file. Chain filters: file type, then keyword, then meaning.
3. **Chunk** what remains: natural units (functions, classes, sections), line ranges, or keyword partitions. Batches of 5 to 10 files.
4. **Recurse**: give each independent batch to a sub-agent with a self-contained brief (files, question, output schema); run batches in parallel.
5. **Verify** the synthesised answer on a smaller window: extract the minimal evidence and re-check it; settle disagreements with a targeted re-read.
6. **Synthesise programmatically**: aggregate the structured results, deduplicate, categorise, then write the answer with file and line references.

## Rules

- MUST size the input before reading it
- MUST search before reading a directory; NEVER list a tree recursively as a substitute for search
- MUST read large files by line range: over 2,000 lines or 50 KB never in one read; PDFs over 100 pages or 30 MB by metadata or split
- NEVER load more than 5 files into the main context without a written batch plan
- MUST give every sub-agent its own context: the files, the question, the output schema
- MUST spot-check the synthesised result against the sources before answering
- SHOULD read definitions first (`grep -n "function"`) and bodies later; tables of contents and abstracts before full text
- NEVER run the same query over the same content in several sub-agents; partition once into disjoint batches

## Tools, agent-agnostic

| Need | Use |
|------|-----|
| Find files | the file search or glob tool, or `find` |
| Find content | the content search or grep tool, never a full read |
| Size | `wc -l`, `ls -lh`, page count |
| Read | the file reader with an offset and a limit, or `sed -n 'START,ENDp'` |
| Delegate | the sub-agent or task tool, one brief per batch |
| Aggregate | a scratch file or structured notes, then one final pass |

Tool names differ between agents (Claude Code, Codex, Cursor, Gemini CLI); map the row to your agent's equivalent.

## Patterns

### Codebase analysis

"Find all error handling patterns." Glob the source files, grep `catch|throw|Error|except`, batch the matches by module (5 to 10 files), one sub-agent per batch with a fixed report schema, merge into a categorised summary with file references. Worked example: [references/codebase-analysis.md](references/codebase-analysis.md).

### Multi-document question answering

"What features are planned across all PRDs?" Glob the documents, size them, define an extraction schema (name, priority, status, quarter), one sub-agent per document group, deduplicate and categorise, spot-check three entries against the sources. Worked example: [references/document-aggregation.md](references/document-aggregation.md).

### Aggregation

"Summarise all TODO comments." Grep `TODO|FIXME|HACK`, group by module, extract context and priority per group, produce a prioritised list.

### Long output

Split the output into sections, generate each independently, store intermediate results in a file, stitch them with a coherence pass.

## Cost and quality

Decomposition spends coordination tokens and keeps quality: in the RLM paper, RLM runs were about 3x cheaper than summarisation baselines and scaled from 2^14 to 2^18 tokens with higher accuracy on multi-hop tasks. Thresholds and break-even: [references/cost-analysis.md](references/cost-analysis.md).

## Anti-patterns

| Anti-pattern | Fix |
|--------------|-----|
| Reading everything first "to get context" | Size, filter, then read by range |
| Decomposing a five-file task | Read directly |
| Sub-agents without the question or the schema | Self-contained briefs |
| Trusting the merged answer | Spot-check on a small window |
| Re-querying the same content in several sub-agents | Partition once, disjoint batches |

## References

- [references/rlm-strategies.md](references/rlm-strategies.md): decomposition strategies from the paper
- [references/cost-analysis.md](references/cost-analysis.md): when to decompose, break-even thresholds
- [references/codebase-analysis.md](references/codebase-analysis.md): worked example, error handling across a codebase
- [references/document-aggregation.md](references/document-aggregation.md): worked example, feature extraction across PRDs
- Paper: [Recursive Language Models](https://arxiv.org/abs/2512.24601), Zhang, Kraska, Khattab, arXiv:2512.24601
