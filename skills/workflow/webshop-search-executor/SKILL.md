---
name: webshop-search-executor
description: Executes a search on an e-commerce platform using parsed keywords. Trigger when you need to find products matching specific criteria from a user query. This skill takes structured search terms and performs a search action, returning a list of product results for evaluation.
---
# Instructions

## Core Function
When triggered, this skill executes a product search on a simulated e-commerce platform (WebShop). Your primary goal is to translate a user's product request into an effective search query, execute it, and return the parsed results for further action.

## 1. Trigger Condition
Activate this skill when the user provides an instruction to find or buy a product with specific attributes (e.g., ingredients, price range, features). The instruction will be provided in the `Observation`.

## 2. Action Protocol
You must respond using **only** the following two action formats. Your final response must be in the exact structure:
