---
name: cloud-deployment
description: "Provides guidance and resources for deploying applications to various cloud platforms like Vercel, Railway, Render, and Fly.io. Use this skill when a user asks to deploy an application, set up a cloud environment, or needs help with cloud configuration, CI/CD, custom domains, and rollbacks for these platforms."
---

# Cloud Deployment Skill

## Overview

This skill provides a structured workflow and reference materials for deploying web applications to popular cloud platforms. It covers platform selection, configuration, and management of common deployment tasks.

## 1. Select a Deployment Platform

The first step is to determine the best platform for the user's project. If the user hasn't already chosen a platform, guide them through the decision process.

**Action**: Read `references/platform_selection_guide.md` to understand the strengths of each platform (Vercel, Railway, Render, Fly.io) and help the user make a choice.

## 2. Follow Platform-Specific Guide

Once a platform is chosen, use the corresponding guide in the `references/` directory. Each guide contains a deployment checklist, CI/CD information, and rollback procedures.

- **Vercel**: `references/vercel.md`
- **Railway**: `references/railway.md`
- **Render**: `references/render.md`
- **Fly.io**: `references/fly_io.md`

## 3. Use General Guides for Common Tasks

For tasks that are common across all platforms, refer to `references/general_guides.md`. This file contains instructions for:

- Environment Variable Setup
- Database Connection
- Custom Domain Configuration
- SSL/TLS Certificate Setup

## 4. Use Asset Templates

The `assets/` directory contains boilerplate configuration files for each platform. Copy these to the user's project as a starting point.

- `assets/vercel.json`
- `assets/railway.json`
- `assets/render.yaml`
- `assets/fly.toml`
