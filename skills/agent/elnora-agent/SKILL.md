---
name: elnora-agent
description: >
  This skill should be used when the user asks about "Elnora agent capabilities",
  "what can the agent do", "agent tools", "web search", "academic search",
  "PubMed", "ArXiv", "Exa", "Tavily", "Perplexity", "Valyu", "ToolUniverse",
  "scientific tools", "agent memory", "code execution", "sandbox",
  "search papers", "search literature", "drug discovery", "protein analysis",
  "clinical trials", "file operations", "agent skills",
  or any question about what the Elnora AI Agent can do when you send it a task.
---

# Elnora Agent Capabilities

The Elnora Agent is a sandboxed Python environment with ~78 core tools + 2,100 ToolUniverse scientific tools. Interact via `elnora_create_task` / `elnora_send_message` — describe what you need in plain language, don't reference internal tool names.

## MCP Tools for Agent Interaction

| Tool | Purpose |
|------|---------|
| `elnora_create_task` | Create a task with optional `initial_message` to start generation |
| `elnora_send_message` | Send follow-up message. 30-120s for complex requests. |
| `elnora_get_task_messages` | Read agent responses |
| `elnora_generate_protocol` | Convenience: create task + send message in one call |

## What the Agent Can Do

| Capability | Examples |
|------------|----------|
| **Web search** (34 tools) | Real-time search, neural/semantic search, deep research, URL extraction, site crawling. Providers: Tavily, Exa, Valyu, Perplexity |
| **Academic databases** (12 tools) | PubMed, ArXiv, Semantic Scholar, bioRxiv, Europe PMC, OpenAlex, UniProt, ClinicalTrials.gov, ChEMBL, Wolfram Alpha |
| **2,100+ scientific tools** (ToolUniverse) | Protein structure (AlphaFold, PDB), genomics (Ensembl, ClinVar), chemistry (PubChem, DrugBank), pathways (KEGG, Reactome), drug safety (OpenFDA), and 21 more categories |
| **35 domain skills** | Literature review, experimental design, drug discovery workflow, protein engineering, single-cell RNA QC, statistical analysis, scientific writing |
| **File operations** (11 tools) | Create/read/search files, full-text grep, upload attachments, link files to tasks |
| **Memory** (9 tools) | Remember facts across tasks, share findings between agents, recall prior context |
| **Code execution** | Persistent Python REPL with pandas, numpy, biopython. Variables survive across executions. 30s timeout, 1MB output max |

## Good Prompts

**Web research:**
> "Search for recent CRISPR delivery methods and summarize the top findings"

**Literature review:**
> "Search PubMed for BRCA1 DNA repair papers from 2024, find the most cited ones"

**Drug target research:**
> "Search for compounds targeting EGFR, cross-reference with active clinical trials"

**Scientific computation:**
> "Use ToolUniverse to run AlphaFold on this sequence: MVLSPADKTNVKAAWGKVGA"

**Memory:**
> "Remember that our lab uses Q5 polymerase for all high-fidelity PCR at 62C"

**File search:**
> "Search all project files for mentions of 'annealing temperature' and summarize"

**Reference existing files:**
Use `file_ids` in `elnora_send_message` or `context_file_ids` in `elnora_create_task` to give the agent context about existing protocols.
