---name: biomcp-server
description: Open source biomedical Model Context Protocol (MCP) toolkit for connecting LLMs to biomedical data sources (PubMed, ClinicalTrials, Genomics).
license: MIT
metadata:
  author: LobeHub / GenomOncology
  source: "https://lobehub.com/mcp/genomoncology-biomcp"
  version: "1.0.0"
compatibility:
  - system: MCP-compliant Client (Claude Desktop, BioKernel)
allowed-tools:
  - web_fetch

keywords:
  - biomcp
  - automation
  - biomedical
measurable_outcome: execute task with >95% success rate.
---"

# BioMCP Server

BioMCP is a standardized Model Context Protocol (MCP) server that provides AI agents with direct, structured access to essential biomedical databases and APIs. It acts as a bridge between the LLM and the vast world of biomedical data.

## When to Use This Skill

*   **Literature Search**: When you need to search PubMed or PMC for recent papers.
*   **Entity Normalization**: When you need to map text to gene IDs, disease codes, or chemical IDs (using PubTator3).
*   **Clinical Data**: To search for active clinical trials.
*   **Genomic Information**: To look up variant information or gene summaries.

## Core Capabilities

1.  **PubMed/PMC Search**: Execute complex queries against the NCBI literature databases.
2.  **PubTator3 API**: Annotate biomedical text with normalized entities (Genes, Diseases, Chemicals, Species).
3.  **ClinicalTrials.gov**: Search and retrieve clinical trial protocols.
4.  **Genomic Variants**: Retrieve information about specific genetic variants.

## Workflow

1.  **Connect**: The agent connects to the running BioMCP server.
2.  **Call Tool**: The agent selects the appropriate tool (e.g., `search_pubmed`, `annotate_text`).
3.  **Process**: The server executes the API call and returns structured JSON.
4.  **Response**: The agent uses the data to answer the user's query.

## Example Usage

**User**: "Find recent clinical trials for CAR-T therapy in glioblastoma and list the key inclusion criteria."

**Agent Action**:
1.  Calls `biomcp_search_clinical_trials(query="CAR-T glioblastoma", status="Recruiting")`.
2.  Parses the returned trial JSON.
3.  Extracts and summarizes the inclusion criteria.
