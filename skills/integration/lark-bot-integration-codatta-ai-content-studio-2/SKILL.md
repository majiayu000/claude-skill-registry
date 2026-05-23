---
name: lark-bot-integration
description: Deploy and manage Lark (Feishu) bot for Milady meme generation, command handling, and team collaboration. Use when setting up Lark webhooks, handling bot commands, deploying to production, or integrating with Lark messaging.
allowed-tools: Read, Write, Bash
model: claude-sonnet-4-20250514
---

# Lark Bot Integration

Complete Lark (Feishu/飞书) bot system for interactive Milady meme generation and team collaboration.

## Overview

Deploy a fully-featured Lark bot that:
- **Handles 10+ commands** for meme generation
- **Processes @mentions** and direct messages
- **Uploads images** directly to Lark chats
- **Manages webhooks** with automatic token refresh
- **Integrates all Skills** - Milady generator, AI effects, Twitter content

## Quick Start

### 1. Configure Lark App

```bash
# Set environment variables
export LARK_APP_ID="cli_xxxxxxxxxxxxx"
export LARK_APP_SECRET="your_app_secret"

# Verify configuration
python scripts/setup_webhook.py --verify
```

### 2. Start Webhook Server

```bash
# Start on port 8000
python webhook_server.py

# Or use startup script
./start_lark_bot.sh
```

### 3. Set Webhook URL

```bash
# Get your public URL (use ngrok or public server)
python scripts/setup_webhook.py --url https://your-domain.com/webhook
```

### 4. Get Chat ID

```bash
# Get group chat ID for posting
python scripts/get_chat_id.py
```

## Supported Commands

### Meme Generation Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/milady` | Generate Milady meme | `/milady 5050` |
| `/milady [layers]` | Add accessories | `/milady 5050 Hat:Beret.png` |
| `/milady [text]` | Add text overlay | `/milady 5050 top:GM bottom:WAGMI` |
| `/memegen` | Classic meme templates (207+) | `/memegen drake old way new way` |

### AI Effects Commands

| Command | Description | Cost | Example |
|---------|-------------|------|---------|
| `/milady_illusion` | Illusion Diffusion effect | $0.006 | `/milady_illusion 5050` |
| `/milady_replace` | FLUX Fill Pro replace | $0.05 | `/milady_replace 5050 hat red cap` |
| `/milady_replace_sam` | SAM + FLUX replace | $0.05 | `/milady_replace_sam 5050 glasses cool shades` |

### Twitter Content Commands

| Command | Description | Cost | Example |
|---------|-------------|------|---------|
| `/tweet gm` | Generate GM tweet | ~$0.02 | `/tweet gm` |
| `/tweet insight` | Generate insight tweet | ~$0.03 | `/tweet insight data ownership` |
| `/tweet casual` | Generate casual tweet | ~$0.02 | `/tweet casual weekend vibes` |
| `/tweet reply` | Generate reply tweet | ~$0.02 | `/tweet reply Great point!` |

### Social Monitoring Commands

| Command | Description | Cost | Example |
|---------|-------------|------|---------|
| `/monitor mentions` | Check @mentions | FREE | `/monitor mentions` |
| `/monitor account` | Monitor user tweets | FREE | `/monitor account vitalikbuterin` |
| `/monitor opportunities` | Find interaction opportunities | FREE | `/monitor opportunities` |
| `/monitor stats` | View monitoring stats | FREE | `/monitor stats` |

### Training Data Commands

| Command | Description | Cost | Example |
|---------|-------------|------|---------|
| `/training check` | Check content freshness | FREE | `/training check gm builders` |
| `/training stats` | View training stats | FREE | `/training stats` |
| `/training add` | Add training sample | FREE | `/training add gm hello world` |
| `/training freshness` | Detailed freshness analysis | FREE | `/training freshness test content` |

### Utility Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/help` | Show all commands | `/help` |
| `/balance` | Check Replicate credit | `/balance` |

## Command Examples

### Basic Meme

```
/milady 5050
```
**Result**: NFT #5050 as image

### With Accessories

```
/milady 5050 Hat:Beret.png Glasses:Sunglasses.png
```
**Result**: NFT #5050 + beret + sunglasses

### With Text

```
/milady 5050 top:"Good Morning" bottom:"Let's Go"
```
**Result**: NFT #5050 with text overlay

### Natural Language

```
/milady 5050 give her a cowboy hat and heart sunglasses
```
**Result**: Bot parses "cowboy hat" → Hat:Cowboy.png, "heart sunglasses" → Glasses:Heart Shaped.png

### AI Effects

```
/milady_illusion 5050 spiral pattern
```
**Result**: NFT #5050 with illusion diffusion effect ($0.006)

```
/milady_replace_sam 5050 hat blue baseball cap
```
**Result**: SAM detects hat, FLUX replaces with blue baseball cap ($0.05)

### Template Meme

```
/milady_template drake
```
**Result**: Random Milady in Drake meme template

## Architecture

### Webhook Flow

```
User sends message in Lark
        ↓
Lark sends POST to /webhook
        ↓
webhook_server.py receives event
        ↓
LarkMemeBot processes command
        ↓
Calls MemeGenerator/AI Effects
        ↓
Uploads result to Lark
        ↓
User sees image in chat
```

### File Structure

```
lark-bot-integration/
├── SKILL.md                    # This file
├── SETUP_GUIDE.md              # Detailed setup
├── COMMAND_REFERENCE.md        # All commands
├── DEPLOYMENT.md               # Production deployment
├── src/
│   ├── lark_meme_bot.py        # Main bot logic
│   ├── webhook_handler.py      # Webhook processing
│   └── lark_api.py             # Lark API wrapper
├── config/
│   └── lark_config.yaml        # Bot configuration
└── scripts/
    ├── setup_webhook.py        # Webhook setup tool
    ├── get_chat_id.py          # Get chat IDs
    └── approve.py              # Approval workflow
```

## Setup Guide

### Prerequisites

1. **Lark Developer Account**
   - Go to https://open.larksuite.com/
   - Create new app
   - Enable bot capability

2. **Server with Public URL**
   - Can use ngrok for testing
   - Production: VPS or cloud server

3. **Required Permissions**
   - Send messages
   - Receive messages
   - Upload files
   - Read group info

### Detailed Setup Steps

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for step-by-step instructions including:
- Creating Lark app
- Configuring event subscriptions
- Setting up permissions
- Webhook URL verification
- Testing the bot

### Using Ngrok (Development)

```bash
# Start ngrok tunnel
./start_tunnel.sh

# Ngrok will output URL like: https://abc123.ngrok.io
# Use this as webhook URL: https://abc123.ngrok.io/webhook

# Set webhook
python scripts/setup_webhook.py --url https://abc123.ngrok.io/webhook
```

## Bot Implementation

### Main Bot Class

```python
from src.lark_meme_bot import LarkMemeBot

# Initialize bot
bot = LarkMemeBot(
    app_id=os.getenv("LARK_APP_ID"),
    app_secret=os.getenv("LARK_APP_SECRET")
)

# Process incoming message
bot.handle_message(
    message_id="om_xxxxx",
    chat_id="oc_xxxxx",
    text="/milady 5050",
    user_id="ou_xxxxx"
)
```

### Adding Custom Commands

```python
# In src/lark_meme_bot.py

def handle_custom_command(self, text, chat_id):
    """Add your custom command handler"""

    if text.startswith("/mycommand"):
        # Your logic here
        result = do_something()

        # Send response
        self.send_message(chat_id, "Done!")

        # Upload image if needed
        if image_path:
            self.upload_image(chat_id, image_path)
```

### Webhook Server

```python
from flask import Flask, request
from src.lark_meme_bot import LarkMemeBot

app = Flask(__name__)
bot = LarkMemeBot()

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    # Handle event
    if data.get('type') == 'message':
        bot.handle_message(
            message_id=data['message']['message_id'],
            chat_id=data['message']['chat_id'],
            text=data['message']['text']
        )

    return {'success': True}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
```

## Message Formats

### Text Messages

```python
bot.send_message(chat_id, "Hello from AI Content Studio! 🎀")
```

### Card Messages (Rich Format)

```python
bot.send_card(
    chat_id=chat_id,
    title="Meme Generated!",
    content="Your Milady meme is ready",
    image_key=image_key
)
```

### Image Upload

```python
# Upload and send image
image_key = bot.upload_image(
    chat_id=chat_id,
    image_path="/path/to/meme.png"
)
```

## Error Handling

### Common Issues

**1. Webhook verification failed**
```bash
# Check URL is publicly accessible
curl https://your-domain.com/webhook

# Verify in Lark console:
# Settings > Event Subscriptions > Verify URL
```

**2. Messages not received**
```bash
# Check event subscriptions are enabled
# Required events:
# - im.message.receive_v1
# - im.message.mention_v1
```

**3. Image upload fails**
```python
# Check image size (max 10MB for Lark)
# Check file format (PNG, JPG supported)
# Verify upload permission is granted
```

**4. Token expired**
```python
# Token auto-refreshes every 2 hours
# Manual refresh:
bot.refresh_token()
```

## Approval Workflow

For production use with Twitter posting:

```bash
# Start approval workflow
python scripts/approve.py

# Bot generates content → sends to Lark
# Team reviews in Lark chat
# Approved tweets get posted to Twitter
```

### Approval Flow

```
1. Bot generates tweet/meme
2. Posts to Lark approval channel
3. Team reacts with ✅ (approve) or ❌ (reject)
4. If approved → Posts to Twitter
5. If rejected → Logs feedback for learning
```

## Production Deployment

### Using systemd (Linux)

```bash
# Create service file
sudo nano /etc/systemd/system/lark-bot.service

# Add:
[Unit]
Description=Lark Meme Bot
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/ai-content-studio
Environment="LARK_APP_ID=cli_xxxxx"
Environment="LARK_APP_SECRET=xxxxx"
ExecStart=/usr/bin/python3 webhook_server.py
Restart=always

[Install]
WantedBy=multi-user.target

# Enable and start
sudo systemctl enable lark-bot
sudo systemctl start lark-bot
```

### Using Docker

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "webhook_server.py"]
```

```bash
# Build and run
docker build -t lark-bot .
docker run -d -p 8000:8000 \
  -e LARK_APP_ID=cli_xxxxx \
  -e LARK_APP_SECRET=xxxxx \
  lark-bot
```

### Using nohup (Simple)

```bash
# Start in background
nohup python3 webhook_server.py > webhook.log 2>&1 &

# Check status
ps aux | grep webhook_server

# View logs
tail -f webhook.log
```

## Monitoring

### Check Bot Status

```bash
# View logs
tail -f webhook.log

# Check if running
ps aux | grep webhook_server

# Test webhook
curl -X POST https://your-domain.com/webhook \
  -H "Content-Type: application/json" \
  -d '{"type":"test"}'
```

### Metrics to Track

- Messages received per hour
- Commands processed
- Images generated
- API errors
- Response time

## Security

### Best Practices

1. **Environment Variables**
   ```bash
   # Never commit credentials
   # Use .env file (add to .gitignore)
   LARK_APP_ID=cli_xxxxx
   LARK_APP_SECRET=xxxxx
   ```

2. **Webhook Verification**
   ```python
   # Verify requests come from Lark
   def verify_webhook(request):
       # Check signature
       # Validate timestamp
       # Reject invalid requests
   ```

3. **Rate Limiting**
   ```python
   # Prevent abuse
   from flask_limiter import Limiter

   limiter = Limiter(app, default_limits=["100 per hour"])
   ```

4. **Access Control**
   ```python
   # Restrict to specific chats/users
   ALLOWED_CHATS = ["oc_xxxxx", "oc_yyyyy"]

   if chat_id not in ALLOWED_CHATS:
       return "Unauthorized"
   ```

## Advanced Features

### Multi-Language Support

```python
# Detect language and respond accordingly
if user_language == "zh-CN":
    response = "梗图生成中..."
else:
    response = "Generating meme..."
```

### Command Shortcuts

```python
# Define aliases
COMMAND_ALIASES = {
    "/m": "/milady",
    "/mr": "/milady_random",
    "/mi": "/milady_illusion"
}
```

### Scheduled Posts

```python
# Use APScheduler for timed posts
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
scheduler.add_job(
    func=bot.post_daily_gm,
    trigger="cron",
    hour=9,
    minute=0
)
scheduler.start()
```

## Integration with Other Skills

### With Milady Generator

```python
from skills.milady_meme_generator.src.meme_generator_v2 import MemeGeneratorV2

generator = MemeGeneratorV2()
image = generator.generate_meme(nft_id=5050)
bot.upload_image(chat_id, image)
```

### With AI Effects

```python
from skills.ai_image_effects.src.flux_fill_pro import FluxFillPro

flux = FluxFillPro()
result = flux.replace_accessory(image, "hat", "cool beanie")
bot.upload_image(chat_id, result)
```

### With Twitter Content

```python
from skills.twitter_content_ai.src.content_generator import ContentGenerator

content = ContentGenerator()
tweet = content.generate_gm_post()
bot.send_message(chat_id, f"Suggested tweet:\n\n{tweet}")
```

## Troubleshooting

See [DEPLOYMENT.md](DEPLOYMENT.md) for comprehensive troubleshooting guide.

## Related Documentation

- [SETUP_GUIDE.md](SETUP_GUIDE.md) - Step-by-step setup
- [COMMAND_REFERENCE.md](COMMAND_REFERENCE.md) - All commands
- [DEPLOYMENT.md](DEPLOYMENT.md) - Production deployment
- [Lark Open Platform Docs](https://open.larksuite.com/document)

## Related Skills

- [milady-meme-generator](../milady-meme-generator/SKILL.md) - Core meme generation
- [ai-image-effects](../ai-image-effects/SKILL.md) - AI effects integration
- [twitter-content-ai](../twitter-content-ai/SKILL.md) - Content generation

---

**Cost**: Free (Lark API is free, only AI effects have costs)
