---
name: implementing-search-filter
description: Logic for constructing Appwrite queries to filter tours. Use when building the search sidebar or search bar.
---

# Search and Filter Logic

## When to use this skill
- Implementing filters for Location, Price, and Dates.
- Handling search queries.

## Appwrite Query Logic
```javascript
import { Query } from 'appwrite';

const queries = [
    Query.equal('location', selectedLocation),
    Query.greaterThanEqual('price', minPrice),
    Query.lessThanEqual('price', maxPrice),
    Query.orderAsc('price')
];

const results = await databases.listDocuments(DATABASE_ID, COLLECTION_ID, queries);
```

## Instructions
- **Debounce**: Debounce text input for location/name search.
- **Sync**: Keep URL params in sync with filter state for shareable links.
