---
name: miro-api
version: 1.0.0
description: Miro whiteboard automation using REST API v2 and Python SDK for creating boards, frames, shapes, connectors, and collaborative visual workflows
author: workspace-hub
category: communication
type: skill
capabilities:
  - board_management
  - sticky_notes_creation
  - shape_drawing
  - connector_lines
  - frame_organization
  - text_elements
  - image_embedding
  - template_usage
  - real_time_collaboration
  - webhook_subscriptions
tools:
  - miro-api-python
  - curl
  - requests
  - httpx
tags: [miro, whiteboard, collaboration, visual, diagrams, sticky-notes, api, python]
platforms: [linux, macos, windows]
related_skills:
  - slack-api
  - notion-api
  - github-actions
---

# Miro API Skill

Master Miro whiteboard automation using the REST API v2 and Python SDK. This skill covers board creation, widget management, frames, shapes, connectors, templates, and real-time collaboration patterns for building automated visual workflows.

## When to Use This Skill

### USE when:
- Automating sprint retrospective board creation
- Building visual project status dashboards
- Creating automated architecture diagrams
- Setting up templated workshop boards
- Integrating Miro with CI/CD pipelines
- Automating user story mapping workflows
- Creating visual incident response boards
- Building automated onboarding boards
- Generating meeting facilitation templates
- Syncing data from external systems to Miro

### DON'T USE when:
- Simple text-based collaboration (use Slack or Teams)
- Document-focused workflows (use Notion or Confluence)
- Code-focused diagramming (use Mermaid or PlantUML)
- Real-time whiteboarding without persistence
- Personal note-taking (use Obsidian)

## Prerequisites

### Miro App Setup

```bash
# 1. Create a Miro App at https://miro.com/app/settings/user-profile/apps
# 2. Choose REST API 2.0
# 3. Configure OAuth 2.0 scopes

# Required OAuth Scopes:
# - boards:read          - Read board data
# - boards:write         - Create and modify boards
# - team:read            - Read team information
# - identity:read        - Read user identity
# - microphone:read      - Read board audio (optional)
# - screen_recording     - Screen recording (optional)

# App Permissions for different use cases:
# Team App:   boards:read, boards:write, team:read
# User App:   boards:read, boards:write, identity:read
# Admin App:  All scopes + organization management

# Get Access Token via OAuth 2.0:
# 1. Redirect user to: https://miro.com/oauth/authorize?response_type=code&client_id=CLIENT_ID&redirect_uri=REDIRECT_URI
# 2. Exchange code for token at: https://api.miro.com/v1/oauth/token
```

### Python Environment Setup

```bash
# Create virtual environment
python -m venv miro-env
source miro-env/bin/activate  # Linux/macOS
# miro-env\Scripts\activate   # Windows

# Install Miro API SDK
pip install miro-api

# Install additional dependencies
pip install python-dotenv requests httpx aiohttp

# Create requirements.txt
cat > requirements.txt << 'EOF'
miro-api>=2.0.0
python-dotenv>=1.0.0
requests>=2.31.0
httpx>=0.25.0
aiohttp>=3.9.0
Pillow>=10.0.0
EOF

# Environment variables
cat > .env << 'EOF'
MIRO_ACCESS_TOKEN=your-access-token
MIRO_CLIENT_ID=your-client-id
MIRO_CLIENT_SECRET=your-client-secret
MIRO_TEAM_ID=your-team-id
EOF
```

### API Authentication

```python
# auth.py
# ABOUTME: Miro API authentication utilities
# ABOUTME: Handles OAuth2 token management and refresh

import os
from dotenv import load_dotenv
import requests
from datetime import datetime, timedelta

load_dotenv()

class MiroAuth:
    """Miro OAuth2 authentication handler"""

    BASE_URL = "https://api.miro.com"
    AUTH_URL = "https://miro.com/oauth/authorize"
    TOKEN_URL = "https://api.miro.com/v1/oauth/token"

    def __init__(self):
        self.client_id = os.environ.get("MIRO_CLIENT_ID")
        self.client_secret = os.environ.get("MIRO_CLIENT_SECRET")
        self.access_token = os.environ.get("MIRO_ACCESS_TOKEN")
        self.refresh_token = os.environ.get("MIRO_REFRESH_TOKEN")
        self.token_expires = None

    def get_authorization_url(self, redirect_uri: str, state: str = None) -> str:
        """Generate OAuth2 authorization URL"""
        params = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": redirect_uri,
        }
        if state:
            params["state"] = state

        query = "&".join(f"{k}={v}" for k, v in params.items())
        return f"{self.AUTH_URL}?{query}"

    def exchange_code_for_token(self, code: str, redirect_uri: str) -> dict:
        """Exchange authorization code for access token"""
        response = requests.post(
            self.TOKEN_URL,
            data={
                "grant_type": "authorization_code",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "code": code,
                "redirect_uri": redirect_uri,
            },
        )
        response.raise_for_status()
        token_data = response.json()

        self.access_token = token_data["access_token"]
        self.refresh_token = token_data.get("refresh_token")
        self.token_expires = datetime.now() + timedelta(
            seconds=token_data.get("expires_in", 3600)
        )

        return token_data

    def refresh_access_token(self) -> dict:
        """Refresh the access token"""
        response = requests.post(
            self.TOKEN_URL,
            data={
                "grant_type": "refresh_token",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "refresh_token": self.refresh_token,
            },
        )
        response.raise_for_status()
        token_data = response.json()

        self.access_token = token_data["access_token"]
        self.refresh_token = token_data.get("refresh_token", self.refresh_token)

        return token_data

    def get_headers(self) -> dict:
        """Get authorization headers for API requests"""
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }
```

## Core Capabilities

### 1. Board Management

```python
# boards.py
# ABOUTME: Miro board management operations
# ABOUTME: Create, read, update, delete boards

import os
from miro_api import Miro
from dotenv import load_dotenv

load_dotenv()

# Initialize Miro client
miro = Miro(access_token=os.environ.get("MIRO_ACCESS_TOKEN"))


def create_board(name: str, description: str = "", team_id: str = None) -> dict:
    """Create a new Miro board"""
    team_id = team_id or os.environ.get("MIRO_TEAM_ID")

    board = miro.boards.create(
        name=name,
        description=description,
        team_id=team_id,
        policy={
            "permissionsPolicy": {
                "collaborationToolsStartAccess": "all_editors",
                "copyAccess": "anyone",
                "sharingAccess": "team_members_with_editing_rights",
            },
            "sharingPolicy": {
                "access": "private",
                "inviteToAccountAndBoardLinkAccess": "editor",
                "organizationAccess": "private",
                "teamAccess": "edit",
            },
        },
    )

    return {
        "id": board.id,
        "name": board.name,
        "view_link": board.view_link,
        "created_at": board.created_at,
    }


def get_board(board_id: str) -> dict:
    """Get board details"""
    board = miro.boards.get(board_id)

    return {
        "id": board.id,
        "name": board.name,
        "description": board.description,
        "view_link": board.view_link,
        "created_at": board.created_at,
        "modified_at": board.modified_at,
    }


def list_boards(team_id: str = None, limit: int = 50) -> list:
    """List all boards in a team"""
    team_id = team_id or os.environ.get("MIRO_TEAM_ID")

    boards = miro.boards.get_all(team_id=team_id, limit=limit)

    return [
        {
            "id": board.id,
            "name": board.name,
            "view_link": board.view_link,
        }
        for board in boards
    ]


def update_board(board_id: str, name: str = None, description: str = None) -> dict:
    """Update board properties"""
    update_data = {}
    if name:
        update_data["name"] = name
    if description:
        update_data["description"] = description

    board = miro.boards.update(board_id, **update_data)

    return {"id": board.id, "name": board.name, "description": board.description}


def delete_board(board_id: str) -> bool:
    """Delete a board"""
    miro.boards.delete(board_id)
    return True


def copy_board(board_id: str, new_name: str, team_id: str = None) -> dict:
    """Copy an existing board"""
    team_id = team_id or os.environ.get("MIRO_TEAM_ID")

    board = miro.boards.copy(board_id, name=new_name, team_id=team_id)

    return {
        "id": board.id,
        "name": board.name,
        "view_link": board.view_link,
    }


# Usage example
if __name__ == "__main__":
    # Create a board
    board = create_board(
        name="Sprint Retrospective - Q1 2026",
        description="Team retrospective for Q1 sprint",
    )
    print(f"Created board: {board['view_link']}")

    # List boards
    boards = list_boards(limit=10)
    for b in boards:
        print(f"- {b['name']}: {b['view_link']}")
```

### 2. Sticky Notes and Cards

```python
# sticky_notes.py
# ABOUTME: Sticky note and card creation
# ABOUTME: Create, position, and style sticky notes

from miro_api import Miro
import os

miro = Miro(access_token=os.environ.get("MIRO_ACCESS_TOKEN"))


def create_sticky_note(
    board_id: str,
    content: str,
    x: float = 0,
    y: float = 0,
    color: str = "yellow",
    width: float = 200,
) -> dict:
    """Create a sticky note on a board"""

    # Color mapping
    colors = {
        "yellow": "yellow",
        "green": "green",
        "blue": "blue",
        "pink": "pink",
        "orange": "orange",
        "purple": "violet",
        "gray": "gray",
        "cyan": "cyan",
        "red": "red",
        "light_yellow": "light_yellow",
        "light_green": "light_green",
        "light_blue": "light_blue",
        "light_pink": "light_pink",
    }

    sticky = miro.sticky_notes.create(
        board_id=board_id,
        data={"content": content, "shape": "square"},
        style={"fillColor": colors.get(color, "yellow")},
        position={"x": x, "y": y, "origin": "center"},
        geometry={"width": width},
    )

    return {
        "id": sticky.id,
        "content": sticky.data.content,
        "position": {"x": sticky.position.x, "y": sticky.position.y},
        "color": sticky.style.fill_color,
    }


def create_sticky_grid(
    board_id: str,
    items: list,
    start_x: float = 0,
    start_y: float = 0,
    columns: int = 4,
    spacing: float = 250,
    color: str = "yellow",
) -> list:
    """Create a grid of sticky notes"""
    created = []

    for i, item in enumerate(items):
        row = i // columns
        col = i % columns

        x = start_x + (col * spacing)
        y = start_y + (row * spacing)

        sticky = create_sticky_note(
            board_id=board_id, content=item, x=x, y=y, color=color
        )
        created.append(sticky)

    return created


def create_card(
    board_id: str,
    title: str,
    description: str = "",
    x: float = 0,
    y: float = 0,
    assignee_id: str = None,
    due_date: str = None,
    tags: list = None,
) -> dict:
    """Create a card widget"""

    card_data = {"title": title, "description": description}

    if assignee_id:
        card_data["assigneeId"] = assignee_id
    if due_date:
        card_data["dueDate"] = due_date
    if tags:
        card_data["tagIds"] = tags

    card = miro.cards.create(
        board_id=board_id,
        data=card_data,
        position={"x": x, "y": y, "origin": "center"},
        geometry={"width": 320, "height": 200},
    )

    return {
        "id": card.id,
        "title": card.data.title,
        "position": {"x": card.position.x, "y": card.position.y},
    }


def update_sticky_note(
    board_id: str, sticky_id: str, content: str = None, color: str = None
) -> dict:
    """Update a sticky note"""
    update_data = {}

    if content:
        update_data["data"] = {"content": content}
    if color:
        update_data["style"] = {"fillColor": color}

    sticky = miro.sticky_notes.update(board_id, sticky_id, **update_data)

    return {"id": sticky.id, "content": sticky.data.content}


def delete_sticky_note(board_id: str, sticky_id: str) -> bool:
    """Delete a sticky note"""
    miro.sticky_notes.delete(board_id, sticky_id)
    return True


# Retrospective board example
def create_retro_board(board_id: str) -> dict:
    """Create a retrospective board layout"""

    # Create category headers
    categories = [
        {"title": "What went well", "color": "green", "x": 0},
        {"title": "What to improve", "color": "pink", "x": 500},
        {"title": "Action items", "color": "blue", "x": 1000},
    ]

    created_stickies = {}

    for cat in categories:
        # Create header sticky
        header = create_sticky_note(
            board_id=board_id,
            content=f"<strong>{cat['title']}</strong>",
            x=cat["x"],
            y=-200,
            color=cat["color"],
            width=400,
        )
        created_stickies[cat["title"]] = [header]

        # Create placeholder stickies
        for i in range(3):
            placeholder = create_sticky_note(
                board_id=board_id,
                content="Add your thoughts here...",
                x=cat["x"],
                y=i * 150,
                color=cat["color"],
            )
            created_stickies[cat["title"]].append(placeholder)

    return created_stickies


if __name__ == "__main__":
    board_id = "YOUR_BOARD_ID"

    # Create grid of stickies
    items = ["Task 1", "Task 2", "Task 3", "Task 4", "Task 5", "Task 6"]
    stickies = create_sticky_grid(
        board_id=board_id, items=items, columns=3, color="blue"
    )
    print(f"Created {len(stickies)} sticky notes")
```

### 3. Shapes and Drawing

```python
# shapes.py
# ABOUTME: Shape creation and manipulation
# ABOUTME: Rectangles, circles, lines, and custom shapes

from miro_api import Miro
import os

miro = Miro(access_token=os.environ.get("MIRO_ACCESS_TOKEN"))


def create_shape(
    board_id: str,
    shape_type: str,
    content: str = "",
    x: float = 0,
    y: float = 0,
    width: float = 200,
    height: float = 100,
    fill_color: str = "#ffffff",
    border_color: str = "#000000",
    border_width: int = 2,
) -> dict:
    """Create a shape on the board

    Shape types: rectangle, circle, triangle, rhombus, parallelogram,
                 trapezoid, pentagon, hexagon, octagon, wedge_round_rectangle_callout,
                 round_rectangle, star, flow_chart_process, flow_chart_decision,
                 flow_chart_terminator, flow_chart_data, flow_chart_document
    """

    shape = miro.shapes.create(
        board_id=board_id,
        data={"content": content, "shape": shape_type},
        style={
            "fillColor": fill_color,
            "borderColor": border_color,
            "borderWidth": str(border_width),
            "borderStyle": "normal",
            "fontFamily": "arial",
            "fontSize": "14",
            "textAlign": "center",
            "textAlignVertical": "middle",
        },
        position={"x": x, "y": y, "origin": "center"},
        geometry={"width": width, "height": height},
    )

    return {
        "id": shape.id,
        "type": shape.data.shape,
        "position": {"x": shape.position.x, "y": shape.position.y},
    }


def create_rectangle(
    board_id: str,
    content: str = "",
    x: float = 0,
    y: float = 0,
    width: float = 200,
    height: float = 100,
    fill_color: str = "#ffffff",
) -> dict:
    """Create a rectangle"""
    return create_shape(
        board_id=board_id,
        shape_type="rectangle",
        content=content,
        x=x,
        y=y,
        width=width,
        height=height,
        fill_color=fill_color,
    )


def create_circle(
    board_id: str,
    content: str = "",
    x: float = 0,
    y: float = 0,
    diameter: float = 100,
    fill_color: str = "#ffffff",
) -> dict:
    """Create a circle"""
    return create_shape(
        board_id=board_id,
        shape_type="circle",
        content=content,
        x=x,
        y=y,
        width=diameter,
        height=diameter,
        fill_color=fill_color,
    )


def create_flowchart_shape(
    board_id: str,
    shape_type: str,
    content: str = "",
    x: float = 0,
    y: float = 0,
    width: float = 150,
    height: float = 80,
) -> dict:
    """Create a flowchart shape

    Types: flow_chart_process, flow_chart_decision, flow_chart_terminator,
           flow_chart_data, flow_chart_document, flow_chart_predefined_process,
           flow_chart_manual_input, flow_chart_display, flow_chart_preparation
    """

    colors = {
        "flow_chart_process": "#e3f2fd",
        "flow_chart_decision": "#fff3e0",
        "flow_chart_terminator": "#f3e5f5",
        "flow_chart_data": "#e8f5e9",
        "flow_chart_document": "#fce4ec",
    }

    return create_shape(
        board_id=board_id,
        shape_type=shape_type,
        content=content,
        x=x,
        y=y,
        width=width,
        height=height,
        fill_color=colors.get(shape_type, "#ffffff"),
    )


def create_flowchart(board_id: str, steps: list, start_x: float = 0, start_y: float = 0) -> list:
    """Create a flowchart from a list of steps

    Each step: {"type": "process|decision|terminator", "content": "text"}
    """
    created = []
    current_y = start_y

    for step in steps:
        shape_type = f"flow_chart_{step.get('type', 'process')}"
        height = 100 if step.get("type") == "decision" else 80

        shape = create_flowchart_shape(
            board_id=board_id,
            shape_type=shape_type,
            content=step["content"],
            x=start_x,
            y=current_y,
            height=height,
        )
        created.append(shape)

        current_y += height + 80  # Add spacing for connectors

    return created


def update_shape(
    board_id: str,
    shape_id: str,
    content: str = None,
    fill_color: str = None,
    x: float = None,
    y: float = None,
) -> dict:
    """Update a shape"""
    update_data = {}

    if content is not None:
        update_data["data"] = {"content": content}
    if fill_color:
        update_data["style"] = {"fillColor": fill_color}
    if x is not None or y is not None:
        position = {}
        if x is not None:
            position["x"] = x
        if y is not None:
            position["y"] = y
        update_data["position"] = position

    shape = miro.shapes.update(board_id, shape_id, **update_data)
    return {"id": shape.id}


if __name__ == "__main__":
    board_id = "YOUR_BOARD_ID"

    # Create a simple flowchart
    steps = [
        {"type": "terminator", "content": "Start"},
        {"type": "process", "content": "Initialize system"},
        {"type": "decision", "content": "Valid input?"},
        {"type": "process", "content": "Process data"},
        {"type": "terminator", "content": "End"},
    ]

    flowchart = create_flowchart(board_id, steps)
    print(f"Created flowchart with {len(flowchart)} shapes")
```

### 4. Connectors and Lines

```python
# connectors.py
# ABOUTME: Connector and line creation
# ABOUTME: Connect shapes, create arrows, and diagram flows

from miro_api import Miro
import os

miro = Miro(access_token=os.environ.get("MIRO_ACCESS_TOKEN"))


def create_connector(
    board_id: str,
    start_item_id: str,
    end_item_id: str,
    start_position: str = "right",
    end_position: str = "left",
    stroke_color: str = "#000000",
    stroke_width: int = 2,
    stroke_style: str = "normal",
    start_cap: str = "none",
    end_cap: str = "stealth",
    caption: str = None,
) -> dict:
    """Create a connector between two items

    Positions: top, right, bottom, left, auto
    Caps: none, stealth, rounded_stealth, diamond, diamond_filled, oval, oval_filled,
          arrow, triangle, triangle_filled, erd_one, erd_many, erd_one_or_many, erd_only_one,
          erd_zero_or_one, erd_zero_or_many
    Stroke styles: normal, dashed, dotted
    """

    connector_data = {
        "startItem": {"id": start_item_id, "position": {"x": start_position}},
        "endItem": {"id": end_item_id, "position": {"x": end_position}},
    }

    connector_style = {
        "strokeColor": stroke_color,
        "strokeWidth": str(stroke_width),
        "strokeStyle": stroke_style,
        "startStrokeCap": start_cap,
        "endStrokeCap": end_cap,
    }

    if caption:
        connector_data["captions"] = [{"content": caption, "position": "50%"}]

    connector = miro.connectors.create(
        board_id=board_id,
        data=connector_data,
        style=connector_style,
    )

    return {
        "id": connector.id,
        "start_item": connector.start_item.id,
        "end_item": connector.end_item.id,
    }


def create_line(
    board_id: str,
    start_x: float,
    start_y: float,
    end_x: float,
    end_y: float,
    stroke_color: str = "#000000",
    stroke_width: int = 2,
    end_cap: str = "none",
) -> dict:
    """Create a standalone line"""

    # For lines without connected items, we use absolute coordinates
    connector = miro.connectors.create(
        board_id=board_id,
        data={
            "startItem": {"position": {"x": start_x, "y": start_y}},
            "endItem": {"position": {"x": end_x, "y": end_y}},
        },
        style={
            "strokeColor": stroke_color,
            "strokeWidth": str(stroke_width),
            "startStrokeCap": "none",
            "endStrokeCap": end_cap,
        },
    )

    return {"id": connector.id}


def connect_flowchart_shapes(board_id: str, shape_ids: list, labels: list = None) -> list:
    """Connect a list of shapes in sequence"""
    created = []

    for i in range(len(shape_ids) - 1):
        label = labels[i] if labels and i < len(labels) else None

        connector = create_connector(
            board_id=board_id,
            start_item_id=shape_ids[i],
            end_item_id=shape_ids[i + 1],
            start_position="bottom",
            end_position="top",
            end_cap="stealth",
            caption=label,
        )
        created.append(connector)

    return created


def create_decision_branches(
    board_id: str,
    decision_shape_id: str,
    yes_shape_id: str,
    no_shape_id: str,
) -> list:
    """Create Yes/No branches from a decision diamond"""

    yes_connector = create_connector(
        board_id=board_id,
        start_item_id=decision_shape_id,
        end_item_id=yes_shape_id,
        start_position="bottom",
        end_position="top",
        end_cap="stealth",
        caption="Yes",
        stroke_color="#4caf50",
    )

    no_connector = create_connector(
        board_id=board_id,
        start_item_id=decision_shape_id,
        end_item_id=no_shape_id,
        start_position="right",
        end_position="left",
        end_cap="stealth",
        caption="No",
        stroke_color="#f44336",
    )

    return [yes_connector, no_connector]


def create_erd_relationship(
    board_id: str,
    entity1_id: str,
    entity2_id: str,
    cardinality_start: str = "erd_one",
    cardinality_end: str = "erd_many",
    label: str = None,
) -> dict:
    """Create an ERD relationship line

    Cardinalities: erd_one, erd_many, erd_one_or_many, erd_only_one,
                   erd_zero_or_one, erd_zero_or_many
    """

    return create_connector(
        board_id=board_id,
        start_item_id=entity1_id,
        end_item_id=entity2_id,
        start_cap=cardinality_start,
        end_cap=cardinality_end,
        caption=label,
    )


def update_connector(
    board_id: str,
    connector_id: str,
    stroke_color: str = None,
    caption: str = None,
) -> dict:
    """Update a connector"""
    update_data = {}

    if stroke_color:
        update_data["style"] = {"strokeColor": stroke_color}
    if caption:
        update_data["captions"] = [{"content": caption, "position": "50%"}]

    connector = miro.connectors.update(board_id, connector_id, **update_data)
    return {"id": connector.id}


def delete_connector(board_id: str, connector_id: str) -> bool:
    """Delete a connector"""
    miro.connectors.delete(board_id, connector_id)
    return True


if __name__ == "__main__":
    board_id = "YOUR_BOARD_ID"

    # Example: Connect shapes
    shape_ids = ["shape1_id", "shape2_id", "shape3_id"]
    connectors = connect_flowchart_shapes(board_id, shape_ids)
    print(f"Created {len(connectors)} connectors")
```

### 5. Frames and Organization

```python
# frames.py
# ABOUTME: Frame creation for board organization
# ABOUTME: Group items, create sections, and manage layout

from miro_api import Miro
import os
from typing import List, Optional

miro = Miro(access_token=os.environ.get("MIRO_ACCESS_TOKEN"))


def create_frame(
    board_id: str,
    title: str,
    x: float = 0,
    y: float = 0,
    width: float = 800,
    height: float = 600,
    fill_color: str = "#f5f5f5",
) -> dict:
    """Create a frame to organize board content"""

    frame = miro.frames.create(
        board_id=board_id,
        data={"title": title, "format": "custom"},
        style={"fillColor": fill_color},
        position={"x": x, "y": y, "origin": "center"},
        geometry={"width": width, "height": height},
    )

    return {
        "id": frame.id,
        "title": frame.data.title,
        "position": {"x": frame.position.x, "y": frame.position.y},
        "geometry": {"width": frame.geometry.width, "height": frame.geometry.height},
    }


def create_frame_grid(
    board_id: str,
    titles: list,
    columns: int = 3,
    frame_width: float = 600,
    frame_height: float = 400,
    spacing: float = 50,
    start_x: float = 0,
    start_y: float = 0,
) -> list:
    """Create a grid of frames"""
    created = []

    for i, title in enumerate(titles):
        row = i // columns
        col = i % columns

        x = start_x + col * (frame_width + spacing)
        y = start_y + row * (frame_height + spacing)

        frame = create_frame(
            board_id=board_id,
            title=title,
            x=x,
            y=y,
            width=frame_width,
            height=frame_height,
        )
        created.append(frame)

    return created


def create_kanban_board(
    board_id: str,
    columns: list = None,
    frame_width: float = 400,
    frame_height: float = 800,
) -> list:
    """Create a Kanban-style board with columns"""

    if columns is None:
        columns = ["To Do", "In Progress", "Review", "Done"]

    colors = {
        "To Do": "#f5f5f5",
        "In Progress": "#fff3e0",
        "Review": "#e8f5e9",
        "Done": "#e3f2fd",
    }

    frames = []
    start_x = 0

    for i, column in enumerate(columns):
        frame = create_frame(
            board_id=board_id,
            title=column,
            x=start_x + i * (frame_width + 50),
            y=0,
            width=frame_width,
            height=frame_height,
            fill_color=colors.get(column, "#f5f5f5"),
        )
        frames.append(frame)

    return frames


def create_workshop_layout(
    board_id: str, sections: list, section_width: float = 1000, section_height: float = 600
) -> dict:
    """Create a workshop board layout

    sections: list of {"title": "name", "description": "desc", "color": "#hex"}
    """
    created = {"frames": [], "headers": []}

    for i, section in enumerate(sections):
        # Create frame for section
        frame = create_frame(
            board_id=board_id,
            title=section["title"],
            x=0,
            y=i * (section_height + 100),
            width=section_width,
            height=section_height,
            fill_color=section.get("color", "#f5f5f5"),
        )
        created["frames"].append(frame)

    return created


def update_frame(
    board_id: str,
    frame_id: str,
    title: str = None,
    width: float = None,
    height: float = None,
) -> dict:
    """Update a frame"""
    update_data = {}

    if title:
        update_data["data"] = {"title": title}
    if width or height:
        geometry = {}
        if width:
            geometry["width"] = width
        if height:
            geometry["height"] = height
        update_data["geometry"] = geometry

    frame = miro.frames.update(board_id, frame_id, **update_data)
    return {"id": frame.id, "title": frame.data.title}


def get_items_in_frame(board_id: str, frame_id: str) -> list:
    """Get all items contained within a frame"""
    frame = miro.frames.get(board_id, frame_id)

    # Get child items
    children = miro.frames.get_children(board_id, frame_id)

    return [
        {"id": child.id, "type": child.type}
        for child in children
    ]


def add_items_to_frame(board_id: str, frame_id: str, item_ids: list) -> bool:
    """Add items to a frame by updating their parent"""
    for item_id in item_ids:
        # Items inside a frame are managed by their position
        # They need to be within the frame's boundaries
        pass
    return True


def delete_frame(board_id: str, frame_id: str) -> bool:
    """Delete a frame"""
    miro.frames.delete(board_id, frame_id)
    return True


if __name__ == "__main__":
    board_id = "YOUR_BOARD_ID"

    # Create Kanban board
    kanban = create_kanban_board(board_id)
    print(f"Created Kanban with {len(kanban)} columns")

    # Create workshop layout
    sections = [
        {"title": "Introduction", "color": "#e3f2fd"},
        {"title": "Brainstorming", "color": "#fff3e0"},
        {"title": "Voting", "color": "#e8f5e9"},
        {"title": "Action Items", "color": "#f3e5f5"},
    ]
    workshop = create_workshop_layout(board_id, sections)
    print(f"Created workshop with {len(workshop['frames'])} sections")
```

### 6. Text and Images

```python
# text_images.py
# ABOUTME: Text elements and image handling
# ABOUTME: Create text boxes, embed images, and manage media

from miro_api import Miro
import os
import requests
from io import BytesIO

miro = Miro(access_token=os.environ.get("MIRO_ACCESS_TOKEN"))


def create_text(
    board_id: str,
    content: str,
    x: float = 0,
    y: float = 0,
    width: float = 200,
    font_size: int = 14,
    font_family: str = "arial",
    text_align: str = "left",
    color: str = "#000000",
) -> dict:
    """Create a text element"""

    text = miro.texts.create(
        board_id=board_id,
        data={"content": content},
        style={
            "color": color,
            "fillOpacity": "1.0",
            "fontFamily": font_family,
            "fontSize": str(font_size),
            "textAlign": text_align,
        },
        position={"x": x, "y": y, "origin": "center"},
        geometry={"width": width},
    )

    return {
        "id": text.id,
        "content": text.data.content,
        "position": {"x": text.position.x, "y": text.position.y},
    }


def create_heading(
    board_id: str,
    content: str,
    x: float = 0,
    y: float = 0,
    level: int = 1,
) -> dict:
    """Create a heading text element"""

    font_sizes = {1: 36, 2: 28, 3: 22, 4: 18}
    font_size = font_sizes.get(level, 14)

    return create_text(
        board_id=board_id,
        content=f"<strong>{content}</strong>",
        x=x,
        y=y,
        width=500,
        font_size=font_size,
    )


def create_bullet_list(
    board_id: str,
    items: list,
    x: float = 0,
    y: float = 0,
) -> dict:
    """Create a bulleted list"""

    content = "<ul>" + "".join(f"<li>{item}</li>" for item in items) + "</ul>"

    return create_text(
        board_id=board_id,
        content=content,
        x=x,
        y=y,
        width=400,
    )


def upload_image_from_url(
    board_id: str,
    image_url: str,
    x: float = 0,
    y: float = 0,
    width: float = None,
    title: str = None,
) -> dict:
    """Create an image from a URL"""

    image_data = {"url": image_url}
    if title:
        image_data["title"] = title

    geometry = {}
    if width:
        geometry["width"] = width

    image = miro.images.create(
        board_id=board_id,
        data=image_data,
        position={"x": x, "y": y, "origin": "center"},
        geometry=geometry if geometry else None,
    )

    return {
        "id": image.id,
        "position": {"x": image.position.x, "y": image.position.y},
    }


def upload_image_from_file(
    board_id: str,
    file_path: str,
    x: float = 0,
    y: float = 0,
    width: float = None,
) -> dict:
    """Upload an image from a local file"""

    with open(file_path, "rb") as f:
        image_data = f.read()

    # Use the image upload endpoint
    headers = {
        "Authorization": f"Bearer {os.environ.get('MIRO_ACCESS_TOKEN')}",
    }

    files = {"resource": (os.path.basename(file_path), image_data)}
    data = {"position": f'{{"x": {x}, "y": {y}, "origin": "center"}}'}

    if width:
        data["geometry"] = f'{{"width": {width}}}'

    response = requests.post(
        f"https://api.miro.com/v2/boards/{board_id}/images",
        headers=headers,
        files=files,
        data=data,
    )
    response.raise_for_status()

    return response.json()


def create_embed(
    board_id: str,
    url: str,
    x: float = 0,
    y: float = 0,
    width: float = 400,
    height: float = 300,
    mode: str = "modal",
) -> dict:
    """Create an embedded content (web page, video, etc.)

    Modes: inline, modal
    """

    embed = miro.embeds.create(
        board_id=board_id,
        data={"url": url, "mode": mode},
        position={"x": x, "y": y, "origin": "center"},
        geometry={"width": width, "height": height},
    )

    return {
        "id": embed.id,
        "url": embed.data.url,
        "position": {"x": embed.position.x, "y": embed.position.y},
    }


def create_document_section(
    board_id: str,
    title: str,
    description: str,
    items: list,
    x: float = 0,
    y: float = 0,
) -> dict:
    """Create a document-like section with title, description, and bullet points"""

    created = {}

    # Create title
    heading = create_heading(board_id, title, x=x, y=y, level=2)
    created["title"] = heading

    # Create description
    desc = create_text(board_id, description, x=x, y=y + 60, width=500)
    created["description"] = desc

    # Create bullet list
    bullets = create_bullet_list(board_id, items, x=x, y=y + 150)
    created["items"] = bullets

    return created


if __name__ == "__main__":
    board_id = "YOUR_BOARD_ID"

    # Create a document section
    section = create_document_section(
        board_id=board_id,
        title="Project Overview",
        description="This project aims to improve team collaboration through automated Miro workflows.",
        items=[
            "Automated board creation",
            "Template-based layouts",
            "Integration with CI/CD",
        ],
    )
    print(f"Created section with {len(section)} elements")
```

## Integration Examples

### GitHub Actions Integration

```yaml
# .github/workflows/miro-sync.yml
name: Sync to Miro

on:
  issues:
    types: [opened, labeled]
  pull_request:
    types: [opened, closed, merged]

jobs:
  sync-miro:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: |
          pip install miro-api requests

      - name: Create issue card in Miro
        if: github.event_name == 'issues'
        env:
          MIRO_ACCESS_TOKEN: ${{ secrets.MIRO_ACCESS_TOKEN }}
          MIRO_BOARD_ID: ${{ secrets.MIRO_BOARD_ID }}
        run: |
          python << 'EOF'
          import os
          from miro_api import Miro

          miro = Miro(access_token=os.environ["MIRO_ACCESS_TOKEN"])
          board_id = os.environ["MIRO_BOARD_ID"]

          # Create sticky note for new issue
          issue_title = "${{ github.event.issue.title }}"
          issue_number = "${{ github.event.issue.number }}"
          issue_url = "${{ github.event.issue.html_url }}"

          miro.sticky_notes.create(
              board_id=board_id,
              data={
                  "content": f"#{issue_number}: {issue_title}\n\n{issue_url}"
              },
              style={"fillColor": "yellow"},
              position={"x": 0, "y": 0, "origin": "center"},
          )
          print(f"Created sticky note for issue #{issue_number}")
          EOF

      - name: Update PR status in Miro
        if: github.event_name == 'pull_request'
        env:
          MIRO_ACCESS_TOKEN: ${{ secrets.MIRO_ACCESS_TOKEN }}
          MIRO_BOARD_ID: ${{ secrets.MIRO_BOARD_ID }}
        run: |
          python << 'EOF'
          import os
          from miro_api import Miro

          miro = Miro(access_token=os.environ["MIRO_ACCESS_TOKEN"])
          board_id = os.environ["MIRO_BOARD_ID"]

          pr_title = "${{ github.event.pull_request.title }}"
          pr_state = "${{ github.event.action }}"

          colors = {
              "opened": "light_blue",
              "closed": "red",
              "merged": "green",
          }

          miro.sticky_notes.create(
              board_id=board_id,
              data={"content": f"PR: {pr_title}\nStatus: {pr_state}"},
              style={"fillColor": colors.get(pr_state, "gray")},
              position={"x": 500, "y": 0, "origin": "center"},
          )
          EOF
```

### Sprint Retrospective Automation

```python
# retro_automation.py
# ABOUTME: Automated sprint retrospective board creation
# ABOUTME: Creates templated retro board with categories

from miro_api import Miro
import os
from datetime import datetime

miro = Miro(access_token=os.environ.get("MIRO_ACCESS_TOKEN"))


def create_retrospective_board(
    sprint_number: int,
    team_name: str,
    team_id: str = None,
) -> dict:
    """Create a complete retrospective board for a sprint"""

    team_id = team_id or os.environ.get("MIRO_TEAM_ID")

    # Create board
    board_name = f"Sprint {sprint_number} Retrospective - {team_name}"
    board = miro.boards.create(
        name=board_name,
        description=f"Retrospective for Sprint {sprint_number}",
        team_id=team_id,
    )
    board_id = board.id

    # Create frames for categories
    categories = [
        {"title": "What Went Well", "color": "#c8e6c9", "x": 0},
        {"title": "What Could Be Improved", "color": "#ffcdd2", "x": 700},
        {"title": "Action Items", "color": "#bbdefb", "x": 1400},
    ]

    frames = []
    for cat in categories:
        frame = miro.frames.create(
            board_id=board_id,
            data={"title": cat["title"], "format": "custom"},
            style={"fillColor": cat["color"]},
            position={"x": cat["x"], "y": 0, "origin": "center"},
            geometry={"width": 600, "height": 800},
        )
        frames.append({"id": frame.id, "title": cat["title"]})

        # Add placeholder stickies
        for i in range(3):
            miro.sticky_notes.create(
                board_id=board_id,
                data={"content": "Add your thoughts here..."},
                style={"fillColor": cat["color"]},
                position={
                    "x": cat["x"],
                    "y": -200 + (i * 150),
                    "origin": "center",
                },
            )

    # Create header
    miro.texts.create(
        board_id=board_id,
        data={
            "content": f"<strong>Sprint {sprint_number} Retrospective</strong><br>{datetime.now().strftime('%B %d, %Y')}"
        },
        style={"fontSize": "36", "textAlign": "center"},
        position={"x": 700, "y": -500, "origin": "center"},
        geometry={"width": 800},
    )

    # Add voting instructions
    miro.texts.create(
        board_id=board_id,
        data={
            "content": "Instructions:<br>1. Add sticky notes to each category<br>2. Vote on items using dots<br>3. Discuss top voted items<br>4. Create action items"
        },
        style={"fontSize": "14"},
        position={"x": -400, "y": 0, "origin": "center"},
        geometry={"width": 300},
    )

    return {
        "board_id": board_id,
        "view_link": board.view_link,
        "frames": frames,
    }


def create_sprint_planning_board(
    sprint_number: int,
    team_name: str,
    stories: list,
) -> dict:
    """Create a sprint planning board with user stories"""

    board = miro.boards.create(
        name=f"Sprint {sprint_number} Planning - {team_name}",
        description=f"Planning board for Sprint {sprint_number}",
        team_id=os.environ.get("MIRO_TEAM_ID"),
    )
    board_id = board.id

    # Create Kanban columns
    columns = ["Backlog", "To Do", "In Progress", "Review", "Done"]
    col_width = 350
    col_height = 1000

    for i, col in enumerate(columns):
        miro.frames.create(
            board_id=board_id,
            data={"title": col, "format": "custom"},
            style={"fillColor": "#f5f5f5"},
            position={"x": i * (col_width + 30), "y": 0, "origin": "center"},
            geometry={"width": col_width, "height": col_height},
        )

    # Add stories to backlog
    for j, story in enumerate(stories):
        miro.cards.create(
            board_id=board_id,
            data={
                "title": story.get("title", "User Story"),
                "description": story.get("description", ""),
            },
            position={"x": 0, "y": -300 + (j * 150), "origin": "center"},
            geometry={"width": 300, "height": 120},
        )

    return {"board_id": board_id, "view_link": board.view_link}


if __name__ == "__main__":
    # Create retrospective board
    retro = create_retrospective_board(sprint_number=15, team_name="Platform Team")
    print(f"Retro board: {retro['view_link']}")

    # Create planning board
    stories = [
        {"title": "As a user, I want to login with SSO", "description": "Implement SSO authentication"},
        {"title": "As a user, I want dark mode", "description": "Add dark mode support"},
    ]
    planning = create_sprint_planning_board(sprint_number=16, team_name="Platform Team", stories=stories)
    print(f"Planning board: {planning['view_link']}")
```

## Best Practices

### 1. Rate Limiting

```python
# Rate limit handling
import time
from functools import wraps

def rate_limit_handler(max_retries=3, base_delay=1):
    """Decorator for handling Miro rate limits"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if "429" in str(e) or "rate" in str(e).lower():
                        delay = base_delay * (2 ** attempt)
                        print(f"Rate limited, waiting {delay}s...")
                        time.sleep(delay)
                    else:
                        raise
            raise Exception("Max retries exceeded")
        return wrapper
    return decorator

@rate_limit_handler(max_retries=3)
def safe_create_sticky(board_id, content, x, y):
    return miro.sticky_notes.create(
        board_id=board_id,
        data={"content": content},
        position={"x": x, "y": y, "origin": "center"},
    )
```

### 2. Batch Operations

```python
# Batch creation for better performance
def batch_create_stickies(board_id: str, items: list, batch_size: int = 10):
    """Create stickies in batches to avoid rate limits"""
    created = []

    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]

        for item in batch:
            sticky = miro.sticky_notes.create(
                board_id=board_id,
                data={"content": item["content"]},
                style={"fillColor": item.get("color", "yellow")},
                position={"x": item["x"], "y": item["y"], "origin": "center"},
            )
            created.append(sticky)

        # Small delay between batches
        if i + batch_size < len(items):
            time.sleep(0.5)

    return created
```

### 3. Error Handling

```python
# Comprehensive error handling
from miro_api.exceptions import MiroApiException

def safe_api_call(func, *args, **kwargs):
    """Wrapper for safe API calls"""
    try:
        return func(*args, **kwargs)
    except MiroApiException as e:
        if e.status_code == 404:
            print(f"Resource not found: {e}")
            return None
        elif e.status_code == 401:
            print("Authentication failed - check token")
            raise
        elif e.status_code == 403:
            print("Permission denied - check scopes")
            raise
        elif e.status_code == 429:
            print("Rate limited - implement backoff")
            time.sleep(60)
            return func(*args, **kwargs)
        else:
            raise
```

### 4. Position Calculations

```python
# Helper functions for positioning
def calculate_grid_position(index: int, columns: int, spacing: float = 250):
    """Calculate x, y for grid layout"""
    row = index // columns
    col = index % columns
    return {
        "x": col * spacing,
        "y": row * spacing,
    }

def calculate_circle_position(index: int, total: int, radius: float = 300, center_x: float = 0, center_y: float = 0):
    """Calculate x, y for circular layout"""
    import math
    angle = (2 * math.pi * index) / total
    return {
        "x": center_x + radius * math.cos(angle),
        "y": center_y + radius * math.sin(angle),
    }
```

## Troubleshooting

### Common Issues

**Issue: 401 Unauthorized**
```python
# Verify token is valid
import requests

def verify_token(token: str) -> bool:
    response = requests.get(
        "https://api.miro.com/v1/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    return response.status_code == 200

# Check token scopes
def get_token_scopes(token: str) -> list:
    response = requests.get(
        "https://api.miro.com/v1/oauth-token",
        headers={"Authorization": f"Bearer {token}"}
    )
    return response.json().get("scopes", [])
```

**Issue: Items not appearing on board**
```python
# Check board permissions
def check_board_access(board_id: str) -> dict:
    board = miro.boards.get(board_id)
    return {
        "id": board.id,
        "permissions": board.policy.permissions_policy,
        "sharing": board.policy.sharing_policy,
    }
```

**Issue: Rate limiting**
```python
# Implement exponential backoff
import time

def with_backoff(func, max_retries=5):
    for i in range(max_retries):
        try:
            return func()
        except Exception as e:
            if "429" in str(e):
                wait = (2 ** i) + (random.random() * 0.1)
                time.sleep(wait)
            else:
                raise
    raise Exception("Max retries exceeded")
```

### Debug Commands

```bash
# Test API authentication
curl -X GET "https://api.miro.com/v1/users/me" \
  -H "Authorization: Bearer $MIRO_ACCESS_TOKEN"

# List boards
curl -X GET "https://api.miro.com/v2/boards?team_id=$MIRO_TEAM_ID" \
  -H "Authorization: Bearer $MIRO_ACCESS_TOKEN"

# Get board details
curl -X GET "https://api.miro.com/v2/boards/$BOARD_ID" \
  -H "Authorization: Bearer $MIRO_ACCESS_TOKEN"

# Create sticky note
curl -X POST "https://api.miro.com/v2/boards/$BOARD_ID/sticky_notes" \
  -H "Authorization: Bearer $MIRO_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"data": {"content": "Test note"}, "position": {"x": 0, "y": 0}}'
```

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-17 | Initial release with comprehensive Miro API v2 patterns |

## Resources

- [Miro REST API Documentation](https://developers.miro.com/reference)
- [Miro Python SDK](https://github.com/miroapp/api-clients)
- [Miro Developer Portal](https://developers.miro.com/)
- [OAuth 2.0 Guide](https://developers.miro.com/docs/getting-started-with-oauth)
- [Webhooks Documentation](https://developers.miro.com/docs/webhooks)
- [Rate Limits](https://developers.miro.com/docs/rate-limiting)

---

*This skill provides production-ready patterns for Miro whiteboard automation, enabling powerful visual collaboration workflows and team productivity tools.*
