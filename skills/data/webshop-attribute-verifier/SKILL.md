---
name: webshop-attribute-verifier
description: This skill confirms specific product attributes on a detailed product page. It is triggered when navigating to an individual product listing to verify details such as color options, exact price, or specifications. The skill checks available selections or displayed information against the user's requirements, ensuring the product matches before proceeding to purchase.
---
# Instructions
You are verifying product attributes on a detailed product page. Your goal is to confirm the product matches the user's requirements before proceeding.

## Core Workflow
1.  **Parse Requirements:** Extract the user's target attributes (e.g., color, max price) from the instruction.
2.  **Inspect Page:** Examine the observation for the product's details, available options (like color buttons), price, and specifications.
3.  **Verify Match:** Systematically check if the product's attributes satisfy all user requirements.
4.  **Act Accordingly:**
    *   If the product matches **all** requirements, proceed to select the correct option (e.g., click the correct color) and then initiate the purchase (e.g., click 'Buy Now').
    *   If the product **does not match** a requirement (e.g., wrong color, price too high), navigate back to search.

## Action Guidelines
*   Use `click[value]` to interact with page elements. The `value` must exactly match a clickable item from the observation.
*   Use `search[keywords]` only if you need to find a new product because the current one does not meet requirements.
*   Your `Thought:` must explicitly state which requirement you are checking and the result of the check.

## Critical Rules
*   **Price Check:** The product's price must be **strictly lower than** the user's specified maximum price.
*   **Attribute Selection:** If a specific attribute (like color) is required, you **must** click the corresponding option button (e.g., `click[black]`) before proceeding to purchase.
*   **Sequential Actions:** Do not skip the attribute selection step. The purchase action should only follow a successful verification and selection.
