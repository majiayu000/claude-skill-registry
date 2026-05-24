---
name: slack-api
version: 1.0.0
description: Slack bot development and workspace automation using Web API, Events API, Socket Mode, and Block Kit for building interactive messaging applications
author: workspace-hub
category: communication
type: skill
capabilities:
  - web_api_integration
  - events_api_handling
  - socket_mode_connections
  - block_kit_messages
  - interactive_components
  - slash_commands
  - modals_and_views
  - workflow_automation
  - message_threading
  - file_sharing
tools:
  - slack-bolt-python
  - slack-sdk
  - ngrok
  - curl
tags: [slack, bot, api, messaging, automation, webhooks, block-kit, events, python]
platforms: [linux, macos, windows]
related_skills:
  - teams-api
  - github-actions
  - python-scientific-computing
---

# Slack API Skill

Master Slack bot development and workspace automation using the Slack Platform. This skill covers the Web API, Events API, Socket Mode, Block Kit UI framework, and the Python Bolt SDK for building production-ready Slack applications.

## When to Use This Skill

### USE when:
- Building notification systems for CI/CD pipelines
- Creating interactive bots for team workflows
- Automating incident response and alerting
- Building approval workflows with interactive messages
- Integrating external services with Slack channels
- Creating slash commands for common operations
- Building internal tools with modal dialogs
- Implementing scheduled message automation

### DON'T USE when:
- Microsoft Teams is the primary platform (use teams-api)
- Simple one-way notifications only (use incoming webhooks directly)
- Need email-based workflows (different domain)
- Slack Enterprise Grid with complex org requirements
- Real-time gaming or high-frequency updates (consider WebSockets)

## Prerequisites

### Slack App Setup

```bash
# 1. Create a Slack App at https://api.slack.com/apps
# 2. Choose "From scratch" and select your workspace

# Required Bot Token Scopes (OAuth & Permissions):
# - chat:write          - Post messages
# - chat:write.public   - Post to channels without joining
# - channels:read       - List public channels
# - channels:history    - Read channel messages
# - groups:read         - List private channels
# - im:read             - List direct messages
# - users:read          - Access user information
# - files:write         - Upload files
# - reactions:write     - Add reactions
# - commands            - Add slash commands

# Event Subscriptions (for Events API):
# - message.channels    - Messages in public channels
# - message.groups      - Messages in private channels
# - message.im          - Direct messages
# - app_mention         - When bot is mentioned

# Interactive Components:
# - Enable in app settings
# - Set Request URL for button/select handling
```

### Python Environment Setup

```bash
# Create virtual environment
python -m venv slack-bot-env
source slack-bot-env/bin/activate  # Linux/macOS
# slack-bot-env\Scripts\activate   # Windows

# Install Slack Bolt SDK
pip install slack-bolt slack-sdk

# Install additional dependencies
pip install python-dotenv aiohttp requests

# Create requirements.txt
cat > requirements.txt << 'EOF'
slack-bolt>=1.18.0
slack-sdk>=3.21.0
python-dotenv>=1.0.0
aiohttp>=3.9.0
requests>=2.31.0
EOF

# Environment variables
cat > .env << 'EOF'
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_SIGNING_SECRET=your-signing-secret
SLACK_APP_TOKEN=xapp-your-app-token  # For Socket Mode
EOF
```

### Local Development with ngrok

```bash
# Install ngrok
brew install ngrok  # macOS
# Or download from https://ngrok.com/download

# Authenticate ngrok
ngrok config add-authtoken YOUR_AUTH_TOKEN

# Start tunnel for local development
ngrok http 3000

# Use the HTTPS URL for:
# - Event Subscriptions Request URL
# - Interactive Components Request URL
# - Slash Commands Request URL
```

## Core Capabilities

### 1. Basic Slack Bot with Bolt

```python
# app.py
# ABOUTME: Basic Slack bot using Bolt framework
# ABOUTME: Handles messages, mentions, and slash commands

import os
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

load_dotenv()

# Initialize app with bot token and signing secret
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

# Listen for messages containing "hello"
@app.message("hello")
def message_hello(message, say):
    """Respond to messages containing 'hello'"""
    user = message['user']
    say(f"Hey there <@{user}>!")

# Listen for app mentions
@app.event("app_mention")
def handle_app_mention(event, say, client):
    """Respond when bot is mentioned"""
    user = event['user']
    channel = event['channel']
    text = event['text']

    # Get user info
    user_info = client.users_info(user=user)
    user_name = user_info['user']['real_name']

    say(f"Hi {user_name}! You mentioned me with: {text}")

# Handle message events
@app.event("message")
def handle_message_events(body, logger):
    """Log all message events"""
    logger.info(f"Message event: {body}")

# Slash command handler
@app.command("/greet")
def handle_greet_command(ack, say, command):
    """Handle /greet slash command"""
    ack()  # Acknowledge command within 3 seconds

    user = command['user_id']
    text = command.get('text', 'everyone')

    say(f"<@{user}> sends greetings to {text}!")

# Error handler
@app.error
def custom_error_handler(error, body, logger):
    """Handle errors gracefully"""
    logger.exception(f"Error: {error}")
    logger.info(f"Request body: {body}")

# Run with Socket Mode (no public URL needed)
if __name__ == "__main__":
    handler = SocketModeHandler(
        app,
        os.environ.get("SLACK_APP_TOKEN")
    )
    print("Bot is running...")
    handler.start()
```

### 2. Block Kit Messages

```python
# blocks.py
# ABOUTME: Block Kit message construction utilities
# ABOUTME: Creates rich, interactive Slack messages

from slack_bolt import App
import os

app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

def create_deployment_message(
    environment: str,
    version: str,
    status: str,
    deploy_url: str,
    logs_url: str
) -> list:
    """Create a deployment notification with Block Kit"""

    status_emoji = {
        "success": ":white_check_mark:",
        "failure": ":x:",
        "in_progress": ":hourglass_flowing_sand:",
        "pending": ":clock3:"
    }

    emoji = status_emoji.get(status, ":question:")

    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": f"{emoji} Deployment {status.title()}",
                "emoji": True
            }
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": f"*Environment:*\n{environment}"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*Version:*\n{version}"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*Status:*\n{status.title()}"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*Time:*\n<!date^{int(time.time())}^{{date_short}} at {{time}}|now>"
                }
            ]
        },
        {
            "type": "divider"
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "View Deployment",
                        "emoji": True
                    },
                    "url": deploy_url,
                    "style": "primary"
                },
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "View Logs",
                        "emoji": True
                    },
                    "url": logs_url
                }
            ]
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": "Deployed by CI/CD Pipeline"
                }
            ]
        }
    ]

    return blocks

def create_approval_message(
    request_id: str,
    requester: str,
    description: str,
    details: dict
) -> list:
    """Create an approval request with interactive buttons"""

    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": ":clipboard: Approval Request",
                "emoji": True
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*Request ID:* `{request_id}`\n*Requested by:* <@{requester}>\n\n{description}"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Details:*\n" + "\n".join(
                    f"- {k}: {v}" for k, v in details.items()
                )
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "actions",
            "block_id": f"approval_{request_id}",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Approve",
                        "emoji": True
                    },
                    "style": "primary",
                    "action_id": "approve_request",
                    "value": request_id
                },
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Reject",
                        "emoji": True
                    },
                    "style": "danger",
                    "action_id": "reject_request",
                    "value": request_id
                },
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Request Info",
                        "emoji": True
                    },
                    "action_id": "request_info",
                    "value": request_id
                }
            ]
        }
    ]

    return blocks

def create_poll_message(question: str, options: list) -> list:
    """Create a poll with radio buttons"""

    option_elements = [
        {
            "text": {
                "type": "plain_text",
                "text": option,
                "emoji": True
            },
            "value": f"option_{i}"
        }
        for i, option in enumerate(options)
    ]

    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": ":bar_chart: Poll",
                "emoji": True
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*{question}*"
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "block_id": "poll_options",
            "text": {
                "type": "mrkdwn",
                "text": "Select your choice:"
            },
            "accessory": {
                "type": "radio_buttons",
                "action_id": "poll_vote",
                "options": option_elements
            }
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Submit Vote",
                        "emoji": True
                    },
                    "style": "primary",
                    "action_id": "submit_vote"
                }
            ]
        }
    ]

    return blocks

# Send deployment notification
def send_deployment_notification(channel: str):
    """Send a deployment notification to a channel"""

    blocks = create_deployment_message(
        environment="production",
        version="v2.1.0",
        status="success",
        deploy_url="https://app.example.com",
        logs_url="https://logs.example.com"
    )

    app.client.chat_postMessage(
        channel=channel,
        blocks=blocks,
        text="Deployment notification"  # Fallback for notifications
    )
```

### 3. Interactive Components and Actions

```python
# interactive.py
# ABOUTME: Handle interactive components like buttons, selects, modals
# ABOUTME: Implements approval workflows with state management

from slack_bolt import App
from datetime import datetime
import json
import os

app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

# In-memory storage (use database in production)
approval_requests = {}

@app.action("approve_request")
def handle_approve(ack, body, client, logger):
    """Handle approval button click"""
    ack()

    user = body['user']['id']
    request_id = body['actions'][0]['value']
    channel = body['channel']['id']
    message_ts = body['message']['ts']

    # Update the message to show approval
    updated_blocks = body['message']['blocks'].copy()

    # Remove action buttons
    updated_blocks = [b for b in updated_blocks if b.get('type') != 'actions']

    # Add approval status
    updated_blocks.append({
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": f":white_check_mark: *Approved* by <@{user}> at {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        }
    })

    # Update the original message
    client.chat_update(
        channel=channel,
        ts=message_ts,
        blocks=updated_blocks,
        text="Request approved"
    )

    # Store approval
    approval_requests[request_id] = {
        "status": "approved",
        "approved_by": user,
        "timestamp": datetime.now().isoformat()
    }

    logger.info(f"Request {request_id} approved by {user}")

@app.action("reject_request")
def handle_reject(ack, body, client, respond):
    """Handle rejection with reason modal"""
    ack()

    request_id = body['actions'][0]['value']
    trigger_id = body['trigger_id']

    # Open modal for rejection reason
    client.views_open(
        trigger_id=trigger_id,
        view={
            "type": "modal",
            "callback_id": f"reject_modal_{request_id}",
            "title": {
                "type": "plain_text",
                "text": "Reject Request"
            },
            "submit": {
                "type": "plain_text",
                "text": "Reject"
            },
            "close": {
                "type": "plain_text",
                "text": "Cancel"
            },
            "blocks": [
                {
                    "type": "input",
                    "block_id": "reason_block",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "rejection_reason",
                        "multiline": True,
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Enter reason for rejection..."
                        }
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Rejection Reason"
                    }
                }
            ],
            "private_metadata": json.dumps({
                "channel": body['channel']['id'],
                "message_ts": body['message']['ts'],
                "request_id": request_id
            })
        }
    )

@app.view_submission("reject_modal_.*")
def handle_reject_submission(ack, body, client, view, logger):
    """Handle rejection modal submission"""
    ack()

    # Get values from modal
    reason = view['state']['values']['reason_block']['rejection_reason']['value']
    metadata = json.loads(view['private_metadata'])
    user = body['user']['id']

    channel = metadata['channel']
    message_ts = metadata['message_ts']
    request_id = metadata['request_id']

    # Update original message
    client.chat_postMessage(
        channel=channel,
        thread_ts=message_ts,
        text=f":x: *Rejected* by <@{user}>\n*Reason:* {reason}"
    )

    # Update the original message blocks
    original_message = client.conversations_history(
        channel=channel,
        latest=message_ts,
        inclusive=True,
        limit=1
    )

    if original_message['messages']:
        updated_blocks = original_message['messages'][0].get('blocks', [])
        updated_blocks = [b for b in updated_blocks if b.get('type') != 'actions']
        updated_blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f":x: *Rejected* by <@{user}>"
            }
        })

        client.chat_update(
            channel=channel,
            ts=message_ts,
            blocks=updated_blocks,
            text="Request rejected"
        )

    logger.info(f"Request {request_id} rejected by {user}: {reason}")

@app.action("poll_vote")
def handle_poll_vote(ack, body, logger):
    """Handle poll vote selection"""
    ack()
    selected = body['actions'][0]['selected_option']['value']
    logger.info(f"Poll vote: {selected}")

@app.action("submit_vote")
def handle_submit_vote(ack, body, client, respond):
    """Handle poll submission"""
    ack()

    user = body['user']['id']

    # Get selected option from state
    state = body.get('state', {}).get('values', {})
    selected = None

    for block_id, block_values in state.items():
        for action_id, action_value in block_values.items():
            if action_value.get('selected_option'):
                selected = action_value['selected_option']

    if selected:
        respond(
            text=f"<@{user}> voted for: {selected['text']['text']}",
            response_type="in_channel"
        )
    else:
        respond(
            text="Please select an option before submitting.",
            response_type="ephemeral"
        )
```

### 4. Modals and Views

```python
# modals.py
# ABOUTME: Modal dialogs for complex user input
# ABOUTME: Multi-step workflows with view updates

from slack_bolt import App
import json
import os

app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

@app.command("/create-ticket")
def open_ticket_modal(ack, body, client):
    """Open a modal for ticket creation"""
    ack()

    client.views_open(
        trigger_id=body['trigger_id'],
        view={
            "type": "modal",
            "callback_id": "create_ticket_modal",
            "title": {
                "type": "plain_text",
                "text": "Create Ticket"
            },
            "submit": {
                "type": "plain_text",
                "text": "Create"
            },
            "close": {
                "type": "plain_text",
                "text": "Cancel"
            },
            "blocks": [
                {
                    "type": "input",
                    "block_id": "title_block",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "title_input",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Brief description of the issue"
                        }
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Title"
                    }
                },
                {
                    "type": "input",
                    "block_id": "description_block",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "description_input",
                        "multiline": True,
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Detailed description..."
                        }
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Description"
                    }
                },
                {
                    "type": "input",
                    "block_id": "priority_block",
                    "element": {
                        "type": "static_select",
                        "action_id": "priority_select",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select priority"
                        },
                        "options": [
                            {
                                "text": {"type": "plain_text", "text": "Low"},
                                "value": "low"
                            },
                            {
                                "text": {"type": "plain_text", "text": "Medium"},
                                "value": "medium"
                            },
                            {
                                "text": {"type": "plain_text", "text": "High"},
                                "value": "high"
                            },
                            {
                                "text": {"type": "plain_text", "text": "Critical"},
                                "value": "critical"
                            }
                        ]
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Priority"
                    }
                },
                {
                    "type": "input",
                    "block_id": "assignee_block",
                    "element": {
                        "type": "users_select",
                        "action_id": "assignee_select",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select assignee"
                        }
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Assignee"
                    },
                    "optional": True
                },
                {
                    "type": "input",
                    "block_id": "due_date_block",
                    "element": {
                        "type": "datepicker",
                        "action_id": "due_date_picker",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select a date"
                        }
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Due Date"
                    },
                    "optional": True
                }
            ]
        }
    )

@app.view("create_ticket_modal")
def handle_ticket_submission(ack, body, client, view, logger):
    """Handle ticket modal submission"""

    # Extract values
    values = view['state']['values']
    title = values['title_block']['title_input']['value']
    description = values['description_block']['description_input']['value']
    priority = values['priority_block']['priority_select']['selected_option']['value']
    assignee = values['assignee_block']['assignee_select'].get('selected_user')
    due_date = values['due_date_block']['due_date_picker'].get('selected_date')

    user = body['user']['id']

    # Validate input
    errors = {}
    if len(title) < 5:
        errors['title_block'] = "Title must be at least 5 characters"
    if len(description) < 10:
        errors['description_block'] = "Description must be at least 10 characters"

    if errors:
        ack(response_action="errors", errors=errors)
        return

    ack()

    # Create ticket (in real app, save to database/API)
    ticket_id = f"TICKET-{hash(title) % 10000:04d}"

    # Notify in channel
    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": f":ticket: New Ticket Created",
                "emoji": True
            }
        },
        {
            "type": "section",
            "fields": [
                {"type": "mrkdwn", "text": f"*ID:*\n`{ticket_id}`"},
                {"type": "mrkdwn", "text": f"*Priority:*\n{priority.title()}"},
                {"type": "mrkdwn", "text": f"*Created by:*\n<@{user}>"},
                {"type": "mrkdwn", "text": f"*Assignee:*\n{'<@' + assignee + '>' if assignee else 'Unassigned'}"}
            ]
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*Title:*\n{title}\n\n*Description:*\n{description}"
            }
        }
    ]

    if due_date:
        blocks.append({
            "type": "context",
            "elements": [
                {"type": "mrkdwn", "text": f":calendar: Due: {due_date}"}
            ]
        })

    # Post to tickets channel
    client.chat_postMessage(
        channel="#tickets",
        blocks=blocks,
        text=f"New ticket: {title}"
    )

    # DM creator confirmation
    client.chat_postMessage(
        channel=user,
        text=f":white_check_mark: Your ticket `{ticket_id}` has been created!"
    )

    logger.info(f"Ticket {ticket_id} created by {user}")

# Multi-step modal workflow
@app.command("/onboard")
def start_onboarding(ack, body, client):
    """Start multi-step onboarding workflow"""
    ack()

    client.views_open(
        trigger_id=body['trigger_id'],
        view={
            "type": "modal",
            "callback_id": "onboard_step_1",
            "title": {"type": "plain_text", "text": "Onboarding (1/3)"},
            "submit": {"type": "plain_text", "text": "Next"},
            "close": {"type": "plain_text", "text": "Cancel"},
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Welcome! Let's set up your profile."
                    }
                },
                {
                    "type": "input",
                    "block_id": "name_block",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "full_name"
                    },
                    "label": {"type": "plain_text", "text": "Full Name"}
                },
                {
                    "type": "input",
                    "block_id": "role_block",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "role"
                    },
                    "label": {"type": "plain_text", "text": "Role/Title"}
                }
            ]
        }
    )

@app.view("onboard_step_1")
def handle_step_1(ack, body, client, view):
    """Handle step 1 and show step 2"""

    values = view['state']['values']
    name = values['name_block']['full_name']['value']
    role = values['role_block']['role']['value']

    # Update to step 2
    ack(response_action="update", view={
        "type": "modal",
        "callback_id": "onboard_step_2",
        "title": {"type": "plain_text", "text": "Onboarding (2/3)"},
        "submit": {"type": "plain_text", "text": "Next"},
        "close": {"type": "plain_text", "text": "Cancel"},
        "private_metadata": json.dumps({"name": name, "role": role}),
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"Great, *{name}*! Now select your team."
                }
            },
            {
                "type": "input",
                "block_id": "team_block",
                "element": {
                    "type": "static_select",
                    "action_id": "team_select",
                    "options": [
                        {"text": {"type": "plain_text", "text": "Engineering"}, "value": "engineering"},
                        {"text": {"type": "plain_text", "text": "Design"}, "value": "design"},
                        {"text": {"type": "plain_text", "text": "Product"}, "value": "product"},
                        {"text": {"type": "plain_text", "text": "Operations"}, "value": "operations"}
                    ]
                },
                "label": {"type": "plain_text", "text": "Team"}
            }
        ]
    })

@app.view("onboard_step_2")
def handle_step_2(ack, body, client, view):
    """Handle step 2 and show step 3 (final)"""

    values = view['state']['values']
    previous = json.loads(view['private_metadata'])
    team = values['team_block']['team_select']['selected_option']['value']

    previous['team'] = team

    ack(response_action="update", view={
        "type": "modal",
        "callback_id": "onboard_step_3",
        "title": {"type": "plain_text", "text": "Onboarding (3/3)"},
        "submit": {"type": "plain_text", "text": "Complete"},
        "close": {"type": "plain_text", "text": "Cancel"},
        "private_metadata": json.dumps(previous),
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Almost done! Any additional info?"
                }
            },
            {
                "type": "input",
                "block_id": "bio_block",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "bio",
                    "multiline": True
                },
                "label": {"type": "plain_text", "text": "Short Bio"},
                "optional": True
            }
        ]
    })

@app.view("onboard_step_3")
def handle_final_step(ack, body, client, view, logger):
    """Complete onboarding"""
    ack()

    values = view['state']['values']
    previous = json.loads(view['private_metadata'])
    bio = values['bio_block']['bio'].get('value', 'No bio provided')

    user = body['user']['id']

    # Complete onboarding
    profile = {
        **previous,
        "bio": bio,
        "user_id": user
    }

    # Announce new team member
    client.chat_postMessage(
        channel="#general",
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f":wave: Welcome <@{user}> to the team!\n\n*Role:* {profile['role']}\n*Team:* {profile['team'].title()}\n*Bio:* {bio}"
                }
            }
        ],
        text=f"Welcome {profile['name']} to the team!"
    )

    logger.info(f"Onboarding completed for {user}: {profile}")
```

### 5. Slash Commands

```python
# commands.py
# ABOUTME: Slash command implementations
# ABOUTME: Various utility commands for team workflows

from slack_bolt import App
from datetime import datetime, timedelta
import random
import os

app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

@app.command("/standup")
def handle_standup(ack, body, client, command):
    """Start a standup thread"""
    ack()

    channel = command['channel_id']
    user = command['user_id']

    # Create standup thread
    result = client.chat_postMessage(
        channel=channel,
        blocks=[
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f":sunrise: Daily Standup - {datetime.now().strftime('%A, %B %d')}",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Please share your updates in this thread:\n\n1. :white_check_mark: What did you accomplish yesterday?\n2. :calendar: What are you working on today?\n3. :construction: Any blockers?"
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "context",
                "elements": [
                    {"type": "mrkdwn", "text": f"Started by <@{user}>"}
                ]
            }
        ],
        text="Daily Standup"
    )

    # Pin the standup
    client.pins_add(channel=channel, timestamp=result['ts'])

@app.command("/poll")
def handle_poll(ack, body, client, command):
    """Create a quick poll: /poll "Question" "Option 1" "Option 2" ..."""
    ack()

    text = command.get('text', '')

    # Parse quoted arguments
    import re
    parts = re.findall(r'"([^"]+)"', text)

    if len(parts) < 3:
        client.chat_postEphemeral(
            channel=command['channel_id'],
            user=command['user_id'],
            text='Usage: /poll "Question" "Option 1" "Option 2" "Option 3"'
        )
        return

    question = parts[0]
    options = parts[1:]

    # Create poll blocks
    option_blocks = []
    emojis = [':one:', ':two:', ':three:', ':four:', ':five:', ':six:', ':seven:', ':eight:', ':nine:']

    for i, option in enumerate(options[:9]):
        option_blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"{emojis[i]} {option}"
            }
        })

    blocks = [
        {
            "type": "header",
            "text": {"type": "plain_text", "text": ":bar_chart: Poll", "emoji": True}
        },
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": f"*{question}*"}
        },
        {"type": "divider"},
        *option_blocks,
        {"type": "divider"},
        {
            "type": "context",
            "elements": [
                {"type": "mrkdwn", "text": f"Poll by <@{command['user_id']}> | React to vote!"}
            ]
        }
    ]

    result = client.chat_postMessage(
        channel=command['channel_id'],
        blocks=blocks,
        text=f"Poll: {question}"
    )

    # Add reaction options
    for i in range(len(options[:9])):
        emoji_names = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
        client.reactions_add(
            channel=command['channel_id'],
            timestamp=result['ts'],
            name=emoji_names[i]
        )

@app.command("/remind-team")
def handle_team_reminder(ack, body, client, command):
    """Set a team reminder: /remind-team 15m Check deployment status"""
    ack()

    text = command.get('text', '').strip()
    parts = text.split(' ', 1)

    if len(parts) < 2:
        client.chat_postEphemeral(
            channel=command['channel_id'],
            user=command['user_id'],
            text='Usage: /remind-team 15m Your reminder message'
        )
        return

    time_str = parts[0]
    message = parts[1]

    # Parse time
    time_map = {'s': 1, 'm': 60, 'h': 3600}
    unit = time_str[-1]

    if unit not in time_map:
        client.chat_postEphemeral(
            channel=command['channel_id'],
            user=command['user_id'],
            text='Time format: 15s, 15m, or 2h'
        )
        return

    try:
        amount = int(time_str[:-1])
        seconds = amount * time_map[unit]
    except ValueError:
        client.chat_postEphemeral(
            channel=command['channel_id'],
            user=command['user_id'],
            text='Invalid time format'
        )
        return

    # Schedule message
    post_at = int(datetime.now().timestamp()) + seconds

    client.chat_scheduleMessage(
        channel=command['channel_id'],
        post_at=post_at,
        text=f":bell: *Reminder:* {message}\n\n_Set by <@{command['user_id']}>_"
    )

    client.chat_postEphemeral(
        channel=command['channel_id'],
        user=command['user_id'],
        text=f"Reminder scheduled for {time_str} from now!"
    )

@app.command("/random-pick")
def handle_random_pick(ack, body, client, command):
    """Randomly pick from options: /random-pick option1 option2 option3"""
    ack()

    text = command.get('text', '').strip()

    if not text:
        client.chat_postEphemeral(
            channel=command['channel_id'],
            user=command['user_id'],
            text='Usage: /random-pick option1 option2 option3'
        )
        return

    options = text.split()
    picked = random.choice(options)

    client.chat_postMessage(
        channel=command['channel_id'],
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f":game_die: <@{command['user_id']}> asked me to pick randomly from: {', '.join(options)}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f":point_right: *{picked}*"
                }
            }
        ],
        text=f"Random pick: {picked}"
    )
```

### 6. Webhooks and Incoming Messages

```python
# webhooks.py
# ABOUTME: Incoming webhook integration for external services
# ABOUTME: CI/CD notifications, alerts, and external triggers

import requests
import json
from typing import Optional, List, Dict
import hmac
import hashlib
import time

class SlackWebhook:
    """Incoming webhook client for Slack"""

    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def send(
        self,
        text: str,
        blocks: Optional[List[Dict]] = None,
        attachments: Optional[List[Dict]] = None,
        thread_ts: Optional[str] = None,
        unfurl_links: bool = True,
        unfurl_media: bool = True
    ) -> dict:
        """Send a message via webhook"""

        payload = {
            "text": text,
            "unfurl_links": unfurl_links,
            "unfurl_media": unfurl_media
        }

        if blocks:
            payload["blocks"] = blocks
        if attachments:
            payload["attachments"] = attachments
        if thread_ts:
            payload["thread_ts"] = thread_ts

        response = requests.post(
            self.webhook_url,
            json=payload,
            headers={"Content-Type": "application/json"}
        )

        response.raise_for_status()
        return {"ok": True, "status": response.status_code}

    def send_deployment_notification(
        self,
        app_name: str,
        environment: str,
        version: str,
        status: str,
        commit_sha: str,
        author: str,
        url: Optional[str] = None
    ):
        """Send a deployment notification"""

        color_map = {
            "success": "#36a64f",
            "failure": "#ff0000",
            "started": "#ffcc00",
            "pending": "#808080"
        }

        status_emoji = {
            "success": ":white_check_mark:",
            "failure": ":x:",
            "started": ":rocket:",
            "pending": ":hourglass:"
        }

        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"{status_emoji.get(status, ':grey_question:')} Deployment {status.title()}: {app_name}",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*Environment:*\n{environment}"},
                    {"type": "mrkdwn", "text": f"*Version:*\n{version}"},
                    {"type": "mrkdwn", "text": f"*Commit:*\n`{commit_sha[:8]}`"},
                    {"type": "mrkdwn", "text": f"*Author:*\n{author}"}
                ]
            }
        ]

        if url:
            blocks.append({
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "View Deployment"},
                        "url": url,
                        "style": "primary" if status == "success" else None
                    }
                ]
            })

        attachments = [
            {
                "color": color_map.get(status, "#808080"),
                "blocks": blocks
            }
        ]

        return self.send(
            text=f"Deployment {status}: {app_name} to {environment}",
            attachments=attachments
        )

    def send_alert(
        self,
        title: str,
        message: str,
        severity: str = "warning",
        source: str = "System",
        details: Optional[Dict] = None
    ):
        """Send an alert notification"""

        severity_config = {
            "critical": {"emoji": ":rotating_light:", "color": "#ff0000"},
            "error": {"emoji": ":x:", "color": "#ff4444"},
            "warning": {"emoji": ":warning:", "color": "#ffcc00"},
            "info": {"emoji": ":information_source:", "color": "#0088ff"}
        }

        config = severity_config.get(severity, severity_config["info"])

        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"{config['emoji']} {title}",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": message}
            },
            {
                "type": "context",
                "elements": [
                    {"type": "mrkdwn", "text": f"*Source:* {source} | *Severity:* {severity.upper()}"}
                ]
            }
        ]

        if details:
            detail_text = "\n".join(f"*{k}:* {v}" for k, v in details.items())
            blocks.insert(2, {
                "type": "section",
                "text": {"type": "mrkdwn", "text": detail_text}
            })

        return self.send(
            text=f"[{severity.upper()}] {title}",
            attachments=[{"color": config["color"], "blocks": blocks}]
        )

# Webhook signature verification
def verify_slack_signature(
    signing_secret: str,
    request_body: str,
    timestamp: str,
    signature: str
) -> bool:
    """Verify Slack request signature"""

    # Check timestamp to prevent replay attacks
    if abs(time.time() - int(timestamp)) > 60 * 5:
        return False

    sig_basestring = f"v0:{timestamp}:{request_body}"

    computed_signature = 'v0=' + hmac.new(
        signing_secret.encode(),
        sig_basestring.encode(),
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(computed_signature, signature)

# Usage example
if __name__ == "__main__":
    webhook = SlackWebhook("https://hooks.slack.com/services/T00/B00/XXX")

    # Send deployment notification
    webhook.send_deployment_notification(
        app_name="my-service",
        environment="production",
        version="v1.2.3",
        status="success",
        commit_sha="abc123def",
        author="developer@example.com",
        url="https://deployments.example.com/123"
    )

    # Send alert
    webhook.send_alert(
        title="High CPU Usage",
        message="Server cpu-usage has exceeded 90% for the last 5 minutes.",
        severity="warning",
        source="Monitoring",
        details={
            "Server": "prod-web-01",
            "Current Usage": "92%",
            "Threshold": "90%"
        }
    )
```

## Integration Examples

### GitHub Actions Integration

```yaml
# .github/workflows/slack-notify.yml
name: Slack Notifications

on:
  push:
    branches: [main]
  pull_request:
    types: [opened, closed, merged]
  workflow_run:
    workflows: ["CI"]
    types: [completed]

jobs:
  notify-deployment:
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    steps:
      - name: Notify Slack
        uses: slackapi/slack-github-action@v1
        with:
          payload: |
            {
              "blocks": [
                {
                  "type": "header",
                  "text": {
                    "type": "plain_text",
                    "text": ":rocket: Deployment Started"
                  }
                },
                {
                  "type": "section",
                  "fields": [
                    {"type": "mrkdwn", "text": "*Repository:*\n${{ github.repository }}"},
                    {"type": "mrkdwn", "text": "*Branch:*\n${{ github.ref_name }}"},
                    {"type": "mrkdwn", "text": "*Commit:*\n`${{ github.sha }}`"},
                    {"type": "mrkdwn", "text": "*Author:*\n${{ github.actor }}"}
                  ]
                },
                {
                  "type": "actions",
                  "elements": [
                    {
                      "type": "button",
                      "text": {"type": "plain_text", "text": "View Commit"},
                      "url": "${{ github.event.head_commit.url }}"
                    }
                  ]
                }
              ]
            }
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
          SLACK_WEBHOOK_TYPE: INCOMING_WEBHOOK
```

### FastAPI Integration

```python
# api_integration.py
# ABOUTME: FastAPI integration for Slack event handling
# ABOUTME: Webhook endpoint for Slack Events API

from fastapi import FastAPI, Request, HTTPException
from slack_bolt import App
from slack_bolt.adapter.fastapi import SlackRequestHandler
import os

# Initialize Slack app
slack_app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

# Register event handlers
@slack_app.event("message")
def handle_message(event, say):
    if "hello" in event.get("text", "").lower():
        say(f"Hi <@{event['user']}>!")

@slack_app.command("/api-status")
def handle_status(ack, respond):
    ack()
    respond("API is healthy!")

# FastAPI setup
app = FastAPI(title="Slack Bot API")
handler = SlackRequestHandler(slack_app)

@app.post("/slack/events")
async def slack_events(request: Request):
    """Handle Slack events"""
    return await handler.handle(request)

@app.post("/slack/interactions")
async def slack_interactions(request: Request):
    """Handle Slack interactive components"""
    return await handler.handle(request)

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}
```

## Best Practices

### 1. Rate Limiting

```python
# Rate limit handling
import time
from functools import wraps

def rate_limit_handler(max_retries=3, base_delay=1):
    """Decorator for handling Slack rate limits"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if "rate_limited" in str(e):
                        delay = base_delay * (2 ** attempt)
                        time.sleep(delay)
                    else:
                        raise
            raise Exception("Max retries exceeded")
        return wrapper
    return decorator

@rate_limit_handler(max_retries=3)
def send_message(client, channel, text):
    return client.chat_postMessage(channel=channel, text=text)
```

### 2. Error Handling

```python
# Comprehensive error handling
from slack_sdk.errors import SlackApiError

def safe_send_message(client, channel, text, blocks=None):
    """Send message with error handling"""
    try:
        result = client.chat_postMessage(
            channel=channel,
            text=text,
            blocks=blocks
        )
        return result
    except SlackApiError as e:
        error_code = e.response.get("error", "unknown_error")

        if error_code == "channel_not_found":
            # Handle missing channel
            raise ValueError(f"Channel {channel} not found")
        elif error_code == "not_in_channel":
            # Try to join channel first
            client.conversations_join(channel=channel)
            return client.chat_postMessage(channel=channel, text=text, blocks=blocks)
        elif error_code == "ratelimited":
            # Wait and retry
            retry_after = int(e.response.headers.get("Retry-After", 1))
            time.sleep(retry_after)
            return safe_send_message(client, channel, text, blocks)
        else:
            raise
```

### 3. Message Formatting

```python
# Safe message formatting
def escape_text(text: str) -> str:
    """Escape special characters for Slack"""
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    return text

def format_user_mention(user_id: str) -> str:
    """Format user mention"""
    return f"<@{user_id}>"

def format_channel_link(channel_id: str) -> str:
    """Format channel link"""
    return f"<#{channel_id}>"

def format_url(url: str, text: str = None) -> str:
    """Format URL with optional text"""
    if text:
        return f"<{url}|{escape_text(text)}>"
    return f"<{url}>"

def format_code_block(code: str, language: str = "") -> str:
    """Format code block"""
    return f"```{language}\n{code}\n```"
```

### 4. Token Security

```python
# Secure token management
import os
from functools import lru_cache

@lru_cache()
def get_slack_client():
    """Get cached Slack client with secure token"""
    from slack_sdk import WebClient

    token = os.environ.get("SLACK_BOT_TOKEN")
    if not token:
        raise ValueError("SLACK_BOT_TOKEN not set")

    if not token.startswith("xoxb-"):
        raise ValueError("Invalid bot token format")

    return WebClient(token=token)

# Never log tokens
import logging
class TokenFilter(logging.Filter):
    def filter(self, record):
        if hasattr(record, 'msg'):
            record.msg = str(record.msg).replace(
                os.environ.get("SLACK_BOT_TOKEN", ""), "[REDACTED]"
            )
        return True
```

## Troubleshooting

### Common Issues

**Issue: Bot not responding to messages**
```python
# Verify bot has correct scopes
# Check Event Subscriptions are enabled
# Ensure Request URL is verified

# Debug with logging
import logging
logging.basicConfig(level=logging.DEBUG)

@app.event("message")
def debug_messages(body, logger):
    logger.info(f"Received message event: {body}")
```

**Issue: Interactive components not working**
```python
# Ensure Interactive Components URL is set
# Check action_id matches handler

@app.action("button_click")  # Must match action_id in block
def handle_click(ack, body, logger):
    ack()
    logger.info(f"Button clicked: {body}")
```

**Issue: Socket Mode connection drops**
```python
# Increase connection timeout
from slack_bolt.adapter.socket_mode import SocketModeHandler

handler = SocketModeHandler(
    app,
    app_token,
    ping_interval=30  # Send ping every 30 seconds
)
```

**Issue: Message not appearing in channel**
```python
# Check channel ID format
# Verify bot is in channel

def ensure_in_channel(client, channel):
    try:
        client.conversations_info(channel=channel)
    except:
        client.conversations_join(channel=channel)
```

### Debug Commands

```bash
# Test webhook
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"text": "Test message"}' \
  $SLACK_WEBHOOK_URL

# Test bot token
curl -X POST \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  https://slack.com/api/auth.test

# List channels
curl -X GET \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  "https://slack.com/api/conversations.list?limit=10"
```

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-17 | Initial release with comprehensive Slack API patterns |

## Resources

- [Slack API Documentation](https://api.slack.com/)
- [Bolt for Python](https://slack.dev/bolt-python/)
- [Block Kit Builder](https://app.slack.com/block-kit-builder/)
- [Slack App Manifest](https://api.slack.com/reference/manifests)
- [Socket Mode](https://api.slack.com/apis/connections/socket)
- [Events API](https://api.slack.com/events-api)

---

*This skill provides production-ready patterns for Slack bot development, enabling powerful team automation and interactive workflows.*
