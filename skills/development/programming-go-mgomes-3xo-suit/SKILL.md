---
name: programming-go
description: Best practices when developing in Go codebases
---

# Programming Go

## Instructions

- Don't use `interface{}` -- use `any` instead

- Use the "-" tag when Marshalling JSON will cause the field to be omitted. Use this when we have private data on a field that’s meant to be excluded from an API response.

- Use the Go 1.22 syntax for `for` loops:

Write this:

```go
for i := range 10 {
    fmt.Println(i+1)
}
```

NOT THIS:

```go
for i := 1; i <= 10; i++ {
    fmt.Println(i)
}
```

- Use the Go 1.25 `waitgroup.Go` function that lets you add Go routines to a waitgroup more easily. It takes the place of using the go keyword, it looks like this:

```go
wg.Go(func() {
    // your goroutine code here
})
```

```go
The implementation is just a wrapper around this:
func (wg *WaitGroup) Go(f func()) {
    wg.Add(1)
    go func() {
        defer wg.Done()
        f()
    }()
}
```

### Renaming Packages

You can use Go’s LSP to rename packages, not just regular variables. The newly named package will be updated in all references. As a bonus, it even renames the directory!

### Package names

Good package names are short and clear. They are lower case, with no under_scores or mixedCaps. They are often simple nouns, such as:

- time (provides functionality for measuring and displaying time)
- list (implements a doubly linked list)
- http (provides HTTP client and server implementations)

The style of names typical of another language might not be idiomatic in a Go program. Here are two examples of names that might be good style in other languages but do not fit well in Go:

- computeServiceClient
- priority_queue

_Abbreviate judiciously_. Package names may be abbreviated when the abbreviation is familiar to the programmer. Widely-used packages often have compressed names:

- strconv (string conversion)
- syscall (system call)
- fmt (formatted I/O)

On the other hand, if abbreviating a package name makes it ambiguous or unclear, don’t do it.

Similarly, the function to make new instances of ring.Ring — which is the definition of a constructor in Go—would normally be called NewRing, but since Ring is the only type exported by the package, and since the package is called ring, it's called just New, which clients of the package see as ring.New. Use the package structure to help you choose good names.

Another short example is once.Do; once.Do(setup) reads well and would not be improved by writing once.DoOrWaitUntilDone(setup). Long names don't automatically make things more readable. A helpful doc comment can often be more valuable than an extra long name.

_Don’t steal good names from the user_. Avoid giving a package a name that is commonly used in client code. For example, the buffered I/O package is called bufio, not buf, since buf is a good variable name for a buffer.
