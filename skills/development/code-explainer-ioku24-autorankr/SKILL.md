---
name: code-explainer
description: Explains code in beginner-friendly terms. Use when user asks 'what does this do', 'how does this work', 'explain this code', or needs to understand generated code. Breaks down complex code into simple explanations for learning.
---

# Code Explainer

Explains code in plain English so you can understand what it does, why it's structured that way, and learn as you build.

## When I Activate

I activate when you:
- Ask "what does this code do?"
- Ask "how does this work?"
- Say "explain this to me"
- Request understanding of generated code
- Want to learn why certain patterns are used
- Need to understand existing code before modifying it

## Explanation Philosophy

**Target Audience:** Beginner with little to no coding experience

**Approach:**
- Plain English, no jargon (or explain jargon when necessary)
- What/Why/How structure
- Real-world analogies
- Show the concept, then the implementation
- Highlight learning opportunities

---

## Explanation Format

### Standard Code Explanation

```
## What This Code Does

[High-level summary in one sentence]

## How It Works

[Step-by-step breakdown in plain English]

## Why It's Written This Way

[Explain design choices and patterns used]

## Key Concepts to Learn

[Highlight important programming concepts demonstrated]

## Related Documentation

[Links to learn more about key concepts]
```

---

## Explanation by Code Type

### Function Explanation

**Template:**
```
## What This Function Does
[Purpose in plain English]

## Parameters (Inputs)
- [param1]: [what it is and why it's needed]
- [param2]: [what it is and why it's needed]

## Return Value (Output)
[What it returns and what that represents]

## Step-by-Step Breakdown
1. [First thing the function does]
2. [Next thing]
3. [And so on...]

## Example Usage
[Show how to call this function with real data]
```

**Example:**
```javascript
function calculateTotal(items, taxRate) {
  const subtotal = items.reduce((sum, item) => sum + item.price, 0);
  const tax = subtotal * taxRate;
  return subtotal + tax;
}
```

**Explanation:**
```
## What This Function Does
Calculates the total price of items including tax.

## Parameters (Inputs)
- items: An array (list) of items, where each item has a price
- taxRate: The tax percentage (e.g., 0.08 for 8% tax)

## Return Value (Output)
The final total price after adding tax

## Step-by-Step Breakdown
1. Add up all the item prices to get a subtotal
   - Uses .reduce() which is like a running total calculator
2. Calculate the tax by multiplying subtotal by tax rate
   - If subtotal is $100 and tax rate is 0.08, tax = $8
3. Add the tax to the subtotal and return the final total

## Real-World Analogy
Like a cash register: it adds up all your items, calculates
sales tax, then gives you the final amount to pay.

## Key Concepts
- Array.reduce(): Method for calculating running totals
- Parameters: Inputs a function needs to do its job
- Return value: The answer the function gives back
```

---

### Component Explanation (React)

**Template:**
```
## What This Component Does
[Purpose - what the user sees/interacts with]

## Props (Inputs)
[Data passed to this component]

## State (Internal Data)
[Data this component manages itself]

## What Happens
1. [Initial render]
2. [User interactions]
3. [Updates and re-renders]

## Visual Result
[What the user actually sees]
```

**Example:**
```jsx
function LoginForm({ onLogin }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onLogin({ email, password });
  };

  return (
    <form onSubmit={handleSubmit}>
      <input value={email} onChange={(e) => setEmail(e.target.value)} />
      <input value={password} onChange={(e) => setPassword(e.target.value)} type="password" />
      <button type="submit">Log In</button>
    </form>
  );
}
```

**Explanation:**
```
## What This Component Does
Creates a login form where users can enter email and password.

## Props (Inputs)
- onLogin: A function to call when the form is submitted
  (passed down from parent component)

## State (Internal Data)
This component remembers:
- email: What the user typed in the email field
- password: What the user typed in the password field

## What Happens

1. **Initial Render:**
   - Shows two empty input boxes and a "Log In" button
   - Email and password start as empty strings

2. **As User Types:**
   - Every keystroke updates the email/password state
   - The input shows what user typed (controlled input)

3. **When User Clicks "Log In":**
   - Prevents page refresh (e.preventDefault)
   - Calls the onLogin function with email and password
   - Parent component handles the actual login logic

## Visual Result
User sees:
- Email input box
- Password input box (text hidden with dots)
- "Log In" button

## Key Concepts
- useState: React's way of remembering data
- Controlled inputs: Input value controlled by React state
- Event handlers: Functions that run when user interacts
- Props: Data passed from parent to child component

## Real-World Analogy
Like a paper form: You fill in the blanks (inputs), and when
you submit, someone else (parent component) processes it.
```

---

### API Call Explanation

**Template:**
```
## What This Code Does
[What API is being called and why]

## The Request
- Where: [API endpoint]
- Method: [GET/POST/etc.]
- Data sent: [Body/params if applicable]

## The Response
- Success: [What comes back if successful]
- Error: [How errors are handled]

## What Happens in the App
[How the response is used in the UI]
```

**Example:**
```javascript
async function fetchUserProfile(userId) {
  try {
    const response = await fetch(`/api/users/${userId}`);
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Failed to fetch user:', error);
    return null;
  }
}
```

**Explanation:**
```
## What This Code Does
Gets a user's profile information from the server.

## The Request
- Where: /api/users/[userId] (e.g., /api/users/123)
- Method: GET (asking for data, not sending any)
- Data sent: None (just asking for info)

## The Response
- Success: User data (name, email, etc.) as JSON
- Error: Logs error to console, returns null

## Step-by-Step Breakdown

1. **Send the request:**
   - Ask the server for user data using their userId
   - Wait for response (that's what "await" does)

2. **If successful:**
   - Convert the response to JavaScript object (response.json())
   - Return the user data

3. **If it fails:**
   - Log the error so we can see what went wrong
   - Return null (nothing) instead of crashing

## What Happens in the App
This function would be called like:
```javascript
const user = await fetchUserProfile(123);
if (user) {
  // Show user profile
} else {
  // Show error message
}
```

## Key Concepts
- async/await: Modern way to handle asynchronous operations
- try/catch: Error handling (what to do if something breaks)
- fetch: Browser's built-in way to make HTTP requests
- JSON: Data format for sending/receiving data from APIs

## Real-World Analogy
Like calling a library to ask about a book: You give them
the book number (userId), they look it up, and tell you the
details or say "book not found."
```

---

### Hook Explanation (React)

**Template:**
```
## What This Hook Does
[Purpose and when to use it]

## How to Use It
[Basic usage example]

## What It Returns
[What you get back and how to use it]

## Why Use This Instead of Alternatives
[Comparison to other approaches]
```

**Example:**
```javascript
function useUserData(userId) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchUserProfile(userId)
      .then(data => {
        setUser(data);
        setLoading(false);
      })
      .catch(err => {
        setError(err);
        setLoading(false);
      });
  }, [userId]);

  return { user, loading, error };
}
```

**Explanation:**
```
## What This Hook Does
Fetches and manages user data for a component. Handles loading
states and errors automatically.

## How to Use It
```javascript
function ProfilePage() {
  const { user, loading, error } = useUserData(123);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error loading user</div>;
  return <div>Hello {user.name}</div>;
}
```

## What It Returns
An object with three properties:
- user: The user data (or null if not loaded yet)
- loading: true while fetching, false when done
- error: null if successful, error message if failed

## What Happens

1. **Component First Renders:**
   - user is null (don't have data yet)
   - loading is true (actively fetching)
   - error is null (no errors yet)

2. **useEffect Runs:**
   - Fetches user data from API
   - When data comes back:
     - Updates user with the data
     - Sets loading to false

3. **Component Re-renders:**
   - Now has user data to display
   - loading is false, so shows content

4. **If userId Changes:**
   - Whole process repeats with new userId

## Why Use This Hook
Instead of writing fetch logic in every component,
write it once here and reuse it everywhere.

## Key Concepts
- Custom hooks: Reusable logic across components
- useEffect: Run code when component mounts or dependencies change
- useState: Track loading states and data
- Dependency array [userId]: Re-run when userId changes
```

---

## Common Patterns Explained

### Ternary Operator

```javascript
const message = isLoggedIn ? 'Welcome back!' : 'Please log in';
```

**Explanation:**
```
This is shorthand for if/else:

Long way:
let message;
if (isLoggedIn) {
  message = 'Welcome back!';
} else {
  message = 'Please log in';
}

Short way (ternary):
condition ? valueIfTrue : valueIfFalse

Read it as: "If isLoggedIn is true, use 'Welcome back!',
otherwise use 'Please log in'"
```

---

### Array.map()

```javascript
const numbers = [1, 2, 3];
const doubled = numbers.map(num => num * 2);
// Result: [2, 4, 6]
```

**Explanation:**
```
.map() transforms each item in an array.

Think of it like an assembly line:
- Input: [1, 2, 3]
- For each item, do something (multiply by 2)
- Output: [2, 4, 6]

In React, commonly used to turn data into UI elements:
{users.map(user => <UserCard key={user.id} user={user} />)}

This creates a <UserCard> for each user in the users array.
```

---

### Destructuring

```javascript
const { name, age } = user;
// Same as:
const name = user.name;
const age = user.age;
```

**Explanation:**
```
Destructuring is a shortcut to extract properties from objects.

Instead of:
const name = user.name;
const age = user.age;
const email = user.email;

You can write:
const { name, age, email } = user;

It's like unpacking a box: Instead of reaching into the box
every time (user.name, user.age), you take everything out at once.
```

---

### Optional Chaining (?.)

```javascript
const userName = user?.profile?.name;
```

**Explanation:**
```
The ?. prevents errors when something might not exist.

Without ?.:
const userName = user.profile.name; // CRASH if user is null!

With ?.:
const userName = user?.profile?.name; // undefined if user is null

Read it as: "Get user's profile's name, but if user or profile
doesn't exist, just give me undefined instead of crashing."

Like asking "Does the house have a door with a doorbell?"
- If there's no house → no answer (undefined)
- If there's a house but no door → no answer
- If there's a door with no doorbell → no answer
- If everything exists → answer is the doorbell
```

---

### Async/Await

```javascript
async function getData() {
  const response = await fetch('/api/data');
  const data = await response.json();
  return data;
}
```

**Explanation:**
```
async/await makes asynchronous code look synchronous.

Asynchronous means: "This takes time, don't wait for it"

Without await (old way):
fetch('/api/data')
  .then(response => response.json())
  .then(data => console.log(data));

With await (new way):
const response = await fetch('/api/data');
const data = await response.json();
console.log(data);

"await" means: "Wait here until this finishes, then continue"

Like ordering food:
- Order food (fetch)
- AWAIT: Wait for food to be ready (don't do next steps yet)
- Receive food (response)
- AWAIT: Wait while you eat (json parsing)
- Leave restaurant (return data)
```

---

## Concept Deep-Dives

When explaining complex concepts, provide:

### 1. The Concept
What it is in simple terms

### 2. Why It Exists
What problem it solves

### 3. How It Works
Simplified explanation of the mechanics

### 4. Real-World Analogy
Relate to something familiar

### 5. Code Example
Show it in action

### 6. Common Gotchas
Things beginners often get wrong

### 7. Further Learning
Where to learn more

---

## Learning Highlights

After explaining code, highlight learning opportunities:

```
## 💡 Learning Opportunities

From this code, you can learn about:

1. **[Concept 1]**: [Brief description]
   - Resource: [Link to docs/tutorial]

2. **[Concept 2]**: [Brief description]
   - Resource: [Link to docs/tutorial]

3. **[Concept 3]**: [Brief description]
   - Resource: [Link to docs/tutorial]

These concepts will help you understand similar code in the future.
```

---

## Comparison to Alternatives

When explaining implementation choices:

```
## Why This Approach?

**What we used:** [Technology/pattern]

**Alternatives:**
1. [Option A]: [Why we didn't use it]
2. [Option B]: [Why we didn't use it]

**We chose this because:**
- [Reason 1]
- [Reason 2]
- [Reason 3]
```

**Example:**
```
## Why This Approach?

**What we used:** React useState for form state

**Alternatives:**
1. Uncontrolled inputs (just read on submit): Harder to validate
   in real-time
2. Form library like Formik: Overkill for simple forms
3. Refs: More complex and less React-idiomatic

**We chose useState because:**
- Simple and straightforward
- Built into React
- Easy to add validation
- You can see what's typed in real-time
```

---

## Progressive Explanation

For complex code, explain in layers:

### Layer 1: What (High-Level)
```
This code creates a user authentication system.
```

### Layer 2: How (Medium-Level)
```
It has three parts:
1. Login form where users enter credentials
2. API call to verify credentials with server
3. Storage of authentication token for future requests
```

### Layer 3: Why (Detailed)
```
We use JWT tokens because:
- Server doesn't need to remember sessions
- Tokens can be verified independently
- Can include user info in token (claims)

We store in localStorage because:
- Persists across page refreshes
- Easy to access from any component
- Simple to clear on logout
```

### Layer 4: Implementation Details
```
[Show actual code with inline comments]
```

---

## Visual Explanations

When helpful, use ASCII diagrams:

```
User Flow Diagram:

User → LoginForm → API → Server
  ↑                        ↓
  └──── Token Stored ←─────┘

1. User enters credentials in LoginForm
2. LoginForm sends to API
3. API verifies with Server
4. Server returns token
5. Token stored locally
6. User can now access protected routes
```

---

## Code Comments in Explanations

When showing code, add beginner-friendly comments:

```javascript
// BEFORE: Code without comments
function handleLogin(credentials) {
  const token = await loginAPI(credentials);
  localStorage.setItem('token', token);
  navigate('/dashboard');
}

// AFTER: Code with explanatory comments
function handleLogin(credentials) {
  // Send email/password to server to verify they're correct
  const token = await loginAPI(credentials);

  // Save the authentication token so we can prove we're logged in later
  localStorage.setItem('token', token);

  // Take the user to their dashboard (they're logged in now!)
  navigate('/dashboard');
}
```

---

## Common Questions Answered

### "Why do we need to import X?"
```
Imports bring in code from other files so we can use it here.

Think of it like borrowing tools:
- You don't own a ladder, so you borrow one from a neighbor
- You don't write every function yourself, so you import from libraries

Without import React from 'react':
- React features wouldn't be available
- Code would crash

The import is like saying "Hey, I need React's tools in this file"
```

### "What's the difference between const, let, and var?"
```
const: Can't be reassigned (most common, use by default)
let: Can be reassigned when needed
var: Old way, avoid using

Examples:
const name = 'Josh';    // Can't change later
name = 'Bob';           // ERROR!

let age = 25;           // Can change later
age = 26;               // OK!

Use const by default. Only use let when you know the value will change.
```

### "Why do we use arrow functions?"
```
Arrow functions are shorthand for regular functions.

Regular function:
function add(a, b) {
  return a + b;
}

Arrow function:
const add = (a, b) => a + b;

They're shorter and handle "this" differently (advanced topic).

In React, commonly used for event handlers and array methods:
<button onClick={() => handleClick()}>
{items.map(item => <div>{item.name}</div>)}
```

---

## Success Metrics

Explanation is successful when:
- You understand what the code does at a high level
- You can explain the flow to someone else
- You understand why it's written this way
- You recognize patterns you can reuse
- You know what to learn next
- You feel confident modifying it (with guidance)

---

## Follow-Up Support

After explaining, offer:

```
## Want to Learn More?

Would you like me to:
- Explain any specific part in more detail?
- Show alternative ways to write this?
- Explain the concepts this uses?
- Walk through what happens step-by-step with example data?
- Compare this to how other developers might solve it?
```

---

## Cost-Conscious Explaining

- Explain only the code section requested, not entire files
- Start with high-level, go deeper only if asked
- Use analogies instead of lengthy technical details
- Highlight key concepts, don't explain every line
- Assume basic concepts are understood unless asked
