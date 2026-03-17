---
name: twilio-voice
description: Comprehensive Twilio Voice API assistance with AI integration patterns
---

# Twilio Voice Skill

Comprehensive assistance for building voice applications with Twilio Voice API, including AI-powered voice assistants, ConversationRelay integrations, and production-ready implementation patterns.

## When to Use This Skill

This skill should be triggered when:

**Core Voice Development:**
- Implementing Twilio Voice API integrations
- Building interactive voice response (IVR) systems
- Debugging Twilio voice applications
- Working with TwiML (Twilio Markup Language)
- Setting up voice webhooks and call routing

**AI-Powered Voice Applications:**
- Building conversational AI voice assistants
- Integrating Twilio with LLMs (OpenAI, Langflow, etc.)
- Implementing real-time bidirectional voice streaming with OpenAI Realtime API
- Creating voice-based customer service automation
- Developing natural language phone interactions
- Building function-calling voice agents with tool invocation
- Implementing low-latency streaming responses (~1 second)
- Managing conversation context and multi-turn dialogues

**Advanced Features:**
- Working with ConversationRelay for real-time AI conversations
- Implementing voice streaming with low latency
- Building voice applications with function calling
- Managing conversation context and memory
- Handling interruptions and turn-taking in voice conversations

**Conversational Intelligence & Analytics:**
- Analyzing call transcripts for business insights
- Implementing sentiment analysis and intent detection
- Building compliance monitoring systems
- Tracking AI agent performance metrics
- Creating custom language operators for business logic
- Extracting structured data from voice conversations
- Monitoring lead generation and customer satisfaction

## Quick Reference

### Common Patterns

#### 1. ConversationRelay Integration
```javascript
// Real-time AI voice conversation setup
app.post('/voice', (req, res) => {
  const twiml = new VoiceResponse();
  const connect = twiml.connect();

  connect.conversationRelay({
    url: 'wss://your-app.ngrok.io/ws',
    voice: 'Polly.Joanna',
    language: 'en-US'
  });

  res.type('text/xml');
  res.send(twiml.toString());
});
```

#### 2. Langflow + Twilio Integration
```javascript
// Forward transcriptions to Langflow for AI processing
conversationRelay.on('transcription', async (data) => {
  const response = await fetch(`${LANGFLOW_URL}/api/v1/run/${FLOW_ID}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${LANGFLOW_API_KEY}`
    },
    body: JSON.stringify({
      message: data.text,
      session_id: data.callSid
    })
  });

  const aiResponse = await response.json();
  conversationRelay.say(aiResponse.message);
});
```

#### 3. Voice-Optimized Prompts
```javascript
// Best practices for AI voice responses
const systemPrompt = `
You are a helpful voice assistant. Follow these guidelines:
- Answer carefully and concisely (2-3 sentences max)
- Spell out ALL numbers (say "twenty-three" not "23")
- NO emojis, bullet points, or special symbols
- Use natural conversational language
- Avoid markdown or formatting
- Keep responses under 30 seconds when spoken
`;
```

#### 4. Webhook Configuration
```javascript
// Basic Twilio webhook handler
app.post('/twiml', (req, res) => {
  const twiml = new VoiceResponse();

  twiml.say({
    voice: 'Polly.Joanna'
  }, 'Hello! How can I help you today?');

  twiml.gather({
    input: 'speech',
    action: '/process-speech',
    timeout: 3
  });

  res.type('text/xml');
  res.send(twiml.toString());
});
```

#### 5. Development Setup with ngrok
```bash
# Expose local server for Twilio webhooks
ngrok http 3000

# Configure Twilio phone number webhook URL:
# https://your-subdomain.ngrok.io/voice
```

#### 6. Conversational Intelligence Analysis
```python
# Analyze call recordings with Conversational Intelligence
from twilio.rest import Client

client = Client(account_sid, auth_token)

# Create Intelligence Service (one-time setup)
service = client.intelligence.v2.services.create(
    auto_transcribe=True,
    unique_name='customer-service-analysis'
)

# Create transcript from call recording
transcript = client.intelligence.v2.transcripts.create(
    service_sid=service.sid,
    channel={
        'media_properties': {
            'source_sid': 'REXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'  # Recording SID
        }
    }
)

# Attach language operators for business insights
sentiment_op = client.intelligence.v2 \
    .services(service.sid) \
    .operators.create(
        operator_type='sentiment-analysis',
        config={'language_code': 'en-US'}
    )

# Retrieve analyzed results
results = client.intelligence.v2 \
    .transcripts(transcript.sid) \
    .operator_results.list()

for result in results:
    print(f"Operator: {result.operator_type}")
    print(f"Results: {result.extract_match}")
```

#### 7. Real-Time Conversation Monitoring
```python
# Monitor ConversationRelay AI agents in real-time
from twilio.rest import Client

client = Client(account_sid, auth_token)

# Create transcript from active ConversationRelay call
transcript = client.intelligence.v2.transcripts.create(
    service_sid='GAxxxxx',
    channel={
        'media_properties': {
            'source_sid': 'CA xxxx',  # Active Call SID
            'participant_label': 'ai_agent'
        }
    }
)

# Access real-time transcription
sentences = client.intelligence.v2 \
    .transcripts(transcript.sid) \
    .sentences.list()

for sentence in sentences:
    print(f"[{sentence.participant_label}]: {sentence.transcript}")
    print(f"Confidence: {sentence.confidence}")
```

#### 8. Custom Language Operators
```python
# Create custom operators for business-specific analysis
from twilio.rest import Client

client = Client(account_sid, auth_token)

# Generative Custom Operator using LLM (public beta)
custom_op = client.intelligence.v2 \
    .services(service_sid) \
    .operators.create(
        operator_type='custom-operator',
        config={
            'name': 'lead-qualification',
            'description': 'Extract lead qualification criteria',
            'prompt': '''
                Analyze this conversation and extract:
                1. Customer budget range
                2. Timeline for decision
                3. Decision maker status
                4. Pain points mentioned
                Return as JSON.
            ''',
            'language_code': 'en-US'
        }
    )

# Pre-built Language Operator for PII detection
pii_op = client.intelligence.v2 \
    .services(service_sid) \
    .operators.create(
        operator_type='pii-detection',
        config={
            'redact': True,
            'pii_types': ['ssn', 'credit_card', 'email']
        }
    )
```

#### 9. OpenAI Realtime API Integration
```python
# Bidirectional voice streaming with OpenAI Realtime API
import asyncio
import websockets
import json
from twilio.twiml.voice_response import VoiceResponse, Connect

@app.route('/incoming-call', methods=['POST'])
def handle_incoming_call():
    """Initiate call with Media Streams"""
    response = VoiceResponse()
    connect = response.connect()
    connect.stream(url=f'wss://{SERVER_DOMAIN}/media-stream')
    return str(response)

async def handle_media_stream(websocket):
    """Relay audio between Twilio and OpenAI Realtime API"""
    async with websockets.connect(
        'wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview-2024-10-01',
        extra_headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "OpenAI-Beta": "realtime=v1"
        }
    ) as openai_ws:

        # Configure session with interruption handling
        session_update = {
            "type": "session.update",
            "session": {
                "turn_detection": {"type": "server_vad"},
                "input_audio_format": "g711_ulaw",
                "output_audio_format": "g711_ulaw"
            }
        }
        await openai_ws.send(json.dumps(session_update))

        # Relay audio bidirectionally
        async def twilio_receiver():
            async for message in websocket:
                data = json.loads(message)
                if data['event'] == 'media':
                    # Forward audio to OpenAI
                    audio_append = {
                        "type": "input_audio_buffer.append",
                        "audio": data['media']['payload']
                    }
                    await openai_ws.send(json.dumps(audio_append))

        async def openai_receiver():
            async for message in openai_ws:
                response = json.loads(message)

                # Handle interruptions
                if response['type'] == 'input_audio_buffer.speech_started':
                    # User started speaking - truncate AI response
                    await openai_ws.send(json.dumps({
                        "type": "conversation.item.truncate",
                        "item_id": current_item_id
                    }))
                    # Clear Twilio audio queue
                    await websocket.send(json.dumps({"event": "clear"}))

                # Forward AI audio to Twilio
                elif response['type'] == 'response.audio.delta':
                    await websocket.send(json.dumps({
                        "event": "media",
                        "media": {"payload": response['delta']}
                    }))

        await asyncio.gather(twilio_receiver(), openai_receiver())
```

#### 10. Function-Calling Voice Agent (Call-GPT Pattern)
```javascript
// Deepgram + GPT-4 with dynamic function calling
const { Deepgram } = require('@deepgram/sdk');
const OpenAI = require('openai');

const deepgram = new Deepgram(process.env.DEEPGRAM_API_KEY);
const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

// Define available functions
const functionManifest = [
    {
        name: 'check_order_status',
        description: 'Check the status of a customer order',
        parameters: {
            type: 'object',
            properties: {
                order_id: { type: 'string', description: 'Order ID' }
            },
            required: ['order_id']
        }
    }
];

let userContext = [];  // Conversation history

async function handleMediaStream(connection) {
    // Set up Deepgram transcription
    const dgConnection = deepgram.transcription.live({
        model: 'nova-2',
        language: 'en-US',
        smart_format: true
    });

    dgConnection.on('transcript', async (data) => {
        const transcript = data.channel.alternatives[0].transcript;
        if (!transcript) return;

        // Add user message to context
        userContext.push({ role: 'user', content: transcript });

        // Stream GPT response with function calling
        const stream = await openai.chat.completions.create({
            model: 'gpt-4',
            messages: userContext,
            tools: functionManifest.map(fn => ({ type: 'function', function: fn })),
            stream: true
        });

        let responseText = '';
        let functionCall = null;

        for await (const chunk of stream) {
            const delta = chunk.choices[0]?.delta;

            // Handle function calls
            if (delta.tool_calls) {
                functionCall = delta.tool_calls[0].function;
                if (functionCall.name) {
                    // Execute function
                    const result = await executeFuncti on(
                        functionCall.name,
                        JSON.parse(functionCall.arguments)
                    );

                    // Add function result to context
                    userContext.push({
                        role: 'function',
                        name: functionCall.name,
                        content: JSON.stringify(result)
                    });

                    // Get follow-up response
                    const followUp = await openai.chat.completions.create({
                        model: 'gpt-4',
                        messages: userContext
                    });

                    responseText = followUp.choices[0].message.content;
                }
            }
            // Handle text deltas
            else if (delta.content) {
                responseText += delta.content;

                // Use bullet points for natural breaking
                if (delta.content.includes('•')) {
                    await synthesizeAndPlay(responseText, connection);
                    responseText = '';
                }
            }
        }

        // Synthesize remaining text
        if (responseText) {
            await synthesizeAndPlay(responseText, connection);
        }

        // Add assistant response to context
        userContext.push({ role: 'assistant', content: responseText });
    });

    // Forward Twilio audio to Deepgram
    connection.on('media', (msg) => {
        dgConnection.send(Buffer.from(msg.media.payload, 'base64'));
    });
}

async function synthesizeAndPlay(text, connection) {
    // Use Deepgram TTS for low latency
    const audio = await deepgram.speak.request(
        { text },
        {
            model: 'aura-asteria-en',
            encoding: 'mulaw',
            sample_rate: 8000
        }
    );

    // Stream to Twilio
    connection.send({
        event: 'media',
        media: { payload: audio.toString('base64') }
    });
}

async function executeFunction(name, args) {
    // Dynamically require and execute function
    const fn = require(`./functions/${name}`);
    return await fn(args);
}
```

#### 11. Low-Latency Streaming with Interruptions
```javascript
// Optimized streaming pattern for <1 second responses
const systemPrompt = `You are a helpful voice assistant.
Keep responses very concise (1-2 sentences).
Use • bullets to break responses into natural chunks.
Ask only ONE question at a time.
Be conversational and friendly.`;

let isAssistantSpeaking = false;
let currentStreamId = null;

async function streamGPTResponse(userMessage, connection) {
    const stream = await openai.chat.completions.create({
        model: 'gpt-4',
        messages: [
            { role: 'system', content: systemPrompt },
            ...userContext,
            { role: 'user', content: userMessage }
        ],
        stream: true,
        max_tokens: 100,  // Limit for voice responses
        temperature: 0.7
    });

    currentStreamId = generateId();
    isAssistantSpeaking = true;
    let buffer = '';

    for await (const chunk of stream) {
        const content = chunk.choices[0]?.delta?.content;
        if (!content) continue;

        buffer += content;

        // Stream on sentence boundaries or bullet points
        if (content.match(/[.!?•]/)) {
            if (!isAssistantSpeaking) break;  // Interrupted

            await synthesizeAndPlay(buffer.trim(), connection, currentStreamId);
            buffer = '';
        }
    }

    // Flush remaining buffer
    if (buffer.trim() && isAssistantSpeaking) {
        await synthesizeAndPlay(buffer.trim(), connection, currentStreamId);
    }

    isAssistantSpeaking = false;
}

// Handle user interruptions
deepgram.on('speech_started', () => {
    if (isAssistantSpeaking) {
        isAssistantSpeaking = false;  // Stop streaming
        connection.send({ event: 'clear' });  // Clear Twilio queue
        currentStreamId = null;
    }
});
```

## Integration Patterns

### AI Voice Assistant Architecture

```
┌─────────────┐         ┌──────────────┐         ┌────────────┐
│   Phone     │ ──────> │    Twilio    │ ──────> │  Your      │
│   Caller    │         │    Voice     │         │  Server    │
│             │ <────── │  +Conversation│ <────── │  (Node.js) │
└─────────────┘         │    Relay     │         └────────────┘
                        └──────────────┘               │
                                                       │
                        ┌──────────────┐               │
                        │   AI Service │ <─────────────┘
                        │  (OpenAI/    │
                        │   Langflow)  │
                        └──────────────┘
```

**Flow:**
1. Caller dials Twilio number
2. Twilio webhook triggers your server's `/voice` endpoint
3. Server responds with TwiML including ConversationRelay
4. ConversationRelay establishes WebSocket for bidirectional audio
5. Audio transcribed and sent to AI service
6. AI response synthesized and streamed back to caller

### Common Use Cases

#### Customer Service Automation
```javascript
// Route calls based on intent
const intentRouter = {
  'billing': handleBillingInquiry,
  'support': handleTechnicalSupport,
  'sales': transferToSales
};

conversationRelay.on('transcription', async (data) => {
  const intent = await detectIntent(data.text);
  await intentRouter[intent](data);
});
```

#### Voice-Based IVR with Natural Language
```javascript
// Replace traditional touch-tone IVR
twiml.gather({
  input: 'speech',
  hints: 'billing, support, sales, account',
  speechTimeout: 'auto'
}).say('How can I help you today?');
```

#### Appointment Scheduling by Voice
```javascript
// Extract structured data from conversation
const extractAppointment = async (transcript) => {
  const prompt = `Extract appointment details: ${transcript}
  Return JSON: { date, time, service }`;

  const response = await openai.chat.completions.create({
    model: 'gpt-4',
    messages: [{ role: 'user', content: prompt }]
  });

  return JSON.parse(response.choices[0].message.content);
};
```

#### Conversational Intelligence for Business Insights
```python
# Complete workflow: Call → Analysis → Business Action
from twilio.rest import Client

client = Client(account_sid, auth_token)

# 1. Create Intelligence Service for your use case
service = client.intelligence.v2.services.create(
    auto_transcribe=True,
    unique_name='sales-call-analysis',
    auto_redaction=True  # Automatically redact PII
)

# 2. Attach business-relevant operators
operators = [
    # Sentiment tracking
    {'type': 'sentiment-analysis', 'config': {'language_code': 'en-US'}},
    # Intent detection
    {'type': 'intent-detection', 'config': {'intents': ['purchase', 'cancel', 'complain']}},
    # Custom lead scoring
    {
        'type': 'custom-operator',
        'config': {
            'name': 'lead-score',
            'prompt': 'Rate this lead 1-10 based on budget, timeline, and authority. Explain reasoning.',
            'language_code': 'en-US'
        }
    }
]

for op in operators:
    client.intelligence.v2 \
        .services(service.sid) \
        .operators.create(operator_type=op['type'], config=op['config'])

# 3. Process call recording
def analyze_call(recording_sid):
    transcript = client.intelligence.v2.transcripts.create(
        service_sid=service.sid,
        channel={'media_properties': {'source_sid': recording_sid}}
    )

    # Wait for processing (async in production)
    import time
    time.sleep(10)

    # 4. Retrieve insights
    results = client.intelligence.v2 \
        .transcripts(transcript.sid) \
        .operator_results.list()

    insights = {}
    for result in results:
        insights[result.operator_type] = result.extract_match

    # 5. Take business action
    if insights.get('lead-score', {}).get('score', 0) >= 8:
        # High-value lead - alert sales team
        send_slack_notification(f"Hot lead detected! Score: {insights['lead-score']}")

    if insights.get('sentiment', {}).get('score', 0) < 0.3:
        # Negative sentiment - trigger retention workflow
        create_support_ticket(transcript.sid, priority='high')

    return insights

# Use with Twilio Voice webhook
@app.route('/call-completed', methods=['POST'])
def handle_call_completed():
    recording_sid = request.form.get('RecordingSid')
    insights = analyze_call(recording_sid)

    # Store in CRM, analytics platform, etc.
    store_call_insights(insights)

    return '', 200
```

#### Compliance Monitoring with Auto-Redaction
```python
# Monitor calls for compliance and automatically redact PII
from twilio.rest import Client

client = Client(account_sid, auth_token)

# Create compliance-focused service
compliance_service = client.intelligence.v2.services.create(
    auto_transcribe=True,
    unique_name='compliance-monitoring',
    auto_redaction=True,
    data_logging=False  # Don't log to Twilio for regulated industries
)

# Attach compliance operators
compliance_ops = [
    # PII detection and redaction
    {
        'type': 'pii-detection',
        'config': {
            'redact': True,
            'pii_types': ['ssn', 'credit_card', 'bank_account', 'email', 'phone']
        }
    },
    # Custom compliance checker
    {
        'type': 'custom-operator',
        'config': {
            'name': 'tcpa-compliance',
            'prompt': '''
                Check if this call follows TCPA compliance:
                1. Was consent obtained before marketing?
                2. Was opt-out option provided?
                3. Was call within allowed hours?
                Return: {compliant: true/false, violations: []}
            ''',
            'language_code': 'en-US'
        }
    }
]

for op in compliance_ops:
    client.intelligence.v2 \
        .services(compliance_service.sid) \
        .operators.create(operator_type=op['type'], config=op['config'])

# Access redacted transcripts (PII removed)
transcript = client.intelligence.v2 \
    .transcripts(transcript_sid) \
    .fetch()

print(f"Redacted transcript: {transcript.redacted_transcript}")
print(f"PII detected: {transcript.pii_matches}")
```

## Prerequisites

### Twilio Account Setup
- Twilio account with phone number
- ConversationRelay enabled in console (for AI voice assistants)
- Conversational Intelligence enabled (for call analysis)
- Account SID and Auth Token
- Voice-enabled phone number

### Development Environment
```bash
# Required packages
npm install twilio express dotenv

# For AI integration
npm install openai  # OpenAI Chat Completions or Realtime API
# OR configure Langflow endpoint

# For Deepgram STT/TTS (Call-GPT pattern)
npm install @deepgram/sdk

# For OpenAI Realtime API (Python)
pip install websockets openai

# For Conversational Intelligence (Python)
pip install twilio

# For local development
npm install -g ngrok  # Webhook tunneling
```

### Environment Variables
```bash
# .env file
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+1234567890

# For AI integration
OPENAI_API_KEY=sk-xxxxxxxxxxxxx  # Chat Completions or Realtime API
# OR
LANGFLOW_URL=http://localhost:7860
LANGFLOW_FLOW_ID=your-flow-id
LANGFLOW_API_KEY=your-api-key

# For Deepgram (STT/TTS)
DEEPGRAM_API_KEY=your_deepgram_api_key

# For Conversational Intelligence
TWILIO_INTELLIGENCE_SERVICE_SID=GAxxxxxxxxxxxxx  # Created via API

# Server configuration
PORT=3000
SERVER_DOMAIN=your-subdomain.ngrok.io  # For OpenAI Realtime API
NGROK_URL=https://your-subdomain.ngrok.io
```

### Twilio Console Configuration
1. Navigate to Phone Numbers → Active Numbers
2. Select your voice-enabled number
3. Configure Voice & Fax:
   - **A CALL COMES IN**: Webhook → `https://your-ngrok-url.ngrok.io/voice`
   - **HTTP Method**: POST
4. Save configuration

## Reference Files

This skill includes comprehensive documentation in `references/`:

- **other.md** - Core Twilio Voice documentation
- **integration-patterns.md** - AI integration examples (see assets/)
- **best-practices.md** - Voice-optimized development patterns

Use `view` to read specific reference files when detailed information is needed.

## Best Practices

### Voice-Optimized AI Responses
1. **Keep responses concise** - 2-3 sentences maximum
2. **Spell out numbers** - Say "twenty-three" not "23"
3. **Avoid special characters** - No emojis, bullets, or markdown
4. **Use natural language** - Conversational, not formal documentation
5. **Time-bound responses** - Aim for < 30 seconds when spoken
6. **Provide clear next steps** - "Would you like me to..." patterns

### Error Handling
```javascript
// Graceful degradation for voice applications
conversationRelay.on('error', (error) => {
  console.error('ConversationRelay error:', error);

  // Fallback to simple IVR
  const twiml = new VoiceResponse();
  twiml.say('I apologize, but I\'m having trouble right now.');
  twiml.redirect('/fallback-menu');

  res.type('text/xml').send(twiml.toString());
});
```

### Security Considerations
```javascript
// Validate Twilio requests
const twilio = require('twilio');

app.post('/voice', (req, res) => {
  const twilioSignature = req.headers['x-twilio-signature'];
  const url = `https://${req.hostname}${req.url}`;

  if (!twilio.validateRequest(
    process.env.TWILIO_AUTH_TOKEN,
    twilioSignature,
    url,
    req.body
  )) {
    return res.status(403).send('Forbidden');
  }

  // Process validated request
  // ...
});
```

### Performance Optimization
- **Use streaming mode** for lower latency AI responses
- **Implement timeouts** to prevent hung connections
- **Cache common responses** for frequently asked questions
- **Monitor call quality metrics** via Twilio Console

## Working with This Skill

### For Beginners
1. Start with basic webhook implementation (Pattern #4)
2. Test with ngrok tunneling (Pattern #5)
3. Experiment with voice-optimized prompts (Pattern #3)
4. Review prerequisites and environment setup

### For AI Integration
1. Choose your AI service (OpenAI, Langflow, or custom LLM)
2. Implement ConversationRelay pattern (#1 or #2)
3. Apply voice-optimization best practices
4. Test conversation flow and interruption handling

### For Production Deployment
1. Move from ngrok to production server with SSL
2. Implement request validation and security measures
3. Set up monitoring and error tracking
4. Configure scaling for call volume
5. Test fallback mechanisms

## Resources

### references/
Organized documentation extracted from official sources:
- **llms.md** - Twilio Voice API overview and core concepts
- **other.md** - Additional documentation and guides
- **index.md** - Quick navigation index

### assets/
Example implementations and templates (added from real-world integrations):
- **langflow-integration.js** - Complete Langflow + Twilio example
- **openai-integration.js** - OpenAI + Twilio Voice assistant
- **voice-prompts.md** - Collection of voice-optimized system prompts
- **.env.example** - Environment variable template

### scripts/
Helper utilities for development:
- **test-webhook.js** - Local webhook testing utility
- **validate-setup.js** - Verify Twilio configuration

### Example Projects
- **langflow-twilio-voice**: https://github.com/langflow-ai/langflow-twilio-voice
- **cr-demo**: https://github.com/robinske/cr-demo
- **speech-assistant-openai-realtime**: https://github.com/twilio-samples/speech-assistant-openai-realtime-api-python
- **call-gpt**: https://github.com/twilio-labs/call-gpt

## Notes

### Skill Enhancement History
- **v1.0** - Auto-generated from Twilio Voice documentation (llms.txt)
- **v1.1** - Enhanced with AI integration patterns from production implementations:
  - ConversationRelay integration patterns
  - Langflow + Twilio Voice workflow
  - OpenAI + Twilio Voice integration
  - Voice-optimized prompting best practices
  - Real-world use cases and examples
  - Security and performance guidelines
- **v1.2** - Added Conversational Intelligence capabilities:
  - Call transcript analysis and insights extraction
  - Sentiment analysis and intent detection
  - Custom language operators for business logic
  - Real-time conversation monitoring
  - Compliance monitoring with PII redaction
  - Business intelligence workflows (lead scoring, compliance)
  - Python SDK examples for Intelligence API
- **v1.3** - Added advanced voice AI patterns from Twilio sample repos:
  - OpenAI Realtime API bidirectional audio streaming
  - Native interruption handling with speech detection
  - Deepgram STT/TTS integration for low latency (~1 second)
  - Function-calling voice agents with dynamic tool invocation
  - Conversation context management with userContext pattern
  - Streaming response optimization with bullet-point breaking
  - Complete async websocket relay architecture
  - Production-ready function manifest patterns

### Knowledge Sources
1. **Official Documentation**: Twilio Voice API (llms.txt extraction)
2. **Production Patterns**: langflow-ai/langflow-twilio-voice repository
3. **Implementation Examples**: robinske/cr-demo repository
4. **Best Practices**: Voice-optimized AI response guidelines
5. **Conversational Intelligence**: Official Twilio Intelligence API documentation
6. **OpenAI Realtime API**: twilio-samples/speech-assistant-openai-realtime-api-python
7. **Function Calling Patterns**: twilio-labs/call-gpt repository

### Quality Status
- **Content Coverage**: Comprehensive (basic API + AI integrations + analytics + realtime streaming)
- **Code Examples**: Production-ready patterns included (11 complete code patterns)
- **Use Cases**: Customer service, IVR, appointments, voice assistants, business intelligence, function-calling agents
- **Integration Support**: Langflow, OpenAI (Chat + Realtime API), Deepgram, Conversational Intelligence API
- **Architecture Patterns**: ConversationRelay, Realtime API websockets, STT/TTS pipelines, function calling

## Updating

To refresh this skill with updated documentation:
1. **API docs**: Re-run `/create-skill --url https://www.twilio.com/docs/voice --name twilio-voice`
2. **Integration patterns**: Review referenced GitHub repositories for updates
3. **Best practices**: Monitor Twilio blog and community discussions
4. **AI enhancements**: Track ConversationRelay feature releases
