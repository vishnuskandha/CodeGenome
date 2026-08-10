# Contributing to CodeGenome

Thanks for your interest in contributing to CodeGenome, the codebase analysis and LLM chat CLI.

## Getting started

1. Fork the repository and clone your fork.
2. Create a feature branch from `main`:

   ```bash
   git checkout -b feature/your-change
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file (see [GITHUB_TOKEN_GUIDE.md](GITHUB_TOKEN_GUIDE.md) and [API_KEY_GUIDE.md](API_KEY_GUIDE.md)). `.env` is gitignored — never commit it.

## Development workflow

- Keep changes focused and atomic; one logical change per pull request.
- Follow PEP 8 style for Python and keep the existing code conventions.
- Run a syntax check before committing:

  ```bash
  python -m compileall -q .
  ```

- Test against a small, public repository to verify output still renders correctly.
- Update [CHANGELOG.md](CHANGELOG.md) under an appropriate heading when you add or change behavior.

## Committing

- Use clear, imperative commit messages (for example: `Add support for new provider detection`).
- Make sure no API keys, tokens, or `.env` files end up in your commits. Run `git status` before `git add` and stage only intended files.

## Pull requests

- Open your PR against `main` with a description of the change and, where relevant, what you verified.
- CI installs `requirements.txt` and runs a syntax check; make sure it passes.
- Reference any related issue in the PR description.

## Reporting bugs and requesting features

Use the issue template in `.github/ISSUE_TEMPLATE/` for bug reports. For security issues, follow [SECURITY.md](SECURITY.md) instead.
