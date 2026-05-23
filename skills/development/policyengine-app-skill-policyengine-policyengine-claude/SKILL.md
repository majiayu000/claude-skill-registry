---
name: policyengine-app
description: PolicyEngine React web application - the user interface at policyengine.org
---

# PolicyEngine App

The PolicyEngine App is the React-based web application that users interact with at policyengine.org.

## For Users 👥

### What is the App?

The app at policyengine.org provides:
- Interactive household calculator
- Policy reform creator
- Population impact analysis
- Blog and research hub

**Access:** https://policyengine.org

### App Features

**Calculator:**
- Enter household details
- See tax and benefit calculations
- Visualize marginal tax rates
- Compare scenarios

**Policy designer:**
- Browse all parameters
- Create custom reforms
- Share via URL
- Download charts

**Research hub:**
- Read policy analysis
- Explore modeled programs
- Access documentation

## For Analysts 📊

### Understanding App URLs

Reform URLs encode all policy changes in the query string, allowing sharing and reproducibility.

**Example URL:**
```
policyengine.org/us/policy?
  focus=policyOutput.policyBreakdown&
  reform=67696&
  region=enhanced_us&
  timePeriod=2025&
  baseline=2
```

**Parameters:**
- `focus` - Which section to display
- `reform` - Reform ID from database
- `region` - Geographic scope (enhanced_us, CA, congressional districts)
- `timePeriod` - Year of analysis
- `baseline` - Baseline policy ID

### Embedding PolicyEngine

**iFrame integration:**
```html
<iframe
  src="https://policyengine.org/us/household?embedded=true"
  width="100%"
  height="800">
</iframe>
```

**Parameter:**
- `embedded=true` - Removes navigation, optimizes for embedding

### URL Structure

**Household calculator:**
```
/us/household?household=12345
/uk/household?household=67890
```

**Policy page:**
```
/us/policy?reform=12345
/uk/policy?reform=67890
```

**Research/blog:**
```
/us/research/article-slug
/uk/research/article-slug
```

## For Contributors 💻

### Repository

**Location:** PolicyEngine/policyengine-app

**Clone:**
```bash
git clone https://github.com/PolicyEngine/policyengine-app
cd policyengine-app
```

### Current Architecture

**To see current structure:**
```bash
tree src/ -L 2

# Key directories:
ls src/
# - pages/         - Page components
# - applets/       - Reusable UI modules
# - api/           - API integration
# - controls/      - Form controls
# - layout/        - Layout components
# - posts/         - Blog posts
# - routing/       - Routing configuration
# - hooks/         - Custom React hooks
# - data/          - Static data
```

### Technology Stack

**Current dependencies:**
```bash
# See package.json for versions
cat package.json

# Key dependencies:
# - React 18
# - React Router v6
# - Plotly.js
# - Ant Design
# - axios
```

### React Patterns (Critical)

**✅ Functional components only (no classes):**
```javascript
// CORRECT
import { useState, useEffect } from "react";

export default function TaxCalculator({ income }) {
  const [tax, setTax] = useState(0);

  useEffect(() => {
    calculateTax(income).then(setTax);
  }, [income]);

  return <div>Tax: ${tax}</div>;
}
```

**❌ Class components forbidden:**
```javascript
// WRONG - Don't use class components
class TaxCalculator extends Component {
  // ...
}
```

**To find component examples:**
```bash
# Reference components
ls src/pages/
ls src/applets/

# See a complete page
cat src/pages/HouseholdPage.jsx
```

### State Management

**No global state (Redux, Context) - lift state up:**

```javascript
// Parent manages state
function PolicyPage() {
  const [reform, setReform] = useState({});
  const [impact, setImpact] = useState(null);

  return (
    <>
      <PolicyEditor reform={reform} onChange={setReform} />
      <ImpactDisplay impact={impact} />
    </>
  );
}
```

**To see state patterns:**
```bash
# Find useState usage
grep -r "useState" src/pages/ | head -20
```

### API Integration

**To see current API patterns:**
```bash
cat src/api/call.js      # Base API caller
cat src/api/variables.js # Variable metadata
cat src/api/parameters.js # Parameter metadata
```

**Standard pattern:**
```javascript
import { api call } from "api/call";

// Fetch data
const result = await call(
  `/us/calculate`,
  { household: householdData },
  "POST"
);
```

### Routing

**To see current routing:**
```bash
cat src/routing/routes.js

# Routes defined with React Router v6
# See examples:
grep -r "useNavigate" src/
grep -r "useSearchParams" src/
```

**URL parameters:**
```javascript
import { useSearchParams } from "react-router-dom";

const [searchParams, setSearchParams] = useSearchParams();

// Read
const reformId = searchParams.get("reform");

// Update
setSearchParams({ ...Object.fromEntries(searchParams), reform: newId });
```

### Custom Hooks

**To see PolicyEngine-specific hooks:**
```bash
ls src/hooks/
# - useCountryId.js    - Current country
# - useDisplayCategory.js
# - etc.
```

**Usage:**
```javascript
import { useCountryId } from "hooks/useCountryId";

function Component() {
  const [countryId, setCountryId] = useCountryId();
  // countryId = "us", "uk", or "ca"
}
```

### Charts and Visualization

**Plotly integration:**
```bash
# See chart components
ls src/pages/policy/output/

# Reference implementation
cat src/pages/policy/output/EconomyOutput.jsx
```

**Standard Plotly pattern:**
```javascript
import Plot from "react-plotly.js";

const layout = {
  font: { family: "Roboto Serif" },
  plot_bgcolor: "white",
  // PolicyEngine branding
};

<Plot
  data={traces}
  layout={layout}
  config={{ displayModeBar: false }}
/>;
```

### Blog Posts

**To see blog post structure:**
```bash
ls src/posts/articles/

# Read a recent post
cat src/posts/articles/harris-eitc.md
```

**Blog posts:**
- Written in Markdown
- Stored in `src/posts/articles/`
- Include metadata (title, date, authors)
- Follow policyengine-writing-skill style

**Adding a post:**
```bash
# Create new file
# src/posts/articles/my-analysis.md

# Add to index (if needed)
# See existing posts for format
```

### Styling

**Current styling approach:**
```bash
# See style configuration
ls src/style/

# Colors
cat src/style/colors.js

# Ant Design theme
cat src/style/theme.js
```

**PolicyEngine colors:**
- Teal: `#39C6C0` (primary accent)
- Blue: `#2C6496` (charts, links)
- Dark gray: `#616161` (text)

### Testing

**To see current tests:**
```bash
ls src/__tests__/

# Run tests
make test

# Test pattern
cat src/__tests__/example.test.js
```

**Testing libraries:**
- Jest (test runner)
- React Testing Library (component testing)
- User-centric testing (not implementation details)

### Development Server

**Start locally:**
```bash
make debug
# Opens http://localhost:3000
```

**Environment:**
```bash
# Environment variables
cat .env.example

# Config
ls src/config/
```

### Building and Deployment

**Build:**
```bash
make build
# Creates optimized production build
```

**Deployment:**
```bash
# See deployment config
cat netlify.toml  # or appropriate hosting config
```

## Component Patterns

### Standard Component Structure

**To see well-structured components:**
```bash
# Example page
cat src/pages/HouseholdPage.jsx

# Example applet
cat src/applets/PolicySearch.jsx
```

**Pattern:**
```javascript
import { useState, useEffect } from "react";
import { useSearchParams } from "react-router-dom";
import { useCountryId } from "hooks/useCountryId";

export default function MyComponent({ prop1, prop2 }) {
  // 1. Hooks first
  const [state, setState] = useState(initialValue);
  const [countryId] = useCountryId();
  const [searchParams] = useSearchParams();

  // 2. Effects
  useEffect(() => {
    // Side effects
  }, [dependencies]);

  // 3. Event handlers
  const handleClick = () => {
    setState(newValue);
  };

  // 4. Render
  return (
    <div>
      {/* JSX */}
    </div>
  );
}
```

### Component Size Limit

**Keep components under 150 lines after formatting.**

**If component is too large:**
1. Extract sub-components
2. Move logic to custom hooks
3. Split into multiple files

**To find large components:**
```bash
# Find files >150 lines
find src/ -name "*.jsx" -exec wc -l {} \; | sort -rn | head -20
```

### File Naming

**Components:** PascalCase.jsx
- `HouseholdPage.jsx`
- `PolicySearch.jsx`
- `ImpactChart.jsx`

**Utilities:** camelCase.js
- `formatCurrency.js`
- `apiUtils.js`
- `chartHelpers.js`

**Hooks:** camelCase.js with 'use' prefix
- `useCountryId.js`
- `usePolicy.js`

## Common Development Tasks

### Task 1: Add New Page

1. **See page structure:**
   ```bash
   cat src/pages/HouseholdPage.jsx
   ```

2. **Create new page:**
   ```javascript
   // src/pages/MyNewPage.jsx
   export default function MyNewPage() {
     return <div>Content</div>;
   }
   ```

3. **Add route:**
   ```bash
   # See routing
   cat src/routing/routes.js

   # Add your route following the pattern
   ```

### Task 2: Add New Chart

1. **See chart examples:**
   ```bash
   ls src/pages/policy/output/
   cat src/pages/policy/output/DistributionalImpact.jsx
   ```

2. **Create chart component:**
   ```javascript
   import Plot from "react-plotly.js";

   export default function MyChart({ data }) {
     return (
       <Plot
         data={traces}
         layout={{
           font: { family: "Roboto Serif" },
           plot_bgcolor: "white"
         }}
       />
     );
   }
   ```

### Task 3: Add Blog Post

1. **See post structure:**
   ```bash
   cat src/posts/articles/harris-eitc.md
   ```

2. **Create post:**
   ```bash
   # Create markdown file
   # src/posts/articles/my-analysis.md

   # Follow policyengine-writing-skill for style
   ```

3. **Images:**
   ```bash
   # Store in public/images/posts/
   # Reference in markdown
   ```

## API Integration Patterns

### Fetching Data

**To see API call patterns:**
```bash
cat src/api/call.js
```

**Standard pattern:**
```javascript
import { call } from "api/call";

const fetchData = async () => {
  const result = await call(
    `/us/calculate`,
    { household: data },
    "POST"
  );
  return result;
};
```

### Loading States

**Pattern:**
```javascript
const [loading, setLoading] = useState(false);
const [error, setError] = useState(null);
const [data, setData] = useState(null);

useEffect(() => {
  setLoading(true);
  fetchData()
    .then(setData)
    .catch(setError)
    .finally(() => setLoading(false));
}, [dependencies]);

if (loading) return <Spin />;
if (error) return <Error message={error} />;
return <Data data={data} />;
```

## Performance Patterns

### Code Splitting

**To see code splitting:**
```bash
grep -r "React.lazy" src/
```

**Pattern:**
```javascript
import { lazy, Suspense } from "react";

const HeavyComponent = lazy(() => import("./HeavyComponent"));

function Page() {
  return (
    <Suspense fallback={<Spin />}>
      <HeavyComponent />
    </Suspense>
  );
}
```

### Memoization

**Use React.memo for expensive components:**
```javascript
import { memo } from "react";

const ExpensiveChart = memo(function ExpensiveChart({ data }) {
  // Only re-renders if data changes
  return <Plot data={data} />;
});
```

## Accessibility

**Requirements:**
- Semantic HTML elements
- ARIA labels for complex widgets
- Keyboard navigation
- Color contrast (WCAG AA)

**To see accessibility patterns:**
```bash
grep -r "aria-" src/
grep -r "role=" src/
```

## Country-Specific Features

### Country Switching

**To see country switching:**
```bash
cat src/hooks/useCountryId.js
```

**Usage:**
```javascript
import { useCountryId } from "hooks/useCountryId";

function Component() {
  const [countryId] = useCountryId();  // "us", "uk", or "ca"

  // Load country-specific data
  const data = countryId === "us" ? usData : ukData;
}
```

### Country-Specific Content

**Conditional rendering:**
```javascript
{countryId === "us" && <USSpecificComponent />}
{countryId === "uk" && <UKSpecificComponent />}
```

**To find country-specific code:**
```bash
grep -r "countryId ===" src/
```

## Development Workflow

### Local Development

**Start dev server:**
```bash
make debug
# App runs on http://localhost:3000
# Connects to production API by default
```

**Connect to local API:**
```bash
# See environment configuration
cat src/config/environment.js

# Or set environment variable
REACT_APP_API_URL=http://localhost:5000 make debug
```

### Testing

**Run tests:**
```bash
make test
```

**Watch mode:**
```bash
npm test -- --watch
```

**Coverage:**
```bash
npm test -- --coverage
```

### Linting and Formatting

**Format code (critical before committing):**
```bash
make format

# Or manually
npm run lint -- --fix
npx prettier --write .
```

**Check linting (CI check):**
```bash
npm run lint -- --max-warnings=0
```

## Current Implementation Reference

### Component Structure

**To see current page structure:**
```bash
ls src/pages/
# - HouseholdPage.jsx
# - PolicyPage.jsx
# - HomePage.jsx
# - etc.
```

**To see a complete page:**
```bash
cat src/pages/PolicyPage.jsx
```

### API Call Patterns

**To see current API integration:**
```bash
cat src/api/call.js      # Base caller
cat src/api/variables.js # Variable metadata fetching
cat src/api/parameters.js # Parameter metadata fetching
```

### Routing Configuration

**To see current routes:**
```bash
cat src/routing/routes.js
```

### Form Controls

**To see PolicyEngine-specific form controls:**
```bash
ls src/controls/
# - InputField.jsx
# - SearchParamControl.jsx
# - etc.
```

### Chart Components

**To see chart implementations:**
```bash
ls src/pages/policy/output/
# - BudgetaryImpact.jsx
# - DistributionalImpact.jsx
# - PovertyImpact.jsx
# - etc.
```

**Reference chart:**
```bash
cat src/pages/policy/output/DistributionalImpact.jsx
```

## Multi-Repository Integration

### How App Relates to Other Repos

```
policyengine-core (engine)
    ↓
policyengine-us, policyengine-uk (country models)
    ↓
policyengine-api (backend)
    ↓
policyengine-app (you are here)
```

**Understanding the stack:**
- See `policyengine-core-skill` for engine concepts
- See `policyengine-us-skill` for what variables/parameters mean
- See `policyengine-api-skill` for API endpoints the app calls

### Blog Posts Reference Country Models

**Blog posts often reference variables:**
```bash
# Posts reference variables like "income_tax", "ctc"
# See policyengine-us-skill for variable definitions
cat src/posts/articles/harris-eitc.md
```

## Common Development Tasks

### Task 1: Add New Parameter to UI

1. **Understand parameter:**
   ```bash
   # See parameter in country model
   cd ../policyengine-us
   cat policyengine_us/parameters/gov/irs/credits/ctc/amount/base_amount.yaml
   ```

2. **Find similar parameter in app:**
   ```bash
   cd ../policyengine-app
   grep -r "ctc.*amount" src/pages/policy/
   ```

3. **Add UI control following pattern**

### Task 2: Add New Chart

1. **See existing charts:**
   ```bash
   cat src/pages/policy/output/DistributionalImpact.jsx
   ```

2. **Create new chart component**

3. **Add to policy output page**

### Task 3: Fix Bug in Calculator

1. **Find relevant component:**
   ```bash
   # Search for the feature
   grep -r "keyword" src/pages/
   ```

2. **Read component code**

3. **Make fix following React patterns**

4. **Test with dev server:**
   ```bash
   make debug
   ```

## Build and Deployment

**Production build:**
```bash
make build
# Creates optimized bundle in build/
```

**Deployment:**
```bash
# See deployment configuration
cat netlify.toml  # or appropriate config
```

**Environment variables:**
```bash
# React env vars must have REACT_APP_ prefix
REACT_APP_API_URL=https://api.policyengine.org

# Or use config file pattern (recommended)
cat src/config/environment.js
```

## Style Guide

**Follow policyengine-standards-skill for:**
- ESLint configuration
- Prettier formatting
- Component size limits
- File organization

**Follow policyengine-writing-skill for:**
- Blog post content
- Documentation
- UI copy

## Resources

**Repository:** https://github.com/PolicyEngine/policyengine-app
**Live app:** https://policyengine.org
**Staging:** https://staging.policyengine.org (if applicable)

**Related skills:**
- **policyengine-api-skill** - Understanding the backend
- **policyengine-us-skill** - Understanding variables/parameters
- **policyengine-writing-skill** - Blog post style
- **policyengine-standards-skill** - Code quality
