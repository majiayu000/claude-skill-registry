---
name: aim-settings
description: 'Display current memory system configuration and settings'
allowed-tools: Read
---

# Memory Settings - Configuration Viewer

Display the current configuration of the AI Memory Module, including collections, types, thresholds, token budgets, and service endpoints.

## Usage

```bash
# Show all memory settings
/aim-settings

# Show specific section
/aim-settings --section collections
/aim-settings --section types
/aim-settings --section thresholds
/aim-settings --section services
/aim-settings --section agents
```

## Configuration Sections

### Collections
Shows the 3 Memory System V2.0 collections:
- **code-patterns** - Project-specific implementation patterns
- **conventions** - Cross-project shared conventions
- **discussions** - Decision context and session summaries

### Memory Types (14 total)
Organized by collection:
- code-patterns: `implementation`, `error_fix`, `refactor`, `file_pattern`
- conventions: `rule`, `guideline`, `port`, `naming`, `structure`
- discussions: `decision`, `session`, `blocker`, `preference`, `context`

### Thresholds
- **similarity_threshold** - Minimum relevance score for search results (default: 0.7)
- **dedup_threshold** - Similarity threshold for duplicate detection (default: 0.95)
- **max_retrievals** - Maximum memories per search (default: 5)
- **token_budget** - Maximum tokens for context injection (default: 4000, per BP-039)

### Services
Shows connection details for:
- **Qdrant** - Vector database (default: localhost:26350)
- **Embedding Service** - Jina AI embeddings (default: localhost:28080)
- **Monitoring API** - Health checks and metrics (default: localhost:28000)
- **Streamlit Dashboard** - Web UI (default: localhost:28501)
- **Grafana** - Metrics visualization (default: localhost:23000)
- **Prometheus** - Metrics storage (default: localhost:29090)
- **Pushgateway** - Metrics push gateway (default: localhost:29091)

### Agent Token Budgets
Shows token allocation per BMAD agent:
- architect: 1500 tokens
- analyst: 1200 tokens
- pm: 1200 tokens
- developer/dev: 1200 tokens
- solo-dev: 1500 tokens
- quick-flow-solo-dev: 1500 tokens
- ux-designer: 1000 tokens
- qa: 1000 tokens
- tea: 1000 tokens
- code-review/code-reviewer: 1200 tokens
- scrum-master/sm: 800 tokens
- tech-writer: 800 tokens
- default: 1000 tokens

### Logging
- **log_level** - Logging verbosity (default: INFO)
- **log_format** - Log output format (json or text, default: json)

### Collection Size Limits
- **Warning threshold** - 10,000 points
- **Critical threshold** - 50,000 points

## Examples

```bash
# View complete configuration
/aim-settings

# Check current thresholds
/aim-settings --section thresholds

# View service endpoints
/aim-settings --section services

# Check agent token budgets
/aim-settings --section agents

# View all memory types
/aim-settings --section types
```

## Python Configuration Reference

Configuration is managed by `src/memory/config.py`:

```python
from src.memory.config import get_config, AGENT_TOKEN_BUDGETS, get_agent_token_budget

# Get configuration singleton
config = get_config()

# Access settings
print(f"Qdrant: {config.qdrant_host}:{config.qdrant_port}")
print(f"Similarity threshold: {config.similarity_threshold}")
print(f"Max retrievals: {config.max_retrievals}")

# Get agent-specific token budget
budget = get_agent_token_budget("architect")  # Returns 1500
```

## Environment Variables

Configuration can be customized via environment variables or `.env` file:

```bash
# Core thresholds
SIMILARITY_THRESHOLD=0.7    # Retrieval relevance cutoff
DEDUP_THRESHOLD=0.95        # Duplicate detection sensitivity
MAX_RETRIEVALS=5            # Results per search
TOKEN_BUDGET=4000           # Context injection limit (per BP-039)

# Service endpoints
QDRANT_HOST=localhost
QDRANT_PORT=26350
EMBEDDING_HOST=localhost
EMBEDDING_PORT=28080
MONITORING_HOST=localhost
MONITORING_PORT=28000

# Logging
LOG_LEVEL=INFO              # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FORMAT=json             # json or text

# Collection size limits
COLLECTION_SIZE_WARNING=10000
COLLECTION_SIZE_CRITICAL=50000
```

## Configuration Precedence

Settings are loaded in this order (highest priority first):
1. Environment variables
2. `.env` file in project root
3. Default values

## Output Format

The skill displays configuration in organized sections with:
- Current values
- Default values (if different)
- Validation ranges (for thresholds)
- Service URLs with ports
- Memory type mappings to collections

## Technical Details

- **Type Safety**: Uses pydantic-settings v2.6+ for validation
- **Immutable**: Configuration is frozen (thread-safe)
- **Singleton**: Single config instance per process (lru_cache)
- **Validation**: All thresholds validated on load

## Related Skills

- `/aim-search` - Use these settings for memory search
- `/aim-status` - Check system health and statistics

## Notes

- Configuration is loaded once at startup
- Changes to .env require service restart
- All ports use 2XXXX prefix to avoid conflicts
- Token budgets optimized per agent role (architects need more context than scrum masters)
