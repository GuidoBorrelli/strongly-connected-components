# GitHub Actions Quick Start

This repository already includes:

- `.github/workflows/tests.yml` for unit tests and a CLI smoke test on Ubuntu, macOS, and Windows with Python 3.14
- `.github/workflows/code-quality.yml` for `flake8`, `black`, and `isort`
- issue templates and a pull request template

## Enable and Verify

1. Commit the workflow files and push your branch.
   ```bash
   git add .github docs/GITHUB_ACTIONS_SETUP.md GITHUB_ACTIONS_QUICK_START.md
   git commit -m "Add GitHub Actions automation"
   git push origin <branch-name>
   ```
2. Open <https://github.com/GuidoBorrelli/strongly-connected-components/actions>
3. Confirm that the `Tests` and `Code Quality` workflows start running

The workflows trigger on pushes and pull requests targeting `master`, `main`, or `develop`.

## Badge Snippets

```markdown
[![Tests](https://github.com/GuidoBorrelli/strongly-connected-components/actions/workflows/tests.yml/badge.svg)](https://github.com/GuidoBorrelli/strongly-connected-components/actions/workflows/tests.yml)
[![Code Quality](https://github.com/GuidoBorrelli/strongly-connected-components/actions/workflows/code-quality.yml/badge.svg)](https://github.com/GuidoBorrelli/strongly-connected-components/actions/workflows/code-quality.yml)
```

## Troubleshooting

- Workflows not running: check that the files are present in `.github/workflows/`
- CI fails but local runs pass: compare the local Python patch level against CI's Python 3.14 environment and reinstall `requirements.txt`
- Workflow is too slow: reduce the test matrix in the workflow file

For details and customization examples, see `docs/GITHUB_ACTIONS_SETUP.md`.
