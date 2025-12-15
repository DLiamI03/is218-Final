// FitTrack Pro - Main JavaScript File
let token = localStorage.getItem('token');
let currentUser = null;
let weightChart = null;
let nutritionChart = null;

// API Helper Function
async function apiRequest(endpoint, options = {}) {
    const headers = {
        'Content-Type': 'application/json',
        ...(token && { 'Authorization': `Bearer ${token}` })
    };

    const response = await fetch(endpoint, {
        ...options,
        headers: { ...headers, ...options.headers }
    });

    if (response.status === 401) {
        logout();
        throw new Error('Unauthorized');
    }

    // Handle 204 No Content (DELETE requests)
    if (response.status === 204) {
        return null;
    }

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.detail || 'Request failed');
    }

    return data;
}

// Toast Notification
function showToast(message, isError = false) {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast show ${isError ? 'error' : ''}`;
    setTimeout(() => toast.classList.remove('show'), 3000);
}

// ===== AUTHENTICATION =====
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    const showRegister = document.getElementById('show-register');
    const showLogin = document.getElementById('show-login');
    const logoutBtn = document.getElementById('logout-btn');

    // Toggle forms
    showRegister?.addEventListener('click', (e) => {
        e.preventDefault();
        document.getElementById('login-form').style.display = 'none';
        document.getElementById('register-form').style.display = 'block';
    });

    showLogin?.addEventListener('click', (e) => {
        e.preventDefault();
        document.getElementById('register-form').style.display = 'none';
        document.getElementById('login-form').style.display = 'block';
    });

    // Login
    loginForm?.addEventListener('submit', async (e) => {
        e.preventDefault();
        const username = document.getElementById('login-username').value;
        const password = document.getElementById('login-password').value;

        try {
            const formData = new URLSearchParams();
            formData.append('username', username);
            formData.append('password', password);

            const data = await fetch('/token', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: formData
            }).then(r => r.json());

            token = data.access_token;
            localStorage.setItem('token', token);
            await loadApp();
        } catch (error) {
            showToast('Login failed: ' + error.message, true);
        }
    });

    // Register
    registerForm?.addEventListener('submit', async (e) => {
        e.preventDefault();
        const username = document.getElementById('register-username').value;
        const email = document.getElementById('register-email').value;
        const password = document.getElementById('register-password').value;

        try {
            await apiRequest('/register', {
                method: 'POST',
                body: JSON.stringify({ username, email, password })
            });

            showToast('Registration successful! Please login.');
            showLogin.click();
        } catch (error) {
            showToast('Registration failed: ' + error.message, true);
        }
    });

    // Logout
    logoutBtn?.addEventListener('click', logout);

    // Check if already logged in
    if (token) {
        loadApp();
    }
});

function logout() {
    token = null;
    currentUser = null;
    localStorage.removeItem('token');
    document.getElementById('auth-section').style.display = 'block';
    document.getElementById('app-section').style.display = 'none';
}

async function loadApp() {
    try {
        currentUser = await apiRequest('/users/me');
        document.getElementById('username-display').textContent = currentUser.username;
        document.getElementById('auth-section').style.display = 'none';
        document.getElementById('app-section').style.display = 'block';
        
        setupNavigation();
        loadDashboard();
    } catch (error) {
        logout();
    }
}

// ===== NAVIGATION =====
function setupNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            const view = link.dataset.view;
            switchView(view);
        });
    });
}

function switchView(viewName) {
    // Update active nav link
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.toggle('active', link.dataset.view === viewName);
    });

    // Show view
    document.querySelectorAll('.view-container').forEach(view => {
        view.classList.remove('active');
    });
    document.getElementById(`${viewName}-view`).classList.add('active');

    // Load view data
    if (viewName === 'dashboard') loadDashboard();
    else if (viewName === 'meals') loadMeals();
    else if (viewName === 'workouts') loadWorkouts();
    else if (viewName === 'progress') loadProgress();
    else if (viewName === 'goals') loadGoals();
    else if (viewName === 'search') loadSearch();
    else if (viewName === 'insights') loadInsights();
    else if (viewName === 'settings') loadSettings();
}

// ===== DASHBOARD =====
async function loadDashboard() {
    try {
        const data = await apiRequest('/dashboard');
        
        document.getElementById('calories-today').textContent = data.total_calories_today;
        document.getElementById('calorie-target').textContent = data.calories_target || '--';
        document.getElementById('workouts-week').textContent = data.workouts_this_week;
        const waterOz = Math.round(data.total_water_today / 29.5735);
        document.getElementById('water-today').textContent = `${waterOz} oz`;
        const weightLbs = data.current_weight ? Math.round(data.current_weight * 2.20462 * 10) / 10 : null;
        document.getElementById('current-weight').textContent = weightLbs ? `${weightLbs} lbs` : '--';
        document.getElementById('goal-weight').textContent = data.goal_weight || '--';
        
        // Load charts
        loadWeightChart();
        loadNutritionChart(data);
    } catch (error) {
        showToast('Error loading dashboard', true);
    }
}

async function loadWeightChart() {
    try {
        const endDate = new Date().toISOString().split('T')[0];
        const startDate = new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0];
        
        const metrics = await apiRequest(`/body-metrics?start_date=${startDate}&end_date=${endDate}`);
        
        const ctx = document.getElementById('weightChart');
        if (weightChart) weightChart.destroy();
        
        weightChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: metrics.map(m => m.date).reverse(),
                datasets: [{
                    label: 'Weight (lbs)',
                    data: metrics.map(m => Math.round(m.weight_kg * 2.20462 * 10) / 10).reverse(),
                    borderColor: '#6366f1',
                    backgroundColor: 'rgba(99, 102, 241, 0.1)',
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { labels: { color: '#f1f5f9' } }
                },
                scales: {
                    x: { ticks: { color: '#94a3b8' }, grid: { color: '#334155' } },
                    y: { ticks: { color: '#94a3b8' }, grid: { color: '#334155' } }
                }
            }
        });
    } catch (error) {
        console.error('Error loading weight chart:', error);
    }
}

function loadNutritionChart(dashboardData) {
    const ctx = document.getElementById('nutritionChart');
    if (nutritionChart) nutritionChart.destroy();
    
    const protein = dashboardData.total_protein_today || 0;
    const carbs = dashboardData.total_carbs_today || 0;
    const fats = dashboardData.total_fats_today || 0;
    
    // If no data, show placeholder values
    const hasData = protein > 0 || carbs > 0 || fats > 0;
    
    nutritionChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: hasData ? ['Protein', 'Carbs', 'Fats'] : ['No data yet'],
            datasets: [{
                data: hasData ? [protein, carbs, fats] : [1],
                backgroundColor: hasData ? ['#10b981', '#f59e0b', '#ef4444'] : ['#334155']
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { labels: { color: '#f1f5f9' } },
                tooltip: {
                    enabled: hasData,
                    callbacks: hasData ? {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.parsed;
                            return label + ': ' + Math.round(value * 10) / 10 + 'g';
                        }
                    } : {}
                }
            }
        }
    });
}

// ===== QUICK LOGGING =====
function showQuickLog(type) {
    const modal = document.getElementById('quick-modal');
    const overlay = document.getElementById('modal-overlay');
    const title = document.getElementById('modal-title');
    const content = document.getElementById('modal-content');
    
    let html = '';
    
    if (type === 'meal') {
        title.textContent = '🍽️ Quick Meal Log';
        html = `
            <form onsubmit="submitQuickMeal(event)">
                <div class="form-group">
                    <label>Meal Type</label>
                    <select id="quick-meal-type">
                        <option value="breakfast">Breakfast</option>
                        <option value="lunch">Lunch</option>
                        <option value="dinner">Dinner</option>
                        <option value="snack">Snack</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Meal Name</label>
                    <input type="text" id="quick-meal-name" placeholder="e.g., Chicken Salad" required>
                </div>
                <div class="form-row">
                    <div class="form-group">
                        <label>Calories</label>
                        <input type="number" id="quick-meal-calories" min="0" value="0" required>
                    </div>
                    <div class="form-group">
                        <label>Protein (g)</label>
                        <input type="number" id="quick-meal-protein" step="0.1" min="0" value="0">
                    </div>
                </div>
                <div class="form-row">
                    <div class="form-group">
                        <label>Carbs (g)</label>
                        <input type="number" id="quick-meal-carbs" step="0.1" min="0" value="0">
                    </div>
                    <div class="form-group">
                        <label>Fats (g)</label>
                        <input type="number" id="quick-meal-fats" step="0.1" min="0" value="0">
                    </div>
                </div>
                <div class="form-group">
                    <label>Notes (optional)</label>
                    <textarea id="quick-meal-notes" rows="2" placeholder="Additional details..."></textarea>
                </div>
                <button type="submit" class="btn btn-primary">Log Meal</button>
            </form>
        `;
    } else if (type === 'workout') {
        title.textContent = '💪 Quick Workout Log';
        html = `
            <form onsubmit="submitQuickWorkout(event)">
                <div class="form-group">
                    <label>Workout Name</label>
                    <input type="text" id="quick-workout-name" placeholder="Morning Run" required>
                </div>
                <div class="form-group">
                    <label>Duration (minutes)</label>
                    <input type="number" id="quick-workout-duration" min="1" value="30">
                </div>
                <div class="form-group">
                    <label>Calories Burned</label>
                    <input type="number" id="quick-workout-calories" min="0" value="200">
                </div>
                <button type="submit" class="btn btn-primary">Log Workout</button>
            </form>
        `;
    } else if (type === 'water') {
        title.textContent = '💧 Quick Water Log';
        html = `
            <form onsubmit="submitQuickWater(event)">
                <div class="form-group">
                    <label>Amount (oz)</label>
                    <input type="number" id="quick-water-amount" min="1" value="8" step="1" required>
                </div>
                <button type="submit" class="btn btn-primary">Log Water</button>
            </form>
        `;
    } else if (type === 'weight') {
        title.textContent = '⚖️ Quick Weight Log';
        html = `
            <form onsubmit="submitQuickWeight(event)">
                <div class="form-group">
                    <label>Weight (lbs)</label>
                    <input type="number" id="quick-weight" step="0.1" required>
                </div>
                <div class="form-group">
                    <label>Body Fat % (optional)</label>
                    <input type="number" id="quick-bodyfat" step="0.1" min="0" max="100">
                </div>
                <button type="submit" class="btn btn-primary">Log Weight</button>
            </form>
        `;
    }
    
    content.innerHTML = html;
    modal.classList.add('active');
    overlay.classList.add('active');
}

function closeModal() {
    document.getElementById('quick-modal').classList.remove('active');
    document.getElementById('modal-overlay').classList.remove('active');
}

async function submitQuickMeal(e) {
    e.preventDefault();
    const mealType = document.getElementById('quick-meal-type').value;
    const mealName = document.getElementById('quick-meal-name').value;
    const calories = parseInt(document.getElementById('quick-meal-calories').value) || 0;
    const protein = parseFloat(document.getElementById('quick-meal-protein').value) || 0;
    const carbs = parseFloat(document.getElementById('quick-meal-carbs').value) || 0;
    const fats = parseFloat(document.getElementById('quick-meal-fats').value) || 0;
    const notes = document.getElementById('quick-meal-notes').value;
    
    try {
        console.log('Creating custom food:', { mealName, calories, protein, carbs, fats });
        
        // Create a custom food with the nutrition data
        const food = await apiRequest('/foods', {
            method: 'POST',
            body: JSON.stringify({
                name: mealName,
                brand: null,
                serving_size: 1.0,
                serving_unit: 'serving',
                calories: calories,
                protein_g: protein,
                carbs_g: carbs,
                fats_g: fats,
                fiber_g: 0.0
            })
        });
        
        console.log('Food created:', food);
        
        // Create meal and link the food
        const meal = await apiRequest('/meals', {
            method: 'POST',
            body: JSON.stringify({
                date: new Date().toISOString().split('T')[0],
                meal_type: mealType,
                notes: notes || null,
                foods: [{
                    food_id: food.id,
                    servings: 1.0
                }]
            })
        });
        
        console.log('Meal created:', meal);
        
        showToast('Meal logged successfully!');
        closeModal();
        loadDashboard();
        if (typeof loadMeals === 'function') loadMeals();
    } catch (error) {
        console.error('Error logging meal:', error);
        showToast('Error logging meal: ' + error.message, true);
    }
}

async function submitQuickWorkout(e) {
    e.preventDefault();
    const name = document.getElementById('quick-workout-name').value;
    const duration = parseInt(document.getElementById('quick-workout-duration').value);
    const calories = parseInt(document.getElementById('quick-workout-calories').value);
    
    try {
        await apiRequest('/workouts', {
            method: 'POST',
            body: JSON.stringify({
                name,
                date: new Date().toISOString().split('T')[0],
                duration_minutes: duration,
                total_calories_burned: calories,
                exercises: []
            })
        });
        
        showToast('Workout logged successfully!');
        closeModal();
        loadDashboard();
    } catch (error) {
        showToast('Error logging workout: ' + error.message, true);
    }
}

async function submitQuickWater(e) {
    e.preventDefault();
    const amountOz = parseInt(document.getElementById('quick-water-amount').value);
    const amountMl = Math.round(amountOz * 29.5735); // Convert oz to ml
    
    // Validate reasonable amount (max ~1700 oz = 50L)
    if (amountOz > 1700) {
        showToast('Amount too large. Please enter a reasonable amount (max 1700 oz)', true);
        return;
    }
    
    try {
        await apiRequest('/water', {
            method: 'POST',
            body: JSON.stringify({
                date: new Date().toISOString().split('T')[0],
                amount_ml: amountMl
            })
        });
        
        showToast('Water intake logged!');
        closeModal();
        loadDashboard();
    } catch (error) {
        console.error('Water logging error:', error);
        const errorMsg = error.message || JSON.stringify(error);
        showToast('Error logging water: ' + errorMsg, true);
    }
}

async function submitQuickWeight(e) {
    e.preventDefault();
    const weightLbs = parseFloat(document.getElementById('quick-weight').value);
    const weightKg = weightLbs * 0.453592; // Convert lbs to kg
    const bodyfat = document.getElementById('quick-bodyfat').value;
    
    try {
        await apiRequest('/body-metrics', {
            method: 'POST',
            body: JSON.stringify({
                date: new Date().toISOString().split('T')[0],
                weight_kg: weightKg,
                body_fat_percentage: bodyfat ? parseFloat(bodyfat) : null
            })
        });
        
        showToast('Weight logged successfully!');
        closeModal();
        loadDashboard();
    } catch (error) {
        showToast('Error logging weight: ' + error.message, true);
    }
}

// ===== AI PARSING =====
async function parseFood() {
    const text = document.getElementById('ai-food-input').value;
    if (!text) return;
    
    const resultsDiv = document.getElementById('ai-food-results');
    resultsDiv.innerHTML = '<p class="loading">AI is parsing your food...</p>';
    
    try {
        const result = await apiRequest('/ai/parse-food', {
            method: 'POST',
            body: JSON.stringify({ text })
        });
        
        let html = '<div style="background: var(--bg); padding: 15px; border-radius: 8px; margin-top: 15px;">';
        html += '<h4>Parsed Foods:</h4>';
        result.food_items.forEach(food => {
            html += `
                <div style="padding: 10px; margin: 10px 0; background: var(--bg-light); border-radius: 8px;">
                    <strong>${food.name}</strong> - ${food.serving_size} ${food.serving_unit}<br>
                    <small>Calories: ${food.calories} | Protein: ${food.protein_g}g | Carbs: ${food.carbs_g}g | Fats: ${food.fats_g}g</small>
                </div>
            `;
        });
        html += '</div>';
        resultsDiv.innerHTML = html;
        
        showToast('Food parsed successfully!');
    } catch (error) {
        resultsDiv.innerHTML = '';
        showToast('AI parsing error: ' + error.message, true);
    }
}

async function parseWorkout() {
    const text = document.getElementById('ai-workout-input').value;
    if (!text) return;
    
    const resultsDiv = document.getElementById('ai-workout-results');
    resultsDiv.innerHTML = '<p class="loading">AI is parsing your workout...</p>';
    
    try {
        const result = await apiRequest('/ai/parse-workout', {
            method: 'POST',
            body: JSON.stringify({ text })
        });
        
        let html = '<div style="background: var(--bg); padding: 15px; border-radius: 8px; margin-top: 15px;">';
        html += '<h4>Parsed Exercises:</h4>';
        result.exercises.forEach(ex => {
            html += `
                <div style="padding: 10px; margin: 10px 0; background: var(--bg-light); border-radius: 8px;">
                    <strong>${ex.name}</strong> - ${ex.category}<br>
                    <small>${ex.sets ? `${ex.sets} sets x ${ex.reps} reps` : `${ex.duration_minutes} minutes`}</small>
                </div>
            `;
        });
        html += '</div>';
        resultsDiv.innerHTML = html;
        
        showToast('Workout parsed successfully!');
    } catch (error) {
        resultsDiv.innerHTML = '';
        showToast('AI parsing error: ' + error.message, true);
    }
}

// ===== MEALS VIEW =====
async function loadMeals() {
    const container = document.getElementById('meals-container');
    container.innerHTML = '<p class="loading">Loading meals...</p>';
    
    try {
        const today = new Date().toISOString().split('T')[0];
        const meals = await apiRequest(`/meals?start_date=${today}&end_date=${today}`);
        
        if (meals.length === 0) {
            container.innerHTML = '<p style="text-align: center; color: var(--text-muted);">No meals logged today. Use the AI parser or quick log to add meals!</p>';
            return;
        }
        
        let html = '';
        meals.forEach(meal => {
            html += `
                <div style="background: var(--bg); padding: 20px; margin-bottom: 15px; border-radius: 8px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <strong style="font-size: 1.2rem;">${meal.meal_type.toUpperCase()}</strong>
                            <p style="color: var(--text-muted); margin: 5px 0;">${meal.date}</p>
                        </div>
                        <button class="btn btn-logout" onclick="deleteMeal(${meal.id})">Delete</button>
                    </div>
                    ${meal.notes ? `<p style="margin-top: 10px;">${meal.notes}</p>` : ''}
                </div>
            `;
        });
        
        container.innerHTML = html;
    } catch (error) {
        container.innerHTML = '<p style="color: var(--danger);">Error loading meals</p>';
    }
}

async function deleteMeal(id) {
    if (!confirm('Delete this meal?')) return;
    
    try {
        await apiRequest(`/meals/${id}`, { method: 'DELETE' });
        showToast('Meal deleted');
        loadMeals();
        loadDashboard();
    } catch (error) {
        console.error('Delete meal error:', error);
        // Don't show error - reload to reflect actual state
        loadMeals();
        loadDashboard();
    }
}

// ===== WORKOUTS VIEW =====
async function loadWorkouts() {
    const container = document.getElementById('workouts-container');
    container.innerHTML = '<p class="loading">Loading workouts...</p>';
    
    try {
        const workouts = await apiRequest('/workouts');
        
        if (workouts.length === 0) {
            container.innerHTML = '<p style="text-align: center; color: var(--text-muted);">No workouts yet. Use the AI parser or quick log to add workouts!</p>';
            return;
        }
        
        let html = '';
        workouts.slice(0, 10).forEach(workout => {
            html += `
                <div style="background: var(--bg); padding: 20px; margin-bottom: 15px; border-radius: 8px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <strong style="font-size: 1.2rem;">${workout.name}</strong>
                            <p style="color: var(--text-muted); margin: 5px 0;">${workout.date} • ${workout.duration_minutes || 0} min • ${workout.total_calories_burned || 0} cal</p>
                        </div>
                        <button class="btn btn-logout" onclick="deleteWorkout(${workout.id})">Delete</button>
                    </div>
                </div>
            `;
        });
        
        container.innerHTML = html;
    } catch (error) {
        container.innerHTML = '<p style="color: var(--danger);">Error loading workouts</p>';
    }
}

async function deleteWorkout(id) {
    if (!confirm('Delete this workout?')) return;
    
    try {
        await apiRequest(`/workouts/${id}`, { method: 'DELETE' });
        showToast('Workout deleted');
        loadWorkouts();
        loadDashboard();
    } catch (error) {
        console.error('Delete workout error:', error);
        // Don't show error - reload to reflect actual state
        loadWorkouts();
        loadDashboard();
    }
}

// ===== PROGRESS VIEW =====
async function loadProgress() {
    const metricsList = document.getElementById('metrics-list');
    metricsList.innerHTML = '<p class="loading">Loading metrics...</p>';
    
    try {
        const metrics = await apiRequest('/body-metrics');
        
        if (metrics.length === 0) {
            metricsList.innerHTML = '<p style="text-align: center; color: var(--text-muted);">No body metrics yet. Use quick log to add your weight!</p>';
            return;
        }
        
        let html = '<table style="width: 100%; border-collapse: collapse;">';
        html += '<tr style="border-bottom: 1px solid var(--border);"><th style="text-align: left; padding: 10px;">Date</th><th>Weight (kg)</th><th>Body Fat %</th></tr>';
        
        metrics.slice(0, 20).forEach(m => {
            html += `
                <tr style="border-bottom: 1px solid var(--border);">
                    <td style="padding: 10px;">${m.date}</td>
                    <td style="text-align: center;">${m.weight_kg}</td>
                    <td style="text-align: center;">${m.body_fat_percentage || '--'}</td>
                </tr>
            `;
        });
        
        html += '</table>';
        metricsList.innerHTML = html;
    } catch (error) {
        metricsList.innerHTML = '<p style="color: var(--danger);">Error loading metrics</p>';
    }
}

// Placeholder functions for form displays
function showMealForm() {
    showQuickLog('meal');
}

function showWorkoutForm() {
    showQuickLog('workout');
}

// ===== GOALS VIEW =====
async function loadGoals() {
    const activeList = document.getElementById('active-goals-list');
    const completedList = document.getElementById('completed-goals-list');
    
    activeList.innerHTML = '<p class="loading">Loading goals...</p>';
    completedList.innerHTML = '<p class="loading">Loading...</p>';
    
    try {
        const allGoals = await apiRequest('/goals?active_only=false');
        
        const activeGoals = allGoals.filter(g => !g.is_achieved);
        const completedGoals = allGoals.filter(g => g.is_achieved);
        
        if (activeGoals.length === 0) {
            activeList.innerHTML = '<p style="text-align: center; color: var(--text-muted);">No active goals. Create one to start!</p>';
        } else {
            let html = '';
            activeGoals.forEach(goal => {
                const progress = Math.min(100, (goal.current_value / goal.target_value) * 100);
                html += `
                    <div class="goal-item">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <strong>${goal.goal_type}</strong>
                            <span style="color: var(--text-muted);">${goal.current_value} / ${goal.target_value}</span>
                        </div>
                        <div class="goal-progress-bar">
                            <div class="goal-progress-fill" style="width: ${progress}%"></div>
                        </div>
                        <p style="color: var(--text-muted); font-size: 0.9rem; margin-top: 5px;">Target: ${goal.target_date || 'No deadline'}</p>
                    </div>
                `;
            });
            activeList.innerHTML = html;
        }
        
        if (completedGoals.length === 0) {
            completedList.innerHTML = '<p style="text-align: center; color: var(--text-muted);">No completed goals yet.</p>';
        } else {
            let html = '';
            completedGoals.forEach(goal => {
                html += `
                    <div class="goal-item" style="border: 2px solid var(--success);">
                        <strong>✅ ${goal.goal_type}</strong>
                        <p style="color: var(--success); margin-top: 5px;">Completed!</p>
                    </div>
                `;
            });
            completedList.innerHTML = html;
        }
    } catch (error) {
        activeList.innerHTML = '<p style="color: var(--danger);">Error loading goals</p>';
        completedList.innerHTML = '';
    }
}

function showGoalForm() {
    const modal = document.getElementById('quick-modal');
    const overlay = document.getElementById('modal-overlay');
    const title = document.getElementById('modal-title');
    const content = document.getElementById('modal-content');
    
    title.textContent = '🎯 Create New Goal';
    content.innerHTML = `
        <form onsubmit="submitGoal(event)">
            <div class="form-group">
                <label>Goal Type</label>
                <input type="text" id="goal-type" placeholder="e.g., Reach 75kg, Run 5k under 25min" required>
            </div>
            <div class="form-group">
                <label>Target Value</label>
                <input type="number" id="goal-target" step="0.1" required>
            </div>
            <div class="form-group">
                <label>Current Value</label>
                <input type="number" id="goal-current" step="0.1" value="0">
            </div>
            <div class="form-group">
                <label>Target Date (Optional)</label>
                <input type="date" id="goal-date">
            </div>
            <button type="submit" class="btn btn-primary">Create Goal</button>
        </form>
    `;
    
    modal.classList.add('active');
    overlay.classList.add('active');
}

async function submitGoal(e) {
    e.preventDefault();
    
    const goalType = document.getElementById('goal-type').value;
    const targetValue = parseFloat(document.getElementById('goal-target').value);
    const currentValue = parseFloat(document.getElementById('goal-current').value);
    const targetDate = document.getElementById('goal-date').value;
    
    try {
        await apiRequest('/goals', {
            method: 'POST',
            body: JSON.stringify({
                goal_type: goalType,
                target_value: targetValue,
                current_value: currentValue,
                start_date: new Date().toISOString().split('T')[0],
                target_date: targetDate || null
            })
        });
        
        showToast('Goal created successfully!');
        closeModal();
        loadGoals();
    } catch (error) {
        showToast('Error creating goal: ' + error.message, true);
    }
}

// ===== SEARCH VIEW =====
function loadSearch() {
    // Setup search tab switching
    document.querySelectorAll('.search-tab').forEach(tab => {
        tab.addEventListener('click', () => {
            const searchType = tab.dataset.search;
            
            // Update active tab
            document.querySelectorAll('.search-tab').forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            
            // Show corresponding search content
            document.querySelectorAll('.search-content').forEach(c => c.classList.remove('active'));
            document.getElementById(`${searchType.slice(0, -1)}-search`).classList.add('active');
        });
    });
    
    // Load initial results
    searchFoods();
}

async function searchFoods() {
    const searchInput = document.getElementById('food-search-input').value;
    const resultsDiv = document.getElementById('food-search-results');
    
    resultsDiv.innerHTML = '<p class="loading">Searching foods...</p>';
    
    try {
        const foods = await apiRequest(`/foods?search=${encodeURIComponent(searchInput)}&limit=50`);
        
        if (foods.length === 0) {
            resultsDiv.innerHTML = '<p style="text-align: center; color: var(--text-muted);">No foods found. Try a different search or create a custom food.</p>';
            return;
        }
        
        let html = '<div class="search-results-grid">';
        foods.forEach(food => {
            html += `
                <div class="result-item">
                    <strong>${food.name}</strong>
                    ${food.brand ? `<p style="color: var(--text-muted); font-size: 0.9rem;">${food.brand}</p>` : ''}
                    <p style="margin: 10px 0; font-size: 0.9rem;">
                        <strong>${food.serving_size} ${food.serving_unit}</strong>
                    </p>
                    <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 5px; font-size: 0.85rem;">
                        <div>Calories: ${food.calories}</div>
                        <div>Protein: ${food.protein_g}g</div>
                        <div>Carbs: ${food.carbs_g}g</div>
                        <div>Fats: ${food.fats_g}g</div>
                    </div>
                    ${food.is_custom ? '<p style="color: var(--primary); margin-top: 5px; font-size: 0.8rem;">Custom Food</p>' : ''}
                </div>
            `;
        });
        html += '</div>';
        
        resultsDiv.innerHTML = html;
    } catch (error) {
        resultsDiv.innerHTML = '<p style="color: var(--danger);">Error searching foods</p>';
    }
}

async function searchExercises() {
    const searchInput = document.getElementById('exercise-search-input').value;
    const resultsDiv = document.getElementById('exercise-search-results');
    
    resultsDiv.innerHTML = '<p class="loading">Searching exercises...</p>';
    
    try {
        const exercises = await apiRequest(`/exercises?search=${encodeURIComponent(searchInput)}&limit=50`);
        
        if (exercises.length === 0) {
            resultsDiv.innerHTML = '<p style="text-align: center; color: var(--text-muted);">No exercises found. Try a different search or create a custom exercise.</p>';
            return;
        }
        
        let html = '<div class="search-results-grid">';
        exercises.forEach(ex => {
            const categoryIcon = ex.category === 'strength' ? '💪' : ex.category === 'cardio' ? '🏃' : ex.category === 'flexibility' ? '🧘' : '⚽';
            html += `
                <div class="result-item">
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <span style="font-size: 2rem;">${categoryIcon}</span>
                        <div>
                            <strong>${ex.name}</strong>
                            <p style="color: var(--text-muted); font-size: 0.9rem;">${ex.category}</p>
                        </div>
                    </div>
                    ${ex.muscle_group ? `<p style="margin-top: 10px;"><strong>Target:</strong> ${ex.muscle_group}</p>` : ''}
                    <p style="margin-top: 5px; font-size: 0.9rem;"><strong>Calories:</strong> ~${ex.calories_per_minute}/min</p>
                    ${ex.description ? `<p style="margin-top: 5px; font-size: 0.85rem; color: var(--text-muted);">${ex.description}</p>` : ''}
                    ${ex.is_custom ? '<p style="color: var(--primary); margin-top: 5px; font-size: 0.8rem;">Custom Exercise</p>' : ''}
                </div>
            `;
        });
        html += '</div>';
        
        resultsDiv.innerHTML = html;
    } catch (error) {
        resultsDiv.innerHTML = '<p style="color: var(--danger);">Error searching exercises</p>';
    }
}

function showCreateFoodForm() {
    const modal = document.getElementById('quick-modal');
    const overlay = document.getElementById('modal-overlay');
    const title = document.getElementById('modal-title');
    const content = document.getElementById('modal-content');
    
    title.textContent = '🍽️ Create Custom Food';
    content.innerHTML = `
        <form onsubmit="submitCustomFood(event)">
            <div class="form-group">
                <label>Food Name</label>
                <input type="text" id="custom-food-name" required>
            </div>
            <div class="form-group">
                <label>Brand (Optional)</label>
                <input type="text" id="custom-food-brand">
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>Serving Size</label>
                    <input type="number" id="custom-food-serving" step="0.1" required>
                </div>
                <div class="form-group">
                    <label>Serving Unit</label>
                    <input type="text" id="custom-food-unit" placeholder="e.g., grams, cup" required>
                </div>
            </div>
            <div class="form-group">
                <label>Calories</label>
                <input type="number" id="custom-food-calories" required>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>Protein (g)</label>
                    <input type="number" id="custom-food-protein" step="0.1" value="0">
                </div>
                <div class="form-group">
                    <label>Carbs (g)</label>
                    <input type="number" id="custom-food-carbs" step="0.1" value="0">
                </div>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>Fats (g)</label>
                    <input type="number" id="custom-food-fats" step="0.1" value="0">
                </div>
                <div class="form-group">
                    <label>Fiber (g)</label>
                    <input type="number" id="custom-food-fiber" step="0.1" value="0">
                </div>
            </div>
            <button type="submit" class="btn btn-primary">Create Food</button>
        </form>
    `;
    
    modal.classList.add('active');
    overlay.classList.add('active');
}

async function submitCustomFood(e) {
    e.preventDefault();
    
    try {
        await apiRequest('/foods', {
            method: 'POST',
            body: JSON.stringify({
                name: document.getElementById('custom-food-name').value,
                brand: document.getElementById('custom-food-brand').value || null,
                serving_size: parseFloat(document.getElementById('custom-food-serving').value),
                serving_unit: document.getElementById('custom-food-unit').value,
                calories: parseInt(document.getElementById('custom-food-calories').value),
                protein_g: parseFloat(document.getElementById('custom-food-protein').value),
                carbs_g: parseFloat(document.getElementById('custom-food-carbs').value),
                fats_g: parseFloat(document.getElementById('custom-food-fats').value),
                fiber_g: parseFloat(document.getElementById('custom-food-fiber').value)
            })
        });
        
        showToast('Custom food created!');
        closeModal();
        searchFoods();
    } catch (error) {
        showToast('Error creating food: ' + error.message, true);
    }
}

function showCreateExerciseForm() {
    const modal = document.getElementById('quick-modal');
    const overlay = document.getElementById('modal-overlay');
    const title = document.getElementById('modal-title');
    const content = document.getElementById('modal-content');
    
    title.textContent = '💪 Create Custom Exercise';
    content.innerHTML = `
        <form onsubmit="submitCustomExercise(event)">
            <div class="form-group">
                <label>Exercise Name</label>
                <input type="text" id="custom-exercise-name" required>
            </div>
            <div class="form-group">
                <label>Category</label>
                <select id="custom-exercise-category" required>
                    <option value="strength">Strength</option>
                    <option value="cardio">Cardio</option>
                    <option value="flexibility">Flexibility</option>
                    <option value="sports">Sports</option>
                </select>
            </div>
            <div class="form-group">
                <label>Muscle Group (Optional)</label>
                <input type="text" id="custom-exercise-muscle" placeholder="e.g., chest, legs">
            </div>
            <div class="form-group">
                <label>Description (Optional)</label>
                <textarea id="custom-exercise-desc" rows="2"></textarea>
            </div>
            <div class="form-group">
                <label>Calories per Minute</label>
                <input type="number" id="custom-exercise-calories" step="0.1" value="5" required>
            </div>
            <button type="submit" class="btn btn-primary">Create Exercise</button>
        </form>
    `;
    
    modal.classList.add('active');
    overlay.classList.add('active');
}

async function submitCustomExercise(e) {
    e.preventDefault();
    
    try {
        await apiRequest('/exercises', {
            method: 'POST',
            body: JSON.stringify({
                name: document.getElementById('custom-exercise-name').value,
                category: document.getElementById('custom-exercise-category').value,
                muscle_group: document.getElementById('custom-exercise-muscle').value || null,
                description: document.getElementById('custom-exercise-desc').value || null,
                calories_per_minute: parseFloat(document.getElementById('custom-exercise-calories').value)
            })
        });
        
        showToast('Custom exercise created!');
        closeModal();
        searchExercises();
    } catch (error) {
        showToast('Error creating exercise: ' + error.message, true);
    }
}

// ===== INSIGHTS VIEW =====
async function loadInsights() {
    loadWeeklySummary();
    loadProgressAnalysis();
}

async function loadWeeklySummary() {
    const summaryDiv = document.getElementById('weekly-summary');
    summaryDiv.innerHTML = '<p class="loading">Loading weekly summary...</p>';
    
    try {
        const endDate = new Date().toISOString().split('T')[0];
        const startDate = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0];
        
        const [meals, workouts, water] = await Promise.all([
            apiRequest(`/meals?start_date=${startDate}&end_date=${endDate}`),
            apiRequest(`/workouts?start_date=${startDate}&end_date=${endDate}`),
            apiRequest(`/water?start_date=${startDate}&end_date=${endDate}`)
        ]);
        
        let totalCalories = 0;
        meals.forEach(meal => {
            meal.foods.forEach(mf => {
                totalCalories += mf.food.calories * mf.servings;
            });
        });
        
        const totalWorkouts = workouts.length;
        const totalWater = water.reduce((sum, w) => sum + w.amount_ml, 0);
        
        summaryDiv.innerHTML = `
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px;">
                <div style="text-align: center; padding: 15px; background: var(--bg); border-radius: 8px;">
                    <div style="font-size: 2rem; margin-bottom: 5px;">🍽️</div>
                    <div style="font-size: 1.5rem; font-weight: bold;">${meals.length}</div>
                    <div style="color: var(--text-muted); font-size: 0.9rem;">Meals Logged</div>
                </div>
                <div style="text-align: center; padding: 15px; background: var(--bg); border-radius: 8px;">
                    <div style="font-size: 2rem; margin-bottom: 5px;">🔥</div>
                    <div style="font-size: 1.5rem; font-weight: bold;">${Math.round(totalCalories)}</div>
                    <div style="color: var(--text-muted); font-size: 0.9rem;">Total Calories</div>
                </div>
                <div style="text-align: center; padding: 15px; background: var(--bg); border-radius: 8px;">
                    <div style="font-size: 2rem; margin-bottom: 5px;">💪</div>
                    <div style="font-size: 1.5rem; font-weight: bold;">${totalWorkouts}</div>
                    <div style="color: var(--text-muted); font-size: 0.9rem;">Workouts</div>
                </div>
                <div style="text-align: center; padding: 15px; background: var(--bg); border-radius: 8px;">
                    <div style="font-size: 2rem; margin-bottom: 5px;">💧</div>
                    <div style="font-size: 1.5rem; font-weight: bold;">${(totalWater / 1000).toFixed(1)}L</div>
                    <div style="color: var(--text-muted); font-size: 0.9rem;">Water Intake</div>
                </div>
            </div>
        `;
    } catch (error) {
        summaryDiv.innerHTML = '<p style="color: var(--danger);">Error loading summary</p>';
    }
}

async function getAIMealSuggestions() {
    const preferences = document.getElementById('meal-preferences').value;
    const restrictions = document.getElementById('meal-restrictions').value;
    const resultsDiv = document.getElementById('meal-suggestions-results');
    
    resultsDiv.innerHTML = '<p class="loading">AI is generating meal suggestions...</p>';
    
    try {
        const result = await apiRequest(`/ai/meal-suggestions?preferences=${encodeURIComponent(preferences)}&dietary_restrictions=${encodeURIComponent(restrictions)}`);
        
        let html = '<div style="background: var(--bg); padding: 15px; border-radius: 8px; margin-top: 15px;">';
        html += '<h4>Suggested Meals:</h4>';
        html += '<ul style="margin: 10px 0; padding-left: 20px;">';
        result.suggestions.forEach(suggestion => {
            html += `<li style="margin: 8px 0;">${suggestion}</li>`;
        });
        html += '</ul>';
        html += '</div>';
        
        resultsDiv.innerHTML = html;
    } catch (error) {
        resultsDiv.innerHTML = '<p style="color: var(--danger);">Error getting suggestions</p>';
    }
}

async function loadProgressAnalysis() {
    const analysisDiv = document.getElementById('progress-analysis');
    analysisDiv.innerHTML = '<p class="loading">Analyzing progress...</p>';
    
    try {
        const endDate = new Date().toISOString().split('T')[0];
        const startDate = new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0];
        
        const metrics = await apiRequest(`/body-metrics?start_date=${startDate}&end_date=${endDate}`);
        
        if (metrics.length < 2) {
            analysisDiv.innerHTML = '<p style="text-align: center; color: var(--text-muted);">Not enough data yet. Log your weight regularly to see progress analysis!</p>';
            return;
        }
        
        const sortedMetrics = metrics.sort((a, b) => new Date(a.date) - new Date(b.date));
        const firstWeight = sortedMetrics[0].weight_kg;
        const lastWeight = sortedMetrics[sortedMetrics.length - 1].weight_kg;
        const weightChange = lastWeight - firstWeight;
        const changePercent = ((weightChange / firstWeight) * 100).toFixed(1);
        
        const trend = weightChange > 0 ? 'increased' : weightChange < 0 ? 'decreased' : 'stayed the same';
        const trendIcon = weightChange > 0 ? '📈' : weightChange < 0 ? '📉' : '➡️';
        const trendColor = weightChange > 0 ? 'var(--warning)' : weightChange < 0 ? 'var(--success)' : 'var(--text-muted)';
        
        analysisDiv.innerHTML = `
            <div style="background: var(--bg); padding: 20px; border-radius: 8px;">
                <div style="text-align: center; margin-bottom: 20px;">
                    <div style="font-size: 3rem; margin-bottom: 10px;">${trendIcon}</div>
                    <h4 style="margin-bottom: 10px;">30-Day Weight Change</h4>
                    <div style="font-size: 2rem; font-weight: bold; color: ${trendColor};">
                        ${Math.abs(weightChange).toFixed(1)} kg
                    </div>
                    <div style="color: var(--text-muted); margin-top: 5px;">
                        (${changePercent > 0 ? '+' : ''}${changePercent}%)
                    </div>
                </div>
                <p style="text-align: center; color: var(--text-muted);">
                    Your weight has ${trend} over the last 30 days.
                    ${weightChange < 0 ? 'Great progress! 🎉' : weightChange > 0 ? 'Keep tracking your goals! 💪' : 'Stay consistent! 👍'}
                </p>
            </div>
        `;
    } catch (error) {
        analysisDiv.innerHTML = '<p style="color: var(--danger);">Error analyzing progress</p>';
    }
}

// ===== SETTINGS VIEW =====
async function loadSettings() {
    // Load user info
    document.getElementById('settings-username').textContent = currentUser.username;
    document.getElementById('settings-email').textContent = currentUser.email;
    document.getElementById('settings-created').textContent = new Date(currentUser.created_at).toLocaleDateString();
    
    // Load profile data
    try {
        const profile = await apiRequest('/profile');
        
        if (profile.date_of_birth) document.getElementById('profile-dob').value = profile.date_of_birth;
        if (profile.height_cm) document.getElementById('profile-height').value = profile.height_cm;
        if (profile.current_weight_kg) document.getElementById('profile-weight').value = profile.current_weight_kg;
        if (profile.goal_weight_kg) document.getElementById('profile-goal-weight').value = profile.goal_weight_kg;
        if (profile.activity_level) document.getElementById('profile-activity').value = profile.activity_level;
        if (profile.goal_type) document.getElementById('profile-goal-type').value = profile.goal_type;
        if (profile.daily_calorie_target) document.getElementById('profile-calorie-target').value = profile.daily_calorie_target;
    } catch (error) {
        console.log('No profile found, creating new one');
    }
    
    // Setup form submission
    document.getElementById('profile-form').onsubmit = async (e) => {
        e.preventDefault();
        await saveProfile();
    };
}

async function saveProfile() {
    const profileData = {
        date_of_birth: document.getElementById('profile-dob').value || null,
        height_cm: parseFloat(document.getElementById('profile-height').value) || null,
        current_weight_kg: parseFloat(document.getElementById('profile-weight').value) || null,
        goal_weight_kg: parseFloat(document.getElementById('profile-goal-weight').value) || null,
        activity_level: document.getElementById('profile-activity').value,
        goal_type: document.getElementById('profile-goal-type').value,
        daily_calorie_target: parseInt(document.getElementById('profile-calorie-target').value) || null
    };
    
    try {
        // Try to update first
        try {
            await apiRequest('/profile', {
                method: 'PUT',
                body: JSON.stringify(profileData)
            });
            showToast('Profile updated successfully!');
        } catch (error) {
            // If update fails, try to create
            await apiRequest('/profile', {
                method: 'POST',
                body: JSON.stringify(profileData)
            });
            showToast('Profile created successfully!');
        }
        
        loadDashboard(); // Refresh dashboard with new data
    } catch (error) {
        showToast('Error saving profile: ' + error.message, true);
    }
}

// ===== DATA EXPORT =====
async function exportData(type) {
    try {
        if (type === 'meals') {
            const meals = await apiRequest('/meals');
            const csv = convertMealsToCSV(meals);
            downloadCSV(csv, 'meals.csv');
            showToast('Meals exported!');
        } else if (type === 'workouts') {
            const workouts = await apiRequest('/workouts');
            const csv = convertWorkoutsToCSV(workouts);
            downloadCSV(csv, 'workouts.csv');
            showToast('Workouts exported!');
        } else if (type === 'metrics') {
            const metrics = await apiRequest('/body-metrics');
            const csv = convertMetricsToCSV(metrics);
            downloadCSV(csv, 'body_metrics.csv');
            showToast('Body metrics exported!');
        } else if (type === 'all') {
            const [meals, workouts, metrics, water, goals] = await Promise.all([
                apiRequest('/meals'),
                apiRequest('/workouts'),
                apiRequest('/body-metrics'),
                apiRequest('/water'),
                apiRequest('/goals')
            ]);
            
            const allData = {
                user: currentUser,
                meals,
                workouts,
                body_metrics: metrics,
                water_intake: water,
                goals,
                exported_at: new Date().toISOString()
            };
            
            downloadJSON(allData, 'fittrack_data.json');
            showToast('All data exported!');
        }
    } catch (error) {
        showToast('Error exporting data: ' + error.message, true);
    }
}

function convertMealsToCSV(meals) {
    let csv = 'Date,Meal Type,Notes,Total Calories\n';
    meals.forEach(meal => {
        const totalCals = meal.foods.reduce((sum, mf) => sum + (mf.food.calories * mf.servings), 0);
        csv += `${meal.date},${meal.meal_type},"${meal.notes || ''}",${totalCals}\n`;
    });
    return csv;
}

function convertWorkoutsToCSV(workouts) {
    let csv = 'Date,Name,Duration (min),Calories Burned,Notes\n';
    workouts.forEach(workout => {
        csv += `${workout.date},${workout.name},${workout.duration_minutes || 0},${workout.total_calories_burned || 0},"${workout.notes || ''}"\n`;
    });
    return csv;
}

function convertMetricsToCSV(metrics) {
    let csv = 'Date,Weight (kg),Body Fat %,Notes\n';
    metrics.forEach(metric => {
        csv += `${metric.date},${metric.weight_kg},${metric.body_fat_percentage || ''},${metric.notes || ''}\n`;
    });
    return csv;
}

function downloadCSV(csv, filename) {
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    window.URL.revokeObjectURL(url);
}

function downloadJSON(data, filename) {
    const json = JSON.stringify(data, null, 2);
    const blob = new Blob([json], { type: 'application/json' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    window.URL.revokeObjectURL(url);
}
