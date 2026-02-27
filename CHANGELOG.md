# Changelog

All notable changes to this project will be documented in this file.

## [2.0.0] - 2026-02-27

### Added
- **Multi-LLM Provider Support**: Native integration for SambaNova Cloud, OpenAI, and OpenRouter.
- **Dynamic Key Detection**: Auto-detects provider based on API key format.
- **Git History Engine**: New module for analyzing commit frequency and codebase hotspots.
- **Code Quality Engine**: Static analysis for documentation coverage and cyclomatic complexity.
- **Security Enhancements**: OWASP Top 10 mapping and detailed security context with fix suggestions.
- **Dependency Scanning**: Automatic CVE checks for `requirements.txt` and `package.json`.
- **License Detection**: Automatic identification of open-source licenses.
- **CLI Optimization**: Professionally formatted, emoji-free terminal output.

### Changed
- Reorganized project structure for professional GitHub distribution.
- Promoted V2 engine to the root directory for easier access.
- Updated default LLM to **GPT OSS 120B** for superior reasoning.

## [1.0.0] - 2026-02-16

### Added
- Initial release of CodeGenome.
- Basic GitHub API file streaming.
- AST-based import extraction and dependency graphing.
- Core security regex patterns.
- OpenRouter integration with Claude 3.5 Sonnet.
