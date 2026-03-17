---
name: read-arxiv-paper
description: Use this skill when when asked to read an arxiv paper given an arxiv URL
---

All file paths below are relative to the **project root** (the directory containing the `.claude/` folder, not the skill directory itself).

You will be given a URL of an arxiv paper, for example:

https://www.arxiv.org/abs/2601.07372

### Part 1: Normalize the URL

The goal is to fetch the TeX Source of the paper (not the PDF!), the URL always looks like this:

https://www.arxiv.org/src/2601.07372

Notice the /src/ in the url. Once you have the URL:

### Part 2: Download the paper source

Fetch the url to a local .tar.gz file.

### Part 3: Unpack the file in that folder

Unpack the contents into `./knowledge/{arxiv_id}` directory and delete the .tar.gz.

### Part 4: Locate the entrypoint

Every latex source usually has an entrypoint, such as `main.tex` or something like that.

### Part 5: Read the paper

Once you've found the entrypoint, Read the contents and then recurse through all other relevant source files to read the paper.

#### Part 6: Report

Once you've read the paper, produce a summary of the paper into a markdown file at `./knowledge/summary_{tag}.md`. Notice that 1) use the local knowledge directory here (it's easier for me to open and reference here), and 2) generate some reasonable `tag` like e.g. `conditional_memory` or whatever seems appropriate given the paper. Probably make sure that the tag doesn't exist yet so you're not overwriting files.

As for the summary itself, remember that you're processing this paper within the context of the ouro_rl repository, which explores the Ouro pretrained language model. Focus on how the paper's ideas might apply to loading, fine-tuning, or doing RL with the Ouro model.
