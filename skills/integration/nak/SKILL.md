---
name: nak
description: Interact with Nostr protocol using the nak CLI tool. Use to generate Nostr secret keys, encode and decode Nostr identifiers (hex/npub/nsec/nip05/etc), fetch events from relays, sign and publish Nostr events, and more.
license: CC-BY-SA-4.0
---

# nak - Nostr Army Knife

Work with the Nostr protocol using the `nak` CLI tool.

GitHub: https://github.com/fiatjaf/nak

## Installation

To install (or upgrade) nak:

```bash
curl -sSL https://raw.githubusercontent.com/fiatjaf/nak/master/install.sh | sh
```

## Core Concepts

Based on analyzing extensive real-world usage, here are the fundamental concepts distilled down, then branched out:

---

### CONCEPT 1: Query & Discovery
*"Finding events and data on Nostr"*

**Basic:**
- Fetch by identifier: "Get event/profile without knowing relays"
  - `nak fetch nevent1...` (uses embedded relay hints)
  - `nak fetch alex@gleasonator.dev` (NIP-05 resolution)
- Query by event ID: "I want THIS specific event from a relay"
  - `nak req -i <event_id> <relay>`
- Query by author: "Show me everything from this person"
  - `nak req -a <pubkey> <relay>`
- Query by kind: "Show me all profiles/notes/videos"
  - `nak req -k <kind> <relay>`

**Intermediate:**
- Fetch addressable events: "Get event by naddr/nprofile"
  - `nak fetch naddr1...` (kind, author, identifier encoded)
  - `nak fetch -r relay.primal.net naddr1...` (override relays)
- Filter by multiple criteria: "Find posts by author X of kind Y"
  - `nak req -k 1 -a <pubkey> <relay>`
- Tag-based queries: "Find events tagged with bitcoin"
  - `nak req --tag t=bitcoin <relay>`

**Advanced:**
- Search with ranking: "Find trending/top content"
  - `nak req --search "sort:hot" <relay>`
  - `nak req --search "popular:24h" <relay>`
- Live monitoring: "Watch events in real-time"
  - `nak req --stream <relay>`
- Cross-protocol queries: "Find bridged Bluesky content"
  - `nak req --tag "proxy=at://..." <relay>`

**Use cases:** Discovering content, debugging relay data, testing search algorithms, monitoring live feeds

---

### CONCEPT 2: Broadcast & Migration
*"Moving/copying events between relays"*

**Basic:**
- Publish a single event: "Put this on relay X"
  - `cat event.json | nak event <relay>`
- Query and republish: "Copy event from relay A to relay B"
  - `nak req -i <id> relay1 | nak event relay2`

**Intermediate:**
- Batch migration: "Copy all events of kind X"
  - `nak req -k 30717 source_relay | nak event dest_relay`
- Paginated backup: "Download everything from a relay"
  - `nak req --paginate source_relay | nak event backup_relay`
- Multi-relay broadcast: "Publish to multiple relays at once"
  - `cat event.json | nak event relay1 relay2 relay3`

**Advanced:**
- Selective migration: "Copy follow list members' data"
  - Loop through follow list, query each author, republish to new relay
- Filter and migrate: "Copy only tagged/searched content"
  - `nak req --tag client=X relay1 | nak event relay2`
- Cross-relay synchronization: "Keep two relays in sync"
  - `nak sync source_relay dest_relay`

**Use cases:** Seeding new relays, backing up data, migrating content between relays, bridging Mostr/Fediverse content

---

### CONCEPT 3: Identity & Encoding
*"Working with Nostr identifiers and keys"*

**Basic:**
- Decode identifiers: "What's inside this npub/nevent?"
  - `nak decode npub1...`
  - `nak decode user@domain.com`
- Encode identifiers: "Turn this pubkey into npub"
  - `nak encode npub <hex_pubkey>`

**Intermediate:**
- Generate keys: "Create a new identity"
  - `nak key generate`
  - `nak key generate | nak key public | nak encode npub`
- Extract hex from NIP-05: "Get the raw pubkey from an address"
  - `nak decode user@domain.com | jq -r .pubkey`
- Create shareable references: "Make a nevent with relay hints"
  - `nak encode nevent <event_id> --relay <relay>`

**Advanced:**
- Complex naddr creation: "Create addressable event reference with metadata"
  - `nak encode naddr -k 30717 -a <author> -d <identifier> -r <relay>`
- Multi-relay nprofile: "Create profile with multiple relay hints"
  - `nak encode nprofile <pubkey> -r relay1 -r relay2 -r relay3`

**Use cases:** Converting between formats, sharing references with relay hints, managing multiple identities, extracting pubkeys for scripting

---

### CONCEPT 4: Event Creation & Publishing
*"Creating and signing new events"*

**Basic:**
- Interactive creation: "Create an event with prompts"
  - `nak event --prompt-sec <relay>`
- Simple note: "Publish a text note"
  - `nak event -k 1 -c "Hello Nostr" <relay>`

**Intermediate:**
- Events with tags: "Create tagged content"
  - `nak event -k 1 -t t=bitcoin -t t=nostr <relay>`
- Event deletion: "Delete a previous event"
  - `nak event -k 5 -e <event_id> --prompt-sec <relay>`
- Replaceable events: "Create/update a profile or app data"
  - `nak event -k 10019 -t mint=<url> -t pubkey=<key> <relay>`

**Advanced:**
- Remote signing with bunker: "Sign without exposing keys"
  - `nak event --connect "bunker://..." <relay>`
- Batch event creation: "Generate many events via script"
  - `for i in {1..100}; do nak event localhost:8000; done`
- Complex events from JSON: "Craft specific event structure"
  - Modify JSON, then `cat event.json | nak event <relay>`

**Use cases:** Testing event creation, developing apps (kind 31990, 37515), wallet integration (kind 10019), moderation (kind 5), bunker/remote signing implementation

---

### CONCEPT 5: Development & Testing
*"Building on Nostr"*

**Basic:**
- Local relay testing: "Test against dev relay"
  - `nak req localhost:8000`
  - `nak event ws://127.0.0.1:7777`

**Intermediate:**
- Inspect JSON: "Examine event structure"
  - `nak req -i <id> <relay> | jq .`
- Test search: "Verify search functionality"
  - `nak req --search "<query>" localhost:8000`
- Admin operations: "Manage relay content"
  - `nak admin --prompt-sec banevent --id <id> <relay>`

**Advanced:**
- Protocol bridging: "Query/test ATProto integration"
  - `nak req --tag "proxy=at://..." eclipse.pub/relay`
- Git over Nostr: "Use git with Nostr transport"
  - `nak git clone nostr://...`
  - `nak req -k 30617 git.shakespeare.diy`
- Performance testing: "Measure query speed"
  - `time nak req -k 0 -a <pubkey> <relay>`
- Custom event kinds: "Test proprietary event types"
  - `nak req -k 37515 -a <author> -d <id> ditto.pub/relay`

**Use cases:** Relay development (Ditto), testing bridges (Mostr/Bluesky), developing video platforms, implementing Git-over-Nostr, testing search ranking algorithms, performance benchmarking

---

### CONCEPT 6: Analytics & Monitoring
*"Understanding Nostr data"*

**Basic:**
- Count results: "How many events match?"
  - `nak req -k 1 <relay> | wc -l`
  - `nak count -k 7 -e <event_id> <relay>`

**Intermediate:**
- Live monitoring: "Watch relay activity"
  - `nak req --stream <relay>`
  - `nak req -l 0 --stream relay1 relay2 relay3`
- Client analytics: "What apps are posting?"
  - `nak req --tag client=<app> <relay>`

**Advanced:**
- Event chain analysis: "Track engagement"
  - `nak count -k 7 -e <event_id> <relay>` (reactions)
  - `nak req -k 6 -k 7 -e <event_id> <relay>` (reposts + reactions)
- Content ranking: "Find top/hot content"
  - `nak req --search "sort:top" <relay>`
- Cross-relay comparison: "Compare event availability"
  - Query same event from multiple relays, compare results

**Use cases:** Monitoring relay health, tracking client usage (Ditto, noStrudel, moStard), analyzing engagement, testing ranking algorithms

---

## Summary: The 6 Core Mental Models

1. **Query & Discovery**: "How do I find things?"
2. **Broadcast & Migration**: "How do I move things?"
3. **Identity & Encoding**: "How do I represent things?"
4. **Event Creation**: "How do I make things?"
5. **Development & Testing**: "How do I build things?"
6. **Analytics & Monitoring**: "How do I measure things?"

---

## Command Shapes and Edge-Cases

Non-obvious patterns and edge cases for nak commands.

### Signing Methods

**Using environment variable:**
```bash
export NOSTR_SECRET_KEY=<hex_key>
nak event -c "hello"  # Automatically uses $NOSTR_SECRET_KEY
```

**Reading key from file:**
```bash
nak event -c "hello" --sec $(cat /path/to/key.txt)
```

### Content from File

**Using @ prefix to read content from file:**
```bash
echo "hello world" > content.txt
nak event -c @content.txt
```

### Tag Syntax

**Tag with multiple values (semicolon-separated):**
```bash
nak event -t custom="value1;value2;value3"
# Creates: ["custom", "value1", "value2", "value3"]
```

### Filter Output Modes

**Print bare filter (JSON only):**
```bash
nak req -k 1 -l 5 --bare
# Output: {"kinds":[1],"limit":5}
```

**Filter from stdin can be modified with flags:**
```bash
echo '{"kinds": [1]}' | nak req -l 5 -k 3 --bare
```

**Unlimited stream:**
```bash
nak req -l 0 --stream wss://relay.example.com
```

### Relay Specification

**Local relays and WebSocket schemes:**
```bash
nak req localhost:8000
nak req ws://127.0.0.1:7777
nak req relay.example.com  # Assumes wss:// if not specified
```

### Encoding

**Encode from JSON stdin (auto-detects type):**
```bash
echo '{"pubkey":"<hex>","relays":["wss://relay.example.com"]}' | nak encode
```

### Key Operations

**Complete key generation pipeline:**
```bash
nak key generate | tee secret.key | nak key public | nak encode npub
# Saves private key to file AND prints the public npub
```

### Verification

**Verify and pipe:**
```bash
nak event -c "test" --sec <key> | nak verify && echo "Valid"
```

### Fetch vs Req

**nak fetch uses relay hints from identifiers:**
```bash
nak fetch nevent1...  # Uses relays encoded in nevent
nak fetch naddr1...   # Uses relays encoded in naddr  
nak fetch alex@gleasonator.dev  # Resolves NIP-05
nak fetch -r relay.primal.net naddr1...  # Override relays
```

**nak req requires explicit relay specification:**
```bash
nak req -i <event_id> wss://relay.example.com
```

### Edge Cases

**No relays specified (prints event without publishing):**
```bash
nak event -c "test" --sec <key>  # Just prints the event JSON
```

**Tag order matters for addressable events:**
```bash
# The first 'd' tag is the identifier
nak event -k 30023 -d first -d second  # "first" is the identifier
```

**Timestamp override:**
```bash
nak event --ts 1700000000 -c "backdated" --sec <key>
nak event --ts 0 -c "genesis" --sec <key>  # Event at Unix epoch
```

**Kind 0 (profile) requires JSON content:**
```bash
nak event -k 0 -c '{"name":"Alice","about":"Developer"}' --sec <key>
```

**POW (Proof of Work):**
```bash
nak event --pow 20 -c "mined event" --sec <key>
# Will compute hash until difficulty target is met
```

**NIP-42 AUTH:**
```bash
nak req --auth -k 1 wss://relay.example.com
nak event --auth -c "test" --sec <key> wss://relay.example.com
# Automatically handles AUTH challenges
```

**Stdin takes precedence over flags:**
```bash
echo '{"content":"from stdin"}' | nak event -c "from flag" --sec <key>
# Uses "from stdin" (stdin overrides flags)
```

