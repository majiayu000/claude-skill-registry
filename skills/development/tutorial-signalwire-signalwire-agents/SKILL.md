---
name: tutorial-signalwire-signalwire-agents
description: Now we'll give Fred the ability to search Wikipedia! The SignalWire SDK's
  skills system makes this incredibly easy.
---

# Lesson 4: Adding the Wikipedia Search Skill

Now we'll give Fred the ability to search Wikipedia! The SignalWire SDK's skills system makes this incredibly easy.

## Table of Contents

1. [Understanding Skills](#understanding-skills)
2. [Adding the Wikipedia Skill](#adding-the-wikipedia-skill)
3. [Configuring the Skill](#configuring-the-skill)
4. [How Skills Work Internally](#how-skills-work-internally)
5. [Testing Wikipedia Search](#testing-wikipedia-search)

---

## Understanding Skills

Skills are modular capabilities that extend your agent's functionality. Think of them as plugins that add specific features.

### What is a Skill?

**A skill is:**
- A self-contained module with specific functionality
- Automatically integrated into your agent
- Configured with simple parameters
- Reusable across different agents

### Available Built-in Skills

The SDK includes several pre-built skills:
- `wikipedia_search` - Search Wikipedia articles
- `datetime` - Get current date/time
- `math` - Perform calculations
- `web_search` - Search Google (requires API key)
- `weather_api` - Get weather information

## Adding the Wikipedia Skill

Let's add Wikipedia search to Fred with just one line of code!

### Step 1: Basic Skill Addition

Add this to Fred's `__init__` method, after the global data:

```python
        # Add the Wikipedia search skill
        self.add_skill("wikipedia_search")
```

That's it! Fred can now search Wikipedia. But let's customize it for better results.

### Step 2: Customized Configuration

Replace the basic addition with this enhanced version:

```python
        # Add the Wikipedia search skill with custom configuration
        self.add_skill("wikipedia_search", {
            "num_results": 2,  # Get up to 2 articles for broader coverage
            "no_results_message": "Oh, I couldn't find anything about '{query}' on Wikipedia. Maybe try different keywords or let me know if you meant something else!",
            "swaig_fields": {
                "fillers": {
                    "en-US": [
                        "Let me look that up on Wikipedia for you...",
                        "Searching Wikipedia for that information...",
                        "One moment, checking Wikipedia...",
                        "Let me find that in the encyclopedia..."
                    ]
                }
            }
        })
```

## Configuring the Skill

Let's understand each configuration option:

### Configuration Parameters

**`num_results`** (default: 1)
- Number of Wikipedia articles to return
- More results = broader coverage but longer responses
- Fred uses 2 for balance

**`no_results_message`**
- Custom message when no articles are found
- Use `{query}` as a placeholder for the search term
- Should match your agent's personality

**`swaig_fields`**
- Additional SWAIG function configuration
- `fillers`: Phrases spoken while searching
- Enhances conversation flow

### Example Configurations

```python
# Minimal configuration
self.add_skill("wikipedia_search")

# Academic assistant
self.add_skill("wikipedia_search", {
    "num_results": 3,
    "no_results_message": "No Wikipedia entries found for '{query}'. Please verify the spelling or try related terms."
})

# Casual helper
self.add_skill("wikipedia_search", {
    "num_results": 1,
    "no_results_message": "Hmm, Wikipedia doesn't have info on '{query}'. Got another topic?",
    "swaig_fields": {
        "fillers": {
            "en-US": ["Let me check...", "Looking that up..."]
        }
    }
})
```

## How Skills Work Internally

Understanding the magic behind `add_skill()`:

### What Happens When You Add a Skill

1. **Skill Loading**
   ```python
   # The SDK dynamically imports the skill module
   from signalwire_agents.skills.wikipedia_search.skill import WikipediaSearchSkill
   ```

2. **Skill Initialization**
   ```python
   # Creates skill instance with your configuration
   skill = WikipediaSearchSkill(agent=self, params=config)
   ```

3. **Tool Registration**
   ```python
   # The skill registers its functions with your agent
   self.define_tool(
       name="search_wiki",
       description="Search Wikipedia for information",
       parameters={"query": {"type": "string", "description": "Search term"}},
       handler=skill._search_wiki_handler
   )
   ```

### The search_wiki Function

After adding the skill, Fred gains the `search_wiki` function:

**Function Signature:**
```python
search_wiki(query: string) -> string
```

**What it does:**
1. Searches Wikipedia for articles matching the query
2. Retrieves article summaries
3. Returns formatted results

**Example calls (by the AI):**
- `search_wiki("Albert Einstein")`
- `search_wiki("quantum physics")`
- `search_wiki("Great Wall of China")`

## Testing Wikipedia Search

Let's add some test code to verify the skill works:

### Step 3: Update Main Function

```python
def main():
    """Run Fred the Wiki Bot"""
    print("=" * 60)
    print("🤖 Fred - The Wikipedia Knowledge Bot")
    print("=" * 60)
    print()
    print("Fred is a friendly assistant who loves searching Wikipedia!")
    print("He can help you learn about almost any topic.")
    print()
    print("Example questions you can ask Fred:")
    print("  • 'Tell me about Albert Einstein'")
    print("  • 'What is quantum physics?'")
    print("  • 'Who was Marie Curie?'")
    print("  • 'Search for information about the solar system'")
    print()

    # Create Fred
    fred = FredTheWikiBot()

    # Show loaded skills
    loaded_skills = fred.list_skills()
    print(f"Fred's capabilities: {', '.join(loaded_skills)}")
    print()

    # The skill automatically adds tools to the agent
    # You can verify this by checking registered functions
    print("Wikipedia search is ready!")
    print("Fred can now search Wikipedia for any topic.")

if __name__ == "__main__":
    main()
```

Run it:
```bash
python fred.py
```

Expected output:
```
============================================================
🤖 Fred - The Wikipedia Knowledge Bot
============================================================

Fred is a friendly assistant who loves searching Wikipedia!
He can help you learn about almost any topic.

Example questions you can ask Fred:
  • 'Tell me about Albert Einstein'
  • 'What is quantum physics?'
  • 'Who was Marie Curie?'
  • 'Search for information about the solar system'

Fred's capabilities: wikipedia_search
Wikipedia search is ready!
Fred can now search Wikipedia for any topic.
```

## How Fred Uses Wikipedia Search

When a user asks Fred about a topic:

1. **User says:** "Tell me about Albert Einstein"

2. **Fred's AI recognizes** the request needs Wikipedia

3. **Fred calls:** `search_wiki("Albert Einstein")`

4. **Wikipedia returns** article summary

5. **Fred responds** with the information conversationally

### Example Conversation Flow

```
User: "Hi there!"
Fred: "Hello! I'm Fred, your friendly Wikipedia assistant! I love helping people learn new things. What would you like to know about today?"

User: "Tell me about black holes"
Fred: [filler] "Let me look that up on Wikipedia for you..."
Fred: "Fascinating topic! According to Wikipedia, a black hole is a region of spacetime where gravity is so strong that nothing—no particles or even electromagnetic radiation such as light—can escape from it..."

User: "That's interesting! Who discovered them?"
Fred: [filler] "Searching Wikipedia for that information..."
Fred: "Great question! The concept of black holes has a rich history..."
```

## Skill Benefits

### Why Use Skills vs Custom Implementation?

**With Skills:**
```python
# One line!
self.add_skill("wikipedia_search")
```

**Without Skills:**
```python
# You'd need to:
# 1. Import Wikipedia API library
# 2. Handle API calls
# 3. Parse responses
# 4. Format results
# 5. Handle errors
# 6. Register SWAIG function
# 7. Implement handler
# ... 50+ lines of code
```

### Skills Provide

1. **Tested functionality** - Pre-built and debugged
2. **Consistent interface** - Standard configuration pattern
3. **Error handling** - Graceful failure modes
4. **Documentation** - Clear usage instructions
5. **Maintenance** - Updates with SDK

## Next Steps

Fred can now search Wikipedia! But let's make him more fun by adding a custom function for sharing Wikipedia facts.

➡️ Continue to [Lesson 5: Creating Custom Functions](05-custom-functions.md)

---

**Skill Checklist:**
- [x] Added wikipedia_search skill
- [x] Configured custom messages
- [x] Added search fillers
- [x] Tested skill loading

**What Fred Can Do Now:**
- ✅ Search Wikipedia for any topic
- ✅ Return up to 2 article summaries
- ✅ Handle searches with no results gracefully
- ✅ Provide natural conversation flow with fillers

---

[← Previous: Basic Agent](03-basic-agent.md) | [Back to Overview](README.md) | [Next: Custom Functions →](05-custom-functions.md)