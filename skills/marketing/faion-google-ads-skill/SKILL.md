---
name: faion-google-ads-skill
user-invocable: false
description: ""
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Google Ads API Skill

**Communication: User's language. Docs/code: English.**

## Purpose

Provides patterns and guidance for Google Ads API operations including campaign management, keyword research, ad groups, bidding strategies, conversion tracking, Google Analytics integration, reporting, and automation.

## 3-Layer Architecture

```
Layer 1: Domain Skills (faion-marketing-domain-skill) - orchestrator
    |
Layer 2: Agents (faion-ads-agent) - executor
    |
Layer 3: Technical Skills (this) - tool
```

---

# Section 1: Authentication

## Overview

Google Ads API uses OAuth 2.0 for authentication with additional developer tokens for API access.

## Authentication Components

| Component | Purpose | Required |
|-----------|---------|----------|
| Developer Token | API access identifier | Yes |
| OAuth 2.0 Client ID | Application identifier | Yes |
| OAuth 2.0 Client Secret | Application secret | Yes |
| Refresh Token | Long-lived token for access | Yes |
| Login Customer ID | Manager account ID (MCC) | For MCC |

## Authentication Flow

```
1. Create Google Cloud Project
   |
2. Enable Google Ads API
   |
3. Create OAuth 2.0 credentials
   |
4. Get Developer Token (ads.google.com)
   |
5. Generate Refresh Token
   |
6. Configure client library
```

## Developer Token Levels

| Level | Daily Requests | Requirements |
|-------|----------------|--------------|
| Test Account | Unlimited (test) | Apply in Google Ads UI |
| Basic Access | 15,000 | Approved application |
| Standard Access | 10,000 per customer | Company verification |

## Python Authentication Setup

```python
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

# Option 1: From YAML config file
client = GoogleAdsClient.load_from_storage("google-ads.yaml")

# Option 2: From dict
credentials = {
    "developer_token": "YOUR_DEVELOPER_TOKEN",
    "client_id": "YOUR_CLIENT_ID",
    "client_secret": "YOUR_CLIENT_SECRET",
    "refresh_token": "YOUR_REFRESH_TOKEN",
    "login_customer_id": "YOUR_MANAGER_ID",  # Optional, for MCC
    "use_proto_plus": True
}
client = GoogleAdsClient.load_from_dict(credentials)
```

## google-ads.yaml Template

```yaml
developer_token: "DEVELOPER_TOKEN"
client_id: "CLIENT_ID.apps.googleusercontent.com"
client_secret: "CLIENT_SECRET"
refresh_token: "REFRESH_TOKEN"
login_customer_id: "MANAGER_ACCOUNT_ID"  # Without dashes
use_proto_plus: True
```

## Service Account Authentication (Server-to-Server)

```python
from google.ads.googleads.client import GoogleAdsClient

# For domain-wide delegation
credentials = {
    "developer_token": "DEVELOPER_TOKEN",
    "json_key_file_path": "service-account.json",
    "impersonated_email": "user@domain.com",
    "login_customer_id": "MANAGER_ID"
}
client = GoogleAdsClient.load_from_dict(credentials)
```

## Security Best Practices

- Store credentials in environment variables or secrets manager
- Never commit credentials to version control
- Use separate credentials for test/production
- Rotate refresh tokens periodically
- Implement least-privilege access

---

# Section 2: Account Structure

## Hierarchy

```
Manager Account (MCC)
|
+-- Customer Account 1
|   |
|   +-- Campaign A
|   |   +-- Ad Group 1
|   |   |   +-- Ads
|   |   |   +-- Keywords
|   |   +-- Ad Group 2
|   |
|   +-- Campaign B
|
+-- Customer Account 2
```

## Resource Types

| Resource | Description | Parent |
|----------|-------------|--------|
| Customer | Ad account | Manager (optional) |
| Campaign | Budget, targeting settings | Customer |
| Ad Group | Ads and keywords container | Campaign |
| Ad | Creative content | Ad Group |
| Keyword | Search targeting | Ad Group |
| Extension | Additional ad info | Campaign/Ad Group |

## Customer Management

```python
def list_accessible_customers(client):
    """List all customers accessible by the authenticated user."""
    customer_service = client.get_service("CustomerService")

    accessible_customers = customer_service.list_accessible_customers()

    for resource_name in accessible_customers.resource_names:
        customer_id = resource_name.split("/")[-1]
        print(f"Customer ID: {customer_id}")

def get_customer_details(client, customer_id):
    """Get details for a specific customer."""
    ga_service = client.get_service("GoogleAdsService")

    query = """
        SELECT
            customer.id,
            customer.descriptive_name,
            customer.currency_code,
            customer.time_zone,
            customer.auto_tagging_enabled
        FROM customer
    """

    response = ga_service.search(customer_id=customer_id, query=query)

    for row in response:
        customer = row.customer
        return {
            "id": customer.id,
            "name": customer.descriptive_name,
            "currency": customer.currency_code,
            "timezone": customer.time_zone,
            "auto_tagging": customer.auto_tagging_enabled
        }
```

---

# Section 3: Campaign Management

## Campaign Types

| Type | Code | Best For |
|------|------|----------|
| Search | SEARCH | Text ads on search results |
| Display | DISPLAY_NETWORK | Banner ads across websites |
| Shopping | SHOPPING | Product listings |
| Video | VIDEO | YouTube ads |
| App | MULTI_CHANNEL | App installs/engagement |
| Performance Max | PERFORMANCE_MAX | AI-optimized cross-channel |
| Demand Gen | DEMAND_GEN | Discovery feeds |

## Create Search Campaign

```python
from google.ads.googleads.client import GoogleAdsClient

def create_search_campaign(client, customer_id, budget_amount_micros):
    """Create a Search campaign with budget."""
    campaign_budget_service = client.get_service("CampaignBudgetService")
    campaign_service = client.get_service("CampaignService")

    # Create campaign budget
    budget_operation = client.get_type("CampaignBudgetOperation")
    budget = budget_operation.create
    budget.name = f"Campaign Budget {uuid.uuid4()}"
    budget.amount_micros = budget_amount_micros  # e.g., 10000000 = $10
    budget.delivery_method = client.enums.BudgetDeliveryMethodEnum.STANDARD

    budget_response = campaign_budget_service.mutate_campaign_budgets(
        customer_id=customer_id,
        operations=[budget_operation]
    )
    budget_resource_name = budget_response.results[0].resource_name

    # Create campaign
    campaign_operation = client.get_type("CampaignOperation")
    campaign = campaign_operation.create
    campaign.name = f"Search Campaign {uuid.uuid4()}"
    campaign.campaign_budget = budget_resource_name
    campaign.advertising_channel_type = (
        client.enums.AdvertisingChannelTypeEnum.SEARCH
    )
    campaign.status = client.enums.CampaignStatusEnum.PAUSED

    # Network settings
    campaign.network_settings.target_google_search = True
    campaign.network_settings.target_search_network = True
    campaign.network_settings.target_partner_search_network = False
    campaign.network_settings.target_content_network = False

    # Bidding strategy
    campaign.manual_cpc.enhanced_cpc_enabled = True

    # Start/end dates (YYYY-MM-DD format)
    campaign.start_date = "2026-02-01"
    campaign.end_date = "2026-12-31"

    response = campaign_service.mutate_campaigns(
        customer_id=customer_id,
        operations=[campaign_operation]
    )

    return response.results[0].resource_name
```

## Create Performance Max Campaign

```python
def create_performance_max_campaign(client, customer_id, budget_micros):
    """Create a Performance Max campaign."""
    campaign_service = client.get_service("CampaignService")

    # Budget (same as above)
    budget_resource = create_campaign_budget(client, customer_id, budget_micros)

    # Campaign
    operation = client.get_type("CampaignOperation")
    campaign = operation.create
    campaign.name = f"PMax Campaign {uuid.uuid4()}"
    campaign.campaign_budget = budget_resource
    campaign.advertising_channel_type = (
        client.enums.AdvertisingChannelTypeEnum.PERFORMANCE_MAX
    )
    campaign.status = client.enums.CampaignStatusEnum.PAUSED

    # PMax requires Maximize Conversions or Maximize Conversion Value
    campaign.maximize_conversions.target_cpa_micros = 0  # Let Google optimize

    # URL expansion
    campaign.url_expansion_opt_out = False

    response = campaign_service.mutate_campaigns(
        customer_id=customer_id,
        operations=[operation]
    )

    return response.results[0].resource_name
```

## Update Campaign

```python
def update_campaign_status(client, customer_id, campaign_id, new_status):
    """Update campaign status (ENABLED, PAUSED, REMOVED)."""
    campaign_service = client.get_service("CampaignService")

    operation = client.get_type("CampaignOperation")
    campaign = operation.update
    campaign.resource_name = f"customers/{customer_id}/campaigns/{campaign_id}"
    campaign.status = getattr(
        client.enums.CampaignStatusEnum,
        new_status.upper()
    )

    # Set update mask
    client.copy_from(
        operation.update_mask,
        protobuf_helpers.field_mask(None, campaign._pb)
    )

    response = campaign_service.mutate_campaigns(
        customer_id=customer_id,
        operations=[operation]
    )

    return response.results[0].resource_name
```

## List Campaigns

```python
def list_campaigns(client, customer_id):
    """List all campaigns with key metrics."""
    ga_service = client.get_service("GoogleAdsService")

    query = """
        SELECT
            campaign.id,
            campaign.name,
            campaign.status,
            campaign.advertising_channel_type,
            campaign_budget.amount_micros,
            metrics.impressions,
            metrics.clicks,
            metrics.cost_micros,
            metrics.conversions
        FROM campaign
        WHERE campaign.status != 'REMOVED'
        ORDER BY campaign.name
    """

    response = ga_service.search(customer_id=customer_id, query=query)

    campaigns = []
    for row in response:
        campaigns.append({
            "id": row.campaign.id,
            "name": row.campaign.name,
            "status": row.campaign.status.name,
            "type": row.campaign.advertising_channel_type.name,
            "budget": row.campaign_budget.amount_micros / 1_000_000,
            "impressions": row.metrics.impressions,
            "clicks": row.metrics.clicks,
            "cost": row.metrics.cost_micros / 1_000_000,
            "conversions": row.metrics.conversions
        })

    return campaigns
```

---

# Section 4: Ad Groups

## Create Ad Group

```python
def create_ad_group(client, customer_id, campaign_id, name, cpc_bid_micros):
    """Create an ad group within a campaign."""
    ad_group_service = client.get_service("AdGroupService")

    operation = client.get_type("AdGroupOperation")
    ad_group = operation.create
    ad_group.name = name
    ad_group.campaign = f"customers/{customer_id}/campaigns/{campaign_id}"
    ad_group.status = client.enums.AdGroupStatusEnum.ENABLED
    ad_group.type_ = client.enums.AdGroupTypeEnum.SEARCH_STANDARD

    # Set default CPC bid
    ad_group.cpc_bid_micros = cpc_bid_micros  # e.g., 1000000 = $1.00

    response = ad_group_service.mutate_ad_groups(
        customer_id=customer_id,
        operations=[operation]
    )

    return response.results[0].resource_name
```

## Ad Group Types

| Type | Campaign Type | Description |
|------|---------------|-------------|
| SEARCH_STANDARD | Search | Standard search ads |
| SEARCH_DYNAMIC_ADS | Search | Dynamic search ads |
| DISPLAY_STANDARD | Display | Standard display ads |
| SHOPPING_PRODUCT_ADS | Shopping | Product listing ads |
| VIDEO_BUMPER | Video | 6-second non-skippable |
| VIDEO_TRUE_VIEW_IN_STREAM | Video | Skippable in-stream |

## Update Ad Group Bid

```python
def update_ad_group_bid(client, customer_id, ad_group_id, new_bid_micros):
    """Update ad group CPC bid."""
    ad_group_service = client.get_service("AdGroupService")

    operation = client.get_type("AdGroupOperation")
    ad_group = operation.update
    ad_group.resource_name = (
        f"customers/{customer_id}/adGroups/{ad_group_id}"
    )
    ad_group.cpc_bid_micros = new_bid_micros

    client.copy_from(
        operation.update_mask,
        protobuf_helpers.field_mask(None, ad_group._pb)
    )

    response = ad_group_service.mutate_ad_groups(
        customer_id=customer_id,
        operations=[operation]
    )

    return response.results[0].resource_name
```

---

# Section 5: Keyword Management

## Match Types

| Match Type | Symbol | Example Keyword | Matches |
|------------|--------|-----------------|---------|
| Broad | none | shoes | running shoes, buy footwear |
| Phrase | "..." | "running shoes" | best running shoes, running shoes sale |
| Exact | [...] | [running shoes] | running shoes (exact or close) |

## Add Keywords

```python
def add_keywords(client, customer_id, ad_group_id, keywords):
    """Add keywords to an ad group.

    Args:
        keywords: List of dicts with 'text' and 'match_type'
    """
    ad_group_criterion_service = client.get_service("AdGroupCriterionService")

    operations = []
    for kw in keywords:
        operation = client.get_type("AdGroupCriterionOperation")
        criterion = operation.create
        criterion.ad_group = f"customers/{customer_id}/adGroups/{ad_group_id}"
        criterion.status = client.enums.AdGroupCriterionStatusEnum.ENABLED

        # Set keyword
        criterion.keyword.text = kw["text"]
        criterion.keyword.match_type = getattr(
            client.enums.KeywordMatchTypeEnum,
            kw["match_type"].upper()
        )

        # Optional: set bid
        if "bid_micros" in kw:
            criterion.cpc_bid_micros = kw["bid_micros"]

        operations.append(operation)

    response = ad_group_criterion_service.mutate_ad_group_criteria(
        customer_id=customer_id,
        operations=operations
    )

    return [r.resource_name for r in response.results]
```

## Add Negative Keywords

```python
def add_negative_keywords(client, customer_id, campaign_id, keywords):
    """Add negative keywords at campaign level."""
    campaign_criterion_service = client.get_service("CampaignCriterionService")

    operations = []
    for text in keywords:
        operation = client.get_type("CampaignCriterionOperation")
        criterion = operation.create
        criterion.campaign = f"customers/{customer_id}/campaigns/{campaign_id}"
        criterion.negative = True
        criterion.keyword.text = text
        criterion.keyword.match_type = (
            client.enums.KeywordMatchTypeEnum.BROAD
        )

        operations.append(operation)

    response = campaign_criterion_service.mutate_campaign_criteria(
        customer_id=customer_id,
        operations=operations
    )

    return [r.resource_name for r in response.results]
```

## Keyword Research with Keyword Planner

```python
def get_keyword_ideas(client, customer_id, keywords, location_ids, language_id):
    """Get keyword ideas from Keyword Planner.

    Args:
        keywords: Seed keywords list
        location_ids: Geographic targeting (e.g., ["2840"] for USA)
        language_id: Language code (e.g., "1000" for English)
    """
    keyword_plan_idea_service = client.get_service("KeywordPlanIdeaService")

    request = client.get_type("GenerateKeywordIdeasRequest")
    request.customer_id = customer_id
    request.language = f"languageConstants/{language_id}"

    # Add location targeting
    for loc_id in location_ids:
        request.geo_target_constants.append(
            f"geoTargetConstants/{loc_id}"
        )

    # Seed keywords
    request.keyword_seed.keywords.extend(keywords)

    # Get ideas
    response = keyword_plan_idea_service.generate_keyword_ideas(
        request=request
    )

    ideas = []
    for idea in response:
        ideas.append({
            "keyword": idea.text,
            "avg_monthly_searches": idea.keyword_idea_metrics.avg_monthly_searches,
            "competition": idea.keyword_idea_metrics.competition.name,
            "low_bid_micros": idea.keyword_idea_metrics.low_top_of_page_bid_micros,
            "high_bid_micros": idea.keyword_idea_metrics.high_top_of_page_bid_micros
        })

    return ideas
```

## Quality Score

```python
def get_keyword_quality_scores(client, customer_id, campaign_id):
    """Get quality scores for keywords."""
    ga_service = client.get_service("GoogleAdsService")

    query = f"""
        SELECT
            ad_group_criterion.keyword.text,
            ad_group_criterion.quality_info.quality_score,
            ad_group_criterion.quality_info.creative_quality_score,
            ad_group_criterion.quality_info.search_predicted_ctr,
            ad_group_criterion.quality_info.post_click_quality_score
        FROM keyword_view
        WHERE campaign.id = {campaign_id}
        AND ad_group_criterion.status != 'REMOVED'
    """

    response = ga_service.search(customer_id=customer_id, query=query)

    keywords = []
    for row in response:
        criterion = row.ad_group_criterion
        keywords.append({
            "keyword": criterion.keyword.text,
            "quality_score": criterion.quality_info.quality_score,
            "creative_quality": criterion.quality_info.creative_quality_score.name,
            "expected_ctr": criterion.quality_info.search_predicted_ctr.name,
            "landing_page": criterion.quality_info.post_click_quality_score.name
        })

    return keywords
```

---

# Section 6: Bidding Strategies

## Strategy Types

| Strategy | Type | Best For |
|----------|------|----------|
| Manual CPC | Manual | Full control |
| Enhanced CPC | Semi-auto | Manual + conversions boost |
| Maximize Clicks | Automated | Traffic focus |
| Maximize Conversions | Automated | Conversion focus |
| Target CPA | Automated | Cost per acquisition goal |
| Target ROAS | Automated | Return on ad spend goal |
| Maximize Conversion Value | Automated | Revenue optimization |

## Create Portfolio Bidding Strategy

```python
def create_target_cpa_strategy(client, customer_id, name, target_cpa_micros):
    """Create a Target CPA portfolio bidding strategy."""
    bidding_strategy_service = client.get_service("BiddingStrategyService")

    operation = client.get_type("BiddingStrategyOperation")
    strategy = operation.create
    strategy.name = name
    strategy.type_ = client.enums.BiddingStrategyTypeEnum.TARGET_CPA
    strategy.target_cpa.target_cpa_micros = target_cpa_micros

    # Optional: set CPC bid ceiling
    strategy.target_cpa.cpc_bid_ceiling_micros = target_cpa_micros * 2

    response = bidding_strategy_service.mutate_bidding_strategies(
        customer_id=customer_id,
        operations=[operation]
    )

    return response.results[0].resource_name
```

## Apply Bidding Strategy to Campaign

```python
def set_campaign_bidding_strategy(client, customer_id, campaign_id, strategy_resource):
    """Apply a portfolio bidding strategy to a campaign."""
    campaign_service = client.get_service("CampaignService")

    operation = client.get_type("CampaignOperation")
    campaign = operation.update
    campaign.resource_name = f"customers/{customer_id}/campaigns/{campaign_id}"
    campaign.bidding_strategy = strategy_resource

    client.copy_from(
        operation.update_mask,
        protobuf_helpers.field_mask(None, campaign._pb)
    )

    response = campaign_service.mutate_campaigns(
        customer_id=customer_id,
        operations=[operation]
    )

    return response.results[0].resource_name
```

## Bid Adjustments

```python
def set_device_bid_adjustment(client, customer_id, campaign_id, device, modifier):
    """Set bid adjustment for a device type.

    Args:
        device: MOBILE, DESKTOP, TABLET
        modifier: Bid modifier (1.0 = no change, 1.2 = +20%, 0.8 = -20%)
    """
    campaign_criterion_service = client.get_service("CampaignCriterionService")

    operation = client.get_type("CampaignCriterionOperation")
    criterion = operation.create
    criterion.campaign = f"customers/{customer_id}/campaigns/{campaign_id}"
    criterion.device.type_ = getattr(
        client.enums.DeviceEnum, device.upper()
    )
    criterion.bid_modifier = modifier

    response = campaign_criterion_service.mutate_campaign_criteria(
        customer_id=customer_id,
        operations=[operation]
    )

    return response.results[0].resource_name
```

---

# Section 7: Conversion Tracking

## Conversion Action Types

| Type | Description |
|------|-------------|
| WEBSITE | Website actions (purchases, signups) |
| APP_INSTALL | Mobile app installs |
| APP_IN_APP_PURCHASE | In-app purchases |
| CALL_FROM_ADS | Calls from ads |
| STORE_VISIT | Physical store visits |
| UPLOAD | Offline conversions |

## Create Conversion Action

```python
def create_conversion_action(client, customer_id, name, category, value=None):
    """Create a conversion action for tracking.

    Args:
        category: PURCHASE, SIGNUP, LEAD, PAGE_VIEW, etc.
        value: Default conversion value (optional)
    """
    conversion_action_service = client.get_service("ConversionActionService")

    operation = client.get_type("ConversionActionOperation")
    action = operation.create
    action.name = name
    action.category = getattr(
        client.enums.ConversionActionCategoryEnum,
        category.upper()
    )
    action.type_ = client.enums.ConversionActionTypeEnum.WEBPAGE
    action.status = client.enums.ConversionActionStatusEnum.ENABLED

    # Counting
    action.counting_type = (
        client.enums.ConversionActionCountingTypeEnum.ONE_PER_CLICK
    )

    # Attribution
    action.attribution_model_settings.attribution_model = (
        client.enums.AttributionModelEnum.GOOGLE_ADS_LAST_CLICK
    )
    action.attribution_model_settings.data_driven_model_status = (
        client.enums.DataDrivenModelStatusEnum.UNKNOWN
    )

    # Value
    if value:
        action.value_settings.default_value = value
        action.value_settings.always_use_default_value = False

    # Click-through window (days)
    action.click_through_lookback_window_days = 30

    response = conversion_action_service.mutate_conversion_actions(
        customer_id=customer_id,
        operations=[operation]
    )

    return response.results[0].resource_name
```

## Get Conversion Tag

```python
def get_conversion_tag(client, customer_id, conversion_action_id):
    """Get the tracking tag for a conversion action."""
    ga_service = client.get_service("GoogleAdsService")

    query = f"""
        SELECT
            conversion_action.id,
            conversion_action.name,
            conversion_action.tag_snippets
        FROM conversion_action
        WHERE conversion_action.id = {conversion_action_id}
    """

    response = ga_service.search(customer_id=customer_id, query=query)

    for row in response:
        return row.conversion_action.tag_snippets
```

## Upload Offline Conversions

```python
def upload_offline_conversions(client, customer_id, conversions):
    """Upload offline conversions.

    Args:
        conversions: List of dicts with gclid, conversion_action,
                     conversion_date_time, conversion_value
    """
    conversion_upload_service = client.get_service("ConversionUploadService")

    click_conversions = []
    for conv in conversions:
        click_conversion = client.get_type("ClickConversion")
        click_conversion.gclid = conv["gclid"]
        click_conversion.conversion_action = (
            f"customers/{customer_id}/conversionActions/{conv['conversion_action_id']}"
        )
        click_conversion.conversion_date_time = conv["conversion_date_time"]
        click_conversion.conversion_value = conv.get("conversion_value", 0)
        click_conversion.currency_code = conv.get("currency", "USD")

        click_conversions.append(click_conversion)

    request = client.get_type("UploadClickConversionsRequest")
    request.customer_id = customer_id
    request.conversions = click_conversions
    request.partial_failure = True

    response = conversion_upload_service.upload_click_conversions(
        request=request
    )

    return response
```

---

# Section 8: Google Analytics Integration

## Link Google Analytics 4

```python
def create_ga4_link(client, customer_id, ga4_property_id):
    """Link Google Ads to Google Analytics 4 property."""
    google_ads_link_service = client.get_service("GoogleAdsLinkService")

    # Note: GA4 linking is typically done through GA4 Admin API
    # Google Ads API reads existing links

    ga_service = client.get_service("GoogleAdsService")

    query = """
        SELECT
            customer.id,
            customer_manager_link.manager_customer,
            customer_manager_link.status
        FROM customer_manager_link
    """

    # Actual GA4 linking requires Google Analytics Admin API
    pass
```

## Import GA4 Conversions

GA4 conversions can be imported to Google Ads through the Google Ads UI or Admin API.

Steps:
1. In GA4, mark events as conversions
2. In Google Ads, go to Tools > Conversions
3. Click + New conversion action > Import > Google Analytics 4 properties
4. Select the conversions to import

## Query Imported Conversions

```python
def get_analytics_conversions(client, customer_id, date_range):
    """Get conversion data including imported GA4 conversions."""
    ga_service = client.get_service("GoogleAdsService")

    query = f"""
        SELECT
            campaign.name,
            segments.conversion_action,
            segments.conversion_action_category,
            metrics.conversions,
            metrics.conversions_value
        FROM campaign
        WHERE segments.date BETWEEN '{date_range[0]}' AND '{date_range[1]}'
        AND metrics.conversions > 0
    """

    response = ga_service.search(customer_id=customer_id, query=query)

    conversions = []
    for row in response:
        conversions.append({
            "campaign": row.campaign.name,
            "action": row.segments.conversion_action,
            "category": row.segments.conversion_action_category.name,
            "conversions": row.metrics.conversions,
            "value": row.metrics.conversions_value
        })

    return conversions
```

---

# Section 9: Reporting

## GAQL (Google Ads Query Language)

### Query Structure

```sql
SELECT field1, field2, metrics.clicks
FROM resource
WHERE conditions
ORDER BY field
LIMIT n
```

### Common Resources

| Resource | Description |
|----------|-------------|
| campaign | Campaign-level data |
| ad_group | Ad group-level data |
| ad_group_ad | Ad-level data |
| keyword_view | Keyword performance |
| search_term_view | Search query data |
| geographic_view | Geographic performance |
| audience | Audience targeting |

### Key Metrics

| Metric | Description |
|--------|-------------|
| metrics.impressions | Ad impressions |
| metrics.clicks | Ad clicks |
| metrics.cost_micros | Cost in micros (divide by 1M) |
| metrics.ctr | Click-through rate |
| metrics.average_cpc | Average cost per click |
| metrics.conversions | Conversion count |
| metrics.conversions_value | Conversion value |
| metrics.cost_per_conversion | Cost per conversion |
| metrics.conversion_rate | Conversion rate |
| metrics.roas | Return on ad spend |

## Report Examples

### Campaign Performance Report

```python
def get_campaign_performance(client, customer_id, start_date, end_date):
    """Get campaign performance metrics."""
    ga_service = client.get_service("GoogleAdsService")

    query = f"""
        SELECT
            campaign.id,
            campaign.name,
            campaign.status,
            metrics.impressions,
            metrics.clicks,
            metrics.ctr,
            metrics.cost_micros,
            metrics.conversions,
            metrics.cost_per_conversion,
            metrics.conversions_value
        FROM campaign
        WHERE segments.date BETWEEN '{start_date}' AND '{end_date}'
        AND campaign.status != 'REMOVED'
        ORDER BY metrics.cost_micros DESC
    """

    response = ga_service.search_stream(customer_id=customer_id, query=query)

    results = []
    for batch in response:
        for row in batch.results:
            results.append({
                "campaign_id": row.campaign.id,
                "campaign_name": row.campaign.name,
                "status": row.campaign.status.name,
                "impressions": row.metrics.impressions,
                "clicks": row.metrics.clicks,
                "ctr": row.metrics.ctr,
                "cost": row.metrics.cost_micros / 1_000_000,
                "conversions": row.metrics.conversions,
                "cpa": row.metrics.cost_per_conversion / 1_000_000 if row.metrics.cost_per_conversion else 0,
                "conv_value": row.metrics.conversions_value
            })

    return results
```

### Search Terms Report

```python
def get_search_terms_report(client, customer_id, campaign_id, start_date, end_date):
    """Get search terms that triggered ads."""
    ga_service = client.get_service("GoogleAdsService")

    query = f"""
        SELECT
            search_term_view.search_term,
            search_term_view.status,
            campaign.name,
            ad_group.name,
            metrics.impressions,
            metrics.clicks,
            metrics.cost_micros,
            metrics.conversions
        FROM search_term_view
        WHERE campaign.id = {campaign_id}
        AND segments.date BETWEEN '{start_date}' AND '{end_date}'
        ORDER BY metrics.impressions DESC
        LIMIT 100
    """

    response = ga_service.search(customer_id=customer_id, query=query)

    terms = []
    for row in response:
        terms.append({
            "search_term": row.search_term_view.search_term,
            "status": row.search_term_view.status.name,
            "campaign": row.campaign.name,
            "ad_group": row.ad_group.name,
            "impressions": row.metrics.impressions,
            "clicks": row.metrics.clicks,
            "cost": row.metrics.cost_micros / 1_000_000,
            "conversions": row.metrics.conversions
        })

    return terms
```

### Geographic Report

```python
def get_geographic_report(client, customer_id, start_date, end_date):
    """Get performance by geographic location."""
    ga_service = client.get_service("GoogleAdsService")

    query = f"""
        SELECT
            geographic_view.country_criterion_id,
            geographic_view.location_type,
            campaign.name,
            metrics.impressions,
            metrics.clicks,
            metrics.cost_micros,
            metrics.conversions
        FROM geographic_view
        WHERE segments.date BETWEEN '{start_date}' AND '{end_date}'
        ORDER BY metrics.cost_micros DESC
    """

    response = ga_service.search(customer_id=customer_id, query=query)

    locations = []
    for row in response:
        locations.append({
            "country_id": row.geographic_view.country_criterion_id,
            "location_type": row.geographic_view.location_type.name,
            "campaign": row.campaign.name,
            "impressions": row.metrics.impressions,
            "clicks": row.metrics.clicks,
            "cost": row.metrics.cost_micros / 1_000_000,
            "conversions": row.metrics.conversions
        })

    return locations
```

---

# Section 10: Automation Patterns

## Batch Operations

```python
def batch_update_keywords(client, customer_id, updates):
    """Batch update multiple keywords efficiently.

    Args:
        updates: List of dicts with ad_group_id, criterion_id, new_bid
    """
    ad_group_criterion_service = client.get_service("AdGroupCriterionService")

    operations = []
    for update in updates:
        operation = client.get_type("AdGroupCriterionOperation")
        criterion = operation.update
        criterion.resource_name = (
            f"customers/{customer_id}/adGroupCriteria/"
            f"{update['ad_group_id']}~{update['criterion_id']}"
        )
        criterion.cpc_bid_micros = update["new_bid"]

        client.copy_from(
            operation.update_mask,
            protobuf_helpers.field_mask(None, criterion._pb)
        )

        operations.append(operation)

    # Process in batches of 5000 (API limit)
    batch_size = 5000
    results = []

    for i in range(0, len(operations), batch_size):
        batch = operations[i:i + batch_size]
        response = ad_group_criterion_service.mutate_ad_group_criteria(
            customer_id=customer_id,
            operations=batch
        )
        results.extend(response.results)

    return results
```

## Scheduled Scripts Pattern

```python
import schedule
import time

def daily_performance_check(client, customer_id, thresholds):
    """Daily check for campaigns exceeding thresholds."""
    campaigns = get_campaign_performance(
        client,
        customer_id,
        get_yesterday(),
        get_yesterday()
    )

    alerts = []
    for campaign in campaigns:
        if campaign["cpa"] > thresholds["max_cpa"]:
            alerts.append(f"High CPA: {campaign['campaign_name']} - ${campaign['cpa']:.2f}")

        if campaign["ctr"] < thresholds["min_ctr"]:
            alerts.append(f"Low CTR: {campaign['campaign_name']} - {campaign['ctr']:.2%}")

    if alerts:
        send_alert_email(alerts)

def auto_pause_poor_performers(client, customer_id, min_conversions, max_cpa):
    """Automatically pause keywords with poor performance."""
    ga_service = client.get_service("GoogleAdsService")

    query = f"""
        SELECT
            ad_group_criterion.resource_name,
            ad_group_criterion.keyword.text,
            metrics.conversions,
            metrics.cost_per_conversion
        FROM keyword_view
        WHERE metrics.impressions > 1000
        AND metrics.conversions < {min_conversions}
        AND metrics.cost_per_conversion > {max_cpa * 1_000_000}
        AND ad_group_criterion.status = 'ENABLED'
    """

    response = ga_service.search(customer_id=customer_id, query=query)

    operations = []
    for row in response:
        operation = client.get_type("AdGroupCriterionOperation")
        criterion = operation.update
        criterion.resource_name = row.ad_group_criterion.resource_name
        criterion.status = client.enums.AdGroupCriterionStatusEnum.PAUSED

        client.copy_from(
            operation.update_mask,
            protobuf_helpers.field_mask(None, criterion._pb)
        )

        operations.append(operation)

    if operations:
        ad_group_criterion_service = client.get_service("AdGroupCriterionService")
        ad_group_criterion_service.mutate_ad_group_criteria(
            customer_id=customer_id,
            operations=operations
        )

# Schedule automation
schedule.every().day.at("08:00").do(daily_performance_check, client, customer_id, thresholds)
schedule.every().day.at("23:00").do(auto_pause_poor_performers, client, customer_id, 1, 50)

while True:
    schedule.run_pending()
    time.sleep(60)
```

## Change History Monitoring

```python
def get_recent_changes(client, customer_id, resource_type, days=7):
    """Get recent changes to account resources."""
    ga_service = client.get_service("GoogleAdsService")

    query = f"""
        SELECT
            change_event.change_date_time,
            change_event.change_resource_type,
            change_event.change_resource_name,
            change_event.client_type,
            change_event.user_email,
            change_event.changed_fields,
            change_event.old_resource,
            change_event.new_resource
        FROM change_event
        WHERE change_event.change_date_time DURING LAST_{days}_DAYS
        AND change_event.change_resource_type = '{resource_type}'
        ORDER BY change_event.change_date_time DESC
        LIMIT 100
    """

    response = ga_service.search(customer_id=customer_id, query=query)

    changes = []
    for row in response:
        changes.append({
            "datetime": row.change_event.change_date_time,
            "resource_type": row.change_event.change_resource_type.name,
            "resource_name": row.change_event.change_resource_name,
            "client": row.change_event.client_type.name,
            "user": row.change_event.user_email,
            "changed_fields": row.change_event.changed_fields
        })

    return changes
```

---

# Section 11: Error Handling

## Common Errors

| Error Code | Description | Solution |
|------------|-------------|----------|
| AUTHENTICATION_ERROR | Invalid credentials | Check tokens, refresh OAuth |
| AUTHORIZATION_ERROR | Insufficient permissions | Verify account access |
| REQUEST_ERROR | Malformed request | Check request structure |
| QUOTA_ERROR | Rate limit exceeded | Implement backoff |
| INTERNAL_ERROR | Server error | Retry with backoff |
| RESOURCE_NOT_FOUND | Invalid resource | Verify resource exists |

## Error Handling Pattern

```python
from google.ads.googleads.errors import GoogleAdsException
import time

def with_retry(func, max_retries=3, initial_delay=1):
    """Retry decorator for API calls."""
    def wrapper(*args, **kwargs):
        delay = initial_delay
        last_exception = None

        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except GoogleAdsException as ex:
                last_exception = ex

                # Check if retryable
                for error in ex.failure.errors:
                    error_code = error.error_code

                    # Quota errors - always retry
                    if error_code.quota_error:
                        time.sleep(delay)
                        delay *= 2
                        continue

                    # Internal errors - retry
                    if error_code.internal_error:
                        time.sleep(delay)
                        delay *= 2
                        continue

                    # Authentication - don't retry
                    if error_code.authentication_error:
                        raise

                    # Authorization - don't retry
                    if error_code.authorization_error:
                        raise

                # Log and continue retry
                print(f"Attempt {attempt + 1} failed: {ex.message}")
                time.sleep(delay)
                delay *= 2

        raise last_exception

    return wrapper

def handle_api_error(ex):
    """Process GoogleAdsException and return actionable info."""
    errors = []

    for error in ex.failure.errors:
        error_info = {
            "code": str(error.error_code),
            "message": error.message,
            "trigger": error.trigger.string_value if error.trigger else None,
            "location": error.location.field_path_elements if error.location else None
        }
        errors.append(error_info)

    return {
        "request_id": ex.request_id,
        "errors": errors
    }
```

## Rate Limiting

```python
import threading
from collections import deque
from datetime import datetime, timedelta

class RateLimiter:
    """Rate limiter for Google Ads API calls."""

    def __init__(self, max_requests_per_day=15000):
        self.max_requests = max_requests_per_day
        self.requests = deque()
        self.lock = threading.Lock()

    def acquire(self):
        """Acquire permission to make a request."""
        with self.lock:
            now = datetime.now()
            day_ago = now - timedelta(days=1)

            # Remove old requests
            while self.requests and self.requests[0] < day_ago:
                self.requests.popleft()

            # Check limit
            if len(self.requests) >= self.max_requests:
                wait_time = (self.requests[0] + timedelta(days=1) - now).total_seconds()
                raise Exception(f"Rate limit reached. Wait {wait_time:.0f} seconds.")

            # Record request
            self.requests.append(now)

    def remaining(self):
        """Get remaining requests for today."""
        with self.lock:
            now = datetime.now()
            day_ago = now - timedelta(days=1)

            while self.requests and self.requests[0] < day_ago:
                self.requests.popleft()

            return self.max_requests - len(self.requests)
```

---

# Section 12: Best Practices

## Account Structure

- Use Manager Accounts (MCC) for multi-account management
- Organize campaigns by objective (brand, non-brand, remarketing)
- Use consistent naming conventions
- Limit ad groups to 15-20 keywords each

## API Usage

- Use `search_stream` for large result sets
- Batch operations (up to 5000 per request)
- Implement exponential backoff for retries
- Cache frequently accessed data
- Use partial responses to reduce payload

## Performance Optimization

```python
# Use search_stream for large queries
def get_large_report(client, customer_id, query):
    ga_service = client.get_service("GoogleAdsService")

    # search_stream returns batches, more efficient for large data
    stream = ga_service.search_stream(customer_id=customer_id, query=query)

    results = []
    for batch in stream:
        for row in batch.results:
            results.append(process_row(row))

    return results

# Select only needed fields
def efficient_query():
    # Good - specific fields
    return """
        SELECT campaign.id, campaign.name, metrics.clicks
        FROM campaign
    """

    # Bad - too many fields
    # SELECT * FROM campaign

# Use parallel requests for independent operations
from concurrent.futures import ThreadPoolExecutor

def get_multiple_reports(client, customer_ids, query):
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {
            executor.submit(get_report, client, cid, query): cid
            for cid in customer_ids
        }

        results = {}
        for future in futures:
            cid = futures[future]
            results[cid] = future.result()

        return results
```

## Security

- Store credentials in environment variables or secrets manager
- Use service accounts for server-to-server auth
- Implement audit logging for all changes
- Review access permissions regularly
- Never expose developer tokens in client-side code

---

# Quick Reference

## API Versions

| Version | Status | End of Life |
|---------|--------|-------------|
| v18 | Current | Active |
| v17 | Supported | TBD |
| v16 | Deprecated | Soon |

## Useful Links

| Resource | URL |
|----------|-----|
| API Documentation | developers.google.com/google-ads/api |
| GAQL Reference | developers.google.com/google-ads/api/docs/query |
| Python Client | github.com/googleads/google-ads-python |
| Node.js Client | github.com/googleads/google-ads-api |
| Rate Limits | developers.google.com/google-ads/api/docs/rate-limits |

## Location IDs (Common)

| Country | ID |
|---------|-----|
| United States | 2840 |
| United Kingdom | 2826 |
| Canada | 2124 |
| Australia | 2036 |
| Germany | 2276 |
| France | 2250 |

## Language IDs (Common)

| Language | ID |
|----------|-----|
| English | 1000 |
| Spanish | 1003 |
| French | 1002 |
| German | 1001 |
| Portuguese | 1014 |

---

*faion-google-ads-skill v1.0*
*Technical Skill (Layer 3)*
*Used by: faion-ads-agent*
