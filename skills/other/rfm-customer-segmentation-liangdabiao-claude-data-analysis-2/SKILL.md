---
name: rfm-customer-segmentation
description: Perform RFM (Recency, Frequency, Monetary) customer segmentation analysis on e-commerce data. Use when you need to analyze customer value, identify VIP customers, or create marketing segments. Automatically cleans data, calculates RFM metrics, applies K-means clustering, and generates visualization reports with Chinese language support.
allowed-tools: Read, Write, Bash, Glob
---

# RFM Customer Segmentation Analysis

A comprehensive customer segmentation skill that automatically analyzes e-commerce transaction data to identify customer value segments using RFM (Recency, Frequency, Monetary) analysis with K-means clustering.

## Instructions

### 1. Data Analysis
When users provide e-commerce data or ask about customer segmentation:
- Load and validate the transaction data
- Clean data by removing invalid orders (negative quantities, zero prices)
- Calculate RFM metrics for each customer:
  - **Recency**: Days since last purchase
  - **Frequency**: Number of purchases
  - **Monetary**: Total purchase amount
- Use K-means clustering on RFM dimensions
- Automatically determine optimal number of clusters using elbow method

### 2. Customer Segmentation
- Create customer value segments: High, Medium, Low value customers
- Score each customer on RFM dimensions (1-3 scale)
- Calculate overall customer value scores
- Identify and rank VIP customers for marketing campaigns

### 3. Visualization and Reporting
- Generate comprehensive customer segmentation dashboard
- Create pie charts for segment distribution and revenue share
- Build RFM scatter plots to visualize customer patterns
- Generate box plots showing value distribution by segment
- Export detailed CSV reports with VIP customer lists

### 4. Marketing Insights
- Provide actionable marketing recommendations for each segment
- Generate executive summary with key findings
- Create customer activation strategies for different value tiers
- Export VIP customer lists for targeted marketing campaigns

## Usage Examples

### Basic Customer Segmentation
```
Analyze these e-commerce orders and segment customers by value:
[CSV data with order_id, user_id, purchase_date, quantity, unit_price]
```

### VIP Customer Identification
```
Find the top 100 most valuable customers from our sales data for marketing campaign
```

### Customer Value Analysis
```
Create a customer segmentation report showing revenue contribution by customer segment
```

## Key Features

- **Automatic Data Cleaning**: Handles Chinese e-commerce data formats, removes invalid orders
- **Intelligent Clustering**: Uses elbow method to determine optimal cluster count
- **Chinese Language Support**: Full support for Chinese field names and visualizations
- **Comprehensive Reports**: Generates HTML reports, PNG dashboards, and CSV exports
- **Marketing Ready**: Provides VIP customer lists and actionable insights

## File Requirements

The skill works with e-commerce transaction data containing:
- **user_id**: Customer identification code (用户码)
- **order_date**: Purchase date (消费日期)
- **quantity**: Order quantity (数量)
- **unit_price**: Item unit price (单价)
- **product_info**: Product details (optional)

## Output Files Generated

- `customer_segments.csv`: Complete customer segmentation data
- `vip_customers_list.csv`: Ranked VIP customer list for marketing
- `segment_summary_statistics.csv`: Detailed statistics by segment
- `customer_segmentation_dashboard.png`: Visual analytics dashboard
- `data_validation_report.txt`: Data quality and analysis validation

## Dependencies

- pandas, numpy for data processing
- scikit-learn for K-means clustering
- matplotlib, seaborn for visualization (with Chinese font support)
- Standard Python libraries for file operations

## Best Practices

- Ensure date fields are in consistent format (YYYY-MM-DD recommended)
- Remove or handle missing values before analysis
- Use sufficient data volume (1000+ orders recommended for reliable clustering)
- Consider business context when interpreting segment results
- Validate results with domain knowledge when possible