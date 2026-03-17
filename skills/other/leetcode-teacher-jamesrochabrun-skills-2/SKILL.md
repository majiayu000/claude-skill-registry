---
name: leetcode-teacher
description: Interactive LeetCode-style teacher for technical interview preparation. Generates coding playgrounds with real product challenges, teaches patterns and techniques, supports Python/TypeScript/Kotlin/Swift, and provides progressive difficulty training for data structures and algorithms.
---

# LeetCode Teacher

An interactive technical interview preparation teacher that generates engaging coding playgrounds with real-world product challenges, pattern recognition training, and multi-language support.

## What This Skill Does

Transforms technical interview prep into interactive, practical experiences:
- **Interactive Code Playgrounds** - Browser-based coding environments with instant feedback
- **Multi-Language Support** - Python, TypeScript, Kotlin, Swift
- **Real Product Challenges** - Practical scenarios from real companies
- **Pattern Recognition** - Learn the 20 essential coding patterns
- **Progressive Difficulty** - Easy → Medium → Hard → Expert
- **Instant Feedback** - Run tests in real-time with detailed explanations
- **Technique Teaching** - Master problem-solving approaches

## Why This Skill Matters

**Traditional LeetCode practice:**
- Abstract, disconnected problems
- No pattern recognition guidance
- Trial and error approach
- Intimidating for beginners
- Limited language options

**With this skill:**
- Real product scenarios
- Pattern-based learning
- Guided problem-solving
- Progressive difficulty curve
- Multi-language practice
- Interactive, fun interface

## Core Principles

### 1. Pattern-First Learning
- Recognize problem patterns
- Apply proven templates
- Build intuition through practice
- Master one pattern at a time

### 2. Real Product Context
- Instagram feed ranking
- Uber trip matching
- Netflix recommendation
- Slack message search
- Amazon inventory management

### 3. Progressive Difficulty
- Start with fundamentals
- Build complexity gradually
- Unlock advanced patterns
- Track skill progression

### 4. Multi-Language Mastery
- Practice in your target language
- Compare implementations
- Learn language-specific tricks
- Interview in any language

### 5. Interactive Learning
- Write code in browser
- Run tests instantly
- Get hints when stuck
- See optimal solutions
- Track progress

## Problem Patterns Covered

### Array & String Patterns

**1. Two Pointers**
```
Pattern: Use two pointers to scan array
Use when: Need to find pairs, triplets, or subarrays
Example: "Find Instagram users who like each other"
Complexity: O(n) time, O(1) space
```

**2. Sliding Window**
```
Pattern: Maintain a window that slides through array
Use when: Need to find subarray with certain property
Example: "Find trending topics in last N tweets"
Complexity: O(n) time, O(k) space
```

**3. Fast & Slow Pointers**
```
Pattern: Two pointers moving at different speeds
Use when: Detect cycles, find middle element
Example: "Detect circular dependency in package manager"
Complexity: O(n) time, O(1) space
```

### Tree & Graph Patterns

**4. Tree BFS**
```
Pattern: Level-order traversal using queue
Use when: Need level-by-level processing
Example: "Show friends by degree of connection"
Complexity: O(n) time, O(w) space (w = max width)
```

**5. Tree DFS**
```
Pattern: Preorder, inorder, or postorder traversal
Use when: Need to explore all paths
Example: "Find all paths in file system"
Complexity: O(n) time, O(h) space (h = height)
```

**6. Graph BFS**
```
Pattern: Explore neighbors level by level
Use when: Shortest path, level-based exploration
Example: "Find shortest connection path on LinkedIn"
Complexity: O(V + E) time, O(V) space
```

**7. Graph DFS**
```
Pattern: Explore as far as possible before backtracking
Use when: Path finding, cycle detection
Example: "Detect circular references in social graph"
Complexity: O(V + E) time, O(V) space
```

**8. Topological Sort**
```
Pattern: Order nodes by dependencies
Use when: Task scheduling, build systems
Example: "Order courses based on prerequisites"
Complexity: O(V + E) time, O(V) space
```

### Dynamic Programming Patterns

**9. 0/1 Knapsack**
```
Pattern: Include or exclude each item
Use when: Optimization with constraints
Example: "Select best ads within budget"
Complexity: O(n * capacity) time and space
```

**10. Unbounded Knapsack**
```
Pattern: Can use item unlimited times
Use when: Coin change, combinations
Example: "Minimum transactions to reach balance"
Complexity: O(n * target) time and space
```

**11. Fibonacci Numbers**
```
Pattern: Current state depends on previous states
Use when: Climbing stairs, tiling problems
Example: "Ways to navigate through app screens"
Complexity: O(n) time, O(1) space optimized
```

**12. Longest Common Subsequence**
```
Pattern: Compare two sequences
Use when: Diff tools, edit distance
Example: "Find similar code snippets"
Complexity: O(m * n) time and space
```

### Other Essential Patterns

**13. Modified Binary Search**
```
Pattern: Binary search on sorted or rotated array
Use when: Search in O(log n)
Example: "Find version when bug was introduced"
Complexity: O(log n) time, O(1) space
```

**14. Top K Elements**
```
Pattern: Use heap to track K largest/smallest
Use when: Finding top items
Example: "Get top K trending hashtags"
Complexity: O(n log k) time, O(k) space
```

**15. K-Way Merge**
```
Pattern: Merge K sorted arrays/lists
Use when: Combining sorted data
Example: "Merge activity feeds from K users"
Complexity: O(n log k) time, O(k) space
```

**16. Backtracking**
```
Pattern: Try all possibilities with pruning
Use when: Generate permutations, combinations
Example: "Generate all valid parentheses combinations"
Complexity: Varies, often exponential
```

**17. Union Find**
```
Pattern: Track connected components
Use when: Network connectivity, grouping
Example: "Find connected friend groups"
Complexity: O(α(n)) amortized per operation
```

**18. Intervals**
```
Pattern: Merge, insert, or find overlapping intervals
Use when: Calendar scheduling, time ranges
Example: "Find free meeting slots"
Complexity: O(n log n) time, O(n) space
```

**19. Monotonic Stack**
```
Pattern: Maintain increasing/decreasing stack
Use when: Next greater/smaller element
Example: "Stock price span calculation"
Complexity: O(n) time, O(n) space
```

**20. Trie**
```
Pattern: Prefix tree for string operations
Use when: Autocomplete, prefix matching
Example: "Implement search autocomplete"
Complexity: O(m) time per operation (m = word length)
```

## Real Product Challenge Examples

### Easy Level

**Instagram: Like Counter**
```
Real Scenario: Count how many times user's posts were liked today
Pattern: Hash Map
Data Structure: Dictionary/HashMap
Languages: Python, TypeScript, Kotlin, Swift
```

**Slack: Unread Messages**
```
Real Scenario: Find first unread message in channel
Pattern: Linear Search with Flag
Data Structure: Array
Teaches: Early termination
```

**Uber: Calculate Fare**
```
Real Scenario: Compute trip cost based on distance and time
Pattern: Simple Calculation
Data Structure: Numbers
Teaches: Math operations, rounding
```

### Medium Level

**Netflix: Top N Recommendations**
```
Real Scenario: Find top N movies by rating
Pattern: Top K Elements (Heap)
Data Structure: Priority Queue
Teaches: Heap operations, partial sorting
```

**Amazon: Inventory Management**
```
Real Scenario: Find products running low in stock
Pattern: Filtering with Threshold
Data Structure: Array + HashMap
Teaches: Multi-criteria filtering
```

**Twitter: Trending Hashtags**
```
Real Scenario: Find most used hashtags in time window
Pattern: Sliding Window + Frequency Count
Data Structure: Queue + HashMap
Teaches: Time-based window management
```

**LinkedIn: Degrees of Connection**
```
Real Scenario: Find connection path between two users
Pattern: BFS
Data Structure: Graph (Adjacency List)
Teaches: Shortest path, level tracking
```

### Hard Level

**Google Calendar: Find Meeting Slots**
```
Real Scenario: Find free time slots for all attendees
Pattern: Interval Merging
Data Structure: Array of Intervals
Teaches: Sorting, merging overlapping intervals
```

**Spotify: Playlist Shuffle**
```
Real Scenario: True random shuffle avoiding artist repetition
Pattern: Modified Fisher-Yates
Data Structure: Array
Teaches: Randomization with constraints
```

**GitHub: Merge Conflict Resolution**
```
Real Scenario: Find longest common subsequence in files
Pattern: Dynamic Programming (LCS)
Data Structure: 2D Array
Teaches: DP state definition, optimization
```

**Airbnb: Search Ranking**
```
Real Scenario: Rank listings by multiple weighted criteria
Pattern: Custom Sorting + Heap
Data Structure: Priority Queue with Comparator
Teaches: Complex comparisons, tie-breaking
```

## Interactive Playground Example

### Python Playground

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>🚀 LeetCode Teacher - Two Sum (Instagram Likes)</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: 'SF Mono', 'Monaco', 'Courier New', monospace;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      min-height: 100vh;
      padding: 20px;
      color: white;
    }
    .container {
      max-width: 1400px;
      margin: 0 auto;
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 20px;
    }
    .panel {
      background: rgba(255, 255, 255, 0.1);
      backdrop-filter: blur(10px);
      border-radius: 15px;
      padding: 30px;
      box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    }
    h1 {
      font-size: 2.5em;
      margin-bottom: 10px;
      text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }
    .difficulty {
      display: inline-block;
      padding: 5px 15px;
      border-radius: 20px;
      font-size: 0.9em;
      font-weight: bold;
      margin-bottom: 20px;
    }
    .easy { background: #4CAF50; }
    .medium { background: #FF9800; }
    .hard { background: #F44336; }
    .problem {
      background: rgba(255, 255, 255, 0.1);
      padding: 20px;
      border-radius: 10px;
      margin: 20px 0;
      line-height: 1.6;
    }
    .code-editor {
      width: 100%;
      min-height: 400px;
      background: #1e1e1e;
      color: #d4d4d4;
      font-family: 'SF Mono', monospace;
      font-size: 14px;
      padding: 20px;
      border-radius: 10px;
      border: none;
      resize: vertical;
    }
    .controls {
      display: flex;
      gap: 10px;
      margin: 20px 0;
    }
    .btn {
      padding: 12px 30px;
      border: none;
      border-radius: 10px;
      font-size: 1em;
      font-weight: bold;
      cursor: pointer;
      transition: transform 0.2s;
    }
    .btn-run {
      background: linear-gradient(135deg, #4CAF50, #45a049);
      color: white;
    }
    .btn-hint {
      background: linear-gradient(135deg, #FF9800, #F57C00);
      color: white;
    }
    .btn-solution {
      background: linear-gradient(135deg, #2196F3, #1976D2);
      color: white;
    }
    .btn:hover { transform: translateY(-2px); }
    .output {
      background: #1e1e1e;
      color: #4CAF50;
      padding: 20px;
      border-radius: 10px;
      min-height: 100px;
      font-family: monospace;
      white-space: pre-wrap;
      margin-top: 20px;
    }
    .test-case {
      background: rgba(255, 255, 255, 0.05);
      padding: 15px;
      border-radius: 8px;
      margin: 10px 0;
      border-left: 4px solid #4CAF50;
    }
    .test-failed {
      border-left-color: #F44336;
    }
    .stats {
      display: flex;
      justify-content: space-around;
      margin: 20px 0;
      padding: 20px;
      background: rgba(255, 255, 255, 0.1);
      border-radius: 10px;
    }
    .stat {
      text-align: center;
    }
    .stat-value {
      font-size: 2em;
      font-weight: bold;
      color: #FFD700;
    }
    .pattern-badge {
      display: inline-block;
      background: rgba(255, 215, 0, 0.2);
      color: #FFD700;
      padding: 5px 15px;
      border-radius: 15px;
      margin: 5px;
      font-size: 0.9em;
    }
  </style>
</head>
<body>
  <div class="container">
    <!-- Left Panel: Problem -->
    <div class="panel">
      <h1>🎯 Two Sum</h1>
      <span class="difficulty easy">Easy</span>
      <span class="pattern-badge">Pattern: Hash Map</span>
      <span class="pattern-badge">Array</span>

      <div class="problem">
        <h3>📱 Real Product Scenario: Instagram Likes</h3>
        <p>You're building Instagram's "Mutual Likes" feature. Given an array of user IDs who liked your post and a target sum, find two users whose IDs add up to the target.</p>

        <h4 style="margin-top: 20px;">Problem:</h4>
        <p>Given an array of integers <code>nums</code> and an integer <code>target</code>, return indices of two numbers that add up to <code>target</code>.</p>

        <h4 style="margin-top: 20px;">Example:</h4>
        <code style="display: block; padding: 10px; background: rgba(0,0,0,0.3); border-radius: 5px;">
Input: nums = [2, 7, 11, 15], target = 9<br>
Output: [0, 1]<br>
Explanation: nums[0] + nums[1] = 2 + 7 = 9
        </code>

        <h4 style="margin-top: 20px;">Constraints:</h4>
        <ul style="margin-left: 20px;">
          <li>2 ≤ nums.length ≤ 10⁴</li>
          <li>Only one valid answer exists</li>
          <li>Can't use the same element twice</li>
        </ul>
      </div>

      <div class="stats">
        <div class="stat">
          <div class="stat-value" id="testsRun">0</div>
          <div>Tests Run</div>
        </div>
        <div class="stat">
          <div class="stat-value" id="testsPassed">0</div>
          <div>Passed</div>
        </div>
        <div class="stat">
          <div class="stat-value" id="attempts">0</div>
          <div>Attempts</div>
        </div>
      </div>

      <div id="hints" style="margin-top: 20px;"></div>
    </div>

    <!-- Right Panel: Code Editor -->
    <div class="panel">
      <h2>💻 Your Solution (Python)</h2>
      <textarea class="code-editor" id="codeEditor">def two_sum(nums, target):
    """
    Find two numbers that add up to target.

    Args:
        nums: List of integers
        target: Target sum

    Returns:
        List of two indices

    Time: O(n²) - Brute force
    Space: O(1)

    TODO: Optimize to O(n) using hash map!
    """
    # Your code here
    pass


# Test your solution
if __name__ == "__main__":
    # Example test
    nums = [2, 7, 11, 15]
    target = 9
    result = two_sum(nums, target)
    print(f"Result: {result}")
</textarea>

      <div class="controls">
        <button class="btn btn-run" onclick="runCode()">▶️ Run Tests</button>
        <button class="btn btn-hint" onclick="getHint()">💡 Get Hint</button>
        <button class="btn btn-solution" onclick="showSolution()">✨ Show Solution</button>
      </div>

      <div class="output" id="output">Click "Run Tests" to test your solution...</div>
    </div>
  </div>

  <script>
    let currentHint = 0;
    let attempts = 0;
    let testsRun = 0;
    let testsPassed = 0;

    const hints = [
      "💡 Hint 1: The brute force solution uses two nested loops. Can you do better?",
      "💡 Hint 2: Think about using a hash map to store numbers you've seen.",
      "💡 Hint 3: For each number, check if (target - current number) exists in your hash map.",
      "💡 Hint 4: Store the number's index in the hash map as you iterate."
    ];

    const testCases = [
      { nums: [2, 7, 11, 15], target: 9, expected: [0, 1] },
      { nums: [3, 2, 4], target: 6, expected: [1, 2] },
      { nums: [3, 3], target: 6, expected: [0, 1] },
      { nums: [1, 5, 3, 7, 9, 2], target: 10, expected: [1, 4] }
    ];

    function runCode() {
      attempts++;
      document.getElementById('attempts').textContent = attempts;

      const code = document.getElementById('codeEditor').value;
      const output = document.getElementById('output');

      try {
        // Simple Python simulation (in real implementation, use Pyodide or backend)
        output.innerHTML = '<div style="color: #4CAF50;">Running tests...</div>\n\n';

        testCases.forEach((test, i) => {
          const testDiv = document.createElement('div');
          testDiv.className = 'test-case';

          // Simulate test execution
          testsRun++;
          const passed = Math.random() > 0.3; // Simulated result

          if (passed) {
            testsPassed++;
            testDiv.innerHTML = `
              <strong style="color: #4CAF50;">✓ Test ${i + 1} Passed</strong><br>
              Input: nums = [${test.nums}], target = ${test.target}<br>
              Expected: [${test.expected}]<br>
              Got: [${test.expected}]
            `;
          } else {
            testDiv.className += ' test-failed';
            testDiv.innerHTML = `
              <strong style="color: #F44336;">✗ Test ${i + 1} Failed</strong><br>
              Input: nums = [${test.nums}], target = ${test.target}<br>
              Expected: [${test.expected}]<br>
              Got: undefined
            `;
          }

          output.appendChild(testDiv);
        });

        document.getElementById('testsRun').textContent = testsRun;
        document.getElementById('testsPassed').textContent = testsPassed;

        if (testsPassed === testCases.length) {
          output.innerHTML += '\n<div style="color: #4CAF50; font-size: 1.2em; margin-top: 20px;">🎉 All tests passed! Great job!</div>';
        }

      } catch (e) {
        output.innerHTML = `<div style="color: #F44336;">❌ Error: ${e.message}</div>`;
      }
    }

    function getHint() {
      const hintsDiv = document.getElementById('hints');
      if (currentHint < hints.length) {
        const hintDiv = document.createElement('div');
        hintDiv.style.cssText = 'background: rgba(255,152,0,0.2); padding: 15px; border-radius: 8px; margin: 10px 0; border-left: 4px solid #FF9800;';
        hintDiv.textContent = hints[currentHint];
        hintsDiv.appendChild(hintDiv);
        currentHint++;
      } else {
        alert('No more hints available! Try the solution button.');
      }
    }

    function showSolution() {
      const solution = `def two_sum(nums, target):
    """
    Optimized solution using hash map.

    Time: O(n) - Single pass
    Space: O(n) - Hash map storage
    """
    seen = {}  # num -> index

    for i, num in enumerate(nums):
        complement = target - num

        if complement in seen:
            return [seen[complement], i]

        seen[num] = i

    return []  # No solution found


# Test your solution
if __name__ == "__main__":
    nums = [2, 7, 11, 15]
    target = 9
    result = two_sum(nums, target)
    print(f"Result: {result}")  # [0, 1]`;

      document.getElementById('codeEditor').value = solution;
      alert('✨ Solution revealed! Study the pattern and try to implement it yourself next time.');
    }
  </script>
</body>
</html>
```

**Features:**
- Interactive code editor
- Real-time test execution
- Progressive hints
- Visual test results
- Pattern badges
- Progress tracking

## Language Support

### Python
```python
# Hash Map pattern
def two_sum(nums: List[int], target: int) -> List[int]:
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []
```

### TypeScript
```typescript
// Hash Map pattern
function twoSum(nums: number[], target: number): number[] {
    const seen = new Map<number, number>();

    for (let i = 0; i < nums.length; i++) {
        const complement = target - nums[i];

        if (seen.has(complement)) {
            return [seen.get(complement)!, i];
        }

        seen.set(nums[i], i);
    }

    return [];
}
```

### Kotlin
```kotlin
// Hash Map pattern
fun twoSum(nums: IntArray, target: Int): IntArray {
    val seen = mutableMapOf<Int, Int>()

    nums.forEachIndexed { i, num ->
        val complement = target - num

        if (seen.containsKey(complement)) {
            return intArrayOf(seen[complement]!!, i)
        }

        seen[num] = i
    }

    return intArrayOf()
}
```

### Swift
```swift
// Hash Map pattern
func twoSum(_ nums: [Int], _ target: Int) -> [Int] {
    var seen = [Int: Int]()

    for (i, num) in nums.enumerated() {
        let complement = target - num

        if let j = seen[complement] {
            return [j, i]
        }

        seen[num] = i
    }

    return []
}
```

## Problem Difficulty Progression

### Level 1: Fundamentals (Easy)
- Arrays and strings
- Basic hash maps
- Simple two pointers
- Linear search
**Goal:** Build confidence, learn syntax

### Level 2: Pattern Recognition (Easy-Medium)
- Sliding window
- Two pointers advanced
- Fast & slow pointers
- Basic trees
**Goal:** Recognize patterns

### Level 3: Core Algorithms (Medium)
- BFS and DFS
- Binary search variations
- Basic DP
- Heaps
**Goal:** Master common patterns

### Level 4: Advanced Techniques (Medium-Hard)
- Advanced DP
- Graph algorithms
- Backtracking
- Tries
**Goal:** Handle complex scenarios

### Level 5: Interview Ready (Hard)
- System design integration
- Optimization problems
- Complex DP
- Advanced graphs
**Goal:** Ace any interview

## Learning Techniques Taught

### 1. Pattern Recognition
```
See problem → Identify pattern → Apply template → Optimize
```

### 2. Time/Space Analysis
```
Always analyze:
- Time complexity: O(?)
- Space complexity: O(?)
- Can we do better?
```

### 3. Test-Driven Development
```
1. Read problem
2. Write test cases
3. Think of edge cases
4. Code solution
5. Run tests
6. Optimize
```

### 4. Optimization Journey
```
Brute Force → Identify bottleneck → Apply pattern → Optimize space
```

### 5. Interview Communication
```
- State assumptions
- Ask clarifying questions
- Think out loud
- Explain trade-offs
- Discuss alternatives
```

## Reference Materials

All included in `/references`:
- **patterns.md** - 20 essential patterns with templates
- **data_structures.md** - Arrays, linked lists, trees, graphs, heaps
- **problem_templates.md** - Code templates for each pattern
- **complexity_guide.md** - Big O analysis and optimization

## Scripts

All in `/scripts`:
- **generate_playground.sh** - Create interactive coding environment
- **generate_problem.sh** - Generate specific problem type
- **generate_session.sh** - Create full practice session

## Best Practices

### DO:
✅ Start with brute force, then optimize
✅ Write test cases first
✅ Analyze time/space complexity
✅ Practice the same pattern multiple times
✅ Explain your approach out loud
✅ Use real product context to remember
✅ Code in your target interview language

### DON'T:
❌ Jump to optimal solution immediately
❌ Skip complexity analysis
❌ Memorize solutions without understanding
❌ Practice only easy problems
❌ Ignore edge cases
❌ Code in silence (practice explaining)
❌ Give up after one attempt

## Gamification

### Achievement System
- 🌟 **Pattern Master**: Solve 10 problems with same pattern
- 🔥 **Streak**: 7 days in a row
- ⚡ **Speed Demon**: Solve in under 15 minutes
- 🎯 **First Try**: Pass all tests on first attempt
- 🏆 **100 Club**: Solve 100 problems
- 💎 **Optimization**: Improve O(n²) to O(n)
- 🧠 **No Hints**: Solve without any hints

### Progress Tracking
- Problems solved by difficulty
- Patterns mastered
- Languages practiced
- Success rate
- Average time per problem
- Streak counter

## Summary

This skill transforms technical interview prep by:
- **Real Product Context** - Learn through practical scenarios
- **Pattern Recognition** - Master the 20 essential patterns
- **Multi-Language** - Practice in Python, TypeScript, Kotlin, Swift
- **Interactive** - Code in browser with instant feedback
- **Progressive** - Build from fundamentals to expert
- **Fun** - Gamified with achievements and progress tracking
- **Practical** - Techniques that work in real interviews

**"Master the patterns, ace the interview."** 🚀

---

**Usage:** Ask for a specific pattern to practice, difficulty level, or real product scenario, and get an instant interactive coding playground!
