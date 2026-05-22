---
name: ml-expert
description: Implement machine learning solutions including model architectures, training pipelines, optimization strategies, and performance improvements. This skill spawns a specialist ML implementation agent...
---

# ML Expert - Machine Learning Implementation Specialist

**Version**: 1.0.0
**Type**: Agent-based skill with SDK implementation
**Domain**: Machine learning model implementation, training, and optimization

## Description

Implement machine learning solutions including model architectures, training pipelines, optimization strategies, and performance improvements. This skill spawns a specialist ML implementation agent with deep expertise in PyTorch, deep learning architectures, training techniques, and production ML systems.

Use this skill when implementing new ML models, fixing training issues, optimizing performance, implementing research papers, or building production ML pipelines.

## Triggers

This skill activates when users request:
- "Implement this ML architecture"
- "Fix the training code"
- "Optimize model performance"
- "Implement [paper/technique]"
- "Build a training pipeline for..."
- "Add [feature] to the model"
- "Improve inference speed"

## Skill Architecture

### Skill Layer (Lightweight)
The skill handles:
1. **Detection**: Identify ML implementation requests
2. **Context Gathering**: Collect requirements, existing code, constraints
3. **Agent Spawning**: Invoke ML expert specialist with context
4. **Result Processing**: Validate and format implementation

### Agent Layer (Specialist)
The ML expert agent handles:
1. **Architecture Design**: Create model structures following best practices
2. **Implementation**: Write production-quality PyTorch code
3. **Optimization**: Apply performance improvements and best practices
4. **Validation**: Ensure correctness through testing

## Communication Protocol

### Skill → Agent Context Package
```json
{
  "task": "Implement TRM × Titans-MAG architecture",
  "requirements": {
    "model_type": "transformer",
    "parameters": "25M target",
    "features": ["sliding_window_attention", "long_term_memory", "ACT"],
    "framework": "pytorch",
    "constraints": {
      "vram": "6GB",
      "inference_speed": "real-time"
    }
  },
  "existing_code": {
    "files": ["model.py", "config.py"],
    "status": "partial_implementation"
  },
  "reference_materials": {
    "papers": ["TRM.pdf", "Titans-MAG.pdf"],
    "implementations": ["reference_model.py"]
  }
}
```

### Agent → Skill Results
```json
{
  "status": "implementation_complete",
  "deliverables": {
    "code_files": [
      {
        "path": "src/model/titans_mag.py",
        "description": "Titans-MAG backbone implementation",
        "loc": 350,
        "tested": true
      }
    ],
    "tests": [
      {
        "path": "tests/test_model.py",
        "coverage": 95,
        "all_passing": true
      }
    ],
    "documentation": {
      "architecture_diagram": "docs/architecture.md",
      "usage_examples": "examples/train.py"
    }
  },
  "performance_metrics": {
    "parameter_count": "25.6M",
    "inference_time": "45ms (GPU)",
    "vram_usage": "5.2GB"
  },
  "validation": {
    "unit_tests": "48/48 passing",
    "integration_tests": "12/12 passing",
    "manual_verification": "Forward/backward pass successful"
  }
}
```

## Agent Spawning Logic

```python
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
import asyncio

async def execute_ml_expert(context: dict):
    """Spawn ML implementation specialist agent."""

    # Load specialist agent prompt
    with open('agents/ml-expert-specialist.prompt', 'r') as f:
        specialist_prompt = f.read()

    # Configure agent with write permissions (plan mode for safety)
    options = ClaudeAgentOptions(
        model='claude-sonnet-4-5',
        system_prompt=specialist_prompt,
        permission_mode='plan',  # Show intent before editing
        allowed_tools=['Read', 'Write', 'Edit', 'Bash', 'Grep'],
        setting_sources=['project']
    )

    client = ClaudeSDKClient(options)

    try:
        await client.connect()

        # Format task for agent
        task = f"""Implement ML solution:

Requirements: {context['requirements']}

Existing code: {context['existing_code']}

Reference materials: {context['reference_materials']}

Deliver production-quality implementation with tests and documentation."""

        await client.query(task)

        # Collect implementation results
        results = []
        async for message in client.receive_messages():
            if message.type == 'assistant':
                results.append(message.content)

        return parse_implementation(results)

    finally:
        await client.disconnect()
```

## Resources

### Scripts
- `scripts/init_model_template.py` - Generate model boilerplate
- `scripts/test_model.py` - Model testing utilities
- `scripts/profile_performance.py` - Performance profiling
- `scripts/validate_architecture.py` - Architecture validation

### References
- `references/pytorch-best-practices.md` - PyTorch coding standards
- `references/architecture-patterns.md` - Common ML architecture patterns
- `references/optimization-techniques.md` - Training optimization guide
- `references/testing-guide.md` - ML testing best practices

### Templates
- `templates/model_template.py` - Base model class template
- `templates/trainer_template.py` - Training loop template
- `templates/config_template.py` - Configuration dataclass template

### Custom Tools
- `create_model_skeleton()` - Generate model file structure
- `add_tests()` - Create test cases for model components
- `benchmark_model()` - Performance benchmarking

## Usage Examples

### Example 1: Implement New Architecture
```
User: "Implement the TRM × Titans-MAG architecture from these papers with 25M parameters"

Skill gathers:
- Paper PDFs with architecture details
- Target parameter count constraint
- PyTorch as framework
- GPU memory constraint (6GB)

Agent implements:
- Titans-MAG backbone (sliding window attention, LMM, MAG gate)
- TRM wrapper (multi-pass reasoning)
- ACT head (adaptive computation)
- Full model integration
- Unit tests (95% coverage)
- Usage examples
- Architecture documentation

Deliverables:
- src/model/titans_mag.py (350 LOC)
- src/model/trm_wrapper.py (180 LOC)
- src/model/act_head.py (120 LOC)
- src/model/full_model.py (200 LOC)
- tests/test_*.py (48 tests, all passing)
- docs/architecture.md
```

### Example 2: Fix Training Issue
```
User: "The ACT head has variance=0 issue. Add diversity regularization."

Skill gathers:
- Current ACT head implementation
- Diagnosis from ml-training-debugger skill
- Recommended fix (diversity loss)

Agent implements:
- Modify compute_act_loss() method
- Add diversity regularization term
- Update docstrings
- Add test for variance>0
- Verify training runs without warning

Deliverables:
- Modified src/model/act_head.py
- New test: tests/test_act_diversity.py
- Validation: Warning eliminated in training
```

### Example 3: Optimize Performance
```
User: "Model inference is too slow. Optimize for real-time performance."

Skill gathers:
- Current model code
- Profiling results
- Performance requirements (< 100ms)

Agent optimizes:
- Enable gradient checkpointing
- Fuse operations where possible
- Use torch.compile() for JIT optimization
- Optimize tensor operations
- Add caching for repeated computations

Deliverables:
- Optimized model code
- Performance benchmarks (45ms → 28ms)
- Memory usage reduced (6.2GB → 5.2GB)
- All tests still passing
```

## Quality Standards

The ML expert agent must:
- ✅ Write production-quality, well-documented code
- ✅ Follow PyTorch best practices and idioms
- ✅ Include comprehensive tests (≥90% coverage)
- ✅ Verify all implementations work end-to-end
- ✅ Provide usage examples and documentation
- ✅ Optimize for readability and maintainability

## Integration with Other Skills

This skill works with:
- **ml-training-debugger** - Implements fixes from diagnoses
- **code-analyzer** - Reviews implementation quality
- **functionality-audit** - Validates implementations work
- **style-audit** - Ensures code style compliance

## Failure Modes and Escalation

If the agent cannot implement the solution:
1. Clarify ambiguous requirements with user
2. Request additional reference materials
3. Implement partial solution with clear TODOs
4. Escalate if task exceeds ML expertise scope

The agent should NEVER:
- Write code without understanding requirements
- Implement untested functionality
- Make breaking changes to existing APIs
- Commit directly without validation

## Testing

Test the skill with:
1. New model implementation (TRM × Titans-MAG)
2. Bug fix implementation (ACT diversity loss)
3. Performance optimization (inference speed)
4. Research paper implementation
5. Production pipeline creation

## Documentation

- Agent system prompt: `agents/ml-expert-specialist.prompt`
- SDK implementation: `index.py`
- Process visualization: `ml-expert-process.dot`
- Testing guide: `tests/README.md`

---

**Next Steps**:
1. Create agent system prompt with ML implementation expertise
2. Implement SDK-based agent spawning
3. Add model templates and utilities
4. Test on Phase 1 implementation tasks
5. Integrate with ml-training-debugger workflow
