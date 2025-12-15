# FitTrack Pro - Quick Start Guide

## 🚀 Setup Instructions

### 1. Environment Setup
Create a `.env` file in the project root with your OpenAI API key:
```bash
OPENAI_API_KEY=your_api_key_here
DATABASE_URL=postgresql://postgres:postgres@db:5432/app_db
```

### 2. Start the Application
```bash
docker-compose up --build
```

### 3. Access the Application
Open your browser to: http://localhost:8000

### 4. Create an Account
- Click "Sign Up" on the login page
- Enter username, email, and password
- Click "Register"
- Login with your new credentials

## 🎯 Features to Demo

### 1. **AI-Powered Food Logging** ⭐
- Go to "Meals" tab
- Use the AI Food Parser
- Example: "I had 2 scrambled eggs, whole wheat toast with butter, and a banana"
- Watch AI parse nutrition info automatically!

### 2. **AI-Powered Workout Logging** ⭐
- Go to "Workouts" tab
- Use the AI Workout Parser
- Example: "Did 3 sets of 10 pushups, then ran 5k in 25 minutes"
- AI identifies exercises automatically!

### 3. **Quick Logging**
Dashboard has quick action buttons for:
- 🍽️ Log Meal
- 💪 Log Workout
- 💧 Log Water
- ⚖️ Log Weight

### 4. **Beautiful Dashboard**
- Real-time calorie tracking
- Weekly workout count
- Water intake monitoring
- Weight progress visualization

### 5. **Data Visualizations** 📊
- Interactive weight progress chart (Chart.js)
- Nutrition breakdown pie chart (Protein/Carbs/Fats)
- Responsive and animated

### 6. **Progress Tracking**
- View weight history
- Track body fat percentage
- See long-term trends

## 🏗️ Architecture Highlights

### Backend (FastAPI)
- ✅ JWT Authentication
- ✅ PostgreSQL Database with SQLAlchemy
- ✅ 30+ RESTful API Endpoints
- ✅ OpenAI GPT-3.5 Integration
- ✅ Pydantic Validation
- ✅ Docker Containerization

### Frontend (Vanilla JS)
- ✅ Modern Dark Theme UI
- ✅ Responsive Design
- ✅ Chart.js Visualizations
- ✅ Real-time Data Updates
- ✅ Smooth Animations

### Database Models
- Users & Authentication
- User Profiles (height, weight goals, activity level)
- Body Metrics (weight tracking)
- Food Database (nutrition info)
- Meal Logs with Foods
- Exercise Library
- Workout Sessions with Exercises & Sets
- Water Intake
- Goals

### API Endpoints (Examples)
```
POST /register - User registration
POST /token - Login
GET /dashboard - Summary stats
POST /ai/parse-food - AI food parsing ⭐
POST /ai/parse-workout - AI workout parsing ⭐
POST /meals - Log meal
GET /meals - Get meal history
POST /workouts - Log workout
GET /workouts - Get workouts
POST /body-metrics - Log weight
GET /body-metrics - Weight history
```

## 🎨 UI/UX Features
- Beautiful gradient backgrounds
- Card-based layouts
- Hover animations
- Toast notifications
- Modal dialogs
- Responsive navigation
- Loading states
- Error handling

## 🤖 AI Integration (OpenAI GPT-3.5)
The app uses OpenAI's API to parse natural language:
- **Food Parser**: Converts "2 eggs and toast" → Structured nutrition data
- **Workout Parser**: Converts "ran 5k" → Exercise with duration/calories
- **Fallback Handling**: Graceful errors if API fails

## 📊 Demo Tips

1. **Start with Registration**: Show the clean auth flow
2. **Use AI Parsers First**: This is the WOW factor! ⭐
3. **Quick Log Actions**: Show how easy it is to log data
4. **Dashboard Visualization**: Highlight the charts and stats
5. **Real-time Updates**: Show data updating across views

## 🔥 Key Selling Points

### ✨ Innovation (AI Integration)
- GPT-powered natural language parsing
- No need to search food databases
- Just describe what you ate/did

### 🎯 Functionality
- Complete BREAD operations on all entities
- Dashboard with live calculations
- Multiple tracking dimensions (food, exercise, water, weight)

### 🎨 Aesthetics
- Modern dark theme
- Smooth animations
- Professional design
- Mobile-responsive

### 🏗️ Development Process
- Docker containerization
- RESTful API design
- Clean code architecture
- Comprehensive error handling

## 📝 API Testing with Swagger
Visit: http://localhost:8000/docs

Try the endpoints directly:
1. POST /register - Create user
2. POST /token - Get auth token
3. Use "Authorize" button with token
4. Test any endpoint!

## 🎯 Project Requirements Met

✅ User Registration & Login (JWT)
✅ Email Validation
✅ Database with Multiple Tables (PostgreSQL)
✅ BREAD Operations (Browse, Read, Edit, Add, Delete)
✅ Beautiful Dashboard
✅ Data Visualizations (Charts)
✅ Responsive Design
✅ Docker Deployment
✅ API Documentation (FastAPI auto-docs)
✅ Error Handling
✅ **BONUS: AI Integration!** ⭐

## 🚀 Deployment Ready

The app is fully containerized and can be deployed to:
- AWS ECS/Fargate
- Google Cloud Run
- Azure Container Instances
- DigitalOcean App Platform
- Heroku

Just push the Docker image and set environment variables!

---

**Built for IS218 Final Project**
*AI-Powered Fitness & Nutrition Tracker*

🎓 December 2025
