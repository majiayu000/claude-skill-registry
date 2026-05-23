---
name: osmani-patterns-performance
description: Write JavaScript code in the style of Addy Osmani, author of "Learning JavaScript Design Patterns" and Chrome DevTools engineer. Emphasizes design patterns, performance optimization, and progressive web apps. Use when building performant, well-structured applications.
---

# Addy Osmani Style Guide

## Overview

Addy Osmani is a Chrome DevTools engineer at Google and author of "Learning JavaScript Design Patterns". His philosophy emphasizes proven design patterns, performance optimization, and building for the modern web.

## Core Philosophy

> "First do it, then do it right, then do it better."

> "Performance is not a feature, it's a necessity."

> "The best request is the one that's never made."

Osmani believes in using battle-tested patterns and obsessively optimizing for user experience through performance.

## Design Principles

1. **Patterns Have Purpose**: Use design patterns to solve specific problems.

2. **Performance First**: Measure, optimize, measure again.

3. **Progressive Enhancement**: Build for all users, enhance for modern browsers.

4. **Loading Performance**: The fastest code is code that never runs.

## When Writing Code

### Always

- Use appropriate design patterns for the problem
- Measure performance before and after optimization
- Consider loading performance and bundle size
- Implement code splitting for large applications
- Use lazy loading for non-critical resources
- Test on real devices and slow connections

### Never

- Apply patterns where they don't fit
- Optimize without measuring
- Load all JavaScript upfront
- Ignore Core Web Vitals
- Block the main thread with heavy computation
- Ship unused JavaScript

### Prefer

- Module pattern for encapsulation
- Observer pattern for event systems
- Factory pattern for object creation
- Dynamic imports over static imports for large modules
- Intersection Observer over scroll events
- CSS containment for rendering performance

## Code Patterns

### The Module Pattern

```javascript
// Classic Module Pattern - encapsulation and privacy
const ShoppingCart = (function() {
    // Private variables and methods
    const items = [];
    
    function calculateTotal() {
        return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
    }
    
    // Public API
    return {
        addItem(item) {
            items.push(item);
        },
        
        removeItem(id) {
            const index = items.findIndex(item => item.id === id);
            if (index > -1) {
                items.splice(index, 1);
            }
        },
        
        getTotal() {
            return calculateTotal();
        },
        
        getItems() {
            return [...items];  // Return copy, not reference
        }
    };
})();


// ES Modules version
// cart.js
const items = [];

function calculateTotal() {
    return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
}

export function addItem(item) {
    items.push(item);
}

export function getTotal() {
    return calculateTotal();
}
```

### The Observer Pattern

```javascript
class EventEmitter {
    constructor() {
        this.events = new Map();
    }
    
    on(event, callback) {
        if (!this.events.has(event)) {
            this.events.set(event, []);
        }
        this.events.get(event).push(callback);
        
        // Return unsubscribe function
        return () => this.off(event, callback);
    }
    
    off(event, callback) {
        if (!this.events.has(event)) return;
        
        const callbacks = this.events.get(event);
        const index = callbacks.indexOf(callback);
        if (index > -1) {
            callbacks.splice(index, 1);
        }
    }
    
    emit(event, data) {
        if (!this.events.has(event)) return;
        
        this.events.get(event).forEach(callback => {
            callback(data);
        });
    }
}

// Usage
const emitter = new EventEmitter();

const unsubscribe = emitter.on('userLogin', (user) => {
    console.log(`${user.name} logged in`);
});

emitter.emit('userLogin', { name: 'Alice' });
unsubscribe();  // Clean up
```

### The Factory Pattern

```javascript
// Factory for creating different notification types
const NotificationFactory = {
    create(type, message) {
        const notifications = {
            success: {
                icon: '✓',
                color: 'green',
                duration: 3000
            },
            error: {
                icon: '✗',
                color: 'red',
                duration: 5000
            },
            warning: {
                icon: '⚠',
                color: 'orange',
                duration: 4000
            }
        };
        
        const config = notifications[type] || notifications.success;
        
        return {
            ...config,
            message,
            show() {
                console.log(`[${this.icon}] ${this.message}`);
            }
        };
    }
};

// Usage
const success = NotificationFactory.create('success', 'Saved!');
const error = NotificationFactory.create('error', 'Failed to save');
```

### Performance: Code Splitting

```javascript
// Dynamic imports for route-based code splitting
const routes = {
    '/': () => import('./pages/Home.js'),
    '/dashboard': () => import('./pages/Dashboard.js'),
    '/settings': () => import('./pages/Settings.js')
};

async function navigate(path) {
    const loadPage = routes[path];
    if (loadPage) {
        const module = await loadPage();
        module.default.render();
    }
}


// React.lazy for component-level splitting
const Dashboard = React.lazy(() => import('./Dashboard'));

function App() {
    return (
        <Suspense fallback={<Spinner />}>
            <Dashboard />
        </Suspense>
    );
}


// Prefetch critical routes on idle
function prefetchRoutes() {
    if ('requestIdleCallback' in window) {
        requestIdleCallback(() => {
            routes['/dashboard']();
        });
    }
}
```

### Performance: Lazy Loading

```javascript
// Intersection Observer for lazy loading
function lazyLoad(selector) {
    const elements = document.querySelectorAll(selector);
    
    const observer = new IntersectionObserver((entries, obs) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                obs.unobserve(img);
            }
        });
    }, {
        rootMargin: '50px 0px',  // Start loading 50px before visible
        threshold: 0.01
    });
    
    elements.forEach(el => observer.observe(el));
}

// HTML
// <img class="lazy" data-src="image.jpg" alt="...">


// Lazy load modules on interaction
let heavyModule = null;

button.addEventListener('click', async () => {
    if (!heavyModule) {
        heavyModule = await import('./heavyModule.js');
    }
    heavyModule.doSomething();
});
```

### Performance: Debounce and Throttle

```javascript
// Debounce: wait until calls stop
function debounce(fn, delay) {
    let timeoutId;
    
    return function(...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => {
            fn.apply(this, args);
        }, delay);
    };
}

// Use for: search input, resize handlers, save drafts
const debouncedSearch = debounce(query => {
    api.search(query);
}, 300);


// Throttle: limit call frequency
function throttle(fn, limit) {
    let inThrottle;
    
    return function(...args) {
        if (!inThrottle) {
            fn.apply(this, args);
            inThrottle = true;
            setTimeout(() => {
                inThrottle = false;
            }, limit);
        }
    };
}

// Use for: scroll handlers, mousemove, game loops
const throttledScroll = throttle(() => {
    updateScrollProgress();
}, 100);
```

### Performance: Virtualization

```javascript
// Virtual scrolling for large lists
class VirtualList {
    constructor(container, items, itemHeight) {
        this.container = container;
        this.items = items;
        this.itemHeight = itemHeight;
        this.visibleCount = Math.ceil(container.clientHeight / itemHeight) + 2;
        
        this.setup();
    }
    
    setup() {
        // Create viewport and content containers
        this.viewport = document.createElement('div');
        this.viewport.style.height = `${this.items.length * this.itemHeight}px`;
        
        this.content = document.createElement('div');
        this.content.style.position = 'relative';
        
        this.viewport.appendChild(this.content);
        this.container.appendChild(this.viewport);
        
        this.container.addEventListener('scroll', () => this.render());
        this.render();
    }
    
    render() {
        const scrollTop = this.container.scrollTop;
        const startIndex = Math.floor(scrollTop / this.itemHeight);
        const endIndex = Math.min(
            startIndex + this.visibleCount,
            this.items.length
        );
        
        this.content.innerHTML = '';
        this.content.style.transform = `translateY(${startIndex * this.itemHeight}px)`;
        
        for (let i = startIndex; i < endIndex; i++) {
            const item = document.createElement('div');
            item.style.height = `${this.itemHeight}px`;
            item.textContent = this.items[i];
            this.content.appendChild(item);
        }
    }
}
```

### The Singleton Pattern

```javascript
// Singleton for app-wide configuration
const Config = (function() {
    let instance;
    
    function createInstance() {
        return {
            apiUrl: 'https://api.example.com',
            timeout: 5000,
            debug: false,
            
            set(key, value) {
                this[key] = value;
            }
        };
    }
    
    return {
        getInstance() {
            if (!instance) {
                instance = createInstance();
            }
            return instance;
        }
    };
})();

// Usage - always same instance
const config1 = Config.getInstance();
const config2 = Config.getInstance();
config1 === config2;  // true
```

## Mental Model

Osmani approaches code by asking:

1. **What pattern fits this problem?** Use proven solutions
2. **What's the performance cost?** Measure before shipping
3. **Can this be deferred?** Load later if not critical
4. **Will this block the main thread?** Keep it responsive
5. **What are users on slow connections experiencing?** Test realistically

## Signature Osmani Moves

- Code splitting at route boundaries
- Lazy loading with Intersection Observer
- PRPL pattern (Push, Render, Pre-cache, Lazy-load)
- Module pattern for clean encapsulation
- Performance budgets and monitoring
- Progressive enhancement as default
