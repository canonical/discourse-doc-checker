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
      - uses: canonical/doc-checker@v1
        with:
          docs-path: 'docs'
          discourse-url: 'https://discourse.charmhub.io'
          discourse-api-key: ${{ secrets.DISCOURSE_API_KEY }}
          discourse-api-user: ${{ secrets.DISCOURSE_API_USER }}
```

## Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `docs-path` | Path to documentation directory | No | `docs` |
| `discourse-url` | Discourse instance URL | No | `https://discourse.charmhub.io` |
| `discourse-api-key` | Discourse API key | No | `` |
| `discourse-api-user` | Discourse API username | No | `system` |
| `working-directory` | Working directory | No | `.` |

## What it does

1. **Converts Contents to Navigation**: Automatically converts markdown Contents sections to Navigation table format
2. **Compares with Discourse**: Fetches content from Discourse and compares formatting
3. **Reports differences**: Shows detailed diffs when documentation doesn't match
4. **Fails on differences**: Returns non-zero exit code to fail CI when issues are found

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

## Repository Structure

```
.
├── action.yml         # Action definition
├── check_docs.py     # Main Python script
├── requirements.txt  # Python dependencies
└── README.md        # This file
```

## Setup Instructions

1. **Create new repository** named `doc-checker`
2. **Add the files** from this directory
3. **Create a release/tag** (e.g., `v1`)
4. **Use in other repositories** with `uses: your-org/doc-checker@v1`

## License

This action is part of the Canonical documentation toolchain.