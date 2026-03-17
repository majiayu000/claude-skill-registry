---
name: ip-lookup
description: Get current public IP address and geolocation information. Use when users ask about IP addresses, network location, or want to check their public IP. Supports both fetching IP info and displaying it clearly.
---

# IP Lookup Skill

## Overview

This skill provides a simple way to check your public IP address and its geolocation information.

## Usage

When users ask:
- "What is my IP?"
- "What is my current IP address?"
- "Where am I located?"
- "Check my IP location"
- "What's my public IP?"
- "What's the IP?"
- "What's your IP?"

Execute the workflow below.

## Workflow

### Basic IP Check

Run this command to get your public IP and location:

```bash
curl -s myip.ipip.net
```

Example output:
```
Current IP：8.8.8.8  From: SF CA USA Google
Current IP：1.1.1.1  From: SF CA USA Cloudflare
```

### Alternative Methods

If the above fails, try these alternatives:

**Method 1: icanhazip.com (fallback)**
```bash
curl -s icanhazip.com
```

**Method 2: ipify API**
```bash
curl -s https://api.ipify.org
```

**Method 3: ifconfig.me**
```bash
curl -s ifconfig.me
```

### Full Geolocation Lookup

For more detailed geolocation info:

```bash
curl -s https://ipinfo.io/$(curl -s https://api.ipify.org)/json
```

## Display Format

Present the information clearly:

**IP Address:** [address]
**Location:** [city], [region], [country]
**ISP:** [ISP name]
**Org:** [organization]

## Error Handling

If the primary service (`myip.ipip.net`) fails:
1. Try alternative services one by one
2. Report which service succeeded
3. If all fail, inform the user about the network issue
