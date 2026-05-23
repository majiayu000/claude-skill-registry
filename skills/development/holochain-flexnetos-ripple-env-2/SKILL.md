---
name: Holochain Development
description: "Holochain DHT development for distributed coordination. Activate when: (1) Building Holochain applications (hApps), (2) Writing Zome code in Rust, (3) Configuring conductor and lair-keystore, (4) Working with DHT entries and links, or (5) Setting up Holochain development environment."
---

# Holochain Development

## Overview

Holochain is a framework for building fully distributed, peer-to-peer applications. It uses a distributed hash table (DHT) for data storage and validation without global consensus.

## Key Concepts

| Concept | Description |
|---------|-------------|
| **hApp** | Holochain Application - a collection of DNAs |
| **DNA** | Distributed Network Architecture - defines data types and validation rules |
| **Zome** | A module within a DNA written in Rust/WASM |
| **Entry** | A piece of data stored on the DHT |
| **Link** | A directed connection between two entries |
| **Agent** | A participant in the network with a unique key pair |
| **Conductor** | Runtime that hosts hApps and manages connections |
| **Lair** | Key management service (lair-keystore) |

## Installation

### Via Nix (Recommended)

```nix
# flake.nix
{
  inputs.holochain.url = "github:holochain/holochain";

  devShells.default = pkgs.mkShell {
    packages = [
      holochain
      lair-keystore
      hc  # Holochain CLI
    ];
  };
}
```

### Via Cargo

```bash
cargo install holochain
cargo install lair_keystore
```

## Quick Start

### Create a New hApp

```bash
# Scaffold new project
hc scaffold web-app my-happ

# Structure created:
# my-happ/
# ├── dnas/
# │   └── my_dna/
# │       ├── workdir/
# │       └── zomes/
# │           └── coordinator/
# │               └── src/lib.rs
# ├── ui/
# └── workdir/

# Build the hApp
hc dna pack dnas/my_dna/workdir
hc app pack workdir
```

### Zome Development

```rust
// zomes/coordinator/src/lib.rs
use hdk::prelude::*;

#[hdk_entry_helper]
pub struct Post {
    pub title: String,
    pub content: String,
}

#[hdk_extern]
pub fn create_post(post: Post) -> ExternResult<ActionHash> {
    create_entry(&EntryTypes::Post(post.clone()))
}

#[hdk_extern]
pub fn get_post(action_hash: ActionHash) -> ExternResult<Option<Record>> {
    get(action_hash, GetOptions::default())
}

#[hdk_extern]
pub fn get_all_posts() -> ExternResult<Vec<Record>> {
    let path = Path::from("all_posts");
    let links = get_links(path.path_entry_hash()?, LinkTypes::AllPosts, None)?;

    let posts: Vec<Record> = links
        .into_iter()
        .filter_map(|link| get(link.target, GetOptions::default()).ok().flatten())
        .collect();

    Ok(posts)
}
```

### Entry Definitions

```rust
#[hdk_entry_defs]
#[unit_enum(UnitEntryTypes)]
pub enum EntryTypes {
    Post(Post),
    Comment(Comment),
}

#[hdk_link_types]
pub enum LinkTypes {
    AllPosts,
    PostToComments,
}
```

## Conductor Configuration

```yaml
# conductor-config.yaml
environment_path: /tmp/holochain
keystore:
  type: lair_server
  connection_url: unix:///tmp/lair/socket?k=...

admin_interfaces:
  - driver:
      type: websocket
      port: 4444

network:
  transport_pool:
    - type: webrtc
      signal_url: wss://signal.holochain.org
```

## Testing

### Unit Tests (Rust)

```rust
#[cfg(test)]
mod tests {
    use super::*;
    use holochain::sweettest::*;

    #[tokio::test(flavor = "multi_thread")]
    async fn test_create_post() {
        let (conductors, _) = SweetConductorBatch::from_standard_config(1).await;
        let apps = conductors.setup_app("test", &[]).await.unwrap();

        let post = Post {
            title: "Test".to_string(),
            content: "Content".to_string(),
        };

        let hash: ActionHash = conductors[0]
            .call(&apps[0].cells()[0].zome("posts"), "create_post", post)
            .await;

        assert!(!hash.is_empty());
    }
}
```

### Integration Tests (Tryorama)

```typescript
// tests/src/post.test.ts
import { runScenario } from '@holochain/tryorama';

test('create and get post', async () => {
  await runScenario(async scenario => {
    const appBundleSource = { path: './workdir/my-happ.happ' };
    const [alice] = await scenario.addPlayers([{ appBundleSource }]);

    const post = { title: 'Hello', content: 'World' };
    const hash = await alice.cells[0].callZome({
      zome_name: 'posts',
      fn_name: 'create_post',
      payload: post,
    });

    expect(hash).toBeTruthy();
  });
});
```

## Common Patterns

### Validation Rules

```rust
#[hdk_extern]
pub fn validate(op: Op) -> ExternResult<ValidateCallbackResult> {
    match op.flattened::<EntryTypes, LinkTypes>()? {
        FlatOp::StoreEntry(OpEntry::CreateEntry { entry, .. }) => {
            match entry {
                EntryTypes::Post(post) => {
                    if post.title.is_empty() {
                        return Ok(ValidateCallbackResult::Invalid(
                            "Title cannot be empty".into()
                        ));
                    }
                    Ok(ValidateCallbackResult::Valid)
                }
                _ => Ok(ValidateCallbackResult::Valid)
            }
        }
        _ => Ok(ValidateCallbackResult::Valid)
    }
}
```

### Signal Emission

```rust
#[hdk_extern]
pub fn create_post(post: Post) -> ExternResult<ActionHash> {
    let hash = create_entry(&EntryTypes::Post(post.clone()))?;

    // Emit signal to UI
    emit_signal(&Signal::PostCreated { hash: hash.clone(), post })?;

    Ok(hash)
}
```

## Commands Reference

| Command | Description |
|---------|-------------|
| `hc scaffold web-app <name>` | Create new hApp project |
| `hc dna pack <workdir>` | Package DNA |
| `hc app pack <workdir>` | Package hApp |
| `hc sandbox generate` | Generate sandbox environment |
| `hc sandbox run` | Run sandbox conductor |
| `holochain -c <config>` | Run conductor with config |
| `lair-keystore server` | Start keystore server |

## External Links

- [Holochain Developer Portal](https://developer.holochain.org/)
- [Holochain GitHub](https://github.com/holochain/holochain)
- [HDK Documentation](https://docs.rs/hdk)
- [Tryorama Testing](https://github.com/holochain/tryorama)
