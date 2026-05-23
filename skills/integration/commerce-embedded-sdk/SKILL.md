---
name: commerce-embedded-sdk
description: Integrate the StateSet iCommerce embedded SDK in apps. Use when creating a Commerce client, configuring `@stateset/embedded`, or wiring embedded SDK calls.
---

# Commerce Embedded SDK

Use the embedded engine from application code via language bindings.

## How It Works

1. Install the binding for the target language.
2. Initialize `Commerce` with a SQLite database path.
3. Call module APIs (customers, products, inventory, orders, etc).
4. Run the matching example to validate behavior.

## Usage

- Node.js: `npm install @stateset/embedded`
- Python: `pip install stateset-embedded`
- Rust: `cargo add stateset-embedded`
- See language examples under `/home/dom/stateset-icommerce/examples/`

## Output

```json
{"status":"ok","order_number":"ORD-12345","customer_id":"cust_123"}
```

## Present Results to User

- Binding used and database path.
- Which example or module calls were validated.
- Any build or runtime constraints.

## Troubleshooting

- Binding build errors: confirm Rust toolchain and target platform.
- Shared library issues: check `LD_LIBRARY_PATH` or platform linking.
- Missing symbols: rebuild the native bindings for your runtime.

## References
- references/bindings.md
- /home/dom/stateset-icommerce/examples/README.md
- /home/dom/stateset-icommerce/examples/basic_usage.rs
- /home/dom/stateset-icommerce/examples/node/basic_usage.js
- /home/dom/stateset-icommerce/examples/python/basic_usage.py
