#!/bin/bash
echo "🧬 CodeGenome v2 Setup"

# 1. Check Python
if ! command -v python3 &> /dev/null
then
    echo "❌ Python3 could not be found. Please install Python 3.8+"
    exit 1
fi

# 2. Install Dependencies
echo "📦 Installing dependencies..."
python3 -m pip install -r requirements.txt

# 3. Setup .env
if [ ! -f .env ]; then
    echo "📝 Creating .env from template..."
    if [ -f .env.example ]; then
        cp .env.example .env
    else
        cat > .env <<EOF
OPENROUTER_API_KEY=
SAMBANOVA_API_KEY=
OPENAI_API_KEY=
GITHUB_TOKEN=
EOF
    fi
    echo "✅ .env created. Please add your API keys!"
else
    echo "✅ .env file exists."
fi

echo -e "\n🚀 Setup complete! Run 'python3 codegenome_v2.py' to start."
