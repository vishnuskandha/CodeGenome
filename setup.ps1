# CodeGenome Setup Script (Windows)
Write-Host "🧬 CodeGenome v2 Setup" -ForegroundColor Cyan

# 1. Check Python
if (!(Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Python not found. Please install Python 3.8+ from python.org" -ForegroundColor Red
    exit 1
}

# 2. Install Dependencies
Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
python -m pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Dependency installation failed. Fix the pip error above and run setup again." -ForegroundColor Red
    exit $LASTEXITCODE
}

# 3. Setup .env
if (!(Test-Path .env)) {
    Write-Host "📝 Creating .env from template..." -ForegroundColor Yellow
    if (Test-Path .env.example) {
        Copy-Item .env.example .env
    } else {
        @(
            "OPENROUTER_API_KEY="
            "SAMBANOVA_API_KEY="
            "OPENAI_API_KEY="
            "GITHUB_TOKEN="
        ) | Set-Content .env
    }
    Write-Host "✅ .env created. Please add your API keys to it!" -ForegroundColor Green
} else {
    Write-Host "✅ .env file exists." -ForegroundColor Green
}

Write-Host "`n🚀 Setup complete! Run 'python codegenome_v2.py' to start." -ForegroundColor Green
