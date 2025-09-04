




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

import cv2
from fer import FER
import datetime
import json
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict, deque
import time

class InterviewEmotionAnalyzer:
    def __init__(self):
        self.detector = FER(mtcnn=True)
        self.emotion_log = []
        self.start_time = None
        self.current_session = {
            'session_id': datetime.datetime.now().strftime("%Y%m%d_%H%M%S"),
            'start_time': None,
            'end_time': None,
            'total_duration': 0,
            'emotion_timeline': [],
            'emotion_summary': {},
            'critical_moments': []
        }
        self.emotion_history = deque(maxlen=30)  # Last 30 detections for smoothing
        
    def start_interview(self):
        """Start interview session"""
        self.start_time = datetime.datetime.now()
        self.current_session['start_time'] = self.start_time.isoformat()
     
        
    def analyze_frame(self, frame):
        """Analyze single frame and return emotion data"""
        if self.start_time is None:
            self.start_interview()
            
        current_time = datetime.datetime.now()
        elapsed_seconds = (current_time - self.start_time).total_seconds()
        
        # Detect emotions
        emotions = self.detector.detect_emotions(frame)
        
        if emotions:
            emotion_scores = emotions[0]["emotions"]
            dominant_emotion = max(emotion_scores, key=emotion_scores.get)
            confidence = emotion_scores[dominant_emotion]
            box = emotions[0]["box"]
            
            # Add to history for smoothing
            self.emotion_history.append(dominant_emotion)
            
            # Get smoothed emotion (most common in last 10 detections)
            if len(self.emotion_history) >= 10:
                emotion_counts = {}
                recent_emotions = list(self.emotion_history)[-10:]
                for emotion in recent_emotions:
                    emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
                smoothed_emotion = max(emotion_counts.items(), key=lambda x: x[1])[0]
            else:
                smoothed_emotion = dominant_emotion
            
            # Log emotion data
            emotion_entry = {
                'timestamp': current_time.isoformat(),
                'elapsed_seconds': round(elapsed_seconds, 2),
                'dominant_emotion': smoothed_emotion,
                'confidence': round(confidence, 3),
                'all_emotions': {k: round(v, 3) for k, v in emotion_scores.items()},
                'face_box': box
            }
            
            self.emotion_log.append(emotion_entry)
            self.current_session['emotion_timeline'].append(emotion_entry)
            
            # Detect critical moments
            self.detect_critical_moments(emotion_entry, elapsed_seconds)
            
            return {
                'emotion': smoothed_emotion,
                'confidence': confidence,
                'box': box,
                'all_emotions': emotion_scores,
                'elapsed_time': elapsed_seconds
            }
            
        return None
    
    def detect_critical_moments(self, emotion_entry, elapsed_seconds):
        """Detect significant emotional moments"""
        emotion = emotion_entry['dominant_emotion']
        confidence = emotion_entry['confidence']
        
        # Define critical moments
        if emotion == 'sad' and confidence > 0.3:
            self.current_session['critical_moments'].append({
                'type': 'high_sadness',
                'timestamp': emotion_entry['timestamp'],
                'elapsed_seconds': elapsed_seconds,
                'emotion': emotion,
                'confidence': confidence,
                'description': 'Candidate showed signs of distress or sadness'
            })
        
        elif emotion == 'angry' and confidence > 0.4:
            self.current_session['critical_moments'].append({
                'type': 'anger_detected',
                'timestamp': emotion_entry['timestamp'],
                'elapsed_seconds': elapsed_seconds,
                'emotion': emotion,
                'confidence': confidence,
                'description': 'Candidate displayed anger or frustration'
            })
            
        elif emotion == 'fear' and confidence > 0.3:
            self.current_session['critical_moments'].append({
                'type': 'anxiety_detected',
                'timestamp': emotion_entry['timestamp'],
                'elapsed_seconds': elapsed_seconds,
                'emotion': emotion,
                'confidence': confidence,
                'description': 'Candidate appeared anxious or fearful'
            })
    
    def end_interview(self):
        """End interview and generate summary"""
        if self.start_time is None:
            return None
            
        end_time = datetime.datetime.now()
        total_duration = (end_time - self.start_time).total_seconds()
        
        self.current_session['end_time'] = end_time.isoformat()
        self.current_session['total_duration'] = round(total_duration, 2)
        
        # Generate emotion summary
        self.generate_emotion_summary()
        
        # Save session data
        self.save_session_data()
        
        print(f"📊 Interview completed. Duration: {total_duration:.1f}s")
        return self.current_session
    
    def generate_emotion_summary(self):
        """Generate comprehensive emotion analysis"""
        if not self.emotion_log:
            return
            
        # Calculate time spent in each emotion
        emotion_durations = defaultdict(float)
        emotion_counts = defaultdict(int)
        
        for i, entry in enumerate(self.emotion_log):
            emotion = entry['dominant_emotion']
            emotion_counts[emotion] += 1
            
            # Calculate duration (approximate)
            if i < len(self.emotion_log) - 1:
                duration = self.emotion_log[i+1]['elapsed_seconds'] - entry['elapsed_seconds']
                emotion_durations[emotion] += duration
        
        total_duration = self.current_session['total_duration']
        
        # Calculate percentages
        emotion_percentages = {}
        for emotion, duration in emotion_durations.items():
            percentage = (duration / total_duration) * 100 if total_duration > 0 else 0
            emotion_percentages[emotion] = round(percentage, 2)
        
        # Emotional stability analysis
        emotion_changes = 0
        if len(self.emotion_log) > 1:
            for i in range(1, len(self.emotion_log)):
                if self.emotion_log[i]['dominant_emotion'] != self.emotion_log[i-1]['dominant_emotion']:
                    emotion_changes += 1
        
        stability_score = max(0, 100 - (emotion_changes / len(self.emotion_log) * 100)) if self.emotion_log else 0
        
        self.current_session['emotion_summary'] = {
            'emotion_percentages': emotion_percentages,
            'emotion_durations': dict(emotion_durations),
            'emotion_counts': dict(emotion_counts),
            'total_emotion_changes': emotion_changes,
            'emotional_stability_score': round(stability_score, 2),
            'dominant_emotion_overall': max(emotion_percentages.items(), key=lambda x: x[1])[0] if emotion_percentages else 'neutral',
            'stress_indicators': {
                'high_sadness_moments': len([m for m in self.current_session['critical_moments'] if m['type'] == 'high_sadness']),
                'anger_moments': len([m for m in self.current_session['critical_moments'] if m['type'] == 'anger_detected']),
                'anxiety_moments': len([m for m in self.current_session['critical_moments'] if m['type'] == 'anxiety_detected'])
            }
        }
    
    def save_session_data(self):
        """Save session data to files"""
        session_id = self.current_session['session_id']
        
        # Save JSON summary
        with open(f'interview_{session_id}_summary.json', 'w') as f:
            json.dump(self.current_session, f, indent=2, default=str)
        
     
        
        print(f"💾 Data saved: interview_{session_id}_summary.json & interview_{session_id}_detailed.csv")
    
    def generate_dashboard_insights(self):
        """Generate insights for dashboard display"""
        if not self.current_session['emotion_summary']:
            return {}
            
        summary = self.current_session['emotion_summary']
        
        insights = {
            'overall_assessment': self.get_overall_assessment(),
            'key_metrics': {
                'emotional_stability': f"{summary['emotional_stability_score']:.1f}%",
                'dominant_emotion': summary['dominant_emotion_overall'].title(),
                'total_duration': f"{self.current_session['total_duration']:.1f}s",
                'emotion_changes': summary['total_emotion_changes']
            },
            'emotional_breakdown': summary['emotion_percentages'],
            'stress_indicators': summary['stress_indicators'],
            'critical_moments': self.current_session['critical_moments'],
            'recommendations': self.generate_recommendations()
        }
        
        return insights
    
    def get_overall_assessment(self):
        """Generate overall emotional assessment"""
        summary = self.current_session['emotion_summary']
        stability = summary['emotional_stability_score']
        stress_total = sum(summary['stress_indicators'].values())
        
        if stability >= 80 and stress_total <= 2:
            return "Excellent - Candidate remained calm and composed throughout the interview"
        elif stability >= 60 and stress_total <= 5:
            return "Good - Candidate showed generally stable emotions with minor stress moments"
        elif stability >= 40 and stress_total <= 8:
            return "Fair - Candidate experienced moderate emotional fluctuations"
        else:
            return "Needs Attention - Candidate showed significant emotional instability or stress"
    
    def generate_recommendations(self):
        """Generate actionable recommendations"""
        summary = self.current_session['emotion_summary']
        recommendations = []
        
        if summary['stress_indicators']['high_sadness_moments'] > 3:
            recommendations.append("Consider providing more encouragement and positive feedback during interviews")
        
        if summary['stress_indicators']['anxiety_moments'] > 2:
            recommendations.append("Create a more relaxed interview environment to reduce candidate anxiety")
        
        if summary['emotional_stability_score'] < 50:
            recommendations.append("Candidate may benefit from interview coaching or stress management techniques")
        
        if summary['emotion_percentages'].get('happy', 0) < 20:
            recommendations.append("Consider incorporating more engaging or positive discussion topics")
        
        return recommendations

# Enhanced main detection loop
def run_interview_analysis():
    analyzer = InterviewEmotionAnalyzer()
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open camera")
        return
    
    print("🎤 AI Interview Emotion Analysis")
    print("Press 'q' to end interview and generate report")
    print("Press 's' to start/restart interview session")
    
    interview_started = False
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        key = cv2.waitKey(1) & 0xFF
        
        # Start interview
        if key == ord('s'):
            analyzer.start_interview()
            interview_started = True
        
        # Analyze frame if interview is active
        emotion_data = None
        if interview_started:
            emotion_data = analyzer.analyze_frame(frame)
        
        # Display results
        if emotion_data:
            x, y, w, h = emotion_data['box']
            emotion = emotion_data['emotion']
            confidence = emotion_data['confidence']
            elapsed_time = emotion_data['elapsed_time']
            
            # Color coding for emotions
            color_map = {
                'happy': (0, 255, 0),      # Green
                'sad': (0, 0, 255),        # Red
                'angry': (0, 0, 139),      # Dark Red
                'fear': (128, 0, 128),     # Purple
                'surprise': (255, 255, 0), # Yellow
                'neutral': (255, 255, 255) # White
            }
            
            color = color_map.get(emotion, (255, 255, 255))
            
            # Draw bounding box and emotion
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, f"{emotion.upper()}: {confidence:.2f}", 
                       (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            
            # Display elapsed time
            cv2.putText(frame, f"Time: {elapsed_time:.1f}s", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            # Show emotional breakdown
            y_offset = 60
            for emotion_name, score in emotion_data['all_emotions'].items():
                if score > 0.1:
                    text = f"{emotion_name}: {score:.2f}"
                    cv2.putText(frame, text, (10, y_offset), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)
                    y_offset += 20
        
        # Status indicator
        status = "RECORDING" if interview_started else "READY - Press 's' to start"
        status_color = (0, 0, 255) if interview_started else (0, 255, 0)
        cv2.putText(frame, status, (10, frame.shape[0] - 20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, status_color, 2)
        
        cv2.imshow('AI Interview Analysis', frame)
        
        # End interview
        if key == ord('q'):
            if interview_started:
                session_data = analyzer.end_interview()
                
                # Generate dashboard insights
                insights = analyzer.generate_dashboard_insights()
                
                # Display summary
                print("\n" + "="*50)
                print("📊 INTERVIEW ANALYSIS COMPLETE")
                print("="*50)
                print(f"Overall Assessment: {insights['overall_assessment']}")
                print(f"Emotional Stability: {insights['key_metrics']['emotional_stability']}")
                print(f"Dominant Emotion: {insights['key_metrics']['dominant_emotion']}")
                print(f"Total Duration: {insights['key_metrics']['total_duration']}")
                
                print("\n🎭 Emotional Breakdown:")
                for emotion, percentage in insights['emotional_breakdown'].items():
                    print(f"  {emotion.title()}: {percentage}%")
                
                print(f"\n⚠️ Stress Indicators:")
                for indicator, count in insights['stress_indicators'].items():
                    if count > 0:
                        print(f"  {indicator.replace('_', ' ').title()}: {count}")
                
                if insights['critical_moments']:
                    print(f"\n🚨 Critical Moments ({len(insights['critical_moments'])}):")
                    for moment in insights['critical_moments'][:3]:  # Show first 3
                        print(f"  {moment['elapsed_seconds']:.1f}s - {moment['description']}")
                
                if insights['recommendations']:
                    print(f"\n💡 Recommendations:")
                    for rec in insights['recommendations']:
                        print(f"  • {rec}")
                
                print("="*50)
                
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_interview_analysis()






