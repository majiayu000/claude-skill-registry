---
name: fullstory-element-properties
version: v2
description: Comprehensive guide for implementing Fullstory's Element Properties API across Web, Android, and iOS platforms. Teaches proper type handling, schema construction, value formatting, and platform-specific patterns including view/cell reuse. Includes detailed good/bad examples for e-commerce, forms, and dynamic content to help developers add semantic decoration to their apps and capture business-relevant properties on interactive elements.
related_skills:
  - fullstory-page-properties
  - fullstory-user-properties
  - fullstory-analytics-events
  - fullstory-data-scoping-decoration
  - fullstory-privacy-controls
  - fullstory-ecommerce
  - fullstory-saas
---

# Fullstory Element Properties API

## Overview

Fullstory's Element Properties API allows developers to capture custom properties on UI elements that can be used for search, filtering, grouping, and analytics. Unlike standard attributes which are only used for CSS selectors, element properties become first-class data points for analysis, similar to user properties, page properties, and event properties.

This skill covers implementation across Web (Browser), Android, and iOS platforms.

## Core Concepts

### API Defined Elements

- API Defined Elements provide a programmatic approach to defining Elements in Fullstory
- Once created, these elements can be used across Fullstory features for search and analysis
- Elements are defined using the `data-fs-element` attribute with a name
- Element names are permanently attached to their associated Element (though display name can change)

### Element Properties vs Attributes

- **Attributes**: Used for CSS selectors and element matching only
- **Element Properties**: Can be used for filtering, grouping, and analytics
- Properties inherit from parent elements in the hierarchy
- The deepest property value is used when conflicts occur

### Key Features

1. Properties are captured on element interactions (clicks, taps, etc.)
2. Properties inherit down the element hierarchy
3. Multiple `data-fs-properties-schema` can be set in the same hierarchy
4. Properties automatically connect to Named Elements

### ⭐ Critical: Property Inheritance (Parent ↔ Child)

This is one of the most powerful features of Element Properties:

**Two-way inheritance:**

- **Parent → Child**: Properties defined on a parent element are inherited by all child elements
- **Child → Parent**: When an action occurs on a parent element, it captures properties from all defined child elements

```
┌─────────────────────────────────────────────────────────────────────┐
│  FORM (data-fs-element="checkout-form")                             │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  SHIPPING SELECT (selectedShipping="express")                │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  PAYMENT SELECT (selectedPayment="credit_card")              │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  GIFT WRAP CHECKBOX (giftWrap="true")                        │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  SUBMIT BUTTON (data-fs-element="submit-order")              │   │
│  │  ───────────────────────────────────────────────────────     │   │
│  │  When clicked, captures ALL properties from siblings:        │   │
│  │  • selectedShipping: "express"                               │   │
│  │  • selectedPayment: "credit_card"                            │   │
│  │  • giftWrap: true                                            │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**Why this matters for analytics:**

```html
<!-- Form with multiple selections and a submit button -->
<form data-fs-element="checkout-form">
  <select data-selected-shipping data-fs-properties-schema='{"data-selected-shipping": "str"}'>
    <option value="standard">Standard</option>
    <option value="express" selected>Express</option>
  </select>

  <select data-selected-payment data-fs-properties-schema='{"data-selected-payment": "str"}'>
    <option value="credit_card" selected>Credit Card</option>
    <option value="paypal">PayPal</option>
  </select>

  <label>
    <input
      type="checkbox"
      checked
      data-gift-wrap="true"
      data-fs-properties-schema='{"data-gift-wrap": "bool"}'
    />
    Gift wrap
  </label>

  <!-- Submit button inherits ALL properties from above -->
  <button type="submit" data-fs-element="submit-order">Place Order</button>
</form>
```

**In Fullstory, when "submit-order" is clicked:**

- The click event captures: `selectedShipping`, `selectedPayment`, `giftWrap`
- You can now create metrics like:
  - "Submit clicks WHERE selectedPayment = 'paypal'"
  - "Group submit clicks BY selectedShipping" → see which shipping option is most popular
  - "Funnel: visits → checkout-form viewed → submit-order clicked WHERE giftWrap = true"

> **Key Insight**: Define element properties on individual form fields, but the submit button (or any parent action element) will automatically capture the state of all child properties at the moment of interaction. This eliminates the need to manually aggregate form state.

## Platform-Specific Implementation

---

## WEB / BROWSER IMPLEMENTATION

### Basic Syntax

Element properties are defined using HTML data attributes:

- `data-fs-properties-schema`: JSON object defining which attributes to capture and their types
- `data-fs-element`: (Optional) Names the element for use in Fullstory

### Schema Structure

```json
{
  "attribute-name": "type",
  "attribute-name-2": {
    "type": "type_value",
    "name": "override_property_name"
  }
}
```

### Supported Value Types

| Type    | Description           | Examples                               |
| ------- | --------------------- | -------------------------------------- |
| `str`   | String value          | "foo", "bar", "foo@bar"                |
| `strs`  | Array of strings      | ["foo", "bar"]                         |
| `int`   | Integer               | 0, -123, 45                            |
| `ints`  | Array of integers     | [0, 1, 2]                              |
| `real`  | Float/decimal         | 12.345, -0.5                           |
| `reals` | Array of reals        | [12.345, 1]                            |
| `bool`  | Boolean               | true, false, 1, 0, t, f                |
| `bools` | Array of booleans     | [true, false]                          |
| `date`  | ISO8601 date/datetime | "2006-01-02T15:04:05Z"                 |
| `dates` | Array of dates        | ["2006-01-02", "2006-01-02T15:04:05Z"] |

### ✅ GOOD WEB IMPLEMENTATION EXAMPLES

#### Example 1: E-commerce Product Card

```html
<!-- GOOD: Comprehensive product card with proper typing and meaningful names -->
<div
  class="product-card"
  data-product-id="SKU-12345"
  data-product-name="Premium Wireless Headphones"
  data-product-category="Electronics"
  data-product-price="199.99"
  data-product-stock="15"
  data-product-rating="4.5"
  data-on-sale="true"
  data-launch-date="2024-01-15"
  data-tags='["wireless", "bluetooth", "noise-canceling"]'
  data-fs-properties-schema='{
    "data-product-id": {
      "type": "str",
      "name": "productId"
    },
    "data-product-name": {
      "type": "str",
      "name": "productName"
    },
    "data-product-category": {
      "type": "str",
      "name": "category"
    },
    "data-product-price": {
      "type": "real",
      "name": "price"
    },
    "data-product-stock": {
      "type": "int",
      "name": "stockLevel"
    },
    "data-product-rating": {
      "type": "real",
      "name": "rating"
    },
    "data-on-sale": {
      "type": "bool",
      "name": "isOnSale"
    },
    "data-launch-date": {
      "type": "date",
      "name": "launchDate"
    },
    "data-tags": {
      "type": "strs",
      "name": "productTags"
    }
  }'
  data-fs-element="Product Card"
>
  <button class="add-to-cart" data-fs-element="Add to Cart Button">Add to Cart</button>
</div>
```

**Why this is good:**

- ✅ Proper type mapping (real for price, int for stock, bool for sale status)
- ✅ Clean property names using the `name` override
- ✅ Captures both scalar and array values appropriately
- ✅ Named element for easy reference in Fullstory
- ✅ Child button inherits all parent properties
- ✅ Uses semantic attribute names that describe the data

#### Example 2: Form with Hierarchy

```html
<!-- GOOD: Form-level properties inherited by all fields -->
<form
  class="checkout-form"
  data-form-type="checkout"
  data-form-step="payment"
  data-user-tier="premium"
  data-fs-properties-schema='{
    "data-form-type": {
      "type": "str",
      "name": "formType"
    },
    "data-form-step": {
      "type": "str",
      "name": "checkoutStep"
    },
    "data-user-tier": {
      "type": "str",
      "name": "userTier"
    }
  }'
  data-fs-element="Checkout Form"
>
  <input
    type="text"
    name="cardNumber"
    data-field-name="cardNumber"
    data-field-required="true"
    data-field-validation="credit-card"
    data-fs-properties-schema='{
      "data-field-name": {
        "type": "str",
        "name": "fieldName"
      },
      "data-field-required": {
        "type": "bool",
        "name": "isRequired"
      },
      "data-field-validation": {
        "type": "str",
        "name": "validationType"
      }
    }'
    data-fs-element="Card Number Field"
  />

  <button
    type="submit"
    data-button-type="primary"
    data-fs-properties-schema='{
      "data-button-type": "str"
    }'
    data-fs-element="Submit Payment Button"
  >
    Complete Purchase
  </button>
</form>
```

**Why this is good:**

- ✅ Hierarchical property inheritance (form properties flow to all children)
- ✅ Each element has appropriate context-specific properties
- ✅ All interactions capture both element-specific and form-level context
- ✅ Clear separation of concerns (form context vs field specifics)

#### Example 3: Dynamic Content (React/Vue Pattern)

```javascript
// GOOD: Dynamically setting properties in a React component
function ProductCard({product}) {
  const schemaRef = useRef(null)

  useEffect(() => {
    if (schemaRef.current) {
      // Set the schema as a data attribute
      schemaRef.current.setAttribute(
        'data-fs-properties-schema',
        JSON.stringify({
          'data-product-id': {type: 'str', name: 'productId'},
          'data-product-name': {type: 'str', name: 'productName'},
          'data-price': {type: 'real', name: 'price'},
          'data-in-stock': {type: 'bool', name: 'inStock'},
          'data-variant-count': {type: 'int', name: 'variantCount'},
        }),
      )

      // Set the actual attribute values
      schemaRef.current.setAttribute('data-product-id', product.id)
      schemaRef.current.setAttribute('data-product-name', product.name)
      schemaRef.current.setAttribute('data-price', product.price.toString())
      schemaRef.current.setAttribute('data-in-stock', product.inStock.toString())
      schemaRef.current.setAttribute('data-variant-count', product.variants.length.toString())
      schemaRef.current.setAttribute('data-fs-element', 'Product Card')
    }
  }, [product])

  return (
    <div ref={schemaRef} className="product-card">
      {/* Component content */}
    </div>
  )
}
```

**Why this is good:**

- ✅ Properly handles dynamic data
- ✅ Sets schema first, then values
- ✅ Converts values to strings as required
- ✅ Uses appropriate types for each property
- ✅ Includes element naming

### ❌ BAD WEB IMPLEMENTATION EXAMPLES

#### Example 1: Common Type Mistakes

```html
<!-- BAD: Multiple type and naming issues -->
<button
  class="product-buy"
  data-price="$199.99"
  data-quantity="5 items"
  data-available="yes"
  data-fs-properties-schema='{
    "data-price": "str",
    "data-quantity": "int",
    "data-available": "bool"
  }'
  data-fs-element="Buy Button"
>
  Buy Now
</button>
```

**Why this is bad:**

- ❌ `data-price` contains "$" currency symbol but typed as string (should be real and clean numeric: "199.99")
- ❌ `data-quantity` contains "items" text but typed as int (should be clean number: "5")
- ❌ `data-available` uses "yes" instead of boolean value (should be "true" or "1")
- ❌ Lost ability to do numeric filtering, comparisons, and aggregations

**CORRECTED VERSION:**

```html
<!-- GOOD: Proper types and clean values -->
<button
  class="product-buy"
  data-price="199.99"
  data-quantity="5"
  data-available="true"
  data-currency="USD"
  data-fs-properties-schema='{
    "data-price": {
      "type": "real",
      "name": "price"
    },
    "data-quantity": {
      "type": "int",
      "name": "quantity"
    },
    "data-available": {
      "type": "bool",
      "name": "isAvailable"
    },
    "data-currency": {
      "type": "str",
      "name": "currency"
    }
  }'
  data-fs-element="Buy Button"
>
  Buy Now
</button>
```

#### Example 2: Over-capturing and Schema Bloat

```html
<!-- BAD: Capturing too many irrelevant properties -->
<div
  data-component-name="ProductCard"
  data-component-version="1.2.3"
  data-react-key="product-123"
  data-render-timestamp="2024-10-20T14:30:00Z"
  data-css-class="product-card mb-4 shadow-lg"
  data-developer-name="John Doe"
  data-git-commit="abc123def456"
  data-build-number="4567"
  data-product-id="SKU-123"
  data-product-name="Widget"
  data-fs-properties-schema='{
    "data-component-name": "str",
    "data-component-version": "str",
    "data-react-key": "str",
    "data-render-timestamp": "date",
    "data-css-class": "str",
    "data-developer-name": "str",
    "data-git-commit": "str",
    "data-build-number": "int",
    "data-product-id": "str",
    "data-product-name": "str"
  }'
></div>
```

**Why this is bad:**

- ❌ Captures technical/debug data not useful for analytics (component version, git commit, developer)
- ❌ Captures implementation details (react-key, css-class)
- ❌ Wastes property quota (limit of 50 per interaction, 500 total)
- ❌ Creates high cardinality issues (timestamp, git commits)
- ❌ Makes actual business data harder to find
- ❌ No meaningful names provided

**CORRECTED VERSION:**

```html
<!-- GOOD: Only business-relevant properties -->
<div
  data-product-id="SKU-123"
  data-product-name="Widget"
  data-product-category="Tools"
  data-product-price="29.99"
  data-fs-properties-schema='{
    "data-product-id": {
      "type": "str",
      "name": "productId"
    },
    "data-product-name": {
      "type": "str",
      "name": "productName"
    },
    "data-product-category": {
      "type": "str",
      "name": "category"
    },
    "data-product-price": {
      "type": "real",
      "name": "price"
    }
  }'
  data-fs-element="Product Card"
></div>
```

#### Example 3: Invalid JSON and Syntax Errors

```html
<!-- BAD: Multiple JSON and syntax errors -->
<button
  data-product-id="SKU-123"
  data-price="49.99"
  data-fs-properties-schema="{
    'data-product-id': 'str',
    "data-price": "real"
  }"
  data-fs-element="Add to Cart">
  Add to Cart
</button>
```

**Why this is bad:**

- ❌ Mixed single and double quotes in JSON (invalid JSON)
- ❌ JSON will fail to parse
- ❌ Properties won't be captured at all
- ❌ Silent failure - no console errors

**CORRECTED VERSION:**

```html
<!-- GOOD: Valid JSON with consistent quoting -->
<button
  data-product-id="SKU-123"
  data-price="49.99"
  data-fs-properties-schema='{
    "data-product-id": {
      "type": "str",
      "name": "productId"
    },
    "data-price": {
      "type": "real",
      "name": "price"
    }
  }'
  data-fs-element="Add to Cart"
>
  Add to Cart
</button>
```

#### Example 4: Missing Property Values

```html
<!-- BAD: Schema references attributes that don't exist -->
<button
  data-product-id="SKU-123"
  data-fs-properties-schema='{
    "data-product-id": "str",
    "data-product-name": "str",
    "data-price": "real",
    "data-category": "str"
  }'
  data-fs-element="Product Button"
>
  View Product
</button>
```

**Why this is bad:**

- ❌ Schema references `data-product-name`, `data-price`, `data-category` but these attributes don't exist
- ❌ Only `data-product-id` will be captured
- ❌ Incomplete data reduces analytics value
- ❌ Creates confusion about what's actually being captured

**CORRECTED VERSION:**

```html
<!-- GOOD: All referenced attributes exist -->
<button
  data-product-id="SKU-123"
  data-product-name="Premium Widget"
  data-price="49.99"
  data-category="Electronics"
  data-fs-properties-schema='{
    "data-product-id": {
      "type": "str",
      "name": "productId"
    },
    "data-product-name": {
      "type": "str",
      "name": "productName"
    },
    "data-price": {
      "type": "real",
      "name": "price"
    },
    "data-category": {
      "type": "str",
      "name": "category"
    }
  }'
  data-fs-element="Product Button"
>
  View Product
</button>
```

---

## ANDROID IMPLEMENTATION

### Basic Syntax

Element properties are set using the `FS.setAttribute()` method:

**Java:**

```java
public static void FS.setAttribute(View view, String attributeName, String attributeValue);
```

**Kotlin:**

```kotlin
fun FS.setAttribute(view: View, attributeName: String, attributeValue: String)
```

### ✅ GOOD ANDROID IMPLEMENTATION EXAMPLES

#### Example 1: Product Card with Comprehensive Properties (Java)

```java
// GOOD: Complete product card implementation with proper typing
public class ProductCardViewHolder extends RecyclerView.ViewHolder {
    private View cardView;

    public void bind(Product product) {
        cardView = itemView.findViewById(R.id.product_card);

        // Set individual attribute values
        FS.setAttribute(cardView, "data-product-id", product.getId());
        FS.setAttribute(cardView, "data-product-name", product.getName());
        FS.setAttribute(cardView, "data-category", product.getCategory());
        FS.setAttribute(cardView, "data-price", String.valueOf(product.getPrice()));
        FS.setAttribute(cardView, "data-stock-level", String.valueOf(product.getStockLevel()));
        FS.setAttribute(cardView, "data-rating", String.valueOf(product.getRating()));
        FS.setAttribute(cardView, "data-on-sale", String.valueOf(product.isOnSale()));
        FS.setAttribute(cardView, "data-launch-date", product.getLaunchDate().toString()); // ISO8601 format

        // Set the properties schema - defines types for all attributes
        String schema = new JSONObject()
            .put("data-product-id", new JSONObject()
                .put("type", "str")
                .put("name", "productId"))
            .put("data-product-name", new JSONObject()
                .put("type", "str")
                .put("name", "productName"))
            .put("data-category", new JSONObject()
                .put("type", "str")
                .put("name", "category"))
            .put("data-price", new JSONObject()
                .put("type", "real")
                .put("name", "price"))
            .put("data-stock-level", new JSONObject()
                .put("type", "int")
                .put("name", "stockLevel"))
            .put("data-rating", new JSONObject()
                .put("type", "real")
                .put("name", "rating"))
            .put("data-on-sale", new JSONObject()
                .put("type", "bool")
                .put("name", "isOnSale"))
            .put("data-launch-date", new JSONObject()
                .put("type", "date")
                .put("name", "launchDate"))
            .toString();

        FS.setAttribute(cardView, "data-fs-properties-schema", schema);

        // Name the element for easy reference in Fullstory
        FS.setAttribute(cardView, "data-fs-element", "Product Card");

        // Configure child button - will inherit parent properties
        Button addToCartBtn = itemView.findViewById(R.id.btn_add_to_cart);
        FS.setAttribute(addToCartBtn, "data-fs-element", "Add to Cart Button");
    }
}
```

**Why this is good:**

- ✅ Uses proper type conversions (String.valueOf for numbers/booleans)
- ✅ Provides clean property names via the `name` field
- ✅ Sets schema AFTER all attribute values are set
- ✅ Uses JSONObject for clean schema construction
- ✅ Child elements automatically inherit parent properties
- ✅ Includes element naming for both parent and child

#### Example 2: Form with Field-Level Properties (Kotlin)

```kotlin
// GOOD: Comprehensive form tracking with hierarchy
class CheckoutFormFragment : Fragment() {

    private fun setupFormTracking() {
        val formContainer = view?.findViewById<ViewGroup>(R.id.checkout_form)

        // Set form-level properties that all fields will inherit
        formContainer?.let { form ->
            FS.setAttribute(form, "data-form-type", "checkout")
            FS.setAttribute(form, "data-form-step", "payment")
            FS.setAttribute(form, "data-user-tier", "premium")
            FS.setAttribute(form, "data-total-amount", viewModel.cartTotal.toString())

            val formSchema = JSONObject().apply {
                put("data-form-type", JSONObject().put("type", "str").put("name", "formType"))
                put("data-form-step", JSONObject().put("type", "str").put("name", "checkoutStep"))
                put("data-user-tier", JSONObject().put("type", "str").put("name", "userTier"))
                put("data-total-amount", JSONObject().put("type", "real").put("name", "cartTotal"))
            }.toString()

            FS.setAttribute(form, "data-fs-properties-schema", formSchema)
            FS.setAttribute(form, "data-fs-element", "Checkout Form")
        }

        // Set field-specific properties
        val cardNumberField = view?.findViewById<EditText>(R.id.card_number_field)
        cardNumberField?.let { field ->
            FS.setAttribute(field, "data-field-name", "cardNumber")
            FS.setAttribute(field, "data-field-required", "true")
            FS.setAttribute(field, "data-field-type", "credit-card")
            FS.setAttribute(field, "data-max-length", "16")

            val fieldSchema = JSONObject().apply {
                put("data-field-name", JSONObject().put("type", "str").put("name", "fieldName"))
                put("data-field-required", JSONObject().put("type", "bool").put("name", "isRequired"))
                put("data-field-type", JSONObject().put("type", "str").put("name", "fieldType"))
                put("data-max-length", JSONObject().put("type", "int").put("name", "maxLength"))
            }.toString()

            FS.setAttribute(field, "data-fs-properties-schema", fieldSchema)
            FS.setAttribute(field, "data-fs-element", "Card Number Field")
        }

        // Submit button inherits form properties
        val submitButton = view?.findViewById<Button>(R.id.submit_payment)
        submitButton?.let { button ->
            FS.setAttribute(button, "data-button-type", "primary")
            FS.setAttribute(button, "data-button-action", "submit-payment")

            val buttonSchema = JSONObject().apply {
                put("data-button-type", "str")
                put("data-button-action", JSONObject().put("type", "str").put("name", "buttonAction"))
            }.toString()

            FS.setAttribute(button, "data-fs-properties-schema", buttonSchema)
            FS.setAttribute(button, "data-fs-element", "Submit Payment Button")
        }
    }
}
```

**Why this is good:**

- ✅ Clear hierarchy: form properties inherited by all children
- ✅ Each element has context-specific properties
- ✅ Proper Kotlin idiomatic code with safe calls
- ✅ Uses JSONObject.apply for clean schema building
- ✅ All interactions capture full context

#### Example 3: RecyclerView with Dynamic Content (Java)

```java
// GOOD: Handling dynamic list items with proper cleanup
public class ProductAdapter extends RecyclerView.Adapter<ProductAdapter.ViewHolder> {

    @Override
    public void onBindViewHolder(@NonNull ViewHolder holder, int position) {
        Product product = products.get(position);

        // Clear previous attributes (important for recycled views)
        holder.clearFullstoryAttributes();

        // Set new attributes
        holder.setProductProperties(product);
    }

    static class ViewHolder extends RecyclerView.ViewHolder {
        private List<String> appliedAttributes = new ArrayList<>();

        void setProductProperties(Product product) {
            View itemView = this.itemView;

            // Track which attributes we're setting
            appliedAttributes.clear();

            // Set attributes
            setAttribute(itemView, "data-product-id", product.getId());
            setAttribute(itemView, "data-product-name", product.getName());
            setAttribute(itemView, "data-price", String.valueOf(product.getPrice()));
            setAttribute(itemView, "data-in-stock", String.valueOf(product.isInStock()));
            setAttribute(itemView, "data-position", String.valueOf(getAdapterPosition()));

            // Build and set schema
            try {
                String schema = new JSONObject()
                    .put("data-product-id", new JSONObject().put("type", "str").put("name", "productId"))
                    .put("data-product-name", new JSONObject().put("type", "str").put("name", "productName"))
                    .put("data-price", new JSONObject().put("type", "real").put("name", "price"))
                    .put("data-in-stock", new JSONObject().put("type", "bool").put("name", "inStock"))
                    .put("data-position", new JSONObject().put("type", "int").put("name", "listPosition"))
                    .toString();

                setAttribute(itemView, "data-fs-properties-schema", schema);
                setAttribute(itemView, "data-fs-element", "Product List Item");
            } catch (JSONException e) {
                Log.e("ProductAdapter", "Error building properties schema", e);
            }
        }

        private void setAttribute(View view, String name, String value) {
            FS.setAttribute(view, name, value);
            appliedAttributes.add(name);
        }

        void clearFullstoryAttributes() {
            // Note: There's no official remove method, but setting empty values works
            for (String attr : appliedAttributes) {
                FS.setAttribute(itemView, attr, "");
            }
            appliedAttributes.clear();
        }
    }
}
```

**Why this is good:**

- ✅ Handles RecyclerView recycling correctly
- ✅ Clears old attributes before setting new ones
- ✅ Tracks applied attributes for cleanup
- ✅ Includes error handling for JSON construction
- ✅ Sets position in list for analytics context
- ✅ Proper type conversions throughout

### ❌ BAD ANDROID IMPLEMENTATION EXAMPLES

#### Example 1: Type Mismatches and String Contamination (Java)

```java
// BAD: Multiple type and formatting issues
public void bindProductCard(Product product) {
    View cardView = findViewById(R.id.product_card);

    // Setting formatted values instead of clean data
    FS.setAttribute(cardView, "data-price", "$" + product.getPrice()); // BAD: includes $
    FS.setAttribute(cardView, "data-stock", product.getStockLevel() + " items"); // BAD: includes "items"
    FS.setAttribute(cardView, "data-available", product.isInStock() ? "Yes" : "No"); // BAD: uses Yes/No not bool
    FS.setAttribute(cardView, "data-rating", product.getRating() + "/5 stars"); // BAD: includes text

    // Schema with wrong types
    String schema = "{" +
        "\"data-price\": \"str\"," +  // BAD: should be "real"
        "\"data-stock\": \"int\"," +   // BAD: value has text, will fail
        "\"data-available\": \"bool\"," + // BAD: value is "Yes"/"No" not boolean
        "\"data-rating\": \"str\"" +   // BAD: should be "real"
        "}";

    FS.setAttribute(cardView, "data-fs-properties-schema", schema);
    FS.setAttribute(cardView, "data-fs-element", "Product Card");
}
```

**Why this is bad:**

- ❌ Price includes "$" symbol but typed as string (loses ability to do numeric operations)
- ❌ Stock includes "items" text but typed as int (will fail parsing)
- ❌ Available uses "Yes"/"No" instead of boolean values
- ❌ Rating includes "/5 stars" text but typed as string (loses numeric analysis)
- ❌ Manual JSON string construction is error-prone
- ❌ No property name overrides for readability

**CORRECTED VERSION:**

```java
// GOOD: Clean values with proper types
public void bindProductCard(Product product) {
    View cardView = findViewById(R.id.product_card);

    // Set clean values
    FS.setAttribute(cardView, "data-price", String.valueOf(product.getPrice()));
    FS.setAttribute(cardView, "data-stock", String.valueOf(product.getStockLevel()));
    FS.setAttribute(cardView, "data-available", String.valueOf(product.isInStock()));
    FS.setAttribute(cardView, "data-rating", String.valueOf(product.getRating()));
    FS.setAttribute(cardView, "data-currency", "USD"); // Separate attribute for currency

    try {
        String schema = new JSONObject()
            .put("data-price", new JSONObject()
                .put("type", "real")
                .put("name", "price"))
            .put("data-stock", new JSONObject()
                .put("type", "int")
                .put("name", "stockLevel"))
            .put("data-available", new JSONObject()
                .put("type", "bool")
                .put("name", "isAvailable"))
            .put("data-rating", new JSONObject()
                .put("type", "real")
                .put("name", "rating"))
            .put("data-currency", new JSONObject()
                .put("type", "str")
                .put("name", "currency"))
            .toString();

        FS.setAttribute(cardView, "data-fs-properties-schema", schema);
        FS.setAttribute(cardView, "data-fs-element", "Product Card");
    } catch (JSONException e) {
        Log.e("ProductCard", "Error building schema", e);
    }
}
```

#### Example 2: Setting Schema Before Values (Kotlin)

```kotlin
// BAD: Setting schema before attribute values
fun setupProductCard(product: Product) {
    val cardView = findViewById<View>(R.id.product_card)

    // BAD: Setting schema first
    val schema = JSONObject().apply {
        put("data-product-id", "str")
        put("data-price", "real")
    }.toString()
    FS.setAttribute(cardView, "data-fs-properties-schema", schema)

    // Then setting values (TOO LATE - schema won't capture these properly)
    FS.setAttribute(cardView, "data-product-id", product.id)
    FS.setAttribute(cardView, "data-price", product.price.toString())

    FS.setAttribute(cardView, "data-fs-element", "Product Card")
}
```

**Why this is bad:**

- ❌ Schema is set before the actual attribute values
- ❌ May cause timing issues with property capture
- ❌ Best practice is to set values first, then schema

**CORRECTED VERSION:**

```kotlin
// GOOD: Setting values first, then schema
fun setupProductCard(product: Product) {
    val cardView = findViewById<View>(R.id.product_card)

    // Set attribute values FIRST
    FS.setAttribute(cardView, "data-product-id", product.id)
    FS.setAttribute(cardView, "data-price", product.price.toString())

    // Then set schema
    val schema = JSONObject().apply {
        put("data-product-id", JSONObject().put("type", "str").put("name", "productId"))
        put("data-price", JSONObject().put("type", "real").put("name", "price"))
    }.toString()
    FS.setAttribute(cardView, "data-fs-properties-schema", schema)

    // Finally name the element
    FS.setAttribute(cardView, "data-fs-element", "Product Card")
}
```

#### Example 3: Forgetting to Convert Numbers (Java)

```java
// BAD: Not converting primitive types to String
public void setupView(View view, int quantity, double price, boolean available) {
    // These will cause compilation errors
    FS.setAttribute(view, "data-quantity", quantity); // ERROR: expects String
    FS.setAttribute(view, "data-price", price); // ERROR: expects String
    FS.setAttribute(view, "data-available", available); // ERROR: expects String
}
```

**Why this is bad:**

- ❌ `FS.setAttribute()` expects String for all values
- ❌ Compilation errors
- ❌ Won't work at all

**CORRECTED VERSION:**

```java
// GOOD: Proper type conversion to String
public void setupView(View view, int quantity, double price, boolean available) {
    FS.setAttribute(view, "data-quantity", String.valueOf(quantity));
    FS.setAttribute(view, "data-price", String.valueOf(price));
    FS.setAttribute(view, "data-available", String.valueOf(available));

    try {
        String schema = new JSONObject()
            .put("data-quantity", new JSONObject().put("type", "int").put("name", "quantity"))
            .put("data-price", new JSONObject().put("type", "real").put("name", "price"))
            .put("data-available", new JSONObject().put("type", "bool").put("name", "isAvailable"))
            .toString();
        FS.setAttribute(view, "data-fs-properties-schema", schema);
    } catch (JSONException e) {
        Log.e("ViewSetup", "Error building schema", e);
    }
}
```

#### Example 4: RecyclerView Without Cleanup (Kotlin)

```kotlin
// BAD: Not handling view recycling properly
class ProductAdapter : RecyclerView.Adapter<ProductAdapter.ViewHolder>() {

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        val product = products[position]

        // BAD: Setting attributes without clearing old ones from recycled view
        FS.setAttribute(holder.itemView, "data-product-id", product.id)
        FS.setAttribute(holder.itemView, "data-product-name", product.name)
        // More attributes...

        // If this view was recycled, it might still have old attributes
        // from previous product that no longer apply
    }
}
```

**Why this is bad:**

- ❌ Recycled views retain old attributes
- ❌ Can cause data contamination (wrong product IDs on interactions)
- ❌ Creates confusing analytics data

**CORRECTED VERSION:**

```kotlin
// GOOD: Properly handling recycled views
class ProductAdapter : RecyclerView.Adapter<ProductAdapter.ViewHolder>() {

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        val product = products[position]

        // Clear old attributes by setting empty values
        // (Note: Track previously set attributes in ViewHolder)
        holder.clearPreviousAttributes()

        // Set new attributes
        holder.setProductAttributes(product, position)
    }

    class ViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        private val previousAttributes = mutableListOf<String>()

        fun clearPreviousAttributes() {
            previousAttributes.forEach { attr ->
                FS.setAttribute(itemView, attr, "")
            }
            previousAttributes.clear()
        }

        fun setProductAttributes(product: Product, position: Int) {
            // Set and track attributes
            setAndTrack("data-product-id", product.id)
            setAndTrack("data-product-name", product.name)
            setAndTrack("data-price", product.price.toString())
            setAndTrack("data-position", position.toString())

            // Set schema
            val schema = JSONObject().apply {
                put("data-product-id", JSONObject().put("type", "str").put("name", "productId"))
                put("data-product-name", JSONObject().put("type", "str").put("name", "productName"))
                put("data-price", JSONObject().put("type", "real").put("name", "price"))
                put("data-position", JSONObject().put("type", "int").put("name", "listPosition"))
            }.toString()

            setAndTrack("data-fs-properties-schema", schema)
            setAndTrack("data-fs-element", "Product List Item")
        }

        private fun setAndTrack(attr: String, value: String) {
            FS.setAttribute(itemView, attr, value)
            previousAttributes.add(attr)
        }
    }
}
```

---

## iOS IMPLEMENTATION

### Basic Syntax

Element properties are set using the `FS.setAttribute()` method:

**Objective-C:**

```objc
[FS setAttribute:view attributeName:@"attribute-name" attributeValue:@"value"];
```

**Swift:**

```swift
FS.setAttribute(view: UIView, attributeName: String, attributeValue: String)
```

### ✅ GOOD iOS IMPLEMENTATION EXAMPLES

#### Example 1: Product Card with Comprehensive Properties (Swift)

```swift
// GOOD: Complete product card implementation
class ProductCardView: UIView {
    private var addToCartButton: UIButton!

    func configure(with product: Product) {
        // Set all attribute values first
        FS.setAttribute(self, attributeName: "data-product-id", attributeValue: product.id)
        FS.setAttribute(self, attributeName: "data-product-name", attributeValue: product.name)
        FS.setAttribute(self, attributeName: "data-category", attributeValue: product.category)
        FS.setAttribute(self, attributeName: "data-price", attributeValue: String(product.price))
        FS.setAttribute(self, attributeName: "data-stock-level", attributeValue: String(product.stockLevel))
        FS.setAttribute(self, attributeName: "data-rating", attributeValue: String(product.rating))
        FS.setAttribute(self, attributeName: "data-on-sale", attributeValue: String(product.isOnSale))
        FS.setAttribute(self, attributeName: "data-launch-date", attributeValue: product.launchDate.iso8601String)

        // Build properties schema as JSON string
        let schema: [String: Any] = [
            "data-product-id": [
                "type": "str",
                "name": "productId"
            ],
            "data-product-name": [
                "type": "str",
                "name": "productName"
            ],
            "data-category": [
                "type": "str",
                "name": "category"
            ],
            "data-price": [
                "type": "real",
                "name": "price"
            ],
            "data-stock-level": [
                "type": "int",
                "name": "stockLevel"
            ],
            "data-rating": [
                "type": "real",
                "name": "rating"
            ],
            "data-on-sale": [
                "type": "bool",
                "name": "isOnSale"
            ],
            "data-launch-date": [
                "type": "date",
                "name": "launchDate"
            ]
        ]

        // Convert to JSON string
        if let schemaData = try? JSONSerialization.data(withJSONObject: schema),
           let schemaString = String(data: schemaData, encoding: .utf8) {
            FS.setAttribute(self, attributeName: "data-fs-properties-schema", attributeValue: schemaString)
        }

        // Name the element
        FS.setAttribute(self, attributeName: "data-fs-element", attributeValue: "Product Card")

        // Configure child button (inherits parent properties)
        FS.setAttribute(addToCartButton, attributeName: "data-fs-element", attributeValue: "Add to Cart Button")
    }
}

// Helper extension for ISO8601 dates
extension Date {
    var iso8601String: String {
        let formatter = ISO8601DateFormatter()
        return formatter.string(from: self)
    }
}
```

**Why this is good:**

- ✅ Proper type conversions using String() initializers
- ✅ Clean property names via `name` field
- ✅ Uses Swift Dictionary for type-safe schema building
- ✅ Converts schema to JSON string properly
- ✅ Sets values before schema
- ✅ Includes ISO8601 date formatting
- ✅ Child button inherits parent properties

#### Example 2: Table View Cell with Reuse Handling (Swift)

```swift
// GOOD: Properly handling cell reuse in UITableView
class ProductTableViewCell: UITableViewCell {
    private var currentAttributes: [String] = []

    override func prepareForReuse() {
        super.prepareForReuse()
        clearFullstoryAttributes()
    }

    func configure(with product: Product, at indexPath: IndexPath) {
        // Clear any existing attributes first
        clearFullstoryAttributes()

        // Set new attributes and track them
        setAndTrack("data-product-id", product.id)
        setAndTrack("data-product-name", product.name)
        setAndTrack("data-price", String(product.price))
        setAndTrack("data-in-stock", String(product.isInStock))
        setAndTrack("data-row", String(indexPath.row))
        setAndTrack("data-section", String(indexPath.section))

        // Build schema
        let schema: [String: Any] = [
            "data-product-id": ["type": "str", "name": "productId"],
            "data-product-name": ["type": "str", "name": "productName"],
            "data-price": ["type": "real", "name": "price"],
            "data-in-stock": ["type": "bool", "name": "inStock"],
            "data-row": ["type": "int", "name": "rowIndex"],
            "data-section": ["type": "int", "name": "sectionIndex"]
        ]

        if let schemaData = try? JSONSerialization.data(withJSONObject: schema),
           let schemaString = String(data: schemaData, encoding: .utf8) {
            setAndTrack("data-fs-properties-schema", schemaString)
        }

        setAndTrack("data-fs-element", "Product Cell")
    }

    private func setAndTrack(_ attribute: String, _ value: String) {
        FS.setAttribute(self, attributeName: attribute, attributeValue: value)
        currentAttributes.append(attribute)
    }

    private func clearFullstoryAttributes() {
        currentAttributes.forEach { attribute in
            FS.setAttribute(self, attributeName: attribute, attributeValue: "")
        }
        currentAttributes.removeAll()
    }
}
```

**Why this is good:**

- ✅ Handles cell reuse with `prepareForReuse()`
- ✅ Tracks applied attributes for cleanup
- ✅ Clears old attributes before setting new ones
- ✅ Includes position information (row/section) for context
- ✅ Helper methods for clean attribute management

#### Example 3: Form with Hierarchical Properties (Objective-C)

```objc
// GOOD: Form implementation with property inheritance
@implementation CheckoutFormViewController

- (void)setupFormTracking {
    UIView *formContainer = self.formContainerView;

    // Set form-level properties (inherited by all children)
    [FS setAttribute:formContainer
        attributeName:@"data-form-type"
        attributeValue:@"checkout"];
    [FS setAttribute:formContainer
        attributeName:@"data-form-step"
        attributeValue:@"payment"];
    [FS setAttribute:formContainer
        attributeName:@"data-user-tier"
        attributeValue:self.userTier];
    [FS setAttribute:formContainer
        attributeName:@"data-cart-total"
        attributeValue:[NSString stringWithFormat:@"%.2f", self.cartTotal]];

    // Build form schema
    NSDictionary *formSchema = @{
        @"data-form-type": @{
            @"type": @"str",
            @"name": @"formType"
        },
        @"data-form-step": @{
            @"type": @"str",
            @"name": @"checkoutStep"
        },
        @"data-user-tier": @{
            @"type": @"str",
            @"name": @"userTier"
        },
        @"data-cart-total": @{
            @"type": @"real",
            @"name": @"cartTotal"
        }
    };

    NSError *error;
    NSData *formSchemaData = [NSJSONSerialization dataWithJSONObject:formSchema
                                                             options:0
                                                               error:&error];
    if (formSchemaData && !error) {
        NSString *formSchemaString = [[NSString alloc] initWithData:formSchemaData
                                                           encoding:NSUTF8StringEncoding];
        [FS setAttribute:formContainer
            attributeName:@"data-fs-properties-schema"
            attributeValue:formSchemaString];
    }

    [FS setAttribute:formContainer
        attributeName:@"data-fs-element"
        attributeValue:@"Checkout Form"];

    // Set field-specific properties
    [self setupFieldTracking:self.cardNumberField
                   fieldName:@"cardNumber"
                    required:YES
                  fieldType:@"credit-card"];

    // Submit button inherits form properties
    [FS setAttribute:self.submitButton
        attributeName:@"data-button-type"
        attributeValue:@"primary"];
    [FS setAttribute:self.submitButton
        attributeName:@"data-fs-element"
        attributeValue:@"Submit Payment Button"];
}

- (void)setupFieldTracking:(UITextField *)field
                 fieldName:(NSString *)name
                  required:(BOOL)required
                 fieldType:(NSString *)type {

    [FS setAttribute:field attributeName:@"data-field-name" attributeValue:name];
    [FS setAttribute:field attributeName:@"data-field-required"
        attributeValue:required ? @"true" : @"false"];
    [FS setAttribute:field attributeName:@"data-field-type" attributeValue:type];

    NSDictionary *fieldSchema = @{
        @"data-field-name": @{@"type": @"str", @"name": @"fieldName"},
        @"data-field-required": @{@"type": @"bool", @"name": @"isRequired"},
        @"data-field-type": @{@"type": @"str", @"name": @"fieldType"}
    };

    NSData *schemaData = [NSJSONSerialization dataWithJSONObject:fieldSchema
                                                         options:0
                                                           error:nil];
    if (schemaData) {
        NSString *schemaString = [[NSString alloc] initWithData:schemaData
                                                       encoding:NSUTF8StringEncoding];
        [FS setAttribute:field
            attributeName:@"data-fs-properties-schema"
            attributeValue:schemaString];
    }

    [FS setAttribute:field
        attributeName:@"data-fs-element"
        attributeValue:[NSString stringWithFormat:@"%@ Field", name]];
}

@end
```

**Why this is good:**

- ✅ Clear hierarchy with form-level properties
- ✅ Reusable field setup method
- ✅ Proper error handling for JSON serialization
- ✅ Boolean values properly converted to "true"/"false" strings
- ✅ All child elements inherit form context

### ❌ BAD iOS IMPLEMENTATION EXAMPLES

#### Example 1: Type Mismatches and Formatting Issues (Swift)

```swift
// BAD: Multiple type and formatting problems
func configureProductCard(with product: Product) {
    let cardView = self.productCardView

    // BAD: Including formatting/symbols in numeric values
    FS.setAttribute(cardView,
        attributeName: "data-price",
        attributeValue: "$\(product.price)") // BAD: includes $

    FS.setAttribute(cardView,
        attributeName: "data-stock",
        attributeValue: "\(product.stockLevel) items") // BAD: includes "items"

    FS.setAttribute(cardView,
        attributeName: "data-available",
        attributeValue: product.isInStock ? "Yes" : "No") // BAD: not boolean value

    FS.setAttribute(cardView,
        attributeName: "data-rating",
        attributeValue: "\(product.rating) stars") // BAD: includes "stars"

    // Schema with wrong types
    let schema = """
    {
        "data-price": "str",
        "data-stock": "int",
        "data-available": "bool",
        "data-rating": "str"
    }
    """

    FS.setAttribute(cardView,
        attributeName: "data-fs-properties-schema",
        attributeValue: schema)
}
```

**Why this is bad:**

- ❌ Price includes "$" making it a string, not a number
- ❌ Stock includes "items" text but typed as int
- ❌ Available uses "Yes"/"No" instead of "true"/"false"
- ❌ Rating includes "stars" text but typed as string
- ❌ Manual JSON string creation is error-prone
- ❌ No clean property names

**CORRECTED VERSION:**

```swift
// GOOD: Clean values with proper types
func configureProductCard(with product: Product) {
    let cardView = self.productCardView

    // Set clean numeric and boolean values
    FS.setAttribute(cardView, attributeName: "data-price",
        attributeValue: String(product.price))
    FS.setAttribute(cardView, attributeName: "data-stock",
        attributeValue: String(product.stockLevel))
    FS.setAttribute(cardView, attributeName: "data-available",
        attributeValue: String(product.isInStock))
    FS.setAttribute(cardView, attributeName: "data-rating",
        attributeValue: String(product.rating))
    FS.setAttribute(cardView, attributeName: "data-currency",
        attributeValue: "USD") // Separate field for currency

    // Build schema using Dictionary for safety
    let schema: [String: Any] = [
        "data-price": ["type": "real", "name": "price"],
        "data-stock": ["type": "int", "name": "stockLevel"],
        "data-available": ["type": "bool", "name": "isAvailable"],
        "data-rating": ["type": "real", "name": "rating"],
        "data-currency": ["type": "str", "name": "currency"]
    ]

    if let schemaData = try? JSONSerialization.data(withJSONObject: schema),
       let schemaString = String(data: schemaData, encoding: .utf8) {
        FS.setAttribute(cardView,
            attributeName: "data-fs-properties-schema",
            attributeValue: schemaString)
    }

    FS.setAttribute(cardView,
        attributeName: "data-fs-element",
        attributeValue: "Product Card")
}
```

#### Example 2: Not Handling Cell Reuse (Swift)

```swift
// BAD: UITableViewCell without cleaning up attributes
class ProductCell: UITableViewCell {
    func configure(with product: Product) {
        // BAD: Just setting new attributes without clearing old ones
        FS.setAttribute(self, attributeName: "data-product-id", attributeValue: product.id)
        FS.setAttribute(self, attributeName: "data-product-name", attributeValue: product.name)

        // When this cell is reused, old attributes from previous product remain!
        // This can cause wrong data to be captured
    }
}
```

**Why this is bad:**

- ❌ Reused cells keep old attributes
- ❌ Can capture wrong product IDs/names
- ❌ Creates data integrity issues
- ❌ Doesn't override `prepareForReuse()`

**CORRECTED VERSION:**

```swift
// GOOD: Proper cell reuse handling
class ProductCell: UITableViewCell {
    private var trackedAttributes: [String] = []

    override func prepareForReuse() {
        super.prepareForReuse()
        clearAttributes()
    }

    func configure(with product: Product) {
        clearAttributes()

        setAndTrack("data-product-id", product.id)
        setAndTrack("data-product-name", product.name)
        setAndTrack("data-price", String(product.price))

        let schema: [String: Any] = [
            "data-product-id": ["type": "str", "name": "productId"],
            "data-product-name": ["type": "str", "name": "productName"],
            "data-price": ["type": "real", "name": "price"]
        ]

        if let schemaData = try? JSONSerialization.data(withJSONObject: schema),
           let schemaString = String(data: schemaData, encoding: .utf8) {
            setAndTrack("data-fs-properties-schema", schemaString)
        }

        setAndTrack("data-fs-element", "Product Cell")
    }

    private func setAndTrack(_ attr: String, _ value: String) {
        FS.setAttribute(self, attributeName: attr, attributeValue: value)
        trackedAttributes.append(attr)
    }

    private func clearAttributes() {
        trackedAttributes.forEach { attr in
            FS.setAttribute(self, attributeName: attr, attributeValue: "")
        }
        trackedAttributes.removeAll()
    }
}
```

#### Example 3: Schema Before Values (Objective-C)

```objc
// BAD: Setting schema before values
- (void)configureProductCard:(Product *)product {
    UIView *cardView = self.productCardView;

    // BAD: Setting schema first
    NSDictionary *schema = @{
        @"data-product-id": @"str",
        @"data-price": @"real"
    };

    NSData *schemaData = [NSJSONSerialization dataWithJSONObject:schema
                                                         options:0
                                                           error:nil];
    NSString *schemaString = [[NSString alloc] initWithData:schemaData
                                                   encoding:NSUTF8StringEncoding];
    [FS setAttribute:cardView
        attributeName:@"data-fs-properties-schema"
        attributeValue:schemaString];

    // Then setting values (wrong order)
    [FS setAttribute:cardView
        attributeName:@"data-product-id"
        attributeValue:product.productId];
    [FS setAttribute:cardView
        attributeName:@"data-price"
        attributeValue:[NSString stringWithFormat:@"%.2f", product.price]];
}
```

**Why this is bad:**

- ❌ Schema set before values
- ❌ May cause timing/capture issues
- ❌ Values should always be set first

**CORRECTED VERSION:**

```objc
// GOOD: Values first, then schema
- (void)configureProductCard:(Product *)product {
    UIView *cardView = self.productCardView;

    // Set values FIRST
    [FS setAttribute:cardView
        attributeName:@"data-product-id"
        attributeValue:product.productId];
    [FS setAttribute:cardView
        attributeName:@"data-price"
        attributeValue:[NSString stringWithFormat:@"%.2f", product.price]];

    // Then set schema
    NSDictionary *schema = @{
        @"data-product-id": @{@"type": @"str", @"name": @"productId"},
        @"data-price": @{@"type": @"real", @"name": @"price"}
    };

    NSData *schemaData = [NSJSONSerialization dataWithJSONObject:schema
                                                         options:0
                                                           error:nil];
    if (schemaData) {
        NSString *schemaString = [[NSString alloc] initWithData:schemaData
                                                       encoding:NSUTF8StringEncoding];
        [FS setAttribute:cardView
            attributeName:@"data-fs-properties-schema"
            attributeValue:schemaString];
    }

    [FS setAttribute:cardView
        attributeName:@"data-fs-element"
        attributeValue:@"Product Card"];
}
```

#### Example 4: Manual JSON String Construction (Swift)

```swift
// BAD: Manually building JSON strings
func setupProduct(_ product: Product) {
    let cardView = self.cardView

    FS.setAttribute(cardView, attributeName: "data-price", attributeValue: String(product.price))
    FS.setAttribute(cardView, attributeName: "data-name", attributeValue: product.name)

    // BAD: Manual JSON string construction
    let schema = """
    {
        "data-price": {
            "type": "real",
            "name": "price"
        },
        "data-name": {
            "type": "str",
            "name": "productName"
        }
    }
    """

    FS.setAttribute(cardView, attributeName: "data-fs-properties-schema", attributeValue: schema)
}
```

**Why this is bad:**

- ❌ Manual JSON string is error-prone
- ❌ Easy to make syntax errors (quotes, commas, brackets)
- ❌ No compile-time checking
- ❌ Hard to maintain

**CORRECTED VERSION:**

```swift
// GOOD: Using Dictionary and JSONSerialization
func setupProduct(_ product: Product) {
    let cardView = self.cardView

    FS.setAttribute(cardView, attributeName: "data-price",
        attributeValue: String(product.price))
    FS.setAttribute(cardView, attributeName: "data-name",
        attributeValue: product.name)

    // Use Dictionary for type safety
    let schema: [String: Any] = [
        "data-price": [
            "type": "real",
            "name": "price"
        ],
        "data-name": [
            "type": "str",
            "name": "productName"
        ]
    ]

    // Convert to JSON safely
    if let schemaData = try? JSONSerialization.data(withJSONObject: schema),
       let schemaString = String(data: schemaData, encoding: .utf8) {
        FS.setAttribute(cardView,
            attributeName: "data-fs-properties-schema",
            attributeValue: schemaString)
    }
}
```

---

## LIMITS AND CONSTRAINTS

### Global Limits

- **1,000 active API Defined Elements** max (archived elements don't count)
- **50 unique properties** per single element interaction max
- **500 unique properties** across all element interactions max

### Property Requirements

- **Property Names**:
  - No type suffix needed (type is specified in schema)
  - Follow standard naming conventions
  - Use meaningful, readable names
- **Property Values**: Must match the specified type
- **Cardinality**: High cardinality properties may be limited

### Best Practices for Limits

1. ✅ Focus on business-relevant properties only
2. ✅ Avoid debug/technical properties
3. ✅ Use property hierarchy to reduce duplication
4. ✅ Archive unused elements to free up quota
5. ✅ Monitor your property count

---

## COMMON IMPLEMENTATION PATTERNS

### Pattern 1: Container + Interactive Element

```
Container (e.g., product card)
  ├── Properties: productId, productName, price, category
  └── Button (e.g., "Add to Cart")
      └── Inherits all container properties
      └── Button interaction captures full product context
```

### Pattern 2: Form + Fields

```
Form Container
  ├── Properties: formType, formStep, userTier
  ├── Field 1
  │   ├── Inherits form properties
  │   └── Own properties: fieldName, isRequired, fieldType
  ├── Field 2
  │   └── Same pattern
  └── Submit Button
      └── Inherits form properties
```

### Pattern 3: List Items

```
List Container
  ├── Properties: listType, totalItems, filterApplied
  └── List Item (repeated)
      ├── Inherits list properties
      └── Own properties: itemId, itemName, position
```

---

## WHEN TO USE ELEMENT PROPERTIES

### ✅ Good Use Cases

1. **E-commerce Product Data**: SKUs, prices, categories, stock levels
2. **Form Analytics**: Form types, steps, field names, validation rules
3. **Content Tracking**: Article IDs, categories, authors, publish dates
4. **A/B Testing**: Variant names, experiment IDs
5. **User Segments**: Tier levels, feature flags, entitlements
6. **Navigation Context**: Section names, page types, user flows

### ❌ Avoid Element Properties For

1. **Technical/Debug Data**: Component versions, render timestamps, git commits
2. **Styling Information**: CSS classes, style properties
3. **Implementation Details**: Framework internals, React keys
4. **High Cardinality**: Unique timestamps, random IDs without business value
5. **Data Already Captured**: Information available as user/page properties
6. **PII Without Consent**: Personal information unless properly handled

---

## TESTING AND VALIDATION

### Pre-Deployment Checklist

- [ ] All attribute values are set before the schema
- [ ] All referenced attributes in schema actually exist
- [ ] Numeric values are clean (no symbols, units, text)
- [ ] Boolean values use "true"/"false" or "1"/"0"
- [ ] Date values are in ISO8601 format
- [ ] JSON schema is valid (no syntax errors)
- [ ] Property names are meaningful and use `name` override
- [ ] Types match the actual data (real for decimals, int for whole numbers)
- [ ] Cell/view reuse is handled (mobile only)
- [ ] Elements are named with `data-fs-element`

### Validation in Fullstory

1. **Trigger an interaction** on the decorated element
2. **Find the session** in Fullstory
3. **Click on the element** in the replay
4. **Check the Inspector** for element properties
5. **Verify all properties appear** with correct names and values
6. **Test filtering** using the captured properties

---

## TROUBLESHOOTING

### Properties Not Appearing

**Symptom**: Properties don't show up in Fullstory after element interaction

**Common Causes**:

1. ❌ Schema set before attribute values
2. ❌ Invalid JSON in schema
3. ❌ Attribute referenced in schema doesn't exist
4. ❌ Type mismatch (e.g., "123abc" as int)
5. ❌ Hit the 50/500 property limits

**Solutions**:

- ✅ Always set values before schema
- ✅ Use JSONObject/Dictionary, not manual strings
- ✅ Verify all attributes exist
- ✅ Ensure clean values matching types
- ✅ Check property count limits

### Wrong Values Captured

**Symptom**: Properties show incorrect or stale values

**Common Causes** (Mobile):

1. ❌ View/cell reuse not handled
2. ❌ Old attributes not cleared
3. ❌ Attributes set at wrong lifecycle point

**Solutions**:

- ✅ Implement prepareForReuse (iOS) or clear in onBindViewHolder (Android)
- ✅ Track and clear previous attributes
- ✅ Set attributes in appropriate lifecycle methods

### Type Conversion Errors

**Symptom**: Numeric/boolean properties show as strings

**Common Causes**:

1. ❌ Values contain non-numeric characters
2. ❌ Type specified as "str" instead of "int"/"real"
3. ❌ Boolean using "yes"/"no" instead of "true"/"false"

**Solutions**:

- ✅ Strip formatting before setting values
- ✅ Use correct type in schema
- ✅ Convert booleans to "true"/"false" strings

---

## KEY TAKEAWAYS FOR AGENT

When helping developers implement Element Properties:

1. **Always emphasize**:
   - Set attribute values BEFORE schema
   - Use clean, unformatted values (no "$", "items", "Yes/No")
   - Match types correctly (real for decimals, int for integers, bool for booleans)
   - Provide meaningful property names via `name` override

2. **For Web**: Remind about JSON validity and proper data attribute syntax

3. **For Android**: Emphasize String.valueOf() conversions and RecyclerView reuse handling

4. **For iOS**: Emphasize JSONSerialization over manual strings and UITableView/UICollectionView reuse

5. **Always ask about**:
   - What data is business-relevant?
   - Is this element in a recycling container? (mobile)
   - Are there parent elements that should have properties?
   - What analytics questions need to be answered?

6. **Red flags to watch for**:
   - Schema set before values
   - Formatted numbers ("$10.99", "5 items")
   - "Yes"/"No" for booleans
   - Manual JSON string construction (mobile)
   - No cell/view reuse handling (mobile)
   - Over-capturing technical/debug data

---

## REFERENCE LINKS

- **Browser API**: https://developer.fullstory.com/browser/fullcapture/set-element-properties/
- **Android API**: https://developer.fullstory.com/mobile/android/fullcapture/set-element-properties/
- **iOS API**: https://developer.fullstory.com/mobile/ios/fullcapture/set-element-properties/
- **Help Center**: https://help.fullstory.com/hc/en-us/articles/24236341468311-Extracted-Element-Properties

---

_This skill document was created to help Agent understand and guide developers in implementing Fullstory's Element Properties API correctly across Web and Mobile platforms._
