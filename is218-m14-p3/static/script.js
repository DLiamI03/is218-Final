// API Base URL
const API_URL = '';

// Token storage
let accessToken = localStorage.getItem('accessToken');
let currentUser = null;

// DOM Elements
const authSection = document.getElementById('auth-section');
const appSection = document.getElementById('app-section');
const loginForm = document.getElementById('loginForm');
const registerForm = document.getElementById('registerForm');
const calculationForm = document.getElementById('calculationForm');
const calculationsList = document.getElementById('calculations-list');
const usernameDisplay = document.getElementById('username-display');
const toast = document.getElementById('toast');

// Toggle between login and register
document.getElementById('show-register').addEventListener('click', (e) => {
    e.preventDefault();
    document.getElementById('login-form').style.display = 'none';
    document.getElementById('register-form').style.display = 'block';
});

document.getElementById('show-login').addEventListener('click', (e) => {
    e.preventDefault();
    document.getElementById('register-form').style.display = 'none';
    document.getElementById('login-form').style.display = 'block';
});

// Show toast message
function showToast(message, type = 'info') {
    toast.textContent = message;
    toast.className = `toast ${type} show`;
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// API Request Helper
async function apiRequest(endpoint, options = {}) {
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };

    if (accessToken && !endpoint.includes('token') && !endpoint.includes('register')) {
        headers['Authorization'] = `Bearer ${accessToken}`;
    }

    try {
        const response = await fetch(`${API_URL}${endpoint}`, {
            ...options,
            headers
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Request failed');
        }

        // Handle 204 No Content
        if (response.status === 204) {
            return null;
        }

        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// Register Handler
registerForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const username = document.getElementById('register-username').value;
    const email = document.getElementById('register-email').value;
    const password = document.getElementById('register-password').value;

    try {
        await apiRequest('/register', {
            method: 'POST',
            body: JSON.stringify({ username, email, password })
        });

        showToast('Registration successful! Please login.', 'success');
        document.getElementById('show-login').click();
        registerForm.reset();
    } catch (error) {
        showToast(error.message, 'error');
    }
});

// Login Handler
loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;

    try {
        // Create form data for OAuth2
        const formData = new URLSearchParams();
        formData.append('username', username);
        formData.append('password', password);

        const response = await fetch(`${API_URL}/token`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: formData
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Login failed');
        }

        const data = await response.json();
        accessToken = data.access_token;
        localStorage.setItem('accessToken', accessToken);

        // Get current user
        await loadCurrentUser();
        
        // Show app section
        authSection.style.display = 'none';
        appSection.style.display = 'block';
        
        showToast('Login successful!', 'success');
        loginForm.reset();
        
        // Load calculations
        await loadCalculations();
    } catch (error) {
        showToast(error.message, 'error');
    }
});

// Load current user
async function loadCurrentUser() {
    try {
        currentUser = await apiRequest('/users/me');
        usernameDisplay.textContent = `Welcome, ${currentUser.username}!`;
    } catch (error) {
        console.error('Failed to load user:', error);
    }
}

// Logout Handler
document.getElementById('logout-btn').addEventListener('click', () => {
    accessToken = null;
    currentUser = null;
    localStorage.removeItem('accessToken');
    
    appSection.style.display = 'none';
    authSection.style.display = 'block';
    
    calculationsList.innerHTML = '<p class="loading">Loading calculations...</p>';
    calculationForm.reset();
    
    showToast('Logged out successfully', 'info');
});

// Format operation symbol
function getOperationSymbol(operation) {
    const symbols = {
        'add': '+',
        'subtract': '-',
        'multiply': '×',
        'divide': '÷'
    };
    return symbols[operation] || operation;
}

// Format date
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString();
}

// Load Calculations (Browse)
async function loadCalculations() {
    try {
        calculationsList.innerHTML = '<p class="loading">Loading calculations...</p>';
        
        const calculations = await apiRequest('/calculations');
        
        if (calculations.length === 0) {
            calculationsList.innerHTML = '<p class="empty-state">No calculations yet. Add your first calculation above!</p>';
            return;
        }

        calculationsList.innerHTML = calculations.map(calc => `
            <div class="calculation-item" data-id="${calc.id}">
                <div class="calculation-info">
                    <div class="calculation-expression">
                        ${calc.operand1} ${getOperationSymbol(calc.operation)} ${calc.operand2}
                    </div>
                    <div class="calculation-result">
                        = ${calc.result}
                    </div>
                    <div class="calculation-meta">
                        Created: ${formatDate(calc.created_at)}
                        ${calc.updated_at !== calc.created_at ? `| Updated: ${formatDate(calc.updated_at)}` : ''}
                    </div>
                </div>
                <div class="calculation-actions">
                    <button class="btn btn-success" onclick="editCalculation(${calc.id})">Edit</button>
                    <button class="btn btn-danger" onclick="deleteCalculation(${calc.id})">Delete</button>
                </div>
            </div>
        `).join('');
    } catch (error) {
        calculationsList.innerHTML = `<p class="error">Failed to load calculations: ${error.message}</p>`;
    }
}

// Add/Update Calculation
calculationForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const calculationId = document.getElementById('calculation-id').value;
    const operand1 = parseFloat(document.getElementById('operand1').value);
    const operand2 = parseFloat(document.getElementById('operand2').value);
    const operation = document.getElementById('operation').value;

    // Validation
    if (!operation) {
        showToast('Please select an operation', 'error');
        return;
    }

    if (operation === 'divide' && operand2 === 0) {
        showToast('Cannot divide by zero', 'error');
        return;
    }

    const data = { operand1, operand2, operation };

    try {
        if (calculationId) {
            // Update existing calculation
            await apiRequest(`/calculations/${calculationId}`, {
                method: 'PUT',
                body: JSON.stringify(data)
            });
            showToast('Calculation updated successfully!', 'success');
        } else {
            // Add new calculation
            await apiRequest('/calculations', {
                method: 'POST',
                body: JSON.stringify(data)
            });
            showToast('Calculation added successfully!', 'success');
        }

        // Reset form and reload calculations
        calculationForm.reset();
        document.getElementById('calculation-id').value = '';
        document.getElementById('form-title').textContent = 'Add New Calculation';
        document.getElementById('submit-btn').textContent = 'Add Calculation';
        document.getElementById('cancel-btn').style.display = 'none';
        
        await loadCalculations();
    } catch (error) {
        showToast(error.message, 'error');
    }
});

// Edit Calculation
async function editCalculation(id) {
    try {
        // Get calculation details (Read)
        const calculation = await apiRequest(`/calculations/${id}`);
        
        // Populate form
        document.getElementById('calculation-id').value = calculation.id;
        document.getElementById('operand1').value = calculation.operand1;
        document.getElementById('operand2').value = calculation.operand2;
        document.getElementById('operation').value = calculation.operation;
        
        // Update form UI
        document.getElementById('form-title').textContent = 'Edit Calculation';
        document.getElementById('submit-btn').textContent = 'Update Calculation';
        document.getElementById('cancel-btn').style.display = 'inline-block';
        
        // Scroll to form
        document.querySelector('.card').scrollIntoView({ behavior: 'smooth' });
    } catch (error) {
        showToast(error.message, 'error');
    }
}

// Cancel Edit
document.getElementById('cancel-btn').addEventListener('click', () => {
    calculationForm.reset();
    document.getElementById('calculation-id').value = '';
    document.getElementById('form-title').textContent = 'Add New Calculation';
    document.getElementById('submit-btn').textContent = 'Add Calculation';
    document.getElementById('cancel-btn').style.display = 'none';
});

// Delete Calculation
async function deleteCalculation(id) {
    if (!confirm('Are you sure you want to delete this calculation?')) {
        return;
    }

    try {
        await apiRequest(`/calculations/${id}`, {
            method: 'DELETE'
        });
        
        showToast('Calculation deleted successfully!', 'success');
        await loadCalculations();
    } catch (error) {
        showToast(error.message, 'error');
    }
}

// Refresh calculations
document.getElementById('refresh-btn').addEventListener('click', loadCalculations);

// Initialize app
if (accessToken) {
    loadCurrentUser().then(() => {
        authSection.style.display = 'none';
        appSection.style.display = 'block';
        loadCalculations();
    }).catch(() => {
        // Token invalid, clear it
        accessToken = null;
        localStorage.removeItem('accessToken');
    });
}
