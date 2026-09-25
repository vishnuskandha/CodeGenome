# CodeGenome


<!-- README polish: repository metadata badges -->
<p>
  <a href="https://github.com/vishnuskandha/CodeGenome"><img alt="GitHub stars" src="https://img.shields.io/github/stars/vishnuskandha/CodeGenome?style=for-the-badge&logo=github&label=Stars"></a>
  <a href="https://github.com/vishnuskandha/CodeGenome/fork"><img alt="GitHub forks" src="https://img.shields.io/github/forks/vishnuskandha/CodeGenome?style=for-the-badge&logo=github&label=Forks"></a>
  <a href="https://github.com/vishnuskandha/CodeGenome/issues"><img alt="GitHub issues" src="https://img.shields.io/github/issues/vishnuskandha/CodeGenome?style=for-the-badge&logo=github&label=Issues"></a>
  <a href="https://github.com/vishnuskandha/CodeGenome/commits"><img alt="Last commit" src="https://img.shields.io/github/last-commit/vishnuskandha/CodeGenome?style=for-the-badge&logo=git&label=Updated"></a>
</p>
<!-- End README polish -->

[![CI](https://github.com/vishnuskandha/CodeGenome/actions/workflows/ci.yml/badge.svg)](https://github.com/vishnuskandha/CodeGenome/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Made by Vishnu Skandha](https://img.shields.io/badge/Author-Vishnu%20Skandha-blue.svg)](https://github.com/vishnuskandha)

CodeGenome is a single-file Python CLI that analyzes a GitHub repository and reports its architecture, code quality, security posture, and dependencies, then lets you ask an LLM questions about the codebase.

It works against any public GitHub repository by using the GitHub API (no full clone required; a shallow clone is used only for Git history analysis).

## Features

- **GitHub API fetching** — pulls the file tree and contents of up to 500 files without cloning
- **Multi-language parsing** — AST parsing for Python plus regex-based parsing for JavaScript, TypeScript, Java, C/C++, Go, Rust, Ruby, PHP, C#, Swift, Kotlin, Scala, Arduino, HTML, CSS, and more
- **Dependency graph** — NetworkX-based import/dependency graph with circular-dependency detection and coupling scoring
- **Security scanning** — regex- and heuristic-based checks mapped to OWASP Top 10 categories, with line-level context and fix suggestions
- **Risk scoring** — 0–100 risk score weighted by issue severity, complexity, and circular dependencies
- **Git history analysis** — commit frequency, contributor breakdown, and most-changed files (hotspots) from a shallow clone
- **Code quality scoring** — documentation coverage, naming conventions, complexity, and test-file detection
- **Dependency vulnerability scan** — flags outdated or unpinned packages in `requirements.txt` and `package.json`
- **License detection** — recognizes common licenses (MIT, Apache-2.0, GPL-3.0, BSD, ISC)
- **LLM chat interface** — ask questions about the analyzed codebase via SambaNova Cloud, OpenRouter, or OpenAI

## Repository layout

```
.
├── codegenome_v2.py          # Main CLI (v2 engine)
├── requirements.txt          # Python dependencies
├── setup.sh                  # Setup for Linux/macOS
├── setup.ps1                 # Setup for Windows
├── API_KEY_GUIDE.md          # Guide: LLM provider API keys
├── GITHUB_TOKEN_GUIDE.md     # Guide: GitHub personal access token
├── CHANGELOG.md              # Version history
└── legacy/
    └── v1/                   # Original v1 codebase (kept for reference)
```

## Installation

Requires Python 3.8+.

```bash
pip install -r requirements.txt
```

Or use the setup script:

- Windows: `powershell -ExecutionPolicy Bypass -File setup.ps1`
- Linux/macOS: `bash setup.sh`

## Configuration

CodeGenome reads credentials from environment variables or a `.env` file in the repo root. The setup scripts create `.env` for you; never commit it.

Required:

| Variable | Purpose |
|----------|---------|
| `GITHUB_TOKEN` | GitHub personal access token (avoids 60/hour rate limits; only needs `public_repo` scope). See [GITHUB_TOKEN_GUIDE.md](GITHUB_TOKEN_GUIDE.md). |

One of the following LLM provider keys (checked in this order):

| Variable | Provider | Default model |
|----------|----------|---------------|
| `OPENROUTER_API_KEY` | OpenRouter | `openai/gpt-oss-120b` |
| `SAMBANOVA_API_KEY` | SambaNova Cloud | `Meta-Llama-3.1-70B-Instruct` |
| `OPENAI_API_KEY` | OpenAI | `gpt-4o-mini` |

See [API_KEY_GUIDE.md](API_KEY_GUIDE.md) for provider-specific setup steps.

## Usage

```bash
python codegenome_v2.py
```

Enter the GitHub repository URL when prompted, for example `https://github.com/flask/flask`. CodeGenome then:

1. Fetches and parses the repository
2. Builds the dependency graph and detects cycles
3. Scans for security issues and computes the risk score
4. Runs Git history, quality, dependency, and license analysis
5. Initializes the LLM and starts an interactive chat about the codebase

Type `exit` (or `quit` / `q`) to leave the chat.

## Reporting output

Results are rendered in the terminal with tables for architecture, Git history, code quality, security, dependency vulnerabilities, and license detection, followed by the top security issues with context and fix suggestions.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for setup, branching, and pull request guidelines.

## Security

Found a vulnerability or an issue with how tokens are handled? See [SECURITY.md](SECURITY.md).

## License

MIT License — see [LICENSE](LICENSE).
