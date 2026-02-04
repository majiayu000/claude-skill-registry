---
name: discover-research
description: Gateway skill for research methodology - automatically loads relevant research skills based on task context
---

# Research Skills Discovery

## Auto-Activation

This skill is automatically activated when your task involves:
- Research synthesis, literature reviews, meta-analysis
- Quantitative research, statistical analysis, surveys, experiments
- Qualitative research, interviews, ethnography, case studies
- Study design, hypothesis testing, sampling strategies
- Data collection, survey design, interview protocols
- Data analysis, coding, statistical tests, visualization
- Research writing, academic papers, citations, reporting

## Available Research Skills

### Core Methodology Skills

**1. research-synthesis** - Synthesizing information and conducting meta-analysis
- Narrative synthesis approaches
- Meta-analysis with Python implementation
- Thematic synthesis of qualitative findings
- Evidence mapping and gap analysis
- GRADE framework for quality assessment
- Use when: Integrating findings across studies

**2. quantitative-methods** - Quantitative research and statistical analysis
- Experimental design with power analysis
- Survey methods and analysis
- Hypothesis testing framework
- Regression analysis with diagnostics
- Effect sizes and reporting
- Use when: Testing hypotheses with numerical data

**3. qualitative-methods** - Qualitative research approaches
- In-depth interview protocols
- Thematic analysis (6 phases)
- Grounded theory coding
- Case study research design
- Quality criteria and rigor
- Use when: Exploring experiences and meanings

**4. research-design** - Planning and designing research studies
- Research question formulation (FINER criteria)
- Validity threat analysis
- Sampling strategies with Python tools
- Experimental control frameworks
- Design quality assessment
- Use when: Planning a new study from scratch

### Implementation Skills

**5. data-collection** - Methods for gathering research data
- Survey instrument design and validation
- Interview protocol development
- Observation methods and field notes
- Data quality control frameworks
- Response rate optimization
- Use when: Implementing data collection

**6. data-analysis** - Analyzing quantitative and qualitative data
- Comprehensive descriptive statistics
- Inferential testing with full reporting
- Systematic qualitative coding
- Thematic development process
- Publication-ready visualizations
- Use when: Making sense of collected data

**7. research-writing** - Writing research papers and reports
- IMRAD structure with guidelines
- APA statistical reporting
- Citation management
- Argument construction
- Peer review response strategies
- Use when: Communicating research findings

## Loading Skills

### Load Individual Skills

```bash
# From skills directory
cat ~/.claude/skills/research/research-synthesis.md
cat ~/.claude/skills/research/quantitative-methods.md
cat ~/.claude/skills/research/qualitative-methods.md
cat ~/.claude/skills/research/research-design.md
cat ~/.claude/skills/research/data-collection.md
cat ~/.claude/skills/research/data-analysis.md
cat ~/.claude/skills/research/research-writing.md
```

### Common Workflow Combinations

**Quantitative Research Study**:
```bash
# Planning phase
cat ~/.claude/skills/research/research-design.md

# Data collection
cat ~/.claude/skills/research/data-collection.md
cat ~/.claude/skills/research/quantitative-methods.md

# Analysis and reporting
cat ~/.claude/skills/research/data-analysis.md
cat ~/.claude/skills/research/research-writing.md
```

**Qualitative Research Study**:
```bash
# Planning phase
cat ~/.claude/skills/research/research-design.md

# Data collection
cat ~/.claude/skills/research/data-collection.md
cat ~/.claude/skills/research/qualitative-methods.md

# Analysis and reporting
cat ~/.claude/skills/research/data-analysis.md
cat ~/.claude/skills/research/research-writing.md
```

**Literature Review / Meta-Analysis**:
```bash
# Synthesis phase
cat ~/.claude/skills/research/research-synthesis.md

# If including quantitative synthesis
cat ~/.claude/skills/research/quantitative-methods.md

# Writing phase
cat ~/.claude/skills/research/research-writing.md
```

**Mixed Methods Study**:
```bash
# All methods
cat ~/.claude/skills/research/research-design.md
cat ~/.claude/skills/research/quantitative-methods.md
cat ~/.claude/skills/research/qualitative-methods.md
cat ~/.claude/skills/research/data-collection.md
cat ~/.claude/skills/research/data-analysis.md
cat ~/.claude/skills/research/research-writing.md
```

## Progressive Loading

Load skills progressively based on research phase:

**Phase 1: Planning** (Load 1-2 skills)
- research-design (always)
- quantitative-methods OR qualitative-methods (based on approach)

**Phase 2: Collection** (Add 1-2 skills)
- data-collection (always)
- Keep loaded: specific method skill

**Phase 3: Analysis** (Add 1 skill)
- data-analysis (always)
- Keep loaded: method and collection skills for reference

**Phase 4: Writing** (Add 1 skill, can unload others)
- research-writing (always)
- research-synthesis (if synthesizing literature)
- Keep one method skill for reporting details

**Phase 5: Synthesis** (If conducting review)
- research-synthesis (load early)
- quantitative-methods (if meta-analysis)
- qualitative-methods (if thematic synthesis)

## Decision Tree

```
Research Task
    ↓
Conducting new study?
    YES → Load research-design
        ↓
        Quantitative approach?
            YES → Load quantitative-methods + data-collection
        Qualitative approach?
            YES → Load qualitative-methods + data-collection
        Mixed methods?
            YES → Load both methods + data-collection
        ↓
        Ready to analyze?
            YES → Load data-analysis
        ↓
        Ready to write?
            YES → Load research-writing

    NO → Synthesizing existing research?
        YES → Load research-synthesis
            ↓
            Quantitative synthesis (meta-analysis)?
                YES → Also load quantitative-methods
            Qualitative synthesis?
                YES → Also load qualitative-methods
            ↓
            Ready to write?
                YES → Load research-writing
```

## Context-Aware Loading

Based on keywords in your task, these skills auto-load:

**Keywords → Skills Mapping**:
- "literature review", "meta-analysis", "systematic review" → research-synthesis
- "survey", "experiment", "hypothesis", "statistical" → quantitative-methods
- "interview", "ethnography", "case study", "lived experience" → qualitative-methods
- "study design", "sampling", "validity", "research plan" → research-design
- "questionnaire", "data collection", "measurement" → data-collection
- "analyze data", "coding", "statistical test", "thematic" → data-analysis
- "write paper", "manuscript", "citation", "peer review" → research-writing

## Related Skill Categories

- **statistics**: Advanced statistical techniques
- **data-science**: Machine learning and big data approaches
- **visualization**: Advanced data visualization
- **academic-writing**: General academic writing skills
- **scientific-computing**: Python/R for research computing

## Quick Start Examples

### "I need to design a survey study"
```bash
cat ~/.claude/skills/research/research-design.md
cat ~/.claude/skills/research/data-collection.md
cat ~/.claude/skills/research/quantitative-methods.md
```

### "I need to analyze interview transcripts"
```bash
cat ~/.claude/skills/research/qualitative-methods.md
cat ~/.claude/skills/research/data-analysis.md
```

### "I need to conduct a meta-analysis"
```bash
cat ~/.claude/skills/research/research-synthesis.md
cat ~/.claude/skills/research/quantitative-methods.md
```

### "I need to write up my results"
```bash
cat ~/.claude/skills/research/research-writing.md
cat ~/.claude/skills/research/data-analysis.md
```

## Best Practices

1. **Start with design**: Load research-design first when planning new studies
2. **Method-specific loading**: Load only the method skill you need (quant OR qual)
3. **Progressive addition**: Add skills as you progress through research phases
4. **Unload when done**: Unload skills from completed phases to manage context
5. **Keep writing loaded**: research-writing useful throughout for documentation

## Skill Maintenance

All research skills follow these standards:
- Practical code examples (Python primary, R when appropriate)
- Real-world templates and protocols
- Best practices and anti-patterns
- Cross-references to related skills
- 250-400 lines optimized for context efficiency

## Integration with Other Skills

Research skills integrate well with:
- **python-data-science**: For advanced analysis
- **python-visualization**: For publication graphics
- **academic-latex**: For paper formatting
- **git-workflow**: For research project management
- **reproducibility**: For reproducible research practices
