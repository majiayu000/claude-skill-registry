---
name: teams-api
version: 1.0.0
description: Microsoft Teams automation using Graph API, Bot Framework, Adaptive Cards, and webhooks for enterprise messaging and collaboration
author: workspace-hub
category: communication
type: skill
capabilities:
  - graph_api_integration
  - bot_framework_development
  - adaptive_cards
  - messaging_extensions
  - webhook_connectors
  - channel_management
  - meeting_automation
  - teams_apps
  - proactive_messaging
  - notification_workflows
tools:
  - microsoft-graph-sdk
  - botbuilder-python
  - azure-identity
  - requests
tags: [teams, microsoft, graph-api, bot, adaptive-cards, enterprise, messaging, azure]
platforms: [linux, macos, windows, azure]
related_skills:
  - slack-api
  - github-actions
  - azure-functions
---

# Microsoft Teams API Skill

Master Microsoft Teams automation using the Microsoft Graph API and Bot Framework. This skill covers channel messaging, adaptive cards, bot development, webhooks, and enterprise integration patterns for Microsoft 365 environments.

## When to Use This Skill

### USE when:
- Building bots for Microsoft 365 organizations
- Creating enterprise notification systems
- Integrating with Azure DevOps and Microsoft ecosystem
- Building approval workflows in Teams
- Automating meeting scheduling and management
- Creating messaging extensions for Teams apps
- Implementing compliance-aware messaging solutions
- Building internal tools with Adaptive Cards

### DON'T USE when:
- Organization uses Slack primarily (use slack-api)
- Need simple webhooks only (use incoming webhooks directly)
- No Microsoft 365 subscription available
- Building consumer-facing chat applications
- Need real-time gaming or high-frequency updates

## Prerequisites

### Azure App Registration

```bash
# 1. Go to Azure Portal -> Azure Active Directory -> App registrations
# 2. New registration:
#    - Name: "Teams Bot App"
#    - Supported account types: Accounts in this organizational directory
#    - Redirect URI: Web - https://your-app.azurewebsites.net/auth

# Required API Permissions (Microsoft Graph):
# Application permissions:
# - ChannelMessage.Send           - Send channel messages
# - Chat.ReadWrite.All            - Read/write chats
# - Team.ReadBasic.All            - Read team info
# - User.Read.All                 - Read user profiles
# - Group.Read.All                - Read group info
# - OnlineMeetings.ReadWrite.All  - Create meetings

# Delegated permissions:
# - Chat.ReadWrite                - User chat access
# - Team.ReadBasic.All            - User team access
# - ChannelMessage.Send           - User can send messages

# 3. Create client secret:
#    - Certificates & secrets -> New client secret
#    - Save the value (shown only once)
```

### Python Environment Setup

```bash
# Create virtual environment
python -m venv teams-bot-env
source teams-bot-env/bin/activate  # Linux/macOS

# Install dependencies
pip install azure-identity msgraph-sdk botbuilder-core aiohttp

# Create requirements.txt
cat > requirements.txt << 'EOF'
azure-identity>=1.14.0
msgraph-sdk>=1.0.0
botbuilder-core>=4.14.0
botbuilder-integration-aiohttp>=4.14.0
aiohttp>=3.9.0
python-dotenv>=1.0.0
requests>=2.31.0
EOF

# Environment variables
cat > .env << 'EOF'
AZURE_TENANT_ID=your-tenant-id
AZURE_CLIENT_ID=your-client-id
AZURE_CLIENT_SECRET=your-client-secret
MICROSOFT_APP_ID=your-bot-app-id
MICROSOFT_APP_PASSWORD=your-bot-password
TEAMS_WEBHOOK_URL=your-webhook-url
EOF
```

### Bot Framework Registration

```bash
# 1. Go to https://dev.botframework.com/bots/new
# 2. Or use Azure Portal -> Create a resource -> Bot Channels Registration

# Bot configuration:
# - Messaging endpoint: https://your-app.azurewebsites.net/api/messages
# - Microsoft App ID: from App Registration
# - Enable Teams channel

# For local development with ngrok:
ngrok http 3978
# Update messaging endpoint to ngrok URL
```

## Core Capabilities

### 1. Microsoft Graph API Client

```python
# graph_client.py
# ABOUTME: Microsoft Graph API client for Teams operations
# ABOUTME: Handles authentication and common API calls

from azure.identity import ClientSecretCredential
from msgraph import GraphServiceClient
from msgraph.generated.models.chat_message import ChatMessage
from msgraph.generated.models.item_body import ItemBody
from msgraph.generated.models.body_type import BodyType
import os
from dotenv import load_dotenv

load_dotenv()

class TeamsGraphClient:
    """Microsoft Graph client for Teams operations"""

    def __init__(self):
        self.credential = ClientSecretCredential(
            tenant_id=os.environ["AZURE_TENANT_ID"],
            client_id=os.environ["AZURE_CLIENT_ID"],
            client_secret=os.environ["AZURE_CLIENT_SECRET"]
        )

        self.client = GraphServiceClient(
            credentials=self.credential,
            scopes=["https://graph.microsoft.com/.default"]
        )

    async def send_channel_message(
        self,
        team_id: str,
        channel_id: str,
        content: str,
        content_type: str = "html"
    ):
        """Send a message to a Teams channel"""

        message = ChatMessage(
            body=ItemBody(
                content_type=BodyType.Html if content_type == "html" else BodyType.Text,
                content=content
            )
        )

        result = await self.client.teams.by_team_id(team_id) \
            .channels.by_channel_id(channel_id) \
            .messages.post(message)

        return result

    async def send_chat_message(
        self,
        chat_id: str,
        content: str
    ):
        """Send a message to a chat (1:1 or group)"""

        message = ChatMessage(
            body=ItemBody(
                content_type=BodyType.Html,
                content=content
            )
        )

        result = await self.client.chats.by_chat_id(chat_id) \
            .messages.post(message)

        return result

    async def list_teams(self):
        """List all teams the app has access to"""
        result = await self.client.groups.get()
        teams = [g for g in result.value if g.resource_provisioning_options
                 and "Team" in g.resource_provisioning_options]
        return teams

    async def list_channels(self, team_id: str):
        """List channels in a team"""
        result = await self.client.teams.by_team_id(team_id) \
            .channels.get()
        return result.value

    async def get_channel_messages(
        self,
        team_id: str,
        channel_id: str,
        top: int = 50
    ):
        """Get recent messages from a channel"""

        result = await self.client.teams.by_team_id(team_id) \
            .channels.by_channel_id(channel_id) \
            .messages.get(
                request_configuration=lambda config:
                    setattr(config.query_parameters, 'top', top)
            )

        return result.value

    async def reply_to_message(
        self,
        team_id: str,
        channel_id: str,
        message_id: str,
        content: str
    ):
        """Reply to a channel message"""

        reply = ChatMessage(
            body=ItemBody(
                content_type=BodyType.Html,
                content=content
            )
        )

        result = await self.client.teams.by_team_id(team_id) \
            .channels.by_channel_id(channel_id) \
            .messages.by_chat_message_id(message_id) \
            .replies.post(reply)

        return result

    async def create_online_meeting(
        self,
        subject: str,
        start_time: str,
        end_time: str,
        attendees: list
    ):
        """Create an online meeting"""
        from msgraph.generated.models.online_meeting import OnlineMeeting
        from msgraph.generated.models.meeting_participants import MeetingParticipants
        from msgraph.generated.models.meeting_participant_info import MeetingParticipantInfo
        from msgraph.generated.models.identity_set import IdentitySet
        from msgraph.generated.models.identity import Identity

        participant_list = [
            MeetingParticipantInfo(
                identity=IdentitySet(
                    user=Identity(id=attendee)
                )
            )
            for attendee in attendees
        ]

        meeting = OnlineMeeting(
            subject=subject,
            start_date_time=start_time,
            end_date_time=end_time,
            participants=MeetingParticipants(
                attendees=participant_list
            )
        )

        result = await self.client.me.online_meetings.post(meeting)
        return result

    async def get_user_by_email(self, email: str):
        """Get user details by email"""
        result = await self.client.users.by_user_id(email).get()
        return result

# Usage example
async def main():
    client = TeamsGraphClient()

    # List teams
    teams = await client.list_teams()
    for team in teams:
        print(f"Team: {team.display_name} ({team.id})")

    # Send channel message
    if teams:
        team_id = teams[0].id
        channels = await client.list_channels(team_id)
        if channels:
            channel_id = channels[0].id
            await client.send_channel_message(
                team_id,
                channel_id,
                "<b>Hello from Python!</b> This is an automated message."
            )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

### 2. Adaptive Cards

```python
# adaptive_cards.py
# ABOUTME: Adaptive Card construction for rich Teams messages
# ABOUTME: Interactive cards with actions and data binding

from typing import Dict, List, Optional, Any
import json

class AdaptiveCardBuilder:
    """Builder for Adaptive Cards"""

    def __init__(self, version: str = "1.4"):
        self.card = {
            "type": "AdaptiveCard",
            "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
            "version": version,
            "body": [],
            "actions": []
        }

    def add_text_block(
        self,
        text: str,
        size: str = "default",
        weight: str = "default",
        color: str = "default",
        wrap: bool = True
    ):
        """Add a text block"""
        self.card["body"].append({
            "type": "TextBlock",
            "text": text,
            "size": size,
            "weight": weight,
            "color": color,
            "wrap": wrap
        })
        return self

    def add_fact_set(self, facts: Dict[str, str]):
        """Add a fact set (key-value pairs)"""
        self.card["body"].append({
            "type": "FactSet",
            "facts": [
                {"title": k, "value": v}
                for k, v in facts.items()
            ]
        })
        return self

    def add_column_set(self, columns: List[Dict]):
        """Add a column set for side-by-side content"""
        self.card["body"].append({
            "type": "ColumnSet",
            "columns": columns
        })
        return self

    def add_image(
        self,
        url: str,
        size: str = "auto",
        alt_text: str = ""
    ):
        """Add an image"""
        self.card["body"].append({
            "type": "Image",
            "url": url,
            "size": size,
            "altText": alt_text
        })
        return self

    def add_action_submit(
        self,
        title: str,
        data: Dict[str, Any],
        style: str = "default"
    ):
        """Add a submit action button"""
        self.card["actions"].append({
            "type": "Action.Submit",
            "title": title,
            "data": data,
            "style": style
        })
        return self

    def add_action_open_url(
        self,
        title: str,
        url: str
    ):
        """Add an open URL action"""
        self.card["actions"].append({
            "type": "Action.OpenUrl",
            "title": title,
            "url": url
        })
        return self

    def add_action_show_card(
        self,
        title: str,
        card: Dict
    ):
        """Add a show card action (nested card)"""
        self.card["actions"].append({
            "type": "Action.ShowCard",
            "title": title,
            "card": card
        })
        return self

    def add_input_text(
        self,
        id: str,
        placeholder: str = "",
        is_multiline: bool = False,
        label: str = ""
    ):
        """Add a text input"""
        input_element = {
            "type": "Input.Text",
            "id": id,
            "placeholder": placeholder,
            "isMultiline": is_multiline
        }
        if label:
            input_element["label"] = label
        self.card["body"].append(input_element)
        return self

    def add_input_choice_set(
        self,
        id: str,
        choices: List[Dict[str, str]],
        is_multi_select: bool = False,
        style: str = "compact",
        label: str = ""
    ):
        """Add a choice set (dropdown/radio)"""
        input_element = {
            "type": "Input.ChoiceSet",
            "id": id,
            "choices": choices,
            "isMultiSelect": is_multi_select,
            "style": style
        }
        if label:
            input_element["label"] = label
        self.card["body"].append(input_element)
        return self

    def add_container(
        self,
        items: List[Dict],
        style: str = "default"
    ):
        """Add a container for grouping elements"""
        self.card["body"].append({
            "type": "Container",
            "items": items,
            "style": style
        })
        return self

    def build(self) -> Dict:
        """Build and return the card"""
        return self.card

    def to_json(self) -> str:
        """Return card as JSON string"""
        return json.dumps(self.card, indent=2)

def create_deployment_card(
    app_name: str,
    environment: str,
    version: str,
    status: str,
    details: Dict[str, str],
    action_url: str
) -> Dict:
    """Create a deployment notification card"""

    status_colors = {
        "success": "good",
        "failure": "attention",
        "in_progress": "warning",
        "pending": "default"
    }

    builder = AdaptiveCardBuilder()

    # Header with status color
    builder.add_container([
        {
            "type": "TextBlock",
            "text": f"Deployment {status.title()}: {app_name}",
            "size": "large",
            "weight": "bolder",
            "color": status_colors.get(status, "default")
        }
    ], style="emphasis" if status == "success" else "default")

    # Facts
    builder.add_fact_set({
        "Environment": environment,
        "Version": version,
        "Status": status.title(),
        **details
    })

    # Actions
    builder.add_action_open_url("View Deployment", action_url)

    if status == "in_progress":
        builder.add_action_submit(
            "Cancel Deployment",
            {"action": "cancel", "app": app_name, "version": version},
            style="destructive"
        )

    return builder.build()

def create_approval_card(
    request_id: str,
    title: str,
    requester: str,
    description: str,
    details: Dict[str, str]
) -> Dict:
    """Create an approval request card"""

    builder = AdaptiveCardBuilder()

    builder.add_text_block(
        "Approval Required",
        size="large",
        weight="bolder"
    )

    builder.add_text_block(title, size="medium", weight="bolder")
    builder.add_text_block(f"Requested by: {requester}")
    builder.add_text_block(description, wrap=True)

    if details:
        builder.add_fact_set(details)

    # Comment input
    builder.add_input_text(
        id="comment",
        placeholder="Add a comment (optional)",
        is_multiline=True,
        label="Comment"
    )

    # Approval actions
    builder.add_action_submit(
        "Approve",
        {"action": "approve", "request_id": request_id},
        style="positive"
    )

    builder.add_action_submit(
        "Reject",
        {"action": "reject", "request_id": request_id},
        style="destructive"
    )

    builder.add_action_submit(
        "Request More Info",
        {"action": "request_info", "request_id": request_id}
    )

    return builder.build()

def create_poll_card(
    question: str,
    options: List[str],
    poll_id: str
) -> Dict:
    """Create a poll card"""

    builder = AdaptiveCardBuilder()

    builder.add_text_block(
        "Poll",
        size="large",
        weight="bolder"
    )

    builder.add_text_block(question, size="medium", wrap=True)

    choices = [
        {"title": option, "value": f"option_{i}"}
        for i, option in enumerate(options)
    ]

    builder.add_input_choice_set(
        id="poll_answer",
        choices=choices,
        style="expanded",
        label="Select your answer"
    )

    builder.add_action_submit(
        "Vote",
        {"action": "vote", "poll_id": poll_id}
    )

    return builder.build()

def create_incident_card(
    incident_id: str,
    title: str,
    severity: str,
    description: str,
    affected_services: List[str],
    timeline: List[Dict[str, str]]
) -> Dict:
    """Create an incident notification card"""

    severity_colors = {
        "critical": "attention",
        "high": "warning",
        "medium": "accent",
        "low": "default"
    }

    builder = AdaptiveCardBuilder()

    # Header
    builder.add_column_set([
        {
            "type": "Column",
            "width": "auto",
            "items": [
                {
                    "type": "TextBlock",
                    "text": f"Incident: {incident_id}",
                    "size": "large",
                    "weight": "bolder",
                    "color": severity_colors.get(severity, "default")
                }
            ]
        },
        {
            "type": "Column",
            "width": "stretch",
            "items": [
                {
                    "type": "TextBlock",
                    "text": severity.upper(),
                    "horizontalAlignment": "right",
                    "weight": "bolder",
                    "color": severity_colors.get(severity, "default")
                }
            ]
        }
    ])

    builder.add_text_block(title, size="medium", weight="bolder")
    builder.add_text_block(description, wrap=True)

    # Affected services
    if affected_services:
        builder.add_text_block("Affected Services:", weight="bolder")
        for service in affected_services:
            builder.add_text_block(f"- {service}")

    # Timeline
    if timeline:
        builder.add_text_block("Timeline:", weight="bolder")
        for entry in timeline:
            builder.add_text_block(
                f"**{entry['time']}**: {entry['update']}",
                wrap=True
            )

    # Actions
    builder.add_action_submit(
        "Acknowledge",
        {"action": "acknowledge", "incident_id": incident_id}
    )

    builder.add_action_submit(
        "Escalate",
        {"action": "escalate", "incident_id": incident_id},
        style="destructive"
    )

    return builder.build()
```

### 3. Incoming Webhooks

```python
# webhooks.py
# ABOUTME: Teams incoming webhook integration
# ABOUTME: Simple notifications without full bot registration

import requests
import json
from typing import Dict, List, Optional
from datetime import datetime

class TeamsWebhook:
    """Incoming webhook client for Microsoft Teams"""

    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def send(
        self,
        text: str = None,
        title: str = None,
        sections: List[Dict] = None,
        theme_color: str = None,
        adaptive_card: Dict = None
    ) -> dict:
        """Send a message via webhook"""

        if adaptive_card:
            # Send Adaptive Card
            payload = {
                "type": "message",
                "attachments": [
                    {
                        "contentType": "application/vnd.microsoft.card.adaptive",
                        "contentUrl": None,
                        "content": adaptive_card
                    }
                ]
            }
        else:
            # Send Message Card (legacy but simpler)
            payload = {
                "@type": "MessageCard",
                "@context": "http://schema.org/extensions",
                "themeColor": theme_color or "0076D7",
                "summary": title or text[:50] if text else "Notification"
            }

            if title:
                payload["title"] = title

            if text:
                payload["text"] = text

            if sections:
                payload["sections"] = sections

        response = requests.post(
            self.webhook_url,
            json=payload,
            headers={"Content-Type": "application/json"}
        )

        if response.status_code == 200:
            return {"ok": True, "status": response.status_code}
        else:
            return {
                "ok": False,
                "status": response.status_code,
                "error": response.text
            }

    def send_deployment_notification(
        self,
        app_name: str,
        environment: str,
        version: str,
        status: str,
        commit_sha: str,
        author: str,
        deploy_url: str = None,
        logs_url: str = None
    ):
        """Send a deployment notification"""

        theme_colors = {
            "success": "00FF00",
            "failure": "FF0000",
            "started": "FFCC00",
            "pending": "808080"
        }

        status_emoji = {
            "success": "OK",
            "failure": "X",
            "started": "ROCKET",
            "pending": "CLOCK"
        }

        sections = [
            {
                "activityTitle": f"Deployment {status.title()}: {app_name}",
                "activitySubtitle": f"by {author}",
                "facts": [
                    {"name": "Environment", "value": environment},
                    {"name": "Version", "value": version},
                    {"name": "Commit", "value": commit_sha[:8]},
                    {"name": "Time", "value": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                ],
                "markdown": True
            }
        ]

        potential_actions = []
        if deploy_url:
            potential_actions.append({
                "@type": "OpenUri",
                "name": "View Deployment",
                "targets": [{"os": "default", "uri": deploy_url}]
            })
        if logs_url:
            potential_actions.append({
                "@type": "OpenUri",
                "name": "View Logs",
                "targets": [{"os": "default", "uri": logs_url}]
            })

        if potential_actions:
            sections[0]["potentialAction"] = potential_actions

        return self.send(
            title=f"Deployment {status.title()}",
            sections=sections,
            theme_color=theme_colors.get(status, "0076D7")
        )

    def send_alert(
        self,
        title: str,
        message: str,
        severity: str = "warning",
        source: str = "System",
        details: Optional[Dict] = None,
        action_url: Optional[str] = None
    ):
        """Send an alert notification"""

        severity_colors = {
            "critical": "FF0000",
            "error": "FF4444",
            "warning": "FFCC00",
            "info": "0088FF"
        }

        facts = [
            {"name": "Severity", "value": severity.upper()},
            {"name": "Source", "value": source},
            {"name": "Time", "value": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        ]

        if details:
            for key, value in details.items():
                facts.append({"name": key, "value": str(value)})

        sections = [
            {
                "activityTitle": title,
                "text": message,
                "facts": facts,
                "markdown": True
            }
        ]

        if action_url:
            sections[0]["potentialAction"] = [
                {
                    "@type": "OpenUri",
                    "name": "View Details",
                    "targets": [{"os": "default", "uri": action_url}]
                }
            ]

        return self.send(
            title=title,
            sections=sections,
            theme_color=severity_colors.get(severity, "0076D7")
        )

    def send_adaptive_card(self, card: Dict):
        """Send an Adaptive Card"""
        return self.send(adaptive_card=card)

# Usage
if __name__ == "__main__":
    webhook = TeamsWebhook("https://outlook.office.com/webhook/...")

    # Simple message
    webhook.send(text="Hello from Python!")

    # Deployment notification
    webhook.send_deployment_notification(
        app_name="my-service",
        environment="production",
        version="v1.2.3",
        status="success",
        commit_sha="abc123def456",
        author="developer@example.com",
        deploy_url="https://deployments.example.com"
    )

    # Alert
    webhook.send_alert(
        title="High CPU Usage",
        message="Server prod-web-01 CPU usage exceeded 90%",
        severity="warning",
        source="Monitoring",
        details={"Server": "prod-web-01", "Current": "92%"}
    )
```

### 4. Bot Framework Integration

```python
# bot.py
# ABOUTME: Teams bot using Bot Framework SDK
# ABOUTME: Handles messages, cards, and proactive messaging

from botbuilder.core import (
    ActivityHandler,
    TurnContext,
    CardFactory,
    MessageFactory
)
from botbuilder.schema import (
    Activity,
    ActivityTypes,
    ChannelAccount,
    Attachment
)
import json

class TeamsBot(ActivityHandler):
    """Microsoft Teams bot handler"""

    def __init__(self, conversation_references: dict = None):
        self.conversation_references = conversation_references or {}

    async def on_message_activity(self, turn_context: TurnContext):
        """Handle incoming messages"""

        # Store conversation reference for proactive messaging
        self._add_conversation_reference(turn_context.activity)

        text = turn_context.activity.text.lower().strip()
        user_name = turn_context.activity.from_property.name

        if text == "help":
            await self._send_help_card(turn_context)
        elif text == "status":
            await self._send_status_card(turn_context)
        elif text.startswith("deploy"):
            await self._handle_deploy_command(turn_context, text)
        else:
            await turn_context.send_activity(
                f"Hi {user_name}! I received: '{text}'. Type 'help' for commands."
            )

    async def on_members_added_activity(
        self,
        members_added: list,
        turn_context: TurnContext
    ):
        """Handle new members added to conversation"""
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(
                    f"Welcome to the team, {member.name}! "
                    "Type 'help' to see available commands."
                )

    async def on_adaptive_card_invoke(
        self,
        turn_context: TurnContext,
        invoke_value: dict
    ):
        """Handle Adaptive Card action invocations"""

        action = invoke_value.get("action")
        data = invoke_value

        if action == "approve":
            return await self._handle_approval(turn_context, data, approved=True)
        elif action == "reject":
            return await self._handle_approval(turn_context, data, approved=False)
        elif action == "vote":
            return await self._handle_vote(turn_context, data)

        return {"status": 200}

    async def _send_help_card(self, turn_context: TurnContext):
        """Send help card"""

        card = {
            "type": "AdaptiveCard",
            "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
            "version": "1.4",
            "body": [
                {
                    "type": "TextBlock",
                    "text": "Bot Commands",
                    "size": "large",
                    "weight": "bolder"
                },
                {
                    "type": "FactSet",
                    "facts": [
                        {"title": "help", "value": "Show this help message"},
                        {"title": "status", "value": "Show system status"},
                        {"title": "deploy [env]", "value": "Trigger deployment"},
                        {"title": "poll [question]", "value": "Create a poll"}
                    ]
                }
            ]
        }

        attachment = Attachment(
            content_type="application/vnd.microsoft.card.adaptive",
            content=card
        )

        await turn_context.send_activity(
            MessageFactory.attachment(attachment)
        )

    async def _send_status_card(self, turn_context: TurnContext):
        """Send status card"""

        card = {
            "type": "AdaptiveCard",
            "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
            "version": "1.4",
            "body": [
                {
                    "type": "TextBlock",
                    "text": "System Status",
                    "size": "large",
                    "weight": "bolder"
                },
                {
                    "type": "ColumnSet",
                    "columns": [
                        {
                            "type": "Column",
                            "width": "stretch",
                            "items": [
                                {"type": "TextBlock", "text": "API", "weight": "bolder"},
                                {"type": "TextBlock", "text": "Healthy", "color": "good"}
                            ]
                        },
                        {
                            "type": "Column",
                            "width": "stretch",
                            "items": [
                                {"type": "TextBlock", "text": "Database", "weight": "bolder"},
                                {"type": "TextBlock", "text": "Healthy", "color": "good"}
                            ]
                        },
                        {
                            "type": "Column",
                            "width": "stretch",
                            "items": [
                                {"type": "TextBlock", "text": "Cache", "weight": "bolder"},
                                {"type": "TextBlock", "text": "Warning", "color": "warning"}
                            ]
                        }
                    ]
                }
            ],
            "actions": [
                {
                    "type": "Action.OpenUrl",
                    "title": "View Dashboard",
                    "url": "https://status.example.com"
                }
            ]
        }

        attachment = Attachment(
            content_type="application/vnd.microsoft.card.adaptive",
            content=card
        )

        await turn_context.send_activity(
            MessageFactory.attachment(attachment)
        )

    async def _handle_deploy_command(
        self,
        turn_context: TurnContext,
        text: str
    ):
        """Handle deploy command"""

        parts = text.split()
        environment = parts[1] if len(parts) > 1 else "staging"

        card = {
            "type": "AdaptiveCard",
            "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
            "version": "1.4",
            "body": [
                {
                    "type": "TextBlock",
                    "text": "Confirm Deployment",
                    "size": "large",
                    "weight": "bolder"
                },
                {
                    "type": "TextBlock",
                    "text": f"Deploy to **{environment}** environment?",
                    "wrap": True
                },
                {
                    "type": "Input.ChoiceSet",
                    "id": "version",
                    "label": "Version",
                    "choices": [
                        {"title": "v1.2.3 (latest)", "value": "v1.2.3"},
                        {"title": "v1.2.2", "value": "v1.2.2"},
                        {"title": "v1.2.1", "value": "v1.2.1"}
                    ],
                    "value": "v1.2.3"
                }
            ],
            "actions": [
                {
                    "type": "Action.Submit",
                    "title": "Deploy",
                    "style": "positive",
                    "data": {
                        "action": "deploy",
                        "environment": environment
                    }
                },
                {
                    "type": "Action.Submit",
                    "title": "Cancel",
                    "data": {"action": "cancel"}
                }
            ]
        }

        attachment = Attachment(
            content_type="application/vnd.microsoft.card.adaptive",
            content=card
        )

        await turn_context.send_activity(
            MessageFactory.attachment(attachment)
        )

    async def _handle_approval(
        self,
        turn_context: TurnContext,
        data: dict,
        approved: bool
    ):
        """Handle approval action"""

        request_id = data.get("request_id")
        comment = data.get("comment", "")
        user = turn_context.activity.from_property.name

        status = "approved" if approved else "rejected"

        # Update the original card
        updated_card = {
            "type": "AdaptiveCard",
            "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
            "version": "1.4",
            "body": [
                {
                    "type": "TextBlock",
                    "text": f"Request {status.title()}",
                    "size": "large",
                    "weight": "bolder",
                    "color": "good" if approved else "attention"
                },
                {
                    "type": "TextBlock",
                    "text": f"By {user}",
                    "isSubtle": True
                }
            ]
        }

        if comment:
            updated_card["body"].append({
                "type": "TextBlock",
                "text": f"Comment: {comment}",
                "wrap": True
            })

        # Return updated card
        return {
            "statusCode": 200,
            "type": "application/vnd.microsoft.card.adaptive",
            "value": updated_card
        }

    async def _handle_vote(self, turn_context: TurnContext, data: dict):
        """Handle poll vote"""

        poll_id = data.get("poll_id")
        answer = data.get("poll_answer")
        user = turn_context.activity.from_property.name

        await turn_context.send_activity(
            f"{user} voted: {answer}"
        )

        return {"statusCode": 200}

    def _add_conversation_reference(self, activity: Activity):
        """Store conversation reference for proactive messaging"""

        conversation_reference = TurnContext.get_conversation_reference(activity)
        self.conversation_references[
            conversation_reference.conversation.id
        ] = conversation_reference
```

### 5. Proactive Messaging

```python
# proactive.py
# ABOUTME: Send proactive messages to Teams channels and users
# ABOUTME: Notify users without them initiating conversation

from botbuilder.core import TurnContext
from botbuilder.core.teams import TeamsInfo
from botbuilder.schema import Activity, ConversationReference
from botbuilder.integration.aiohttp import CloudAdapter, ConfigurationBotFrameworkAuthentication
import asyncio
from typing import Dict

class ProactiveMessenger:
    """Send proactive messages to Teams"""

    def __init__(
        self,
        adapter: CloudAdapter,
        app_id: str,
        conversation_references: Dict[str, ConversationReference]
    ):
        self.adapter = adapter
        self.app_id = app_id
        self.conversation_references = conversation_references

    async def send_to_conversation(
        self,
        conversation_id: str,
        message: str = None,
        card: Dict = None
    ):
        """Send a proactive message to a stored conversation"""

        if conversation_id not in self.conversation_references:
            raise ValueError(f"No conversation reference for {conversation_id}")

        conversation_reference = self.conversation_references[conversation_id]

        async def callback(turn_context: TurnContext):
            if card:
                from botbuilder.schema import Attachment
                from botbuilder.core import MessageFactory

                attachment = Attachment(
                    content_type="application/vnd.microsoft.card.adaptive",
                    content=card
                )
                await turn_context.send_activity(
                    MessageFactory.attachment(attachment)
                )
            else:
                await turn_context.send_activity(message)

        await self.adapter.continue_conversation(
            conversation_reference,
            callback,
            self.app_id
        )

    async def send_to_channel(
        self,
        service_url: str,
        team_id: str,
        channel_id: str,
        message: str = None,
        card: Dict = None
    ):
        """Send a proactive message to a Teams channel"""

        from botbuilder.schema import (
            ConversationParameters,
            Activity,
            ChannelAccount
        )

        # Create conversation reference for channel
        conversation_parameters = ConversationParameters(
            is_group=True,
            channel_data={"channel": {"id": channel_id}},
            activity=Activity(
                type="message",
                text=message
            ) if message else None
        )

        async def callback(turn_context: TurnContext):
            if card:
                from botbuilder.schema import Attachment
                from botbuilder.core import MessageFactory

                attachment = Attachment(
                    content_type="application/vnd.microsoft.card.adaptive",
                    content=card
                )
                await turn_context.send_activity(
                    MessageFactory.attachment(attachment)
                )
            elif message:
                await turn_context.send_activity(message)

        # Create and send the proactive message
        conversation_reference = ConversationReference(
            service_url=service_url,
            channel_id="msteams",
            conversation={"id": channel_id}
        )

        await self.adapter.continue_conversation(
            conversation_reference,
            callback,
            self.app_id
        )

    async def notify_all_conversations(
        self,
        message: str = None,
        card: Dict = None
    ):
        """Broadcast a message to all stored conversations"""

        for conv_id in self.conversation_references:
            try:
                await self.send_to_conversation(conv_id, message, card)
            except Exception as e:
                print(f"Failed to notify {conv_id}: {e}")

# Example usage with Azure Functions
"""
# function_app.py
import azure.functions as func
from proactive import ProactiveMessenger

async def notify_deployment_complete(req: func.HttpRequest) -> func.HttpResponse:
    # Load configuration and adapter
    messenger = ProactiveMessenger(adapter, app_id, conversation_references)

    card = create_deployment_card(
        app_name="my-service",
        environment="production",
        version="v1.2.3",
        status="success"
    )

    await messenger.send_to_channel(
        service_url="https://smba.trafficmanager.net/teams/",
        team_id="your-team-id",
        channel_id="your-channel-id",
        card=card
    )

    return func.HttpResponse("Notification sent", status_code=200)
"""
```

### 6. Meeting Automation

```python
# meetings.py
# ABOUTME: Teams meeting automation via Graph API
# ABOUTME: Create, manage, and get meeting details

from datetime import datetime, timedelta
from typing import List, Optional, Dict
import asyncio

class MeetingManager:
    """Manage Teams meetings via Graph API"""

    def __init__(self, graph_client):
        self.client = graph_client

    async def create_instant_meeting(
        self,
        subject: str,
        organizer_id: str
    ) -> Dict:
        """Create an instant meeting"""

        from msgraph.generated.models.online_meeting import OnlineMeeting

        meeting = OnlineMeeting(
            subject=subject,
            start_date_time=datetime.utcnow().isoformat() + "Z",
            end_date_time=(datetime.utcnow() + timedelta(hours=1)).isoformat() + "Z"
        )

        result = await self.client.users.by_user_id(organizer_id) \
            .online_meetings.post(meeting)

        return {
            "join_url": result.join_web_url,
            "meeting_id": result.id,
            "subject": result.subject
        }

    async def schedule_meeting(
        self,
        subject: str,
        start_time: datetime,
        end_time: datetime,
        organizer_id: str,
        attendee_emails: List[str],
        body: str = ""
    ) -> Dict:
        """Schedule a meeting with attendees"""

        from msgraph.generated.models.event import Event
        from msgraph.generated.models.item_body import ItemBody
        from msgraph.generated.models.body_type import BodyType
        from msgraph.generated.models.attendee import Attendee
        from msgraph.generated.models.email_address import EmailAddress
        from msgraph.generated.models.attendee_type import AttendeeType
        from msgraph.generated.models.date_time_time_zone import DateTimeTimeZone

        attendees = [
            Attendee(
                email_address=EmailAddress(address=email),
                type=AttendeeType.Required
            )
            for email in attendee_emails
        ]

        event = Event(
            subject=subject,
            body=ItemBody(
                content_type=BodyType.Html,
                content=body
            ),
            start=DateTimeTimeZone(
                date_time=start_time.isoformat(),
                time_zone="UTC"
            ),
            end=DateTimeTimeZone(
                date_time=end_time.isoformat(),
                time_zone="UTC"
            ),
            attendees=attendees,
            is_online_meeting=True,
            online_meeting_provider="teamsForBusiness"
        )

        result = await self.client.users.by_user_id(organizer_id) \
            .events.post(event)

        return {
            "event_id": result.id,
            "subject": result.subject,
            "join_url": result.online_meeting.join_url if result.online_meeting else None
        }

    async def get_user_calendar(
        self,
        user_id: str,
        start_date: datetime,
        end_date: datetime
    ) -> List[Dict]:
        """Get user's calendar events"""

        result = await self.client.users.by_user_id(user_id) \
            .calendar_view.get(
                request_configuration=lambda config: (
                    setattr(config.query_parameters, 'start_date_time', start_date.isoformat()),
                    setattr(config.query_parameters, 'end_date_time', end_date.isoformat())
                )
            )

        return [
            {
                "id": event.id,
                "subject": event.subject,
                "start": event.start.date_time,
                "end": event.end.date_time,
                "is_online": event.is_online_meeting
            }
            for event in result.value
        ]

    async def cancel_meeting(
        self,
        user_id: str,
        event_id: str,
        cancellation_message: str = ""
    ):
        """Cancel a scheduled meeting"""

        await self.client.users.by_user_id(user_id) \
            .events.by_event_id(event_id) \
            .cancel.post(comment=cancellation_message)

# Usage example
async def schedule_standup():
    """Schedule a daily standup meeting"""

    from graph_client import TeamsGraphClient

    client = TeamsGraphClient()
    meetings = MeetingManager(client.client)

    # Schedule for tomorrow at 9 AM
    tomorrow = datetime.utcnow().replace(hour=9, minute=0) + timedelta(days=1)

    result = await meetings.schedule_meeting(
        subject="Daily Standup",
        start_time=tomorrow,
        end_time=tomorrow + timedelta(minutes=30),
        organizer_id="organizer@company.com",
        attendee_emails=[
            "team-member1@company.com",
            "team-member2@company.com"
        ],
        body="<h2>Daily Standup</h2><p>Please be prepared to share your updates.</p>"
    )

    print(f"Meeting scheduled: {result['join_url']}")
```

## Integration Examples

### Azure DevOps Pipeline Integration

```yaml
# azure-pipelines.yml
trigger:
  - main

pool:
  vmImage: 'ubuntu-latest'

stages:
  - stage: Build
    jobs:
      - job: BuildJob
        steps:
          - script: echo "Building..."

          - task: PowerShell@2
            displayName: 'Notify Teams - Build Started'
            inputs:
              targetType: 'inline'
              script: |
                $webhook = "$(TEAMS_WEBHOOK_URL)"
                $body = @{
                  "@type" = "MessageCard"
                  "@context" = "http://schema.org/extensions"
                  "themeColor" = "FFCC00"
                  "summary" = "Build Started"
                  "sections" = @(
                    @{
                      "activityTitle" = "Build Started: $(Build.DefinitionName)"
                      "facts" = @(
                        @{ "name" = "Branch"; "value" = "$(Build.SourceBranchName)" }
                        @{ "name" = "Commit"; "value" = "$(Build.SourceVersion)" }
                        @{ "name" = "Build ID"; "value" = "$(Build.BuildId)" }
                      )
                    }
                  )
                } | ConvertTo-Json -Depth 10
                Invoke-RestMethod -Uri $webhook -Method Post -Body $body -ContentType 'application/json'

  - stage: Deploy
    dependsOn: Build
    jobs:
      - deployment: DeployJob
        environment: 'production'
        strategy:
          runOnce:
            deploy:
              steps:
                - script: echo "Deploying..."

                - task: PowerShell@2
                  displayName: 'Notify Teams - Deployment Complete'
                  inputs:
                    targetType: 'inline'
                    script: |
                      $webhook = "$(TEAMS_WEBHOOK_URL)"
                      $body = @{
                        "@type" = "MessageCard"
                        "themeColor" = "00FF00"
                        "summary" = "Deployment Complete"
                        "sections" = @(
                          @{
                            "activityTitle" = "Deployment Complete"
                            "facts" = @(
                              @{ "name" = "Environment"; "value" = "Production" }
                              @{ "name" = "Version"; "value" = "$(Build.BuildNumber)" }
                            )
                            "potentialAction" = @(
                              @{
                                "@type" = "OpenUri"
                                "name" = "View Release"
                                "targets" = @(@{ "os" = "default"; "uri" = "$(System.TeamFoundationCollectionUri)/$(System.TeamProject)/_release?releaseId=$(Release.ReleaseId)" })
                              }
                            )
                          }
                        )
                      } | ConvertTo-Json -Depth 10
                      Invoke-RestMethod -Uri $webhook -Method Post -Body $body -ContentType 'application/json'
```

### FastAPI Bot Endpoint

```python
# main.py
# ABOUTME: FastAPI endpoint for Teams bot
# ABOUTME: Handles bot messages and card actions

from fastapi import FastAPI, Request, Response
from botbuilder.core import TurnContext
from botbuilder.integration.aiohttp import CloudAdapter, ConfigurationBotFrameworkAuthentication
from botbuilder.schema import Activity
from bot import TeamsBot
import os

# Configuration
class DefaultConfig:
    PORT = 3978
    APP_ID = os.environ.get("MICROSOFT_APP_ID", "")
    APP_PASSWORD = os.environ.get("MICROSOFT_APP_PASSWORD", "")

CONFIG = DefaultConfig()

# Create adapter
SETTINGS = ConfigurationBotFrameworkAuthentication(CONFIG)
ADAPTER = CloudAdapter(SETTINGS)

# Create bot
CONVERSATION_REFERENCES = {}
BOT = TeamsBot(CONVERSATION_REFERENCES)

# Error handler
async def on_error(context: TurnContext, error: Exception):
    print(f"Bot error: {error}")
    await context.send_activity("Sorry, an error occurred.")

ADAPTER.on_turn_error = on_error

# FastAPI app
app = FastAPI()

@app.post("/api/messages")
async def messages(request: Request) -> Response:
    """Main bot messaging endpoint"""

    if "application/json" not in request.headers.get("Content-Type", ""):
        return Response(status_code=415)

    body = await request.json()
    activity = Activity().deserialize(body)

    auth_header = request.headers.get("Authorization", "")

    response = await ADAPTER.process_activity(auth_header, activity, BOT.on_turn)

    if response:
        return Response(
            content=response.body,
            status_code=response.status
        )
    return Response(status_code=201)

@app.get("/api/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=CONFIG.PORT)
```

## Best Practices

### 1. Rate Limiting

```python
# Respect Graph API rate limits
import time
from functools import wraps

def rate_limit_handler(max_retries=3):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if "429" in str(e):  # Too Many Requests
                        delay = 2 ** attempt
                        await asyncio.sleep(delay)
                    else:
                        raise
            raise Exception("Max retries exceeded")
        return wrapper
    return decorator
```

### 2. Token Management

```python
# Secure token handling
from azure.identity import DefaultAzureCredential
from functools import lru_cache

@lru_cache()
def get_credential():
    """Get cached Azure credential"""
    return DefaultAzureCredential()

# Use managed identity in production
# Use environment variables for local dev
```

### 3. Card Design

```python
# Adaptive Card best practices
def create_accessible_card():
    return {
        "type": "AdaptiveCard",
        "version": "1.4",
        "body": [
            {
                "type": "TextBlock",
                "text": "Important Message",
                "size": "large",
                "weight": "bolder",
                # Always include fallback text
                "fallback": "drop"
            }
        ],
        # Provide fallback for older clients
        "fallbackText": "This card requires a newer Teams client."
    }
```

## Troubleshooting

### Common Issues

**Issue: Bot not receiving messages**
```bash
# Verify messaging endpoint is accessible
curl -X POST https://your-bot.azurewebsites.net/api/messages \
  -H "Content-Type: application/json" \
  -d '{"type": "ping"}'

# Check Azure App Registration permissions
# Verify Teams channel is enabled in Bot Framework
```

**Issue: Webhook returns error**
```python
# Debug webhook response
response = requests.post(webhook_url, json=payload)
print(f"Status: {response.status_code}")
print(f"Response: {response.text}")
```

**Issue: Graph API permission denied**
```bash
# Verify API permissions are granted
# Admin consent may be required for application permissions
# Check token scopes match required permissions
```

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-17 | Initial release with comprehensive Teams API patterns |

## Resources

- [Microsoft Graph API](https://docs.microsoft.com/graph/)
- [Bot Framework SDK](https://docs.microsoft.com/azure/bot-service/)
- [Adaptive Cards Designer](https://adaptivecards.io/designer/)
- [Teams App Manifest](https://docs.microsoft.com/microsoftteams/platform/resources/schema/manifest-schema)
- [Teams Webhook Connectors](https://docs.microsoft.com/microsoftteams/platform/webhooks-and-connectors/)

---

*This skill provides production-ready patterns for Microsoft Teams automation, enabling enterprise messaging and collaboration workflows.*
