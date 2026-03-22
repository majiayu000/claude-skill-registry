---
name: zephyr-index
description: Navigation hub for the Zephyr RTOS Agent Skill ecosystem. Use this skill to discover, select, and navigate to specialized skills for building, configuring, and debugging Zephyr-based embedded applications. Trigger when you are unsure which specialized Zephyr skill to apply to a task.
---

# Zephyr Index

The **Zephyr Index** is your entry point to a suite of specialized Agent Skills designed for professional Zephyr RTOS development. 

## When to Use
- You are starting a new Zephyr task and don't know which skill is relevant.
- You need a high-level overview of the Zephyr skill ecosystem.
- You want to navigate between foundational, common, and advanced Zephyr features.

## Quick Start (Skill Selection)
1. Open **[quick_reference.md](references/quick_reference.md)** and match your task category.
2. If the task spans multiple domains, follow **[decision_tree.md](references/decision_tree.md)**.
3. Open the selected skill `SKILL.md`, then load only the referenced docs needed for the current task.

## Navigation Hub

### 1. Skill Selection
If you have a specific task but aren't sure which skill to load, consult the **[Decision Tree](references/decision_tree.md)** or the **[Quick Reference](references/quick_reference.md)**.

### 2. Full Catalog
Review the **[Skill Catalog](references/skill_catalog.md)** for a complete index of all 21 consolidated skills across four implementation phases.

## Core Categories

### Foundations & Workflows
Covers the bedrock of Zephyr: West, Devicetree, Build Systems, and Core Kernel Basics.
- **Key Skills**: `zephyr-foundations`, `build-system`, `devicetree`, `kernel-basics`.

### Hardware & Peripherals
Interfacing with the physical world: GPIO, I2C, SPI, Sensors, and Power Management.
- **Key Skills**: `hardware-io`, `power-performance`.

### Connectivity
Networking and communication: BLE, IP (MQTT/CoAP/LwM2M), USB, and CAN.
- **Key Skills**: `connectivity-ble`, `connectivity-ip`, `connectivity-usb-can`.

### Production & Advanced
Taking your product to the finish line: Security, OTA Updates, Testing, and Multicore.
- **Key Skills**: `security-updates`, `testing-debugging`, `multicore`.

## Automation Tools
- **[task_skill_match.py](scripts/task_skill_match.py)**: Match task text to likely skills using keyword maps.

## Examples & Templates
- **[task_skill_keywords.csv](assets/task_skill_keywords.csv)**: Starter keyword-to-skill mapping for quick routing.

## Validation Checklist
- [ ] At least one representative task in each phase maps cleanly through `quick_reference.md`.
- [ ] Decision tree path selected for a task resolves to an existing skill file.
- [ ] Skill catalog entries match current directories under `skills/*`.
- [ ] Navigation links in this index resolve without broken relative paths.

## Resources

- **[References](references/)**:
  - `skill_catalog.md`: Complete list of all skills and their triggers.
  - `decision_tree.md`: Visual guide for skill selection.
  - `quick_reference.md`: Task-to-skill mapping for common queries.
- **[Scripts](scripts/)**:
  - `task_skill_match.py`: Keyword router for skill discovery.
- **[Assets](assets/)**:
  - `task_skill_keywords.csv`: Starter keyword map for routing.
