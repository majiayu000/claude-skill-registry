---
name: vivian-memory
description: Aiden的个人记忆API。支持向量语义搜索、混合权重模型、多种返回格式。省token模式用format=compact。
---

# Memory API Skill

Aiden 的个人记忆基础设施。任何 AI 都可以调用，但必须遵守协议。

**API代码位置**: `skills/vivian-memory/api/`

## Endpoint

```
https://memory-api.vivian-memory.workers.dev
```

## 认证

```
Authorization: Bearer my-memory-secret-123
```

---

## API 接口

### 1. 检索记忆

```bash
curl -s ".../memory/search?q=<query>&limit=5&format=compact" -H "Authorization: Bearer ..."
```

| 参数 | 默认 | 说明 |
|------|------|------|
| q | 必填 | 自然语言查询 |
| limit | 5 | 返回数量，最大20 |
| type | all | all/personal/assistant/project |
| format | full | text/compact/full（见下方） |

**format 参数（省token）：**
| 值 | 说明 |
|----|------|
| text | 纯文本，---分隔，最省token |
| compact | 只有text+score |
| full | 全部字段+_debug |

**推荐日常用 format=compact**

### 2. 写入记忆

```bash
curl -s -X POST ".../memory" -H "Auth..." -d '{"items": [{"text": "内容", "weight": 0.8}]}'
```

| 字段 | 默认 | 说明 |
|------|------|------|
| text | 必填 | 原子化（一条一个事实） |
| weight | 1.0 | 0.3-1.0 |
| tags | [] | bio/pref/tech/work/goal |
| type | personal | personal/assistant/project |

批量最多20条/请求。

### 3. 删除/统计

```bash
curl -s -X DELETE ".../memory/{id}" -H "Auth..."
curl -s ".../memory/stats" -H "Auth..."
```

### 4. 可视化（公开）

```
https://memory-api.vivian-memory.workers.dev/viz
```

---

## 混合权重模型

```
final_score = similarity × (0.5×base + 0.3×recency + 0.2×frequency)
```

| 因子 | 说明 |
|------|------|
| base | 写入时的weight |
| recency | 1/(1+days/30)，越近越高 |
| frequency | log(count+1)/log(10)，召回越多越重要 |

用 format=full 看 _debug 字段调试。

---

## 批量脚本

位置: `scripts/utils/memory-batch.sh`

```bash
./memory-batch.sh add "内容" 0.8 "tag"  # 暂存
./memory-batch.sh list                   # 查看
./memory-batch.sh flush                  # 批量上传
./memory-batch.sh import file.txt        # 导入
```

---

## 写入协议

✅ 写入：新事实、状态变化、明确说"记住"的内容
❌ 不写：废话、重复、临时细节

**原子化**：一条 = 一个事实
**权重**：1.0核心 / 0.8长期 / 0.5临时 / 0.3琐碎

**冲突处理**：search找旧的 → delete → 写新的

---

## 检索后行为

- 自然使用，不说"根据记忆"
- score<0.3 可能不相关
- 不要复述检索内容

---

## 省Token

1. 用 format=compact
2. 批量写入
3. 限制limit
4. 避免重复检索
