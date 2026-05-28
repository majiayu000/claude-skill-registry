---
name: reply-to-text
description: Review text message conversations with a specified contact and send appropriate replies with cheerful tone and humor using Arlen's authentic writing style. This skill should be used when the user says "reply to [name]'s text", "respond to [name]", "text [name] back", or wants to send contextual replies to contacts. Automatically handles contact lookup and conversation review via subagent delegation. Integrates email skill writing style guide for authentic voice. Considers ALL messages received from contact since last reply (not just latest). TRIGGER PHRASES - "reply to", "respond to", "text back", "answer [name]'s message".
version: 1.2.0
---

# Reply To Text

## Purpose

Review text message conversation history with a specified contact and send contextually appropriate replies with a cheerful tone and a bit of humor. This skill delegates to a subagent that uses the text-message skill to analyze the conversation and craft an engaging response.

## When to Use This Skill

Use this skill when:
- User requests to reply to a text message from a specific contact
- User wants to review a conversation before responding
- User asks to send a contextual reply to someone
- Keywords detected: "reply to text", "respond to [name]", "text back [name]", "answer [name]'s message"

**Trigger Patterns**:
- "Reply to [contact name]'s text"
- "Respond to [contact name]"
- "Text [contact name] back"
- "Answer [contact name]'s message"
- "Send a reply to [contact name]"

## Core Workflow

### 1. Contact Identification

**Contact Specified**:
```
User: "Reply to Michele Berry's text"

Parse contact name: "Michele Berry"
Proceed to subagent delegation
```

**No Contact Specified**:
```
User: "Reply to my latest text"

Prompt: "Which contact would you like to reply to?"
Wait for user response with contact name
Proceed to subagent delegation
```

### 2. Subagent Delegation

Use the Task tool to spawn a specialized subagent with the following configuration:

**Subagent Type**: `general-purpose`

**Subagent Prompt Template**:
```
Use the text-message skill to complete this task:

1. Review the recent conversation with [CONTACT_NAME]
2. Analyze ALL messages received from the contact since the last reply (not just the latest one)
   - Identify all messages from them that haven't been responded to yet
   - Consider the full context of everything they've said
   - Note if there are multiple topics or questions to address
3. Craft an appropriate reply using Arlen's authentic writing style:
   - Responds to ALL points they raised (not just the latest message)
   - Maintains a cheerful, friendly tone
   - Includes a bit of humor when appropriate
   - Feels natural and conversational
   - Follows Arlen's texting voice (see Writing Style Integration below)
4. Send the reply using the text-message skill

Important guidelines:
- Read enough of the conversation to identify where the last reply from Arlen was
- Consider ALL messages from the contact since that last reply
- If they sent multiple messages, address all relevant points in your response
- Match the conversational style (casual vs formal)
- Avoid over-explaining or being too verbose
- Keep humor light and appropriate
- Ensure the reply feels authentic to Arlen's voice
- Reference the writing style guide: ~/.claude/skills/email/references/writing_style_guide.md
- Adapt email style patterns to texting context (more casual, briefer, friendly)
```

**Delegation Pattern**:
```
Task(
  subagent_type="general-purpose",
  description="Review and reply to text",
  prompt="Use the text-message skill to review the conversation with [CONTACT_NAME] and send a cheerful, humorous reply that responds appropriately to ALL messages they've sent since the last reply (not just the most recent one)."
)
```

### 3. Result Confirmation

Once the subagent completes:
- Confirm that the reply was sent successfully
- Display what message was sent
- Note any relevant context from the conversation

## Workflow Examples

### Example 1: Named Contact
```
User: "Reply to Leah Burt's text"

Steps:
1. Parse contact name: "Leah Burt"
2. Spawn subagent with prompt:
   "Use the text-message skill to review the conversation with Leah Burt
   and send a cheerful, humorous reply that responds appropriately to
   ALL messages they've sent since the last reply."
3. Subagent:
   - Uses text-message skill to read recent messages
   - Identifies all messages from Leah since Arlen's last reply
   - Analyzes full conversation context
   - Crafts appropriate reply addressing all points
   - Sends message
4. Confirm completion: "✅ Reply sent to Leah Burt: [message preview]"
```

### Example 2: No Contact Specified
```
User: "Reply to that text message"

Steps:
1. Prompt: "Which contact would you like to reply to?"
2. User responds: "Michele Berry"
3. Spawn subagent with prompt:
   "Use the text-message skill to review the conversation with Michele Berry
   and send a cheerful, humorous reply that responds appropriately to
   ALL messages they've sent since the last reply."
4. Subagent completes workflow
5. Confirm completion
```

### Example 3: Multiple Conversations
```
User: "Reply to both Leah and Michele"

Steps:
1. Parse contacts: ["Leah Burt", "Michele Berry"]
2. For each contact, spawn separate subagent:
   - Subagent 1: Handle Leah Burt's conversation
   - Subagent 2: Handle Michele Berry's conversation
3. Run subagents in parallel
4. Confirm completion for both:
   "✅ Replies sent:
   - Leah Burt: [preview]
   - Michele Berry: [preview]"
```

## Writing Style Integration

**Arlen's Authentic Voice for Texting** - This skill uses Arlen's personal writing style adapted for text messaging.

**Style Guide Reference**: `~/.claude/skills/email/references/writing_style_guide.md`

**Text Messaging Adaptations**:
- **More casual than email** - Texts are brief and conversational
- **Direct and friendly** - Get to the point, be warm
- **Natural language** - Use "hey", "got it", "sounds good"
- **Brief responses** - No need for formal structure like emails
- **Emoji when appropriate** - Use sparingly but naturally (👍, 😊, etc.)
- **No signatures** - Just send the message without "-Arlen"

**Tone Characteristics**:
- Cheerful and positive
- Helpful and supportive
- Light humor when contextually appropriate
- Professional when context requires, casual when appropriate
- Responsive to the other person's energy and style

**Example Adaptations**:
```
Email style: "Hi Mark, I've successfully integrated the database connection. Let me know if you run into any issues. -Arlen"
Text style: "Hey! Got the database integrated 👍 Let me know if any issues come up"

Email style: "Thank you for the update. I'll review this and get back to you by end of day."
Text style: "Thanks! Will review and get back to you today"

Email style: "I'm not sure I understand why this is needed. Could you provide more details?"
Text style: "Can you give me more details on why this is needed?"
```

## Integration with Text-Message Skill

The subagent will automatically use the text-message skill to:

1. **Look up contact** via contacts skill if name provided
2. **Read conversation history** using `read_messages.sh`
3. **Analyze context** to understand the conversation flow
4. **Apply Arlen's texting style** from writing style guide
5. **Craft reply** that is contextually appropriate, cheerful, and authentic
6. **Send message** using `send_message.sh`

The text-message skill handles all the technical details:
- Contact phone number resolution
- Message history retrieval
- Phone number formatting
- Message sending via Apple Messages
- Writing style guide integration

## Best Practices

### Tone Guidelines

**Cheerful**:
- Use positive language and enthusiasm
- Include friendly expressions
- Show genuine interest in the conversation

**Humorous**:
- Add light jokes or playful observations when appropriate
- Use self-deprecating humor occasionally
- Keep humor contextual and natural
- Avoid forced or excessive jokes

**Conversational**:
- Match the contact's communication style
- Use contractions and casual language (but remember apostrophes may cause send failures)
- Keep responses concise but warm
- Show personality

### Reply Crafting Strategy

1. **Acknowledge**: Respond directly to what they said
2. **Add Value**: Contribute something new to the conversation
3. **Engage**: Give them something to respond to if appropriate
4. **Keep It Light**: Maintain positive, friendly energy

### Subagent Guidance

Provide clear guidance to the subagent:
- Review enough message history to understand context (10-20 recent messages recommended)
- Identify where Arlen's last outgoing message was in the conversation
- Consider ALL messages from the contact since that last reply
- Address all questions, topics, or points they raised in their message(s)
- Consider the relationship with the contact (friend, family, professional)
- Match their energy level and conversation style
- Avoid overthinking - natural replies are best
- If they sent multiple messages, acknowledge the full scope of what they said

## Error Handling

**Contact Not Found**:
```
Subagent reports: "Contact [name] not found in contacts"

Response to user:
"❌ Could not find contact '[name]' in your contacts.
Please provide the correct name or phone number."

Wait for user clarification before retrying
```

**No Recent Messages**:
```
Subagent reports: "No recent messages from [contact]"

Response to user:
"ℹ️ No recent message history found with [contact].
Would you like to send a new message instead?"

Offer to use regular text-message skill instead
```

**Send Failure**:
```
Subagent reports: "Failed to send message to [contact]"

Response to user:
"❌ Failed to send reply to [contact]. Error: [details]
Would you like to try again or revise the message?"

Offer to retry or manually compose message
```

## Limitations

- **macOS Only**: Requires Apple Messages app
- **Contact Dependency**: Contact must exist in Google Contacts or phone number must be provided
- **Message History Access**: Requires Full Disk Access permissions for Terminal
- **Subagent Autonomy**: Replies are crafted by subagent based on guidelines; user can review afterwards
- **Humor Variance**: Quality and appropriateness of humor depends on subagent's interpretation

## Quick Reference

**Basic Usage**:
```
"Reply to [contact name]'s text"
```

**Subagent Delegation**:
```
Task(
  subagent_type="general-purpose",
  description="Review and reply to text",
  prompt="Use the text-message skill to review the conversation
          with [CONTACT_NAME] and send a cheerful, humorous reply
          that addresses ALL messages received since the last reply."
)
```

**Confirmation Pattern**:
```
✅ Reply sent to [Contact Name]: "[message preview]"
```

## Version History

- **1.2.0** (2025-11-02) - **COMPREHENSIVE MESSAGE HANDLING**: Updated skill to explicitly consider ALL messages received from a contact since the last reply, not just the latest message. Subagent now identifies where the last outgoing reply was and addresses all subsequent messages from the contact. Enhanced guidance to review 10-20 messages, identify all unreplied messages, and craft responses that address the full scope of what the contact said.
- **1.1.0** (2025-11-01) - **WRITING STYLE INTEGRATION**: Added comprehensive "Writing Style Integration" section that documents how Arlen's authentic voice is applied to text messaging. Includes text messaging adaptations from email style guide, tone characteristics, example conversions, and integration with text-message skill. Subagent prompts updated to reference writing style guide. Reference: `~/.claude/skills/email/references/writing_style_guide.md`
- **1.0.0** (2025-11-01) - Initial reply-to-text skill creation with subagent delegation, conversation review, and cheerful reply generation

---

**Version**: 1.2.0
**Dependencies**: text-message skill, contacts skill, Task tool with general-purpose subagent, email skill writing style guide
