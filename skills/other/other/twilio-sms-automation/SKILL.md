---
name: Twilio SMS Automation
description: Automate SMS communications, two-way messaging, notifications, and voice workflows with Twilio
version: 1.0.0
author: Claude Office Skills
category: communication
tags:
  - twilio
  - sms
  - messaging
  - notifications
  - voice
department: operations
models:
  - claude-3-opus
  - claude-3-sonnet
  - gpt-4
mcp:
  server: communication-mcp
  tools:
    - twilio_send_sms
    - twilio_voice_call
    - twilio_lookup
    - twilio_verify
capabilities:
  - SMS sending and receiving
  - Voice call automation
  - Phone number verification
  - Two-factor authentication
input:
  - Phone numbers
  - Message content
  - Call scripts
  - Verification codes
output:
  - Message delivery status
  - Call recordings
  - Verification results
  - Analytics reports
languages:
  - en
  - multi
related_skills:
  - whatsapp-automation
  - slack-workflows
  - email-marketing
---

# Twilio SMS Automation

Comprehensive skill for automating SMS, voice, and verification workflows with Twilio.

## Core Workflows

### 1. SMS Messaging Flow

```
SMS AUTOMATION FLOW:
┌─────────────────┐
│    Trigger      │
│  (Event/API)    │
└────────┬────────┘
         ▼
┌─────────────────┐
│  Message Build  │
│  - Template     │
│  - Personalize  │
└────────┬────────┘
         ▼
┌─────────────────┐
│  Number Lookup  │
│  - Validate     │
│  - Format       │
└────────┬────────┘
         ▼
┌─────────────────┐
│     Send        │
│  - Twilio API   │
│  - Queue        │
└────────┬────────┘
         ▼
┌─────────────────┐
│    Delivery     │
│  - Status       │
│  - Callback     │
└─────────────────┘
```

### 2. Message Configuration

```yaml
sms_config:
  sender:
    phone_number: "+1234567890"
    messaging_service_sid: "MG..."  # For higher throughput
    
  defaults:
    status_callback: "https://api.example.com/sms/status"
    validity_period: 14400  # 4 hours
    
  rate_limiting:
    messages_per_second: 10
    daily_limit_per_recipient: 5
    
  compliance:
    opt_out_keywords: ["STOP", "UNSUBSCRIBE", "CANCEL"]
    opt_in_required: true
    quiet_hours:
      start: "21:00"
      end: "09:00"
      timezone: "America/New_York"
```

## Message Templates

### Notification Templates

```yaml
templates:
  order_confirmation:
    content: |
      {{company}}: Your order #{{order_id}} has been confirmed!
      Total: ${{total}}
      Track: {{tracking_url}}
      Reply HELP for assistance.
    max_length: 160
    
  shipping_update:
    content: |
      {{company}}: Your order #{{order_id}} has shipped!
      Carrier: {{carrier}}
      Tracking: {{tracking_number}}
      Delivery: {{estimated_date}}
    
  appointment_reminder:
    content: |
      Reminder: Your appointment with {{provider}} is tomorrow at {{time}}.
      Location: {{address}}
      Reply C to confirm or R to reschedule.
    
  two_factor:
    content: |
      Your {{company}} verification code is: {{code}}
      This code expires in 10 minutes.
      Don't share this code with anyone.
```

### Conversational Templates

```yaml
two_way_messaging:
  welcome:
    trigger: opt_in
    response: |
      Welcome to {{company}} updates! 
      You'll receive order and shipping notifications.
      Reply HELP for commands or STOP to unsubscribe.
      
  help:
    trigger: ["HELP", "?", "INFO"]
    response: |
      {{company}} SMS Commands:
      STATUS - Check order status
      TRACK - Get tracking info
      SUPPORT - Contact support
      STOP - Unsubscribe
      
  status_inquiry:
    trigger: ["STATUS", "ORDER"]
    action: lookup_order
    response: |
      Order #{{order_id}}: {{status}}
      {{#if tracking}}
      Tracking: {{tracking_url}}
      {{/if}}
      
  unsubscribe:
    trigger: ["STOP", "UNSUBSCRIBE"]
    action: opt_out
    response: |
      You've been unsubscribed from {{company}} messages.
      Reply START to resubscribe anytime.
```

## Verification (2FA)

### Verify API Integration

```yaml
verification_config:
  channel: sms  # or: call, email, whatsapp
  
  code_settings:
    length: 6
    expiry_minutes: 10
    
  rate_limits:
    max_attempts: 5
    lockout_minutes: 30
    
  templates:
    sms: "Your {{company}} code is {{code}}"
    call: "Your verification code is {{code_spoken}}"
```

### Verification Flow

```javascript
// Start Verification
const verification = await twilio.verify.v2
  .services('VA...')
  .verifications
  .create({
    to: '+1234567890',
    channel: 'sms',
    customCode: '123456', // Optional
    locale: 'en'
  });

// Check Verification
const check = await twilio.verify.v2
  .services('VA...')
  .verificationChecks
  .create({
    to: '+1234567890',
    code: '123456'
  });

// Result
if (check.status === 'approved') {
  // Verification successful
} else {
  // Invalid code
}
```

## Voice Automation

### Outbound Calls

```yaml
voice_config:
  outbound_call:
    from: "+1234567890"
    twiml_url: "https://api.example.com/voice/script"
    status_callback: "https://api.example.com/voice/status"
    timeout: 30
    record: true
    
  twiml_script: |
    <?xml version="1.0" encoding="UTF-8"?>
    <Response>
      <Say voice="alice">
        Hello {{name}}, this is a reminder about your
        appointment tomorrow at {{time}}.
      </Say>
      <Gather numDigits="1" action="/handle-response">
        <Say>Press 1 to confirm, 2 to reschedule.</Say>
      </Gather>
    </Response>
```

### IVR Menu

```yaml
ivr_menu:
  greeting: |
    Thank you for calling {{company}}.
    For sales, press 1.
    For support, press 2.
    For billing, press 3.
    To speak with an operator, press 0.
    
  routing:
    - digit: "1"
      action: transfer
      destination: "+1987654321"
      queue: "sales"
      
    - digit: "2"
      action: transfer
      destination: "+1876543210"
      queue: "support"
      
    - digit: "3"
      action: transfer
      destination: "+1765432109"
      queue: "billing"
      
    - digit: "0"
      action: operator
      fallback: voicemail
```

## Bulk Messaging

### Campaign Configuration

```yaml
bulk_campaign:
  name: "Holiday Promotion"
  
  audience:
    source: segment
    filter:
      opted_in: true
      last_purchase: "> 30_days"
      
  message:
    template: holiday_promo
    variables:
      discount_code: "HOLIDAY20"
      
  schedule:
    start_time: "2024-11-25T10:00:00"
    timezone: "America/New_York"
    batch_size: 100
    delay_between_batches: 60  # seconds
    
  tracking:
    delivery_report: true
    click_tracking: true
    conversion_tracking: true
```

### Broadcast Status

```
CAMPAIGN STATUS: Holiday Promotion
═══════════════════════════════════════

Progress: ████████████████░░░░ 78%

DELIVERY STATS:
Sent:        7,800
Delivered:   7,450 (95.5%)
Failed:      125 (1.6%)
Pending:     225 (2.9%)

ENGAGEMENT:
Clicks:      1,245 (16.7%)
Replies:     89 (1.2%)
Opt-outs:    23 (0.3%)

ERRORS:
Invalid Number:  45
Unsubscribed:    52
Carrier Block:   18
Rate Limited:    10

ESTIMATED COMPLETION: 25 minutes
```

## Phone Number Management

### Number Lookup

```yaml
number_lookup:
  capabilities:
    - carrier_info
    - caller_name
    - line_type
    
  validation:
    - check_format
    - verify_active
    - detect_landline_vs_mobile
    
  example_response:
    phone_number: "+14155551234"
    country_code: "US"
    carrier:
      name: "Verizon"
      type: "mobile"
    caller_name: "John Doe"
    valid: true
```

### Number Provisioning

```yaml
number_management:
  search_criteria:
    country: "US"
    area_code: "415"
    capabilities: ["SMS", "MMS", "Voice"]
    
  purchase:
    phone_number: "+14155559999"
    friendly_name: "Marketing Line"
    sms_url: "https://api.example.com/sms/incoming"
    voice_url: "https://api.example.com/voice/incoming"
```

## Analytics Dashboard

```
SMS ANALYTICS - LAST 30 DAYS
═══════════════════════════════════════

VOLUME:
Sent:        45,230
Delivered:   43,456 (96.1%)
Failed:      1,774 (3.9%)

BY TYPE:
Notifications  ████████████░░░░ 62%
Marketing      ██████░░░░░░░░░░ 23%
2FA            ████░░░░░░░░░░░░ 15%

DELIVERY BY CARRIER:
Verizon     ████████████████ 97%
AT&T        ███████████████░ 95%
T-Mobile    ██████████████░░ 94%
Sprint      █████████████░░░ 92%

COST:
Total Spend:     $1,245.67
Per Message:     $0.0275
Per Delivered:   $0.0287

ENGAGEMENT:
Link Clicks:     3,456 (7.9%)
Replies:         892 (2.1%)
Opt-outs:        56 (0.1%)
```

## API Examples

### Send SMS

```javascript
// Simple SMS
const message = await twilio.messages.create({
  body: 'Hello from Twilio!',
  from: '+1234567890',
  to: '+0987654321',
  statusCallback: 'https://api.example.com/sms/status'
});

// With Messaging Service (recommended for scale)
const message = await twilio.messages.create({
  body: 'Order confirmed!',
  messagingServiceSid: 'MG...',
  to: '+0987654321'
});

// MMS with Media
const mms = await twilio.messages.create({
  body: 'Check out this image!',
  from: '+1234567890',
  to: '+0987654321',
  mediaUrl: ['https://example.com/image.jpg']
});
```

### Handle Incoming SMS

```javascript
// Express webhook handler
app.post('/sms/incoming', (req, res) => {
  const { From, Body } = req.body;
  
  const twiml = new twilio.twiml.MessagingResponse();
  
  if (Body.toUpperCase() === 'STATUS') {
    twiml.message('Your order is on the way!');
  } else {
    twiml.message('Thanks for your message. We\'ll respond shortly.');
  }
  
  res.type('text/xml');
  res.send(twiml.toString());
});
```

## Best Practices

1. **Get Consent**: Always have opt-in before messaging
2. **Include Opt-Out**: STOP keyword in every message
3. **Respect Quiet Hours**: Don't message late night
4. **Validate Numbers**: Use Lookup API before sending
5. **Handle Failures**: Retry logic for transient errors
6. **Monitor Delivery**: Track delivery rates by carrier
7. **Stay Compliant**: Follow TCPA/CTIA guidelines
8. **Use Templates**: Consistent, tested messages
