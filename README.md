# 💪 FitTrack Pro - AI-Powered Fitness & Nutrition Tracker

![CI/CD Pipeline](https://github.com/DLiamI03/is218-Final/actions/workflows/ci-cd.yml/badge.svg)
![Tests](https://github.com/DLiamI03/is218-Final/actions/workflows/tests.yml/badge.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🌐 Live Demo

**🚀 Try it now:** [http://159.203.79.244:8000](http://159.203.79.244:8000)

---

A full-stack web application that helps users track their fitness journey with **AI-powered food and workout parsing** using OpenAI's GPT API.

## 🌟 Features

### Core Features
- ✅ **User Authentication**: Secure JWT-based registration and login
- ✅ **Beautiful Dashboard**: Real-time stats and visualizations
- ✅ **Meal Tracking**: Log meals with detailed nutrition breakdown
- ✅ **Workout Tracking**: Record exercises with sets, reps, and calories
- ✅ **Body Metrics**: Track weight and body fat percentage over time
- ✅ **Water Intake**: Monitor daily hydration
- ✅ **Goal Setting**: Set and track fitness goals
- ✅ **Progress Charts**: Interactive weight and nutrition visualizations

### 🤖 AI-Powered Features (OpenAI GPT)
- ⭐ **AI Food Parser**: "I had 2 eggs and toast" → Structured nutrition data
- ⭐ **AI Workout Parser**: "Ran 5k in 25 minutes" → Exercise with calories
- ⭐ **Natural Language Input**: No more searching databases!

## 🏗️ Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: ORM for database management
- **PostgreSQL**: Relational database
- **OpenAI API**: GPT-3.5 for natural language parsing
- **JWT**: Secure authentication
- **Pydantic**: Data validation

### Frontend
- **Vanilla JavaScript**: No framework dependencies
- **Chart.js**: Interactive data visualizations
- **Modern CSS**: Dark theme with gradients and animations
- **Responsive Design**: Mobile-friendly interface

### DevOps
- **Docker & Docker Compose**: Containerization
- **Pytest**: Backend testing
- **Playwright**: E2E testing

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose installed
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Setup

1. **Clone and navigate to project:**
```bash
cd IS218_Last
```

2. **Create `.env` file:**
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your OpenAI API key:
OPENAI_API_KEY=sk-your-actual-api-key-here
```

3. **Start the application:**
```bash
docker-compose up --build
```

4. **Access the application:**
- Open browser to: http://localhost:8000
- API documentation: http://localhost:8000/docs

5. **Seed the database (optional but recommended):**
```bash
# In another terminal:
docker-compose exec web python seed_data.py
```
This adds 23 common foods and 27 exercises to get you started!

## 📖 Usage Guide

### 1. Create an Account
- Click "Sign Up" on the login page
- Enter username, email, and password
- Login with your credentials

### 2. Set Up Profile (Optional)
- Add your height, weight, and fitness goals
- Set daily calorie targets
- Choose activity level

### 3. Log Your Meals (AI-Powered! 🤖)
- Go to "Meals" tab
- Use the **AI Food Parser**:
  - Type: "I had 2 scrambled eggs, whole wheat toast with butter, and a banana"
  - Click "Parse with AI"
  - Watch AI automatically extract nutrition info!
- Or use Quick Log button for faster entry

### 4. Log Your Workouts (AI-Powered! 🤖)
- Go to "Workouts" tab
- Use the **AI Workout Parser**:
  - Type: "Did 3 sets of 10 pushups, then ran 5k in 25 minutes"
  - Click "Parse with AI"
  - AI identifies exercises automatically!
- Or use Quick Log for manual entry

### 5. Track Progress
- View weight trends on Dashboard
- Check nutrition breakdown (protein/carbs/fats)
- Monitor weekly workout count
- See body metrics history in Progress tab

## 🎯 API Endpoints

### Authentication
- `POST /register` - Create new user
- `POST /token` - Login (get JWT token)
- `GET /users/me` - Get current user info

### Dashboard
- `GET /dashboard` - Get summary statistics

### AI Parsing ⭐
- `POST /ai/parse-food` - Parse natural language food description
- `POST /ai/parse-workout` - Parse natural language workout description
- `GET /ai/meal-suggestions` - Get AI meal suggestions

### Meals
- `POST /meals` - Create meal log
- `GET /meals` - Get meal history (with filters)
- `DELETE /meals/{id}` - Delete meal

### Workouts
- `POST /workouts` - Create workout session
- `GET /workouts` - Get workout history
- `DELETE /workouts/{id}` - Delete workout

### Body Metrics
- `POST /body-metrics` - Log weight/body fat
- `GET /body-metrics` - Get metrics history

### Food & Exercise Database
- `GET /foods` - Search foods
- `POST /foods` - Add custom food
- `GET /exercises` - Search exercises
- `POST /exercises` - Add custom exercise

### Water & Goals
- `POST /water` - Log water intake
- `GET /water` - Get water history
- `POST /goals` - Create goal
- `GET /goals` - Get goals

Full API documentation available at: http://localhost:8000/docs

## 🏗️ Architecture

### Database Models
- **Users**: Authentication and user data
- **UserProfile**: Height, weight goals, activity level
- **BodyMetric**: Weight tracking history
- **FoodDatabase**: Nutrition information (23 pre-seeded items)
- **MealLog**: Meal entries
- **MealFood**: Foods in each meal (many-to-many)
- **ExerciseLibrary**: Exercise database (27 pre-seeded items)
- **WorkoutSession**: Workout entries
- **WorkoutExercise**: Exercises in workout
- **ExerciseSet**: Sets/reps/weight for each exercise
- **WaterIntake**: Daily hydration tracking
- **Goal**: User fitness goals

### Project Structure
```
IS218_Last/
├── app/
│   ├── main.py           # FastAPI app & all endpoints
│   ├── database.py       # SQLAlchemy models
│   ├── schemas.py        # Pydantic validation schemas
│   ├── auth.py          # Authentication logic
│   └── ai_service.py    # OpenAI integration ⭐
├── static/
│   ├── index.html       # Frontend UI
│   ├── style.css        # Styling
│   └── script.js        # Frontend logic
├── tests/               # Pytest tests
├── docker-compose.yml   # Docker orchestration
├── Dockerfile          # Container configuration
├── requirements.txt    # Python dependencies
├── seed_data.py       # Database seeding script
└── DEMO_GUIDE.md      # Presentation guide
```

## 🧪 Testing

### Run Tests
```bash
# Backend tests
docker-compose exec web pytest

# E2E tests (requires Playwright installed)
pytest tests/test_e2e.py
```

### Test Coverage
- User authentication flow
- API endpoint validation
- Database operations
- (Add more tests as needed)

## 🎨 UI Features

- **Modern Dark Theme**: Purple/blue gradients
- **Responsive Design**: Works on mobile and desktop
- **Interactive Charts**: Weight trends and nutrition breakdown
- **Quick Action Buttons**: Fast logging of meals, workouts, water, weight
- **AI-Powered Forms**: Natural language input fields
- **Toast Notifications**: User-friendly feedback
- **Modal Dialogs**: Clean form interfaces
- **Loading States**: Visual feedback during API calls

## 🔒 Security

- JWT token authentication
- Password hashing with bcrypt
- SQL injection protection (SQLAlchemy ORM)
- CORS configuration
- Environment variable secrets
- User data isolation

## 🚢 Deployment

The application is containerized and ready for deployment to:
- AWS ECS/Fargate
- Google Cloud Run
- Azure Container Instances
- DigitalOcean App Platform
- Heroku

### Environment Variables Required
```bash
OPENAI_API_KEY=your_key
DATABASE_URL=postgresql://...
SECRET_KEY=your_secret
```

## 📊 Database Schema

```sql
Users (id, username, email, hashed_password, created_at)
  ├── UserProfile (1:1)
  ├── BodyMetric (1:many)
  ├── MealLog (1:many)
  │   └── MealFood (many:many with FoodDatabase)
  ├── WorkoutSession (1:many)
  │   └── WorkoutExercise (many:many with ExerciseLibrary)
  │       └── ExerciseSet (1:many)
  ├── WaterIntake (1:many)
  └── Goal (1:many)
```

## 🤖 AI Integration Details

The app uses OpenAI's GPT-3.5-turbo model to parse natural language:

**Food Parsing Example:**
```
Input: "I had 2 scrambled eggs, whole wheat toast with butter, and a banana"
Output: [
  {name: "Eggs", servings: 2, calories: 140, protein: 12g, ...},
  {name: "Whole Wheat Toast", servings: 1, calories: 80, ...},
  {name: "Banana", servings: 1, calories: 105, ...}
]
```

**Workout Parsing Example:**
```
Input: "Did 3 sets of 10 pushups, then ran 5k in 25 minutes"
Output: [
  {name: "Push-ups", category: "strength", sets: 3, reps: 10},
  {name: "Running", category: "cardio", duration_minutes: 25}
]
```

## 🎓 Course Requirements Met

✅ User Registration & Login (JWT)
✅ Email Validation
✅ Database with Multiple Related Tables
✅ CRUD Operations (Create, Read, Update, Delete)
✅ Beautiful, Responsive Dashboard
✅ Data Visualizations (Chart.js)
✅ Docker Containerization
✅ API Documentation (FastAPI)
✅ Error Handling & Validation
✅ **Bonus: AI Integration!** ⭐

## 📝 Development

### Local Development Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export OPENAI_API_KEY=your_key
export DATABASE_URL=postgresql://...

# Run locally
uvicorn app.main:app --reload
```

### Adding New Features
1. Add database model in `app/database.py`
2. Create Pydantic schemas in `app/schemas.py`
3. Add endpoints in `app/main.py`
4. Update frontend in `static/`
5. Add tests in `tests/`

## 🐛 Troubleshooting

**AI parsing not working?**
- Check OPENAI_API_KEY is set in `.env`
- Verify API key has credits
- Check logs: `docker-compose logs web`

**Database connection issues?**
- Ensure PostgreSQL container is healthy: `docker-compose ps`
- Check DATABASE_URL environment variable
- Wait for database to initialize (first startup)

**Port 8000 already in use?**
- Change port in docker-compose.yml: `"8001:8000"`

## 📚 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [OpenAI API](https://platform.openai.com/docs/)
- [Chart.js](https://www.chartjs.org/)

## 👨‍💻 Author

Built for IS218 Final Project
December 2025

## 📄 License

MIT License - Feel free to use for learning!

---

**🎯 Ready for Demo? Check out [DEMO_GUIDE.md](DEMO_GUIDE.md) for presentation tips!**
