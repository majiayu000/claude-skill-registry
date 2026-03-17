---
name: data-operations-skill
description: Generic CRUD operations for in-memory storage using a list of dictionaries with auto-generated IDs.
functions:
  - name: create
    description: Add a new item to storage and return its auto-generated ID
    parameters:
      type: object
      properties:
        item:
          type: dict
          description: The item to add to storage
      required:
        - item
    returns:
      type: int
      description: The auto-generated ID of the new item

  - name: read
    description: Retrieve an item from storage by its ID
    parameters:
      type: object
      properties:
        id:
          type: int
          description: The ID of the item to retrieve
      required:
        - id
    returns:
      type: dict | None
      description: The item dict if found, None otherwise

  - name: update
    description: Update fields of an existing item in storage
    parameters:
      type: object
      properties:
        id:
          type: int
          description: The ID of the item to update
        data:
          type: dict
          description: The dictionary of fields to update
      required:
        - id
        - data
    returns:
      type: bool
      description: True if item was found and updated, False if not found

  - name: delete
    description: Remove an item from storage by its ID
    parameters:
      type: object
      properties:
        id:
          type: int
          description: The ID of the item to delete
      required:
        - id
    returns:
      type: bool
      description: True if item was found and deleted, False if not found

  - name: list_all
    description: Return all items in storage sorted by ID
    parameters:
      type: object
      properties: {}
    returns:
      type: list[dict]
      description: List of all items, sorted by their ID

  - name: _generate_id
    description: Generate the next auto-incremented ID
    parameters:
      type: object
      properties: {}
    returns:
      type: int
      description: The next available unique ID
---

# Data Operations Skill

## Purpose
Provides generic CRUD (Create, Read, Update, Delete) operations for in-memory storage using a list of dictionaries.

## Storage Structure

Storage is maintained as a list of dictionaries, where each dictionary represents an item and includes an `id` field.

**Example Storage:**
```python
[
    {"id": 1, "name": "Item 1", "value": 100},
    {"id": 2, "name": "Item 2", "value": 200}
]
```

## Methods

### 1. create(item: dict) -> int

Adds a new item to storage with an auto-generated ID.

**Parameters:**
- `item` (dict): The item dictionary to add. Should not include an `id` field (it will be auto-generated).

**Returns:**
- `int`: The auto-generated ID of the newly created item.

**Behavior:**
- Generates a unique ID using `_generate_id()`
- Adds the `id` field to the item
- Appends the item to the storage list
- Returns the new ID

**Example:**
```python
new_id = create({"name": "New Item", "value": 300})
# Returns: 3
```

### 2. read(id: int) -> dict | None

Retrieves an item from storage by its ID.

**Parameters:**
- `id` (int): The ID of the item to retrieve.

**Returns:**
- `dict`: The item dictionary if found.
- `None`: If no item with the given ID exists.

**Example:**
```python
item = read(1)
# Returns: {"id": 1, "name": "Item 1", "value": 100}
```

### 3. update(id: int, data: dict) -> bool

Updates fields of an existing item in storage.

**Parameters:**
- `id` (int): The ID of the item to update.
- `data` (dict): A dictionary containing the fields to update. The `id` field cannot be updated.

**Returns:**
- `True`: If the item was found and updated successfully.
- `False`: If no item with the given ID exists.

**Behavior:**
- Finds the item by ID
- Updates only the fields provided in `data`
- Preserves existing fields not included in `data`
- Does not allow modifying the `id` field

**Example:**
```python
success = update(1, {"value": 150})
# Returns: True
```
 
### 4. delete(id: int) -> bool

Removes an item from storage by its ID.

**Parameters:**
- `id` (int): The ID of the item to delete.

**Returns:**
- `True`: If the item was found and deleted successfully.
- `False`: If no item with the given ID exists.

**Example:**
```python
success = delete(1)
# Returns: True
```

### 5. list_all() -> list[dict]

Returns all items in storage, sorted by their ID.

**Parameters:**
- None

**Returns:**
- `list[dict]`: A list of all items in storage, sorted in ascending order by ID.

**Example:**
```python
items = list_all()
# Returns: [{"id": 1, ...}, {"id": 2, ...}]
```

### 6. _generate_id() -> int

Generates the next auto-incremented unique ID.

**Parameters:**
- None

**Returns:**
- `int`: The next available unique ID.

**Behavior:**
- Maintains an internal counter
- Increments the counter after each generation
- IDs start at 1 and increment by 1

**Example:**
```python
next_id = _generate_id()
# Returns: 4 (if 3 items exist)
```

## Thread-Safety Considerations

**Warning:** This implementation is NOT thread-safe by default.

For multi-threaded environments, add thread synchronization:

```python
from threading import Lock

class ThreadSafeDataOperations:
    def __init__(self):
        self._storage: list[dict] = []
        self._id_counter: int = 0
        self._lock = Lock()

    def create(self, item: dict) -> int:
        with self._lock:
            self._id_counter += 1
            new_id = self._id_counter
            item["id"] = new_id
            self._storage.append(item)
            return new_id

    def read(self, id: int) -> dict | None:
        with self._lock:
            for item in self._storage:
                if item["id"] == id:
                    return item.copy()
            return None

    def update(self, id: int, data: dict) -> bool:
        with self._lock:
            for item in self._storage:
                if item["id"] == id:
                    item.update(data)
                    return True
            return False

    def delete(self, id: int) -> bool:
        with self._lock:
            for i, item in enumerate(self._storage):
                if item["id"] == id:
                    del self._storage[i]
                    return True
            return False

    def list_all(self) -> list[dict]:
        with self._lock:
            return [item.copy() for item in self._storage]
```

## Usage Example

```python
# Create items
id1 = create({"name": "Task 1", "status": "pending"})
id2 = create({"name": "Task 2", "status": "completed"})

# Read item
task = read(id1)

# Update item
update(id1, {"status": "in_progress"})

# List all
all_tasks = list_all()

# Delete item
delete(id2)
```

## Implementation Notes

- All methods include proper type hints
- All methods have docstrings documenting parameters, returns, and behavior
- The `id` field is reserved and auto-generated
- Items are returned as direct references (use `.copy()` for isolation)
- For production use, implement thread-safety as shown above
