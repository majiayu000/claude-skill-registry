---
name: embedded-thinking
description: 提供嵌入式系统软硬件协同思考框架，涵盖硬件层、软件架构、资源约束、实时性、测试调试五大维度。当需要设计嵌入式应用、评审物联网系统、或需要全局视角审视 MCU/MPU 与软件配合时使用。支持裸机/RTOS 选型、功耗优化、内存预算、中断响应、OTA 升级等嵌入式特有场景决策。
stage: SPECIAL
level_supported: [L1-STREAMLINED, L2-BALANCED, L3-RIGOROUS]
---

# Embedded Thinking Skill

> **Scope**: SPECIAL（用户自定义）
>
> **版本**: 0.1.0（占位）| **创建日期**: 2025-11-27

---

## 概述

嵌入式应用整体思考维度：

```
┌─────────────────────────────────────────────────────┐
│              ⚙️ Embedded System                     │
├─────────────┬─────────────┬─────────────────────────┤
│  Hardware   │  Software   │      Constraints        │
│  ─────────  │  ─────────  │  ─────────────────────  │
│  • MCU/MPU  │  • RTOS     │  • Memory (KB/MB)       │
│  • Sensors  │  • Drivers  │  • Power (mW)           │
│  • GPIO     │  • Protocol │  • Real-time (ms/μs)    │
│  • Bus      │  • OTA      │  • Temperature          │
└─────────────┴─────────────┴─────────────────────────┘
```

---

## 思考维度

### 1. 硬件层
- [ ] 处理器选型（MCU/MPU/DSP）
- [ ] 外设接口（GPIO/ADC/DAC/PWM）
- [ ] 通信总线（I2C/SPI/UART/CAN）
- [ ] 电源管理

### 2. 软件架构
- [ ] 裸机 vs RTOS（FreeRTOS/Zephyr）
- [ ] 驱动层设计
- [ ] 中间件（协议栈、文件系统）
- [ ] 应用层

### 3. 资源约束
- [ ] 内存预算（RAM/Flash）
- [ ] CPU 占用率
- [ ] 功耗优化（休眠模式）
- [ ] 代码大小优化

### 4. 实时性要求
- [ ] 硬实时 vs 软实时
- [ ] 中断响应时间
- [ ] 任务优先级
- [ ] 死锁避免

### 5. 可靠性与安全
- [ ] 看门狗机制
- [ ] 异常恢复
- [ ] 安全启动
- [ ] OTA 升级

### 6. 开发与调试
- [ ] 交叉编译环境
- [ ] 仿真器/调试器（JTAG/SWD）
- [ ] 日志与诊断
- [ ] 自动化测试（HIL）

---

## 分级思考深度

### L1-STREAMLINED
- 每维度选择 1 个关键决策
- 快速架构评审（30-60 分钟）
- 适用：简单嵌入式、单 MCU 系统

### L2-BALANCED
- 每维度覆盖 2-3 个决策点
- 标准架构评审（2-4 小时）
- 包含 MCU 选型对比 + 资源预算
- 适用：中型嵌入式、多任务 RTOS

### L3-RIGOROUS
- 全维度深入分析（6 维度 × 4 子项）
- 完整架构评审（1-2 天）
- 包含 WCET 分析/安全认证/EMC 考虑
- 生成硬件接口规格 + 软件架构文档
- 适用：复杂嵌入式、安全关键系统

---

## >> 命令

```
>>embedded_review_l1   # 嵌入式系统快速审视
>>embedded_checklist   # 生成检查清单
```

---

## 相关 Skills

- **设计**: layer-design（嵌入式分层架构）
- **测试**: test-strategy（嵌入式测试策略）
- **原则**: principle-kiss, principle-yagni（资源约束下的简化）
- **同类**: mobile-app-thinking（IoT 与移动端融合）

---

**TODO**: 待细化各 RTOS 选型和硬件平台差异
