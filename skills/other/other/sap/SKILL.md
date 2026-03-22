---
name: sap
description: >-
  Integrate with SAP systems and build extensions. Use when a user asks to
  connect to SAP S/4HANA, SAP Business One, or SAP ERP via OData, RFC, BAPI, or
  IDoc interfaces, build SAP BTP (Business Technology Platform) applications,
  work with SAP CAP (Cloud Application Programming), consume SAP APIs from the
  API Business Hub, manage master data, automate procurement or sales processes,
  build Fiori apps, extract SAP data for analytics, or integrate SAP with
  external systems. Covers S/4HANA APIs, Business One, BTP, CAP, and integration
  patterns.
license: Apache-2.0
compatibility: 'Node.js 18+ (SAP Cloud SDK), any HTTP client (OData APIs)'
metadata:
  author: terminal-skills
  version: 1.0.0
  category: business
  tags:
    - sap
    - erp
    - s4hana
    - odata
    - btp
---

# SAP

## Overview

Integrate with SAP — the enterprise ERP backbone. This skill covers SAP S/4HANA Cloud and on-premise APIs (OData V2/V4, BAPI/RFC), SAP Business One (Service Layer), SAP BTP application development, SAP CAP (Cloud Application Programming model), SAP Cloud SDK for JavaScript/TypeScript, master data management, procurement and sales document automation, and integration patterns for connecting SAP with external systems.

## Instructions

### Step 1: Authentication & Connectivity

**S/4HANA Cloud — OAuth2 Client Credentials:**
```bash
export SAP_TOKEN_URL="https://your-tenant.authentication.eu10.hana.ondemand.com/oauth/token"
export SAP_CLIENT_ID="client-id"
export SAP_CLIENT_SECRET="client-secret"
export SAP_BASE_URL="https://my-s4hana.com/sap/opu/odata/sap"
```

```typescript
async function getSAPToken() {
  const res = await fetch(process.env.SAP_TOKEN_URL!, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
      Authorization: "Basic " + Buffer.from(`${SAP_CLIENT_ID}:${SAP_CLIENT_SECRET}`).toString("base64"),
    },
    body: "grant_type=client_credentials",
  });
  return (await res.json()).access_token;
}

async function sapApi(method: string, path: string, token: string, body?: any) {
  const res = await fetch(`${process.env.SAP_BASE_URL}${path}`, {
    method,
    headers: {
      Authorization: `Bearer ${token}`, "Content-Type": "application/json", Accept: "application/json",
      ...(method !== "GET" ? { "X-CSRF-Token": await getCSRFToken(token) } : {}),
    },
    body: body ? JSON.stringify(body) : undefined,
  });
  if (!res.ok) throw new Error(`SAP ${res.status}: ${await res.text()}`);
  return res.json();
}
```

**SAP Business One — Service Layer:**
```typescript
const B1_URL = "https://your-b1-server:50000/b1s/v1";

async function b1Login() {
  const res = await fetch(`${B1_URL}/Login`, {
    method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ CompanyDB: "SBODemoUS", UserName: "manager", Password: "password" }),
  });
  return res.headers.get("set-cookie"); // Session cookie
}

async function b1Api(method: string, path: string, session: string, body?: any) {
  const res = await fetch(`${B1_URL}${path}`, {
    method, headers: { "Content-Type": "application/json", Cookie: session },
    body: body ? JSON.stringify(body) : undefined,
  });
  return res.json();
}
```

### Step 2: S/4HANA OData APIs

**Business Partners:**
```typescript
const customers = await sapApi("GET",
  "/API_BUSINESS_PARTNER/A_BusinessPartner?$filter=BusinessPartnerCategory eq '1'&$select=BusinessPartner,BusinessPartnerFullName,Industry&$top=50", token);

await sapApi("POST", "/API_BUSINESS_PARTNER/A_BusinessPartner", token, {
  BusinessPartnerCategory: "1", BusinessPartnerFullName: "TechStart GmbH",
  SearchTerm1: "TECHSTART", Industry: "IT",
  to_BusinessPartnerAddress: [{ Country: "DE", CityName: "Berlin", StreetName: "Friedrichstraße", HouseNumber: "123", PostalCode: "10117" }],
});
```

**Sales Orders:**
```typescript
await sapApi("POST", "/API_SALES_ORDER_SRV/A_SalesOrder", token, {
  SalesOrderType: "OR", SalesOrganization: "1010", DistributionChannel: "10",
  SoldToParty: "CUSTOMER_BP_ID", PurchaseOrderByCustomer: "PO-2026-001",
  to_Item: [
    { Material: "TG11", RequestedQuantity: "10", RequestedQuantityUnit: "EA", NetPriceAmount: "100.00", NetPriceCurrency: "EUR" },
    { Material: "TG12", RequestedQuantity: "5", RequestedQuantityUnit: "EA", NetPriceAmount: "250.00", NetPriceCurrency: "EUR" },
  ],
});
```

**Purchase Orders & Material Master:**
```typescript
await sapApi("POST", "/API_PURCHASEORDER_PROCESS_SRV/A_PurchaseOrder", token, {
  PurchaseOrderType: "NB", CompanyCode: "1010", Supplier: "VENDOR_BP_ID",
  to_PurchaseOrderItem: [{ Material: "RAW-001", OrderQuantity: "1000", PurchaseOrderQuantityUnit: "KG",
    NetPriceAmount: "5.50", DocumentCurrency: "EUR", Plant: "1010" }],
});

const material = await sapApi("GET", "/API_PRODUCT_SRV/A_Product('TG11')?$expand=to_Description,to_Plant", token);
```

### Step 3: SAP Business One Operations

```typescript
// Sales order → invoice → payment flow
const order = await b1Api("POST", "/Orders", session, {
  CardCode: "C20000", DocDate: "2026-02-18",
  DocumentLines: [
    { ItemCode: "A00001", Quantity: 10, UnitPrice: 100 },
    { ItemCode: "A00002", Quantity: 5, UnitPrice: 250 },
  ],
});

const invoice = await b1Api("POST", "/Invoices", session, {
  CardCode: "C20000",
  DocumentLines: [
    { BaseType: 17, BaseEntry: order.DocEntry, BaseLine: 0 },
    { BaseType: 17, BaseEntry: order.DocEntry, BaseLine: 1 },
  ],
});

await b1Api("POST", "/IncomingPayments", session, {
  CardCode: "C20000", DocDate: "2026-02-18", CashSum: 1750,
  PaymentInvoices: [{ DocEntry: invoice.DocEntry, SumApplied: 1750, InvoiceType: "it_Invoice" }],
});
```

### Step 4: SAP CAP (Cloud Application Programming)

```bash
npm install -g @sap/cds-dk
cds init my-project && cd my-project && npm install
```

**Data model** (`db/schema.cds`):
```cds
namespace my.project;
entity Products { key ID: UUID; name: String(100); price: Decimal(10,2); stock: Integer; category: Association to Categories; }
entity Categories { key ID: UUID; name: String(50); products: Association to many Products on products.category = $self; }
entity Orders { key ID: UUID; orderDate: Date; customer: String(100); status: String(20) default 'New';
  items: Composition of many OrderItems on items.order = $self; totalAmount: Decimal(12,2); }
entity OrderItems { key ID: UUID; order: Association to Orders; product: Association to Products; quantity: Integer; unitPrice: Decimal(10,2); }
```

**Service logic** (`srv/catalog-service.js`):
```javascript
const cds = require("@sap/cds");
module.exports = class CatalogService extends cds.ApplicationService {
  init() {
    const { Products, Orders } = this.entities;
    this.before("CREATE", Orders, async (req) => {
      for (const item of req.data.items) {
        const product = await SELECT.one.from(Products).where({ ID: item.product_ID });
        if (!product) throw req.reject(404, `Product ${item.product_ID} not found`);
        if (product.stock < item.quantity) throw req.reject(409, `Insufficient stock for ${product.name}`);
        item.unitPrice = product.price;
      }
      req.data.totalAmount = req.data.items.reduce((s, i) => s + i.unitPrice * i.quantity, 0);
    });
    this.after("CREATE", Orders, async (order) => {
      for (const item of order.items)
        await UPDATE(Products).set({ stock: { "-=": item.quantity } }).where({ ID: item.product_ID });
    });
    return super.init();
  }
};
```

Run locally: `cds watch` → API at `http://localhost:4004/catalog`.

### Step 5: Integration Patterns

**SAP → External (polling):**
```typescript
import cron from "node-cron";
let lastCheck = new Date().toISOString();
cron.schedule("*/5 * * * *", async () => {
  const token = await getSAPToken();
  const orders = await sapApi("GET",
    `/API_SALES_ORDER_SRV/A_SalesOrder?$filter=CreationDate gt datetime'${lastCheck}'&$expand=to_Item`, token);
  for (const order of orders.d.results) {
    await externalApi.createOrder({ sapOrderId: order.SalesOrder, customer: order.SoldToParty,
      items: order.to_Item.results.map((i: any) => ({ material: i.Material, quantity: parseFloat(i.OrderQuantity) })),
    });
  }
  lastCheck = new Date().toISOString();
});
```

**External → SAP (Shopify webhook):**
```typescript
app.post("/webhook/shopify/order", async (req, res) => {
  const token = await getSAPToken();
  const items = req.body.line_items.map((item: any) => ({
    Material: item.sku, RequestedQuantity: String(item.quantity),
    NetPriceAmount: String(item.price), NetPriceCurrency: req.body.currency,
  }));
  await sapApi("POST", "/API_SALES_ORDER_SRV/A_SalesOrder", token, {
    SalesOrderType: "OR", SalesOrganization: "1010", DistributionChannel: "10",
    SoldToParty: "CUSTOMER_BP_ID", to_Item: items,
  });
  res.sendStatus(200);
});
```

## Examples

### Example 1: Automated procurement workflow with inventory checks

**User prompt:** "When our warehouse stock for material RAW-001 drops below 500 KG, automatically create a purchase order to our primary vendor for 2000 KG. Check stock daily and log every PO created."

The agent will set up a cron job that runs daily, querying the SAP Product API for material RAW-001's current stock level. If stock is below 500, it will create a purchase order via the Purchase Order API with the vendor BP ID, 2000 KG quantity, the standard plant and storage location, and log the PO number and creation date. It will also check for any existing open POs for the same material to avoid duplicate orders.

### Example 2: E-commerce to SAP sales order sync

**User prompt:** "Build a webhook endpoint that receives Shopify orders and creates matching sales orders in S/4HANA with all line items mapped by SKU to SAP material numbers, including a customer lookup by email."

The agent will create an Express POST endpoint that receives Shopify order webhooks, extracts customer email and line items, queries the Business Partner API to find an existing customer by email (or creates a new one), maps each Shopify line item's SKU to an SAP material number, and creates a sales order via the Sales Order API with all items, quantities, prices, and the customer reference. It will return a 200 status and log the SAP sales order number for reconciliation.

## Guidelines

- **Always fetch a CSRF token before write operations** — S/4HANA on-premise requires an `X-CSRF-Token: Fetch` GET request before any POST/PATCH/DELETE; cache the token and refresh on 403 responses.
- **Use `$select` and `$top` on all OData queries** — SAP OData endpoints return all fields by default, which is slow for entities with hundreds of columns; always limit fields and page size.
- **Handle SAP date formats carefully** — OData V2 uses `/Date(timestamp)/` format while V4 uses ISO 8601; parse dates explicitly rather than relying on automatic conversion.
- **Use SAP Cloud SDK for type safety** — the generated VDM (Virtual Data Model) clients provide compile-time checking of field names, filters, and navigation properties.
- **Rate-limit polling integrations** — SAP systems have finite OData throughput; poll no more frequently than every 5 minutes and use `$filter` on timestamps to minimize payload size.
- **Test against the SAP API Business Hub sandbox** — use `api.sap.com` sandbox endpoints during development to avoid impacting production or QA systems.
