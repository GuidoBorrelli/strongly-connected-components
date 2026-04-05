# Contributing to Strongly Connected Components

## Reporting Bugs

- Check existing issues first: <https://github.com/GuidoBorrelli/strongly-connected-components/issues>
- When opening a new issue, include the steps to reproduce, expected behavior, actual behavior, and your Python/OS details

## Submitting Changes

1. Fork the repository, then clone the branch you want to work on.
   ```bash
   git clone https://github.com/<your-user>/strongly-connected-components.git
   cd strongly-connected-components
   ```
2. Use Python 3.14.3 locally.
   ```bash
   python3.14 -m venv .venv
   source .venv/bin/activate
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```
3. Create a topic branch.
   ```bash
   git checkout -b feature/your-change
   ```
4. Make the change and update documentation when behavior or configuration changes.
5. Run the relevant checks locally.
   ```bash
   python -m unittest discover -s tests -p 'test_*.py'
   python main.py
   ```
6. Commit and push your branch.
   ```bash
   git add <files>
   git commit -m "Describe the change"
   git push origin feature/your-change
   ```
7. Open a pull request with a clear summary of the change and any tradeoffs.

## Development Guidelines

- Follow [PEP 8](https://peps.python.org/pep-0008/)
- Prefer clear names, small functions, and straightforward control flow
- Keep the code compatible with Python 3.14 only
- Add type hints and docstrings where they improve readability
- Update `README.md` or docs in `docs/` when user-facing behavior changes

## Testing Notes

- Python target: 3.14.3 locally, latest 3.14 patch in CI
- Python versions earlier than 3.14 are unsupported for contributions and bug reports
- Correctness mode: `TEST = True`, `MEMORY_TEST = False`
- Benchmark mode: `TEST = False`
- Memory mode: `TEST = True`, `MEMORY_TEST = True`

## License

By contributing, you agree that your contributions are released under the MIT License.
