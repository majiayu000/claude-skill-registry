---
name: coding-r
cluster: coding
description: "R: data frames, tidyverse, ggplot2, statistical modeling, RMarkdown, Shiny, package development"
tags: ["r","statistics","data-science","coding"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "r language statistics tidyverse ggplot2 data science shiny"
---

## Purpose

This skill allows the AI to execute R programming tasks for data manipulation, visualization, and analysis using packages like tidyverse and ggplot2, focusing on data frames, statistical modeling, RMarkdown reports, Shiny apps, and package development.

## When to Use

- When handling tabular data with data frames, such as cleaning and transforming datasets.
- For creating visualizations with ggplot2, like scatter plots or histograms.
- In statistical modeling scenarios, e.g., linear regression on datasets.
- Building interactive apps with Shiny or generating reports via RMarkdown.
- Developing or extending R packages for custom data science workflows.

## Key Capabilities

- Manipulate data frames using tidyverse functions (e.g., dplyr for filtering and mutating).
- Generate plots with ggplot2, including layers, themes, and faceting.
- Perform statistical modeling with base R or packages like lm() for regression.
- Create RMarkdown documents for reproducible reports, including code chunks and outputs.
- Develop Shiny apps for interactive dashboards and package development using devtools.
- Integrate with data science pipelines, such as reading from CSV or connecting to databases.

## Usage Patterns

Always prefix R code with the skill ID "coding-r" in agent commands, e.g., "Use coding-r to load and plot data". Invoke via code blocks in responses, ensuring scripts are self-contained. For multi-step tasks, break into functions: first load libraries, then process data, and finally output results. Use R scripts (.R files) for complex workflows, calling them with `source("script.R")`. If environment variables are needed (e.g., for API keys in packages), set them like `Sys.setenv(API_KEY = "$MY_API_KEY")` before running code.

## Common Commands/API

- Load tidyverse: `library(tidyverse)` followed by `df <- read_csv("data.csv") %>% filter(column > 10)`.
- Create a ggplot: `library(ggplot2); ggplot(df, aes(x=var1, y=var2)) + geom_point() + theme_minimal()`.
- Statistical modeling: `model <- lm(y ~ x, data=df); summary(model)`.
- RMarkdown basics: Start with `--- title: "Report" output: html_document ---` in a .Rmd file, then add code chunks like ````{r} print(summary(df)) ````.
- Shiny app skeleton: `library(shiny); ui <- fluidPage(); server <- function(input, output) {}; shinyApp(ui, server)`.
- Package development: Use `devtools::create("mypackage")` to initialize, then add functions in R/ folder.

## Integration Notes

Integrate R code into larger workflows by embedding in Python via rpy2 (e.g., `import rpy2.robjects as robjects; robjects.r('library(tidyverse)')`), or use reticulate for Python-R bridging. For web services, deploy Shiny apps on Shiny Server or shinyapps.io, configuring with environment variables like `$SHINY_API_KEY` for authentication. Use config files (e.g., YAML) for parameters: create a `config.yml` with `api_key: $MY_API_KEY`, then read in R with `yaml::yaml.load_file("config.yml")`. Ensure R version compatibility (e.g., >=4.0) and install dependencies via `install.packages(c("tidyverse", "ggplot2"))` before execution.

## Error Handling

Use tryCatch() for robust code: `tryCatch({ result <- lm(y ~ x, data=df) }, error = function(e) print(paste("Error:", e)))`. Check for missing packages with `if (!require(tidyverse)) install.packages("tidyverse")`. Handle data issues like NA values with `df <- df %>% drop_na()` before operations. For Shiny, debug with `shiny::runApp(launch.browser=TRUE)` and log errors via `options(shiny.error = recover)`. Always validate inputs, e.g., `if (is.null(df)) stop("Data frame is missing")`. If API calls fail (e.g., in httr package), retry with `httr::RETRY("GET", url, times=3)`.

## Concrete Usage Examples

1. **Data Analysis and Plotting**: To analyze a CSV file and create a scatter plot, use: `library(tidyverse); library(ggplot2); df <- read_csv("data.csv"); ggplot(df, aes(x=age, y=income)) + geom_point() + labs(title="Age vs Income")`. This loads data, filters if needed, and outputs the plot.

2. **Statistical Modeling in RMarkdown**: For a regression report, create an RMarkdown file: `--- output: html_document --- # Analysis ````{r} library(tidyverse); model <- lm(sales ~ advertising, data=df); summary(model) ````. Render with `rmarkdown::render("report.Rmd")` to generate an HTML output with results.

## Graph Relationships

- Related to: ID: coding-python (shares data science cluster for integrated workflows)
- Related to: ID: coding-julia (overlaps in statistical modeling and data analysis)
- Connected via tags: "statistics" with other skills like data-analysis, and "coding" cluster for general programming tools
