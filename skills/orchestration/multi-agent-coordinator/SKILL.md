---
name: Multi-Agent Coordinator
description: Spawn 10-20 parallel agents for Leavn codebase audits, systematic fixes, comprehensive analysis across multiple domains simultaneously
allowed-tools: Task (general-purpose, Explore agents)
---

# Multi-Agent Coordinator

Deploy agent swarms for comprehensive work:

1. **Audit swarms** (10-15 agents):
   - UserDefaults usage
   - @Published migration targets
   - Error handling patterns
   - Performance issues
   - Duplicate services
   - Navigation patterns
   - Memory leak risks
   - Test coverage gaps

2. **Fix swarms** (5-10 agents):
   - Fix group 1 errors (files 1-5)
   - Fix group 2 errors (files 6-10)
   - Migrate tier 1 ViewModels
   - Migrate tier 2 Services
   - Create entities 1-3
   - Create entities 4-6

3. **Verification swarms** (3-5 agents):
   - Test feature A
   - Test feature B
   - Verify integration C

4. **Deploy pattern**:
   - Single message, multiple Task calls
   - Clear tasks with specific deliverables
   - Collect all results before acting

Use when: Large refactoring, comprehensive audit, parallel fixes needed, systematic analysis
