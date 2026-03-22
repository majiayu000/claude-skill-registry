---
name: whatsapp-automation
description: "WhatsApp Business automation - customer support, notifications, chatbots, and broadcast messaging"
version: "1.0.0"
author: claude-office-skills
license: MIT

category: messaging
tags:
  - whatsapp
  - business
  - chatbot
  - customer-support
  - automation
department: Customer Service

models:
  recommended:
    - claude-sonnet-4

mcp:
  server: whatsapp-mcp
  tools:
    - whatsapp_send_message
    - whatsapp_send_template
    - whatsapp_get_media

capabilities:
  - message_automation
  - chatbot_flows
  - broadcast_messaging
  - customer_support
  - order_notifications

languages:
  - en
  - zh

related_skills:
  - telegram-bot
  - crm-automation
  - email-marketing
---

# WhatsApp Automation

Automate WhatsApp Business communications including customer support, notifications, chatbots, and broadcast messaging. Based on n8n's WhatsApp integration templates.

## Overview

This skill covers:
- WhatsApp Business API setup
- Automated chatbot flows
- Order/shipping notifications
- Customer support automation
- Broadcast messaging

---

## Setup & Configuration

### WhatsApp Business API

```yaml
setup_requirements:
  1. meta_business_account:
      - Create at business.facebook.com
      - Verify business
      
  2. whatsapp_business_api:
      - Access through Meta Developer Portal
      - Create WhatsApp Business App
      - Get Phone Number ID
      - Get Access Token
      
  3. webhook_configuration:
      - Set callback URL
      - Verify token
      - Subscribe to messages
      
  4. message_templates:
      - Create templates in Business Manager
      - Wait for approval (24-48h)
```

### Message Templates

```yaml
template_categories:
  transactional:
    - order_confirmation
    - shipping_update
    - delivery_notification
    - appointment_reminder
    
  marketing:
    - promotional_offer
    - product_launch
    - newsletter
    
  utility:
    - account_verification
    - password_reset
    - payment_reminder
    
template_example:
  name: "order_confirmation"
  language: "en"
  category: "TRANSACTIONAL"
  components:
    - type: HEADER
      format: TEXT
      text: "Order Confirmed! 🎉"
      
    - type: BODY
      text: |
        Hi {{1}},
        
        Your order #{{2}} has been confirmed!
        
        Items: {{3}}
        Total: {{4}}
        
        We'll notify you when it ships.
        
    - type: FOOTER
      text: "Reply HELP for support"
      
    - type: BUTTONS
      buttons:
        - type: URL
          text: "Track Order"
          url: "https://example.com/track/{{1}}"
```

---

## Chatbot Flows

### Customer Support Bot

```yaml
chatbot_flow:
  name: "Customer Support"
  
  welcome:
    trigger: first_message
    response: |
      👋 Welcome to {Company} Support!
      
      How can I help you today?
      
      1️⃣ Track Order
      2️⃣ Return/Exchange
      3️⃣ Product Questions
      4️⃣ Speak to Agent
      
      Reply with a number to continue.
      
  flows:
    track_order:
      trigger: "1" OR "track" OR "order"
      steps:
        - ask: "Please enter your order number:"
        - validate: order_number_format
        - lookup: order_status
        - respond: |
            📦 *Order #{order_number}*
            
            Status: {status}
            {if_shipped: Tracking: {tracking_number}}
            Estimated delivery: {eta}
            
            [Track Package]({tracking_url})
            
    return_exchange:
      trigger: "2" OR "return" OR "exchange"
      steps:
        - ask: "Order number for return?"
        - check: return_eligibility
        - if_eligible:
            respond: return_instructions
        - if_not:
            respond: contact_support
            
    product_questions:
      trigger: "3" OR "product" OR "question"
      steps:
        - ai_response:
            model: gpt-4
            context: product_faq_knowledge_base
            
    agent_handoff:
      trigger: "4" OR "agent" OR "human"
      steps:
        - check: agent_availability
        - if_available:
            transfer: to_live_agent
            notify: "#support-queue"
        - if_unavailable:
            respond: "Our team is currently unavailable. Leave a message and we'll get back to you within 24 hours."
            create: support_ticket
```

### AI-Powered Responses

```yaml
ai_chatbot:
  model: gpt-4
  
  system_prompt: |
    You are a WhatsApp customer support agent for {Company}.
    
    Guidelines:
    - Be helpful and friendly
    - Keep responses concise (WhatsApp prefers short messages)
    - Use emojis appropriately
    - If you can't help, offer to connect with a human agent
    - Never make up information about orders or products
    
    You have access to:
    - Order lookup
    - Product catalog
    - FAQ knowledge base
    
  tools:
    - lookup_order: by order number
    - search_products: by keyword
    - check_inventory: by product id
    - create_ticket: for complex issues
    
  escalation_triggers:
    - sentiment: very_negative
    - keywords: ["complaint", "refund", "angry", "sue"]
    - loop_detected: same_question_3x
```

---

## Notification Workflows

### Order Notifications

```yaml
order_notifications:
  order_placed:
    trigger: shopify_order_created
    template: order_confirmation
    variables:
      - customer_name
      - order_number
      - items_summary
      - total_amount
      
  payment_received:
    trigger: payment_captured
    message: |
      ✅ Payment received for order #{order_number}!
      
      Amount: {amount}
      
      We're preparing your order now.
      
  shipped:
    trigger: fulfillment_created
    template: shipping_update
    variables:
      - tracking_number
      - carrier
      - estimated_delivery
      
  out_for_delivery:
    trigger: tracking_status_change
    condition: status == "out_for_delivery"
    message: |
      🚚 Your order is out for delivery!
      
      Expected today by {eta}.
      
      Track live: {tracking_url}
      
  delivered:
    trigger: tracking_status_change
    condition: status == "delivered"
    message: |
      📦 Your order has been delivered!
      
      We hope you love it! 
      
      [Leave a Review]({review_url})
      [Need Help?]({support_url})
```

### Appointment Reminders

```yaml
appointment_reminders:
  schedule:
    - 24_hours_before
    - 1_hour_before
    
  template: appointment_reminder
  
  24h_message: |
    📅 *Appointment Reminder*
    
    Hi {name},
    
    You have an appointment tomorrow:
    
    📍 {location}
    🕐 {time}
    👤 {provider}
    
    Reply:
    ✅ CONFIRM to confirm
    ❌ CANCEL to cancel
    📅 RESCHEDULE to change time
    
  1h_message: |
    ⏰ Your appointment is in 1 hour!
    
    {provider} at {location}
    
    See you soon!
```

---

## Broadcast Messaging

### Campaign Management

```yaml
broadcast_campaigns:
  setup:
    - import_contacts: from_crm
    - segment_audience: by_criteria
    - create_template: get_approval
    - schedule_send
    
  targeting_options:
    - all_contacts
    - by_tag: [vip, new_customer, inactive]
    - by_purchase_history
    - by_location
    - custom_segment
    
  compliance:
    - opt_in_required: true
    - opt_out_easy: reply_STOP
    - frequency_limits: per_contact_per_day
    - quiet_hours: respect_timezone
    
  tracking:
    - delivered
    - read
    - replied
    - clicked_link
    - opted_out
```

### Campaign Templates

```yaml
campaign_templates:
  promotional:
    template: |
      🎉 *Special Offer for You!*
      
      Hi {name},
      
      {offer_description}
      
      Use code: {promo_code}
      Valid until: {expiry}
      
      [Shop Now]({url})
      
      Reply STOP to unsubscribe
      
  product_launch:
    template: |
      🚀 *New Arrival Alert*
      
      {name}, check out our latest:
      
      {product_name}
      {product_description}
      
      {price}
      
      [View Product]({url})
      
  reengagement:
    template: |
      👋 *We Miss You, {name}!*
      
      It's been a while since your last visit.
      
      Here's 15% off to welcome you back:
      
      Code: COMEBACK15
      
      [Shop Now]({url})
```

---

## n8n Integration

### Workflow Example

```yaml
workflow: "WhatsApp Order Bot"

nodes:
  - name: "WhatsApp Trigger"
    type: "n8n-nodes-base.whatsAppTrigger"
    parameters:
      events: ["messages"]
      
  - name: "Parse Message"
    type: "n8n-nodes-base.code"
    parameters:
      code: |
        const message = $input.first().json;
        return {
          from: message.from,
          text: message.text.body,
          type: message.type
        };
        
  - name: "AI Response"
    type: "n8n-nodes-base.openAi"
    parameters:
      model: "gpt-4"
      messages: [
        { role: "system", content: "..." },
        { role: "user", content: "{{ $json.text }}" }
      ]
      
  - name: "Send Reply"
    type: "n8n-nodes-base.whatsApp"
    parameters:
      operation: "sendMessage"
      phoneNumberId: "{{ $env.WHATSAPP_PHONE_ID }}"
      recipientPhoneNumber: "{{ $json.from }}"
      message: "{{ $json.response }}"
```

---

## Output Example

**Request**: "Create WhatsApp order notification flow"

**Output**:

```markdown
# WhatsApp Order Notifications

## Message Templates (Need Meta Approval)

### 1. Order Confirmation
```
Hi {{1}}! 🎉

Your order #{{2}} is confirmed!

Items: {{3}}
Total: {{4}}

We'll update you when it ships.

[Track Order]({{5}})
```

### 2. Shipping Update
```
📦 Your order is on the way!

Order: #{{1}}
Carrier: {{2}}
Tracking: {{3}}

Expected delivery: {{4}}

[Track Package]({{5}})
```

### 3. Delivered
```
✅ Delivered!

Your order #{{1}} has arrived.

Love it? Leave a review!
Need help? Reply to this message.

[Review]({{2}})
```

## n8n Workflow

```yaml
trigger: Shopify Order Created
steps:
  1. Get customer phone
  2. Format order details
  3. Send WhatsApp template
  4. Log to CRM
```

## Automation Rules

- Order placed → Confirmation (immediate)
- Shipped → Tracking (immediate)
- Out for delivery → Alert (immediate)
- Delivered → Review request (1 day later)
```

---

*WhatsApp Automation Skill - Part of Claude Office Skills*
