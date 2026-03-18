---
name: zero-build-frontend
description: Zero-build frontend development with CDN-loaded React, Tailwind CSS, and vanilla JavaScript. Use when building static web apps without bundlers, creating Leaflet maps, integrating Google Sheets as database, or developing browser extensions. Covers patterns from rosen-frontend, NJCIC map, and PocketLink projects.
---

# Zero-build frontend development

Patterns for building production-quality web applications without build tools, bundlers, or complex toolchains.

## React via CDN (esm.sh)

### Basic setup

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Zero-Build React App</title>

  <!-- Tailwind CSS via CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      theme: {
        extend: {
          fontFamily: {
            display: ['Special Elite', 'monospace'],
            body: ['Roboto Mono', 'monospace'],
          },
          colors: {
            brand: {
              primary: '#2dc8d2',
              secondary: '#f34213',
              dark: '#183642',
            }
          }
        }
      }
    }
  </script>

  <!-- Google Fonts -->
  <link href="https://fonts.googleapis.com/css2?family=Special+Elite&family=Roboto+Mono:wght@400;500;700&display=swap" rel="stylesheet">

  <!-- Custom styles -->
  <link rel="stylesheet" href="index.css">
</head>
<body>
  <div id="root"></div>

  <!-- ES Module imports -->
  <script type="importmap">
  {
    "imports": {
      "react": "https://esm.sh/react@18.2.0",
      "react-dom/client": "https://esm.sh/react-dom@18.2.0/client",
      "htm": "https://esm.sh/htm@3.1.1"
    }
  }
  </script>

  <script type="module" src="index.js"></script>
</body>
</html>
```

### React with htm (no JSX, no build)

```javascript
// index.js
import React, { useState, useEffect, useRef } from 'react';
import { createRoot } from 'react-dom/client';
import htm from 'htm';

// Bind htm to React.createElement
const html = htm.bind(React.createElement);

// Components use html`` instead of JSX
function App() {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');

  useEffect(() => {
    loadData();
  }, []);

  async function loadData() {
    try {
      const response = await fetch('data/archive-data.json');
      const data = await response.json();
      setRecords(data.records);
    } catch (error) {
      console.error('Failed to load data:', error);
    } finally {
      setLoading(false);
    }
  }

  const filtered = records.filter(r =>
    r.title.toLowerCase().includes(search.toLowerCase())
  );

  if (loading) {
    return html`<div class="flex items-center justify-center h-screen">
      <div class="animate-spin w-8 h-8 border-4 border-brand-primary border-t-transparent rounded-full"></div>
    </div>`;
  }

  return html`
    <div class="min-h-screen bg-gray-900 text-white">
      <header class="p-4 border-b border-gray-700">
        <h1 class="font-display text-2xl">Archive Explorer</h1>
        <input
          type="text"
          placeholder="Search records..."
          value=${search}
          onInput=${(e) => setSearch(e.target.value)}
          class="mt-2 w-full p-2 bg-gray-800 rounded border border-gray-600 focus:border-brand-primary outline-none"
        />
      </header>

      <main class="p-4">
        <${RecordList} records=${filtered} />
      </main>
    </div>
  `;
}

function RecordList({ records }) {
  return html`
    <div class="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
      ${records.map(record => html`
        <${RecordCard} key=${record.id} record=${record} />
      `)}
    </div>
  `;
}

function RecordCard({ record }) {
  return html`
    <article class="p-4 bg-gray-800 rounded-lg border border-gray-700 hover:border-brand-primary transition-colors">
      <h2 class="font-display text-lg mb-2">${record.title}</h2>
      <p class="text-sm text-gray-400 mb-2">${record.publication_date}</p>
      <p class="text-sm line-clamp-3">${record.summary}</p>
      <div class="mt-2 flex flex-wrap gap-1">
        ${record.tags?.map(tag => html`
          <span key=${tag} class="px-2 py-1 text-xs bg-gray-700 rounded">${tag}</span>
        `)}
      </div>
    </article>
  `;
}

// Mount app
const root = createRoot(document.getElementById('root'));
root.render(html`<${App} />`);
```

## Data caching with localStorage

```javascript
// services/cacheService.js

const CACHE_TTL = 60 * 60 * 1000; // 1 hour

export function getCached(key) {
  const cached = localStorage.getItem(key);
  if (!cached) return null;

  try {
    const { data, timestamp } = JSON.parse(cached);
    if (Date.now() - timestamp > CACHE_TTL) {
      localStorage.removeItem(key);
      return null;
    }
    return data;
  } catch {
    localStorage.removeItem(key);
    return null;
  }
}

export function setCache(key, data) {
  localStorage.setItem(key, JSON.stringify({
    data,
    timestamp: Date.now()
  }));
}

export async function fetchWithCache(url, cacheKey) {
  // Check cache first
  const cached = getCached(cacheKey);
  if (cached) return cached;

  // Fetch fresh data
  const response = await fetch(url);
  const data = await response.json();

  // Cache for next time
  setCache(cacheKey, data);

  return data;
}

// Usage
const records = await fetchWithCache('data/archive-data.json', 'archive-records');
```

## Leaflet.js maps

### Basic map setup

```html
<!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
  <link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.4.1/dist/MarkerCluster.css" />
  <link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.4.1/dist/MarkerCluster.Default.css" />
  <style>
    #map { height: 85vh; width: 100%; }
  </style>
</head>
<body>
  <div id="map"></div>

  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
  <script src="https://unpkg.com/leaflet.markercluster@1.4.1/dist/leaflet.markercluster.js"></script>
  <script src="js/app.js"></script>
</body>
</html>
```

### Map application with clustering

```javascript
// js/app.js

class MapApp {
  constructor() {
    this.map = null;
    this.markers = null;
    this.data = [];
    this.filters = {
      year: null,
      county: null,
      status: null
    };
  }

  async init() {
    this.setupMap();
    await this.loadData();
    this.renderMarkers();
    this.setupFilters();
  }

  setupMap() {
    // Initialize map centered on NJ
    this.map = L.map('map', {
      center: [40.0583, -74.4057],
      zoom: 8,
      scrollWheelZoom: false,  // Disable mouse wheel zoom
      zoomControl: false       // We'll add custom controls
    });

    // Add tile layer (CARTO Voyager)
    L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
      attribution: '&copy; OpenStreetMap, &copy; CARTO',
      maxZoom: 19
    }).addTo(this.map);

    // Add custom zoom control (top-right)
    L.control.zoom({ position: 'topright' }).addTo(this.map);

    // Initialize marker cluster group
    this.markers = L.markerClusterGroup({
      spiderfyOnMaxZoom: true,
      showCoverageOnHover: false,
      maxClusterRadius: 50,
      spiderLegPolylineOptions: { weight: 1.5, color: '#2dc8d2' }
    });

    this.map.addLayer(this.markers);
  }

  async loadData() {
    const response = await fetch('data/grantees.json');
    this.data = await response.json();
  }

  renderMarkers() {
    this.markers.clearLayers();

    const filtered = this.data.filter(item => {
      if (this.filters.year && item.year !== this.filters.year) return false;
      if (this.filters.county && item.county !== this.filters.county) return false;
      if (this.filters.status && item.status !== this.filters.status) return false;
      return true;
    });

    filtered.forEach(item => {
      if (!item.lat || !item.lng) return;

      const marker = L.marker([item.lat, item.lng], {
        icon: this.createIcon(item.status)
      });

      marker.bindPopup(this.createPopup(item));
      this.markers.addLayer(marker);
    });

    // Update count display
    document.getElementById('count').textContent = filtered.length;
  }

  createIcon(status) {
    const colors = {
      'Active': '#2dc8d2',
      'Completed': '#666666',
      'Pending': '#f34213'
    };

    return L.divIcon({
      html: `<div style="background: ${colors[status] || '#2dc8d2'}; width: 12px; height: 12px; border-radius: 50%; border: 2px solid white;"></div>`,
      className: 'custom-marker',
      iconSize: [16, 16],
      iconAnchor: [8, 8]
    });
  }

  createPopup(item) {
    return `
      <div class="popup-content">
        <h3 class="font-bold text-lg">${item.name}</h3>
        <p class="text-sm text-gray-600">${item.county} County</p>
        <p class="text-sm mt-2">${item.description || ''}</p>
        <div class="mt-2">
          <span class="px-2 py-1 text-xs rounded bg-gray-200">${item.status}</span>
          <span class="px-2 py-1 text-xs rounded bg-gray-200">${item.year}</span>
        </div>
        ${item.website ? `<a href="${item.website}" target="_blank" class="block mt-2 text-brand-primary">Visit Website →</a>` : ''}
      </div>
    `;
  }

  setupFilters() {
    // Year filter
    const years = [...new Set(this.data.map(d => d.year))].sort();
    const yearSelect = document.getElementById('year-filter');
    years.forEach(year => {
      const option = document.createElement('option');
      option.value = year;
      option.textContent = year;
      yearSelect.appendChild(option);
    });

    yearSelect.addEventListener('change', (e) => {
      this.filters.year = e.target.value || null;
      this.renderMarkers();
    });

    // Similar for county, status filters...
  }
}

// Initialize on load
document.addEventListener('DOMContentLoaded', () => {
  const app = new MapApp();
  app.init();
});
```

## Google Sheets as database

### Fetching published CSV

```javascript
// Google Sheets published as CSV
const SHEET_URL = 'https://docs.google.com/spreadsheets/d/e/SPREADSHEET_ID/pub?gid=0&single=true&output=csv';

async function loadFromSheets() {
  const response = await fetch(SHEET_URL);
  const csv = await response.text();

  // Parse with PapaParse (CDN)
  const { data, errors } = Papa.parse(csv, {
    header: true,
    skipEmptyLines: true,
    transformHeader: (h) => h.trim().toLowerCase().replace(/\s+/g, '_')
  });

  if (errors.length > 0) {
    console.warn('CSV parsing errors:', errors);
  }

  return data;
}
```

### Real-time state with localStorage

```javascript
class DataManager {
  constructor(sheetUrl, cacheKey) {
    this.sheetUrl = sheetUrl;
    this.cacheKey = cacheKey;
    this.data = [];
    this.localState = this.loadLocalState();
  }

  loadLocalState() {
    const stored = localStorage.getItem(`${this.cacheKey}-state`);
    return stored ? JSON.parse(stored) : {};
  }

  saveLocalState() {
    localStorage.setItem(`${this.cacheKey}-state`, JSON.stringify(this.localState));
  }

  async refresh() {
    const response = await fetch(this.sheetUrl);
    const csv = await response.text();
    this.data = Papa.parse(csv, { header: true, skipEmptyLines: true }).data;

    // Merge with local state
    this.data.forEach(row => {
      const localData = this.localState[row.id];
      if (localData) {
        Object.assign(row, localData);
      }
    });

    return this.data;
  }

  updateLocal(id, updates) {
    this.localState[id] = { ...this.localState[id], ...updates };
    this.saveLocalState();

    // Update in-memory data too
    const item = this.data.find(d => d.id === id);
    if (item) Object.assign(item, updates);
  }
}

// Usage
const manager = new DataManager(SHEET_URL, 'volunteer-data');
await manager.refresh();

// Mark task as complete (stored locally)
manager.updateLocal('task-123', { completed: true, completed_at: new Date().toISOString() });
```

## Browser extension (Manifest V3)

### manifest.json

```json
{
  "manifest_version": 3,
  "name": "PocketLink",
  "version": "1.0.0",
  "description": "Create shortlinks from right-click context menu",

  "permissions": [
    "contextMenus",
    "storage",
    "activeTab",
    "scripting",
    "notifications",
    "offscreen"
  ],

  "background": {
    "service_worker": "background.js",
    "type": "module"
  },

  "action": {
    "default_popup": "popup.html",
    "default_icon": {
      "16": "icons/icon16.png",
      "48": "icons/icon48.png",
      "128": "icons/icon128.png"
    }
  },

  "options_page": "options.html",

  "icons": {
    "16": "icons/icon16.png",
    "48": "icons/icon48.png",
    "128": "icons/icon128.png"
  }
}
```

### Service worker (background.js)

```javascript
// background.js - Service Worker

// Create context menu on install
chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: 'create-shortlink',
    title: 'Create Shortlink',
    contexts: ['page', 'link']
  });
});

// Handle context menu click
chrome.contextMenus.onClicked.addListener(async (info, tab) => {
  if (info.menuItemId !== 'create-shortlink') return;

  const url = info.linkUrl || info.pageUrl;

  try {
    const shortUrl = await createShortlink(url);
    await copyToClipboard(shortUrl);
    showNotification('Shortlink Created', shortUrl);
  } catch (error) {
    showNotification('Error', error.message);
  }
});

async function createShortlink(longUrl) {
  const { apiToken } = await chrome.storage.sync.get('apiToken');
  if (!apiToken) throw new Error('API token not configured');

  const response = await fetch('https://api-ssl.bitly.com/v4/shorten', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${apiToken}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ long_url: longUrl })
  });

  if (!response.ok) throw new Error('API request failed');

  const data = await response.json();
  return data.link;
}

// Clipboard methods (three fallback strategies)

// Method 1: Offscreen API (preferred)
async function copyToClipboard(text) {
  try {
    await copyViaOffscreen(text);
  } catch {
    try {
      await copyViaContentScript(text);
    } catch {
      await copyViaPopup(text);
    }
  }
}

async function copyViaOffscreen(text) {
  await chrome.offscreen.createDocument({
    url: 'offscreen.html',
    reasons: ['CLIPBOARD'],
    justification: 'Copy shortlink to clipboard'
  });

  await chrome.runtime.sendMessage({ type: 'copy', text });
  await chrome.offscreen.closeDocument();
}

async function copyViaContentScript(text) {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  await chrome.scripting.executeScript({
    target: { tabId: tab.id },
    func: (text) => navigator.clipboard.writeText(text),
    args: [text]
  });
}

function showNotification(title, message) {
  chrome.notifications.create({
    type: 'basic',
    iconUrl: 'icons/icon48.png',
    title,
    message
  });
}
```

### Options page

```html
<!-- options.html -->
<!DOCTYPE html>
<html>
<head>
  <style>
    /* Inline CSS for extension compliance (no remote code) */
    body {
      font-family: system-ui, sans-serif;
      padding: 20px;
      max-width: 400px;
      margin: 0 auto;
    }
    h1 { font-size: 1.5rem; margin-bottom: 1rem; }
    label { display: block; margin-bottom: 0.5rem; font-weight: 500; }
    input {
      width: 100%;
      padding: 8px;
      border: 1px solid #ccc;
      border-radius: 4px;
      font-size: 14px;
    }
    button {
      margin-top: 1rem;
      padding: 10px 20px;
      background: #2dc8d2;
      color: white;
      border: none;
      border-radius: 4px;
      cursor: pointer;
    }
    button:hover { background: #25a8b0; }
    .status { margin-top: 1rem; padding: 10px; border-radius: 4px; }
    .success { background: #d4edda; color: #155724; }
    .error { background: #f8d7da; color: #721c24; }
  </style>
</head>
<body>
  <h1>PocketLink Settings</h1>

  <label for="apiToken">Bit.ly API Token</label>
  <input type="password" id="apiToken" placeholder="Enter your API token">

  <button id="save">Save Settings</button>

  <div id="status" class="status" style="display: none;"></div>

  <script src="options.js"></script>
</body>
</html>
```

```javascript
// options.js
document.addEventListener('DOMContentLoaded', async () => {
  const tokenInput = document.getElementById('apiToken');
  const saveButton = document.getElementById('save');
  const status = document.getElementById('status');

  // Load saved token
  const { apiToken } = await chrome.storage.sync.get('apiToken');
  if (apiToken) tokenInput.value = apiToken;

  saveButton.addEventListener('click', async () => {
    const token = tokenInput.value.trim();

    if (!token) {
      showStatus('Please enter an API token', 'error');
      return;
    }

    // Validate token by making test request
    try {
      const response = await fetch('https://api-ssl.bitly.com/v4/user', {
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (!response.ok) throw new Error('Invalid token');

      await chrome.storage.sync.set({ apiToken: token });
      showStatus('Settings saved successfully!', 'success');
    } catch {
      showStatus('Invalid API token', 'error');
    }
  });

  function showStatus(message, type) {
    status.textContent = message;
    status.className = `status ${type}`;
    status.style.display = 'block';
    setTimeout(() => { status.style.display = 'none'; }, 3000);
  }
});
```

## Cache busting for deployments

```html
<!-- Manual versioning for static files -->
<link rel="stylesheet" href="styles.css?v=1.3.0">
<script src="app.js?v=1.3.0"></script>

<!-- Or use build timestamp -->
<script>
  const version = Date.now();
  document.write(`<link rel="stylesheet" href="styles.css?v=${version}">`);
</script>
```

## Deployment patterns

### Static hosting (FTP/SFTP)
```
# Directory structure for WordPress wp-content deployment
wp-content/
└── archive-explorer/
    ├── index.html
    ├── index.js
    ├── index.css
    ├── components/
    │   ├── Sidebar.js
    │   ├── RecordList.js
    │   └── RecordCard.js
    └── data/
        └── archive-data.json
```

### Path management for subdirectory deployment
```javascript
// constants.js

// Auto-detect base path from current URL
const getBasePath = () => {
  const path = window.location.pathname;
  const lastSlash = path.lastIndexOf('/');
  return path.substring(0, lastSlash + 1);
};

export const BASE_PATH = getBasePath();
export const DATA_URL = `${BASE_PATH}data/archive-data.json`;

// Usage
const response = await fetch(DATA_URL);
```

## Performance tips

- **Lazy load large JSON**: Parse incrementally or paginate
- **Use CSS containment**: `contain: layout style` on repeated elements
- **Debounce search input**: Wait 300ms after typing stops
- **Virtualize long lists**: Only render visible items
- **Preconnect to CDNs**: `<link rel="preconnect" href="https://esm.sh">`
