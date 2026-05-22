---
name: deepgram-webhooks
description: >
  Receive and verify Deepgram webhooks (callbacks). Use when setting up Deepgram webhook
  handlers, processing transcription callbacks, or handling asynchronous transcription results.
license: MIT
metadata:
  author: hookdeck
  version: "0.1.0"
  repository: https://github.com/hookdeck/webhook-skills
---

# Deepgram Webhooks

## When to Use This Skill

- Setting up Deepgram callback handlers for transcription results
- Processing asynchronous transcription results from Deepgram
- Implementing webhook authentication for Deepgram callbacks
- Handling transcription completion events

## Essential Code

Deepgram webhooks (callbacks) are used to receive transcription results asynchronously. When you provide a callback URL in your transcription request, Deepgram immediately responds with a `request_id` and sends the transcription results to your callback URL when processing is complete.

### Basic Webhook Handler

```javascript
// Express.js example
app.post('/webhooks/deepgram', express.raw({ type: 'application/json' }), (req, res) => {
  // Verify webhook authenticity using dg-token header
  const dgToken = req.headers['dg-token'];

  if (!dgToken) {
    return res.status(401).send('Missing dg-token header');
  }

  // Verify the token matches your expected API Key Identifier
  // The dg-token contains the API Key Identifier used in the original request
  if (dgToken !== process.env.DEEPGRAM_API_KEY_ID) {
    return res.status(403).send('Invalid dg-token');
  }

  // Parse the transcription result
  const transcriptionResult = JSON.parse(req.body.toString());

  // Process the transcription
  console.log('Received transcription:', transcriptionResult);

  // Return success to prevent retries
  res.status(200).send('OK');
});
```

### Authentication Methods

Deepgram supports two authentication methods for webhooks:

1. **dg-token Header**: Automatically included, contains the API Key Identifier
2. **Basic Auth**: Embed credentials in the callback URL

```javascript
// Using dg-token header (recommended)
const verifyDgToken = (req, res, next) => {
  const dgToken = req.headers['dg-token'];

  if (!dgToken || dgToken !== process.env.DEEPGRAM_API_KEY_ID) {
    return res.status(403).send('Invalid authentication');
  }

  next();
};

// Basic Auth in callback URL
// https://username:password@your-domain.com/webhooks/deepgram
```

### Making a Request with Callback

```bash
curl \
  --request POST \
  --header 'Authorization: Token YOUR_DEEPGRAM_API_KEY' \
  --header 'Content-Type: audio/wav' \
  --data-binary @audio.wav \
  --url 'https://api.deepgram.com/v1/listen?callback=https://your-domain.com/webhooks/deepgram'
```

## Common Event Types

Deepgram sends transcription results as webhook payloads. The structure varies based on the features enabled in your request:

| Field | Description | Always Present |
|-------|-------------|----------------|
| `request_id` | Unique identifier for the transcription request | Yes |
| `created` | Timestamp when transcription was created | Yes |
| `duration` | Length of the audio in seconds | Yes |
| `channels` | Number of audio channels | Yes |
| `results` | Transcription results by channel | Yes |
| `results.channels[].alternatives` | Transcription alternatives | Yes |
| `results.channels[].alternatives[].transcript` | The transcribed text | Yes |
| `results.channels[].alternatives[].confidence` | Confidence score (0-1) | Yes |

## Environment Variables

```bash
# Your Deepgram API Key (for making requests)
DEEPGRAM_API_KEY=your_api_key_here

# API Key Identifier (shown in Deepgram console, used to verify dg-token)
# Note: This is NOT your API Key secret - it's a unique identifier shown
# in the Deepgram console that identifies which API key was used for a request
DEEPGRAM_API_KEY_ID=your_api_key_id_here

# Your webhook endpoint URL
WEBHOOK_URL=https://your-domain.com/webhooks/deepgram
```

## Local Development

For local webhook testing, install Hookdeck CLI:

```bash
# Install via npm
npm install -g hookdeck-cli

# Or via Homebrew
brew install hookdeck/hookdeck/hookdeck

# Create a local tunnel (no account required)
hookdeck listen 3000 --path /webhooks/deepgram

# Use the provided URL as your callback URL when making Deepgram requests
```

This provides:
- Local tunnel URL for testing
- Web UI for inspecting webhook payloads
- Request history and debugging tools

## Important Notes

### Retry Behavior
- Deepgram retries failed callbacks (non-200-299 status) up to 10 times
- 30-second delay between retry attempts
- Always return 200-299 status for successfully processed webhooks

### Port Restrictions
- Only ports 80, 443, 8080, and 8443 are allowed for callbacks
- Ensure your webhook endpoint uses one of these ports

### No Signature Verification
- Deepgram uses a simple token-based authentication via the dg-token header rather than cryptographic HMAC signatures used by other providers
- Authentication relies on the `dg-token` header or Basic Auth
- Always use HTTPS for webhook endpoints

## Resources

- [overview.md](references/overview.md) - What Deepgram webhooks are, transcription events
- [setup.md](references/setup.md) - Configure callbacks in Deepgram API requests
- [verification.md](references/verification.md) - Authentication methods and security considerations
- [examples/](examples/) - Complete implementations for Express, Next.js, and FastAPI

## Recommended: webhook-handler-patterns

For production handlers, install the patterns skill alongside this one. Key references (links work when only this skill is installed):

- [Idempotency](https://github.com/hookdeck/webhook-skills/blob/main/skills/webhook-handler-patterns/references/idempotency.md)
- [Error handling](https://github.com/hookdeck/webhook-skills/blob/main/skills/webhook-handler-patterns/references/error-handling.md)
- [Retry logic](https://github.com/hookdeck/webhook-skills/blob/main/skills/webhook-handler-patterns/references/retry-logic.md)

## Related Skills

- [stripe-webhooks](https://github.com/hookdeck/webhook-skills/tree/main/skills/stripe-webhooks) - Stripe payment webhooks
- [shopify-webhooks](https://github.com/hookdeck/webhook-skills/tree/main/skills/shopify-webhooks) - Shopify store webhooks
- [github-webhooks](https://github.com/hookdeck/webhook-skills/tree/main/skills/github-webhooks) - GitHub repository webhooks
- [webhook-handler-patterns](https://github.com/hookdeck/webhook-skills/tree/main/skills/webhook-handler-patterns) - Idempotency, error handling, retry logic
- [hookdeck-event-gateway](https://github.com/hookdeck/webhook-skills/tree/main/skills/hookdeck-event-gateway) - Webhook infrastructure that replaces your queue — guaranteed delivery, automatic retries, replay, rate limiting, and observability for your webhook handlers