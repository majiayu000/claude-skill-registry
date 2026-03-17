---
name: geo-ip
description: "Look up geographic location for any IP address"
metadata:
  {
    "openclaw":
      {
        "emoji": "🌍",
        "requires": { "bins": ["curl"] },
        "install": [],
      },
  }
---

# Geo IP

Look up the geographic location for any IP address using the ipinfo.io API. Returns city, region, country, coordinates, and ISP information.

## Commands

```bash
# Look up location for a specific IP address
geo-ip <ip-address>

# Look up your own public IP location
geo-ip me
```

## Install

No installation needed. `curl` is always present on the system. Uses the public ipinfo.io API.
