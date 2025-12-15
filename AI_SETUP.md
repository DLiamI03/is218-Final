# 🤖 AI Integration Setup

## Overview
Your fitness tracker uses **OpenAI GPT-3.5-turbo** for three powerful AI features:
1. **Natural language food parsing** - "I had 2 eggs and toast" → Structured nutrition data
2. **Natural language workout parsing** - "Did 3 sets of 10 pushups" → Structured workout data  
3. **AI meal suggestions** - Get personalized meal ideas based on preferences

## Setup Steps

### 1. Get Your OpenAI API Key

1. Go to [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Sign up or log in
3. Click "Create new secret key"
4. Copy your key (starts with `sk-...`)

### 2. Add API Key to .env File

Open the `.env` file in the project root and replace `your-api-key-here`:

```bash
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxx
```

### 3. Restart Docker Containers

```powershell
docker-compose down
docker-compose up --build
```

## 🧪 Testing AI Features

### Test 1: AI Food Parsing
1. Log in to your app at http://localhost:8000
2. Go to **Meals** tab
3. Scroll to "Log with AI" section
4. Type: `I had 2 scrambled eggs, 1 slice of whole wheat toast with butter, and a banana`
5. Click "Parse with AI"
6. You should see structured food items with calories and macros!

### Test 2: AI Workout Parsing
1. Go to **Workouts** tab
2. Scroll to "Log with AI" section
3. Type: `Did 3 sets of 10 pushups, 3 sets of 15 squats, and ran for 20 minutes`
4. Click "Parse with AI"
5. You should see structured exercises!

### Test 3: AI Meal Suggestions
1. Go to **Insights** tab
2. Scroll to "AI Meal Suggestions"
3. Enter preferences (e.g., "high protein, quick meals")
4. Enter restrictions (e.g., "dairy-free")
5. Click "Get Suggestions"
6. You should see 5 personalized meal ideas!

## 💰 Cost Information

- GPT-3.5-turbo is **very cheap**: ~$0.0015 per 1000 tokens
- Average food parsing: ~300 tokens = **$0.0005** (less than a penny!)
- Average workout parsing: ~250 tokens = **$0.0004**
- 1000 AI parses ≈ **$0.50**

For demo/testing purposes, $5 credit will give you thousands of AI requests.

## 🔧 Troubleshooting

### Issue: "AI parsing error"
**Solution:** Check if your API key is valid and has credits.

```powershell
# Check logs for API errors
docker-compose logs web
```

### Issue: "Rate limit exceeded"
**Solution:** OpenAI has rate limits for free tier. Wait a minute or upgrade your account.

### Issue: Slow responses
**Normal:** First AI request takes 2-3 seconds. This is normal for GPT API calls.

## 🎯 Demo Tips

**For your presentation tomorrow:**

1. **Pre-test**: Run all 3 AI features before your demo to ensure they work
2. **Have examples ready**: 
   - Food: "chicken breast with rice and broccoli"
   - Workout: "bench press 3x8, ran 30 minutes"
3. **Explain the value**: Natural language input is much faster than manual entry
4. **Show the fallback**: Even if AI fails, the app has graceful fallbacks

## 📊 What the AI Does

### Food Parsing (`parse_food_with_ai`)
- **Input:** Natural language text
- **Process:** GPT-3.5 analyzes the text and estimates:
  - Food names
  - Serving sizes
  - Calories, protein, carbs, fats, fiber
- **Output:** Structured JSON array ready for database insertion

### Workout Parsing (`parse_workout_with_ai`)
- **Input:** Natural language workout description
- **Process:** GPT-3.5 extracts:
  - Exercise names
  - Sets, reps, duration
  - Exercise categories (strength/cardio/etc)
- **Output:** Structured JSON array of exercises

### Meal Suggestions (`get_meal_suggestions`)
- **Input:** User preferences and dietary restrictions
- **Process:** GPT-3.5 generates personalized meal ideas
- **Output:** 5 healthy meal suggestions

## 🚀 Production Considerations

**Before deploying to production:**
1. Never commit your API key to Git (already in `.gitignore`)
2. Set usage limits in OpenAI dashboard
3. Monitor API costs in OpenAI dashboard
4. Consider caching common food/workout responses
5. Add rate limiting to prevent abuse

## ✅ Verification

Your AI integration is complete when:
- ✅ `.env` file has valid OpenAI API key
- ✅ Docker containers restart successfully
- ✅ Food parsing works in UI
- ✅ Workout parsing works in UI
- ✅ Meal suggestions work in UI
- ✅ No errors in `docker-compose logs web`

---

**Good luck with your presentation tomorrow! 🎉**
