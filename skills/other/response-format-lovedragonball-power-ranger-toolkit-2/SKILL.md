# 📝 Response Format Skill

---
name: response-format
description: Format AI responses for clarity, readability, and actionability
---

## 🎯 Purpose

Ensure all AI responses are well-formatted, easy to understand, and actionable for the user.

## 📋 When to Use

- Every response to user
- Documentation generation
- Report creation
- Summary generation

## 🔧 Formatting Guidelines

### Headers
```markdown
# H1 - Main Topic (use sparingly)
## H2 - Sections
### H3 - Subsections
#### H4 - Details (rarely needed)
```

### Lists
```markdown
**Bullet Lists** - For unordered items:
- Item 1
- Item 2
  - Sub-item

**Numbered Lists** - For sequences:
1. First step
2. Second step
3. Third step
```

### Code Blocks
````markdown
**Inline code**: Use `backticks` for code

**Code block with language**:
```javascript
const example = "highlighted";
```
````

### Tables
```markdown
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Data 1   | Data 2   | Data 3   |
```

## 📊 Response Templates

### Summary Response
```markdown
## 📋 Summary

**Goal**: [What we're doing]

**Key Points**:
- Point 1
- Point 2
- Point 3

**Next Steps**:
1. [Action 1]
2. [Action 2]
```

### Technical Explanation
```markdown
## 🔧 [Topic]

### What
[Brief explanation]

### Why
[Reasoning]

### How
```code
[Implementation]
```

### Example
[Usage example]
```

### Problem/Solution
```markdown
## 🐛 Problem

[Description of issue]

## ✅ Solution

[How to fix]

## 💡 Prevention

[How to avoid in future]
```

## 🎨 Visual Enhancements

### Emoji Usage
| Category | Emojis |
|----------|--------|
| Success | ✅ 🎉 🟢 |
| Warning | ⚠️ 🟡 |
| Error | ❌ 🔴 🐛 |
| Info | ℹ️ 💡 📋 |
| Tasks | 📋 ✏️ 🔧 |

### Emphasis
```markdown
**Bold** - Important terms
*Italic* - Subtle emphasis
`Code` - Technical terms
> Quote - Callouts
```

### Alerts (GitHub style)
```markdown
> [!NOTE]
> Helpful information

> [!TIP]
> Optimization suggestion

> [!IMPORTANT]
> Critical information

> [!WARNING]
> Potential issues

> [!CAUTION]
> Dangerous actions
```

## 📏 Response Length Guidelines

| Type | Length | Example |
|------|--------|---------|
| Quick answer | 1-3 sentences | Yes/No questions |
| Explanation | 1-2 paragraphs | How-to questions |
| Tutorial | Multiple sections | Step-by-step guides |
| Report | Full document | Analysis, summaries |

## ✅ Response Checklist

- [ ] Clear structure with headers
- [ ] Scannable (bullets, tables)
- [ ] Code properly formatted
- [ ] Actionable next steps
- [ ] Appropriate length
- [ ] Emoji for visual clarity

## 🔗 Related Skills

- `documentation` - Full docs
- `progress-tracking` - Progress reports
- `business-context` - Business reports
