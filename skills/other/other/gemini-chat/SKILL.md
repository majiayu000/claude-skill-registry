---
name: gemini-chat
description: Interactive chat workflows with Gemini CLI including context management, multimodal conversations, and session persistence. Use for extended AI conversations, brainstorming, or collaborative problem-solving.
---

# Gemini Interactive Chat

Advanced interactive chat workflows with Gemini CLI, featuring context management, multimodal support, and session persistence.

## Quick Start

```bash
# Start interactive chat
gemini -i "Let's work on my project"

# Start with specific context
gemini --include-directories ./src -i "Help me refactor this code"

# Start with checkpointing and YOLO mode (toggle in session)
gemini --checkpointing -i "Complex multi-step task"
```

## YOLO Mode in Interactive Sessions

**YOLO mode** can be toggled during interactive sessions for automated execution:

```bash
# In interactive mode:
# Ctrl+Y              # Toggle YOLO mode on/off
# /yolo on            # Enable auto-approval
# /yolo off           # Disable auto-approval

# Start with YOLO already enabled (for automation)
gemini --yolo -i "Set up complete development environment automatically"

# Mixed mode workflow
gemini -i "Let's plan first, then execute with YOLO"
# Plan manually, then: Ctrl+Y to enable YOLO for execution
```

**When to use YOLO in chat:**
- ✅ File operations (create, edit, organize)
- ✅ Batch processing tasks
- ✅ Project setup and configuration
- ✅ Documentation generation
- ❌ Complex system changes (review first)
- ❌ Unknown/experimental commands

## Interactive Commands

### Essential Commands

```bash
/help              # Show all available commands
/tools             # List available tools
/mcp               # Show MCP server status
/compress          # Compress conversation context
/copy              # Copy last response
/clear             # Clear screen and context
/checkpoint        # Save current state
/restore           # Restore previous state
/exit              # End session
```

### Context Management

```bash
# In chat, reference files
@./src/main.js     # Include file in context
@./docs/           # Include entire directory
@https://example.com  # Include web page

# Include images
@./diagram.png     # Add image to conversation
Ctrl+V             # Paste image from clipboard

# Context commands
/compress          # Summarize long conversation
/clear context     # Clear context, keep chat
/show context      # Display current context
```

## Chat Workflows

### Code Review Session

```bash
#!/bin/bash
# Interactive code review

start_code_review() {
  local project_dir="${1:-.}"
  
  gemini \
    --include-directories "$project_dir/src" \
    --exclude-directories node_modules,.git \
    --checkpointing \
    -i "Let's do a code review. Start by giving me an overview of the codebase structure."
}

# Usage
start_code_review ./my-project
```

### Brainstorming Session

```bash
#!/bin/bash
# Creative brainstorming with saves

brainstorm_session() {
  local topic="$1"
  local session_name="brainstorm-$(date +%Y%m%d-%H%M%S)"
  
  # Create session directory
  mkdir -p ~/.gemini/sessions/$session_name
  
  # Start session with logging
  gemini \
    --checkpointing \
    --log ~/.gemini/sessions/$session_name/chat.log \
    -i "Let's brainstorm about: $topic
    
Please help me:
    1. Generate creative ideas
    2. Evaluate feasibility
    3. Identify challenges
    4. Suggest next steps"
  
  # Save final summary with YOLO
  gemini --yolo -p "Summarize our brainstorming session and create actionable next steps" \
    > ~/.gemini/sessions/$session_name/summary.md
  
  echo "Session saved to ~/.gemini/sessions/$session_name/"
}

# Automated brainstorming with YOLO
automated_brainstorm() {
  local topic="$1"
  local session_name="auto-brainstorm-$(date +%Y%m%d-%H%M%S)"
  
  mkdir -p ~/.gemini/sessions/$session_name
  
  # Fully automated brainstorming session
  gemini --yolo --checkpointing \
    -i "Automated brainstorming session for: $topic

Execute this workflow automatically:
1. Generate 10 creative ideas
2. Evaluate each for feasibility (1-10 scale)
3. Identify top 3 ideas with rationale
4. Create implementation roadmap for top idea
5. List potential challenges and solutions
6. Generate final summary document

Save all outputs to organized files."
}
```

### Learning Session

```bash
#!/bin/bash
# Interactive learning with examples

learn_with_gemini() {
  local subject="$1"
  
  gemini \
    --yolo \
    -i "I want to learn about $subject.
    
    Please:
    1. Start with fundamentals
    2. Provide examples
    3. Create exercises
    4. Check my understanding
    5. Suggest resources
    
    Let's begin!"
}
```

## Advanced Features

### Session Management

```bash
#!/bin/bash
# Save and resume sessions

# Save session
save_session() {
  local name="${1:-session}"
  gemini checkpoint save "$name"
  echo "Session saved as: $name"
}

# List sessions
list_sessions() {
  gemini checkpoint list
}

# Resume session
resume_session() {
  local name="$1"
  gemini checkpoint restore "$name"
  gemini -i "Let's continue where we left off"
}

# Delete old sessions
cleanup_sessions() {
  local days_old="${1:-7}"
  find ~/.gemini/checkpoints -mtime +$days_old -delete
  echo "Cleaned up sessions older than $days_old days"
}
```

### Multi-Modal Conversations

```bash
#!/bin/bash
# Work with images and text

analyze_designs() {
  local design_dir="$1"
  
  gemini -i "Let's review UI designs"
  
  # In the chat:
  # @./designs/homepage.png
  # @./designs/dashboard.png
  # "Compare these designs and suggest improvements"
}

# Screenshot analysis
analyze_screenshot() {
  # Take screenshot (macOS)
  screencapture -i /tmp/screenshot.png
  
  # Or Linux
  # import /tmp/screenshot.png
  
  gemini -p "Analyze this screenshot: @/tmp/screenshot.png"
}
```

### Context Optimization

```bash
#!/bin/bash
# Manage context efficiently

optimized_chat() {
  local max_context="${1:-50000}"  # tokens
  
  # Monitor context size
  while true; do
    context_size=$(gemini context size)
    
    if [ $context_size -gt $max_context ]; then
      echo "Context limit approaching. Compressing..."
      gemini /compress
    fi
    
    # Continue chat
    gemini -i "Continue"
  done
}

# Selective context
focused_chat() {
  local focus_dir="$1"
  local task="$2"
  
  # Start with minimal context
  gemini \
    --include-directories "$focus_dir" \
    --max-depth 1 \
    -i "Focus only on: $task"
}
```

## Prompt Engineering

### Structured Prompts

```bash
# Engineering prompt
gemini -i "You are a senior software engineer.

Context:
- Language: Python
- Framework: FastAPI
- Database: PostgreSQL

Task: Help me design a scalable API

Constraints:
- Must handle 10k requests/second
- Must have <100ms response time
- Must be maintainable

Let's start with the architecture."
```

### Role-Based Sessions

```bash
#!/bin/bash
# Different personas for different tasks

start_role_session() {
  local role="$1"
  
  case $role in
    architect)
      PROMPT="You are a solutions architect. Focus on system design, scalability, and best practices."
      ;;
    reviewer)
      PROMPT="You are a code reviewer. Focus on bugs, security issues, and code quality."
      ;;
    teacher)
      PROMPT="You are a patient teacher. Explain concepts simply with examples."
      ;;
    debugger)
      PROMPT="You are a debugging expert. Focus on finding and fixing issues systematically."
      ;;
    *)
      PROMPT="You are a helpful AI assistant."
      ;;
  esac
  
  gemini -i "$PROMPT
  
  How can I help you today?"
}
```

## Automation Scripts

### Daily Standup

```bash
#!/bin/bash
# Automated daily standup

daily_standup() {
  local git_log=$(git log --oneline -5)
  local todos=$(cat TODO.md 2>/dev/null || echo "No TODO file")
  
  gemini -p "Based on recent commits and TODOs, generate a standup update:
  
  Recent commits:
  $git_log
  
  TODOs:
  $todos
  
  Format:
  - What I did yesterday
  - What I'm doing today
  - Any blockers"
}
```

### Continuous Learning

```bash
#!/bin/bash
# Learn from codebase changes

learn_from_changes() {
  local since="${1:-1 week ago}"
  
  # Get changes
  local changes=$(git diff --stat "@{$since}")
  local new_files=$(git ls-files --others --exclude-standard)
  
  gemini --yolo -i "Analyze these recent changes and teach me:
  
  Changes since $since:
  $changes
  
  New files:
  $new_files
  
  Please:
  1. Explain what was changed and why
  2. Identify patterns and best practices
  3. Suggest improvements
  4. Generate documentation for changes
  5. Create knowledge summary document
  6. Quiz me on the concepts"
}

# Automated development workflow session
auto_dev_workflow() {
  local task="$1"
  
  gemini --yolo --checkpointing -i "Automated development workflow: $task

Execute this complete development cycle:
1. Analyze current codebase and requirements
2. Create detailed implementation plan
3. Generate all necessary code files
4. Write comprehensive tests
5. Create documentation
6. Set up CI/CD integration
7. Generate deployment scripts
8. Create progress report

Work autonomously and save all outputs."
}
```

## Integration Patterns

### Vim Integration

```vim
" .vimrc
" Send selection to Gemini
vnoremap <leader>g :w !gemini -p "Explain this code: $(cat)"<CR>

" Get suggestions
nnoremap <leader>G :r !gemini -p "Improve this function: $(cat %:p)"<CR>

" Interactive help
nnoremap <leader>? :terminal gemini -i "Help with vim and %:t"<CR>
```

### VS Code Integration

```bash
# Connect Gemini to VS Code
gemini /ide install
gemini /ide enable

# Now Gemini can see your VS Code context
gemini -i "Help me with the file I have open in VS Code"
```

### Tmux Workflow

```bash
#!/bin/bash
# Split-screen coding with Gemini

gemini_tmux() {
  tmux new-session -d -s gemini-coding
  
  # Main coding pane
  tmux send-keys -t gemini-coding "vim" C-m
  
  # Gemini chat pane
  tmux split-window -h -t gemini-coding
  tmux send-keys -t gemini-coding "gemini -i 'Help me code'" C-m
  
  # File tree pane
  tmux split-window -v -t gemini-coding
  tmux send-keys -t gemini-coding "watch -n 2 'tree -L 2'" C-m
  
  # Attach to session
  tmux attach -t gemini-coding
}
```

## Best Practices

### Effective Prompting

1. **Be Specific**
   ```bash
   # Bad
   "Help me with code"
   
   # Good
   "Help me refactor this authentication module to use JWT tokens"
   ```

2. **Provide Context**
   ```bash
   # Include relevant files
   gemini --include-directories ./src/auth,./tests/auth
   ```

3. **Set Constraints**
   ```bash
   "Explain in simple terms, with examples, max 100 lines"
   ```

### Session Hygiene

1. **Regular Compression**
   ```bash
   # Compress every 30 minutes
   /compress
   ```

2. **Save Important Sessions**
   ```bash
   /checkpoint
   ```

3. **Clear Irrelevant Context**
   ```bash
   /clear context
   ```

## Troubleshooting

### Common Issues

1. **Slow Responses**
   - Compress context: `/compress`
   - Use faster model: `gemini -m gemini-2.5-flash`
   - Reduce included directories

2. **Lost Context**
   - Check checkpoints: `/restore`
   - Review history: `~/.gemini/history`

3. **Tool Errors**
   - Check available tools: `/tools`
   - Verify permissions: `ls -la`

## Related Skills

- `gemini-cli`: Main Gemini CLI integration
- `gemini-auth`: Authentication management
- `gemini-tools`: Tool execution workflows
- `gemini-mcp`: MCP server management