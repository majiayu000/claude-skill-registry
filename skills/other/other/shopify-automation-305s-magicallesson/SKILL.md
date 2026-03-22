---
name: shopify-automation
description: "Shopify e-commerce automation - inventory management, order processing, customer workflows, and analytics"
version: "1.0.0"
author: claude-office-skills
license: MIT

category: ecommerce
tags:
  - shopify
  - ecommerce
  - inventory
  - orders
  - automation
department: Operations

models:
  recommended:
    - claude-sonnet-4

mcp:
  server: shopify-mcp
  tools:
    - shopify_orders
    - shopify_inventory
    - shopify_customers
    - shopify_products

capabilities:
  - inventory_management
  - order_processing
  - customer_automation
  - analytics_reporting
  - multi_channel_sync

languages:
  - en
  - zh

related_skills:
  - email-marketing
  - crm-automation
  - sheets-automation
---

# Shopify Automation

Comprehensive Shopify e-commerce automation covering inventory management, order processing, customer workflows, and analytics. Based on n8n's e-commerce workflow templates.

## Overview

This skill covers:
- Inventory management and alerts
- Order processing automation
- Customer lifecycle workflows
- Multi-channel synchronization
- Analytics and reporting

---

## Inventory Management

### Low Stock Alerts

```yaml
workflow: "Inventory Alert System"
schedule: "Daily 9am"

steps:
  1. fetch_inventory:
      shopify:
        endpoint: products
        include: variants
        
  2. filter_low_stock:
      condition: inventory_quantity <= reorder_threshold
      default_threshold: 10
      
  3. categorize_urgency:
      critical: inventory_quantity <= 5
      warning: inventory_quantity <= 10
      
  4. generate_report:
      group_by: [category, urgency]
      
  5. notify:
      slack:
        channel: "#inventory-alerts"
        message: |
          ⚠️ *Low Stock Alert*
          
          🚨 *Critical (≤5 units):*
          {critical_items}
          
          ⚠️ *Warning (≤10 units):*
          {warning_items}
          
          [View in Shopify]({admin_link})
          
  6. create_purchase_orders:
      if: auto_reorder_enabled
      template: generate_po_for_each_supplier
```

### Predictive Reordering

```yaml
workflow: "Smart Inventory Reordering"

analysis:
  data_sources:
    - sales_history: last_90_days
    - seasonal_trends: year_over_year
    - current_velocity: last_14_days
    
  calculations:
    daily_sales_rate: avg(units_sold_per_day)
    days_of_stock: current_inventory / daily_sales_rate
    reorder_point: daily_sales_rate * lead_time * safety_factor
    
  safety_factor:
    high_velocity: 1.5
    normal: 1.3
    slow_moving: 1.1
    
actions:
  auto_reorder:
    condition: days_of_stock <= lead_time + buffer
    action: generate_purchase_order
    notify: purchasing_team
```

---

## Order Processing

### Order Fulfillment Workflow

```yaml
workflow: "Order Processing Pipeline"
trigger: shopify_order_created

steps:
  1. validate_order:
      checks:
        - fraud_score: < threshold
        - inventory_available: true
        - payment_captured: true
        
  2. categorize_order:
      rules:
        - high_value: total > $500
        - international: country != home_country
        - expedited: shipping_method == "express"
        - subscription: has_subscription_items
        
  3. assign_fulfillment:
      routing:
        - if: international
          warehouse: international_hub
        - if: expedited
          priority: high
        - default:
          warehouse: nearest_to_customer
          
  4. create_shipping_label:
      carrier: based_on_service_level
      integrate: [shipstation, easypost, shippo]
      
  5. update_inventory:
      action: decrement_stock
      
  6. notify_customer:
      email: order_confirmation_template
      sms: if_opted_in
      
  7. update_systems:
      - accounting: create_invoice
      - crm: update_customer_record
      - analytics: log_order_data
```

### Order Status Automation

```yaml
order_status_notifications:
  confirmed:
    delay: immediate
    email: "Thank you for your order!"
    
  processing:
    delay: when_status_changes
    email: "We're preparing your order"
    
  shipped:
    delay: immediate
    email: |
      Your order is on the way!
      Tracking: {tracking_number}
      Carrier: {carrier}
      Estimated delivery: {eta}
    sms: "Your order shipped! Track: {tracking_url}"
    
  delivered:
    delay: 1_day_after_delivery
    email: "How was your order? Leave a review!"
    
  delayed:
    trigger: no_tracking_update_3_days
    action: proactive_customer_outreach
```

---

## Customer Workflows

### Post-Purchase Sequence

```yaml
workflow: "Post-Purchase Engagement"

sequence:
  day_0:
    trigger: order_delivered
    action: 
      - email: delivery_confirmation
      - start_review_timer
      
  day_3:
    action:
      - email: review_request
        template: |
          Hi {first_name},
          
          How are you enjoying your {product_name}?
          
          We'd love to hear your thoughts!
          [Leave a Review]({review_link})
          
  day_7:
    condition: no_review_submitted
    action:
      - email: review_reminder
      - offer: 10%_off_next_order
      
  day_14:
    action:
      - email: related_products
        personalization: based_on_purchase
        
  day_30:
    condition: consumable_product
    action:
      - email: replenishment_reminder
        discount: returning_customer
```

### Customer Segmentation

```yaml
segmentation:
  vip:
    criteria:
      - total_spent: >= $1000
      - orders: >= 5
    actions:
      - tag: "VIP"
      - add_to_list: "VIP Customers"
      - priority_support: true
      - early_access: new_products
      
  at_risk:
    criteria:
      - last_order: > 90_days
      - previous_orders: >= 2
    actions:
      - tag: "Win-Back"
      - email_sequence: reactivation
      - offer: special_discount
      
  new_customers:
    criteria:
      - orders: 1
      - days_since_first_order: <= 30
    actions:
      - email_sequence: onboarding
      - recommend: best_sellers
      
  wholesale:
    criteria:
      - average_order_value: >= $500
      - orders: >= 3
    actions:
      - tag: "B2B Potential"
      - notify: sales_team
```

---

## Multi-Channel Sync

### Inventory Sync

```yaml
multi_channel_inventory:
  platforms:
    - shopify: primary
    - amazon: secondary
    - ebay: secondary
    - walmart: secondary
    
  sync_rules:
    frequency: real_time
    buffer_stock: 5_units  # Safety buffer
    
    allocation:
      shopify: 100%  # Full inventory
      amazon: available - buffer
      ebay: available - buffer
      walmart: available - buffer
      
  actions:
    on_sale:
      - update_all_channels: immediately
      - if_stockout: pause_listings
      
    on_restock:
      - update_all_channels: immediately
      - reactivate_listings: if_paused
```

### Price Sync

```yaml
price_synchronization:
  base_price: shopify
  
  channel_adjustments:
    amazon:
      markup: +15%  # Account for fees
      
    ebay:
      markup: +10%
      
    wholesale:
      discount: -30%
      
  automation:
    - on_price_change: sync_all_channels
    - competitor_monitoring: optional
    - dynamic_pricing: based_on_demand
```

---

## Analytics & Reporting

### Daily Sales Report

```yaml
workflow: "Daily Sales Report"
schedule: "8am daily"

metrics:
  revenue:
    - total_sales
    - average_order_value
    - comparison_vs_yesterday
    - comparison_vs_same_day_last_week
    
  orders:
    - order_count
    - units_sold
    - new_vs_returning_customers
    
  products:
    - top_sellers
    - low_performers
    - out_of_stock_items
    
  channels:
    - by_source: [direct, google, facebook, email]
    - conversion_rates
    
output:
  format: |
    📊 *Daily Sales Report - {date}*
    
    💰 *Revenue*
    Today: ${total_sales} ({change_vs_yesterday})
    AOV: ${aov}
    
    📦 *Orders*
    Count: {order_count}
    New customers: {new_customers}
    
    🏆 *Top Products*
    1. {product_1} - {units_1} units
    2. {product_2} - {units_2} units
    3. {product_3} - {units_3} units
    
    ⚠️ *Attention*
    - {low_stock_count} products low stock
    - {abandoned_carts} abandoned carts (${value})
    
  destinations:
    - slack: "#daily-sales"
    - email: leadership_team
    - google_sheets: sales_tracker
```

### Abandoned Cart Recovery

```yaml
workflow: "Cart Recovery"

trigger: cart_abandoned
wait: 1_hour

sequence:
  email_1:
    delay: 1_hour
    subject: "Forgot something? 🛒"
    content: |
      Hi {first_name},
      
      You left these items in your cart:
      {cart_items}
      
      [Complete Your Order]({checkout_link})
      
  email_2:
    delay: 24_hours
    condition: cart_not_recovered
    subject: "Your cart is waiting"
    offer: free_shipping
    
  email_3:
    delay: 72_hours
    condition: cart_not_recovered
    subject: "Last chance - 10% off your cart"
    offer: 10_percent_discount
    expiry: 24_hours

tracking:
  metrics:
    - recovery_rate
    - revenue_recovered
    - best_performing_offer
```

---

## Output Example

**Request**: "Set up Shopify inventory alerts"

**Output**:

```markdown
# Shopify Inventory Alert System

## Workflow Configuration

```yaml
name: "Low Stock Monitor"
schedule: "Daily 9am + On inventory change"
```

## Alert Rules

| Urgency | Threshold | Action |
|---------|-----------|--------|
| 🚨 Critical | ≤ 5 units | Immediate Slack + Email |
| ⚠️ Warning | ≤ 10 units | Daily digest |
| 📋 Monitor | ≤ 20 units | Weekly report |

## Sample Alert

```
🚨 CRITICAL STOCK ALERT

Product: Blue Widget (SKU: BW-001)
Current Stock: 3 units
Daily Sales Avg: 5 units
Days of Stock: 0.6 days

⚠️ WARNING STOCK (5 items)
• Red Widget - 8 units (1.6 days)
• Green Widget - 9 units (3 days)
...

📊 Recommended Actions:
1. Reorder Blue Widget immediately
2. Review Red Widget demand
3. Contact supplier for Green Widget ETA

[View Inventory Dashboard]
[Generate Purchase Orders]
```

## n8n Implementation

```yaml
nodes:
  1. Schedule Trigger (Daily 9am)
  2. Shopify - Get Products
  3. Filter - Low Stock Items
  4. IF - Check Urgency Level
  5. Slack - Send Alert
  6. Google Sheets - Log Data
```

Ready to implement?
```

---

*Shopify Automation Skill - Part of Claude Office Skills*
