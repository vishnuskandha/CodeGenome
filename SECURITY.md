# Security Policy

## Supported versions

| Version | Supported |
|---------|-----------|
| 2.0.x   | Yes       |

## Reporting a vulnerability

If you discover a security issue in this repository, do **not** open a public issue. Report it privately by emailing the maintainer (see the author in [README.md](README.md) or the GitHub profile), or by opening a draft GitHub Security Advisory via the repository's **Security** tab.

Please include:

- A description of the vulnerability and its impact
- Steps to reproduce, including any relevant files or commands
- The version(s) affected

You should receive a response within a few business days. After triage, the issue is fixed on a private branch and released, and the report is credited (unless you prefer to remain anonymous).

## Token handling

This tool requires API credentials to function, so keep the following rules in mind:

- **Never commit credentials.** API keys and tokens live only in `.env` or environment variables. `.gitignore` already excludes `.env`, `.env.*`, `*.key`, `*.pem`, and related secret files.
- Only give your GitHub token the `public_repo` scope — no more than necessary (see [GITHUB_TOKEN_GUIDE.md](GITHUB_TOKEN_GUIDE.md)).
- If you believe a token has been exposed (for example, pushed to a public repo), revoke it immediately in GitHub or the provider dashboard and generate a new one.
- The code only reads tokens from the environment via `os.getenv` and `load_dotenv()`; it never writes them back to disk.

## Security notes

- The tool runs local code-quality checks (pylint/radon) and shallow-clones target repositories; only analyze repositories you trust.
- The dependency scan uses static heuristics rather than a live CVE feed; treat its results as advisory.
