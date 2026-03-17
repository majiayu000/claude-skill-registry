# Search Optimization Skill

## Purpose
Master Fuse.js fuzzy search implementation and optimization for fast, accurate tune search in the music-app project.

## Fuse.js Configuration

### Optimized Setup
```javascript
import Fuse from 'fuse.js';

const fuseOptions = {
  keys: [
    { name: 'Tune Title', weight: 0.5 },  // Most important
    { name: 'Genre', weight: 0.2 },
    { name: 'Rhythm', weight: 0.2 },
    { name: 'Key', weight: 0.1 }
  ],
  threshold: 0.3,              // 0 = perfect match, 1 = match anything
  distance: 100,               // Character distance to search
  minMatchCharLength: 2,       // Min query length
  ignoreLocation: true,        // Don't weight by position
  findAllMatches: false,       // Stop at first match (faster)
  useExtendedSearch: false,    // Disable if not needed
};

let fuseInstance = null;

export const initializeSearch = (data) => {
  if (!fuseInstance) {
    fuseInstance = new Fuse(data, fuseOptions);
  }
  return fuseInstance;
};

export const search = (query) => {
  if (!fuseInstance) {
    console.error('Fuse not initialized');
    return [];
  }

  if (!query || query.length < 2) {
    return [];
  }

  const results = fuseInstance.search(query);
  return results.map(result => result.item);
};
```

## Configuration Parameters

### Threshold
```javascript
// 0.0 = Perfect match only
threshold: 0.0,

// 0.3 = Good balance (recommended)
threshold: 0.3,

// 0.6 = Very fuzzy (matches anything similar)
threshold: 0.6,
```

### Keys (What to Search)
```javascript
// Simple array
keys: ['Tune Title', 'Genre']

// With weights
keys: [
  { name: 'Tune Title', weight: 0.7 },  // More important
  { name: 'Genre', weight: 0.3 }        // Less important
]

// Nested paths
keys: ['metadata.title', 'metadata.artist']
```

### Performance Options
```javascript
const fastOptions = {
  threshold: 0.3,
  minMatchCharLength: 3,     // Require longer queries
  ignoreLocation: true,      // Faster than location-aware
  findAllMatches: false,     // Stop at first match
  shouldSort: false,         // Skip sorting if not needed
};
```

## Debouncing Search

### With Lodash
```javascript
import { debounce } from 'lodash';

const debouncedSearch = debounce((query) => {
  const results = fuseInstance.search(query);
  setSearchResults(results);
}, 300); // Wait 300ms after typing stops
```

### Custom Hook
```javascript
function useSearch(data, options) {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const fuseRef = useRef(null);

  useEffect(() => {
    if (!fuseRef.current && data.length > 0) {
      fuseRef.current = new Fuse(data, options);
    }
  }, [data, options]);

  const debouncedSearch = useMemo(
    () => debounce((searchQuery) => {
      if (!searchQuery || searchQuery.length < 2) {
        setResults([]);
        return;
      }

      const searchResults = fuseRef.current.search(searchQuery);
      setResults(searchResults.map(r => r.item));
    }, 300),
    []
  );

  useEffect(() => {
    debouncedSearch(query);
  }, [query, debouncedSearch]);

  return { query, setQuery, results };
}
```

## Best Practices

✅ **Do:**
- Initialize Fuse once, reuse instance
- Debounce search input (300ms recommended)
- Limit indexed fields to essentials
- Set reasonable threshold (0.3 is good default)
- Require minimum query length (2-3 chars)

❌ **Don't:**
- Create new Fuse instance on every search
- Index unnecessary fields (slower)
- Set threshold too low (too strict) or too high (too fuzzy)
- Search on every keystroke without debouncing
- Forget to handle empty queries

## Performance Optimization

### Index Only What's Needed
```javascript
// ❌ Too many fields
keys: ['title', 'description', 'content', 'tags', 'author', 'date']

// ✅ Essential fields only
keys: ['title', 'tags']
```

### Limit Results
```javascript
const results = fuseInstance.search(query, { limit: 20 });
```

### Pre-filter Data
```javascript
// Filter first, then search
const activeCategory = 'Irish Traditional';
const filtered = tunes.filter(t => t.Genre === activeCategory);
const fuse = new Fuse(filtered, options);
const results = fuse.search(query);
```

## Extended Search (Advanced)

```javascript
// Enable extended search
const options = {
  useExtendedSearch: true,
  keys: ['Tune Title']
};

// Exact match
fuse.search("='The Butterfly'")

// Prefix match
fuse.search("^The")

// Suffix match
fuse.search("!fly$")

// Include/exclude
fuse.search("butterfly !moth")
```

## Project Implementation

### tunesService.js Pattern
```javascript
let tunesData = [];
let fuseInstance = null;

export const initializeTunesData = async () => {
  if (tunesData.length > 0) return tunesData;

  // Load CSV
  const response = await fetch('/data/tunes_data.csv');
  const csvText = await response.text();

  return new Promise((resolve) => {
    Papa.parse(csvText, {
      header: true,
      complete: (results) => {
        tunesData = results.data;

        // Initialize Fuse
        fuseInstance = new Fuse(tunesData, {
          keys: ['Tune Title', 'Genre', 'Rhythm', 'Key', 'Mode'],
          threshold: 0.3
        });

        resolve(tunesData);
      }
    });
  });
};

export const searchTunes = (query) => {
  if (!fuseInstance) {
    console.error('Search not initialized');
    return [];
  }

  if (!query || query.length < 2) {
    return tunesData; // Return all if no query
  }

  const results = fuseInstance.search(query);
  return results.map(result => result.item);
};
```

## Common Issues

**Issue:** Search is slow
**Solution:** Reduce indexed fields, debounce input, limit results

**Issue:** No results for valid searches
**Solution:** Check threshold (increase if too strict), verify data loaded

**Issue:** Too many irrelevant results
**Solution:** Decrease threshold, adjust key weights, require longer queries

**Issue:** Search not updating
**Solution:** Check Fuse instance initialized, verify state updates

## Comparison: Fuse.js vs Array.filter

### Array.filter (Session Tunes)
```javascript
const filtered = tunes.filter(tune =>
  tune.name.toLowerCase().includes(query.toLowerCase()) ||
  tune.type.toLowerCase().includes(query.toLowerCase())
);
```
- **Pros**: Simple, no library, fast for small datasets
- **Cons**: No fuzzy matching, case-sensitive without toLowerCase

### Fuse.js (Hatao Tunes)
```javascript
const results = fuseInstance.search(query);
```
- **Pros**: Fuzzy matching, typo tolerance, weighted scoring
- **Cons**: Setup overhead, slower for small datasets

**Recommendation**: Use Fuse.js for >100 items or when fuzzy search needed.
