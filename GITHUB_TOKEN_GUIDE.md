# How to Get GitHub Token — Quick Guide

## Why You Need It

**Without Token:** 60 requests/hour (rate limit errors)  
**With Token:** 5,000 requests/hour ✅

---

## Step-by-Step Instructions

### 1. Visit GitHub Token Settings

🔗 **Direct Link:** [github.com/settings/tokens](https://github.com/settings/tokens)

Or navigate:
```
GitHub.com → Your Profile Picture → Settings → 
Developer settings → Personal access tokens → Tokens (classic)
```

### 2. Generate New Token

Click: **"Generate new token"** → **"Generate new token (classic)"**

### 3. Configure Token

| Setting | Value |
|---------|-------|
| **Note** | `CodeGenome API Access` |
| **Expiration** | 90 days (recommended) |
| **Scopes** | ✅ `public_repo` only |

> [!IMPORTANT]
> Only select `public_repo` — nothing else needed!

### 4. Generate and Copy

1. Click **"Generate token"**
2. **Copy the token** (starts with `ghp_`)
3. ⚠️ **Save it now** — you won't see it again!

### 5. Add to `.env` File

Edit: `codegenome_v2\.env`

```env
OPENROUTER_API_KEY=sk-or-v1-your-key-here

# Add this line:
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 6. Test It

```bash
python codegenome_v2.py
# Enter any GitHub URL
```

You should see no rate limit errors! ✅

---

## Visual Guide

```
┌─────────────────────────────────────────┐
│  GitHub.com                             │
│  ┌───────────────────────────────────┐  │
│  │ Your Profile Picture ▼            │  │
│  │   Settings                        │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│  Settings                               │
│  ┌───────────────────────────────────┐  │
│  │ Developer settings                │  │
│  │   → Personal access tokens        │  │
│  │      → Tokens (classic)           │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│  Personal Access Tokens                 │
│  ┌───────────────────────────────────┐  │
│  │ Generate new token (classic)      │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│  New Personal Access Token              │
│  ┌───────────────────────────────────┐  │
│  │ Note: CodeGenome API Access       │  │
│  │ Expiration: 90 days               │  │
│  │                                   │  │
│  │ Select scopes:                    │  │
│  │ ☐ repo (full control)             │  │
│  │ ☑ public_repo (read public)       │  │
│  │ ☐ workflow                        │  │
│  │ ☐ write:packages                  │  │
│  │                                   │  │
│  │ [Generate token]                  │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│  Token Generated!                       │
│  ┌───────────────────────────────────┐  │
│  │ ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxx  │  │
│  │                                   │  │
│  │ ⚠️ Copy now! Won't show again     │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

---

## Troubleshooting

### "Token doesn't work"

✅ **Check:** Token starts with `ghp_`  
✅ **Check:** `public_repo` scope is selected  
✅ **Check:** Token is not expired  

### "Still getting rate limit errors"

✅ **Check:** `.env` file has `GITHUB_TOKEN=ghp_...`  
✅ **Check:** No spaces around `=`  
✅ **Check:** Restart the script after adding token  

### "Can't find token settings"

Use direct link: [github.com/settings/tokens](https://github.com/settings/tokens)

---

## Security Best Practices

1. ✅ **Never commit `.env` to Git**
2. ✅ **Set expiration (90 days recommended)**
3. ✅ **Only select `public_repo` scope**
4. ✅ **Rotate tokens regularly**
5. ✅ **Delete unused tokens**

---

## Rate Limits Comparison

| Type | Requests/Hour | Good For |
|------|---------------|----------|
| **No Token** | 60 | Small repos only |
| **With Token** | 5,000 | Production use ✅ |

**Example:**
- Analyzing 1 repo = ~20 requests
- Without token: 3 repos/hour
- With token: 250 repos/hour

---

**Done!** 🎉 Your GitHub token is now active.
