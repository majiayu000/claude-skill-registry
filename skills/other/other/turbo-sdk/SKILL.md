---
name: turbo-sdk
description: Complete Arweave Turbo ecosystem including client SDKs, core upload infrastructure, payment service backend, and CLI tools for permanent decentralized storage
version: 1.3.0
---

# turbo-sdk

Complete Arweave Turbo ecosystem skill covering client SDKs, core upload infrastructure, backend payment services, and CLI tooling for permanent decentralized storage.

## Description

This skill provides end-to-end coverage of the Turbo Upload Service ecosystem for permanent decentralized storage on Arweave:

### turbo-sdk (Client SDK)
The first SDK on Arweave to bring you programmable fiat top ups, Turbo-powered upload reliability, and fast data and indexing finality for TypeScript based Web and Node projects.

**Repository:** [ardriveapp/turbo-sdk](https://github.com/ardriveapp/turbo-sdk)
**Language:** TypeScript (97.8%)
**Stars:** 51
**License:** Apache License 2.0
**Status:** Production-ready with 144 releases
**Purpose:** Client-side upload and payment integration

### turbo-upload-service (Core Infrastructure)
Production-grade data bundling service that packages ANS-104 "data items" and delivers them to Arweave. Two-component architecture (Upload Service + Fulfillment Service) designed for AWS at-scale deployment with Docker support.

**Repository:** [ardriveapp/turbo-upload-service](https://github.com/ardriveapp/turbo-upload-service)
**Language:** TypeScript (97.9%)
**Stars:** 11
**License:** AGPL-3.0 (strong copyleft)
**Status:** Production infrastructure with PostgreSQL, S3, SQS
**Purpose:** Core upload orchestration and Arweave delivery

### turbo-payment-service (Backend Service)
Production-grade backend payment processing system managing Turbo balances, cryptocurrency transactions, and Stripe integration for the ArDrive platform.

**Repository:** [ardriveapp/turbo-payment-service](https://github.com/ardriveapp/turbo-payment-service)
**Language:** TypeScript (99.8%)
**Stars:** 8
**License:** AGPL-3.0 (strong copyleft)
**Status:** Production backend with PostgreSQL, Docker, Koa framework
**Purpose:** Payment infrastructure and balance management

### x402-turbo-upload (CLI Tool)
A minimal TypeScript command-line tool demonstrating x402 protocol integration with Turbo Upload Service using EVM wallet authentication.

**Repository:** [ardriveapp/x402-turbo-upload](https://github.com/ardriveapp/x402-turbo-upload)
**Language:** TypeScript (100%)
**Stars:** 0 (new - created Nov 2025)
**Status:** Development/Educational tool
**Purpose:** CLI automation and protocol learning

## When to Use This Skill

### For Frontend/Client Development (turbo-sdk)
- Implementing permanent file uploads to Arweave
- Building applications with programmable fiat top-ups
- Integrating Turbo Upload Service into TypeScript/JavaScript projects
- Requiring production-grade upload reliability and error handling
- Needing comprehensive API documentation and examples
- Checking known issues or recent changes
- Reviewing extensive release history (144 releases)

### For Core Infrastructure Development (turbo-upload-service)
- Building or hosting your own Turbo upload infrastructure
- Understanding ANS-104 data item bundling for Arweave
- Operating upload services at AWS scale
- Implementing multi-signature upload support (Arweave, Ethereum, Solana)
- Managing asynchronous fulfillment workflows
- Docker and LocalStack development environments
- Database migration workflows with Knex
- S3 object storage and SQS queue integration
- Understanding AGPL-3.0 implications for infrastructure hosting

### For Payment Infrastructure Development (turbo-payment-service)
- Building payment processing infrastructure
- Managing Turbo balances and cryptocurrency transactions
- Integrating Stripe for fiat payments
- Setting up multi-blockchain payment support (Ethereum, Solana, Arweave)
- Implementing balance management systems
- Creating payment service backends with PostgreSQL
- Docker deployment and database migration workflows
- Understanding AGPL-3.0 license implications for backend services

### For Learning & Simple Automation (x402-turbo-upload)
- Learning x402 protocol basics and implementation
- Creating simple CLI automation scripts
- Testing custom Turbo Upload endpoints
- Understanding EVM wallet authentication with uploads
- Quick one-off upload testing
- Minimal reference implementation study

### General Use Cases
- Understanding complete Turbo ecosystem (client + infrastructure + payment + CLI)
- Comparing frontend SDK vs backend service vs core infrastructure architectures
- Evaluating production vs development tooling
- Integrating permanent storage with payment processing
- Planning full-stack Arweave applications
- White-labeling Turbo infrastructure for custom platforms

## Quick Reference

### turbo-sdk (Client SDK)
- **Homepage:** https://ardrive.io/turbo/
- **Topics:** ardrive, arweave, commonjs, esm, nodejs, turbo
- **Open Issues:** 1
- **Last Updated:** 2025-12-26
- **Latest Release:** v1.39.2 (2025-12-15)
- **Use For:** Frontend uploads, client integration

### turbo-upload-service (Core Infrastructure)
- **Technology Stack:** Koa, PostgreSQL, S3, SQS, Docker, LocalStack
- **Architecture:** Two-component (Upload Service + Fulfillment Service)
- **Stars:** 11
- **Multi-Signature Support:** Arweave, Ethereum, Solana
- **Deployment:** AWS-optimized with Docker support
- **License Warning:** AGPL-3.0 requires source disclosure for network use
- **Use For:** Core upload infrastructure, platform hosting

### turbo-payment-service (Payment Backend)
- **Technology Stack:** Node.js, Koa, PostgreSQL, Stripe
- **Contributors:** 4 active developers
- **Total Commits:** 24
- **Blockchain Support:** Ethereum, Solana, Arweave
- **License Warning:** AGPL-3.0 requires source disclosure for network use
- **Use For:** Payment infrastructure, balance management

### x402-turbo-upload (CLI Tool)
- **Repository:** GitHub - ardriveapp/x402-turbo-upload
- **Purpose:** Minimal demonstration/educational tool
- **Created:** November 17, 2025
- **Total Commits:** 4
- **Use For:** Learning, simple automation

### Languages
- **TypeScript:** 97.8%
- **JavaScript:** 1.6%
- **Shell:** 0.4%
- **HTML:** 0.2%

### Recent Releases
- **v1.39.2** (2025-12-15): v1.39.2
- **v1.39.1** (2025-12-11): v1.39.1
- **v1.39.1-alpha.1** (2025-12-10): v1.39.1-alpha.1

## Available References

### turbo-sdk (Client SDK) References
- `references/README.md` - Complete README documentation (51 KB)
- `references/CHANGELOG.md` - Version history and changes (33 KB)
- `references/issues.md` - Recent GitHub issues (678 bytes)
- `references/releases.md` - Release notes (112 KB, 144 releases)
- `references/file_structure.md` - Repository structure (196 items)

### turbo-upload-service (Core Infrastructure) Reference
- `references/turbo-upload-service.md` - Complete infrastructure documentation including two-component architecture (Upload + Fulfillment), AWS deployment, Docker setup, LocalStack configuration, database migrations, testing strategies, multi-signature support, API endpoints, and AGPL-3.0 license considerations

### turbo-payment-service (Payment Backend) Reference
- `references/turbo-payment-service.md` - Complete backend documentation including architecture, API design, database schema, deployment, testing, Stripe integration, cryptocurrency payment flows, Docker setup, and AGPL-3.0 license considerations

### x402-turbo-upload (CLI Tool) Reference
- `references/x402-turbo-upload.md` - CLI tool documentation with usage examples, security considerations, and comparison with turbo-sdk

## Ecosystem Component Selection Guide

| Need | Component | Reason |
|------|-----------|--------|
| **Client-side uploads** | **turbo-sdk** | Production SDK, comprehensive, 144 releases |
| **Host upload infrastructure** | **turbo-upload-service** | Core bundling service, AWS-scale, Docker support |
| **ANS-104 data bundling** | **turbo-upload-service** | Arweave delivery orchestration |
| **Multi-signature uploads** | **turbo-upload-service** | Arweave, Ethereum, Solana support |
| **Backend payment processing** | **turbo-payment-service** | Multi-blockchain, Stripe, PostgreSQL |
| **Balance management** | **turbo-payment-service** | Transaction tracking, database-backed |
| **Fiat payments** | **turbo-payment-service** | Stripe integration built-in |
| **Cryptocurrency payments** | **turbo-payment-service** | Ethereum, Solana, Arweave support |
| **Simple CLI automation** | **x402-turbo-upload** | Minimal, straightforward |
| **Learning x402 protocol** | **x402-turbo-upload** | Clear, minimal example |
| **Full-stack application** | **All four** | Complete ecosystem coverage |
| **White-label platform** | **upload-service + payment-service** | Core infrastructure components |

## Usage

### turbo-sdk (Client SDK)
See `references/README.md` for complete API documentation, installation instructions, and comprehensive usage examples for client-side upload integration.

### turbo-upload-service (Core Infrastructure)
See `references/turbo-upload-service.md` for:
- Two-component architecture (Upload Service + Fulfillment Service)
- AWS production deployment at scale
- Docker and LocalStack local development
- Database migrations with Knex
- Multi-signature upload support (Arweave, Ethereum, Solana)
- S3 and SQS integration
- Testing strategies (unit + integration)
- API endpoint documentation
- **IMPORTANT:** AGPL-3.0 license compliance requirements for hosting

### turbo-payment-service (Payment Backend)
See `references/turbo-payment-service.md` for:
- Backend architecture and technology stack
- Local development setup with Docker
- Database migration workflows
- Payment integration (Stripe + cryptocurrency)
- API design patterns
- Testing strategies
- Production deployment
- **IMPORTANT:** AGPL-3.0 license compliance requirements

### x402-turbo-upload (CLI Tool)
See `references/x402-turbo-upload.md` for CLI usage, parameters, examples, and important production considerations.

---

**Skill Version:** 1.3.0
**Last Enhanced:** January 3, 2026
**Coverage:** Complete Turbo ecosystem (client SDK + upload infrastructure + payment backend + CLI tool)
**Components:** 4 repositories, 8 reference files
**Generated by Skill Seeker** | Enhanced with complete infrastructure coverage
