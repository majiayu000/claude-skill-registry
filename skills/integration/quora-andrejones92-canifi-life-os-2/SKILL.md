---
name: quora
description: Enables Claude to manage Quora questions, answers, and knowledge sharing
version: 1.0.0
author: Canifi
category: social
---

# Quora Skill

## Overview
Automates Quora operations including asking questions, writing answers, following topics, and engaging with the knowledge-sharing community through browser automation.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/quora/install.sh | bash
```

Or manually:
```bash
cp -r skills/quora ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set QUORA_EMAIL "your-email@example.com"
canifi-env set QUORA_PASSWORD "your-password"
```

## Privacy & Authentication

**Your credentials, your choice.** Canifi LifeOS respects your privacy.

### Option 1: Manual Browser Login (Recommended)
If you prefer not to share credentials with Claude Code:
1. Complete the [Browser Automation Setup](/setup/automation) using CDP mode
2. Login to the service manually in the Playwright-controlled Chrome window
3. Claude will use your authenticated session without ever seeing your password

### Option 2: Environment Variables
If you're comfortable sharing credentials, you can store them locally:
```bash
canifi-env set SERVICE_EMAIL "your-email"
canifi-env set SERVICE_PASSWORD "your-password"
```

**Note**: Credentials stored in canifi-env are only accessible locally on your machine and are never transmitted.

## Capabilities
- Ask questions
- Write and edit answers
- Upvote and downvote content
- Follow topics and users
- Search questions and answers
- Create Spaces
- Share content
- View analytics for answers

## Usage Examples

### Example 1: Answer a Question
```
User: "Answer that question about Python best practices"
Claude: I'll write that answer.
- Navigate to question
- Click Answer
- Write comprehensive response
- Add relevant details
- Submit answer
```

### Example 2: Ask a Question
```
User: "Ask a question on Quora about startup funding"
Claude: I'll post that question.
- Navigate to Quora
- Click Add Question
- Write well-formed question
- Add to relevant topics
- Submit question
```

### Example 3: Search Topics
```
User: "Find Quora content about machine learning"
Claude: I'll search for that topic.
- Navigate to search
- Search "machine learning"
- Browse questions and answers
- Present top content
```

### Example 4: Follow Topic
```
User: "Follow the Entrepreneurship topic on Quora"
Claude: I'll follow that topic.
- Search for topic
- Navigate to Entrepreneurship topic page
- Click Follow
- Confirm following
```

## Authentication Flow
1. Navigate to quora.com via Playwright MCP
2. Enter email and password from canifi-env
3. Handle 2FA if enabled (notify user via iMessage)
4. Verify feed access
5. Maintain session cookies

## Error Handling
- **Login Failed**: Clear cookies, verify credentials
- **Session Expired**: Re-authenticate automatically
- **2FA Required**: iMessage for verification code
- **Answer Rejected**: Check quality guidelines
- **Question Duplicate**: Link to existing question
- **Rate Limited**: Wait before posting
- **Topic Not Found**: Search with alternatives
- **Edit Window Closed**: May need to add new answer

## Self-Improvement Instructions
When encountering new Quora features:
1. Document new UI elements
2. Add support for new content types
3. Log successful answer patterns
4. Update for Quora changes

## Notes
- Quora values quality answers
- Answers can be edited indefinitely
- Spaces are community pages
- Quora Partner Program for monetization
- Anonymous posting available
- Credentials add credibility
- Topics help categorize content
