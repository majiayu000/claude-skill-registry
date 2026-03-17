---
name: fparsec
description: |
  Use when building high-performance text parsers in F# using FParsec parser combinators.
  USE FOR: F# parser combinators, text parsing, expression parsers, DSL implementation in F#, protocol parsing, structured data extraction
  DO NOT USE FOR: C# parser combinators (use pidgin or parakeet), JSON/XML parsing (use System.Text.Json), regex-based text matching
license: MIT
metadata:
  displayName: "FParsec"
  author: "Tyler-R-Kendrick"
  version: "1.0.0"
compatibility: claude, copilot, cursor
references:
  - title: "FParsec Documentation"
    url: "https://www.quanttec.com/fparsec/"
  - title: "FParsec GitHub Repository"
    url: "https://github.com/stephan-tolksdorf/fparsec"
  - title: "FParsec NuGet Package"
    url: "https://www.nuget.org/packages/FParsec"
---

# FParsec

## Overview
FParsec is a parser combinator library for F# inspired by Haskell's Parsec. It provides a rich set of combinators for building complex parsers from simple building blocks. FParsec is designed for high performance with optimized low-level primitives and supports user-state threading for context-sensitive parsing. It excels at parsing structured text formats, DSLs, programming languages, and data protocols.

## NuGet Packages
- `FParsec` -- core parser combinator library for F#

## Basic Parsing
```fsharp
open FParsec

// Parse an integer
let pint : Parser<int, unit> = pint32

// Parse a floating-point number
let pfloat : Parser<float, unit> = pfloat

// Parse a specific string
let pHello : Parser<string, unit> = pstring "hello"

// Running a parser
let result = run pint "42"
match result with
| Success(value, _, _) -> printfn "Parsed: %d" value
| Failure(msg, _, _) -> printfn "Error: %s" msg
```

## Combinators
```fsharp
open FParsec

// Sequence: parse one thing then another
let pPoint : Parser<float * float, unit> =
    pchar '(' >>. pfloat .>> pchar ',' .>>. pfloat .>> pchar ')'

// run pPoint "(3.5,4.2)" => Success((3.5, 4.2))

// Choice: try alternatives
let pBool : Parser<bool, unit> =
    (stringReturn "true" true) <|> (stringReturn "false" false)

// Many: zero or more
let pDigits : Parser<char list, unit> = many digit

// SepBy: items separated by a delimiter
let pCsvInts : Parser<int list, unit> = sepBy pint32 (pchar ',')

// Between: surrounded by delimiters
let pBracketed : Parser<int list, unit> =
    between (pchar '[') (pchar ']') pCsvInts

// run pBracketed "[1,2,3]" => Success([1; 2; 3])
```

## Identifier and Keyword Parsing
```fsharp
open FParsec

let isIdentifierFirstChar c = isLetter c || c = '_'
let isIdentifierChar c = isLetter c || isDigit c || c = '_'

let pIdentifier : Parser<string, unit> =
    many1Satisfy2L isIdentifierFirstChar isIdentifierChar "identifier"

let pKeyword (s: string) : Parser<unit, unit> =
    pstring s >>. notFollowedBy (satisfy isIdentifierChar) >>. spaces

// Keywords with reserved word checking
let keywords = Set.ofList ["let"; "if"; "then"; "else"; "true"; "false"]

let pIdent : Parser<string, unit> =
    pIdentifier >>= fun id ->
        if Set.contains id keywords then
            fail (sprintf "'%s' is a reserved keyword" id)
        else
            preturn id
```

## Expression Parser with Operator Precedence
```fsharp
open FParsec

type Expr =
    | Number of float
    | BinOp of string * Expr * Expr
    | UnaryMinus of Expr
    | Variable of string

let pExpr, pExprRef = createParserForwardedToRef<Expr, unit>()

let pNumber : Parser<Expr, unit> = pfloat |>> Number
let pVariable : Parser<Expr, unit> =
    many1Satisfy2L isLetter isLetterOrDigit "variable" |>> Variable

let pAtom : Parser<Expr, unit> =
    pNumber
    <|> pVariable
    <|> between (pchar '(' >>. spaces) (pchar ')' >>. spaces) pExpr

let opp = new OperatorPrecedenceParser<Expr, unit, unit>()
opp.TermParser <- pAtom .>> spaces

// Binary operators (left-associative)
opp.AddOperator(InfixOperator("+", spaces, 1, Associativity.Left,
    fun x y -> BinOp("+", x, y)))
opp.AddOperator(InfixOperator("-", spaces, 1, Associativity.Left,
    fun x y -> BinOp("-", x, y)))
opp.AddOperator(InfixOperator("*", spaces, 2, Associativity.Left,
    fun x y -> BinOp("*", x, y)))
opp.AddOperator(InfixOperator("/", spaces, 2, Associativity.Left,
    fun x y -> BinOp("/", x, y)))

// Exponentiation (right-associative)
opp.AddOperator(InfixOperator("^", spaces, 3, Associativity.Right,
    fun x y -> BinOp("^", x, y)))

// Unary minus (prefix)
opp.AddOperator(PrefixOperator("-", spaces, 4, true,
    fun x -> UnaryMinus x))

pExprRef.Value <- opp.ExpressionParser

// run opp.ExpressionParser "2 + 3 * 4" => BinOp("+", Number 2, BinOp("*", Number 3, Number 4))
```

## JSON Parser Example
```fsharp
open FParsec

type JsonValue =
    | JsonNull
    | JsonBool of bool
    | JsonNumber of float
    | JsonString of string
    | JsonArray of JsonValue list
    | JsonObject of (string * JsonValue) list

let pJsonValue, pJsonValueRef = createParserForwardedToRef<JsonValue, unit>()

let ws = spaces
let pNull = stringReturn "null" JsonNull .>> ws
let pTrue = stringReturn "true" (JsonBool true) .>> ws
let pFalse = stringReturn "false" (JsonBool false) .>> ws
let pBoolVal = pTrue <|> pFalse

let pJsonNumber = pfloat .>> ws |>> JsonNumber

let pStringLiteral =
    let normalChar = satisfy (fun c -> c <> '\\' && c <> '"')
    let escapedChar =
        pchar '\\' >>. (anyOf "\\\"nrt" |>> function
            | 'n' -> '\n' | 'r' -> '\r' | 't' -> '\t' | c -> c)
    between (pchar '"') (pchar '"')
        (manyChars (normalChar <|> escapedChar)) .>> ws

let pJsonString = pStringLiteral |>> JsonString

let pJsonArray =
    between (pchar '[' >>. ws) (pchar ']' >>. ws)
        (sepBy pJsonValue (pchar ',' >>. ws)) |>> JsonArray

let pKeyValue =
    pStringLiteral .>> pchar ':' .>> ws .>>. pJsonValue

let pJsonObject =
    between (pchar '{' >>. ws) (pchar '}' >>. ws)
        (sepBy pKeyValue (pchar ',' >>. ws)) |>> JsonObject

pJsonValueRef.Value <-
    pNull <|> pBoolVal <|> pJsonNumber <|> pJsonString <|> pJsonArray <|> pJsonObject
```

## User State for Context-Sensitive Parsing
```fsharp
open FParsec

// User state tracks indentation level
type IndentState = { IndentLevel: int }

let pIndented (p: Parser<'a, IndentState>) : Parser<'a, IndentState> =
    getUserState >>= fun state ->
        let expectedIndent = state.IndentLevel * 4
        skipManyMinMaxSatisfy expectedIndent expectedIndent (fun c -> c = ' ')
        >>. p

let pBlock (p: Parser<'a, IndentState>) : Parser<'a list, IndentState> =
    updateUserState (fun s -> { s with IndentLevel = s.IndentLevel + 1 })
    >>. many1 (pIndented p)
    .>> updateUserState (fun s -> { s with IndentLevel = s.IndentLevel - 1 })
```

## Consuming from C#
```csharp
// F# parser library exposed as a C#-friendly API
// In your F# library project:
// module MyParser
// let parseExpression (input: string) : Result<Expr, string> =
//     match run pExpr input with
//     | Success(result, _, _) -> Ok result
//     | Failure(msg, _, _) -> Error msg

// C# consumption:
var result = MyParser.parseExpression("2 + 3 * 4");
result.Match(
    ok: expr => Console.WriteLine($"Parsed: {expr}"),
    error: msg => Console.WriteLine($"Error: {msg}")
);
```

## FParsec vs Other Parsers

| Feature | FParsec | Pidgin (C#) | Regex |
|---------|---------|-------------|-------|
| Language | F# | C# | Any |
| Approach | Parser combinators | Parser combinators | Pattern matching |
| Error messages | Excellent, positional | Good | Poor |
| Expressiveness | Full recursive descent | Full recursive descent | Limited (no recursion) |
| Performance | High (optimized C code) | Good | Varies |
| User state | Built-in threading | Manual | None |
| Best for | Complex grammars in F# | Complex grammars in C# | Simple patterns |

## Best Practices
- Use `createParserForwardedToRef` for recursive grammars (e.g., expressions, JSON) to break circular references between parser definitions.
- Use `OperatorPrecedenceParser` for expression grammars with infix, prefix, and postfix operators rather than manually implementing precedence climbing.
- Add `spaces` or custom whitespace parsers after tokens (`pchar '(' >>. spaces`) to handle whitespace consistently throughout the grammar.
- Use `many1Satisfy2L` with descriptive labels so error messages report what was expected (e.g., "identifier", "digit") instead of raw character expectations.
- Guard keyword parsers with `notFollowedBy` to prevent "if" from matching as a prefix of "iffy"; use `>>. notFollowedBy (satisfy isIdentifierChar)`.
- Use `attempt` sparingly and only when backtracking is genuinely needed; excessive backtracking degrades performance and obscures error messages.
- Thread user state through parsers for context-sensitive features (indentation tracking, symbol tables) rather than using mutable external state.
- Expose F# parser libraries to C# consumers via a simple API returning `Result<T, string>` to hide FParsec's F#-specific types.
- Test parsers with both valid and malformed input to verify error messages are descriptive and point to the correct position in the input.
- Profile parser performance with `runParserOnStream` for large inputs; FParsec's stream-based parsing avoids loading entire files into memory.
