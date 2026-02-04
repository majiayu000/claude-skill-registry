---
name: setup
description: Initial Dex system setup and onboarding
disable-model-invocation: true
---

---
name: setup
description: Set up your personal knowledge system with a simple conversation
---

# Set Up Your Dex

Guide the user through a friendly, conversational setup. No technical steps required.

## Task

Have a conversation to understand who the user is and what they need. Then generate a personalized configuration.

## Process

### Step 1: Welcome

Say: "Welcome to Dex! I'm your personal knowledge assistant. Let's get you set up in about 2 minutes."

"First, what's your name?"

### Step 2: Role

Ask: "What's your role?"

Present this list:

```
**Core Functions**
1. Product Manager
2. Sales / Account Executive
3. Marketing
4. Engineering
5. Design

**Customer-Facing**
6. Customer Success
7. Solutions Engineering

**Operations**
8. Product Operations
9. RevOps / BizOps
10. Data / Analytics

**Support Functions**
11. Finance
12. People (HR)
13. Legal
14. IT Support

**Leadership**
15. Founder

**C-Suite**
16. CEO
17. CFO
18. COO
19. CMO
20. CRO
21. CTO
22. CPO
23. CIO
24. CISO
25. CHRO / Chief People Officer
26. CLO / General Counsel
27. CCO (Chief Customer Officer)

**Independent / Advisory**
28. Fractional CPO
29. Consultant
30. Coach

Type a number, or describe your role if it's not listed:
```

Accept numbers, role names, or descriptions like "I'm mostly PM but do some engineering."

### Step 3: Company Size

Ask: "What's your company size?"

```
1. 1-100 people (startup/small)
2. 100-1,000 people (scaling)
3. 1,000-10,000 people (enterprise)
4. 10,000+ people (large enterprise)
```

### Step 4: Priorities

Ask: "What are your 2-3 main priorities right now? These will become your strategic pillars."

Examples to help them: "Like 'close Q1 deals', 'launch new product', 'build team', 'thought leadership'..."

### Step 5: Profile Research (Optional)

Ask: "Would you like me to research your public work to better understand your context? This helps me give more relevant suggestions."

If yes:
- Ask for any identifying details (company, website, LinkedIn)
- Search for information
- Show findings and confirm: "Is this you?"
- If wrong person or multiple found, clarify
- Save relevant context

If no or later: Skip to next step.

### Step 5b: Meeting Intelligence (Optional)

Ask: "Do you use Granola for meeting transcription?"

**If no:** Skip to Step 6.

**If yes:**

Check if Granola cache exists: `~/Library/Application Support/Granola/cache-v3.json`

If cache not found:
> "I don't see Granola's cache yet. Make sure you've run at least one meeting with Granola, then we can set this up."

If cache found, ask:

> "Great! Dex can process your Granola meetings to extract summaries, action items, and update person pages.
>
> **How would you like to process meetings?**
>
> 1. **Manual** (recommended to start) — Run `/process-meetings` whenever you want. Uses Claude directly, no API key needed.
>
> 2. **Automatic** — Runs in the background every 30 minutes, even when Cursor is closed. Requires an API key.
>
> Which do you prefer?"

**If Manual (option 1):**
- No additional setup needed
- Update `System/user-profile.yaml` with `meeting_processing: manual`
- Say: "You're all set! Run `/process-meetings` after your meetings to pull them into Dex."

**If Automatic (option 2):**

Ask which API provider they want to use:

> "Automatic processing needs an API key to run in the background. Which provider do you prefer?
>
> | Provider | Cost | Notes |
> |----------|------|-------|
> | **Gemini** | Free tier (1500 req/day) | Best for most users |
> | **Anthropic** | ~$0.01/meeting | Highest quality |
> | **OpenAI** | ~$0.01/meeting | Fast, reliable |
>
> Type 1 for Gemini, 2 for Anthropic, or 3 for OpenAI:"

Based on choice:

**For all providers:**

1. Provide the appropriate link:
   - **Gemini:** https://aistudio.google.com/apikey
   - **Anthropic:** https://console.anthropic.com/settings/keys
   - **OpenAI:** https://platform.openai.com/api-keys

2. Ask: "Please get your API key from the link above and paste it here:"

3. Wait for their key, then:
   - If `.env` doesn't exist, create it from `env.example`
   - Add a comment: `# API key for automatic meeting processing`
   - Add their key: `GEMINI_API_KEY=their-key` (or `ANTHROPIC_API_KEY` or `OPENAI_API_KEY`)

4. Explain simply:
   > "I've saved your API key to a file called `.env` (a secure place for credentials). The background meeting sync will use this to process your meetings automatically."

5. Run `npm install` to install dependencies
5. Update `System/user-profile.yaml` with `meeting_processing: automatic` and `meeting_api_provider: [choice]`
6. Run `.scripts/meeting-intel/install-automation.sh`

Say: "Automatic processing enabled! Meetings will sync every 30 minutes. You can also run `/process-meetings` anytime."

**Configure meeting intelligence based on role:**
- **Sales/AE**: Enable customer intel + competitive intel
- **Product Manager**: Enable customer intel + competitive intel
- **Engineering**: Disable customer/competitive intel (focus on decisions/action items)
- **Other**: Ask which intelligence types they want

Update `System/user-profile.yaml` with their preferences.

### Step 6: Generate Configuration

Based on their answers:

1. **Create folder structure** (silently, no terminal output needed):
   - `04-Projects/`
   - `05-Areas/People/Internal/`
   - `05-Areas/People/External/`
   - `05-Areas/Companies/`
   - `06-Resources/Learnings/`
   - `06-Resources/Quarterly_Reviews/`
   - `System/Templates/`
   - `07-Archives/Projects/`
   - `07-Archives/Plans/`
   - `07-Archives/Reviews/`
   - `00-Inbox/Meetings/`
   - `00-Inbox/Ideas/`
   - `01-Quarter_Goals/` (optional)
   - `03-Tasks/`
   - `02-Week_Priorities/`
2. **Update CLAUDE.md** with their profile:
   - Name
   - Role
   - Company size
   - Pillars (their priorities)
3. **Update `System/pillars.yaml`** with their strategic pillars
4. **Update `System/user-profile.yaml`** with:
   - Name
   - Role
   - Company (if provided)
   - Meeting intelligence preferences (based on role or their choices)
5. **Save to `.claude/vault-config.json`**:
   ```json
   {
     "user": {
       "name": "Their Name",
       "role": "Product Manager",
       "companySize": "scaling",
       "pillars": ["priority1", "priority2", "priority3"]
     },
     "createdAt": "2026-01-22"
   }
   ```

### Step 7: Welcome Message

Say: "You're all set, [Name]! Here's what I created for you:"

Show a brief summary:
- Their role and pillars
- Key folders created
- 2-3 suggested first actions based on their role


**Optional:** If this is a fresh start, mention:

> "Tip: Want to explore with sample data first? Run `/dex-demo on` to try demo mode with pre-populated content. You can switch back anytime with `/dex-demo off`."

End with: "What would you like to work on first?"

## For Users with Existing Notes

If user mentions they have existing notes:

Say: "Great! Just copy them into the `00-Inbox/` folder and I'll help you organize them. You can drag and drop files, or copy whole folders."

No automated import needed - simple manual copy works for everyone.

## Viewing Your Notes

Dex creates markdown files you can view with any app:
- VS Code or Cursor (where you're running Claude)
- Obsidian (popular free option)
- Notion (can import markdown)
- Any text editor

## Example Conversation

```
Dex: Welcome to Dex! I'm your personal knowledge assistant. Let's get you set up in about 2 minutes.

First, what's your name?

User: Sarah

Dex: Nice to meet you, Sarah! What's your role?

[Shows role list]

User: 1

Dex: Product Manager - great choice! What's your company size?

[Shows size options]

User: 2

Dex: Got it, you're at a scaling company (100-1,000 people). 

What are your 2-3 main priorities right now? These will become your strategic pillars.

User: Launching our mobile app, improving customer retention, and building out the PM team

Dex: Perfect priorities! Would you like me to research your public work to better understand your context?

User: No thanks

Dex: No problem! You're all set, Sarah!

Here's what I created for you:
- **Role:** Product Manager at a scaling company
- **Your pillars:** Mobile app launch, Customer retention, PM team building
- **Folders:** Projects, Relationships, Content, Meetings, Ideas

Suggested first actions:
1. Create a project for your mobile app launch
2. Start a meeting note for your next 1:1
3. Capture an idea that's been on your mind

What would you like to work on first?
```
