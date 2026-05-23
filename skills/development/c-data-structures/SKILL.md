---
name: c-data-structures
description: Use when implementing data structures in C including arrays, linked lists, trees, and hash tables with manual memory management.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
---

# C Data Structures

Master implementing fundamental and advanced data structures in C with
proper memory management, including arrays, linked lists, trees, hash
tables, and more.

## Arrays and Pointers

### Static Arrays

```c
#include <stdio.h>

void print_array(int arr[], size_t size) {
    for (size_t i = 0; i < size; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
}

int main(void) {
    int numbers[5] = {10, 20, 30, 40, 50};

    printf("Array size: %zu bytes\n", sizeof(numbers));
    printf("Element size: %zu bytes\n", sizeof(numbers[0]));
    printf("Number of elements: %zu\n", sizeof(numbers) / sizeof(numbers[0]));

    print_array(numbers, 5);

    // Array indexing is pointer arithmetic
    printf("numbers[2] = %d\n", numbers[2]);
    printf("*(numbers + 2) = %d\n", *(numbers + 2));

    return 0;
}
```

### Dynamic Arrays

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int *data;
    size_t size;
    size_t capacity;
} DynamicArray;

DynamicArray *array_create(size_t initial_capacity) {
    DynamicArray *arr = malloc(sizeof(DynamicArray));
    if (!arr) return NULL;

    arr->data = malloc(initial_capacity * sizeof(int));
    if (!arr->data) {
        free(arr);
        return NULL;
    }

    arr->size = 0;
    arr->capacity = initial_capacity;
    return arr;
}

int array_push(DynamicArray *arr, int value) {
    if (arr->size >= arr->capacity) {
        size_t new_capacity = arr->capacity * 2;
        int *new_data = realloc(arr->data, new_capacity * sizeof(int));
        if (!new_data) return -1;

        arr->data = new_data;
        arr->capacity = new_capacity;
    }

    arr->data[arr->size++] = value;
    return 0;
}

int array_get(DynamicArray *arr, size_t index) {
    if (index >= arr->size) {
        fprintf(stderr, "Index out of bounds\n");
        return -1;
    }
    return arr->data[index];
}

void array_free(DynamicArray *arr) {
    if (arr) {
        free(arr->data);
        free(arr);
    }
}

int main(void) {
    DynamicArray *arr = array_create(2);

    array_push(arr, 10);
    array_push(arr, 20);
    array_push(arr, 30);  // Will trigger resize

    for (size_t i = 0; i < arr->size; i++) {
        printf("%d ", array_get(arr, i));
    }
    printf("\n");

    array_free(arr);
    return 0;
}
```

## Structs and Unions

### Structs

```c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

typedef struct {
    char name[50];
    int age;
    float gpa;
} Student;

typedef struct {
    int x;
    int y;
} Point;

// Struct with flexible array member
typedef struct {
    size_t length;
    char data[];  // Flexible array member
} String;

String *string_create(const char *str) {
    size_t len = strlen(str);
    String *s = malloc(sizeof(String) + len + 1);
    if (!s) return NULL;

    s->length = len;
    strcpy(s->data, str);
    return s;
}

void demonstrate_structs(void) {
    Student s1 = {"Alice", 20, 3.8};
    Student s2;

    // Copy struct
    s2 = s1;
    s2.age = 21;

    printf("s1: %s, age %d\n", s1.name, s1.age);
    printf("s2: %s, age %d\n", s2.name, s2.age);

    // Struct pointer
    Student *sp = &s1;
    printf("Name via pointer: %s\n", sp->name);

    // Flexible array member
    String *str = string_create("Hello, World!");
    printf("String: %s (length: %zu)\n", str->data, str->length);
    free(str);
}
```

### Unions

```c
#include <stdio.h>
#include <stdint.h>

typedef union {
    uint32_t word;
    uint16_t halfwords[2];
    uint8_t bytes[4];
} Word;

typedef enum {
    TYPE_INT,
    TYPE_FLOAT,
    TYPE_STRING
} ValueType;

typedef struct {
    ValueType type;
    union {
        int i;
        float f;
        char *s;
    } value;
} Value;

void print_value(Value *v) {
    switch (v->type) {
        case TYPE_INT:
            printf("int: %d\n", v->value.i);
            break;
        case TYPE_FLOAT:
            printf("float: %f\n", v->value.f);
            break;
        case TYPE_STRING:
            printf("string: %s\n", v->value.s);
            break;
    }
}

int main(void) {
    Word w = {.word = 0x12345678};
    printf("Word: 0x%08x\n", w.word);
    printf("Byte 0: 0x%02x\n", w.bytes[0]);
    printf("Byte 1: 0x%02x\n", w.bytes[1]);

    Value v1 = {TYPE_INT, {.i = 42}};
    Value v2 = {TYPE_FLOAT, {.f = 3.14}};
    Value v3 = {TYPE_STRING, {.s = "Hello"}};

    print_value(&v1);
    print_value(&v2);
    print_value(&v3);

    return 0;
}
```

## Linked Lists

### Singly Linked List

```c
#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int data;
    struct Node *next;
} Node;

typedef struct {
    Node *head;
    size_t size;
} LinkedList;

LinkedList *list_create(void) {
    LinkedList *list = malloc(sizeof(LinkedList));
    if (!list) return NULL;

    list->head = NULL;
    list->size = 0;
    return list;
}

int list_push_front(LinkedList *list, int data) {
    Node *new_node = malloc(sizeof(Node));
    if (!new_node) return -1;

    new_node->data = data;
    new_node->next = list->head;
    list->head = new_node;
    list->size++;

    return 0;
}

int list_push_back(LinkedList *list, int data) {
    Node *new_node = malloc(sizeof(Node));
    if (!new_node) return -1;

    new_node->data = data;
    new_node->next = NULL;

    if (!list->head) {
        list->head = new_node;
    } else {
        Node *current = list->head;
        while (current->next) {
            current = current->next;
        }
        current->next = new_node;
    }

    list->size++;
    return 0;
}

int list_remove(LinkedList *list, int data) {
    if (!list->head) return -1;

    if (list->head->data == data) {
        Node *temp = list->head;
        list->head = list->head->next;
        free(temp);
        list->size--;
        return 0;
    }

    Node *current = list->head;
    while (current->next && current->next->data != data) {
        current = current->next;
    }

    if (current->next) {
        Node *temp = current->next;
        current->next = current->next->next;
        free(temp);
        list->size--;
        return 0;
    }

    return -1;
}

void list_print(LinkedList *list) {
    Node *current = list->head;
    while (current) {
        printf("%d -> ", current->data);
        current = current->next;
    }
    printf("NULL\n");
}

void list_free(LinkedList *list) {
    if (!list) return;

    Node *current = list->head;
    while (current) {
        Node *next = current->next;
        free(current);
        current = next;
    }
    free(list);
}
```

### Doubly Linked List

```c
#include <stdio.h>
#include <stdlib.h>

typedef struct DNode {
    int data;
    struct DNode *prev;
    struct DNode *next;
} DNode;

typedef struct {
    DNode *head;
    DNode *tail;
    size_t size;
} DoublyLinkedList;

DoublyLinkedList *dlist_create(void) {
    DoublyLinkedList *list = malloc(sizeof(DoublyLinkedList));
    if (!list) return NULL;

    list->head = NULL;
    list->tail = NULL;
    list->size = 0;
    return list;
}

int dlist_push_back(DoublyLinkedList *list, int data) {
    DNode *new_node = malloc(sizeof(DNode));
    if (!new_node) return -1;

    new_node->data = data;
    new_node->next = NULL;
    new_node->prev = list->tail;

    if (!list->head) {
        list->head = new_node;
    } else {
        list->tail->next = new_node;
    }

    list->tail = new_node;
    list->size++;
    return 0;
}

int dlist_push_front(DoublyLinkedList *list, int data) {
    DNode *new_node = malloc(sizeof(DNode));
    if (!new_node) return -1;

    new_node->data = data;
    new_node->prev = NULL;
    new_node->next = list->head;

    if (!list->head) {
        list->tail = new_node;
    } else {
        list->head->prev = new_node;
    }

    list->head = new_node;
    list->size++;
    return 0;
}

void dlist_print_forward(DoublyLinkedList *list) {
    DNode *current = list->head;
    while (current) {
        printf("%d <-> ", current->data);
        current = current->next;
    }
    printf("NULL\n");
}

void dlist_print_backward(DoublyLinkedList *list) {
    DNode *current = list->tail;
    while (current) {
        printf("%d <-> ", current->data);
        current = current->prev;
    }
    printf("NULL\n");
}

void dlist_free(DoublyLinkedList *list) {
    if (!list) return;

    DNode *current = list->head;
    while (current) {
        DNode *next = current->next;
        free(current);
        current = next;
    }
    free(list);
}
```

## Stacks and Queues

### Stack (Array-based)

```c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

typedef struct {
    int *data;
    size_t capacity;
    int top;
} Stack;

Stack *stack_create(size_t capacity) {
    Stack *stack = malloc(sizeof(Stack));
    if (!stack) return NULL;

    stack->data = malloc(capacity * sizeof(int));
    if (!stack->data) {
        free(stack);
        return NULL;
    }

    stack->capacity = capacity;
    stack->top = -1;
    return stack;
}

bool stack_is_empty(Stack *stack) {
    return stack->top == -1;
}

bool stack_is_full(Stack *stack) {
    return stack->top == (int)(stack->capacity - 1);
}

int stack_push(Stack *stack, int value) {
    if (stack_is_full(stack)) {
        return -1;
    }

    stack->data[++stack->top] = value;
    return 0;
}

int stack_pop(Stack *stack, int *value) {
    if (stack_is_empty(stack)) {
        return -1;
    }

    *value = stack->data[stack->top--];
    return 0;
}

int stack_peek(Stack *stack, int *value) {
    if (stack_is_empty(stack)) {
        return -1;
    }

    *value = stack->data[stack->top];
    return 0;
}

void stack_free(Stack *stack) {
    if (stack) {
        free(stack->data);
        free(stack);
    }
}
```

### Queue (Circular Buffer)

```c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

typedef struct {
    int *data;
    size_t capacity;
    size_t front;
    size_t rear;
    size_t size;
} Queue;

Queue *queue_create(size_t capacity) {
    Queue *queue = malloc(sizeof(Queue));
    if (!queue) return NULL;

    queue->data = malloc(capacity * sizeof(int));
    if (!queue->data) {
        free(queue);
        return NULL;
    }

    queue->capacity = capacity;
    queue->front = 0;
    queue->rear = 0;
    queue->size = 0;
    return queue;
}

bool queue_is_empty(Queue *queue) {
    return queue->size == 0;
}

bool queue_is_full(Queue *queue) {
    return queue->size == queue->capacity;
}

int queue_enqueue(Queue *queue, int value) {
    if (queue_is_full(queue)) {
        return -1;
    }

    queue->data[queue->rear] = value;
    queue->rear = (queue->rear + 1) % queue->capacity;
    queue->size++;
    return 0;
}

int queue_dequeue(Queue *queue, int *value) {
    if (queue_is_empty(queue)) {
        return -1;
    }

    *value = queue->data[queue->front];
    queue->front = (queue->front + 1) % queue->capacity;
    queue->size--;
    return 0;
}

void queue_free(Queue *queue) {
    if (queue) {
        free(queue->data);
        free(queue);
    }
}
```

## Binary Trees

### Binary Search Tree

```c
#include <stdio.h>
#include <stdlib.h>

typedef struct TreeNode {
    int data;
    struct TreeNode *left;
    struct TreeNode *right;
} TreeNode;

typedef struct {
    TreeNode *root;
    size_t size;
} BST;

BST *bst_create(void) {
    BST *tree = malloc(sizeof(BST));
    if (!tree) return NULL;

    tree->root = NULL;
    tree->size = 0;
    return tree;
}

TreeNode *create_node(int data) {
    TreeNode *node = malloc(sizeof(TreeNode));
    if (!node) return NULL;

    node->data = data;
    node->left = NULL;
    node->right = NULL;
    return node;
}

TreeNode *bst_insert_helper(TreeNode *node, int data) {
    if (!node) {
        return create_node(data);
    }

    if (data < node->data) {
        node->left = bst_insert_helper(node->left, data);
    } else if (data > node->data) {
        node->right = bst_insert_helper(node->right, data);
    }

    return node;
}

int bst_insert(BST *tree, int data) {
    tree->root = bst_insert_helper(tree->root, data);
    if (tree->root) {
        tree->size++;
        return 0;
    }
    return -1;
}

TreeNode *bst_search_helper(TreeNode *node, int data) {
    if (!node || node->data == data) {
        return node;
    }

    if (data < node->data) {
        return bst_search_helper(node->left, data);
    }
    return bst_search_helper(node->right, data);
}

bool bst_search(BST *tree, int data) {
    return bst_search_helper(tree->root, data) != NULL;
}

TreeNode *find_min(TreeNode *node) {
    while (node->left) {
        node = node->left;
    }
    return node;
}

TreeNode *bst_delete_helper(TreeNode *node, int data) {
    if (!node) return NULL;

    if (data < node->data) {
        node->left = bst_delete_helper(node->left, data);
    } else if (data > node->data) {
        node->right = bst_delete_helper(node->right, data);
    } else {
        // Node to delete found
        if (!node->left) {
            TreeNode *temp = node->right;
            free(node);
            return temp;
        } else if (!node->right) {
            TreeNode *temp = node->left;
            free(node);
            return temp;
        }

        // Node has two children
        TreeNode *temp = find_min(node->right);
        node->data = temp->data;
        node->right = bst_delete_helper(node->right, temp->data);
    }

    return node;
}

void inorder_traversal(TreeNode *node) {
    if (node) {
        inorder_traversal(node->left);
        printf("%d ", node->data);
        inorder_traversal(node->right);
    }
}

void preorder_traversal(TreeNode *node) {
    if (node) {
        printf("%d ", node->data);
        preorder_traversal(node->left);
        preorder_traversal(node->right);
    }
}

void postorder_traversal(TreeNode *node) {
    if (node) {
        postorder_traversal(node->left);
        postorder_traversal(node->right);
        printf("%d ", node->data);
    }
}

void bst_free_helper(TreeNode *node) {
    if (node) {
        bst_free_helper(node->left);
        bst_free_helper(node->right);
        free(node);
    }
}

void bst_free(BST *tree) {
    if (tree) {
        bst_free_helper(tree->root);
        free(tree);
    }
}
```

## Hash Tables

### Simple Hash Table

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

typedef struct HashNode {
    char *key;
    int value;
    struct HashNode *next;
} HashNode;

typedef struct {
    HashNode **buckets;
    size_t capacity;
    size_t size;
} HashTable;

unsigned long hash(const char *str, size_t capacity) {
    unsigned long hash = 5381;
    int c;

    while ((c = *str++)) {
        hash = ((hash << 5) + hash) + c;
    }

    return hash % capacity;
}

HashTable *hashtable_create(size_t capacity) {
    HashTable *table = malloc(sizeof(HashTable));
    if (!table) return NULL;

    table->buckets = calloc(capacity, sizeof(HashNode *));
    if (!table->buckets) {
        free(table);
        return NULL;
    }

    table->capacity = capacity;
    table->size = 0;
    return table;
}

int hashtable_insert(HashTable *table, const char *key, int value) {
    unsigned long index = hash(key, table->capacity);

    // Check if key exists
    HashNode *current = table->buckets[index];
    while (current) {
        if (strcmp(current->key, key) == 0) {
            current->value = value;
            return 0;
        }
        current = current->next;
    }

    // Create new node
    HashNode *new_node = malloc(sizeof(HashNode));
    if (!new_node) return -1;

    new_node->key = strdup(key);
    if (!new_node->key) {
        free(new_node);
        return -1;
    }

    new_node->value = value;
    new_node->next = table->buckets[index];
    table->buckets[index] = new_node;
    table->size++;

    return 0;
}

bool hashtable_get(HashTable *table, const char *key, int *value) {
    unsigned long index = hash(key, table->capacity);

    HashNode *current = table->buckets[index];
    while (current) {
        if (strcmp(current->key, key) == 0) {
            *value = current->value;
            return true;
        }
        current = current->next;
    }

    return false;
}

bool hashtable_remove(HashTable *table, const char *key) {
    unsigned long index = hash(key, table->capacity);

    HashNode *current = table->buckets[index];
    HashNode *prev = NULL;

    while (current) {
        if (strcmp(current->key, key) == 0) {
            if (prev) {
                prev->next = current->next;
            } else {
                table->buckets[index] = current->next;
            }

            free(current->key);
            free(current);
            table->size--;
            return true;
        }

        prev = current;
        current = current->next;
    }

    return false;
}

void hashtable_free(HashTable *table) {
    if (!table) return;

    for (size_t i = 0; i < table->capacity; i++) {
        HashNode *current = table->buckets[i];
        while (current) {
            HashNode *next = current->next;
            free(current->key);
            free(current);
            current = next;
        }
    }

    free(table->buckets);
    free(table);
}
```

## Memory Management

### Custom Allocator

```c
#include <stdio.h>
#include <stdlib.h>
#include <stddef.h>
#include <stdbool.h>

typedef struct Block {
    size_t size;
    bool is_free;
    struct Block *next;
} Block;

typedef struct {
    void *memory;
    size_t total_size;
    Block *free_list;
} Allocator;

Allocator *allocator_create(size_t size) {
    Allocator *alloc = malloc(sizeof(Allocator));
    if (!alloc) return NULL;

    alloc->memory = malloc(size);
    if (!alloc->memory) {
        free(alloc);
        return NULL;
    }

    alloc->total_size = size;

    // Initialize free list with one large block
    alloc->free_list = (Block *)alloc->memory;
    alloc->free_list->size = size - sizeof(Block);
    alloc->free_list->is_free = true;
    alloc->free_list->next = NULL;

    return alloc;
}

void *allocator_alloc(Allocator *alloc, size_t size) {
    Block *current = alloc->free_list;
    Block *prev = NULL;

    // Find first fit
    while (current) {
        if (current->is_free && current->size >= size) {
            // Split block if there's enough space
            if (current->size >= size + sizeof(Block) + 1) {
                Block *new_block = (Block *)((char *)current + sizeof(Block) + size);
                new_block->size = current->size - size - sizeof(Block);
                new_block->is_free = true;
                new_block->next = current->next;

                current->size = size;
                current->next = new_block;
            }

            current->is_free = false;
            return (char *)current + sizeof(Block);
        }

        prev = current;
        current = current->next;
    }

    return NULL;
}

void allocator_free(Allocator *alloc, void *ptr) {
    if (!ptr) return;

    Block *block = (Block *)((char *)ptr - sizeof(Block));
    block->is_free = true;

    // Coalesce with next block if free
    if (block->next && block->next->is_free) {
        block->size += sizeof(Block) + block->next->size;
        block->next = block->next->next;
    }

    // Coalesce with previous block if free
    Block *current = alloc->free_list;
    while (current && current->next != block) {
        current = current->next;
    }

    if (current && current->is_free) {
        current->size += sizeof(Block) + block->size;
        current->next = block->next;
    }
}

void allocator_destroy(Allocator *alloc) {
    if (alloc) {
        free(alloc->memory);
        free(alloc);
    }
}
```

## Best Practices

1. **Always Initialize Pointers**: Initialize pointers to NULL to avoid
   accessing uninitialized memory. Check for NULL before dereferencing.

2. **Free All Allocated Memory**: Every malloc/calloc/realloc must have a
   corresponding free. Track allocations carefully to prevent memory leaks.

3. **Check Allocation Success**: Always check if malloc/calloc/realloc
   returns NULL before using the allocated memory.

4. **Avoid Dangling Pointers**: Set pointers to NULL after freeing them.
   Never use a pointer after the memory it points to has been freed.

5. **Use Size Parameters**: Pass size parameters to functions instead of
   hardcoding array sizes for better reusability and safety.

6. **Implement Consistent Cleanup**: Provide free/destroy functions for all
   data structures that perform complete cleanup in reverse order of
   allocation.

7. **Validate Input Parameters**: Check for NULL pointers and invalid
   indices before performing operations on data structures.

8. **Use typedef for Clarity**: Use typedef for structs to improve code
   readability and reduce verbosity.

9. **Consider Cache Locality**: Arrange struct members and access patterns
   to maximize CPU cache efficiency, especially for performance-critical
   code.

10. **Document Ownership**: Clearly document which functions own allocated
    memory and which are responsible for freeing it.

## Common Pitfalls

1. **Memory Leaks**: Forgetting to free allocated memory or losing the last
   reference to allocated memory causes memory leaks.

2. **Buffer Overflows**: Writing beyond allocated array bounds corrupts
   memory and causes undefined behavior or security vulnerabilities.

3. **Use After Free**: Accessing memory after it has been freed causes
   undefined behavior and potential crashes.

4. **Double Free**: Freeing the same memory twice corrupts the heap and
   causes crashes. Always set pointers to NULL after freeing.

5. **Uninitialized Pointers**: Using pointers before initialization leads
   to accessing random memory addresses.

6. **Shallow Copy Issues**: Copying structs with pointers creates multiple
   references to the same memory, leading to double frees or unintended
   modifications.

7. **Off-by-One Errors**: Incorrect loop bounds or array indexing causes
   buffer overflows or missed elements.

8. **Integer Overflow**: Not checking for overflow when calculating sizes
   for allocation can lead to undersized allocations.

9. **Mixing sizeof Operand Types**: Using sizeof with pointer instead of
   pointed-to type (sizeof(ptr) vs sizeof(*ptr)) allocates wrong size.

10. **Inefficient Reallocation**: Reallocating for every element instead of
    doubling capacity leads to poor performance (O(n²) instead of amortized
    O(1)).

## When to Use This Skill

Use C data structures when you need to:

- Implement custom data structures for specific performance requirements
- Work on embedded systems with constrained memory
- Build system-level software requiring fine-grained memory control
- Create high-performance applications where memory layout matters
- Develop kernel modules or device drivers
- Understand low-level memory management for learning purposes
- Port algorithms from textbooks to production code
- Build foundational libraries and frameworks
- Optimize memory usage in resource-constrained environments
- Implement custom allocators or memory pools

This skill is essential for systems programmers, embedded developers,
performance engineers, and anyone working with C in resource-constrained or
performance-critical environments.

## Resources

### Books

- The C Programming Language by Kernighan and Ritchie
- Data Structures Using C by Reema Thareja
- Algorithms in C by Robert Sedgewick
- Understanding and Using C Pointers by Richard Reese

### Online Resources

- GeeksforGeeks C Data Structures: <https://www.geeksforgeeks.org/data-structures/>
- Learn-C.org: <https://www.learn-c.org/>
- C Data Structures Tutorial: <https://www.tutorialspoint.com/data_structures_algorithms/index.htm>
- Visualgo: <https://visualgo.net/> (Algorithm visualizations)

### Tools

- Valgrind: Memory error detection and profiling
- AddressSanitizer: Fast memory error detector
- GDB: GNU debugger with memory inspection
- cppcheck: Static analysis tool for C/C++
- Electric Fence: Library for detecting memory allocation errors
