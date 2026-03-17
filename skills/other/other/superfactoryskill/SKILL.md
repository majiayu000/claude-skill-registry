---
name: SuperfactorySkill
description: Provides specialized functionality for writing and managing Super Factory Manager (SFM) scripts for Minecraft, including script generation, optimization, and troubleshooting.
---

# SuperfactorySkill

## Description
This skill provides specialized functionality for writing and managing Super Factory Manager (SFM) scripts for Minecraft. It helps users create efficient factory automation programs using SFM's domain-specific language.

## What it does
- Generates Super Factory Manager scripts for various automation tasks
- Provides code examples and templates for common factory setups
- Offers performance optimization guidance for SFM  programs
- Explains SFM syntax and best practices
- Helps troubleshoot common SFM script issues

## When to use it
Use this skill when you need to:
- Create SFM scripts for factory automation in Minecraft
- Optimize existing SFM programs for better performance
- Learn SFM syntax and programming concepts
- Troubleshoot issues with SFM scripts
- Get examples for specific automation tasks

## How to use it
1. The agent will automatically detect this skill when SFM-related topics are discussed
2. The agent will load this skill and provide relevant guidance
3. The agent may use the included instructions and examples to assist
4. The agent can generate complete SFM scripts based on your requirements

## Inputs
- **task**: string - The automation task you want to accomplish
- **components**: array - Minecraft blocks and items involved
- **requirements**: object - Specific requirements for the automation
- **performance_goals**: object - Performance optimization goals

## Outputs
- **script**: string - The generated SFM script
- **explanation**: string - Explanation of how the script works
- **performance_analysis**: object - Performance considerations
- **troubleshooting**: string - Common issues and solutions

## Dependencies
- None

## Files in this skill
- `SKILL.md` - This file, the main skill definition
- `instructions/` - Detailed step-by-step instructions for SFM programming
- `examples/` - Example SFM scripts for various automation tasks
  - `item_transfer.sfm` - Basic item transfer between chests
  - `furnace_automation.sfm` - Automatic furnace feeding and collection
  - `performance_optimization.sfm` - High-performance transfer techniques
  - `fluid_transfer.sfm` - Fluid transportation between tanks and machines
  - `energy_transfer.sfm` - Energy distribution to machines
  - `gas_transfer.sfm` - Gas collection and distribution
  - `advanced_filtering.sfm` - Various item filtering techniques
  - `conditional_logic.sfm` - IF statements and conditional operations
  - `complex_automation.sfm` - Multi-step manufacturing process
  - `round_robin.sfm` - Balanced distribution across multiple destinations
  - `redstone_signals.sfm` - Redstone-controlled operations
  - `empty_slots.sfm` - Output only to empty inventory slots
  - `slot_operations.sfm` - Targeting specific inventory slots
  - `timer_triggers.sfm` - Various timer configurations and syntaxes
- `resources/` - Templates, reference materials, and best practices
  - `best_practices.md` - Best practices and performance guidelines
  - `sfm_keywords.md` - Comprehensive SFM keywords reference with examples
