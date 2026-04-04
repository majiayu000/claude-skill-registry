---
name: agent-tuning
description: Optimize ElevenLabs conversational AI agents for real estate applications. Use when creating new agents, improving conversation quality, selecting voices, engineering system prompts, configuring agent parameters, or analyzing agent performance metrics. Includes voice selection, model tuning, prompt engineering, and A/B testing strategies.
allowed-tools: Read, Write, Edit, Glob, Grep, WebSearch, WebFetch
---

# Agent Tuning Skill

Expert guidance for optimizing ElevenLabs Conversational AI agents for **Next Level Real Estate** platform. This skill provides systematic approaches to agent configuration, performance optimization, and continuous improvement.

## When to Use This Skill

Invoke this skill when you need to:
- ✅ Create a new conversational AI agent
- ✅ Select the optimal voice for an agent
- ✅ Craft or improve system prompts
- ✅ Configure agent parameters (latency, turn-taking, language)
- ✅ Design conversation flows for real estate use cases
- ✅ Set up A/B testing for agent optimization
- ✅ Analyze agent performance and identify improvements
- ✅ Update knowledge bases with successful patterns

## Agent Configuration Framework

### 1. Define Agent Purpose

Every agent needs a clear, specific purpose:

**Good Examples:**
- "Qualify wholesale leads within 3 minutes by assessing motivation, timeline, and property condition"
- "Follow up with warm leads who haven't responded in 7 days, re-engage and schedule viewing"
- "Conduct market research calls to gather intel on neighborhood pricing and seller motivations"

**Bad Examples:**
- "Talk to leads" (too vague)
- "Do real estate stuff" (no clear objective)
- "Help with sales" (not specific enough)

**Template:**
```
Purpose: [Action] [Target] within [Timeframe] by [Method]
Success Criteria: [Measurable outcome]
```

### 2. Voice Selection Process

Follow this systematic approach:

#### Step 1: List Available Voices
```bash
# Use MCP tool to browse voices
Use mcp__elevenlabs__elevenlabs_list_voices with filters:
{
  "category": "professional",
  "availableForTts": true
}
```

#### Step 2: Filter by Characteristics

**For Real Estate Wholesale:**
- **Tone**: Professional, warm, trustworthy
- **Pace**: Moderate (not too fast, not too slow)
- **Accent**: Match target market (American, British, etc.)
- **Gender**: Test both male and female voices with A/B

**Voice Categories:**
- `professional` - Business calls, formal tone
- `conversational` - Warm, friendly interactions
- `narrative` - Storytelling, explanatory calls

#### Step 3: Preview Top Candidates

```bash
# Get voice details with preview URL
Use mcp__elevenlabs__elevenlabs_get_voice with:
{
  "voiceId": "candidate_voice_id"
}
```

Listen to preview URLs and rate on:
- Clarity (1-10)
- Warmth (1-10)
- Professionalism (1-10)
- Energy level (1-10)

#### Step 4: Test with Sample Script

Create a test agent with your top 3 voices and run sample conversations. Compare:
- User comfort level
- Conversation naturalness
- Response appropriateness

**Recommended Voices for Real Estate:**
- Professional female: `21m00Tcm4TlvDq8ikWAM` (Rachel)
- Professional male: `ErXwobaYiN019PkySvjV` (Antoni)
- Conversational: `EXAVITQu4vr4xnSDxMaL` (Bella)

### 3. Model Selection

Choose based on use case requirements:

| Model | Latency | Languages | Best For | Cost |
|-------|---------|-----------|----------|------|
| **eleven_flash_v2_5** | 75ms | 32 | Real-time calls, quick responses | Low |
| **eleven_turbo_v2_5** | 120ms | 32 | Balanced quality/speed | Medium |
| **eleven_multilingual_v2** | 200ms | 29 | High-quality, multi-language | High |

**Recommendation for Real Estate:**
Always start with `eleven_flash_v2_5` - the 75ms latency is critical for natural conversation flow.

### 4. System Prompt Engineering

#### Prompt Structure Template

```
You are [role/identity] working for [company].

OBJECTIVE:
[Primary goal in one sentence]

CONVERSATION APPROACH:
1. [Step 1]
2. [Step 2]
3. [Step 3]

KEY INFORMATION TO GATHER:
- [Data point 1]
- [Data point 2]
- [Data point 3]

CONVERSATION GUIDELINES:
- Be [tone: warm/professional/friendly]
- Keep responses [length: brief/moderate/detailed]
- Listen for [signal 1], [signal 2]
- Adapt to [condition]

WHAT NOT TO DO:
- Don't [unwanted behavior 1]
- Avoid [unwanted behavior 2]
- Never [critical constraint]

SUCCESS CRITERIA:
[Measurable outcome that defines success]
```

#### Real Estate Example: Lead Qualifier

```
You are Sarah, a professional real estate investor representative working for Next Level Real Estate.

OBJECTIVE:
Qualify motivated sellers within 3 minutes by assessing their situation, timeline, and property details.

CONVERSATION APPROACH:
1. Warm greeting acknowledging their inquiry
2. Confirm they're interested in selling quickly
3. Ask about motivation (probate, foreclosure, relocation, etc.)
4. Gather property basics (address, condition, estimated value)
5. Assess timeline urgency (days, weeks, months)
6. Explain next steps and schedule viewing if qualified

KEY INFORMATION TO GATHER:
- Seller motivation (why selling)
- Property address and type
- Condition (repairs needed?)
- Timeline (how soon)
- Estimated value or recent comps
- Existing liens or mortgages

CONVERSATION GUIDELINES:
- Be empathetic and professional
- Keep responses brief (2-3 sentences max)
- Listen for urgency signals (probate, foreclosure, "need to sell fast")
- Build trust before asking financial details
- Mirror their energy level
- Use their name naturally

WHAT NOT TO DO:
- Don't pressure or use aggressive sales tactics
- Avoid real estate jargon unless they use it first
- Never make promises about specific offers
- Don't ask about finances until trust is established
- Avoid talking over them or interrupting

SUCCESS CRITERIA:
Qualified lead with complete contact info, property address, condition assessment, and scheduled viewing appointment within 48 hours.
```

### 5. Parameter Configuration

#### Critical Parameters

```javascript
{
  // Model & Voice
  "modelId": "eleven_flash_v2_5",
  "voiceId": "21m00Tcm4TlvDq8ikWAM",

  // Conversation Quality
  "interruptionSensitivity": "high",  // high = more natural turn-taking
  "responseLatency": 75,              // milliseconds, 75 is minimum

  // Language
  "language": "en",
  "supportedLanguages": ["en", "es"], // Add Spanish for broader reach
  "autoDetectLanguage": true,         // Auto-switch mid-conversation

  // Compliance
  "tcpaCompliance": true,             // MANDATORY for TCPA 2025
  "recordingConsent": true,           // Disclose recording at start

  // Conversation Control
  "maxDuration": 300,                 // 5 minutes max
  "greeting": "[Your greeting]",
  "firstMessage": "[Opening line]"
}
```

#### Parameter Tuning Guide

**Interruption Sensitivity:**
- `low` - Agent waits longer, fewer interruptions (use for formal/structured)
- `medium` - Balanced turn-taking
- `high` - More natural, human-like interruptions (RECOMMENDED for sales)

**Response Latency:**
- 75ms - Minimum, feels instant (RECOMMENDED)
- 100-150ms - Slightly delayed but acceptable
- 200ms+ - Noticeable lag, avoid for sales calls

**Max Duration:**
- Lead qualification: 180-300s (3-5 minutes)
- Market research: 300-600s (5-10 minutes)
- Follow-up: 120-180s (2-3 minutes)

### 6. Knowledge Base Integration

#### Document Preparation

1. **Create Knowledge Documents**
   - Market trends and comparables
   - Successful objection handling scripts
   - Property valuation guidelines
   - Common seller FAQs with answers

2. **Format for RAG**
   ```markdown
   # Topic Title

   ## Key Points
   - Point 1
   - Point 2

   ## When to Use
   [Context for when this information is relevant]

   ## Examples
   [Concrete examples of application]
   ```

3. **Reference in Agent Config**
   ```javascript
   {
     "knowledgeBase": [
       "kb://market-trends-2025",
       "kb://objection-handling",
       "kb://valuation-guide"
     ]
   }
   ```

#### Knowledge Base Best Practices

- **Keep documents focused** - One topic per document
- **Update regularly** - Feed successful call patterns back
- **Include examples** - Show, don't just tell
- **Version control** - Track what changed and when
- **Test references** - Ensure agent can access and use knowledge

## Conversation Flow Design

### Lead Qualification Flow

```
1. GREETING (5-10 seconds)
   "Hi [Name], this is Sarah from Next Level Real Estate.
    I saw you inquired about selling your property. How are you today?"

2. CONFIRM INTENT (10-15 seconds)
   "Great! Are you still interested in exploring your options for [Address]?"

3. ASSESS MOTIVATION (30-45 seconds)
   "What's prompting you to consider selling at this time?"
   [Listen for: probate, foreclosure, relocation, downsizing, repairs]

4. GATHER PROPERTY INFO (45-60 seconds)
   "Tell me a bit about the property - what condition is it in?"
   "Do you have a sense of what it might be worth?"

5. ESTABLISH TIMELINE (20-30 seconds)
   "How soon are you looking to make a move on this?"

6. QUALIFY & NEXT STEPS (30-45 seconds)
   "Based on what you've shared, I think we can definitely help.
    Would you be available for a quick property viewing [tomorrow/this week]?"

7. CLOSE (10-15 seconds)
   "Perfect! You'll receive a confirmation text shortly.
    Looking forward to meeting you!"

Total: ~3 minutes
```

### Error Recovery Patterns

Handle common conversation breakdowns:

```javascript
// User confusion
IF user says "What?" OR "I don't understand"
  THEN rephrase last question more simply

// Objection
IF user expresses concern OR resistance
  THEN acknowledge concern, provide reassurance, continue

// Off-topic
IF user goes off-topic for >30 seconds
  THEN gently redirect: "I understand, and just to make sure
       I have the key details about your property..."

// Technical issues
IF audio problems OR long silence
  THEN check connection: "Are you still there? I think we might
       have had a brief connection issue."
```

## A/B Testing Framework

### Test Design

```javascript
// Control Agent (A)
{
  "name": "Lead Qualifier Control",
  "greeting": "Hi, this is Sarah from Next Level Real Estate...",
  "systemPrompt": "[Original prompt]"
}

// Variant Agent (B)
{
  "name": "Lead Qualifier Variant",
  "greeting": "Hey there! This is Sarah calling from Next Level...",
  "systemPrompt": "[Modified prompt with different approach]"
}
```

### What to Test

1. **Greeting variations**
   - Formal vs. casual tone
   - Company name placement
   - Length (short vs. detailed)

2. **Question ordering**
   - Motivation first vs. property details first
   - Timeline early vs. timeline late

3. **Voice characteristics**
   - Male vs. female
   - Different accents
   - Different energy levels

4. **System prompt approaches**
   - Consultative vs. direct
   - Question-based vs. statement-based
   - More guidance vs. less guidance

### Metrics to Track

```javascript
// Per Agent
{
  "connectRate": 0.75,        // % calls reaching person
  "avgDuration": 187,         // seconds
  "completionRate": 0.82,     // % reaching conversation goal
  "qualificationRate": 0.45,  // % leads qualified
  "sentimentPositive": 0.68,  // % positive sentiment
  "viewingsScheduled": 0.38   // % scheduling viewing
}
```

### Statistical Significance

- Run each variant for at least 50 calls
- Aim for 95% confidence interval
- Use tools like [AB Test Calculator](https://www.abtestguide.com/calc/)

## Performance Analysis

### Key Performance Indicators (KPIs)

```markdown
## Agent Performance Report

**Agent Name:** Lead Qualifier v2.1
**Period:** March 1-15, 2025
**Total Calls:** 247

### Call Metrics
- Connect Rate: 78% (193/247)
- Avg Duration: 3m 42s
- Completion Rate: 84% (162/193)

### Conversation Quality
- Sentiment Distribution:
  - Positive: 71% (137/193)
  - Neutral: 22% (42/193)
  - Negative: 7% (14/193)

### Business Outcomes
- Leads Qualified: 89 (46% of connected calls)
- Viewings Scheduled: 67 (35% of connected calls)
- Cost per Qualified Lead: $3.45

### Top Performing Elements
1. Opening greeting with property address mention
2. Empathy statements during motivation discussion
3. Flexible viewing scheduling approach

### Improvement Opportunities
1. Reduce negative sentiment calls (current 7%, target <5%)
2. Increase qualification rate (current 46%, target 50%)
3. Optimize for calls <3 minutes (faster = more calls/hour)
```

### Transcript Analysis

Use this checklist when reviewing transcripts:

```markdown
## Transcript Review Checklist

### Conversation Flow
- [ ] Greeting was warm and professional
- [ ] Intent confirmation was clear
- [ ] Questions were open-ended
- [ ] Agent listened before responding
- [ ] Natural transitions between topics

### Content Quality
- [ ] All required info gathered
- [ ] Agent handled objections well
- [ ] Context was properly used
- [ ] No compliance violations
- [ ] Clear next steps provided

### Technical Quality
- [ ] No awkward pauses >3 seconds
- [ ] Appropriate turn-taking
- [ ] No audio issues
- [ ] Response latency acceptable
- [ ] Voice quality maintained

### Optimization Notes
[What worked well?]
[What could be improved?]
[Patterns to extract for knowledge base?]
```

## Common Issues & Solutions

| Issue | Symptoms | Root Cause | Solution |
|-------|----------|------------|----------|
| Robotic conversation | Lacks warmth, sounds scripted | System prompt too rigid | Add personality, use conversational language |
| Slow responses | >500ms latency | Wrong model or overloaded system | Switch to Flash 2.5, reduce prompt length |
| Poor listening | Interrupts frequently | Sensitivity too low | Increase interruptionSensitivity to "high" |
| Misses context | Doesn't use lead data | Context not injected properly | Verify context format in start_conversation |
| Off-topic | Strays from objective | Prompt lacks constraints | Add "WHAT NOT TO DO" section to prompt |
| Low completion | Calls drop before goal | Too long or unclear objective | Reduce maxDuration, simplify goal |

## Optimization Workflow

### 1. Baseline Measurement (Week 1)
- Deploy agent with initial configuration
- Run 50-100 calls
- Measure all KPIs
- Analyze transcripts
- Identify top 3 issues

### 2. Hypothesis Formation (Week 2)
- Select ONE variable to test
- Form hypothesis: "If we change X, then Y will improve by Z%"
- Create variant agent
- Define success metrics

### 3. A/B Testing (Weeks 3-4)
- Run both agents in parallel
- Collect data for 100+ calls per variant
- Compare metrics
- Validate statistical significance

### 4. Implementation (Week 5)
- Deploy winning variant to production
- Update knowledge base with learnings
- Document what worked and why
- Plan next optimization cycle

### 5. Continuous Monitoring (Ongoing)
- Track KPIs daily
- Review transcripts weekly
- Update prompts monthly
- Refresh voices quarterly

## Advanced Techniques

### Dynamic Prompt Injection

Customize system prompt based on lead characteristics:

```javascript
// Base prompt
const basePrompt = "You are Sarah, a real estate professional..."

// Add-ons based on context
if (leadData.motivation === "probate") {
  basePrompt += "\n\nNOTE: This seller is dealing with probate.
                 Be extra empathetic about the loss and complex process."
}

if (propertyInfo.condition === "poor") {
  basePrompt += "\n\nNOTE: Property needs significant repairs.
                 Emphasize our as-is purchase capability."
}
```

### Sentiment-Driven Adaptation

Adjust agent behavior based on real-time sentiment:

```javascript
// In agent logic (future capability)
if (currentSentiment === "negative") {
  // Slow down, be more empathetic
  // Avoid pushy questions
  // Offer to call back later
}

if (currentSentiment === "positive") {
  // Maintain energy
  // Move toward scheduling
  // Confirm next steps clearly
}
```

### Knowledge Base Auto-Update

Extract successful patterns automatically:

```javascript
// After call with positive sentiment and scheduled viewing
1. Extract agent responses that got positive reactions
2. Add to "successful_responses.md" knowledge base
3. Tag with context (motivation type, property condition)
4. Reference in future agents
```

## Resources & References

### Internal Documentation
- Main project guide: `/home/onesmartguy/projects/next-level-real-estate/CLAUDE.md`
- MCP server docs: `/home/onesmartguy/projects/next-level-real-estate/mcp-servers/mcp-elevenlabs-server/README.md`
- Agent examples: `.claude/skills/agent-tuning/examples.md`

### External Resources
- [ElevenLabs Conversational AI Best Practices](https://elevenlabs.io/docs/conversational-ai/best-practices)
- [Voice Selection Guide](https://elevenlabs.io/docs/voices)
- [Real Estate Conversation Scripts](https://www.biggerpockets.com/wholesaling)

### Research & Learning
Use WebSearch for:
- "ElevenLabs conversation optimization 2025"
- "real estate cold calling scripts that convert"
- "AI agent system prompt engineering"
- "conversation design best practices"

## Example Configurations

See [examples.md](./examples.md) for complete agent configurations including:
- Lead qualifier agent (wholesale)
- Follow-up campaign agent
- Market research agent
- Appointment setter agent
- Objection handler agent

## Success Metrics

Track these metrics to validate optimization:

### Short-term (Daily/Weekly)
- Call connect rate >75%
- Average duration 2-4 minutes
- Positive sentiment >65%
- Completion rate >80%

### Medium-term (Monthly)
- Qualification rate >45%
- Viewing scheduled rate >30%
- Cost per qualified lead <$5
- Agent uptime >99%

### Long-term (Quarterly)
- Lead-to-close rate improvement
- Revenue per call increase
- Agent configuration stability
- Knowledge base growth

---

**Remember:** Agent tuning is an iterative process. Start with a solid baseline, test one variable at a time, and continuously feed learnings back into your configuration. The best agents are constantly evolving based on real conversation data.
