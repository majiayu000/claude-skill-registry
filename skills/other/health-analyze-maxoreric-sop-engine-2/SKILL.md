# health-analyze

**用途**: 分析健康数据，计算健康评分

**输入**:
```yaml
date: string
data:
  temperature: number
  heart_rate: number
  steps: number
```

**输出**:
```yaml
status: string          # 状态：analyzed
health_score: number    # 健康评分 (0-100)
analysis:
  temperature_ok: boolean
  heart_rate_ok: boolean
  steps_ok: boolean
  issues: array         # 问题列表
timestamp: string
```

## 评分规则

总分 100 分，分为三个维度：

1. **体温评分** (30 分)
   - 36.0 - 37.5°C: 30 分
   - 其他: 0 分

2. **心率评分** (30 分)
   - 60 - 100 bpm: 30 分
   - 其他: 0 分

3. **步数评分** (40 分)
   - ≥ 10000: 40 分
   - ≥ 5000: 30 分
   - < 5000: 0 分

## 健康等级

- **优秀**: 80-100 分
- **良好**: 60-79 分
- **需改善**: 0-59 分
