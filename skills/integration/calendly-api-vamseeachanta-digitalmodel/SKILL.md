---
name: calendly-api
version: 1.0.0
description: Calendly scheduling automation using REST API v2 for managing event types, availability, bookings, webhooks, and scheduling workflows
author: workspace-hub
category: communication
type: skill
capabilities:
  - event_type_management
  - availability_scheduling
  - booking_management
  - webhook_subscriptions
  - invitee_tracking
  - routing_forms
  - organization_management
  - user_scheduling
  - cancellation_handling
  - scheduling_links
tools:
  - curl
  - requests
  - httpx
  - python
tags: [calendly, scheduling, calendar, booking, meetings, api, automation, webhooks]
platforms: [linux, macos, windows]
related_skills:
  - slack-api
  - teams-api
  - github-actions
---

# Calendly API Skill

Master Calendly scheduling automation using the REST API v2. This skill covers event type management, availability configuration, booking workflows, webhook integrations, and automated scheduling patterns for building seamless meeting coordination.

## When to Use This Skill

### USE when:
- Automating interview scheduling workflows
- Building meeting booking integrations
- Creating round-robin scheduling systems
- Tracking scheduled events programmatically
- Integrating calendars with CRM systems
- Building appointment reminders
- Creating custom booking confirmation flows
- Automating follow-up sequences after meetings
- Syncing Calendly with external calendars
- Building scheduling analytics dashboards

### DON'T USE when:
- Simple calendar display (use Google Calendar API)
- Real-time video calls (use Zoom/Teams API)
- Complex resource scheduling (use specialized tools)
- Internal meeting coordination only (use calendar apps)
- One-off manual scheduling (use Calendly UI directly)

## Prerequisites

### Calendly API Setup

```bash
# 1. Get API credentials at https://calendly.com/integrations/api_webhooks
# 2. Create a Personal Access Token or OAuth app
# 3. Note: API v2 requires organization-level access for some endpoints

# Personal Access Token:
# - Go to Integrations > API & Webhooks
# - Generate a new token
# - Copy the token (shown only once)

# OAuth 2.0 App:
# - Go to https://developer.calendly.com/
# - Create an OAuth application
# - Configure redirect URIs
# - Note client_id and client_secret

# Required OAuth Scopes:
# - default                    - Basic access
# - organization:read          - Read organization data
# - organization:write         - Manage organization
# - user:read                  - Read user profiles
# - scheduling_link:read       - Read scheduling links
# - event_type:read            - Read event types
# - event_type:write           - Manage event types
# - scheduled_event:read       - Read scheduled events
# - scheduled_event:write      - Manage scheduled events
# - invitee:read               - Read invitee data
# - webhook:read               - Read webhooks
# - webhook:write              - Manage webhooks
```

### Python Environment Setup

```bash
# Create virtual environment
python -m venv calendly-env
source calendly-env/bin/activate  # Linux/macOS
# calendly-env\Scripts\activate   # Windows

# Install dependencies
pip install requests python-dotenv httpx aiohttp

# Create requirements.txt
cat > requirements.txt << 'EOF'
requests>=2.31.0
python-dotenv>=1.0.0
httpx>=0.25.0
aiohttp>=3.9.0
pydantic>=2.5.0
EOF

# Environment variables
cat > .env << 'EOF'
CALENDLY_API_KEY=your-personal-access-token
CALENDLY_CLIENT_ID=your-oauth-client-id
CALENDLY_CLIENT_SECRET=your-oauth-client-secret
CALENDLY_WEBHOOK_SECRET=your-webhook-signing-secret
EOF
```

### API Client Setup

```python
# client.py
# ABOUTME: Calendly API client with authentication
# ABOUTME: Handles requests, pagination, and error handling

import os
import requests
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv

load_dotenv()


class CalendlyClient:
    """Calendly API v2 client"""

    BASE_URL = "https://api.calendly.com"

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("CALENDLY_API_KEY")
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        })
        self._current_user = None
        self._organization = None

    def _request(
        self,
        method: str,
        endpoint: str,
        params: Dict = None,
        json: Dict = None,
    ) -> Dict:
        """Make an API request"""
        url = f"{self.BASE_URL}{endpoint}"

        response = self.session.request(
            method=method,
            url=url,
            params=params,
            json=json,
        )

        if response.status_code == 429:
            # Rate limited
            retry_after = int(response.headers.get("Retry-After", 60))
            raise Exception(f"Rate limited. Retry after {retry_after}s")

        response.raise_for_status()

        if response.status_code == 204:
            return {}

        return response.json()

    def get(self, endpoint: str, params: Dict = None) -> Dict:
        """GET request"""
        return self._request("GET", endpoint, params=params)

    def post(self, endpoint: str, json: Dict = None) -> Dict:
        """POST request"""
        return self._request("POST", endpoint, json=json)

    def delete(self, endpoint: str) -> Dict:
        """DELETE request"""
        return self._request("DELETE", endpoint)

    def paginate(
        self,
        endpoint: str,
        params: Dict = None,
        key: str = "collection",
        limit: int = None,
    ) -> List[Dict]:
        """Paginate through results"""
        params = params or {}
        params["count"] = 100
        results = []

        while True:
            response = self.get(endpoint, params)
            items = response.get(key, [])
            results.extend(items)

            if limit and len(results) >= limit:
                return results[:limit]

            pagination = response.get("pagination", {})
            next_page_token = pagination.get("next_page_token")

            if not next_page_token:
                break

            params["page_token"] = next_page_token

        return results

    @property
    def current_user(self) -> Dict:
        """Get current user info (cached)"""
        if not self._current_user:
            response = self.get("/users/me")
            self._current_user = response.get("resource")
        return self._current_user

    @property
    def user_uri(self) -> str:
        """Get current user URI"""
        return self.current_user["uri"]

    @property
    def organization_uri(self) -> str:
        """Get current organization URI"""
        return self.current_user["current_organization"]


# Global client instance
client = CalendlyClient()
```

## Core Capabilities

### 1. User and Organization Management

```python
# users.py
# ABOUTME: User and organization management
# ABOUTME: Retrieve user profiles, organization info, memberships

from client import client


def get_current_user() -> dict:
    """Get the current authenticated user"""
    response = client.get("/users/me")
    user = response.get("resource", {})

    return {
        "uri": user.get("uri"),
        "name": user.get("name"),
        "email": user.get("email"),
        "slug": user.get("slug"),
        "scheduling_url": user.get("scheduling_url"),
        "timezone": user.get("timezone"),
        "organization": user.get("current_organization"),
    }


def get_user_by_uri(user_uri: str) -> dict:
    """Get a user by their URI"""
    # Extract UUID from URI
    uuid = user_uri.split("/")[-1]
    response = client.get(f"/users/{uuid}")
    return response.get("resource", {})


def get_organization(organization_uri: str = None) -> dict:
    """Get organization details"""
    org_uri = organization_uri or client.organization_uri
    uuid = org_uri.split("/")[-1]
    response = client.get(f"/organizations/{uuid}")
    return response.get("resource", {})


def list_organization_memberships(
    organization_uri: str = None,
    email: str = None,
) -> list:
    """List organization memberships"""
    org_uri = organization_uri or client.organization_uri

    params = {"organization": org_uri}
    if email:
        params["email"] = email

    return client.paginate("/organization_memberships", params=params)


def get_user_availability_schedules(user_uri: str = None) -> list:
    """Get user's availability schedules"""
    user = user_uri or client.user_uri
    params = {"user": user}
    return client.paginate("/user_availability_schedules", params=params)


def get_user_busy_times(
    user_uri: str = None,
    start_time: str = None,
    end_time: str = None,
) -> list:
    """Get user's busy times for a date range

    Times should be ISO 8601 format: 2026-01-17T00:00:00Z
    """
    user = user_uri or client.user_uri
    params = {
        "user": user,
        "start_time": start_time,
        "end_time": end_time,
    }
    response = client.get("/user_busy_times", params=params)
    return response.get("collection", [])


if __name__ == "__main__":
    # Get current user
    user = get_current_user()
    print(f"User: {user['name']} ({user['email']})")
    print(f"Scheduling URL: {user['scheduling_url']}")

    # List memberships
    memberships = list_organization_memberships()
    print(f"\nOrganization has {len(memberships)} members")
```

### 2. Event Types

```python
# event_types.py
# ABOUTME: Event type management
# ABOUTME: Create, list, and configure event types

from client import client
from typing import Optional, List


def list_event_types(
    user_uri: str = None,
    organization_uri: str = None,
    active: bool = True,
) -> list:
    """List all event types for a user or organization"""
    params = {}

    if user_uri:
        params["user"] = user_uri
    elif organization_uri:
        params["organization"] = organization_uri
    else:
        params["user"] = client.user_uri

    if active is not None:
        params["active"] = str(active).lower()

    return client.paginate("/event_types", params=params)


def get_event_type(event_type_uri: str) -> dict:
    """Get event type details"""
    uuid = event_type_uri.split("/")[-1]
    response = client.get(f"/event_types/{uuid}")
    return response.get("resource", {})


def get_event_type_by_slug(slug: str, user_uri: str = None) -> Optional[dict]:
    """Find event type by slug"""
    event_types = list_event_types(user_uri=user_uri)

    for et in event_types:
        if et.get("slug") == slug:
            return et

    return None


def get_available_times(
    event_type_uri: str,
    start_time: str,
    end_time: str,
) -> list:
    """Get available time slots for an event type

    Times should be ISO 8601 format: 2026-01-17T00:00:00Z
    """
    params = {
        "event_type": event_type_uri,
        "start_time": start_time,
        "end_time": end_time,
    }
    response = client.get("/event_type_available_times", params=params)
    return response.get("collection", [])


def format_event_type_summary(event_type: dict) -> dict:
    """Format event type for display"""
    return {
        "name": event_type.get("name"),
        "slug": event_type.get("slug"),
        "duration": event_type.get("duration"),
        "scheduling_url": event_type.get("scheduling_url"),
        "type": event_type.get("type"),  # StandardEventType, AdhocEventType
        "kind": event_type.get("kind"),  # solo, round_robin, collective
        "active": event_type.get("active"),
        "description": event_type.get("description_plain"),
    }


def list_event_types_summary(user_uri: str = None) -> list:
    """Get summarized list of event types"""
    event_types = list_event_types(user_uri=user_uri)
    return [format_event_type_summary(et) for et in event_types]


if __name__ == "__main__":
    # List all event types
    event_types = list_event_types_summary()

    print("Available Event Types:")
    for et in event_types:
        status = "Active" if et["active"] else "Inactive"
        print(f"  - {et['name']} ({et['duration']} min) [{status}]")
        print(f"    URL: {et['scheduling_url']}")

    # Get available times for an event type
    if event_types:
        et_uri = event_types[0].get("uri")
        from datetime import datetime, timedelta

        start = datetime.now().isoformat() + "Z"
        end = (datetime.now() + timedelta(days=7)).isoformat() + "Z"

        times = get_available_times(et_uri, start, end)
        print(f"\nAvailable slots: {len(times)}")
```

### 3. Scheduled Events

```python
# scheduled_events.py
# ABOUTME: Scheduled event management
# ABOUTME: List, retrieve, and cancel scheduled events

from client import client
from typing import Optional, List
from datetime import datetime, timedelta


def list_scheduled_events(
    user_uri: str = None,
    organization_uri: str = None,
    min_start_time: str = None,
    max_start_time: str = None,
    status: str = "active",
    invitee_email: str = None,
    sort: str = "start_time:asc",
) -> list:
    """List scheduled events

    status: active, canceled
    sort: start_time:asc, start_time:desc
    """
    params = {
        "status": status,
        "sort": sort,
    }

    if user_uri:
        params["user"] = user_uri
    elif organization_uri:
        params["organization"] = organization_uri
    else:
        params["user"] = client.user_uri

    if min_start_time:
        params["min_start_time"] = min_start_time
    if max_start_time:
        params["max_start_time"] = max_start_time
    if invitee_email:
        params["invitee_email"] = invitee_email

    return client.paginate("/scheduled_events", params=params)


def get_scheduled_event(event_uri: str) -> dict:
    """Get scheduled event details"""
    uuid = event_uri.split("/")[-1]
    response = client.get(f"/scheduled_events/{uuid}")
    return response.get("resource", {})


def cancel_scheduled_event(event_uri: str, reason: str = None) -> dict:
    """Cancel a scheduled event"""
    uuid = event_uri.split("/")[-1]
    data = {}
    if reason:
        data["reason"] = reason

    response = client.post(f"/scheduled_events/{uuid}/cancellation", json=data)
    return response.get("resource", {})


def get_upcoming_events(
    user_uri: str = None,
    days_ahead: int = 7,
) -> list:
    """Get upcoming events for the next N days"""
    now = datetime.utcnow()
    end = now + timedelta(days=days_ahead)

    return list_scheduled_events(
        user_uri=user_uri,
        min_start_time=now.isoformat() + "Z",
        max_start_time=end.isoformat() + "Z",
        status="active",
    )


def get_past_events(
    user_uri: str = None,
    days_back: int = 30,
) -> list:
    """Get past events from the last N days"""
    now = datetime.utcnow()
    start = now - timedelta(days=days_back)

    return list_scheduled_events(
        user_uri=user_uri,
        min_start_time=start.isoformat() + "Z",
        max_start_time=now.isoformat() + "Z",
        status="active",
        sort="start_time:desc",
    )


def format_event_summary(event: dict) -> dict:
    """Format event for display"""
    return {
        "uri": event.get("uri"),
        "name": event.get("name"),
        "start_time": event.get("start_time"),
        "end_time": event.get("end_time"),
        "status": event.get("status"),
        "location": event.get("location", {}).get("type"),
        "event_type": event.get("event_type"),
        "guests_count": len(event.get("event_guests", [])),
        "cancellation": event.get("cancellation"),
    }


def get_events_by_email(email: str, user_uri: str = None) -> list:
    """Find all events with a specific invitee email"""
    return list_scheduled_events(
        user_uri=user_uri,
        invitee_email=email,
    )


if __name__ == "__main__":
    # Get upcoming events
    events = get_upcoming_events(days_ahead=14)

    print(f"Upcoming events: {len(events)}")
    for event in events:
        summary = format_event_summary(event)
        print(f"  - {summary['name']} at {summary['start_time']}")

    # Get events for specific invitee
    email_events = get_events_by_email("john@example.com")
    print(f"\nEvents with john@example.com: {len(email_events)}")
```

### 4. Invitees

```python
# invitees.py
# ABOUTME: Invitee management for scheduled events
# ABOUTME: Retrieve invitee details and custom answers

from client import client
from typing import Optional, List


def list_invitees(
    event_uri: str,
    status: str = None,
    email: str = None,
) -> list:
    """List invitees for a scheduled event

    status: active, canceled
    """
    uuid = event_uri.split("/")[-1]
    params = {}

    if status:
        params["status"] = status
    if email:
        params["email"] = email

    return client.paginate(f"/scheduled_events/{uuid}/invitees", params=params)


def get_invitee(invitee_uri: str) -> dict:
    """Get invitee details"""
    # Parse invitee URI to get event and invitee UUIDs
    parts = invitee_uri.split("/")
    event_uuid = parts[-3]
    invitee_uuid = parts[-1]

    response = client.get(f"/scheduled_events/{event_uuid}/invitees/{invitee_uuid}")
    return response.get("resource", {})


def get_invitee_no_show(invitee_uri: str) -> Optional[dict]:
    """Get no-show status for an invitee"""
    parts = invitee_uri.split("/")
    invitee_uuid = parts[-1]

    try:
        response = client.get(f"/invitee_no_shows/{invitee_uuid}")
        return response.get("resource")
    except Exception:
        return None


def mark_invitee_no_show(invitee_uri: str) -> dict:
    """Mark an invitee as a no-show"""
    response = client.post("/invitee_no_shows", json={"invitee": invitee_uri})
    return response.get("resource", {})


def unmark_invitee_no_show(no_show_uri: str) -> bool:
    """Remove no-show status from an invitee"""
    uuid = no_show_uri.split("/")[-1]
    client.delete(f"/invitee_no_shows/{uuid}")
    return True


def format_invitee_summary(invitee: dict) -> dict:
    """Format invitee for display"""
    return {
        "uri": invitee.get("uri"),
        "name": invitee.get("name"),
        "email": invitee.get("email"),
        "status": invitee.get("status"),
        "timezone": invitee.get("timezone"),
        "created_at": invitee.get("created_at"),
        "rescheduled": invitee.get("rescheduled"),
        "questions_and_answers": [
            {
                "question": qa.get("question"),
                "answer": qa.get("answer"),
            }
            for qa in invitee.get("questions_and_answers", [])
        ],
        "tracking": invitee.get("tracking", {}),
        "utm_parameters": {
            "source": invitee.get("utm_source"),
            "medium": invitee.get("utm_medium"),
            "campaign": invitee.get("utm_campaign"),
        },
    }


def get_invitee_custom_answers(invitee: dict) -> dict:
    """Extract custom question answers from invitee"""
    answers = {}
    for qa in invitee.get("questions_and_answers", []):
        question = qa.get("question")
        answer = qa.get("answer")
        answers[question] = answer
    return answers


def get_all_invitees_for_events(event_uris: list) -> list:
    """Get invitees for multiple events"""
    all_invitees = []

    for event_uri in event_uris:
        invitees = list_invitees(event_uri)
        for invitee in invitees:
            invitee["event_uri"] = event_uri
        all_invitees.extend(invitees)

    return all_invitees


if __name__ == "__main__":
    from scheduled_events import get_upcoming_events

    # Get upcoming events and their invitees
    events = get_upcoming_events(days_ahead=7)

    for event in events[:5]:
        print(f"\nEvent: {event['name']}")
        invitees = list_invitees(event["uri"])

        for inv in invitees:
            summary = format_invitee_summary(inv)
            print(f"  - {summary['name']} ({summary['email']})")

            if summary["questions_and_answers"]:
                for qa in summary["questions_and_answers"]:
                    print(f"    Q: {qa['question']}")
                    print(f"    A: {qa['answer']}")
```

### 5. Webhooks

```python
# webhooks.py
# ABOUTME: Webhook subscription management
# ABOUTME: Create, manage, and handle webhook events

from client import client
import hmac
import hashlib
from typing import Optional, List


def list_webhook_subscriptions(
    organization_uri: str = None,
    user_uri: str = None,
    scope: str = None,
) -> list:
    """List webhook subscriptions

    scope: organization, user
    """
    params = {}

    if organization_uri:
        params["organization"] = organization_uri
    elif user_uri:
        params["user"] = user_uri
    else:
        params["organization"] = client.organization_uri

    if scope:
        params["scope"] = scope

    return client.paginate("/webhook_subscriptions", params=params)


def create_webhook_subscription(
    url: str,
    events: list,
    organization_uri: str = None,
    user_uri: str = None,
    signing_key: str = None,
) -> dict:
    """Create a webhook subscription

    events: invitee.created, invitee.canceled, routing_form_submission.created
    """
    data = {
        "url": url,
        "events": events,
    }

    if organization_uri:
        data["organization"] = organization_uri
        data["scope"] = "organization"
    elif user_uri:
        data["user"] = user_uri
        data["scope"] = "user"
    else:
        data["organization"] = client.organization_uri
        data["scope"] = "organization"

    if signing_key:
        data["signing_key"] = signing_key

    response = client.post("/webhook_subscriptions", json=data)
    return response.get("resource", {})


def get_webhook_subscription(subscription_uri: str) -> dict:
    """Get webhook subscription details"""
    uuid = subscription_uri.split("/")[-1]
    response = client.get(f"/webhook_subscriptions/{uuid}")
    return response.get("resource", {})


def delete_webhook_subscription(subscription_uri: str) -> bool:
    """Delete a webhook subscription"""
    uuid = subscription_uri.split("/")[-1]
    client.delete(f"/webhook_subscriptions/{uuid}")
    return True


def verify_webhook_signature(
    payload: bytes,
    signature: str,
    signing_key: str,
    tolerance: int = 180,
) -> bool:
    """Verify Calendly webhook signature

    Calendly uses HMAC-SHA256 for webhook signatures
    """
    import time

    # Parse signature header
    # Format: t=timestamp,v1=signature
    parts = dict(p.split("=", 1) for p in signature.split(","))

    timestamp = int(parts.get("t", 0))
    expected_sig = parts.get("v1", "")

    # Check timestamp tolerance
    if abs(time.time() - timestamp) > tolerance:
        return False

    # Compute expected signature
    signed_payload = f"{timestamp}.{payload.decode()}"
    computed_sig = hmac.new(
        signing_key.encode(),
        signed_payload.encode(),
        hashlib.sha256,
    ).hexdigest()

    return hmac.compare_digest(computed_sig, expected_sig)


# Webhook event types
WEBHOOK_EVENTS = {
    "invitee.created": "When a new invitee schedules an event",
    "invitee.canceled": "When an invitee cancels an event",
    "routing_form_submission.created": "When a routing form is submitted",
}


class WebhookHandler:
    """Handler for Calendly webhook events"""

    def __init__(self, signing_key: str = None):
        self.signing_key = signing_key
        self.handlers = {}

    def on(self, event: str):
        """Decorator to register an event handler"""
        def decorator(func):
            self.handlers[event] = func
            return func
        return decorator

    def handle(self, payload: dict) -> dict:
        """Handle an incoming webhook event"""
        event = payload.get("event")
        data = payload.get("payload", {})

        handler = self.handlers.get(event)
        if handler:
            return handler(data)

        return {"handled": False, "event": event}


# Example webhook handler
webhook = WebhookHandler()


@webhook.on("invitee.created")
def handle_new_booking(data: dict) -> dict:
    """Handle new booking webhook"""
    invitee = data.get("invitee", {})
    event = data.get("scheduled_event", {})

    return {
        "handled": True,
        "action": "booking_created",
        "invitee_email": invitee.get("email"),
        "event_name": event.get("name"),
        "start_time": event.get("start_time"),
    }


@webhook.on("invitee.canceled")
def handle_cancellation(data: dict) -> dict:
    """Handle cancellation webhook"""
    invitee = data.get("invitee", {})
    cancellation = invitee.get("cancellation", {})

    return {
        "handled": True,
        "action": "booking_canceled",
        "invitee_email": invitee.get("email"),
        "reason": cancellation.get("reason"),
        "canceled_by": cancellation.get("canceled_by"),
    }


if __name__ == "__main__":
    # List existing webhooks
    webhooks = list_webhook_subscriptions()
    print(f"Active webhooks: {len(webhooks)}")

    for wh in webhooks:
        print(f"  - {wh['callback_url']}")
        print(f"    Events: {', '.join(wh['events'])}")
        print(f"    Scope: {wh['scope']}")

    # Create a new webhook
    new_webhook = create_webhook_subscription(
        url="https://example.com/webhooks/calendly",
        events=["invitee.created", "invitee.canceled"],
    )
    print(f"\nCreated webhook: {new_webhook['uri']}")
```

### 6. Scheduling Links and Routing

```python
# scheduling.py
# ABOUTME: Scheduling links and routing forms
# ABOUTME: Single-use links, routing, and booking customization

from client import client
from typing import Optional


def create_single_use_link(event_type_uri: str, max_event_count: int = 1) -> dict:
    """Create a single-use scheduling link

    These links can only be used for a limited number of bookings
    """
    response = client.post(
        "/scheduling_links",
        json={
            "max_event_count": max_event_count,
            "owner": event_type_uri,
            "owner_type": "EventType",
        },
    )
    return response.get("resource", {})


def get_scheduling_link(link_uri: str) -> dict:
    """Get scheduling link details"""
    uuid = link_uri.split("/")[-1]
    response = client.get(f"/scheduling_links/{uuid}")
    return response.get("resource", {})


def list_routing_forms(organization_uri: str = None) -> list:
    """List routing forms"""
    org = organization_uri or client.organization_uri
    params = {"organization": org}
    return client.paginate("/routing_forms", params=params)


def get_routing_form(form_uri: str) -> dict:
    """Get routing form details"""
    uuid = form_uri.split("/")[-1]
    response = client.get(f"/routing_forms/{uuid}")
    return response.get("resource", {})


def list_routing_form_submissions(
    form_uri: str,
    sort: str = "created_at:desc",
) -> list:
    """List routing form submissions"""
    params = {
        "routing_form": form_uri,
        "sort": sort,
    }
    return client.paginate("/routing_form_submissions", params=params)


def get_routing_form_submission(submission_uri: str) -> dict:
    """Get routing form submission details"""
    uuid = submission_uri.split("/")[-1]
    response = client.get(f"/routing_form_submissions/{uuid}")
    return response.get("resource", {})


def build_scheduling_url(
    base_url: str,
    name: str = None,
    email: str = None,
    utm_source: str = None,
    utm_medium: str = None,
    utm_campaign: str = None,
    custom_answers: dict = None,
) -> str:
    """Build a pre-filled scheduling URL

    custom_answers: {"a1": "answer1", "a2": "answer2"} for custom questions
    """
    from urllib.parse import urlencode, urlparse, parse_qs, urlunparse

    params = {}

    if name:
        params["name"] = name
    if email:
        params["email"] = email
    if utm_source:
        params["utm_source"] = utm_source
    if utm_medium:
        params["utm_medium"] = utm_medium
    if utm_campaign:
        params["utm_campaign"] = utm_campaign
    if custom_answers:
        params.update(custom_answers)

    if not params:
        return base_url

    parsed = urlparse(base_url)
    query = urlencode(params)

    return urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        parsed.params,
        query,
        parsed.fragment,
    ))


def generate_interview_links(
    event_type_uri: str,
    candidates: list,
) -> list:
    """Generate single-use interview links for candidates

    candidates: [{"name": "John", "email": "john@example.com"}, ...]
    """
    event_type = get_event_type(event_type_uri)
    base_url = event_type["scheduling_url"]

    links = []
    for candidate in candidates:
        # Create single-use link
        link = create_single_use_link(event_type_uri, max_event_count=1)

        # Build pre-filled URL
        scheduling_url = build_scheduling_url(
            base_url=link["booking_url"],
            name=candidate.get("name"),
            email=candidate.get("email"),
            utm_source="interview",
            utm_campaign=candidate.get("campaign", "hiring"),
        )

        links.append({
            "candidate": candidate,
            "link_uri": link["uri"],
            "scheduling_url": scheduling_url,
        })

    return links


from event_types import get_event_type


if __name__ == "__main__":
    from event_types import list_event_types

    # Get an event type
    event_types = list_event_types()
    if event_types:
        et = event_types[0]

        # Build pre-filled URL
        url = build_scheduling_url(
            base_url=et["scheduling_url"],
            name="Jane Doe",
            email="jane@example.com",
            utm_source="email",
            utm_campaign="q1-outreach",
        )
        print(f"Pre-filled URL: {url}")

        # Create single-use link
        single_use = create_single_use_link(et["uri"])
        print(f"Single-use booking URL: {single_use['booking_url']}")
```

## Integration Examples

### Slack Notification Integration

```python
# slack_integration.py
# ABOUTME: Notify Slack when Calendly events are scheduled
# ABOUTME: Webhook handler with Slack notifications

import os
import requests
from flask import Flask, request, jsonify
from webhooks import WebhookHandler, verify_webhook_signature

app = Flask(__name__)
webhook = WebhookHandler(signing_key=os.environ.get("CALENDLY_WEBHOOK_SECRET"))

SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")


def send_slack_notification(message: dict):
    """Send a message to Slack"""
    requests.post(SLACK_WEBHOOK_URL, json=message)


@webhook.on("invitee.created")
def handle_new_booking(data: dict) -> dict:
    """Notify Slack of new booking"""
    invitee = data.get("invitee", {})
    event = data.get("scheduled_event", {})
    event_type = data.get("event_type", {})

    # Extract custom answers
    answers = {}
    for qa in invitee.get("questions_and_answers", []):
        answers[qa["question"]] = qa["answer"]

    # Send Slack notification
    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": ":calendar: New Meeting Scheduled",
            },
        },
        {
            "type": "section",
            "fields": [
                {"type": "mrkdwn", "text": f"*Event:*\n{event_type.get('name')}"},
                {"type": "mrkdwn", "text": f"*Invitee:*\n{invitee.get('name')}"},
                {"type": "mrkdwn", "text": f"*Email:*\n{invitee.get('email')}"},
                {"type": "mrkdwn", "text": f"*Time:*\n{event.get('start_time')}"},
            ],
        },
    ]

    if answers:
        answer_text = "\n".join(f"*{q}:* {a}" for q, a in answers.items())
        blocks.append({
            "type": "section",
            "text": {"type": "mrkdwn", "text": f"*Responses:*\n{answer_text}"},
        })

    blocks.append({
        "type": "actions",
        "elements": [
            {
                "type": "button",
                "text": {"type": "plain_text", "text": "View in Calendly"},
                "url": f"https://calendly.com/app/scheduled_events/{event['uri'].split('/')[-1]}",
            },
        ],
    })

    send_slack_notification({"blocks": blocks})

    return {"handled": True, "notified": "slack"}


@webhook.on("invitee.canceled")
def handle_cancellation(data: dict) -> dict:
    """Notify Slack of cancellation"""
    invitee = data.get("invitee", {})
    event = data.get("scheduled_event", {})
    cancellation = invitee.get("cancellation", {})

    send_slack_notification({
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": ":x: Meeting Canceled",
                },
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*Event:*\n{event.get('name')}"},
                    {"type": "mrkdwn", "text": f"*Invitee:*\n{invitee.get('name')}"},
                    {"type": "mrkdwn", "text": f"*Reason:*\n{cancellation.get('reason', 'Not provided')}"},
                    {"type": "mrkdwn", "text": f"*Canceled by:*\n{cancellation.get('canceled_by')}"},
                ],
            },
        ],
    })

    return {"handled": True, "notified": "slack"}


@app.route("/webhooks/calendly", methods=["POST"])
def calendly_webhook():
    """Handle Calendly webhook"""
    # Verify signature
    signature = request.headers.get("Calendly-Webhook-Signature")
    if signature:
        signing_key = os.environ.get("CALENDLY_WEBHOOK_SECRET")
        if not verify_webhook_signature(request.data, signature, signing_key):
            return jsonify({"error": "Invalid signature"}), 401

    payload = request.json
    result = webhook.handle(payload)
    return jsonify(result)


if __name__ == "__main__":
    app.run(port=8080)
```

### GitHub Actions Integration

```yaml
# .github/workflows/calendly-sync.yml
name: Sync Calendly Events

on:
  schedule:
    - cron: '0 8 * * *'  # Daily at 8 AM
  workflow_dispatch:

jobs:
  sync-events:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: pip install requests

      - name: Fetch upcoming events
        env:
          CALENDLY_API_KEY: ${{ secrets.CALENDLY_API_KEY }}
        run: |
          python << 'EOF'
          import os
          import requests
          from datetime import datetime, timedelta
          import json

          API_KEY = os.environ["CALENDLY_API_KEY"]
          BASE_URL = "https://api.calendly.com"

          headers = {
              "Authorization": f"Bearer {API_KEY}",
              "Content-Type": "application/json",
          }

          # Get current user
          user_response = requests.get(f"{BASE_URL}/users/me", headers=headers)
          user = user_response.json()["resource"]
          user_uri = user["uri"]

          # Get upcoming events
          now = datetime.utcnow()
          end = now + timedelta(days=7)

          params = {
              "user": user_uri,
              "min_start_time": now.isoformat() + "Z",
              "max_start_time": end.isoformat() + "Z",
              "status": "active",
          }

          events_response = requests.get(
              f"{BASE_URL}/scheduled_events",
              headers=headers,
              params=params,
          )
          events = events_response.json()["collection"]

          print(f"Found {len(events)} upcoming events")

          # Save to file
          with open("upcoming_events.json", "w") as f:
              json.dump(events, f, indent=2)

          # Create summary
          summary = []
          for event in events:
              summary.append({
                  "name": event["name"],
                  "start_time": event["start_time"],
                  "status": event["status"],
              })

          with open("events_summary.json", "w") as f:
              json.dump(summary, f, indent=2)

          print("Events synced successfully")
          EOF

      - name: Upload events artifact
        uses: actions/upload-artifact@v4
        with:
          name: calendly-events
          path: |
            upcoming_events.json
            events_summary.json
```

## Best Practices

### 1. Rate Limiting

```python
# Rate limit handling
import time
from functools import wraps

def rate_limit_handler(max_retries=3, base_delay=1):
    """Decorator for handling Calendly rate limits"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if "429" in str(e):
                        delay = base_delay * (2 ** attempt)
                        print(f"Rate limited, waiting {delay}s...")
                        time.sleep(delay)
                    else:
                        raise
            raise Exception("Max retries exceeded")
        return wrapper
    return decorator
```

### 2. Token Management

```python
# Secure token management
import os
from functools import lru_cache

@lru_cache()
def get_calendly_client():
    """Get cached Calendly client with secure token"""
    token = os.environ.get("CALENDLY_API_KEY")
    if not token:
        raise ValueError("CALENDLY_API_KEY not set")
    return CalendlyClient(api_key=token)

# Never log tokens
def redact_token(text: str) -> str:
    token = os.environ.get("CALENDLY_API_KEY", "")
    if token and token in text:
        return text.replace(token, "[REDACTED]")
    return text
```

### 3. Webhook Security

```python
# Webhook signature verification
def verify_and_process_webhook(request):
    """Verify webhook signature before processing"""
    signature = request.headers.get("Calendly-Webhook-Signature")

    if not signature:
        return {"error": "Missing signature"}, 401

    signing_key = os.environ.get("CALENDLY_WEBHOOK_SECRET")
    if not verify_webhook_signature(request.data, signature, signing_key):
        return {"error": "Invalid signature"}, 401

    # Process webhook
    return process_webhook(request.json)
```

### 4. Error Handling

```python
# Comprehensive error handling
class CalendlyError(Exception):
    """Base Calendly API error"""
    pass

class RateLimitError(CalendlyError):
    """Rate limit exceeded"""
    def __init__(self, retry_after: int):
        self.retry_after = retry_after
        super().__init__(f"Rate limited. Retry after {retry_after}s")

class NotFoundError(CalendlyError):
    """Resource not found"""
    pass

def handle_api_error(response):
    """Handle API error responses"""
    if response.status_code == 429:
        retry_after = int(response.headers.get("Retry-After", 60))
        raise RateLimitError(retry_after)
    elif response.status_code == 404:
        raise NotFoundError(response.json().get("message"))
    else:
        response.raise_for_status()
```

## Troubleshooting

### Common Issues

**Issue: 401 Unauthorized**
```python
# Verify token is valid
def verify_token(token: str) -> bool:
    response = requests.get(
        "https://api.calendly.com/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    return response.status_code == 200
```

**Issue: No events returned**
```python
# Check time range format
from datetime import datetime

def format_time_for_api(dt: datetime) -> str:
    """Format datetime for Calendly API (ISO 8601 with Z)"""
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")

# Ensure UTC timezone
start = datetime.utcnow()
formatted = format_time_for_api(start)
```

**Issue: Webhook not receiving events**
```python
# Verify webhook subscription
def check_webhook_status(webhook_uri: str):
    webhook = get_webhook_subscription(webhook_uri)
    print(f"Status: {webhook.get('state')}")
    print(f"Events: {webhook.get('events')}")
    print(f"URL: {webhook.get('callback_url')}")

    # Verify URL is accessible
    import requests
    try:
        response = requests.post(webhook["callback_url"], json={"test": True})
        print(f"URL accessible: {response.status_code < 500}")
    except Exception as e:
        print(f"URL not accessible: {e}")
```

### Debug Commands

```bash
# Test API authentication
curl -X GET "https://api.calendly.com/users/me" \
  -H "Authorization: Bearer $CALENDLY_API_KEY"

# List event types
curl -X GET "https://api.calendly.com/event_types?user=$(curl -s -X GET https://api.calendly.com/users/me -H "Authorization: Bearer $CALENDLY_API_KEY" | jq -r '.resource.uri')" \
  -H "Authorization: Bearer $CALENDLY_API_KEY"

# List webhooks
curl -X GET "https://api.calendly.com/webhook_subscriptions?organization=$(curl -s -X GET https://api.calendly.com/users/me -H "Authorization: Bearer $CALENDLY_API_KEY" | jq -r '.resource.current_organization')" \
  -H "Authorization: Bearer $CALENDLY_API_KEY"
```

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-17 | Initial release with comprehensive Calendly API v2 patterns |

## Resources

- [Calendly API Documentation](https://developer.calendly.com/api-docs)
- [Calendly Developer Portal](https://developer.calendly.com/)
- [OAuth 2.0 Guide](https://developer.calendly.com/getting-started-with-oauth)
- [Webhooks Guide](https://developer.calendly.com/api-docs/4e4e9a77ef8bc-webhooks)
- [Rate Limits](https://developer.calendly.com/api-docs/rate-limiting)
- [API Changelog](https://developer.calendly.com/api-changelog)

---

*This skill provides production-ready patterns for Calendly scheduling automation, enabling seamless meeting coordination and booking workflows.*
