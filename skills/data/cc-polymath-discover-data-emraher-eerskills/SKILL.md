---
name: discover-data
description: Automatically discover data pipeline and ETL skills when working with ETL. Activates for data development tasks.
---

# Data Skills Discovery

Provides automatic access to comprehensive data skills.

## When This Skill Activates

This skill auto-activates when you're working with:
- ETL
- data pipelines
- batch processing
- stream processing
- data validation
- orchestration
- Airflow
- timely dataflow
- differential dataflow
- streaming aggregations
- windowing
- real-time analytics

## Available Skills

### Quick Reference

The Data category contains 9 skills:

1. **batch-processing** - Orchestrating complex data pipelines with dependencies
2. **data-validation** - Validating data schema before processing
3. **dataflow-coordination** - Coordination patterns for distributed dataflow systems
4. **differential-dataflow** - Differential computation for incremental updates and efficient joins
5. **etl-patterns** - Designing data extraction from multiple sources
6. **pipeline-orchestration** - Coordinating complex multi-step data workflows
7. **stream-processing** - Processing real-time event streams (Kafka, Flink)
8. **streaming-aggregations** - Windowing, sessionization, time-series aggregation
9. **timely-dataflow** - Low-latency streaming computation with progress tracking

### Load Full Category Details

For complete descriptions and workflows:

```bash
cat ~/.claude/skills/data/INDEX.md
```

This loads the full Data category index with:
- Detailed skill descriptions
- Usage triggers for each skill
- Common workflow combinations
- Cross-references to related skills

### Load Specific Skills

Load individual skills as needed:

```bash
# Traditional ETL/Batch
cat ~/.claude/skills/data/batch-processing.md
cat ~/.claude/skills/data/data-validation.md
cat ~/.claude/skills/data/etl-patterns.md
cat ~/.claude/skills/data/pipeline-orchestration.md

# Stream Processing
cat ~/.claude/skills/data/stream-processing.md
cat ~/.claude/skills/data/streaming-aggregations.md

# Advanced Dataflow Systems
cat ~/.claude/skills/data/timely-dataflow.md
cat ~/.claude/skills/data/differential-dataflow.md
cat ~/.claude/skills/data/dataflow-coordination.md
```

## Common Workflow Combinations

### Real-Time Analytics Pipeline
```bash
# Load these skills together:
cat ~/.claude/skills/data/stream-processing.md          # Kafka setup
cat ~/.claude/skills/data/streaming-aggregations.md     # Windowing patterns
cat ~/.claude/skills/data/dataflow-coordination.md      # Coordination
```

### Incremental Computation System
```bash
# Load these skills together:
cat ~/.claude/skills/data/timely-dataflow.md           # Foundation
cat ~/.claude/skills/data/differential-dataflow.md     # Incremental updates
cat ~/.claude/skills/data/dataflow-coordination.md     # Distributed coordination
```

### Hybrid Batch + Stream
```bash
# Load these skills together:
cat ~/.claude/skills/data/batch-processing.md          # Batch jobs
cat ~/.claude/skills/data/stream-processing.md         # Stream processing
cat ~/.claude/skills/data/pipeline-orchestration.md    # Overall coordination
```

## Progressive Loading

This gateway skill enables progressive loading:
- **Level 1**: Gateway loads automatically (you're here now)
- **Level 2**: Load category INDEX.md for full overview
- **Level 3**: Load specific skills as needed

## Usage Instructions

1. **Auto-activation**: This skill loads automatically when Claude Code detects data work
2. **Browse skills**: Run `cat ~/.claude/skills/data/INDEX.md` for full category overview
3. **Load specific skills**: Use bash commands above to load individual skills

---

**Next Steps**: Run `cat ~/.claude/skills/data/INDEX.md` to see full category details.
