# GitHub Actions Setup Guide

## Overview

This repository uses GitHub Actions for two tasks:

- unit-test discovery through `python -m unittest discover -s tests -p 'test_*.py'`
- code-quality checks with `flake8`, `black`, and `isort`

Both workflows trigger on pushes and pull requests targeting `master`, `main`, or `develop`.

## Included Workflows

### `tests.yml`

- Matrix: Ubuntu, macOS, Windows
- Python: 3.14
- Installs dependencies from `requirements.txt`
- Runs unit tests from `tests/test_scc_algorithms.py`
- Runs `python main.py`

### `code-quality.yml`

- Ubuntu only
- Python 3.14
- Runs `flake8`
- Checks formatting with `black --check`
- Checks import order with `isort --check-only`

## Enable the Workflows

```bash
git add .github docs/GITHUB_ACTIONS_SETUP.md GITHUB_ACTIONS_QUICK_START.md
git commit -m "Add GitHub Actions automation"
git push origin <branch-name>
```

Then open <https://github.com/GuidoBorrelli/strongly-connected-components/actions> and confirm the workflows are listed and running.

## Badge Snippets

```markdown
[![Tests](https://github.com/GuidoBorrelli/strongly-connected-components/actions/workflows/tests.yml/badge.svg)](https://github.com/GuidoBorrelli/strongly-connected-components/actions/workflows/tests.yml)
[![Code Quality](https://github.com/GuidoBorrelli/strongly-connected-components/actions/workflows/code-quality.yml/badge.svg)](https://github.com/GuidoBorrelli/strongly-connected-components/actions/workflows/code-quality.yml)
```

## Common Customizations

### Change the Python matrix

```yaml
strategy:
  matrix:
    python-version: ['3.14']
```

### Change the target branches

```yaml
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]
```

### Add another project command

```yaml
- name: Run another check
  run: python some_script.py
```

## Troubleshooting

- Workflow does not start: confirm the YAML files are in `.github/workflows/`
- CI fails but local runs pass: compare the local Python patch level against the CI Python 3.14 runner and reinstall `requirements.txt`
- The matrix is too slow: reduce OS or Python combinations

## References

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Workflow Syntax Reference](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
