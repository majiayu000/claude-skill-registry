---
name: webshop-option-selector
description: This skill selects product options or variants (such as size, color, or quantity) on a product detail page based on user preferences or cost optimization. It should be triggered when a product page displays configurable options. The skill evaluates available choices (e.g., 1pcs vs 2pcs) and selects the one that best aligns with the user's constraints, such as minimizing cost.
---
# Skill: WebShop Option Selector

## Trigger Condition
Activate this skill when the observation from the WebShop environment contains:
1. A product detail page (indicated by the presence of a "Price:" field and product title).
2. One or more configurable option categories (e.g., "size:", "color:", "quantity:") with clickable values listed beneath them.

## Core Logic
1. **Parse the Observation:** Identify all configurable option categories and their available values from the current page state.
2. **Apply Selection Strategy:** By default, implement a **cost-minimization strategy**. For each option category, select the value that results in the lowest final price while still meeting any explicit user constraints from the original instruction (e.g., "price lower than 40.00 dollars").
3. **Execute Selection:** Perform a `click[value]` action for the chosen option value. If multiple categories exist, they should be selected in the order they appear on the page.

## Important Notes
- The skill assumes the displayed price updates (or is representative) after an option is selected. Your action should be based on the currently displayed information.
- If the user's instruction contains specific preferences (e.g., "large size", "blue color"), prioritize those over cost minimization.
- If no clear cost difference can be inferred, select the first available option.
- After selecting the desired option, you may proceed with other actions (e.g., `click[buy now]`).

## Example from Trajectory
**Observation Excerpt:**
