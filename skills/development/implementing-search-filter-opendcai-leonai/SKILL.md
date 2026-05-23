---
name: implementing-search-filter
description: Implements search and filter interfaces for both frontend (React/TypeScript) and backend (Python) with debouncing, query management, and database integration. Use when adding search functionality, building filter UIs, implementing faceted search, or optimizing search performance.
---

# Search & Filter Implementation

Implement search and filter interfaces with comprehensive frontend components and backend query optimization.

## Purpose

This skill provides production-ready patterns for implementing search and filtering functionality across the full stack. It covers React/TypeScript components for the frontend (search inputs, filter UIs, autocomplete) and Python patterns for the backend (SQLAlchemy queries, Elasticsearch integration, API design). The skill emphasizes performance optimization, accessibility, and user experience.

## When to Use

- Building product search with category and price filters
- Implementing autocomplete/typeahead search
- Creating faceted search interfaces with dynamic counts
- Adding search to data tables or lists
- Building advanced boolean search for power users
- Implementing backend search with SQLAlchemy or Django ORM
- Integrating Elasticsearch for full-text search
- Optimizing search performance with debouncing and caching
- Creating accessible search experiences

## Core Components

### Frontend Search Patterns

**Search Input with Debouncing**
- Implement 300ms debounce for performance
- Show loading states during search
- Clear button (X) for resetting
- Keyboard shortcuts (Cmd/Ctrl+K)
- See `references/search-input-patterns.md`

**Autocomplete/Typeahead**
- Suggestion dropdown with keyboard navigation
- Highlight matched text in suggestions
- Recent searches and popular items
- Prevent request flooding with debouncing
- See `references/autocomplete-patterns.md`

**Filter UI Components**
- Checkbox filters for multi-select
- Range sliders for numerical values
- Dropdown filters for single selection
- Filter chips showing active selections
- See `references/filter-ui-patterns.md`

### Backend Query Patterns

**Database Query Building**
- Dynamic query construction with SQLAlchemy
- Django ORM filter chaining
- Index optimization for search columns
- Full-text search in PostgreSQL
- See `references/database-querying.md`

**Elasticsearch Integration**
- Document indexing strategies
- Query DSL for complex searches
- Faceted aggregations
- Relevance scoring and boosting
- See `references/elasticsearch-integration.md`

**API Design**
- RESTful search endpoints
- Query parameter validation
- Pagination with cursor/offset
- Response caching strategies
- See `references/api-design.md`

## Implementation Workflows

### Client-Side Search (<1000 items)

1. Load data into memory
2. Implement filter functions in JavaScript
3. Apply debounced search on text input
4. Update results instantly
5. Maintain filter state in React

### Server-Side Search (>1000 items)

1. Design search API endpoint
2. Validate and sanitize query parameters
3. Build database query dynamically
4. Apply pagination
5. Return results with metadata
6. Cache frequent queries

### Hybrid Approach

1. Use client-side filtering for immediate feedback
2. Fetch server results in background
3. Merge and deduplicate results
4. Update UI progressively
5. Cache recent searches locally

## Performance Optimization

### Frontend Optimization

**Debouncing Implementation**
- Use `debounce` from lodash or custom implementation
- Cancel pending requests on new input
- Show skeleton loaders during fetch
- Script: `scripts/debounce_calculator.js`

**Query Parameter Management**
- Sync filters with URL for shareable searches
- Use React Router or Next.js for URL state
- Compress complex queries
- See `references/query-parameter-management.md`

### Backend Optimization

**Query Optimization**
- Create appropriate database indexes
- Use query analyzers to identify bottlenecks
- Implement query result caching
- Script: `scripts/generate_filter_query.py`

**Validation & Security**
- Sanitize all search inputs
- Prevent SQL injection
- Rate limit search endpoints
- Script: `scripts/validate_search_params.py`

## Accessibility Requirements

### ARIA Patterns

- Use `role="search"` for search regions
- Implement `aria-live` for result updates
- Provide clear labels for filters
- Support keyboard-only navigation

### Keyboard Support

- Tab through all interactive elements
- Arrow keys for autocomplete navigation
- Escape to close dropdowns
- Enter to select/submit

## Technology Stack

### Frontend Libraries

**Primary: Downshift (Autocomplete)**
- Accessible autocomplete primitives
- Headless/unstyled for flexibility
- WAI-ARIA compliant
- Install: `npm install downshift`

**Alternative: React Select**
- Full-featured select/filter component
- Built-in async search
- Multi-select support

### Backend Technologies

**Python/SQLAlchemy**
- Dynamic query building
- Relationship loading optimization
- Query result pagination

**Python/Django**
- Django Filter backend
- Django REST Framework filters
- Full-text search with PostgreSQL

**Elasticsearch (Python)**
- elasticsearch-py client
- elasticsearch-dsl for query building

## Bundled Resources

### References
- `references/search-input-patterns.md` - Input implementations
- `references/autocomplete-patterns.md` - Typeahead patterns
- `references/filter-ui-patterns.md` - Filter components
- `references/database-querying.md` - SQL query patterns
- `references/elasticsearch-integration.md` - Elasticsearch setup
- `references/api-design.md` - API endpoint patterns
- `references/performance-optimization.md` - Performance tips
- `references/library-comparison.md` - Library evaluation

### Scripts
- `scripts/generate_filter_query.py` - Build SQL/ES queries
- `scripts/validate_search_params.py` - Validate inputs
- `scripts/debounce_calculator.js` - Calculate debounce timing

### Examples
- `examples/product-search.tsx` - E-commerce search
- `examples/autocomplete-search.tsx` - Autocomplete implementation
- `examples/sqlalchemy_search.py` - SQLAlchemy patterns
- `examples/fastapi_search.py` - FastAPI search endpoint
- `examples/django_filter_backend.py` - Django filters

### Assets
- `assets/filter-config-schema.json` - Filter configuration
- `assets/search-api-spec.json` - OpenAPI specification