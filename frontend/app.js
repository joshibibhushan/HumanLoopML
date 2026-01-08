// Configuration - Auto-detects environment
// For local development: uses localhost
// For production (GitHub Pages): uses Render backend
// To update Render URL: Change the RENDER_BACKEND_URL below
const RENDER_BACKEND_URL = 'https://humanloopml.onrender.com';

// Auto-detect environment
const isProduction = window.location.hostname !== 'localhost' && 
                     window.location.hostname !== '127.0.0.1' &&
                     !window.location.hostname.startsWith('192.168.');

const API_BASE_URL = isProduction ? RENDER_BACKEND_URL : 'http://localhost:8000';

// State
let currentText = '';
let currentPrediction = '';
let selectedLabel = '';
let performanceChart = null;

// DOM Elements
const textInput = document.getElementById('textInput');
const predictBtn = document.getElementById('predictBtn');
const predictionResult = document.getElementById('predictionResult');
const predictionText = document.getElementById('predictionText');
const confidenceText = document.getElementById('confidenceText');
const modelVersion = document.getElementById('modelVersion');
const correctBtn = document.getElementById('correctBtn');
const incorrectBtn = document.getElementById('incorrectBtn');
const feedbackSection = document.getElementById('feedbackSection');
const labelButtons = document.querySelectorAll('.label-btn');
const submitFeedbackBtn = document.getElementById('submitFeedbackBtn');
const statusMessage = document.getElementById('statusMessage');
const currentModelVersion = document.getElementById('currentModelVersion');
const currentAccuracy = document.getElementById('currentAccuracy');
const currentF1 = document.getElementById('currentF1');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadMetrics();
    initializeChart();
    setupEventListeners();
});

// Event Listeners
function setupEventListeners() {
    predictBtn.addEventListener('click', handlePredict);
    correctBtn.addEventListener('click', handleCorrect);
    incorrectBtn.addEventListener('click', handleIncorrect);
    
    labelButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            // Remove previous selection
            labelButtons.forEach(b => b.classList.remove('selected'));
            // Select clicked button
            btn.classList.add('selected');
            selectedLabel = btn.dataset.label;
            submitFeedbackBtn.classList.remove('hidden');
        });
    });
    
    submitFeedbackBtn.addEventListener('click', handleSubmitFeedback);
    
    // Allow Enter key to predict (Shift+Enter for new line)
    textInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handlePredict();
        }
    });
}

// Prediction
async function handlePredict() {
    const text = textInput.value.trim();
    
    if (!text) {
        showStatus('Please enter some text to classify.', 'error');
        return;
    }
    
    currentText = text;
    setLoading(true);
    hideStatus();
    
    try {
        const response = await fetch(`${API_BASE_URL}/predict`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: text })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Display prediction
        predictionText.textContent = data.prediction;
        confidenceText.textContent = (data.confidence * 100).toFixed(1) + '%';
        modelVersion.textContent = data.model_version;
        
        currentPrediction = data.prediction;
        predictionResult.classList.remove('hidden');
        feedbackSection.classList.add('hidden');
        
        // Reset feedback state
        selectedLabel = '';
        labelButtons.forEach(b => b.classList.remove('selected'));
        submitFeedbackBtn.classList.add('hidden');
        
    } catch (error) {
        console.error('Prediction error:', error);
        showStatus('Error making prediction. Please check if the backend is running.', 'error');
    } finally {
        setLoading(false);
    }
}

// Feedback Handlers
function handleCorrect() {
    showStatus('Thank you for confirming the prediction is correct!', 'success');
    feedbackSection.classList.add('hidden');
}

async function handleIncorrect() {
    feedbackSection.classList.remove('hidden');
    submitFeedbackBtn.classList.add('hidden');
    selectedLabel = '';
    labelButtons.forEach(b => b.classList.remove('selected'));
}

async function handleSubmitFeedback() {
    if (!selectedLabel) {
        showStatus('Please select the correct label.', 'error');
        return;
    }
    
    setLoading(true);
    
    try {
        const response = await fetch(`${API_BASE_URL}/feedback`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: currentText,
                model_prediction: currentPrediction,
                human_label: selectedLabel
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        showStatus('Feedback submitted successfully! Thank you for helping improve the model.', 'success');
        
        // Reset UI
        feedbackSection.classList.add('hidden');
        predictionResult.classList.add('hidden');
        textInput.value = '';
        
        // Reload metrics to show updated performance
        setTimeout(() => {
            loadMetrics();
        }, 1000);
        
    } catch (error) {
        console.error('Feedback error:', error);
        showStatus('Error submitting feedback. Please try again.', 'error');
    } finally {
        setLoading(false);
    }
}

// Metrics
async function loadMetrics() {
    try {
        const response = await fetch(`${API_BASE_URL}/metrics`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        const metrics = data.metrics;
        
        // Update current metrics display
        currentModelVersion.textContent = data.version;
        currentAccuracy.textContent = (metrics.accuracy * 100).toFixed(2) + '%';
        currentF1.textContent = (metrics.f1_macro * 100).toFixed(2) + '%';
        
        // Update chart with performance over time
        updatePerformanceChart();
        
    } catch (error) {
        console.error('Metrics error:', error);
        // Don't show error to user, just use defaults
        currentModelVersion.textContent = 'N/A';
        currentAccuracy.textContent = 'N/A';
        currentF1.textContent = 'N/A';
    }
}

async function updatePerformanceChart() {
    try {
        // Try to load multiple versions for comparison
        const versions = [1, 2, 3, 4, 5]; // Try up to v5
        const metricsData = [];
        
        for (const version of versions) {
            try {
                const response = await fetch(`${API_BASE_URL}/metrics?version=${version}`);
                if (response.ok) {
                    const data = await response.json();
                    metricsData.push({
                        version: data.version,
                        accuracy: data.metrics.accuracy,
                        f1: data.metrics.f1_macro
                    });
                }
            } catch (e) {
                // Version doesn't exist, skip
                break;
            }
        }
        
        if (metricsData.length === 0) {
            return;
        }
        
        const labels = metricsData.map(d => d.version);
        const accuracies = metricsData.map(d => d.accuracy);
        const f1Scores = metricsData.map(d => d.f1);
        
        if (performanceChart) {
            performanceChart.data.labels = labels;
            performanceChart.data.datasets[0].data = accuracies;
            performanceChart.data.datasets[1].data = f1Scores;
            performanceChart.update();
        } else {
            initializeChartWithData(labels, accuracies, f1Scores);
        }
        
    } catch (error) {
        console.error('Chart update error:', error);
    }
}

function initializeChart() {
    const ctx = document.getElementById('performanceChart').getContext('2d');
    
    performanceChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [
                {
                    label: 'Accuracy',
                    data: [],
                    borderColor: 'rgb(102, 126, 234)',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    tension: 0.4,
                    fill: true
                },
                {
                    label: 'F1 Score (Macro)',
                    data: [],
                    borderColor: 'rgb(245, 158, 11)',
                    backgroundColor: 'rgba(245, 158, 11, 0.1)',
                    tension: 0.4,
                    fill: true
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                },
                title: {
                    display: true,
                    text: 'Model Performance Over Time'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 1,
                    ticks: {
                        callback: function(value) {
                            return (value * 100).toFixed(0) + '%';
                        }
                    }
                }
            }
        }
    });
    
    // Load initial data
    updatePerformanceChart();
}

function initializeChartWithData(labels, accuracies, f1Scores) {
    if (performanceChart) {
        performanceChart.data.labels = labels;
        performanceChart.data.datasets[0].data = accuracies;
        performanceChart.data.datasets[1].data = f1Scores;
        performanceChart.update();
    }
}

// UI Helpers
function showStatus(message, type = 'info') {
    statusMessage.textContent = message;
    statusMessage.className = `status-message ${type}`;
    statusMessage.classList.remove('hidden');
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        hideStatus();
    }, 5000);
}

function hideStatus() {
    statusMessage.classList.add('hidden');
}

function setLoading(loading) {
    if (loading) {
        predictBtn.disabled = true;
        predictBtn.textContent = 'Predicting...';
        document.body.classList.add('loading');
    } else {
        predictBtn.disabled = false;
        predictBtn.textContent = 'Predict';
        document.body.classList.remove('loading');
    }
}
