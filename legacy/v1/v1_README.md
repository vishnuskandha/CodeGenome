# CodeGenome 🧬

> 🚨 **MAJOR UPGRADE: V2 IS NOW AVAILABLE!** 🚨
> We highly recommend using **CodeGenome v2** located in the `codegenome_v2/` directory.
> v2 features Git history analysis, multi-provider fast LLM support (SambaNova, OpenAI, OpenRouter), dependency vulnerability scanning, and license detection.
> 👉 **[Go to CodeGenome v2 README](codegenome_v2/README.md)**

**Single-File Autonomous Codebase Intelligence Engine**

Analyze any GitHub repository without cloning - get architecture insights, security analysis, and AI-powered chat in seconds.

---

## ✨ Features

- 🚀 **No Cloning Required** - Streams files via GitHub API
- 🏗️ **Architecture Analysis** - Detects design patterns, coupling, entry points
- 🔒 **Security Scanning** - Finds vulnerabilities with severity ranking
- 📊 **Risk Scoring** - Quantified 0-100 risk assessment
- 🤖 **AI Chat** - Ask questions about the codebase via OpenRouter
- 📈 **Dependency Graphs** - Visualizes module relationships

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set API Key
```bash
# Windows PowerShell
$env:OPENROUTER_API_KEY="sk-or-v1-..."

# Linux/Mac
export OPENROUTER_API_KEY="sk-or-v1-..."
```

Or create a `.env` file:
```
OPENROUTER_API_KEY=sk-or-v1-...
```

### 3. Run Analysis
```bash
python codegenome.py
```

Enter a GitHub repository URL when prompted (e.g., `https://github.com/pallets/flask`)

---

## 📖 Example Output

```
╭─────────────────────────────────────────╮
│ CodeGenome Analysis Complete            │
│ Repository: https://github.com/user/repo│
╰─────────────────────────────────────────╯

Architecture Summary
┏━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Property     ┃ Value                  ┃
┡━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Type         │ Multi-Module           │
│ Pattern      │ Layered Architecture   │
│ Entry Points │ main.py, app.py        │
│ Coupling     │ medium                 │
│ Files        │ 42                     │
│ Total Lines  │ 8,432                  │
└──────────────┴────────────────────────┘

Security Analysis
┏━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┓
┃ Metric          ┃ Value        ┃
┡━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━┩
│ Risk Score      │ 68/100 (MED) │
│ Critical Issues │ 1            │
│ High Issues     │ 3            │
│ Medium Issues   │ 5            │
│ Low Issues      │ 12           │
└─────────────────┴──────────────┘

Top Security Issues:
  CRITICAL config.py:45 - Hardcoded secret detected
  HIGH utils.py:89 - Use of eval() - code injection risk
  HIGH db.py:120 - SQL string concatenation
```

---

## 💬 Chat Examples

```
You: Where is authentication handled?
AI: Authentication logic is in auth.py, specifically in the verify_user() 
    function (lines 34-67). It uses JWT tokens but stores the secret key 
    in plain text in config.py line 45.

You: Is this scalable?
AI: The architecture shows medium coupling with 42 modules. The main 
    bottleneck is the synchronous database calls in db.py. Consider 
    implementing async/await patterns for better scalability.

You: Find security risks
AI: Found 21 total issues. Most critical: hardcoded API key in config.py. 
    Also detected 3 instances of eval() usage which pose code injection 
    risks. Recommend moving secrets to environment variables and replacing 
    eval() with ast.literal_eval().
```

---

## 🏗️ Architecture

### Internal Modules (Single File Design)

```python
class GitHubFetcher:           # GitHub API interaction
class CodeParser:              # AST parsing, import extraction  
class DependencyGraphBuilder:  # NetworkX graph construction
class SecurityScanner:         # Vulnerability detection
class RiskEngine:              # Risk scoring algorithm
class LLMReasoner:             # OpenRouter integration
class ChatInterface:           # Rich CLI interface
```

### Data Flow
```
User Input → GitHub API → File Streaming → AST Parsing → 
Security Scan → Dependency Graph → Risk Calculation → 
LLM Context Compression → Interactive Chat
```

---

## 🔒 Security Detection

### Vulnerability Patterns

**Critical**:
- Hardcoded secrets (API keys, passwords, tokens)
- Hardcoded credentials (AWS, GitHub)

**High**:
- `eval()` / `exec()` usage
- `subprocess` with `shell=True`

**Medium**:
- Weak hashing (MD5, SHA1)
- Open CORS policies
- Debug mode in production

**Low**:
- Large functions (>200 lines)
- Code complexity issues

### Risk Scoring Formula
```
risk = (critical × 5) + (high × 3) + (medium × 2) + (low × 1) +
       (avg_complexity / 10) + (circular_dependencies × 2)
```
Normalized to 0-100 scale.

---

## 🔧 Configuration

### Environment Variables
- `OPENROUTER_API_KEY` - Required for AI chat
- `GITHUB_TOKEN` - Optional, increases API rate limits

### Customization
Edit `codegenome.py`:
- Line 474: Change LLM model (default: `anthropic/claude-3.5-sonnet`)
- Line 107: Adjust max files to fetch (default: 100)
- Line 289: Modify security patterns

---

## 🤝 RalphLoop Integration

CodeGenome works alongside **RalphLoop** (autonomous AI agent for Antigravity):

### Setup RalphLoop
1. Install Antigravity (VS Code fork)
2. Install "Ralph Loop Pro" extension
3. Create `task.md`:
```markdown
- [ ] Analyze https://github.com/user/repo with CodeGenome
- [ ] Save report to reports/analysis.json
- [ ] If risk > 70, create GitHub issue
```

4. Configure RalphLoop sidebar:
   - Task file: `task.md`
   - Model: OpenRouter (same API key)
   - Max iterations: 10

---

## 📊 Use Cases

### Code Review
```bash
python codegenome.py
# Enter PR branch URL
# Review security issues before merge
```

### Security Audit
```bash
python codegenome.py
# Analyze production repo
# Export risk report
```

### Architecture Research
```bash
python codegenome.py
# Compare design patterns across repos
# Study dependency structures
```

---

## 🎓 Academic Value

### Research Contributions
- **Context Compression**: 10:1 ratio for LLM efficiency
- **Static Analysis**: AST-based vulnerability detection
- **Graph Modeling**: Dependency cycle detection
- **Risk Quantification**: Normalized scoring algorithm

### Viva Defense Points
> "Why single file?"
> 
> Demonstrates architectural abstraction within minimal implementation surface. 
> Focus is on intelligence pipeline, not scaffolding. Modular classes simulate 
> microservices within a monolith.

> "How does this differ from SonarQube?"
>
> SonarQube focuses on linting and code quality. CodeGenome provides semantic 
> understanding via LLM integration, enabling natural language queries about 
> architecture and security.

---

## 🛠️ Troubleshooting

### API Rate Limits
- Set `GITHUB_TOKEN` environment variable
- Reduce `max_files` parameter

### LLM Errors
- Verify `OPENROUTER_API_KEY` is valid
- Check OpenRouter credits at [openrouter.ai](https://openrouter.ai)
- Try alternative model (edit line 474)

### No Python Files Found
- Ensure repository contains `.py` files
- Check repository is public or token has access

---

## 📝 License

MIT License - Free for academic and commercial use

---

## 🙏 Credits

Built with:
- [requests](https://requests.readthedocs.io/) - HTTP library
- [networkx](https://networkx.org/) - Graph algorithms
- [rich](https://rich.readthedocs.io/) - Terminal formatting
- [openai](https://github.com/openai/openai-python) - LLM client
- [OpenRouter](https://openrouter.ai/) - Multi-model API

---

**Made with 🧬 by CodeGenome**
