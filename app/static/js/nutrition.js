class NutritionTracker {
    constructor() {
        this.foodItems = [];
        this.currentDate = new Date();
        this.initializeEventListeners();
        this.loadFoodItems();
        this.initializeCharts();
    }

    initializeEventListeners() {
        // Date navigation
        document.getElementById('prevDate').addEventListener('click', () => this.changeDate(-1));
        document.getElementById('nextDate').addEventListener('click', () => this.changeDate(1));
        
        // Food item search
        document.getElementById('foodSearch').addEventListener('input', (e) => this.searchFoodItems(e.target.value));
        
        // Barcode scanner
        document.getElementById('scanBarcode').addEventListener('click', () => this.startBarcodeScanner());
        
        // Meal type selection
        document.querySelectorAll('.meal-type').forEach(button => {
            button.addEventListener('click', (e) => this.selectMealType(e.target.dataset.mealType));
        });
    }

    async loadFoodItems() {
        try {
            const response = await fetch('/api/food-items');
            this.foodItems = await response.json();
            this.updateFoodItemList();
        } catch (error) {
            console.error('Error loading food items:', error);
            showToast('Error loading food items', 'error');
        }
    }

    updateFoodItemList(searchTerm = '') {
        const filteredItems = this.foodItems.filter(item => 
            item.name.toLowerCase().includes(searchTerm.toLowerCase())
        );
        
        const container = document.getElementById('foodItemsList');
        container.innerHTML = filteredItems.map(item => `
            <div class="food-item" data-id="${item.id}">
                <h3>${item.name}</h3>
                <p>Calories: ${item.calories} | Protein: ${item.protein}g | Carbs: ${item.carbs}g | Fat: ${item.fat}g</p>
                <button onclick="nutritionTracker.addFoodItem(${item.id})">Add</button>
            </div>
        `).join('');
    }

    async addFoodItem(foodItemId) {
        const quantity = prompt('Enter quantity (in servings):', '1');
        if (!quantity) return;

        try {
            const response = await fetch('/api/nutrition-log', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    food_item_id: foodItemId,
                    quantity: parseFloat(quantity),
                    date: this.formatDate(this.currentDate),
                    meal_type: this.selectedMealType
                })
            });

            if (response.ok) {
                showToast('Food item added successfully', 'success');
                this.updateNutritionStats();
            }
        } catch (error) {
            console.error('Error adding food item:', error);
            showToast('Error adding food item', 'error');
        }
    }

    async updateNutritionStats() {
        try {
            const response = await fetch(`/api/nutrition-stats?start_date=${this.formatDate(this.currentDate)}&end_date=${this.formatDate(this.currentDate)}`);
            const stats = await response.json();
            
            // Update charts
            this.updateCalorieChart(stats.calories);
            this.updateMacroChart(stats.protein, stats.carbs, stats.fat);
            
            // Update summary
            document.getElementById('calorieSummary').textContent = `Total Calories: ${stats.calories}`;
            document.getElementById('macroSummary').textContent = 
                `Protein: ${stats.protein}g | Carbs: ${stats.carbs}g | Fat: ${stats.fat}g`;
        } catch (error) {
            console.error('Error updating nutrition stats:', error);
            showToast('Error updating nutrition stats', 'error');
        }
    }

    initializeCharts() {
        // Initialize calorie chart
        this.calorieChart = new Chart(document.getElementById('calorieChart'), {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Calories',
                    data: [],
                    borderColor: 'rgb(75, 192, 192)',
                    tension: 0.1
                }]
            }
        });

        // Initialize macro chart
        this.macroChart = new Chart(document.getElementById('macroChart'), {
            type: 'doughnut',
            data: {
                labels: ['Protein', 'Carbs', 'Fat'],
                datasets: [{
                    data: [0, 0, 0],
                    backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56']
                }]
            }
        });
    }

    updateCalorieChart(calories) {
        this.calorieChart.data.labels.push(this.formatDate(this.currentDate));
        this.calorieChart.data.datasets[0].data.push(calories);
        this.calorieChart.update();
    }

    updateMacroChart(protein, carbs, fat) {
        this.macroChart.data.datasets[0].data = [protein, carbs, fat];
        this.macroChart.update();
    }

    formatDate(date) {
        return date.toISOString().split('T')[0];
    }

    changeDate(days) {
        this.currentDate.setDate(this.currentDate.getDate() + days);
        document.getElementById('currentDate').textContent = this.formatDate(this.currentDate);
        this.updateNutritionStats();
    }

    startBarcodeScanner() {
        startBarcodeScan();
    }
}

// Initialize water intake
let waterIntake = 0;
const waterGoal = 8;

// Add water glass
async function addWaterGlass() {
    try {
        const response = await fetch('/api/water', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                date: new Date().toISOString().split('T')[0],
                glasses: 1
            })
        });
        
        if (response.ok) {
            waterIntake++;
            updateWaterDisplay();
            // Show success message
            alert('Water glass added!');
        } else {
            throw new Error('Failed to add water');
        }
    } catch (error) {
        console.error('Error adding water:', error);
        alert('Error adding water glass');
    }
}

// Update water display
function updateWaterDisplay() {
    document.getElementById('waterIntake').textContent = `${waterIntake}/${waterGoal}`;
    
    // Update water glasses display
    const waterGlassesContainer = document.querySelector('.grid-cols-8');
    waterGlassesContainer.innerHTML = '';
    
    for (let i = 0; i < waterGoal; i++) {
        waterGlassesContainer.innerHTML += `
            <div class="h-8 rounded-lg ${i < waterIntake ? 'bg-blue-500' : 'bg-gray-200 dark:bg-gray-700'}"></div>
        `;
    }
}

// Load water intake
async function loadWaterIntake() {
    try {
        const date = new Date().toISOString().split('T')[0];
        const response = await fetch(`/api/water?date=${date}`);
        const data = await response.json();
        
        waterIntake = data.glasses || 0;
        updateWaterDisplay();
    } catch (error) {
        console.error('Error loading water intake:', error);
    }
}

// Initialize event listeners
document.addEventListener('DOMContentLoaded', () => {
    // Initialize water intake
    loadWaterIntake();
    
    // Add water glass button
    const addWaterButton = document.querySelector('.bg-blue-500');
    if (addWaterButton) {
        addWaterButton.addEventListener('click', addWaterGlass);
    }
    
    // Initialize nutrition tracker
    window.nutritionTracker = new NutritionTracker();
});

// Add food to meal
async function addFoodToMeal(mealType) {
    // Show food search modal
    const modal = document.createElement('div');
    modal.className = 'fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50';
    modal.innerHTML = `
        <div class="bg-white dark:bg-gray-800 p-6 rounded-lg max-w-md w-full">
            <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-4">Add Food to ${mealType.charAt(0).toUpperCase() + mealType.slice(1)}</h3>
            <div class="space-y-4">
                <div class="relative">
                    <input type="text" id="modalFoodSearch" placeholder="Search for food items..." 
                           class="w-full p-4 pl-12 rounded-lg border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-green-500 focus:border-transparent">
                    <i class="fas fa-search absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400"></i>
                </div>
                <div id="modalFoodItemsList" class="max-h-96 overflow-y-auto space-y-2">
                    <!-- Food items will be loaded here -->
                </div>
                <div class="flex justify-end space-x-4">
                    <button onclick="this.closest('.fixed').remove()" 
                            class="px-4 py-2 text-gray-600 dark:text-gray-300 hover:text-gray-800 dark:hover:text-white">
                        Cancel
                    </button>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Setup search functionality
    const searchInput = modal.querySelector('#modalFoodSearch');
    let searchTimeout;
    searchInput.addEventListener('input', (e) => {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => searchFoodForModal(e.target.value, mealType), 300);
    });
    
    // Focus the search input
    searchInput.focus();
}

// Search food for modal
async function searchFoodForModal(query, mealType) {
    if (!query) {
        document.getElementById('modalFoodItemsList').innerHTML = '';
        return;
    }

    try {
        const response = await fetch(`/api/food/search?q=${encodeURIComponent(query)}`);
        if (!response.ok) {
            throw new Error('Search failed');
        }
        
        const foods = await response.json();
        const foodList = document.getElementById('modalFoodItemsList');
        
        if (!foods || foods.length === 0) {
            foodList.innerHTML = `
                <div class="text-center py-4 text-gray-500 dark:text-gray-400">
                    No food items found. Try a different search term.
                </div>
            `;
            return;
        }
        
        foodList.innerHTML = foods.map(food => `
            <div class="bg-gray-50 dark:bg-gray-700 p-4 rounded-lg flex justify-between items-center">
                <div>
                    <h4 class="font-semibold text-gray-900 dark:text-white">${food.name}</h4>
                    <p class="text-sm text-gray-500 dark:text-gray-400">
                        ${food.calories} cal | P: ${food.protein}g | C: ${food.carbs}g | F: ${food.fat}g
                    </p>
                </div>
                <button onclick="addFoodToMealEntry(${food.id}, '${mealType}')" 
                        class="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-lg transition-colors">
                    Add
                </button>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error searching food:', error);
        document.getElementById('modalFoodItemsList').innerHTML = `
            <div class="text-center py-4 text-red-500">
                Error searching for food items. Please try again.
            </div>
        `;
    }
}

// Add food to meal entry
async function addFoodToMealEntry(foodId, mealType, servings = 1.0) {
    try {
        const response = await fetch('/api/meals', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                food_item_id: foodId,
                meal_type: mealType,
                servings: servings,
                date: new Date().toISOString().split('T')[0]
            })
        });
        
        if (response.ok) {
            // Close the modal
            document.querySelector('.fixed').remove();
            // Reload meals
            loadMeals();
            // Show success message
            alert('Food added successfully!');
        } else {
            throw new Error('Failed to add food');
        }
    } catch (error) {
        console.error('Error adding food:', error);
        alert('Error adding food to meal');
    }
}

// Load meals for the current date
async function loadMeals() {
    try {
        const date = new Date().toISOString().split('T')[0];
        const response = await fetch(`/api/meals?date=${date}`);
        const meals = await response.json();
        
        // Clear existing meals
        ['breakfast', 'lunch', 'dinner', 'snack'].forEach(mealType => {
            document.getElementById(`${mealType}Items`).innerHTML = '';
        });
        
        // Add meals to their respective sections
        meals.forEach(meal => {
            const mealSection = document.getElementById(`${meal.meal_type}Items`);
            mealSection.innerHTML += `
                <div class="bg-gray-50 dark:bg-gray-700 p-4 rounded-lg flex justify-between items-center">
                    <div>
                        <h4 class="font-semibold text-gray-900 dark:text-white">${meal.food.name}</h4>
                        <p class="text-sm text-gray-500 dark:text-gray-400">
                            ${meal.food.calories * meal.servings} cal | P: ${meal.food.protein * meal.servings}g | 
                            C: ${meal.food.carbs * meal.servings}g | F: ${meal.food.fat * meal.servings}g
                        </p>
                    </div>
                    <div class="flex items-center space-x-2">
                        <span class="text-sm text-gray-500 dark:text-gray-400">${meal.servings} serving(s)</span>
                        <button onclick="removeMeal(${meal.id})" class="text-red-500 hover:text-red-600">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </div>
            `;
        });
        
        // Update nutrition stats
        updateNutritionStats();
    } catch (error) {
        console.error('Error loading meals:', error);
        alert('Error loading meals');
    }
}

// Remove a meal
async function removeMeal(mealId) {
    if (!confirm('Are you sure you want to remove this food item?')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/meals/${mealId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            loadMeals();
        } else {
            throw new Error('Failed to remove meal');
        }
    } catch (error) {
        console.error('Error removing meal:', error);
        alert('Error removing food item');
    }
}

// Start barcode scanning
async function startBarcodeScan() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } });
        
        // Create modal for scanner
        const modal = document.createElement('div');
        modal.className = 'fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50';
        modal.innerHTML = `
            <div class="bg-white dark:bg-gray-800 p-6 rounded-lg max-w-md w-full">
                <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-4">Scan Barcode</h3>
                <div class="relative">
                    <video class="w-full rounded-lg"></video>
                    <div class="absolute inset-0 border-2 border-green-500"></div>
                </div>
                <p class="text-center mt-4 text-gray-600 dark:text-gray-300">Position barcode in frame</p>
                <div class="flex justify-end mt-4">
                    <button class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg transition-colors">
                        Cancel
                    </button>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        const videoElement = modal.querySelector('video');
        videoElement.srcObject = stream;
        await videoElement.play();

        // Initialize barcode scanner
        const codeReader = new ZXing.BrowserMultiFormatReader();
        let scanning = true;

        codeReader.decodeFromVideoDevice(null, videoElement, (result, err) => {
            if (result && scanning) {
                scanning = false;
                handleBarcodeResult(result.text);
                codeReader.reset();
                stream.getTracks().forEach(track => track.stop());
                modal.remove();
            }
        });

        // Cancel button
        modal.querySelector('button').addEventListener('click', () => {
            scanning = false;
            codeReader.reset();
            stream.getTracks().forEach(track => track.stop());
            modal.remove();
        });
    } catch (error) {
        console.error('Error starting barcode scanner:', error);
        alert('Error accessing camera. Please make sure you have granted camera permissions.');
    }
}

// Handle barcode scan result
async function handleBarcodeResult(barcode) {
    try {
        const response = await fetch(`/api/food/barcode/${barcode}`);
        const food = await response.json();
        
        if (food.error) {
            alert('Food not found in database');
            return;
        }

        // Show food details modal
        const modal = document.createElement('div');
        modal.className = 'fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50';
        modal.innerHTML = `
            <div class="bg-white dark:bg-gray-800 p-6 rounded-lg max-w-md w-full">
                <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-4">${food.name}</h3>
                <div class="space-y-4">
                    <div class="grid grid-cols-2 gap-4 text-sm">
                        <div>
                            <p class="text-gray-500 dark:text-gray-400">Calories</p>
                            <p class="font-semibold text-gray-900 dark:text-white">${food.calories} cal</p>
                        </div>
                        <div>
                            <p class="text-gray-500 dark:text-gray-400">Protein</p>
                            <p class="font-semibold text-gray-900 dark:text-white">${food.protein}g</p>
                        </div>
                        <div>
                            <p class="text-gray-500 dark:text-gray-400">Carbs</p>
                            <p class="font-semibold text-gray-900 dark:text-white">${food.carbs}g</p>
                        </div>
                        <div>
                            <p class="text-gray-500 dark:text-gray-400">Fat</p>
                            <p class="font-semibold text-gray-900 dark:text-white">${food.fat}g</p>
                        </div>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Add to Meal</label>
                        <select class="w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white p-2">
                            <option value="breakfast">Breakfast</option>
                            <option value="lunch">Lunch</option>
                            <option value="dinner">Dinner</option>
                            <option value="snack">Snack</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Servings</label>
                        <input type="number" min="0.1" step="0.1" value="1.0" 
                               class="w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white p-2">
                    </div>
                    <div class="flex justify-end space-x-4">
                        <button class="px-4 py-2 text-gray-600 dark:text-gray-300 hover:text-gray-800 dark:hover:text-white">
                            Cancel
                        </button>
                        <button class="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-lg transition-colors">
                            Add to Meal
                        </button>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        
        // Add event listeners
        const addButton = modal.querySelector('button:last-child');
        addButton.addEventListener('click', () => {
            const mealType = modal.querySelector('select').value;
            const servings = parseFloat(modal.querySelector('input').value);
            addFoodToMealEntry(food.id, mealType, servings);
            modal.remove();
        });
        
        modal.querySelector('button:first-child').addEventListener('click', () => {
            modal.remove();
        });
    } catch (error) {
        console.error('Error handling barcode result:', error);
        alert('Error looking up food item');
    }
}
