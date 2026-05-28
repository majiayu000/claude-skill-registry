---
name: cfn-provider-routing
version: 1.0.0
complexity: Low
keywords: [
    "provider routing",
    "API management",
    "cost optimization",
    "model compatibility",
    "cross-provider"
]
triggers: [
    "agent spawning with provider selection",
    "cost optimization requirements",
    "multi-provider compatibility"
]
performance_targets: {
    "resolution_latency_ms": 1,
    "memory_footprint_mb": 1,
    "startup_time_ms": 10
}
---

# CFN Provider Routing - Cross-Provider Model Compatibility

**Status:** Production Ready | **Category:** Provider Integration | **Complexity:** Low

## Overview

Translates agent-specified models (sonnet/haiku/opus) to provider-specific model names. Enables seamless cross-provider compatibility without modifying agent profiles.

## Core Function

**Primary Use Case:** Agent spawning with provider-specific model resolution
**Secondary Use Case:** Cost optimization through tier-based model selection
**Validation:** Model mapping completeness and provider support verification

## Usage Patterns

### Direct Model Resolution
```bash
# Basic usage - resolve sonnet for Z.ai
./resolve-provider-model.ts --provider zai --model sonnet
# Returns: glm-4.6

# With cost optimization
./resolve-provider-model.ts --provider kimi --model haiku --tier economy
# Returns: kimi-k2-turbo-preview
```

### Integration with Agent Spawning
```bash
# In agent spawning scripts
AGENT_MODEL="sonnet"
PROVIDER="zai"
RESOLVED_MODEL=$(./resolve-provider-model.ts --provider "$PROVIDER" --model "$AGENT_MODEL")
export ANTHROPIC_MODEL="$RESOLVED_MODEL"
```

### Configuration Validation
```bash
# Check provider support
./resolve-provider-model.ts --summary
# Returns JSON with supported providers and models
```

## Parameters

### Required Parameters
- `--provider <provider>`: Target provider (zai, kimi, openrouter, gemini, xai, anthropic)

### Optional Parameters
- `--model <agent-model>`: Agent-specified model (sonnet, haiku, opus)
- `--tier <cost-tier>`: Cost optimization tier (economy, standard, premium)
- `--summary`: Show configuration summary

## Return Values

### Success
- **Model resolution**: Returns provider-specific model name as string
- **Configuration summary**: Returns JSON with provider/model mappings

### Error Conditions
- **Provider not supported**: Returns error with supported providers list
- **Configuration missing**: Falls back to basic mappings with warning
- **Invalid parameters**: Returns usage information

## Integration Points

### Agent Spawning Pipeline
```
Agent Profile (model: sonnet) → Provider Router → Z.ai (glm-4.6)
```

### CLI Mode Provider Selection
```
/cfn-loop-cli "task" --provider zai → Router → Agent with glm-4.6
```

### Cost Optimization
```
--tier economy → Router → Fast models for simple tasks
--tier premium → Router → High-quality models for complex tasks
```

## Examples

### Basic Provider Routing
```bash
# Spawn backend-developer with Z.ai
AGENT_TYPE="backend-developer"  # Has model: sonnet
PROVIDER="zai"
MODEL=$(./resolve-provider-model.ts --provider "$PROVIDER" --model sonnet)
# MODEL="glm-4.6"
```

### Cross-Provider Compatibility
```bash
# Same agent, different providers
./resolve-provider-model.ts --provider zai --model sonnet      # glm-4.6
./resolve-provider-model.ts --provider kimi --model sonnet     # kimi-k2-turbo-preview
./resolve-provider-model.ts --provider openrouter --model sonnet # anthropic/claude-sonnet-4.5
```

### Cost-Optimized Execution
```bash
# Economy mode for bulk operations
ECONOMY_MODEL=$(./resolve-provider-model.ts --provider kimi --model haiku --tier economy)
# Returns: kimi-k2-turbo-preview (fast, cost-effective)

# Premium mode for critical tasks
PREMIUM_MODEL=$(./resolve-provider-model.ts --provider openrouter --model sonnet --tier premium)
# Returns: anthropic/claude-sonnet-4.5 (high quality)
```

## Dependencies

### External Dependencies
- **Node.js**: Runtime environment
- **js-yaml**: YAML configuration parsing (bundled)

### Configuration Dependencies
- **provider-model-mappings.yaml**: Model mapping configuration
- **No Redis required**: Pure configuration resolution

## Anti-Patterns

### ❌ Manual Model Hardcoding
```bash
# AVOID: Hardcoded provider-specific models
if [[ "$PROVIDER" == "zai" ]]; then
  export ANTHROPIC_MODEL="glm-4.6"
fi
```

### ❌ Agent Profile Modification
```yaml
# AVOID: Updating 65+ agent files for new provider
<!-- PROVIDER_PARAMETERS
provider: zai
model: glm-4.6  # Wrong approach - maintenance nightmare
-->
```

### ✅ Centralized Mapping
```bash
# CORRECT: Use centralized resolver
MODEL=$(./resolve-provider-model.ts --provider "$PROVIDER" --model "$AGENT_MODEL")
export ANTHROPIC_MODEL="$MODEL"
```

## Performance Characteristics

- **Resolution latency**: <1ms per lookup
- **Memory footprint**: <1MB configuration object
- **Startup time**: <10ms YAML file load
- **Scalability**: O(1) lookup time, unlimited concurrent requests

## Monitoring & Troubleshooting

### Configuration Validation
```bash
# Check if all providers are supported
./resolve-provider-model.ts --summary
```

### Model Resolution Testing
```bash
# Test all agent models for a provider
for model in sonnet haiku opus; do
  echo "$model → $(./resolve-provider-model.ts --provider zai --model "$model")"
done
```

### Common Issues
- **Provider not found**: Check provider name spelling in configuration
- **Model resolution fails**: Verify agent model exists in mappings
- **Configuration missing**: Fallback to basic mappings automatically

## Evolution Path

### Phase 1: Current Implementation
- Basic model mapping resolution
- Configuration file-based approach
- CLI integration for agent spawning

### Phase 2: Enhanced Features
- Dynamic model capability detection
- Provider-specific optimization hints
- Integration with cost tracking

### Phase 3: Advanced Routing
- AI-driven model selection based on task complexity
- Performance-based model switching
- Multi-provider failover routing