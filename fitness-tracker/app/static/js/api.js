// API utility functions
const api = {
    // Activities
    async getActivities() {
        try {
            const response = await fetch(API_ENDPOINTS.activities);
            if (!response.ok) throw new Error('Failed to fetch activities');
            return await response.json();
        } catch (error) {
            handleApiError(error);
            return [];
        }
    },

    async createActivity(data) {
        try {
            const response = await fetch(API_ENDPOINTS.activities, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            if (!response.ok) throw new Error('Failed to create activity');
            return await response.json();
        } catch (error) {
            handleApiError(error);
            return null;
        }
    },

    // Goals
    async getGoals() {
        try {
            const response = await fetch(API_ENDPOINTS.goals);
            if (!response.ok) throw new Error('Failed to fetch goals');
            return await response.json();
        } catch (error) {
            handleApiError(error);
            return [];
        }
    },

    async createGoal(data) {
        try {
            const response = await fetch(API_ENDPOINTS.goals, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            if (!response.ok) throw new Error('Failed to create goal');
            return await response.json();
        } catch (error) {
            handleApiError(error);
            return null;
        }
    },

    async updateGoal(goalId, data) {
        try {
            const response = await fetch(`${API_ENDPOINTS.goals}/${goalId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            if (!response.ok) throw new Error('Failed to update goal');
            return await response.json();
        } catch (error) {
            handleApiError(error);
            return null;
        }
    },

    async deleteGoal(goalId) {
        try {
            const response = await fetch(`${API_ENDPOINTS.goals}/${goalId}`, {
                method: 'DELETE'
            });
            if (!response.ok) throw new Error('Failed to delete goal');
            return await response.json();
        } catch (error) {
            handleApiError(error);
            return null;
        }
    },

    // Nutrition
    async getFoodItems() {
        try {
            const response = await fetch(API_ENDPOINTS.nutrition.foodItems);
            if (!response.ok) throw new Error('Failed to fetch food items');
            return await response.json();
        } catch (error) {
            handleApiError(error);
            return [];
        }
    },

    async createFoodItem(data) {
        try {
            const response = await fetch(API_ENDPOINTS.nutrition.foodItems, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            if (!response.ok) throw new Error('Failed to create food item');
            return await response.json();
        } catch (error) {
            handleApiError(error);
            return null;
        }
    },

    async logFood(data) {
        try {
            const response = await fetch(API_ENDPOINTS.nutrition.nutritionLog, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            if (!response.ok) throw new Error('Failed to log food');
            return await response.json();
        } catch (error) {
            handleApiError(error);
            return null;
        }
    },

    async getNutritionStats(startDate, endDate) {
        try {
            const response = await fetch(`${API_ENDPOINTS.nutrition.nutritionStats}?start_date=${startDate}&end_date=${endDate}`);
            if (!response.ok) throw new Error('Failed to fetch nutrition stats');
            return await response.json();
        } catch (error) {
            handleApiError(error);
            return null;
        }
    },

    // Workouts
    async getWorkouts() {
        try {
            const response = await fetch(API_ENDPOINTS.workouts);
            if (!response.ok) throw new Error('Failed to fetch workouts');
            return await response.json();
        } catch (error) {
            handleApiError(error);
            return [];
        }
    },

    async getWorkout(workoutId) {
        try {
            const response = await fetch(`${API_ENDPOINTS.workouts}/${workoutId}`);
            if (!response.ok) throw new Error('Failed to fetch workout');
            return await response.json();
        } catch (error) {
            handleApiError(error);
            return null;
        }
    },

    async completeWorkout(data) {
        try {
            const response = await fetch(`${API_ENDPOINTS.workouts}/complete`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            if (!response.ok) throw new Error('Failed to complete workout');
            return await response.json();
        } catch (error) {
            handleApiError(error);
            return null;
        }
    },

    // Consultations
    async getConsultations() {
        try {
            const response = await fetch(API_ENDPOINTS.consultations);
            if (!response.ok) throw new Error('Failed to fetch consultations');
            return await response.json();
        } catch (error) {
            handleApiError(error);
            return [];
        }
    },

    async createConsultation(data) {
        try {
            const response = await fetch(API_ENDPOINTS.consultations, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            if (!response.ok) throw new Error('Failed to create consultation');
            return await response.json();
        } catch (error) {
            handleApiError(error);
            return null;
        }
    },

    async cancelConsultation(consultationId) {
        try {
            const response = await fetch(`${API_ENDPOINTS.consultations}/${consultationId}/cancel`, {
                method: 'POST'
            });
            if (!response.ok) throw new Error('Failed to cancel consultation');
            return await response.json();
        } catch (error) {
            handleApiError(error);
            return null;
        }
    }
}; 