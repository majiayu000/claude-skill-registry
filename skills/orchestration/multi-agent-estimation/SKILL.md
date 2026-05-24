---
name: multi-agent-estimation
description: "Build multi-agent AI systems for construction estimation. Use CrewAI/LangGraph to orchestrate specialized agents: QTO agent, pricing agent, validation agent. Automate complex estimation workflows."
---

# Multi-Agent Estimation System

## Overview

In 2026, AI agents are moving from single-task assistants to orchestrated multi-agent systems. This skill enables building a crew of specialized AI agents that work together to automate construction estimation.

> "Thanks to LLM nodes, you can simply ask ChatGPT, Claude, or any advanced AI assistant to generate n8n automation pipelines — whether for extracting tables from PDFs, validating parameters, or producing custom QTO tables — and get ready-to-run workflows in seconds." — Artem Boiko

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    MULTI-AGENT ESTIMATION                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐     │
│  │  QTO     │   │ Pricing  │   │Validation│   │  Report  │     │
│  │  Agent   │──▶│  Agent   │──▶│  Agent   │──▶│  Agent   │     │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘     │
│       │              │              │              │            │
│       ▼              ▼              ▼              ▼            │
│   Extract        Match to       Validate       Generate        │
│   quantities     CWICR DB       totals         Excel/PDF       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Quick Start with CrewAI

```python
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI

# Initialize LLM
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# QTO Agent - Extracts quantities from documents
qto_agent = Agent(
    role="Quantity Takeoff Specialist",
    goal="Extract accurate quantities from IFC models and PDF drawings",
    backstory="""You are an expert quantity surveyor with 20 years of
    experience in construction. You meticulously extract volumes, areas,
    and counts from building models and drawings.""",
    llm=llm,
    verbose=True
)

# Pricing Agent - Matches items to price database
pricing_agent = Agent(
    role="Cost Estimator",
    goal="Match extracted quantities to CWICR database and apply unit rates",
    backstory="""You are a senior estimator who knows construction costs
    inside out. You match work items to standardized codes and apply
    appropriate unit rates based on project location and conditions.""",
    llm=llm,
    verbose=True
)

# Validation Agent - Checks for errors and outliers
validation_agent = Agent(
    role="Quality Assurance Specialist",
    goal="Validate estimate accuracy and flag potential errors",
    backstory="""You review estimates for completeness, accuracy, and
    reasonableness. You catch errors that others miss and ensure
    estimates are defensible.""",
    llm=llm,
    verbose=True
)

# Report Agent - Generates final deliverables
report_agent = Agent(
    role="Report Generator",
    goal="Create professional estimate reports in Excel and PDF",
    backstory="""You transform raw estimate data into polished,
    professional reports that clients can understand and trust.""",
    llm=llm,
    verbose=True
)
```

## Define Tasks

```python
# Task 1: Extract quantities from IFC
qto_task = Task(
    description="""
    Extract all quantities from the provided IFC model:
    - Walls: volumes, areas, lengths
    - Slabs: areas, volumes
    - Columns: counts, volumes
    - Beams: lengths, volumes

    Group by building level and element type.
    Output as structured JSON.
    """,
    expected_output="JSON with quantities grouped by level and type",
    agent=qto_agent
)

# Task 2: Match to price database
pricing_task = Task(
    description="""
    For each extracted quantity:
    1. Match to CWICR code using semantic search
    2. Apply unit rate from price database
    3. Calculate line item totals
    4. Add markup percentages (OH&P, contingency)

    Output detailed cost breakdown.
    """,
    expected_output="Cost breakdown with CWICR codes and totals",
    agent=pricing_agent,
    context=[qto_task]
)

# Task 3: Validate estimate
validation_task = Task(
    description="""
    Review the estimate for:
    - Missing scope items
    - Unrealistic unit rates (compare to historical)
    - Math errors
    - Inconsistent quantities

    Flag any issues with severity rating.
    """,
    expected_output="Validation report with issues and severity",
    agent=validation_agent,
    context=[pricing_task]
)

# Task 4: Generate report
report_task = Task(
    description="""
    Generate professional estimate report:
    - Executive summary with total
    - Detailed breakdown by CSI division
    - Assumptions and exclusions
    - Risk items identified during validation

    Format for Excel export.
    """,
    expected_output="Formatted estimate report ready for export",
    agent=report_agent,
    context=[pricing_task, validation_task]
)
```

## Run the Crew

```python
# Create the crew
estimation_crew = Crew(
    agents=[qto_agent, pricing_agent, validation_agent, report_agent],
    tasks=[qto_task, pricing_task, validation_task, report_task],
    verbose=True
)

# Execute
result = estimation_crew.kickoff(inputs={
    "ifc_path": "building.ifc",
    "price_db": "cwicr_prices.xlsx",
    "project_location": "Berlin, Germany"
})

print(result)
```

## n8n Integration

```json
{
  "workflow": "Multi-Agent Estimation",
  "nodes": [
    {
      "name": "Trigger",
      "type": "Webhook",
      "note": "Receive IFC file upload"
    },
    {
      "name": "QTO Agent",
      "type": "AI Agent",
      "model": "gpt-4o",
      "tools": ["ifcopenshell", "pandas"]
    },
    {
      "name": "Pricing Agent",
      "type": "AI Agent",
      "model": "gpt-4o",
      "tools": ["qdrant_search", "cwicr_api"]
    },
    {
      "name": "Validation Agent",
      "type": "AI Agent",
      "model": "gpt-4o",
      "tools": ["historical_db", "outlier_detection"]
    },
    {
      "name": "Generate Excel",
      "type": "Spreadsheet",
      "operation": "create"
    },
    {
      "name": "Send Email",
      "type": "Email",
      "to": "estimator@company.com"
    }
  ]
}
```

## Why Multi-Agent in 2026?

| Single Agent | Multi-Agent |
|--------------|-------------|
| One prompt, one task | Specialized experts collaborate |
| Context limits | Distributed memory |
| Single point of failure | Redundancy and validation |
| Hard to debug | Clear responsibility |
| Generic output | Domain-specific quality |

## Requirements

```bash
pip install crewai langchain-openai ifcopenshell pandas qdrant-client
```

## Resources

- CrewAI: https://www.crewai.com
- LangGraph: https://langchain-ai.github.io/langgraph/
- n8n AI Agents: https://docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/n8n-nodes-langchain.agent/
