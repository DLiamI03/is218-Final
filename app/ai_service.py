"""
OpenAI GPT Integration Service for Food and Exercise Parsing
"""
import os
from openai import OpenAI
import json
from typing import List, Dict

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", ""))


def parse_food_with_ai(text: str) -> List[Dict]:
    """
    Parse natural language food descriptions using GPT API.
    Example: "I had 2 eggs, 1 slice of whole wheat toast, and a banana for breakfast"
    Returns structured food data.
    """
    prompt = f"""Parse the following food description into structured data. Return ONLY a valid JSON array of food items.
Each item should have: name, serving_size (float), serving_unit (string), calories (int), protein_g (float), carbs_g (float), fats_g (float), fiber_g (float).
Use your knowledge of common foods to estimate nutrition values.

Food description: {text}

Return format:
[
  {{
    "name": "Eggs",
    "brand": null,
    "serving_size": 2,
    "serving_unit": "large eggs",
    "calories": 140,
    "protein_g": 12.0,
    "carbs_g": 1.0,
    "fats_g": 10.0,
    "fiber_g": 0.0,
    "is_custom": false
  }}
]
"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-5-nano",
            messages=[
                {"role": "system", "content": "You are a nutrition expert. Parse food descriptions into structured JSON data with accurate nutrition information."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        content = response.choices[0].message.content.strip()
        
        # Try to extract JSON from response (GPT sometimes adds explanation text)
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        
        food_items = json.loads(content)
        return food_items if isinstance(food_items, list) else [food_items]
        
    except Exception as e:
        error_msg = f"Error parsing food with AI: {str(e)}"
        print(error_msg)
        # Re-raise the exception so the user can see what's wrong
        raise Exception(f"AI parsing failed: {str(e)}")


def parse_workout_with_ai(text: str) -> List[Dict]:
    """
    Parse natural language workout descriptions using GPT API.
    Example: "Did 3 sets of 10 pushups, ran for 20 minutes"
    Returns structured workout data.
    """
    prompt = f"""Parse the following workout description into structured data. Return ONLY a valid JSON array of exercises.
Each item should have: name, category (strength/cardio/flexibility/sports), muscle_group (optional), sets (optional, int), reps (optional, int), duration_minutes (optional, int), weight_kg (optional, float).

Workout description: {text}

Return format:
[
  {{
    "name": "Push-ups",
    "category": "strength",
    "muscle_group": "chest",
    "sets": 3,
    "reps": 10,
    "duration_minutes": null,
    "weight_kg": null
  }}
]
"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-5-nano",
            messages=[
                {"role": "system", "content": "You are a fitness expert. Parse workout descriptions into structured JSON data."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        content = response.choices[0].message.content.strip()
        
        # Try to extract JSON from response
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        
        exercises = json.loads(content)
        return exercises if isinstance(exercises, list) else [exercises]
        
    except Exception as e:
        error_msg = f"Error parsing workout with AI: {str(e)}"
        print(error_msg)
        # Re-raise the exception so the user can see what's wrong
        raise Exception(f"AI parsing failed: {str(e)}")


def get_meal_suggestions(preferences: str = "", dietary_restrictions: str = "") -> List[str]:
    """
    Get AI-powered meal suggestions based on user preferences.
    """
    prompt = f"""Suggest 5 healthy meal ideas.
Preferences: {preferences or 'None'}
Dietary restrictions: {dietary_restrictions or 'None'}

Provide simple meal names only, one per line."""
    
    try:
        response = client.chat.completions.create(
            model="gpt-5-nano",
            messages=[
                {"role": "system", "content": "You are a nutrition expert providing healthy meal suggestions."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        
        content = response.choices[0].message.content.strip()
        suggestions = [line.strip() for line in content.split('\n') if line.strip() and not line.strip().startswith('#')]
        return suggestions[:5]
        
    except Exception as e:
        error_msg = f"Error getting meal suggestions: {str(e)}"
        print(error_msg)
        # Re-raise the exception so the user can see what's wrong
        raise Exception(f"AI suggestions failed: {str(e)}")
