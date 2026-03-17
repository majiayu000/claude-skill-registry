---
name: cicd-setup
description: "Sets up a CI/CD pipeline for Python projects using GitHub Actions. Includes templates for PR checks, deployment via SSH, pre-commit hooks, and email notifications. Use this skill when a user wants to create a new CI/CD pipeline for a Python project."
---

# CI/CD Pipeline Setup Skill

This skill provides templates and guides to set up a CI/CD pipeline for a Python project using GitHub Actions.

## Core Workflow

1.  **Set up Pre-commit Hooks**:
    -   Copy the `.pre-commit-config.yaml` from `assets/pre-commit/` to the root of the user's repository.
    -   Guide the user to install pre-commit (`pip install pre-commit`) and set it up (`pre-commit install`).

2.  **Set up GitHub Actions Workflows**:
    -   Create a `.github/workflows/` directory in the user's repository if it doesn't exist.
    -   Copy `assets/github_actions/python_pr_workflow.yml` to `.github/workflows/`. This workflow runs tests and linting on every pull request to `main`.
    -   Copy `assets/github_actions/python_deploy_workflow.yml` to `.github/workflows/`. This workflow deploys the application when a PR is merged to `main`.

3.  **Configure Secrets**:
    -   Guide the user to add the necessary secrets for deployment and notifications as described in `references/secret_management.md`.

4.  **Set Up Branch Protection**:
    -   Guide the user through setting up branch protection rules for the `main` branch as detailed in `references/branch_protection.md`.

## Bundled Resources

### Assets

-   `assets/github_actions/python_pr_workflow.yml`: Workflow to run checks on pull requests.
-   `assets/github_actions/python_deploy_workflow.yml`: Workflow to deploy on merge to `main`.
-   `assets/notifications/email_notification_template.txt`: Template for email notifications on successful deployment.
-   `assets/pre-commit/.pre-commit-config.yaml`: Configuration for pre-commit hooks for Python projects.

### References

-   `references/secret_management.md`: How to configure secrets for SSH and email.
-   `references/caching_strategies.md`: Explanation of caching for Python dependencies.
-   `references/branch_protection.md`: How to set up branch protection rules in GitHub.

**Before starting, ask the user if they use `requirements.txt`, `poetry`, or `pipenv` for dependency management and adjust the caching steps in the workflows if necessary.**
