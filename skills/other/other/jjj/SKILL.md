---
name: jjj
description: Smart multi-agent task execution with automatic routing. Use when user types 'jjj' or for routine coding tasks (tests, comments, refactoring). Saves 80%+ cost with intelligent agent selection.
model: haiku
---

# JJJ - Junior Developer CLI Wrapper

## Purpose
Smart multi-agent task execution with automatic routing and cost optimization. Routes tasks to appropriate agents (Junior/Claude) based on complexity.

## When to Use
- User explicitly types `jjj`
- Writing unit tests
- Adding comments/docstrings
- Simple refactoring
- Generating boilerplate code
- Any routine coding task

## Cost Comparison
```
Claude-Only Workflow:
  - Every task: $0.075
  - 10 tasks: $0.75

Multi-Agent Workflow:
  - Simple (40%): $0.0021 per task
  - Moderate (30%): $0.0231 per task
  - Complex (30%): $0.0231 per task
  - 10 tasks: $0.147
  - SAVINGS: 80%+ 🎉
```

## Three Execution Modes

### Mode 1: Smart Mode (Default) - Automatic Routing

**Best for**: Most use cases, maximum cost optimization

**Usage:**
```bash
./scripts/jjj.sh
```

**Interactive prompts:**
1. Task description?
2. File path? (optional)
3. Include file content? (y/n)

**System automatically:**
- Analyzes complexity
- Routes to Junior/Junior+Review/Claude
- Shows agent status in real-time
- Displays cost savings

**Agent Status Display:**
```
🔍 Analyzing task complexity...
✅ Complexity: simple

🤖 Routing Decision:
   Agent: Junior Developer
   Model: Gemini Flash
   Estimated Cost: $0.0021

⚙️  Junior Developer [ACTIVE]
   Status: Generating code...

✅ Task completed!
   Generated: 245 lines
   Savings: $0.0525 (96.2%)
```

### Mode 2: Manual Mode - Force Junior Developer

**Best for**: Testing, specific scenarios, full control

**Usage:**
```bash
./scripts/jjj.sh --manual
```

**Full control:**
- Select task type (test/comment/refactor/boilerplate/general)
- Choose model (auto/flash/local)
- Provide context code
- Junior executes directly (no routing)

### Mode 3: Quick Mode - One-liner

**Best for**: Fast, one-off tasks

**Usage:**
```bash
./scripts/jjj.sh "Add docstring" utils.py
./scripts/jjj.sh "Write tests" auth.ts
./scripts/jjj.sh "Refactor function" --mode local
```

## Steps

### 1. Check Prerequisites

```bash
# Check script exists
test -f scripts/jjj.sh && echo "✅ Found" || echo "❌ Missing: scripts/jjj.sh"

# Check dependencies
which jq > /dev/null && echo "✅ jq installed" || echo "❌ Need: brew install jq"

# Check Python modules
python -c "import agent_coordinator" 2>/dev/null && echo "✅ Python ready" || echo "❌ Missing Python modules"
```

### 2. Determine Mode

**Ask user:**
```
Which mode would you like to use?

1. Smart Mode (recommended) - Automatic routing
2. Manual Mode - Direct Junior Developer
3. Quick Mode - One-liner

Or just tell me the task and I'll use Smart Mode.
```

### 3. Execute Based on Mode

**Smart Mode:**
```bash
./scripts/jjj.sh

# Then provide when prompted:
# - Task description
# - File path (if applicable)
# - Whether to include file content
```

**Manual Mode:**
```bash
./scripts/jjj.sh --manual

# Then follow prompts:
# - Select task type
# - Choose model
# - Provide context
```

**Quick Mode:**
```bash
./scripts/jjj.sh "[task]" [file] [--mode MODE]
```

### 4. Monitor Execution

The script will show:
- 🔍 Analyzing task complexity...
- 🤖 Routing decision (agent/model/cost)
- ⚙️ Agent status (active/generating)
- ✅ Completion (result/savings)

### 5. Review Output

**Junior Developer output includes:**
- Generated code
- Quality score (if reviewed)
- Cost comparison
- Savings percentage

**Present to user:**
```
✅ Task Complete!

**Agent Used**: Junior Developer (Gemini Flash)
**Generated**: [lines] lines of code
**Cost**: $0.0021
**Savings**: $0.0525 (96.2%) vs Claude-only

**Output:**
[Show generated code]

**Quality**: 8/10 (Claude reviewed)

Ready to apply this code?
```

### 6. Apply or Iterate

**If quality good (score ≥ 8):**
- Apply the code directly
- Commit with appropriate message

**If quality needs improvement:**
- Ask user if they want to iterate
- Re-run with different parameters
- Or escalate to Claude for complex handling

## Options & Flags

### CLI Options
```bash
--manual          # Force Manual Mode (Junior only)
--mode MODE       # LLM mode: auto/flash/local
--type TYPE       # Task type: test/comment/refactor/boilerplate/general
--help            # Show detailed help
```

### Task Types
- `test`: Writing unit tests
- `comment`: Adding comments/docstrings
- `refactor`: Simple refactoring
- `boilerplate`: Generating boilerplate code
- `general`: General coding task

### LLM Modes
- `auto`: Try Gemini Flash → fallback to Local LLM
- `flash`: Force Gemini Flash (best quality)
- `local`: Force Local LLM (offline/privacy)

## Environment Variables

```bash
# Gemini Flash API for Junior Developer
export GEMINI_API_KEY="your-key-here"

# Local LLM (optional, fallback)
export LOCAL_LLM_URL="http://192.168.1.202:8088/v1/chat/completions"
```

## Important Notes

### When to Use Smart Mode
- Maximum cost optimization (80%+)
- Automatic complexity analysis
- Real-time agent status
- Best user experience

### When to Use Manual Mode
- Testing Junior Developer
- Specific task types
- Override routing decision
- Learning/experimentation

### When to Use Quick Mode
- Fast, one-off tasks
- Scripting/automation
- When you know exactly what you want

### Offline Mode
Works offline with Local LLM:
```bash
./scripts/jjj.sh --mode local
```

## Error Handling

**"jjj.sh not found":**
```bash
# Check if script exists
ls -la scripts/jjj.sh

# If missing:
"❌ Junior Developer script not found at scripts/jjj.sh"
```

**"jq not installed":**
```bash
# Install jq
brew install jq  # macOS
sudo apt install jq  # Linux

# Or inform user:
"❌ jq required. Install: brew install jq"
```

**"Python modules missing":**
```bash
# Check what's missing
python -c "import agent_coordinator; import task_router; import junior_developer"

# Inform user which modules are missing
```

**"Agent routing failed":**
```bash
# Fall back to Claude
"⚠️ Routing failed. Using Claude for this task."
```

## Success Criteria
- ✅ Script executed successfully
- ✅ Agent selected appropriately
- ✅ Code generated with quality score
- ✅ Cost savings calculated and shown
- ✅ User provided with clear output
- ✅ Ready to apply or iterate

## Performance Tips
- Use Smart Mode for best results (80%+ savings)
- Manual Mode useful for testing specific scenarios
- Quick Mode for automation and scripting
- Review Junior output before applying
- Iterate if quality score < 8
- See `scripts/README.md` for detailed docs

## Related Skills
- `ggg` - Use Gatekeeper before jjj for large files
- `nnn` - Plan complex tasks before using jjj
- `gogogo` - Execute plans, using jjj for simple sub-tasks
