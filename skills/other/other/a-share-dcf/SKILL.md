---
name: a-share-dcf
description: "A\u80A1DCF\u4F30\u503C\u6A21\u578B/\u73B0\u91D1\u6D41\u6298\u73B0\u3002\u5F53\u7528\u6237\u8BF4\u201CDCF\u201D\u3001\u201C\u73B0\u91D1\u6D41\u6298\u73B0\u201D\u3001\u201CDCF\u4F30\u503C\u201D\u3001\u201C\u5185\u5728\u4EF7\u503C\u201D\u3001\u201Cintrinsic value\u201D\u3001\u201C\u5E2E\u6211\u7B97\u4E00\u4E0BXX\u503C\u591A\u5C11\u94B1\u201D\u3001\u201C\u5408\u7406\u4F30\u503C\u201D\u3001\u201C\u76EE\u6807\u4EF7\u63A8\u5BFC\u201D\u65F6\u89E6\u53D1\u3002\u57FA\u4E8E cn-stock-data \u83B7\u53D6\u5386\u53F2\u8D22\u52A1\u6570\u636E\uFF0C\u6784\u5EFA\u81EA\u7531\u73B0\u91D1\u6D41\u6298\u73B0\u6A21\u578B\uFF08FCFF\uFF09\uFF0C\u8BA1\u7B97 WACC\uFF0C\u8F93\u51FA\u542B\u654F\u611F\u6027\u5206\u6790\u7684\u4F30\u503C Excel\u3002\u652F\u6301\u673A\u6784 DCF \u62A5\u544A\u98CE\u683C\uFF08formal\uFF09\u548C\u4E2A\u4EBA\u4F30\u503C\u7B14\u8BB0\u98CE\u683C\uFF08brief\uFF09\u3002\u4E0D\u9002\u7528\u4E8E\u53EF\u6BD4\u516C\u53F8\u4F30\u503C\u6CD5\uFF08\u7528 a-share-comps\uFF09\u6216\u8D22\u62A5\u5206\u6790\uFF08\u7528 a-share-earnings-analysis\uFF09\u3002"
---

## 数据源

```bash
SCRIPTS="$SKILLS_ROOT/cn-stock-data/scripts"

# 历史财务指标（收入/利润/折旧/资本开支/营运资金等）
python "$SCRIPTS/cn_stock_data.py" finance --code [CODE]

# 最新行情（市值、股价，用于 WACC 和对比）
python "$SCRIPTS/cn_stock_data.py" quote --code [CODE]

# 行业可比公司行情（用于 Beta/WACC 参考）
python "$SCRIPTS/cn_stock_data.py" quote --code [COMP1],[COMP2],[COMP3]
```

补充：通过 web 搜索获取：
- 无风险利率（10 年期国债收益率）
- 行业 Beta 参考值
- 公司债务成本（如有公开债券）
- 分析师收入/利润预测（用于交叉验证）

## Workflow

### Step 1: 数据收集

1. 通过 cn-stock-data finance 获取过去 3-5 年财务数据
2. 通过 cn-stock-data quote 获取当前市值
3. Web 搜索：10 年期国债收益率、公司有息负债利率

### Step 2: 历史分析

分析过去 3-5 年的关键财务趋势：
- 收入增速趋势
- EBIT/EBITDA 利润率趋势
- 资本开支/收入 比率
- 营运资金/收入 比率
- 折旧摊销/收入 比率
- 有效税率

### Step 3: 收入预测

- 基于历史趋势 + 行业增速 + web 搜索的分析师预期
- 预测期：通常 5 年（高增长公司可延长到 7-10 年）
- 构建 Base 情景，可选 Bull/Bear

### Step 4: 利润率与费用建模

- 毛利率预测（基于历史趋势 + 竞争格局判断）
- 运营费用率预测
- EBIT/EBITDA 推导
- 折旧摊销预测（基于历史比率或资本开支的固定比例）
- 资本开支预测
- 营运资金变动预测

### Step 5: 自由现金流(FCFF)计算

```
FCFF = EBIT × (1 - 税率) + 折旧摊销 - 资本开支 - 营运资金增加
```

### Step 6: WACC 计算

```
A 股 WACC 参数:
- 无风险利率 Rf: 10 年期国债收益率（web 搜索获取，通常 2.5%-3.5%）
- 市场风险溢价 ERP: A 股通常取 5%-7%（高于美股的 4%-6%，反映新兴市场溢价）
- Beta: 优先用 web 搜索获取；若不可用，取行业平均或根据公司特征估计
- 股权成本 Ke = Rf + Beta × ERP
- 债务成本 Kd: 公司实际借款利率或同类公司债利率
- 税率: A 股一般企业 25%，高新技术企业 15%
- WACC = Ke × (E/(E+D)) + Kd × (1-T) × (D/(E+D))
```

### Step 7: 终值(Terminal Value)计算

两种方法取平均或选其一：
- **永续增长法**: TV = FCFF_最后年 × (1+g) / (WACC - g)
  - A 股永续增长率 g 通常取 2%-3%（GDP 长期增速预期）
- **退出倍数法**: TV = EBITDA_最后年 × Exit Multiple
  - Exit Multiple 参考行业可比公司 EV/EBITDA 中位数

### Step 8: 估值汇总与敏感性分析

**估值桥**:
```
FCFF 现值之和
+ 终值现值
= 企业价值(EV)
- 净债务（有息负债 - 现金）
- 少数股东权益
= 股权价值
/ 总股本
= 每股价值
vs 当前股价 → 上行/下行空间(%)
```

**敏感性分析表**（必须）：
1. WACC vs 永续增长率 → 每股价值
2. 收入增速 vs EBIT 利润率 → 每股价值
3. 可选：Beta vs 无风险利率 → WACC

## 输出

### Excel 输出（formal 模式）

- Sheet 1 "DCF": 历史数据 → 预测数据 → FCFF → 折现 → 估值汇总 → 敏感性分析表
- Sheet 2 "WACC": 资本成本计算详细过程
- 格式规则：
  - 蓝色字体 = 输入假设
  - 黑色字体 = 公式计算
  - 所有派生值必须是 Excel 公式
  - 敏感性分析表每个单元格是完整公式（非线性插值）
  - 基准情景（中心格）用蓝色底色 + 粗体标注

### Markdown 输出（brief 模式）

- 直接输出 Markdown 表格
- 包含：关键假设 → FCFF 预测表 → 估值结果 → 简化敏感性分析
- 在结果下方给出个人判断

## 风格说明

| 维度 | formal（机构 DCF） | brief（个人估值笔记） |
|------|-------------------|---------------------|
| 输出格式 | Excel (.xlsx) | Markdown |
| 预测年数 | 5-7 年 | 3-5 年 |
| WACC | 完整推导过程 | 直接给出假设值 |
| 敏感性 | 3 张 5×5 表 | 1 张简化 3×3 表 |
| 情景 | Base + 可选 Bull/Bear | 仅 Base |
| 数据源标注 | 每个输入附来源 | 关键假设说明即可 |
| 免责声明 | 需要 | 不需要 |

## 关键规则

1. **公式优先于硬编码**：Excel 中所有计算值必须是公式，不硬编码数字
2. **假设透明**：每个关键假设（增长率、利润率、WACC 参数）都必须明确标注
3. **合理性检验**：
   - 每股价值 vs 当前股价差异 > 50% 时必须解释原因
   - 永续增长率不应超过长期 GDP 增速
   - 终值占比不应超过总价值的 75%（否则预测期不够长）
4. **A 股特殊考量**：
   - ERP 取 5%-7%（新兴市场溢价）
   - 注意限售股对总股本的影响
   - 部分行业有政府补贴，需判断是否持续
   - 关联交易可能扭曲利润，需调整
5. **不做精确预测**：DCF 的价值在于理解价值驱动因素和估值区间，而非得出一个"精确"的目标价
6. **与其他 skill 联动**：建议用 a-share-comps 的估值中位数交叉验证 DCF 结果
