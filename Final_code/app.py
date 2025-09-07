




## Audio-To-Text
from faster_whisper import WhisperModel
from pydub import AudioSegment, silence
import re

def transcribe_with_all_pauses_integrated(audio_file, pause_threshold=2.0):
    """
    Properly integrate ALL detected silences into the transcript
    """
    # Get transcription from CrisperWhisper
    model = WhisperModel('nyrahealth/faster_CrisperWhisper', device="cpu", compute_type="float32")
    segments, info = model.transcribe(
        audio_file, 
        beam_size=1, 
        language='en', 
        word_timestamps=True,
        vad_filter=False
    )
    
    segments_list = list(segments)
 
    
    # Load audio and detect actual silences
    audio = AudioSegment.from_wav(audio_file)
    silences = silence.detect_silence(
        audio,
        min_silence_len=int(pause_threshold * 1000),
        silence_thresh=-40
    )
    
   
    for i, (start_ms, end_ms) in enumerate(silences):
        duration = (end_ms - start_ms) / 1000
   
    
    # Create timeline events (segments + silences)
    events = []
    
    # Add segment events
    for segment in segments_list:
        events.append({
            'type': 'segment',
            'time': segment.start,
            'end_time': segment.end,
            'text': clean_transcript_text(segment.text)
        })
    
    # Add silence events
    for start_ms, end_ms in silences:
        start_s = start_ms / 1000
        duration = (end_ms - start_ms) / 1000
        events.append({
            'type': 'silence',
            'time': start_s,
            'duration': duration
        })
    
    # Sort all events by time
    events.sort(key=lambda x: x['time'])
    
    # Build transcript chronologically
    transcript = ""
    
    for event in events:
        if event['type'] == 'segment':
            transcript += event['text'] + " "
           
        elif event['type'] == 'silence':
            transcript += f"[PAUSE:{event['duration']:.1f}s] "
          
    
    return transcript.strip()

def clean_transcript_text(text):
    """Clean transcript text"""
    text = re.sub(r',([a-z])', r' \1', text)
    text = re.sub(r',\s*', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    if text:
        text = text[0].upper() + text[1:]
    return text

# Usage
result = transcribe_with_all_pauses_integrated("WhatsApp Audio 2025-09-02 at 7.12.44 PM.wav", pause_threshold=2.0)
print("\nTranscript with ALL Pauses Integrated:")
print("="*60)
print(result)
print("="*60)





## Text-Detect


import joblib
import whisper
import speech_recognition as sr
import warnings
import re
warnings.filterwarnings('ignore')
# ==================== STEP 9: INFERENCE PIPELINE ====================
print("\n🚀 STEP 9: Creating Inference Pipeline")
print("=" * 60)

class FluentInterviewAnalyzer:
    """
    Complete pipeline for analyzing interview fluency from audio or transcript
    """
    
    def __init__(self, model_path):
        """
        Load the trained model and initialize the analyzer
        """
        self.model_package = joblib.load(model_path)
        self.model = self.model_package['model']
        self.scaler = self.model_package['scaler']
        self.feature_names = self.model_package['feature_names']
        self.filler_patterns = r'\b(um|uh|er|ah|you know|like|actually|basically)\b'
        self.pause_pattern = r'\[PAUSE:(\d+\.?\d*)s\]'
        
        print(f"✅ Fluency analyzer loaded successfully!")
        print(f"   Model: {self.model_package['model_name']}")
        print(f"   Test R² Score: {self.model_package['performance_metrics']['test_r2']:.4f}")
    
    def analyze_transcript(self, enhanced_transcript):
        """
        Analyze fluency from an enhanced transcript with pause markers
        
        Args:
            enhanced_transcript (str): Transcript with [PAUSE:Xs] markers
            
        Returns:
            dict: Analysis results including fluency score and breakdown
        """
        # Extract basic features
        filler_matches = re.findall(self.filler_patterns, enhanced_transcript, re.IGNORECASE)
        pause_matches = re.findall(self.pause_pattern, enhanced_transcript)
        
        filler_count = len(filler_matches)
        pause_count = len(pause_matches)
        total_pause_time = sum(float(p) for p in pause_matches)
        
        # Clean transcript for word count
        clean_text = re.sub(self.pause_pattern, '', enhanced_transcript)
        clean_text = re.sub(self.filler_patterns, '', clean_text, re.IGNORECASE)
        word_count = len(clean_text.split())
        
        # Calculate derived features
        filler_density = filler_count / max(word_count, 1)
        pause_density = pause_count / max(word_count, 1)
        avg_pause_duration = total_pause_time / max(pause_count, 1)
        has_long_pauses = int(total_pause_time > 3.0)
        has_multiple_pauses = int(pause_count > 1)
        
        # Estimate speech rate (approximate)
        estimated_speech_time = word_count / 2.0 + total_pause_time  # Rough estimate
        speech_rate = (word_count / estimated_speech_time) * 60 if estimated_speech_time > 0 else 120
        
        filler_type_count = len(set(filler_matches))
        hesitation_score = filler_density * 0.4 + pause_density * 0.3 + has_long_pauses * 0.3
        speech_efficiency = word_count / (word_count + filler_count + pause_count)
        
        # Create feature vector
        features = {
            'filler_count': filler_count,
            'pause_count': pause_count,
            'total_pause_time': total_pause_time,
            'word_count': word_count,
            'speech_rate': speech_rate,
            'filler_density': filler_density,
            'pause_density': pause_density,
            'avg_pause_duration': avg_pause_duration,
            'has_long_pauses': has_long_pauses,
            'has_multiple_pauses': has_multiple_pauses,
            'filler_type_count': filler_type_count,
            'hesitation_score': hesitation_score,
            'speech_efficiency': speech_efficiency
        }
        
        # Prepare for prediction
        feature_vector = [features.get(name, 0) for name in self.feature_names]
        feature_vector_scaled = self.scaler.transform([feature_vector])
        
        # Predict fluency
        fluency_score = self.model.predict(feature_vector_scaled)[0]
        fluency_score = max(0.0, min(1.0, fluency_score))  # Ensure valid range
        
        # Generate interpretation
        if fluency_score >= 0.8:
            fluency_level = "Excellent"
            interpretation = "Very fluent response with minimal hesitations"
        elif fluency_score >= 0.7:
            fluency_level = "Good"
            interpretation = "Generally fluent with some minor hesitations"
        elif fluency_score >= 0.6:
            fluency_level = "Fair"
            interpretation = "Moderate fluency with noticeable hesitations"
        else:
            fluency_level = "Poor"
            interpretation = "Low fluency with significant hesitations"
        
        return {
            'fluency_score': round(fluency_score, 3),
            'fluency_level': fluency_level,
            'interpretation': interpretation,
            'details': {
                'filler_count': filler_count,
                'filler_words': list(set(filler_matches)),
                'pause_count': pause_count,
                'total_pause_time': round(total_pause_time, 1),
                'word_count': word_count,
                'speech_rate': round(speech_rate, 1)
            }
            
        }
    
   

# Create analyzer instance
analyzer = FluentInterviewAnalyzer("fluency_predictor_linear_regression.pkl")
transcript="Hello mynameismuthubani and[UH] asyouknow I'mtryingtobuildaproject.Youknow I'mfacingverymuchdifficultiesrightnow because [UH] inmymind there'salotofthingshappeningrightnow but Ithink so Icanovercomethat because Godisnmyside Iknow I'mjustmakingthisaudio to [UH]tryandtestmy. [PAUSE:3.3s] [PAUSE:2.9s] [UH] I'm. Don't."



result = analyzer.analyze_transcript(transcript)











### Face Detection

# import cv2
# from fer import FER
# import datetime
# import json
# import pandas as pd
# import matplotlib.pyplot as plt
# from collections import defaultdict, deque
# import time

# class InterviewEmotionAnalyzer:
#     def __init__(self):
#         self.detector = FER(mtcnn=True)
#         self.emotion_log = []
#         self.start_time = None
#         self.current_session = {
#             'session_id': datetime.datetime.now().strftime("%Y%m%d_%H%M%S"),
#             'start_time': None,
#             'end_time': None,
#             'total_duration': 0,
#             'emotion_timeline': [],
#             'emotion_summary': {},
#             'critical_moments': []
#         }
#         self.emotion_history = deque(maxlen=30)  # Last 30 detections for smoothing
        
#     def start_interview(self):
#         """Start interview session"""
#         self.start_time = datetime.datetime.now()
#         self.current_session['start_time'] = self.start_time.isoformat()
     
        
#     def analyze_frame(self, frame):
#         """Analyze single frame and return emotion data"""
#         if self.start_time is None:
#             self.start_interview()
            
#         current_time = datetime.datetime.now()
#         elapsed_seconds = (current_time - self.start_time).total_seconds()
        
#         # Detect emotions
#         emotions = self.detector.detect_emotions(frame)
        
#         if emotions:
#             emotion_scores = emotions[0]["emotions"]
#             dominant_emotion = max(emotion_scores, key=emotion_scores.get)
#             confidence = emotion_scores[dominant_emotion]
#             box = emotions[0]["box"]
            
#             # Add to history for smoothing
#             self.emotion_history.append(dominant_emotion)
            
#             # Get smoothed emotion (most common in last 10 detections)
#             if len(self.emotion_history) >= 10:
#                 emotion_counts = {}
#                 recent_emotions = list(self.emotion_history)[-10:]
#                 for emotion in recent_emotions:
#                     emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
#                 smoothed_emotion = max(emotion_counts.items(), key=lambda x: x[1])[0]
#             else:
#                 smoothed_emotion = dominant_emotion
            
#             # Log emotion data
#             emotion_entry = {
#                 'timestamp': current_time.isoformat(),
#                 'elapsed_seconds': round(elapsed_seconds, 2),
#                 'dominant_emotion': smoothed_emotion,
#                 'confidence': round(confidence, 3),
#                 'all_emotions': {k: round(v, 3) for k, v in emotion_scores.items()},
#                 'face_box': box
#             }
            
#             self.emotion_log.append(emotion_entry)
#             self.current_session['emotion_timeline'].append(emotion_entry)
            
#             # Detect critical moments
#             self.detect_critical_moments(emotion_entry, elapsed_seconds)
            
#             return {
#                 'emotion': smoothed_emotion,
#                 'confidence': confidence,
#                 'box': box,
#                 'all_emotions': emotion_scores,
#                 'elapsed_time': elapsed_seconds
#             }
            
#         return None
    
#     def detect_critical_moments(self, emotion_entry, elapsed_seconds):
#         """Detect significant emotional moments"""
#         emotion = emotion_entry['dominant_emotion']
#         confidence = emotion_entry['confidence']
        
#         # Define critical moments
#         if emotion == 'sad' and confidence > 0.3:
#             self.current_session['critical_moments'].append({
#                 'type': 'high_sadness',
#                 'timestamp': emotion_entry['timestamp'],
#                 'elapsed_seconds': elapsed_seconds,
#                 'emotion': emotion,
#                 'confidence': confidence,
#                 'description': 'Candidate showed signs of distress or sadness'
#             })
        
#         elif emotion == 'angry' and confidence > 0.4:
#             self.current_session['critical_moments'].append({
#                 'type': 'anger_detected',
#                 'timestamp': emotion_entry['timestamp'],
#                 'elapsed_seconds': elapsed_seconds,
#                 'emotion': emotion,
#                 'confidence': confidence,
#                 'description': 'Candidate displayed anger or frustration'
#             })
            
#         elif emotion == 'fear' and confidence > 0.3:
#             self.current_session['critical_moments'].append({
#                 'type': 'anxiety_detected',
#                 'timestamp': emotion_entry['timestamp'],
#                 'elapsed_seconds': elapsed_seconds,
#                 'emotion': emotion,
#                 'confidence': confidence,
#                 'description': 'Candidate appeared anxious or fearful'
#             })
    
#     def end_interview(self):
#         """End interview and generate summary"""
#         if self.start_time is None:
#             return None
            
#         end_time = datetime.datetime.now()
#         total_duration = (end_time - self.start_time).total_seconds()
        
#         self.current_session['end_time'] = end_time.isoformat()
#         self.current_session['total_duration'] = round(total_duration, 2)
        
#         # Generate emotion summary
#         self.generate_emotion_summary()
        
#         # Save session data
#         self.save_session_data()
        
#         print(f"📊 Interview completed. Duration: {total_duration:.1f}s")
#         return self.current_session
    
#     def generate_emotion_summary(self):
#         """Generate comprehensive emotion analysis"""
#         if not self.emotion_log:
#             return
            
#         # Calculate time spent in each emotion
#         emotion_durations = defaultdict(float)
#         emotion_counts = defaultdict(int)
        
#         for i, entry in enumerate(self.emotion_log):
#             emotion = entry['dominant_emotion']
#             emotion_counts[emotion] += 1
            
#             # Calculate duration (approximate)
#             if i < len(self.emotion_log) - 1:
#                 duration = self.emotion_log[i+1]['elapsed_seconds'] - entry['elapsed_seconds']
#                 emotion_durations[emotion] += duration
        
#         total_duration = self.current_session['total_duration']
        
#         # Calculate percentages
#         emotion_percentages = {}
#         for emotion, duration in emotion_durations.items():
#             percentage = (duration / total_duration) * 100 if total_duration > 0 else 0
#             emotion_percentages[emotion] = round(percentage, 2)
        
#         # Emotional stability analysis
#         emotion_changes = 0
#         if len(self.emotion_log) > 1:
#             for i in range(1, len(self.emotion_log)):
#                 if self.emotion_log[i]['dominant_emotion'] != self.emotion_log[i-1]['dominant_emotion']:
#                     emotion_changes += 1
        
#         stability_score = max(0, 100 - (emotion_changes / len(self.emotion_log) * 100)) if self.emotion_log else 0
        
#         self.current_session['emotion_summary'] = {
#             'emotion_percentages': emotion_percentages,
#             'emotion_durations': dict(emotion_durations),
#             'emotion_counts': dict(emotion_counts),
#             'total_emotion_changes': emotion_changes,
#             'emotional_stability_score': round(stability_score, 2),
#             'dominant_emotion_overall': max(emotion_percentages.items(), key=lambda x: x[1])[0] if emotion_percentages else 'neutral',
#             'stress_indicators': {
#                 'high_sadness_moments': len([m for m in self.current_session['critical_moments'] if m['type'] == 'high_sadness']),
#                 'anger_moments': len([m for m in self.current_session['critical_moments'] if m['type'] == 'anger_detected']),
#                 'anxiety_moments': len([m for m in self.current_session['critical_moments'] if m['type'] == 'anxiety_detected'])
#             }
#         }
    
#     def save_session_data(self):
#         """Save session data to files"""
#         session_id = self.current_session['session_id']
        
#         # Save JSON summary
#         with open(f'interview_{session_id}_summary.json', 'w') as f:
#             json.dump(self.current_session, f, indent=2, default=str)
        
     
        
#         print(f"💾 Data saved: interview_{session_id}_summary.json & interview_{session_id}_detailed.csv")
    
#     def generate_dashboard_insights(self):
#         """Generate insights for dashboard display"""
#         if not self.current_session['emotion_summary']:
#             return {}
            
#         summary = self.current_session['emotion_summary']
        
#         insights = {
#             'overall_assessment': self.get_overall_assessment(),
#             'key_metrics': {
#                 'emotional_stability': f"{summary['emotional_stability_score']:.1f}%",
#                 'dominant_emotion': summary['dominant_emotion_overall'].title(),
#                 'total_duration': f"{self.current_session['total_duration']:.1f}s",
#                 'emotion_changes': summary['total_emotion_changes']
#             },
#             'emotional_breakdown': summary['emotion_percentages'],
#             'stress_indicators': summary['stress_indicators'],
#             'critical_moments': self.current_session['critical_moments'],
#             'recommendations': self.generate_recommendations()
#         }
        
#         return insights
    
#     def get_overall_assessment(self):
#         """Generate overall emotional assessment"""
#         summary = self.current_session['emotion_summary']
#         stability = summary['emotional_stability_score']
#         stress_total = sum(summary['stress_indicators'].values())
        
#         if stability >= 80 and stress_total <= 2:
#             return "Excellent - Candidate remained calm and composed throughout the interview"
#         elif stability >= 60 and stress_total <= 5:
#             return "Good - Candidate showed generally stable emotions with minor stress moments"
#         elif stability >= 40 and stress_total <= 8:
#             return "Fair - Candidate experienced moderate emotional fluctuations"
#         else:
#             return "Needs Attention - Candidate showed significant emotional instability or stress"
    
#     def generate_recommendations(self):
#         """Generate actionable recommendations"""
#         summary = self.current_session['emotion_summary']
#         recommendations = []
        
#         if summary['stress_indicators']['high_sadness_moments'] > 3:
#             recommendations.append("Consider providing more encouragement and positive feedback during interviews")
        
#         if summary['stress_indicators']['anxiety_moments'] > 2:
#             recommendations.append("Create a more relaxed interview environment to reduce candidate anxiety")
        
#         if summary['emotional_stability_score'] < 50:
#             recommendations.append("Candidate may benefit from interview coaching or stress management techniques")
        
#         if summary['emotion_percentages'].get('happy', 0) < 20:
#             recommendations.append("Consider incorporating more engaging or positive discussion topics")
        
#         return recommendations

# # Enhanced main detection loop
# def run_interview_analysis():
#     analyzer = InterviewEmotionAnalyzer()
#     cap = cv2.VideoCapture(0)
    
#     if not cap.isOpened():
#         print("Error: Could not open camera")
#         return
    
#     print("🎤 AI Interview Emotion Analysis")
#     print("Press 'q' to end interview and generate report")
#     print("Press 's' to start/restart interview session")
    
#     interview_started = False
    
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break
        
#         key = cv2.waitKey(1) & 0xFF
        
#         # Start interview
#         if key == ord('s'):
#             analyzer.start_interview()
#             interview_started = True
        
#         # Analyze frame if interview is active
#         emotion_data = None
#         if interview_started:
#             emotion_data = analyzer.analyze_frame(frame)
        
#         # Display results
#         if emotion_data:
#             x, y, w, h = emotion_data['box']
#             emotion = emotion_data['emotion']
#             confidence = emotion_data['confidence']
#             elapsed_time = emotion_data['elapsed_time']
            
#             # Color coding for emotions
#             color_map = {
#                 'happy': (0, 255, 0),      # Green
#                 'sad': (0, 0, 255),        # Red
#                 'angry': (0, 0, 139),      # Dark Red
#                 'fear': (128, 0, 128),     # Purple
#                 'surprise': (255, 255, 0), # Yellow
#                 'neutral': (255, 255, 255) # White
#             }
            
#             color = color_map.get(emotion, (255, 255, 255))
            
#             # Draw bounding box and emotion
#             cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
#             cv2.putText(frame, f"{emotion.upper()}: {confidence:.2f}", 
#                        (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            
#             # Display elapsed time
#             cv2.putText(frame, f"Time: {elapsed_time:.1f}s", 
#                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
#             # Show emotional breakdown
#             y_offset = 60
#             for emotion_name, score in emotion_data['all_emotions'].items():
#                 if score > 0.1:
#                     text = f"{emotion_name}: {score:.2f}"
#                     cv2.putText(frame, text, (10, y_offset), 
#                                cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)
#                     y_offset += 20
        
#         # Status indicator
#         status = "RECORDING" if interview_started else "READY - Press 's' to start"
#         status_color = (0, 0, 255) if interview_started else (0, 255, 0)
#         cv2.putText(frame, status, (10, frame.shape[0] - 20), 
#                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, status_color, 2)
        
#         cv2.imshow('AI Interview Analysis', frame)
        
#         # End interview
#         if key == ord('q'):
#             if interview_started:
#                 session_data = analyzer.end_interview()
                
#                 # Generate dashboard insights
#                 insights = analyzer.generate_dashboard_insights()
                
#                 # Display summary
#                 print("\n" + "="*50)
#                 print("📊 INTERVIEW ANALYSIS COMPLETE")
#                 print("="*50)
#                 print(f"Overall Assessment: {insights['overall_assessment']}")
#                 print(f"Emotional Stability: {insights['key_metrics']['emotional_stability']}")
#                 print(f"Dominant Emotion: {insights['key_metrics']['dominant_emotion']}")
#                 print(f"Total Duration: {insights['key_metrics']['total_duration']}")
                
#                 print("\n🎭 Emotional Breakdown:")
#                 for emotion, percentage in insights['emotional_breakdown'].items():
#                     print(f"  {emotion.title()}: {percentage}%")
                
#                 print(f"\n⚠️ Stress Indicators:")
#                 for indicator, count in insights['stress_indicators'].items():
#                     if count > 0:
#                         print(f"  {indicator.replace('_', ' ').title()}: {count}")
                
#                 if insights['critical_moments']:
#                     print(f"\n🚨 Critical Moments ({len(insights['critical_moments'])}):")
#                     for moment in insights['critical_moments'][:3]:  # Show first 3
#                         print(f"  {moment['elapsed_seconds']:.1f}s - {moment['description']}")
                
#                 if insights['recommendations']:
#                     print(f"\n💡 Recommendations:")
#                     for rec in insights['recommendations']:
#                         print(f"  • {rec}")
                
#                 print("="*50)
                
#             break
    
#     cap.release()
#     cv2.destroyAllWindows()

# if __name__ == "__main__":
#     run_interview_analysis()




# import cv2
# from fer import FER
# import datetime
# import json
# import pandas as pd
# from collections import defaultdict, deque


# class InterviewEmotionAnalyzer:
#     """
#     Analyzes facial emotions in real-time during an interview, providing insights
#     into the candidate's emotional state, stability, and critical moments.
#     """
#     def __init__(self):
#         self.detector = FER(mtcnn=True)
#         self.emotion_log = []
#         self.start_time = None
#         self.current_session = self._create_new_session()
        
#         # Use deques for efficient, fixed-size history tracking
#         self.emotion_history = deque(maxlen=15)  # Smoothed over last 15 frames
#         self.neutral_streak = 0
#         self.low_confidence_streak = 0

#     def _create_new_session(self):
#         """Initializes a fresh session dictionary."""
#         return {
#             'session_id': datetime.datetime.now().strftime("%Y%m%d_%H%M%S"),
#             'start_time': None,
#             'end_time': None,
#             'total_duration': 0,
#             'emotion_timeline': [],
#             'emotion_summary': {},
#             'critical_moments': []
#         }

#     def start_interview(self):
#         """Starts or restarts the interview analysis session."""
#         self.start_time = datetime.datetime.now()
#         # Reset all tracking variables for a clean start
#         self.emotion_log = []
#         self.emotion_history.clear()
#         self.neutral_streak = 0
#         self.low_confidence_streak = 0
#         self.current_session = self._create_new_session()
#         self.current_session['start_time'] = self.start_time.isoformat()
#         print(f"🎥 Interview session started: {self.current_session['session_id']}")

#     def analyze_frame(self, frame):
#         """
#         Analyzes a single video frame for emotions, logs the data, and detects
#         critical moments. Returns processed data for display.
#         """
#         if self.start_time is None:
#             return None

#         current_time = datetime.datetime.now()
#         elapsed_seconds = (current_time - self.start_time).total_seconds()
        
#         emotions = self.detector.detect_emotions(frame)
        
#         if not emotions:
#             return None

#         primary_face = emotions[0]
#         emotion_scores = primary_face["emotions"]
#         dominant_emotion = max(emotion_scores, key=emotion_scores.get)
#         confidence = emotion_scores[dominant_emotion]
        
#         self.emotion_history.append(dominant_emotion)
#         smoothed_emotion = max(set(self.emotion_history), key=list(self.emotion_history).count)

#         emotion_entry = {
#             'timestamp': current_time.isoformat(),
#             'elapsed_seconds': round(elapsed_seconds, 2),
#             'dominant_emotion': smoothed_emotion,
#             'confidence': round(confidence, 3),
#             'all_emotions': {k: round(v, 3) for k, v in emotion_scores.items()},
#             'face_box': primary_face["box"]
#         }
        
#         self.emotion_log.append(emotion_entry)
#         self.detect_critical_moments(emotion_entry)
#         return emotion_entry

#     def detect_critical_moments(self, emotion_entry):
#         """
#         Identifies and flags moments of significant emotional shifts, stress,
#         or disengagement based on refined heuristics.
#         """
#         emotion = emotion_entry['dominant_emotion']
#         confidence = emotion_entry['confidence']
#         all_emotions = emotion_entry['all_emotions']

#         if (emotion == 'sad' and confidence > 0.35) or (emotion == 'fear' and confidence > 0.4):
#             self._log_critical_moment('high_stress', emotion_entry, f"Candidate showed strong signs of {emotion}.")

#         if emotion == 'neutral':
#             self.neutral_streak += 1
#             if self.neutral_streak == 30:
#                 self._log_critical_moment('prolonged_neutrality', emotion_entry, "Candidate showed a prolonged neutral expression.")
#         else:
#             self.neutral_streak = 0

#         is_ambiguous = (all_emotions.get('neutral', 0) > 0.2 and (all_emotions.get('sad', 0) + all_emotions.get('fear', 0)) > 0.25)
#         if confidence < 0.45 and is_ambiguous:
#             self.low_confidence_streak += 1
#             if self.low_confidence_streak == 15:
#                 self._log_critical_moment('low_confidence', emotion_entry, "Candidate appeared uncertain.")
#         else:
#             self.low_confidence_streak = 0

#     def _log_critical_moment(self, type, entry, description):
#         """Helper to append a critical moment to the session log, avoiding rapid duplicates."""
#         if self.current_session['critical_moments']:
#             last_moment = self.current_session['critical_moments'][-1]
#             if last_moment['type'] == type and (entry['elapsed_seconds'] - last_moment['elapsed_seconds']) < 5:
#                 return
#         self.current_session['critical_moments'].append({
#             'type': type, 'timestamp': entry['timestamp'], 'elapsed_seconds': entry['elapsed_seconds'],
#             'emotion': entry['dominant_emotion'], 'confidence': entry['confidence'], 'description': description
#         })
        
#     def end_interview(self):
#         """Finalizes the interview session and generates the summary."""
#         if self.start_time is None:
#             print("No interview session was started.")
#             return
            
#         end_time = datetime.datetime.now()
#         self.current_session['end_time'] = end_time.isoformat()
#         self.current_session['total_duration'] = round((end_time - self.start_time).total_seconds(), 2)
        
#         self.generate_emotion_summary()
        
#         print(f"\n📊 Interview completed. Duration: {self.current_session['total_duration']:.1f}s")

#     def generate_emotion_summary(self):
#         """Calculates and stores aggregate emotion statistics for the session."""
#         if not self.emotion_log:
#             return

#         df = pd.DataFrame(self.emotion_log)
#         emotion_percentages = (df['dominant_emotion'].value_counts(normalize=True) * 100).round(2).to_dict()
#         emotion_changes = (df['dominant_emotion'].shift() != df['dominant_emotion']).sum()
#         stability_score = max(0, 100 - (emotion_changes / len(df) * 100)) if len(df) > 0 else 100
        
#         critical_moment_counts = defaultdict(int)
#         for moment in self.current_session['critical_moments']:
#             critical_moment_counts[moment['type']] += 1

#         self.current_session['emotion_summary'] = {
#             'emotion_percentages': emotion_percentages,
#             'emotional_stability_score': round(stability_score, 2),
#             'dominant_emotion_overall': max(emotion_percentages, key=emotion_percentages.get, default='neutral'),
#             'critical_moment_counts': dict(critical_moment_counts)
#         }

#     def get_final_report(self):
#         """Generates a structured, human-readable report from the session data."""
#         if not self.current_session.get('emotion_summary'):
#             return {"error": "No summary available."}
        
#         summary = self.current_session['emotion_summary']
#         stability = summary['emotional_stability_score']
#         stress_total = sum(summary.get('critical_moment_counts', {}).values())

#         if stability >= 75 and stress_total <= 2: assessment = "Excellent"
#         elif stability >= 55 and stress_total <= 5: assessment = "Good"
#         elif stability >= 35 or summary.get('critical_moment_counts', {}).get('low_confidence', 0) > 0: assessment = "Fair"
#         else: assessment = "Needs Attention"
            
#         return {
#             'assessment': assessment,
#             'stability_score': f"{summary['emotional_stability_score']:.1f}%",
#             'dominant_emotion': summary['dominant_emotion_overall'].title(),
#             'emotion_breakdown_percentage': summary['emotion_percentages'],
#             'critical_moments_summary': dict(summary.get('critical_moment_counts', {}))
#         }


# def run_interview_analysis():
#     """Main loop to capture video, run analysis, and display results."""
#     analyzer = InterviewEmotionAnalyzer()
#     cap = cv2.VideoCapture(0)
#     if not cap.isOpened():
#         print("Error: Could not open camera.")
#         return

#     print("\n🎤 AI Interview Emotion Analysis")
#     print("Press 's' to START interview.")
#     print("Press 'q' to END interview and save the report.")
    
#     interview_started = False
    
#     while True:
#         ret, frame = cap.read()
#         if not ret: break

#         key = cv2.waitKey(1) & 0xFF
        
#         if key == ord('s'):
#             analyzer.start_interview()
#             interview_started = True
        
#         elif key == ord('q'):
#             if interview_started:
#                 analyzer.end_interview()
#                 report = analyzer.get_final_report()
                
#                 # Create and save the single, concise JSON report
#                 if 'error' not in report:
#                     session_id = analyzer.current_session['session_id']
#                     report_filename = f"final_report_summary_{session_id}.json"
#                     with open(report_filename, 'w') as f:
#                         json.dump(report, f, indent=4)
#                     print(f"📄 Report saved to: {report_filename}")

#                 # Display final report in console
#                 print("\n" + "="*60)
#                 print("📊 FINAL INTERVIEW REPORT")
#                 print("="*60)
#                 for key, value in report.items():
#                     if isinstance(value, dict):
#                         print(f"{key.replace('_', ' ').title()}:")
#                         for sub_key, sub_value in value.items():
#                             print(f"  - {sub_key.title()}: {sub_value}")
#                     else:
#                         print(f"{key.replace('_', ' ').title()}: {value}")
#                 print("="*60)
#             break
        
#         if interview_started:
#             emotion_data = analyzer.analyze_frame(frame)
#             if emotion_data:
#                 x, y, w, h = emotion_data['face_box']
#                 emotion = emotion_data['dominant_emotion']
#                 confidence = emotion_data['confidence']
                
#                 color_map = {'happy': (0, 255, 0), 'sad': (255, 100, 0), 'angry': (0, 0, 255),
#                              'fear': (128, 0, 128), 'surprise': (0, 255, 255), 'neutral': (220, 220, 220)}
#                 color = color_map.get(emotion, (255, 255, 255))
                
#                 cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
#                 cv2.putText(frame, f"{emotion.upper()} ({confidence:.2f})", 
#                             (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

#         status_text = "RECORDING" if interview_started else "READY: Press 's' to start"
#         status_color = (0, 0, 255) if interview_started else (0, 255, 0)
#         cv2.putText(frame, status_text, (10, frame.shape[0] - 15), 
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.6, status_color, 2)
        
#         cv2.imshow('AI Interview Analysis', frame)

#     cap.release()
#     cv2.destroyAllWindows()

# if __name__ == "__main__":
#     run_interview_analysis()


import cv2
from fer import FER
import datetime
import json
import pandas as pd
from collections import defaultdict, deque
import numpy as np

class IntegratedInterviewEmotionAnalyzer:
    """
    Comprehensive emotion analyzer that combines:
    - Original emotion tracking with critical moments
    - Simple gaze-based confidence (center=high, left/right=low)
    - Sadness detection with appropriate thresholds
    """
    def __init__(self):
        self.detector = FER(mtcnn=True)
        self.emotion_log = []
        self.start_time = None
        self.current_session = self._create_new_session()
        
        # Original tracking variables
        self.emotion_history = deque(maxlen=15)
        self.neutral_streak = 0
        self.low_confidence_streak = 0
        
        # NEW: Gaze tracking variables
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        self.gaze_low_confidence_start = None
        self.sustained_gaze_low_confidence_count = 0

    def _create_new_session(self):
        """Initializes a fresh session dictionary."""
        return {
            'session_id': datetime.datetime.now().strftime("%Y%m%d_%H%M%S"),
            'start_time': None,
            'end_time': None,
            'total_duration': 0,
            'emotion_timeline': [],
            'emotion_summary': {},
            'gaze_analysis': {},  # NEW: Gaze analysis
            'critical_moments': []
        }

    def start_interview(self):
        """Starts or restarts the interview analysis session."""
        self.start_time = datetime.datetime.now()
        # Reset all tracking variables for a clean start
        self.emotion_log = []
        self.emotion_history.clear()
        self.neutral_streak = 0
        self.low_confidence_streak = 0
        
        # NEW: Reset gaze tracking
        self.gaze_low_confidence_start = None
        self.sustained_gaze_low_confidence_count = 0
        
        self.current_session = self._create_new_session()
        self.current_session['start_time'] = self.start_time.isoformat()
        print(f"🎥 Enhanced Interview Analysis Started: {self.current_session['session_id']}")

    def detect_gaze_direction(self, frame, face_box):
        """
        Simple gaze detection: center, left, right
        Returns: 'center', 'left', 'right'
        """
        x, y, w, h = face_box
        face_roi = frame[y:y+h, x:x+w]
        face_gray = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)
        
        eyes = self.eye_cascade.detectMultiScale(face_gray, 1.1, 5)
        
        if len(eyes) < 2:
            return 'center'  # Default to center
        
        face_center_x = w // 2
        eyes_sorted = sorted(eyes, key=lambda e: e[2] * e[3], reverse=True)[:2]
        
        eye_centers_x = []
        for (ex, ey, ew, eh) in eyes_sorted:
            eye_center_x = ex + ew // 2
            eye_centers_x.append(eye_center_x)
        
        if len(eye_centers_x) == 2:
            avg_eye_x = sum(eye_centers_x) // 2
            horizontal_deviation = avg_eye_x - face_center_x
            threshold = w * 0.15  # 15% of face width
            
            if abs(horizontal_deviation) <= threshold:
                return 'center'
            elif horizontal_deviation < -threshold:
                return 'left'
            else:
                return 'right'
        
        return 'center'

    def calculate_gaze_confidence(self, gaze_direction):
        """
        Simple gaze-based confidence:
        - Center = HIGH confidence  
        - Left/Right = LOW confidence
        """
        if gaze_direction == 'center':
            return 'high'
        elif gaze_direction in ['left', 'right']:
            return 'low'
        else:
            return 'high'  # Default

    def analyze_frame(self, frame):
        """
        Enhanced frame analysis combining original emotion tracking with gaze analysis.
        """
        if self.start_time is None:
            return None

        current_time = datetime.datetime.now()
        elapsed_seconds = (current_time - self.start_time).total_seconds()
        
        emotions = self.detector.detect_emotions(frame)
        
        if not emotions:
            return None

        primary_face = emotions[0]
        emotion_scores = primary_face["emotions"]
        face_box = primary_face["box"]
        
        # Original emotion processing
        dominant_emotion = max(emotion_scores, key=emotion_scores.get)
        confidence = emotion_scores[dominant_emotion]
        
        self.emotion_history.append(dominant_emotion)
        smoothed_emotion = max(set(self.emotion_history), key=list(self.emotion_history).count)

        # NEW: Gaze-based confidence
        gaze_direction = self.detect_gaze_direction(frame, face_box)
        gaze_confidence_level = self.calculate_gaze_confidence(gaze_direction)
        
        # Track sustained gaze-based low confidence
        is_sustained_gaze_low_confidence = False
        if gaze_confidence_level == 'low':
            if self.gaze_low_confidence_start is None:
                self.gaze_low_confidence_start = current_time
            elif (current_time - self.gaze_low_confidence_start).total_seconds() > 1.0:
                is_sustained_gaze_low_confidence = True
                self.sustained_gaze_low_confidence_count += 1
        else:
            self.gaze_low_confidence_start = None

        emotion_entry = {
            'timestamp': current_time.isoformat(),
            'elapsed_seconds': round(elapsed_seconds, 2),
            'dominant_emotion': smoothed_emotion,
            'confidence': round(confidence, 3),
            'all_emotions': {k: round(v, 3) for k, v in emotion_scores.items()},
            'face_box': face_box,
            # NEW: Gaze data
            'gaze_direction': gaze_direction,
            'gaze_confidence_level': gaze_confidence_level,
            'sustained_gaze_low_confidence': is_sustained_gaze_low_confidence
        }
        
        self.emotion_log.append(emotion_entry)
        self.detect_critical_moments(emotion_entry)
        return emotion_entry

    def detect_critical_moments(self, emotion_entry):
        """
        Enhanced critical moment detection including gaze-based issues.
        """
        emotion = emotion_entry['dominant_emotion']
        confidence = emotion_entry['confidence']
        all_emotions = emotion_entry['all_emotions']
        gaze_direction = emotion_entry['gaze_direction']

        # Original emotion-based detection
        if (emotion == 'sad' and confidence > 0.40) or (emotion == 'fear' and confidence > 0.4):
            self._log_critical_moment('high_stress', emotion_entry, f"Candidate showed strong signs of {emotion}.")

        if emotion == 'neutral':
            self.neutral_streak += 1
            if self.neutral_streak == 30:
                self._log_critical_moment('prolonged_neutrality', emotion_entry, "Candidate showed a prolonged neutral expression.")
        else:
            self.neutral_streak = 0

        # Original low confidence detection
        is_ambiguous = (all_emotions.get('neutral', 0) > 0.2 and (all_emotions.get('sad', 0) + all_emotions.get('fear', 0)) > 0.25)
        if confidence < 0.45 and is_ambiguous:
            self.low_confidence_streak += 1
            if self.low_confidence_streak == 15:
                self._log_critical_moment('low_confidence', emotion_entry, "Candidate appeared uncertain.")
        else:
            self.low_confidence_streak = 0

        # NEW: Gaze-based critical moments
        if gaze_direction in ['left', 'right'] and emotion_entry['sustained_gaze_low_confidence']:
            self._log_critical_moment('gaze_avoidance', emotion_entry, f"Candidate avoided eye contact by looking {gaze_direction}.")

    def _log_critical_moment(self, type, entry, description):
        """Helper to append a critical moment to the session log, avoiding rapid duplicates."""
        if self.current_session['critical_moments']:
            last_moment = self.current_session['critical_moments'][-1]
            if last_moment['type'] == type and (entry['elapsed_seconds'] - last_moment['elapsed_seconds']) < 5:
                return
        self.current_session['critical_moments'].append({
            'type': type, 'timestamp': entry['timestamp'], 'elapsed_seconds': entry['elapsed_seconds'],
            'emotion': entry['dominant_emotion'], 'confidence': entry['confidence'], 
            'gaze_direction': entry.get('gaze_direction', 'unknown'),
            'description': description
        })
        
    def end_interview(self):
        """Finalizes the interview session and generates comprehensive summary."""
        if self.start_time is None:
            print("No interview session was started.")
            return
            
        end_time = datetime.datetime.now()
        self.current_session['end_time'] = end_time.isoformat()
        self.current_session['total_duration'] = round((end_time - self.start_time).total_seconds(), 2)
        
        self.generate_comprehensive_summary()
        
        print(f"\n📊 Enhanced Interview Analysis Complete!")
        print(f"Duration: {self.current_session['total_duration']:.1f}s")

    def generate_comprehensive_summary(self):
        """Enhanced summary generation including gaze analysis."""
        if not self.emotion_log:
            return

        df = pd.DataFrame(self.emotion_log)
        
        # Original emotion analysis
        emotion_percentages = (df['dominant_emotion'].value_counts(normalize=True) * 100).round(2).to_dict()
        emotion_changes = (df['dominant_emotion'].shift() != df['dominant_emotion']).sum()
        stability_score = max(0, 100 - (emotion_changes / len(df) * 100)) if len(df) > 0 else 100
        
        # NEW: Gaze analysis
        gaze_percentages = (df['gaze_direction'].value_counts(normalize=True) * 100).round(2).to_dict()
        gaze_confidence_percentages = (df['gaze_confidence_level'].value_counts(normalize=True) * 100).round(2).to_dict()
        engagement_score = gaze_percentages.get('center', 0)
        
        # Calculate gaze-based low confidence duration
        gaze_low_confidence_frames = df['sustained_gaze_low_confidence'].sum()
        fps_estimate = 30
        gaze_low_confidence_duration = round(gaze_low_confidence_frames / fps_estimate, 2)
        
        critical_moment_counts = defaultdict(int)
        for moment in self.current_session['critical_moments']:
            critical_moment_counts[moment['type']] += 1

        # Original emotion summary
        self.current_session['emotion_summary'] = {
            'emotion_percentages': emotion_percentages,
            'emotional_stability_score': round(stability_score, 2),
            'dominant_emotion_overall': max(emotion_percentages, key=emotion_percentages.get, default='neutral'),
            'critical_moment_counts': dict(critical_moment_counts)
        }
        
        # NEW: Gaze analysis summary
        self.current_session['gaze_analysis'] = {
            'gaze_percentages': gaze_percentages,
            'gaze_confidence_percentages': gaze_confidence_percentages,
            'engagement_score': round(engagement_score, 1),
            'looking_at_camera_percentage': gaze_percentages.get('center', 0),
            'gaze_low_confidence_duration_seconds': gaze_low_confidence_duration
        }

    def get_final_report(self):
        """Enhanced final report including gaze analysis."""
        if not self.current_session.get('emotion_summary'):
            return {"error": "No summary available."}
        
        summary = self.current_session['emotion_summary']
        gaze_summary = self.current_session.get('gaze_analysis', {})
        
        stability = summary['emotional_stability_score']
        stress_total = sum(summary.get('critical_moment_counts', {}).values())
        engagement = gaze_summary.get('engagement_score', 0)

        # Enhanced assessment including gaze
        if stability >= 75 and stress_total <= 2 and engagement >= 70:
            assessment = "Excellent"
        elif stability >= 55 and stress_total <= 5 and engagement >= 50:
            assessment = "Good"
        elif stability >= 35 and engagement >= 30:
            assessment = "Fair"
        else:
            assessment = "Needs Attention"
            
        return {
            'assessment': assessment,
            'stability_score': f"{summary['emotional_stability_score']:.1f}%",
            'dominant_emotion': summary['dominant_emotion_overall'].title(),
            'emotion_breakdown_percentage': summary['emotion_percentages'],
            'engagement_score': f"{gaze_summary.get('engagement_score', 0):.1f}%",
            'looking_at_camera_percentage': f"{gaze_summary.get('looking_at_camera_percentage', 0):.1f}%",
            'gaze_distribution': gaze_summary.get('gaze_percentages', {}),
            'gaze_confidence_breakdown': gaze_summary.get('gaze_confidence_percentages', {}),
            'gaze_low_confidence_duration': f"{gaze_summary.get('gaze_low_confidence_duration_seconds', 0):.1f}s",
            'critical_moments_summary': dict(summary.get('critical_moment_counts', {}))
        }

def run_integrated_interview_analysis():
    """Main loop combining comprehensive emotion analysis with simple gaze confidence."""
    analyzer = IntegratedInterviewEmotionAnalyzer()
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    print("\n🎤 CLEAN AI Interview Analysis")
    print("Features:")
    print("✅ Comprehensive emotion tracking (including sadness >0.40 threshold)")
    print("✅ Simple gaze-based confidence (center=HIGH, left/right=LOW)")
    print("✅ Critical moment detection")
    print("✅ Engagement scoring")
    print("\nControls:")
    print("Press 's' to START interview")
    print("Press 'q' to END interview and generate comprehensive report")
    
    interview_started = False
    
    while True:
        ret, frame = cap.read()
        if not ret: 
            break

        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('s'):
            analyzer.start_interview()
            interview_started = True
        
        elif key == ord('q'):
            if interview_started:
                analyzer.end_interview()
                report = analyzer.get_final_report()
                
                # Save comprehensive report
                if 'error' not in report:
                    session_id = analyzer.current_session['session_id']
                    report_filename = f"clean_interview_report_{session_id}.json"
                    with open(report_filename, 'w') as f:
                        json.dump(report, f, indent=4)
                    print(f"📄 Comprehensive report saved: {report_filename}")

                # Display enhanced report
                print("\n" + "="*70)
                print("📊 CLEAN INTERVIEW ANALYSIS REPORT")
                print("="*70)
                print(f"Overall Assessment: {report.get('assessment', 'N/A')}")
                print(f"Emotional Stability: {report.get('stability_score', 'N/A')}")
                print(f"Dominant Emotion: {report.get('dominant_emotion', 'N/A')}")
                print(f"Engagement Score: {report.get('engagement_score', 'N/A')}")
                print(f"Looking at Camera: {report.get('looking_at_camera_percentage', 'N/A')}")
                print(f"Gaze Low Confidence Duration: {report.get('gaze_low_confidence_duration', 'N/A')}")
                
                print(f"\n📈 Detailed Breakdowns:")
                print(f"Emotions: {report.get('emotion_breakdown_percentage', {})}")
                print(f"Gaze Distribution: {report.get('gaze_distribution', {})}")
                print(f"Gaze Confidence: {report.get('gaze_confidence_breakdown', {})}")
                print(f"Critical Moments: {report.get('critical_moments_summary', {})}")
                print("="*70)
            break
        
        if interview_started:
            emotion_data = analyzer.analyze_frame(frame)
            # REMOVED: All visual overlays (green box, text, status)
            # The analysis still runs in the background but shows clean video feed
        
        # REMOVED: Status display text ("RECORDING" etc.)
        cv2.imshow('Clean AI Interview Analysis', frame)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_integrated_interview_analysis()




