class WorkoutTimer {
    constructor() {
        // DOM Elements
        this.timer = document.getElementById('timer');
        this.startBtn = document.getElementById('startBtn');
        this.pauseBtn = document.getElementById('pauseBtn');
        this.resetBtn = document.getElementById('resetBtn');
        this.progressBar = document.getElementById('progressBar');
        this.progressText = document.getElementById('progress');
        this.exerciseName = document.getElementById('exerciseName');
        this.formVideo = document.getElementById('formVideo');
        this.exerciseTips = document.getElementById('exerciseTips');
        this.nextExerciseName = document.getElementById('nextExerciseName');
        this.workoutStats = document.getElementById('workoutStats');

        // Timer State
        this.timeLeft = 0;
        this.totalTime = 0;
        this.currentExercise = 0;
        this.exercises = [];
        this.timerInterval = null;
        this.isPaused = false;
        this.workoutStartTime = null;
        this.totalWorkoutTime = 0;
        this.completedExercises = 0;

        // Sound Effects
        this.sounds = {
            start: new Audio('/static/sounds/start.mp3'),
            complete: new Audio('/static/sounds/complete.mp3'),
            rest: new Audio('/static/sounds/rest.mp3'),
            warning: new Audio('/static/sounds/warning.mp3')
        };

        this.initializeEventListeners();
        this.setupKeyboardShortcuts();
    }

    initializeEventListeners() {
        this.startBtn.addEventListener('click', () => this.startTimer());
        this.pauseBtn.addEventListener('click', () => this.pauseTimer());
        this.resetBtn.addEventListener('click', () => this.resetTimer());

        // Add touch events for mobile
        this.startBtn.addEventListener('touchstart', (e) => {
            e.preventDefault();
            this.startTimer();
        });
        this.pauseBtn.addEventListener('touchstart', (e) => {
            e.preventDefault();
            this.pauseTimer();
        });
        this.resetBtn.addEventListener('touchstart', (e) => {
            e.preventDefault();
            this.resetTimer();
        });
    }

    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            if (e.code === 'Space') {
                e.preventDefault();
                if (this.isPaused) {
                    this.startTimer();
                } else {
                    this.pauseTimer();
                }
            } else if (e.code === 'KeyR') {
                this.resetTimer();
            }
        });
    }

    async loadWorkout(workoutId) {
        try {
            const response = await fetch(`/api/workouts/${workoutId}`);
            const data = await response.json();
            this.exercises = data.exercises;
            this.currentExercise = 0;
            this.workoutStartTime = new Date();
            this.updateExerciseDisplay();
            this.updateWorkoutStats();
            animateElement(this.progressBar, 'fade-in');
            showToast('Workout loaded successfully', 'success');
        } catch (error) {
            console.error('Error loading workout:', error);
            showToast('Error loading workout', 'error');
        }
    }

    updateExerciseDisplay() {
        const exercise = this.exercises[this.currentExercise];
        this.exerciseName.textContent = exercise.name;
        this.timeLeft = exercise.duration;
        this.totalTime = exercise.duration;
        this.updateTimerDisplay();
        this.updateProgress();
        this.loadExerciseForm(exercise.id);
        this.updateNextExercise();
    }

    updateNextExercise() {
        if (this.currentExercise < this.exercises.length - 1) {
            const nextExercise = this.exercises[this.currentExercise + 1];
            this.nextExerciseName.textContent = `Next: ${nextExercise.name}`;
        } else {
            this.nextExerciseName.textContent = 'Final Exercise';
        }
    }

    updateWorkoutStats() {
        const elapsedTime = Math.floor((new Date() - this.workoutStartTime) / 1000);
        this.totalWorkoutTime = elapsedTime;
        
        const stats = {
            'Total Time': this.formatTime(elapsedTime),
            'Exercises Completed': this.completedExercises,
            'Remaining Exercises': this.exercises.length - this.currentExercise - 1
        };

        this.workoutStats.innerHTML = Object.entries(stats)
            .map(([key, value]) => `<div class="stat-item"><span class="stat-label">${key}:</span> ${value}</div>`)
            .join('');
    }

    formatTime(seconds) {
        const hours = Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        const secs = seconds % 60;
        return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }

    updateTimerDisplay() {
        const minutes = Math.floor(this.timeLeft / 60);
        const seconds = this.timeLeft % 60;
        this.timer.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        
        // Add warning when time is running low
        if (this.timeLeft <= 5) {
            this.timer.classList.add('text-red-500');
            if (this.timeLeft === 5) {
                this.sounds.warning.play();
            }
        } else {
            this.timer.classList.remove('text-red-500');
        }
    }

    updateProgress() {
        const progress = ((this.currentExercise + 1) / this.exercises.length) * 100;
        animateProgressBar(this.progressBar, progress);
        this.progressText.textContent = `${this.currentExercise + 1}/${this.exercises.length}`;
    }

    async loadExerciseForm(exerciseId) {
        try {
            const response = await fetch(`/api/exercises/${exerciseId}/form`);
            const data = await response.json();
            this.formVideo.src = data.video_url;
            this.exerciseTips.innerHTML = data.form_tips;
            this.formVideo.addEventListener('error', () => handleImageError(this.formVideo));
        } catch (error) {
            console.error('Error loading exercise form:', error);
            showToast('Error loading exercise form', 'error');
        }
    }

    startTimer() {
        if (this.isPaused) {
            this.isPaused = false;
        } else {
            this.timeLeft = this.exercises[this.currentExercise].duration;
            this.sounds.start.play();
        }

        this.startBtn.classList.add('hidden');
        this.pauseBtn.classList.remove('hidden');
        animateElement(this.pauseBtn, 'fade-in');

        this.timerInterval = setInterval(() => {
            if (this.timeLeft > 0) {
                this.timeLeft--;
                this.updateTimerDisplay();
                this.updateWorkoutStats();
            } else {
                this.handleExerciseComplete();
            }
        }, 1000);
    }

    pauseTimer() {
        this.isPaused = true;
        clearInterval(this.timerInterval);
        this.startBtn.classList.remove('hidden');
        this.pauseBtn.classList.add('hidden');
        animateElement(this.startBtn, 'fade-in');
    }

    resetTimer() {
        clearInterval(this.timerInterval);
        this.timeLeft = this.exercises[this.currentExercise].duration;
        this.updateTimerDisplay();
        this.startBtn.classList.remove('hidden');
        this.pauseBtn.classList.add('hidden');
        this.isPaused = false;
        animateElement(this.resetBtn, 'fade-in');
    }

    handleExerciseComplete() {
        clearInterval(this.timerInterval);
        this.sounds.complete.play();
        this.completedExercises++;
        
        if (this.currentExercise < this.exercises.length - 1) {
            this.currentExercise++;
            this.updateExerciseDisplay();
            this.startRestPeriod();
            showToast('Exercise completed!', 'success');
        } else {
            this.handleWorkoutComplete();
        }
    }

    startRestPeriod() {
        const restDuration = this.exercises[this.currentExercise].rest_duration || 60;
        this.timeLeft = restDuration;
        this.updateTimerDisplay();
        this.startTimer();
        this.sounds.rest.play();
        showToast('Rest period started', 'success');
    }

    async handleWorkoutComplete() {
        try {
            const workoutData = {
                workout_id: this.workoutId,
                completed_at: new Date().toISOString(),
                total_time: this.totalWorkoutTime,
                exercises_completed: this.completedExercises
            };

            await fetch('/api/workouts/complete', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(workoutData)
            });
            
            showToast('Workout completed! Great job!', 'success');
            
            // Redirect to workout history
            window.location.href = '/workout/history';
        } catch (error) {
            console.error('Error completing workout:', error);
            showToast('Error saving workout completion', 'error');
        }
    }
}

// Initialize timer when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const timer = new WorkoutTimer();
    // Load workout if workoutId is present in URL
    const urlParams = new URLSearchParams(window.location.search);
    const workoutId = urlParams.get('workout');
    if (workoutId) {
        timer.loadWorkout(workoutId);
    }
});
