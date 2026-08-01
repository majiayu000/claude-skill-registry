---
name: ml-training-debugger
description: 'Type: Agent-based skill with SDK implementation'
---

# ML Training Debugger

**Version**: 1.0.0
**Type**: Agent-based skill with SDK implementation
**Domain**: Machine learning training diagnostics

## Description

Diagnose machine learning training failures including loss divergence, mode collapse, gradient issues, architecture problems, and optimization failures. This skill spawns a specialist ML debugging agent that systematically analyzes training artifacts to identify root causes and propose evidence-based fixes.

Use this skill when encountering training failures, when loss curves exhibit pathological behavior, when models produce degenerate outputs, when experiencing GPU memory issues, or when hyperparameter tuning produces inconsistent results.

## Triggers

This skill activates when users request:
- "Debug my training run"
- "Why is my loss diverging?"
- "Model outputs are all the same token"
- "Training failed at epoch X"
- "Help diagnose mode collapse"
- "Why are gradients exploding/vanishing?"
- "Model not learning anything"

## Skill Architecture

### Skill Layer (Lightweight)
The skill handles:
1. **Detection**: Identify ML training debugging requests
2. **Context Gathering**: Collect training logs, loss curves, model code
3. **Agent Spawning**: Invoke ML debugging specialist with context
4. **Result Processing**: Format diagnosis and fixes for user

### Agent Layer (Specialist)
The ML debugging agent handles:
1. **Systematic Analysis**: Apply debugging methodology to artifacts
2. **Root Cause Identification**: Diagnose underlying issues
3. **Fix Prioritization**: Rank solutions by impact
4. **Evidence-Based Recommendations**: Propose fixes with reasoning

## Communication Protocol

### Skill → Agent Context Package
```json
{
  "task": "Diagnose training failure",
  "artifacts": {
    "training_logs": "path/to/logs.txt",
    "loss_curves": "path/to/losses.csv",
    "model_code": ["model.py", "trainer.py"],
    "error_messages": ["error1.txt"],
    "config": "config.yaml"
  },
  "symptoms": [
    "Loss diverged at epoch 7",
    "Mode collapse to single token",
    "Gradient norm exploded"
  ],
  "constraints": {
    "max_analysis_time": "5 minutes",
    "output_format": "structured_diagnosis"
  }
}
```

### Agent → Skill Results
```json
{
  "status": "diagnosis_complete",
  "root_causes": [
    {
      "issue": "Learning rate too high for Muon optimizer",
      "severity": "critical",
      "evidence": ["grad_norm spike at step 24590", "loss increased 15% in epoch 7"],
      "fix": "Reduce muon_lr from 1e-2 to 5e-3",
      "confidence": 0.95
    }
  ],
  "quick_fixes": ["Reduce LR by 50%", "Enable gradient clipping"],
  "analysis_artifacts": {
    "gradient_analysis": "path/to/grad_analysis.md",
    "loss_visualization": "path/to/loss_plot.png"
  }
}
```

## Agent Spawning Logic

```python
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
import asyncio

async def execute_ml_debugger(context: dict):
    """Spawn ML debugging specialist agent."""

    # Load specialist agent prompt
    with open('agents/ml-debugger-specialist.prompt', 'r') as f:
        specialist_prompt = f.read()

    # Configure agent
    options = ClaudeAgentOptions(
        model='claude-sonnet-4-5',
        system_prompt=specialist_prompt,
        permission_mode='default',  # Read-only for safety
        allowed_tools=['Read', 'Grep', 'Bash'],  # Analysis tools only
        setting_sources=['project']
    )

    client = ClaudeSDKClient(options)

    try:
        await client.connect()

        # Format task for agent
        task = f"""Diagnose ML training failure:

Symptoms: {context['symptoms']}

Artifacts available:
- Training logs: {context['artifacts']['training_logs']}
- Loss curves: {context['artifacts']['loss_curves']}
- Model code: {', '.join(context['artifacts']['model_code'])}

Perform systematic analysis and provide structured diagnosis."""

        await client.query(task)

        # Collect diagnosis
        diagnosis = []
        async for message in client.receive_messages():
            if message.type == 'assistant':
                diagnosis.append(message.content)

        return parse_diagnosis(diagnosis)

    finally:
        await client.disconnect()
```

## Resources

### Scripts
- `scripts/analyze_loss_curve.py` - Loss curve analysis and visualization
- `scripts/check_gradients.py` - Gradient flow analysis
- `scripts/count_parameters.py` - Model parameter counting and distribution
- `scripts/profile_memory.py` - GPU memory profiling

### References
- `references/common-failure-modes.md` - Catalog of ML training failures
- `references/debugging-checklist.md` - Systematic debugging workflow
- `references/fix-templates.md` - Code templates for common fixes

### Custom Tools
- `extract_training_metrics()` - Parse logs for key metrics
- `visualize_loss_curve()` - Generate loss/gradient plots
- `analyze_architecture()` - Check model architecture balance

## Usage Examples

### Example 1: Loss Divergence
```
User: "My model was training fine until epoch 7, then loss started increasing. Help debug this."

Skill gathers:
- Training logs from epochs 1-10
- Loss curve data
- trainer.py and model.py
- Hyperparameter config

Agent diagnoses:
- Root cause: Learning rate too high for curriculum transition
- Evidence: Loss increased 15% at epoch 7, gradient norm spiked
- Fix: Reduce learning rate by 50%, add cosine annealing
- Confidence: 95%
```

### Example 2: Mode Collapse
```
User: "Model only outputs colons (::::) regardless of input. What's wrong?"

Skill gathers:
- Model checkpoint
- Inference test logs
- Training loss history
- Model architecture code

Agent diagnoses:
- Root cause: Embedding layer has 79% of params, transformer underparameterized
- Evidence: Training loss decreased but model has no capacity to learn patterns
- Fix: Rebalance architecture (50% embeddings, 50% transformers)
- Confidence: 90%
```

### Example 3: Gradient Issues
```
User: "Getting warning 'var(): degrees of freedom is <= 0' during training"

Skill gathers:
- Full error traceback
- Gradient statistics from logs
- ACT head implementation code

Agent diagnoses:
- Root cause: ACT variance = 0 (all tokens use same halting steps)
- Evidence: Warning appears in ACT loss computation
- Fix: Add diversity regularization to ACT loss
- Confidence: 98%
```

## Result Processing

The skill processes agent diagnosis into user-friendly format:

1. **Extract Root Causes**: Parse structured diagnosis
2. **Prioritize Fixes**: Rank by impact and confidence
3. **Format Recommendations**: Present as actionable steps
4. **Include Evidence**: Show supporting data/logs
5. **Generate Visualizations**: Create loss plots, gradient heatmaps

## Quality Standards

The ML debugging agent must:
- ✅ Identify root cause with >80% confidence or request more data
- ✅ Provide evidence from actual artifacts (not speculation)
- ✅ Propose fixes with expected impact and reasoning
- ✅ Complete analysis within 5 minutes for typical cases
- ✅ Handle missing artifacts gracefully (work with available data)

## Integration with Other Skills

This skill can be used in conjunction with:
- **ml-expertise** skill for implementing fixes
- **code-analyzer** skill for architecture review
- **functionality-audit** skill for validating fixes

## Failure Modes and Escalation

If the agent cannot diagnose the issue:
1. Request additional artifacts (specific logs, config files)
2. Provide partial diagnosis with lower confidence
3. Suggest alternative debugging approaches
4. Escalate to user with specific questions

The agent should NEVER:
- Guess at root causes without evidence
- Propose fixes that could corrupt training state
- Modify code directly (read-only mode)

## Testing

Test the skill with:
1. Real Phase 1 training failure (loss divergence at epoch 7)
2. Synthetic mode collapse scenario
3. Architecture imbalance case (79% embedding params)
4. Gradient explosion/vanishing cases
5. Missing artifacts scenario

## Documentation

- Agent system prompt: `agents/ml-debugger-specialist.prompt`
- SDK implementation: `index.py`
- Process visualization: `ml-training-debugger-process.dot`
- Testing guide: `tests/README.md`

---

**Next Steps**:
1. Create agent system prompt with ML debugging expertise
2. Implement SDK-based agent spawning
3. Add custom analysis tools
4. Test on Phase 1 training failures
5. Iterate based on real debugging sessions
