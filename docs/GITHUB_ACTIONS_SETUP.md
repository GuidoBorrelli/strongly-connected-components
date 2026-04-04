# GitHub Actions Setup Guide

## Overview

This project uses GitHub Actions for automated testing and code quality checks. Every push and pull request automatically runs tests to ensure code quality and correctness.

## Workflows Included

### 1. **Tests Workflow** (`.github/workflows/tests.yml`)
- **Triggers**: On every push and pull request
- **Matrix Testing**:
  - Operating Systems: Ubuntu, macOS, Windows
  - Python Versions: 3.8, 3.9, 3.10, 3.11
- **What it does**:
  - Sets up Python environment
  - Installs dependencies from `requirements.txt`
  - Runs correctness tests (`python main.py`)
  - Runs 3 iterations of tests for reliability

### 2. **Code Quality Workflow** (`.github/workflows/code-quality.yml`)
- **Triggers**: On every push and pull request
- **What it does**:
  - Checks code style with **flake8**
  - Checks formatting with **black**
  - Checks import ordering with **isort**
  - Continues on errors (warnings don't block PRs)

## Manual Setup (If Not Auto-Enabled)

### Step 1: Files are Already Created
The workflow files are already in place:
```
.github/
├── workflows/
│   ├── tests.yml
│   └── code-quality.yml
├── ISSUE_TEMPLATE/
│   ├── bug_report.yml
│   └── feature_request.yml
└── PULL_REQUEST_TEMPLATE.md
```

### Step 2: Push to GitHub
```bash
git add .github/
git commit -m "Add GitHub Actions workflows"
git push origin master
```

### Step 3: GitHub Automatically Enables Actions
- Go to your repository on GitHub
- Click **Actions** tab
- You should see your workflows listed
- They will run automatically on next push/PR

## Viewing Workflow Results

### On GitHub
1. Go to your repository
2. Click **Actions** tab
3. Select a workflow run to see details
4. Drill down to see individual test results

### Badge in README
Add workflow status badges to your README:

```markdown
[![Tests](https://github.com/yourusername/strongly-connected-components/workflows/Tests/badge.svg)](https://github.com/yourusername/strongly-connected-components/actions)
[![Code Quality](https://github.com/yourusername/strongly-connected-components/workflows/Code%20Quality/badge.svg)](https://github.com/yourusername/strongly-connected-components/actions)
```

## Customizing Workflows

### Modify Python Versions
Edit `.github/workflows/tests.yml`:
```yaml
matrix:
  python-version: ['3.9', '3.10', '3.11']  # Add/remove versions
```

### Modify Operating Systems
```yaml
matrix:
  os: [ubuntu-latest, macos-latest, windows-latest]
```

### Add Additional Tests
```yaml
- name: Run benchmarks
  run: |
    python main.py
  env:
    TEST: False  # Run benchmarks instead
```

### Skip Workflows for Certain Commits
Add `[skip ci]` to your commit message:
```bash
git commit -m "Update README [skip ci]"
```

## GitHub Issue Templates

### How They Work
When a user clicks "New Issue", they'll see options:
- **Bug Report**: For reporting issues
- **Feature Request**: For suggesting improvements

### Using Them
Templates are automatically available when users create issues on GitHub. No additional setup needed!

## Pull Request Template

### How It Works
When users create a PR, they'll see the template with checkboxes and guidelines.

### Customize
Edit `.github/PULL_REQUEST_TEMPLATE.md` to add your own guidelines.

## Best Practices

### For Developers
1. ✅ Make sure tests pass locally before pushing
2. ✅ Run `python main.py` to verify
3. ✅ Keep commits clean and focused
4. ✅ Update documentation with your changes

### For Project Maintainers
1. ✅ Monitor the Actions tab regularly
2. ✅ Review workflow logs if tests fail
3. ✅ Update workflows as project evolves
4. ✅ Keep Python versions current

## Troubleshooting

### Workflow Not Running
1. Check that files are in `.github/workflows/` directory
2. Verify YAML syntax (use online YAML validator)
3. Go to Actions tab and check for errors
4. Try force-pushing a change to trigger workflows

### Tests Failing in CI but Passing Locally
1. Check Python version differences
2. Check OS-specific issues (paths, dependencies)
3. Review environment variables
4. Check for missing dependencies in `requirements.txt`

### Workflow Runs Too Long
1. Reduce number of Python versions tested
2. Reduce number of OS tested
3. Remove code quality checks if not needed
4. Consider splitting into multiple smaller jobs

## Advanced: Custom Actions

You can add more sophisticated workflows. Examples:

### Automated Changelog Generation
```yaml
- name: Generate changelog
  uses: actions/create-release@v1
```

### Code Coverage Reports
```yaml
- name: Upload coverage
  uses: codecov/codecov-action@v3
```

### Automated Releases
```yaml
- name: Create Release
  uses: actions/create-release@v1
  if: startsWith(github.ref, 'refs/tags/')
```

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Workflow Syntax Reference](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [Marketplace Actions](https://github.com/marketplace?type=actions)
- [GitHub Actions Best Practices](https://docs.github.com/en/actions/guides)

## Next Steps

1. ✅ Commit and push `.github/` directory
2. ✅ Monitor the Actions tab for workflow runs
3. ✅ Add workflow badges to README
4. ✅ Enable GitHub Discussions
5. ✅ Consider adding code coverage tracking

