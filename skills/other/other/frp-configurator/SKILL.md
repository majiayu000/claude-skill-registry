---
name: frp-configurator
description: "Automates FRP (Fast Reverse Proxy) deployment. Configures Client/Server, sets up Systemd services/Web UI, and generates pairing installers for the counterpart platform. Invoke when user wants to setup FRP, tunneling, or remote access."
---

# FRP Configurator

This skill helps you set up and manage FRP (Fast Reverse Proxy) for secure intranet penetration and remote access.

## Capabilities

1.  **Configure Local (Client)**: Install and configure `frpc` on the current machine.
2.  **Configure Remote (Server)**: Install and configure `frps` on the current machine.
3.  **Pairing / Export**:
    *   **Export to Remote**: If you have a Client config, generate a Server installer package that matches your keys.
    *   **Export to Local**: If you have a Server config, generate a Client installer package that matches your keys.
4.  **Uninstall**: Remove FRP services and configuration.

## Tools & Scripts

Located in `scripts/`:

*   `setup_client.sh`: Installs `frpc`, sets up systemd service, configures Web UI.
*   `setup_server.sh`: Installs `frps`, sets up systemd service, configures Dashboard.
*   `pack_for_server.sh`: Reads local `frpc.toml` $\rightarrow$ Generates `frps_bundle.tar.gz`.
*   `pack_for_client.sh`: Reads local `frps.toml` $\rightarrow$ Generates `frpc_bundle.tar.gz`.
*   `uninstall.sh`: Stops services and removes FRP installation.

## Usage Examples

### 1. Setup Client (Local)
```bash
# Interactive setup
bash scripts/setup_client.sh

# Non-interactive / Automated setup (Recommended for scripts)
# This avoids the "Connection Refused" error by setting the correct server upfront.
export FRP_SERVER_IP="x.x.x.x"     # Replace with your Server IP
export FRP_SERVER_PORT="7000"      # Replace with your Server Port
export FRP_AUTH_TOKEN="my-secret-token" # Replace with your Token
bash scripts/setup_client.sh -y    # Use -y to skip prompts
```

### 2. Setup Server (Remote)
```bash
# Interactive setup
bash scripts/setup_server.sh
```

### 3. I have a Client, I need to setup the Server
```bash
# Generate server installer based on my client config
bash scripts/pack_for_server.sh
# Then upload 'frps_bundle.tar.gz' to your server and run the install script inside.
```

### 4. I have a Server, I need to setup a Client
```bash
# Generate client installer based on my server config
bash scripts/pack_for_client.sh
# Then download 'frpc_bundle.tar.gz' to your client machine and run the install script inside.
```

### 5. Uninstall
```bash
bash scripts/uninstall.sh
```

## Configuration Details

*   **Default Install Path**: `/srv/frp`
*   **Config Files**: `frpc.toml` / `frps.toml`
*   **Systemd Services**: `frpc.service` / `frps.service`
*   **Web UI**:
    *   Client Admin: Port 7555 (default)
    *   Server Dashboard: Port 7500 (default)

## Troubleshooting

### Connection Refused (client/service.go error)

If you see errors like `connect to server error: dial tcp 127.0.0.1:7000: connect: connection refused` in the logs:
1.  **Check Config**: Ensure `serverAddr` in `/srv/frp/frpc.toml` points to your actual Remote Server IP, not `127.0.0.1`.
2.  **Check Logs**: `tail -f /srv/frp/frpc.log`
3.  **Update Config**:
    ```toml
    # /srv/frp/frpc.toml
    serverAddr = "YOUR_REMOTE_IP"
    serverPort = 7000 # Must match server's bindPort
    auth.token = "YOUR_AUTH_TOKEN" # Must match server's auth.token
    ```
4.  **Restart Service**: `sudo systemctl restart frpc`

### Example Configuration (frpc.toml)

```toml
serverAddr = "203.0.113.10"
serverPort = 7000

auth.method = "token"
auth.token = "secure_token_123"

# Expose local SSH (Port 22) to Remote Server (Port 6000)
[[proxies]]
name = "ssh-my-laptop"
type = "tcp"
localIP = "127.0.0.1"
localPort = 22
remotePort = 6000
```
