# The Platform Engineer's Handbook - Platform Team Administration

[![Pulumi Infrastructure](https://github.com/Jdavid77/platform-team-admin/actions/workflows/pulumi.yml/badge.svg)](https://github.com/Jdavid77/platform-team-admin/actions/workflows/pulumi.yml)

Follow-along repository for *The Platform Engineer's Handbook*.

This repo demonstrates how a platform team can manage GitHub as code using Pulumi. Instead of clicking through the GitHub UI, all repositories, branch protection rules, and deployment environments are declared in a single YAML file (`config/platform_team_values.yaml`) and applied automatically via a CI/CD pipeline.

The workflow is tag-driven: pushing a `v*` tag triggers a Pulumi preview, waits for manual approval, then runs `pulumi up` to reconcile the declared state with GitHub.

## Prerequisites

- [Pulumi CLI](https://www.pulumi.com/docs/install/)
- [uv](https://docs.astral.sh/uv/getting-started/installation/) — Python toolchain
- [Bitwarden CLI](https://bitwarden.com/help/cli/) (`bw`) — used to fetch secrets
- A GitHub personal access token with `repo` and `admin:org` scopes

## Setup

**1. Install dependencies**

```bash
uv sync
```

**2. Configure secrets**

Copy `.env.example` to `.env` and fill in your Bitwarden credentials, then run:

```bash
cd secrets-setup
./fetch_secrets.sh
```

This pulls your GitHub token and org owner from Bitwarden and sets them as Pulumi config values.

## Configure repositories

Edit `config/platform_team_values.yaml` to define your repositories, environments, and branch protection rules:

```yaml
github_repositories:
  - name: my-repo
    description: "My repository"
    visibility: public
    branch_protection:
      pattern: "main"
      enforce_admins: true
      require_signed_commits: true
      required_pull_request_reviews:       # optional
        required_approving_review_count: 1
        dismiss_stale_reviews: false
        require_code_owner_reviews: false
        require_last_push_approval: false
    environments:
      - name: production
        reviewers:
          - your-github-username
```

## Deploy

Preview changes:

```bash
pulumi preview
```

Apply changes (triggered automatically on tags matching `v*`):

```bash
pulumi up
```
