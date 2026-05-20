---
name: pexpect-cli
description: Persistent pexpect sessions for automating interactive terminal applications. Use when you need to control interactive programs like ssh, databases, or debuggers that require user input.
---

# Usage

```bash
# Start a new session
pexpect-cli --start
# 888d9bf4

# Start with a label
pexpect-cli --start --name ssh-prod
# a3f4b2c1

# Execute code in a session
pexpect-cli 888d9bf4 <<'EOF'
child = pexpect.spawn("bash")
child.sendline("pwd")
child.expect(r"\$")
print(child.before.decode())
EOF

# List sessions
pexpect-cli --list

# Stop a session
pexpect-cli --stop 888d9bf4
```

# Examples

## SSH Session

```bash
session=$(pexpect-cli --start --name ssh-session)

pexpect-cli $session <<'EOF'
child = pexpect.spawn('ssh user@example.com')
child.expect('password:')
child.sendline('mypassword')
child.expect('\$')
print("Connected!")
EOF

# Run commands
pexpect-cli $session <<'EOF'
child.sendline('uptime')
child.expect('\$')
print(child.before.decode())
EOF
```

## Database Interaction

```bash
session=$(pexpect-cli --start --name db-session)

pexpect-cli $session <<'EOF'
child = pexpect.spawn('sqlite3 mydb.db')
child.expect('sqlite>')
child.sendline('.tables')
child.expect('sqlite>')
print("Tables:", child.before.decode())
EOF
```

# Available in Namespace

- `pexpect`: The pexpect module
- `child`: Persistent child process variable (persists across executions)

See [README.md](../../pexpect-cli/README.md) for installation, monitoring, and advanced usage.
