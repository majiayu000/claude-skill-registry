---
description: Enforces Given-When-Then test structure
triggers:
  - file_pattern: "*.test.*;*.spec.*;*Test.java;*_test.go;test_*.py"
---

# Test Writing Skill

**Naming:** `should{Behavior}When{State}`

**Structure:**
```javascript
// GIVEN - setup
// WHEN - act
// THEN - assert
```

**Requirements:** Independent, Fast (<100ms), Edge cases

`Read .claude/reference/skills-full/test-writing-full.md`
