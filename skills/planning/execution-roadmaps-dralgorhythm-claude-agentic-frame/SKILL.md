---
name: execution-roadmaps
description: Create execution roadmaps for projects. Use when planning multi-phase projects or feature rollouts. Covers phased delivery and milestone planning.
allowed-tools: Read, Write, Glob, Grep
---

# Execution Roadmaps

## Workflows

- [ ] **Define Phases**: Break work into logical phases
- [ ] **Set Milestones**: Define measurable checkpoints
- [ ] **Identify Dependencies**: Map critical path
- [ ] **Assign Ownership**: Who is responsible
- [ ] **Save Artifact**: Save to `./artifacts/roadmap_[project].md`

## Roadmap Structure

### Phase 1: Foundation
- Core infrastructure
- Basic functionality
- Initial testing

### Phase 2: MVP
- Key features
- User testing
- Feedback integration

### Phase 3: Enhancement
- Additional features
- Performance optimization
- Scale preparation

### Phase 4: Launch
- Production deployment
- Monitoring
- Documentation

### Phase 5: Iteration
- User feedback
- Bug fixes
- Continuous improvement

## Milestone Definition

Each milestone should have:
- **Name**: Clear, descriptive
- **Criteria**: What defines completion
- **Date**: Target completion
- **Owner**: Who is accountable
- **Dependencies**: What must be done first

## Example Milestone

```markdown
## Milestone: Authentication MVP

**Target**: Week 4

**Criteria**:
- [ ] Login/logout working
- [ ] Password reset implemented
- [ ] Session management secure
- [ ] Integration tests passing
- [ ] Security review complete

**Owner**: Auth Team

**Dependencies**:
- Database schema complete
- API framework selected
```

## Resources

- [Roadmap Template](./resources/execution-roadmap.template.md)
