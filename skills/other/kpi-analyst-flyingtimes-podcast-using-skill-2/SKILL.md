---
name: kpi-analyst
description: 根据用户给出的excel文件内容，从中分析kpi指标的情况，并按照分工的列表，分别生成markdown格式的报告
allowed-tools: Read, Grep, Glob, Write, Search
---

# kpi-analyst

## Instructions
1、所有的运行中输出的临时程序、文件、代码统一放到当前项目根目录下的output/
2、根据用户指定的输入xlsx文件，参考[refrerence/xlsx.md](reference/xlsx.md)，得到每一页中的所有内容，并将结果写入当前项目根目录下的output/{sheetname}.md
3、根据当前项目根目录下output/指标通报.md文件中的内容，找到各个地市的指标，并按照[reference/分工.md](reference/分工.md)中的负责人信息，分别生成给不同地市的负责人的指标通报，结果写入当前项目根目录下的output/{负责人}.md
4、检查是否正确的在当前项目根目录下的output/文件夹中存在各个负责人的输出文件，如果没有这个输出请再检查整个过程是否存在问题。
