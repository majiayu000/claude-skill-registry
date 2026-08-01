---
name: features
description: import React, { useRef, useEffect } from 'react';
---

# D3.js

## 기술

```js
import React, { useRef, useEffect } from 'react';
import * as d3 from 'd3';

const Skills = ({ title }) => {
  const widthRef = useRef();
  const svgRef = useRef();

  const skillData = [
    {
      title: 'HTML & CSS',
      value: 65,
      color: '#d9a1ab',
    },
    {
      title: 'JS',
      value: 70,
      color: '#d9a1ab',
    },
    {
      title: 'React.js',
      value: 52,
      color: '#ceb5df',
    },
    {
      title: 'Vue.js',
      value: 35,
      color: '#ceb5df',
    },
    {
      title: 'Node.js',
      value: 15,
      color: '#dcdfb5',
    },
    {
      title: 'Java',
      value: 50,
      color: '#dcdfb5',
    },
    {
      title: 'Oracle',
      value: 38,
      color: '#bddfb5',
    },
    {
      title: 'Mysql',
      value: 28,
      color: '#bddfb5',
    },
  ];

  useEffect(() => {
    const svg = d3.select(svgRef.current);
    const chart = svg.append('g').attr('transform', `translate(40, 20)`);

    const margin = 50;
    // width: 렌더링될 때의 화면 너비에 맞춤
    const width = widthRef.current.clientWidth - margin * 2;
    const height = 350 - margin * 2;

    // scaleLinear() 사용
    const yScale = d3.scaleLinear().range([height, 0]).domain([0, 100]);
    const xScale = d3
      .scaleBand()
      .range([0, width])
      .domain(skillData.map(d => d.title))
      .padding(0.4);

    // x축, y축 만들기
    chart.append('g').call(d3.axisLeft(yScale));
    chart
      .append('g')
      .attr('transform', `translate(0, ${height})`)
      .call(d3.axisBottom(xScale));

    // 수평 그리드선 만들기
    chart
      .append('g')
      .call(d3.axisLeft().scale(yScale).tickSize(-width, 0, 0).tickFormat(''));

    // bar 만들기
    const barGroups = chart.selectAll().data(skillData).enter().append('g');
    barGroups
      .append('rect')
      .attr('x', d => xScale(d.title))
      .attr('y', height)
      .attr('width', xScale.bandwidth())
      .attr('height', 0)
      .attr('fill', d => d.color);

    // 점수 셋팅: display none
    barGroups
      .append('text')
      .attr('class', 'value')
      .attr('id', d => d.title.substring(0, 2))
      .attr('x', d => xScale(d.title) + xScale.bandwidth() / 2)
      .attr('y', d => yScale(d.value) + 30)
      .attr('text-anchor', 'middle')
      .text(d => d.value)
      .style('display', 'none');

    // 애니메이션 효과
    barGroups
      .selectAll('rect')
      .transition()
      .duration(800)
      .attr('y', d => yScale(d.value))
      .attr('height', d => height - yScale(d.value));

    // 마우스 이벤트
    barGroups
      .selectAll('rect')
      .on('mouseenter', function (r, i) {
        d3.select(this)
          .transition()
          .duration(300)
          .attr('opacity', 0.7)
          .attr('x', d => xScale(d.title) - 2)
          .attr('width', xScale.bandwidth() + 4);

        // 점수 표시
        d3.selectAll(`#${i.title.substring(0, 2)}`).style('display', 'block');

        // 가이드 눈금선 표시
        const y = yScale(i.value);
        chart
          .append('line')
          .attr('id', 'limit')
          .attr('x1', 0)
          .attr('y1', y)
          .attr('x2', width)
          .attr('y2', y);
      })
      .on('mouseleave', function () {
        d3.select(this)
          .transition()
          .duration(300)
          .attr('opacity', 1)
          .attr('x', d => xScale(d.title))
          .attr('width', xScale.bandwidth());

        d3.selectAll('.value').style('display', 'none');
        chart.selectAll('#limit').remove();
      });

    barGroups
      .selectAll('text')
      .on('mouseenter', function (r, i) {
        d3.selectAll(`#${i.title.substring(0, 2)}`).style('display', 'block');
      })
      .on('mouseleave', function () {
        d3.selectAll('.value').style('display', 'none');
      });
  }, []);

  // code...
};
```


