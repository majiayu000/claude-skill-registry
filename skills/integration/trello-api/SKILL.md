---
name: trello-api
version: 1.0.0
description: Kanban board automation with Trello API including boards, lists, cards, members, webhooks, power-ups, and Python SDK (py-trello) integration
author: workspace-hub
category: productivity
type: skill
capabilities:
  - Board creation and management
  - List CRUD operations
  - Card creation and manipulation
  - Labels and checklists
  - Member management
  - Attachments and comments
  - Webhook integration
  - Power-up development
  - Batch operations
  - Custom fields
tools:
  - trello-api
  - py-trello
  - curl
  - jq
tags: [trello, kanban, api, productivity, boards, cards, webhooks, automation, project-management, py-trello]
platforms: [rest-api, python, web]
related_skills:
  - todoist-api
  - notion-api
  - api-integration
  - github-actions
---

# Trello API Integration Skill

Master the Trello API for Kanban board automation, including boards, lists, cards, members, webhooks, and the py-trello Python SDK. Build powerful workflow automations and custom integrations with Trello's comprehensive REST API.

## When to Use This Skill

### USE Trello API when:
- **Automating board management** - Create, update, archive boards programmatically
- **Building workflow integrations** - Connect Trello with other tools
- **Card automation** - Auto-create cards from external events
- **Progress tracking** - Build dashboards from Trello data
- **Notification systems** - React to board changes via webhooks
- **Bulk operations** - Move/update many cards at once
- **Custom reporting** - Extract data for analysis
- **Power-up development** - Extend Trello functionality

### DON'T USE Trello API when:
- **Need complex dependencies** - Use Jira or Asana
- **Require time tracking** - Built-in feature limited, use Toggl integration
- **Database-style queries** - Use Notion API instead
- **Enterprise compliance** - May need Enterprise-grade solutions
- **Complex workflows** - Consider Monday.com or Linear

## Prerequisites

### API Authentication

```bash
# Get API Key from:
# https://trello.com/app-key

# Get Token (authorize your app):
# https://trello.com/1/authorize?expiration=never&scope=read,write,account&response_type=token&name=MyApp&key=YOUR_API_KEY

# Set environment variables
export TRELLO_API_KEY="your-api-key"
export TRELLO_TOKEN="your-token"

# Verify authentication
curl -s "https://api.trello.com/1/members/me?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq '.fullName'
```

### Python SDK Installation

```bash
# Install py-trello
pip install py-trello

# Using uv (recommended)
uv pip install py-trello

# With additional dependencies
pip install py-trello requests python-dateutil

# Verify installation
python -c "from trello import TrelloClient; print('py-trello installed!')"
```

### Verify Setup

```python
from trello import TrelloClient
import os

client = TrelloClient(
    api_key=os.environ["TRELLO_API_KEY"],
    token=os.environ["TRELLO_TOKEN"]
)

# Test connection
me = client.get_member("me")
print(f"Connected as: {me.full_name}")
print(f"Username: {me.username}")
```

## Core Capabilities

### 1. Board Management

**REST API - Boards:**
```bash
# List all boards
curl -s "https://api.trello.com/1/members/me/boards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq '.[].name'

# Get specific board
curl -s "https://api.trello.com/1/boards/BOARD_ID?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq

# Get board with lists and cards
curl -s "https://api.trello.com/1/boards/BOARD_ID?lists=all&cards=all&key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq

# Create board
curl -s -X POST "https://api.trello.com/1/boards" \
    -d "key=$TRELLO_API_KEY" \
    -d "token=$TRELLO_TOKEN" \
    -d "name=Project Alpha" \
    -d "desc=Main project board" \
    -d "defaultLists=false" \
    -d "prefs_permissionLevel=private" | jq

# Create board from template
curl -s -X POST "https://api.trello.com/1/boards" \
    -d "key=$TRELLO_API_KEY" \
    -d "token=$TRELLO_TOKEN" \
    -d "name=New Project" \
    -d "idBoardSource=TEMPLATE_BOARD_ID" | jq

# Update board
curl -s -X PUT "https://api.trello.com/1/boards/BOARD_ID" \
    -d "key=$TRELLO_API_KEY" \
    -d "token=$TRELLO_TOKEN" \
    -d "name=Project Alpha - Updated" \
    -d "desc=Updated description" | jq

# Close (archive) board
curl -s -X PUT "https://api.trello.com/1/boards/BOARD_ID/closed" \
    -d "key=$TRELLO_API_KEY" \
    -d "token=$TRELLO_TOKEN" \
    -d "value=true" | jq

# Delete board permanently
curl -s -X DELETE "https://api.trello.com/1/boards/BOARD_ID?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN"
```

**Python SDK - Boards:**
```python
from trello import TrelloClient
import os

client = TrelloClient(
    api_key=os.environ["TRELLO_API_KEY"],
    token=os.environ["TRELLO_TOKEN"]
)

# List all boards
boards = client.list_boards()
for board in boards:
    print(f"{board.name} (ID: {board.id})")

# Get specific board
board = client.get_board("BOARD_ID")
print(f"Board: {board.name}")
print(f"URL: {board.url}")

# Create new board
new_board = client.add_board(
    board_name="Development Sprint",
    source_board=None,  # Or source board for template
    permission_level="private"  # "private", "org", "public"
)
print(f"Created board: {new_board.id}")

# Get board lists
lists = board.list_lists()
for lst in lists:
    print(f"  List: {lst.name}")

# Get all cards on board
cards = board.get_cards()
for card in cards:
    print(f"  Card: {card.name}")

# Get board members
members = board.get_members()
for member in members:
    print(f"  Member: {member.full_name}")

# Close board
board.close()

# Reopen board
board.open()
```

### 2. List Management

**REST API - Lists:**
```bash
# Get lists for board
curl -s "https://api.trello.com/1/boards/BOARD_ID/lists?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq

# Create list
curl -s -X POST "https://api.trello.com/1/lists" \
    -d "key=$TRELLO_API_KEY" \
    -d "token=$TRELLO_TOKEN" \
    -d "name=In Progress" \
    -d "idBoard=BOARD_ID" \
    -d "pos=bottom" | jq

# Update list name
curl -s -X PUT "https://api.trello.com/1/lists/LIST_ID" \
    -d "key=$TRELLO_API_KEY" \
    -d "token=$TRELLO_TOKEN" \
    -d "name=Currently Working" | jq

# Move list to different position
curl -s -X PUT "https://api.trello.com/1/lists/LIST_ID" \
    -d "key=$TRELLO_API_KEY" \
    -d "token=$TRELLO_TOKEN" \
    -d "pos=top" | jq

# Archive list
curl -s -X PUT "https://api.trello.com/1/lists/LIST_ID/closed" \
    -d "key=$TRELLO_API_KEY" \
    -d "token=$TRELLO_TOKEN" \
    -d "value=true" | jq

# Move all cards in list to another list
curl -s -X POST "https://api.trello.com/1/lists/LIST_ID/moveAllCards" \
    -d "key=$TRELLO_API_KEY" \
    -d "token=$TRELLO_TOKEN" \
    -d "idBoard=BOARD_ID" \
    -d "idList=TARGET_LIST_ID" | jq

# Archive all cards in list
curl -s -X POST "https://api.trello.com/1/lists/LIST_ID/archiveAllCards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN"
```

**Python SDK - Lists:**
```python
from trello import TrelloClient
import os

client = TrelloClient(
    api_key=os.environ["TRELLO_API_KEY"],
    token=os.environ["TRELLO_TOKEN"]
)

board = client.get_board("BOARD_ID")

# Get all lists
lists = board.list_lists()
for lst in lists:
    print(f"List: {lst.name} (ID: {lst.id})")

# Create new list
new_list = board.add_list(
    name="Backlog",
    pos="bottom"  # "top", "bottom", or position number
)
print(f"Created list: {new_list.id}")

# Get specific list
target_list = board.get_list("LIST_ID")

# Get cards in list
cards = target_list.list_cards()
for card in cards:
    print(f"  Card: {card.name}")

# Rename list
target_list.set_name("New Backlog")

# Change list position
target_list.set_pos("top")

# Archive list
target_list.close()

# Move all cards from one list to another
source_list = board.get_list("SOURCE_LIST_ID")
dest_list = board.get_list("DEST_LIST_ID")

for card in source_list.list_cards():
    card.change_list(dest_list.id)
```

### 3. Card Management

**REST API - Cards:**
```bash
# Get cards for list
curl -s "https://api.trello.com/1/lists/LIST_ID/cards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq

# Get single card
curl -s "https://api.trello.com/1/cards/CARD_ID?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq

# Create card with all options
curl -s -X POST "https://api.trello.com/1/cards" \
    -d "key=$TRELLO_API_KEY" \
    -d "token=$TRELLO_TOKEN" \
    -d "idList=LIST_ID" \
    -d "name=Implement feature X" \
    -d "desc=Detailed description of the feature" \
    -d "pos=top" \
    -d "due=2025-01-30T12:00:00.000Z" \
    -d "dueComplete=false" \
    -d "idMembers=MEMBER_ID1,MEMBER_ID2" \
    -d "idLabels=LABEL_ID1,LABEL_ID2" | jq

# Update card
curl -s -X PUT "https://api.trello.com/1/cards/CARD_ID" \
    -d "key=$TRELLO_API_KEY" \
    -d "token=$TRELLO_TOKEN" \
    -d "name=Updated card name" \
    -d "desc=Updated description" \
    -d "due=2025-02-15" | jq

# Move card to different list
curl -s -X PUT "https://api.trello.com/1/cards/CARD_ID" \
    -d "key=$TRELLO_API_KEY" \
    -d "token=$TRELLO_TOKEN" \
    -d "idList=NEW_LIST_ID" | jq

# Move card to different board
curl -s -X PUT "https://api.trello.com/1/cards/CARD_ID" \
    -d "key=$TRELLO_API_KEY" \
    -d "token=$TRELLO_TOKEN" \
    -d "idBoard=NEW_BOARD_ID" \
    -d "idList=NEW_LIST_ID" | jq

# Archive card
curl -s -X PUT "https://api.trello.com/1/cards/CARD_ID" \
    -d "key=$TRELLO_API_KEY" \
    -d "token=$TRELLO_TOKEN" \
    -d "closed=true" | jq

# Delete card permanently
curl -s -X DELETE "https://api.trello.com/1/cards/CARD_ID?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN"

# Add comment to card
curl -s -X POST "https://api.trello.com/1/cards/CARD_ID/actions/comments" \
    -d "key=$TRELLO_API_KEY" \
    -d "token=$TRELLO_TOKEN" \
    -d "text=This is a comment on the card" | jq

# Add attachment via URL
curl -s -X POST "https://api.trello.com/1/cards/CARD_ID/attachments" \
    -d "key=$TRELLO_API_KEY" \
    -d "token=$TRELLO_TOKEN" \
    -d "url=https://example.com/file.pdf" \
    -d "name=Important Document" | jq
```

**Python SDK - Cards:**
```python
from trello import TrelloClient
from datetime import datetime, timedelta
import os

client = TrelloClient(
    api_key=os.environ["TRELLO_API_KEY"],
    token=os.environ["TRELLO_TOKEN"]
)

board = client.get_board("BOARD_ID")
target_list = board.get_list("LIST_ID")

# Create card
new_card = target_list.add_card(
    name="Complete API integration",
    desc="Full description of the task with acceptance criteria",
    labels=None,  # Add labels later
    due="2025-02-01",
    source=None,  # Or source card ID to copy from
    position="top"  # "top", "bottom", or number
)
print(f"Created card: {new_card.id}")

# Get card
card = client.get_card("CARD_ID")
print(f"Card: {card.name}")
print(f"Description: {card.description}")
print(f"Due: {card.due_date}")

# Update card properties
card.set_name("Updated: Complete API integration")
card.set_description("Updated description with more details")

# Set due date
due_date = datetime.now() + timedelta(days=7)
card.set_due(due_date)

# Mark due date complete
card.set_due_complete()

# Add label to card
labels = board.get_labels()
for label in labels:
    if label.name == "High Priority":
        card.add_label(label)
        break

# Assign member
members = board.get_members()
for member in members:
    if member.username == "target_user":
        card.add_member(member)
        break

# Add comment
card.comment("This task is now in progress")

# Add checklist
checklist = card.add_checklist(
    title="Implementation Steps",
    items=["Design API", "Write code", "Write tests", "Deploy"]
)

# Move card to different list
done_list = board.get_list("DONE_LIST_ID")
card.change_list(done_list.id)

# Archive card
card.set_closed(True)

# Unarchive card
card.set_closed(False)

# Delete card
card.delete()
```

### 4. Labels Management

**REST API - Labels:**
```bash
# Get labels for board
curl -s "https://api.trello.com/1/boards/BOARD_ID/labels?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq

# Create label
curl -s -X POST "https://api.trello.com/1/labels" \
    -d "key=$TRELLO_API_KEY" \
    -d "token=$TRELLO_TOKEN" \
    -d "name=Bug" \
    -d "color=red" \
    -d "idBoard=BOARD_ID" | jq

# Available colors: yellow, purple, blue, red, green, orange, black, sky, pink, lime

# Update label
curl -s -X PUT "https://api.trello.com/1/labels/LABEL_ID" \
    -d "key=$TRELLO_API_KEY" \
    -d "token=$TRELLO_TOKEN" \
    -d "name=Critical Bug" \
    -d "color=red" | jq

# Delete label
curl -s -X DELETE "https://api.trello.com/1/labels/LABEL_ID?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN"

# Add label to card
curl -s -X POST "https://api.trello.com/1/cards/CARD_ID/idLabels" \
    -d "key=$TRELLO_API_KEY" \
    -d "token=$TRELLO_TOKEN" \
    -d "value=LABEL_ID" | jq

# Remove label from card
curl -s -X DELETE "https://api.trello.com/1/cards/CARD_ID/idLabels/LABEL_ID?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN"
```

**Python SDK - Labels:**
```python
# Get all labels for board
labels = board.get_labels()
for label in labels:
    print(f"Label: {label.name} (Color: {label.color})")

# Create new label
new_label = board.add_label(
    name="Enhancement",
    color="blue"
)

# Add label to card
card.add_label(new_label)

# Remove label from card
card.remove_label(new_label)

# Update label (using API directly)
import requests

requests.put(
    f"https://api.trello.com/1/labels/{label.id}",
    params={
        "key": os.environ["TRELLO_API_KEY"],
        "token": os.environ["TRELLO_TOKEN"],
        "name": "New Name",
        "color": "green"
    }
)
```

### 5. Checklists Management

**REST API - Checklists:**
```bash
# Get checklists on card
curl -s "https://api.trello.com/1/cards/CARD_ID/checklists?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq

# Create checklist
curl -s -X POST "https://api.trello.com/1/checklists" \
    -d "key=$TRELLO_API_KEY" \
    -d "token=$TRELLO_TOKEN" \
    -d "idCard=CARD_ID" \
    -d "name=Deployment Checklist" | jq

# Add item to checklist
curl -s -X POST "https://api.trello.com/1/checklists/CHECKLIST_ID/checkItems" \
    -d "key=$TRELLO_API_KEY" \
    -d "token=$TRELLO_TOKEN" \
    -d "name=Run tests" \
    -d "pos=bottom" \
    -d "checked=false" | jq

# Update checklist item (mark complete)
curl -s -X PUT "https://api.trello.com/1/cards/CARD_ID/checkItem/CHECKITEM_ID" \
    -d "key=$TRELLO_API_KEY" \
    -d "token=$TRELLO_TOKEN" \
    -d "state=complete" | jq

# Delete checklist
curl -s -X DELETE "https://api.trello.com/1/checklists/CHECKLIST_ID?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN"
```

**Python SDK - Checklists:**
```python
# Get checklists on card
checklists = card.fetch_checklists()
for checklist in checklists:
    print(f"Checklist: {checklist.name}")
    for item in checklist.items:
        status = "[x]" if item["checked"] else "[ ]"
        print(f"  {status} {item['name']}")

# Create checklist with items
checklist = card.add_checklist(
    title="Release Checklist",
    items=[
        "Code review completed",
        "Tests passing",
        "Documentation updated",
        "Changelog updated",
        "Version bumped"
    ]
)

# Check/uncheck item
checklist.set_checklist_item("Code review completed", checked=True)

# Delete checklist item
checklist.delete_checklist_item("Documentation updated")

# Rename checklist
checklist.rename("Pre-Release Checklist")

# Delete checklist
checklist.delete()
```

### 6. Member Management

**REST API - Members:**
```bash
# Get board members
curl -s "https://api.trello.com/1/boards/BOARD_ID/members?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq

# Get member info
curl -s "https://api.trello.com/1/members/MEMBER_ID?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq

# Add member to board
curl -s -X PUT "https://api.trello.com/1/boards/BOARD_ID/members/MEMBER_ID" \
    -d "key=$TRELLO_API_KEY" \
    -d "token=$TRELLO_TOKEN" \
    -d "type=normal" | jq  # "admin", "normal", "observer"

# Remove member from board
curl -s -X DELETE "https://api.trello.com/1/boards/BOARD_ID/members/MEMBER_ID?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN"

# Assign member to card
curl -s -X POST "https://api.trello.com/1/cards/CARD_ID/idMembers" \
    -d "key=$TRELLO_API_KEY" \
    -d "token=$TRELLO_TOKEN" \
    -d "value=MEMBER_ID" | jq

# Remove member from card
curl -s -X DELETE "https://api.trello.com/1/cards/CARD_ID/idMembers/MEMBER_ID?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN"

# Get cards assigned to member
curl -s "https://api.trello.com/1/members/MEMBER_ID/cards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq
```

**Python SDK - Members:**
```python
# Get current user
me = client.get_member("me")
print(f"Name: {me.full_name}")
print(f"Username: {me.username}")
print(f"Email: {me.email}")

# Get board members
members = board.get_members()
for member in members:
    print(f"Member: {member.full_name} (@{member.username})")

# Assign member to card
card.add_member(member)

# Remove member from card
card.remove_member(member)

# Get all cards for a member
member_cards = client.get_member("me").fetch_cards()
for card in member_cards:
    print(f"Assigned card: {card.name}")

# Get boards for member
member_boards = client.get_member("me").fetch_boards()
for board in member_boards:
    print(f"Board: {board.name}")
```

### 7. Webhooks

**REST API - Webhooks:**
```bash
# Create webhook
curl -s -X POST "https://api.trello.com/1/webhooks" \
    -d "key=$TRELLO_API_KEY" \
    -d "token=$TRELLO_TOKEN" \
    -d "callbackURL=https://your-server.com/webhook/trello" \
    -d "idModel=BOARD_ID" \
    -d "description=Board events webhook" | jq

# List webhooks
curl -s "https://api.trello.com/1/tokens/$TRELLO_TOKEN/webhooks?key=$TRELLO_API_KEY" | jq

# Get webhook details
curl -s "https://api.trello.com/1/webhooks/WEBHOOK_ID?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq

# Update webhook
curl -s -X PUT "https://api.trello.com/1/webhooks/WEBHOOK_ID" \
    -d "key=$TRELLO_API_KEY" \
    -d "token=$TRELLO_TOKEN" \
    -d "callbackURL=https://new-server.com/webhook/trello" | jq

# Delete webhook
curl -s -X DELETE "https://api.trello.com/1/webhooks/WEBHOOK_ID?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN"
```

**Webhook Handler Example:**
```python
from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route("/webhook/trello", methods=["HEAD", "POST"])
def trello_webhook():
    # HEAD request is for webhook verification
    if request.method == "HEAD":
        return "", 200

    # Process webhook payload
    data = request.json

    action = data.get("action", {})
    action_type = action.get("type")

    print(f"Received Trello webhook: {action_type}")

    # Handle different action types
    if action_type == "createCard":
        handle_card_created(action)
    elif action_type == "updateCard":
        handle_card_updated(action)
    elif action_type == "moveCardToBoard":
        handle_card_moved(action)
    elif action_type == "addMemberToCard":
        handle_member_assigned(action)
    elif action_type == "commentCard":
        handle_comment_added(action)
    elif action_type == "updateCheckItemStateOnCard":
        handle_checklist_item_updated(action)

    return jsonify({"status": "ok"})


def handle_card_created(action):
    card_data = action.get("data", {}).get("card", {})
    print(f"Card created: {card_data.get('name')}")


def handle_card_updated(action):
    card_data = action.get("data", {}).get("card", {})
    old_data = action.get("data", {}).get("old", {})
    print(f"Card updated: {card_data.get('name')}")

    # Check if moved to different list
    if "idList" in old_data:
        list_after = action.get("data", {}).get("listAfter", {})
        list_before = action.get("data", {}).get("listBefore", {})
        print(f"  Moved from '{list_before.get('name')}' to '{list_after.get('name')}'")


def handle_card_moved(action):
    card_data = action.get("data", {}).get("card", {})
    print(f"Card moved to different board: {card_data.get('name')}")


def handle_member_assigned(action):
    card_data = action.get("data", {}).get("card", {})
    member_data = action.get("data", {}).get("member", {})
    print(f"Member {member_data.get('username')} assigned to: {card_data.get('name')}")


def handle_comment_added(action):
    card_data = action.get("data", {}).get("card", {})
    text = action.get("data", {}).get("text", "")
    print(f"Comment on {card_data.get('name')}: {text[:100]}")


def handle_checklist_item_updated(action):
    card_data = action.get("data", {}).get("card", {})
    item = action.get("data", {}).get("checkItem", {})
    state = item.get("state")
    print(f"Checklist item '{item.get('name')}' marked {state}")


if __name__ == "__main__":
    app.run(port=5000)
```

**Webhook Events:**
```python
# Common Trello webhook action types
WEBHOOK_ACTIONS = {
    # Board events
    "updateBoard": "Board settings changed",
    "addMemberToBoard": "Member added to board",
    "removeMemberFromBoard": "Member removed from board",

    # List events
    "createList": "List created",
    "updateList": "List updated (renamed, moved, archived)",
    "moveListToBoard": "List moved to different board",

    # Card events
    "createCard": "Card created",
    "updateCard": "Card updated (name, desc, due date, position, list)",
    "deleteCard": "Card deleted",
    "moveCardToBoard": "Card moved to different board",
    "copyCard": "Card copied",
    "convertToCardFromCheckItem": "Checklist item converted to card",

    # Card member events
    "addMemberToCard": "Member assigned to card",
    "removeMemberFromCard": "Member removed from card",

    # Card label events
    "addLabelToCard": "Label added to card",
    "removeLabelFromCard": "Label removed from card",

    # Card attachment events
    "addAttachmentToCard": "Attachment added",
    "deleteAttachmentFromCard": "Attachment deleted",

    # Comment events
    "commentCard": "Comment added to card",
    "updateComment": "Comment updated",
    "deleteComment": "Comment deleted",

    # Checklist events
    "addChecklistToCard": "Checklist added to card",
    "removeChecklistFromCard": "Checklist removed",
    "updateChecklist": "Checklist updated",
    "updateCheckItemStateOnCard": "Checklist item checked/unchecked",
    "createCheckItem": "Checklist item created",
    "deleteCheckItem": "Checklist item deleted",
}
```

### 8. Custom Fields

**REST API - Custom Fields:**
```bash
# Get custom fields on board
curl -s "https://api.trello.com/1/boards/BOARD_ID/customFields?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq

# Create custom field
curl -s -X POST "https://api.trello.com/1/customFields" \
    -d "key=$TRELLO_API_KEY" \
    -d "token=$TRELLO_TOKEN" \
    -d "idModel=BOARD_ID" \
    -d "modelType=board" \
    -d "name=Priority Score" \
    -d "type=number" \
    -d "pos=top" | jq

# Field types: number, text, date, checkbox, list

# Create dropdown custom field
curl -s -X POST "https://api.trello.com/1/customFields" \
    -H "Content-Type: application/json" \
    -d '{
        "key": "'$TRELLO_API_KEY'",
        "token": "'$TRELLO_TOKEN'",
        "idModel": "BOARD_ID",
        "modelType": "board",
        "name": "Status",
        "type": "list",
        "pos": "bottom",
        "options": [
            {"value": {"text": "Not Started"}, "pos": 1},
            {"value": {"text": "In Progress"}, "pos": 2},
            {"value": {"text": "Completed"}, "pos": 3}
        ]
    }' | jq

# Set custom field value on card
curl -s -X PUT "https://api.trello.com/1/cards/CARD_ID/customField/FIELD_ID/item" \
    -H "Content-Type: application/json" \
    -d '{
        "key": "'$TRELLO_API_KEY'",
        "token": "'$TRELLO_TOKEN'",
        "value": {"number": "85"}
    }' | jq

# For dropdown, use idValue
curl -s -X PUT "https://api.trello.com/1/cards/CARD_ID/customField/FIELD_ID/item" \
    -H "Content-Type: application/json" \
    -d '{
        "key": "'$TRELLO_API_KEY'",
        "token": "'$TRELLO_TOKEN'",
        "idValue": "OPTION_ID"
    }' | jq

# Get custom field values for card
curl -s "https://api.trello.com/1/cards/CARD_ID/customFieldItems?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq
```

**Python Custom Fields:**
```python
import requests
import os

API_KEY = os.environ["TRELLO_API_KEY"]
TOKEN = os.environ["TRELLO_TOKEN"]

def get_custom_fields(board_id):
    """Get all custom fields for a board."""
    url = f"https://api.trello.com/1/boards/{board_id}/customFields"
    response = requests.get(url, params={"key": API_KEY, "token": TOKEN})
    return response.json()


def set_custom_field_value(card_id, field_id, value, field_type="text"):
    """Set custom field value on a card."""
    url = f"https://api.trello.com/1/cards/{card_id}/customField/{field_id}/item"

    # Build value based on type
    if field_type == "number":
        data = {"value": {"number": str(value)}}
    elif field_type == "text":
        data = {"value": {"text": value}}
    elif field_type == "checkbox":
        data = {"value": {"checked": str(value).lower()}}
    elif field_type == "date":
        data = {"value": {"date": value}}  # ISO format
    elif field_type == "list":
        data = {"idValue": value}  # Option ID for dropdown
    else:
        data = {"value": {"text": str(value)}}

    response = requests.put(
        url,
        json={**data, "key": API_KEY, "token": TOKEN}
    )
    return response.json()


def get_card_custom_fields(card_id):
    """Get all custom field values for a card."""
    url = f"https://api.trello.com/1/cards/{card_id}/customFieldItems"
    response = requests.get(url, params={"key": API_KEY, "token": TOKEN})
    return response.json()


# Example usage
fields = get_custom_fields("BOARD_ID")
for field in fields:
    print(f"Field: {field['name']} (Type: {field['type']})")

# Set a numeric field
set_custom_field_value("CARD_ID", "FIELD_ID", 95, "number")

# Get field values
values = get_card_custom_fields("CARD_ID")
for value in values:
    print(f"Field {value['idCustomField']}: {value.get('value', value.get('idValue'))}")
```

## Complete Examples

### Example 1: Sprint Board Automation

```python
#!/usr/bin/env python3
"""sprint_automation.py - Automate sprint board management"""

from trello import TrelloClient
from datetime import datetime, timedelta
import os
import json

def create_sprint_board(client, sprint_name, team_members=None):
    """
    Create a new sprint board with standard structure.

    Args:
        client: TrelloClient instance
        sprint_name: Name for the sprint
        team_members: List of member usernames to add

    Returns:
        Created board object
    """
    # Create board
    board = client.add_board(
        board_name=f"Sprint: {sprint_name}",
        permission_level="private"
    )
    print(f"Created board: {board.name}")

    # Create standard sprint lists
    lists_config = [
        {"name": "Backlog", "pos": "bottom"},
        {"name": "To Do", "pos": "bottom"},
        {"name": "In Progress", "pos": "bottom"},
        {"name": "In Review", "pos": "bottom"},
        {"name": "Done", "pos": "bottom"},
    ]

    created_lists = {}
    for list_cfg in lists_config:
        new_list = board.add_list(name=list_cfg["name"])
        created_lists[list_cfg["name"]] = new_list
        print(f"  Created list: {list_cfg['name']}")

    # Create standard labels
    labels_config = [
        {"name": "Bug", "color": "red"},
        {"name": "Feature", "color": "green"},
        {"name": "Enhancement", "color": "blue"},
        {"name": "Technical Debt", "color": "orange"},
        {"name": "Documentation", "color": "purple"},
        {"name": "Blocked", "color": "black"},
    ]

    for label_cfg in labels_config:
        board.add_label(name=label_cfg["name"], color=label_cfg["color"])
        print(f"  Created label: {label_cfg['name']}")

    # Add sprint info card
    sprint_end = datetime.now() + timedelta(days=14)
    info_card = created_lists["Backlog"].add_card(
        name="Sprint Information",
        desc=f"""# Sprint: {sprint_name}

**Start Date:** {datetime.now().strftime('%Y-%m-%d')}
**End Date:** {sprint_end.strftime('%Y-%m-%d')}

## Sprint Goals
- [ ] Goal 1
- [ ] Goal 2
- [ ] Goal 3

## Team
Add team member assignments here.
""",
        position="top"
    )

    # Add checklist for sprint ceremonies
    info_card.add_checklist(
        title="Sprint Ceremonies",
        items=[
            "Sprint Planning",
            "Daily Standup (Day 1-10)",
            "Sprint Review",
            "Sprint Retrospective"
        ]
    )

    return board, created_lists


def add_sprint_tasks(board, lists, tasks):
    """
    Add tasks to the sprint board.

    Args:
        board: Board object
        lists: Dictionary of list objects by name
        tasks: List of task dictionaries
    """
    labels = {label.name: label for label in board.get_labels()}

    for task in tasks:
        list_name = task.get("list", "Backlog")
        target_list = lists.get(list_name)

        if not target_list:
            print(f"Warning: List '{list_name}' not found")
            continue

        # Create card
        card = target_list.add_card(
            name=task["name"],
            desc=task.get("description", ""),
            due=task.get("due_date")
        )

        # Add labels
        for label_name in task.get("labels", []):
            if label_name in labels:
                card.add_label(labels[label_name])

        # Add checklist if provided
        if "checklist" in task:
            card.add_checklist(
                title=task["checklist"].get("name", "Tasks"),
                items=task["checklist"].get("items", [])
            )

        print(f"  Created task: {task['name']}")


def generate_sprint_report(board):
    """Generate sprint progress report."""
    lists = board.list_lists()
    list_cards = {}

    for lst in lists:
        cards = lst.list_cards()
        list_cards[lst.name] = cards

    total_cards = sum(len(cards) for cards in list_cards.values())
    done_cards = len(list_cards.get("Done", []))

    report = {
        "board_name": board.name,
        "generated_at": datetime.now().isoformat(),
        "total_tasks": total_cards,
        "completed_tasks": done_cards,
        "completion_percentage": round(done_cards / total_cards * 100, 1) if total_cards > 0 else 0,
        "by_list": {}
    }

    for list_name, cards in list_cards.items():
        report["by_list"][list_name] = {
            "count": len(cards),
            "cards": [{"name": c.name, "due": str(c.due_date)} for c in cards]
        }

    return report


# Example usage
if __name__ == "__main__":
    client = TrelloClient(
        api_key=os.environ["TRELLO_API_KEY"],
        token=os.environ["TRELLO_TOKEN"]
    )

    # Create sprint board
    board, lists = create_sprint_board(
        client,
        sprint_name="2025-W05",
        team_members=["user1", "user2"]
    )

    # Add sample tasks
    tasks = [
        {
            "name": "Implement user authentication",
            "description": "Add JWT-based authentication",
            "list": "To Do",
            "labels": ["Feature"],
            "due_date": "2025-02-07",
            "checklist": {
                "name": "Implementation Steps",
                "items": ["Design API", "Implement backend", "Add tests", "Update docs"]
            }
        },
        {
            "name": "Fix login page bug",
            "description": "Users can't login with special characters",
            "list": "To Do",
            "labels": ["Bug"],
            "due_date": "2025-02-03"
        },
        {
            "name": "Refactor database queries",
            "description": "Optimize slow queries",
            "list": "Backlog",
            "labels": ["Technical Debt"]
        }
    ]

    add_sprint_tasks(board, lists, tasks)

    # Generate report
    report = generate_sprint_report(board)
    print(f"\n{'='*50}")
    print(f"Sprint Report: {report['board_name']}")
    print(f"{'='*50}")
    print(f"Total Tasks: {report['total_tasks']}")
    print(f"Completed: {report['completed_tasks']} ({report['completion_percentage']}%)")
```

### Example 2: Card Migration Tool

```python
#!/usr/bin/env python3
"""card_migration.py - Migrate cards between boards"""

from trello import TrelloClient
import os
import json
from datetime import datetime

def migrate_cards(
    client,
    source_board_id,
    target_board_id,
    list_mapping,
    include_labels=True,
    include_checklists=True,
    include_attachments=False,
    archive_source=False
):
    """
    Migrate cards from source board to target board.

    Args:
        client: TrelloClient instance
        source_board_id: Source board ID
        target_board_id: Target board ID
        list_mapping: Dict mapping source list names to target list names
        include_labels: Copy labels to new cards
        include_checklists: Copy checklists to new cards
        include_attachments: Copy attachments (URLs only)
        archive_source: Archive source cards after migration

    Returns:
        Migration report dictionary
    """
    source_board = client.get_board(source_board_id)
    target_board = client.get_board(target_board_id)

    # Build target lists lookup
    target_lists = {lst.name: lst for lst in target_board.list_lists()}

    # Build target labels lookup
    target_labels = {}
    if include_labels:
        for label in target_board.get_labels():
            target_labels[label.name] = label

    report = {
        "started_at": datetime.now().isoformat(),
        "source_board": source_board.name,
        "target_board": target_board.name,
        "migrated": [],
        "skipped": [],
        "errors": []
    }

    # Process each source list
    for source_list in source_board.list_lists():
        source_list_name = source_list.name

        # Check if this list should be migrated
        if source_list_name not in list_mapping:
            print(f"Skipping list: {source_list_name} (not in mapping)")
            continue

        target_list_name = list_mapping[source_list_name]
        target_list = target_lists.get(target_list_name)

        if not target_list:
            print(f"Warning: Target list '{target_list_name}' not found")
            continue

        print(f"\nMigrating: {source_list_name} -> {target_list_name}")

        # Migrate each card
        for card in source_list.list_cards():
            try:
                # Create new card
                new_card = target_list.add_card(
                    name=card.name,
                    desc=card.description,
                    due=str(card.due_date) if card.due_date else None
                )

                # Copy labels
                if include_labels:
                    for label in card.labels or []:
                        if label.name in target_labels:
                            new_card.add_label(target_labels[label.name])

                # Copy checklists
                if include_checklists:
                    for checklist in card.fetch_checklists():
                        items = [item["name"] for item in checklist.items]
                        new_checklist = new_card.add_checklist(
                            title=checklist.name,
                            items=items
                        )
                        # Copy checked state
                        for item in checklist.items:
                            if item["checked"]:
                                new_checklist.set_checklist_item(
                                    item["name"],
                                    checked=True
                                )

                # Archive source card if requested
                if archive_source:
                    card.set_closed(True)

                report["migrated"].append({
                    "name": card.name,
                    "source_list": source_list_name,
                    "target_list": target_list_name,
                    "new_card_id": new_card.id
                })

                print(f"  Migrated: {card.name}")

            except Exception as e:
                report["errors"].append({
                    "name": card.name,
                    "error": str(e)
                })
                print(f"  Error migrating {card.name}: {e}")

    report["completed_at"] = datetime.now().isoformat()
    report["total_migrated"] = len(report["migrated"])
    report["total_errors"] = len(report["errors"])

    return report


# Example usage
if __name__ == "__main__":
    client = TrelloClient(
        api_key=os.environ["TRELLO_API_KEY"],
        token=os.environ["TRELLO_TOKEN"]
    )

    # Define list mapping
    list_mapping = {
        "Backlog": "Product Backlog",
        "To Do": "Sprint Backlog",
        "In Progress": "In Development",
        "Done": "Completed"
    }

    report = migrate_cards(
        client=client,
        source_board_id="SOURCE_BOARD_ID",
        target_board_id="TARGET_BOARD_ID",
        list_mapping=list_mapping,
        include_labels=True,
        include_checklists=True,
        archive_source=False
    )

    # Save report
    with open("migration_report.json", "w") as f:
        json.dump(report, f, indent=2)

    print(f"\n{'='*50}")
    print(f"Migration Complete!")
    print(f"Migrated: {report['total_migrated']} cards")
    print(f"Errors: {report['total_errors']}")
```

### Example 3: Board Analytics Dashboard

```python
#!/usr/bin/env python3
"""board_analytics.py - Generate board analytics"""

from trello import TrelloClient
from datetime import datetime, timedelta
from collections import defaultdict
import os
import json

def analyze_board(client, board_id, days_back=30):
    """
    Generate comprehensive analytics for a board.

    Args:
        client: TrelloClient instance
        board_id: Board ID to analyze
        days_back: Number of days of history to analyze

    Returns:
        Analytics dictionary
    """
    board = client.get_board(board_id)
    cutoff_date = datetime.now() - timedelta(days=days_back)

    analytics = {
        "board_name": board.name,
        "analyzed_at": datetime.now().isoformat(),
        "period_days": days_back,
        "summary": {},
        "lists": {},
        "labels": {},
        "members": {},
        "cards": {
            "total": 0,
            "with_due_date": 0,
            "overdue": 0,
            "completed": 0
        }
    }

    # Analyze lists
    lists = board.list_lists()
    for lst in lists:
        cards = lst.list_cards()
        analytics["lists"][lst.name] = {
            "card_count": len(cards),
            "cards": []
        }

        for card in cards:
            analytics["cards"]["total"] += 1

            card_info = {
                "name": card.name,
                "has_due": card.due_date is not None,
                "labels": [l.name for l in (card.labels or [])],
                "members": len(card.member_ids) if card.member_ids else 0,
                "checklists": len(card.fetch_checklists())
            }

            if card.due_date:
                analytics["cards"]["with_due_date"] += 1
                if card.due_date < datetime.now() and not card.is_due_complete:
                    analytics["cards"]["overdue"] += 1
                    card_info["overdue"] = True

            analytics["lists"][lst.name]["cards"].append(card_info)

    # Identify done list (common names)
    done_lists = ["Done", "Completed", "Finished", "Closed"]
    for done_name in done_lists:
        if done_name in analytics["lists"]:
            analytics["cards"]["completed"] = analytics["lists"][done_name]["card_count"]
            break

    # Analyze labels
    labels = board.get_labels()
    label_usage = defaultdict(int)

    for lst_data in analytics["lists"].values():
        for card in lst_data["cards"]:
            for label in card["labels"]:
                label_usage[label] += 1

    analytics["labels"] = dict(label_usage)

    # Calculate summary metrics
    total = analytics["cards"]["total"]
    analytics["summary"] = {
        "total_cards": total,
        "total_lists": len(lists),
        "total_labels": len(labels),
        "completion_rate": round(
            analytics["cards"]["completed"] / total * 100, 1
        ) if total > 0 else 0,
        "overdue_rate": round(
            analytics["cards"]["overdue"] / total * 100, 1
        ) if total > 0 else 0,
        "due_date_coverage": round(
            analytics["cards"]["with_due_date"] / total * 100, 1
        ) if total > 0 else 0
    }

    return analytics


def generate_report_markdown(analytics):
    """Generate markdown report from analytics."""
    report = f"""# Board Analytics Report

**Board:** {analytics['board_name']}
**Generated:** {analytics['analyzed_at']}
**Period:** Last {analytics['period_days']} days

## Summary

| Metric | Value |
|--------|-------|
| Total Cards | {analytics['summary']['total_cards']} |
| Total Lists | {analytics['summary']['total_lists']} |
| Completion Rate | {analytics['summary']['completion_rate']}% |
| Overdue Rate | {analytics['summary']['overdue_rate']}% |
| Due Date Coverage | {analytics['summary']['due_date_coverage']}% |

## Cards by List

"""

    for list_name, list_data in analytics["lists"].items():
        report += f"### {list_name} ({list_data['card_count']} cards)\n\n"

        if list_data["cards"]:
            for card in list_data["cards"][:5]:  # Show top 5
                overdue_marker = " [OVERDUE]" if card.get("overdue") else ""
                report += f"- {card['name']}{overdue_marker}\n"
            if len(list_data["cards"]) > 5:
                report += f"- ... and {len(list_data['cards']) - 5} more\n"
        report += "\n"

    report += "## Label Usage\n\n"
    report += "| Label | Count |\n"
    report += "|-------|-------|\n"

    for label, count in sorted(
        analytics["labels"].items(),
        key=lambda x: x[1],
        reverse=True
    ):
        report += f"| {label} | {count} |\n"

    return report


# Example usage
if __name__ == "__main__":
    client = TrelloClient(
        api_key=os.environ["TRELLO_API_KEY"],
        token=os.environ["TRELLO_TOKEN"]
    )

    # Analyze board
    analytics = analyze_board(
        client=client,
        board_id="BOARD_ID",
        days_back=30
    )

    # Save JSON
    with open("board_analytics.json", "w") as f:
        json.dump(analytics, f, indent=2, default=str)

    # Generate markdown report
    report = generate_report_markdown(analytics)
    with open("board_report.md", "w") as f:
        f.write(report)

    print("Analytics generated!")
    print(f"Total cards: {analytics['summary']['total_cards']}")
    print(f"Completion rate: {analytics['summary']['completion_rate']}%")
```

## Integration Examples

### Trello with GitHub Actions

```yaml
# .github/workflows/trello-sync.yml
name: Sync Issues to Trello

on:
  issues:
    types: [opened, labeled]

jobs:
  create-card:
    runs-on: ubuntu-latest
    steps:
      - name: Create Trello Card
        env:
          TRELLO_API_KEY: ${{ secrets.TRELLO_API_KEY }}
          TRELLO_TOKEN: ${{ secrets.TRELLO_TOKEN }}
          TRELLO_LIST_ID: ${{ secrets.TRELLO_LIST_ID }}
        run: |
          curl -s -X POST "https://api.trello.com/1/cards" \
            -d "key=$TRELLO_API_KEY" \
            -d "token=$TRELLO_TOKEN" \
            -d "idList=$TRELLO_LIST_ID" \
            -d "name=${{ github.event.issue.title }}" \
            -d "desc=${{ github.event.issue.body }}" \
            -d "urlSource=${{ github.event.issue.html_url }}"
```

### Trello with Slack

```python
#!/usr/bin/env python3
"""trello_slack_integration.py - Notify Slack on Trello updates"""

import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

SLACK_WEBHOOK_URL = os.environ["SLACK_WEBHOOK_URL"]

@app.route("/webhook/trello", methods=["HEAD", "POST"])
def trello_webhook():
    if request.method == "HEAD":
        return "", 200

    data = request.json
    action = data.get("action", {})
    action_type = action.get("type")

    # Build Slack message
    message = None

    if action_type == "createCard":
        card = action["data"]["card"]
        list_name = action["data"]["list"]["name"]
        member = action["memberCreator"]["fullName"]

        message = {
            "text": f"New card created by {member}",
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*New Card Created*\n"
                                f"*Card:* {card['name']}\n"
                                f"*List:* {list_name}\n"
                                f"*By:* {member}"
                    }
                }
            ]
        }

    elif action_type == "updateCard" and "listAfter" in action["data"]:
        card = action["data"]["card"]
        list_before = action["data"]["listBefore"]["name"]
        list_after = action["data"]["listAfter"]["name"]
        member = action["memberCreator"]["fullName"]

        message = {
            "text": f"Card moved by {member}",
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Card Moved*\n"
                                f"*Card:* {card['name']}\n"
                                f"*From:* {list_before} -> *To:* {list_after}\n"
                                f"*By:* {member}"
                    }
                }
            ]
        }

    if message:
        requests.post(SLACK_WEBHOOK_URL, json=message)

    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(port=5000)
```

## Best Practices

### 1. Use Batch Operations

```python
# GOOD: Batch operations when possible
import requests

def batch_create_cards(list_id, cards):
    """Create multiple cards efficiently."""
    for card in cards:
        requests.post(
            "https://api.trello.com/1/cards",
            data={
                "key": API_KEY,
                "token": TOKEN,
                "idList": list_id,
                **card
            }
        )
        # Small delay to avoid rate limits
        time.sleep(0.1)

# AVOID: Individual requests without batching consideration
```

### 2. Handle Rate Limits

```python
import time
from functools import wraps

def rate_limit(max_per_second=10):
    """Rate limit decorator."""
    min_interval = 1.0 / max_per_second
    last_call = [0.0]

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_call[0]
            if elapsed < min_interval:
                time.sleep(min_interval - elapsed)
            result = func(*args, **kwargs)
            last_call[0] = time.time()
            return result
        return wrapper
    return decorator

@rate_limit(max_per_second=10)
def api_call(endpoint, **kwargs):
    return requests.get(endpoint, params=kwargs)
```

### 3. Cache Board Data

```python
from functools import lru_cache
from datetime import datetime, timedelta

class TrelloCache:
    def __init__(self, ttl_seconds=300):
        self.ttl = ttl_seconds
        self.cache = {}

    def get_board(self, client, board_id):
        key = f"board_{board_id}"
        now = datetime.now()

        if key in self.cache:
            data, timestamp = self.cache[key]
            if now - timestamp < timedelta(seconds=self.ttl):
                return data

        board = client.get_board(board_id)
        self.cache[key] = (board, now)
        return board
```

### 4. Error Handling

```python
import requests
from requests.exceptions import RequestException

def safe_trello_request(method, url, **kwargs):
    """Make Trello API request with error handling."""
    try:
        response = requests.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            # Rate limited - wait and retry
            time.sleep(10)
            return safe_trello_request(method, url, **kwargs)
        elif e.response.status_code == 401:
            raise Exception("Invalid API credentials")
        else:
            raise
    except RequestException as e:
        raise Exception(f"Network error: {e}")
```

## Troubleshooting

### Common Issues

**Issue: 401 Unauthorized**
```bash
# Verify credentials
curl -s "https://api.trello.com/1/members/me?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN"

# Regenerate token if needed:
# https://trello.com/1/authorize?expiration=never&scope=read,write&response_type=token&key=YOUR_API_KEY
```

**Issue: 429 Rate Limited**
```python
# Implement exponential backoff
import time

def retry_with_backoff(func, max_retries=5):
    for i in range(max_retries):
        try:
            return func()
        except Exception as e:
            if "429" in str(e):
                wait = 2 ** i
                print(f"Rate limited, waiting {wait}s")
                time.sleep(wait)
            else:
                raise
```

**Issue: Card not found**
```python
# Cards may be archived - search with filter
cards = board.get_cards(card_filter="all")  # Includes archived
```

**Issue: Webhook not receiving events**
```bash
# Check webhook status
curl -s "https://api.trello.com/1/tokens/$TRELLO_TOKEN/webhooks?key=$TRELLO_API_KEY" | jq

# Ensure callback URL is HTTPS and publicly accessible
```

## Version History

- **1.0.0** (2026-01-17): Initial release
  - Board, list, card management
  - Labels and checklists
  - Member management
  - Webhook integration
  - Custom fields
  - Sprint automation example
  - Card migration tool
  - Board analytics
  - GitHub Actions integration
  - Slack integration

## Resources

- **Trello REST API**: https://developer.atlassian.com/cloud/trello/rest/
- **py-trello GitHub**: https://github.com/sarumont/py-trello
- **Trello Developer Portal**: https://developer.atlassian.com/cloud/trello/
- **Webhook Guide**: https://developer.atlassian.com/cloud/trello/guides/rest-api/webhooks/

---

**Automate your Kanban workflows with Trello API - boards, lists, cards, and beyond!**
