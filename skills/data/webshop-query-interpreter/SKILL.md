---
name: webshop-query-interpreter
description: This skill interprets a user's shopping query to extract key product requirements such as item type, attributes, and constraints. It should be triggered when a new shopping instruction is received, parsing natural language into structured criteria (e.g., product category, desired features, price limits). The output is a clear set of search parameters for use in subsequent product lookup steps.
---
# Instructions

## Trigger
Activate this skill when a new shopping instruction is received from the user. The instruction will be a natural language request for a product.

## Core Process

1.  **Parse the Instruction:** Analyze the user's query to identify the following key components:
    *   **Primary Product Type:** The main item being requested (e.g., "hair extension").
    *   **Key Attributes/Features:** Descriptive requirements (e.g., "long", "clip-in", "natural looking").
    *   **Constraints:** Hard limits, especially price (e.g., "price lower than 40.00 dollars").

2.  **Structure the Output:** Format the extracted information into a clear, structured set of search parameters. Use the following template:
    