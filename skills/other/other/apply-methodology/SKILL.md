---
name: 'Apply Methodology Rule'
description: 'Apply an existing rule processor to a specific methodology using the apply script.'
---

1. **Identify the parameters**:
   - `<methodology>`: the target methodology (e.g., `carbon-organic`, `bold-recycling`)
   - `<rule>`: the rule processor name (e.g., `geolocation-precision`)
   - `<scope>`: the processor group (`mass-id`, `credit-order`, or `mass-id-certificate`)

2. **Run the apply script**:

   ```bash
   pnpm apply-methodology-rule <methodology> <rule> <scope>
   ```

   Example:

   ```bash
   pnpm apply-methodology-rule carbon-organic geolocation-precision mass-id
   ```

3. **Verify** the application was successful by running quality checks:

   ```bash
   pnpm lint:affected
   pnpm ts:affected
   pnpm test:affected
   ```

   All three checks must pass.
