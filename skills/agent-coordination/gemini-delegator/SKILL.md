---
name: gemini-delegator
description: >-
  Automatically delegate complex, logic-intensive tasks to Gemini CLI via
  `gemini --yolo`. Claude Code uses this skill to invoke Gemini for complex
  backend logic, intricate algorithms, or persistent bugs. Enables seamless
  AI-to-AI collaboration where Claude Code analyzes and Gemini executes.
targets:
  - '*'
---
# Gemini Delegator

## Overview

This skill enables Claude Code to automatically delegate complex, challenging tasks to Gemini CLI using `gemini --yolo`. When Claude Code encounters tasks that require different problem-solving approaches, deep logical analysis, or tasks that have proven resistant to repeated attempts, it can seamlessly invoke Gemini to provide fresh perspectives and alternative solutions. The delegation happens automatically and transparently, with Claude Code handling context preparation, execution, and solution validation.

## How Automated Delegation Works

When Claude Code determines a task is suitable for delegation:

1. **Analysis Phase**: Claude Code analyzes the task complexity, context, and requirements
2. **Decision**: Determines if delegation would be beneficial based on:
   - Task has been attempted 2+ times without success
   - High logic complexity (nested conditions, complex algorithms)
   - Backend/algorithm intensive work
   - Need for different problem-solving approach

3. **Delegation**: Automatically invokes Gemini:
   ```bash
   gemini --model gemini-2.5-pro --yolo "detailed task context with:
   - Problem description
   - Architecture and constraints
   - Previous attempts and failures
   - Success criteria"
   ```

4. **Validation**: Claude Code reviews Gemini's solution for correctness and completeness
5. **Integration**: Returns validated solution to user with transparency about using Gemini

**User Transparency**: Claude Code will inform you when it delegates to Gemini, e.g., "I'm using Gemini to generate this complex backend logic..."

## When to Use This Skill

Activate this skill specifically for:

1. **Complex Backend Logic**
   - Intricate business logic implementations
   - Complex data processing pipelines
   - Sophisticated algorithm implementations
   - Multi-layered service architectures
   - Advanced state management systems

2. **Logic-Intensive Problems**
   - Complex conditional logic with many edge cases
   - Intricate data transformations
   - Complex query optimization
   - Advanced caching strategies
   - Sophisticated error handling flows

3. **Persistent Unsolved Problems**
   - Bugs that remain after multiple fix attempts
   - Performance issues that resist optimization
   - Race conditions and concurrency problems
   - Memory leaks that are hard to track
   - Integration issues between complex systems

4. **When Different Perspective Needed**
   - Tasks attempted multiple times without success
   - Problems requiring alternative approaches
   - Situations where fresh analysis would help
   - Complex refactoring that's gotten stuck

## DO NOT Use This Skill For

- Simple CRUD operations
- Basic UI components
- Straightforward bug fixes
- Simple configuration changes
- General coding questions or tutorials

## Quick Decision Framework

**Use Gemini when:**
- ✅ Problem has been attempted 2+ times without resolution
- ✅ Logic complexity score is high (multiple nested conditions, complex state)
- ✅ Backend/algorithm heavy task
- ✅ Need different problem-solving approach

**Don't use Gemini when:**
- ❌ Problem is straightforward
- ❌ First attempt at the problem
- ❌ Simple frontend/styling work
- ❌ Basic setup or configuration

## Delegation Workflow

### Step 1: Prepare Task Context

Create clear, detailed task description including:

1. **Problem statement** - What needs to be solved
2. **Context** - Relevant code, architecture, constraints
3. **Attempts made** - What has been tried and why it failed
4. **Expected outcome** - Clear success criteria
5. **Key files** - Specific files that need attention

### Step 3: Choose Execution Strategy

#### Strategy A: Interactive Mode (Recommended for Complex Problems)

Use when problem requires exploration and iteration:

```bash
cd /path/to/project
gemini --model gemini-2.5-pro
```

Then provide detailed context:
```
I need help with [problem description].

Context:
- [Architecture overview]
- [Relevant constraints]
- [Previous attempts and failures]

The issue is in these files:
- [file1]: [specific problem]
- [file2]: [specific problem]

Goal: [clear success criteria]
```

**Advantages:**
- Can iterate on the solution
- Review changes
- Switch models with `--model`

#### Strategy B: One-Shot Mode (For Well-Defined Problems)

Use when problem is clear and specific:

```bash
gemini --model gemini-2.5-pro "detailed task description with full context"
```

Add flags as needed:
- `-y` or `--yolo` - For trusted, well-scoped tasks (auto-accept)

#### Strategy C: Resume Mode (For Persistent Problems)

Use for problems needing continuity:

```bash
gemini --model gemini-2.5-pro --resume latest
```

**Advantages:**
- Continues previous context
- Good for iterative scenarios

### Step 4: Monitor and Validate

**In interactive mode:**
- Review changes before accepting
- Use `--resume` if approach is wrong to continue context

**After execution:**
- Run tests to verify solution
- Check edge cases
- Validate performance improvements
- Document the solution approach

### Step 5: Resume or Pivot

If problem persists:

```bash
# Resume previous session
gemini --model gemini-2.5-pro --resume latest

# Or try different model
gemini --model gemini-3-pro-preview
```

## Effective Task Delegation Examples

### Example 1: Complex Backend Logic

**Scenario:** Implementing sophisticated multi-tenant data isolation with complex permission rules.

```bash
cd /path/to/project
gemini --model gemini-2.5-pro
```

```
I need to implement row-level security for a multi-tenant application.

Requirements:
- Each tenant can only access their own data
- Admin users can access all tenants
- Super admins can impersonate any user
- Audit all data access

Current architecture:
- PostgreSQL database
- Node.js/Express backend
- Using Sequelize ORM

Files involved:
- src/middleware/tenancy.js
- src/models/User.js
- src/policies/access-control.js

Previous attempts:
1. Tried global Sequelize scopes - leaked data in JOIN queries
2. Tried middleware checks - inconsistent across endpoints
3. Current approach using hooks - performance issues

Goal: Bulletproof tenant isolation with good performance
```

### Example 2: Persistent Bug

**Scenario:** Race condition causing intermittent failures.

```bash
gemini --model gemini-2.5-pro "Debug and fix race condition in payment processing:

Context:
- Stripe webhook handler in src/webhooks/stripe.js
- Order service in src/services/orders.js
- Redis cache for order status

Problem:
- 5% of payments succeed but orders stay in 'pending' state
- Happens only under high load
- Attempted fixes:
  1. Added database transaction - didn't help
  2. Increased Redis TTL - still fails
  3. Added retry logic - made it worse

Stack trace (intermittent):
[paste stack trace]

Need: Root cause analysis and fix with proper synchronization"
```

### Example 3: Complex Algorithm

**Scenario:** Optimizing complex matching algorithm.

```bash
cd /path/to/project
gemini --model gemini-2.5-pro
```

```
Need to optimize recommendation engine in src/algorithms/matching.js

Current implementation:
- O(n²) complexity with nested loops
- Processes 10k items in 30 seconds (too slow)
- Need to handle 100k+ items

Constraints:
- Must maintain ranking accuracy
- Memory limit: 2GB
- Real-time updates required

Attempted optimizations:
1. Added caching - helped but not enough
2. Tried batch processing - broke real-time requirement
3. Implemented early termination - minimal impact

Goal: Sub-second processing for 100k items
```

## Advanced Techniques

### Using Stronger Models

For extremely complex problems, request a stronger model:

```bash
gemini --model gemini-3-pro-preview
```

Then provide the complex problem.

### Leveraging MCP for Enhanced Context

Add relevant MCP servers for domain-specific knowledge:

```bash
gemini mcp add <name> <command>
```

### Multi-Session Strategy

For very difficult problems, use sessions effectively:

```bash
# List previous sessions
gemini --list-sessions

# Resume a specific session
gemini --resume <session-id>
```

## Validating Solutions

After Gemini provides solution:

1. **Review**
   Review the code changes provided by Gemini.

2. **Run Tests**
   ```bash
   npm test
   # or appropriate test command
   ```

3. **Performance Testing**
   - Benchmark critical paths
   - Load testing for backend changes
   - Profile memory usage

## Integration with Claude Code Workflow

This skill enables seamless AI-to-AI collaboration:

### Automated Workflow

1. **User Request**: "Fix this race condition bug that I've been trying to solve for hours"
2. **Claude Code Analysis**: Recognizes this fits delegation criteria (persistent problem, complex)
3. **Automatic Delegation**:
   ```bash
   gemini --model gemini-2.5-pro --yolo "Debug race condition in payment processing:
   [Full context from previous attempts]
   [Architecture details]
   [Attempted fixes and why they failed]"
   ```
4. **Gemini Execution**: Analyzes, generates solution, applies fix
5. **Claude Code Validation**: Reviews solution, runs tests, checks integration
6. **User Response**: "I've used Gemini to fix the race condition. The issue was... [explanation]"

### Manual Workflow (Still Supported)

Users can also manually invoke Gemini following the guidance in this skill for more control over the delegation process.

## Cost and Performance Considerations

**Gemini is cost-effective for:**
- Complex problems requiring deep analysis
- Tasks needing context retention (sessions)
- Problems that would take many iterations

**Use Claude Code instead for:**
- First attempts at problems
- Straightforward implementations
- Simple bug fixes

## Resources

### Reference Documentation

See `references/gemini_strategies.md` for:
- Detailed command syntax
- Complex task template examples
- Troubleshooting patterns
- Performance optimization techniques

Load this reference when detailed command syntax or advanced patterns are needed.

### Quick Reference Commands

```bash
# Interactive mode (most common for complex tasks)
cd /path/to/project
gemini --model gemini-2.5-pro

# One-shot mode with context
gemini --model gemini-2.5-pro "detailed task with full context"

# Resume previous session
gemini --model gemini-2.5-pro --resume latest

# Key options
--model <name>      # Switch models
--yolo              # Auto-accept actions
--list-sessions     # List sessions
```

### External Resources

- GitHub repository: https://github.com/google-gemini/gemini-cli
- Command reference: `gemini --help`

## Success Metrics

Track when delegation is effective:

✅ **Success indicators:**
- Problem solved after delegation
- Solution more elegant than previous attempts
- Performance improvements achieved
- Bug fixed permanently

❌ **Failure indicators:**
- Problem still unsolved
- Solution too complex
- Introduced new bugs
- Didn't understand requirements

Adjust delegation strategy based on these outcomes.
