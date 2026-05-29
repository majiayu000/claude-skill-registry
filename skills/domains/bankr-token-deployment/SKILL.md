---
name: Bankr Agent - Token Deployment
description: This skill should be used when the user asks to "deploy token", "create token", "launch token", "Clanker", "claim fees", "token metadata", "update token", "mint new token", or any token deployment operation. Provides guidance on deploying ERC20 tokens via Clanker.
version: 1.0.0
---

# Bankr Token Deployment

Deploy and manage ERC20 tokens using Clanker.

## Supported Chains

- **Base**: Primary deployment chain, full Clanker support
- **Unichain**: Secondary option

## Deployment Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| Name | Yes | Token name (e.g., "MyToken") |
| Symbol | Yes | Ticker, 3-5 chars (e.g., "MTK") |
| Description | No | Token description |
| Image | No | Logo URL or upload |
| Website | No | Project website |
| Twitter | No | Twitter/X handle |
| Telegram | No | Telegram group |

## Prompt Examples

**Deploy tokens:**
- "Deploy a token called BankrFan with symbol BFAN"
- "Create a memecoin: name=DogeKiller, symbol=DOGEK"
- "Deploy token with website myproject.com and Twitter @myproject"

**Claim fees:**
- "Claim fees for my token MTK"
- "Check my Clanker fees"
- "Claim legacy Clanker fees"

**Update metadata:**
- "Update description for MyToken"
- "Add Twitter link to my token"
- "Update logo for MyToken"

## Rate Limits

| User Type | Daily Limit |
|-----------|-------------|
| Standard Users | 1 token/day |
| Bankr Club Members | 10 tokens/day |

## Fee Structure

- Small fee on each trade, accumulated for token creator
- Claimable anytime via "Claim fees for my token"
- Legacy fees (older Clanker versions) claimed separately

## Common Issues

| Issue | Resolution |
|-------|------------|
| Rate limit reached | Wait 24 hours or upgrade |
| Name taken | Choose different name |
| Symbol exists | Use unique symbol |
| Image upload failed | Check format/size |

## Best Practices

- Choose unique, memorable name and symbol
- Add description and social links immediately
- Upload quality logo
- Claim fees regularly
