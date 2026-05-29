---
name: webshop-action-executor
description: This skill executes a specific interface action, such as clicking a button or selecting an option, within a web shopping environment. It should be triggered when a decision has been made (e.g., to choose a color or proceed to purchase). The input is the target action identifier (e.g., 'white' or 'buy now'), and the output is the corresponding formatted action command (e.g., click[white]).
---
# Skill: WebShop Action Executor

## Purpose
Execute a single, specific action in a WebShop environment after a decision has been made. This skill formats the action into the required command structure for the WebShop interface.

## When to Use
- **Trigger:** When the agent has completed its analysis and has decided on the exact action to take (e.g., "select the white color option," "proceed to buy now").
- **Input:** A clear target identifier (string) derived from the available actions on the current page.
- **Output:** A correctly formatted `click[value]` or `search[keywords]` command.

## Core Instruction
1.  **Receive Input:** The skill is provided with a single `target_action` string (e.g., 'white', 'buy now', 'b08w25dbb7').
2.  **Format Output:** Immediately output the action in the exact format required by the WebShop environment:
    