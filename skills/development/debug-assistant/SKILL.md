---
name: debug-assistant
description: 调试辅助工具。快速诊断后端、前端和数据库问题。适用于 API 失败、日志分析、服务健康检查等场景。
allowed-tools:
  - Bash
  - Read
  - Grep
  - Glob
---

# 调试辅助 Skill

## 服务架构

| 服务 | 端口 | 日志位置 | 健康检查 |
|------|------|----------|----------|
| Cretas Backend | 10010 | `/www/wwwroot/cretas/cretas-backend.log` | `/api/mobile/health` |
| AI Service | 8085 | `/www/wwwroot/cretas/ai-service/ai-service.log` | `/health` |
| Mall Backend | 7500 | `/www/wwwroot/mall-admin/mall-admin.log` | `/actuator/health` |
| React Native | 3010 | Metro bundler 控制台 | N/A |

## 快速诊断命令

### 服务状态检查

```bash
# 检查端口
nc -zv 139.196.165.140 10010

# 健康检查
curl -s http://139.196.165.140:10010/api/mobile/health
curl -s http://139.196.165.140:8085/health
curl -s http://139.196.165.140:7500/actuator/health
```

### 查看日志

```bash
# Cretas 后端日志
ssh root@139.196.165.140 "tail -100 /www/wwwroot/cretas/cretas-backend.log"

# 过滤 ERROR
ssh root@139.196.165.140 "tail -500 /www/wwwroot/cretas/cretas-backend.log | grep -A5 'ERROR'"

# AI 服务日志
ssh root@139.196.165.140 "tail -100 /www/wwwroot/cretas/ai-service/ai-service.log"
```

### 数据库检查

```bash
ssh root@139.196.165.140 "mysql -u root -p cretas_db -e 'SELECT 1'"
```

## 常见错误速查

| 错误 | 检查命令 | 常见原因 |
|------|----------|----------|
| 500 Error | `grep ERROR backend.log` | Entity字段缺失、NPE、JSON错误 |
| 401 Unauthorized | `echo TOKEN \| cut -d'.' -f2 \| base64 -d` | Token过期/格式错误/权限不足 |
| 网络失败 | `nc -zv 139.196.165.140 10010` | 端口未开放/防火墙 |
| RN 白屏 | `npx expo start --clear` | Metro 编译错误 |

## JWT Token 调试

```bash
# 解码 JWT payload
echo "YOUR_TOKEN" | cut -d'.' -f2 | base64 -d 2>/dev/null | jq
```

## React Native 调试

```bash
cd frontend/CretasFoodTrace
npx expo start --clear          # 清除缓存启动
npx expo doctor                 # 检查环境
```

## 参考文档

- `references/common-errors.md` - 完整错误速查表
