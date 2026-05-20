---
name: taboola-launcher
description: Launch complete Taboola native ad campaigns with AI-generated creative assets. Use when user wants to create a new Taboola campaign, launch native ads for mortgage (or other verticals), or run "/launch-taboola". Orchestrates Taboola, RedTrack, Presales, and Gemini Image MCP tools to generate headlines, images, landing pages, set up tracking, and create campaigns. All campaigns start PAUSED until explicit "/taboola-unpause".
---

# Taboola Campaign Launcher

End-to-end Taboola native ad campaign creation with AI-generated creative assets.

## Quick Start

```
/launch-taboola vertical:mortgage brief:"Florida homeowners paying 7%+ rates" everflow-offer-ids:"654"
```

**Result**: PAUSED campaign with 100 ad items (10 headlines × 10 images), 3 landing page styles, full RedTrack tracking.

## Workflow Overview

5-phase orchestrator pattern with parallel subagent execution:

```
Phase 1: Creative Generation (PARALLEL)
├── headline-generator    → 10 headlines from proven formulas
├── image-generator       → 10 images via Gemini
└── lander-generator      → 3 styles via Presales

Phase 2: Asset Upload (PARALLEL)
├── taboola-uploader      → Images to Taboola CDN
└── ftp-uploader          → Landers to FTP

Phase 3: Tracking Setup (SEQUENTIAL)
└── redtrack-setup        → Offers + landers + campaign → trackback_url

Phase 4: Campaign Creation (SEQUENTIAL)
├── taboola-campaign      → Create PAUSED campaign
└── item-matrix           → 100 items (headlines × images)

Phase 5: Save & Report
└── manifest + summary with unpause instructions
```

**IMPORTANT**: Campaigns are ALWAYS created PAUSED. Run `/taboola-unpause {id}` to activate.

## Required Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `vertical` | Target vertical | `mortgage` |
| `brief` | Creative angle/targeting | `"Florida homeowners paying 7%+"` |
| `everflow-offer-ids` | Offer ID(s), comma-sep | `"654"` or `"654,655"` |

## Optional Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--daily-cap` | 50.0 | Daily budget cap in USD |
| `--cpc` | 0.35 | Cost per click |
| `--num-variations` | 10 | Headlines and images to generate |
| `--landing-ids` | (generate) | Use existing RedTrack lander IDs |
| `--dry-run` | false | Preview without creating |

## Execution

Read `workflows/orchestrator.md` for the complete 5-phase workflow.

### Phase 1: Creative Generation

Dispatch 3 subagents IN PARALLEL using Task tool:

1. **headline-generator** - See `workflows/subagents/headline-generator.md`
2. **image-generator** - See `workflows/subagents/image-generator.md`
3. **lander-generator** - See `workflows/subagents/lander-generator.md`

Timeout: 5 minutes. Minimum: 1 headline, 1 image.

### Phase 2: Asset Upload

Dispatch 2 subagents IN PARALLEL:

1. **taboola-uploader** - `tb_upload_image_from_url` for each image
2. **ftp-uploader** - `presales_ftp_upload` for landers

### Phase 3: Tracking Setup

SEQUENTIAL - requires lander URLs from Phase 2:

1. Look up existing offers with `rt_lookup_offer`
2. Create offers if needed with `rt_setup_regular_offer`
3. Register landers with `rt_create_lander`
4. Create campaign with `rt_create_campaign_v2`
5. Get `trackback_url` for Taboola items

### Phase 4: Campaign Creation

SEQUENTIAL:

1. Create campaign PAUSED with `tb_create_campaign`
2. Create item matrix with `tb_create_items_batch` (headlines × images)

### Phase 5: Save & Report

1. Save manifest to `outputs/taboola-campaigns/{campaign_id}.json`
2. Return summary with all URLs and IDs
3. Include: "Run `/taboola-unpause {campaign_id}` to activate"

## Configuration

### Media Buyers

Read `config/media-buyers.json` for Everflow affiliate mappings.

### Vertical Config

Read `config/mortgage.json` for:
- Default CPC, daily cap, bid strategy
- Proven headline angles and formulas
- Image templates for Gemini
- Compliance rules

## Related Commands

| Command | Purpose |
|---------|---------|
| `/taboola-unpause {id}` | Activate paused campaign |
| `/taboola-pause {id}` | Pause running campaign |
| `/taboola-status {id}` | Get performance metrics |

## MCP Tools Reference

See `references/mcp-tools.md` for complete tool documentation.

**Key Tools**:
- `tb_create_campaign`, `tb_create_items_batch`, `tb_upload_image_from_url`
- `rt_setup_regular_offer`, `rt_create_lander`, `rt_create_campaign_v2`
- `presales_generate`, `presales_ftp_upload`
- `gemini_batch_generate`

## Error Handling

| Phase | If Fails | Action |
|-------|----------|--------|
| Headline gen | Retry once | Continue with fewer headlines |
| Image gen | Retry once | Continue with fewer images |
| Lander gen | Retry once | Skip landers, direct to offer |
| Upload | Retry once | Flag failed assets |
| Tracking | Critical | Abort, save partial state |
| Campaign | Critical | Abort, save partial state |

## Output

Campaign manifest saved to `outputs/taboola-campaigns/{campaign_id}.json`:

```json
{
  "campaign_id": "123456",
  "status": "PAUSED",
  "vertical": "mortgage",
  "brief": "...",
  "created_at": "2025-01-26T...",
  "taboola": {
    "campaign_id": "123456",
    "items_created": 100
  },
  "redtrack": {
    "campaign_id": "abc123",
    "trackback_url": "https://...",
    "offer_ids": ["..."],
    "lander_ids": ["..."]
  },
  "assets": {
    "headlines": [...],
    "images": [...],
    "landers": [...]
  }
}
```
