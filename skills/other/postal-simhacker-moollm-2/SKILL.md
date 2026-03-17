---
name: postal
description: Complete messaging system — letters, texts, goals, rewards, attachments
allowed-tools:
  - read_file
  - write_file
tier: 1
protocol: POSTAL-SYSTEM
tags: [moollm, mail, message, goals, rewards, attachments, phone, communication]
related: [goal, character, object, room, storage, buff]
adversary: instant-coupling
---

# Postal System

> *"Any address can send and receive. Goals come from anyone, not just Mom."*
> — The Gezelligheid Grotto Design Principles

---

## What Is It?

The **Postal System** is the complete messaging infrastructure:

| Feature | Description |
|---------|-------------|
| **Messages** | Letters between any endpoints |
| **Texts** | SMS-style instant messages |
| **Attachments** | Items, gold, images, buffs, room access |
| **Goals** | Any character can assign/modify/complete goals |
| **Phone** | Always-available mobile access (it's 2026!) |
| **Routing** | Deterministic delivery without LLM |

---

## Core Concepts

### Endpoints

Anything addressable can send/receive:

```yaml
to: "player"                       # Reserved keyword
to: "characters/family/mom/"       # Character path
to: "characters/npcs/bartender/"   # Any NPC
to: "pub/"                         # Room
to: "storage/vault/"               # Directory
to: "start/mailbox.yml"            # Object
```

### Deterministic Addressing

**CRITICAL:** Addresses are paths, not names. The simulator routes without LLM.

```yaml
# BAD: Symbolic (requires LLM)
from: mom
to: the bartender

# GOOD: Deterministic paths
from: "characters/family/mom/"
to: "characters/npcs/bartender/"
```

### Reserved Keywords

| Keyword | Resolves To |
|---------|-------------|
| `player` | Current player character |
| `party` | All party members |
| `narrator` | System/narrative voice |

---

## It's 2026 — You Have a Phone!

You carry a phone at all times. Mail and texts are always available.

```yaml
player:
  devices:
    phone:
      always_carried: true
      capabilities: [mail, text, notifications, camera, maps]
```

### Notification Types

| Type | Example |
|------|---------|
| 📬 Mail | "New letter from Mom!" |
| 💬 Text | "Don: Meet me at the pub" |
| 🎯 Quest | "Quest updated: Find the Key" |
| ⚠️ Alert | "WARNING: Grue nearby!" |
| 🎁 Reward | "You received: Gold Coins (50)" |

---

## Letters (Full Messages)

### Structure

```yaml
letter:
  id: "letter-001"
  from: "characters/family/mom/"
  to: "player"
  subject: "Your First Quest"
  
  body: |
    Dearest child,
    
    I need you to find something for me.
    There's a brass key somewhere in the maze.
    
    With love,
    Mom
    
  attachments: []
  
  # Goal integration (optional — ANY character can do this!)
  creates_goal:
    id: find-key
    name: "Find the Key"
    complete_when: "player has brass-key"
    reward:
      letter: mom-reward-001
      item: family-locket
      
  # Metadata
  sent: null
  delivered: null
  read: false
  status: draft  # draft | outbox | sent | delivered | read
```

### Goal Integration

**Any character can create/modify/complete goals** — not just Mom:

```yaml
# Bartender assigns a quest
letter:
  from: "characters/npcs/bartender/"
  to: "player"
  subject: "A Favor to Ask"
  body: "Could you deliver this package to the mayor?"
  
  creates_goal:
    id: deliver-package
    name: "Deliver the Package"
    complete_when: "player has talked to mayor with package"
    reward:
      gold: 50
      
# Don Hopkins updates your quest
letter:
  from: "characters/real-people/don-hopkins/"
  to: "player"
  subject: "Found something!"
  
  modifies_goal:
    id: find-key
    extend_with: "also check the old chest"
```

---

## Texts (Instant Messages)

Short, instant messages. It's 2026!

```yaml
text:
  id: "text-001"
  from: "characters/npcs/bartender/"
  to: "player"
  body: "Hey, you left your hat here!"
  
  quick_replies:
    - "On my way!"
    - "Thanks, be there soon"
    - "Can you hold it?"
    
  delivery: instant  # Not queued like letters
  timestamp: null
  read: false
```

### Texts vs Letters

| Feature | Text | Letter |
|---------|------|--------|
| Length | Short (< 160) | Long |
| Attachments | Photos only | Anything |
| Delivery | Instant | Next tick |
| Creates goals | Rarely | Yes |
| Formality | Casual | Can be formal |

---

## Attachments

Messages can carry anything:

```yaml
attachments:
  # Objects
  - type: object
    ref: "brass-key"
    action: send       # Remove from sender, give to recipient
    
  - type: object
    ref: "map"
    action: reference  # Just mention, don't transfer
    
  # Currency
  - type: gold
    quantity: 100
    action: send
    
  # Images
  - type: image
    ref: "images/treasure-map.png"
    action: copy
    
  - type: image
    action: generate
    prompt: "A hand-drawn map to the treasure..."
    
  # Buffs
  - type: buff
    ref:
      name: "Blessed"
      effect: "+1 luck"
      duration: 10
    action: apply
    
  # Room access
  - type: room
    ref: "maze/secret-chamber/"
    action: unlock
```

### Attachment Actions

| Action | Effect |
|--------|--------|
| `send` | Remove from sender, give to recipient |
| `give` | Give to recipient (sender keeps if applicable) |
| `copy` | Duplicate for recipient |
| `reference` | Mention without transfer |
| `unlock` | Grant access (for rooms) |
| `apply` | Apply effect (for buffs) |
| `generate` | Create on delivery (for images) |

---

## Inbox & Outbox

### Inbox

```yaml
# player/INBOX.yml
inbox:
  owner: "player"
  
  messages:
    - ref: "messages/mom-quest.yml"
      received: "2026-01-10T10:00:00Z"
      read: false
      priority: high
      from: "characters/family/mom/"
      subject: "Your First Quest"
      preview: "Dearest child, I need you to..."
      
  unread_count: 1
  
  settings:
    max_messages: 100
    forward_to: null
```

### Outbox (Optional)

Stage messages before sending:

```yaml
# player/OUTBOX.yml
outbox:
  owner: "player"
  
  drafts:
    - ref: "messages/draft-001.yml"
      started: "2026-01-10T09:00:00Z"
      
  pending:
    - ref: "messages/ready-001.yml"
      to: "characters/family/mom/"
```

---

## Delivery Simulation

The postal system simulates realistic delivery:

### Delivery Time

Messages don't arrive instantly (unless texting!):

```yaml
letter:
  from: "characters/family/mom/"
  to: "player"
  
  # Delivery simulation
  delivery:
    method: letter           # letter, express, text
    
    # Time calculation
    base_time: 3             # Base turns
    distance_factor: 1       # Turns per "hop" of distance
    total_time: 5            # Calculated: base + (distance * factor)
    
    # Timestamps
    sent: "2026-01-10T10:00:00Z"
    estimated_arrival: "2026-01-10T10:05:00Z"  # 5 turns later
    delivered: null          # Set when actually delivered
    
    # Status
    status: in_transit       # draft | outbox | in_transit | delivered | read
    turns_remaining: 5
```

### Delivery Methods

| Method | Base Time | Cost | Features |
|--------|-----------|------|----------|
| `text` | 0 (instant) | Free | Photos only, casual |
| `letter` | 3 turns | 1 gold | Full attachments, goals |
| `express` | 1 turn | 5 gold | Priority delivery |
| `freight` | 10 turns | 0.5 gold/kg | Heavy items, bulk |
| `courier` | 2 turns | 10 gold | Guaranteed, tracked |

### Distance Calculation

Distance is measured in "hops" through the room graph:

```yaml
# Distance examples:
# Same room: 0 hops
# Adjacent room: 1 hop
# Through maze: 5+ hops
# Different "region": 10+ hops

delivery:
  from_location: "pub/"
  to_location: "characters/family/mom/"  # Mom's home
  hops: 4
  time_per_hop: 1
  total_delivery_time: 7  # base 3 + (4 * 1)
```

### Postage Costs

Sending mail costs resources:

```yaml
letter:
  from: "player"
  to: "characters/family/mom/"
  
  postage:
    method: letter
    base_cost: 1             # Gold
    weight_cost: 0           # Per kg for heavy items
    distance_cost: 0.5       # Per hop
    total_cost: 3            # Calculated
    
    # Payment
    paid: false
    paid_from: "player"      # Who pays
    
    # Insufficient funds?
    requires_payment: true
    can_send: true           # false if can't afford
```

### Free Messaging

Some messages are free:

```yaml
# Texts are free
text:
  postage:
    method: text
    total_cost: 0
    
# System messages are free
letter:
  from: "narrator"
  postage:
    total_cost: 0
    reason: "system message"
    
# Within same location is free
letter:
  from: "pub/bartender.yml"
  to: "pub/patron.yml"
  postage:
    total_cost: 0
    reason: "same location"
```

### In-Transit Tracking

Track messages in transit:

```yaml
# world.skills.postal state
postal:
  in_transit:
    - id: letter-001
      from: "player"
      to: "characters/family/mom/"
      turns_remaining: 3
      
    - id: letter-002
      from: "characters/npcs/bartender/"
      to: "player"
      turns_remaining: 1
      
  # Each tick, turns_remaining decrements
  # When 0, message is delivered
```

### Delivery Simulation in Tick

```python
# MAIL phase of simulation
def deliver_mail(world):
    postal = world.skills.postal
    
    # Decrement turns for in-transit messages
    still_in_transit = []
    for message in postal.get('in_transit', []):
        message['turns_remaining'] -= 1
        
        if message['turns_remaining'] <= 0:
            # Deliver now!
            actually_deliver(world, message)
            world.trigger_event('MAIL_ARRIVED', {
                'from': message['from'],
                'to': message['to']
            })
        else:
            still_in_transit.append(message)
    
    postal['in_transit'] = still_in_transit
```

### Express & Priority

Pay more for faster delivery:

```yaml
letter:
  delivery:
    method: express
    
  postage:
    base_cost: 5             # Express premium
    guaranteed_time: 1       # Arrives next turn
    tracking: true           # Can check status
    insurance: true          # Compensated if lost
```

### Lost Mail (Optional Mechanic)

For added realism/drama:

```yaml
postal:
  settings:
    loss_chance: 0.01        # 1% chance of loss
    loss_recoverable: true   # Can be found later
    
    # Lost mail goes to:
    lost_mail_location: "maze/lost-and-found/"
```

---

## Deterministic Routing

The simulator delivers mail without LLM. See [ROUTING.md](./ROUTING.md).

### Routing Instructions

```yaml
letter:
  from: "characters/family/mom/"
  to: "player"
  
  # Generated routing (deterministic)
  routing:
    destination_type: player
    destination_path: player
    delivery_point: inbox
    inbox_path: player/INBOX.yml
    
    attachments_transfer:
      - type: object
        ref: "brass-key"
        action: send
        from_inventory: "characters/family/mom/"
        to_inventory: "player"
        
    triggers:
      - event: MESSAGE_RECEIVED
        data: { from: "characters/family/mom/" }
      - event: GOAL_CREATED
        data: { goal_id: find-key }
```

### Simulation Phase

Mail delivery is a phase in the simulation tick:

```
1. RESET     — foo_effective = foo
2. BUFFS     — Apply modifiers
3. SIMULATE  — Objects run
4. MAIL      — Deliver queued messages (deterministic!)
5. EVENTS    — Process queue
6. NAVIGATE  — Move player
7. DISPLAY   — Update UI
```

---

## Storage Integration

Mail items to your vault:

```yaml
letter:
  from: "player"
  to: "storage/vault/"
  subject: "Depositing treasure"
  
  attachments:
    - type: gold
      quantity: 500
      action: send
```

---

## Logistics Integration — Postal IS the Transport Layer!

**KEY INSIGHT:** You don't need physical bots to move items between logistic containers.
The postal system IS the transport layer — instantaneous, free, efficient!

### The Unification

| Factorio | MOOLLM |
|----------|--------|
| Logistics bots | Postal system (free, instant) |
| Flying between chests | Email/text delivery |
| Request list | Triggers automated mail |
| Active provider pushing | Auto-send attachments |
| Circuit signals | Text notifications |

### How It Works

When a logistics requester needs items, instead of dispatching a bot:

```yaml
# Automatic postal delivery for logistics
logistics_delivery:
  trigger: "requester.request_unfulfilled"
  
  # Find a provider with matching items
  provider: "nw/iron-ore/"
  requester: "forge/"
  item: "iron-ore"
  count: 20
  
  # Generate a postal transfer (instant, free!)
  postal_transfer:
    type: internal-logistics    # Special type: no cost, instant
    from: "nw/iron-ore/"
    to: "forge/"
    attachments:
      - type: object
        ref: "iron-ore"
        quantity: 20
        action: send
        
    # No delivery time for internal logistics!
    delivery:
      method: logistics         # New method: instant, free
      total_time: 0
      cost: 0
```

### Logistics Delivery Methods

| Method | Time | Cost | Use Case |
|--------|------|------|----------|
| `logistics` | 0 | Free | Internal network transfers |
| `text` | 0 | Free | Signals, notifications |
| `letter` | 3+ turns | 1+ gold | Player-to-player with drama |
| `freight` | 10+ turns | Per weight | Physical bulk transport |

### Camera Phone = Image Generation!

Your phone's camera can generate images via prompts:

```yaml
text:
  from: "player"
  to: "narrator"
  body: "Take a photo of this treasure map"
  
  attachments:
    - type: image
      action: generate
      prompt: "A weathered treasure map showing the maze layout..."
      save_to: "player/photos/treasure-map.png"
```

### Text Messages = Circuit Signals!

Texts can carry logistics signals:

```yaml
# Room emits signal when low on fuel
room:
  signals:
    enabled: true
    emit:
      - signal: "low-fuel"
        when: "stacks.coal < 5"
        action:
          text:
            to: "player"
            body: "⚠️ Forge is running low on coal!"
```

### No Bots Needed (But You Can Have Them!)

**Default:** Logistics uses postal (instant, free)
**Optional:** Physical bots for gameplay/drama

```yaml
logistic-container:
  transport:
    method: postal           # Default: instant via mail
    # OR
    method: bot              # Physical transport (slower, visible)
    bot_path: "characters/courier-kitten/"
```

When using bots:
- Player sees the kitten carrying items
- Can intercept, pet, or redirect
- Adds gameplay and drama
- But slower than postal!

### The Complete Flow

```
1. REQUESTER: "I need 20 iron ore"
   │
   ▼
2. LOGISTICS ENGINE finds provider with iron ore
   │
   ▼
3. Generate POSTAL TRANSFER (internal, instant, free)
   │
   ├─── method: postal ────→ Instant delivery
   │                         No physical movement
   │                         Items "teleport"
   │
   └─── method: bot ───────→ Dispatch courier kitten
                             Physical movement
                             Player can see/interact
   │
   ▼
4. REQUESTER receives items
   │
   ▼
5. on_request_fulfilled fires
```

### Why This Is Better

| Physical Bots | Postal Transport |
|---------------|------------------|
| Slow (travel time) | Instant |
| Visible (might break immersion) | Invisible (just works) |
| Can get stuck | Never fails |
| Limited cargo | Unlimited |
| Fun to watch | Efficient |

**Use bots for drama. Use postal for efficiency.**

---

## Commands

| Command | Effect |
|---------|--------|
| `CHECK PHONE` | See notifications and quick access |
| `READ MAIL` | Open inbox |
| `READ [letter]` | Display letter |
| `COMPOSE` | Start writing |
| `REPLY` | Reply to current |
| `ATTACH [item]` | Add attachment |
| `SEND` | Send current message |
| `TEXT [character]` | Quick text |

---

## Mom as a Character

Mom isn't special infrastructure — she's just a character:

```yaml
# characters/family/mom/CHARACTER.yml
character:
  id: mom
  name: "Mom"
  type: correspondent
  
  personality:
    warmth: 10
    worry: 7
    pride: 9
    
  voice:
    patterns:
      - "Dearest child"
      - "I'm so proud"
      - "Be careful out there"
      
  triggers:
    on_goal_complete: "Send congratulations letter"
    on_danger: "Send worried letter"
    on_long_silence: "Send 'are you okay?' letter"
```

Any character can have similar triggers. The bartender can send quests. Don Hopkins can send updates. Goals come from anyone!

---

## Browser UI

See [BROWSER-UI.md](./BROWSER-UI.md) for the delightful mail interface.

---

## Protocol Symbol

```
POSTAL-SYSTEM — Complete messaging with deterministic routing
```
