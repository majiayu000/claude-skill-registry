---
name: vue-component
description: Create a new Vue 3 component following this project's patterns. Use when creating POS components, backoffice components, or modals.
argument-hint: [ComponentName] [type: pos|backoffice|modal]
disable-model-invocation: true
---

# Create Vue Component

Create a new Vue 3 component for `$ARGUMENTS` following this project's established patterns.

## Project Structure

This project has TWO separate Vue applications:

### POS App (waitstaff interface)
- Entry: `resources/js/app.js`
- Router: `resources/js/router.js`
- Store: `resources/js/store.js` (modules: general, epos, printing)
- Components: `resources/js/components/`
  - `Tables/` - Table management
  - `InventoryOverview/` - Menu items
  - `Invoices/` - Invoice management
  - `Modals/` - Modal dialogs

### Backoffice App (admin interface)
- Entry: `resources/js/backoffice.js`
- Router: `resources/js/backofficeRouter.js`
- Store: `resources/js/backofficeStore.js` (modules: backoffice, printing)
- Components: `resources/js/components/Backoffice/`

## Component Patterns

### Standard Component Structure (Options API)
```vue
<template>
  <div class="component-wrapper">
    <!-- Template content -->
  </div>
</template>

<script>
export default {
  name: 'ComponentName',

  props: {
    item: {
      type: Object,
      required: true
    }
  },

  data() {
    return {
      loading: false,
      localState: null
    }
  },

  computed: {
    // Access Vuex getters
    items() {
      return this.$store.getters.items
    },

    // Computed from props
    formattedPrice() {
      return this.$filters.formatPrice(this.item.price)
    }
  },

  mounted() {
    this.loadData()
  },

  methods: {
    async loadData() {
      this.loading = true
      await this.$store.dispatch('loadItems')
      this.loading = false
    },

    handleClick() {
      this.$emit('selected', this.item)
    }
  }
}
</script>
```

### Modal Component Pattern
```vue
<template>
  <Modal @close="$emit('close')">
    <template #header>
      <h3>Modal Title</h3>
    </template>

    <template #body>
      <!-- Modal content -->
    </template>

    <template #footer>
      <button @click="$emit('close')">Cancel</button>
      <button @click="save">Save</button>
    </template>
  </Modal>
</template>

<script>
import Modal from './Modal.vue'

export default {
  components: { Modal },

  props: {
    data: Object
  },

  emits: ['close', 'saved'],

  methods: {
    async save() {
      // API call
      await axios.post('/api/resource', this.data)
      this.$emit('saved')
      this.$emit('close')
    }
  }
}
</script>
```

### Backoffice List Component Pattern
```vue
<template>
  <div>
    <!-- Filters -->
    <div class="filters">
      <input v-model="search" @input="debouncedSearch" placeholder="Search...">
      <Select v-model="category" :options="categories" />
    </div>

    <!-- Table -->
    <table>
      <thead>
        <tr>
          <th>Name</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <BackofficeItemRow
          v-for="item in items"
          :key="item.id"
          :item="item"
          @edit="openEdit"
          @delete="confirmDelete"
        />
      </tbody>
    </table>

    <!-- Pagination -->
    <Pagination
      :current="pagination.current_page"
      :total="pagination.last_page"
      @change="loadPage"
    />
  </div>
</template>

<script>
import _ from 'lodash'

export default {
  data() {
    return {
      search: '',
      category: null
    }
  },

  computed: {
    items() {
      return this.$store.state.backoffice.items
    },
    pagination() {
      return this.$store.state.backoffice.pagination
    }
  },

  created() {
    this.debouncedSearch = _.debounce(this.performSearch, 300)
  },

  mounted() {
    this.$store.dispatch('backoffice/getItems')
  },

  methods: {
    performSearch() {
      this.$store.dispatch('backoffice/getItems', { q: this.search })
    },
    loadPage(page) {
      this.$store.dispatch('backoffice/getItems', { page })
    }
  }
}
</script>
```

## Global Utilities Available

### Filters (via this.$filters)
```javascript
this.$filters.formatPrice(1000)     // "1.000" (POS) or "1.000,00" (Backoffice)
this.$filters.formatDate(date)      // Localized date
this.$filters.imgUrl(path)          // Full image URL
```

### Global Libraries
```javascript
window.axios    // HTTP client
window._        // Lodash
window.dayjs    // Date manipulation
```

## Styling

Use Tailwind CSS classes. Common patterns:
```html
<!-- Card -->
<div class="bg-white rounded-lg shadow p-4">

<!-- Button -->
<button class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">

<!-- Input -->
<input class="border rounded px-3 py-2 focus:ring-2 focus:ring-blue-500">

<!-- Grid -->
<div class="grid grid-cols-3 gap-4">
```

## Steps

1. Create component file in appropriate directory
2. If POS component, consider adding to router.js
3. If Backoffice component, add to backofficeRouter.js
4. If needs state, add Vuex actions/mutations
5. Import and register in parent component
