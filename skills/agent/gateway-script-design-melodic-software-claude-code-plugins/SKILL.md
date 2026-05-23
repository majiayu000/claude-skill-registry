---
name: gateway-script-design
description: Design gateway scripts as entry points for agentic coding. Use when creating CLI entry points for agents, designing subprocess-based agent invocation, or building script interfaces for agentic workflows.
allowed-tools: Read, Grep, Glob
---

# Gateway Script Design Skill

Guide creation of gateway scripts - the entry points into agentic coding.

## When to Use

- Creating new CLI entry points for agents
- Building programmatic agent invocation
- Designing composed workflows
- Setting up automation scripts

## Core Concept

> "This script is the gateway into agentic coding. It's distinctly different from any other type of code - it's calling an agent."

Gateway scripts move you from conversation to automation.

## Three Gateway Patterns

### Pattern 1: Direct Prompt

Execute ad-hoc prompts:

```python
# adw_prompt.py
@click.command()
@click.argument("prompt")
@click.option("--model", default="opus")
def main(prompt: str, model: str):
    request = AgentPromptRequest(
        prompt=prompt,
        model=model,
        agent_name="oneoff"
    )
    response = prompt_claude_code(request)
```

**Use case:** Quick one-offs, testing, exploration

### Pattern 2: Slash Command Wrapper

Execute slash commands programmatically:

```python
# adw_slash_command.py
@click.command()
@click.argument("command")
@click.argument("args", nargs=-1)
def main(command: str, args: tuple):
    request = AgentTemplateRequest(
        slash_command=f"/{command}",
        args=list(args)
    )
    response = execute_template(request)
```

**Use case:** Scheduled commands, triggers, external integration

### Pattern 3: Composed Workflow

Chain multiple agents:

```python
# adw_chore_implement.py
def main(description: str):
    # Phase 1: Plan
    plan_response = execute_template("/chore", description)
    plan_path = extract_plan_path(plan_response)

    # Phase 2: Implement
    impl_response = execute_template("/implement", plan_path)
    return impl_response
```

**Use case:** Multi-step automation, full workflows

## Design Checklist

### 1. CLI Interface

```python
import click

@click.command()
@click.argument("input", required=True)
@click.option("--model", default="opus", help="Model to use")
@click.option("--verbose", is_flag=True, help="Verbose output")
def main(input: str, model: str, verbose: bool):
    ...
```

### 2. Unique Identification

```python
def generate_short_id() -> str:
    return uuid.uuid4().hex[:8]

adw_id = generate_short_id()  # e.g., "a1b2c3d4"
```

### 3. Output Organization

```python
output_dir = f"agents/{adw_id}/{agent_name}"
os.makedirs(output_dir, exist_ok=True)

output_file = f"{output_dir}/cc_raw_output.jsonl"
```

### 4. Safe Environment

```python
def get_safe_env() -> dict:
    return {
        "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY"),
        "PATH": os.getenv("PATH"),
        # Only essential vars
    }
```

### 5. Error Handling

```python
try:
    response = prompt_claude_code(request)
except TimeoutError:
    log_error("Agent timed out")
    sys.exit(1)
except ExecutionError as e:
    log_error(f"Execution failed: {e}")
    sys.exit(1)
```

### 6. Rich Output

```python
from rich.console import Console
from rich.panel import Panel

console = Console()

console.print(Panel(
    response.output,
    title=f"[bold green]{agent_name}[/]",
    border_style="green"
))
```

## Request/Response Models

```python
class AgentPromptRequest(BaseModel):
    prompt: str
    adw_id: str
    model: str = "opus"
    agent_name: str = "oneoff"
    output_file: Optional[str] = None

class AgentPromptResponse(BaseModel):
    output: str
    success: bool
    error: Optional[str] = None
    output_file: str
```

## Output File Structure

Every gateway produces:

```text
agents/{adw_id}/{agent_name}/
├── cc_raw_output.jsonl     # Streaming messages
├── cc_raw_output.json      # Parsed array
├── cc_final_object.json    # Last message
└── custom_summary.json     # Metadata
```

## Key Memory References

- @gateway-script-patterns.md - Pattern examples
- @agentic-layer-structure.md - Where scripts live
- @programmable-claude-patterns.md - CLI invocation

## Output Format

```markdown
## Gateway Script Design

**Script Name:** adw_{purpose}.py
**Pattern:** [Direct | Wrapper | Composed]

### CLI Interface
- Arguments: {required args}
- Options: --model, --verbose

### Agent Configuration
- Name: {agent_name}
- Model: opus (default)
- Output: agents/{adw_id}/{agent_name}/

### Execution Flow
1. Parse arguments
2. Generate ADW ID
3. Create output directory
4. Build request
5. Execute agent
6. Handle response
7. Display results

### Error Handling
- Timeout: Log and exit 1
- Execution error: Log reason and exit 1
- Success: Display panel with results

### Files Generated
- cc_raw_output.jsonl
- cc_raw_output.json
- cc_final_object.json
- custom_summary.json
```

## Anti-Patterns

- Passing full environment to subprocess
- Not generating unique IDs (collision risk)
- No error handling (silent failures)
- Inline output instead of files (not auditable)
- No CLI interface (hard to use)

## Version History

- **v1.0.0** (2025-12-26): Initial release

---

## Last Updated

**Date:** 2025-12-26
**Model:** claude-opus-4-5-20251101
