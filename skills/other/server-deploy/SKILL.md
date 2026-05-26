---
name: server-deploy
description: 通用项目部署到远程服务器。自动识别项目类型（Node.js/Python/Rust/Go/静态站），SSH 配置、环境安装、项目上传、进程管理、Nginx 反向代理、Cloudflare SSL、安全加固。当用户需要部署项目、上线服务、配置域名时使用
allowed-tools: Bash, Read, Write, Edit, AskUserQuestion, Task, Glob, Grep
metadata:
  argument-hint: "[SSH连接信息，如 root@host]"
---

# 通用服务器部署

将本地项目一键部署到远程 Linux 服务器。自动识别项目类型，适配对应的构建、运行和进程管理方案。

---

## 第零步：项目识别与信息收集

### 0a. 自动识别项目类型

扫描项目根目录，按以下规则判断类型：

| 标志文件 | 项目类型 | 运行时 | 进程管理 |
|---------|---------|--------|---------|
| `package.json` | Node.js | node | PM2 |
| `Cargo.toml` | Rust | 编译产物 | systemd |
| `go.mod` | Go | 编译产物 | systemd |
| `pyproject.toml` / `requirements.txt` / `setup.py` | Python | python3 | systemd / gunicorn |
| `Dockerfile` / `docker-compose.yml` | Docker | docker | docker compose |
| `index.html`（无其他标志） | 静态站点 | 无 | Nginx 直接托管 |

如果检测到多个标志文件（如 package.json + Dockerfile），用 AskUserQuestion 让用户选择部署方式。

### 0b. 收集信息

用 AskUserQuestion 收集以下信息（上下文已有的跳过）：

1. **SSH 连接**（header: "服务器"）
   - 根据上下文动态生成选项（如之前用过的服务器 IP）
   - 兜底选项"其他服务器"

2. **项目路径**（header: "项目"）
   - 根据当前工作目录自动推断
   - 如果不确定，询问用户

3. **域名**（header: "域名"）
   - 已有域名（让用户输入）
   - 仅用 IP 访问（跳过域名和 SSL 配置）

4. **运行端口**（header: "端口"）
   - 自动检测：
     - Node.js：从 package.json scripts 或 .env 中提取
     - Python：从 main.py / app.py / manage.py 中提取
     - Rust/Go：从 main.rs / main.go 或配置文件中提取
   - 如检测不到，让用户指定
   - 禁止使用 3000, 3001, 4000, 5000, 5173, 8000, 8080, 8888

### 0c. 变量定义

| 变量 | 说明 |
|------|------|
| `$SSH_TARGET` | SSH 连接串（如 `root@192.168.1.1`） |
| `$PROJECT_DIR` | 本地项目绝对路径 |
| `$PROJECT_NAME` | 项目名称 |
| `$PROJECT_TYPE` | 项目类型：`nodejs` / `python` / `rust` / `go` / `docker` / `static` |
| `$REMOTE_DIR` | 远程部署目录（默认 `/opt/$PROJECT_NAME`） |
| `$PORT` | 应用运行端口 |
| `$DOMAIN` | 域名（可选） |

---

## 第一步：SSH 连接与密钥配置

### 1a. 检查本地 SSH 公钥

```bash
cat ~/.ssh/id_rsa.pub 2>/dev/null || cat ~/.ssh/id_ed25519.pub 2>/dev/null
```

如果没有公钥，生成一个：`ssh-keygen -t ed25519 -N "" -f ~/.ssh/id_ed25519`

### 1b. 测试免密登录

```bash
ssh -o ConnectTimeout=5 -o BatchMode=yes $SSH_TARGET "echo ok" 2>/dev/null
```

如果失败，用密码登录并添加公钥：

```bash
sshpass -p '<PASSWORD>' ssh -o StrictHostKeyChecking=no $SSH_TARGET \
  "mkdir -p ~/.ssh && chmod 700 ~/.ssh && echo '<PUBLIC_KEY>' >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
```

### 1c. 验证免密登录

```bash
ssh -o ConnectTimeout=5 $SSH_TARGET "echo '免密登录成功' && uname -a"
```

---

## 第二步：服务器环境检查

**单条命令获取全部信息**：

```bash
ssh $SSH_TARGET "echo '=== 系统 ===' && cat /etc/os-release | grep PRETTY_NAME && uname -m && echo '=== CPU ===' && nproc && echo '=== 内存 ===' && free -h && echo '=== 磁盘 ===' && df -h / && echo '=== 包管理器 ===' && which apt yum dnf pacman 2>/dev/null && echo '=== Node.js ===' && node -v 2>/dev/null || echo '未安装' && echo '=== Python ===' && python3 --version 2>/dev/null || echo '未安装' && echo '=== Rust ===' && rustc --version 2>/dev/null || echo '未安装' && echo '=== Go ===' && go version 2>/dev/null || echo '未安装' && echo '=== Docker ===' && docker --version 2>/dev/null || echo '未安装' && echo '=== Nginx ===' && nginx -v 2>&1 || echo '未安装'"
```

**检查要点**：
- 磁盘空间是否足够
- 内存：Node.js ≥ 512MB，Rust 编译 ≥ 1GB（或本地交叉编译）
- 架构：`x86_64` / `aarch64`（Rust/Go 需匹配编译目标）
- 记录缺少的组件，后续统一安装

---

## 第三步：安装运行时环境

根据 `$PROJECT_TYPE` 安装对应运行时。仅安装缺少的组件。

### Node.js 项目

```bash
# 安装 Node.js 20（如未安装）
ssh $SSH_TARGET "curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && apt-get install -y nodejs"
# 安装 PM2
ssh $SSH_TARGET "npm install -g pm2"
```

### Python 项目

```bash
# 安装 Python3 + pip + venv（如未安装）
ssh $SSH_TARGET "apt-get install -y python3 python3-pip python3-venv"
```

### Rust 项目

两种方案，根据服务器资源选择：

**方案 A：服务器编译（内存 ≥ 1GB）**
```bash
ssh $SSH_TARGET "curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y && source ~/.cargo/env"
```

**方案 B：本地交叉编译（推荐低配服务器）**
```bash
# 本地编译（需安装对应 target）
rustup target add x86_64-unknown-linux-gnu  # 或 aarch64-unknown-linux-gnu
cargo build --release --target x86_64-unknown-linux-gnu
# 仅上传编译产物
```

### Go 项目

同样两种方案：

**方案 A：服务器编译**
```bash
ssh $SSH_TARGET "wget -q https://go.dev/dl/go1.22.0.linux-amd64.tar.gz && tar -C /usr/local -xzf go1.22.0.linux-amd64.tar.gz && echo 'export PATH=\$PATH:/usr/local/go/bin' >> ~/.bashrc"
```

**方案 B：本地交叉编译（推荐）**
```bash
GOOS=linux GOARCH=amd64 go build -o $PROJECT_NAME .
# 仅上传二进制文件
```

### Docker 项目

```bash
# 安装 Docker（如未安装）
ssh $SSH_TARGET "curl -fsSL https://get.docker.com | sh && systemctl enable docker && systemctl start docker"
```

### Nginx（有域名时必装）

```bash
ssh $SSH_TARGET "apt-get install -y nginx && systemctl enable nginx && systemctl start nginx"
```

---

## 第四步：上传项目

### 4a. 排除项（按项目类型）

| 项目类型 | 排除目录/文件 |
|---------|-------------|
| Node.js | `node_modules/`, `.next/`, `dist/`, `.git/` |
| Python | `__pycache__/`, `.venv/`, `venv/`, `*.pyc`, `.git/` |
| Rust | `target/`, `.git/`（方案 B 仅上传 `target/release/$BINARY`） |
| Go | `vendor/`（如有）, `.git/`（方案 B 仅上传二进制） |
| Docker | `.git/`（需要上传 Dockerfile） |
| 静态站 | `.git/`, `node_modules/` |

### 4b. rsync 上传

**注意**：大文件传输时 SSH 可能断连。使用保活参数：

```bash
rsync -avz --timeout=300 \
  -e "ssh -o ServerAliveInterval=30 -o ServerAliveCountMax=10" \
  --exclude='.git' --exclude='<TYPE_SPECIFIC_EXCLUDES>' \
  $PROJECT_DIR/ $SSH_TARGET:$REMOTE_DIR/
```

**如果文件很大（>500MB）**：先上传代码，再单独上传大文件。

**如果 SSH 频繁断连**：调整服务器 SSH 配置：
```bash
ssh $SSH_TARGET "sed -i 's/#ClientAliveInterval.*/ClientAliveInterval 60/' /etc/ssh/sshd_config && sed -i 's/#ClientAliveCountMax.*/ClientAliveCountMax 120/' /etc/ssh/sshd_config && systemctl reload ssh || systemctl reload sshd"
```

### 4c. 安装依赖 + 构建

**用 nohup 后台执行**，防止断连中断：

| 项目类型 | 命令 |
|---------|------|
| Node.js | `nohup bash -c 'npm install && npm run build' > /tmp/build.log 2>&1 &` |
| Python | `nohup bash -c 'python3 -m venv .venv && .venv/bin/pip install -r requirements.txt' > /tmp/build.log 2>&1 &` |
| Rust (方案A) | `nohup bash -c 'source ~/.cargo/env && cargo build --release' > /tmp/build.log 2>&1 &` |
| Go (方案A) | `nohup bash -c 'go build -o $PROJECT_NAME .' > /tmp/build.log 2>&1 &` |
| Docker | `nohup bash -c 'docker compose build' > /tmp/build.log 2>&1 &` |
| 静态站 | 无需构建 |

等待后查看构建结果：`ssh $SSH_TARGET "tail -20 /tmp/build.log"`

---

## 第五步：启动应用与进程管理

根据项目类型选择对应的进程管理方案。

### Node.js → PM2

```bash
ssh $SSH_TARGET "cd $REMOTE_DIR && pm2 start npm --name $PROJECT_NAME -- start && pm2 startup && pm2 save"
```

验证：`ssh $SSH_TARGET "pm2 list && curl -s -o /dev/null -w '%{http_code}' http://localhost:$PORT"`

### Python → systemd

```bash
ssh $SSH_TARGET "cat > /etc/systemd/system/$PROJECT_NAME.service << EOF
[Unit]
Description=$PROJECT_NAME
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$REMOTE_DIR
ExecStart=$REMOTE_DIR/.venv/bin/python -m uvicorn main:app --host 0.0.0.0 --port $PORT
# 或 gunicorn: ExecStart=$REMOTE_DIR/.venv/bin/gunicorn -w 4 -b 0.0.0.0:$PORT main:app
Restart=on-failure
RestartSec=5
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
EOF
systemctl daemon-reload && systemctl enable $PROJECT_NAME && systemctl start $PROJECT_NAME"
```

> **注意**：ExecStart 根据框架调整：
> - FastAPI/Starlette: `uvicorn main:app`
> - Flask: `gunicorn -w 4 main:app`
> - Django: `gunicorn -w 4 project.wsgi:application`
> - 纯脚本: `python main.py`

验证：`ssh $SSH_TARGET "systemctl status $PROJECT_NAME && curl -s -o /dev/null -w '%{http_code}' http://localhost:$PORT"`

### Rust / Go → systemd

```bash
ssh $SSH_TARGET "cat > /etc/systemd/system/$PROJECT_NAME.service << EOF
[Unit]
Description=$PROJECT_NAME
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$REMOTE_DIR
ExecStart=$REMOTE_DIR/$BINARY_NAME
Restart=on-failure
RestartSec=5
Environment=PORT=$PORT

[Install]
WantedBy=multi-user.target
EOF
systemctl daemon-reload && systemctl enable $PROJECT_NAME && systemctl start $PROJECT_NAME"
```

> Rust 二进制路径：`$REMOTE_DIR/target/release/$PROJECT_NAME`（方案 A）或 `$REMOTE_DIR/$PROJECT_NAME`（方案 B）
> Go 二进制路径：`$REMOTE_DIR/$PROJECT_NAME`

验证：`ssh $SSH_TARGET "systemctl status $PROJECT_NAME && curl -s -o /dev/null -w '%{http_code}' http://localhost:$PORT"`

### Docker → docker compose

```bash
ssh $SSH_TARGET "cd $REMOTE_DIR && docker compose up -d"
```

配置开机自启：Docker 服务默认随 systemd 启动，docker compose 使用 `restart: unless-stopped` 即可。

验证：`ssh $SSH_TARGET "docker compose ps && curl -s -o /dev/null -w '%{http_code}' http://localhost:$PORT"`

### 静态站 → Nginx 直接托管

无需进程管理，Nginx 直接指向静态文件目录（见第六步）。

---

## 第六步：Nginx 反向代理

> 如果用户选择"仅用 IP 访问"，跳过此步和后续 SSL 步骤。

### 6a. 动态应用（HTTP 反向代理）

```bash
ssh $SSH_TARGET "cat > /etc/nginx/sites-available/$PROJECT_NAME << 'NGINX'
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;

    client_max_body_size 50M;

    location / {
        proxy_pass http://127.0.0.1:$PORT;
        proxy_http_version 1.1;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection \"upgrade\";
    }
}
NGINX
ln -sf /etc/nginx/sites-available/$PROJECT_NAME /etc/nginx/sites-enabled/$PROJECT_NAME
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl reload nginx"
```

### 6b. 静态站（直接托管）

```bash
ssh $SSH_TARGET "cat > /etc/nginx/sites-available/$PROJECT_NAME << 'NGINX'
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;

    root $REMOTE_DIR;
    index index.html;

    location / {
        try_files \$uri \$uri/ /index.html;
    }

    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2)$ {
        expires 30d;
        add_header Cache-Control \"public, immutable\";
    }
}
NGINX
ln -sf /etc/nginx/sites-available/$PROJECT_NAME /etc/nginx/sites-enabled/$PROJECT_NAME
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl reload nginx"
```

### 6c. HTTPS 版本（有 SSL 证书时）

在对应的 server 块基础上：
- 80 端口 server 加 `return 301 https://$host$request_uri;`
- 新增 443 端口 server 块，加 ssl_certificate 和安全头

```nginx
server {
    listen 443 ssl;
    server_name $DOMAIN www.$DOMAIN;

    ssl_certificate /etc/ssl/cloudflare/fullchain.pem;
    ssl_certificate_key /etc/ssl/cloudflare/key.pem;

    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    # ... location 块同上 ...
}
```

### 6d. Nginx 安全加固

```bash
ssh $SSH_TARGET "sed -i 's/# server_tokens off;/server_tokens off;/' /etc/nginx/nginx.conf && nginx -t && systemctl reload nginx"
```

---

## 第七步：DNS 与 SSL 配置

> 仅当用户有域名时执行。

### 7a. DNS 配置指引

告知用户在域名注册商后台添加 DNS 记录：

| 记录类型 | 名称 | 内容 |
|---------|------|------|
| A | `@` | `<服务器IP>` |
| A | `www` | `<服务器IP>` |

如果使用 Cloudflare，建议开启橙色云朵（代理模式）。

### 7b. SSL 方案选择

用 AskUserQuestion 询问：

1. **Cloudflare Origin Certificate（推荐）** — DNS 托管在 Cloudflare，证书有效期 15 年
2. **Let's Encrypt** — 免费公共证书，需定期续期
3. **暂不配置 SSL**

#### Cloudflare Origin Certificate 流程：

1. 告知用户操作：Cloudflare → **SSL/TLS** → **源服务器** → **创建证书**
   - 主机名确保包含 `$DOMAIN` 和 `*.$DOMAIN`
   - 私钥类型：RSA，有效期：15 年

2. 用户提供证书和私钥后，写入服务器并拼接证书链：

```bash
ssh $SSH_TARGET "mkdir -p /etc/ssl/cloudflare"
# 写入 cert.pem 和 key.pem（chmod 600）
# 下载 Origin CA 根证书并拼接
ssh $SSH_TARGET "curl -s -o /etc/ssl/cloudflare/origin-ca-rsa-root.pem https://developers.cloudflare.com/ssl/static/origin_ca_rsa_root.pem && cat /etc/ssl/cloudflare/cert.pem /etc/ssl/cloudflare/origin-ca-rsa-root.pem > /etc/ssl/cloudflare/fullchain.pem"
```

3. **必须验证证书**：
```bash
ssh $SSH_TARGET "openssl x509 -in /etc/ssl/cloudflare/cert.pem -noout -text | grep -E 'DNS:|Subject:|Issuer:|Extended'"
```
- `DNS:` 包含域名
- `Extended Key Usage` 包含 `TLS Web Server Authentication`
- 如果缺少，告知用户重新创建

4. Cloudflare SSL 模式：先设 **Full (Strict)**，如果 526 错误则降级为 **Full**

#### Let's Encrypt 流程：

```bash
ssh $SSH_TARGET "apt-get install -y certbot python3-certbot-nginx && certbot --nginx -d $DOMAIN -d www.$DOMAIN --non-interactive --agree-tos --email <EMAIL>"
```

> 需要临时关闭 Cloudflare 代理（橙色→灰色），完成后可重新开启。

---


## Extended Reference

Detailed material starting at `## 第八步：安全加固` has been moved to [`reference/extended.md`](reference/extended.md) to keep this skill concise. Load that reference when the task requires the moved examples, command catalogs, checklists, platform details, or implementation templates.
