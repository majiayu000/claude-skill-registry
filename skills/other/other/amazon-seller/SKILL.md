---
name: Amazon Seller
description: Automate Amazon seller operations including inventory, orders, pricing, and advertising management
version: 1.0.0
author: Claude Office Skills
category: e-commerce
tags:
  - amazon
  - fba
  - inventory
  - advertising
  - e-commerce
department: operations
models:
  - claude-3-opus
  - claude-3-sonnet
  - gpt-4
mcp:
  server: ecommerce-mcp
  tools:
    - amazon_sp_api
    - amazon_ads_api
    - amazon_inventory
    - amazon_orders
capabilities:
  - Inventory management
  - Order processing
  - Pricing automation
  - PPC campaign management
input:
  - Product listings
  - Inventory data
  - Order information
  - Ad campaigns
output:
  - Inventory reports
  - Sales analytics
  - Ad performance
  - Profit calculations
languages:
  - en
related_skills:
  - shopify-automation
  - woocommerce-automation
  - inventory-management
---

# Amazon Seller

Comprehensive skill for automating Amazon seller operations and FBA management.

## Core Workflows

### 1. Seller Central Pipeline

```
AMAZON SELLER OPERATIONS:
┌─────────────────────────────────────────────────────────┐
│                    LISTING MANAGEMENT                    │
│  Create → Optimize → Price → Inventory → Monitor        │
└────────────────────────┬────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────┐
│                    ORDER FULFILLMENT                     │
│  FBA: Amazon handles │ FBM: Seller handles              │
└────────────────────────┬────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────┐
│                    ADVERTISING (PPC)                     │
│  Sponsored Products │ Brands │ Display                  │
└────────────────────────┬────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────┐
│                    ANALYTICS & GROWTH                    │
│  Sales Reports │ Profit Analysis │ Market Research      │
└─────────────────────────────────────────────────────────┘
```

### 2. Automation Triggers

```yaml
automations:
  - name: low_stock_alert
    trigger:
      metric: fba_inventory
      condition: "< 14_days_supply"
    actions:
      - send_alert: slack
      - create_shipment_plan
      - reorder_from_supplier
      
  - name: price_adjustment
    trigger:
      event: competitor_price_change
      threshold: 5%
    actions:
      - recalculate_price
      - update_listing
      - log_change
      
  - name: review_request
    trigger:
      event: order_delivered
      delay: 7_days
    actions:
      - check_return_status
      - send_review_request
```

## Product Listing Management

### Listing Optimization

```yaml
listing_template:
  title:
    format: "{{brand}} {{product_name}} - {{key_feature}} | {{variant}}"
    max_chars: 200
    rules:
      - capitalize_first_word
      - no_promotional_phrases
      - include_main_keywords
      
  bullet_points:
    count: 5
    format: |
      • {{benefit}} - {{feature_description}}
    guidelines:
      - Start with key benefit
      - Include dimensions/specs
      - Address common questions
      - Use relevant keywords
      
  description:
    format: enhanced_brand_content  # or basic_html
    sections:
      - brand_story
      - key_features
      - specifications
      - usage_instructions
      
  backend_keywords:
    max_bytes: 250
    strategy:
      - Include misspellings
      - Add synonyms
      - No punctuation
      - No repeated words
```

### Keyword Research

```yaml
keyword_strategy:
  tools:
    - helium10
    - jungle_scout
    - amazon_brand_analytics
    
  categories:
    primary_keywords:
      - High search volume
      - High relevance
      - Moderate competition
      
    secondary_keywords:
      - Long-tail variations
      - Question phrases
      - Comparison keywords
      
    backend_keywords:
      - Misspellings
      - Abbreviations
      - Foreign translations
      
  tracking:
    monitor_rankings: daily
    track_competitors: weekly
```

## Inventory Management

### FBA Inventory Planning

```yaml
inventory_planning:
  reorder_rules:
    - sku: "PROD-001"
      reorder_point: 30_days_supply
      target_stock: 90_days_supply
      lead_time: 21_days
      min_order_qty: 500
      
  storage_optimization:
    aged_inventory:
      threshold: 180_days
      actions:
        - create_removal_order
        - run_promotion
        - adjust_price
        
    storage_fees:
      monitor: monthly
      optimize_for: Q4  # Holiday season
      
  shipment_automation:
    trigger: stock_below_reorder
    workflow:
      - calculate_quantity
      - create_shipment_plan
      - generate_labels
      - notify_warehouse
```

### Inventory Dashboard

```
FBA INVENTORY STATUS
═══════════════════════════════════════

OVERVIEW:
Total SKUs:        245
In Stock:          198
Low Stock:         32
Out of Stock:      15

INVENTORY HEALTH:
Healthy           ██████████████░░ 78%
Excess            ████░░░░░░░░░░░░ 12%
Stranded          ██░░░░░░░░░░░░░░ 6%
Aged (180+ days)  █░░░░░░░░░░░░░░░ 4%

TOP SELLERS (Days of Supply):
┌──────────────────┬───────────┬──────────┐
│ Product          │ Stock     │ Days     │
├──────────────────┼───────────┼──────────┤
│ Widget Pro       │ 1,245     │ 28 ⚠️    │
│ Gadget Plus      │ 856       │ 45 ✓     │
│ Accessory Kit    │ 2,340     │ 120 📈   │
└──────────────────┴───────────┴──────────┘

RECOMMENDED ACTIONS:
• Reorder Widget Pro (28 days supply)
• Create removal for excess Accessory Kit
• Investigate 15 stranded SKUs
```

## Pricing Strategy

### Dynamic Pricing

```yaml
pricing_rules:
  - name: compete_for_buy_box
    conditions:
      - has_buy_box: false
      - competitor_price: "<= my_price"
    action:
      adjust: match_lowest - $0.01
      floor: min_profit_price
      
  - name: demand_based
    conditions:
      - sales_velocity: "> 2x_average"
      - stock_level: "> 60_days"
    action:
      adjust: "+5%"
      ceiling: max_price
      
  - name: clearance
    conditions:
      - stock_age: "> 150_days"
      - sales_velocity: "< 0.5x_average"
    action:
      adjust: "-15%"
      floor: cost + fees
```

### Profit Calculator

```yaml
profit_calculation:
  revenue:
    - sale_price
    - shipping_credit
    
  costs:
    - product_cost
    - shipping_to_fba
    - fba_fulfillment_fee
    - referral_fee
    - storage_fee
    - advertising_cost
    
  formula: |
    Profit = Sale Price
             - Product Cost
             - FBA Fee (size-based)
             - Referral Fee (15% typical)
             - Storage Fee (monthly)
             - Inbound Shipping
             - PPC Cost (ACoS-based)
             
  example:
    sale_price: $29.99
    product_cost: $8.00
    fba_fee: $4.75
    referral_fee: $4.50
    storage_fee: $0.25
    shipping: $1.50
    ppc_cost: $2.00
    profit: $8.99 (30% margin)
```

## Advertising (PPC)

### Campaign Structure

```yaml
ppc_structure:
  sponsored_products:
    auto_campaigns:
      - name: "{{product}}_Auto_Research"
        targeting: auto
        budget: $20/day
        purpose: keyword_discovery
        
    manual_campaigns:
      - name: "{{product}}_Exact"
        match_type: exact
        keywords: top_performers
        budget: $50/day
        
      - name: "{{product}}_Phrase"
        match_type: phrase
        keywords: mid_performers
        budget: $30/day
        
      - name: "{{product}}_Broad"
        match_type: broad
        keywords: discovery
        budget: $20/day
        
  bid_optimization:
    target_acos: 25%
    rules:
      - condition: "acos < 20%"
        action: "increase_bid_10%"
      - condition: "acos > 35%"
        action: "decrease_bid_15%"
      - condition: "no_sales_7_days"
        action: "pause_keyword"
```

### PPC Dashboard

```
PPC PERFORMANCE - LAST 30 DAYS
═══════════════════════════════════════

OVERVIEW:
Spend:        $4,523
Sales:        $18,750
ACoS:         24.1%
TACoS:        8.2%
Orders:       625

BY CAMPAIGN TYPE:
Sponsored Products  ████████████████ $3,200
Sponsored Brands    ████░░░░░░░░░░░░ $823
Sponsored Display   ██░░░░░░░░░░░░░░ $500

TOP KEYWORDS:
┌────────────────────┬────────┬───────┬──────┐
│ Keyword            │ Spend  │ Sales │ ACoS │
├────────────────────┼────────┼───────┼──────┤
│ wireless charger   │ $450   │ $2,100│ 21%  │
│ fast charging pad  │ $320   │ $1,450│ 22%  │
│ phone charger      │ $280   │ $980  │ 29%  │
└────────────────────┴────────┴───────┴──────┘

RECOMMENDATIONS:
• Increase bid on "wireless charger" (+15%)
• Add negative: "car charger" (0 conversions)
• Test new keyword: "qi charger" (competitor)
```

## Order Management

### Order Processing

```yaml
order_workflows:
  fba_orders:
    # Amazon handles fulfillment
    automation:
      - monitor_returns
      - respond_to_messages
      - request_reviews
      
  fbm_orders:
    # Seller handles fulfillment
    workflow:
      - receive_order
      - pick_pack
      - generate_label
      - ship_order
      - confirm_shipment
      - upload_tracking
      
  multi_channel:
    # FBA for non-Amazon orders
    sources:
      - shopify
      - ebay
      - website
    action: create_mcf_order
```

### Customer Communication

```yaml
messaging_automation:
  order_shipped:
    delay: immediate
    template: |
      Hi {{buyer_name}},
      
      Your order has shipped! Here's your tracking: {{tracking}}
      
      Estimated delivery: {{delivery_date}}
      
      Thank you for your purchase!
      
  review_request:
    delay: 7_days_after_delivery
    conditions:
      - no_return_requested
      - no_negative_feedback
    template: seller_central_request_review
```

## Analytics & Reporting

### Sales Dashboard

```
SALES PERFORMANCE - THIS MONTH
═══════════════════════════════════════

Revenue:      $45,230 (+12% MoM)
Units:        1,892 (+8% MoM)
Orders:       1,654 (+10% MoM)

PROFIT BREAKDOWN:
Gross Revenue    $45,230
- Product Cost   $15,200 (33.6%)
- Amazon Fees    $12,450 (27.5%)
- Advertising    $3,680 (8.1%)
= Net Profit     $13,900 (30.7%)

BY PRODUCT:
Widget Pro    ████████████░░░░ $18,500
Gadget Plus   ████████░░░░░░░░ $12,300
Accessory     ██████░░░░░░░░░░ $8,430
Bundle        ████░░░░░░░░░░░░ $6,000

BUY BOX %:
Widget Pro    ████████████████ 95%
Gadget Plus   ██████████████░░ 88%
Accessory     ████████████░░░░ 78%
```

## API Integration

### SP-API Examples

```python
# List Orders
orders = sp_api.orders.get_orders(
    MarketplaceIds=["ATVPDKIKX0DER"],
    CreatedAfter="2024-01-01T00:00:00Z",
    OrderStatuses=["Unshipped", "PartiallyShipped"]
)

# Update Inventory
sp_api.fba_inventory.create_inbound_shipment_plan(
    ShipFromAddress=warehouse_address,
    InboundShipmentPlanRequestItems=[
        {
            "SellerSKU": "PROD-001",
            "Quantity": 500
        }
    ]
)

# Get Product Fees
fees = sp_api.products.get_my_fees_estimate_for_sku(
    SellerSKU="PROD-001",
    MarketplaceId="ATVPDKIKX0DER",
    PriceToEstimateFees={"ListingPrice": {"Amount": 29.99}}
)
```

## Best Practices

1. **Optimize Listings**: Keywords, images, A+ content
2. **Monitor Buy Box**: Maintain competitive pricing
3. **Manage Inventory**: Avoid stockouts and excess
4. **Control ACoS**: Optimize PPC efficiency
5. **Respond Quickly**: 24-hour message response
6. **Track Metrics**: Daily sales and profit review
7. **Plan for Seasons**: Q4 inventory prep
8. **Stay Compliant**: Follow Amazon policies
