---
name: microsim-vis-network
description: Create an educational MicroSim using the vis-network JavaScript library.  Each MicroSim is a directory located in the /docs/sims folder.  It has a main.html file that can be referenced with an iframe.  The main.html file imports the main JavaScript code to run the educational MicroSim.
---
# Educational MicroSim Creation Skill for Vis-Network

## Overview

This skill contains the rules for generating a Educational MicroSim using the vis.network JavaScript library.
MicroSims are lightweight, interactive educational simulations designed for browser-based learning. 
MicroSims occupy a unique position at the intersection of 

1. **Simplicity** (focused scope, transparent code)
2. **Accessibility** (browser-native, universal embedding)
3. **AI Generation** (standardized patterns, prompt-compatible design).

## Purpose

Educational MicroSims transform abstract concepts into visual interactive, manipulable experiences that enable students to learn through exploration and experimentation. Each MicroSim addresses specific learning objectives while maintaining the pedagogical rigor and technical quality necessary for educational deployment.

## Development Process

### Step 1: Educational Requirements Specification

Before generating code, articulate the educational purpose:

1. **Subject Area and Topic**: What specific concept does this simulation teach?
2. **Grade Level**: Elementary (K-5), Middle School (6-8), High School (9-12), or Undergraduate
3. **Learning Objectives**: What should students understand after using this simulation? (Align with Bloom's Taxonomy: Remember, Understand, Apply, Analyze, Evaluate, Create)
4. **Duration**: Typical engagement time (5-15 minutes recommended)
5. **Prerequisites**: What knowledge must students have before using this?
6. **Assessment Opportunities**: How can educators verify learning?

### Step 2: MicroSim Implementation with Vis-Network

Generate a self-contained, interactive vis-network.js simulation following the standardized MicroSim architecture.  The program is width responsive.

#### Folder Structure
Each Vis-Network MicroSim is contained in a folder within the /docs/sims directory.  The folder name is $MICROSIM_NAME

```
/docs/sims/$MICROSIM_NAME
/docs/sims/$MICROSIM_NAME/index.md # main index markdown for each MicroSim containing the iframe and documentation
/docs/sims/$MICROSIM_NAME/main.html # main HTML5 file containing the p5.js CDN link and importing the p5.js JavaScript
/docs/sims/$MICROSIM_NAME/$MICROSIM_NAME.js # All the p5.js JavaScript
/docs/sims/$MICROSIM_NAME/metadata.json # JSON file with Dublin core metadata and description of controls
```
