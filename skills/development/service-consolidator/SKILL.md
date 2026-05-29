---
name: Service Consolidator
description: Find and consolidate duplicate service implementations in Leavn app - analyze variants, choose winner, update call sites, delete duplicates
allowed-tools: Read, Edit, Grep, Glob, Bash
---

# Service Consolidator

Consolidate duplicate services:

1. **Find duplicates**: Search for services with similar names (Enhanced, Live, Base)
2. **Compare implementations**: Feature completeness, code quality, usage
3. **Choose winner**: Modern patterns (@Observable, async/await, protocol-based)
4. **Update DIContainer**: Use correct implementation
5. **Find all usages**: Grep for class name
6. **Delete unused**: Remove files + update imports

Use when: Multiple similar services exist, Enhanced variants, consolidation needed
