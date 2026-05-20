---
name: doc-update-blog
description: Update development blog with implementation milestones, learnings, and progress. Use after completing major milestones or phases.
mcp_fallback: none
category: doc
---

# Update Progress Blog Skill

Document progress and technical learnings in blog format.

## When to Use

- Completed major milestone
- Finished implementation phase
- Learned something significant
- Major refactoring or optimization completed

## Quick Reference

```bash
cat > notes/blog/MM-DD-YYYY.md << 'EOF'
# Progress Update: YYYY-MM-DD

## What Was Accomplished
- Item 1
- Item 2

## Technical Highlights
- Implementation detail or optimization

## Next Steps
- Upcoming work
EOF
```

## Blog Structure

```markdown
# Progress Update: YYYY-MM-DD

## What Was Accomplished
- Completed X
- Implemented Y
- Achieved Z

## Challenges Faced
- Challenge 1 and how it was solved
- Challenge 2 and lessons learned

## Technical Highlights
- Interesting implementation detail
- Performance optimization achieved

## Metrics
- Lines of code: X
- Test coverage: Y%
- Performance: Z% improvement

## Next Steps
- Upcoming work
- Planned improvements
```

## Blog Location

- `notes/blog/MM-DD-YYYY.md` - All blog entries (flat structure)

## Best Practices

- Write regularly (weekly or per milestone)
- Be specific with metrics
- Document learnings and challenges
- Link to relevant code/issues
- Keep entries focused (one milestone per entry)

## Content Tips

### Metrics Format

```text
- Lines of code: 250 (tensor operations)
- Test coverage: 94% (up from 87%)
- Performance: 3x speedup on matmul (cache optimization)
```

### Challenge Documentation

```text
**Problem**: Matrix alignment causing segfaults
**Solution**: Added padding to align rows to SIMD width
**Lessons**: Always validate memory layout for SIMD operations
```

## Error Handling

| Issue | Fix |
|-------|-----|
| No metrics | Measure before/after with specific numbers |
| Vague accomplishments | List specific implementations or fixes |
| Missing learnings | Add what was discovered/surprised you |
| No next steps | Plan immediate next work |

## References

- Related skill: `doc-generate-adr` for architectural decisions
- See existing blog posts in `/notes/blog/` for examples
