# 🎨 UI-First Builder Skill

---
name: ui-first-builder
description: Build user interfaces first, then add logic - the visual-first development approach
---

## 🎯 Purpose

Develop applications by creating the UI first with mock data, then gradually adding real functionality.

## 📋 When to Use

- Starting new features
- Rapid prototyping
- Getting stakeholder feedback early
- When requirements are unclear

## 🔧 UI-First Workflow

```
┌─────────────────┐
│ 1. MOCKUP       │ ← Wireframe/Design
└────────┬────────┘
         ▼
┌─────────────────┐
│ 2. STATIC UI    │ ← HTML/CSS with mock data
└────────┬────────┘
         ▼
┌─────────────────┐
│ 3. COMPONENTS   │ ← Break into reusable parts
└────────┬────────┘
         ▼
┌─────────────────┐
│ 4. INTERACTIONS │ ← Add click handlers, forms
└────────┬────────┘
         ▼
┌─────────────────┐
│ 5. REAL DATA    │ ← Connect to APIs
└────────┬────────┘
         ▼
┌─────────────────┐
│ 6. POLISH       │ ← Animations, edge cases
└─────────────────┘
```

## 📝 Step-by-Step Guide

### Step 1: Create Mockup
```markdown
- Sketch the UI layout
- Identify key components
- Define user flow
- Get initial feedback
```

### Step 2: Static UI with Mock Data
```jsx
// Mock data first
const mockUsers = [
  { id: 1, name: 'John Doe', email: 'john@example.com' },
  { id: 2, name: 'Jane Smith', email: 'jane@example.com' },
];

// Static component
function UserList() {
  return (
    <div className="user-list">
      {mockUsers.map(user => (
        <div key={user.id} className="user-card">
          <h3>{user.name}</h3>
          <p>{user.email}</p>
        </div>
      ))}
    </div>
  );
}
```

### Step 3: Extract Components
```jsx
// UserCard component
function UserCard({ user }) {
  return (
    <div className="user-card">
      <h3>{user.name}</h3>
      <p>{user.email}</p>
    </div>
  );
}

// UserList uses UserCard
function UserList({ users }) {
  return (
    <div className="user-list">
      {users.map(user => (
        <UserCard key={user.id} user={user} />
      ))}
    </div>
  );
}
```

### Step 4: Add Interactions
```jsx
function UserCard({ user, onSelect }) {
  return (
    <div 
      className="user-card"
      onClick={() => onSelect(user)}
    >
      <h3>{user.name}</h3>
      <p>{user.email}</p>
    </div>
  );
}
```

### Step 5: Connect Real Data
```jsx
function UserList() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/users')
      .then(res => res.json())
      .then(data => {
        setUsers(data);
        setLoading(false);
      });
  }, []);

  if (loading) return <LoadingSpinner />;
  
  return (
    <div className="user-list">
      {users.map(user => (
        <UserCard key={user.id} user={user} />
      ))}
    </div>
  );
}
```

### Step 6: Polish
```jsx
// Add animations, error states, empty states
function UserList() {
  const { users, loading, error } = useUsers();

  if (loading) return <Skeleton count={5} />;
  if (error) return <ErrorMessage error={error} />;
  if (users.length === 0) return <EmptyState />;
  
  return (
    <motion.div className="user-list" layout>
      {users.map(user => (
        <motion.div
          key={user.id}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
        >
          <UserCard user={user} />
        </motion.div>
      ))}
    </motion.div>
  );
}
```

## 🎨 Component Patterns

### Card Pattern
```jsx
function Card({ children, header, footer }) {
  return (
    <div className="card">
      {header && <div className="card-header">{header}</div>}
      <div className="card-body">{children}</div>
      {footer && <div className="card-footer">{footer}</div>}
    </div>
  );
}
```

### List Pattern
```jsx
function List({ items, renderItem, emptyMessage }) {
  if (items.length === 0) {
    return <p>{emptyMessage}</p>;
  }
  return (
    <ul className="list">
      {items.map((item, index) => (
        <li key={item.id || index}>{renderItem(item)}</li>
      ))}
    </ul>
  );
}
```

## ✅ UI-First Checklist

- [ ] Mockup reviewed and approved
- [ ] Static UI matches design
- [ ] Components are reusable
- [ ] All states handled (loading, error, empty)
- [ ] Interactions feel responsive
- [ ] Mobile responsive
- [ ] Animations smooth

## 🔗 Related Skills

- `design-mastery` - Design patterns
- `vision-to-code` - Convert designs
- `testing` - Test UI components
