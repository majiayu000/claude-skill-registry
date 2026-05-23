---
name: arweave-ao-cookbook
description: Build decentralized applications on AO - a permanent, decentralized compute platform using actor model for parallel processes with native message-passing and permanent storage on Arweave
version: 1.0.0
category: blockchain-development
tags: [arweave, ao, decentralized-compute, smart-contracts, blockchain, lua, permanent-storage, distributed-systems]
source: https://cookbook_ao.arweave.net/
author: AO Community
last_updated: 2025-12-26
---

# AO Cookbook Skill

## Purpose

Master building decentralized applications on AO - a revolutionary decentralized compute system where countless parallel processes interact within a single, cohesive environment. AO combines permanent storage on Arweave with actor model architecture to create truly decentralized, permanently available compute.

## What is AO?

**AO** is a decentralized compute system built on the AO-Core protocol that employs the actor model (inspired by Erlang), enabling independent process operation through native message-passing mechanisms. Each process is an independent server in the network, communicating through messages stored permanently on Arweave.

**HyperBEAM** is the current production network, delivering:
- High-performance message processing
- Instant HTTP access to process state
- Trustless, permissionless infrastructure
- Permanent availability

**Key Differentiator**: Unlike traditional blockchains or cloud platforms, AO provides "your personal server in the AO computer" - a genuinely decentralized alternative to traditional hosting with permanent message storage.

## When to Use This Skill

✅ **Perfect for**:
- Building decentralized applications requiring permanent storage
- Creating smart contracts with complex state and interactions
- Developing chatbots, games, and interactive applications on blockchain
- Implementing token systems, voting mechanisms, and governance
- Building systems that require trustless, permanent compute
- Creating applications that benefit from parallel process execution
- Developing Arweave-integrated applications

❌ **Not ideal for**:
- Simple static websites (use traditional hosting)
- Applications requiring real-time sub-millisecond latency
- Systems that need to delete or modify historical data
- Traditional centralized database applications
- Projects without permanent storage requirements

## Core Concepts

### 1. Processes
Independent servers in the decentralized AO network. Each process:
- Has its own state and memory
- Executes autonomously
- Communicates via messages
- Persists permanently on Arweave
- Can spawn other processes

### 2. Messages
The core communication mechanism between processes:
- Permanently stored on Arweave
- Asynchronous by nature
- Contain data and metadata
- Trigger handler functions
- Enable process interaction

### 3. Handlers
Event processors that respond to incoming messages:
- Pattern-match on message properties
- Execute logic based on message content
- Update process state
- Send responses to other processes
- Enable reactive programming model

### 4. aos (AO Shell)
Interactive development environment:
- Command-line interface for AO processes
- Built-in Lua REPL
- Supports modules and blueprints
- Enables rapid prototyping
- Provides process management tools

### 5. Permanence
Everything is permanent on Arweave:
- Messages never disappear
- Code is immutable once deployed
- State history is preserved
- Audit trails are built-in
- No centralized control

## Installation & Setup

### Prerequisites
- **NodeJS**: Version 20 or higher
- **Code Editor**: Any editor (VS Code recommended)
- **Arweave Wallet** (optional): For custom wallet authentication

### Step 1: Install AOS
```bash
# Install AOS globally via npm
npm i -g https://get_ao.arweave.net

# Verify installation
aos --version
```

### Step 2: Connect to HyperBEAM Network
```bash
# Option 1: Connect to HyperBEAM for optimal performance
aos --node https://forward.computer

# Option 2: Use default settings
aos

# Option 3: Specify custom wallet
aos --wallet ~/.arweave-wallet.json

# Auto-generated wallet location
# Default: ~/.aos.json (created automatically if not specified)
```

### Step 3: Verify Connection
```lua
-- In aos shell, try basic commands:
print("Hello AO")
-- Output: Hello AO

-- Check your process ID
Name
-- Output: Your process name

Owner
-- Output: Your wallet address

-- View inbox
#Inbox
-- Output: Number of unhandled messages
```

## Basic Usage Patterns

### Pattern 1: Simple State Management

```lua
-- Initialize state variable
counter = 0

-- Create handler for increment messages
Handlers.add(
  "increment",
  Handlers.utils.hasMatchingTag("Action", "Increment"),
  function(msg)
    counter = counter + 1
    print("Counter incremented to: " .. counter)

    -- Send response
    Send({
      Target = msg.From,
      Data = tostring(counter)
    })
  end
)

-- Access state via HTTP
-- https://forward.computer/<process-id>~process@1.0/compute/counter
```

**Why this works**: State persists permanently and is accessible via HTTP through HyperBEAM.

### Pattern 2: Message Passing Between Processes

```lua
-- Send message to another process
Send({
  Target = "process-id-here",
  Action = "Chat-Message",
  Data = "Hello from my process!"
})

-- Handle incoming messages
Handlers.add(
  "chat",
  Handlers.utils.hasMatchingTag("Action", "Chat-Message"),
  function(msg)
    print("Received: " .. msg.Data)
    print("From: " .. msg.From)

    -- Reply to sender
    Send({
      Target = msg.From,
      Data = "Message received!"
    })
  end
)
```

**Pattern**: Asynchronous message-passing enables loosely-coupled process communication.

### Pattern 3: Inbox Monitoring

```lua
-- Custom prompt showing inbox count
function Prompt()
  return "📬 Inbox: " .. #Inbox .. " > "
end

-- Check inbox
if #Inbox > 0 then
  -- Access first message
  local msg = Inbox[1]
  print("From: " .. msg.From)
  print("Data: " .. msg.Data)
end
```

**Pattern**: Monitor incoming messages in real-time with custom prompts.

### Pattern 4: Using Modules

```lua
-- Load JSON module
local json = require("json")

-- Encode data
local data = { name = "Alice", balance = 1000 }
local encoded = json.encode(data)

-- Decode JSON
local decoded = json.decode(encoded)
print(decoded.name)  -- Output: Alice

-- Use .utils module for functional programming
local utils = require(".utils")
local numbers = {1, 2, 3, 4, 5}
local doubled = utils.map(function(n) return n * 2 end, numbers)
-- Result: {2, 4, 6, 8, 10}
```

**Available Modules**:
- `json`: JSON encoding/decoding
- `ao`: Core AO functions (Send, Spawn)
- `.base64`: Base64 encoding/decoding
- `.pretty`: Formatted output (tprint)
- `.utils`: Functional utilities (map, reduce, filter)

### Pattern 5: Multi-line Code with Editor Mode

```lua
-- Enter editor mode
.editor

-- Write multi-line function (type all lines, then Ctrl+D to execute)
function createToken(name, symbol, supply)
  return {
    Name = name,
    Symbol = symbol,
    TotalSupply = supply,
    Balances = {}
  }
end
-- Press Ctrl+D to exit editor mode

-- Use the function
myToken = createToken("MyToken", "MTK", 1000000)
print(myToken.Name)  -- Output: MyToken
```

### Pattern 6: Loading External Lua Files

```lua
-- Load functions from file
.load myFunctions.lua

-- Functions from file are now available
-- (assuming myFunctions.lua defines functions)
```

**Use case**: Organize complex logic in files, load into aos session.

## Common Workflows

### Workflow 1: Building a Token System

```lua
-- Initialize token state
Token = {
  Name = "MyToken",
  Symbol = "MTK",
  TotalSupply = 1000000,
  Balances = {}
}

-- Initialize owner balance
Token.Balances[Owner] = Token.TotalSupply

-- Transfer handler
Handlers.add(
  "transfer",
  Handlers.utils.hasMatchingTag("Action", "Transfer"),
  function(msg)
    local recipient = msg.Tags.Recipient
    local amount = tonumber(msg.Tags.Amount)

    -- Validate sender has balance
    if Token.Balances[msg.From] >= amount then
      Token.Balances[msg.From] = Token.Balances[msg.From] - amount
      Token.Balances[recipient] = (Token.Balances[recipient] or 0) + amount

      Send({
        Target = msg.From,
        Data = "Transfer successful"
      })
    else
      Send({
        Target = msg.From,
        Data = "Insufficient balance"
      })
    end
  end
)

-- Balance query handler
Handlers.add(
  "balance",
  Handlers.utils.hasMatchingTag("Action", "Balance"),
  function(msg)
    local target = msg.Tags.Target or msg.From
    local balance = Token.Balances[target] or 0

    Send({
      Target = msg.From,
      Data = tostring(balance)
    })
  end
)
```

### Workflow 2: Creating a Chatroom

```lua
-- Chatroom state
Chatroom = {
  Members = {},
  Messages = {}
}

-- Join handler
Handlers.add(
  "join",
  Handlers.utils.hasMatchingTag("Action", "Join"),
  function(msg)
    Chatroom.Members[msg.From] = true

    -- Notify all members
    for member, _ in pairs(Chatroom.Members) do
      Send({
        Target = member,
        Action = "Notification",
        Data = msg.Tags.Username .. " joined the chatroom"
      })
    end
  end
)

-- Send message handler
Handlers.add(
  "broadcast",
  Handlers.utils.hasMatchingTag("Action", "Broadcast"),
  function(msg)
    -- Store message
    table.insert(Chatroom.Messages, {
      From = msg.From,
      Text = msg.Data,
      Timestamp = msg.Timestamp
    })

    -- Broadcast to all members
    for member, _ in pairs(Chatroom.Members) do
      if member ~= msg.From then
        Send({
          Target = member,
          Action = "ChatMessage",
          From = msg.From,
          Data = msg.Data
        })
      end
    end
  end
)
```

### Workflow 3: Spawning New Processes

```lua
-- Spawn a new process
Send({
  Target = ao.id,  -- ao core process
  Action = "Eval",
  Data = [[
    -- Code for new process
    Handlers.add(
      "ping",
      Handlers.utils.hasMatchingTag("Action", "Ping"),
      function(msg)
        Send({ Target = msg.From, Data = "Pong!" })
      end
    )
  ]]
})

-- Programmatic spawn with Spawn()
local newProcess = Spawn("module-id", {
  Data = "Initial state",
  Tags = {
    Name = "SubProcess",
    Type = "Worker"
  }
})
```

### Workflow 4: Using Blueprints

Available blueprint templates:
- **chatroom**: Complete chatroom implementation
- **token**: Token standard with transfer/balance
- **voting**: Voting mechanism with proposals
- **staking**: Token staking with rewards
- **CRED**: Reputation/credit system

```lua
-- Load blueprint (example - actual syntax may vary)
-- Blueprints provide pre-built handlers and state management
```

## Advanced Patterns

### Pattern: State Persistence & HTTP Access

```lua
-- Define state that should be HTTP accessible
GameState = {
  players = {},
  score = 0,
  round = 1
}

-- State is automatically accessible via HTTP
-- GET https://forward.computer/<process-id>~process@1.0/compute/GameState
-- Returns JSON representation of GameState
```

**Power**: Any process variable becomes instantly queryable via HTTP through HyperBEAM.

### Pattern: Handler Composition

```lua
-- Helper function for common checks
local function isAuthorized(msg)
  return msg.From == Owner
end

-- Composed handler with authorization
Handlers.add(
  "admin-action",
  function(msg)
    return Handlers.utils.hasMatchingTag("Action", "Admin")(msg)
      and isAuthorized(msg)
  end,
  function(msg)
    -- Admin logic here
    print("Admin action executed")
  end
)
```

### Pattern: Error Handling

```lua
Handlers.add(
  "safe-operation",
  Handlers.utils.hasMatchingTag("Action", "SafeOp"),
  function(msg)
    local success, result = pcall(function()
      -- Potentially error-prone operation
      local value = tonumber(msg.Tags.Amount)
      assert(value > 0, "Amount must be positive")
      return value * 2
    end)

    if success then
      Send({
        Target = msg.From,
        Data = tostring(result)
      })
    else
      Send({
        Target = msg.From,
        Error = result  -- Contains error message
      })
    end
  end
)
```

## Troubleshooting

### Issue: "aos command not found"

**Solution**:
```bash
# Verify NodeJS version
node --version  # Should be v20+

# Reinstall aos
npm i -g https://get_ao.arweave.net

# Check PATH
echo $PATH | grep npm
```

### Issue: Connection timeout

**Solution**:
```bash
# Try different node
aos --node https://forward.computer

# Check network connection
curl https://forward.computer

# Verify wallet if using custom
aos --wallet ~/.arweave-wallet.json
```

### Issue: "Handler not triggering"

**Solutions**:
1. **Check tag matching**:
   ```lua
   -- Verify message has correct tags
   print(msg.Tags.Action)  -- Should match your matcher
   ```

2. **Test handler directly**:
   ```lua
   -- Simulate message
   local testMsg = {
     From = "test-id",
     Tags = { Action = "Test" },
     Data = "test data"
   }
   -- Call handler function manually
   ```

3. **Check handler order**:
   ```lua
   -- List all handlers
   Handlers.list()
   -- Handlers execute in order, first match wins
   ```

### Issue: State not persisting

**Explanation**: State in aos session is temporary until messages are sent/processed. To persist:
1. Send messages to your process (triggers permanent storage)
2. Deploy handlers as permanent code
3. Use `.load` to reload functions across sessions

### Issue: "Inbox full" or performance degradation

**Solution**:
```lua
-- Process and clear inbox
for i = 1, #Inbox do
  local msg = Inbox[i]
  -- Handle message
  print("Processing: " .. msg.From)
end

-- Inbox clears automatically after handlers process messages
```

## CLI Reference

### aos Command-Line Options

```bash
aos [options]

Options:
  --wallet <path>       Path to Arweave wallet (default: ~/.aos.json)
  --node <url>          AO node URL (default: https://forward.computer)
  --module <id>         Module ID for process
  --cron <interval>     Cron interval for process
  --version             Show version
  --help                Show help
```

### aos Shell Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `.editor` | Enter multi-line edit mode | `.editor` then Ctrl+D to execute |
| `.load <file>` | Load Lua file | `.load functions.lua` |
| `.exit` | Exit aos shell | `.exit` |
| `#Inbox` | Count unhandled messages | `print(#Inbox)` |
| `Inbox[n]` | Access message at index | `local msg = Inbox[1]` |

### Global Functions & Variables

| Global | Type | Purpose |
|--------|------|---------|
| `Send(msg)` | Function | Send message to process |
| `Spawn(module, msg)` | Function | Create new process |
| `Inbox` | Table | Unhandled messages |
| `Handlers` | Module | Handler management |
| `Owner` | String | Process owner address |
| `Name` | String | Process name |

## Best Practices

### 1. Handler Organization
```lua
-- Group related handlers
-- Authentication handlers
Handlers.add("auth:login", ...)
Handlers.add("auth:logout", ...)

-- Business logic handlers
Handlers.add("game:move", ...)
Handlers.add("game:score", ...)
```

### 2. State Management
```lua
-- Use clear state structures
State = {
  users = {},
  config = {
    maxUsers = 100,
    timeout = 300
  },
  stats = {
    totalMessages = 0,
    activeUsers = 0
  }
}

-- Avoid global pollution
-- Use tables to organize
```

### 3. Error Handling
```lua
-- Always validate inputs
function validateAmount(amount)
  local num = tonumber(amount)
  assert(num, "Amount must be a number")
  assert(num > 0, "Amount must be positive")
  return num
end

-- Use pcall for risky operations
local success, result = pcall(validateAmount, msg.Tags.Amount)
if not success then
  Send({ Target = msg.From, Error = result })
  return
end
```

### 4. Testing Handlers
```lua
-- Create test utilities
function testHandler(handler, mockMsg)
  return pcall(function()
    handler(mockMsg)
  end)
end

-- Test before deploying
local testMsg = {
  From = "test-sender",
  Tags = { Action = "Transfer", Amount = "100" },
  Data = ""
}
local success, err = testHandler(transferHandler, testMsg)
print(success and "✓ Test passed" or "✗ Test failed: " .. err)
```

### 5. Documentation
```lua
--[[
  Handler: token:transfer
  Purpose: Transfer tokens between addresses
  Tags Required:
    - Action: "Transfer"
    - Recipient: target address
    - Amount: token amount (string number)
  Returns: Success/failure message
]]
Handlers.add("token:transfer", ...)
```

## Resources

### Official Documentation
- **Cookbook**: https://cookbook_ao.arweave.net/
- **HyperBEAM**: https://forward.computer
- **GitHub**: https://github.com/permaweb/ao

### Community
- **Discord**: Community support and discussions
- **Tutorials**: Begin track, Bots & Games, Advanced guides

### Learning Paths
1. **Getting Started**: Welcome → Installation → Basic messaging
2. **Token Development**: Token tutorial → Transfer mechanics → Balance queries
3. **Game Development**: Bots & Games track → State management → Multiplayer
4. **Advanced**: Custom modules → Process spawning → HTTP integration

## Examples Repository

See `/examples` directory for complete working examples:
- `chatroom.lua` - Full chatroom implementation
- `token.lua` - Token standard with all handlers
- `game.lua` - Simple game with state management
- `voting.lua` - Voting system with proposals

## Version History

- **1.0.0** (2025-12-26): Initial skill creation
  - Core concepts and patterns
  - Installation and setup
  - Basic and advanced workflows
  - Troubleshooting guide
  - CLI reference
  - Best practices

---

**Last Updated**: December 26, 2025
**Source**: https://cookbook_ao.arweave.net/
**Community**: AO Discord and GitHub
**Status**: Production Ready ✅
