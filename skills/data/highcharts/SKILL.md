---
name: highcharts
version: 1.0.0
description: Create enterprise-grade interactive charts with Highcharts
author: workspace-hub
category: data-visualization
tags: [charts, highcharts, enterprise, stock, maps, accessibility]
platforms: [web, javascript, typescript]
---

# Highcharts Enterprise Charting Skill

Create professional, enterprise-grade interactive charts with Highcharts - trusted by Fortune 500 companies worldwide.

## When to Use This Skill

Use Highcharts when you need:
- **Enterprise features** - Stock charts, Gantt charts, network diagrams
- **Accessibility** - WCAG compliant, screen reader support
- **Financial charts** - Advanced stock/trading visualizations
- **Professional quality** - Polished, production-ready charts
- **Export capabilities** - PDF, PNG, SVG, Excel exports built-in
- **Commercial support** - Professional licensing and support available

**License Note:** Highcharts is free for non-commercial use. Commercial use requires a license.

**Avoid when:**
- Budget constraints (use Chart.js or ECharts)
- Maximum customization needed (use D3.js)
- Only need basic charts (use Chart.js)

## Core Capabilities

### 1. Basic Line Chart
```html
<!DOCTYPE html>
<html>
<head>
  <script src="https://code.highcharts.com/highcharts.js"></script>
</head>
<body>
  <div id="container" style="width: 100%; height: 400px;"></div>
  <script>
    Highcharts.chart('container', {
      title: {
        text: 'Monthly Sales'
      },
      subtitle: {
        text: 'Source: Sales Department'
      },
      xAxis: {
        categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
      },
      yAxis: {
        title: {
          text: 'Sales (units)'
        }
      },
      series: [{
        name: 'Product A',
        data: [29.9, 71.5, 106.4, 129.2, 144.0, 176.0]
      }],
      credits: {
        enabled: false
      }
    });
  </script>
</body>
</html>
```

### 2. Column Chart with Multiple Series
```javascript
Highcharts.chart('container', {
  chart: {
    type: 'column'
  },
  title: {
    text: 'Quarterly Revenue Comparison'
  },
  xAxis: {
    categories: ['Q1', 'Q2', 'Q3', 'Q4']
  },
  yAxis: {
    min: 0,
    title: {
      text: 'Revenue (thousands)'
    }
  },
  tooltip: {
    headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
    pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
      '<td style="padding:0"><b>{point.y:.1f}</b></td></tr>',
    footerFormat: '</table>',
    shared: true,
    useHTML: true
  },
  plotOptions: {
    column: {
      pointPadding: 0.2,
      borderWidth: 0
    }
  },
  series: [{
    name: '2023',
    data: [49.9, 71.5, 106.4, 129.2]
  }, {
    name: '2024',
    data: [83.6, 78.8, 98.5, 93.4]
  }]
});
```

### 3. Pie Chart with Drilldown
```javascript
Highcharts.chart('container', {
  chart: {
    type: 'pie'
  },
  title: {
    text: 'Browser Market Share'
  },
  tooltip: {
    pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
  },
  accessibility: {
    point: {
      valueSuffix: '%'
    }
  },
  plotOptions: {
    pie: {
      allowPointSelect: true,
      cursor: 'pointer',
      dataLabels: {
        enabled: true,
        format: '<b>{point.name}</b>: {point.percentage:.1f} %'
      },
      showInLegend: true
    }
  },
  series: [{
    name: 'Share',
    colorByPoint: true,
    data: [{
      name: 'Chrome',
      y: 61.41,
      sliced: true,
      selected: true
    }, {
      name: 'Firefox',
      y: 11.84
    }, {
      name: 'Edge',
      y: 4.67
    }, {
      name: 'Safari',
      y: 4.18
    }, {
      name: 'Other',
      y: 17.9
    }]
  }]
});
```

## Complete Examples

### Example 1: Stock Chart with Time Series
```html
<script src="https://code.highcharts.com/stock/highstock.js"></script>
<div id="container"></div>

<script>
// Load stock data from CSV
fetch('../data/stock_prices.csv')
  .then(response => response.text())
  .then(csvText => {
    const lines = csvText.split('\n');
    const data = [];

    for (let i = 1; i < lines.length; i++) {
      const row = lines[i].split(',');
      if (row.length >= 2) {
        const date = new Date(row[0]).getTime();
        const price = parseFloat(row[1]);
        data.push([date, price]);
      }
    }

    Highcharts.stockChart('container', {
      rangeSelector: {
        selected: 1
      },
      title: {
        text: 'Stock Price History'
      },
      series: [{
        name: 'Price',
        data: data,
        tooltip: {
          valueDecimals: 2
        }
      }],
      navigator: {
        enabled: true
      },
      scrollbar: {
        enabled: true
      }
    });
  });
</script>
```

### Example 2: Combination Chart (Column + Line)
```javascript
Highcharts.chart('container', {
  title: {
    text: 'Sales vs Profit Margin'
  },
  xAxis: {
    categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
  },
  yAxis: [{
    title: {
      text: 'Sales'
    }
  }, {
    title: {
      text: 'Profit Margin (%)'
    },
    opposite: true
  }],
  tooltip: {
    shared: true
  },
  series: [{
    type: 'column',
    name: 'Sales',
    data: [49.9, 71.5, 106.4, 129.2, 144.0, 176.0]
  }, {
    type: 'spline',
    name: 'Profit Margin',
    yAxis: 1,
    data: [15.2, 16.8, 18.9, 19.3, 20.1, 21.4],
    marker: {
      enabled: true
    },
    dashStyle: 'shortdot'
  }]
});
```

### Example 3: Heatmap
```javascript
Highcharts.chart('container', {
  chart: {
    type: 'heatmap'
  },
  title: {
    text: 'Sales per employee per weekday'
  },
  xAxis: {
    categories: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
  },
  yAxis: {
    categories: ['Employee 1', 'Employee 2', 'Employee 3', 'Employee 4', 'Employee 5'],
    title: null
  },
  colorAxis: {
    min: 0,
    minColor: '#FFFFFF',
    maxColor: Highcharts.getOptions().colors[0]
  },
  legend: {
    align: 'right',
    layout: 'vertical',
    margin: 0,
    verticalAlign: 'top',
    y: 25,
    symbolHeight: 280
  },
  tooltip: {
    formatter: function () {
      return '<b>' + this.series.yAxis.categories[this.point.y] + '</b> sold <br><b>' +
        this.point.value + '</b> items on <br><b>' + this.series.xAxis.categories[this.point.x] + '</b>';
    }
  },
  series: [{
    name: 'Sales per employee',
    borderWidth: 1,
    data: [[0, 0, 10], [0, 1, 19], [0, 2, 8], [0, 3, 24], [0, 4, 67],
           [1, 0, 92], [1, 1, 58], [1, 2, 78], [1, 3, 117], [1, 4, 48],
           [2, 0, 35], [2, 1, 15], [2, 2, 123], [2, 3, 64], [2, 4, 52],
           [3, 0, 72], [3, 1, 132], [3, 2, 114], [3, 3, 19], [3, 4, 16],
           [4, 0, 38], [4, 1, 5], [4, 2, 8], [4, 3, 117], [4, 4, 115]],
    dataLabels: {
      enabled: true,
      color: '#000000'
    }
  }]
});
```

### Example 4: Gantt Chart
```html
<script src="https://code.highcharts.com/gantt/highcharts-gantt.js"></script>
<div id="container"></div>

<script>
Highcharts.ganttChart('container', {
  title: {
    text: 'Project Timeline'
  },
  xAxis: {
    min: Date.UTC(2024, 0, 1),
    max: Date.UTC(2024, 11, 31)
  },
  series: [{
    name: 'Project Tasks',
    data: [{
      name: 'Planning',
      start: Date.UTC(2024, 0, 1),
      end: Date.UTC(2024, 1, 15),
      completed: 1
    }, {
      name: 'Development',
      start: Date.UTC(2024, 1, 15),
      end: Date.UTC(2024, 7, 1),
      completed: 0.65,
      dependency: 'Planning'
    }, {
      name: 'Testing',
      start: Date.UTC(2024, 6, 1),
      end: Date.UTC(2024, 9, 1),
      completed: 0.3,
      dependency: 'Development'
    }, {
      name: 'Deployment',
      start: Date.UTC(2024, 9, 1),
      end: Date.UTC(2024, 10, 15),
      completed: 0,
      dependency: 'Testing'
    }]
  }]
});
</script>
```

### Example 5: 3D Chart
```html
<script src="https://code.highcharts.com/highcharts.js"></script>
<script src="https://code.highcharts.com/highcharts-3d.js"></script>
<div id="container"></div>

<script>
Highcharts.chart('container', {
  chart: {
    type: 'column',
    options3d: {
      enabled: true,
      alpha: 15,
      beta: 15,
      depth: 50,
      viewDistance: 25
    }
  },
  title: {
    text: '3D Column Chart'
  },
  xAxis: {
    categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May']
  },
  yAxis: {
    title: {
      text: 'Sales'
    }
  },
  plotOptions: {
    column: {
      depth: 25
    }
  },
  series: [{
    name: 'Sales',
    data: [29.9, 71.5, 106.4, 129.2, 144.0]
  }]
});
</script>
```

### Example 6: Live Updating Chart
```javascript
Highcharts.chart('container', {
  chart: {
    type: 'spline',
    animation: Highcharts.svg,
    marginRight: 10,
    events: {
      load: function () {
        var series = this.series[0];
        setInterval(function () {
          var x = (new Date()).getTime(),
              y = Math.random() * 100;
          series.addPoint([x, y], true, true);
        }, 1000);
      }
    }
  },
  time: {
    useUTC: false
  },
  title: {
    text: 'Live Random Data'
  },
  xAxis: {
    type: 'datetime',
    tickPixelInterval: 150
  },
  yAxis: {
    title: {
      text: 'Value'
    },
    plotLines: [{
      value: 0,
      width: 1,
      color: '#808080'
    }]
  },
  tooltip: {
    headerFormat: '<b>{series.name}</b><br/>',
    pointFormat: '{point.x:%Y-%m-%d %H:%M:%S}<br/>{point.y:.2f}'
  },
  legend: {
    enabled: false
  },
  exporting: {
    enabled: false
  },
  series: [{
    name: 'Random data',
    data: (function () {
      var data = [],
          time = (new Date()).getTime(),
          i;

      for (i = -19; i <= 0; i += 1) {
        data.push({
          x: time + i * 1000,
          y: Math.random() * 100
        });
      }
      return data;
    }())
  }]
});
```

## Best Practices

### 1. Enable Accessibility
```javascript
Highcharts.chart('container', {
  accessibility: {
    enabled: true,
    description: 'Chart showing sales trends over time',
    keyboardNavigation: {
      enabled: true
    }
  },
  // ... rest of config
});
```

### 2. Customize Tooltips
```javascript
tooltip: {
  formatter: function () {
    return '<b>' + this.series.name + '</b><br/>' +
           this.x + ': ' + this.y.toFixed(2);
  }
}
```

### 3. Use Responsive Options
```javascript
Highcharts.chart('container', {
  chart: {
    height: (9 / 16 * 100) + '%' // 16:9 ratio
  },
  responsive: {
    rules: [{
      condition: {
        maxWidth: 500
      },
      chartOptions: {
        legend: {
          align: 'center',
          verticalAlign: 'bottom',
          layout: 'horizontal'
        },
        yAxis: {
          labels: {
            align: 'left',
            x: 0,
            y: -5
          },
          title: {
            text: null
          }
        }
      }
    }]
  }
});
```

### 4. Export Functionality
```javascript
exporting: {
  enabled: true,
  buttons: {
    contextButton: {
      menuItems: [
        'downloadPNG',
        'downloadJPEG',
        'downloadPDF',
        'downloadSVG',
        'separator',
        'downloadCSV',
        'downloadXLS'
      ]
    }
  }
}
```

## Chart Types Available

### Basic Charts
- Line, Spline, Area, Column, Bar, Pie, Scatter

### Advanced Charts
- Stock charts, Gantt charts, Heatmap, Treemap, Network graphs

### Financial Charts
- Candlestick, OHLC, Flags

### Statistical Charts
- Box plot, Error bars, Histogram, Bell curve

### 3D Charts
- 3D Column, 3D Pie, 3D Scatter

### Maps
- Map chart, Mapbubble, Mapline, Tilemap

## Installation

### CDN
```html
<!-- Basic Highcharts -->
<script src="https://code.highcharts.com/highcharts.js"></script>

<!-- Stock Charts -->
<script src="https://code.highcharts.com/stock/highstock.js"></script>

<!-- Maps -->
<script src="https://code.highcharts.com/maps/highmaps.js"></script>

<!-- Gantt -->
<script src="https://code.highcharts.com/gantt/highcharts-gantt.js"></script>

<!-- Additional modules -->
<script src="https://code.highcharts.com/modules/exporting.js"></script>
<script src="https://code.highcharts.com/modules/export-data.js"></script>
<script src="https://code.highcharts.com/modules/accessibility.js"></script>
```

### NPM
```bash
npm install highcharts
```

```javascript
import Highcharts from 'highcharts';
import HighchartsStock from 'highcharts/modules/stock';
import HighchartsMap from 'highcharts/modules/map';

HighchartsStock(Highcharts);
HighchartsMap(Highcharts);
```

## TypeScript Support

```typescript
import * as Highcharts from 'highcharts';

const options: Highcharts.Options = {
  title: {
    text: 'TypeScript Example'
  },
  series: [{
    type: 'line',
    data: [1, 2, 3, 4, 5]
  }]
};

Highcharts.chart('container', options);
```

## Advanced Features

### Boost Module (Large Datasets)
```html
<script src="https://code.highcharts.com/modules/boost.js"></script>

<script>
Highcharts.chart('container', {
  boost: {
    useGPUTranslations: true,
    usePreAllocated: true
  },
  series: [{
    boostThreshold: 1, // Start boosting at 1 point
    data: largeDataArray // 100,000+ points
  }]
});
</script>
```

### Annotations
```javascript
annotations: [{
  labels: [{
    point: {
      x: 3,
      y: 50,
      xAxis: 0,
      yAxis: 0
    },
    text: 'Important milestone'
  }],
  labelOptions: {
    backgroundColor: 'rgba(255,255,255,0.5)',
    borderColor: 'silver'
  }
}]
```

### Drill-down
```html
<script src="https://code.highcharts.com/modules/drilldown.js"></script>

<script>
Highcharts.chart('container', {
  series: [{
    data: [{
      name: 'Category A',
      y: 5,
      drilldown: 'category-a'
    }]
  }],
  drilldown: {
    series: [{
      id: 'category-a',
      data: [
        ['Subcategory 1', 2],
        ['Subcategory 2', 3]
      ]
    }]
  }
});
</script>
```

## Theming

```javascript
// Apply custom theme
Highcharts.setOptions({
  colors: ['#058DC7', '#50B432', '#ED561B', '#DDDF00'],
  chart: {
    backgroundColor: '#f4f4f4',
    style: {
      fontFamily: 'Arial, sans-serif'
    }
  },
  title: {
    style: {
      color: '#000',
      font: 'bold 16px Arial'
    }
  }
});
```

## Integration Examples

### With React
```jsx
import { useEffect, useRef } from 'react';
import Highcharts from 'highcharts';

function HighchartsComponent({ options }) {
  const chartRef = useRef(null);

  useEffect(() => {
    const chart = Highcharts.chart(chartRef.current, options);

    return () => {
      chart.destroy();
    };
  }, [options]);

  return <div ref={chartRef} />;
}
```

### With Vue
```vue
<template>
  <div ref="chartContainer"></div>
</template>

<script>
import Highcharts from 'highcharts';

export default {
  props: ['options'],
  mounted() {
    this.chart = Highcharts.chart(this.$refs.chartContainer, this.options);
  },
  beforeUnmount() {
    if (this.chart) {
      this.chart.destroy();
    }
  },
  watch: {
    options: {
      deep: true,
      handler(newOptions) {
        this.chart.update(newOptions);
      }
    }
  }
};
</script>
```

## Resources

- **Official Docs**: https://www.highcharts.com/docs/
- **API Reference**: https://api.highcharts.com/highcharts/
- **Demos**: https://www.highcharts.com/demo
- **GitHub**: https://github.com/highcharts/highcharts
- **Support**: https://www.highcharts.com/support

## Licensing

- **Free** for non-commercial/personal use
- **Commercial license** required for business use
- **OEM licenses** available for redistribution
- Visit: https://shop.highsoft.com/

## Performance Tips

1. **Use Boost module** for datasets >5k points
2. **Disable animations** for real-time updates
3. **Limit tooltip calculations**
4. **Use turboThreshold** wisely
5. **Optimize data format** (avoid objects when arrays suffice)

---

**Use this skill for enterprise-grade, professional charts with extensive features and support!**
