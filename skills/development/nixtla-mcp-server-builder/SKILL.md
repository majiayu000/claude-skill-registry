---
name: nixtla-mcp-server-builder
description: Generate production-ready MCP server implementations from PRD tool specifications with schema validation, error handling, and testing infrastructure. Use when building MCP servers for Nixtla plugins, implementing tool handlers, or scaffolding server infrastructure. Trigger with 'build MCP server', 'generate MCP implementation', or 'scaffold MCP tools'.
allowed-tools: "Write,Read,Glob,Bash(python:*),Bash(mkdir:*)"
version: "1.0.0"
author: "Jeremy Longshore <jeremy@intentsolutions.io>"
license: MIT
---

# Nixtla MCP Server Builder

## Purpose

Generate complete, production-ready MCP (Model Context Protocol) server implementations from PRD tool specifications, enabling rapid development of Claude Code plugin backends.

## Overview

This skill automates MCP server development by:
- Parsing PRD documents to extract MCP tool definitions
- Generating Python MCP server implementation with tool handlers
- Creating input/output schema validation using Pydantic
- Implementing error handling and logging
- Generating test suites for all tools
- Creating server configuration (JSON schema)
- Scaffolding deployment infrastructure

**Key Benefits**:
- Reduces MCP server development time from 6-8 hours to 10 minutes
- Ensures consistent server architecture across all plugins
- Auto-generates boilerplate code (validators, error handlers, tests)
- Implements MCP specification best practices

## Prerequisites

- PRD document with MCP Server Tools section (FR-X format)
- Python 3.10+ installed
- MCP SDK (`pip install mcp`)
- Pydantic for schema validation (`pip install pydantic`)

**Expected PRD Structure**:
```markdown
## Functional Requirements

### FR-X: MCP Server Tools
Expose N tools to Claude Code:
1. `tool_name` - Tool description
2. `another_tool` - Another description
...
```

## Instructions

### Step 1: Parse PRD for Tool Definitions

The script automatically:
1. Reads PRD markdown file
2. Extracts MCP tool names and descriptions
3. Infers input/output schemas from tool descriptions
4. Generates Pydantic models for validation

**Usage**:
```bash
python {baseDir}/scripts/build_mcp_server.py \
    --prd /path/to/PRD.md \
    --output /path/to/mcp_server/ \
    --plugin-name nixtla-plugin-name
```

### Step 2: Generate Server Implementation

Creates complete MCP server with:

**mcp_server.py** - Main server implementation:
```python
from mcp.server import Server
from mcp.server.stdio import stdio_server
from pydantic import BaseModel

# Tool schemas
class ToolNameInput(BaseModel):
    param1: str
    param2: int = 14

class ToolNameOutput(BaseModel):
    status: str
    result: dict

# Server initialization
app = Server("plugin-name")

@app.call_tool()
async def tool_name(arguments: dict) -> dict:
    """Tool description from PRD"""
    # Validate input
    input_data = ToolNameInput(**arguments)

    # TODO: Implement tool logic
    result = {"data": "placeholder"}

    # Return validated output
    return ToolNameOutput(
        status="success",
        result=result
    ).dict()
```

**Key Features**:
- Async/await support for all tools
- Pydantic schema validation
- Type hints throughout
- Docstrings from PRD descriptions
- Error handling with informative messages
- Logging for debugging

### Step 3: Generate Tool Handler Stubs

For each tool, creates handler stub with:
- Input validation (Pydantic model)
- TODO comment for implementation logic
- Output schema enforcement
- Error handling template

**Example Handler**:
```python
@app.call_tool()
async def calculate_roi(arguments: dict) -> dict:
    """Calculate ROI comparing TimeGPT vs. build-in-house."""
    try:
        # Validate input
        input_data = CalculateRoiInput(**arguments)

        # TODO: Implement ROI calculation logic
        # 1. Parse input parameters
        # 2. Calculate 5-year TCO
        # 3. Generate comparison metrics

        # Placeholder result
        result = {
            "roi": 245.0,
            "payback_months": 6,
            "total_savings": 500000
        }

        # Return validated output
        return CalculateRoiOutput(
            status="success",
            roi_percentage=result["roi"],
            details=result
        ).dict()

    except ValidationError as e:
        return {"status": "error", "message": str(e)}
    except Exception as e:
        logging.error(f"calculate_roi failed: {e}")
        return {"status": "error", "message": "Internal server error"}
```

### Step 4: Create Schema Validation

Generates Pydantic models for all tools:

**schemas.py**:
```python
from pydantic import BaseModel, Field
from typing import Optional, List, Dict

class CalculateRoiInput(BaseModel):
    """Input schema for calculate_roi tool."""
    current_infrastructure_cost: float = Field(..., description="Annual cost in USD")
    forecast_volume: int = Field(..., description="Number of series to forecast")
    team_size: int = Field(default=0, description="Current data science team size")

class CalculateRoiOutput(BaseModel):
    """Output schema for calculate_roi tool."""
    status: str
    roi_percentage: float
    payback_months: int
    details: Dict
```

### Step 5: Generate Test Suite

Creates comprehensive test suite:

**test_mcp_server.py**:
```python
import pytest
from mcp_server import app, calculate_roi

class TestCalculateRoiTool:
    """Test calculate_roi MCP tool."""

    @pytest.mark.asyncio
    async def test_valid_input(self):
        """Test with valid ROI calculation inputs."""
        result = await calculate_roi({
            "current_infrastructure_cost": 100000,
            "forecast_volume": 1000,
            "team_size": 5
        })
        assert result["status"] == "success"
        assert "roi_percentage" in result

    @pytest.mark.asyncio
    async def test_invalid_input(self):
        """Test with missing required fields."""
        result = await calculate_roi({})
        assert result["status"] == "error"

    @pytest.mark.asyncio
    async def test_edge_cases(self):
        """Test edge cases (zero cost, large volumes)."""
        result = await calculate_roi({
            "current_infrastructure_cost": 0,
            "forecast_volume": 1000000
        })
        assert result["status"] == "success"
```

### Step 6: Generate Server Configuration

Creates plugin.json for server metadata:

```json
{
  "name": "nixtla-plugin-name",
  "version": "0.1.0",
  "description": "Plugin description from PRD",
  "mcp_server": {
    "command": "python",
    "args": ["mcp_server.py"],
    "env": {
      "NIXTLA_API_KEY": "${NIXTLA_API_KEY}"
    }
  },
  "tools": [
    {
      "name": "calculate_roi",
      "description": "Calculate ROI comparing TimeGPT vs. build-in-house",
      "inputSchema": {
        "type": "object",
        "properties": {
          "current_infrastructure_cost": {"type": "number"},
          "forecast_volume": {"type": "integer"}
        },
        "required": ["current_infrastructure_cost", "forecast_volume"]
      }
    }
  ]
}
```

### Step 7: Create Deployment Files

Generates supporting files:

**requirements.txt**:
```
mcp>=1.0.0
pydantic>=2.0.0
python-dotenv>=1.0.0
```

**README.md**:
```markdown
# Plugin MCP Server

## Installation
pip install -r requirements.txt

## Running
python mcp_server.py

## Testing
pytest test_mcp_server.py -v
```

**.env.example**:
```bash
NIXTLA_API_KEY=nixak-your-api-key-here
```

## Output

The script generates:
1. **mcp_server.py** - Main server implementation (200-500 lines)
2. **schemas.py** - Pydantic validation models
3. **test_mcp_server.py** - Comprehensive test suite
4. **plugin.json** - MCP server configuration
5. **requirements.txt** - Python dependencies
6. **README.md** - Server documentation
7. **.env.example** - Environment variable template

**Directory Structure**:
```
mcp_server/
├── mcp_server.py          # Main server
├── schemas.py             # Validation schemas
├── test_mcp_server.py     # Tests
├── plugin.json            # Configuration
├── requirements.txt       # Dependencies
├── README.md             # Documentation
└── .env.example          # Environment template
```

## Error Handling

**Missing PRD File**:
```
Error: PRD not found at /path/to/PRD.md
Solution: Verify PRD path and ensure file exists
```

**No MCP Tools Found**:
```
Warning: No MCP tools section found in PRD
Solution: Ensure PRD has "### FR-X: MCP Server Tools" section
```

**Invalid Tool Definition**:
```
Error: Tool 'calculate_roi' missing description
Solution: Ensure all tools have format: `tool_name` - Description
```

**Server Startup Failure**:
```
Error: MCP server failed to start on port 3000
Solution: Check port availability, verify dependencies installed
```

## Examples

### Example 1: Generate Complete MCP Server

```bash
python {baseDir}/scripts/build_mcp_server.py \
    --prd 000-docs/000a-planned-plugins/implemented/nixtla-roi-calculator/02-PRD.md \
    --output 005-plugins/nixtla-roi-calculator/mcp_server \
    --plugin-name nixtla-roi-calculator \
    --verbose
```

**Output**:
```
✓ Parsed PRD: Found 4 MCP tools
  - calculate_roi
  - generate_report
  - compare_scenarios
  - export_salesforce
✓ Generated mcp_server.py (412 lines)
✓ Generated schemas.py (8 Pydantic models)
✓ Generated test_mcp_server.py (16 test functions)
✓ Generated plugin.json
✓ Generated supporting files (README, requirements.txt, .env.example)

Server ready! Start with: python mcp_server.py
```

### Example 2: Dry Run (Preview Without Writing)

```bash
python {baseDir}/scripts/build_mcp_server.py \
    --prd PRD.md \
    --output mcp_server/ \
    --dry-run
```

**Output**:
```
[DRY RUN] Would generate:
  - mcp_server/mcp_server.py (estimate: 350 lines)
  - mcp_server/schemas.py (4 tools, 8 models)
  - mcp_server/test_mcp_server.py (12 test functions)
  - mcp_server/plugin.json
  - mcp_server/README.md
  - mcp_server/requirements.txt
  - mcp_server/.env.example
```

### Example 3: Generate Minimal Server (No Tests)

```bash
python {baseDir}/scripts/build_mcp_server.py \
    --prd PRD.md \
    --output mcp_server/ \
    --no-tests
```

### Example 4: Update Existing Server

```bash
python {baseDir}/scripts/build_mcp_server.py \
    --prd updated_PRD.md \
    --output existing_mcp_server/ \
    --update \
    --backup
```

**Output**:
```
⚠️  Existing server detected. Creating backup...
✓ Backup created: existing_mcp_server.backup.20251221_223000/
✓ Updated mcp_server.py (added 2 new tools)
✓ Updated schemas.py (added 4 new models)
✓ Updated test_mcp_server.py (added 8 new tests)
```

## Best Practices

1. **Review Generated Code**: Always review and customize generated tool handlers
2. **Implement TODO Logic**: Replace placeholder logic with actual implementation
3. **Test Thoroughly**: Run pytest suite before deploying
4. **Validate Schemas**: Use Pydantic models to catch type errors early
5. **Handle Errors Gracefully**: Return informative error messages to Claude
6. **Log Everything**: Use logging for debugging MCP communication
7. **Version Control**: Commit generated code to track changes
8. **Environment Variables**: Never hardcode API keys, use .env files
9. **Type Hints**: Maintain type hints for better IDE support
10. **Async/Await**: Use async properly for I/O-bound operations

## Resources

- **Script**: `{baseDir}/scripts/build_mcp_server.py`
- **Template**: `{baseDir}/assets/templates/mcp_server_template.py`
- **Example Server**: `{baseDir}/references/EXAMPLE_MCP_SERVER.py`
- **MCP Specification**: https://modelcontextprotocol.io/
- **Pydantic Docs**: https://docs.pydantic.dev/
- **MCP Python SDK**: https://github.com/modelcontextprotocol/python-sdk
