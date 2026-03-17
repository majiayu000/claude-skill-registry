---
name: discord-bot
description: |
  Build Discord bots with modern frameworks.
  Use when: creating Discord bot, slash commands, moderation bot.
  Triggers: "discord", "discord bot", "serenity", "discord.js", "discord.py".
---

# Discord Bot Development

## Project Protection Setup

**MANDATORY before writing any code:**

```bash
# 1. Create .gitignore
cat >> .gitignore << 'EOF'
# Build
target/
node_modules/
__pycache__/
dist/

# Secrets - CRITICAL for bots!
.env
.env.*
!.env.example
bot_token.txt
config.json  # If contains token

# IDE
.idea/
.vscode/
.DS_Store
EOF

# 2. Setup pre-commit hooks
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: detect-private-key
      - id: check-added-large-files
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.21.2
    hooks:
      - id: gitleaks
EOF

pre-commit install
```

**Why critical:** Discord bot tokens give FULL access. Leaked token = bot compromised, can spam users.

---

## Stack Options

| Language | Framework | Best For |
|----------|-----------|----------|
| **Rust** | serenity + poise | Performance, type safety |
| **Python** | discord.py / nextcord | Rapid development |
| **Node** | discord.js | JS ecosystem, largest community |

---

## Quick Start

### Rust (serenity + poise)

```toml
# Cargo.toml
[dependencies]
serenity = { version = "0.12", features = ["framework"] }
poise = "0.6"
tokio = { version = "1", features = ["full"] }
```

```rust
use poise::serenity_prelude as serenity;

struct Data {}
type Error = Box<dyn std::error::Error + Send + Sync>;
type Context<'a> = poise::Context<'a, Data, Error>;

/// Say hello
#[poise::command(slash_command)]
async fn hello(ctx: Context<'_>) -> Result<(), Error> {
    ctx.say("Hello!").await?;
    Ok(())
}

#[tokio::main]
async fn main() {
    let framework = poise::Framework::builder()
        .options(poise::FrameworkOptions {
            commands: vec![hello()],
            ..Default::default()
        })
        .setup(|ctx, _ready, framework| {
            Box::pin(async move {
                poise::builtins::register_globally(ctx, &framework.options().commands).await?;
                Ok(Data {})
            })
        })
        .build();

    let token = std::env::var("DISCORD_TOKEN").unwrap();
    let intents = serenity::GatewayIntents::non_privileged();

    let client = serenity::ClientBuilder::new(token, intents)
        .framework(framework)
        .await
        .unwrap();

    client.start().await.unwrap();
}
```

### Python (discord.py)

```python
# requirements.txt
discord.py>=2.0
```

```python
import discord
from discord import app_commands

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@tree.command(name="hello", description="Say hello")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("Hello!")

@client.event
async def on_ready():
    await tree.sync()
    print(f"Logged in as {client.user}")

client.run("BOT_TOKEN")
```

### Node (discord.js)

```typescript
// package.json: "discord.js": "^14.14"
import { Client, GatewayIntentBits, SlashCommandBuilder, REST, Routes } from 'discord.js';

const client = new Client({ intents: [GatewayIntentBits.Guilds] });

const commands = [
  new SlashCommandBuilder().setName('hello').setDescription('Say hello'),
].map(cmd => cmd.toJSON());

client.once('ready', async () => {
  const rest = new REST().setToken(process.env.DISCORD_TOKEN!);
  await rest.put(Routes.applicationCommands(client.user!.id), { body: commands });
  console.log(`Logged in as ${client.user?.tag}`);
});

client.on('interactionCreate', async (interaction) => {
  if (!interaction.isChatInputCommand()) return;
  if (interaction.commandName === 'hello') {
    await interaction.reply('Hello!');
  }
});

client.login(process.env.DISCORD_TOKEN);
```

---

## Slash Commands

### With Options (Rust/poise)

```rust
/// Ban a user
#[poise::command(slash_command, required_permissions = "BAN_MEMBERS")]
async fn ban(
    ctx: Context<'_>,
    #[description = "User to ban"] user: serenity::User,
    #[description = "Reason"] reason: Option<String>,
) -> Result<(), Error> {
    let reason = reason.unwrap_or_else(|| "No reason provided".to_string());

    ctx.guild_id()
        .unwrap()
        .ban_with_reason(&ctx.serenity_context().http, user.id, 0, &reason)
        .await?;

    ctx.say(format!("Banned {} for: {}", user.name, reason)).await?;
    Ok(())
}
```

### With Options (Python)

```python
@tree.command(name="ban", description="Ban a user")
@app_commands.describe(user="User to ban", reason="Reason for ban")
@app_commands.default_permissions(ban_members=True)
async def ban(
    interaction: discord.Interaction,
    user: discord.Member,
    reason: str = "No reason provided"
):
    await user.ban(reason=reason)
    await interaction.response.send_message(f"Banned {user.name} for: {reason}")
```

---

## Embeds

### Rust

```rust
use serenity::builder::{CreateEmbed, CreateMessage};

let embed = CreateEmbed::new()
    .title("User Info")
    .description("Details about the user")
    .field("Username", &user.name, true)
    .field("ID", user.id.to_string(), true)
    .color(0x00ff00)
    .thumbnail(user.avatar_url().unwrap_or_default());

ctx.send(poise::CreateReply::default().embed(embed)).await?;
```

### Python

```python
embed = discord.Embed(
    title="User Info",
    description="Details about the user",
    color=0x00ff00
)
embed.add_field(name="Username", value=user.name, inline=True)
embed.add_field(name="ID", value=str(user.id), inline=True)
embed.set_thumbnail(url=user.avatar.url if user.avatar else None)

await interaction.response.send_message(embed=embed)
```

---

## Buttons & Components

### Rust

```rust
use serenity::builder::{CreateButton, CreateActionRow};

let button = CreateButton::new("confirm")
    .label("Confirm")
    .style(serenity::ButtonStyle::Primary);

let cancel = CreateButton::new("cancel")
    .label("Cancel")
    .style(serenity::ButtonStyle::Danger);

let row = CreateActionRow::Buttons(vec![button, cancel]);

ctx.send(poise::CreateReply::default()
    .content("Are you sure?")
    .components(vec![row])
).await?;
```

### Python

```python
from discord.ui import Button, View

class ConfirmView(View):
    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.primary)
    async def confirm(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("Confirmed!")
        self.stop()

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.danger)
    async def cancel(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("Cancelled!")
        self.stop()

view = ConfirmView()
await interaction.response.send_message("Are you sure?", view=view)
```

---

## Event Handlers

### Rust

```rust
struct Handler;

#[serenity::async_trait]
impl serenity::EventHandler for Handler {
    async fn message(&self, ctx: serenity::Context, msg: serenity::Message) {
        if msg.content == "!ping" {
            msg.channel_id.say(&ctx.http, "Pong!").await.ok();
        }
    }

    async fn guild_member_addition(&self, ctx: serenity::Context, member: serenity::Member) {
        if let Some(channel) = member.guild_id.to_guild_cached(&ctx.cache) {
            // Send welcome message
        }
    }
}
```

### Python

```python
@client.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return
    if message.content == "!ping":
        await message.channel.send("Pong!")

@client.event
async def on_member_join(member: discord.Member):
    channel = member.guild.system_channel
    if channel:
        await channel.send(f"Welcome {member.mention}!")
```

---

## Permissions

### Rust

```rust
#[poise::command(
    slash_command,
    required_permissions = "MANAGE_MESSAGES",  // Bot needs this
    default_member_permissions = "MANAGE_MESSAGES",  // User needs this
)]
async fn clear(
    ctx: Context<'_>,
    #[description = "Number of messages"] count: u8,
) -> Result<(), Error> {
    let messages = ctx.channel_id()
        .messages(&ctx.serenity_context().http, serenity::GetMessages::new().limit(count))
        .await?;

    ctx.channel_id()
        .delete_messages(&ctx.serenity_context().http, messages)
        .await?;

    ctx.say(format!("Deleted {} messages", count)).await?;
    Ok(())
}
```

---

## Sharding (for 2500+ servers)

### Rust

```rust
let client = serenity::ClientBuilder::new(token, intents)
    .framework(framework)
    .await?;

// Auto-sharding
client.start_autosharded().await?;

// Or manual sharding
// client.start_shard(shard_id, total_shards).await?;
```

### Python

```python
from discord import AutoShardedClient

client = AutoShardedClient(intents=intents)
```

---

## Environment & Security

```bash
# .env
DISCORD_TOKEN=your_bot_token
GUILD_ID=123456789  # For development

# .gitignore
.env
```

---

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Commands not showing | Call `tree.sync()` / register commands |
| Missing intents | Enable in Developer Portal + code |
| Rate limits | Use caching, batch operations |
| Privileged intents | Enable in portal for members/presence |
| Token exposed | Use env vars, never commit |

---

## Bot Permissions Calculator

Required intents for common features:
- Messages: `MESSAGE_CONTENT` (privileged)
- Members: `GUILD_MEMBERS` (privileged)
- Presence: `GUILD_PRESENCES` (privileged)

Invite URL format:
```
https://discord.com/api/oauth2/authorize?client_id=YOUR_ID&permissions=PERMS&scope=bot%20applications.commands
```

---

## Testing

### Rust (serenity/poise)

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parse_duration() {
        assert_eq!(parse_duration("1h"), Duration::hours(1));
        assert_eq!(parse_duration("30m"), Duration::minutes(30));
    }

    #[tokio::test]
    async fn test_ban_requires_permission() {
        // Test permission checks
        let result = check_ban_permission(user_without_perms).await;
        assert!(result.is_err());
    }
}
```

### Python (discord.py)

```python
import pytest
from unittest.mock import AsyncMock, MagicMock

@pytest.fixture
def mock_interaction():
    interaction = MagicMock()
    interaction.response.send_message = AsyncMock()
    interaction.user.guild_permissions.ban_members = True
    return interaction

@pytest.mark.asyncio
async def test_hello_command(mock_interaction):
    await hello(mock_interaction)
    mock_interaction.response.send_message.assert_called_once()

@pytest.mark.asyncio
async def test_ban_without_permission(mock_interaction):
    mock_interaction.user.guild_permissions.ban_members = False
    with pytest.raises(discord.errors.Forbidden):
        await ban(mock_interaction, MagicMock())
```

### Node (discord.js)

```typescript
import { describe, it, expect, vi } from 'vitest';

describe('Commands', () => {
  it('hello command replies', async () => {
    const interaction = {
      reply: vi.fn(),
      isChatInputCommand: () => true,
      commandName: 'hello',
    };

    await handleInteraction(interaction);
    expect(interaction.reply).toHaveBeenCalled();
  });
});
```

---

## TDD Workflow

```
1. Task[tdd-test-writer]: "Create /ban slash command"
   → Writes test expecting permission check + success
   → cargo test / pytest / npm test → FAILS (RED)

2. Task[rust-developer]: "Implement /ban command"
   → Implements with permission checks
   → Tests PASS (GREEN)

3. Repeat for each command

4. Task[code-reviewer]: "Review bot implementation"
   → Checks security, permissions, rate limits
```

---

## Security Checklist

- [ ] Token in environment variable (never in code)
- [ ] `.env` in `.gitignore`
- [ ] pre-commit hooks with gitleaks
- [ ] Permission checks on all moderation commands
- [ ] Rate limiting for user commands
- [ ] Input sanitization (no injection in embeds)
- [ ] No privileged intents unless needed
- [ ] Audit log for moderation actions

---

## Project Structure

```
discord-bot/
├── src/
│   ├── main.rs
│   ├── commands/
│   │   ├── mod.rs
│   │   ├── moderation.rs
│   │   └── fun.rs
│   └── events.rs
├── tests/
│   └── commands_test.rs
├── Cargo.toml
├── .env.example
├── .env              # NOT committed
└── .gitignore
```
