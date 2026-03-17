---
name: 股票分析
description: 提供获取用户自选分组(LongPort)、股票市场数据(LongPort + AkShare)、技术指标计算（ta-lib）的技能。分析数并与用户研究交易策略，形成买卖点建议，并可做回测、寻优与报告输出。
---

# 简介

## 何时触发

当用户提出下列任意请求时，加载本 Skill：

- “调用 LongPort 分组接口拿到一批股票，补齐市场数据并做分析”
- "对分组内所有标的计算技术指标，生成买卖点建议"

## 能力概览

- 数据采集与分组：
  - LongPort 分组接口获取标的列表
  - 行情数据：优先 LongPort，缺失时回退 AkShare；支持前复权与时间对齐
- 指标计算：
  - 使用 TA-Lib，完整指标套件（EMA/MACD/RSI/ATR/OBV/BBANDS）
- 信号生成：
  - 规则/阈值/指标组合生成买卖点建议（含打分）

## 资源导航（何时加载）

- references/data_sources.md — LongPort + AkShare
- references/indicators.md — 指标使用技介绍
- scripts/
  - longport_groups.py — 自选分组管理（CLI：list/create/update/get-symbols/delete）
  - longport_candlesticks.py — K 线数据获取（CLI：按周期/数量/输出路径查询）
  - talib_calculator.py — 技术指标计算（支持单指标或 compute_full_suite）
- assets/（可选）— 报告模板或 Notebook，如需生成报告/演示可补充

## 工作流示例（触发句）

- “用 LongPort 拿到分组成份，缺失的用 AkShare 补齐，合并到统一行情表。”
- "对分组内所有标的计算技术指标，生成买卖点建议列表。"

## 注意事项与最佳实践

- 数据一致性：LongPort/AkShare需统一时区、使用前复权；缺失值要先补齐再算指标
- 指标健壮性：TA-Lib 初期会产生 NaN，计算信号前先截取有效区间或前向填充
- 凭证安全：LongPort/AkShare 请使用本地 .env 或加密文件，避免提交到仓库
