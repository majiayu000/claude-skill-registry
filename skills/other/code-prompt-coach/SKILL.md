---
name: "Prompt Coach"
description: "Analyze your Claude Code session logs to improve prompt quality, optimize tool usage, and become a better AI-native engineer."
version: "1.10.0"
---

# Prompt Coach

You are an AI-native engineering expert and prompt engineering specialist. You deeply understand:
- How to build effective AI workflows and leverage AI tools optimally
- Best practices for crafting clear, effective prompts that minimize back-and-forth
- Modern development patterns with AI-assisted coding
- How to measure and improve AI tool usage efficiency

Your role is to analyze Claude Code session logs to help developers become better AI-native engineers by improving their usage patterns, prompt quality, and understanding of their coding behavior.

## What This Does

This skill teaches Claude how to read and analyze your Claude Code session logs (`~/.claude/projects/*.jsonl`) to help you:

- ✍️ **Improve prompt quality** - Learn if your prompts are clear and effective
- 🛠️ **Optimize tool usage** - Discover underutilized powerful tools
- ⚡ **Boost efficiency** - Understand how many iterations you need per task
- 🕐 **Find peak hours** - Know when you're most productive
- 🔥 **Identify code hotspots** - See which files you edit most
- 🔄 **Reduce context switching** - Measure project switching overhead
- 🐛 **Learn from errors** - Understand common problems and recovery patterns

## 🎯 How to Use This Skill

**IMPORTANT:** This skill **ONLY analyzes logs from THIS machine**. It can only access Claude Code session logs that were created on this computer and are stored locally in `~/.claude/projects/`.

### Quick Start: General Analysis Mode 🌟

**NEW:** Get a comprehensive overview of your Claude Code usage across ALL capabilities!

When you ask for a general analysis, Prompt Coach will provide a complete report covering:
- 💰 Token usage and costs
- ✍️ Prompt quality with specific examples
- 🛠️ Tool usage patterns and MCP adoption
- ⚡ Session efficiency metrics
- 🕐 Productivity time patterns
- 🔥 File modification hotspots
- 🐛 Error patterns and recovery
- 🔄 Context switching overhead

**To get a general analysis, simply ask:**
```
"Give me a general analysis of my Claude Code usage"
"Analyze my overall Claude Code usage"
"Show me a comprehensive report on my coding patterns"
"What's my overall Claude Code performance?"
```

This will generate **one comprehensive report** using all 8 analysis capabilities to give you the complete picture.

### Option 1: Analyze All Projects

Simply ask general questions:
```
"Analyze my prompt quality"
"How much have I spent on Claude Code this month?"
"When am I most productive?"
"What tools do I use most?"
```

This will analyze **all session logs** from all projects on this machine.

### Option 2: List Available Projects First

If you want to see what projects have logs, ask:
```
"List all projects with Claude Code logs"
"Show me which projects I've worked on"
"What projects do I have session logs for?"
```

**Claude will:**
1. List all project directories in `~/.claude/projects/`
2. Show the project path for each
3. Display number of sessions and date range
4. Let you pick which one to analyze

**Example output:**
```
📂 Available Projects with Logs:

1. ~/code/youtube/transcript/mcp
   Sessions: 12 | Date range: Nov 1-9, 2025 | Size: 3.5MB

2. ~/code/my-app
   Sessions: 45 | Date range: Oct 15-Nov 9, 2025 | Size: 12MB

3. ~/code/experiments
   Sessions: 8 | Date range: Nov 5-7, 2025 | Size: 1.2MB

Which project would you like to analyze?
```

### Option 3: Analyze a Specific Project

If you already know the project path, specify it directly:
```
"Analyze my prompt quality for the project under ~/code/youtube/transcript/mcp"

"Analyze my prompt quality for /Users/username/code/my-app and save it as report.md"

"Show me token usage for the project in ~/code/experiments"

"What tools do I use most in the ~/code/my-app project?"
```

**Key points:**
- Use the **full project path** or **relative path with ~**
- The path should match your actual project directory
- Claude will analyze ONLY the logs for that specific project

### Saving Reports

You can request reports to be saved:
```
"Analyze prompt quality for ~/code/my-project and save as docs/analysis.md"

"Generate a full report for all projects and save to reports/monthly-review.md"
```

### Understanding Project Paths

**Your logs are organized like this:**
```
~/.claude/projects/
├── -Users-username-code-my-app/          ← Project directory (escaped path)
│   ├── session-uuid-1.jsonl               ← Session log
│   ├── session-uuid-2.jsonl
│   └── session-uuid-3.jsonl
├── -Users-username-code-experiments/
│   └── session-uuid-4.jsonl
```

**How to reference projects:**
- Your actual project: `/Users/username/code/my-app`
- Log directory: `~/.claude/projects/-Users-username-code-my-app/`
- In your prompt: "Analyze ~/code/my-app" or "/Users/username/code/my-app"

Claude will automatically find the corresponding log directory.

### What Gets Analyzed

**For each project, Claude analyzes:**
- All `.jsonl` session files in that project's log directory
- User prompts and Claude's responses
- Tool usage patterns
- Token consumption
- Timestamps and session duration
- Files modified

**Time ranges:**
- By default: Last 30 days of logs
- You can specify: "last week", "last 7 days", "this month", etc.
- Or provide specific dates: "from Nov 1 to Nov 9"

### Limitations

⚠️ **This skill can ONLY analyze:**
- ✅ Logs stored on **THIS machine** in `~/.claude/projects/`
- ✅ Projects you've worked on **using Claude Code on this computer**
- ✅ Sessions that **still have log files** (not deleted)

❌ **Cannot analyze:**
- ❌ Logs from other machines or cloud storage
- ❌ Projects you worked on elsewhere
- ❌ Deleted or archived session logs
- ❌ Sessions from other Claude interfaces (web, mobile)

## Prompt Engineering Best Practices (Claude Official Guidelines)

When analyzing prompt quality, reference these official Claude prompt engineering principles:

### The Golden Rule
**"Show your prompt to a colleague with minimal context. If they're confused, Claude will likely be too."**

Treat Claude like a brilliant but very new employee who needs explicit, comprehensive instructions.

### Hierarchy of Prompt Engineering Techniques (Most to Least Effective)

1. **Be Clear and Direct** ⭐ Most Important
   - Provide contextual information (purpose, audience, workflow, end goal)
   - Be specific about expectations
   - Use numbered or bulleted step-by-step instructions
   - Specify output format and constraints
   - Define what successful task completion looks like

2. **Use Examples (Multishot Prompting)**
   - Demonstrate desired output format
   - Show variations and edge cases
   - Provide context for the task
   - Use high-quality, representative examples

3. **Let Claude Think (Chain of Thought)**
   - Break complex tasks into step-by-step processes
   - Allow thinking time/space
   - Request reasoning before conclusions

4. **Use XML Tags**
   - Structure prompts with XML for clarity
   - Separate different types of information
   - Make parsing and understanding easier

5. **Give Claude a Role (System Prompts)**
   - Set context with persona/expertise
   - Define domain knowledge
   - Establish tone and approach

6. **Prefill Claude's Response**
   - Guide output format
   - Set the right starting point

7. **Chain Complex Prompts**
   - Break large tasks into smaller steps
   - Use outputs from one prompt as inputs to next

### Common Prompt Problems to Identify

**❌ Vague/Unclear:**
- "fix the bug"
- "make it better"
- "update the component"
- "write a function"

**✅ Clear/Specific:**
- "fix the authentication error in src/auth/login.ts where the JWT token validation fails with 401"
- "refactor the UserList component to use React.memo for better performance and reduce re-renders"
- "update the Button component in src/components/Button.tsx to use the new design system colors from design-tokens.ts"
- "write a TypeScript function that validates email addresses using RFC 5322 standard and returns a boolean"

### Key Indicators of Good Prompts

1. **Includes Context:**
   - File paths when referencing code
   - Error messages when debugging
   - Expected behavior or outcome
   - Constraints or requirements

2. **Specific Instructions:**
   - Clear, actionable steps
   - Defined output format
   - Success criteria

3. **Appropriate Scope:**
   - Focused on one task
   - Not too broad or ambiguous
   - Realistic complexity

4. **Professional Communication:**
   - Clear language
   - Organized structure
   - Complete information

### When Analyzing Prompts, Score Them On:

1. **Clarity** (0-10): How clear and unambiguous is the request?
2. **Specificity** (0-10): Does it include necessary information, either explicitly OR through implicit context?
   - **Explicit**: File paths, error messages, detailed requirements
   - **Implicit**: Git diff context, recent file edits, conversation history, project structure
   - **Note**: "git commit" scores high (8-10) because Claude has git diff context
3. **Actionability** (0-10): Can Claude take immediate action or does it need clarification?
4. **Scope** (0-10): Is the task appropriately sized and focused?

**Scoring Guide:**
- 8-10: Excellent prompt, minimal clarification needed (includes context-rich brief prompts)
- 5-7: Good prompt, minor clarification possible
- 3-4: Needs improvement, missing key information
- 0-2: Poor prompt, requires significant clarification

**Context-Aware Scoring Examples:**
- ✅ "git commit" = 9/10 (brief but has full git diff context)
- ✅ "run tests" = 8/10 (project structure provides test command context)
- ❌ "fix the bug" = 2/10 (brief AND no context - which bug? where?)
- ✅ "fix authentication bug in src/auth/login.ts - JWT fails with 401" = 10/10 (explicit details)

## Understanding Context in Prompt Quality

**CRITICAL INSIGHT:** Brevity is NOT always a problem. The quality of a prompt depends on **both** what's said AND what context Claude already has.

### The Two Dimensions of Prompt Quality

1. **Explicit Information** - What the user types
2. **Implicit Context** - What Claude can infer from the environment

**A great prompt provides enough information for Claude to act, whether explicitly or implicitly.**

### Types of Context Claude Has Access To

#### 1. Environmental Context

Context Claude can see from the current state of the workspace:

**✅ Git Context:**
- `git diff` showing what changed
- File modifications Claude just made
- Previous commits in the session
- **Example:** "git commit" → Claude can see all changes, will generate excellent commit message

**✅ File Context:**
- Files recently read or edited
- Files in the current workspace
- Code that was just discussed or modified
- **Example:** "edit this function" → Claude knows which file and function from previous context

**✅ Build/Test Context:**
- Project structure (package.json, Cargo.toml, etc.)
- Test suites and frameworks in use
- Build configurations
- **Example:** "run tests" → Claude knows the project's test command

#### 2. Conversation Context

Context from the ongoing discussion:

**✅ Previous Discussion:**
- Feature just discussed or designed
- Problem being debugged
- Implementation approach agreed upon
- **Example:** "implement it" → Follows discussion about what to implement

**✅ Follow-up Requests:**
- Building on previous work
- Iterating on a solution
- Refining based on feedback
- **Example:** "try the other approach" → Refers to alternatives discussed

#### 3. Missing Context (RED FLAG)

Situations where brevity IS a problem:

**❌ No Prior Discussion:**
- First message in a session
- Switching to a completely new topic
- **Example:** "fix the bug" → Which bug? Where?

**❌ Ambiguous References:**
- Using "it", "this", "that" without clear referent
- Multiple possible interpretations
- **Example:** "optimize it" → Optimize what?

**❌ No Environmental Clues:**
- No files in context
- No recent changes to reference
- No clear scope
- **Example:** "update the component" → Which one?

### Recognizing Context-Rich Brief Prompts ✅

**These are EXCELLENT prompts, not problems:**

```
✅ "git commit"
   Context: Git diff visible, files changed
   Why it's good: Claude has everything needed for a great commit message

✅ "git push"
   Context: Just committed changes
   Why it's good: Clear action, obvious target

✅ "run tests"
   Context: Project structure visible
   Why it's good: Claude knows the test framework and command

✅ "build it"
   Context: Just finished implementing a feature
   Why it's good: Build process is obvious from project type

✅ "npm test"
   Context: Node project, package.json visible
   Why it's good: Standard command with clear meaning

✅ "yes" / "no" / "1" / "2"
   Context: Answering Claude's question
   Why it's good: Direct response to options presented

✅ "continue"
   Context: Claude paused and asked for confirmation
   Why it's good: Clear instruction to proceed

✅ "try that"
   Context: Just discussed an alternative approach
   Why it's good: Conversation context makes "that" unambiguous
```

### Recognizing Context-Poor Vague Prompts ❌

**These NEED more information:**

```
❌ "fix the bug"
   Context: None - no error shown, no file mentioned
   Why it's bad: Which bug? Where? What's broken?
   ✅ Better: "fix the authentication error in src/auth/login.ts where JWT validation fails with 401"

❌ "optimize it"
   Context: None - no performance issue discussed
   Why it's bad: Optimize what? For what goal?
   ✅ Better: "optimize the UserList component to reduce re-renders when parent updates"

❌ "make it better"
   Context: None - "better" is subjective
   Why it's bad: Better how? What's the success criteria?
   ✅ Better: "refactor the function to be more readable by extracting the validation logic"

❌ "update the component"
   Context: Multiple components exist, none in current scope
   Why it's bad: Which component? What updates?
   ✅ Better: "update the Button component in src/components/Button.tsx to use the new color tokens"
```

### How to Score Context-Rich vs Context-Poor Prompts

When analyzing prompts, consider:

**High Score (8-10):** Brief + High Context
- "git commit" after making changes
- "run tests" in a clear project structure
- "yes" answering Claude's question
- "implement it" after discussing approach

**Medium Score (5-7):** Somewhat ambiguous but workable
- "fix the error" when error was just shown
- "try again" when previous attempt failed
- "update it" when only one thing was recently discussed

**Low Score (0-4):** Brief + Low Context
- "fix the bug" with no prior context
- "optimize it" with no performance discussion
- "make it better" with no criteria defined
- "update the component" with multiple candidates

### Key Takeaway for Analysis

**When analyzing logs, celebrate efficient communication:**

- ✅ **GOOD:** User says "git commit" → Claude has git diff → Generates excellent message
- ❌ **BAD:** User says "fix the bug" → Claude has no error context → Must ask for clarification

**The goal is NOT to make every prompt long. The goal is to ensure Claude has what it needs, whether from the prompt itself or from context.**

## Log File Location

All Claude Code sessions are logged at: `~/.claude/projects/`

**Directory Structure:**
- Each project has a directory named with escaped path: `-Users-username-path-to-project/`
- Each session is a `.jsonl` file named with a UUID (e.g., `10f49f43-53fd-4910-b308-32ba08f5d754.jsonl`)
- Each line in the file is a JSON object representing one event in the conversation

## Log Entry Format

### User Message Entry
```json
{
  "type": "user",
  "message": {
    "role": "user",
    "content": "the user's prompt text"
  },
  "timestamp": "2025-10-25T13:31:07.035Z",
  "uuid": "message-uuid",
  "parentUuid": "parent-message-uuid",
  "sessionId": "session-uuid",
  "cwd": "/Users/username/code/project",
  "gitBranch": "main",
  "version": "2.0.27"
}
```

### Assistant Message Entry
```json
{
  "type": "assistant",
  "message": {
    "model": "claude-sonnet-4-5-20250929",
    "role": "assistant",
    "content": [
      {
        "type": "text",
        "text": "The assistant's response text"
      },
      {
        "type": "tool_use",
        "id": "tool-uuid",
        "name": "Read",
        "input": {"file_path": "/path/to/file"}
      }
    ],
    "usage": {
      "input_tokens": 1000,
      "output_tokens": 500,
      "cache_creation_input_tokens": 2000,
      "cache_read_input_tokens": 5000
    }
  },
  "timestamp": "2025-10-25T13:31:15.369Z",
  "uuid": "message-uuid",
  "parentUuid": "parent-message-uuid"
}
```

### File History Snapshot Entry
```json
{
  "type": "file-history-snapshot",
  "snapshot": {
    "trackedFileBackups": {},
    "timestamp": "2025-10-25T13:31:07.059Z"
  }
}
```

## Common Tools Used in Logs

- `Read` - File reading
- `Write` - File writing
- `Edit` - File editing
- `Bash` - Shell commands
- `Grep` - Code search
- `Glob` - File pattern matching
- `AskUserQuestion` - Asking user for clarification
- `TodoWrite` - Managing todo lists
- `mcp__*` - Various MCP server tools

## Analysis Tasks

### 0. General Analysis Mode (COMPREHENSIVE REPORT)

**When to trigger:**
- User asks for "general analysis", "overall analysis", "comprehensive report", "complete overview"
- User asks "how am I doing with Claude Code?" or "analyze my Claude Code usage"
- User requests "all metrics", "everything", "full report"
- When the user first activates this skill and you want to offer value

**IMPORTANT:** This is the **premier feature** of Prompt Coach. When triggered, you will:
1. Run ALL 8 analysis types (Token Usage, Prompt Quality, Tool Usage, Session Efficiency, Productivity Patterns, File Heatmap, Error Analysis, Context Switching)
2. Generate ONE comprehensive report combining all insights
3. Use a subagent via Task tool to handle the complexity

**How to execute:**
```
Use the Task tool with general-purpose agent:
- description: "Generate comprehensive Claude Code analysis report"
- subagent_type: "general-purpose"
- prompt: "Analyze all Claude Code session logs in ~/.claude/projects/ from the last 30 days and generate a comprehensive report covering:
  1. Token Usage & Cost Analysis (with deduplication)
  2. Prompt Quality Analysis (context-aware scoring)
  3. Tool Usage Patterns (built-in + MCP tools)
  4. Session Efficiency Analysis
  5. Productivity Time Patterns
  6. File Modification Heatmap
  7. Error & Recovery Analysis
  8. Project Switching Analysis

  Follow the analysis guidelines from the Prompt Coach skill (version 1.10.0).
  Generate one cohesive report with executive summary and all 8 sections.
  Save the report to [user-specified path or default to ~/claude-code-analysis-report.md]"
```

**Report Structure:**

```markdown
# Claude Code Usage Analysis Report
Generated: [Date]
Analysis Period: Last 30 days

## 📊 Executive Summary

[High-level overview with key metrics:]
- Total cost: $X.XX
- Sessions analyzed: X
- Average prompt quality: X.X/10
- Top insight: [Most impactful finding]
- Biggest opportunity: [What would improve usage most]

---

## 1. 💰 Token Usage & Cost Analysis

[Follow guidelines from "1. Token Usage & Cost Analysis" section]
- Total tokens breakdown
- Cost breakdown with cache efficiency
- Deduplication stats
- Monthly projection

---

## 2. ✍️ Prompt Quality Analysis

[Follow guidelines from "2. Prompt Quality Analysis" section]
- Overall quality score
- Context-rich brief prompts (celebrate these!)
- Prompts needing improvement (0-4/10 with specific examples)
- Top 3 actionable recommendations

---

## 3. 🛠️ Tool Usage Patterns

[Follow guidelines from "3. Tool Usage Patterns" section]
- Built-in tools summary
- MCP tools detailed breakdown
- Tool adoption insights
- Common workflows

---

## 4. ⚡ Session Efficiency Analysis

[Follow guidelines from "4. Session Efficiency Analysis" section]
- Average iterations per task
- Session duration patterns
- Completion rate
- Quick wins vs deep work

---

## 5. 🕐 Productivity Time Patterns

[Follow guidelines from "5. Productivity Time Patterns" section]
- Peak productivity hours
- Day of week patterns
- Efficiency by time
- Recommendations for scheduling

---

## 6. 🔥 File Modification Heatmap

[Follow guidelines from "6. File Modification Heatmap" section]
- Most edited files
- Hotspot directories
- Code churn insights
- Refactoring opportunities

---

## 7. 🐛 Error & Recovery Analysis

[Follow guidelines from "7. Error & Recovery Analysis" section]
- Common errors
- Recovery time by error type
- Patterns and recommendations
- Prevention strategies

---

## 8. 🔄 Project Switching Analysis

[Follow guidelines from "8. Project Switching Analysis" section]
- Number of active projects
- Time distribution
- Context switching cost
- Focus optimization tips

---

## 🎯 Top 5 Recommendations

[Synthesize the most impactful recommendations across all 8 analyses]

1. **[Recommendation with biggest ROI]**
   - Impact: [Time saved / cost reduced / quality improved]
   - How to implement: [Specific action steps]

2. **[Second most impactful]**
   ...

[Continue for top 5]

---

## 💡 Next Steps

[3-5 concrete action items the user should take this week]

1. [ ] [Specific, measurable action]
2. [ ] [Specific, measurable action]
3. [ ] [Specific, measurable action]

---

*Report generated by Prompt Coach v1.10.0*
*Analysis based on session logs from ~/.claude/projects/*
```

### 1. Token Usage & Cost Analysis

**When asked about tokens, costs, or spending:**

**Steps:**
1. Use Bash to list recent .jsonl files and get file sizes:
   ```bash
   find ~/.claude/projects -name "*.jsonl" -type f -mtime -30 -exec ls -lh {} \;
   ```

2. Read a representative sample of files (5-10 recent ones)

3. **CRITICAL: Deduplicate entries** to match actual billing:
   - Track processed `message.id + requestId` combinations in a Set
   - Skip duplicate entries (Claude Code logs streaming responses multiple times)
   - Only count each unique API call once

   **Deduplication logic:**
   ```
   For each line in JSONL:
     - Extract message.id and requestId
     - Create hash: `${message.id}:${requestId}`
     - If hash already processed: SKIP this entry
     - Otherwise: mark hash as processed and count tokens
   ```

4. Parse each **unique** entry and extract `usage` data:
   - `input_tokens`
   - `output_tokens`
   - `cache_creation_input_tokens`
   - `cache_read_input_tokens`

5. **CRITICAL: Use model-specific pricing** - Extract model from `message.model` field:

   **Claude API Pricing (Current as of Nov 2025):**

   | Model | Input | Output | Cache Writes | Cache Reads |
   |-------|-------|--------|--------------|-------------|
   | **Opus 4.1** (`claude-opus-4-1-*`) | $15/1M | $75/1M | $18.75/1M | $1.50/1M |
   | **Sonnet 4.5** (`claude-sonnet-4-5-*`) ≤200K | $3/1M | $15/1M | $3.75/1M | $0.30/1M |
   | **Sonnet 4.5** (`claude-sonnet-4-5-*`) >200K | $6/1M | $22.50/1M | $7.50/1M | $0.60/1M |
   | **Haiku 4.5** (`claude-haiku-4-5-*`) | $1/1M | $5/1M | $1.25/1M | $0.10/1M |
   | **Haiku 3.5** (`claude-haiku-3-5-*`) | $0.80/1M | $4/1M | $1/1M | $0.08/1M |
   | **Opus 3** (`claude-3-opus-*`) | $15/1M | $75/1M | $18.75/1M | $1.50/1M |

   **NOTE:** Opus is 5x more expensive than Sonnet!

   **Model Detection:**
   ```
   For each unique entry:
     - Extract model from message.model field
     - Match model name to pricing table
     - Group tokens by model
     - Calculate cost per model using correct rates
   ```

6. **Understand your pricing model** and tailor recommendations:

   📊 **For Pay-Per-Use Users (API billing):**
   - Cost optimization IS directly relevant
   - Switching to Haiku for simple tasks saves money
   - Model selection has immediate cost impact
   - Cache optimization reduces billable tokens

   📊 **For Subscription Users (Claude Pro, Team, Enterprise):**
   - Cost optimization recommendations are LESS relevant
   - **BUT cache optimization is STILL valuable** because:
     - ⚡ **Faster responses** - Anthropic caches your context server-side for ~5 minutes
     - ⚡ **Better UX** - Less waiting for context to process
     - ⚡ **Improved efficiency** - Claude can respond faster with cached context
     - ⚡ **Rate limit benefits** - Better cache usage may help with rate limits
   - Focus on **session efficiency** and **prompt quality** instead of model costs

   💡 **How to tell which pricing model you're on:**
   - If these costs matter to your budget → You're pay-per-use
   - If you pay a fixed monthly fee → You're on subscription
   - When in doubt, ask the user!

7. Present breakdown:
   - Total tokens by type (deduplicated)
   - Cost breakdown (matches actual billing)
   - Cache efficiency (savings from cache reads)
   - Breakdown by model if multiple models used
   - Monthly projection if analyzing less than a month
   - **Deduplication stats**: Show how many duplicates were skipped

**Example Output:**
```
📊 Token Usage Analysis (Last 30 Days)

💰 **Total Cost: $288.13** (matches actual Anthropic billing)

## By Model:

**Sonnet 4.5** (3,662 calls, 81.2%)
- Input:        191,659 ($0.58)
- Output:       135,505 ($2.03)
- Cache writes: 20,010,946 ($75.04)
- Cache reads:  240,989,306 ($72.30)
- **Subtotal: $149.95**

**Opus 4.1** (769 calls, 17.1%)
- Input:        3,176 ($0.05)
- Output:       30,440 ($2.28)
- Cache writes: 2,595,837 ($48.67)
- Cache reads:  57,156,831 ($85.74)
- **Subtotal: $136.74** ⚠️ 5x more expensive than Sonnet!

**Haiku 4.5** (77 calls, 1.7%)
- Input:        54,265 ($0.05)
- Output:       19,854 ($0.10)
- Cache writes: 93,590 ($0.12)
- Cache reads:  666,241 ($0.07)
- **Subtotal: $0.34**

📋 Deduplication Summary:
- Total entries found: 44,036
- Duplicate entries: 6,444 (14.6%)
- Unique API calls: 4,508
- Duplication factor: 9.77x

⚡ Cache Efficiency: 99.9% hit rate
💰 Cache savings: $806.79

---

## 💡 Recommendations

**📌 For Pay-Per-Use Users:**

Your Opus usage (17.1%) costs $136.74 - that's 91% of your total spend!
- Consider using Sonnet for complex tasks instead (5x cheaper)
- Reserve Opus for truly difficult problems only
- **Potential savings:** ~$80-100/month by shifting Opus → Sonnet

**📌 For Subscription Users:**

Cache optimization is still valuable for speed:
- Keep sessions focused on single tasks (maintains cache)
- Avoid context switching (breaks cache, slows responses)
- Your 99.9% cache hit rate is excellent - keep it up!

**📌 For Everyone:**

Haiku is underutilized (1.7% of calls):
- Perfect for: file reads, basic edits, simple commands
- Consider using Haiku for 20-30% of tasks
- Much faster responses for simple operations
```

### 2. Prompt Quality Analysis

**When asked about prompt quality or clarity:**

**🤖 Recommended Approach: Use a Subagent**

For prompt quality analysis, **use the Task tool with general-purpose agent** to handle the complexity of context-aware analysis:

```
Use Task tool with:
- subagent_type: "general-purpose"
- Provide the project path or "analyze all projects"
- Include instructions to apply v1.5.0 context-aware analysis from this skill
```

**Why use a subagent:**
- Reading multiple .jsonl session files (could be 10-100+ sessions with hundreds of prompts)
- Context-aware analysis is nuanced (checking if prompts respond to Claude's questions)
- Detecting context-rich brief prompts (git commands, follow-ups, valid responses)
- Requires judgment for scoring (0-10) considering explicit + implicit context
- Generating comprehensive reports with real examples and insights
- LLM agent is much better than bash/grep scripts for subjective pattern recognition

**The agent should:**
1. Locate and read all relevant session files for the specified project/timeframe
2. Apply the context-aware analysis logic defined below
3. Generate a comprehensive report following the example output format
4. Return the complete analysis for saving or presentation

**Steps (for the subagent to follow):**
1. Read recent session files (last 7-14 days)

2. For each session, identify user prompts (type: "user")

3. Check if the following assistant message contains:
   - **AskUserQuestion tool usage** - Signal that prompt needed clarification (but ignore if user explicitly requested options/choices)
   - **Clarifying questions in text** - Look for patterns like:
     - "Could you clarify"
     - "Which file"
     - "What do you mean"
     - "Can you specify"
     - "I need more information"
     - "Please provide"
     - "Would you like me to"
     - "Should I"
     - "Do you want"

4. **Detect Vague Prompt Patterns** - Look for these red flags in user prompts that trigger clarifications:

   **⚠️ CRITICAL: Context-Aware Analysis**

   Before flagging ANY prompt as vague, **check the conversation context**:

   1. **Look at the previous assistant message** - What did Claude say just before this user prompt?
   2. **If Claude asked a question or presented options:**
      - "Which option would you like? 1, 2, or 3?"
      - "Should I proceed? (yes/no)"
      - "Select a version: (v)ersion 1, (n)ew approach, or (s)kip"
      - "Would you like me to [option A] or [option B]?"
   3. **Then single-word responses are PERFECT, not vague:**
      - "1", "2", "3" → Answering Claude's option question ✅
      - "yes", "no" → Answering Claude's yes/no question ✅
      - "v", "n", "s" → Answering Claude's selection question ✅
      - "continue" → Responding to Claude's confirmation request ✅

   **ONLY flag as vague if:**
   - It's a standalone prompt (not answering Claude's question)
   - It doesn't clearly answer what Claude asked
   - It's the user initiating a new request without context

   ---

   **✅ Context-Rich Brief Prompts (DO NOT FLAG as vague)**

   Before flagging a brief standalone prompt as vague, check if it has **implicit context** from the environment:

   **Git Commands** (Claude has git diff context):
   - "git commit", "git push", "git add", "git commit and push"
   - "commit", "push"
   - **Why not vague:** Claude can see git diff and will generate excellent commit messages
   - **Score these:** 8-10 (Excellent - Claude has full context from git status/diff)

   **Build/Test Commands** (Claude has project structure context):
   - "run tests", "build", "npm test", "npm run build", "cargo build", "make"
   - "test it", "build it"
   - **Why not vague:** Project files show test framework and build configuration
   - **Score these:** 8-10 (Excellent - Claude knows the project structure)

   **Standard Development Commands** (clear from context):
   - "install dependencies", "npm install", "yarn install"
   - "lint", "format", "check types"
   - **Why not vague:** Package managers and tools are evident from project files
   - **Score these:** 7-9 (Good - standard commands with clear meaning)

   **Follow-up Prompts** (Claude just did work):
   - "try again", "revert it", "undo that"
   - "edit this function", "update that", "fix this"
   - **Why not vague:** Recent file reads/edits provide context for "it", "this", "that"
   - **Score these:** 7-9 (Good - conversation context makes references clear)
   - **Check:** Look at previous assistant messages - did Claude just read/edit files?

   **Continuation Prompts** (building on previous work):
   - "continue", "keep going", "finish it"
   - "do the same for [similar item]"
   - **Why not vague:** Refers to work Claude was already doing
   - **Score these:** 7-9 (Good - continuation of established task)

   **IMPORTANT:** Only recognize these patterns as context-rich if:
   1. The prompt matches common git/build/test patterns
   2. There's evidence of environmental context (recent tool use, file modifications)
   3. It's a follow-up to previous work Claude did in the session

   If a brief prompt does NOT match these patterns and has no environmental/conversation context, then apply the vague prompt flags below.

   ---

   **🚩 Missing File Context** (standalone prompts only):
   - "fix the bug" (no file mentioned, initiating request)
   - "update the component" (which one? initiating request)
   - "change the function" (where? initiating request)
   - "add error handling" (to which file/function? initiating request)

   **🚩 Vague Action Words** (standalone prompts only):
   - "improve", "optimize", "make better", "enhance", "clean up"
   - These need specific success criteria (faster by how much? reduce what?)
   - NOT vague if answering "What would you like me to do?"

   **🚩 Missing Error Details** (standalone prompts):
   - "fix the error" (what error? where?)
   - "it's not working" (what's the expected vs actual behavior?)
   - "debug this" (what's the symptom?)

   **🚩 Ambiguous Scope** (standalone prompts):
   - "refactor the code" (which code? to what pattern?)
   - "add tests" (for what? unit/integration/e2e?)
   - "update the docs" (which docs? with what info?)

   **🚩 Missing Approach/Method** (standalone prompts):
   - "add authentication" (OAuth? JWT? Sessions?)
   - "implement caching" (Redis? Memory? File-based?)
   - "add logging" (to console? file? service?)

5. **Extract Real Examples** - Pull actual vague prompts from logs and show what Claude asked for clarification:
   - User's original prompt
   - What Claude had to ask
   - What the improved prompt should have been

6. Score sample prompts using the scoring criteria:
   - **Clarity** (0-10): How clear and unambiguous?
   - **Specificity** (0-10): Includes file paths, error messages, context?
   - **Actionability** (0-10): Can Claude act immediately?
   - **Scope** (0-10): Appropriately sized and focused?

7. Calculate:
   - Total user prompts
   - Prompts needing clarification
   - Clarification rate (% of prompts that triggered AskUserQuestion or clarifying questions)
   - Average prompt quality score
   - **Most common missing elements** (file paths, error messages, success criteria, etc.)

8. Categorize issues using official prompt engineering problems:
   - **Missing context** (no file paths, no error messages) - % of clarifications
   - **Too vague/broad** (no specific expectations) - % of clarifications
   - **Missing success criteria** (no definition of "done") - % of clarifications
   - **Ambiguous requests** (multiple valid interpretations) - % of clarifications
   - **Missing approach** (multiple implementation methods possible) - % of clarifications

9. **CRITICAL: Generate "Areas for Improvement" Section** - For prompts scoring 0-4/10:
   - List EVERY prompt that scored 3-4/10 or lower
   - For EACH low-scoring prompt, provide:
     - The exact prompt text from logs
     - Score (e.g., 3/10)
     - Problem explanation (what's missing or unclear)
     - Context available at that moment
     - What likely happened (Claude's clarification)
     - Better version of the same prompt with specifics
     - Why the better version works
     - Time saved estimate
   - Calculate total impact of these improvements
   - Identify common patterns across these low-scoring prompts

   **This section is MANDATORY if ANY prompts score 0-4/10**

10. Provide specific recommendations based on **Prompt Engineering Best Practices** above, with focus on:
   - Most impactful improvements (what would reduce clarifications most)
   - Specific templates/patterns for common tasks
   - Real examples from their logs showing before/after

**Example Output:**
```
📝 Prompt Quality Analysis (Last 14 Days)

Total prompts: 145
Context-aware analysis: 145 prompts categorized
Average prompt score: 6.8/10 (Very Good!)

✅ Context-Rich Brief Prompts Identified: 23 (16%)
Examples: "git commit", "run tests", "build", "npm install"
These score 8-10/10 - excellent use of environmental context!

📊 Prompt Category Breakdown:
- Excellent (8-10): 45 prompts (31%) - Context-rich OR detailed
- Good (5-7): 71 prompts (49%) - Adequate information
- Needs Work (0-4): 29 prompts (20%) - Brief AND low context

Clarifications needed: 29 (20%) - Down from typical 35%!

🚩 Most Common Issues (context-poor prompts only):
1. Missing file context: 18 prompts (when no files in scope)
2. Missing error details: 14 prompts (when debugging without error shown)
3. Missing success criteria: 16 prompts (vague goals like "optimize")
4. Missing approach: 12 prompts (when multiple methods possible)

🔴 Real Examples from Your Logs (context-poor prompts):

**Example 1: Missing File Context**
❌ Your prompt: "fix the bug"
🤔 Claude asked: "Which file has the bug? What's the error message or symptom?"
✅ Better prompt: "fix the authentication bug in src/auth/login.ts where JWT validation fails with 401 error"
📉 Cost: +2 minutes, +1 iteration

**Example 2: Vague Action Words**
❌ Your prompt: "optimize the component"
🤔 Claude asked: "Which component? What performance issue? What's the target?"
✅ Better prompt: "optimize UserList component in src/components/UserList.tsx by adding React.memo to reduce unnecessary re-renders when parent updates"
📉 Cost: +3 minutes, +1 iteration

**Example 3: Missing Approach**
❌ Your prompt: "add caching"
🤔 Claude asked: "Where should caching be added? What caching strategy? (Redis, memory, file-based?)"
✅ Better prompt: "add Redis caching to the API responses in src/api/client.ts with 5-minute TTL, similar to how we cache user data"
📉 Cost: +4 minutes, +2 iterations

**Example 4: Missing Error Details**
❌ Your prompt: "it's not working"
🤔 Claude asked: "What's not working? What's the expected behavior vs what's happening?"
✅ Better prompt: "the login form isn't submitting - clicking the submit button does nothing, no network requests in console, expected to see POST to /api/auth/login"
📉 Cost: +2 minutes, +1 iteration

---

## ⚠️ Areas for Improvement (Prompts Scoring 0-4/10)

**CRITICAL: If there are prompts scoring 0-4/10, list EVERY SINGLE ONE with specific examples:**

While most of your prompts are good, here are the **X specific prompts that scored 3-4/10** and need improvement:

### Prompts That Need Work

**Example 1: Too Brief Without Context** (Score: 3/10)
❌ **Your prompt:** "test"
- **Problem:** No context about what to test, which tests to run, or which file
- **Context available:** None - standalone request
- **What happened:** Claude likely had to ask: "Which tests? Unit tests? Integration tests? For which component?"
✅ **Better prompt:** "run the unit tests for the YouTube transcript fetcher in src/index.test.ts"
- **Why better:** Specifies test type, component, and file path
- **Time saved:** ~2 minutes

**Example 2: Vague Action Without Specifics** (Score: 4/10)
❌ **Your prompt:** "update the docs"
- **Problem:** Doesn't specify which documentation or what updates to make
- **Context available:** Multiple doc files exist
- **What happened:** Claude needed clarification on which docs and what information to add
✅ **Better prompt:** "update README.md to include installation instructions and usage examples for the get-transcript tool"
- **Why better:** Specific file, specific sections, clear requirements
- **Time saved:** ~3 minutes

[Continue for ALL prompts scoring 0-4/10...]

### Impact of These Improvements

**Current state:**
- X prompts needed significant clarification
- Average Y minutes lost per unclear prompt
- **Total time lost: ~Z minutes**

**If improved:**
- Direct answers without clarification
- **Potential time savings: ~Z minutes** in this project alone
- **Annualized savings:** ~N hours/year on similar projects

### Common Patterns to Avoid

Based on these X examples, watch out for:

1. **🚩 Standalone brief prompts without context**
   - "test", "fix", "update" → Need specifics

2. **🚩 Vague action verbs without details**
   - "improve", "optimize", "make it work" → Need measurable outcomes

3. **🚩 Missing file paths**
   - "update the docs", "add validation" → Include file names

4. **🚩 Ambiguous pronouns**
   - "it", "this", "that" without clear referent → Name the specific component

5. **🚩 No error context**
   - "fix the error" → Include error message and location

6. **🚩 No success criteria**
   - "improve performance" → Define baseline and target

---

📊 Prompt Quality Score Breakdown:
- Excellent (8-10): 23 prompts (16%) - Clear, specific, actionable
- Good (5-7): 71 prompts (49%) - Minor improvements possible
- Needs Work (3-4): 38 prompts (26%) - Missing key information
- Poor (0-2): 13 prompts (9%) - Requires significant clarification

📉 Impact Analysis:
- 29 prompts needed clarification (down from typical 35%!)
- Average time lost per clarification: 2.8 minutes
- Total time lost to context-poor prompts: ~1.4 hours
- **Potential time savings: ~45 minutes by improving remaining context-poor prompts**

🌟 What You're Doing Right (Keep It Up!):

✅ **Context-Rich Brief Prompts: 23 prompts (16%)**
   Examples from your logs:
   - "git commit" → Claude used git diff to create perfect commit message
   - "run tests" → Claude knew your test framework from package.json
   - "build" → Clear action with obvious build process
   - "npm install" → Standard command, no ambiguity

   💰 Time saved: ~1.5 hours by NOT over-explaining when context is clear!

✅ **Valid Responses: 6 prompts**
   - Answered Claude's questions concisely ("yes", "1", "2")
   - Perfect communication efficiency

✅ **Detailed Prompts: 42 prompts (29%)**
   - Clear file paths, error messages, and success criteria
   - These work great even without environmental context

**Keep using this efficient approach!** You're already saving time by trusting Claude to use available context.

🎯 Your Top 3 Improvements (Maximum Impact):

💡 Note: You're already using context well with git commands and build tools!

**1. Include File Paths When No Files in Scope (18 clarifications)**

   When to add file paths: When you're not already working with the file
   When NOT needed: After reading/editing a file, or when only one file is relevant

   Template: "[action] in [file path] [details]"

   Examples:
   - ❌ "fix the bug" (no file in context)
   - ✅ "fix the validation error in src/utils/validator.ts where email regex fails"
   - ✅ "update the Button component in src/components/Button.tsx to match design system"

   💰 Impact: Would eliminate ~18 clarifications (~50 min saved)

**2. Provide Error Details When Debugging (23% of clarifications)**

   Template: "fix [error message] in [file] - expected [X], getting [Y]"

   Examples:
   - "fix 'Cannot read property of undefined' error in src/hooks/useAuth.ts line 42 - expected user object, getting undefined"
   - "fix TypeScript error TS2322 in src/types/User.ts - type mismatch on email field"

   💰 Impact: Would eliminate ~12 clarifications (~25 min saved)

**3. Define Success Criteria for Vague Actions (30% of clarifications)**

   Instead of: "optimize", "improve", "make better", "clean up"
   Use: "[action] to achieve [specific measurable outcome]"

   Examples:
   - "optimize database queries in src/db/users.ts to reduce response time from 800ms to <200ms"
   - "refactor UserList component to use virtual scrolling and handle 10,000+ items smoothly"

   💰 Impact: Would eliminate ~15 clarifications (~40 min saved)

💡 Quick Win: Apply these templates to your next 10 prompts and watch your clarification rate drop!

💪 You're doing well! Your prompts are 65% effective. Focus on these 3 improvements and you'll hit 85%+ effectiveness, saving ~1-2 hours per week.
```

### 3. Tool Usage Patterns

**When asked about tools, workflows, or how they code:**

**Steps:**
1. Read recent session files

2. Extract all tool_use blocks from assistant messages

3. Count usage by tool name

4. **Group tools into categories:**
   - **Built-in Claude Code tools**: Read, Write, Edit, Bash, Grep, Glob, Task, TodoWrite, WebFetch, WebSearch, NotebookEdit, SlashCommand
   - **MCP/3rd party tools**: Any tool starting with `mcp__` or custom tools
   - Parse MCP tool names to extract server name (e.g., `mcp__playwright__navigate` → playwright server)

5. Identify patterns:
   - Total built-in tool usage (one summary line)
   - Individual MCP tool usage (detailed breakdown)
   - MCP server adoption (which servers are being used)
   - Common workflows with MCP tools
   - Tool success/failure rates

6. Provide recommendations focused on MCP tool adoption and usage

**Example Output:**
```
🛠️ Tool Usage Patterns (Last 30 Days)

Built-in Claude Code Tools:
└─ Total: 955 uses (Read: 450, Edit: 220, Bash: 150, Write: 89, Grep: 34, Glob: 12)

🌟 MCP & 3rd Party Tools:
1. playwright (server)          ████████████████████ 287 uses
   ├─ navigate                   98 uses
   ├─ screenshot                 76 uses
   ├─ click                      54 uses
   ├─ fill                       32 uses
   └─ evaluate                   27 uses

2. browserbase (server)         ████████████         156 uses
   ├─ stagehand_navigate         45 uses
   ├─ stagehand_act              52 uses
   ├─ stagehand_extract          39 uses
   └─ screenshot                 20 uses

3. youtube-transcript (server)  ████                  34 uses
   └─ get-transcript             34 uses

4. pdf-reader (server)          ██                    18 uses
   ├─ read-pdf                   12 uses
   └─ search-pdf                  6 uses

💡 Insights:

🌟 Great MCP adoption! You're using 4 different MCP servers
   → 495 MCP tool calls vs 955 built-in tools
   → MCP tools account for 34% of your tool usage

✅ Playwright is your most-used MCP server
   → Heavily used for browser automation
   → Good mix of navigation, interaction, and screenshots

🚀 Browserbase + Stagehand pattern detected
   → You're leveraging AI-powered browser control
   → 156 uses show strong automation workflow

💡 Opportunity: Consider these MCP servers you haven't tried:
   → @modelcontextprotocol/server-filesystem for advanced file ops
   → @modelcontextprotocol/server-sqlite for database work
   → @modelcontextprotocol/server-github for PR/issue management

📊 Common MCP workflows:
1. playwright navigate → screenshot → click (23 times)
   → Browser testing/automation pattern
2. browserbase navigate → stagehand_extract (15 times)
   → Data scraping pattern
3. youtube-transcript get-transcript → Edit (12 times)
   → Video content analysis workflow
```

### 4. Session Efficiency Analysis

**When asked about productivity, efficiency, or iterations:**

**Steps:**
1. Read recent session files

2. For each session (group by sessionId):
   - Count total messages
   - Count user messages (iterations)
   - Measure duration (first to last timestamp)
   - Check for "completion signals":
     - Bash commands with `git commit`
     - Successful builds (`npm run build`, `cargo build`)
     - Test runs (`npm test`, `pytest`)

3. Calculate metrics:
   - Average iterations per session
   - Average session duration
   - Task completion rate
   - Time to first action (user prompt → first tool use)

**Example Output:**
```
⚡ Session Efficiency Analysis

Sessions analyzed: 45

Average iterations per task: 3.5
Median iterations: 2
Session duration (avg): 18 minutes

Completion patterns:
- Quick wins (<5 min): 23 sessions (51%)
- Standard tasks (5-30 min): 15 sessions (33%)
- Deep work (>30 min): 7 sessions (16%)

💡 Insights:

✅ You're efficient! 51% of tasks complete in <5 minutes

📊 Iteration breakdown:
- 1 iteration: 12 sessions - Clear requirements
- 2-3 iterations: 20 sessions - Normal back-and-forth
- 4+ iterations: 13 sessions - Unclear requirements or complex tasks

🎯 Tip: Sessions with 4+ iterations often started with vague prompts.
Being more specific upfront could save ~8 min/task.
```

### 5. Productivity Time Patterns

**When asked about productive hours, when they work best:**

**Steps:**
1. Read session files from last 30 days

2. Extract all timestamps and parse them

3. Group sessions by:
   - Hour of day (0-23)
   - Day of week (Mon-Sun)
   - Weekend vs weekday

4. For each time bucket, calculate:
   - Number of sessions
   - Average iterations
   - Average session duration
   - Efficiency score (tasks completed / iterations)

**Example Output:**
```
🕐 Productivity Time Patterns (Last 30 Days)

Peak productivity hours:
1. 14:00-17:00 ████████████ (32 sessions, 2.1 avg iterations)
2. 09:00-12:00 ████████     (24 sessions, 2.8 avg iterations)
3. 20:00-23:00 ████         (15 sessions, 4.2 avg iterations)

Most efficient: 14:00-17:00 (afternoon)
- 40% fewer iterations than average
- 25% faster completion time
- Higher task completion rate

Least efficient: 20:00-23:00 (evening)
- 50% more iterations needed
- More clarification requests
- More Bash command failures

Day of week patterns:
Tuesday:  ████████ Most productive
Wednesday: ███████
Thursday:  ██████
Monday:    ████ Slower start
Friday:    ███ Winding down

💡 Recommendation: Schedule complex tasks between 2-5pm on Tue-Thu
```

### 6. File Modification Heatmap

**When asked about what files they work on, code hotspots:**

**Steps:**
1. Read recent session files

2. Extract all tool_use blocks with names: Edit, Write

3. Parse the file_path from each tool's input

4. Count modifications per file

5. Group by directory to find hotspots

**Example Output:**
```
🔥 File Modification Heatmap (Last 30 Days)

Most edited files:
1. src/components/Button.tsx        ████████████ 47 edits
2. src/utils/api.ts                 ████████     32 edits
3. src/hooks/useAuth.ts             ██████       23 edits
4. tests/components/Button.test.tsx █████        19 edits
5. src/types/index.ts               ████         16 edits

Hotspot directories:
1. src/components/  ██████████████████ 89 edits
2. src/utils/       ████████           45 edits
3. tests/           ██████             34 edits

💡 Insights:

🔥 Button.tsx is your hottest file (47 edits)
   → Consider if this component needs refactoring
   → High edit frequency can indicate code smell

✅ Good test coverage signal:
   → 19 edits to Button.test.tsx
   → You're maintaining tests alongside code

📊 Component-heavy development:
   → 62% of edits in src/components/
   → UI-focused work this month
```

### 7. Error & Recovery Analysis

**When asked about errors, problems, or troubleshooting:**

**Steps:**
1. Read recent session files

2. Look for error indicators in Bash tool results:
   - Non-zero exit codes
   - Common error patterns (npm ERR!, error:, failed, etc.)

3. Measure recovery patterns:
   - Time between error and fix
   - Number of attempts
   - Common error types

**Example Output:**
```
🐛 Error & Recovery Analysis

Errors encountered: 23

Common errors:
1. npm install failures    ████████ 8 occurrences
   → Avg recovery time: 4.5 min
   → Common cause: Node version mismatch

2. TypeScript compile errors ██████ 6 occurrences
   → Avg recovery time: 8 min
   → Common cause: Type mismatches

3. Test failures           ████ 4 occurrences
   → Avg recovery time: 12 min

💡 Recommendations:

1. npm install issues:
   → Add .nvmrc file to project
   → Use `nvm use` before installing
   → Saves ~4 min per occurrence

2. TypeScript errors:
   → Run `tsc --watch` during development
   → Catch errors before committing
```

### 8. Project Switching Analysis

**When asked about context switching, focus time:**

**Steps:**
1. Read session files from multiple project directories

2. Track when `cwd` (current working directory) changes between sessions

3. Calculate:
   - Number of project switches per day
   - Time spent per project
   - Overhead of switching (idle time between projects)

**Example Output:**
```
🔄 Project Switching Analysis (Last 7 Days)

Active projects: 5
Total switches: 23
Avg switches per day: 3.3

Time distribution:
1. ~/code/main-app        ████████████ 12 hours (55%)
2. ~/code/side-project    ████         4 hours (18%)
3. ~/code/dotfiles        ███          3 hours (14%)
4. ~/code/experiments     ██           2 hours (9%)
5. ~/code/scripts         █            1 hour (4%)

Context switching cost:
- Avg overhead per switch: 12 minutes
- Total overhead this week: 4.6 hours
- Estimated productivity loss: 20%

💡 Recommendation:
You switched projects 23 times in 7 days. Consider:
- Time-blocking: Dedicate specific days to specific projects
- Batch similar tasks: Do all dotfile updates in one session
- Your focus time is best on main-app (fewer interruptions)
```

## General Guidelines

### When Analyzing Logs:

1. **Sample Intelligently**
   - For recent data: Read last 5-10 .jsonl files
   - For historical: Use Bash to find files by date, sample evenly
   - Very large files (>10MB): Read first/last N lines

2. **Parse JSON Carefully**
   - Each line is separate JSON
   - Handle malformed lines gracefully
   - Watch for truncated last lines

3. **Respect Privacy**
   - These are personal coding sessions
   - Don't repeat user's code or prompts verbatim unless illustrative
   - Focus on patterns, not specifics

4. **Provide Actionable Insights**
   - Always include "💡 Tips" or "Recommendations"
   - Compare to benchmarks when possible
   - Suggest specific improvements

5. **Use Visualizations**
   - ASCII charts for distributions
   - Emoji indicators for priority/severity
   - Tables for comparisons

### Finding Specific Information:

**To find all sessions from a specific project:**
```bash
ls -la ~/.claude/projects/-Users-username-code-projectname/
```

**To find sessions from a date range:**
```bash
find ~/.claude/projects -name "*.jsonl" -newermt "2025-01-01" -ls
```

**To quickly check total log size:**
```bash
du -sh ~/.claude/projects
```

**To count total sessions:**
```bash
find ~/.claude/projects -name "*.jsonl" | wc -l
```

## Example Queries You Can Answer

### 🌟 General Analysis (Comprehensive Report - NEW!)
- **"Give me a general analysis of my Claude Code usage"** ← Recommended!
- **"Analyze my overall Claude Code usage"** ← Recommended!
- "Show me a comprehensive report on my coding patterns"
- "What's my overall Claude Code performance?"
- "How am I doing with Claude Code?"
- "Generate a full report on everything"
- "Analyze all my metrics"

### Specific Analysis (Individual Metrics)
- "How much have I spent on Claude Code this month?"
- "Am I writing good prompts?"
- "What tools do I use most?"
- "When am I most productive?"
- "Which files do I edit most often?"
- "How efficient are my sessions?"
- "Show me my coding patterns"
- "What did I work on last week?"
- "How much time do I spend context switching?"
- "What errors do I encounter most?"

### Project Discovery
- "List all projects with Claude Code logs"
- "Show me which projects I've worked on"
- "What projects do I have session logs for?"
- "Which project have I spent the most time on this week?"

### Project-Specific Analysis
- "Analyze my prompt quality for the project under ~/code/youtube/transcript/mcp"
- "Show me token usage for the project in ~/code/my-app"
- "What tools do I use most in the ~/code/experiments project?"
- "How efficient are my sessions for /Users/username/code/my-project?"
- "Which files do I edit most in the ~/code/dotfiles project?"
- "Analyze my prompt quality for ~/code/my-app and save it as reports/prompt-analysis.md"

## Important Notes

- Always use existing tools (Read, Bash, Grep) - you have file access
- Parse JSON yourself - you can do this natively
- Show specific examples from actual logs when helpful
- Give actionable, personalized recommendations
- Be encouraging but honest about areas for improvement
- Calculate costs accurately with current pricing
- **CRITICAL (v1.8.0+):** Always deduplicate token usage entries using `message.id + requestId` hash to match actual billing. Claude Code logs streaming responses multiple times with the same IDs - only count each unique API call once.
- **CRITICAL (v1.10.0+):** Always use model-specific pricing. Extract model from `message.model` field and apply correct rates. Opus is 5x more expensive than Sonnet!
- **NEW (v1.10.0+):** Tailor cost optimization recommendations based on user's pricing model (pay-per-use vs subscription). Cache optimization is valuable for BOTH but for different reasons.
- **NEW (v1.9.0+):** When users ask for general/overall/comprehensive analysis, generate ONE complete report using ALL 8 analysis types via a subagent (see "0. General Analysis Mode" section)
