# CodeGenome v2 — Enhanced Codebase Intelligence

> **Multi-dimensional repository analysis with Git history, quality scoring, and AI-powered insights**

---

## 🆕 What's New in v2

| Feature | Description |
|---------|-------------|
| 🔄 **Git History Analysis** | Commit frequency, contributor patterns, code hotspots |
| 📈 **Code Quality Scoring** | Documentation coverage, naming conventions, complexity metrics |
| 🧪 **Test Coverage Estimation** | Automatic test file detection and coverage estimates |
| 🔗 **Dependency Vulnerability Scan** | CVE checks for `requirements.txt` and `package.json` |
| 📜 **License Detection** | Automatic license identification (MIT, Apache, GPL, etc.) |
| 🛡️ **OWASP Mapping** | Security issues mapped to OWASP Top 10 categories |

---

## 📦 Installation

```bash
cd codegenome_v2
pip install -r requirements.txt
```

### New Dependencies
- `GitPython` — Git history analysis
- `pylint` — Code quality linting
- `radon` — Complexity metrics
- `osv` — CVE vulnerability database

---

## 🚀 Usage

```bash
python codegenome_v2.py
# Enter: https://github.com/user/repo
```

---

## 📊 Enhanced Output

### Git Analysis
```
Git History:
├─ Total Commits: 1,234
├─ Contributors: 15
├─ Top Contributor: Alice (45%)
└─ Hotspots (most changed):
   1. src/core.py (89 changes)
   2. tests/test_main.py (67 changes)
```

### Code Quality
```
Quality Score: 78.5/100
├─ Documentation Coverage: 65%
├─ Naming Conventions: 92%
├─ Complexity Score: 85%
└─ Test Coverage Estimate: 45% (12 test files)
```

### Dependency Vulnerabilities
```
Dependency Issues: 3
├─ requirements.txt: Django==1.11 (outdated)
├─ package.json: lodash@* (unpinned version)
└─ Recommendation: Update to latest secure versions
```

### License Info
```
License: MIT
File: LICENSE
Compatible: ✅ Yes
```

---

## 🔧 Configuration

Edit `.env`:
```env
# Choose ONE of the following AI Providers (Checked in this order):
OPENROUTER_API_KEY=sk-or-v1-your-key-here     # Uses openai/gpt-oss-120b
SAMBANOVA_API_KEY=your-uuid-format-key-here   # Uses Meta-Llama-3.1-70B-Instruct
OPENAI_API_KEY=sk-proj-your-key-here          # Uses gpt-4o-mini

# GitHub Token (REQUIRED to avoid 403 Rate Limit errors)
GITHUB_TOKEN=ghp_your-token-here
```
> **Detailed Guides:** See [API_KEY_GUIDE.md](./API_KEY_GUIDE.md) and [GITHUB_TOKEN_GUIDE.md](./GITHUB_TOKEN_GUIDE.md) for setup help.

---

## 📈 Comparison: v1 vs v2

| Feature | v1 | v2 |
|---------|----|----|
| Multi-language support | ✅ | ✅ |
| Security scanning | ✅ | ✅ Enhanced |
| Git history analysis | ❌ | ✅ |
| Code quality scoring | ❌ | ✅ |
| Dependency CVE checks | ❌ | ✅ |
| License detection | ❌ | ✅ |
| Test coverage estimation | ❌ | ✅ |

---

## 🎯 Use Cases

1. **Pre-commit Analysis** — Check quality before pushing
2. **Code Review** — Comprehensive review metrics
3. **Security Audit** — Find vulnerabilities + dependency issues
4. **Technical Debt** — Identify hotspots and complexity
5. **License Compliance** — Verify license compatibility

---

## 📝 Example Output

```
╭──────────────────────────────────────╮
│ CodeGenome v2 Analysis Complete      │
│ Repository: flask/flask              │
╰──────────────────────────────────────╯

Architecture Summary
┏━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┓
┃ Property       ┃ Value            ┃
┡━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━┩
│ Type           │ Web Framework    │
│ Quality Score  │ 78.5/100         │
│ Risk Score     │ 35/100 (LOW)     │
│ License        │ BSD-3-Clause     │
│ Contributors   │ 15               │
└────────────────┴──────────────────┘
```

---

## 🤝 Contributing

Found a bug? Want a feature? Open an issue or PR!

---

## 📄 License

MIT License — Free for academic and commercial use.
