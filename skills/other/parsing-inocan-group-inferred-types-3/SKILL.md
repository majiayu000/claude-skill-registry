---
name: Parsing and Mutating Strings
description: Utilities in this library which provide effective ways to parse or mutate text at both runtime and design-time while ensuring that the resulting type is as narrow as possible.
---
# Parsing and Mutating Strings

## Instructions

1. Identify which of the two best describe your needs:

    1. `Simple`
        - finding a **sub-string** inside a string variable
        - **stripping** or **retaining** content UNTIL a certain delimiter is found
        - **ensuring** that the string starts or ends with a certain sub-string
    2. `Structured`
        - you need to parse a string for language features
        - different parts of the string will have different parsing rules based on the characters which preceded it.

2. If your need fits the `Simple` description then ...

    You will likely want to use one of the following type or runtime utilities found in this repo. Every utility's source will have a description above the symbol and many also may include a simple example.

    ### Type Utilities

    > you can import all of these utilities from `inferred-types/types`

    - Trim whitespace
        - `Trim<T>` [ [source](), [examples]() ]
        - `TrimStart<T>` [ [source](), [examples]() ]
        - and `TrimEnd<T>` [ [source](), [examples]() ]
    - Strip a subsection of content
        - `StripAfter<TStr,TBreak>` [ [source](), [examples]() ] - strip `TStrip` after first instance of `TBreak`
        - `StripAfterLast<TStr,TBreak>` [ [source](), [examples]() ] - strip `TStrip` after last instance of `TBreak`
        - `StripBefore<TStr,TBreak>` [ [source](), [examples]() ] - strip `TStr` _before_ the substring `TBreak` is found; retain the rest
        - `StripFirst<T,U>` [ [source](), [examples]() ]
        - `StripLeading<T,U>` [ [source](), [examples]() ]
        - `StripSurround<T,U>` [ [source](), [examples]() ]
        - `StripTrailing<T,U>` [ [source](), [examples]() ]
        - `StripUntil<T,U>` [ [source](), [examples]() ]
    - Retain a subsection of content (the inverse of "strip")
      - `RetainAfter<T,U>` [ [source](), [examples]() ]
      - `RetainAfterLast<T,U>` [ [source](), [examples]() ]
      - `RetainBetween<T,U>` [ [source](), [examples]() ]
      - `RetainUntil<T,U>` [ [source](), [examples]() ]
      - `RetainWhile<T,U>` [ [source](), [examples]() ]
    - String Interpolation (aka, injecting content into sections of a corpus of text)
        - TODO




3. If your need fits the `Structured` need then ...


---

**Notes:**

- there is often (but not always) a 1:1 relationship between a type utility and a runtime function.
    - The runtime function (often but not always) will leverage the corresponding type utility to produce narrow types.
- many _example links_ are to test files; these test files use both runtime and type tests. For more about type tests you can read [type testing](../../docs/type-testing.md) document.
