---
name: create-tutorial
description: Create high-quality, progressive learning tutorials for VRP Toolkit. Use when the user requests creating tutorials, educational content, or learning materials for any VRP toolkit feature (problem creation, algorithm implementation, data generation, visualization, etc.). This skill ensures tutorials follow best learning practices with progressive disclosure, hands-on examples, and clear explanations.
---

# Create Tutorial

Create comprehensive, learner-centered tutorials for the VRP Toolkit project.

## Core Philosophy

Tutorials are **progressive learning experiences**, not documentation dumps. They should:
- Start simple, build complexity gradually
- Emphasize hands-on practice over theory
- Show real, runnable code
- Explain the "why" not just the "how"

## Tutorial Categories

### 1. Feature Tutorials (How to use X)
**Examples:** "How to use OSMnx integration", "How to visualize routes"
- Focus on one specific feature
- Show multiple use cases
- Include troubleshooting

### 2. Concept Tutorials (Understanding X)
**Examples:** "Custom problems explained", "Algorithm configuration"
- Explain underlying concepts
- Compare alternatives
- Show when to use what

### 3. Task Tutorials (Build X)
**Examples:** "Build a custom heuristic", "Create CVRP variant"
- Goal-oriented, project-based
- Step-by-step construction
- Final working artifact

### 4. Integration Tutorials (Combine X + Y)
**Examples:** "Real maps + custom algorithms", "Benchmarking workflow"
- Show how pieces fit together
- Realistic workflows
- Best practices

## Tutorial Structure Template

Use this structure for all tutorials:

### Section 1: Introduction (2-3 minutes read)
```markdown
# Tutorial XX: [Clear, Action-Oriented Title]

[2-3 sentence overview of what student will learn]

**What you'll learn:**
- Concrete skill 1
- Concrete skill 2
- Concrete skill 3

**Prerequisites:**
- Tutorial YY (if applicable)
- Basic Python knowledge

**Time:** ~XX minutes
```

### Section 2: Setup (5 minutes)
```markdown
## 1. Setup and Imports

[Minimal imports needed - copy-pasteable]

```python
# Standard imports
import numpy as np
import pandas as pd

# VRP Toolkit imports
from vrp_toolkit.xxx import yyy
```

[Quick validation - ensure imports work]
```

### Section 3: Quick Win (10 minutes)
```markdown
## 2. Quick Start: [Simplest Possible Example]

Let's start with the **simplest possible example** to see it working:

[Code that runs in <10 lines and produces visible output]

**What just happened:**
[Brief explanation of what the code did]
```

**Critical:** Student should get a working result in first 10 minutes.

### Section 4: Core Concepts (15-20 minutes)
```markdown
## 3. Understanding [Key Concept]

Now let's understand what's really happening.

### 3.1 [Sub-concept 1]
[Explanation]
[Code example]

### 3.2 [Sub-concept 2]
[Explanation]
[Code example]

### 3.3 [Sub-concept 3]
[Explanation]
[Code example]
```

**Progressive disclosure:** Introduce complexity one piece at a time.

### Section 5: Advanced Usage (10-15 minutes)
```markdown
## 4. Advanced Features

Now that you understand the basics, let's explore advanced options:

### 4.1 [Advanced Feature 1]
**When to use:** [Specific scenario]
**How it works:** [Brief explanation]

```python
[Code example]
```

### 4.2 [Advanced Feature 2]
[Similar structure]
```

### Section 6: Real-World Example (10-15 minutes)
```markdown
## 5. Real-World Example: [Concrete Scenario]

Let's apply everything to a realistic scenario:

**Scenario:** [Describe a real problem]

[Complete, runnable example that combines concepts]

**Key observations:**
- Point 1
- Point 2
```

### Section 7: Comparison & When to Use (5 minutes)
```markdown
## 6. Comparison and Best Practices

**When to use [this approach]:**
- Scenario 1
- Scenario 2

**When to use [alternative]:**
- Scenario 3
- Scenario 4

**Common pitfalls:**
- Pitfall 1 and how to avoid it
- Pitfall 2 and how to avoid it
```

### Section 8: Exercises (Optional)
```markdown
## 7. Practice Exercises

Try these on your own:

1. **Basic:** [Simple modification task]
2. **Intermediate:** [Combine concepts]
3. **Advanced:** [Open-ended challenge]

[Hints or solution sketches]
```

### Section 9: Summary & Next Steps
```markdown
## 8. Summary

**What you learned:**
- ✅ Skill 1
- ✅ Skill 2
- ✅ Skill 3

**Key takeaways:**
1. Important insight 1
2. Important insight 2

**Next steps:**
- Try Tutorial XX for [related topic]
- Explore [related feature]
- Build your own [project idea]
```

## Code Quality Standards

### All code must be:
1. **Runnable** - Copy-paste works without modification
2. **Realistic** - Uses actual VRP toolkit APIs (not pseudo-code)
3. **Minimal** - Shortest code that demonstrates the concept
4. **Commented** - Explain non-obvious parts

### Code Examples Structure:
```python
# Step 1: [What this does]
code_line_1

# Step 2: [What this does]
code_line_2

# Verify result
print(f"Result: {result}")  # Show output
```

## Best Practices

### DO:
✅ Start with working code, explain after
✅ Use consistent variable names across examples
✅ Show output for every code block
✅ Explain errors students might encounter
✅ Compare alternatives ("X vs Y")
✅ Include visual output (plots, tables)
✅ Build on previous tutorials

### DON'T:
❌ Start with theory before showing code
❌ Assume prior knowledge (state prerequisites)
❌ Use complex examples too early
❌ Skip error handling in advanced sections
❌ Leave code unexplained
❌ Use pseudo-code instead of real code

## Tutorial Naming Convention

```
XX_topic_name.ipynb

Where:
- XX = Tutorial number (01, 02, 03, ...)
- topic_name = snake_case description
```

**Examples:**
- `03_custom_problems.ipynb`
- `04_problem_variants.ipynb`
- `06_custom_algorithms.ipynb`

## Creating a New Tutorial: Step-by-Step

### 1. Define Learning Objectives
Ask yourself:
- What specific skill will students have after this?
- What can they build that they couldn't before?
- What prerequisite knowledge is needed?

### 2. Create the Notebook
```python
# Create new Jupyter notebook
touch tutorials/XX_topic_name.ipynb
```

### 3. Follow the Template
Use the structure template above, adapting as needed for the topic.

### 4. Test Every Code Block
- Run all cells in order
- Verify output matches what's described
- Test on fresh Python environment

### 5. Review Checklist
Before finalizing, verify:
- [ ] Title clearly states what student will learn
- [ ] Prerequisites are stated upfront
- [ ] First example works within 10 minutes
- [ ] All code blocks run without errors
- [ ] Code examples use actual VRP toolkit APIs
- [ ] Each concept builds on previous ones
- [ ] Output is shown for all code examples
- [ ] Common errors are addressed
- [ ] Summary lists concrete skills learned
- [ ] Next steps are suggested

### 6. Integration
- Add to README.md tutorial list
- Update tutorial numbering if needed
- Test links between tutorials

## Topic-Specific Guidance

### For Problem Creation Tutorials:
- Show multiple input formats (CSV, manual, generated)
- Demonstrate validation and error checking
- Compare with built-in examples
- Show how to visualize the problem

### For Algorithm Tutorials:
- Explain the algorithm intuition first
- Show simplest version, then add complexity
- Compare with baseline (greedy, random)
- Demonstrate configuration options
- Include performance comparisons

### For Integration Tutorials:
- Start with working individual pieces
- Show integration points clearly
- Explain why integration is beneficial
- Provide complete end-to-end example

## Quality Metrics

A good tutorial:
- **Time-to-first-win** < 10 minutes
- **Code-to-text ratio** > 30%
- **Student can build something** after completion
- **Progressive complexity** (easy → medium → hard)
- **All code runs** without errors

## Example Tutorial Outline

See [references/example-tutorial-outline.md](references/example-tutorial-outline.md) for a complete example of applying this template.

## Resources

- **Template notebook**: [assets/tutorial-template.ipynb](assets/tutorial-template.ipynb)
- **Example tutorial**: [references/example-tutorial-outline.md](references/example-tutorial-outline.md)
- **Learning principles**: [references/learning-principles.md](references/learning-principles.md)

## Usage Workflow

When user requests a tutorial:

1. **Clarify scope** - What should students learn?
2. **Identify category** - Feature/Concept/Task/Integration?
3. **Check prerequisites** - What do students need to know first?
4. **Follow template** - Use structure above
5. **Write code first** - Then add explanations
6. **Test thoroughly** - Run all cells
7. **Review checklist** - Ensure quality standards
8. **Integrate** - Add to README and cross-link

## Tutorial Maintenance

When updating existing tutorials:
- Maintain backward compatibility in code examples
- Update for API changes
- Add clarifications based on user feedback
- Keep examples realistic and current
