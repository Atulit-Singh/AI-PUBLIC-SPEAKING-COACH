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
        this.currentMode = 'practice';
        this.crowdEvents = [];
        this.juryReactions = [];
        this.eventTimeouts = [];
        
        this.initializeElements();
        this.setupEventListeners();
        this.initializeCamera();
        this.setupModeSelection();
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
        this.speechDuration = document.getElementById('speechDuration');
        this.currentModeDisplay = document.getElementById('currentMode');
        this.juryPanel = document.getElementById('juryPanel');
        this.crowdSimulation = document.getElementById('crowdSimulation');
        this.videoContainer = document.getElementById('videoContainer');
        this.viewProgressBtn = document.getElementById('viewProgressBtn');
        this.progressSection = document.getElementById('progressSection');
        this.progressContent = document.getElementById('progressContent');
        this.insufficientSpeechModal = new bootstrap.Modal(document.getElementById('insufficientSpeechModal'));
        this.retryRecordingBtn = document.getElementById('retryRecordingBtn');
        
        // Audio elements
        this.audioElements = {
            crowdMurmur: document.getElementById('crowdMurmur'),
            applause: document.getElementById('applause'),
            phoneRing: document.getElementById('phoneRing'),
            cough: document.getElementById('cough'),
            doorSlam: document.getElementById('doorSlam')
        };
    }
    
    setupEventListeners() {
        this.getTopicBtn.addEventListener('click', () => this.getTopic());
        this.startBtn.addEventListener('click', () => this.startSession());
        this.stopBtn.addEventListener('click', () => this.stopSession());
        this.viewProgressBtn.addEventListener('click', () => this.loadProgress());
        this.retryRecordingBtn.addEventListener('click', () => {
            this.insufficientSpeechModal.hide();
            this.resetSession();
        });
    }
    
    setupModeSelection() {
        const modeCards = document.querySelectorAll('.mode-card');
        modeCards.forEach(card => {
            card.addEventListener('click', () => {
                // Remove active class from all cards
                modeCards.forEach(c => c.classList.remove('active'));
                // Add active class to clicked card
                card.classList.add('active');
                
                const mode = card.dataset.mode;
                this.setMode(mode);
            });
        });
        
        // Set default mode
        modeCards[0].classList.add('active');
    }
    
    async setMode(mode) {
        try {
            const response = await fetch('/api/set_mode', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ mode: mode })
            });
            
            const data = await response.json();
            if (data.status === 'success') {
                this.currentMode = mode;
                this.currentModeDisplay.textContent = data.mode.name;
                this.updateModeEnvironment(mode);
            }
        } catch (error) {
            console.error('Error setting mode:', error);
        }
    }
    
    updateModeEnvironment(mode) {
        // Reset all environments
        this.juryPanel.style.display = 'none';
        this.crowdSimulation.style.display = 'none';
        this.videoContainer.className = 'video-container';
        
        // Stop any playing audio
        Object.values(this.audioElements).forEach(audio => {
            audio.pause();
            audio.currentTime = 0;
        });
        
        // Apply mode-specific environment
        switch(mode) {
            case 'interview':
                this.videoContainer.classList.add('interview-mode');
                this.juryPanel.style.display = 'block';
                break;
            case 'public_speech':
                this.videoContainer.classList.add('public-speech-mode');
                this.crowdSimulation.style.display = 'block';
                break;
            case 'practice':
            default:
                this.videoContainer.classList.add('practice-mode');
                break;
        }
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
            
            // Store mode-specific events
            this.crowdEvents = data.crowd_events || [];
            this.juryReactions = data.jury_reactions || [];
            
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
            
            // Start mode-specific effects
            this.startModeEffects();
            
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
        
        // Update speech duration
        if (indicators.speech_duration) {
            const duration = indicators.speech_duration;
            this.speechDuration.textContent = `${duration}s`;
            this.speechDuration.className = duration >= 30 ? 'badge bg-success' : 'badge bg-warning';
        }
    }
    
    async stopSession() {
        this.isRecording = false;
        
        // Stop intervals and effects
        if (this.timerInterval) {
            clearInterval(this.timerInterval);
        }
        if (this.analysisInterval) {
            clearInterval(this.analysisInterval);
        }
        this.stopModeEffects();
        
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
                this.displayReport(data.report, data.progress_data, data.improvement_trend);
                this.updateStatus('Analysis Complete', 'ready');
            } else if (data.status === 'insufficient_speech') {
                this.handleInsufficientSpeech(data);
                return;
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
        this.metricsDisplay.style.display = 'none';
    }
    
    handleInsufficientSpeech(data) {
        this.updateStatus('Insufficient Speech', 'stopped');
        document.getElementById('insufficientSpeechMessage').textContent = data.message;
        this.insufficientSpeechModal.show();
        
        // Reset UI
        this.startBtn.disabled = false;
        this.getTopicBtn.disabled = false;
        this.metricsDisplay.style.display = 'none';
    }
    
    resetSession() {
        this.updateStatus('Ready', 'ready');
        this.speechDuration.textContent = '0s';
        this.speechDuration.className = 'badge bg-info';
    }
    
    async loadProgress() {
        try {
            const response = await fetch('/api/get_progress');
            const data = await response.json();
            
            if (data.progress_data) {
                this.displayProgress(data.progress_data, data.stats, data.improvement_trend);
            } else {
                this.progressContent.innerHTML = '<p class="text-muted">No session data available yet. Complete a few sessions to see your progress!</p>';
            }
            
            this.progressSection.style.display = 'block';
            this.progressSection.scrollIntoView({ behavior: 'smooth' });
            
        } catch (error) {
            console.error('Error loading progress:', error);
        }
    }
    
    displayProgress(progressData, stats, trend) {
        const trendClass = trend === 'improving' ? 'trend-improving' : 
                          trend === 'declining' ? 'trend-declining' : 'trend-stable';
        const trendIcon = trend === 'improving' ? 'fa-arrow-up' : 
                         trend === 'declining' ? 'fa-arrow-down' : 'fa-minus';
        const trendText = trend === 'improving' ? 'Improving' : 
                         trend === 'declining' ? 'Needs Attention' : 'Stable';
        
        this.progressContent.innerHTML = `
            <div class="row">
                <div class="col-md-6">
                    <div class="progress-chart">
                        <h5>Session Statistics</h5>
                        <div class="row text-center">
                            <div class="col-4">
                                <h3 class="text-primary">${stats.valid_sessions}</h3>
                                <small>Valid Sessions</small>
                            </div>
                            <div class="col-4">
                                <h3 class="text-warning">${stats.invalid_sessions}</h3>
                                <small>Incomplete</small>
                            </div>
                            <div class="col-4">
                                <h3 class="text-success">${stats.avg_overall_anxiety.toFixed(1)}</h3>
                                <small>Avg Anxiety</small>
                            </div>
                        </div>
                        <div class="mt-3">
                            <span class="trend-indicator ${trendClass}">
                                <i class="fas ${trendIcon} me-1"></i>${trendText}
                            </span>
                        </div>
                    </div>
                </div>
                
                <div class="col-md-6">
                    <div class="progress-chart">
                        <h5>Mode Distribution</h5>
                        ${Object.entries(stats.mode_distribution).map(([mode, count]) => `
                            <div class="d-flex justify-content-between mb-2">
                                <span>${mode.charAt(0).toUpperCase() + mode.slice(1)}:</span>
                                <span class="badge bg-primary">${count} sessions</span>
                            </div>
                        `).join('')}
                    </div>
                </div>
            </div>
            
            <div class="mt-4">
                <h5>Recent Sessions</h5>
                <div class="row">
                    ${progressData.slice(0, 5).map(session => `
                        <div class="col-md-6 mb-3">
                            <div class="session-item">
                                <div class="d-flex justify-content-between align-items-center">
                                    <div>
                                        <strong>${session.mode.charAt(0).toUpperCase() + session.mode.slice(1)} Mode</strong>
                                        <br><small class="text-muted">${new Date(session.timestamp).toLocaleDateString()}</small>
                                    </div>
                                    <div class="text-end">
                                        <div class="badge bg-${session.overall_anxiety < 30 ? 'success' : session.overall_anxiety < 60 ? 'warning' : 'danger'} mb-1">
                                            ${session.overall_anxiety.toFixed(1)} Anxiety
                                        </div>
                                        <br><small>${session.speech_duration}s speech</small>
                                    </div>
                                </div>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }
    
    displayReport(reportData, progressData, trend) {
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
        
        // Show calibration status if available
        if (data.calibration_status) {
            const status = data.calibration_status;
            if (status.is_calibrated) {
                const calibrationInfo = document.createElement('div');
                calibrationInfo.className = 'alert alert-success mt-3';
                calibrationInfo.innerHTML = `
                    <i class="fas fa-check-circle me-2"></i>
                    <strong>Model Calibrated:</strong> Analysis accuracy improved based on ${status.sample_count} sessions.
                `;
                this.reportContent.appendChild(calibrationInfo);
            } else {
                const calibrationInfo = document.createElement('div');
                calibrationInfo.className = 'alert alert-info mt-3';
                calibrationInfo.innerHTML = `
                    <i class="fas fa-info-circle me-2"></i>
                    <strong>Calibrating:</strong> Complete ${3 - status.sample_count} more sessions for personalized accuracy.
                `;
                this.reportContent.appendChild(calibrationInfo);
            }
        }
        
        // Show progress hint if user has multiple sessions
        if (progressData && progressData.length > 1) {
            setTimeout(() => {
                this.viewProgressBtn.classList.add('btn-primary');
                this.viewProgressBtn.classList.remove('btn-outline-primary');
                this.viewProgressBtn.innerHTML = '<i class="fas fa-chart-area me-1"></i>View Progress <span class="badge bg-light text-dark ms-1">New!</span>';
            }, 2000);
        }
    }
    
    startModeEffects() {
        if (this.currentMode === 'public_speech') {
            // Start crowd murmur
            this.audioElements.crowdMurmur.volume = 0.3;
            this.audioElements.crowdMurmur.play();
            
            // Schedule crowd events
            this.crowdEvents.forEach(event => {
                const timeout = setTimeout(() => {
                    this.triggerCrowdEvent(event);
                }, event.time * 1000);
                this.eventTimeouts.push(timeout);
            });
        } else if (this.currentMode === 'interview') {
            // Schedule jury reactions
            this.juryReactions.forEach(reaction => {
                const timeout = setTimeout(() => {
                    this.triggerJuryReaction(reaction);
                }, reaction.time * 1000);
                this.eventTimeouts.push(timeout);
            });
        }
    }
    
    triggerCrowdEvent(event) {
        // Show noise indicator
        const indicator = document.createElement('div');
        indicator.className = 'crowd-noise-indicator';
        indicator.textContent = event.type.replace('_', ' ').toUpperCase();
        this.videoContainer.appendChild(indicator);
        
        // Play sound effect
        const audioKey = event.type.replace('_', '');
        if (this.audioElements[audioKey]) {
            this.audioElements[audioKey].volume = event.intensity === 'high' ? 0.8 : 
                                                 event.intensity === 'medium' ? 0.5 : 0.3;
            this.audioElements[audioKey].play();
        }
        
        // Remove indicator after 2 seconds
        setTimeout(() => {
            if (indicator.parentNode) {
                indicator.parentNode.removeChild(indicator);
            }
        }, 2000);
    }
    
    triggerJuryReaction(reaction) {
        const juror = document.getElementById(`juror${reaction.juror}`);
        if (juror) {
            juror.classList.add('reacting');
            juror.textContent = reaction.reaction.replace('_', ' ');
            
            setTimeout(() => {
                juror.classList.remove('reacting');
                juror.textContent = `Judge ${reaction.juror}`;
            }, 3000);
        }
    }
    
    stopModeEffects() {
        // Clear all timeouts
        this.eventTimeouts.forEach(timeout => clearTimeout(timeout));
        this.eventTimeouts = [];
        
        // Stop all audio
        Object.values(this.audioElements).forEach(audio => {
            audio.pause();
            audio.currentTime = 0;
        });
        
        // Remove any crowd indicators
        const indicators = document.querySelectorAll('.crowd-noise-indicator');
        indicators.forEach(indicator => {
            if (indicator.parentNode) {
                indicator.parentNode.removeChild(indicator);
            }
        });
        
        // Reset jury reactions
        for (let i = 1; i <= 3; i++) {
            const juror = document.getElementById(`juror${i}`);
            if (juror) {
                juror.classList.remove('reacting');
                juror.textContent = `Judge ${i}`;
            }
        }
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