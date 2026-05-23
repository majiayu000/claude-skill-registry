---
name: godot-coding-standards
description: Godot 4.x 核心架构原则。当设计、审查 Godot 组件和系统时使用。关注：组件模式、信号通信、Resource设计、系统架构。触发词：godot, 组件, 信号, 架构, 设计。
---

# Godot 4.x 核心架构原则

为 Godot 4.x 项目设计的核心原则，确保代码的**通用性、模块化、可复用性、简洁性**。

## 核心设计原则

### 1. 通用性优先
- 使用 `@export` 暴露可配置参数，避免硬编码
- 组件应该能在不同场景中复用，不依赖特定父节点
- 通过配置而非代码修改来调整行为

### 2. 模块化设计
- **单一职责**：每个组件只做一件事（Health、Movement、Attack）
- **组件化思维**：用小组件组合出复杂行为，避免巨型类
- **信号松耦合**：通过信号通信，避免直接调用和硬依赖

### 3. 可复用性
- **Resource 类**：用于存储配置数据（Damage、SkillData）
- **清晰接口**：公共方法定义清晰，private方法用 `_` 前缀
- **独立性**：组件可以独立测试和使用

### 4. 简洁实用
- 注重实用性，避免过度设计
- 不为未来需求预先设计
- 代码自解释，复杂逻辑才加注释

## 组件模式示例

### 基础组件模板
```gdscript
extends Node
class_name Health

## 可复用的生命值组件
## 通过信号通知状态变化，不依赖特定父节点

signal health_changed(current: float, maximum: float)
signal died()

@export var max_health: float = 100.0

var health: float = max_health:
    set(val):
        health = clamp(val, 0, max_health)
        health_changed.emit(health, max_health)
        if health <= 0:
            died.emit()

func take_damage(amount: float) -> void:
    health -= amount

func heal(amount: float) -> void:
    health += amount
```

### Resource 数据类
```gdscript
extends Resource
class_name Damage

## 伤害数据配置类
## 可在编辑器中创建 .tres 资源文件

@export var base_damage: float = 10.0
@export var damage_type: String = "physical"
@export_group("Effects")
@export var knockback_force: float = 0.0
@export var stun_duration: float = 0.0
```

## 架构检查要点

- **通用性**：是否使用 `@export` 配置化？能否跨场景复用？
- **模块化**：是否单一职责？是否用信号解耦？
- **可复用性**：是否有清晰接口？Resource 类是否正确使用？
- **简洁性**：是否避免过度设计？代码是否自解释？
