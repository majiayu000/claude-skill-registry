---
name: Haskell Ecosystem
description: This skill should be used when working with Haskell projects, "cabal.project", "stack.yaml", "ghc", "cabal build/test/run", "stack build/test/run", or Haskell language patterns. Provides comprehensive Haskell ecosystem patterns and best practices.
version: 0.1.0
---

<purpose>
  Provide comprehensive patterns for Haskell language, GHC toolchain, Cabal/Stack build systems, and type-level programming.
</purpose>

<tools>
  <tool>Read - Analyze cabal files, stack.yaml, and Haskell source files</tool>
  <tool>Edit - Modify Haskell code and build configuration</tool>
  <tool>Bash - Run cabal build, stack build, ghci commands</tool>
  <tool>mcp__context7__get-library-docs - Fetch latest Haskell documentation</tool>
</tools>

<concepts>
  <concept name="purity">Functions have no side effects; same input always produces same output</concept>
  <concept name="laziness">Expressions evaluated only when needed; enables infinite data structures</concept>
  <concept name="type_inference">Hindley-Milner type system; explicit signatures recommended for top-level definitions</concept>
  <concept name="monads">Compose computations with effects; IO, Maybe, Either, State, Reader, Writer</concept>
  <concept name="type_classes">Ad-hoc polymorphism; define operations for types (Eq, Ord, Show, Functor, Applicative, Monad)</concept>
</concepts>

<haskell_language>
  <type_system>
    <concept name="algebraic_data_types">
      <description>Sum types (Either, Maybe) and product types (tuples, records)</description>
      <example>
        data Maybe a = Nothing | Just a
        data Either a b = Left a | Right b
        data Person = Person { name :: String, age :: Int }
      </example>
    </concept>

    <concept name="type_classes">
      <description>Define behavior for types; similar to interfaces but more powerful</description>
      <common_classes>
        <class name="Eq">Equality comparison (==, /=)</class>
        <class name="Ord">Ordering comparison (compare, &lt;, &gt;, &lt;=, &gt;=)</class>
        <class name="Show">String representation (show)</class>
        <class name="Read">Parse from string (read)</class>
        <class name="Functor">Mappable containers (fmap, &lt;$&gt;)</class>
        <class name="Applicative">Apply functions in context (&lt;*&gt;, pure)</class>
        <class name="Monad">Sequence computations (&gt;&gt;=, return, do-notation)</class>
        <class name="Foldable">Reducible structures (foldr, foldl, toList)</class>
        <class name="Traversable">Traverse with effects (traverse, sequenceA)</class>
        <class name="Semigroup">Associative binary operation (&lt;&gt;)</class>
        <class name="Monoid">Semigroup with identity (mempty, mappend)</class>
      </common_classes>
      <example>
        class Eq a where
          (==) :: a -> a -> Bool
          (/=) :: a -> a -> Bool

        instance Eq Person where
          p1 == p2 = name p1 == name p2 && age p1 == age p2
      </example>
    </concept>

    <concept name="type_level_programming">
      <description>Advanced type system features for compile-time guarantees</description>

      <pattern name="gadts">
        <description>Generalized Algebraic Data Types - refine types in pattern matching</description>
        <pragma>GADTs</pragma>
        <example>
          {-# LANGUAGE GADTs #-}
          data Expr a where
            LitInt  :: Int -> Expr Int
            LitBool :: Bool -> Expr Bool
            Add     :: Expr Int -> Expr Int -> Expr Int
            If      :: Expr Bool -> Expr a -> Expr a -> Expr a

          eval :: Expr a -> a
          eval (LitInt n)    = n
          eval (LitBool b)   = b
          eval (Add e1 e2)   = eval e1 + eval e2
          eval (If c t e)    = if eval c then eval t else eval e
        </example>
      </pattern>

      <pattern name="type_families">
        <description>Type-level functions; compute types from types</description>
        <pragma>TypeFamilies</pragma>
        <example>
          {-# LANGUAGE TypeFamilies #-}
          type family Element c where
            Element [a]       = a
            Element (Set a)   = a
            Element Text      = Char

          class Container c where
            type Elem c
            empty :: c
            insert :: Elem c -> c -> c
        </example>
      </pattern>

      <pattern name="data_kinds">
        <description>Promote data types to kinds for type-level programming</description>
        <pragma>DataKinds</pragma>
        <example>
          {-# LANGUAGE DataKinds, KindSignatures #-}
          data Nat = Zero | Succ Nat

          data Vec (n :: Nat) a where
            VNil  :: Vec 'Zero a
            VCons :: a -> Vec n a -> Vec ('Succ n) a
        </example>
      </pattern>

      <pattern name="phantom_types">
        <description>Type parameters that don't appear in value constructors</description>
        <example>
          newtype Tagged tag a = Tagged { unTagged :: a }

          data Validated
          data Unvalidated

          validateEmail :: Tagged Unvalidated String -> Maybe (Tagged Validated String)
        </example>
      </pattern>
    </concept>

    <concept name="higher_kinded_types">
      <description>Type constructors as parameters; enables Functor, Monad abstractions</description>
      <example>
        class Functor f where
          fmap :: (a -> b) -> f a -> f b

        -- f is a type constructor (* -> *)
        -- Functor operates on type constructors, not concrete types
      </example>
    </concept>
  </type_system>

  <monad_transformers>
    <description>Compose monadic effects using transformers from mtl/transformers</description>

    <pattern name="transformers_stack">
      <description>Build custom monad stacks with transformers</description>
      <example>
        import Control.Monad.Trans.Reader
        import Control.Monad.Trans.State
        import Control.Monad.Trans.Except

        type App a = ReaderT Config (StateT AppState (ExceptT AppError IO)) a

        runApp :: Config -> AppState -> App a -> IO (Either AppError (a, AppState))
        runApp cfg st app = runExceptT (runStateT (runReaderT app cfg) st)
      </example>
    </pattern>

    <pattern name="mtl_style">
      <description>Use mtl type classes for polymorphic effect handling</description>
      <example>
        import Control.Monad.Reader
        import Control.Monad.State
        import Control.Monad.Except

        doSomething :: (MonadReader Config m, MonadState AppState m, MonadError AppError m) => m Result
        doSomething = do
          cfg <- ask
          st <- get
          when (invalid cfg) $ throwError InvalidConfig
          pure (compute cfg st)
      </example>
    </pattern>

    <common_transformers>
      <transformer name="ReaderT">Read-only environment; ask, local</transformer>
      <transformer name="StateT">Mutable state; get, put, modify</transformer>
      <transformer name="ExceptT">Error handling; throwError, catchError</transformer>
      <transformer name="WriterT">Accumulate output; tell, listen</transformer>
      <transformer name="MaybeT">Short-circuit on Nothing</transformer>
      <transformer name="ListT">Non-determinism (use list-t or logict for correct semantics)</transformer>
    </common_transformers>
  </monad_transformers>

  <optics>
    <description>Composable getters, setters, and traversals using lens library</description>

    <pattern name="lens_basics">
      <description>Focus on parts of data structures</description>
      <example>
        import Control.Lens

        data Person = Person { _name :: String, _age :: Int }
        makeLenses ''Person

        -- name :: Lens' Person String
        -- age :: Lens' Person Int

        getName :: Person -> String
        getName p = p ^. name

        setName :: String -> Person -> Person
        setName n p = p & name .~ n

        modifyAge :: (Int -> Int) -> Person -> Person
        modifyAge f p = p & age %~ f
      </example>
    </pattern>

    <pattern name="optic_types">
      <description>Different optic types for different access patterns</description>
      <optics_hierarchy>
        <optic name="Lens">Get and set exactly one value</optic>
        <optic name="Prism">Focus on one branch of a sum type</optic>
        <optic name="Traversal">Focus on zero or more values</optic>
        <optic name="Iso">Bidirectional transformation</optic>
        <optic name="Getter">Read-only access</optic>
        <optic name="Fold">Read-only traversal</optic>
      </optics_hierarchy>
    </pattern>

    <pattern name="lens_operators">
      <description>Common lens operators</description>
      <operators>
        <operator name="^.">View through lens (view)</operator>
        <operator name=".~">Set value (set)</operator>
        <operator name="%~">Modify value (over)</operator>
        <operator name="&amp;">Apply function (flip ($))</operator>
        <operator name="^?">View through prism (preview)</operator>
        <operator name="^..">View all through traversal (toListOf)</operator>
      </operators>
    </pattern>

    <alternative name="optics">
      <description>Alternative to lens with better type errors and composition</description>
      <package>optics</package>
      <note>Considered more modern; lens has larger ecosystem</note>
    </alternative>
  </optics>

  <error_handling>
    <pattern name="maybe">
      <description>Optional values; prefer over null</description>
      <example>
        findUser :: UserId -> Maybe User
        findUser uid = lookup uid users

        -- Safe chaining with Monad
        getUserEmail :: UserId -> Maybe Email
        getUserEmail uid = do
          user <- findUser uid
          pure (userEmail user)
      </example>
    </pattern>

    <pattern name="either">
      <description>Computations that may fail with error information</description>
      <example>
        parseConfig :: Text -> Either ParseError Config
        parseConfig input = do
          json <- parseJSON input
          validateConfig json
      </example>
    </pattern>

    <pattern name="exceptt">
      <description>Error handling in monadic contexts</description>
      <example>
        import Control.Monad.Except

        data AppError = NotFound | InvalidInput String | IOError IOException

        loadUser :: MonadError AppError m => UserId -> m User
        loadUser uid = do
          mUser <- findUser uid
          case mUser of
            Nothing -> throwError NotFound
            Just u  -> pure u
      </example>
    </pattern>
  </error_handling>

  <common_patterns>
    <pattern name="newtype">
      <description>Zero-cost wrapper for type safety</description>
      <example>
        newtype UserId = UserId { unUserId :: Int }
          deriving (Eq, Ord, Show)

        newtype Email = Email { unEmail :: Text }
          deriving (Eq, Show)
      </example>
    </pattern>

    <pattern name="smart_constructors">
      <description>Validate data at construction time</description>
      <example>
        module Email (Email, mkEmail, unEmail) where

        newtype Email = Email Text

        mkEmail :: Text -> Maybe Email
        mkEmail t
          | isValidEmail t = Just (Email t)
          | otherwise      = Nothing
      </example>
    </pattern>

    <pattern name="records">
      <description>Named fields with accessor functions</description>
      <example>
        {-# LANGUAGE RecordWildCards #-}
        data Config = Config
          { configHost :: String
          , configPort :: Int
          , configTimeout :: Int
          }

        -- Using RecordWildCards
        mkConnection :: Config -> IO Connection
        mkConnection Config{..} = connect configHost configPort
      </example>
    </pattern>
  </common_patterns>

  <anti_patterns>
    <avoid name="partial_functions">
      <description>Functions that crash on some inputs (head, tail, fromJust, read)</description>
      <instead>Use safe alternatives (headMay, listToMaybe) or pattern matching</instead>
    </avoid>

    <avoid name="string_type">
      <description>Using String ([Char]) for text processing</description>
      <instead>Use Text or ByteString for performance</instead>
    </avoid>

    <avoid name="lazy_io">
      <description>Using lazy IO (readFile, getContents) in production</description>
      <instead>Use strict IO or streaming (conduit, pipes, streaming)</instead>
    </avoid>

    <avoid name="orphan_instances">
      <description>Defining type class instances outside the module of the type or class</description>
      <instead>Use newtype wrappers or define instances in appropriate modules</instead>
    </avoid>
  </anti_patterns>
</haskell_language>

<cabal>
  <project_structure>
    <standard_layout>
      .
      ├── my-project.cabal
      ├── cabal.project          # Multi-package configuration
      ├── cabal.project.local    # Local overrides (gitignored)
      ├── src/
      │   └── MyProject.hs
      ├── app/
      │   └── Main.hs
      ├── test/
      │   └── Spec.hs
      └── bench/
          └── Bench.hs
    </standard_layout>
  </project_structure>

  <cabal_file>
    <basic_structure>
      cabal-version: 3.0
      name:          my-project
      version:       0.1.0.0
      synopsis:      Short description
      license:       MIT
      author:        Your Name
      maintainer:    your@email.com

      common warnings
        ghc-options: -Wall -Wcompat -Widentities -Wincomplete-record-updates
                     -Wincomplete-uni-patterns -Wpartial-fields -Wredundant-constraints

      library
        import:           warnings
        exposed-modules:  MyProject
        build-depends:    base ^>=4.18,
                          text ^>=2.0,
                          containers ^>=0.6
        hs-source-dirs:   src
        default-language: GHC2021

      executable my-project
        import:           warnings
        main-is:          Main.hs
        build-depends:    base ^>=4.18,
                          my-project
        hs-source-dirs:   app
        default-language: GHC2021

      test-suite my-project-test
        import:           warnings
        type:             exitcode-stdio-1.0
        main-is:          Spec.hs
        build-depends:    base ^>=4.18,
                          my-project,
                          hspec ^>=2.11,
                          QuickCheck ^>=2.14
        hs-source-dirs:   test
        default-language: GHC2021
    </basic_structure>

    <version_bounds>
      -- Caret (^>=): major version compatible
      base ^>=4.18        -- 4.18.x.x

      -- Range
      text >=2.0 && <2.2

      -- Any version (avoid in published packages)
      containers
    </version_bounds>

    <language_extensions>
      default-extensions:
        OverloadedStrings
        LambdaCase
        RecordWildCards
        DerivingStrategies
        GeneralizedNewtypeDeriving
        TypeApplications

      default-language: GHC2021  -- Recommended for new projects
    </language_extensions>
  </cabal_file>

  <cabal_project>
    <description>Multi-package project configuration</description>
    <example>
      packages: .
                ./subpackage

      -- Use local package
      optional-packages: ../local-dependency

      -- Optimization
      optimization: 2

      -- Documentation
      documentation: True

      -- Test options
      tests: True

      -- Allow newer dependencies
      allow-newer: base
    </example>
  </cabal_project>

  <commands>
    <command name="cabal build">Compile the project</command>
    <command name="cabal build all">Build all targets</command>
    <command name="cabal run">Build and run executable</command>
    <command name="cabal test">Run test suites</command>
    <command name="cabal repl">Start GHCi with project loaded</command>
    <command name="cabal haddock">Generate documentation</command>
    <command name="cabal update">Update package index</command>
    <command name="cabal freeze">Lock dependency versions</command>
    <command name="cabal gen-bounds">Generate version bounds</command>
    <command name="cabal outdated">Check for outdated dependencies</command>
  </commands>
</cabal>

<stack>
  <project_structure>
    <standard_layout>
      .
      ├── stack.yaml           # Stack project configuration
      ├── stack.yaml.lock      # Locked dependency versions
      ├── package.yaml         # hpack format (generates .cabal)
      └── ... (same as cabal)
    </standard_layout>
  </project_structure>

  <stack_yaml>
    <basic_structure>
      resolver: lts-22.0  # Stackage LTS snapshot

      packages:
        - .
        - ./subpackage

      extra-deps:
        - some-package-1.0.0
        - github: owner/repo
          commit: abc123

      ghc-options:
        "$locals": -Wall -Werror
    </basic_structure>
  </stack_yaml>

  <package_yaml>
    <description>hpack format; generates .cabal file</description>
    <example>
      name: my-project
      version: 0.1.0.0

      dependencies:
        - base >= 4.18 && < 5
        - text
        - containers

      ghc-options:
        - -Wall
        - -Wcompat

      default-extensions:
        - OverloadedStrings
        - LambdaCase

      library:
        source-dirs: src

      executables:
        my-project:
          main: Main.hs
          source-dirs: app
          dependencies:
            - my-project

      tests:
        my-project-test:
          main: Spec.hs
          source-dirs: test
          dependencies:
            - my-project
            - hspec
            - QuickCheck
    </example>
  </package_yaml>

  <commands>
    <command name="stack build">Compile the project</command>
    <command name="stack test">Run tests</command>
    <command name="stack run">Build and run executable</command>
    <command name="stack ghci">Start GHCi with project loaded</command>
    <command name="stack haddock">Generate documentation</command>
    <command name="stack clean">Clean build artifacts</command>
    <command name="stack upgrade">Upgrade Stack itself</command>
  </commands>

  <decision_tree name="cabal_vs_stack">
    <question>Which build tool should I use?</question>
    <branch condition="Need reproducible builds with Stackage">Stack with LTS resolver</branch>
    <branch condition="Publishing to Hackage">Cabal (native format)</branch>
    <branch condition="Complex dependency overrides">Cabal with cabal.project</branch>
    <branch condition="New to Haskell">Stack (simpler getting started)</branch>
    <branch condition="Nix integration">Cabal with haskell.nix or nixpkgs</branch>
  </decision_tree>
</stack>

<toolchain>
  <ghc>
    <description>Glasgow Haskell Compiler</description>
    <current_version>GHC 9.12+ (2025-2026)</current_version>

    <common_options>
      <option name="-Wall">Enable all warnings</option>
      <option name="-Werror">Treat warnings as errors</option>
      <option name="-O2">Optimization level 2</option>
      <option name="-threaded">Enable threaded runtime</option>
      <option name="-rtsopts">Enable runtime system options</option>
      <option name="-with-rtsopts">Set default RTS options</option>
    </common_options>

    <language_standards>
      <standard name="Haskell2010">Previous standard</standard>
      <standard name="GHC2021">Default edition; enables common extensions</standard>
      <standard name="GHC2024">Current recommended for new code; extends GHC2021</standard>
    </language_standards>
  </ghc>

  <hls>
    <description>Haskell Language Server - IDE support via LSP</description>
    <features>
      <feature>Code completion</feature>
      <feature>Type information on hover</feature>
      <feature>Go to definition</feature>
      <feature>Find references</feature>
      <feature>Code actions (import, qualify)</feature>
      <feature>Diagnostics (errors, warnings, hlint)</feature>
      <feature>Code formatting (fourmolu, ormolu, stylish-haskell)</feature>
    </features>

    <configuration>
      <file_reference>hls.yaml or hie.yaml</file_reference>
      cradle:
        cabal:
          - path: "src"
            component: "lib:my-project"
          - path: "app"
            component: "exe:my-project"
          - path: "test"
            component: "test:my-project-test"
    </configuration>
  </hls>

  <formatters>
    <formatter name="fourmolu">
      <description>Opinionated formatter; ormolu fork with more options</description>
      <usage>fourmolu -i src/**/*.hs</usage>
    </formatter>

    <formatter name="ormolu">
      <description>Minimal configuration formatter</description>
      <usage>ormolu -i src/**/*.hs</usage>
    </formatter>

    <formatter name="stylish-haskell">
      <description>Configurable import organization and formatting</description>
      <usage>stylish-haskell -i src/**/*.hs</usage>
    </formatter>
  </formatters>

  <linters>
    <linter name="hlint">
      <description>Suggest idiomatic Haskell improvements</description>
      <usage>hlint src/</usage>
      <configuration>
        <file_reference>.hlint.yaml</file_reference>
        - ignore: {name: "Use camelCase"}
        - warn: {name: "Use head"}
        - error: {name: "Use String"}
      </configuration>
    </linter>

    <linter name="stan">
      <description>Static analysis for Haskell</description>
      <usage>stan</usage>
    </linter>

    <linter name="weeder">
      <description>Detect dead code</description>
      <usage>weeder</usage>
    </linter>
  </linters>
</toolchain>

<testing>
  <hspec>
    <description>BDD-style testing framework</description>
    <example>
      import Test.Hspec

      main :: IO ()
      main = hspec $ do
        describe "Calculator" $ do
          it "adds two numbers" $ do
            add 1 2 `shouldBe` 3

          it "handles negative numbers" $ do
            add (-1) 1 `shouldBe` 0

        describe "Parser" $ do
          context "when input is valid" $ do
            it "parses successfully" $ do
              parse "valid" `shouldSatisfy` isRight

          context "when input is invalid" $ do
            it "returns error" $ do
              parse "invalid" `shouldSatisfy` isLeft
    </example>

    <matchers>
      <matcher name="shouldBe">Equality check</matcher>
      <matcher name="shouldSatisfy">Predicate check</matcher>
      <matcher name="shouldReturn">IO action result</matcher>
      <matcher name="shouldThrow">Exception check</matcher>
      <matcher name="shouldContain">List containment</matcher>
    </matchers>
  </hspec>

  <quickcheck>
    <description>Property-based testing; generate random test cases</description>
    <example>
      import Test.QuickCheck

      prop_reverseReverse :: [Int] -> Bool
      prop_reverseReverse xs = reverse (reverse xs) == xs

      prop_sortIdempotent :: [Int] -> Bool
      prop_sortIdempotent xs = sort (sort xs) == sort xs

      -- With preconditions
      prop_headLast :: NonEmptyList Int -> Bool
      prop_headLast (NonEmpty xs) = head xs == head xs

      -- Custom generators
      newtype PositiveInt = PositiveInt Int deriving Show

      instance Arbitrary PositiveInt where
        arbitrary = PositiveInt . abs <$> arbitrary
    </example>

    <integration>
      -- With HSpec
      describe "reverse" $ do
        it "is its own inverse" $ property $
          \xs -> reverse (reverse xs) == (xs :: [Int])
    </integration>
  </quickcheck>

  <hedgehog>
    <description>Modern property-based testing with integrated shrinking</description>
    <example>
      import Hedgehog
      import qualified Hedgehog.Gen as Gen
      import qualified Hedgehog.Range as Range

      prop_reverse :: Property
      prop_reverse = property $ do
        xs <- forAll $ Gen.list (Range.linear 0 100) Gen.alpha
        reverse (reverse xs) === xs
    </example>
  </hedgehog>

  <best_practices>
    <practice priority="critical">Use QuickCheck for properties; HSpec for examples</practice>
    <practice priority="high">Test edge cases: empty lists, zero, negative numbers</practice>
    <practice priority="high">Use type-driven development; write types first</practice>
    <practice priority="medium">Use doctest for documentation examples</practice>
  </best_practices>
</testing>

<context7_integration>
  <description>Use Context7 MCP for up-to-date Haskell documentation</description>

  <haskell_libraries>
    <!-- Verified Context7 IDs (Hackage format) -->
    <library name="Servant" id="/haskell-servant/servant" />
    <library name="Optics" id="/websites/hackage_haskell_package_optics-0_4_2_1" />
    <library name="HSpec" id="/websites/hackage_haskell_package_hspec-2_11_12" />
    <library name="Hedgehog" id="/websites/hackage-content_haskell_package_hedgehog-1_7" />
    <library name="Aeson" id="/websites/hackage_haskell_package_aeson-2_2_3_0" />
    <library name="Criterion" id="/haskell/criterion" />
    <library name="Haskell LSP" id="/haskell/lsp" />
    <library name="HTTP Client" id="/snoyberg/http-client" />
    <!-- Note: mtl, transformers, lens, QuickCheck not indexed in Context7 -->
    <!-- Use Hackage directly for these: hackage.haskell.org/package/{name} -->
  </haskell_libraries>

  <usage_patterns>
    <pattern name="optics_usage">
      <step>resolve-library-id libraryName="optics haskell"</step>
      <step>get-library-docs context7CompatibleLibraryID="/websites/hackage_haskell_package_optics-0_4_2_1" topic="lenses"</step>
    </pattern>

    <pattern name="testing_framework">
      <step>get-library-docs context7CompatibleLibraryID="/websites/hackage_haskell_package_hspec-2_11_12" topic="expectations"</step>
    </pattern>

    <pattern name="web_framework">
      <step>get-library-docs context7CompatibleLibraryID="/haskell-servant/servant" topic="server"</step>
    </pattern>
  </usage_patterns>
</context7_integration>

<workflow>
  <phase name="analyze">
    <objective>Understand Haskell code requirements</objective>
    <step>1. Check cabal file or package.yaml for project configuration</step>
    <step>2. Review existing types and type classes</step>
    <step>3. Identify monad transformer requirements</step>
    <step>4. Check for type-level programming needs</step>
  </phase>
  <phase name="implement">
    <objective>Write pure, type-safe Haskell code</objective>
    <step>1. Design with types first; let types guide implementation</step>
    <step>2. Use appropriate abstractions (Functor, Applicative, Monad)</step>
    <step>3. Handle errors with Maybe/Either/ExceptT</step>
    <step>4. Write property-based tests for core logic</step>
  </phase>
  <phase name="validate">
    <objective>Verify Haskell code correctness</objective>
    <step>1. Run cabal build or stack build</step>
    <step>2. Run hlint for suggestions</step>
    <step>3. Run cabal test or stack test</step>
    <step>4. Check formatting with fourmolu/ormolu</step>
  </phase>
</workflow>

<best_practices>
  <practice priority="critical">Let types guide design; use the type system to prevent errors</practice>
  <practice priority="critical">Avoid partial functions; use safe alternatives</practice>
  <practice priority="critical">Run hlint and fix suggestions before committing</practice>
  <practice priority="high">Use Text/ByteString instead of String for performance</practice>
  <practice priority="high">Prefer mtl-style type class constraints over concrete monad stacks</practice>
  <practice priority="high">Write property-based tests for core logic</practice>
  <practice priority="medium">Document exported functions with Haddock comments</practice>
  <practice priority="medium">Use newtypes for type safety</practice>
  <practice priority="medium">Enable GHC2021 or explicit commonly-used extensions</practice>
</best_practices>

<rules priority="critical">
  <rule>Run hlint before committing; address all suggestions</rule>
  <rule>Avoid partial functions (head, tail, fromJust); use safe alternatives</rule>
  <rule>Use types to encode invariants; make illegal states unrepresentable</rule>
</rules>

<rules priority="standard">
  <rule>Use fourmolu or ormolu for consistent formatting</rule>
  <rule>Prefer Text over String for text processing</rule>
  <rule>Write HSpec tests for behavior; QuickCheck for properties</rule>
  <rule>Use explicit type signatures for top-level definitions</rule>
</rules>

<related_agents>
  <agent name="design">Type system design, monad transformer architecture, and effect modeling</agent>
  <agent name="execute">Haskell implementation with proper abstractions and error handling</agent>
  <agent name="code-quality">Run hlint, check formatting, and enforce Haskell idioms</agent>
</related_agents>

<error_escalation>
  <level severity="low">
    <example>HLint suggestion about style</example>
    <action>Apply suggestion, maintain idiomatic code</action>
  </level>
  <level severity="medium">
    <example>Type error or missing instance</example>
    <action>Review types, add instance or adjust design</action>
  </level>
  <level severity="high">
    <example>Breaking change in public API</example>
    <action>Stop, present migration options to user</action>
  </level>
  <level severity="critical">
    <example>Partial function usage or unsafe code in library</example>
    <action>Block operation, require safe alternatives</action>
  </level>
</error_escalation>

<related_skills>
  <skill name="serena-usage">Navigate type class hierarchies and module structure</skill>
  <skill name="context7-usage">Fetch Haskell documentation and library references</skill>
  <skill name="investigation-patterns">Debug type errors, missing instances, and performance issues</skill>
  <skill name="nix-ecosystem">haskell.nix integration and nixpkgs Haskell infrastructure</skill>
</related_skills>

<constraints>
  <must>Use types to encode invariants</must>
  <must>Avoid partial functions in library code</must>
  <must>Follow Haskell style conventions</must>
  <avoid>Using String for text processing</avoid>
  <avoid>Lazy IO in production code</avoid>
  <avoid>Orphan instances</avoid>
</constraints>
