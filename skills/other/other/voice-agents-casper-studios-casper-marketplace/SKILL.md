---
name: voice-agents
description: ElevenLabs voice agent creation for client discovery and feedback calls. Use this skill when creating AI voice agents, setting up discovery call agents, or configuring automated phone conversations. Triggers on voice agent creation, ElevenLabs agent setup, or automated call agent requests.
---

# Voice Agents

## Overview

Create ElevenLabs Conversational AI voice agents for client discovery, feedback, and check-in calls. Automatically generates agent configuration from client context.

## Quick Decision Tree

```
What type of agent?
│
├── Discovery agent (interview clients)
│   └── --scope discovery
│
├── Feedback agent (post-project)
│   └── --scope feedback
│
├── Check-in agent (relationship)
│   └── --scope check-in
│
├── Qualification agent (leads)
│   └── --scope qualification
│
└── Onboarding agent (new contacts)
    └── --scope onboarding
```

## Environment Setup

```bash
# Required in .env
ELEVENLABS_API_KEY=your_api_key
OPENROUTER_API_KEY=your_api_key  # For prompt generation
```

## Common Usage

### Create Discovery Agent
```bash
python scripts/create_voice_agent.py "Microsoft" --scope discovery --notes "CRM migration project"
```

### Create Feedback Agent
```bash
python scripts/create_voice_agent.py "Acme Corp" --scope feedback --notes "Post-project review"
```

### Dry Run (Preview)
```bash
python scripts/create_voice_agent.py "Test Company" --scope discovery --notes "Testing" --dry-run
```

## Scope Types

| Scope | Purpose |
|-------|---------|
| `discovery` | Interview client team about operations, pain points, tech stack |
| `feedback` | Gather feedback on completed project |
| `check-in` | Periodic relationship check-ins |
| `qualification` | Qualify inbound leads before sales |
| `onboarding` | Guide new contacts through info gathering |

## Generated Agent Config

The script generates:

### Agent Name
`[{Company Name}] {Scope} Agent v1`

### First Message
Voice-optimized greeting that:
- Introduces as calling on behalf of Casper Studios
- Confirms speaking with right person
- States purpose aligned with scope
- Sets time expectations (10-15 minutes)
- Asks for confirmation

### System Prompt
Comprehensive conversation guide with:
- Identity and context
- Tone and communication style
- Conversation flow (5-7 stages)
- Interviewing techniques
- Guardrails and boundaries

## Output

```json
{
  "agent_id": "abc123xyz",
  "agent_name": "[Microsoft] Discovery Agent v1",
  "agent_url": "https://elevenlabs.io/app/conversational-ai/agents/abc123xyz",
  "first_message": "Hi there! This is an AI assistant...",
  "company_name": "Microsoft",
  "scope": "discovery"
}
```

## Context Enrichment

The script optionally fetches context from Google Drive:
1. Client's "Research" document
2. Previous meeting transcripts (intro calls)

If not available, generates with provided notes only.

## Cost

| Service | Cost |
|---------|------|
| OpenRouter (prompt generation) | ~$0.01-0.03 |
| ElevenLabs agent creation | Free |
| Google Drive | Free |

## Security Notes

### Credential Handling
- Store `ELEVENLABS_API_KEY` in `.env` file (never commit to git)
- Store `OPENROUTER_API_KEY` in `.env` file (never commit to git)
- Regenerate keys from respective dashboards if compromised
- Never log or print API keys in script output

### Data Privacy
- Voice agents conduct live conversations with customers
- Call content may include sensitive business discussions
- Agent prompts may contain internal business context
- Conversation logs are stored by ElevenLabs
- Client context from Google Drive may be included in prompts

### Access Scopes
- `ELEVENLABS_API_KEY` - Full access to voice agent creation/management
- `OPENROUTER_API_KEY` - AI model access for prompt generation
- Google OAuth - Optional, for client context enrichment

### Compliance Considerations
- **Recording Consent**: Inform callers that conversations may be recorded
- **AI Disclosure**: Disclose that caller is speaking with an AI agent
- **Caller Privacy**: Conversation data is processed by ElevenLabs servers
- **GDPR**: EU caller conversations require appropriate consent
- **TCPA/CCPA**: Comply with applicable telecommunications regulations
- **Call Recording Laws**: Recording laws vary by jurisdiction (one-party vs two-party consent)
- **Data Retention**: Review ElevenLabs data retention policies
- **Agent Guardrails**: Ensure agents have appropriate conversation boundaries

## Troubleshooting

### Common Issues

#### Issue: Agent creation failed
**Symptoms:** API error when creating voice agent
**Cause:** Invalid configuration, missing fields, or API issue
**Solution:**
- Validate agent config JSON format
- Ensure all required fields are present (name, first_message, system_prompt)
- Check prompt length doesn't exceed limits
- Review ElevenLabs API documentation for requirements

#### Issue: Invalid voice ID
**Symptoms:** "Voice not found" or "invalid voice_id" error
**Cause:** Voice ID doesn't exist or not accessible
**Solution:**
- Use valid ElevenLabs voice ID from your library
- Check voice availability at https://elevenlabs.io/app/voice-library
- Verify voice is not a custom voice from another account
- Use default voice if custom voice unavailable

#### Issue: API quota exceeded
**Symptoms:** "Quota exceeded" or rate limit error
**Cause:** ElevenLabs subscription limits reached
**Solution:**
- Check usage at https://elevenlabs.io/app/subscription
- Upgrade subscription tier for more capacity
- Reduce number of concurrent agents
- Delete unused agents to free up slots

#### Issue: Agent not responding in calls
**Symptoms:** Agent created but doesn't respond in conversations
**Cause:** System prompt issues, webhook configuration, or service issue
**Solution:**
- Test agent directly in ElevenLabs console first
- Review system prompt for clear instructions
- Check webhook URL is accessible (if configured)
- Verify ElevenLabs service status

#### Issue: OpenRouter prompt generation failed
**Symptoms:** Error generating agent prompt
**Cause:** OpenRouter API issue or invalid model
**Solution:**
- Verify `OPENROUTER_API_KEY` is set correctly
- Check model availability at OpenRouter
- Try a different model if current one unavailable
- Run with `--dry-run` to test without API calls

#### Issue: Google Drive context not loading
**Symptoms:** Agent created without client context
**Cause:** OAuth issue or client folder not found
**Solution:**
- Verify Google OAuth credentials (see google-workspace skill)
- Check client folder exists in expected location
- Provide context via `--notes` flag as alternative
- Run without context enrichment first to isolate issue

## Resources

- **references/elevenlabs.md** - ElevenLabs API details

## Integration Patterns

### Context-Aware Agents
**Skills:** transcript-search → voice-agents
**Use case:** Create voice agents with client history
**Flow:**
1. Search transcript-search for past client meetings
2. Extract relationship history, pain points, and preferences
3. Include context in voice agent system prompt for personalized conversations

### Agent Notes to CRM
**Skills:** voice-agents → attio-crm
**Use case:** Log voice agent call summaries
**Flow:**
1. Voice agent completes discovery or feedback call
2. Extract call summary, insights, and action items
3. Create note on Attio company record with call details

### Research-Enriched Agents
**Skills:** parallel-research → voice-agents
**Use case:** Arm voice agents with company intelligence
**Flow:**
1. Run parallel-research on target company
2. Extract recent news, funding, tech stack, and pain points
3. Include research in agent prompt for informed conversations
