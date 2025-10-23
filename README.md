# Documentation Checker Action

A reusable GitHub Action that checks documentation format by converting Contents sections to Navigation tables and comparing with Discourse posts.

## Usage

Add this action to any repository with documentation:

```yaml
name: Check Documentation

on:
  pull_request:
    paths:
      - 'docs/**'

jobs:
  check-docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: canonical/discourse-doc-checker@main  # or @v1 once tagged
        with:
          docs-path: 'docs'
          discourse-url: 'https://discourse.charmhub.io'
          discourse-api-key: ${{ secrets.DISCOURSE_API_KEY }}
          discourse-api-user: ${{ secrets.DISCOURSE_API_USER }}
          # Optional: Create an issue with results
          create-issue: 'true'
          github-token: ${{ secrets.GITHUB_TOKEN }}
          issue-title: 'Documentation Check Failed'
          issue-labels: 'documentation,bug'
```

## Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `docs-path` | Path to documentation directory | No | `docs` |
| `discourse-url` | Discourse instance URL | No | `https://discourse.charmhub.io` |
| `discourse-api-key` | Discourse API key | No | `` |
| `discourse-api-user` | Discourse API username | No | `system` |
| `working-directory` | Working directory | No | `.` |
| `github-token` | GitHub token for creating issues | No | `` |
| `create-issue` | Whether to create an issue with the output (true/false) | No | `false` |
| `issue-title` | Title for the issue to be created | No | `Documentation Check Failed` |
| `issue-labels` | Comma-separated list of labels to add to the issue | No | `documentation` |

## What it does

1. **Converts Contents to Navigation**: Automatically converts markdown Contents sections to Navigation table format
2. **Compares with Discourse**: Fetches content from Discourse and compares formatting
3. **Reports differences**: Shows detailed diffs when documentation doesn't match
4. **Fails on differences**: Returns non-zero exit code to fail CI when issues are found
5. **Creates issues (optional)**: Can automatically create GitHub issues with the check results and detailed output

## Example conversion

**Before (Contents format):**
```markdown
# Contents

1. [Tutorial](tutorial)
  1. [Getting Started](tutorial/getting-started.md)
  1. [Testing NetBox](tutorial/testing-netbox.md)
```

**After (Navigation format):**
```markdown
# Navigation

| Level | Path | Navlink |
| -- | -- | -- |
| 1 | tutorial | [Tutorial]() |
| 2 | tutorial-getting-started | [Getting Started](/t/netbox-k8s-docs-getting-started/18935) |
| 2 | tutorial-testing-netbox | [Testing NetBox](/t/netbox-k8s-docs-testing-netbox/18937) |
```

## Issue Creation

When `create-issue` is set to `true` and a `github-token` is provided, the action will **only create a GitHub issue when problems are detected**, such as:

- Documentation differences found between local files and Discourse
- Documentation directory not found
- Errors during the documentation check process

The issue will include:
- **Repository information**: Name, branch, commit SHA
- **Action run details**: Link to the workflow run
- **Issue type**: Specific problem detected (missing directory, differences found, etc.)
- **Full output**: Complete output from the documentation check
- **Next steps**: Guidance on how to resolve the issue

Issues are **not created** for successful runs where no differences are found.

**Note**: The `GITHUB_TOKEN` secret is automatically available in GitHub Actions and has the necessary permissions to create issues in the same repository.

## Repository Structure

```
.
├── action.yml         # Action definition
├── check_docs.py     # Main Python script
├── requirements.txt  # Python dependencies
└── README.md        # This file
```

## Action References

You can reference this action in different ways:

### Using a specific branch (recommended for development)
```yaml
uses: canonical/discourse-doc-checker@main
```

### Using a specific tag/release (recommended for production)
```yaml
uses: canonical/discourse-doc-checker@v1
```

### Using a specific commit (for maximum stability)
```yaml
uses: canonical/discourse-doc-checker@abc1234
```

## Setup Instructions

1. **Ensure the repository exists** at `canonical/discourse-doc-checker`
2. **Create a release/tag** (e.g., `v1`) for stable usage
3. **Use in other repositories** with the appropriate reference

## License

This action is part of the Canonical documentation toolchain.