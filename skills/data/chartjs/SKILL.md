---
name: chartjs
version: 1.0.0
description: Create simple, responsive charts quickly with Chart.js
author: workspace-hub
category: data-visualization
tags: [charts, chartjs, simple, quick, responsive, canvas]
platforms: [web, javascript]
---

# Chart.js Quick Charting Skill

Create beautiful, responsive charts in minutes with Chart.js - the simple yet flexible JavaScript charting library.

## When to Use This Skill

Use Chart.js when you need:
- **Quick implementation** - Up and running in minutes
- **Simple charts** - Line, bar, pie, doughnut, radar charts
- **Minimal configuration** - Sensible defaults that work out of the box
- **Small projects** - Lightweight library (60KB gzipped)
- **Responsive charts** - Mobile-friendly by default
- **No dependencies** - Standalone library

**Avoid when:**
- Complex customization needed (use D3.js)
- 3D charts required (use Plotly)
- Advanced scientific visualizations needed (use Plotly)
- Large datasets >10k points (use Plotly with WebGL)

## Core Capabilities

### 1. Basic Line Chart
```html
<!DOCTYPE html>
<html>
<head>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
  <canvas id="myChart" width="400" height="200"></canvas>
  <script>
    const ctx = document.getElementById('myChart').getContext('2d');
    const myChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        datasets: [{
          label: 'Sales 2024',
          data: [12, 19, 3, 5, 2, 3],
          borderColor: 'rgb(75, 192, 192)',
          backgroundColor: 'rgba(75, 192, 192, 0.2)',
          tension: 0.1
        }]
      },
      options: {
        responsive: true,
        plugins: {
          title: {
            display: true,
            text: 'Monthly Sales'
          }
        }
      }
    });
  </script>
</body>
</html>
```

### 2. Bar Chart
```javascript
const ctx = document.getElementById('barChart').getContext('2d');
const barChart = new Chart(ctx, {
  type: 'bar',
  data: {
    labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
    datasets: [{
      label: 'Votes',
      data: [12, 19, 3, 5, 2, 3],
      backgroundColor: [
        'rgba(255, 99, 132, 0.6)',
        'rgba(54, 162, 235, 0.6)',
        'rgba(255, 206, 86, 0.6)',
        'rgba(75, 192, 192, 0.6)',
        'rgba(153, 102, 255, 0.6)',
        'rgba(255, 159, 64, 0.6)'
      ],
      borderColor: [
        'rgba(255, 99, 132, 1)',
        'rgba(54, 162, 235, 1)',
        'rgba(255, 206, 86, 1)',
        'rgba(75, 192, 192, 1)',
        'rgba(153, 102, 255, 1)',
        'rgba(255, 159, 64, 1)'
      ],
      borderWidth: 1
    }]
  },
  options: {
    responsive: true,
    scales: {
      y: {
        beginAtZero: true
      }
    }
  }
});
```

### 3. Pie/Doughnut Chart
```javascript
const ctx = document.getElementById('pieChart').getContext('2d');
const pieChart = new Chart(ctx, {
  type: 'pie', // or 'doughnut'
  data: {
    labels: ['Desktop', 'Mobile', 'Tablet'],
    datasets: [{
      label: 'Device Usage',
      data: [55, 35, 10],
      backgroundColor: [
        'rgb(255, 99, 132)',
        'rgb(54, 162, 235)',
        'rgb(255, 205, 86)'
      ],
      hoverOffset: 4
    }]
  },
  options: {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Device Usage Statistics'
      }
    }
  }
});
```

## Complete Examples

### Example 1: Multi-Dataset Line Chart
```html
<!DOCTYPE html>
<html>
<head>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    .chart-container {
      position: relative;
      height: 400px;
      width: 80%;
      margin: auto;
    }
  </style>
</head>
<body>
  <div class="chart-container">
    <canvas id="multiLineChart"></canvas>
  </div>
  <script>
    const ctx = document.getElementById('multiLineChart').getContext('2d');
    const chart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
        datasets: [
          {
            label: 'Product A',
            data: [30, 50, 45, 60],
            borderColor: 'rgb(255, 99, 132)',
            backgroundColor: 'rgba(255, 99, 132, 0.1)',
            tension: 0.4
          },
          {
            label: 'Product B',
            data: [20, 40, 55, 50],
            borderColor: 'rgb(54, 162, 235)',
            backgroundColor: 'rgba(54, 162, 235, 0.1)',
            tension: 0.4
          },
          {
            label: 'Product C',
            data: [40, 30, 35, 55],
            borderColor: 'rgb(75, 192, 192)',
            backgroundColor: 'rgba(75, 192, 192, 0.1)',
            tension: 0.4
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: {
          mode: 'index',
          intersect: false,
        },
        plugins: {
          title: {
            display: true,
            text: 'Product Sales Comparison'
          },
          legend: {
            display: true,
            position: 'top'
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            title: {
              display: true,
              text: 'Sales (units)'
            }
          },
          x: {
            title: {
              display: true,
              text: 'Time Period'
            }
          }
        }
      }
    });
  </script>
</body>
</html>
```

### Example 2: Stacked Bar Chart
```javascript
const ctx = document.getElementById('stackedBar').getContext('2d');
const stackedChart = new Chart(ctx, {
  type: 'bar',
  data: {
    labels: ['Q1', 'Q2', 'Q3', 'Q4'],
    datasets: [
      {
        label: 'Revenue',
        data: [100, 120, 115, 134],
        backgroundColor: 'rgba(75, 192, 192, 0.7)',
      },
      {
        label: 'Costs',
        data: [60, 70, 65, 80],
        backgroundColor: 'rgba(255, 99, 132, 0.7)',
      },
      {
        label: 'Profit',
        data: [40, 50, 50, 54],
        backgroundColor: 'rgba(54, 162, 235, 0.7)',
      }
    ]
  },
  options: {
    responsive: true,
    scales: {
      x: {
        stacked: true,
      },
      y: {
        stacked: true,
        beginAtZero: true
      }
    },
    plugins: {
      title: {
        display: true,
        text: 'Quarterly Financial Overview'
      }
    }
  }
});
```

### Example 3: Radar Chart
```javascript
const ctx = document.getElementById('radarChart').getContext('2d');
const radarChart = new Chart(ctx, {
  type: 'radar',
  data: {
    labels: ['Speed', 'Reliability', 'Comfort', 'Safety', 'Efficiency'],
    datasets: [
      {
        label: 'Vehicle A',
        data: [85, 90, 70, 95, 80],
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
        borderColor: 'rgb(255, 99, 132)',
        pointBackgroundColor: 'rgb(255, 99, 132)',
      },
      {
        label: 'Vehicle B',
        data: [75, 85, 90, 85, 90],
        backgroundColor: 'rgba(54, 162, 235, 0.2)',
        borderColor: 'rgb(54, 162, 235)',
        pointBackgroundColor: 'rgb(54, 162, 235)',
      }
    ]
  },
  options: {
    responsive: true,
    scales: {
      r: {
        beginAtZero: true,
        max: 100
      }
    },
    plugins: {
      title: {
        display: true,
        text: 'Vehicle Comparison'
      }
    }
  }
});
```

### Example 4: Loading Data from CSV
```javascript
// Using Fetch API to load CSV
fetch('../data/sales.csv')
  .then(response => response.text())
  .then(csvText => {
    const lines = csvText.split('\n');
    const headers = lines[0].split(',');

    const labels = [];
    const data = [];

    for (let i = 1; i < lines.length; i++) {
      const values = lines[i].split(',');
      labels.push(values[0]);
      data.push(parseFloat(values[1]));
    }

    const ctx = document.getElementById('csvChart').getContext('2d');
    new Chart(ctx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [{
          label: 'Sales Data',
          data: data,
          borderColor: 'rgb(75, 192, 192)',
          tension: 0.1
        }]
      },
      options: {
        responsive: true
      }
    });
  });
```

### Example 5: Real-Time Updating Chart
```javascript
const ctx = document.getElementById('realtimeChart').getContext('2d');
const chart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: [],
    datasets: [{
      label: 'Real-time Data',
      data: [],
      borderColor: 'rgb(75, 192, 192)',
      tension: 0.1
    }]
  },
  options: {
    responsive: true,
    scales: {
      x: {
        display: true
      },
      y: {
        beginAtZero: true
      }
    },
    animation: {
      duration: 0 // Disable animation for real-time
    }
  }
});

// Update every second
let dataPoint = 0;
setInterval(() => {
  const now = new Date();
  const timeLabel = now.getHours() + ':' + now.getMinutes() + ':' + now.getSeconds();

  chart.data.labels.push(timeLabel);
  chart.data.datasets[0].data.push(Math.random() * 100);

  // Keep only last 20 points
  if (chart.data.labels.length > 20) {
    chart.data.labels.shift();
    chart.data.datasets[0].data.shift();
  }

  chart.update();
}, 1000);
```

### Example 6: Mixed Chart Types
```javascript
const ctx = document.getElementById('mixedChart').getContext('2d');
const mixedChart = new Chart(ctx, {
  data: {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
    datasets: [
      {
        type: 'bar',
        label: 'Sales',
        data: [50, 60, 70, 80, 90],
        backgroundColor: 'rgba(54, 162, 235, 0.7)',
      },
      {
        type: 'line',
        label: 'Target',
        data: [55, 65, 75, 85, 95],
        borderColor: 'rgb(255, 99, 132)',
        fill: false
      }
    ]
  },
  options: {
    responsive: true,
    plugins: {
      title: {
        display: true,
        text: 'Sales vs Target'
      }
    }
  }
});
```

## Best Practices

### 1. Use Responsive Containers
```html
<div style="position: relative; height: 400px; width: 100%;">
  <canvas id="myChart"></canvas>
</div>
```

```javascript
options: {
  responsive: true,
  maintainAspectRatio: false
}
```

### 2. Destroy Charts Before Recreating
```javascript
let myChart;

function createChart(data) {
  // Destroy existing chart
  if (myChart) {
    myChart.destroy();
  }

  const ctx = document.getElementById('myChart').getContext('2d');
  myChart = new Chart(ctx, {
    type: 'line',
    data: data
  });
}
```

### 3. Use Plugins for Extended Functionality
```javascript
// Example: Chart.js Data Labels Plugin
import ChartDataLabels from 'chartjs-plugin-datalabels';

const chart = new Chart(ctx, {
  plugins: [ChartDataLabels],
  data: {...},
  options: {
    plugins: {
      datalabels: {
        color: '#fff',
        display: true
      }
    }
  }
});
```

### 4. Optimize for Performance
```javascript
options: {
  // Disable animations for large datasets
  animation: {
    duration: 0
  },
  // Use decimation for large datasets
  parsing: false,
  normalized: true
}
```

## Available Chart Types

1. **Line** - Trend analysis, time series
2. **Bar** - Comparisons, categorical data
3. **Pie** - Proportions, percentages
4. **Doughnut** - Like pie, with center hole
5. **Radar** - Multivariate data
6. **Polar Area** - Similar to pie with variable radii
7. **Bubble** - 3-dimensional data (x, y, size)
8. **Scatter** - Correlation analysis

## Common Customizations

### Custom Colors
```javascript
const colors = [
  'rgba(255, 99, 132, 0.7)',
  'rgba(54, 162, 235, 0.7)',
  'rgba(255, 206, 86, 0.7)',
  'rgba(75, 192, 192, 0.7)',
  'rgba(153, 102, 255, 0.7)'
];
```

### Custom Tooltips
```javascript
options: {
  plugins: {
    tooltip: {
      callbacks: {
        label: function(context) {
          let label = context.dataset.label || '';
          if (label) {
            label += ': ';
          }
          label += '$' + context.parsed.y.toFixed(2);
          return label;
        }
      }
    }
  }
}
```

### Custom Legends
```javascript
options: {
  plugins: {
    legend: {
      position: 'bottom',
      labels: {
        font: {
          size: 14
        },
        usePointStyle: true
      }
    }
  }
}
```

## Installation

### CDN (Quick Start)
```html
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
```

### NPM
```bash
npm install chart.js
```

```javascript
import Chart from 'chart.js/auto';
```

### ES Modules
```html
<script type="module">
  import Chart from 'https://cdn.jsdelivr.net/npm/chart.js@4/+esm';

  const ctx = document.getElementById('myChart');
  new Chart(ctx, {...});
</script>
```

## Popular Plugins

### Chart.js Zoom Plugin
```bash
npm install chartjs-plugin-zoom
```

```javascript
import zoomPlugin from 'chartjs-plugin-zoom';
Chart.register(zoomPlugin);

options: {
  plugins: {
    zoom: {
      zoom: {
        wheel: { enabled: true },
        pinch: { enabled: true },
        mode: 'xy'
      }
    }
  }
}
```

### Chart.js Annotation Plugin
```bash
npm install chartjs-plugin-annotation
```

### Chart.js Data Labels
```bash
npm install chartjs-plugin-datalabels
```

## Integration Examples

### With React
```javascript
import { useEffect, useRef } from 'react';
import Chart from 'chart.js/auto';

function ChartComponent({ data }) {
  const chartRef = useRef(null);
  const chartInstance = useRef(null);

  useEffect(() => {
    if (chartInstance.current) {
      chartInstance.current.destroy();
    }

    const ctx = chartRef.current.getContext('2d');
    chartInstance.current = new Chart(ctx, {
      type: 'line',
      data: data,
      options: { responsive: true }
    });

    return () => {
      if (chartInstance.current) {
        chartInstance.current.destroy();
      }
    };
  }, [data]);

  return <canvas ref={chartRef} />;
}
```

### With Vue
```vue
<template>
  <canvas ref="chartCanvas"></canvas>
</template>

<script>
import Chart from 'chart.js/auto';

export default {
  props: ['chartData'],
  mounted() {
    this.renderChart();
  },
  methods: {
    renderChart() {
      const ctx = this.$refs.chartCanvas.getContext('2d');
      new Chart(ctx, {
        type: 'bar',
        data: this.chartData,
        options: { responsive: true }
      });
    }
  }
};
</script>
```

## Resources

- **Official Docs**: https://www.chartjs.org/docs/latest/
- **Samples**: https://www.chartjs.org/docs/latest/samples/
- **GitHub**: https://github.com/chartjs/Chart.js
- **Community**: https://github.com/chartjs/awesome

## Performance Tips

1. **Disable animations** for large datasets
2. **Use decimation** to reduce data points
3. **Limit updates** - batch chart updates
4. **Destroy unused charts** - free memory
5. **Use canvas size wisely** - larger canvas = slower rendering

---

**Use this skill for quick, simple charts that look great with minimal configuration!**
