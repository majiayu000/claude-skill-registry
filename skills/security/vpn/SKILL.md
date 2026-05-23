---
name: vpn
description: VPN 配置与管理
version: 1.0.0
author: terminal-skills
tags: [networking, vpn, openvpn, wireguard, ipsec]
---

# VPN 配置与管理

## 概述
OpenVPN、WireGuard、IPSec VPN 配置与管理技能。

## WireGuard

### 安装
```bash
# Debian/Ubuntu
apt install wireguard

# CentOS/RHEL
yum install epel-release elrepo-release
yum install kmod-wireguard wireguard-tools

# 验证安装
wg --version
```

### 生成密钥
```bash
# 生成私钥
wg genkey > privatekey

# 从私钥生成公钥
wg pubkey < privatekey > publickey

# 一步生成
wg genkey | tee privatekey | wg pubkey > publickey

# 生成预共享密钥（可选，增强安全）
wg genpsk > presharedkey
```

### 服务端配置
```bash
# /etc/wireguard/wg0.conf
[Interface]
Address = 10.0.0.1/24
ListenPort = 51820
PrivateKey = <server_private_key>

# 启用 IP 转发
PostUp = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
PostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE

[Peer]
PublicKey = <client_public_key>
AllowedIPs = 10.0.0.2/32
```

### 客户端配置
```bash
# /etc/wireguard/wg0.conf
[Interface]
Address = 10.0.0.2/24
PrivateKey = <client_private_key>
DNS = 8.8.8.8

[Peer]
PublicKey = <server_public_key>
Endpoint = server.example.com:51820
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25
```

### 管理命令
```bash
# 启动
wg-quick up wg0
systemctl start wg-quick@wg0

# 停止
wg-quick down wg0
systemctl stop wg-quick@wg0

# 开机启动
systemctl enable wg-quick@wg0

# 查看状态
wg show
wg show wg0

# 添加 peer
wg set wg0 peer <public_key> allowed-ips 10.0.0.3/32
```

## OpenVPN

### 安装
```bash
# Debian/Ubuntu
apt install openvpn easy-rsa

# CentOS/RHEL
yum install epel-release
yum install openvpn easy-rsa
```

### 初始化 PKI
```bash
# 创建 CA 目录
make-cadir ~/openvpn-ca
cd ~/openvpn-ca

# 初始化 PKI
./easyrsa init-pki

# 创建 CA
./easyrsa build-ca nopass

# 生成服务器证书
./easyrsa gen-req server nopass
./easyrsa sign-req server server

# 生成 DH 参数
./easyrsa gen-dh

# 生成 TLS 密钥
openvpn --genkey secret ta.key

# 生成客户端证书
./easyrsa gen-req client1 nopass
./easyrsa sign-req client client1
```

### 服务端配置
```bash
# /etc/openvpn/server.conf
port 1194
proto udp
dev tun

ca ca.crt
cert server.crt
key server.key
dh dh.pem
tls-auth ta.key 0

server 10.8.0.0 255.255.255.0
ifconfig-pool-persist ipp.txt

push "redirect-gateway def1 bypass-dhcp"
push "dhcp-option DNS 8.8.8.8"
push "dhcp-option DNS 8.8.4.4"

keepalive 10 120
cipher AES-256-GCM
auth SHA256

user nobody
group nogroup
persist-key
persist-tun

status /var/log/openvpn-status.log
log-append /var/log/openvpn.log
verb 3
```

### 客户端配置
```bash
# client.ovpn
client
dev tun
proto udp
remote server.example.com 1194
resolv-retry infinite
nobind

persist-key
persist-tun

ca ca.crt
cert client1.crt
key client1.key
tls-auth ta.key 1

cipher AES-256-GCM
auth SHA256
verb 3
```

### 管理命令
```bash
# 启动服务
systemctl start openvpn@server
systemctl enable openvpn@server

# 查看状态
systemctl status openvpn@server

# 查看连接
cat /var/log/openvpn-status.log

# 吊销证书
cd ~/openvpn-ca
./easyrsa revoke client1
./easyrsa gen-crl
```

## IPSec (strongSwan)

### 安装
```bash
# Debian/Ubuntu
apt install strongswan strongswan-pki

# CentOS/RHEL
yum install strongswan
```

### 生成证书
```bash
# 生成 CA
ipsec pki --gen --type rsa --size 4096 --outform pem > ca-key.pem
ipsec pki --self --ca --lifetime 3650 \
    --in ca-key.pem --type rsa \
    --dn "CN=VPN CA" \
    --outform pem > ca-cert.pem

# 生成服务器证书
ipsec pki --gen --type rsa --size 4096 --outform pem > server-key.pem
ipsec pki --pub --in server-key.pem --type rsa | \
    ipsec pki --issue --lifetime 1825 \
    --cacert ca-cert.pem --cakey ca-key.pem \
    --dn "CN=vpn.example.com" \
    --san vpn.example.com \
    --flag serverAuth --flag ikeIntermediate \
    --outform pem > server-cert.pem
```

### 服务端配置
```bash
# /etc/ipsec.conf
config setup
    charondebug="ike 2, knl 2, cfg 2"
    uniqueids=no

conn ikev2-vpn
    auto=add
    compress=no
    type=tunnel
    keyexchange=ikev2
    fragmentation=yes
    forceencaps=yes
    
    dpdaction=clear
    dpddelay=300s
    rekey=no
    
    left=%any
    leftid=@vpn.example.com
    leftcert=server-cert.pem
    leftsendcert=always
    leftsubnet=0.0.0.0/0
    
    right=%any
    rightid=%any
    rightauth=eap-mschapv2
    rightsourceip=10.10.10.0/24
    rightdns=8.8.8.8,8.8.4.4
    rightsendcert=never
    
    eap_identity=%identity
```

### 用户配置
```bash
# /etc/ipsec.secrets
: RSA "server-key.pem"
user1 : EAP "password1"
user2 : EAP "password2"
```

### 管理命令
```bash
# 启动
systemctl start strongswan
systemctl enable strongswan

# 重载配置
ipsec reload
ipsec rereadall

# 查看状态
ipsec statusall
ipsec status

# 查看 SA
ipsec listall
```

## 常见场景

### 场景 1：WireGuard 站点到站点
```bash
# 站点 A 配置
[Interface]
Address = 10.0.0.1/24
PrivateKey = <site_a_private>
ListenPort = 51820

[Peer]
PublicKey = <site_b_public>
Endpoint = site-b.example.com:51820
AllowedIPs = 10.0.0.2/32, 192.168.2.0/24

# 站点 B 配置
[Interface]
Address = 10.0.0.2/24
PrivateKey = <site_b_private>
ListenPort = 51820

[Peer]
PublicKey = <site_a_public>
Endpoint = site-a.example.com:51820
AllowedIPs = 10.0.0.1/32, 192.168.1.0/24
```

### 场景 2：分流配置
```bash
# WireGuard 仅代理特定网段
[Peer]
PublicKey = <server_public_key>
Endpoint = server.example.com:51820
AllowedIPs = 10.0.0.0/24, 192.168.100.0/24
```

### 场景 3：多用户管理脚本
```bash
#!/bin/bash
# add-wg-client.sh
CLIENT_NAME=$1
SERVER_PUBLIC_KEY="<server_public_key>"
SERVER_ENDPOINT="vpn.example.com:51820"

# 生成密钥
wg genkey | tee ${CLIENT_NAME}_private | wg pubkey > ${CLIENT_NAME}_public

# 生成客户端配置
cat > ${CLIENT_NAME}.conf << EOF
[Interface]
PrivateKey = $(cat ${CLIENT_NAME}_private)
Address = 10.0.0.${2}/24
DNS = 8.8.8.8

[Peer]
PublicKey = ${SERVER_PUBLIC_KEY}
Endpoint = ${SERVER_ENDPOINT}
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25
EOF

echo "添加到服务器："
echo "[Peer]"
echo "PublicKey = $(cat ${CLIENT_NAME}_public)"
echo "AllowedIPs = 10.0.0.${2}/32"
```

## 故障排查

| 问题 | 排查方法 |
|------|----------|
| 连接失败 | 检查防火墙、端口、密钥配置 |
| 握手失败 | 检查公钥配置、时间同步 |
| 无法访问内网 | 检查 AllowedIPs、路由、IP 转发 |
| 性能差 | 检查 MTU、加密算法 |

```bash
# WireGuard 调试
wg show
dmesg | grep wireguard
tcpdump -i any port 51820

# OpenVPN 调试
tail -f /var/log/openvpn.log
tcpdump -i any port 1194

# IPSec 调试
ipsec statusall
journalctl -u strongswan -f

# 检查 IP 转发
cat /proc/sys/net/ipv4/ip_forward
sysctl net.ipv4.ip_forward=1
```
