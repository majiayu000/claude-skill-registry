---
name: torvalds-kernel-pragmatism
description: Write systems code in the style of Linus Torvalds, creator of Linux and Git. Emphasizes pragmatic excellence, performance awareness, subsystem design, and uncompromising code review. Use when writing kernel-level code or high-performance systems.
---

# Linus Torvalds Style Guide

## Overview

Linus Torvalds created the Linux kernel and Git, managing one of the largest collaborative software projects in history. His approach combines deep technical excellence with pragmatic decision-making and famously direct code review.

## Core Philosophy

> "Talk is cheap. Show me the code."

> "Bad programmers worry about the code. Good programmers worry about data structures and their relationships."

> "Given enough eyeballs, all bugs are shallow."

Torvalds believes in practical excellence: code that works, performs well, and can be maintained by a distributed team of thousands.

## Design Principles

1. **Data Structures First**: Get the data structures right; the code follows.

2. **Performance Matters**: Understand cache, branches, and memory.

3. **Pragmatism Over Purity**: Working code beats elegant theory.

4. **Code Review Is Essential**: Every patch must withstand scrutiny.

## When Writing Code

### Always

- Design data structures before algorithms
- Think about cache locality
- Profile before optimizing
- Write clear commit messages
- Keep patches small and focused
- Test on real hardware

### Never

- Submit untested code
- Ignore performance implications
- Use abstractions that hide costs
- Write clever code that obscures intent
- Break userspace API/ABI
- Ignore reviewer feedback

### Prefer

- Arrays over linked lists (cache friendly)
- Simple loops over recursion
- Inline functions over macros
- Explicit state over hidden magic
- Measured optimizations over speculative

## Code Patterns

### Linux Kernel Style

```c
// kernel style: tabs, 80 columns, spaces around operators

#include <linux/kernel.h>
#include <linux/slab.h>

struct device_data {
        struct list_head list;
        unsigned long flags;
        void __iomem *base;
        int irq;
};

static int device_init(struct device_data *dev)
{
        int ret;

        dev->base = ioremap(DEVICE_BASE, DEVICE_SIZE);
        if (!dev->base) {
                pr_err("Failed to map device memory\n");
                return -ENOMEM;
        }

        ret = request_irq(dev->irq, device_handler, 0, "mydev", dev);
        if (ret) {
                iounmap(dev->base);
                return ret;
        }

        return 0;
}
```

### Data Structures Matter

```c
// BAD: Linked list for frequently traversed data
struct node {
    struct node *next;
    int value;
};

// Traversal: terrible cache behavior
// Each node is a cache miss

// GOOD: Array-based for cache locality
struct array {
    int *values;
    size_t count;
    size_t capacity;
};

// Traversal: sequential memory access
// Prefetcher works, cache is happy


// When you need linked lists, use the kernel's
#include <linux/list.h>

struct my_item {
    struct list_head list;  // Embed the list node
    int data;
};

struct list_head my_list;
INIT_LIST_HEAD(&my_list);

// Iterate safely
struct my_item *item;
list_for_each_entry(item, &my_list, list) {
    process(item->data);
}
```

### Error Handling Patterns

```c
// Single exit point with goto for cleanup
int complex_init(struct device *dev)
{
        int ret;

        dev->buffer = kmalloc(BUF_SIZE, GFP_KERNEL);
        if (!dev->buffer) {
                ret = -ENOMEM;
                goto err_buffer;
        }

        dev->workqueue = create_workqueue("mydev");
        if (!dev->workqueue) {
                ret = -ENOMEM;
                goto err_workqueue;
        }

        ret = register_device(dev);
        if (ret)
                goto err_register;

        return 0;

err_register:
        destroy_workqueue(dev->workqueue);
err_workqueue:
        kfree(dev->buffer);
err_buffer:
        return ret;
}

// Cleanup in reverse order of initialization
// One error path, easy to audit
```

### Commit Message Excellence

```
subsystem: short summary (50 chars or less)

More detailed explanatory text, if necessary. Wrap it to about 72
characters. The blank line separating the summary from the body is
critical.

Explain the problem that this commit is solving. Focus on why you
are making this change as opposed to how. The code shows the how.

If there are any side effects or other unintuitive consequences of
this change, explain them here.

Fixes: abc123def456 ("commit that introduced bug")
Reported-by: Someone <someone@example.com>
Signed-off-by: Your Name <you@example.com>
```

### Performance-Conscious Code

```c
// Branch prediction: common case first
if (likely(fast_path_condition)) {
    // Common case
    return quick_result;
}
// Slow path
return handle_slow_case();


// Cache-friendly iteration
// BAD: strided access
for (int i = 0; i < rows; i++)
    for (int j = 0; j < cols; j++)
        process(matrix[j][i]);  // Column-major = cache misses

// GOOD: sequential access
for (int i = 0; i < rows; i++)
    for (int j = 0; j < cols; j++)
        process(matrix[i][j]);  // Row-major = cache friendly


// Avoid unnecessary memory barriers
// Use READ_ONCE/WRITE_ONCE for shared data
int value = READ_ONCE(shared_variable);
WRITE_ONCE(shared_variable, new_value);
```

### Git Usage

```bash
# Torvalds Git workflow

# Commit often, commit small
git add -p                    # Stage hunks, not files
git commit -m "subsystem: specific change"

# Rebase for clean history (before sharing)
git rebase -i HEAD~5          # Clean up local commits

# Never rebase published history
# History is sacred once pushed

# Bisect to find bugs
git bisect start
git bisect bad HEAD
git bisect good v5.10
# Git finds the breaking commit

# Blame to understand code
git blame -w -C -C file.c     # Ignore whitespace, track moves
```

### Subsystem Design

```c
// Define clear boundaries between subsystems
// Each subsystem has:
// 1. Public API (exported symbols)
// 2. Internal implementation
// 3. Data structures

// Public API
int subsystem_init(void);
void subsystem_cleanup(void);
int subsystem_do_thing(struct thing *t);

// Internal - not exported
static int internal_helper(void);
static struct cache internal_cache;

// Use proper namespacing
// subsystem_verb_noun()

int netdev_register_device(struct net_device *dev);
int netdev_unregister_device(struct net_device *dev);
int blkdev_read_sector(struct block_device *bdev, sector_t sector);
```

### Reference Counting

```c
#include <linux/kref.h>

struct my_object {
    struct kref refcount;
    // ... other fields
};

static void my_object_release(struct kref *kref)
{
    struct my_object *obj = container_of(kref, struct my_object, refcount);
    kfree(obj);
}

// Get reference
struct my_object *my_object_get(struct my_object *obj)
{
    if (obj)
        kref_get(&obj->refcount);
    return obj;
}

// Release reference
void my_object_put(struct my_object *obj)
{
    if (obj)
        kref_put(&obj->refcount, my_object_release);
}
```

## Mental Model

Torvalds approaches systems code by asking:

1. **What are the data structures?** Design these first
2. **What's the cache behavior?** Memory access patterns matter
3. **What's the common case?** Optimize for it
4. **Can I review this easily?** Clear code, small patches
5. **What breaks if this is wrong?** Systems code must be reliable

## Signature Torvalds Moves

- Data structures before algorithms
- goto for cleanup (in kernel code)
- likely/unlikely for branch hints
- Cache-conscious data layout
- Small, focused commits
- Direct, honest code review
