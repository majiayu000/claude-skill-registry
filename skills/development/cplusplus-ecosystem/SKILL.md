---
name: C++ Ecosystem
description: This skill should be used when working with C++ projects, CMakeLists.txt, Ninja, clang-tidy, clang-format, GoogleTest, Catch2, or Modern C++ (C++11-23) language patterns. Provides comprehensive C++ ecosystem patterns and best practices.
---

<purpose>
  Provide comprehensive patterns for Modern C++ (C++11-23) language, CMake build system, and toolchain configuration.
</purpose>

<cplusplus_language>
  <modern_features>
    <decision_tree name="when_to_use">
      <question>Are you working with modern C++ features like smart pointers, move semantics, or ranges?</question>
      <if_yes>Apply modern C++ patterns for safer, more efficient code</if_yes>
      <if_no>Consider refactoring legacy code to modern C++ standards</if_no>
    </decision_tree>

    <concept name="move_semantics">
      <description>Transfer ownership of resources without copying. Introduced in C++11.</description>
      <example>
        std::vector&lt;int&gt; v1 = {1, 2, 3};
        std::vector&lt;int&gt; v2 = std::move(v1); // v1 is now empty
      </example>
      <use>Use std::move for expensive-to-copy objects when ownership transfer is intended</use>
    </concept>

    <concept name="smart_pointers">
      <description>RAII-based automatic memory management</description>
      <types>
        <type name="unique_ptr">Exclusive ownership, zero overhead</type>
        <type name="shared_ptr">Shared ownership with reference counting</type>
        <type name="weak_ptr">Non-owning observer of shared_ptr</type>
      </types>
      <example>
        auto ptr = std::make_unique&lt;MyClass&gt;(args);
        auto shared = std::make_shared&lt;MyClass&gt;(args);
      </example>
    </concept>

    <concept name="constexpr">
      <description>Compile-time computation</description>
      <evolution>
        <version name="C++11">Simple expressions only</version>
        <version name="C++14">Loops and local variables allowed</version>
        <version name="C++17">if constexpr for compile-time branching</version>
        <version name="C++20">constexpr std::vector, std::string</version>
      </evolution>
    </concept>

    <concept name="auto_type_deduction">
      <description>Compiler deduces type from initializer</description>
      <example>
        auto x = 42;                    // int
        auto vec = std::vector&lt;int&gt;{};  // std::vector&lt;int&gt;
        auto [key, value] = pair;       // structured bindings (C++17)
      </example>
    </concept>

    <concept name="lambdas">
      <description>Anonymous function objects</description>
      <example>
        auto add = [](int a, int b) { return a + b; };
        auto capture_by_ref = [&amp;x]() { x++; };
        auto capture_by_val = [=]() { return x; };
        auto generic = [](auto a, auto b) { return a + b; };  // C++14
      </example>
    </concept>

    <concept name="concepts">
      <description>Constraints on template parameters (C++20)</description>
      <example>
        template&lt;typename T&gt;
        concept Addable = requires(T a, T b) { a + b; };

        template&lt;Addable T&gt;
        T add(T a, T b) { return a + b; }
      </example>
    </concept>

    <concept name="ranges">
      <description>Composable range operations (C++20)</description>
      <example>
        auto result = numbers
        | std::views::filter([](int n) { return n % 2 == 0; })
        | std::views::transform([](int n) { return n * 2; });
      </example>
    </concept>

    <concept name="modules">
      <description>C++20 modules for faster compilation and better encapsulation</description>
      <example>
        // math.cppm (module interface)
        export module math;
        export int add(int a, int b) { return a + b; }

        // main.cpp
        import math;
        int main() { return add(1, 2); }
      </example>
      <note>Requires CMake 3.28+ with CMAKE_CXX_SCAN_FOR_MODULES</note>
    </concept>

    <concept name="coroutines">
      <description>C++20 coroutines for async and generator patterns</description>
      <example>
        #include &lt;coroutine&gt;

        generator&lt;int&gt; range(int start, int end) {
          for (int i = start; i &lt; end; ++i) {
            co_yield i;
          }
        }

        task&lt;int&gt; async_compute() {
          co_return co_await some_async_operation();
        }
      </example>
      <note>Requires coroutine library (cppcoro, libcoro, or custom promise types)</note>
    </concept>

    <concept name="three_way_comparison">
      <description>C++20 spaceship operator for simplified comparisons</description>
      <example>
        struct Point {
          int x, y;
          auto operator&lt;=&gt;(const Point&amp;) const = default;
        };

        // Automatically generates ==, !=, &lt;, &gt;, &lt;=, &gt;=
      </example>
    </concept>

    <concept name="vocabulary_types">
      <description>C++17 vocabulary types for safer value handling</description>
      <types>
        <type name="std::optional">Maybe-value container, replaces nullable pointers</type>
        <type name="std::variant">Type-safe union, replaces raw unions</type>
        <type name="std::any">Type-erased container for any single value</type>
      </types>
      <example>
        std::optional&lt;int&gt; find_value(const std::vector&lt;int&gt;&amp; v, int target) {
          auto it = std::find(v.begin(), v.end(), target);
          if (it != v.end()) return *it;
          return std::nullopt;
        }

        std::variant&lt;int, std::string, double&gt; data = 42;
        std::visit([](auto&amp;&amp; val) { std::cout &lt;&lt; val; }, data);
      </example>
    </concept>
  </modern_features>

  <concurrency>
    <decision_tree name="when_to_use">
      <question>Do you need concurrent or parallel execution?</question>
      <if_yes>Use std::thread for explicit control, std::async for task-based parallelism, or atomics for lock-free synchronization</if_yes>
      <if_no>Use single-threaded sequential execution for simplicity</if_no>
    </decision_tree>

    <concept name="threads">
      <description>Thread creation and management</description>
      <example>
        std::thread t([]{ /* work */ });
        t.join();  // or t.detach()

        auto future = std::async(std::launch::async, []{ return 42; });
        int result = future.get();
      </example>
    </concept>

    <concept name="mutexes">
      <description>Mutual exclusion for shared data</description>
      <example>
        std::mutex mtx;
        std::lock_guard&lt;std::mutex&gt; lock(mtx);  // RAII lock

        std::shared_mutex rw_mtx;
        std::shared_lock&lt;std::shared_mutex&gt; read_lock(rw_mtx); // multiple readers
        std::unique_lock&lt;std::shared_mutex&gt; write_lock(rw_mtx); // exclusive writer
      </example>
    </concept>

    <concept name="atomics">
      <description>Lock-free atomic operations</description>
      <example>
        std::atomic&lt;int&gt; counter{0};
        counter.fetch_add(1, std::memory_order_relaxed);
        counter.store(10, std::memory_order_release);
        int val = counter.load(std::memory_order_acquire);
      </example>
    </concept>

    <concept name="condition_variables">
      <description>Thread synchronization primitives</description>
      <example>
        std::condition_variable cv;
        std::mutex mtx;
        bool ready = false;

        // Waiting thread
        std::unique_lock&lt;std::mutex&gt; lock(mtx);
        cv.wait(lock, []{ return ready; });

        // Notifying thread
        {
          std::lock_guard&lt;std::mutex&gt; lock(mtx);
          ready = true;
        }
        cv.notify_one();
      </example>
    </concept>

    <anti_patterns>
      <avoid name="data_races">
        <description>Accessing shared data without synchronization</description>
        <instead>Use mutex, atomic, or immutable data</instead>
      </avoid>
      <avoid name="deadlocks">
        <description>Circular lock dependencies</description>
        <instead>Use std::scoped_lock for multiple mutexes, consistent lock ordering</instead>
      </avoid>
    </anti_patterns>
  </concurrency>

  <patterns>
    <pattern name="raii">
      <description>Resource Acquisition Is Initialization - bind resource lifetime to object lifetime</description>
      <example>
        class FileHandle {
          FILE* file_;
        public:
          explicit FileHandle(const char* path) : file_(fopen(path, "r")) {}
          ~FileHandle() { if (file_) fclose(file_); }
          FileHandle(const FileHandle&amp;) = delete;
          FileHandle&amp; operator=(const FileHandle&amp;) = delete;
        };
      </example>
      <use_case>Managing resources: files, sockets, locks, memory</use_case>
    </pattern>

    <pattern name="rule_of_zero">
      <description>Prefer classes that do not define special member functions</description>
      <example>
        class Person {
          std::string name_;
          std::vector&lt;std::string&gt; addresses_;
          // No destructor, copy/move constructors, or assignment operators needed
        };
      </example>
      <use_case>Use smart pointers and standard containers; let compiler generate defaults</use_case>
    </pattern>

    <pattern name="rule_of_five">
      <description>If you define one of destructor, copy/move constructor, or copy/move assignment, define all five</description>
      <example>
        class Resource {
          int* data_;
        public:
          Resource();
          ~Resource();
          Resource(const Resource&amp;);
          Resource(Resource&amp;&amp;) noexcept;
          Resource&amp; operator=(const Resource&amp;);
          Resource&amp; operator=(Resource&amp;&amp;) noexcept;
        };
      </example>
      <use_case>Classes managing raw resources directly</use_case>
    </pattern>

    <pattern name="pimpl">
      <description>Pointer to Implementation - hide implementation details and reduce compilation dependencies</description>
      <example>
        // header
        class Widget {
          class Impl;
          std::unique_ptr&lt;Impl&gt; pimpl_;
        public:
          Widget();
          ~Widget();
          void doSomething();
        };

        // source
        class Widget::Impl {
          // implementation details
        };
      </example>
      <use_case>Reducing compile times, ABI stability, hiding implementation</use_case>
    </pattern>

    <pattern name="crtp">
      <description>Curiously Recurring Template Pattern - static polymorphism</description>
      <example>
        template&lt;typename Derived&gt;
        class Base {
        public:
          void interface() {
            static_cast&lt;Derived*&gt;(this)-&gt;implementation();
          }
        };

        class Derived : public Base&lt;Derived&gt; {
        public:
          void implementation() { /_ ... _/ }
        };
      </example>
      <use_case>Static polymorphism, mixin classes, compile-time polymorphism</use_case>
    </pattern>

    <pattern name="type_erasure">
      <description>Hide concrete types behind a uniform interface</description>
      <example>
        class AnyCallable {
          struct Concept {
            virtual ~Concept() = default;
            virtual void call() = 0;
          };
          template&lt;typename T&gt;
          struct Model : Concept {
            T obj_;
            void call() override { obj_(); }
          };
          std::unique_ptr&lt;Concept&gt; ptr_;
        public:
          template&lt;typename T&gt;
          AnyCallable(T obj) : ptr_(std::make_unique&lt;Model&lt;T&gt;&gt;(std::move(obj))) {}
        };
      </example>
      <use_case>std::function, std::any, runtime polymorphism without inheritance</use_case>
    </pattern>
  </patterns>

  <anti_patterns>
    <avoid name="raw_pointer_ownership">
      <description>Using raw pointers for ownership</description>
      <instead>Use std::unique_ptr or std::shared_ptr</instead>
    </avoid>

    <avoid name="manual_memory_management">
      <description>Using new/delete directly</description>
      <instead>Use std::make_unique/std::make_shared</instead>
    </avoid>

    <avoid name="c_style_casts">
      <description>Using (Type)value casts</description>
      <instead>Use static_cast, dynamic_cast, const_cast, or reinterpret_cast</instead>
    </avoid>

    <avoid name="using_namespace_in_headers">
      <description>Using using namespace std; in headers</description>
      <instead>Use fully qualified names or limited using declarations in source files</instead>
    </avoid>

    <avoid name="throwing_in_destructors">
      <description>Throwing exceptions in destructors</description>
      <instead>Mark destructors noexcept, handle errors internally</instead>
    </avoid>

    <avoid name="const_cast_abuse">
      <description>Using const_cast to remove const from data you do not own</description>
      <instead>Fix the design to avoid needing const_cast</instead>
    </avoid>
  </anti_patterns>
</cplusplus_language>

<cmake>
  <decision_tree name="when_to_use">
    <question>Are you building a C++ project with dependencies and multiple targets?</question>
    <if_yes>Use CMake for cross-platform, modern build configuration</if_yes>
    <if_no>Use simple Makefile for single-file projects or prototypes</if_no>
  </decision_tree>

  <project_structure>
    <standard_layout>
      .
      ├── CMakeLists.txt
      ├── cmake/
      │ └── modules/
      ├── src/
      │ ├── CMakeLists.txt
      │ ├── main.cpp
      │ └── lib/
      ├── include/
      │ └── project/
      ├── tests/
      │ ├── CMakeLists.txt
      │ └── test_*.cpp
      └── build/
    </standard_layout>
  </project_structure>

  <cmake_patterns>
    <pattern name="modern_cmake">
      <description>Target-based CMake (3.0+)</description>
      <example>
        cmake_minimum_required(VERSION 3.20)
        project(MyProject VERSION 1.0.0 LANGUAGES CXX)

        set(CMAKE_CXX_STANDARD 20)
        set(CMAKE_CXX_STANDARD_REQUIRED ON)
        set(CMAKE_CXX_EXTENSIONS OFF)

        add_library(mylib STATIC src/mylib.cpp)
        target_include_directories(mylib PUBLIC include)
        target_compile_features(mylib PUBLIC cxx_std_20)

        add_executable(myapp src/main.cpp)
        target_link_libraries(myapp PRIVATE mylib)
      </example>
    </pattern>

    <pattern name="find_package">
      <description>Finding and using external dependencies</description>
      <example>
        find_package(Threads REQUIRED)
        find_package(GTest REQUIRED)

        target_link_libraries(myapp PRIVATE Threads::Threads)
        target_link_libraries(mytests PRIVATE GTest::gtest GTest::gtest_main)
      </example>
    </pattern>

    <pattern name="compiler_options">
      <description>Setting compiler warnings and options</description>
      <example>
        add_library(project_warnings INTERFACE)
        target_compile_options(project_warnings INTERFACE
          $&lt;$&lt;CXX_COMPILER_ID:GNU,Clang&gt;:
            -Wall -Wextra -Wpedantic -Werror
            -Wshadow -Wnon-virtual-dtor -Wold-style-cast
            -Wcast-align -Wunused -Woverloaded-virtual
            -Wconversion -Wsign-conversion -Wnull-dereference
          &gt;
        )
      </example>
    </pattern>
  </cmake_patterns>

  <commands>
    <command name="cmake -B build -G Ninja">Configure with Ninja generator</command>
    <command name="cmake --build build">Build the project</command>
    <command name="cmake --build build --target test">Run tests</command>
    <command name="cmake --build build --config Release">Build in Release mode</command>
    <command name="cmake --install build --prefix /usr/local">Install the project</command>
  </commands>
</cmake>

<toolchain>
  <compilers>
    <compiler name="clang">
      <description>LLVM C++ compiler</description>
      <flags>
        <flag name="-std=c++20">Enable C++20 standard</flag>
        <flag name="-stdlib=libc++">Use LLVM libc++ standard library</flag>
        <flag name="-Wall -Wextra -Wpedantic">Enable comprehensive warnings</flag>
        <flag name="-Werror">Treat warnings as errors</flag>
        <flag name="-fsanitize=address,undefined">Enable sanitizers</flag>
      </flags>
    </compiler>

    <compiler name="gcc">
      <description>GNU C++ compiler</description>
      <flags>
        <flag name="-std=c++20">Enable C++20 standard</flag>
        <flag name="-Wall -Wextra -Wpedantic">Enable comprehensive warnings</flag>
        <flag name="-Werror">Treat warnings as errors</flag>
        <flag name="-fsanitize=address,undefined">Enable sanitizers</flag>
        <flag name="-fanalyzer">Enable static analysis (GCC 10+)</flag>
      </flags>
    </compiler>
  </compilers>

  <clang_tidy>
    <description>Static analysis and linting tool</description>
    <usage>clang-tidy src/*.cpp -- -std=c++20</usage>

    <configuration>
      <file_reference>.clang-tidy</file_reference>
      Checks: >
        -*,
        bugprone-*,
        clang-analyzer-*,
        cppcoreguidelines-*,
        modernize-*,
        performance-*,
        readability-*,
        -modernize-use-trailing-return-type

      WarningsAsErrors: '_'
      HeaderFilterRegex: '._'

      CheckOptions:
        - key: readability-identifier-naming.ClassCase
          value: CamelCase
        - key: readability-identifier-naming.FunctionCase
          value: camelBack
        - key: readability-identifier-naming.VariableCase
          value: lower_case
    </configuration>

    <common_checks>
      <check name="modernize-use-nullptr">Replace NULL with nullptr</check>
      <check name="modernize-use-auto">Use auto where appropriate</check>
      <check name="modernize-use-override">Use override keyword</check>
      <check name="modernize-loop-convert">Convert C-style loops to range-based</check>
      <check name="cppcoreguidelines-owning-memory">Check ownership semantics</check>
      <check name="bugprone-use-after-move">Detect use-after-move bugs</check>
      <check name="performance-unnecessary-copy-initialization">Detect unnecessary copies</check>
    </common_checks>
  </clang_tidy>

  <clang_format>
    <description>Code formatting tool</description>
    <usage>clang-format -i src/*.cpp include/*.hpp</usage>

    <configuration>
      <file_reference>.clang-format</file_reference>
      BasedOnStyle: LLVM
      IndentWidth: 4
      ColumnLimit: 100
      Language: Cpp
      Standard: c++20
      AccessModifierOffset: -4
      AlignAfterOpenBracket: Align
      AllowShortFunctionsOnASingleLine: Inline
      BreakBeforeBraces: Attach
      IncludeBlocks: Regroup
      IncludeCategories:
        - Regex: '^<.*>'
          Priority: 1
        - Regex: '^".*"'
          Priority: 2
      PointerAlignment: Left
      SortIncludes: CaseSensitive
    </configuration>
  </clang_format>

  <sanitizers>
    <description>Runtime error detection tools</description>

    <sanitizer name="AddressSanitizer">
      <description>Detects memory errors (buffer overflow, use-after-free)</description>
      <flags>-fsanitize=address -fno-omit-frame-pointer</flags>
      <cmake>
        target_compile_options(myapp PRIVATE -fsanitize=address -fno-omit-frame-pointer)
        target_link_options(myapp PRIVATE -fsanitize=address)
      </cmake>
    </sanitizer>

    <sanitizer name="UndefinedBehaviorSanitizer">
      <description>Detects undefined behavior (signed overflow, null dereference)</description>
      <flags>-fsanitize=undefined</flags>
      <cmake>
        target_compile_options(myapp PRIVATE -fsanitize=undefined)
        target_link_options(myapp PRIVATE -fsanitize=undefined)
      </cmake>
    </sanitizer>

    <sanitizer name="ThreadSanitizer">
      <description>Detects data races and deadlocks</description>
      <flags>-fsanitize=thread</flags>
      <note>Cannot be combined with AddressSanitizer</note>
    </sanitizer>

    <sanitizer name="MemorySanitizer">
      <description>Detects uninitialized memory reads (Clang only)</description>
      <flags>-fsanitize=memory</flags>
      <note>Requires all code and libraries to be instrumented</note>
    </sanitizer>

    <cmake_preset>
      # CMakePresets.json sanitizer configuration
      {
        "configurePresets": [{
          "name": "sanitize",
          "cacheVariables": {
            "CMAKE_CXX_FLAGS": "-fsanitize=address,undefined -fno-omit-frame-pointer"
          }
        }]
      }
    </cmake_preset>
  </sanitizers>
</toolchain>

<testing>
  <decision_tree name="when_to_use">
    <question>Do you need unit testing for C++ code?</question>
    <if_yes>Use GoogleTest for comprehensive testing features or Catch2 for header-only simplicity</if_yes>
    <if_no>Consider adding tests to improve code quality and maintainability</if_no>
  </decision_tree>

  <googletest>
    <description>Google Test framework</description>
    <cmake_integration>
      enable_testing()
      find_package(GTest REQUIRED)

      add_executable(tests tests/test_main.cpp)
      target_link_libraries(tests PRIVATE GTest::gtest GTest::gtest_main)

      include(GoogleTest)
      gtest_discover_tests(tests)
    </cmake_integration>

    <example>
      #include &lt;gtest/gtest.h&gt;

      TEST(MyTest, BasicAssertion) {
        EXPECT_EQ(1 + 1, 2);
      }

      TEST(MyTest, StringComparison) {
        std::string s = "hello";
        EXPECT_STREQ(s.c_str(), "hello");
      }

      class MyFixture : public ::testing::Test {
      protected:
        void SetUp() override { /_ setup _/ }
        void TearDown() override { /_ cleanup _/ }
      };

      TEST_F(MyFixture, FixtureTest) {
        EXPECT_TRUE(true);
      }
    </example>
  </googletest>

  <catch2>
    <description>Catch2 test framework</description>
    <cmake_integration>
      find_package(Catch2 3 REQUIRED)

      add_executable(tests tests/test_main.cpp)
      target_link_libraries(tests PRIVATE Catch2::Catch2WithMain)

      include(CTest)
      include(Catch)
      catch_discover_tests(tests)
    </cmake_integration>

    <example>
      #include &lt;catch2/catch_test_macros.hpp&gt;

      TEST_CASE("Basic arithmetic", "[math]") {
        REQUIRE(1 + 1 == 2);
        CHECK(2 * 2 == 4);
      }

      TEST_CASE("String operations", "[string]") {
        std::string s = "hello";

        SECTION("length") {
          REQUIRE(s.length() == 5);
        }

        SECTION("comparison") {
          REQUIRE(s == "hello");
        }
      }
    </example>
  </catch2>
</testing>

<context7_integration>
  <description>Use Context7 MCP for up-to-date C++ documentation</description>

  <cplusplus_libraries>
    <library name="cppreference" id="/websites/cppreference_com" />
    <library name="CMake" id="/Kitware/CMake" />
    <library name="GoogleTest" id="/google/googletest" />
    <library name="Catch2" id="/catchorg/Catch2" />
  </cplusplus_libraries>

  <usage_patterns>
    <pattern name="language_reference">
      <step>resolve-library-id libraryName="cppreference"</step>
      <step>get-library-docs context7CompatibleLibraryID="/websites/cppreference_com" topic="std::unique_ptr"</step>
    </pattern>

    <pattern name="cmake_reference">
      <step>get-library-docs context7CompatibleLibraryID="/Kitware/CMake" topic="target_link_libraries"</step>
    </pattern>

    <pattern name="testing_reference">
      <step>get-library-docs context7CompatibleLibraryID="/google/googletest" topic="assertions"</step>
    </pattern>
  </usage_patterns>
</context7_integration>

<best_practices>
  <practice priority="critical">Use smart pointers instead of raw pointers for ownership</practice>
  <practice priority="critical">Enable -Wall -Wextra -Werror for all builds</practice>
  <practice priority="critical">Run clang-tidy before committing</practice>
  <practice priority="critical">Format with clang-format for consistent style</practice>
  <practice priority="standard">Prefer const correctness throughout</practice>
  <practice priority="standard">Use noexcept for move constructors and destructors</practice>
  <practice priority="standard">Prefer constexpr for compile-time computation</practice>
  <practice priority="standard">Use std::string_view for non-owning string references</practice>
  <practice priority="standard">Prefer range-based for loops over index-based</practice>
  <practice priority="standard">Use structured bindings for tuple/pair access</practice>
  <practice priority="standard">Document public API with Doxygen comments</practice>
  <practice priority="standard">Write unit tests alongside implementation</practice>
</best_practices>

<workflow>
  <phase name="analyze">
    <objective>Understand C++ code requirements</objective>
    <step>1. Check CMakeLists.txt for build configuration</step>
    <step>2. Review existing code patterns and standards</step>
    <step>3. Identify memory management requirements</step>
  </phase>
  <phase name="implement">
    <objective>Write modern, safe C++ code</objective>
    <step>1. Use RAII and smart pointers</step>
    <step>2. Follow C++ Core Guidelines</step>
    <step>3. Prefer standard library over raw implementations</step>
  </phase>
  <phase name="validate">
    <objective>Verify C++ code correctness</objective>
    <step>1. Build with warnings enabled</step>
    <step>2. Run static analysis tools</step>
    <step>3. Execute tests with sanitizers</step>
  </phase>
</workflow>

<error_escalation>
  <level severity="low">
    <example>Compiler warning about unused variable</example>
    <action>Fix warning, maintain clean build</action>
  </level>
  <level severity="medium">
    <example>Compilation error</example>
    <action>Fix error, verify with full build</action>
  </level>
  <level severity="high">
    <example>Memory leak or undefined behavior detected</example>
    <action>Stop, require safe memory management</action>
  </level>
  <level severity="critical">
    <example>Buffer overflow or security vulnerability</example>
    <action>Block operation, require immediate fix</action>
  </level>
</error_escalation>

<constraints>
  <must>Use smart pointers for memory management</must>
  <must>Enable compiler warnings (-Wall -Wextra)</must>
  <must>Follow C++ Core Guidelines</must>
  <avoid>Raw pointers for ownership</avoid>
  <avoid>Manual memory management when smart pointers suffice</avoid>
  <avoid>Undefined behavior</avoid>
</constraints>

<related_agents>
  <agent name="design">Architecture design for C++ class hierarchies and template metaprogramming</agent>
  <agent name="docs">Doxygen documentation and API reference generation</agent>
  <agent name="execute">CMake configuration and C++ implementation tasks</agent>
  <agent name="bug">Debugging memory leaks, segfaults, and undefined behavior</agent>
</related_agents>

<related_skills>
  <skill name="serena-usage">Symbol operations for C++ code navigation and refactoring</skill>
  <skill name="context7-usage">C++ documentation via /websites/cppreference_com and CMake docs via /Kitware/CMake</skill>
  <skill name="investigation-patterns">Debugging with sanitizers, valgrind, and gdb</skill>
  <skill name="technical-documentation">Creating library documentation with Doxygen</skill>
</related_skills>
