---
name: xray
description: Understand what just happened under the hood - learn AI by seeing it in action
---

# /xray - The AI Education Experience

**Default behavior:** Explain what just happened in THIS conversation — the specific tools, files, and context that were used, with educational explanations of WHY.

**With qualifiers:** Deep dive into specific topics (AI fundamentals, Dex architecture, how to extend).

---

## Philosophy

The best way to learn is by examining what just happened, not abstract concepts. When you run `/xray`:

1. **Show the work** - What tools ran, what files were read/written
2. **Explain why** - Why each action was necessary
3. **Connect to concepts** - Link specific actions to how AI/Dex works
4. **Empower extension** - "You could customize this by..."

**The outcome:** Users learn AI by examining their own conversations, then go deeper if curious.

**Tone:** Like a senior engineer doing a code review of what just happened. "Here's what I did and why."

---

## Step 1: Determine Mode

### Default (no arguments): "This Conversation"

When user just says `/xray` with no qualifier:
→ **Immediately explain what happened in this conversation**
→ Don't show a menu, just show the work

### With qualifiers: Specific topics

| Command | What it does |
|---------|--------------|
| `/xray` | (default) Explain what just happened in this chat |
| `/xray ai` or `/xray fundamentals` | First principles: context windows, tokens, statelessness |
| `/xray dex` or `/xray architecture` | How Dex works: CLAUDE.md, hooks, MCPs, skills |
| `/xray boot` or `/xray session start` | The session startup sequence |
| `/xray today` | ScreenPipe analysis of your day |
| `/xray extend` or `/xray customize` | How to customize and build on Dex yourself |

---

## DEFAULT MODE: This Conversation (Show Your Work)

**This is the primary mode.** When user runs `/xray`, explain what happened.

### Step 1: Analyze the conversation

Look at the current conversation and identify:
1. What files were read
2. What files were written/modified
3. What tools/MCPs were used
4. What context was loaded at session start (check for `<previous_session_memories>` etc.)
5. Key decision points in the AI's reasoning

### Step 2: Present as educational walkthrough

Output format:

```markdown
## 🔬 X-Ray: What Just Happened

Let me explain what happened under the hood in our conversation.

---

### 📖 The Story of This Chat

Here's what I did, step by step:

**1. Session Started**
Before you typed anything, the system loaded:
- `CLAUDE.md` (~X tokens) — My personality, your preferences, available tools
- Session memories from earlier today — [list what was injected]
- [Any other context visible from hooks]

**Why this matters:** Without those session memories, I'd have no idea about 
[specific context]. That came from a **session hook** that runs before you type.

**2. You Asked: "[summarize their first message]"**

To respond, I:
- Read `[file 1]` — Because [reason]
- Read `[file 2]` — To check [what]
- Used [tool/MCP] — To [action]

**Why these files?** Your CLAUDE.md tells me where to look. It says [quote relevant 
instruction]. Without those instructions, I wouldn't know your file structure.

**3. [Continue for each major exchange in the conversation]**

---

### 🔧 Tools Used This Session

| Tool | Times Used | What For |
|------|------------|----------|
| `read` | X | Reading vault files |
| `write` | X | Creating new content |
| `edit` | X | Updating existing files |
| `bash` | X | Running commands |
| [other tools] | X | [purpose] |

**Why tools matter:** Without tools, I can only generate text. Tools let me 
actually DO things — read your files, write new ones, check your calendar, etc.

---

### 💡 Key Insight: The Context Window

Everything I "know" right now is what's in the **context window**:

```
┌─────────────────────────────────────────────────┐
│  What I can see (the context window)            │
├─────────────────────────────────────────────────┤
│ ✓ CLAUDE.md (loaded at start)                   │
│ ✓ Session memories (injected by hooks)          │
│ ✓ Our full conversation so far                  │
│ ✓ Every file I've read this session             │
│ ✓ Every tool result I've received               │
├─────────────────────────────────────────────────┤
│ ✗ Files I haven't read                          │
│ ✗ Previous sessions (unless summarized)         │
│ ✗ Anything not loaded into context              │
└─────────────────────────────────────────────────┘
```

If something isn't in this window, I literally don't know it exists.

---

### 📁 Files Touched This Session

**Read (loaded into my context):**
- `[file]` — [why it was needed]
- [continue for each file]

**Written/Modified:**
- `[file]` — [what was created/changed]
- [continue for each file]

**Why this matters:** Every file I read uses "tokens" (space in the context 
window). I try to read only what's relevant, not everything.

---

### 🎓 Concepts You Just Saw in Action

| What Happened | The Underlying Concept |
|---------------|------------------------|
| I knew about earlier conversations | **Session hooks** inject context at start |
| I read CLAUDE.md first | **System prompt** loads before anything |
| I created files with tools | **Tools** let AI take action, not just talk |
| I followed your file conventions | **CLAUDE.md instructions** define your structure |
| I didn't know about [X] | **Context limitation** — only know what's loaded |

---

### 🔮 What You Could Customize

Based on what just happened:

**1. Add to CLAUDE.md**
If you want me to always [behavior], add it to your `USER_EXTENSIONS` block.

**2. Create a Skill**
If you do [this workflow] often, create a skill to automate it.

**3. Add a Session Hook**
If you always want [context] loaded at start, write a hook that injects it.

---

### 🎓 Want to Go Deeper?

- `/xray ai` — First principles: context windows, tokens, statelessness
- `/xray dex` — Full architecture: CLAUDE.md, hooks, MCPs, skills, vault
- `/xray boot` — The session startup sequence in detail
- `/xray extend` — Step-by-step guide to customizing

Or ask anything: "How do hooks work?", "What's an MCP?", "How can I add my own tools?"
```

---

## MODE: AI Fundamentals (`/xray ai`)

**Purpose:** Teach the core concepts that make everything else make sense.

### Output Format

```markdown
## 🧠 How AI Actually Works

Let me explain the core concepts that underpin everything Dex does.

---

### The Big Truth: AI Has No Memory

**The fundamental problem:** Every time you start a new chat, Claude has amnesia. 
It doesn't remember yesterday's conversation. It doesn't know your name, your 
projects, or what you discussed last week.

This is true for ALL LLM-based AI — ChatGPT, Claude, Gemini, all of them.

**Why?** LLMs are "stateless." They process text in, text out, with no permanent 
storage between sessions. Each conversation starts from zero.

**So how does Dex remember things?** We engineer around the limitation. 
That's what Dex is — clever engineering to give a forgetful AI the *appearance* 
of memory, context, and continuity.

---

### Concept 1: The Context Window

When you chat with an AI, there's an invisible "window" of text the AI can see:

```
┌─────────────────────────────────────────────────┐
│              THE CONTEXT WINDOW                 │
│  (Everything the AI knows about THIS chat)      │
├─────────────────────────────────────────────────┤
│ • System prompt (CLAUDE.md)                     │
│ • Injected context (session memories, etc.)     │
│ • Our conversation so far                       │
│ • Any files I've read                           │
│ • Tool results (MCP responses)                  │
└─────────────────────────────────────────────────┘
          ↓
     AI generates response based on ALL of this
```

**Key insight:** The AI can only work with what's IN the context window. 
If information isn't in there, the AI doesn't know it exists.

**Dex's job:** Get the RIGHT information INTO that window at the RIGHT time.

---

### Concept 2: Tokens (The Currency)

Context windows are measured in "tokens" (roughly 4 characters = 1 token).

- Claude's window: ~200,000 tokens (~150,000 words)
- Your CLAUDE.md: ~4,500 tokens
- A typical person page: ~500 tokens

**Why it matters:** There's a budget. Load too much context and you hit limits 
or slow things down. Load too little and the AI lacks crucial information.

**Dex's approach:** Selective loading. Don't dump everything — load what's 
*relevant* to what you're asking about.

---

### Concept 3: System Prompts (The Personality)

Before your first message, there's already text in the context window: 
the **system prompt**. For Dex, that's `CLAUDE.md`.

```
┌─────────────────────────────────────────────────┐
│ CLAUDE.md (loaded before you type anything)     │
├─────────────────────────────────────────────────┤
│ "You are Dex, a personal knowledge assistant"   │
│ "User's pillars: [your pillars]"                │
│ "When tasks are mentioned, use Work MCP"        │
│ "Person pages are in 05-Areas/People/"          │
│ ... (hundreds more lines of context)            │
└─────────────────────────────────────────────────┘
```

**The power move:** Everything in CLAUDE.md influences EVERY response. 
It's like setting the AI's personality and knowledge before you say hello.

---

### Concept 4: Tools (How AI Does Things)

Claude can't *do* things by default — it can only generate text. But with 
**tools**, it can take actions:

- Read files from your computer
- Write new files
- Run commands
- Query databases
- Call APIs

In Dex, tools come from **MCP servers** (Model Context Protocol). Each MCP 
gives Claude new capabilities.

**Without tools:** Claude can only talk.
**With tools:** Claude can take action on your behalf.

---

### Concept 5: The Conversation Loop

Here's what happens every time you send a message:

```
1. Your message gets added to context window
                    ↓
2. Claude sees: system prompt + history + your message
                    ↓
3. Claude decides: should I use a tool?
   - If yes → Tool runs → Result added to context → Back to step 3
   - If no → Generate response
                    ↓
4. Response appears (and gets added to context for next turn)
                    ↓
5. Wait for your next message → Repeat from step 1
```

**Key insight:** Each turn, Claude sees MORE context (the history grows). 
Long conversations = more context = closer to limits.

---

### So What?

Understanding these fundamentals helps you:

1. **Know why Dex loads things at session start** — to get context into the window
2. **Understand why some info is "missing"** — it wasn't loaded into context
3. **See opportunities to extend** — what else could be loaded? what tools could help?

---

**Want to see Dex's specific architecture?** Try `/xray dex`
```

---

## MODE: Dex Architecture (`/xray dex`)

**Purpose:** Explain the specific building blocks that make Dex work.

### Output Format

```markdown
## 🏗️ How Dex Works: The Architecture

Now that you understand AI fundamentals, here's how Dex engineers around 
the limitations to create something useful.

---

### The Core Insight

**Problem:** Claude forgets everything between sessions.  
**Solution:** Store everything in FILES and reload context intelligently.

```
┌─────────────────────────────────────────────────┐
│                YOUR VAULT                        │
│  (Plain Markdown files YOU own)                 │
├─────────────────────────────────────────────────┤
│ • CLAUDE.md - Core context & personality        │
│ • 05-Areas/People/ - Relationship memory        │
│ • 03-Tasks/Tasks.md - Work in progress          │
│ • System/Session_Memory/ - Past conversations   │
│ • System/Work_In_Progress.md - Active projects  │
└─────────────────────────────────────────────────┘
            ↓ loaded at session start ↓
         ┌─────────────────────────────┐
         │      AI Context Window      │
         └─────────────────────────────┘
```

**The magic:** Your knowledge lives in files. AI reads files. 
Therefore, AI can "remember" by reading what was written before.

---

### Building Block 1: CLAUDE.md (The Brain)

The system prompt that defines who Dex is and how it behaves.

**Location:** `/CLAUDE.md` (root of your vault)

**Contains:**
- Your user profile (name, role, company)
- Your strategic pillars
- How Dex should behave
- What skills are available
- References to other docs

**Why it matters:** This loads FIRST, before anything else. It shapes every 
response. Edit this, and you change how Dex thinks.

**You can customize:**
```markdown
## USER_EXTENSIONS_START
<!-- Your personal additions go here -->
## USER_EXTENSIONS_END
```

---

### Building Block 2: Session Hooks (The Boot Sequence)

When you start a chat, things happen BEFORE you type anything.

**What hooks do:**
- Inject session memories from recent conversations
- Surface relevant context (person info, project status)
- Pre-load data you'll likely need

**Current hooks in Dex:**
- Session memories injection
- Person context surfacing
- Company context surfacing

**The power:** You can ADD hooks. Want weather loaded at session start? 
Your calendar? Write a hook, and it's there every session.

---

### Building Block 3: MCP Servers (The Toolbox)

MCP = Model Context Protocol. It's how Claude gets superpowers.

Each MCP server gives Claude new abilities:

| Server | What It Does |
|--------|--------------|
| **Work MCP** | Task management with deduplication and pillar alignment |
| **Calendar MCP** | Reads your Apple Calendar |
| **Granola MCP** | Searches meeting transcripts |
| **Career MCP** | Career evidence tracking and analysis |

**Why MCPs instead of just reading files?**
- **Speed:** Pre-process data instead of parsing raw files
- **Logic:** Implement business rules (like "can't have 4 P0 tasks")
- **Integration:** Connect to external systems

---

### Building Block 4: Skills (The Playbook)

Skills are structured instructions for multi-step workflows.

**Location:** `.claude/skills/[skill-name]/SKILL.md`

**Examples:**
- `/daily-plan` - Check calendar, review tasks, generate plan
- `/meeting-prep` - Load person context, surface recent discussions
- `/xray` - This skill you're running right now!

**Why skills?**
- **Consistency:** Same workflow every time
- **Complexity:** Handle multi-step processes
- **Reusability:** Build once, use forever

---

### Building Block 5: The Vault (The Memory)

Everything persists to Markdown files:

```
Your Vault/
├── 00-Inbox/           ← Capture zone
├── 03-Tasks/           ← Active tasks
├── 04-Projects/        ← Time-bound work
├── 05-Areas/           ← Ongoing responsibilities
│   ├── People/         ← Person pages
│   └── Companies/      ← Company profiles
├── 06-Resources/       ← Reference material
└── System/             ← Dex configuration
```

**Why plain Markdown?**
- You own it forever (no vendor lock-in)
- Works anywhere (Obsidian, VS Code, any editor)
- AI can read and write it
- Version control with Git if you want

---

### How It All Connects

```
Session starts
     ↓
Hooks fire (inject context)
     ↓
CLAUDE.md loads (personality + instructions)
     ↓
You type your message
     ↓
Claude reads relevant files (on-demand)
     ↓
Claude uses MCPs (if needed)
     ↓
Response generated + files updated
     ↓
Repeat for each message
```

---

### Key Insight: It's All Text

There's no magic database. No proprietary format. No cloud service.

- CLAUDE.md is text
- Skills are text
- Your notes are text
- Session memories are text

Claude reads text, processes it, generates text, writes text.

**Everything you're experiencing is text transformation.**

Understanding this is liberating — you can read, edit, and extend anything.

---

**Want to see the session startup in detail?** Try `/xray boot`
**Ready to customize?** Try `/xray extend`
```

---

## MODE: Session Boot Sequence (`/xray boot`)

**Purpose:** Detailed walkthrough of what happens when a session starts.

### Output Format

```markdown
## 🚀 What Happens When You Start a Chat

Let me walk you through exactly what happens from the moment you open 
a new chat to when you type your first message.

---

### The Boot Sequence (In Order)

#### Step 1: Environment Detection
```
Is this Claude Desktop? Claude Code? Cursor? PI?
     ↓
Each environment has slightly different capabilities
```

#### Step 2: Settings Load
```
Read configuration files
     ↓
This defines which hooks to run and which MCPs are available
```

#### Step 3: Hooks Fire (CRITICAL)
```
Pre-session hooks run in order:
     ↓
┌─────────────────────────────────────────────┐
│ Session memory injection                    │
│ → Reads System/Session_Memory/[date].md     │
│ → Injects summaries of recent conversations │
│ → AI "remembers" what you discussed before  │
└─────────────────────────────────────────────┘
     ↓
┌─────────────────────────────────────────────┐
│ Context injectors                           │
│ → Person context ready when you mention     │
│   names                                     │
│ → Company context ready when relevant       │
└─────────────────────────────────────────────┘
     ↓
┌─────────────────────────────────────────────┐
│ (Your custom hooks could go here)           │
│ → Whatever YOU want loaded at start         │
└─────────────────────────────────────────────┘
```

**This is where the magic happens!** Hooks let you inject ANY context 
before the conversation starts.

#### Step 4: CLAUDE.md Loads
```
The entire CLAUDE.md file enters the context window:
     ↓
• Your profile (name, role, company)
• Your strategic pillars  
• Behavior guidelines
• Reference to skills and tools
• User extensions (YOUR customizations)
```

#### Step 5: MCPs Connect
```
MCP servers become available:
     ↓
• Calendar MCP → Ready to check schedule
• Work MCP → Ready to manage tasks
• Granola MCP → Ready to search meetings
```

#### Step 6: Ready for Input
```
NOW you can type your first message.

The AI already has:
• Your personality and preferences (CLAUDE.md)
• Recent conversation summaries (from hooks)
• Relevant context (from hooks)
• Access to tools (MCPs)
```

---

### What This Means for You

**The AI doesn't start from zero.** By the time you type your first message, 
Claude already knows who you are, what you've been working on, and what 
tools are available.

**The boot sequence IS the memory system.** It's how a stateless AI 
"remembers" who you are.

---

### 💡 Customization Opportunity

**What else could be loaded at session start?**

Ideas for hooks:
1. Today's calendar events
2. Current sprint goals
3. Recent Git commits
4. Weather for outdoor planning
5. Your daily intention

**The pattern:** Anything you want the AI to "know" at the start of every 
session can be injected via a hook.

---

**Ready to create your own customizations?** Try `/xray extend`
```

---

## MODE: Today (`/xray today`)

**Purpose:** ScreenPipe-powered analysis of the day's activity.

### Prerequisites

First check if ScreenPipe is running. If not:

```markdown
## 🔬 X-Ray: Today

ScreenPipe isn't running, so I can't analyze your full day.

**To enable day analysis:**
1. Start ScreenPipe: Run `screenpipe` in terminal
2. It records your screen activity locally (nothing sent to cloud)
3. Come back and run `/xray today` again

**What you'll get:**
- Time breakdown by app
- Activity patterns
- "Moments you missed" where Dex could have helped
```

### If ScreenPipe is running

Query ScreenPipe for today's activity and present:

```markdown
## 🔬 X-Ray: Today

[Activity summary from ScreenPipe]

---

### 🎓 How This Works

**What you just saw was ScreenPipe integration.** Here's what's happening:

1. **ScreenPipe records your screen** - Every few seconds, captures what's visible
2. **OCR extracts text** - It can "read" what's on screen
3. **A local database stores it** - SQLite on YOUR machine, not the cloud
4. **I query that database** - Via ScreenPipe tools

**Privacy model:**
- Everything stays on YOUR computer
- No data sent to external servers
- You control retention

**What this enables:**
- "What was I doing at 2pm?" → I can look it up
- "How much time in Slack?" → I can calculate
- "When did I see that error?" → I can search

---

[Continue with activity analysis, patterns, and suggestions]
```

---

## MODE: How to Extend (`/xray extend`)

**Purpose:** Practical guide to customization.

### Output Format

```markdown
## 🛠️ How to Extend Dex

Now that you understand how it works, here's how to make it your own.

---

### Level 1: Edit CLAUDE.md (5 minutes)

**The simplest customization.** Add your own instructions:

1. Open `CLAUDE.md` in any editor
2. Find the `USER_EXTENSIONS` section
3. Add your rules:

```markdown
## USER_EXTENSIONS_START

### My Preferences
- I'm a morning person — suggest important work before noon
- "The board" always means my company's board of directors
- Never suggest scheduling meetings on Wednesdays (my focus day)

## USER_EXTENSIONS_END
```

**This survives updates.** When you run `/dex-update`, this block is preserved.

---

### Level 2: Create a Skill (30 minutes)

**Make a reusable workflow:**

1. Create folder: `.claude/skills/my-skill/`
2. Create file: `SKILL.md`

```markdown
---
name: my-skill
description: What it does in one line
---

# My Custom Skill

## When to Use
[Trigger conditions]

## Steps
[Instructions for Claude to follow]

## Output Format
[What the result should look like]
```

3. Use it: Just type `/my-skill`

**Example ideas:**
- `/standup-prep` - Generate daily standup update
- `/client-brief` - Create client meeting brief
- `/weekly-email` - Draft weekly summary email

---

### Level 3: Create a Hook (1 hour)

**Inject context at every session start:**

1. Create a script that outputs the context you want
2. The output gets injected into the AI's context window
3. Now every conversation starts with that knowledge

**Example ideas:**
- Inject today's calendar at start
- Load current sprint goals
- Show recent Git commits

---

### Level 4: Create an MCP Server (Half day)

**Give Claude new capabilities:**

Run `/create-mcp` for guided setup.

**Example ideas:**
- Todoist MCP - Sync tasks with Todoist
- Notion MCP - Read/write to Notion
- Weather MCP - Get current conditions

---

### The Extension Philosophy

**Dex is scaffolding, not a finished product.** It's a starting point you customize.

The goal isn't to use Dex "as is" forever — it's to understand it well 
enough to make it truly yours.

**Question for you:** What do you wish the AI knew at the start of 
every session? That's your first extension.
```

---

## Usage Tracking

After running `/xray`, silently update `System/usage_log.md`:
- Check `X-ray transparency (/xray)` in the discovery section

If user runs specific educational modes, update the AI Education Progress section:
- `/xray ai` → Check "Understands context windows", "Understands tokens"
- `/xray dex` → Check "Understands system prompts", "Understands tools/MCPs"
- `/xray boot` → Check "Understands session hooks"
- `/xray extend` → Check "Understands vault architecture"

---

## Tone Guidelines

- **Concrete over abstract** — Use specific examples from their conversation
- **Show don't tell** — Point to actual files, tools, actions
- **Empowering not impressive** — Goal is their understanding, not your cleverness
- **Inviting curiosity** — End with pathways to learn more

---

## Track Usage (Silent)

Update `System/usage_log.md` to mark AI transparency education as used.

**Analytics (Silent):**

Call `track_event` with event_name `xray_used` and properties:
- `mode` (context/tokens/prompts/tools/hooks/vault/extend)

This only fires if the user has opted into analytics. No action needed if it returns "analytics_disabled".
