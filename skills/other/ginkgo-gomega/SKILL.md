---
name: ginkgo-gomega
description: Ginkgo v2 BDD testing framework and Gomega assertions (Go)
category: Testing-BDD
---

# Skill: ginkgo-gomega

## What I do

I teach Ginkgo v2 BDD testing framework for Go, using descriptive test suites with human-readable assertions via Gomega. This makes tests readable as specifications while maintaining rigorous test coverage.

## When to use me

- Writing BDD tests in Go
- Converting table-driven tests to Ginkgo format
- Building test suites with nested Describe/Context blocks
- Writing expressive assertions with Gomega matchers
- Implementing hierarchical test organisation

## Core principles

1. **Tests are specifications** - Test names describe behaviour, not implementation
2. **Describe/Context nesting** - Organise tests by context, not flat
3. **Expressive matchers** - Assertions read like English, not assertions
4. **BeforeEach/AfterEach** - Setup/teardown grouped with tests
5. **Table-driven as last resort** - Ginkgo specs usually clearer

## Patterns & examples

**Ginkgo test structure:**
```go
Describe("User authentication", func() {
  var user *User
  
  BeforeEach(func() {
    user = NewUser("test@example.com")
  })
  
  Context("valid credentials", func() {
    It("authenticates successfully", func() {
      err := user.Authenticate("password123")
      Expect(err).NotTo(HaveOccurred())
      Expect(user.IsAuthenticated).To(BeTrue())
    })
  })
  
  Context("invalid credentials", func() {
    It("returns authentication error", func() {
      err := user.Authenticate("wrongpass")
      Expect(err).To(HaveOccurred())
      Expect(user.IsAuthenticated).To(BeFalse())
    })
  })
})
```

**Gomega matchers (expressive):**
```go
// ✅ Correct: readable matcher chains
Expect(users).To(HaveLen(3))
Expect(name).To(Equal("Alice"))
Expect(age).To(BeNumerically(">", 18))
Expect(tags).To(ContainElement("featured"))
Expect(response).To(HaveKeyWithValue("status", "success"))

// ❌ Wrong: non-matcher assertions
if len(users) != 3 { t.Fail() }
if name != "Alice" { t.Fail() }
```

**Async testing pattern:**
```go
It("processes message eventually", func(done Done) {
  result := make(chan string)
  go ProcessAsync(result)
  
  // Gomega Eventually waits for condition
  Eventually(result).Should(Receive(Equal("done")))
  close(done)
}, 2.0)  // 2 second timeout
```

## Anti-patterns to avoid

- ❌ Flat test list (use Describe/Context nesting)
- ❌ Multiple assertions in one It (focus on one behaviour)
- ❌ Magic values in tests (use meaningful variable names)
- ❌ Table-driven when Ginkgo specs would be clearer
- ❌ Ignoring helper functions (extract test setup)

## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/Testing-BDD/Ginkgo Gomega.md`

## Related skills

- `bdd-workflow` - Red-Green-Refactor cycle that Ginkgo enables
- `golang` - Core Go language idioms
- `test-fixtures-go` - Generate realistic test data for Ginkgo specs
- `gomock` - Mocking in Ginkgo tests
- `clean-code` - Apply SOLID principles to test code
