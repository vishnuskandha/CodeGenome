# Dynamic API Key Handling — Implementation Guide

## Overview

CodeGenome v2 now supports **SambaNova Cloud, OpenRouter, and OpenAI** API keys with automatic detection and intelligent fallback.

---

## How It Works

### 1. API Key Detection

The system checks for API keys in this order:

```python
api_key = os.getenv("SAMBANOVA_API_KEY") or os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY")
```

### 2. Provider Auto-Detection

Based on the API key prefix or format:

| Key Prefix / Format | Provider | Base URL | Default Model |
|---------------------|----------|----------|---------------|
| `UUID format` | SambaNova | `https://api.sambanova.ai/v1` | `Meta-Llama-3.1-70B-Instruct` |
| `sk-or-` | OpenRouter | `https://openrouter.ai/api/v1` | `openai/gpt-oss-120b` |
| `sk-` | OpenAI | `https://api.openai.com/v1` | `gpt-4o-mini` |
| Other | OpenRouter (fallback) | `https://openrouter.ai/api/v1` | `openai/gpt-oss-120b` |

### 3. Visual Feedback

When initializing, you'll see one of:

```
[dim]Using SambaNova Cloud API[/dim]
[dim]Using OpenRouter API with FREE Gemini model[/dim]
[dim]Using OpenAI API[/dim]
```

---

## Configuration

### Option 1: SambaNova Cloud (Fastest Llama-3.1)

**Advantages:**
- Extreme inference speed (hundreds of tokens per second)
- High-quality Llama-3.1 70B and 405B models
- Free tier available for developers

**Setup:**

1. Get API key from [SambaNova Cloud](https://cloud.sambanova.ai/)
2. Add to `.env`:

```env
SAMBANOVA_API_KEY=your-uuid-style-key-here
```

---

### Option 2: OpenRouter (Recommended for Variety)

**Advantages:**
- Access to 100+ models (Claude, GPT-4, Llama, Gemini, etc.)
- Competitive pricing
- Single API key for all models

**Setup:**

1. Get API key from [openrouter.ai](https://openrouter.ai/)
2. Add to `.env`:

```env
OPENROUTER_API_KEY=sk-or-v1-your-key-here
```

**Available Models:**
```python
# Premium models
"anthropic/claude-3.5-sonnet"
"openai/gpt-4o"
"google/gemini-2.0-flash-exp"

# Budget models
"anthropic/claude-3-haiku"
"openai/gpt-4o-mini"
"meta-llama/llama-3.1-8b-instruct"
```

### Option 2: OpenAI Direct

**Advantages:**
- Direct access to OpenAI models
- Potentially lower latency

**Setup:**

1. Get API key from [platform.openai.com](https://platform.openai.com/)
2. Add to `.env`:

```env
OPENAI_API_KEY=sk-your-key-here
```

**Available Models:**
```python
"gpt-4o"
"gpt-4o-mini"
"gpt-4-turbo"
"gpt-3.5-turbo"
```

---

## Usage Examples

### Using OpenRouter

```bash
# .env file
OPENROUTER_API_KEY=sk-or-v1-abc123...

# Run
python codegenome_v2.py
# Output: [dim]Using OpenRouter API[/dim]
```

### Using OpenAI

```bash
# .env file
OPENAI_API_KEY=sk-abc123...

# Run
python codegenome_v2.py
# Output: [dim]Using OpenAI API[/dim]
```

### Custom Model Selection

You can override the default model:

```python
# In codegenome_v2.py, line ~1100
llm = LLMReasoner(model="openai/gpt-4o")  # For OpenRouter
llm = LLMReasoner(model="gpt-4o")         # For OpenAI
```

---

## Error Handling

### No API Key Found

```
ValueError: No API key found. Please set either:
  - OPENROUTER_API_KEY (for OpenRouter)
  - OPENAI_API_KEY (for OpenAI)
in your .env file
```

**Solution:** Add one of the API keys to your `.env` file

### Unknown Key Format

```
[dim yellow]Warning: Unknown API key format, defaulting to OpenRouter[/dim yellow]
```

**What it means:** The key doesn't start with `sk-or-` or `sk-`, so the system assumes OpenRouter

**Action:** Verify your API key is correct

---

## Implementation Details

### Code Changes (Lines 803-843)

```python
class LLMReasoner:
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        # Multi-source API key detection
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY")
        
        if not self.api_key:
            raise ValueError("No API key found...")
        
        # Auto-detect provider
        if self.api_key.startswith("sk-or-"):
            self.provider = "openrouter"
            self.base_url = "https://openrouter.ai/api/v1"
            self.model = model or "anthropic/claude-3.5-sonnet"
        elif self.api_key.startswith("sk-"):
            self.provider = "openai"
            self.base_url = "https://api.openai.com/v1"
            self.model = model or "gpt-4o-mini"
        else:
            # Fallback to OpenRouter
            self.provider = "openrouter"
            self.base_url = "https://openrouter.ai/api/v1"
            self.model = model or "anthropic/claude-3.5-sonnet"
        
        # Initialize client
        self.client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key
        )
```

### Benefits

1. **Flexibility** — Use either provider without code changes
2. **Automatic Detection** — No manual configuration needed
3. **Clear Feedback** — Know which provider is being used
4. **Fallback Logic** — Graceful handling of unknown key formats
5. **Model Defaults** — Optimized defaults for each provider

---

## Cost Comparison

### OpenRouter Pricing (as of 2026)

| Model | Input (per 1M tokens) | Output (per 1M tokens) |
|-------|----------------------|------------------------|
| Claude 3.5 Sonnet | $3.00 | $15.00 |
| GPT-4o Mini | $0.15 | $0.60 |
| Llama 3.1 8B | $0.06 | $0.06 |

### OpenAI Direct Pricing

| Model | Input (per 1M tokens) | Output (per 1M tokens) |
|-------|----------------------|------------------------|
| GPT-4o | $2.50 | $10.00 |
| GPT-4o Mini | $0.15 | $0.60 |

**Typical CodeGenome Analysis:**
- Input: ~2,000 tokens (compressed context)
- Output: ~500 tokens (AI response)
- **Cost per analysis:** $0.001 - $0.01 (depending on model)

---

## Troubleshooting

### Both Keys Set

If both `OPENROUTER_API_KEY` and `OPENAI_API_KEY` are set:
- **OpenRouter takes priority** (checked first)
- To use OpenAI, comment out the OpenRouter key

### Model Not Found

```
Error: Model 'xyz' not found
```

**Solution:** Check the model name is correct for your provider:
- OpenRouter: Use full path (e.g., `anthropic/claude-3.5-sonnet`)
- OpenAI: Use short name (e.g., `gpt-4o-mini`)

### Rate Limits

- **OpenRouter:** Varies by model
- **OpenAI:** 500 requests/day (free tier), 10,000/day (paid)

**Solution:** Add delays between analyses or upgrade your plan

---

## Migration Guide

### From v1 to v2

**v1 (OpenRouter only):**
```env
OPENROUTER_API_KEY=sk-or-v1-...
```

**v2 (Both supported):**
```env
# Option 1: Keep using OpenRouter (no changes needed)
OPENROUTER_API_KEY=sk-or-v1-...

# Option 2: Switch to OpenAI
OPENAI_API_KEY=sk-...
```

**No code changes required!** The system auto-detects.

---

## Best Practices

1. **Use OpenRouter for variety** — Access to 100+ models
2. **Use OpenAI for consistency** — Stable, well-documented models
3. **Set one key only** — Avoid confusion
4. **Monitor costs** — Check usage dashboards regularly
5. **Rotate keys** — Change API keys every 90 days for security

---

**End of Guide**
