---
name: pass
description: >
  Complete guide for using pass, the standard Unix password manager. Use this
  skill whenever the user asks about pass, password-store, managing passwords
  from the terminal, GPG-encrypted passwords, setting up pass for the first
  time, inserting or generating passwords, syncing a password store with git,
  using pass-otp for TOTP codes, importing passwords from another manager, or
  any task involving the `pass` CLI. Trigger on phrases like "set up pass",
  "add a password to pass", "sync my password store", "generate a password",
  "pass git", "pass-otp", "pass-import", or any variation.
---

# pass — The Standard Unix Password Manager

Each password is a GPG-encrypted file under `~/.password-store/`. The store is
plain files in a folder hierarchy; no proprietary formats, no daemon.

---

## 1. Installation

### Linux

| Distro           | Command                        |
|------------------|--------------------------------|
| Arch / Manjaro   | `pacman -S pass`               |
| Debian / Ubuntu  | `apt install pass`             |
| Fedora / RHEL    | `dnf install pass`             |
| openSUSE         | `zypper in password-store`     |

### macOS

```bash
brew install pass
```

---

## 2. GPG Key Setup

pass requires a GPG key. Skip this block if you already have one.

```bash
# Generate a new key (use RSA 4096 or ed25519)
gpg --full-generate-key

# List your keys — note the key ID or email
gpg --list-secret-keys --keyid-format LONG
```

The key ID looks like `3AA5C34371567BD2` or you can use the email you registered.

---

## 3. Initialise the Store

```bash
pass init "your@email.com"
# or using the key ID:
pass init 3AA5C34371567BD2
```

This creates `~/.password-store/` and a `.gpg-id` file.

Multiple GPG IDs are supported (for team use):

```bash
pass init alice@example.com bob@example.com
```

Use `-p` to scope a different GPG key to a subfolder (useful for shared stores):

```bash
pass init -p work/ work@company.com
```

Running `pass init` on an existing store re-encrypts all entries with the new key(s).

---

## 4. Data Organisation Convention

Store each entry as a **multiline file** with this structure:

```
<password>
url: https://example.com
username: you@example.com
notes: anything extra
```

- **First line is always the password.** `pass -c` and clipboard tools only
  copy line 1.
- Use lowercase keys (`url:`, `username:`, `notes:`) for compatibility with
  browser extensions and `pass-import`.
- Organise with folders that mirror context, not the URL structure:

```
~/.password-store/
├── email/
│   ├── gmail
│   └── fastmail
├── dev/
│   ├── github
│   └── npm
└── finance/
    ├── bank-hsbc
    └── revolut
```

---

## 5. Daily Usage

### List the store

```bash
pass                       # full tree
pass email/                # subtree
pass ls email/             # explicit alias
```

### Find entries by name

```bash
pass find github           # lists all entries whose path matches "github"
```

### Read a password

```bash
pass email/gmail           # print all lines to stdout
pass -c email/gmail        # copy line 1 to clipboard (clears after 45s)
pass -c2 email/gmail       # copy line 2 (e.g. the username) to clipboard
```

### Search inside decrypted content

```bash
pass grep username         # grep across all decrypted entries
pass grep -i "amazon"      # case-insensitive; accepts any grep option
```

### Insert an existing password

```bash
pass insert email/gmail              # prompted twice for confirmation
pass insert -e email/gmail           # echo password as you type (single prompt)
pass insert -m email/gmail           # multiline (recommended, ends with Ctrl-D)
pass insert -f email/gmail           # overwrite without prompt
```

### Generate a new password

```bash
pass generate email/gmail            # 25-char password (default length)
pass generate email/gmail 20        # custom length
pass generate -n email/gmail 20     # no symbols
pass generate -c email/gmail 20     # copy to clipboard instead of printing
pass generate -i email/gmail 20     # replace only line 1, keep rest of file
pass generate -f email/gmail 20     # overwrite without prompt
```

### Edit an entry

```bash
pass edit email/gmail      # opens $EDITOR; creates entry if it doesn't exist
```

### Remove an entry

```bash
pass rm email/gmail
pass rm -r email/          # remove a folder recursively
pass rm -f email/gmail     # no confirmation prompt
```

### Move / copy

```bash
pass mv email/gmail email/gmail-old
pass mv -f email/gmail email/gmail-old   # overwrite without prompt
pass cp email/gmail backup/gmail
pass cp -f email/gmail backup/gmail      # overwrite without prompt
```

---

## 6. Git Sync

Initialise git inside the store:

```bash
pass git init
pass git remote add origin git@github.com:you/pass-store.git
```

Every `pass insert`, `generate`, `edit`, `rm` automatically creates a git
commit. Push and pull manually:

```bash
pass git push
pass git pull
```

To clone the store on another machine:

```bash
# Import your GPG key first:
gpg --import private-key.asc
gpg --edit-key your@email.com  # then: trust → 5 → quit

# Clone the store:
git clone git@github.com:you/pass-store.git ~/.password-store
```

---

## 7. Extensions

### pass-otp (TOTP / 2FA codes)

```bash
# Install
pacman -S pass-otp          # Arch
brew install pass-otp       # macOS

# Add a TOTP secret (use the otpauth:// URI from your provider)
pass otp insert totp/github
# paste: otpauth://totp/GitHub:you@example.com?secret=BASE32SECRET&issuer=GitHub

# Generate a code
pass otp totp/github

# Copy to clipboard
pass otp -c totp/github
```

### pass-import (migrate from another manager)

```bash
pip install pass-import    # or: pacman -S pass-import

# Import from Bitwarden (JSON export)
pass import bitwarden bitwarden-export.json

# Import from 1Password (1PUX export)
pass import 1password export.1pux

# List all supported formats
pass import --list
```

### pass-update

```bash
# Install
git clone https://github.com/roddhjav/pass-update ~/.password-store/.extensions/update.bash

# Update a password interactively
pass update email/gmail
```

---

## 8. Shell Completion

```bash
# bash — add to ~/.bashrc
source /usr/share/bash-completion/completions/pass

# zsh — add to ~/.zshrc
autoload -U compinit && compinit

# fish — works out of the box after install
```

---

## 9. Useful Environment Variables

| Variable                          | Purpose                                      |
|-----------------------------------|----------------------------------------------|
| `PASSWORD_STORE_DIR`              | Override default `~/.password-store`         |
| `PASSWORD_STORE_KEY`              | Default GPG key ID                           |
| `PASSWORD_STORE_GIT`              | Override git directory                       |
| `PASSWORD_STORE_CLIP_TIME`        | Seconds before clipboard clears (default 45) |
| `PASSWORD_STORE_ENABLE_EXTENSIONS`| Set to `true` to enable user extensions      |
| `EDITOR`                          | Editor used by `pass edit`                   |

---

## 10. Troubleshooting

**`gpg: decryption failed: No secret key`**
Your GPG key is not available. Import it with `gpg --import` and set trust.

**`gpg-agent` keeps asking for passphrase**
Add to `~/.gnupg/gpg-agent.conf`:
```
default-cache-ttl 3600
max-cache-ttl 14400
```
Then restart: `gpgconf --kill gpg-agent`

**Clipboard does not clear on Wayland**
Install `wl-clipboard` and set `PASSWORD_STORE_CLIP_TOOL=wl-copy` or pass `-c`
with `wl-clipboard` in PATH.

**pass git shows dirty tree after clone**
Run `pass git status`; if only `.gpg-id` is untracked, run `pass git add .`
and `pass git commit -m "add gpg-id"`.
