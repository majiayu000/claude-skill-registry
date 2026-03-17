---
name: copilot-spark
description: Build apps with natural language using GitHub Copilot Spark. Perfect for rapid prototyping, teaching non-coders, and exploring ideas before committing to full implementation. Triggers on spark, prototype, app builder, no-code, low-code, natural language app, teach coding, onboarding.
---

# GitHub Copilot Spark Skill

> **AI-powered app builder for rapid prototyping and teaching**

GitHub Copilot Spark transforms natural language descriptions into working web applications. Use it to prototype ideas quickly, teach programming concepts, or bridge the gap between idea and implementation.

## Prerequisites

- **GitHub Account**: With Copilot access
- **Spark Access**: Visit [spark.github.com](https://spark.github.com) or use `gh spark` CLI
- **Browser**: Modern browser for the Spark editor

## Quick Reference

### Core Workflows

| Workflow | Description | Best For |
|----------|-------------|----------|
| **Prototype** | Describe app → Get working code | Rapid iteration, proof of concept |
| **Teach** | Explain concepts through building | Onboarding, learning |
| **Explore** | Try different approaches quickly | Architecture decisions |
| **Bridge** | Move from Spark to production code | Handoff to development |

### Key Commands

| Action | Method |
|--------|--------|
| Create new app | Describe in natural language |
| Modify app | "Change the button to blue" |
| Add feature | "Add a dark mode toggle" |
| Export code | Download or copy generated code |
| Share prototype | Generate shareable link |

## Use Cases

### 1. Rapid Prototyping

```
User: "Create a todo list app with categories and due dates"

Spark generates:
- React components for todo items
- Category filtering
- Date picker for due dates
- Local storage persistence
```

### 2. Teaching Non-Coders

```
User: "Show me how a login form works"

Spark creates:
- Email/password form
- Basic validation
- Submit handling
- Explains each part
```

### 3. Architecture Exploration

```
User: "Build a dashboard with charts showing sales data"

Spark provides:
- Chart component options
- Data structure suggestions
- Layout alternatives
```

## Spark to Production Workflow

### Step 1: Prototype in Spark
```
Describe your idea → Iterate until satisfied → Export code
```

### Step 2: Review Generated Code
```bash
# Spark exports typically include:
- src/components/     # React components
- src/styles/        # CSS/styling
- src/utils/         # Helper functions
- package.json       # Dependencies
```

### Step 3: Integrate with Production Codebase
```bash
# Copy relevant components
cp -r spark-export/src/components/* ./src/components/spark-prototype/

# Review and refactor for production standards
# - Add TypeScript types
# - Add error handling
# - Add tests
# - Follow project conventions
```

### Step 4: Production Hardening Checklist
- [ ] Add TypeScript types/interfaces
- [ ] Implement proper error handling
- [ ] Add unit and integration tests
- [ ] Apply project styling conventions
- [ ] Add accessibility attributes
- [ ] Implement proper state management
- [ ] Add loading and error states
- [ ] Security review (input validation, XSS prevention)

## Best Practices

### Effective Prompts

| ✅ Good Prompts | ❌ Avoid |
|-----------------|----------|
| "Todo app with drag-and-drop reordering" | "Make an app" |
| "Dashboard showing user activity metrics" | "Analytics thing" |
| "Form with email validation and submit" | "Some inputs" |
| "Card grid with hover effects" | "Display stuff" |

### Iteration Tips

1. **Start simple**: Begin with core functionality
2. **Iterate incrementally**: Add features one at a time
3. **Be specific**: "Blue button" vs "styled button"
4. **Reference examples**: "Like Twitter's compose box"

### Teaching Approach

1. **Show, don't tell**: Let Spark generate, then explain
2. **Break it down**: Ask for one concept at a time
3. **Compare approaches**: "Show me two ways to do this"
4. **Explain the why**: Ask Spark to comment the code

## Integration with This Repository

### Using Spark Prototypes

```bash
# 1. Create prototype in Spark
# 2. Export to local directory
# 3. Use the bridge prompt to integrate

/spark-bridge --source ./spark-export --target ./src/features/new-feature
```

### Related Resources

| Resource | Purpose |
|----------|---------|
| `@spark-prototyper` | Agent for guided prototyping |
| `/spark-prototype` | Quick prototype prompt |
| `/spark-teach` | Teaching/onboarding prompt |
| `reference.md` | Detailed command reference |

## Limitations

- **Complexity**: Best for simple to medium complexity apps
- **Backend**: Limited backend/API generation
- **State**: Basic state management only
- **Testing**: No test generation
- **Types**: Limited TypeScript support

## When to Use Spark vs. Traditional Development

| Use Spark When | Use Traditional Dev When |
|----------------|-------------------------|
| Exploring ideas | Production code |
| Quick demos | Complex logic |
| Teaching concepts | Team collaboration |
| UI prototyping | Backend services |
| Client presentations | Security-critical |

---

## Related Documentation

- [Spark Workflow Guide](../../../docs/guides/spark-workflow.md)
- [Reference Documentation](./reference.md)
- [Spark Prototyper Agent](../../agents/spark-prototyper.md)
