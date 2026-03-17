---
name: ai-setup
description: Configure AI model options - budget cloud models (save 80%+) and offline mode (use Dex without internet)
---

## Purpose

Help users configure alternative AI models for Dex:
1. **Budget Cloud** - Cheaper models like Kimi, DeepSeek (80-97% savings)
2. **Offline Mode** - Local models via Ollama (works without internet)
3. **Smart Routing** - Automatically pick the best model per task

This skill is designed for users of ALL technical levels. Use plain language, avoid jargon, and guide step-by-step.

## When to Run

- User types `/ai-setup`
- Mentioned during onboarding (optional advanced setup)
- User asks about reducing AI costs
- User asks about working offline
- User is traveling frequently

---

## Entry Point

Say:

```
**Let's configure your AI options!**

Right now, Dex uses Claude for everything. It's excellent, but it costs money per use and requires internet.

Here are your options:

---

**1. 💰 Budget Cloud Mode** — Cheaper AI when online
   
   **What it is:** Use models like Kimi or DeepSeek that cost 80-97% less than Claude
   
   **The catch:** Requires a small upfront payment (~$5-10) to a service called OpenRouter
   - You'll need a credit card or Apple Pay
   - That $5-10 lasts weeks or months
   - Example: If Claude costs you $90/month, this would cost ~$10-20/month
   
   **Best for:** People who use Dex heavily and want to cut costs

---

**2. ✈️ Offline Mode** — AI that runs on your computer
   
   **What it is:** Download a free AI model that works without internet
   
   **The catch:** Uses your computer's memory and processing power
   - Requires ~8GB RAM minimum (you have 36GB ✅)
   - One-time download of 8-20GB
   - Slightly lower quality than Claude
   
   **Best for:** Travel (planes, trains), privacy, or if you don't want to pay anything
   
   **Cost: Completely free forever**

---

**3. 🎯 Smart Routing** — Automatic model selection
   
   This automatically picks the best model for each task. It works with whatever you set up above — if you only set up offline mode, it'll use that for simple tasks.

---

**Which would you like to set up?**

- "Budget cloud" — I'll walk you through the payment setup
- "Offline" — Free, no payment needed, let's do it
- "Both" — Get the most flexibility
- "Neither" — Stick with Claude for now
```

Wait for user response, then branch accordingly.

### If User Chooses "Both"

```
Great choice — you'll have maximum flexibility!

Let's start with **offline mode** first (it's free and quick), then we'll do budget cloud.

---
```

Then run Branch 2 (Offline), and when complete, transition:

```
**Offline mode is ready!** ✅

Now let's set up budget cloud so you can save money when you're online.

Budget cloud requires adding ~$5-10 to an OpenRouter account.

**Ready to continue, or want to stop here?**
- "Continue" — Let's set up budget cloud
- "Stop here" — Offline is enough for now (you can add budget cloud later)
```

If they continue, run Branch 1. If they stop, skip to smart routing offer.

### Graceful Pivots

If user hesitates on budget cloud or mentions payment concerns:

```
No problem! The offline option is completely free and works great for most daily tasks.

Want to set that up instead? You can always add budget cloud later when it makes sense.
```

If user can't do offline (old hardware, not enough RAM):

```
With your current setup, local AI would be quite slow. 

Your best options are:
1. **Stick with Claude** — Best quality, you're already set up
2. **Budget cloud** — Much cheaper than Claude, but does need that initial payment

What sounds better?
```

---

## Branch 1: Budget Cloud Setup

### Step 1.0: Confirm They're Ready to Pay

Before diving into setup, confirm:

```
**Quick check before we start:**

Budget cloud requires:
✓ Creating an account at OpenRouter.ai
✓ Adding ~$5-10 in credits (credit card or Apple Pay)
✓ About 5 minutes to set up

This is a one-time setup. That $5-10 will last you weeks or months.

**Ready to proceed?**
- "Yes" — Let's do it
- "Actually, let's do offline instead" — No problem, that's free
- "Maybe later" — We can come back to this anytime
```

If they want to pivot to offline, go to Branch 2.

### Step 1.1: Explain the Options (Plain Language)

```
**Budget Cloud Models — What Are Your Options?**

These are AI models from other companies that cost much less:

| Model | Monthly Savings | Quality | Best For |
|-------|-----------------|---------|----------|
| **Kimi K2.5** | ~80% cheaper | ⭐⭐⭐⭐ Great | General tasks, thinking |
| **DeepSeek V3** | ~95% cheaper | ⭐⭐⭐⭐ Great | Coding, analysis |
| **Gemini Flash** | ~97% cheaper | ⭐⭐⭐ Good | Long documents |

**My recommendation:** Start with **Kimi K2.5** — it's the closest to Claude in quality.

**Real cost example:**
If you currently spend ~$90/month on Claude, Kimi would cost ~$18/month for similar tasks.

Want to set up Kimi? (You can always add others later)
```

### Step 1.2: OpenRouter Setup (The Key Step)

```
**Setting Up Kimi (5-minute setup)**

To use these models, we go through a service called **OpenRouter**. 
Think of it like a phone plan that lets you call different networks.

**Here's what to do:**

**Step 1: Create an OpenRouter account**
   Go to: **https://openrouter.ai/keys**
   Click "Sign up" (Google/GitHub login works)

**Step 2: Add credits**
   - Click "Credits" in the top menu
   - Add $5-10 to start (this lasts weeks/months)
   - They accept cards, Apple Pay, etc.

**Step 3: Create an API key**
   - Go to: https://openrouter.ai/keys
   - Click "Create Key"
   - Give it a name like "Dex"
   - Copy the key (starts with `sk-or-...`)

**Step 4: Paste your key here**

Once you have your key, paste it here and I'll configure everything automatically.

---

*Stuck? Here's what each step looks like:*
- OpenRouter's interface is simple - big blue buttons
- The API key is just a password for your account
- Your credits work for ALL their models (Kimi, DeepSeek, etc.)
```

### Step 1.3: Configure the Key

When user provides key:

```python
# Validate key format
if not key.startswith("sk-or-"):
    respond("Hmm, that doesn't look like an OpenRouter key. They usually start with 'sk-or-'. Can you double-check?")
    return

# Create or update models.json
```

Generate `~/.pi/agent/models.json`:

```json
{
  "providers": {
    "openrouter": {
      "baseUrl": "https://openrouter.ai/api/v1",
      "api": "openai-completions",
      "apiKey": "USER_KEY_HERE",
      "models": [
        {
          "id": "moonshotai/kimi-k2.5",
          "name": "Kimi K2.5 (Budget)",
          "input": ["text"],
          "contextWindow": 262144,
          "maxTokens": 32768,
          "cost": { "input": 0.6, "output": 3, "cacheRead": 0, "cacheWrite": 0 }
        },
        {
          "id": "deepseek/deepseek-chat",
          "name": "DeepSeek V3 (Budget)",
          "input": ["text"],
          "contextWindow": 64000,
          "maxTokens": 8192,
          "cost": { "input": 0.14, "output": 0.28, "cacheRead": 0, "cacheWrite": 0 }
        },
        {
          "id": "google/gemini-2.0-flash-exp:free",
          "name": "Gemini Flash (Free tier)",
          "input": ["text", "image"],
          "contextWindow": 1048576,
          "maxTokens": 8192,
          "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 }
        }
      ]
    }
  }
}
```

Say:

```
**Done! Budget models are ready.**

I've added three models you can switch to anytime:
- **Kimi K2.5** — Best quality budget option
- **DeepSeek V3** — Super cheap, great for coding
- **Gemini Flash** — Google's free tier (with limits)

**How to use them:**

**Option A: Switch in this session**
   Type `/model` and select one from the list

**Option B: Ask me to switch**
   Just say "use the budget model" or "switch to Kimi"

**Option C: Set as default** (advanced)
   I can make Kimi your default and only use Claude for complex stuff

---

**Quick test:** Want me to do something simple with Kimi right now so you can see it work?
```

### Step 1.4: Update User Profile

Add to `System/user-profile.yaml`:

```yaml
ai_models:
  budget_cloud:
    enabled: true
    provider: openrouter
    primary_model: moonshotai/kimi-k2.5
    configured_date: 2026-02-04
```

---

## Branch 2: Offline Mode Setup

### Step 2.1: Check System Requirements

```
**Offline Mode — Let's Check Your Setup**

To run AI on your computer, I need to know what you're working with.

**Quick question:** What kind of computer are you using?

1. **Mac with Apple Silicon** (M1, M2, M3, M4 chip)
2. **Mac with Intel** (older Mac)
3. **Windows PC**
4. **Linux**
5. **Not sure**

(Most Macs from 2020 onwards have Apple Silicon)
```

Based on response, check RAM:

```
**Great! Now let's check your memory (RAM).**

On Mac:
1. Click the Apple menu (top-left corner)
2. Click "About This Mac"
3. Look for "Memory" — what number do you see?

On Windows:
1. Right-click the Start button
2. Click "System"
3. Look for "Installed RAM"

What does it say? (e.g., "8 GB", "16 GB", "32 GB")
```

### Step 2.2: Recommend Model Based on RAM

```python
if ram <= 8:
    model = "qwen2.5:7b"
    quality = "Good for 70% of tasks"
    size = "4.4 GB download"
elif ram <= 16:
    model = "qwen2.5:14b" 
    quality = "Good for 80% of tasks"
    size = "8.5 GB download"
elif ram <= 32:
    model = "qwen2.5:32b"
    quality = "Near-Claude for most tasks"
    size = "18 GB download"
else:
    model = "qwen2.5:72b"
    quality = "Excellent, close to Claude"
    size = "40 GB download"
```

Say:

```
**Perfect! Here's my recommendation:**

With **{{RAM}} GB** of memory, you can run **Qwen 2.5 {{size}}**.

**What to expect:**
- Quality: {{quality_description}}
- Download size: {{size}}
- Speed: {{speed based on chip}}

**What works great offline:**
✅ Daily planning and reviews
✅ Meeting summaries
✅ Task management
✅ Note organization
✅ Simple analysis

**What's better with Claude:**
⚠️ Complex strategic planning
⚠️ Nuanced writing
⚠️ Multi-step reasoning

Ready to set this up? It takes about 10-15 minutes (mostly download time).
```

### Step 2.3: Install Ollama

Check if Ollama is already installed:

```bash
which ollama || echo "not installed"
```

If not installed:

```
**Step 1: Install Ollama**

Ollama is a free app that runs AI models on your computer.

**On Mac (easiest way):**
1. Go to: **https://ollama.ai/download**
2. Click "Download for macOS"
3. Open the downloaded file
4. Drag Ollama to your Applications folder
5. Open Ollama from Applications (you'll see a llama icon in your menu bar)

**On Windows:**
1. Go to: **https://ollama.ai/download**
2. Click "Download for Windows"
3. Run the installer
4. Follow the prompts

**Let me know when Ollama is installed and running** (you should see a llama icon in your menu bar / system tray).
```

### Step 2.4: Download the Model

Once Ollama is confirmed running:

```
**Step 2: Download the AI model**

Now let's download the model to your computer. This is a one-time download.

**Run this command in Terminal:**

```
ollama pull {{recommended_model}}
```

**How to open Terminal:**
- Mac: Press Cmd+Space, type "Terminal", press Enter
- Windows: Search for "Command Prompt"

**Then paste the command above and press Enter.**

This will download ~{{size}}. It might take 5-15 minutes depending on your internet speed.

Let me know when it says "success"!
```

### Step 2.5: Configure Pi for Offline

Once model is downloaded, update `~/.pi/agent/models.json` to add Ollama:

```json
{
  "providers": {
    "ollama": {
      "baseUrl": "http://localhost:11434/v1",
      "api": "openai-completions", 
      "apiKey": "ollama",
      "models": [
        {
          "id": "{{recommended_model}}",
          "name": "{{model_name}} (Offline)",
          "input": ["text"],
          "contextWindow": 32768,
          "maxTokens": 8192,
          "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 }
        }
      ]
    }
  }
}
```

### Step 2.6: Test Offline Mode

```
**Step 3: Let's test it!**

Try this:
1. Turn off your WiFi (just for testing)
2. In Pi, type `/model` and select "{{model_name}} (Offline)"
3. Ask me something simple like "What day is it?"

If I respond, offline mode works! 🎉

Go ahead and test, then turn WiFi back on and let me know how it went.
```

### Step 2.7: Confirm Success

```
**Offline mode is ready!**

What happens now:
- When you have internet → Dex uses Claude (best quality)
- When you're offline → Dex can use your local model
- You can also manually switch anytime with `/model`

**For your next flight or train ride:**
1. Make sure Ollama is running (llama icon in menu bar)
2. Start Pi/Dex as usual
3. If internet isn't available, switch to your offline model

**Pro tip:** Test it at home once before relying on it during travel!

---

Want to also set up budget cloud models to save money when online?
```

Update `System/user-profile.yaml`:

```yaml
ai_models:
  offline:
    enabled: true
    runner: ollama
    model: qwen2.5:14b
    configured_date: 2026-02-04
```

---

## Branch 3: Smart Routing

### Step 3.1: Check What's Already Configured

First, check what's set up:
- Read `System/user-profile.yaml` for `ai_models` section
- Run `bash ~/Claudesidian/System/scripts/test-ai-connections.sh` silently

Then adapt the explanation:

**If both budget cloud and offline are configured:**

```
**Smart Routing — I'll Pick the Best Model Automatically**

You've got all three tiers set up — nice! Here's how I'll use them:

| Task Type | Model | Why |
|-----------|-------|-----|
| Complex planning, coaching | Claude | Needs deep reasoning |
| Daily tasks, summaries | Kimi (budget) | Good enough, saves money |
| Quick questions | Kimi (budget) | Fast and cheap |
| When you're offline | Qwen (local) | Only option! |

**Want to enable smart routing?**
- "Yes" — I'll pick automatically (you can always override)
- "No" — I'll always ask before switching
```

**If only offline is configured:**

```
**Smart Routing — I'll Pick Based on What You Have**

Since you set up offline mode, here's how routing works:

| Task Type | Model | Why |
|-----------|-------|-----|
| Complex tasks | Claude | When you need the best |
| Simple tasks | Claude | (budget not configured) |
| When you're offline | Qwen (local) | Your backup! |

**Tip:** If you add budget cloud later, I can start using cheaper models for simple tasks automatically.

**Want to enable smart routing?**
- "Yes" — Claude when online, local when offline
- "No" — I'll always ask
```

**If only budget cloud is configured:**

```
**Smart Routing — I'll Pick Based on What You Have**

Since you set up budget cloud, here's how routing works:

| Task Type | Model | Why |
|-----------|-------|-----|
| Complex tasks | Claude | When you need the best |
| Simple tasks | Kimi (budget) | Saves money! |
| Offline | ❌ Not available | (not configured) |

**Tip:** If you add offline mode later, you'll have a backup for travel.

**Want to enable smart routing?**
- "Yes" — Claude for complex, Kimi for simple
- "No" — I'll always ask
```

**If neither is configured:**

```
**Smart Routing — Nothing to Route Yet!**

Smart routing works best when you have alternatives set up. Right now you only have Claude.

Would you like to set up:
- "Offline mode" — Free, works without internet
- "Budget cloud" — Cheaper models, needs ~$5-10 upfront
- "Neither for now" — Stick with Claude
```

### Step 3.2: Configure Smart Routing

Based on what's configured, update `System/user-profile.yaml`:

```yaml
ai_models:
  smart_routing:
    enabled: true
    # Only include models that are actually configured
    rules:
      complex_tasks:
        model: claude-sonnet  # Always available
      routine_tasks:
        model: {{budget_model_if_configured OR "claude-sonnet"}}
      offline:
        model: {{offline_model_if_configured OR null}}
```

**Confirmation message (adapts to setup):**

If budget + offline:
```
**Smart routing is enabled!**

Here's what I'll do:
- Complex tasks (planning, coaching) → Claude
- Simple tasks (summaries, quick questions) → Kimi (saves money)
- When offline → Your local model

You can always override by saying "use Claude for this" or "switch to budget".
```

If only offline:
```
**Smart routing is enabled!**

Here's what I'll do:
- When online → Claude (best quality)
- When offline → Your local model (automatic fallback)

If you add budget cloud later, I can start saving you money on simple tasks.
```

If only budget:
```
**Smart routing is enabled!**

Here's what I'll do:
- Complex tasks → Claude (best quality)
- Simple tasks → Kimi (saves money)

If you add offline mode later, you'll have a backup for travel.
```

---

## Troubleshooting Section

### Ollama Not Starting

```
**Ollama won't start?**

Try these fixes:

**Mac:**
1. Open Applications folder
2. Right-click Ollama → Open
3. If blocked: System Preferences → Security → Allow Ollama

**If still stuck:**
1. Open Terminal
2. Run: `ollama serve`
3. Keep that window open

Let me know if you see any error messages.
```

### OpenRouter Key Not Working

```
**OpenRouter key not working?**

Let's debug:

1. **Check key format** — Should start with `sk-or-`
2. **Check credits** — Go to openrouter.ai/credits, make sure you have balance
3. **Test the key:**
   ```
   curl https://openrouter.ai/api/v1/models \
     -H "Authorization: Bearer YOUR_KEY_HERE"
   ```
   
   You should see a list of models, not an error.

4. **Regenerate key** — Go to openrouter.ai/keys, delete old key, make new one

What do you see when you try the test?
```

### Model Too Slow

```
**Local model running slow?**

This usually means the model is too big for your RAM.

**Fix options:**
1. **Try a smaller model:**
   ```
   ollama pull qwen2.5:7b
   ```
   (smaller = faster, but slightly less capable)

2. **Close other apps** — Free up memory

3. **Check Activity Monitor** (Mac) or Task Manager (Windows)
   - If RAM is maxed out, you need a smaller model

Want me to help you switch to a smaller model?
```

---

## Edge Cases

### User Has No Credit Card

```
**No credit card for OpenRouter?**

Some alternatives:

1. **Gemini Flash Free Tier** — Google offers free usage (with limits)
   I can set that up instead

2. **Offline Only** — Skip budget cloud, just use local models
   Free forever, works without internet

3. **Anthropic Direct** — If you have Claude credits already, we can optimize usage

Which works for you?
```

### User on Very Old Hardware

```
**Older computer detected**

With {{RAM}} GB RAM, local AI will be very slow.

**Better options for you:**
1. **Budget cloud only** — Uses internet, but works on any computer
2. **Stick with Claude** — Best quality, works everywhere

Offline mode really needs 8GB+ RAM to be useful.

Want to set up budget cloud instead?
```

---

## Success Metrics

After setup, track in `System/usage_log.md`:
- [ ] Configured budget cloud models
- [ ] Configured offline mode  
- [ ] Enabled smart routing
- [ ] Used budget model for a task
- [ ] Used offline model

---

## Post-Setup Summary

After any setup completes, show an adaptive summary and offer smart routing:

### If only offline was set up:

```
**Setup Complete!** ✅

| Mode | Status |
|------|--------|
| Premium (Claude) | ✅ Always available |
| Budget Cloud | ❌ Not configured |
| Offline Mode | ✅ Ready (Qwen 2.5) |

**How to use offline mode:**
- When you're online: Dex uses Claude (best quality)
- When you're offline: Switch with `/model` or say "use offline model"
- Or I can switch automatically when I detect you're offline

**Want to enable smart routing?** (I'll automatically use your local model when offline)
- "Yes" — Enable automatic switching
- "No" — I'll ask before switching

You can add budget cloud later with `/ai-setup` if you want to save money.
```

### If only budget cloud was set up:

```
**Setup Complete!** ✅

| Mode | Status |
|------|--------|
| Premium (Claude) | ✅ Always available |
| Budget Cloud | ✅ Ready (Kimi K2.5) |
| Offline Mode | ❌ Not configured |

**How to use budget models:**
- Say "use budget model" or "use Kimi"
- Or use `/model` to switch manually
- Or I can pick automatically based on task complexity

**Want to enable smart routing?** (I'll use Kimi for simple tasks, Claude for complex ones)
- "Yes" — Enable automatic switching
- "No" — I'll ask before switching

You can add offline mode later with `/ai-setup` for travel.
```

### If both were set up:

```
**Setup Complete!** ✅

| Mode | Status | Model |
|------|--------|-------|
| Premium | ✅ | Claude Sonnet |
| Budget | ✅ | Kimi K2.5 |
| Offline | ✅ | Qwen 2.5 |

**You have maximum flexibility!**

**Want to enable smart routing?** 
I'll automatically:
- Use Claude for complex tasks (planning, coaching)
- Use Kimi for simple tasks (summaries, quick questions) — saves money
- Use your local model when offline — automatic fallback

- "Yes" — Enable smart routing
- "No" — I'll ask each time

**Quick reference:**
- "Use Kimi" → Switch to budget
- "Use Claude" → Switch to premium
- `/model` → Manual picker
- `/ai-status` → Check configuration
```

## Track Usage (Silent)

Update `System/usage_log.md` to mark AI setup as used.

**Analytics (Silent):**

Call `track_event` with event_name `ai_setup_completed` and properties:
- `mode` (budget_cloud/offline/smart_routing)

This only fires if the user has opted into analytics. No action needed if it returns "analytics_disabled".

---

## Follow-up Skill: /ai-status

Users can check their AI setup anytime:

```
/ai-status

**Your AI Configuration**

| Mode | Status | Model |
|------|--------|-------|
| Premium | ✅ | Claude Sonnet |
| Budget | {{✅ / ❌}} | {{Kimi K2.5 / Not configured}} |
| Offline | {{✅ / ❌}} | {{Qwen 2.5 / Not configured}} |
| Smart Routing | {{✅ Enabled / ❌ Disabled}} | |

**This session:** Using {{current_model}}
{{If OpenRouter configured:}} **OpenRouter credits:** ${{balance}} remaining
{{If Ollama configured:}} **Ollama status:** {{Running ✅ / Not running ⚠️}}

**Quick actions:**
- `/model` — Switch models
- `/ai-setup` — Configure more options
- "Use budget model" — Quick switch
```
