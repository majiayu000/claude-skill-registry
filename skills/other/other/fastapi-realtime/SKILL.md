---
name: FastAPI Real-Time Features
description: This skill should be used when the user asks to "add WebSocket", "implement real-time", "create file upload", "add S3 upload", "send email", "implement notifications", "broadcast events", or mentions WebSockets, file storage, email service, push notifications, or real-time communication. Provides WebSocket, file upload, and notification patterns.
version: 0.1.0
---

# FastAPI Real-Time & Integration Features

This skill provides patterns for WebSockets, file uploads to S3, and email/notification services.

## WebSocket Implementation

### Connection Manager

```python
# app/websocket/manager.py
from fastapi import WebSocket
from typing import Dict, List, Set
import json
import asyncio

class ConnectionManager:
    def __init__(self):
        # room_id -> set of websockets
        self.rooms: Dict[str, Set[WebSocket]] = {}
        # user_id -> websocket
        self.user_connections: Dict[str, WebSocket] = {}

    async def connect(
        self,
        websocket: WebSocket,
        user_id: str,
        room_id: str = None
    ):
        await websocket.accept()
        self.user_connections[user_id] = websocket

        if room_id:
            if room_id not in self.rooms:
                self.rooms[room_id] = set()
            self.rooms[room_id].add(websocket)

    def disconnect(self, user_id: str, room_id: str = None):
        websocket = self.user_connections.pop(user_id, None)
        if websocket and room_id and room_id in self.rooms:
            self.rooms[room_id].discard(websocket)
            if not self.rooms[room_id]:
                del self.rooms[room_id]

    async def send_personal(self, user_id: str, message: dict):
        websocket = self.user_connections.get(user_id)
        if websocket:
            await websocket.send_json(message)

    async def broadcast_to_room(self, room_id: str, message: dict):
        if room_id in self.rooms:
            for websocket in self.rooms[room_id]:
                try:
                    await websocket.send_json(message)
                except Exception:
                    pass  # Connection closed

    async def broadcast_all(self, message: dict):
        for websocket in self.user_connections.values():
            try:
                await websocket.send_json(message)
            except Exception:
                pass

manager = ConnectionManager()
```

### WebSocket Endpoint

```python
# app/routes/websocket.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query
from app.websocket.manager import manager
from app.core.security import decode_token

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str = Query(...)
):
    # Authenticate
    try:
        payload = decode_token(token)
        user_id = payload["sub"]
    except Exception:
        await websocket.close(code=4001, reason="Invalid token")
        return

    # Connect
    await manager.connect(websocket, user_id)

    try:
        while True:
            data = await websocket.receive_json()
            await handle_message(user_id, data)
    except WebSocketDisconnect:
        manager.disconnect(user_id)

async def handle_message(user_id: str, data: dict):
    message_type = data.get("type")

    if message_type == "join_room":
        room_id = data.get("room_id")
        websocket = manager.user_connections.get(user_id)
        if websocket and room_id:
            if room_id not in manager.rooms:
                manager.rooms[room_id] = set()
            manager.rooms[room_id].add(websocket)
            await manager.broadcast_to_room(room_id, {
                "type": "user_joined",
                "user_id": user_id
            })

    elif message_type == "message":
        room_id = data.get("room_id")
        content = data.get("content")
        await manager.broadcast_to_room(room_id, {
            "type": "message",
            "user_id": user_id,
            "content": content
        })

    elif message_type == "typing":
        room_id = data.get("room_id")
        await manager.broadcast_to_room(room_id, {
            "type": "typing",
            "user_id": user_id
        })
```

## File Upload to S3

### S3 Service

```python
# app/services/storage.py
import boto3
from botocore.config import Config
from typing import BinaryIO, Optional
import uuid
from app.config import get_settings

settings = get_settings()

class S3Storage:
    def __init__(self):
        self.client = boto3.client(
            's3',
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            region_name=settings.aws_region,
            config=Config(signature_version='s3v4')
        )
        self.bucket = settings.s3_bucket

    async def upload_file(
        self,
        file: BinaryIO,
        filename: str,
        content_type: str,
        folder: str = "uploads"
    ) -> str:
        """Upload file to S3 and return URL."""
        # Generate unique key
        ext = filename.split('.')[-1] if '.' in filename else ''
        key = f"{folder}/{uuid.uuid4()}.{ext}"

        # Upload
        self.client.upload_fileobj(
            file,
            self.bucket,
            key,
            ExtraArgs={
                'ContentType': content_type,
                'ACL': 'private'
            }
        )

        return key

    def get_presigned_url(
        self,
        key: str,
        expires_in: int = 3600
    ) -> str:
        """Generate presigned URL for download."""
        return self.client.generate_presigned_url(
            'get_object',
            Params={'Bucket': self.bucket, 'Key': key},
            ExpiresIn=expires_in
        )

    def get_presigned_upload_url(
        self,
        key: str,
        content_type: str,
        expires_in: int = 3600
    ) -> dict:
        """Generate presigned URL for direct upload."""
        return self.client.generate_presigned_post(
            self.bucket,
            key,
            Fields={'Content-Type': content_type},
            Conditions=[
                {'Content-Type': content_type},
                ['content-length-range', 1, 10485760]  # 10MB max
            ],
            ExpiresIn=expires_in
        )

    async def delete_file(self, key: str):
        """Delete file from S3."""
        self.client.delete_object(Bucket=self.bucket, Key=key)

storage = S3Storage()
```

### Upload Endpoint

```python
# app/routes/uploads.py
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from app.services.storage import storage
from app.core.security import get_current_user

router = APIRouter(prefix="/uploads", tags=["Uploads"])

ALLOWED_TYPES = ["image/jpeg", "image/png", "image/gif", "application/pdf"]
MAX_SIZE = 10 * 1024 * 1024  # 10MB

@router.post("/")
async def upload_file(
    file: UploadFile = File(...),
    user: User = Depends(get_current_user)
):
    # Validate content type
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(400, f"File type not allowed: {file.content_type}")

    # Validate size (read first chunk)
    contents = await file.read()
    if len(contents) > MAX_SIZE:
        raise HTTPException(400, f"File too large. Max size: {MAX_SIZE} bytes")

    # Reset file position
    await file.seek(0)

    # Upload to S3
    key = await storage.upload_file(
        file.file,
        file.filename,
        file.content_type,
        folder=f"users/{user.id}"
    )

    # Save metadata to database
    upload = await Upload(
        user_id=user.id,
        filename=file.filename,
        s3_key=key,
        content_type=file.content_type,
        size=len(contents)
    ).insert()

    return {
        "id": str(upload.id),
        "filename": file.filename,
        "url": storage.get_presigned_url(key)
    }

@router.get("/presigned-upload")
async def get_presigned_upload(
    filename: str,
    content_type: str,
    user: User = Depends(get_current_user)
):
    """Get presigned URL for direct S3 upload."""
    if content_type not in ALLOWED_TYPES:
        raise HTTPException(400, f"File type not allowed")

    ext = filename.split('.')[-1] if '.' in filename else ''
    key = f"users/{user.id}/{uuid.uuid4()}.{ext}"

    presigned = storage.get_presigned_upload_url(key, content_type)

    return {
        "upload_url": presigned["url"],
        "fields": presigned["fields"],
        "key": key
    }
```

## Email Service

### Email Service with Templates

```python
# app/services/email.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader
from typing import List, Optional
import asyncio
from functools import partial

class EmailService:
    def __init__(self, settings):
        self.host = settings.smtp_host
        self.port = settings.smtp_port
        self.username = settings.smtp_username
        self.password = settings.smtp_password
        self.from_email = settings.from_email
        self.from_name = settings.from_name

        # Setup Jinja2 for templates
        self.templates = Environment(
            loader=FileSystemLoader("app/templates/email")
        )

    async def send(
        self,
        to: str | List[str],
        subject: str,
        template: str,
        context: dict = None,
        attachments: List[dict] = None
    ):
        """Send email using template."""
        if isinstance(to, str):
            to = [to]

        # Render template
        html_template = self.templates.get_template(f"{template}.html")
        html_content = html_template.render(**(context or {}))

        # Create message
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"{self.from_name} <{self.from_email}>"
        msg["To"] = ", ".join(to)

        # Attach HTML
        msg.attach(MIMEText(html_content, "html"))

        # Send async
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None,
            partial(self._send_smtp, msg, to)
        )

    def _send_smtp(self, msg: MIMEMultipart, recipients: List[str]):
        with smtplib.SMTP(self.host, self.port) as server:
            server.starttls()
            server.login(self.username, self.password)
            server.sendmail(self.from_email, recipients, msg.as_string())

    async def send_welcome(self, user_email: str, user_name: str):
        await self.send(
            to=user_email,
            subject="Welcome to Our Platform!",
            template="welcome",
            context={"name": user_name}
        )

    async def send_password_reset(self, user_email: str, reset_link: str):
        await self.send(
            to=user_email,
            subject="Password Reset Request",
            template="password_reset",
            context={"reset_link": reset_link}
        )

email_service = EmailService(get_settings())
```

### Email Templates

```html
<!-- app/templates/email/welcome.html -->
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; }
        .container { max-width: 600px; margin: 0 auto; }
        .header { background: #4F46E5; color: white; padding: 20px; }
        .content { padding: 20px; }
        .button { background: #4F46E5; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Welcome, {{ name }}!</h1>
        </div>
        <div class="content">
            <p>Thank you for joining us.</p>
            <a href="{{ dashboard_url }}" class="button">Go to Dashboard</a>
        </div>
    </div>
</body>
</html>
```

## Push Notifications

### Notification Service

```python
# app/services/notifications.py
from typing import List, Optional
from app.models.notification import Notification
from app.websocket.manager import manager

class NotificationService:
    async def create(
        self,
        user_id: str,
        title: str,
        message: str,
        type: str = "info",
        data: dict = None
    ) -> Notification:
        """Create notification and push via WebSocket."""
        notification = await Notification(
            user_id=user_id,
            title=title,
            message=message,
            type=type,
            data=data or {}
        ).insert()

        # Push via WebSocket
        await manager.send_personal(user_id, {
            "type": "notification",
            "data": notification.model_dump()
        })

        return notification

    async def mark_read(self, notification_id: str, user_id: str):
        notification = await Notification.get(notification_id)
        if notification and notification.user_id == user_id:
            await notification.set({Notification.read: True})

    async def get_unread(self, user_id: str) -> List[Notification]:
        return await Notification.find(
            Notification.user_id == user_id,
            Notification.read == False
        ).to_list()

notification_service = NotificationService()
```

## Additional Resources

### Reference Files

For detailed patterns:
- **`references/websocket-auth.md`** - WebSocket authentication patterns
- **`references/s3-advanced.md`** - Multipart upload, CDN integration
- **`references/email-templates.md`** - Email template library

### Example Files

Working examples in `examples/`:
- **`examples/websocket_chat.py`** - Complete chat implementation
- **`examples/file_upload_service.py`** - Full upload service
- **`examples/notification_worker.py`** - Background notification processing
