---
name: "dns"
description: "Manages DNS records, DDNS, and SSL certificates using ChatTool. Invoke when user wants to list domains, modify DNS records, or update certificates."
---

# DNS Manager

This skill allows you to manage DNS records and SSL certificates using the ChatTool library.

## Capabilities

- **List Domains**: View all domains under the configured account (Aliyun/Tencent).
- **Get Records**: Retrieve DNS records for a specific domain.
- **Add/Delete Records**: Modify DNS records.
- **DDNS**: Update dynamic DNS records.
- **SSL Certificates**: Request or renew Let's Encrypt certificates.

## Tools

You should use the available MCP tools for these operations:
- `dns_list_domains`
- `dns_get_records`
- `dns_add_record`
- `dns_delete_record`
- `dns_ddns_update`
- `dns_cert_update`

## Configuration

Ensure the environment variables for the DNS provider are set (e.g., `ALIBABA_CLOUD_ACCESS_KEY_ID`, `TENCENT_CLOUD_SECRET_ID`, etc.).
