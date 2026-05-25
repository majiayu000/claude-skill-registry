---
name: agent-debugging
description: Debug and troubleshoot ElevenLabs conversational AI agents and Twilio calls. Use when diagnosing agent issues, analyzing failed calls, troubleshooting audio problems, investigating conversation breakdowns, reviewing error logs, or optimizing underperforming agents. Includes transcript analysis, error diagnosis, and performance troubleshooting.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Agent Debugging Skill

Systematic debugging and troubleshooting framework for **ElevenLabs Conversational AI + Twilio** integration on the Next Level Real Estate platform. This skill provides diagnostic procedures, root cause analysis techniques, and resolution strategies.

## When to Use This Skill

Invoke this skill when you need to:
- ✅ Debug agent configuration issues
- ✅ Analyze failed or poor-quality calls
- ✅ Troubleshoot audio/latency problems
- ✅ Investigate conversation breakdowns
- ✅ Review and interpret error logs
- ✅ Diagnose context injection failures
- ✅ Identify performance bottlenecks
- ✅ Generate diagnostic reports

## Debugging Methodology

### The 5-Step Debug Process

```
1. OBSERVE   → Gather symptoms and error data
2. REPRODUCE → Confirm issue is consistent
3. ISOLATE   → Narrow down to specific component
4. DIAGNOSE  → Identify root cause
5. FIX       → Implement and verify solution
```

## Common Issues & Solutions

### Issue Category 1: Agent Configuration

#### Problem: Agent Not Starting/Responding

**Symptoms:**
- Agent status shows "inactive" or "error"
- Conversation fails to start
- No greeting heard on call
- Error: "Agent not found" or "Invalid agent ID"

**Diagnostic Steps:**

```bash
# 1. Check agent exists and is active
Use mcp__elevenlabs__elevenlabs_get_agent with:
{
  "agentId": "your_agent_id"
}

# Expected output:
# - status: "active"
# - voiceId: valid voice ID
# - modelId: valid model
# - systemPrompt: non-empty

# 2. Verify voice is valid
Use mcp__elevenlabs__elevenlabs_get_voice with:
{
  "voiceId": "voice_from_agent_config"
}

# 3. Check agent configuration file
Read .claude/agents/elevenlabs-agent-manager.md

# Look for:
# - Syntax errors in frontmatter
# - Invalid tool names
# - Malformed YAML
```

**Common Root Causes:**

| Root Cause | Symptoms | Solution |
|------------|----------|----------|
| Invalid voice ID | Agent fails to start | Use `list_voices` to find valid ID |
| Voice not available for TTS | "Voice not supported" error | Select voice with `availableForTts: true` |
| Empty system prompt | Generic/confused responses | Add detailed system prompt |
| Wrong model ID | "Model not found" error | Use: `eleven_flash_v2_5`, `eleven_turbo_v2_5`, or `eleven_multilingual_v2` |
| Agent not deployed | "Agent not found" | Re-create agent or verify agent ID |

**Fix Template:**

```typescript
// Validate and fix agent configuration
const agentConfig = {
  name: "Fixed Lead Qualifier",
  voiceId: "21m00Tcm4TlvDq8ikWAM",  // Verified valid voice
  modelId: "eleven_flash_v2_5",      // Verified valid model
  greeting: "Hi, this is Sarah from Next Level Real Estate.",
  systemPrompt: `[Complete, detailed prompt here]`,  // Non-empty
  tcpaCompliance: true,
  recordingConsent: true
}

// Create new agent with validated config
const agent = await createAgent(agentConfig)
console.log(`Agent created: ${agent.agentId}`)
```

#### Problem: Agent Gives Incorrect/Off-Topic Responses

**Symptoms:**
- Agent doesn't follow system prompt instructions
- Responses are generic or unrelated
- Agent doesn't use injected context
- Agent goes off-topic frequently

**Diagnostic Steps:**

```bash
# 1. Review agent's system prompt
Use mcp__elevenlabs__elevenlabs_get_agent to retrieve full config

# 2. Check if prompt is too vague
# BAD: "You are a helpful assistant"
# GOOD: "You are Sarah, a real estate professional. Your goal is to..."

# 3. Analyze conversation transcript
Use mcp__elevenlabs__elevenlabs_get_conversation with conversationId

# Look for:
# - Agent ignoring prompt instructions
# - Generic responses instead of specific
# - Missing context usage
```

**Root Cause Analysis:**

```markdown
## System Prompt Issues

### Too Vague
❌ "You are helpful"
✅ "You are Sarah, a wholesale real estate buyer. Qualify leads by asking about motivation, timeline, and property condition."

### Missing Constraints
❌ No "WHAT NOT TO DO" section
✅ Include explicit constraints: "DON'T discuss pricing until property details gathered"

### No Examples
❌ Abstract instructions only
✅ Include example conversations showing desired behavior

### Context Not Referenced
❌ Prompt doesn't mention lead data
✅ "You will receive lead data including name, property address, and motivation. Use these naturally."
```

**Fix:**

```typescript
// Update agent with improved prompt
await updateAgent(agentId, {
  systemPrompt: `
You are Sarah, a professional real estate investor representative for Next Level Real Estate.

OBJECTIVE:
Qualify motivated sellers in under 3 minutes by gathering property details, assessing motivation, and scheduling viewings.

CONTEXT PROVIDED:
- Lead name and contact info
- Property address
- Estimated value
- Source of inquiry

USE THIS CONTEXT NATURALLY:
"Hi [name], I'm following up on your inquiry about [address]..."

KEY QUESTIONS TO ASK:
1. "What's prompting you to consider selling?"
2. "How soon are you looking to move?"
3. "Can you describe the property's current condition?"

CONVERSATION GUIDELINES:
- Be empathetic and professional
- Listen more than you talk
- Keep responses under 2 sentences
- Build rapport before asking detailed questions

WHAT NOT TO DO:
- Don't pressure or use aggressive tactics
- Don't discuss specific offers without property viewing
- Don't ask about price until property details gathered
- Don't use jargon unless lead uses it first

SUCCESS:
Lead qualified with viewing scheduled within 48 hours.
`
})
```

### Issue Category 2: Audio & Call Quality

#### Problem: Poor Audio Quality

**Symptoms:**
- Choppy, robotic voice
- Echo or feedback
- Audio dropouts or silence
- Laggy responses (>500ms)

**Diagnostic Steps:**

```bash
# 1. Get conversation details
Use mcp__elevenlabs__elevenlabs_get_conversation with conversationId

# 2. Check transcript for issues
# Look for:
# - Multiple "What?" or "Can you repeat?" from user
# - Agent repeating itself
# - Long pauses between turns
# - Incomplete sentences

# 3. Measure response latency
# Calculate time between user speech end and agent response start
# Target: <200ms
# Acceptable: <400ms
# Poor: >500ms

# 4. Review call logs
Grep logs/calling-service.log for:
- WebSocket connection errors
- Audio buffer underruns
- Network timeout errors
```

**Root Cause Analysis:**

| Symptom | Likely Cause | Quick Test |
|---------|--------------|------------|
| Robotic voice | Wrong model or voice settings | Try different voice ID |
| High latency | Model too slow or overloaded | Switch to Flash 2.5 |
| Dropouts | Network issues | Test network bandwidth |
| Echo | Audio feedback loop | Check Twilio echo cancellation |
| Choppy | Buffer issues | Adjust jitter buffer size |

**Diagnostic Script:**

```typescript
async function diagnoseAudioQuality(conversationId: string) {
  const conversation = await getConversation(conversationId)

  // Analyze transcript timing
  const responseLatencies = []
  for (let i = 1; i < conversation.transcript.length; i++) {
    const userTurn = conversation.transcript[i - 1]
    const agentTurn = conversation.transcript[i]

    if (userTurn.role === 'user' && agentTurn.role === 'agent') {
      const latency = new Date(agentTurn.timestamp).getTime() -
                     new Date(userTurn.timestamp).getTime()
      responseLatencies.push(latency)
    }
  }

  const avgLatency = average(responseLatencies)
  const maxLatency = Math.max(...responseLatencies)

  // Count audio issues indicators
  const transcriptText = conversation.transcript
    .map(t => t.text.toLowerCase())
    .join(' ')

  const clarificationRequests = (transcriptText.match(/what\?|pardon|repeat|didn't hear/g) || []).length
  const incompleteResponses = conversation.transcript.filter(t =>
    t.text.endsWith('...') || t.text.length < 5
  ).length

  // Diagnosis
  const diagnosis = {
    avgLatency,
    maxLatency,
    clarificationRequests,
    incompleteResponses,
    quality: avgLatency < 200 ? 'excellent' :
             avgLatency < 400 ? 'good' :
             avgLatency < 600 ? 'acceptable' : 'poor',
    issues: []
  }

  if (avgLatency > 400) {
    diagnosis.issues.push('High average latency - consider switching to Flash 2.5 model')
  }

  if (maxLatency > 1000) {
    diagnosis.issues.push('Extreme latency spikes detected - check network stability')
  }

  if (clarificationRequests > 2) {
    diagnosis.issues.push('Multiple clarification requests - audio clarity issue')
  }

  if (incompleteResponses > 1) {
    diagnosis.issues.push('Incomplete responses - possible audio dropouts')
  }

  return diagnosis
}
```

**Fixes:**

```typescript
// 1. Switch to fastest model
await updateAgent(agentId, {
  modelId: "eleven_flash_v2_5",
  responseLatency: 75
})

// 2. Optimize voice settings
await updateAgent(agentId, {
  voiceSettings: {
    stability: 0.5,        // More stable = less natural but clearer
    similarityBoost: 0.75, // Higher = closer to original voice
    useSpeakerBoost: true  // Enhance clarity
  }
})

// 3. Improve network handling
// In Twilio config:
{
  codec: 'opus',              // Better quality
  jitterBufferSize: 'small',  // Reduce latency
  echoCancellation: true      // Eliminate echo
}

// 4. Reduce system prompt length
// Shorter prompts = faster processing
// Trim unnecessary details, keep core instructions
```

#### Problem: Awkward Pauses or Interruptions

**Symptoms:**
- Agent waits too long to respond
- Agent interrupts user mid-sentence
- Conversation feels unnatural
- Multiple false starts

**Diagnostic Steps:**

```bash
# 1. Review transcript for turn-taking patterns
Use mcp__elevenlabs__elevenlabs_get_conversation

# Look for:
# - Pauses >3 seconds
# - Agent responses overlapping user speech
# - User having to repeat multiple times

# 2. Check interruption sensitivity setting
Use mcp__elevenlabs__elevenlabs_get_agent

# Current setting: "interruptionSensitivity"
# - low: Agent waits longer (formal)
# - medium: Balanced
# - high: More interruptions (conversational)
```

**Fix:**

```typescript
// Adjust interruption sensitivity
await updateAgent(agentId, {
  interruptionSensitivity: "high",  // More natural for sales calls
  responseLatency: 75              // Quick responses
})

// Test with different settings and measure:
// - Average pause duration
// - Number of interruptions
// - User satisfaction (via sentiment)
```

### Issue Category 3: Context & Integration

#### Problem: Agent Not Using Lead Context

**Symptoms:**
- Agent doesn't mention lead's name
- Doesn't reference property address
- Ignores motivation or timeline info
- Generic, impersonal responses

**Diagnostic Steps:**

```bash
# 1. Verify context was sent
# Check application logs
Grep logs/calling-service.log for "context injection"

# Should see:
# "Starting conversation with context: {leadData: {...}}"

# 2. Review conversation details
Use mcp__elevenlabs__elevenlabs_get_conversation

# Check if context is in conversation metadata

# 3. Analyze transcript for context usage
# Search for lead name, property address, motivation keywords
```

**Root Cause Analysis:**

```typescript
// Common context injection mistakes:

// ❌ WRONG: Context not passed at all
await startConversation({ agentId: "abc123" })

// ❌ WRONG: Incorrect format
await startConversation({
  agentId: "abc123",
  context: "John Smith, 123 Main St"  // String instead of object
})

// ❌ WRONG: Deeply nested
await startConversation({
  agentId: "abc123",
  context: {
    lead: {
      personal: {
        name: "John"  // Too nested, hard for agent to access
      }
    }
  }
})

// ✅ CORRECT: Flat, clear structure
await startConversation({
  agentId: "abc123",
  context: {
    leadData: {
      name: "John Smith",
      phone: "+1234567890",
      motivation: "probate",
      timeline: "urgent"
    },
    propertyInfo: {
      address: "123 Main St, Austin TX",
      estimatedValue: 250000,
      condition: "needs_repairs"
    }
  }
})
```

**Fix:**

```typescript
// 1. Ensure context is properly formatted
const context = {
  leadData: {
    name: leadName,
    phone: leadPhone,
    motivation: leadMotivation,
    timeline: leadTimeline
  },
  propertyInfo: {
    address: propertyAddress,
    estimatedValue: propertyValue,
    condition: propertyCondition
  },
  strategyRules: {
    minEquity: 0.20,
    targetARV: targetARV
  }
}

// 2. Update system prompt to reference context
await updateAgent(agentId, {
  systemPrompt: `
...existing prompt...

CONTEXT PROVIDED TO YOU:
You will receive information about the lead and property:
- leadData.name: The person's name
- leadData.motivation: Why they're selling (use this to show empathy)
- leadData.timeline: How soon they need to sell
- propertyInfo.address: The property location
- propertyInfo.condition: Property state

USE THIS INFORMATION NATURALLY:
- Start with: "Hi [leadData.name], I'm calling about [propertyInfo.address]"
- Reference motivation: "I understand you're dealing with [leadData.motivation]"
- Adapt urgency based on timeline

EXAMPLE:
"Hi John, this is Sarah from Next Level Real Estate. I saw you inquired about your property at 123 Main St. I understand you're dealing with a probate situation and need to move quickly. I'd love to help..."
`
})

// 3. Verify context injection in test
const testCall = await startConversation({
  agentId: agentId,
  context: context
})

console.log('Context sent:', JSON.stringify(context, null, 2))

// 4. Check transcript
const conversation = await getConversation(testCall.conversationId)
const transcript = conversation.transcript.map(t => t.text).join(' ')

console.log('Name used:', transcript.includes(context.leadData.name))
console.log('Address mentioned:', transcript.includes(context.propertyInfo.address))
```

#### Problem: Twilio Call Connection Failures

**Symptoms:**
- Call status: "failed" or "busy"
- No audio on either end
- Call drops immediately
- Webhook not called

**Diagnostic Steps:**

```bash
# 1. Check Twilio account status
# Log into Twilio Console > Monitor > Debugger
# Look for error codes

# 2. Verify webhook is accessible
curl -X POST https://your-domain.com/twiml/test-123

# Should return 200 with valid TwiML XML

# 3. Check phone number validity
# In Twilio Console > Phone Numbers
# Verify number is active and voice-enabled

# 4. Review application logs
Grep logs/calling-service.log for:
- "Twilio error"
- "Webhook failed"
- "Connection refused"
```

**Common Error Codes:**

| Error Code | Meaning | Solution |
|------------|---------|----------|
| 11200 | HTTP retrieval failure | Check webhook URL accessibility |
| 11205 | HTTP connection failure | Verify server is running |
| 11206 | Connection refused | Check firewall rules |
| 12100 | Document parse failure | Validate TwiML XML syntax |
| 13224 | Invalid phone number | Verify "to" number format |
| 13225 | Invalid callback URL | Check webhook URL format |
| 21211 | Invalid 'To' phone number | Verify number is E.164 format |

**Fix:**

```typescript
// 1. Validate phone number format
function validatePhoneNumber(phone: string): boolean {
  // E.164 format: +[country code][number]
  const e164Regex = /^\+[1-9]\d{1,14}$/
  return e164Regex.test(phone)
}

// 2. Ensure webhook returns valid TwiML
router.post('/twiml/:conversationId', (req, res) => {
  try {
    const { conversationId } = req.params

    const twiml = new VoiceResponse()

    // Add greeting
    twiml.say({
      voice: 'alice',
      language: 'en-US'
    }, 'This call may be recorded.')

    // Connect to ElevenLabs
    const connect = twiml.connect()
    connect.stream({
      url: `wss://api.elevenlabs.io/v1/convai/${conversationId}/stream`
    })

    // CRITICAL: Set correct content type
    res.type('text/xml')
    res.send(twiml.toString())

  } catch (error) {
    console.error('TwiML generation error:', error)

    // Return error TwiML
    const errorTwiml = new VoiceResponse()
    errorTwiml.say('An error occurred. Please try again later.')
    errorTwiml.hangup()

    res.type('text/xml')
    res.send(errorTwiml.toString())
  }
})

// 3. Add retry logic
async function initiateCallWithRetry(config, maxRetries = 3) {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      const call = await twilioClient.initiateCall(config)
      console.log(`Call initiated successfully on attempt ${attempt}`)
      return call

    } catch (error) {
      console.error(`Call attempt ${attempt} failed:`, error.message)

      if (attempt === maxRetries) {
        throw error
      }

      // Wait before retrying (exponential backoff)
      await sleep(1000 * Math.pow(2, attempt - 1))
    }
  }
}

// 4. Test webhook endpoint
async function testWebhook() {
  const response = await fetch('https://your-domain.com/twiml/test', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: 'From=%2B1234567890&To=%2B0987654321'
  })

  console.log('Webhook status:', response.status)
  console.log('Webhook body:', await response.text())

  if (response.status !== 200) {
    throw new Error(`Webhook test failed with status ${response.status}`)
  }
}
```

### Issue Category 4: Performance & Reliability

#### Problem: High Call Failure Rate

**Symptoms:**
- >10% of calls fail
- Inconsistent connect rates
- Random disconnections
- System errors under load

**Diagnostic Steps:**

```bash
# 1. Collect failure metrics
Use mcp__elevenlabs__elevenlabs_list_conversations with:
{
  "status": "failed"
}

# Count failures by type

# 2. Analyze failure patterns
# Group by:
# - Time of day
# - Agent ID
# - Error message
# - Call duration before failure

# 3. Check system resources
# In server logs:
Grep logs/*.log for:
- "Out of memory"
- "Connection timeout"
- "Rate limit exceeded"
- "Service unavailable"
```

**Root Cause Analysis:**

```typescript
async function analyzeFailures(timeRange: { start: Date, end: Date }) {
  const conversations = await listConversations(timeRange)
  const failures = conversations.filter(c => c.status === 'failed')

  // Group by error type
  const errorTypes = {}
  failures.forEach(f => {
    const error = f.error || 'unknown'
    errorTypes[error] = (errorTypes[error] || 0) + 1
  })

  // Group by time
  const hourlyFailures = new Array(24).fill(0)
  failures.forEach(f => {
    const hour = new Date(f.startedAt).getHours()
    hourlyFailures[hour]++
  })

  // Group by agent
  const agentFailures = {}
  failures.forEach(f => {
    agentFailures[f.agentId] = (agentFailures[f.agentId] || 0) + 1
  })

  return {
    totalFailures: failures.length,
    failureRate: (failures.length / conversations.length) * 100,
    errorTypes,
    hourlyFailures,
    agentFailures,
    recommendations: generateRecommendations(errorTypes, hourlyFailures, agentFailures)
  }
}

function generateRecommendations(errors, hourly, agents) {
  const recommendations = []

  // Error-based recommendations
  if (errors['Rate limit exceeded'] > 10) {
    recommendations.push('Implement rate limiting and request throttling')
  }

  if (errors['Connection timeout'] > 5) {
    recommendations.push('Increase timeout settings and check network stability')
  }

  if (errors['Agent not found'] > 0) {
    recommendations.push('Validate agent IDs before starting conversations')
  }

  // Time-based recommendations
  const peakHour = hourly.indexOf(Math.max(...hourly))
  if (hourly[peakHour] > 10) {
    recommendations.push(`High failures at hour ${peakHour}:00 - consider load balancing`)
  }

  // Agent-based recommendations
  const problematicAgent = Object.entries(agents)
    .sort(([,a], [,b]) => b - a)[0]

  if (problematicAgent && problematicAgent[1] > 5) {
    recommendations.push(`Agent ${problematicAgent[0]} has high failure rate - review configuration`)
  }

  return recommendations
}
```

**Fix:**

```typescript
// 1. Implement rate limiting
import rateLimit from 'express-rate-limit'

const callLimiter = rateLimit({
  windowMs: 60 * 1000,  // 1 minute
  max: 100,             // Max 100 calls per minute
  message: 'Too many calls, please try again later'
})

app.use('/api/calls', callLimiter)

// 2. Add circuit breaker pattern
class CircuitBreaker {
  private failureCount = 0
  private lastFailureTime = 0
  private state = 'closed'  // closed, open, half-open

  async execute(fn: Function) {
    if (this.state === 'open') {
      // Check if should try again
      if (Date.now() - this.lastFailureTime > 60000) {
        this.state = 'half-open'
      } else {
        throw new Error('Circuit breaker is open')
      }
    }

    try {
      const result = await fn()

      if (this.state === 'half-open') {
        this.state = 'closed'
        this.failureCount = 0
      }

      return result

    } catch (error) {
      this.failureCount++
      this.lastFailureTime = Date.now()

      if (this.failureCount >= 5) {
        this.state = 'open'
        console.error('Circuit breaker opened due to failures')
      }

      throw error
    }
  }
}

// 3. Add health checks
async function healthCheck() {
  const checks = {
    elevenlabs: false,
    twilio: false,
    database: false
  }

  try {
    // Check ElevenLabs
    await listVoices()
    checks.elevenlabs = true
  } catch (error) {
    console.error('ElevenLabs health check failed:', error)
  }

  try {
    // Check Twilio
    await twilioClient.getCallStatus('test')
    checks.twilio = true
  } catch (error) {
    console.error('Twilio health check failed:', error)
  }

  try {
    // Check database
    await database.ping()
    checks.database = true
  } catch (error) {
    console.error('Database health check failed:', error)
  }

  return {
    healthy: Object.values(checks).every(v => v),
    checks
  }
}

// Run health checks every 5 minutes
setInterval(healthCheck, 5 * 60 * 1000)

// 4. Implement retry with exponential backoff
async function retryWithBackoff(fn: Function, maxRetries = 3) {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      return await fn()
    } catch (error) {
      if (attempt === maxRetries) throw error

      const delay = Math.min(1000 * Math.pow(2, attempt), 10000)
      console.log(`Retry attempt ${attempt} failed, waiting ${delay}ms`)
      await sleep(delay)
    }
  }
}
```

## Logging & Monitoring

### Comprehensive Logging Setup

```typescript
// logging.ts
import winston from 'winston'

export const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  transports: [
    // Write errors to dedicated file
    new winston.transports.File({
      filename: 'logs/error.log',
      level: 'error'
    }),

    // Write all logs to combined file
    new winston.transports.File({
      filename: 'logs/combined.log'
    }),

    // Console output for development
    new winston.transports.Console({
      format: winston.format.combine(
        winston.format.colorize(),
        winston.format.simple()
      )
    })
  ]
})

// Call-specific logger
export function createCallLogger(conversationId: string) {
  return logger.child({ conversationId })
}

// Usage in call flow:
const callLogger = createCallLogger(conversationId)

callLogger.info('Call initiated', {
  to: phoneNumber,
  agentId: agentId
})

callLogger.debug('Context injected', {
  leadData: leadData
})

callLogger.error('Call failed', {
  error: error.message,
  stack: error.stack
})
```

### Monitoring Dashboard Queries

```bash
# Count errors in last hour
Grep logs/error.log "$(date -d '1 hour ago' '+%Y-%m-%d %H')"

# Find slow calls (>5 minutes)
Grep logs/combined.log "duration" | awk '$NF > 300'

# Count failures by agent
Grep logs/combined.log "Call failed" |
  grep -oP 'agentId":"[^"]+' |
  sort | uniq -c

# Track error types
Grep logs/error.log "error" |
  grep -oP '"message":"[^"]+' |
  sort | uniq -c
```

## Diagnostic Report Template

```markdown
# Agent Debugging Report

## Issue Summary
**Date:** [Date of issue]
**Agent ID:** [Agent identifier]
**Conversation ID(s):** [Affected conversations]
**Severity:** [Critical / High / Medium / Low]

## Symptoms Observed
- [Symptom 1]
- [Symptom 2]
- [Symptom 3]

## Diagnostic Steps Taken
1. [Step 1 with results]
2. [Step 2 with results]
3. [Step 3 with results]

## Root Cause Analysis
**Primary Cause:** [Main issue identified]

**Contributing Factors:**
- [Factor 1]
- [Factor 2]

**Evidence:**
- [Log excerpt or transcript snippet]
- [Metric data]

## Solution Implemented
**Changes Made:**
```typescript
// Configuration changes
```

**Verification:**
- [How you verified the fix]
- [Test results]

## Prevention Measures
- [Step to prevent recurrence]
- [Monitoring to add]
- [Documentation to update]

## Follow-up Actions
- [ ] Monitor for 24 hours
- [ ] Update runbook
- [ ] Train team on new process
```

## Troubleshooting Checklist

```markdown
## Pre-Flight Checklist

Before debugging, verify basics:

### Configuration
- [ ] Agent exists and status is "active"
- [ ] Voice ID is valid and available for TTS
- [ ] Model ID is correct (flash/turbo/multilingual)
- [ ] System prompt is non-empty and well-formed
- [ ] TCPA compliance flags are enabled

### Infrastructure
- [ ] Webhook endpoint is accessible (200 OK)
- [ ] Twilio account has sufficient balance
- [ ] Phone number is active and voice-enabled
- [ ] ElevenLabs API key is valid
- [ ] Environment variables are set correctly

### Network
- [ ] Internet connectivity is stable
- [ ] No firewall blocking WebSocket connections
- [ ] DNS resolution working
- [ ] Sufficient bandwidth available

### System
- [ ] Server/application is running
- [ ] No resource exhaustion (CPU, memory, disk)
- [ ] Logs are being written
- [ ] Database is accessible
```

## Resources

### Log Locations
- Application logs: `logs/calling-service.log`
- Error logs: `logs/error.log`
- Conversation logs: `logs/conversations/`
- Twilio debugger: https://www.twilio.com/console/debugger

### Useful Commands
```bash
# Tail logs in real-time
tail -f logs/calling-service.log

# Search for specific conversation
Grep logs/combined.log "conversation_abc123"

# Count errors by type
Grep logs/error.log "error" | cut -d'"' -f4 | sort | uniq -c

# Find slow responses
Grep logs/combined.log "latency" | awk '$NF > 500'
```

### External Resources
- [ElevenLabs API Status](https://status.elevenlabs.io)
- [Twilio Status](https://status.twilio.com)
- [WebSocket Debugging Tools](https://www.websocket.org/echo.html)

---

**Remember:** Systematic debugging saves time. Follow the 5-step process: Observe, Reproduce, Isolate, Diagnose, Fix. Document everything for future reference.
