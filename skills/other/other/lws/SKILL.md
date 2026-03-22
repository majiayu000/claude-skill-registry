---
name: lws
description: Lightweight Wallet Signer CLI — generate wallets, derive addresses, and sign messages across EVM, Solana, Bitcoin, Cosmos, and Tron chains.
version: 0.1.0
metadata:
  openclaw:
    requires:
      bins:
        - git
        - cargo
    homepage: https://github.com/dawnlabsai/lws
    os:
      - darwin
      - linux
---

# LWS CLI

Minimal, offline-first CLI for generating wallets, deriving addresses, and signing messages across multiple chains.

## Installation

One-liner:

```bash
curl -fsSL https://raw.githubusercontent.com/dawnlabsai/lws/main/lws/install.sh | bash
```

The installer will:
1. Install Rust via `rustup` if not already present
2. Clone the repo and build from source
3. Place the `lws` binary at `~/.lws/bin/lws`
4. Add `~/.lws/bin` to your shell's `PATH` (supports zsh, bash, fish)

Set `LWS_INSTALL_DIR` to override the install location.

From source:

```bash
git clone https://github.com/dawnlabsai/lws.git
cd lws/lws
cargo build --workspace --release
cp target/release/lws ~/.lws/bin/lws
```

## Commands

### `lws generate`

Generate a new BIP-39 mnemonic phrase.

```
lws generate [--words 12|24]
```

- `--words` — Number of mnemonic words, 12 or 24 (default: `12`)

### `lws derive`

Derive an address from a mnemonic.

```
lws derive --mnemonic <PHRASE> --chain <CHAIN> [--index 0]
```

- `--mnemonic` — BIP-39 mnemonic phrase (required)
- `--chain` — Chain type: `evm`, `solana`, `bitcoin`, `cosmos`, `tron` (required)
- `--index` — Account index (default: `0`)

### `lws sign`

Sign a message with a mnemonic-derived key.

```
lws sign --mnemonic <PHRASE> --chain <CHAIN> --message <MSG> [--index 0]
```

- `--mnemonic` — BIP-39 mnemonic phrase (required)
- `--chain` — Chain type (required)
- `--message` — Message to sign (required)
- `--index` — Account index (default: `0`)

### `lws info`

Show the vault path and list supported chains.

```
lws info
```

### `lws create-wallet`

Create a new wallet — generates a mnemonic and saves a wallet descriptor to the vault.

```
lws create-wallet --name <NAME> --chain <CHAIN> [--words 12|24]
```

- `--name` — Wallet name (required)
- `--chain` — Chain type (required)
- `--words` — Mnemonic word count (default: `12`)

### `lws list-wallets`

List all saved wallets in the vault.

```
lws list-wallets
```

### `lws update`

Update lws to the latest version by building from the latest commit.

```
lws update [--force]
```

- `--force` — Rebuild even if already on the latest commit

### `lws uninstall`

Remove lws from the system.

```
lws uninstall [--purge]
```

- `--purge` — Also remove all wallet data and config (`~/.lws`)

Removes the binary, cleans PATH entries from shell config files, and optionally deletes the entire `~/.lws` directory. Prompts for confirmation before proceeding.

## File Layout

```
~/.lws/
├── bin/
│   └── lws              # CLI binary
└── wallets/
    └── <wallet-id>.json  # Wallet descriptors
```
