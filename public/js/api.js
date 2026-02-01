/**
 * API Client Layer
 * Decoupled communication with the Calorie Management API
 */

const urlParams = new URLSearchParams(window.location.search);
const apiPort = urlParams.get('api_port') || '8080';
const BASE_URL = `http://localhost:${apiPort}/v1`;
const TOKEN = 'SECRET_TOKEN';

async function request(endpoint, method = 'GET', body = null) {
    const options = {
        method,
        headers: {
            'Content-Type': 'application/json',
            'X-Auth-Token': TOKEN
        }
    };

    if (body) {
        options.body = JSON.stringify(body);
    }

    try {
        const response = await fetch(`${BASE_URL}${endpoint}`, options);

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.error?.message || `HTTP error! status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error(`API Request Failed (${endpoint}):`, error);
        throw error;
    }
}

export const API = {
    getProfile: () => request('/profile'),
    updateProfile: (data) => request('/profile', 'POST', data),

    getGoals: () => request('/goals'),
    updateGoals: (data) => request('/goals', 'POST', data),

    getMeals: () => request('/meals'),
    addMeal: (data) => request('/meals', 'POST', data),

    getSummary: () => request('/summary')
};
