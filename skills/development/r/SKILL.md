---
name: r
description: R statistical programming for data analysis, visualization, and modeling. Use for .r files.
---

# R

A language and environment for statistical computing and graphics.

## When to Use

- Statistical Analysis
- Data Visualization (ggplot2)
- Bioinformatics
- Academic research

## Quick Start

```r
print("Hello, World!")

# Vector
x <- c(1, 2, 3, 4, 5)

# Mean
mean(x)

# Data Frame
df <- data.frame(
  Name = c("Alice", "Bob"),
  Age = c(25, 30)
)
```

## Core Concepts

### Vectorization

R operations are designed to work on entire vectors at once, avoiding explicit loops.

```r
x + 1 # Adds 1 to every element in x
```

### Pipe Operator `%>%`

Used to clean code by passing output of one function as input to the next (Tidyverse).

```r
data %>%
  filter(users > 100) %>%
  group_by(region) %>%
  summarize(total = sum(users))
```

## Best Practices

**Do**:

- Use the Tidyverse (dplyr, ggplot2) for modern R
- Document functions with Roxygen2
- Use RStudio IDE

**Don't**:

- Use explicit `for` loops if vectorization is possible (performance)
- Mix naming conventions (snake_case is preferred in tidyverse)

## References

- [R Project](https://www.r-project.org/)
- [R for Data Science](https://r4ds.had.co.nz/)
