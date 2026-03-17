---
name: refactor-guide
description: 代码重构指南技能。当用户需要优化代码结构、消除代码异味、改进设计模式、提升代码可维护性或进行架构改进时使用此技能。
---

# Refactor Guide

系统化的代码重构方法，在不改变外部行为的前提下改进代码内部结构。

## 重构原则

1. **小步前进**：每次只做一个小改动
2. **持续测试**：每次改动后运行测试
3. **保持行为**：不改变代码外部行为
4. **及时提交**：每个重构点单独提交

## 代码异味识别

### 🔴 高优先级
- **重复代码**：相同逻辑出现多处
- **过长函数**：函数超过 50 行
- **过大类**：类承担过多职责
- **过长参数列表**：参数超过 4 个

### 🟡 中优先级
- **发散式变化**：一个类因多种原因修改
- **霰弹式修改**：一个变化需要修改多处
- **依恋情结**：方法过度使用其他类数据
- **数据泥团**：相同数据组总是一起出现

## 常用重构手法

### 提取函数
```python
# Before
def process_order(order):
    # 验证订单
    if not order.items:
        raise ValueError("空订单")
    if order.total < 0:
        raise ValueError("金额错误")
    # 处理逻辑...

# After
def process_order(order):
    validate_order(order)
    # 处理逻辑...

def validate_order(order):
    if not order.items:
        raise ValueError("空订单")
    if order.total < 0:
        raise ValueError("金额错误")
```

### 引入参数对象
```python
# Before
def create_report(start_date, end_date, format, include_header):
    ...

# After
@dataclass
class ReportConfig:
    start_date: date
    end_date: date
    format: str = "pdf"
    include_header: bool = True

def create_report(config: ReportConfig):
    ...
```

## 重构检查清单

- [ ] 有充分的测试覆盖
- [ ] 每次改动后测试通过
- [ ] 代码可读性提升
- [ ] 没有引入新的依赖
- [ ] 提交信息清晰描述重构内容