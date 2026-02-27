#!/usr/bin/env python3
"""
CodeGenome: Single-File Autonomous Codebase Intelligence Engine

A powerful repository analysis tool that:
- Fetches GitHub repos via API (no cloning)
- Builds semantic dependency maps
- Performs security vulnerability scanning
- Calculates risk scores
- Provides AI-powered chat interface via OpenRouter
"""

import os
import re
import ast
import json
import base64
from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, field
from collections import defaultdict

import requests
import networkx as nx
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

console = Console()


# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class FileInfo:
    """Represents a file in the repository"""
    path: str
    content: str
    size: int
    language: str = "unknown"


@dataclass
class SecurityIssue:
    """Represents a security vulnerability"""
    severity: str  # critical, high, medium, low
    line: int
    file: str
    description: str
    code_snippet: str = ""
    fix_suggestion: str = ""
    context_before: str = ""
    context_after: str = ""


@dataclass
class AnalysisResult:
    """Complete analysis result"""
    repo_url: str
    architecture_type: str
    design_pattern: str
    entry_points: List[str] = field(default_factory=list)
    coupling_level: str = "unknown"
    scalability_risk: str = "unknown"
    dependencies: List[str] = field(default_factory=list)
    security_issues: List[SecurityIssue] = field(default_factory=list)
    risk_score: float = 0.0
    total_files: int = 0
    total_lines: int = 0
    avg_complexity: float = 0.0
    circular_dependencies: int = 0


# ============================================================================
# MODULE 1: GITHUB FETCHER
# ============================================================================

class GitHubFetcher:
    """Handles GitHub API interactions without cloning"""
    
    def __init__(self, repo_url: str, token: Optional[str] = None):
        self.repo_url = repo_url
        self.token = token or os.getenv("GITHUB_TOKEN")
        self.headers = {}
        if self.token:
            self.headers["Authorization"] = f"token {self.token}"
        
        # Parse repo owner and name
        parts = repo_url.rstrip("/").split("/")
        self.owner = parts[-2]
        self.repo = parts[-1]
        self.api_base = f"https://api.github.com/repos/{self.owner}/{self.repo}"
    
    def get_repo_tree(self, max_files: int = 500) -> List[Dict[str, Any]]:
        """Get repository file tree via GitHub API"""
        console.print(f"[cyan]Fetching repository tree for {self.owner}/{self.repo}...[/cyan]")
        
        url = f"{self.api_base}/git/trees/main?recursive=1"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 404:
            # Try 'master' branch
            url = f"{self.api_base}/git/trees/master?recursive=1"
            response = requests.get(url, headers=self.headers)
        
        if response.status_code != 200:
            raise Exception(f"Failed to fetch repo tree: {response.status_code} - {response.text}")
        
        tree = response.json().get("tree", [])
        
        # Filter only files (not directories) and limit count
        files = [item for item in tree if item["type"] == "blob"][:max_files]
        console.print(f"[green]Found {len(files)} files[/green]")
        return files
    
    def get_file_content(self, path: str) -> Optional[str]:
        """Fetch content of a specific file"""
        url = f"{self.api_base}/contents/{path}"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code != 200:
            return None
        
        data = response.json()
        if data.get("encoding") == "base64":
            try:
                content = base64.b64decode(data["content"]).decode("utf-8")
                return content
            except Exception:
                return None
        return None
    
    def fetch_code_files(self, max_files: int = 200) -> List[FileInfo]:
        """Fetch all code files from repository (multi-language support)"""
        tree = self.get_repo_tree(max_files=max_files)
        
        # Language extensions mapping
        LANGUAGE_MAP = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.java': 'java',
            '.cpp': 'cpp',
            '.c': 'c',
            '.go': 'go',
            '.rs': 'rust',
            '.rb': 'ruby',
            '.php': 'php',
            '.cs': 'csharp',
            '.swift': 'swift',
            '.kt': 'kotlin',
            '.scala': 'scala',
            '.ino': 'arduino',
            '.h': 'c_header',
            '.hpp': 'cpp_header',
            '.md': 'markdown',
            '.txt': 'text',
            '.json': 'json',
            '.yaml': 'yaml',
            '.yml': 'yaml',
            '.xml': 'xml',
            '.html': 'html',
            '.css': 'css'
        }
        
        code_files = []
        readme_files = []
        
        for item in tree:
            path = item["path"]
            ext = '.' + path.split('.')[-1] if '.' in path else ''
            
            # Check if it's a code file or README
            if ext.lower() in LANGUAGE_MAP:
                console.print(f"[dim]Fetching {path}...[/dim]")
                content = self.get_file_content(path)
                if content:
                    code_files.append(FileInfo(
                        path=path,
                        content=content,
                        size=item["size"],
                        language=LANGUAGE_MAP[ext.lower()]
                    ))
            elif 'readme' in path.lower():
                console.print(f"[dim]Fetching {path} (README)...[/dim]")
                content = self.get_file_content(path)
                if content:
                    readme_files.append(FileInfo(
                        path=path,
                        content=content,
                        size=item["size"],
                        language="markdown"
                    ))
        
        # Combine code files and READMEs
        all_files = code_files + readme_files
        console.print(f"[green]Fetched {len(code_files)} code files + {len(readme_files)} README files[/green]")
        return all_files


# ============================================================================
# MODULE 2: CODE PARSER
# ============================================================================

class CodeParser:
    """Parses code files (multi-language support)"""
    
    @staticmethod
    def parse_file(file_info: FileInfo) -> Dict[str, Any]:
        """Extract metadata from code files (language-agnostic)"""
        result = {
            "imports": [],
            "classes": [],
            "functions": [],
            "entry_point": False,
            "complexity": 0,
            "language": file_info.language
        }
        
        # Python-specific AST parsing
        if file_info.language == "python":
            try:
                tree = ast.parse(file_info.content)
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            result["imports"].append(alias.name)
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            result["imports"].append(node.module)
                    elif isinstance(node, ast.ClassDef):
                        result["classes"].append(node.name)
                    elif isinstance(node, ast.FunctionDef):
                        result["functions"].append(node.name)
                        complexity = sum(1 for _ in ast.walk(node) if isinstance(_, (ast.If, ast.For, ast.While, ast.Try)))
                        result["complexity"] += complexity
                if "__main__" in file_info.content:
                    result["entry_point"] = True
            except SyntaxError:
                pass
        
        # Generic regex-based parsing for other languages
        else:
            content = file_info.content
            
            # Detect imports (various patterns)
            import_patterns = [
                r'^import\s+([\w.]+)',  # Python, Java
                r'^from\s+([\w.]+)\s+import',  # Python
                r'#include\s*[<"]([\w./]+)[>"]',  # C/C++
                r'require\s*\(?[\'"]([\w./]+)[\'"]\)?',  # JavaScript, Ruby
                r'use\s+([\w:]+)',  # Rust, PHP
            ]
            for pattern in import_patterns:
                matches = re.findall(pattern, content, re.MULTILINE)
                result["imports"].extend(matches)
            
            # Detect classes
            class_patterns = [
                r'class\s+(\w+)',  # Python, Java, C++, JS, PHP
                r'struct\s+(\w+)',  # C, C++, Rust
                r'interface\s+(\w+)',  # Java, TypeScript
            ]
            for pattern in class_patterns:
                matches = re.findall(pattern, content)
                result["classes"].extend(matches)
            
            # Detect functions
            func_patterns = [
                r'def\s+(\w+)\s*\(',  # Python
                r'function\s+(\w+)\s*\(',  # JavaScript, PHP
                r'fn\s+(\w+)\s*\(',  # Rust
                r'func\s+(\w+)\s*\(',  # Go
                r'void\s+(\w+)\s*\(',  # C, C++, Java
                r'(public|private|protected)\s+\w+\s+(\w+)\s*\(',  # Java, C#
            ]
            for pattern in func_patterns:
                matches = re.findall(pattern, content)
                if isinstance(matches, list) and matches:
                    if isinstance(matches[0], tuple):
                        result["functions"].extend([m[-1] for m in matches])
                    else:
                        result["functions"].extend(matches)
            
            # Entry point detection
            entry_patterns = [
                r'if\s+__name__\s*==\s*[\'"]__main__[\'"]',  # Python
                r'int\s+main\s*\(',  # C, C++
                r'public\s+static\s+void\s+main',  # Java
                r'func\s+main\s*\(',  # Go
            ]
            for pattern in entry_patterns:
                if re.search(pattern, content):
                    result["entry_point"] = True
                    break
            
            # Simple complexity: count control flow keywords
            complexity_keywords = ['if', 'else', 'for', 'while', 'switch', 'case', 'try', 'catch']
            for keyword in complexity_keywords:
                result["complexity"] += len(re.findall(r'\b' + keyword + r'\b', content))
        
        return result
    
    @staticmethod
    def extract_all_metadata(files: List[FileInfo]) -> Dict[str, Dict[str, Any]]:
        """Parse all files and return metadata"""
        metadata = {}
        for file_info in files:
            metadata[file_info.path] = CodeParser.parse_file(file_info)
        return metadata


# ============================================================================
# MODULE 3: DEPENDENCY GRAPH BUILDER
# ============================================================================

class DependencyGraphBuilder:
    """Builds dependency graph using NetworkX"""
    
    @staticmethod
    def build_graph(metadata: Dict[str, Dict[str, Any]]) -> nx.DiGraph:
        """Create directed graph of file dependencies"""
        graph = nx.DiGraph()
        
        # Add all files as nodes
        for filepath in metadata.keys():
            graph.add_node(filepath)
        
        # Add edges based on imports
        for filepath, data in metadata.items():
            for imp in data["imports"]:
                # Try to match import to a file in the repo
                for other_file in metadata.keys():
                    # Simple heuristic: if import name is in file path
                    if imp.replace(".", "/") in other_file:
                        graph.add_edge(filepath, other_file)
        
        return graph
    
    @staticmethod
    def detect_circular_dependencies(graph: nx.DiGraph) -> List[List[str]]:
        """Find circular dependencies"""
        try:
            cycles = list(nx.simple_cycles(graph))
            return cycles
        except Exception:
            return []
    
    @staticmethod
    def calculate_coupling(graph: nx.DiGraph) -> str:
        """Calculate coupling level based on graph density"""
        if len(graph.nodes) == 0:
            return "unknown"
        
        density = nx.density(graph)
        if density < 0.1:
            return "low"
        elif density < 0.3:
            return "medium"
        else:
            return "high"


# ============================================================================
# MODULE 4: SECURITY SCANNER
# ============================================================================

class SecurityScanner:
    """Scans for security vulnerabilities using AST and regex"""
    
    # Security patterns with fix suggestions (pattern, description, fix_suggestion)
    PATTERNS = {
        "critical": [
            (
                r"(password|secret|api_key|token)\s*=\s*['\"][^'\"]+['\"]",
                "Hardcoded secret detected",
                "Move to environment variable: os.getenv('SECRET_NAME') or use a secrets manager"
            ),
            (
                r"(AWS_ACCESS_KEY|AWS_SECRET|GITHUB_TOKEN)\s*=\s*['\"][^'\"]+['\"]",
                "Hardcoded credential",
                "Use AWS Secrets Manager, environment variables, or .env file (never commit .env)"
            ),
        ],
        "high": [
            (
                r"\beval\s*\(",
                "Use of eval() - code injection risk",
                "Replace with ast.literal_eval() for safe evaluation or use json.loads() for JSON data"
            ),
            (
                r"\bexec\s*\(",
                "Use of exec() - code injection risk",
                "Avoid exec(). Use function calls, importlib, or refactor to eliminate dynamic code execution"
            ),
            (
                r"subprocess\.(call|run|Popen).*shell\s*=\s*True",
                "Subprocess with shell=True - command injection risk",
                "Set shell=False and pass command as list: subprocess.run(['cmd', 'arg1', 'arg2'])"
            ),
        ],
        "medium": [
            (
                r"hashlib\.(md5|sha1)\(",
                "Weak hashing algorithm (MD5/SHA1)",
                "Use hashlib.sha256() or hashlib.sha512() for cryptographic hashing"
            ),
            (
                r"CORS.*origin.*\*",
                "Open CORS policy",
                "Restrict CORS to specific domains: Access-Control-Allow-Origin: https://yourdomain.com"
            ),
            (
                r"debug\s*=\s*True",
                "Debug mode enabled in production",
                "Set debug=False in production or use environment variable: debug=os.getenv('DEBUG', False)"
            ),
        ],
        "low": [
            (
                r"def\s+\w+\([^)]*\):[^\n]*\n(?:\s{4}[^\n]*\n){200,}",
                "Large function (>200 lines)",
                "Refactor into smaller functions following Single Responsibility Principle"
            ),
        ]
    }
    
    @staticmethod
    def get_context_lines(lines: List[str], line_num: int, context_size: int = 2) -> Tuple[str, str]:
        """Get context lines before and after the issue"""
        start = max(0, line_num - context_size - 1)
        end = min(len(lines), line_num + context_size)
        
        before = "\n".join(lines[start:line_num-1]) if line_num > 1 else ""
        after = "\n".join(lines[line_num:end]) if line_num < len(lines) else ""
        
        return before, after
    
    @staticmethod
    def scan_file(file_info: FileInfo) -> List[SecurityIssue]:
        """Scan a single file for vulnerabilities with detailed context"""
        issues = []
        lines = file_info.content.split("\n")
        
        for severity, patterns in SecurityScanner.PATTERNS.items():
            for pattern_data in patterns:
                pattern, description, fix_suggestion = pattern_data
                for line_num, line in enumerate(lines, start=1):
                    if re.search(pattern, line, re.IGNORECASE):
                        context_before, context_after = SecurityScanner.get_context_lines(lines, line_num)
                        
                        issues.append(SecurityIssue(
                            severity=severity,
                            line=line_num,
                            file=file_info.path,
                            description=description,
                            code_snippet=line.strip(),
                            fix_suggestion=fix_suggestion,
                            context_before=context_before,
                            context_after=context_after
                        ))
        
        return issues
    
    @staticmethod
    def scan_all_files(files: List[FileInfo]) -> List[SecurityIssue]:
        """Scan all files for vulnerabilities"""
        all_issues = []
        for file_info in files:
            issues = SecurityScanner.scan_file(file_info)
            all_issues.extend(issues)
        return all_issues


# ============================================================================
# MODULE 5: RISK ENGINE
# ============================================================================

class RiskEngine:
    """Calculates risk scores"""
    
    SEVERITY_WEIGHTS = {
        "critical": 5,
        "high": 3,
        "medium": 2,
        "low": 1
    }
    
    @staticmethod
    def calculate_risk_score(
        security_issues: List[SecurityIssue],
        avg_complexity: float,
        circular_deps: int
    ) -> float:
        """
        Calculate risk score (0-100)
        Formula: (critical×5 + high×3 + medium×2 + low×1) + (avg_complexity/10) + (circular_deps×2)
        """
        severity_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
        for issue in security_issues:
            severity_counts[issue.severity] += 1
        
        risk = (
            severity_counts["critical"] * 5 +
            severity_counts["high"] * 3 +
            severity_counts["medium"] * 2 +
            severity_counts["low"] * 1 +
            (avg_complexity / 10) +
            (circular_deps * 2)
        )
        
        # Normalize to 0-100
        normalized = min(100, risk * 2)
        return round(normalized, 2)
    
    @staticmethod
    def get_risk_level(score: float) -> str:
        """Convert score to risk level"""
        if score >= 70:
            return "HIGH"
        elif score >= 40:
            return "MEDIUM"
        else:
            return "LOW"


# ============================================================================
# MODULE 6: LLM REASONER
# ============================================================================

class LLMReasoner:
    """Interfaces with OpenRouter for AI-powered analysis"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "anthropic/claude-3.5-sonnet"):
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY not found in environment")
        
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key
        )
        self.model = model
        self.context = ""
    
    def build_context(self, analysis: AnalysisResult, metadata: Dict[str, Dict[str, Any]]) -> str:
        """Compress repository data into structured context"""
        context_parts = [
            f"# Repository Analysis: {analysis.repo_url}",
            f"\n## Architecture",
            f"- Type: {analysis.architecture_type}",
            f"- Pattern: {analysis.design_pattern}",
            f"- Entry Points: {', '.join(analysis.entry_points) if analysis.entry_points else 'None detected'}",
            f"- Coupling: {analysis.coupling_level}",
            f"- Files: {analysis.total_files}",
            f"- Total Lines: {analysis.total_lines}",
            f"\n## Dependencies",
        ]
        
        # Extract unique dependencies
        all_deps = set()
        for data in metadata.values():
            all_deps.update(data["imports"])
        context_parts.append(f"External: {', '.join(sorted(all_deps)[:20])}")
        
        context_parts.append(f"\n## Security Overview")
        context_parts.append(f"- Risk Score: {analysis.risk_score}/100 ({RiskEngine.get_risk_level(analysis.risk_score)})")
        
        # Group issues by severity
        by_severity = {"critical": [], "high": [], "medium": [], "low": []}
        for issue in analysis.security_issues:
            by_severity[issue.severity].append(issue)
        
        for severity in ["critical", "high", "medium", "low"]:
            issues = by_severity[severity]
            if issues:
                context_parts.append(f"- {severity.upper()}: {len(issues)} issues")
                for issue in issues[:3]:  # Show first 3
                    context_parts.append(f"  - {issue.file}:{issue.line} - {issue.description}")
        
        context_parts.append(f"\n## File Structure")
        for filepath, data in list(metadata.items())[:10]:  # First 10 files
            context_parts.append(f"- {filepath}")
            if data["classes"]:
                context_parts.append(f"  Classes: {', '.join(data['classes'][:5])}")
            if data["functions"]:
                context_parts.append(f"  Functions: {', '.join(data['functions'][:5])}")
        
        self.context = "\n".join(context_parts)
        return self.context
    
    def query(self, question: str) -> str:
        """Ask LLM a question about the codebase"""
        if not self.context:
            return "Error: Context not built. Run analysis first."
        
        messages = [
            {
                "role": "system",
                "content": "You are a senior software architect analyzing a codebase. Provide concise, technical answers based on the provided context."
            },
            {
                "role": "user",
                "content": f"{self.context}\n\n---\n\nQuestion: {question}"
            }
        ]
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error querying LLM: {str(e)}"


# ============================================================================
# MODULE 7: CHAT INTERFACE
# ============================================================================

class ChatInterface:
    """Rich CLI interface for user interaction"""
    
    def __init__(self, analysis: AnalysisResult, llm: LLMReasoner):
        self.analysis = analysis
        self.llm = llm
    
    def display_summary(self):
        """Display analysis summary"""
        console.print("\n")
        console.print(Panel.fit(
            f"[bold cyan]CodeGenome Analysis Complete[/bold cyan]\n"
            f"Repository: {self.analysis.repo_url}",
            border_style="cyan"
        ))
        
        # Architecture table
        arch_table = Table(title="Architecture Summary", show_header=True)
        arch_table.add_column("Property", style="cyan")
        arch_table.add_column("Value", style="green")
        
        arch_table.add_row("Type", self.analysis.architecture_type)
        arch_table.add_row("Pattern", self.analysis.design_pattern)
        arch_table.add_row("Entry Points", ", ".join(self.analysis.entry_points) if self.analysis.entry_points else "None")
        arch_table.add_row("Coupling", self.analysis.coupling_level)
        arch_table.add_row("Files Analyzed", str(self.analysis.total_files))
        arch_table.add_row("Total Lines", str(self.analysis.total_lines))
        
        console.print(arch_table)
        
        # Security table
        risk_color = "red" if self.analysis.risk_score >= 70 else "yellow" if self.analysis.risk_score >= 40 else "green"
        
        sec_table = Table(title="Security Analysis", show_header=True)
        sec_table.add_column("Metric", style="cyan")
        sec_table.add_column("Value", style=risk_color)
        
        sec_table.add_row("Risk Score", f"{self.analysis.risk_score}/100 ({RiskEngine.get_risk_level(self.analysis.risk_score)})")
        
        # Count by severity
        by_severity = {"critical": 0, "high": 0, "medium": 0, "low": 0}
        for issue in self.analysis.security_issues:
            by_severity[issue.severity] += 1
        
        sec_table.add_row("Critical Issues", str(by_severity["critical"]))
        sec_table.add_row("High Issues", str(by_severity["high"]))
        sec_table.add_row("Medium Issues", str(by_severity["medium"]))
        sec_table.add_row("Low Issues", str(by_severity["low"]))
        
        console.print(sec_table)
        
        # Show detailed security issues
        if self.analysis.security_issues:
            console.print("\n[bold red]🔒 Security Issues (Detailed Report):[/bold red]")
            console.print("[dim]Showing top 5 issues with fix suggestions[/dim]\n")
            
            for idx, issue in enumerate(self.analysis.security_issues[:5], 1):
                severity_color = {"critical": "red", "high": "yellow", "medium": "blue", "low": "dim"}[issue.severity]
                
                console.print(f"\n[bold {severity_color}]Issue #{idx}: {issue.severity.upper()}[/bold {severity_color}]")
                console.print(f"[cyan]📁 File:[/cyan] {issue.file}")
                console.print(f"[cyan]📍 Line:[/cyan] {issue.line}")
                console.print(f"[cyan]⚠️  Problem:[/cyan] {issue.description}")
                
                # Show code context
                if issue.context_before:
                    console.print(f"\n[dim]Context (before):[/dim]")
                    for line in issue.context_before.split("\n"):
                        console.print(f"  [dim]{line}[/dim]")
                
                console.print(f"\n[bold {severity_color}]→ Line {issue.line}:[/bold {severity_color}] {issue.code_snippet}")
                
                if issue.context_after:
                    console.print(f"\n[dim]Context (after):[/dim]")
                    for line in issue.context_after.split("\n"):
                        console.print(f"  [dim]{line}[/dim]")
                
                console.print(f"\n[green]✅ Fix Suggestion:[/green]")
                console.print(f"  {issue.fix_suggestion}")
                console.print("[dim]" + "─" * 80 + "[/dim]")
    
    def chat_loop(self):
        """Interactive chat loop"""
        console.print("\n[bold green]Chat Mode Enabled[/bold green]")
        console.print("[dim]Ask questions about the codebase. Type 'exit' to quit.[/dim]\n")
        
        while True:
            try:
                question = console.input("[bold cyan]You:[/bold cyan] ")
                if question.lower() in ["exit", "quit", "q"]:
                    console.print("[yellow]Goodbye![/yellow]")
                    break
                
                if not question.strip():
                    continue
                
                console.print("[dim]Thinking...[/dim]")
                answer = self.llm.query(question)
                console.print(f"[bold green]AI:[/bold green] {answer}\n")
            
            except KeyboardInterrupt:
                console.print("\n[yellow]Goodbye![/yellow]")
                break
            except Exception as e:
                console.print(f"[red]Error: {e}[/red]")


# ============================================================================
# MAIN PIPELINE
# ============================================================================

def analyze_repository(repo_url: str, max_files: int = 200) -> Tuple[AnalysisResult, Dict[str, Dict[str, Any]], LLMReasoner]:
    """Main analysis pipeline (multi-language support)"""
    
    # Step 1: Fetch files
    fetcher = GitHubFetcher(repo_url)
    files = fetcher.fetch_code_files(max_files=max_files)
    
    if not files:
        raise Exception("No code files found in repository")
    
    # Step 2: Parse code
    console.print("[cyan]Parsing code files...[/cyan]")
    metadata = CodeParser.extract_all_metadata(files)
    
    # Step 2.5: Extract architecture from README files
    readme_content = ""
    for f in files:
        if f.language == "markdown" and "readme" in f.path.lower():
            readme_content += f.content + "\n"
    
    # Step 3: Build dependency graph
    console.print("[cyan]Building dependency graph...[/cyan]")
    graph = DependencyGraphBuilder.build_graph(metadata)
    cycles = DependencyGraphBuilder.detect_circular_dependencies(graph)
    coupling = DependencyGraphBuilder.calculate_coupling(graph)
    
    # Step 4: Security scan
    console.print("[cyan]Scanning for security vulnerabilities...[/cyan]")
    security_issues = SecurityScanner.scan_all_files(files)
    
    # Step 5: Calculate metrics
    total_lines = sum(len(f.content.split("\n")) for f in files)
    avg_complexity = sum(m["complexity"] for m in metadata.values()) / len(metadata) if metadata else 0
    
    # Detect architecture from README
    arch_type = "Unknown"
    pattern = "Unknown"
    
    if readme_content:
        readme_lower = readme_content.lower()
        # Architecture detection from README
        if "microservice" in readme_lower:
            arch_type = "Microservices"
            pattern = "Distributed Services"
        elif "monolith" in readme_lower:
            arch_type = "Monolithic"
            pattern = "Single Application"
        elif "iot" in readme_lower or "embedded" in readme_lower:
            arch_type = "IoT/Embedded System"
            pattern = "Hardware Integration"
        elif "api" in readme_lower and "rest" in readme_lower:
            arch_type = "RESTful API"
            pattern = "Client-Server"
        elif "web" in readme_lower or "frontend" in readme_lower:
            arch_type = "Web Application"
            pattern = "MVC/Component-Based"
    
    # Fallback: Detect from file structure
    entry_points = [path for path, data in metadata.items() if data["entry_point"]]
    
    if arch_type == "Unknown":
        # Count languages
        languages = set(m["language"] for m in metadata.values())
        
        if len(files) == 1:
            arch_type = "Single File Script"
            pattern = "Procedural"
        elif len(files) < 10:
            arch_type = "Small Modular Project"
            pattern = "Functional/OOP Mix"
        elif "arduino" in languages or "c" in languages:
            arch_type = "Embedded/IoT System"
            pattern = "Hardware Control"
        else:
            arch_type = "Multi-Module Application"
            pattern = "Layered Architecture"
    
    # Step 6: Risk scoring
    risk_score = RiskEngine.calculate_risk_score(security_issues, avg_complexity, len(cycles))
    
    # Build result
    result = AnalysisResult(
        repo_url=repo_url,
        architecture_type=arch_type,
        design_pattern=pattern,
        entry_points=entry_points,
        coupling_level=coupling,
        scalability_risk="Medium" if len(files) < 20 else "Low",
        dependencies=list(set(imp for m in metadata.values() for imp in m["imports"]))[:20],
        security_issues=security_issues,
        risk_score=risk_score,
        total_files=len(files),
        total_lines=total_lines,
        avg_complexity=avg_complexity,
        circular_dependencies=len(cycles)
    )
    
    # Step 7: Initialize LLM
    console.print("[cyan]Initializing LLM...[/cyan]")
    llm = LLMReasoner()
    llm.build_context(result, metadata)
    
    return result, metadata, llm


def main():
    """Main entry point"""
    console.print(Panel.fit(
        "[bold cyan]CodeGenome[/bold cyan]\n"
        "[dim]Single-File Autonomous Codebase Intelligence Engine[/dim]",
        border_style="cyan"
    ))
    
    # Get repository URL
    repo_url = console.input("\n[bold]Enter GitHub repository URL:[/bold] ").strip()
    
    if not repo_url:
        console.print("[red]Error: Repository URL required[/red]")
        return
    
    try:
        # Run analysis
        analysis, metadata, llm = analyze_repository(repo_url)
        
        # Display results
        interface = ChatInterface(analysis, llm)
        interface.display_summary()
        
        # Start chat
        interface.chat_loop()
    
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
