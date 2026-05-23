---
name: podcast-writer
description: 根据用户给出的文字或者用户指定的txt/md文件内容，从类型列表中选择合适的文本类型，按照指定的格式给出podcast直播口述稿
allowed-tools: Read, Grep, Glob, Write, Search
---

# Your Skill Name

## Instructions
1、如果用户指定了输入的txt或者md文件，那么从文件中读取输入内容{input}
2、如果用户给出一个链接，调用工具从链接中读取输入内容{input}
3、如果用户直接给出了内容，则这个内容就是输入内容{input}
4、对输入内容进行分析，判断这个内容适合使用什么样的方式来输出podcast直播口述稿，可选的类型列表如下：
["名人访谈录","中美贸易战","新闻分析","新技术","其他"]
所有无法找到明确分类的都归类为"其他"
"名人访谈录"对应的提示词模版为: [FAMOUS_TEMPL.md](FAMOUS_TEMPL.md)
"中美贸易战"对应的提示词模版为: [TRADE.md](TRADE.md)
"新闻分析"对应的提示词模版为: [NEWS.md](NEWS.md)
"新技术"对应的提示词模版为: [TECH.md](TECH.md)
"其他"对应的提示词模版为: [OTHER.md](OTHER.md)
5、为这个内容生成一个合适的标题{title}
6、根据给出的提示词模版和输入{input},直接生成podcast直播口述稿，并写入当前项目目录下的/output/{title}_{currentdate_currenttime}.txt
7、将{input}单独写入当前项目目录下的/output/{title}_{currentdate_currenttime}_original.txt
8、第6步生成的文件内容还是很拗口，请将其改成更口语化的表达，除了口述稿正文内容，不要添加其他任何标题、旁白、解释,并将结果写入当前项目目录下的/output/{title}_{currentdate_currenttime}_final.txt
9、生成音频文件。
运行帮助脚本runninghub_api.py,使用当前项目目录下的/output/{title}_{currentdate_currenttime}_final.txt 作为input.txt,使用当前项目目录下的/output/{title}_{currentdate_currenttime}_final.flac 作为output.flac
```
# 使用指定文本文件和指定输出路径
python scripts/runninghub_api.py man input.txt output.flac
```
