# 🤝 AI Pair Programming Skill

---
name: ai-pair-programming
description: Collaborate with AI in real-time pair programming sessions for enhanced productivity
---

## 🎯 Purpose

ทำงานร่วมกับ AI แบบ pair programming เพื่อเพิ่ม productivity และ code quality

## 📋 When to Use

- ทำงาน complex features
- Need second opinion
- Learning new technology
- Debugging difficult issues
- Code review in real-time

## 🔧 Pair Programming Modes

### 1. Driver-Navigator Mode
```
Human = Driver (writes code)
AI = Navigator (reviews, suggests, catches errors)

Flow:
1. Human writes code
2. AI reviews each change
3. AI suggests improvements
4. Human decides to accept/modify
```

### 2. Ping-Pong Mode
```
Alternate writing code:

1. Human writes test
2. AI writes code to pass
3. Human refactors
4. AI suggests improvements
```

### 3. AI-First Mode
```
AI = Driver (writes code)
Human = Navigator (reviews, directs)

Flow:
1. Human describes what's needed
2. AI writes code
3. Human reviews and provides feedback
4. AI refines code
```

## 📝 Session Flow

```
START SESSION
    │
    ▼
┌─────────────────┐
│ Define Goal     │ ← What are we building?
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Discuss Approach│ ← How will we build it?
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Write Code      │ ← Collaborate on implementation
│ (iterative)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Review Together │ ← Check quality, bugs
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Refine          │ ← Improve based on feedback
└────────┬────────┘
         │
         ▼
    COMPLETE ✅
```

## 🎯 Best Practices

### Communication
| Do | Don't |
|----|-------|
| Be specific about goals | Give vague instructions |
| Ask for alternatives | Accept first solution |
| Explain context | Assume AI knows everything |
| Give feedback | Silently reject |

### Code Quality
| Practice | Description |
|----------|-------------|
| Review all AI code | Don't blindly accept |
| Test suggestions | Verify they work |
| Understand changes | Ask for explanations |
| Keep it simple | Avoid over-engineering |

## 📋 Session Template

```markdown
## 🤝 Pair Programming Session

### Goal
{What we're building}

### Approach
{How we'll build it}

### Progress
- [x] Step 1: Setup
- [ ] Step 2: Core logic
- [ ] Step 3: Testing

### Decisions Made
- Decision 1: Why
- Decision 2: Why

### Questions/Blockers
- Question 1?
```

## ✅ Session Checklist

- [ ] Goal clearly defined
- [ ] Approach agreed
- [ ] Code reviewed
- [ ] Tests written
- [ ] Documentation updated
- [ ] Knowledge shared

## 🔗 Related Skills

- `code-review` - Review code quality
- `debugging` - Debug issues together
- `testing` - Write tests together
