---
name: matlab-performance-optimizer
description: Optimize MATLAB code for better performance through vectorization, memory management, and profiling. Use when user requests optimization, mentions slow code, performance issues, speed improvements, or asks to make code faster or more efficient.
license: MathWorks BSD-3-Clause (see LICENSE)
---

# MATLAB Performance Optimizer

This skill provides comprehensive guidelines for optimizing MATLAB code performance. Apply vectorization techniques, memory optimization strategies, and profiling tools to make code faster and more efficient.

## When to Use This Skill

- Optimizing slow or inefficient MATLAB code
- Converting loops to vectorized operations
- Reducing memory usage
- Improving algorithm performance
- When user mentions: slow, performance, optimize, speed up, efficient, memory
- Profiling code to find bottlenecks
- Parallelizing computations

## Core Optimization Principles

### 1. Vectorization (Most Important)

**Replace loops with vectorized operations whenever possible.**

**SLOW - Using loops:**
```matlab
% Slow approach
n = 1000000;
result = zeros(n, 1);
for i = 1:n
    result(i) = sin(i) * cos(i);
end
```

**FAST - Vectorized:**
```matlab
% Fast approach
n = 1000000;
i = 1:n;
result = sin(i) .* cos(i);
```

### 2. Preallocate Arrays

**Always preallocate arrays before loops.**

**SLOW - Growing arrays:**
```matlab
% Very slow - array grows each iteration
result = [];
for i = 1:10000
    result(end+1) = i^2;
end
```

**FAST - Preallocated:**
```matlab
% Fast - preallocated array
n = 10000;
result = zeros(n, 1);
for i = 1:n
    result(i) = i^2;
end
```

### 3. Use Built-in Functions

**MATLAB built-in functions are highly optimized.**

**SLOW - Manual implementation:**
```matlab
% Slow
sum_val = 0;
for i = 1:length(x)
    sum_val = sum_val + x(i);
end
```

**FAST - Built-in function:**
```matlab
% Fast
sum_val = sum(x);
```

## Vectorization Techniques

### Element-wise Operations

Use `.*`, `./`, `.^` for element-wise operations:

```matlab
% Instead of this:
for i = 1:length(x)
    y(i) = x(i)^2 + 2*x(i) + 1;
end

% Do this:
y = x.^2 + 2*x + 1;
```

### Logical Indexing

Replace conditional loops with logical indexing:

```matlab
% Instead of this:
count = 0;
for i = 1:length(data)
    if data(i) > threshold
        count = count + 1;
        filtered(count) = data(i);
    end
end
filtered = filtered(1:count);

% Do this:
filtered = data(data > threshold);
```

### Matrix Operations

Use matrix multiplication instead of nested loops:

```matlab
% Instead of this:
C = zeros(size(A, 1), size(B, 2));
for i = 1:size(A, 1)
    for j = 1:size(B, 2)
        for k = 1:size(A, 2)
            C(i,j) = C(i,j) + A(i,k) * B(k,j);
        end
    end
end

% Do this:
C = A * B;
```

### Cumulative Operations

Use `cumsum`, `cumprod`, `cummax`, `cummin`:

```matlab
% Instead of this:
running_sum = zeros(size(data));
running_sum(1) = data(1);
for i = 2:length(data)
    running_sum(i) = running_sum(i-1) + data(i);
end

% Do this:
running_sum = cumsum(data);
```

## Memory Optimization

### Use Appropriate Data Types

```matlab
% Instead of default double (8 bytes)
data = rand(1000, 1000);  % 8 MB

% Use single precision when appropriate (4 bytes)
data = single(rand(1000, 1000));  % 4 MB

% Use integers when applicable
indices = uint32(1:1000000);  % 4 MB instead of 8 MB
```

### Sparse Matrices

For matrices with mostly zeros:

```matlab
% Dense matrix (wastes memory)
A = zeros(10000, 10000);
A(1:100, 1:100) = rand(100);  % 800 MB

% Sparse matrix (efficient)
A = sparse(10000, 10000);
A(1:100, 1:100) = rand(100);  % Only stores non-zeros
```

### Clear Unused Variables

```matlab
% Process large data
largeData = loadData();
processedData = processData(largeData);

% Clear when no longer needed
clear largeData;

% Continue with processed data
results = analyze(processedData);
```

### In-Place Operations

```matlab
% Instead of creating copies
A = A + 5;  % In-place when possible

% Avoid unnecessary copies
B = A;      % Creates copy if A is modified later
B = A + 0;  % Forces copy
```

## Profiling and Benchmarking

### Using the Profiler

```matlab
% Profile code execution
profile on
myFunction(inputs);
profile viewer
profile off
```

The profiler shows:
- Time spent in each function
- Number of calls to each function
- Lines that take the most time

### Timing Comparisons

```matlab
% Time single execution
tic;
result = myFunction(data);
elapsedTime = toc;

% Benchmark with timeit (more accurate)
timeit(@() myFunction(data))

% Compare multiple approaches
time1 = timeit(@() approach1(data));
time2 = timeit(@() approach2(data));
fprintf('Approach 1: %.6f s\nApproach 2: %.6f s\n', time1, time2);
```

## Common Optimization Patterns

### Pattern 1: Replace find with Logical Indexing

```matlab
% SLOW
indices = find(x > 5);
y = x(indices);

% FAST
y = x(x > 5);
```

### Pattern 2: Use bsxfun for Broadcasting

```matlab
% Instead of repmat
A = rand(1000, 5);
B = rand(1, 5);
C = A - repmat(B, size(A, 1), 1);

% Use implicit expansion (R2016b+) or bsxfun
C = A - B;  % Implicit expansion
C = bsxfun(@minus, A, B);  % Older MATLAB
```

### Pattern 3: Avoid Repeated Calculations

```matlab
% SLOW - recalculates each iteration
for i = 1:n
    result(i) = data(i) / sqrt(sum(data.^2));
end

% FAST - calculate once
norm_factor = sqrt(sum(data.^2));
for i = 1:n
    result(i) = data(i) / norm_factor;
end

% EVEN FASTER - vectorize
result = data / sqrt(sum(data.^2));
```

### Pattern 4: Efficient String Operations

```matlab
% SLOW - concatenating in loop
str = '';
for i = 1:1000
    str = [str, sprintf('Line %d\n', i)];
end

% FAST - cell array + join
lines = cell(1000, 1);
for i = 1:1000
    lines{i} = sprintf('Line %d', i);
end
str = strjoin(lines, '\n');

% FASTEST - vectorized sprintf
str = sprintf('Line %d\n', 1:1000);
```

### Pattern 5: Use Table for Mixed Data Types

```matlab
% Instead of separate arrays
names = cell(1000, 1);
ages = zeros(1000, 1);
scores = zeros(1000, 1);

% Use table
data = table(names, ages, scores);
% Faster access and better organization
```

## Algorithm-Specific Optimizations

### Convolution and Filtering

```matlab
% Use built-in functions
filtered = conv(signal, kernel, 'same');
filtered = filter(b, a, signal);

% For 2D
filtered = conv2(image, kernel, 'same');
filtered = imfilter(image, kernel);

% FFT-based for large kernels
filtered = ifft(fft(signal) .* fft(kernel, length(signal)));
```

### Distance Calculations

```matlab
% Instead of nested loops for pairwise distances
% SLOW
n = size(points, 1);
distances = zeros(n, n);
for i = 1:n
    for j = 1:n
        distances(i,j) = norm(points(i,:) - points(j,:));
    end
end

% FAST - vectorized
distances = pdist2(points, points);

% Or using bsxfun
diff = bsxfun(@minus, permute(points, [1 3 2]), permute(points, [3 1 2]));
distances = sqrt(sum(diff.^2, 3));
```

### Sorting and Searching

```matlab
% Presort for multiple searches
sortedData = sort(data);

% Binary search on sorted data
idx = find(sortedData >= value, 1, 'first');

% Use ismember for set operations
[isPresent, locations] = ismember(searchValues, data);

% Use unique for removing duplicates
uniqueData = unique(data);
```

## Parallel Computing

### Simple Parallel Loops (parfor)

```matlab
% Convert for to parfor for independent iterations
parfor i = 1:n
    results(i) = expensiveFunction(data(i));
end
```

**Requirements for parfor:**
- Iterations must be independent
- Loop variable must be consecutive integers
- Variables must be classified as loop, sliced, broadcast, or reduction

### Parallel Array Operations

```matlab
% Create parallel pool
parpool('local', 4);  % 4 workers

% Use parallel array functions
result = arrayfun(@expensiveFunction, data, 'UniformOutput', false);

% GPU arrays for massive parallelization
gpuData = gpuArray(data);
result = arrayfun(@myFunction, gpuData);
result = gather(result);  % Bring back to CPU
```

## Advanced Optimizations

### MEX Functions for Critical Sections

Convert performance-critical code to C/C++:

```matlab
% Create MEX file for bottleneck function
% Write myFunction.c, then compile:
% mex myFunction.c

% Call like regular MATLAB function
result = myFunction(inputs);
```

### Persistent Variables for Cached Results

```matlab
function result = expensiveComputation(input)
    persistent cachedData cachedInput

    if isequal(input, cachedInput)
        % Return cached result
        result = cachedData;
        return;
    end

    % Compute and cache
    result = computeExpensiveOperation(input);
    cachedData = result;
    cachedInput = input;
end
```

### JIT Acceleration Best Practices

MATLAB's JIT (Just-In-Time) compiler optimizes:
- Simple for-loops with scalar operations
- Functions without dynamic features

**JIT-friendly code:**
```matlab
function result = jitFriendly(n)
    result = 0;
    for i = 1:n
        result = result + i;
    end
end
```

**JIT-unfriendly code (avoid):**
```matlab
function result = jitUnfriendly(n)
    result = 0;
    for i = 1:n
        eval(['x' num2str(i) ' = i;']);  % Dynamic code
    end
end
```

## Performance Checklist

Before finalizing optimized code, verify:
- [ ] Loops are vectorized where possible
- [ ] Arrays are preallocated before loops
- [ ] Built-in functions used instead of manual implementations
- [ ] Logical indexing used instead of find + indexing
- [ ] Appropriate data types used (single vs double, integers)
- [ ] Sparse matrices used for sparse data
- [ ] Repeated calculations moved outside loops
- [ ] String concatenation uses efficient methods
- [ ] Code profiled to identify actual bottlenecks
- [ ] Matrix operations used instead of element-wise loops
- [ ] Parallel computing considered for independent operations
- [ ] Memory-intensive operations optimized
- [ ] Caching implemented for repeated expensive calls

## Profiling Workflow

1. **Measure First**: Profile before optimizing
   ```matlab
   profile on
   myScript;
   profile viewer
   ```

2. **Identify Bottlenecks**: Focus on functions taking most time

3. **Optimize**: Apply appropriate techniques

4. **Measure Again**: Verify improvement
   ```matlab
   % Before
   time_before = timeit(@() myFunction(data));

   % After optimization
   time_after = timeit(@() myFunctionOptimized(data));

   fprintf('Speedup: %.2fx\n', time_before/time_after);
   ```

5. **Iterate**: Repeat for remaining bottlenecks

## Common Performance Pitfalls

### Pitfall 1: Premature Optimization
- Profile first, optimize second
- Focus on actual bottlenecks, not assumptions

### Pitfall 2: Over-vectorization
- Sometimes loops are clearer and fast enough
- Balance readability with performance

### Pitfall 3: Ignoring Memory Access Patterns
```matlab
% SLOW - column-wise access (MATLAB is column-major)
for j = 1:cols
    for i = 1:rows
        A(i,j) = process(i, j);
    end
end

% FAST - row-wise iteration, column-wise access
for i = 1:rows
    for j = 1:cols
        A(i,j) = process(i, j);
    end
end

% FASTEST - vectorized
[I, J] = ndgrid(1:rows, 1:cols);
A = process(I, J);
```

### Pitfall 4: Unnecessary Data Type Conversions
```matlab
% SLOW - repeated conversions
for i = 1:n
    x = double(data(i));
    result(i) = sin(x);
end

% FAST - convert once
x = double(data);
result = sin(x);
```

## Optimization Examples

### Example 1: Image Processing

```matlab
% SLOW
[rows, cols] = size(image);
output = zeros(rows, cols);
for i = 2:rows-1
    for j = 2:cols-1
        output(i,j) = mean(image(i-1:i+1, j-1:j+1), 'all');
    end
end

% FAST
kernel = ones(3,3) / 9;
output = conv2(image, kernel, 'same');
```

### Example 2: Statistical Analysis

```matlab
% SLOW
n = size(data, 1);
means = zeros(n, 1);
for i = 1:n
    means(i) = mean(data(i, :));
end

% FAST
means = mean(data, 2);
```

### Example 3: Time Series Processing

```matlab
% SLOW
n = length(signal);
movingAvg = zeros(size(signal));
window = 10;
for i = window:n
    movingAvg(i) = mean(signal(i-window+1:i));
end

% FAST
movingAvg = movmean(signal, window);
```

## Troubleshooting Performance

**Issue**: Code still slow after vectorization
- **Solution**: Profile to find new bottlenecks; consider algorithm complexity

**Issue**: Out of memory errors
- **Solution**: Use smaller data types, process in chunks, use sparse matrices

**Issue**: parfor slower than for loop
- **Solution**: Check if overhead outweighs benefits; ensure iterations are expensive enough

**Issue**: GPU computation slower than CPU
- **Solution**: Data transfer overhead may exceed computation time; use for large arrays

## Additional Resources

- Use `profile viewer` to analyze performance
- Use `memory` to check memory usage
- Use `doc` with: `timeit`, `tic/toc`, `parfor`, `gpuArray`, `sparse`
- Check MATLAB Performance and Memory documentation
