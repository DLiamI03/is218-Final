# ⚙️ OpenAI API Key Setup Guide

## Why You Need It
The AI food and workout parsing features require an OpenAI API key. Without it, the app still works perfectly for manual logging, but you'll miss the WOW factor AI features!

## How to Get Your API Key

### Step 1: Create OpenAI Account
1. Go to https://platform.openai.com/
2. Click "Sign up" (or login if you have an account)
3. Complete the registration

### Step 2: Get API Key
1. Go to https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Give it a name like "FitTrack Pro"
4. **COPY THE KEY IMMEDIATELY** (you can't see it again!)
5. Key format looks like: `sk-proj-...` (starts with `sk-`)

### Step 3: Add Credits (If Needed)
- New accounts get $5 free credits (usually enough for demo!)
- Check balance at: https://platform.openai.com/usage
- If needed, add payment method at: https://platform.openai.com/settings/organization/billing

## Setup in Your Project

### Method 1: Using .env File (Recommended)

1. **Create `.env` file** in project root:
```bash
cd c:\Users\Dogukan\Documents\VSC\IS218_Last
notepad .env
```

2. **Add this content:**
```bash
OPENAI_API_KEY=sk-proj-your-actual-key-here
DATABASE_URL=postgresql://postgres:postgres@db:5432/app_db
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

3. **Replace `sk-proj-your-actual-key-here`** with your real key

4. **Save and close**

5. **Restart Docker containers:**
```bash
docker-compose restart
```

### Method 2: Directly in docker-compose.yml

1. **Open docker-compose.yml**

2. **Find this line:**
```yaml
OPENAI_API_KEY: ${OPENAI_API_KEY:-your-openai-api-key-here}
```

3. **Replace with your key:**
```yaml
OPENAI_API_KEY: sk-proj-your-actual-key-here
```

4. **Restart:**
```bash
docker-compose restart
```

## Verify It Works

### Test 1: Check Environment Variable
```bash
docker-compose exec web python -c "import os; print('Key set:', 'Yes' if os.getenv('OPENAI_API_KEY') else 'No')"
```

Should output: `Key set: Yes`

### Test 2: Test AI Parsing
1. Open http://localhost:8000
2. Login/Register
3. Go to "Meals" tab
4. Type in AI Food Parser: "2 eggs and toast"
5. Click "Parse with AI"
6. Should return structured food data!

### Test 3: Check Logs
```bash
docker-compose logs web | grep -i "openai"
```

Should NOT show "API key not set" errors.

## Troubleshooting

### ❌ Error: "AI parsing error: No API key provided"
**Solution:** API key not set or incorrect format
- Check `.env` file exists and has correct key
- Restart containers: `docker-compose restart`
- Key should start with `sk-`

### ❌ Error: "Incorrect API key provided"
**Solution:** Key is invalid or revoked
- Generate new key at: https://platform.openai.com/api-keys
- Update `.env` file
- Restart containers

### ❌ Error: "You exceeded your current quota"
**Solution:** No credits left
- Check usage: https://platform.openai.com/usage
- Add payment method: https://platform.openai.com/settings/organization/billing
- New accounts get $5 free (usually enough for demo!)

### ❌ AI parsing returns generic fallback data
**Solution:** API call failed but app handled it gracefully
- Check internet connection
- Verify OpenAI service status: https://status.openai.com/
- Check logs: `docker-compose logs web`

### ❌ AI parsing is very slow (>10 seconds)
**Solution:** Normal for first call, API warming up
- Subsequent calls should be 2-3 seconds
- If consistently slow, check internet speed

## Cost Information

### Pricing (as of Dec 2024)
- **GPT-3.5-turbo**: ~$0.002 per 1,000 tokens
- Average food parsing: ~300 tokens = $0.0006 (less than 1 cent!)
- Average workout parsing: ~250 tokens = $0.0005

### For Your Demo
- New account: **$5 free credits**
- Estimated demo usage: **~$0.05** (100 AI calls)
- Your free credits will last for **thousands of requests**!

### After Demo
- Set spending limits in OpenAI dashboard
- Monitor usage at: https://platform.openai.com/usage
- Consider using rate limiting in production

## Security Best Practices

### ✅ DO:
- Keep API key in `.env` file (never in code)
- Add `.env` to `.gitignore`
- Use environment variables in production
- Rotate keys periodically
- Set spending limits in OpenAI dashboard

### ❌ DON'T:
- Commit API keys to GitHub
- Share keys publicly
- Expose keys in client-side code
- Use same key for multiple projects

## Alternative: Demo Without OpenAI

If you can't get an API key in time, the app still works great:

### Manual Logging Still Available
- ✅ Quick Log buttons work perfectly
- ✅ Manual meal entry
- ✅ Manual workout entry
- ✅ All other features work
- ❌ Just no AI parsing

### Demo Strategy Without AI
1. Emphasize other features: Dashboard, Charts, CRUD operations
2. Show the AI parsing UI: "This would call OpenAI API"
3. Explain the architecture: "Here's how the AI integration works"
4. Focus on database design, API structure, UI/UX
5. Still a solid project!

## Quick Reference

### Where to Get Key
https://platform.openai.com/api-keys

### Where to Check Usage
https://platform.openai.com/usage

### Where to Add Credits
https://platform.openai.com/settings/organization/billing

### Documentation
https://platform.openai.com/docs/

### Support
https://help.openai.com/

---

## Final Checklist

Before demo tomorrow:
- [ ] OpenAI account created
- [ ] API key generated and copied
- [ ] Key added to `.env` file
- [ ] Containers restarted
- [ ] Tested AI food parsing
- [ ] Tested AI workout parsing
- [ ] Verified credits available
- [ ] Set spending limit (optional but safe)

---

**You're all set! The AI features will blow away your audience! 🤖⭐**
