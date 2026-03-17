---
name: twilio-video
cluster: twilio
description: "Video rooms: group/P2P, recording composition, track publication, network quality API, bandwidth"
tags: ["video","rooms","webrtc","twilio"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "twilio video room participant recording webrtc bandwidth quality"
---

# twilio-video

## Purpose

Enable OpenClaw to design, implement, operate, and troubleshoot Twilio Video in production:

- Create and manage Video Rooms (Group and Peer-to-Peer), including lifecycle controls.
- Issue Access Tokens with Video grants (identity, room scoping, TTL, key rotation).
- Publish/subscribe tracks (audio/video/data), manage track priorities, and implement moderation (mute/unpublish/remove participants).
- Enable and operate recording via Compositions (server-side recording outputs), including callbacks and storage pipelines.
- Use Network Quality API and bandwidth profiles to maintain call quality under real-world network constraints.
- Integrate Video with Twilio cluster patterns: webhooks, auth, rate limits, cost controls, and operational playbooks.

This guide assumes you are building a multi-tenant, production WebRTC system with compliance, observability, and incident response requirements.

---

## Prerequisites

### Twilio account + credentials

- Twilio Account SID (format `AC...`)
- Twilio API Key SID (format `SK...`) and Secret
- (Optional) Twilio Auth Token (format `...`) for legacy/basic auth; prefer API Key + Secret for server-to-server.
- A Twilio Video-enabled project (default for most accounts).

Create API Key:

```bash
twilio api:core:keys:create --friendly-name "video-prod-key-2026-02"
```

### Supported SDKs / libraries (pin versions)

Server-side (token minting, REST API calls):

- Node.js: `node >= 20.11.1` (LTS), npm `>= 10.2.4`
  - `twilio@4.23.0` (Twilio Node helper library)
  - `jsonwebtoken@9.0.2` (if you implement custom JWT handling; Twilio helper can mint tokens)
- Python: `python >= 3.11.7`
  - `twilio==9.4.1`
- Go: `go >= 1.22.1`
  - `github.com/twilio/twilio-go@v1.20.3`

Client-side:

- Twilio Video JS SDK: `twilio-video@2.31.1`
  - Browser support: latest Chrome/Edge, Firefox ESR, Safari 17+ (macOS/iOS constraints apply)
- iOS: TwilioVideo iOS SDK `5.10.0` (CocoaPods/SPM)
- Android: Twilio Video Android SDK `7.6.0` (Gradle)

Twilio CLI:

- `twilio-cli@5.5.1` (Node-based)
- Plugins:
  - `@twilio-labs/plugin-video@0.7.0` (Video commands; plugin availability varies—verify in your environment)

Install Twilio CLI:

```bash
npm i -g twilio-cli@5.5.1
twilio --version
```

Install plugin:

```bash
twilio plugins:install @twilio-labs/plugin-video@0.7.0
twilio plugins
```

### Auth setup (local dev + CI)

Prefer environment variables:

- `TWILIO_ACCOUNT_SID`
- `TWILIO_API_KEY`
- `TWILIO_API_SECRET`
- (Optional) `TWILIO_AUTH_TOKEN` (avoid in CI if possible)

Example (bash):

```bash
export TWILIO_ACCOUNT_SID="YOUR_ACCOUNT_SID"
export TWILIO_API_KEY="YOUR_API_KEY_SID"
export TWILIO_API_SECRET="your_api_secret_from_console"
```

Twilio CLI login (stores credentials locally; not recommended for CI runners):

```bash
twilio login
```

### Network + infra prerequisites

- Public HTTPS endpoint for webhooks (Composition callbacks, Status callbacks).
- TLS: modern ciphers; certificate from a trusted CA (Let’s Encrypt OK).
- Time sync: NTP enabled on servers minting JWTs (clock skew breaks tokens).
- TURN/STUN: Twilio provides; ensure outbound UDP/TCP 3478/5349 allowed; enterprise networks may require TCP/TLS fallback.

---

## Core Concepts

### Rooms: Group vs Peer-to-Peer (P2P)

- **Group Room**: media routed via Twilio’s SFU; supports larger rooms, recording/compositions, bandwidth profiles, network quality, dominant speaker, etc. Default for most production use.
- **Peer-to-Peer Room**: direct mesh between participants; limited scalability; fewer server-side features; generally not recommended for production beyond 1:1 with strict latency constraints.

Key properties:
- `type`: `group` | `group-small` | `peer-to-peer` (availability depends on account/region)
- `status`: `in-progress` | `completed`
- `maxParticipants`: enforce caps to control cost and quality

### Participants and Tracks

- **Participant**: identity in a room (unique per room).
- **Tracks**:
  - Audio track
  - Video track
  - Data track (reliable/unreliable messaging)
- Track lifecycle: `published` → `subscribed` (remote) → `unpublished` / `stopped`
- Server-side moderation often means:
  - Disconnect participant
  - Force unpublish (where supported)
  - Enforce client behavior via signaling + policy

### Access Tokens (JWT)

Twilio Video uses JWT access tokens with a **VideoGrant**:

- `identity`: stable user identifier (tenant-scoped)
- `ttl`: seconds; keep short (e.g., 3600) and refresh
- `room`: optional; restrict token to a specific room
- Signed with API Key Secret

Clock skew is a common failure mode; keep NTP.

### Recording via Compositions

Twilio Video “recording” in production typically means **Compositions**:

- A Composition is a server-side rendered output (e.g., MP4) created from recorded tracks.
- You can configure:
  - Layout (grid, active speaker, custom)
  - Format
  - Status callback URL
- You must handle asynchronous completion and storage (S3/GCS/Azure) yourself.

### Network Quality API

- Provides per-participant network quality levels (0–5) and stats.
- Use it to:
  - Adapt bitrate/resolution
  - Trigger UI warnings
  - Decide when to switch to audio-only
- Combine with bandwidth profiles for predictable behavior.

### Bandwidth Profiles and Track Priority

- Bandwidth profiles define how Twilio allocates bandwidth among tracks.
- Track priority (`low`/`standard`/`high`) influences which tracks degrade first.
- Use for:
  - Prioritizing presenter video
  - Keeping audio stable under congestion

### Webhooks and callbacks

Common callback types:
- Composition status callbacks
- Room status callbacks (where configured)
- Participant events (often handled client-side; server can poll REST API)

Webhooks must be:
- HTTPS
- Verified (Twilio signature validation)
- Idempotent (Twilio retries)

---

## Installation & Setup

### Official Python SDK — Video

**Repository:** https://github.com/twilio/twilio-python  
**PyPI:** `pip install twilio` · **Supported:** Python 3.7–3.13

```python
from twilio.rest import Client
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant

client = Client()

# Create a room
room = client.video.v1.rooms.create(
    unique_name="DailyStandup",
    type="go"  # or 'group' / 'peer-to-peer'
)
print(room.sid)

# Generate participant access token
token = AccessToken(
    os.environ["TWILIO_ACCOUNT_SID"],
    os.environ["TWILIO_API_KEY"],
    os.environ["TWILIO_API_SECRET"],
    identity="alice"
)
token.add_grant(VideoGrant(room="DailyStandup"))
print(token.to_jwt())
```

Source: [twilio/twilio-python — video](https://github.com/twilio/twilio-python/blob/main/twilio/rest/video/)

### Ubuntu 22.04 LTS (x86_64)

```bash
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg jq
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs
node -v
npm -v

sudo npm i -g twilio-cli@5.5.1
twilio --version
twilio plugins:install @twilio-labs/plugin-video@0.7.0
```

### Fedora 39/40 (x86_64)

```bash
sudo dnf install -y nodejs npm jq
node -v
npm -v

sudo npm i -g twilio-cli@5.5.1
twilio plugins:install @twilio-labs/plugin-video@0.7.0
```

### macOS (Intel + Apple Silicon)

Using Homebrew:

```bash
brew install node@20 jq
echo 'export PATH="/opt/homebrew/opt/node@20/bin:$PATH"' >> ~/.zshrc  # Apple Silicon
echo 'export PATH="/usr/local/opt/node@20/bin:$PATH"' >> ~/.zshrc     # Intel
source ~/.zshrc

npm i -g twilio-cli@5.5.1
twilio plugins:install @twilio-labs/plugin-video@0.7.0
```

### Windows 11 (PowerShell)

Install Node.js 20 LTS from official installer or winget:

```powershell
winget install OpenJS.NodeJS.LTS
node -v
npm -v
npm i -g twilio-cli@5.5.1
twilio --version
twilio plugins:install @twilio-labs/plugin-video@0.7.0
```

### Server library setup (Node.js)

```bash
mkdir -p video-service && cd video-service
npm init -y
npm i twilio@4.23.0 fastify@4.26.2 @fastify/env@4.3.0 pino@8.19.0
npm i -D typescript@5.3.3 tsx@4.7.0 @types/node@20.11.19
```

Minimal `tsconfig.json`:

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true
  }
}
```

### Server library setup (Python)

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip==24.0
pip install twilio==9.4.1 fastapi==0.109.2 uvicorn==0.27.1 python-dotenv==1.0.1
```

---

## Key Capabilities

### Room lifecycle management

Production patterns:

- Create rooms on-demand (or pre-provision for scheduled sessions).
- Enforce `uniqueName` naming conventions: include tenant + resource id.
- Set `maxParticipants` to control cost and prevent abuse.
- Complete rooms explicitly when sessions end to stop billing.

Example naming scheme:

- `acme-prod:class:9f3c2b1a`
- `tenantId:resourceType:resourceId`

Node: create room:

```ts
import twilio from "twilio";

const client = twilio(process.env.TWILIO_API_KEY!, process.env.TWILIO_API_SECRET!, {
  accountSid: process.env.TWILIO_ACCOUNT_SID!,
});

async function createRoom() {
  const room = await client.video.v1.rooms.create({
    uniqueName: "acme-prod:class:9f3c2b1a",
    type: "group",
    maxParticipants: 25,
    recordParticipantsOnConnect: false
  });
  return room;
}
```

Complete room:

```ts
await client.video.v1.rooms("RM0123456789abcdef0123456789abcdef")
  .update({ status: "completed" });
```

### Access token minting (VideoGrant)

Token service requirements:

- Authenticate caller (your auth, not Twilio’s).
- Authorize access to a room (tenant + role checks).
- Mint short-lived token (e.g., 15–60 minutes).
- Rotate API keys without downtime (support multiple signing keys).

Node token minting:

```ts
import twilio from "twilio";

const { AccessToken } = twilio.jwt;
const { VideoGrant } = AccessToken;

export function mintVideoToken(params: {
  identity: string;
  room?: string;
  ttlSeconds?: number;
}) {
  const token = new AccessToken(
    process.env.TWILIO_ACCOUNT_SID!,
    process.env.TWILIO_API_KEY!,
    process.env.TWILIO_API_SECRET!,
    {
      identity: params.identity,
      ttl: params.ttlSeconds ?? 3600
    }
  );

  token.addGrant(new VideoGrant({ room: params.room }));
  return token.toJwt();
}
```

Python token minting:

```python
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant

def mint_video_token(identity: str, room: str | None = None, ttl: int = 3600) -> str:
    token = AccessToken(
        account_sid=os.environ["TWILIO_ACCOUNT_SID"],
        signing_key_sid=os.environ["TWILIO_API_KEY"],
        secret=os.environ["TWILIO_API_SECRET"],
        identity=identity,
        ttl=ttl,
    )
    token.add_grant(VideoGrant(room=room))
    return token.to_jwt()
```

### Track publication, subscription, and moderation

Client-side (JS) connect with bandwidth profile and dominant speaker:

```js
import Video from "twilio-video";

const room = await Video.connect(token, {
  name: "acme-prod:class:9f3c2b1a",
  dominantSpeaker: true,
  networkQuality: { local: 1, remote: 1 },
  bandwidthProfile: {
    video: {
      mode: "collaboration",
      dominantSpeakerPriority: "high",
      maxSubscriptionBitrate: 2500000,
      renderDimensions: {
        high: { width: 1280, height: 720 },
        standard: { width: 640, height: 360 },
        low: { width: 320, height: 180 }
      }
    }
  }
});
```

Moderation patterns:

- “Mute” is typically enforced by client policy (disable local track) + server-side role enforcement.
- For hard enforcement, disconnect participant:

```ts
await client.video.v1.rooms("RM...").participants("PA...")
  .update({ status: "disconnected" });
```

### Recording and Compositions

Typical flow:

1. Enable participant recording (if required) or rely on composition sources.
2. Create Composition when room completes (or on-demand).
3. Receive status callback (`processing` → `completed`/`failed`).
4. Fetch composition media URL and ingest into storage.

Create composition (Node):

```ts
const composition = await client.video.v1.compositions.create({
  roomSid: "RM0123456789abcdef0123456789abcdef",
  audioSources: "*",
  videoLayout: {
    grid: { video_sources: ["*"] }
  },
  format: "mp4",
  statusCallback: "https://video.acme.com/twilio/composition-status",
  statusCallbackMethod: "POST"
});
```

Fetch composition media:

```ts
const c = await client.video.v1.compositions("CJ0123456789abcdef0123456789abcdef").fetch();
console.log(c.links?.media);
```

### Network Quality API usage

Client-side event handling:

```js
room.on("networkQualityLevelChanged", (level, stats) => {
  // level: 0..5
  // stats: { audio: { send, recv }, video: { send, recv } } depending on SDK
  if (level <= 2) {
    console.warn("Network degraded", level, stats);
  }
});
```

Server-side: fetch participant network quality (where supported by REST API fields; otherwise rely on client telemetry).

### Bandwidth and codec tuning

Production defaults:

- Prefer VP8 for broad compatibility; consider H.264 for Safari-heavy audiences.
- Use `maxSubscriptionBitrate` to cap downstream usage.
- Use track priority for presenter:

```js
const videoTrack = Array.from(room.localParticipant.videoTracks.values())[0]?.track;
videoTrack?.setPriority("high");
```

### Webhook handling (Composition callbacks)

Requirements:

- Validate Twilio signature (`X-Twilio-Signature`)
- Idempotency: dedupe by `CompositionSid` + `Status`
- Retry-safe: Twilio retries on non-2xx

Fastify example:

```ts
import Fastify from "fastify";
import twilio from "twilio";

const app = Fastify({ logger: true });

app.post("/twilio/composition-status", async (req, reply) => {
  const signature = req.headers["x-twilio-signature"] as string | undefined;
  const url = "https://video.acme.com/twilio/composition-status";

  const isValid = twilio.validateRequest(
    process.env.TWILIO_AUTH_TOKEN!, // signature validation uses Auth Token
    signature ?? "",
    url,
    req.body as Record<string, string>
  );

  if (!isValid) return reply.code(403).send({ error: "invalid signature" });

  // process CompositionSid, Status, RoomSid, etc.
  return reply.code(204).send();
});

app.listen({ port: 3000, host: "0.0.0.0" });
```

Note: Signature validation uses **Auth Token**, not API Secret. If you avoid Auth Token in services, isolate webhook verification into a small component with restricted secret access.

---

## Command Reference

> Notes:
> - Twilio CLI command availability depends on installed plugins and Twilio CLI version.
> - For Video, many operations are easiest via REST API using helper libraries; CLI is useful for inspection.

### Twilio CLI: global flags

Common across commands:

- `-o, --output [json|tsv|table]` output format
- `--properties <props>` comma-separated properties to display
- `--no-header` omit header (tsv/table)
- `--profile <name>` use a named profile from `~/.twilio-cli/config.json`
- `--log-level [debug|info|warn|error]`

Example:

```bash
twilio api:video:v1:rooms:list -o json --log-level debug
```

### Rooms (REST via CLI)

List rooms:

```bash
twilio api:video:v1:rooms:list \
  --status in-progress \
  --limit 50 \
  -o table \
  --properties sid,uniqueName,status,type,maxParticipants,dateCreated
```

Relevant flags:
- `--status <in-progress|completed>`
- `--unique-name <string>` (filter; if supported by CLI generator)
- `--limit <int>`

Fetch room:

```bash
twilio api:video:v1:rooms:fetch --sid RM0123456789abcdef0123456789abcdef -o json
```

Create room:

```bash
twilio api:video:v1:rooms:create \
  --unique-name "acme-prod:class:9f3c2b1a" \
  --type group \
  --max-participants 25 \
  --record-participants-on-connect false \
  -o json
```

Update room (complete):

```bash
twilio api:video:v1:rooms:update \
  --sid RM0123456789abcdef0123456789abcdef \
  --status completed \
  -o json
```

### Participants

List participants in a room:

```bash
twilio api:video:v1:rooms:participants:list \
  --room-sid RM0123456789abcdef0123456789abcdef \
  --status connected \
  --limit 200 \
  -o table \
  --properties sid,identity,status,dateCreated
```

Flags:
- `--room-sid <RM...>`
- `--status <connected|disconnected>`
- `--identity <string>` (if supported)
- `--limit <int>`

Disconnect participant:

```bash
twilio api:video:v1:rooms:participants:update \
  --room-sid RM0123456789abcdef0123456789abcdef \
  --sid PA0123456789abcdef0123456789abcdef \
  --status disconnected \
  -o json
```

### Compositions

Create composition:

```bash
twilio api:video:v1:compositions:create \
  --room-sid RM0123456789abcdef0123456789abcdef \
  --audio-sources "*" \
  --format mp4 \
  --status-callback "https://video.acme.com/twilio/composition-status" \
  --status-callback-method POST \
  -o json
```

Fetch composition:

```bash
twilio api:video:v1:compositions:fetch \
  --sid CJ0123456789abcdef0123456789abcdef \
  -o json
```

List compositions:

```bash
twilio api:video:v1:compositions:list \
  --room-sid RM0123456789abcdef0123456789abcdef \
  --limit 20 \
  -o table \
  --properties sid,status,format,dateCreated
```

### Recordings (if applicable to your account/features)

List recordings for a room:

```bash
twilio api:video:v1:recordings:list \
  --grouping-sid RM0123456789abcdef0123456789abcdef \
  --limit 50 \
  -o table \
  --properties sid,status,trackName,dateCreated
```

### API Keys (rotation support)

Create key:

```bash
twilio api:core:keys:create --friendly-name "video-key-rotation-2026-02" -o json
```

List keys:

```bash
twilio api:core:keys:list -o table --properties sid,friendlyName,dateCreated
```

Revoke key:

```bash
twilio api:core:keys:remove --sid YOUR_API_KEY_SID
```

---

## Configuration Reference

### 1) OpenClaw service env file

Path (Linux systemd pattern):

- `/etc/openclaw/video-service.env`

Example:

```bash
TWILIO_ACCOUNT_SID=YOUR_ACCOUNT_SID
TWILIO_API_KEY=YOUR_API_KEY_SID
TWILIO_API_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy

VIDEO_TOKEN_TTL_SECONDS=3600
VIDEO_ROOM_TYPE=group
VIDEO_MAX_PARTICIPANTS=25

PUBLIC_BASE_URL=https://video.acme.com
COMPOSITION_STATUS_CALLBACK_URL=https://video.acme.com/twilio/composition-status

LOG_LEVEL=info
```

### 2) systemd unit

Path:

- `/etc/systemd/system/openclaw-video.service`

```ini
[Unit]
Description=OpenClaw Twilio Video Service
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
EnvironmentFile=/etc/openclaw/video-service.env
WorkingDirectory=/opt/openclaw/video-service
ExecStart=/usr/bin/node /opt/openclaw/video-service/dist/server.js
Restart=on-failure
RestartSec=2
User=openclaw
Group=openclaw
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/var/lib/openclaw-video
AmbientCapabilities=
CapabilityBoundingSet=
LockPersonality=true
MemoryDenyWriteExecute=true

[Install]
WantedBy=multi-user.target
```

### 3) NGINX reverse proxy (TLS + webhook path)

Path:

- `/etc/nginx/sites-available/video.acme.com`
- symlink to `/etc/nginx/sites-enabled/video.acme.com`

```nginx
server {
  listen 443 ssl http2;
  server_name video.acme.com;

  ssl_certificate     /etc/letsencrypt/live/video.acme.com/fullchain.pem;
  ssl_certificate_key /etc/letsencrypt/live/video.acme.com/privkey.pem;

  client_max_body_size 2m;

  location /twilio/ {
    proxy_pass http://127.0.0.1:3000;
    proxy_set_header Host $host;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_read_timeout 30s;
  }

  location /healthz {
    proxy_pass http://127.0.0.1:3000/healthz;
  }
}
```

### 4) Twilio CLI config

Path:

- `~/.twilio-cli/config.json`

Example with profiles:

```json
{
  "activeProfile": "prod",
  "profiles": {
    "prod": {
      "accountSid": "YOUR_ACCOUNT_SID",
      "apiKeySid": "YOUR_API_KEY_SID",
      "apiKeySecret": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    },
    "staging": {
      "accountSid": "YOUR_ACCOUNT_SID",
      "apiKeySid": "YOUR_API_KEY_SID",
      "apiKeySecret": "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
    }
  }
}
```

---

## Integration Patterns

### Compose with Twilio Verify (step-up auth before joining a room)

Pattern:

1. User logs in with your primary auth.
2. For high-risk actions (joining a paid session, recording-enabled room), require Verify challenge.
3. Only mint Video token after Verify success.

Pseudo-flow:

- `POST /verify/start` → Twilio Verify V2
- `POST /verify/check`
- `POST /video/token` (requires verified session)

Operational notes:
- Rate limit token minting per user/IP.
- Store Verify decision with TTL (e.g., 10 minutes).

### Compose with Programmable Messaging (session notifications)

Use Messaging to send:
- “Room starting” reminders
- “Recording available” link after composition completes

Production requirements:
- Handle STOP/opt-out
- Status callbacks for delivery failures
- 10DLC registration (US A2P) if using long codes

Pipeline example:

1. Composition callback `completed`
2. Store media in S3
3. Send SMS with link
4. Track delivery via status webhook

### Compose with SendGrid (recording delivery + audit)

SendGrid transactional email:
- Dynamic template with recording link, session metadata, retention policy
- Handle bounces/spam; suppress invalid recipients

### Compose with Studio (orchestration)

Use Studio Flow to orchestrate:
- Pre-session reminders
- Post-session surveys
- Escalation to support if composition fails

Trigger Studio via REST Trigger API from your backend when room completes.

### CI/CD pipeline (key rotation + smoke tests)

- Rotate API keys monthly:
  - Create new key
  - Deploy with dual-key support (active + next)
  - Switch signing key
  - Revoke old key after TTL window

Smoke test script:
- Create room
- Mint token
- (Optional) headless connect test (Playwright) for JS SDK
- Complete room
- Create composition
- Verify callback received

---

## Error Handling & Troubleshooting

Include these in runbooks; ensure logs capture Twilio request IDs.

### 1) Auth failure (bad credentials)

Error (REST):

```
TwilioRestException: Authenticate
HTTP 401
{"code":20003,"message":"Authenticate","more_info":"https://www.twilio.com/docs/errors/20003","status":401}
```

Root causes:
- Wrong API Key/Secret
- Using API Key SID with Auth Token as password
- Account SID mismatch in client initialization

Fix:
- Verify `TWILIO_ACCOUNT_SID`, `TWILIO_API_KEY`, `TWILIO_API_SECRET`
- Ensure helper library is initialized with `accountSid` when using API keys
- Rotate compromised keys

### 2) Rate limiting

Error:

```
TwilioRestException: Too Many Requests
HTTP 429
{"code":20429,"message":"Too Many Requests","more_info":"https://www.twilio.com/docs/errors/20429","status":429}
```

Root causes:
- Bursty room/participant polling
- Excessive composition creation retries

Fix:
- Add exponential backoff + jitter
- Cache room state; avoid tight polling loops
- Batch operations; reduce list calls
- Implement circuit breaker for Twilio API

### 3) Invalid room name / duplicate uniqueName

Error (typical):

```
TwilioRestException: The requested resource /Rooms was not found
HTTP 404
```

Or validation errors depending on endpoint. Another common failure is attempting to create a room with an existing `uniqueName` while it’s in-progress.

Root causes:
- Reusing `uniqueName` for concurrent sessions
- Not completing rooms

Fix:
- Use unique per-session names (include timestamp/UUID)
- Complete rooms on session end
- If you need stable names, fetch existing room by uniqueName and reuse only if `completed`

### 4) Token rejected (clock skew / expired)

Client error (JS SDK):

```
TwilioError: Access Token expired or invalid
```

Root causes:
- Server clock skew
- TTL too short
- Token minted with wrong signing key secret

Fix:
- Ensure NTP on token service
- Increase TTL to 3600 and refresh proactively
- Validate key rotation logic

### 5) Webhook signature validation fails

Your service logs:

```
invalid signature
```

Root causes:
- Using wrong URL in validation (must match exact public URL)
- Missing/incorrect `TWILIO_AUTH_TOKEN`
- Proxy modifies URL/host; mismatch between internal and external URL

Fix:
- Use externally visible URL (including scheme/host/path) in validation
- Ensure NGINX sets `Host` and `X-Forwarded-Proto`
- Log computed URL and compare to Twilio request

### 6) Composition stuck in processing / never completes

Composition status remains `processing` for extended time.

Root causes:
- Very large room duration
- Layout configuration issues
- Source tracks missing or ended unexpectedly
- Twilio-side processing delays

Fix:
- Ensure room completed before composition creation (or accept longer processing)
- Use `audioSources: "*"` and `video_sources: ["*"]` for broad capture
- Add watchdog: if `processing` > threshold (e.g., 2 hours), alert and open Twilio support ticket with Composition SID

### 7) Participant cannot connect behind corporate firewall

Client logs show ICE failures; typical symptom: “Connecting…” then disconnect.

Root causes:
- UDP blocked; TURN over TCP/TLS required
- Deep packet inspection interfering with WebRTC

Fix:
- Ensure outbound TCP 443 allowed (Twilio TURN over TLS)
- Provide guidance to allowlist Twilio domains
- Consider fallback to audio-only or PSTN (Twilio Voice) for extreme networks

### 8) Media permissions denied (browser)

Browser error:

```
NotAllowedError: Permission denied
```

Root causes:
- User denied mic/camera
- Insecure context (not HTTPS)
- iOS Safari requires user gesture to start capture

Fix:
- Enforce HTTPS
- Prompt with clear UI and retry
- Request permissions after user interaction

### 9) “Participant identity already exists” (duplicate identity in same room)

Some SDKs surface:

```
TwilioError: Participant identity is already in use
```

Root causes:
- Reconnecting with same identity without disconnecting old session
- Multi-tab join without unique identity suffix

Fix:
- Enforce single session per identity (kick old participant)
- Use identity scheme: `userId:deviceId` and map to user in app layer

### 10) 21211 invalid To (cluster pattern relevance)

If you send SMS notifications and see:

```
{"code":21211,"message":"The 'To' number +1555... is not a valid phone number.","status":400}
```

Fix:
- Normalize E.164
- Validate phone numbers before sending
- Store verified numbers only

---

## Security Hardening

### Secrets management

- Store `TWILIO_API_SECRET` and `TWILIO_AUTH_TOKEN` in a secrets manager:
  - AWS Secrets Manager / GCP Secret Manager / Vault
- Do not bake secrets into container images.
- Rotate API keys regularly; revoke unused keys.

### Webhook verification

- Always validate `X-Twilio-Signature`.
- Enforce strict path matching; reject unexpected methods.
- Implement idempotency keys:
  - `CompositionSid + Status` unique constraint in DB

### Least privilege and isolation

- Separate services:
  - Token minting service (API Key Secret)
  - Webhook verification service (Auth Token)
- Use distinct Twilio API keys per environment and per service.

### TLS and headers

- Enforce TLS 1.2+ (prefer TLS 1.3).
- HSTS for your domain.
- For web apps: CSP, Permissions-Policy for camera/mic.

### OS hardening (CIS-aligned)

For Linux hosts (CIS Ubuntu 22.04 LTS guidance):

- Disable password SSH auth; use keys.
- Enable automatic security updates.
- Restrict outbound egress where possible (Twilio endpoints + your storage).
- systemd hardening (see unit file: `NoNewPrivileges`, `ProtectSystem=strict`, etc.).

### Abuse prevention

- Rate limit token endpoint by:
  - user id
  - IP
  - room id
- Require authenticated session; never mint tokens anonymously.
- Validate room membership server-side; do not trust client-provided room names.

---

## Performance Tuning

### Reduce API calls (measurable)

Before: polling room participants every 2 seconds per active room.
- 500 rooms → 250 req/s → triggers 20429.

After: event-driven + cached state:
- Poll only on state transitions (room created/completed) or on-demand admin actions.
- Expected reduction: >90% API traffic.

Implementation:
- Cache room metadata in Redis with TTL.
- Use client-side events for participant join/leave; send to backend via your own websocket if needed.

### Bandwidth profile tuning

Set `maxSubscriptionBitrate` to cap downstream:

- Default (uncapped): can exceed 4–6 Mbps in grid views.
- Tuned: `2.5 Mbps` cap for collaboration.
- Expected impact: fewer freezes on mid-tier connections; lower egress cost.

### Track priority for presenter

- Set presenter video to `high`, others `standard/low`.
- Expected impact: presenter remains stable under congestion; non-critical tiles degrade first.

### Composition cost control

- Only create compositions when needed:
  - user requested recording
  - compliance requirement
- Avoid composing every room by default.

### Client-side capture constraints

Use 720p for presenter, 360p for others:

```js
const localVideoTrack = await Video.createLocalVideoTrack({
  width: 1280,
  height: 720,
  frameRate: 24
});
```

Expected impact:
- Lower CPU on clients vs 1080p
- Better stability on integrated GPUs

---

## Advanced Topics

### Multi-region considerations

- Twilio Video media region selection may affect latency.
- Keep your token service region-agnostic but consider routing users to nearest region via room configuration (where supported).
- Measure RTT and join time by geography; store metrics per ISP.

### Key rotation without downtime

Pattern:

- Maintain `ACTIVE_SIGNING_KEY_SID` and `NEXT_SIGNING_KEY_SID`.
- Mint tokens with active key; accept tokens signed by either during rotation window.
- Rotate:
  1. Create new key
  2. Deploy config with both keys
  3. Switch active
  4. Wait > max TTL
  5. Revoke old key

### Idempotent composition creation

If your “room completed” handler can run twice:

- Use DB unique constraint on `roomSid` for composition job.
- If composition already exists, skip creation.

### Handling reconnect storms

When a network blip occurs, many clients reconnect simultaneously.

Mitigations:
- Token endpoint rate limiting with burst allowance
- Client backoff before reconnect
- Avoid creating new rooms on reconnect; reuse same room name

### Safari/iOS constraints

- Autoplay restrictions: require user gesture before starting audio.
- Camera switching behavior differs; test with iOS 17+.
- H.264 often more reliable on Safari; validate codec negotiation.

### Data tracks for control plane

Use data tracks for:
- “raise hand”
- “mute request”
- “layout hints”

But do not rely on them for authoritative moderation; enforce server-side policy.

---

## Usage Examples

### 1) Create a scheduled group room, mint tokens, and enforce max participants

Steps:
1. Backend creates room at schedule time.
2. Users request token; backend checks enrollment.
3. Client connects with bandwidth profile.

Backend (Node) create room:

```ts
const room = await client.video.v1.rooms.create({
  uniqueName: "acme-prod:webinar:2026-02-21T18-00Z",
  type: "group",
  maxParticipants: 100,
  recordParticipantsOnConnect: false
});
```

Token endpoint returns JWT scoped to room:

```ts
const jwt = mintVideoToken({
  identity: "tenant_acme:user_42",
  room: "acme-prod:webinar:2026-02-21T18-00Z",
  ttlSeconds: 1800
});
```

### 2) Moderator disconnects abusive participant

Admin UI calls backend:

```bash
curl -X POST https://video.acme.com/admin/rooms/RM.../participants/PA.../disconnect
```

Backend:

```ts
await client.video.v1.rooms(roomSid).participants(participantSid)
  .update({ status: "disconnected" });
```

Audit log:
- actor identity
- participant identity
- timestamp
- reason code

### 3) Post-session composition + SMS notification (Messaging cluster pattern)

Flow:
1. Room completed.
2. Create composition.
3. On callback `completed`, store media URL, send SMS.

Composition callback handler:
- Verify signature
- If `Status=completed`, enqueue job `send_recording_sms`

SMS send (ensure STOP handling + status callbacks in your messaging service).

### 4) Network quality-driven UI downgrade to audio-only

Client:
- Subscribe to `networkQualityLevelChanged`.
- If level <= 1 for > 10 seconds:
  - disable local video track
  - show banner
- When level >= 3 for > 20 seconds:
  - re-enable video

Pseudo:

```js
let lowSince = null;

room.on("networkQualityLevelChanged", (level) => {
  const now = Date.now();
  if (level <= 1) {
    lowSince ??= now;
    if (now - lowSince > 10000) {
      room.localParticipant.videoTracks.forEach(pub => pub.track.disable());
    }
  } else {
    lowSince = null;
  }
});
```

### 5) Key rotation drill (monthly)

1. Create new API key.
2. Deploy token service with both secrets.
3. Switch active signing key.
4. Validate new tokens connect.
5. After 2 hours (if TTL=3600), revoke old key.

Commands:

```bash
twilio api:core:keys:create --friendly-name "video-prod-2026-03" -o json
twilio api:core:keys:list -o table --properties sid,friendlyName,dateCreated
twilio api:core:keys:remove --sid SKoldkey...
```

### 6) Incident: 20429 rate limit during peak

Mitigation steps:
- Immediately increase backoff in API callers.
- Disable non-essential polling endpoints.
- Use cached room state for dashboards.
- Postmortem: identify hot loops (participants:list) and replace with event ingestion.

---

## Quick Reference

| Task | Command / API | Key flags / fields |
|---|---|---|
| List in-progress rooms | `twilio api:video:v1:rooms:list` | `--status in-progress --limit 50 -o table` |
| Create room | `twilio api:video:v1:rooms:create` | `--unique-name ... --type group --max-participants N` |
| Complete room | `twilio api:video:v1:rooms:update` | `--sid RM... --status completed` |
| List participants | `twilio api:video:v1:rooms:participants:list` | `--room-sid RM... --status connected` |
| Disconnect participant | `twilio api:video:v1:rooms:participants:update` | `--room-sid RM... --sid PA... --status disconnected` |
| Create composition | `twilio api:video:v1:compositions:create` | `--room-sid RM... --audio-sources "*" --format mp4 --status-callback URL` |
| Fetch composition | `twilio api:video:v1:compositions:fetch` | `--sid CJ...` |
| Rotate API key | `twilio api:core:keys:create/remove` | `--friendly-name ...` / `--sid SK...` |
| Mint token (Node) | `AccessToken + VideoGrant` | `identity`, `ttl`, `room` |

---

## Graph Relationships

### DEPENDS_ON

- `twilio-core-auth`: Account SID, API Key/Secret, Auth Token handling, key rotation
- `twilio-webhooks`: signature validation, retry/idempotency patterns
- `webrtc-client`: browser/device constraints, ICE/TURN behavior, media permissions
- `observability`: structured logs, request IDs, metrics, alerting

### COMPOSES

- `twilio-messaging`: SMS/WhatsApp notifications for session events, recording delivery, status callbacks, STOP handling
- `twilio-verify`: step-up authentication before token minting / recording access
- `sendgrid-email`: transactional email for recording links, audit trails, bounce handling
- `twilio-studio`: orchestration of reminders, surveys, escalation flows
- `twilio-voice`: PSTN fallback for audio when WebRTC fails; IVR for support

### SIMILAR_TO

- `zoom-video-sdk` (conceptually similar: rooms/sessions, tokens, recording)
- `agora-rtc` (tracks, channel join, bandwidth profiles)
- `daily-webrtc` (rooms, recording, webhooks)
