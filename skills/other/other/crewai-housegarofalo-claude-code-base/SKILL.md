---
name: crewai
description: Build multi-agent AI systems with CrewAI. Create autonomous agents with roles, tools, and collaborative workflows. Use for complex task automation, research teams, and orchestrated AI agent systems.
---

# CrewAI

Expert guidance for building multi-agent AI systems.

## Triggers

Use this skill when:
- Building multi-agent AI systems
- Creating autonomous agents with roles and tools
- Implementing collaborative AI workflows
- Working with research or analysis teams of AI agents
- Orchestrating complex task automation with multiple agents
- Keywords: crewai, multi-agent, crew, agent, task, autonomous, orchestration

## Installation

```bash
pip install crewai crewai-tools
```

## Basic Concepts

### Agents

```python
from crewai import Agent, LLM

# Define LLM
llm = LLM(
    model="openai/gpt-4o",
    temperature=0.7
)

# Create agent
researcher = Agent(
    role="Senior Research Analyst",
    goal="Uncover cutting-edge developments in AI and data science",
    backstory="""You work at a leading tech think tank.
    Your expertise lies in identifying emerging trends and technologies.
    You have a knack for dissecting complex data and presenting
    actionable insights.""",
    verbose=True,
    allow_delegation=False,
    llm=llm,
    tools=[search_tool, scrape_tool]
)

writer = Agent(
    role="Tech Content Writer",
    goal="Write compelling content about AI advancements",
    backstory="""You are a renowned content writer specializing in
    technology and AI. You transform complex concepts into engaging
    narratives that educate and inspire.""",
    verbose=True,
    allow_delegation=True,
    llm=llm
)
```

### Tasks

```python
from crewai import Task

research_task = Task(
    description="""Conduct comprehensive research on the latest
    developments in AI agents technology in 2024.
    Focus on identifying key trends, breakthrough technologies,
    and potential industry impacts.""",
    expected_output="""A detailed 3-paragraph report covering:
    1. Main AI agent frameworks and their capabilities
    2. Key use cases and applications
    3. Future predictions and challenges""",
    agent=researcher,
    tools=[search_tool]
)

write_task = Task(
    description="""Using the research findings, write a blog post
    about AI agents that is engaging and accessible to a technical
    audience. The post should be informative yet engaging.""",
    expected_output="A 4-paragraph blog post in markdown format",
    agent=writer,
    context=[research_task]  # Depends on research task
)
```

### Crew

```python
from crewai import Crew, Process

crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task],
    process=Process.sequential,  # or Process.hierarchical
    verbose=True
)

# Run the crew
result = crew.kickoff()
print(result)
```

## Tools

### Built-in Tools

```python
from crewai_tools import (
    SerperDevTool,
    ScrapeWebsiteTool,
    FileReadTool,
    DirectoryReadTool,
    CodeInterpreterTool,
    PDFSearchTool,
    YoutubeVideoSearchTool
)

# Search tool
search_tool = SerperDevTool()

# Web scraping
scrape_tool = ScrapeWebsiteTool()

# File operations
file_tool = FileReadTool(file_path="data.txt")
dir_tool = DirectoryReadTool(directory="./documents")

# Code execution
code_tool = CodeInterpreterTool()

# PDF search
pdf_tool = PDFSearchTool(pdf="report.pdf")
```

### Custom Tools

```python
from crewai.tools import BaseTool
from pydantic import Field

class CalculatorTool(BaseTool):
    name: str = "Calculator"
    description: str = "Useful for performing mathematical calculations"

    def _run(self, expression: str) -> str:
        try:
            result = eval(expression)
            return str(result)
        except Exception as e:
            return f"Error: {str(e)}"

class DatabaseTool(BaseTool):
    name: str = "Database Query"
    description: str = "Query the database for information"
    connection_string: str = Field(default="")

    def _run(self, query: str) -> str:
        # Execute database query
        return execute_query(self.connection_string, query)

# Use tools
calculator = CalculatorTool()
db_tool = DatabaseTool(connection_string="postgresql://...")
```

### Function-based Tools

```python
from crewai.tools import tool

@tool("Weather Lookup")
def weather_tool(city: str) -> str:
    """Look up current weather for a city."""
    # API call to weather service
    return f"Weather in {city}: 72°F, Sunny"

@tool("Stock Price")
def stock_tool(symbol: str) -> str:
    """Get current stock price for a symbol."""
    # API call to stock service
    return f"{symbol}: $150.00"
```

## Advanced Patterns

### Hierarchical Process

```python
from crewai import Crew, Process, Agent

manager = Agent(
    role="Project Manager",
    goal="Coordinate the team to deliver high-quality results",
    backstory="Experienced manager who ensures efficient collaboration",
    allow_delegation=True
)

crew = Crew(
    agents=[researcher, writer, editor],
    tasks=[research_task, write_task, edit_task],
    process=Process.hierarchical,
    manager_agent=manager,  # Or use manager_llm
    verbose=True
)
```

### Task Callbacks

```python
def task_callback(output):
    print(f"Task completed with output: {output.raw}")
    # Save to database, send notification, etc.

task = Task(
    description="Research AI trends",
    expected_output="Research report",
    agent=researcher,
    callback=task_callback
)
```

### Memory

```python
from crewai import Crew

crew = Crew(
    agents=[agent1, agent2],
    tasks=[task1, task2],
    memory=True,  # Enable memory
    embedder={
        "provider": "openai",
        "config": {"model": "text-embedding-3-small"}
    }
)
```

### Async Execution

```python
import asyncio
from crewai import Crew

async def run_crew():
    crew = Crew(
        agents=[researcher, writer],
        tasks=[research_task, write_task],
        verbose=True
    )

    result = await crew.kickoff_async()
    return result

# Run
result = asyncio.run(run_crew())
```

## Configuration

### YAML Configuration

```yaml
# agents.yaml
researcher:
  role: "Senior Research Analyst"
  goal: "Uncover cutting-edge developments"
  backstory: "Expert at identifying trends"
  tools:
    - search_tool
    - scrape_tool

writer:
  role: "Tech Content Writer"
  goal: "Write compelling content"
  backstory: "Renowned content writer"
```

```yaml
# tasks.yaml
research_task:
  description: "Research latest AI developments"
  expected_output: "Detailed research report"
  agent: researcher

write_task:
  description: "Write blog post from research"
  expected_output: "Blog post in markdown"
  agent: writer
  context:
    - research_task
```

```python
from crewai import Crew
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class MyCrew:
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def researcher(self) -> Agent:
        return Agent(config=self.agents_config["researcher"])

    @task
    def research_task(self) -> Task:
        return Task(config=self.tasks_config["research_task"])

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential
        )
```

## LLM Configuration

```python
from crewai import LLM

# OpenAI
openai_llm = LLM(model="openai/gpt-4o", temperature=0.7)

# Anthropic
claude_llm = LLM(model="anthropic/claude-3-5-sonnet-20241022")

# Ollama (local)
ollama_llm = LLM(
    model="ollama/llama3.1",
    base_url="http://localhost:11434"
)

# Azure OpenAI
azure_llm = LLM(
    model="azure/gpt-4o",
    api_key="your-api-key",
    base_url="https://your-resource.openai.azure.com"
)
```

## Example: Research Team

```python
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool, ScrapeWebsiteTool

# Tools
search = SerperDevTool()
scrape = ScrapeWebsiteTool()

# Agents
researcher = Agent(
    role="Research Analyst",
    goal="Find and analyze information",
    backstory="Expert researcher with attention to detail",
    tools=[search, scrape],
    verbose=True
)

analyst = Agent(
    role="Data Analyst",
    goal="Analyze data and extract insights",
    backstory="Expert in data analysis and visualization",
    verbose=True
)

writer = Agent(
    role="Report Writer",
    goal="Create comprehensive reports",
    backstory="Skilled technical writer",
    verbose=True
)

# Tasks
research = Task(
    description="Research {topic} thoroughly",
    expected_output="Comprehensive research notes",
    agent=researcher
)

analyze = Task(
    description="Analyze the research findings",
    expected_output="Key insights and trends",
    agent=analyst,
    context=[research]
)

report = Task(
    description="Write final report",
    expected_output="Professional report document",
    agent=writer,
    context=[research, analyze]
)

# Crew
crew = Crew(
    agents=[researcher, analyst, writer],
    tasks=[research, analyze, report],
    process=Process.sequential,
    verbose=True
)

# Execute
result = crew.kickoff(inputs={"topic": "AI Agents in 2024"})
```

## Resources

- [CrewAI Documentation](https://docs.crewai.com/)
- [CrewAI GitHub](https://github.com/crewAIInc/crewAI)
- [CrewAI Tools](https://github.com/crewAIInc/crewAI-tools)
