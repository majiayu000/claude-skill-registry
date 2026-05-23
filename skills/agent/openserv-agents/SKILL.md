---
name: openserv-agents
version: 2.0.0
author: OpenServ Labs (combined from agent-starter and openserv-docs)
created: 2026-01-22
last_updated: 2026-01-22
status: active
complexity: moderate
category: ai-agent-development
tags: [ai-agents, multi-agent-orchestration, openserv-platform, openserv-sdk, agent-deployment, typescript, python, agent-framework]
sources:
  - https://github.com/openserv-labs/agent-starter
  - https://github.com/openserv-labs/openserv-docs
---

# OpenServ Agents - Complete Platform Guide

> **Combined Skill**: This skill merges the agent-starter SDK guide and openserv-docs platform documentation into a single comprehensive resource for building AI agents on the OpenServ platform.

## When to Use This Skill

Use this skill when you need to:
- Build AI agents for the OpenServ multi-agent orchestration platform
- Deploy agents using the OpenServ API, SDK, or no-code builder
- Integrate agents with the OpenServ "Second Brain" architecture
- Implement agent endpoints for task handling and chat messaging
- Deploy agents to production hosting services
- Understand the BRAID reasoning framework
- Work with OpenServ's tokenization and startup platform features

## When NOT to Use This Skill

Do not use this skill when:
- You need general AI agent development without platform integration
- You're working with other agent platforms (LangChain, AutoGPT, CrewAI, etc.)
- You need model-agnostic agent orchestration
- You don't need the OpenServ platform's specific features

## Prerequisites

Before using this skill, ensure you have:
- JavaScript/TypeScript or Python programming knowledge
- Node.js v16+ (for SDK/API development) or Python 3.8+
- OpenServ platform account (https://platform.openserv.ai)
- OpenServ API key (optional: for local testing)
- OpenAI API key (optional: for `.process()` method)
- Tunneling tool for local development (ngrok or localtunnel)
- Basic understanding of REST APIs and async programming

## What This Skill Does

This skill provides comprehensive guidance for building autonomous AI agents on the OpenServ platform, covering:

1. **Three Development Paths**:
   - API approach (maximum flexibility, any language)
   - SDK approach (TypeScript framework for advanced agents)
   - No-code approach (visual builder, no programming)

2. **Platform Integration**:
   - "Second Brain" architecture understanding
   - Agent registration and API key creation
   - Endpoint implementation patterns
   - Task and chat message handling

3. **Deployment Workflows**:
   - Local development with tunneling
   - Production deployment strategies
   - Multi-platform deployment guides
   - Environment configuration

4. **OpenServ API Integration**:
   - File management endpoints
   - Task management (complete/error)
   - Chat messaging
   - Workspace interactions

5. **Testing and Review**:
   - Development testing checklist
   - Multi-agent scenario testing
   - Platform submission process

## Workflow

### Phase 1: Choose Development Approach

**Decision Point: Select Your Development Path**

Based on your requirements and expertise:

**Option A: API Approach (Maximum Flexibility)**
- Use when: You want language freedom, need custom workflows, have existing codebase
- Provides: Complete control over implementation
- Language: Any language with HTTP support
- Best for: Experienced developers, custom integrations

**Option B: SDK Approach (Powerful Framework)**
- Use when: Building advanced agents quickly, need TypeScript strong typing
- Provides: Built-in methods, autonomous agent runtime, agent collaboration
- Language: TypeScript/JavaScript only
- Best for: Rapid development, complex agent logic

**Option C: No-Code Approach (Zero Programming)**
- Use when: Non-technical users, rapid prototyping, simple agents
- Provides: Visual interface, natural language configuration
- Language: None required
- Best for: Beginners, simple use cases, quick deployment

**Validation Checklist**:
- [ ] Selected development approach based on expertise and requirements
- [ ] Confirmed prerequisites are met (Node.js/Python, platform account)
- [ ] Understood chosen approach's capabilities and limitations

### Phase 2: Platform Setup and Registration

**Step 1: Create OpenServ Account**
```bash
# Visit platform and create account
https://platform.openserv.ai

# Navigate to Developer menu → Profile
# Set up developer account
```

**Step 2: Set Up Local Development Environment**

For API/SDK development, install tunneling tool:

```bash
# Option 1: ngrok (recommended)
# Download from https://ngrok.com/download

# Start tunnel on your development port
ngrok http 7378

# Copy the forwarding URL (e.g., https://abc123.ngrok-free.app)
```

```bash
# Option 2: localtunnel (open source)
npm install -g localtunnel

# Start tunnel
lt --port 7378

# Copy the tunnel URL
```

**Step 3: Register Your Agent**

Navigate to Developer → Add Agent:
- **Agent Name**: Descriptive name (e.g., "Summarizer First Agent")
- **Agent Endpoint**: Your tunneling URL from Step 2
- **Capabilities Description**: Specific description of what your agent does
  - ✅ Good: "I receive text input and generate a concise, three-sentence summary about it."
  - ❌ Bad: "I can summarize text."

**Step 4: Create API Key**

Navigate to Developer → Your Agents → [Your Agent] → Details:
```bash
# Click "Create Secret Key"
# Store securely - required for API authentication
```

**Step 5: Configure Environment Variables**

```bash
# Add to .env file or export
export OPENSERV_API_KEY=your_api_key_here
export OPENAI_API_KEY=your_openai_api_key_here  # Optional
```

**Validation Checklist**:
- [ ] OpenServ developer account created
- [ ] Tunneling tool installed and running
- [ ] Agent registered with proper capabilities description
- [ ] API key created and stored securely
- [ ] Environment variables configured

### Phase 3: Agent Implementation

#### Implementation Path A: Using the OpenServ API

**Architecture: "Second Brain" Concept**

OpenServ uses a "Second Brain" architecture:
1. **Your agent**: Implements core capabilities (e.g., summarizing)
2. **Project Manager agent**: Routes requests to appropriate agents
3. **Your job**: Implement endpoints, handle requests, return responses

**Required Endpoint Structure**

Implement a single POST endpoint (typically `/`) that handles different action types:

```typescript
// TypeScript/Express example
import express from 'express';

const app = express();
app.use(express.json());

app.post("/", async (req, res) => {
  const action = req.body as Action;

  switch (action.type) {
    case "do-task": {
      // Handle task execution asynchronously
      void doTask(action);
      break;
    }
    case "respond-chat-message": {
      // Handle chat messages asynchronously
      void respondChatMessage(action);
      break;
    }
  }

  // Immediately respond to acknowledge receipt
  res.json({ message: "OK" });
});

app.listen(7378, () => {
  console.log("Agent running on http://localhost:7378");
});
```

```python
# Python/Flask example
from flask import Flask, request, jsonify
import threading

app = Flask(__name__)

@app.route("/", methods=["POST"])
def handle_action():
    action = request.json
    action_type = action.get("type")

    if action_type == "do-task":
        # Handle task asynchronously
        threading.Thread(target=do_task, args=(action,)).start()
    elif action_type == "respond-chat-message":
        # Handle chat asynchronously
        threading.Thread(target=respond_chat_message, args=(action,)).start()

    # Immediately acknowledge receipt
    return jsonify({"message": "OK"})

if __name__ == "__main__":
    app.run(port=7378)
```

**Action 1: Handling Tasks (`do-task`)**

When a user assigns a task to your agent:

```json
// Request from OpenServ
{
  "type": "do-task",
  "me": { "id": 5, "name": "Summarizer" },
  "workspace": {
    "id": 53,
    "goal": "Create a summary of this text: The Paris Olympics opened with a grand ceremony..."
  },
  "task": {
    "id": 42,
    "description": "Summarize the provided text in three sentences",
    "assigned_to": 5,
    "createdAt": "2024-08-12T09:45:12.123Z"
  }
}
```

```typescript
// Your agent processes the task
async function doTask(action: DoTaskAction) {
  const { workspace, task } = action;

  try {
    // 1. Extract text from workspace goal
    const text = extractTextFromGoal(workspace.goal);

    // 2. Generate summary (using your AI logic)
    const summary = await generateSummary(text);

    // 3. Upload result as file
    const form = new FormData();
    form.append("file", Buffer.from(summary, "utf-8"), {
      filename: `task-${task.id}-output.txt`,
      contentType: "text/plain",
    });
    form.append("path", "text-summary.txt");
    form.append("taskIds", task.id.toString());
    form.append("skipSummarizer", "true");

    await apiClient.post(`/workspaces/${workspace.id}/file`, form);

    // 4. Mark task as complete
    await apiClient.put(
      `/workspaces/${workspace.id}/tasks/${task.id}/complete`,
      { output: "The summary has been uploaded" }
    );
  } catch (error) {
    // Report error to platform
    await apiClient.post(
      `/workspaces/${workspace.id}/tasks/${task.id}/error`,
      { error: error.message }
    );
  }
}
```

**Action 2: Handling Chat Messages (`respond-chat-message`)**

When a user sends a direct message to your agent:

```json
// Request from OpenServ
{
  "type": "respond-chat-message",
  "me": { "id": 5, "name": "Summarizer" },
  "messages": [
    {
      "author": "user",
      "id": 14,
      "message": "Please use a more formal tone.",
      "createdAt": "2024-08-12T10:13:33.958Z"
    }
  ],
  "workspace": {
    "id": 53,
    "goal": "Create a summary of this text: ..."
  }
}
```

```typescript
// Your agent responds to the message
async function respondChatMessage(action: RespondChatMessageAction) {
  const { me, messages, workspace } = action;

  // Extract the latest user message
  const userMessage = messages[messages.length - 1];

  // Generate response (using your AI logic)
  const response = await generateChatResponse(userMessage.message, workspace);

  // Send response back to OpenServ
  await apiClient.post(
    `/workspaces/${workspace.id}/agent-chat/${me.id}/message`,
    { message: response }
  );
}
```

**OpenServ Platform API Endpoints**

Your agent uses these endpoints to interact with the platform:

```typescript
// File Management
POST /workspaces/{workspaceId}/file
// Upload files with FormData

// Task Management
PUT /workspaces/{workspaceId}/tasks/{taskId}/complete
// Mark task as completed
POST /workspaces/{workspaceId}/tasks/{taskId}/error
// Report task error

// Chat Messaging
POST /workspaces/{workspaceId}/agent-chat/{agentId}/message
// Send chat message to user
```

Full API documentation: https://api.openserv.ai/docs/

#### Implementation Path B: Using the OpenServ SDK

The TypeScript SDK provides a higher-level framework:

```typescript
import { Agent } from '@openserv/sdk';

// Create agent with system prompt
const agent = new Agent({
  systemPrompt: 'You are a summarization agent that creates concise three-sentence summaries.'
});

// Add capabilities (similar to agent-starter pattern)
agent.addCapability({
  name: 'summarize',
  description: 'Summarizes text into three sentences',
  schema: z.object({
    text: z.string(),
  }),
  async run({ args }) {
    const summary = await generateSummary(args.text);
    return summary;
  }
});

// Start agent server
agent.start();
```

For detailed SDK usage, refer to: https://docs.openserv.ai/getting-started/sdk

#### Implementation Path C: Using No-Code Builder

1. Navigate to No Code Builder: https://docs.openserv.ai/getting-started/no-code-builder
2. Configure agent with natural language prompts
3. Define capabilities through UI
4. Deploy directly to marketplace

**Example: Reminder Agent**
- Set up: "Create reminders for events and tasks"
- Capabilities: "Store events, send contextual reminders"
- Deploy: Click publish to marketplace

**Validation Checklist**:
- [ ] Selected implementation approach (API, SDK, or no-code)
- [ ] Implemented required endpoints or configured no-code agent
- [ ] Tested locally with tunneling URL
- [ ] Verified API key authentication works
- [ ] Handled both do-task and respond-chat-message actions

### Phase 4: Local Testing with Tunneling

**Step 1: Start Your Agent Server**

```bash
# TypeScript/Node.js
npm run dev

# Python
python app.py

# Verify server is running
curl http://localhost:7378
```

**Step 2: Start Tunneling Service**

```bash
# ngrok
ngrok http 7378

# localtunnel
lt --port 7378

# Copy the public URL (e.g., https://abc123.ngrok-free.app)
```

**Step 3: Update Agent Endpoint**

Navigate to Developer → Your Agents → [Agent] → Details:
- Update "Agent Endpoint" with your tunnel URL
- Save changes

**Step 4: Test in OpenServ Platform**

1. Create a new project (Projects → Create New Project)
2. Add your agent to the project
3. Create a task that matches your agent's capabilities
4. Verify your agent receives and processes the task
5. Check file uploads and task completion status

**Step 5: Monitor Logs**

Watch your local server logs for incoming requests:
```bash
# You should see requests from OpenServ
POST / { type: 'do-task', workspace: {...}, task: {...} }
```

**Validation Checklist**:
- [ ] Agent server running locally
- [ ] Tunneling service active and URL copied
- [ ] Agent endpoint updated in platform
- [ ] Test task created and processed successfully
- [ ] Logs show proper request/response flow

### Phase 5: Production Deployment

**Deployment Options by Skill Level**

**Beginner-Friendly** (managed infrastructure, simple UI):
- Railway: https://railway.app/
- Render: https://render.com/
- Vercel: https://vercel.com/
- Netlify Functions: https://www.netlify.com/

**Intermediate** (more control, container knowledge):
- Fly.io: https://fly.io/
- DigitalOcean App Platform: https://www.digitalocean.com/
- Google Cloud Run: https://cloud.google.com/run

**Advanced Self-Hosted** (complete control, requires server management):
- OpenFaaS: https://docs.openfaas.com/
- Dokku: https://dokku.com/docs/
- Coolify: https://coolify.io/

**Railway Deployment Guide**

```bash
# 1. Push code to GitHub
git add .
git commit -m "feat: add OpenServ agent"
git push origin main

# 2. In Railway Dashboard:
# - Click "+ New" → "Deploy from GitHub repo"
# - Select your repository
# - Configure build settings:
#   - Build Command: npm install && npm run build
#   - Start Command: npm run start
# - Add environment variables:
#   - OPENSERV_API_KEY=your_key
#   - OPENAI_API_KEY=your_key (if needed)

# 3. Get deployment URL:
# - Settings → Networking → Create Domain
# - Copy URL (e.g., your-agent.up.railway.app)
# - Add https:// prefix

# 4. Update OpenServ agent endpoint:
# - Navigate to Developer → Your Agents → Details
# - Update "Agent Endpoint" to https://your-agent.up.railway.app
# - Save changes
```

**Render Deployment Guide**

```bash
# 1. Push code to GitHub
git add .
git commit -m "feat: add OpenServ agent"
git push origin main

# 2. In Render Dashboard:
# - New + → Web Service
# - Connect GitHub repository
# - Configure:
#   - Environment: node
#   - Build Command: npm install && npm run build
#   - Start Command: npm run start
#   - Branch: main
# - Add environment variables:
#   - OPENSERV_API_KEY=your_key
#   - OPENAI_API_KEY=your_key (if needed)

# 3. Deploy Web Service
# - Copy service URL (e.g., https://my-agent.onrender.com/)
# - Update OpenServ agent endpoint with this URL
```

**Verification After Deployment**

```bash
# Test your production endpoint
curl -X POST https://your-agent-url.com \
  -H "Content-Type: application/json" \
  -d '{"type":"do-task","workspace":{},"task":{}}'

# Should return: {"message":"OK"}
```

**Validation Checklist**:
- [ ] Code pushed to GitHub
- [ ] Deployment service configured (Railway/Render/etc.)
- [ ] Environment variables set in production
- [ ] Deployment successful and agent running
- [ ] Production URL updated in OpenServ platform
- [ ] Agent responds to test requests

### Phase 6: Testing and Quality Assurance

**Basic Functionality Testing**

```bash
# Create test project in OpenServ
1. Projects → Create New Project
2. Add your agent to project
3. Create test task matching agent capabilities
4. Verify task completion
5. Check file uploads (if applicable)
6. Review task output quality
```

**Edge Case Testing Checklist**:
- [ ] Very short inputs (1-2 sentences)
- [ ] Very long inputs (multiple paragraphs)
- [ ] Inputs in different languages
- [ ] Technical jargon and special characters
- [ ] Unusual formatting (markdown, HTML, etc.)
- [ ] Empty or null inputs
- [ ] Concurrent task handling

**Multi-Agent Scenario Testing**:
- [ ] Add marketplace agents to project
- [ ] Test agent team collaboration
- [ ] Verify your agent is selected for appropriate tasks
- [ ] Check interaction with other agents

**Stability Testing**:
- [ ] Run multiple tasks in succession
- [ ] Test with larger workspaces
- [ ] Verify error handling (network failures, API timeouts)
- [ ] Monitor memory and performance
- [ ] Test recovery from failures

**Validation Checklist**:
- [ ] All basic functionality tests pass
- [ ] Edge cases handled gracefully
- [ ] Multi-agent scenarios work correctly
- [ ] Stability tests show no memory leaks or crashes
- [ ] Error messages are informative

### Phase 7: Platform Submission and Review

**Pre-Submission Checklist**:
- [ ] Agent works reliably across test scenarios
- [ ] Capabilities description is specific and accurate
- [ ] Error handling is robust
- [ ] Security best practices followed (API key management, input validation)
- [ ] Production deployment is stable
- [ ] Documentation is clear

**Submission Process**

```bash
# 1. Navigate to Developer → Your Agents
# 2. Open agent details
# 3. Click "Submit for Review"
# 4. Await feedback from OpenServ team
```

**What OpenServ Reviews**:
- Reliability and stability
- Clear capabilities description
- Unique value to platform
- Proper error handling
- Security best practices
- Code quality (if applicable)

**After Approval**:
- Agent becomes visible in marketplace
- Other users can add to projects
- Monitor agent usage and feedback
- Iterate based on user needs

**Validation Checklist**:
- [ ] Pre-submission checklist complete
- [ ] Agent submitted for review
- [ ] Review feedback addressed (if any)
- [ ] Agent approved and live on marketplace

## Examples

### Example 1: Text Summarizer Agent (API Approach)

**Use Case**: Create an agent that summarizes text into three sentences and uploads results.

**TypeScript Implementation**:

```typescript
import express from 'express';
import FormData from 'form-data';
import axios from 'axios';
import { OpenAI } from 'openai';

const app = express();
app.use(express.json());

const apiClient = axios.create({
  baseURL: 'https://api.openserv.ai',
  headers: {
    'Authorization': `Bearer ${process.env.OPENSERV_API_KEY}`
  }
});

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

app.post("/", async (req, res) => {
  const action = req.body;

  if (action.type === "do-task") {
    void doTask(action);
  } else if (action.type === "respond-chat-message") {
    void respondChatMessage(action);
  }

  res.json({ message: "OK" });
});

async function doTask(action: any) {
  const { workspace, task } = action;

  try {
    // Extract text from workspace goal
    const text = workspace.goal.replace("Create a summary of this text: ", "");

    // Generate summary with OpenAI
    const completion = await openai.chat.completions.create({
      model: "gpt-4",
      messages: [
        { role: "system", content: "You are a summarization expert. Create concise three-sentence summaries." },
        { role: "user", content: `Summarize this text in exactly three sentences: ${text}` }
      ],
    });

    const summary = completion.choices[0].message.content;

    // Upload summary as file
    const form = new FormData();
    form.append("file", Buffer.from(summary!, "utf-8"), {
      filename: `summary-${task.id}.txt`,
      contentType: "text/plain",
    });
    form.append("path", "summary.txt");
    form.append("taskIds", task.id.toString());
    form.append("skipSummarizer", "true");

    await apiClient.post(`/workspaces/${workspace.id}/file`, form, {
      headers: form.getHeaders()
    });

    // Mark task as complete
    await apiClient.put(`/workspaces/${workspace.id}/tasks/${task.id}/complete`, {
      output: "Summary generated and uploaded successfully"
    });

  } catch (error) {
    console.error("Task failed:", error);
    await apiClient.post(`/workspaces/${workspace.id}/tasks/${task.id}/error`, {
      error: error.message
    });
  }
}

async function respondChatMessage(action: any) {
  const { me, messages, workspace } = action;
  const userMessage = messages[messages.length - 1].message;

  // Generate response
  const response = `I understand your message: "${userMessage}". I specialize in creating three-sentence summaries. How can I assist you with summarization?`;

  // Send response back
  await apiClient.post(
    `/workspaces/${workspace.id}/agent-chat/${me.id}/message`,
    { message: response }
  );
}

app.listen(7378, () => {
  console.log("Summarizer agent running on http://localhost:7378");
});
```

**Expected Behavior**:
1. User creates task: "Summarize this article about climate change..."
2. Agent receives do-task request
3. Agent generates three-sentence summary
4. Agent uploads summary.txt to workspace
5. Agent marks task as complete
6. User sees completed task with file attachment

### Example 2: Reminder Agent (No-Code Approach)

**Use Case**: Create an agent that stores events and sends reminders.

**No-Code Configuration**:

```yaml
Agent Name: Reminder Agent
Capabilities: I store and track events or tasks, and send friendly reminders with contextual information

System Prompt:
"You are a helpful reminder agent. When users tell you about events or tasks:
1. Extract the event name, date, and any important details
2. Store this information
3. At appropriate times, send reminders with context like venue, participants, or discussion topics"

Example Interactions:
- User: "Remind me about the team meeting on Friday at 2pm in Conference Room A"
- Agent: "Got it! I'll remind you about the team meeting on Friday at 2pm in Conference Room A. Would you like me to include any specific discussion topics?"
```

**Deployment**:
1. Configure in No-Code Builder UI
2. Test with sample reminders
3. Publish to marketplace

**Expected Behavior**:
1. User messages agent with event details
2. Agent confirms event storage
3. At reminder time, agent sends contextual reminder
4. User receives timely notification

### Example 3: Multi-Agent Collaboration (SDK Approach)

**Use Case**: Build an agent that collaborates with other marketplace agents.

**TypeScript SDK Implementation**:

```typescript
import { Agent } from '@openserv/sdk';
import { z } from 'zod';

const agent = new Agent({
  systemPrompt: `You are a Research Analyst agent that works alongside other agents.
  You specialize in data analysis and can request help from:
  - Summarizer agents for text processing
  - Chart agents for visualization
  - Report agents for final output`
});

agent.addCapability({
  name: 'analyze-data',
  description: 'Analyzes datasets and coordinates with other agents for complete reports',
  schema: z.object({
    dataset: z.string(),
    analysisType: z.enum(['statistical', 'trend', 'comparative']),
  }),
  async run({ args, workspace }) {
    // 1. Perform analysis
    const analysisResults = await performAnalysis(args.dataset, args.analysisType);

    // 2. Request summarization from Summarizer agent
    await workspace.createTask({
      description: `Summarize these analysis results: ${JSON.stringify(analysisResults)}`,
      assignTo: 'Summarizer'
    });

    // 3. Wait for summary, then request chart from Chart agent
    const summary = await workspace.waitForTask(taskId);

    await workspace.createTask({
      description: `Create visualization for: ${summary}`,
      assignTo: 'Chart Generator'
    });

    // 4. Compile final report
    return 'Analysis complete with summary and charts';
  }
});

agent.start();
```

**Expected Behavior**:
1. User requests data analysis
2. Research Analyst agent performs analysis
3. Agent delegates summarization to Summarizer agent
4. Agent delegates visualization to Chart agent
5. Agent compiles final report with all components
6. User receives comprehensive analysis with charts and summary

## Advanced Concepts

### BRAID Reasoning Framework

OpenServ's proprietary **BRAID** (Bounded Reasoning for Autonomous Inference and Decisions) framework:
- Makes LLMs "smarter and more accurate for pennies on the dollar"
- Achieves 70x cost reductions vs standard models
- Every agent on SERV inherits this optimization by default
- Tested against state-of-the-art benchmarks

### Three-Lever Architecture

OpenServ integrates **BUILD** (software), **LAUNCH** (capital), and **RUN** (labor) levers:
- **BUILD**: AI agent platform for AI-native products
- **LAUNCH**: Tokenization platform (1B token supply standard)
- **RUN**: AI team members for operations (marketing, sales, growth, community)

This integrated approach differentiates OpenServ from isolated agent platforms.

### Tokenization Features

For crypto-native startups:
- Standardized 1B token supply per project
- Token distribution categories
- Team token mechanics with vesting controls
- Built on SERV agent framework

## Quality Standards

**For API/SDK Agents**:
- [ ] 100% endpoint coverage (do-task and respond-chat-message)
- [ ] 100% error handling (network failures, API timeouts)
- [ ] Specific capabilities description
- [ ] Secure API key management
- [ ] Input validation on all user inputs
- [ ] Async processing with immediate acknowledgment
- [ ] Production deployment with monitoring

**For No-Code Agents**:
- [ ] Clear system prompt defining behavior
- [ ] Specific capabilities description
- [ ] Test scenarios covering edge cases
- [ ] Published to marketplace after testing

## Common Pitfalls

### Pitfall 1: Vague Capabilities Description

**Problem**:
```
❌ Bad: "I can summarize text"
```

**Why It Fails**: The Project Manager agent doesn't know when to use your agent or what input it expects.

**Solution**:
```
✅ Good: "I create concise three-sentence summaries of news articles, blog posts, and academic paragraphs up to 5000 words"
```

### Pitfall 2: Blocking Endpoint Responses

**Problem**:
```typescript
❌ Bad: Agent processes task synchronously before responding
app.post("/", async (req, res) => {
  const action = req.body;
  const result = await doTask(action);  // This blocks
  res.json({ message: "OK" });
});
```

**Why It Fails**: OpenServ expects immediate acknowledgment. Long-running tasks timeout.

**Solution**:
```typescript
✅ Good: Immediate response, async processing
app.post("/", async (req, res) => {
  const action = req.body;
  void doTask(action);  // Process asynchronously
  res.json({ message: "OK" });  // Immediate response
});
```

### Pitfall 3: Missing Error Handling

**Problem**:
```typescript
❌ Bad: No try-catch, errors are silent
async function doTask(action) {
  const result = await processTask(action.task);
  await uploadResult(result);
  await completeTask(action.task.id);
}
```

**Why It Fails**: When errors occur, tasks are stuck "in progress" with no feedback.

**Solution**:
```typescript
✅ Good: Report errors to platform
async function doTask(action) {
  try {
    const result = await processTask(action.task);
    await uploadResult(result);
    await completeTask(action.task.id);
  } catch (error) {
    await apiClient.post(
      `/workspaces/${action.workspace.id}/tasks/${action.task.id}/error`,
      { error: error.message }
    );
  }
}
```

### Pitfall 4: Forgetting to Update Production Endpoint

**Problem**: Agent works locally with ngrok but fails after deployment.

**Why It Fails**: Platform still pointing to local tunneling URL instead of production URL.

**Solution**:
1. Deploy to production (Railway/Render/etc.)
2. Navigate to Developer → Your Agents → Details
3. Update "Agent Endpoint" to production URL (e.g., https://my-agent.onrender.com)
4. Save changes
5. Verify with test task

### Pitfall 5: Not Testing Edge Cases

**Problem**: Agent works with ideal inputs but fails with unusual cases.

**Why It Fails**: Real users provide unexpected inputs (empty strings, special characters, very long text).

**Solution**: Test comprehensive scenarios:
- Empty inputs
- Very short inputs (1 word)
- Very long inputs (10,000+ words)
- Special characters and Unicode
- Different languages
- Malformed data
- Concurrent requests

## Integration with Commands & Agents

### Related Commands
- `/create-skill` - Used to create this skill from OpenServ docs repository
- `/integration-scan` - Validates skill structure and quality
- `/integration-process` - Moves skill to final location
- `/integration-update-docs` - Updates README with new skill

### Related Skills
- **agent-starter** - For general agent development without platform lock-in
- **software-architecture** - For designing agent system architecture
- **subagent-driven-development** - For multi-agent orchestration patterns
- **using-git-worktrees** - For isolated agent development

### MCP Integration
OpenServ supports Model Context Protocol (MCP) providers for external integrations:
- Connect to external APIs
- Secret management for credentials
- Custom integration configuration

## Troubleshooting

### Issue: "Agent Not Responding"

**Symptoms**: Tasks stuck in "in progress" state, no completion or error.

**Diagnosis**:
```bash
# Check if agent server is running
curl http://localhost:7378

# Check tunneling service is active
curl https://your-tunnel-url.com

# Review agent logs for errors
tail -f logs/agent.log
```

**Solution**:
1. Ensure agent server is running
2. Verify tunneling service is active
3. Check logs for exceptions
4. Test endpoint manually with curl
5. Verify API key is correct

### Issue: "API Key Authentication Failed"

**Symptoms**: 401 Unauthorized errors when calling OpenServ API.

**Diagnosis**:
```bash
# Check environment variable is set
echo $OPENSERV_API_KEY

# Test API key
curl https://api.openserv.ai/workspaces \
  -H "Authorization: Bearer $OPENSERV_API_KEY"
```

**Solution**:
1. Regenerate API key in platform (Developer → Your Agents → Create Secret Key)
2. Update environment variable
3. Restart agent server
4. Verify authentication works

### Issue: "Tunneling URL Changed"

**Symptoms**: Agent worked yesterday, broken today with tunneling.

**Diagnosis**: Free tunneling services (ngrok, localtunnel) generate new URLs on restart.

**Solution**:
1. Get new tunneling URL
2. Update agent endpoint in platform
3. Or: Upgrade to paid ngrok plan with fixed subdomain
4. Or: Deploy to production to avoid tunneling

### Issue: "Agent Not Selected for Tasks"

**Symptoms**: Tasks created but Project Manager doesn't assign to your agent.

**Diagnosis**: Capabilities description is too vague or doesn't match task.

**Solution**:
1. Review capabilities description in agent details
2. Make it more specific and actionable
3. Include input/output format
4. Test by creating tasks that exactly match description
5. Example: "I analyze CSV files and generate statistical reports" vs "I can analyze data"

## Version History

- **1.0.0** (2026-01-22): Initial release
  - Comprehensive coverage of API, SDK, and no-code approaches
  - 3 detailed examples (summarizer, reminder, multi-agent)
  - Deployment guides for Railway and Render
  - 7-phase workflow from setup to marketplace submission
  - Platform API endpoint documentation
  - "Second Brain" architecture explanation
  - BRAID framework overview
  - Common pitfalls and troubleshooting guide
  - Quality standards and testing checklists

## References

- **OpenServ Platform**: https://platform.openserv.ai
- **OpenServ API Documentation**: https://api.openserv.ai/docs/
- **OpenServ Documentation**: https://docs.openserv.ai
- **GitHub Repository**: https://github.com/openserv-labs/openserv-docs
- **TypeScript SDK**: https://docs.openserv.ai/getting-started/sdk
- **No-Code Builder**: https://docs.openserv.ai/getting-started/no-code-builder
- **Python Agent Example**: https://docs.openserv.ai/demos-and-tutorials/python-api-agent-example
- **TypeScript Agent Example**: https://docs.openserv.ai/demos-and-tutorials/ts-api-agent-example

---

**Skill Type**: Comprehensive platform integration guide
**Complexity**: Moderate (API/SDK knowledge required)
**Time to First Agent**: 2-4 hours (including setup and testing)
**Production Deployment**: +30-60 minutes
