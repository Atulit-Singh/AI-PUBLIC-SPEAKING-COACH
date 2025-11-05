class PublicSpeakingCoach {
    constructor() {
        this.video = document.getElementById('videoElement');
        this.canvas = document.createElement('canvas');
        this.ctx = this.canvas.getContext('2d');
        this.isRecording = false;
        this.sessionStartTime = null;
        this.timerInterval = null;
        this.analysisInterval = null;
        this.mediaRecorder = null;
        this.audioChunks = [];
        
        this.initializeElements();
        this.setupEventListeners();
        this.initializeCamera();
    }
    
    initializeElements() {
        this.getTopicBtn = document.getElementById('getTopicBtn');
        this.startBtn = document.getElementById('startBtn');
        this.stopBtn = document.getElementById('stopBtn');
        this.timer = document.getElementById('timer');
        this.statusText = document.getElementById('statusText');
        this.statusIndicator = document.querySelector('.status-indicator');
        this.topicCard = document.getElementById('topicCard');
        this.topicText = document.getElementById('topicText');
        this.instructionsList = document.getElementById('instructionsList');
        this.reportSection = document.getElementById('reportSection');
        this.reportContent = document.getElementById('reportContent');
        this.metricsDisplay = document.getElementById('metricsDisplay');
        this.faceDetection = document.getElementById('faceDetection');
        this.liveBlinkRate = document.getElementById('liveBlinkRate');
        this.liveMovement = document.getElementById('liveMovement');
    }
    
    setupEventListeners() {
        this.getTopicBtn.addEventListener('click', () => this.getTopic());
        this.startBtn.addEventListener('click', () => this.startSession());
        this.stopBtn.addEventListener('click', () => this.stopSession());
    }
    
    async initializeCamera() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({
                video: { width: 640, height: 480 },
                audio: true
            });
            
            this.video.srcObject = stream;
            this.stream = stream;
            this.updateStatus('Ready', 'ready');
            
        } catch (error) {
            console.error('Error accessing camera:', error);
            this.updateStatus('Camera Error', 'stopped');
            alert('Unable to access camera. Please check permissions.');
        }
    }
    
    async getTopic() {
        try {
            const response = await fetch('/api/get_topic');
            const data = await response.json();
            
            this.topicText.textContent = data.topic;
            this.instructionsList.innerHTML = '';
            
            data.instructions.instructions.forEach(instruction => {
                const li = document.createElement('li');
                li.textContent = instruction;
                this.instructionsList.appendChild(li);
            });
            
            this.topicCard.style.display = 'block';
            this.startBtn.disabled = false;
            
        } catch (error) {
            console.error('Error getting topic:', error);
            alert('Error getting topic. Please try again.');
        }
    }
    
    async startSession() {
        try {
            // Start backend session
            await fetch('/api/start_session', { method: 'POST' });
            
            this.isRecording = true;
            this.sessionStartTime = Date.now();
            
            // Setup audio recording
            this.setupAudioRecording();
            
            // Start timer
            this.startTimer();
            
            // Start frame analysis
            this.startFrameAnalysis();
            
            // Update UI
            this.updateStatus('Recording', 'recording');
            this.startBtn.disabled = true;
            this.stopBtn.disabled = false;
            this.getTopicBtn.disabled = true;
            this.metricsDisplay.style.display = 'block';
            
        } catch (error) {
            console.error('Error starting session:', error);
            alert('Error starting session. Please try again.');
        }
    }
    
    setupAudioRecording() {
        if (this.stream) {
            this.mediaRecorder = new MediaRecorder(this.stream);
            this.audioChunks = [];
            
            this.mediaRecorder.ondataavailable = (event) => {
                this.audioChunks.push(event.data);
            };
            
            this.mediaRecorder.start();
        }
    }
    
    startTimer() {
        this.timerInterval = setInterval(() => {
            const elapsed = Math.floor((Date.now() - this.sessionStartTime) / 1000);
            const minutes = Math.floor(elapsed / 60);
            const seconds = elapsed % 60;
            this.timer.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
            
            // Auto-stop after 2 minutes
            if (elapsed >= 120) {
                this.stopSession();
            }
        }, 1000);
    }
    
    startFrameAnalysis() {
        this.analysisInterval = setInterval(() => {
            this.analyzeFrame();
        }, 1000); // Analyze every second
    }
    
    analyzeFrame() {
        if (!this.isRecording) return;
        
        // Capture frame from video
        this.canvas.width = this.video.videoWidth;
        this.canvas.height = this.video.videoHeight;
        this.ctx.drawImage(this.video, 0, 0);
        
        // Convert to base64
        const imageData = this.canvas.toDataURL('image/jpeg', 0.8);
        
        // Send to backend for analysis
        fetch('/api/analyze_frame', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ image: imageData })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                this.updateLiveMetrics(data.indicators);
            }
        })
        .catch(error => {
            console.error('Error analyzing frame:', error);
        });
    }
    
    updateLiveMetrics(indicators) {
        if (indicators.face_detected) {
            this.faceDetection.textContent = 'Detected';
            this.faceDetection.className = 'badge bg-success';
            
            this.liveBlinkRate.textContent = `${indicators.blink_rate.toFixed(1)} /min`;
            
            const movementLevel = indicators.movement_level < 0.01 ? 'Low' : 
                                 indicators.movement_level < 0.03 ? 'Medium' : 'High';
            this.liveMovement.textContent = movementLevel;
            
        } else {
            this.faceDetection.textContent = 'Not Detected';
            this.faceDetection.className = 'badge bg-warning';
        }
    }
    
    async stopSession() {
        this.isRecording = false;
        
        // Stop intervals
        if (this.timerInterval) {
            clearInterval(this.timerInterval);
        }
        if (this.analysisInterval) {
            clearInterval(this.analysisInterval);
        }
        
        // Stop audio recording
        if (this.mediaRecorder && this.mediaRecorder.state === 'recording') {
            this.mediaRecorder.stop();
        }
        
        // Update UI
        this.updateStatus('Processing...', 'stopped');
        this.stopBtn.disabled = true;
        this.metricsDisplay.style.display = 'none';
        
        try {
            // Send stop signal to backend
            const response = await fetch('/api/stop_session', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    audio: this.audioChunks.length > 0 ? 'audio_data_placeholder' : null
                })
            });
            
            const data = await response.json();
            
            if (data.status === 'success') {
                this.displayReport(data.report);
                this.updateStatus('Analysis Complete', 'ready');
            } else {
                throw new Error(data.error || 'Unknown error');
            }
            
        } catch (error) {
            console.error('Error stopping session:', error);
            alert('Error processing session. Please try again.');
            this.updateStatus('Error', 'stopped');
        }
        
        // Reset UI
        this.startBtn.disabled = false;
        this.getTopicBtn.disabled = false;
    }
    
    displayReport(reportData) {
        const overallScore = reportData.overall_anxiety_score;
        const visualScore = reportData.visual_analysis.anxiety_score;
        const voiceScore = reportData.voice_analysis.anxiety_score;
        
        // Determine anxiety level
        const getAnxietyLevel = (score) => {
            if (score < 30) return { level: 'Low', class: 'success', icon: 'smile' };
            if (score < 60) return { level: 'Moderate', class: 'warning', icon: 'meh' };
            return { level: 'High', class: 'danger', icon: 'frown' };
        };
        
        const overallLevel = getAnxietyLevel(overallScore);
        const visualLevel = getAnxietyLevel(visualScore);
        const voiceLevel = getAnxietyLevel(voiceScore);
        
        this.reportContent.innerHTML = `
            <div class="row">
                <div class="col-md-4">
                    <div class="card border-${overallLevel.class} mb-3">
                        <div class="card-header bg-${overallLevel.class} text-white">
                            <h5><i class="fas fa-${overallLevel.icon} me-2"></i>Overall Anxiety</h5>
                        </div>
                        <div class="card-body text-center">
                            <h2 class="text-${overallLevel.class}">${overallScore.toFixed(1)}</h2>
                            <p class="mb-0">${overallLevel.level} Level</p>
                        </div>
                    </div>
                </div>
                
                <div class="col-md-4">
                    <div class="card border-${visualLevel.class} mb-3">
                        <div class="card-header bg-${visualLevel.class} text-white">
                            <h5><i class="fas fa-eye me-2"></i>Visual Analysis</h5>
                        </div>
                        <div class="card-body text-center">
                            <h2 class="text-${visualLevel.class}">${visualScore.toFixed(1)}</h2>
                            <p class="mb-0">${visualLevel.level} Level</p>
                        </div>
                    </div>
                </div>
                
                <div class="col-md-4">
                    <div class="card border-${voiceLevel.class} mb-3">
                        <div class="card-header bg-${voiceLevel.class} text-white">
                            <h5><i class="fas fa-microphone me-2"></i>Voice Analysis</h5>
                        </div>
                        <div class="card-body text-center">
                            <h2 class="text-${voiceLevel.class}">${voiceScore.toFixed(1)}</h2>
                            <p class="mb-0">${voiceLevel.level} Level</p>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="row mt-4">
                <div class="col-md-6">
                    <h5><i class="fas fa-chart-bar me-2"></i>Detailed Metrics</h5>
                    <ul class="list-group">
                        <li class="list-group-item d-flex justify-content-between">
                            <span>Average Blink Rate:</span>
                            <span>${reportData.visual_analysis.blink_rate.toFixed(1)} /min</span>
                        </li>
                        <li class="list-group-item d-flex justify-content-between">
                            <span>Movement Level:</span>
                            <span>${(reportData.visual_analysis.movement_level * 100).toFixed(1)}%</span>
                        </li>
                        <li class="list-group-item d-flex justify-content-between">
                            <span>Face Detection Rate:</span>
                            <span>${reportData.visual_analysis.face_detection_rate.toFixed(1)}%</span>
                        </li>
                        <li class="list-group-item d-flex justify-content-between">
                            <span>Voice Pauses:</span>
                            <span>${reportData.voice_analysis.total_pauses}</span>
                        </li>
                    </ul>
                </div>
                
                <div class="col-md-6">
                    <h5><i class="fas fa-lightbulb me-2"></i>Recommendations</h5>
                    <div class="accordion" id="recommendationsAccordion">
                        <div class="accordion-item">
                            <h2 class="accordion-header">
                                <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#immediateTips">
                                    Immediate Tips
                                </button>
                            </h2>
                            <div id="immediateTips" class="accordion-collapse collapse show">
                                <div class="accordion-body">
                                    <ul>
                                        ${reportData.recommendations.immediate_tips.map(tip => `<li>${tip}</li>`).join('')}
                                    </ul>
                                </div>
                            </div>
                        </div>
                        
                        <div class="accordion-item">
                            <h2 class="accordion-header">
                                <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#practiceExercises">
                                    Practice Exercises
                                </button>
                            </h2>
                            <div id="practiceExercises" class="accordion-collapse collapse">
                                <div class="accordion-body">
                                    <ul>
                                        ${reportData.recommendations.practice_exercises.map(exercise => `<li>${exercise}</li>`).join('')}
                                    </ul>
                                </div>
                            </div>
                        </div>
                        
                        <div class="accordion-item">
                            <h2 class="accordion-header">
                                <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#longTermStrategies">
                                    Long-term Strategies
                                </button>
                            </h2>
                            <div id="longTermStrategies" class="accordion-collapse collapse">
                                <div class="accordion-body">
                                    <ul>
                                        ${reportData.recommendations.long_term_strategies.map(strategy => `<li>${strategy}</li>`).join('')}
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        this.reportSection.style.display = 'block';
        this.reportSection.scrollIntoView({ behavior: 'smooth' });
    }
    
    updateStatus(text, type) {
        this.statusText.textContent = text;
        this.statusIndicator.className = `status-indicator status-${type}`;
    }
}

// Initialize the application when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new PublicSpeakingCoach();
});