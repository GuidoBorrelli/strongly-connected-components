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
2. Create a topic branch.
   ```bash
   git checkout -b feature/your-change
   ```
3. Make the change and update documentation when behavior or configuration changes.
4. Run the relevant checks locally.
   ```bash
   python main.py
   ```
5. Commit and push your branch.
   ```bash
   git add <files>
   git commit -m "Describe the change"
   git push origin feature/your-change
   ```
6. Open a pull request with a clear summary of the change and any tradeoffs.

## Development Guidelines

- Follow [PEP 8](https://peps.python.org/pep-0008/)
- Prefer clear names, small functions, and straightforward control flow
- Add type hints and docstrings where they improve readability
- Update `README.md` or docs in `docs/` when user-facing behavior changes

## Testing Notes

- Correctness mode: `TEST = True`, `MEMORY_TEST = False`
- Benchmark mode: `TEST = False`
- Memory mode: `TEST = True`, `MEMORY_TEST = True`

## License

By contributing, you agree that your contributions are released under the MIT License.
