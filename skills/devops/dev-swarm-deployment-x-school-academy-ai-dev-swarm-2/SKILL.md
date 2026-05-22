---
name: dev-swarm-deployment
description: Deploy application to staging/production environments, setup CD pipelines, manage cloud infrastructure, and configure monitoring. Use when user asks to deploy application, setup production environment, or configure automated deployment.
---

# AI Builder - Deployment

This skill handles the deployment of applications to various environments (staging, production), sets up CD pipelines, manages cloud infrastructure, and configures monitoring and logging systems.

## When to Use This Skill

- User asks to deploy the application
- User wants to setup production or staging environment
- User needs CD pipeline configuration
- User wants to configure cloud infrastructure (AWS, Azure, GCP, etc.)
- User needs to setup monitoring, logging, or alerting
- User wants to configure domain names and SSL certificates
- When application is ready for production deployment
- When `09-sprints/` development is complete and ready for release

## Your Roles in This Skill

- **Deployment Engineer**: Execute and manage application deployments to various environments. Identify the best deployment strategy (blue-green, canary, rolling updates) based on project requirements and ensure zero-downtime deployments.
- **Cloud Infrastructure Architect**: Design and implement scalable, cost-effective cloud infrastructure solutions. Make decisions on cloud provider selection, infrastructure as code approach, and resource optimization.
- **DevOps Engineer**: Setup and maintain CI/CD pipelines for automated testing and deployment. Ensure proper integration between development, testing, and production environments.
- **SysOps Engineer**: Provision and manage cloud resources (compute, storage, networking). Configure web servers, load balancers, and security groups. Implement system-wide logging, monitoring, and alerting. Manage infrastructure security and scaling strategies. Ensure high availability and disaster recovery. Optimize cloud costs and resource utilization.
- **Site Reliability Engineer (SRE)**: Implement monitoring, logging, and alerting systems. Ensure application reliability, performance, and quick incident response. Define and track SLIs, SLOs, and error budgets. Implement automated remediation and incident response procedures.

## Role Communication

As an expert in your assigned roles, you must announce your actions before performing them using the following format:

As a {Role} [and {Role}, ...], I will {action description}

This communication pattern ensures transparency and allows for human-in-the-loop oversight at key decision points.
## Instructions

Follow these steps in order:

### Step 0: Verify Prerequisites and Gather Context

1. **Check if `09-sprints/` folder exists (recommended):**
   - If found: Read to understand:
     - Development progress and readiness
     - Features completed

1.5 **Verify previous stage completion (09-sprints if used):**
   - If `09-sprints/README.md` exists, read it and list required docs
   - If README is missing or required docs are missing:
     - Ask the user to start/continue stage 09, or skip it
     - If skip: create `09-sprints/SKIP.md` with a short reason
     - If continue: STOP and return after stage 09 is complete

2. **Check if `07-tech-specs/` folder exists (mandatory):**
   - If NOT found: Inform user they need to define tech specs first, then STOP
   - If found: Read all files to understand:
     - Technology stack chosen
     - Infrastructure requirements
     - Deployment needs

3. **Check if `00-init-ideas/` folder exists (recommended):**
   - If found: Read to understand all files

4. **Check if this stage should be skipped:**
   - Check if `10-deployment/SKIP.md` exists
   - **If SKIP.md exists:**
     - Read SKIP.md to understand why this stage was skipped
     - Inform the user: "Stage 10 (deployment) is marked as SKIP because [reason from SKIP.md]"
     - Ask the user: "Would you like to proceed anyway?"
     - **If user says yes:**
       - Delete SKIP.md and continue with this skill
     - **If user says no:**
       - Exit the skill

5. **Check if `10-deployment/` folder exists:**
   - If exists: Read all existing files to understand current deployment state
   - If NOT exists: Will create new structure

6. **If README.md exists:** Check whether it requires diagrams. If it does,
   follow `dev-swarm/docs/mermaid-diagram-guide.md` and use the
   `dev-swarm-mermaid` skill to render outputs.

7. **Assess Current State:**
   - Verify build process works (`npm run build`, `docker build`, etc.)
   - Check if tests pass
   - Review tech specs from `07-tech-specs/` for deployment requirements
   - Check if application has production configuration files
   - Look for existing cloud configurations (AWS, Azure, GCP credentials)
   - Check for infrastructure as code files (Terraform, CloudFormation, etc.)
   - Review existing deployment scripts or CI/CD configurations
   - Look for `src/.github/workflows/` (GitHub Actions)
   - Check for other CI/CD configurations (Jenkins, GitLab CI, CircleCI, etc.)

8. **Analyze Deployment Requirements:**

   Based on the tech stack (from `07-tech-specs/`) and project requirements:

   - Determine deployment needs:
     - **L2 Tools/Skills**: Deploy to `dev-swarm/py_scripts`, `dev-swarm/js_scripts`, or `dev-swarm/skills`.
     - **Hosting Platform**: Static hosting (Netlify, Vercel), PaaS (Heroku, Railway), IaaS (AWS EC2, Azure VMs), Container (ECS, Kubernetes), Serverless (Lambda, Cloud Functions)
     - **Database Hosting**: Managed database service vs self-hosted
     - **Storage**: Object storage (S3, Azure Blob), CDN requirements
     - **Compute**: Serverless, containers, or VMs
     - **Environments**: Development, staging, production (number of environments needed)

   - Identify complexity level:
     - **Basic**: Simple static sites or single PaaS deployment
     - **Standard**: Multi-environment setup with managed services, basic CI/CD
     - **Complex**: Multi-region deployment, microservices, advanced CI/CD, infrastructure as code, auto-scaling

   - Determine CD requirements:
     - Automated testing before deployment
     - Deployment approval process
     - Rollback strategy
     - Deployment frequency and schedule

   - Identify monitoring and observability needs:
     - Application performance monitoring (APM)
     - Error tracking and logging
     - Uptime monitoring
     - Alerting channels (email, Slack, PagerDuty)
     - Analytics and metrics

9. Proceed to Step 1 with gathered context

### Step 1: Refine Design Requirements in README and Get Approval

**CRITICAL: Create/update README.md first without pre-approval. Then ask the user to review/update/approve it, re-read it after approval, and only then create deployment plan files.**

1. **Analyze information from previous stages:**
   - Read `07-tech-specs/` to understand technology stack and infrastructure needs
   - Consider cost-budget constraints for deployment
   - Assess application readiness from Step 0

2. **Create or update 10-deployment/README.md with refined requirements:**
   - Use the template in `references/README.md`
   - Follow the checkbox rules: checked items apply after README approval; create file items only after approval; propose default checks; allow user changes
   - Populate only the template sections; do not add new headings such as Documents or Deliverables
   - Follow `dev-swarm/docs/stage-readme-guidelines.md` before drafting
   - Refer to `references/deliverables.md` to select deliverables by project type
   - Present any choices as checkbox lists with a default selection
   - **For L2 projects:** Create a simple README (just several lines) indicating the project level and the target deployment directory (e.g., `dev-swarm/py_scripts` or `dev-swarm/skills`).
   - **For L3+ projects:** List deliverables explicitly in README (typical: infrastructure-plan.md, cd-pipeline.md, deployment-strategy.md, monitoring-logging.md, environment-config.md)
   - **Stage overview and objectives** (based on previous stage context)
   - **Owners:** Deployment Engineer (lead), DevOps Engineer, SysOps Engineer, Site Reliability Engineer
   - **Diagrams (if required by project init):**
     - Reference `dev-swarm/docs/mermaid-diagram-guide.md`
     - Include `diagram/` deliverables when needed
   - **What deployment will include:**
     - For L2: Deployment to local script/skill directories (`deployment.md`)
     - Infrastructure setup (hosting, database, storage)
     - **CD strategy options (with checkboxes):**
       - [ ] Release to GitHub
       - [ ] Deploy to Cloud
       - [ ] Publish Package
     - CD pipeline configuration
     - Deployment strategy (blue-green, rolling, canary)
     - Monitoring and logging setup
     - Environment configurations
   - **Methodology:**
     - How infrastructure will be provisioned
     - How CD will be configured
   - **Deliverables planned:**
     - List of files that will be created (deployment.md for L2; infrastructure-plan.md, cd-pipeline.md, etc. for L3+)
   - **Status:** In Progress (update to "Completed" after deployment)

3. **Notify user after README is created:**
   - Say: "I have created README.md file, please check and update or approve the content."
   - Summarize the deployment approach and what will be configured
   - Summarize what setup files will be created
   - Explain cost implications of chosen infrastructure

4. **Wait for user approval:**
   - **If user says yes:** Re-read README.md (user may have updated it), then proceed to Step 2
   - **If user says no:**
     - Ask what needs to be changed
     - Update README based on feedback
     - Ask for approval again, then re-read README.md before proceeding

### Step 2: Create Deployment Plan Files

**Only after user approves the README and you re-read it:**

**IMPORTANT**: These files serve dual purposes:
1. **Initially**: Deployment plans/instructions for user approval
2. **Finally**: Documentation of the actual deployment setup (source of truth for future updates)

1. **Create folder structure:**
   ```
   10-deployment/
   ├── README.md
   ├── deployment-info.md (if independently runnable package/MCP server)
   ├── infrastructure-plan.md
   ├── cd-pipeline.md
   ├── deployment-strategy.md
   ├── monitoring-logging.md
   └── environment-config.md
   ```
   Just as sample, the actual file list should be samed as the `README.md` which user has selected.

2. **Create deployment plan files with proposed configurations:**

Use `references/deliverables.md` for file-by-file content guidance.

### Step 3: Get User Confirmation

1. Present all deployment plan files to the user
2. Explain what will be deployed and configured
3. Highlight cost implications if applicable
4. Ask user to review and confirm before proceeding
5. Make any adjustments based on user feedback
6. **DO NOT PROCEED** until user explicitly confirms

### Step 4: Execute Infrastructure Setup

**ONLY AFTER USER CONFIRMATION**, execute each setup:

1. **Execute Infrastructure Setup:**
   - Follow steps in `infrastructure-plan.md`
   - Create cloud accounts if needed (guide user)
   - Setup infrastructure as code (Terraform, CloudFormation, etc.)
   - Create and configure cloud resources
   - Setup VPC, subnets, security groups
   - Provision compute resources (servers, containers, serverless)
   - Setup databases and configure backups
   - Configure storage and CDN
   - Setup domain name and DNS records
   - Configure SSL/TLS certificates
   - **Fix any errors encountered during setup**
   - Retry failed steps with corrections
   - Document any manual steps user needs to complete

2. **Execute CD Pipeline Setup:**
   - Follow steps in `cd-pipeline.md`
   - Create CD configuration files
   - Configure build steps
   - Setup testing stages
   - Configure deployment stages for each environment
   - Setup secrets and environment variables in CD platform
   - Configure approval gates
   - Test pipeline with a sample deployment
   - **Fix any errors encountered during setup**
   - Retry failed steps with corrections
   - Document any manual approvals required

3. **Execute Monitoring and Logging Setup:**
   - Follow steps in `monitoring-logging.md`
   - Setup monitoring tools and agents
   - Configure logging aggregation
   - Setup error tracking service
   - Configure uptime monitoring
   - Create monitoring dashboards
   - Setup alerting rules
   - Configure notification channels
   - Test alerts and notifications
   - **Fix any errors encountered during setup**
   - Retry failed steps with corrections

4. **Configure Environments:**
   - Follow steps in `environment-config.md`
   - Setup environment variables in each environment
   - Configure secrets management
   - Store credentials securely
   - Configure feature flags
   - Verify configuration in each environment
   - **Fix any errors encountered during setup**
   - Retry failed steps with corrections

### Step 5: Initial Deployment

1. **For Independently Runnable Packages/MCP Servers:**
   - Follow deployment strategy from `deployment-info.md`
   - **Update src/README.md:**
     - Add installation instructions for end users
     - Include command examples (pnpm dlx, npx, or uvx --from)
     - Document all available commands and options
     - Add usage examples
   - **Push code to GitHub:**
     - Ask for explicit user approval before pushing
     - Ensure all changes are committed
     - Push code: `git push origin main` (or appropriate branch)
   - **Create GitHub Release:**
     - Ask for explicit user approval before opening the browser or creating the release
     - Use playwright-browser-* agent skills to automate browser interactions
     - Open GitHub repository releases page
     - Create a new release through the GitHub UI
     - Set version number (e.g., v1.0.0)
     - Add release notes describing the changes
     - Publish the release
   - **Verify installation:**
     - Test installation using the documented commands with the release version
     - Verify all commands work as expected
   - **Fix any errors encountered during deployment**
   - Document deployment completion
   - Update `deployment-info.md` with actual installation commands tested and release URL

2. **Deploy to Development/Staging First (For Cloud Deployments):**
   - Follow deployment strategy from `deployment-strategy.md`
   - Execute pre-deployment checklist
   - Trigger deployment via CD pipeline
   - Monitor deployment progress
   - Verify deployment success
   - Execute post-deployment verification
   - **Fix any errors encountered during deployment**
   - Adjust configuration as needed
   - Document any issues and resolutions

3. **Deploy to Production (if approved):**
   - Get explicit user confirmation for production deployment
   - Execute pre-deployment checklist
   - Trigger production deployment
   - Monitor deployment closely
   - Verify all services are running
   - Check monitoring dashboards
   - Verify application functionality
   - **Fix any errors encountered during deployment**
   - Be prepared to rollback if issues occur
   - Document deployment completion

### Step 6: Verification and Testing

For each deployed environment:

1. **Verify Infrastructure:**
   - All resources are running
   - Network connectivity is working
   - DNS resolution is correct
   - SSL certificates are valid
   - Security groups are properly configured
   - Backups are configured and working

2. **Verify Application:**
   - Application is accessible via public URL
   - All features are working correctly
   - Database connections are successful
   - API endpoints respond correctly
   - Static assets are served via CDN
   - Performance is acceptable

3. **Verify CD Pipeline:**
   - Pipeline executes successfully
   - Tests run and pass
   - Deployment completes without errors
   - Approval gates work correctly
   - Secrets are properly injected

4. **Verify Monitoring and Logging:**
   - Metrics are being collected
   - Logs are being aggregated
   - Errors are being tracked
   - Alerts are triggered correctly
   - Notifications are received
   - Dashboards display data correctly

### Step 7: Update Documentation Files

**CRITICAL**: Update all deployment files to reflect actual environment:

1. **Update deployment-info.md (if applicable):**
   - Change from "deployment plan" to "current deployment configuration"
   - Document actual version numbers released
   - Document actual installation commands tested and verified
   - Add links to GitHub releases page
   - Document the release creation process using playwright-browser-* agent skills
   - Document actual src/README.md updates made
   - Add verification results
   - Add troubleshooting notes for any issues encountered
   - Document how to create future releases using the browser automation approach

2. **Update infrastructure-plan.md:**
   - Change from "deployment plan" to "current infrastructure"
   - Document actual resources created with IDs/ARNs
   - Document actual costs (if available)
   - Add verification results
   - Add troubleshooting notes for any issues encountered
   - Document how to access and manage infrastructure

3. **Update cd-pipeline.md:**
   - Change from "deployment plan" to "current pipeline configuration"
   - Document actual pipeline setup and workflow
   - Add links to pipeline runs
   - Add verification results
   - Add troubleshooting notes for any issues encountered
   - Document how to trigger and monitor deployments

4. **Update deployment-strategy.md:**
   - Change from "deployment plan" to "current deployment process"
   - Document actual deployment steps executed
   - Add verification results
   - Add troubleshooting notes for any issues encountered
   - Document successful deployment timeline
   - Update rollback procedures based on actual setup

5. **Update monitoring-logging.md:**
   - Change from "deployment plan" to "current monitoring setup"
   - Document actual monitoring tools configured
   - Add dashboard URLs
   - Add verification results
   - Add troubleshooting notes for any issues encountered
   - Document how to access logs and metrics

6. **Update environment-config.md:**
   - Change from "deployment plan" to "current environment configuration"
   - Document actual environment variables (without sensitive values)
   - Document where secrets are stored
   - Add verification results
   - Add troubleshooting notes for any issues encountered
   - Document how to update configuration

7. **Update 10-deployment/README.md:**
   - Update current deployment status to "Deployed"
   - Add environment URLs for each deployed environment
   - Add summary of deployed infrastructure
   - Add links to monitoring dashboards
   - Add links to CD pipelines
   - Note date of deployment completion
   - Add quick troubleshooting guide

**These updated files now serve as the source of truth for:**
- Future deployments and updates
- Infrastructure modifications
- Troubleshooting deployment issues
- Onboarding new team members
- Disaster recovery procedures

### Step 8: Security and Compliance Check

1. **Security Review:**
   - Verify all secrets are stored securely
   - Check that no credentials are in code or logs
   - Verify SSL/TLS is configured correctly
   - Review security group rules
   - Check for unnecessary public access
   - Verify backup encryption

2. **Cost Optimization:**
   - Review actual costs vs estimates
   - Identify optimization opportunities
   - Setup cost alerts
   - Document cost breakdown

3. **Compliance:**
   - Document compliance requirements met
   - Verify data residency requirements
   - Check backup and retention policies

### Step 9: Final User Review

1. **Inform user that deployment is complete**
2. **Update README.md:**
   - Change **Status** from "In Progress" to "Completed"
   - Add a **Summary** section with key insights (2-3 paragraphs)
   - Add a **Created Files** section listing all created files
   - Add **Deployment URLs** section with links to deployed environments

3. **Present completed work to user:**
   - Show the updated documentation showing actual deployment
   - Show verification results for all environments
   - Provide URLs to access deployed application
   - Share monitoring dashboard links
   - Confirm everything is working as expected
   - Provide handoff documentation for ongoing maintenance

4. Ask if they want any adjustments or additional configurations

### Step 10: Commit to Git

1. **Ask user if they want to commit the deployment documentation:**
   - Stage all changes in `10-deployment/`
   - Stage any infrastructure as code files created
   - Stage CD configuration files
   - Commit with message: "Setup deployment infrastructure and CD pipeline"

2. **Optionally push to remote**
