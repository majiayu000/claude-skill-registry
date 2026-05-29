---
name: Find TODO and FIXME Comments
description: Search markdown files, Nextflow scripts, and config files for TODO/FIXME comments, categorize by priority, and provide actionable recommendations. Use when you need to identify pending work or track technical debt.
---

# Find TODO and FIXME Comments

Search the training materials codebase for TODO and FIXME comments to identify pending work.

Execute from repository root. See [../shared/repo-conventions.md](../shared/repo-conventions.md) for directory structure.

## Tasks to Perform

1. **Search Markdown Files**

   - Use Grep to find TODO and FIXME in `docs/**/*.md`
   - Capture file path, line number, and full comment
   - Note context (which module/lesson)

2. **Search Nextflow Scripts**

   - Find TODO/FIXME in `**/*.nf` files
   - Distinguish between training examples and solution code
   - Note if in core examples or side-quests

3. **Search Configuration Files**

   - Check `mkdocs.yml`
   - Check `.github/**/*.yml` and `.github/**/*.py`
   - Check `CONTRIBUTING.md`

4. **Categorize Results**

   - **High Priority**: Marked as FIXME, TODO(urgent), or blocking
   - **Documentation**: TODOs in markdown files
   - **Code**: TODOs in .nf or .py files
   - **Configuration**: TODOs in config files

5. **Check Known Issues**
   - Read CONTRIBUTING.md for any documented TODOs
   - Note which are tracked vs untracked

## Output Format

Provide an organized report:

````
# TODO/FIXME Report

## Summary
- Total items: 23
- High priority: 3
- Documentation: 15
- Code: 4
- Configuration: 1

## High Priority Items

### docs/hello_nextflow/03_hello_workflow.md:156
```markdown
<!-- FIXME: Update this example for DSL2 syntax -->
````

## Documentation TODOs

### By File

**docs/side_quests/debugging.md** (5 items)

- Line 45: TODO: Add example of common error message
- Line 89: TODO: Include screenshot of trace report
- ...

**docs/nf4_science/genomics/01_per_sample_variant_calling.md** (3 items)

- Line 234: TODO: Verify this command works with latest GATK
- ...

## Code TODOs

### nf-training/script7.nf:23

```groovy
// TODO: Add error handling for missing files
```

## Configuration TODOs

### CONTRIBUTING.md:204

Known limitation documented - needs upstream fix in mkdocs plugin

## Recommendations

1. **Immediate attention** (3 items):

   - Fix blocking issues in hello_nextflow
   - Update genomics examples for latest tools

2. **Next sprint** (8 items):

   - Complete debugging module exercises
   - Add missing screenshots

3. **Low priority** (12 items):
   - Style improvements
   - Nice-to-have features

## Files with Most TODOs

1. docs/side_quests/debugging.md (5)
2. docs/nf4_science/genomics/01_per_sample_variant_calling.md (3)
3. nf-training/script7.nf (2)

```

## Notes

- Use Grep tool with pattern `TODO|FIXME` (case insensitive)
- Show enough context to understand what needs doing
- Distinguish between legitimate TODOs and example comments in training materials
- Provide actionable priorities, not just a list
```
