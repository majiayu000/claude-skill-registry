---
name: d3-visualization
description: Generate D3.js visualizations including charts, graphs, and interactive data visualizations. Use when creating data visualizations with D3.js.
---

# D3.js Visualization Skill

D3.jsを使った高度なデータ可視化を生成するスキルです。

## 概要

D3.jsで複雑で美しいデータ可視化を作成します。Chart.jsより高度なカスタマイズが可能です。

## 主な機能

- **多様なチャート**: ネットワーク図、ツリーマップ、サンキー図等
- **インタラクティブ**: ズーム、ドラッグ、ツールチップ
- **アニメーション**: スムーズなトランジション
- **地理データ**: 地図、コロプレス図
- **階層データ**: ツリー、パックレイアウト
- **時系列**: ライン、エリアチャート

## 使用方法

```
以下のデータでD3.jsネットワーク図を作成：
ノード: A, B, C, D
リンク: A-B, B-C, C-D, D-A
```

## 可視化例

### ネットワーク図（Force-Directed Graph）

```html
<!DOCTYPE html>
<html>
<head>
  <script src="https://d3js.org/d3.v7.min.js"></script>
  <style>
    .node { fill: #69b3a2; stroke: #fff; stroke-width: 2px; }
    .link { stroke: #999; stroke-opacity: 0.6; }
  </style>
</head>
<body>
  <svg id="graph" width="800" height="600"></svg>
  <script>
    const data = {
      nodes: [
        {id: "A"}, {id: "B"}, {id: "C"}, {id: "D"}
      ],
      links: [
        {source: "A", target: "B"},
        {source: "B", target: "C"},
        {source: "C", target: "D"},
        {source: "D", target: "A"}
      ]
    };

    const svg = d3.select("#graph");
    const width = +svg.attr("width");
    const height = +svg.attr("height");

    const simulation = d3.forceSimulation(data.nodes)
      .force("link", d3.forceLink(data.links).id(d => d.id))
      .force("charge", d3.forceManyBody().strength(-400))
      .force("center", d3.forceCenter(width / 2, height / 2));

    const link = svg.append("g")
      .selectAll("line")
      .data(data.links)
      .join("line")
      .attr("class", "link");

    const node = svg.append("g")
      .selectAll("circle")
      .data(data.nodes)
      .join("circle")
      .attr("class", "node")
      .attr("r", 20)
      .call(d3.drag()
        .on("start", dragstarted)
        .on("drag", dragged)
        .on("end", dragended));

    simulation.on("tick", () => {
      link
        .attr("x1", d => d.source.x)
        .attr("y1", d => d.source.y)
        .attr("x2", d => d.target.x)
        .attr("y2", d => d.target.y);

      node
        .attr("cx", d => d.x)
        .attr("cy", d => d.y);
    });

    function dragstarted(event, d) {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      d.fx = d.x;
      d.fy = d.y;
    }

    function dragged(event, d) {
      d.fx = event.x;
      d.fy = event.y;
    }

    function dragended(event, d) {
      if (!event.active) simulation.alphaTarget(0);
      d.fx = null;
      d.fy = null;
    }
  </script>
</body>
</html>
```

### ツリーマップ

```javascript
const data = {
  name: "root",
  children: [
    {name: "A", value: 100},
    {name: "B", value: 200},
    {name: "C", value: 150}
  ]
};

const width = 800;
const height = 600;

const treemap = d3.treemap()
  .size([width, height])
  .padding(2);

const root = d3.hierarchy(data)
  .sum(d => d.value);

treemap(root);

const svg = d3.select("body")
  .append("svg")
  .attr("width", width)
  .attr("height", height);

svg.selectAll("rect")
  .data(root.leaves())
  .join("rect")
  .attr("x", d => d.x0)
  .attr("y", d => d.y0)
  .attr("width", d => d.x1 - d.x0)
  .attr("height", d => d.y1 - d.y0)
  .attr("fill", "#69b3a2")
  .attr("stroke", "white");
```

## チャートタイプ

- **ネットワーク図**: 関係性の可視化
- **ツリーマップ**: 階層データ
- **サンキー図**: フロー可視化
- **コロプレス図**: 地理データ
- **バブルチャート**: 3次元データ
- **ヒートマップ**: マトリックスデータ

## バージョン情報

- スキルバージョン: 1.0.0
- 最終更新: 2025-01-22
