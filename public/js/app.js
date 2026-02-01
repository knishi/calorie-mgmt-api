import { API } from './api.js';

// DOM Elements
const tabs = document.querySelectorAll('.tab');
const contents = document.querySelectorAll('.tab-content');
const mealForm = document.getElementById('meal-form');
const profileForm = document.getElementById('profile-form');
const goalForm = document.getElementById('goal-form');

// State Initialization
async function init() {
    await refreshDashboard();
    setupEventListeners();
}

// UI Refreshers
async function refreshDashboard() {
    try {
        const summary = await API.getSummary();
        const meals = await API.getMeals();

        // Update Summary Card
        document.getElementById('total-consumed').textContent = summary.total_consumed;
        document.getElementById('daily-goal').textContent = summary.daily_goal;
        document.getElementById('remaining-value').textContent = summary.remaining;

        const progress = Math.min((summary.total_consumed / summary.daily_goal) * 100, 100);
        document.getElementById('progress-fill').style.width = `${progress}%`;

        renderHistory(meals);
        renderProfile();
    } catch (err) {
        console.error('Failed to refresh dashboard', err);
    }
}

function renderHistory(meals) {
    const historyList = document.getElementById('meal-history');
    historyList.innerHTML = meals.slice(0, 10).map(meal => `
    <li class="history-item">
      <div class="history-info">
        <div class="food-name">${meal.food_name}</div>
        <div class="time">${new Date(meal.consumed_at).toLocaleTimeString()}</div>
      </div>
      <div class="history-cals">${meal.calories} kcal</div>
    </li>
  `).join('');
}

async function renderProfile() {
    try {
        const profile = await API.getProfile();
        const goals = await API.getGoals();

        // Fill Profile Form
        document.getElementById('gender').value = profile.gender || 'male';
        document.getElementById('age').value = profile.age || '';
        document.getElementById('height').value = profile.height || '';
        document.getElementById('weight').value = profile.weight || '';

        // Fill Goal Form
        document.getElementById('target-weight').value = goals.target_weight || '';
        if (goals.target_date) {
            document.getElementById('target-date').value = goals.target_date.split('T')[0];
        }
    } catch (err) {
        console.warn('Profile/Goals not set yet');
    }
}

// Event Listeners
function setupEventListeners() {
    // Tab Switching
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('active'));
            contents.forEach(c => c.classList.add('hidden'));

            tab.classList.add('active');
            document.getElementById(tab.dataset.tab).classList.remove('hidden');
        });
    });

    // Meal Submission
    mealForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const data = {
            food_name: document.getElementById('food-name').value,
            calories: parseInt(document.getElementById('calories').value)
        };

        try {
            await API.addMeal(data);
            mealForm.reset();
            await refreshDashboard();
            alert('Meal added!');
        } catch (err) {
            alert('Error: ' + err.message);
        }
    });

    // Profile Submission
    profileForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const data = {
            gender: document.getElementById('gender').value,
            age: parseInt(document.getElementById('age').value),
            height: parseInt(document.getElementById('height').value),
            weight: parseInt(document.getElementById('weight').value)
        };
        try {
            await API.updateProfile(data);
            alert('Profile updated!');
            await refreshDashboard();
        } catch (err) {
            alert('Error: ' + err.message);
        }
    });

    // Goal Submission
    goalForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const data = {
            target_weight: parseInt(document.getElementById('target-weight').value),
            target_date: document.getElementById('target-date').value
        };
        try {
            await API.updateGoals(data);
            alert('Goal set! Daily target recalculated.');
            await refreshDashboard();
        } catch (err) {
            alert('Error: ' + err.message);
        }
    });
}

// Let's go!
init();
