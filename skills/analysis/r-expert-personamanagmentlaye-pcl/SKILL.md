---
name: r-expert
version: 1.0.0
description: Expert-level R statistical computing, data analysis, and visualization
category: languages
tags: [r, statistics, data-analysis, ggplot2, tidyverse]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash(R:*, Rscript:*)
---

# R Statistical Computing Expert

Expert guidance for R programming, statistical analysis, data visualization, and data science.

## Core Concepts

### R Fundamentals
- Vectors and data frames
- Factors and lists
- Functions and apply family
- Packages and libraries
- R Markdown
- Tidyverse ecosystem

### Statistical Analysis
- Descriptive statistics
- Hypothesis testing
- Regression analysis
- ANOVA
- Time series analysis
- Machine learning

### Data Visualization
- ggplot2
- Base R graphics
- Interactive plots (plotly)
- Statistical charts
- Maps and spatial data

## R Basics

```r
# Vectors
numbers <- c(1, 2, 3, 4, 5)
names <- c("Alice", "Bob", "Charlie")

# Data frames
df <- data.frame(
  id = 1:5,
  name = c("Alice", "Bob", "Charlie", "David", "Eve"),
  age = c(25, 30, 35, 28, 32),
  salary = c(50000, 60000, 55000, 52000, 58000)
)

# Subsetting
df[df$age > 30, ]  # Rows where age > 30
df[, c("name", "age")]  # Select columns

# Functions
calculate_mean <- function(x) {
  sum(x) / length(x)
}

# Apply family
sapply(df$age, function(x) x * 2)
lapply(list(1:5, 6:10), sum)

# Control structures
if (mean(df$age) > 30) {
  print("Average age is above 30")
} else {
  print("Average age is 30 or below")
}

# Loops
for (i in 1:nrow(df)) {
  print(df$name[i])
}
```

## Tidyverse

```r
library(dplyr)
library(tidyr)
library(stringr)

# dplyr operations
df %>%
  filter(age > 28) %>%
  select(name, age, salary) %>%
  mutate(
    salary_bonus = salary * 1.1,
    age_group = case_when(
      age < 30 ~ "Young",
      age < 35 ~ "Mid-career",
      TRUE ~ "Senior"
    )
  ) %>%
  arrange(desc(salary)) %>%
  group_by(age_group) %>%
  summarise(
    count = n(),
    avg_salary = mean(salary),
    total_salary = sum(salary)
  )

# Reshaping data
wide_data <- data.frame(
  id = 1:3,
  year_2021 = c(100, 200, 150),
  year_2022 = c(120, 210, 160)
)

# Wide to long
long_data <- wide_data %>%
  pivot_longer(
    cols = starts_with("year"),
    names_to = "year",
    values_to = "value",
    names_prefix = "year_"
  )

# Long to wide
wide_again <- long_data %>%
  pivot_wider(
    names_from = year,
    values_from = value,
    names_prefix = "year_"
  )

# String operations
df %>%
  mutate(
    name_upper = str_to_upper(name),
    name_length = str_length(name),
    first_letter = str_sub(name, 1, 1)
  )

# Joining data
df1 <- data.frame(id = 1:3, value1 = c("A", "B", "C"))
df2 <- data.frame(id = 2:4, value2 = c("X", "Y", "Z"))

inner_join(df1, df2, by = "id")
left_join(df1, df2, by = "id")
full_join(df1, df2, by = "id")
```

## ggplot2 Visualization

```r
library(ggplot2)

# Basic scatter plot
ggplot(df, aes(x = age, y = salary)) +
  geom_point(size = 3, color = "blue") +
  geom_smooth(method = "lm", se = TRUE) +
  labs(
    title = "Age vs Salary",
    x = "Age (years)",
    y = "Salary ($)"
  ) +
  theme_minimal()

# Bar plot with facets
ggplot(df, aes(x = name, y = salary, fill = age_group)) +
  geom_col() +
  facet_wrap(~ age_group) +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

# Box plot
ggplot(df, aes(x = age_group, y = salary)) +
  geom_boxplot(fill = "lightblue") +
  geom_jitter(width = 0.2, alpha = 0.5)

# Histogram with density
ggplot(df, aes(x = salary)) +
  geom_histogram(aes(y = ..density..), bins = 10, fill = "steelblue") +
  geom_density(color = "red", size = 1)

# Time series
ggplot(time_series_df, aes(x = date, y = value)) +
  geom_line(color = "darkgreen") +
  geom_point() +
  scale_x_date(date_breaks = "1 month", date_labels = "%b %Y") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))
```

## Statistical Analysis

```r
# Descriptive statistics
summary(df)
mean(df$age)
median(df$salary)
sd(df$age)
var(df$salary)
quantile(df$age, probs = c(0.25, 0.5, 0.75))

# Correlation
cor(df$age, df$salary)
cor.test(df$age, df$salary)

# T-test
t.test(df$salary ~ df$gender)

# ANOVA
model <- aov(salary ~ age_group, data = df)
summary(model)
TukeyHSD(model)

# Linear regression
lm_model <- lm(salary ~ age + experience, data = df)
summary(lm_model)

# Predictions
new_data <- data.frame(age = c(30, 35), experience = c(5, 8))
predict(lm_model, new_data, interval = "confidence")

# Multiple regression
multi_model <- lm(salary ~ age + experience + education, data = df)
summary(multi_model)

# Check assumptions
par(mfrow = c(2, 2))
plot(multi_model)

# Logistic regression
logit_model <- glm(outcome ~ age + salary,
                   data = df,
                   family = binomial(link = "logit"))
summary(logit_model)
```

## Time Series Analysis

```r
library(forecast)

# Create time series
ts_data <- ts(data, start = c(2020, 1), frequency = 12)

# Decomposition
decomposed <- decompose(ts_data)
plot(decomposed)

# ARIMA model
auto_arima <- auto.arima(ts_data)
summary(auto_arima)

# Forecasting
forecast_result <- forecast(auto_arima, h = 12)
plot(forecast_result)

# Accuracy metrics
accuracy(forecast_result)
```

## Machine Learning

```r
library(caret)
library(randomForest)

# Split data
set.seed(123)
train_index <- createDataPartition(df$outcome, p = 0.8, list = FALSE)
train_data <- df[train_index, ]
test_data <- df[-train_index, ]

# Train model
rf_model <- randomForest(
  outcome ~ .,
  data = train_data,
  ntree = 500,
  importance = TRUE
)

# Predictions
predictions <- predict(rf_model, test_data)

# Confusion matrix
confusionMatrix(predictions, test_data$outcome)

# Feature importance
importance(rf_model)
varImpPlot(rf_model)

# Cross-validation
train_control <- trainControl(
  method = "cv",
  number = 10,
  savePredictions = TRUE
)

cv_model <- train(
  outcome ~ .,
  data = train_data,
  method = "rf",
  trControl = train_control
)

print(cv_model)
```

## R Markdown

```r
---
title: "Analysis Report"
author: "Data Scientist"
date: "`r Sys.Date()`"
output:
  html_document:
    toc: true
    toc_float: true
    code_folding: hide
---

## Introduction

This analysis explores the relationship between variables.

```{r setup, include=FALSE}
knitr::opts_chunk$set(echo = TRUE, message = FALSE, warning = FALSE)
library(tidyverse)
```

## Data Loading

```{r load-data}
df <- read.csv("data.csv")
head(df)
```

## Visualization

```{r plot, fig.width=8, fig.height=6}
ggplot(df, aes(x = x, y = y)) +
  geom_point() +
  theme_minimal()
```

## Results

The analysis shows that `r cor(df$x, df$y)` correlation.
```

## Data Import/Export

```r
# CSV
df <- read.csv("data.csv")
write.csv(df, "output.csv", row.names = FALSE)

# Excel
library(readxl)
library(writexl)
df <- read_excel("data.xlsx", sheet = "Sheet1")
write_xlsx(df, "output.xlsx")

# JSON
library(jsonlite)
df <- fromJSON("data.json")
write_json(df, "output.json")

# Database
library(DBI)
library(RSQLite)
con <- dbConnect(SQLite(), "database.db")
df <- dbReadTable(con, "table_name")
dbWriteTable(con, "new_table", df)
dbDisconnect(con)

# Web APIs
library(httr)
response <- GET("https://api.example.com/data")
data <- content(response, as = "parsed")
```

## Best Practices

### Code Style
- Use <- for assignment
- Follow tidyverse style guide
- Write functions for repeated code
- Use meaningful variable names
- Comment complex operations
- Use %>% pipe for readability

### Data Analysis
- Always explore data first
- Check for missing values
- Validate assumptions
- Use visualization
- Document your analysis
- Make analysis reproducible

### Performance
- Vectorize operations
- Use data.table for large data
- Avoid growing objects in loops
- Profile code with Rprof()
- Use parallel processing
- Cache expensive computations

## Anti-Patterns

❌ Growing vectors in loops
❌ Not setting random seed
❌ Ignoring NA values
❌ Using attach()
❌ Not documenting code
❌ Hardcoding file paths
❌ Not checking assumptions

## Resources

- R Documentation: https://www.r-project.org/
- Tidyverse: https://www.tidyverse.org/
- ggplot2: https://ggplot2.tidyverse.org/
- R for Data Science (book): https://r4ds.had.co.nz/
- CRAN Task Views: https://cran.r-project.org/web/views/
