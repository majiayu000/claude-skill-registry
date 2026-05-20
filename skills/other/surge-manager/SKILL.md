---
name: surge-manager
description: "Surge 配置管理技能，支持规则添加、配置编辑、Tailscale 设备管理等操作"
---

# Surge Manager Skill

用于管理 Surge 配置文件，支持规则添加、配置编辑、Tailscale 设备直连配置等操作。

## 配置文件路径

默认 Surge 配置文件路径：
```
~/Library/Application Support/Surge/Profiles/cc.conf
```

## 主要功能

### 1. 添加直连规则

为指定的 IP 地址或域名添加直连规则。

**使用场景**：
- Tailscale 设备直连
- 内网服务直连
- 特定域名直连

**规则类型**：
- `IP-CIDR`: IP 网段直连
- `DOMAIN`: 域名直连
- `DOMAIN-SUFFIX`: 域名后缀直连

### 2. 管理 bypass-tun

管理 TUN 模式下的直连网段列表。

**使用场景**：
- 添加内网网段直连
- 添加 VPN 网段直连
- 添加 Tailscale 网段直连

### 3. 添加 Tailscale 设备

自动为 Tailscale 设备添加直连规则（IP + 域名）。

**Tailscale 网段**：`100.64.0.0/10`
**域名格式**：`设备名.ts.net`

## 使用示例

### 添加单个设备直连

```bash
# 添加 IP 直连
IP-CIDR,100.89.35.126/32,🎯 全球直连,no-resolve

# 添加域名直连
DOMAIN,mbp.ts.net,🎯 全球直连
```

### 添加 Tailscale 网段

```bash
# 在 bypass-tun 中添加
bypass-tun = 192.168.0.0/16,10.0.0.0/8,172.16.0.0/12,100.64.0.0/10

# 在规则中添加
IP-CIDR,100.64.0.0/10,🎯 全球直连,no-resolve
DOMAIN-SUFFIX,ts.net,🎯 全球直连
```

### 批量添加 Tailscale 设备

为所有 Tailscale 设备添加单独规则：

```bash
# 从 tailscale status 获取设备列表后自动生成规则
IP-CIDR,100.89.35.126/32,🎯 全球直连,no-resolve
DOMAIN,mbp.ts.net,🎯 全球直连
IP-CIDR,100.107.176.21/32,🎯 全球直连,no-resolve
DOMAIN,tserver.ts.net,🎯 全球直连
# ... 更多设备
```

## 配置结构

### [General] 部分

```ini
bypass-tun = 192.168.0.0/16,10.0.0.0/8,172.16.0.0/12,100.64.0.0/10
```

### [Rule] 部分

```ini
[Rule]
# Tailscale 直连规则
IP-CIDR,100.64.0.0/10,🎯 全球直连,no-resolve
DOMAIN-SUFFIX,ts.net,🎯 全球直连
# 设备单独规则
IP-CIDR,100.89.35.126/32,🎯 全球直连,no-resolve
DOMAIN,mbp.ts.net,🎯 全球直连
# ... 其他规则
RULE-SET,https://raw.githubusercontent.com/...
```

## 常见操作

### 查看当前配置

```bash
cat ~/Library/Application\ Support/Surge/Profiles/cc.conf
```

### 备份配置

```bash
cp ~/Library/Application\ Support/Surge/Profiles/cc.conf ~/Library/Application\ Support/Surge/Profiles/cc.conf.backup
```

### 重新加载配置

修改配置后，需要在 Surge 中重新加载配置使规则生效。

## Tailscale 设备管理

### 获取设备列表

```bash
tailscale status
```

### 设备信息格式

```
100.89.35.126   mbp              Dwsy@  macOS    -
100.107.176.21  tserver          Dwsy@  linux    active; direct 118.24.74.226:41641
```

格式：`IP地址 设备名 用户名 操作系统 状态`

### 自动生成规则

从 `tailscale status` 输出自动生成直连规则：

```bash
# 第一列：IP 地址
# 第二列：设备名
# 域名：设备名.ts.net
```

## 注意事项

1. **规则优先级**：
   - 具体规则（IP-CIDR /32、DOMAIN）优先于网段规则
   - 规则顺序很重要，越靠前优先级越高

2. **no-resolve 参数**：
   - IP 规则建议添加 `no-resolve` 避免不必要的 DNS 查询

3. **配置备份**：
   - 修改前建议先备份配置文件

4. **重新加载**：
   - 修改后需要在 Surge 中重新加载配置

5. **Tailscale 网段**：
   - Tailscale 使用 CGNAT 网段 `100.64.0.0/10`
   - 域名统一使用 `.ts.net` 后缀

## 扩展功能

### 添加代理规则

```ini
IP-CIDR,192.168.1.0/24,🚀 节点选择,no-resolve
DOMAIN,example.com,🚀 节点选择
```

### 添加拦截规则

```ini
DOMAIN,ads.example.com,🛑 广告拦截
DOMAIN-SUFFIX,tracker.com,🍃 应用净化
```

### 添加分流规则

```ini
DOMAIN-SUFFIX,youtube.com,📹 油管视频
DOMAIN-SUFFIX,netflix.com,🎥 奈飞视频
```

## 故障排查

### 规则不生效

1. 检查规则顺序是否正确
2. 确认是否重新加载了配置
3. 使用 Surge 的规则测试功能验证

### IP 无法直连

1. 确认 IP 在 bypass-tun 列表中
2. 检查是否有冲突的规则
3. 使用 ping 测试网络连通性

### 域名无法直连

1. 确认 DNS 解析正确
2. 检查域名规则拼写
3. 尝试使用 IP 规则替代

## 相关链接

- Surge 官方文档：https://manual.nssurge.com/
- Tailscale 官网：https://tailscale.com/