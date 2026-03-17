---
name: pivot-on-ioc
description: "Explore GTI relationships for an IOC to discover related entities. Use to expand investigation by finding connected domains, IPs, files, or threat actors. Takes an IOC and relationship types to query."
required_roles:
  gti: GTI Enterprise+
personas: [tier2-analyst, tier3-analyst, threat-hunter]
---

# Pivot on IOC Skill

Explore relationships connected to an IOC within Google Threat Intelligence (GTI) to discover related entities for investigation expansion.

## Inputs

- `IOC_VALUE` - The indicator value to pivot from
- `IOC_TYPE` - The type: "IP Address", "Domain", "File Hash", "URL", or "Collection"
- `RELATIONSHIP_NAMES` - List of relationships to query (see table below)

## Available Relationships by IOC Type

| IOC Type | Common Relationships |
|----------|---------------------|
| IP Address | `communicating_files`, `downloaded_files`, `referrer_files`, `resolutions` |
| Domain | `resolutions`, `communicating_files`, `downloaded_files`, `subdomains`, `siblings` |
| File Hash | `contacted_domains`, `contacted_ips`, `contacted_urls`, `dropped_files`, `embedded_domains` |
| URL | `communicating_files`, `downloaded_files`, `last_serving_ip_address` |
| Collection | `malware_families`, `attack_techniques`, `threat_actors`, `indicators` |

## Workflow

### Step 1: Select GTI Tool

Based on IOC_TYPE:

| IOC Type | Tool |
|----------|------|
| IP Address | `gti-mcp.get_entities_related_to_an_ip_address` |
| Domain | `gti-mcp.get_entities_related_to_a_domain` |
| File Hash | `gti-mcp.get_entities_related_to_a_file` |
| URL | `gti-mcp.get_entities_related_to_an_url` |
| Collection | `gti-mcp.get_entities_related_to_a_collection` |

### Step 2: Query Each Relationship

For each relationship in `RELATIONSHIP_NAMES`:

```
[selected_tool](
    identifier=IOC_VALUE,
    relationship_name=relationship
)
```

Store results keyed by relationship name.

## Required Outputs

**After completing this skill, you MUST report these outputs:**

| Output | Description |
|--------|-------------|
| `RELATED_ENTITIES` | Dictionary of entities found per relationship |
| `EXPANDED_IOCS` | Flattened list of all discovered IOCs (IPs, domains, hashes) |
| `THREAT_CONTEXT` | Threat actor/campaign context if found during pivoting |
| `PIVOT_STATUS` | Success/failure status of the pivoting |

## Example Usage

**File Hash Investigation:**
```
IOC_VALUE: "abcdef123456..."
IOC_TYPE: "File Hash"
RELATIONSHIP_NAMES: ["contacted_domains", "contacted_ips", "dropped_files"]
```

**Domain Investigation:**
```
IOC_VALUE: "suspicious-domain.com"
IOC_TYPE: "Domain"
RELATIONSHIP_NAMES: ["resolutions", "communicating_files", "subdomains"]
```
