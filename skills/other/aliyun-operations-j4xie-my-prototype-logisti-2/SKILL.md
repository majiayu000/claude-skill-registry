---
name: aliyun-operations
description: 阿里云服务器运维操作。包括ECS实例管理、安全组配置、服务部署、日志查看。适用于服务器管理、端口开放、应用部署等任务。
allowed-tools:
  - Bash
  - Read
  - Write
  - Grep
  - Glob
---

# 阿里云运维操作 Skill

## 凭证配置

使用环境变量（参见 CREDENTIAL-MANAGEMENT.md）：

| 配置项 | 环境变量 |
|--------|----------|
| **AccessKey ID** | `${ALIBABA_ACCESSKEY_ID}` |
| **AccessKey Secret** | `${ALIBABA_SECRET_KEY}` |
| **Region** | `cn-shanghai` |

## 服务器信息

| 项目 | 值 |
|------|-----|
| **ECS 公网 IP** | `139.196.165.140` |
| **SSH 用户** | `root` |
| **宝塔面板** | `https://139.196.165.140:16435/a96c4c2e` |

## 服务端口

| 服务 | 端口 | 路径 |
|------|------|------|
| Cretas 后端 | 10010 | `/www/wwwroot/cretas/` |
| MallCenter 后端 | 7500 | `/www/wwwroot/mall-admin/` |
| Python AI | 8085 | `/www/wwwroot/cretas/ai-service/` |
| MySQL | 3306 | - |
| Redis | 6379 | - |

## 常用运维命令

| 操作 | 命令 |
|------|------|
| SSH 连接 | `ssh root@139.196.165.140` |
| 查看进程 | `ssh root@139.196.165.140 "ps aux \| grep java"` |
| 查看端口 | `ssh root@139.196.165.140 "netstat -tlnp \| grep 10010"` |
| Cretas 日志 | `ssh root@139.196.165.140 "tail -100 /www/wwwroot/cretas/cretas-backend.log"` |
| MallCenter 日志 | `ssh root@139.196.165.140 "tail -100 /www/wwwroot/mall-admin/mall-admin.log"` |

## 部署操作

### Cretas 后端 (端口 10010)

```bash
cd /Users/jietaoxie/my-prototype-logistics/backend-java
JAVA_HOME=/Library/Java/JavaVirtualMachines/jdk-17.jdk/Contents/Home mvn clean package -DskipTests
scp target/cretas-backend-system-1.0.0.jar root@139.196.165.140:/www/wwwroot/cretas/
ssh root@139.196.165.140 "bash /www/wwwroot/cretas/restart.sh"
curl -s http://139.196.165.140:10010/api/mobile/health
```

### Python AI 服务 (端口 8085)

```bash
cd /Users/jietaoxie/my-prototype-logistics/backend-java/backend-ai-chat
rsync -avz --exclude 'venv' --exclude '__pycache__' scripts/ root@139.196.165.140:/www/wwwroot/cretas/ai-service/
ssh root@139.196.165.140 "cd /www/wwwroot/cretas/ai-service && bash restart-ai.sh"
curl -s http://139.196.165.140:8085/health
```

### MallCenter 后端 (端口 7500)

```bash
cd /Users/jietaoxie/my-prototype-logistics/MallCenter/mall_admin_center
JAVA_HOME=/Library/Java/JavaVirtualMachines/jdk-17.jdk/Contents/Home mvn clean package -DskipTests -pl logistics-admin -am
scp logistics-admin/target/logistics-admin.jar root@139.196.165.140:/www/wwwroot/mall-admin/
ssh root@139.196.165.140 "bash /www/wwwroot/mall-admin/restart.sh"
```

## 阿里云 CLI

```bash
# 查看安全组
aliyun ecs DescribeSecurityGroups --RegionId cn-shanghai

# 开放端口
aliyun ecs AuthorizeSecurityGroup --RegionId cn-shanghai \
  --SecurityGroupId <sg-id> --IpProtocol tcp --PortRange 8083/8083 --SourceCidrIp 0.0.0.0/0
```

## 健康检查

```bash
curl -s http://139.196.165.140:10010/api/mobile/health   # Cretas
curl -s http://139.196.165.140:7500/actuator/health      # MallCenter
curl -s http://139.196.165.140:8085/health               # AI Service
```
