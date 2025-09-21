import asyncio
import websockets
import cv2
import base64
import numpy as np
import json
from fer import FER
import datetime
import pandas as pd
from collections import defaultdict, deque

class WebSocketInterviewAnalyzer:
    """
    Complete WebSocket version of your IntegratedInterviewEmotionAnalyzer
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
        
        # Gaze tracking variables
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        self.gaze_low_confidence_start = None
        self.sustained_gaze_low_confidence_count = 0
        
        # WebSocket specific
        self.clients = set()
        self.interview_active = False

    def _create_new_session(self):
        """Initializes a fresh session dictionary."""
        return {
            'session_id': datetime.datetime.now().strftime("%Y%m%d_%H%M%S"),
            'start_time': None,
            'end_time': None,
            'total_duration': 0,
            'emotion_timeline': [],
            'emotion_summary': {},
            'gaze_analysis': {},
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
        
        # Reset gaze tracking
        self.gaze_low_confidence_start = None
        self.sustained_gaze_low_confidence_count = 0
        
        self.current_session = self._create_new_session()
        self.current_session['start_time'] = self.start_time.isoformat()
        self.interview_active = True
        print(f"🎥 WebSocket Interview Analysis Started: {self.current_session['session_id']}")

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

        # Gaze-based confidence
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

        # Gaze-based critical moments
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

    def generate_comprehensive_summary(self):
        """Enhanced summary generation including gaze analysis."""
        if not self.emotion_log:
            return

        df = pd.DataFrame(self.emotion_log)
        
        # Original emotion analysis
        emotion_percentages = (df['dominant_emotion'].value_counts(normalize=True) * 100).round(2).to_dict()
        emotion_changes = (df['dominant_emotion'].shift() != df['dominant_emotion']).sum()
        stability_score = max(0, 100 - (emotion_changes / len(df) * 100)) if len(df) > 0 else 100
        
        # Gaze analysis
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
        
        # Gaze analysis summary
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

    def end_interview(self):
        """Finalizes the interview session and generates comprehensive summary."""
        if self.start_time is None:
            return {"error": "No interview session was started."}
            
        self.interview_active = False
        end_time = datetime.datetime.now()
        self.current_session['end_time'] = end_time.isoformat()
        self.current_session['total_duration'] = round((end_time - self.start_time).total_seconds(), 2)
        
        self.generate_comprehensive_summary()
        
        # Save report
        report = self.get_final_report()
        session_id = self.current_session['session_id']
        report_filename = f"websocket_interview_report_{session_id}.json"
        
        try:
            with open(report_filename, 'w') as f:
                json.dump(report, f, indent=4)
            print(f"📊 Interview Analysis Complete! Report saved: {report_filename}")
        except Exception as e:
            print(f"Could not save report: {e}")
        
        return report

    # WebSocket-specific methods
    def process_frame_from_frontend(self, frame_base64):
        """Process frame received from React frontend"""
        try:
            # Decode base64 frame
            img_data = base64.b64decode(frame_base64)
            np_array = np.frombuffer(img_data, np.uint8)
            frame = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
            
            if not self.interview_active:
                # Just return the original frame if interview not started
                return self._frame_to_base64(frame), None
            
            # Your existing emotion analysis
            emotion_data = self.analyze_frame(frame)
            
            # Draw analysis overlay on frame (optional)
            annotated_frame = self._draw_analysis_overlay(frame, emotion_data)
            
            # Convert back to base64
            processed_frame_base64 = self._frame_to_base64(annotated_frame)
            
            return processed_frame_base64, emotion_data
            
        except Exception as e:
            print(f"Error processing frame: {e}")
            return None, None

    def _draw_analysis_overlay(self, frame, emotion_data):
        """Optional: Draw analysis overlay on frame"""
        if emotion_data:
            # Draw face box
            face_box = emotion_data['face_box']
            x, y, w, h = face_box
            
            # Draw rectangle around face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
            
            # Add emotion and gaze info
            emotion = emotion_data['dominant_emotion']
            gaze = emotion_data['gaze_direction']
            confidence = emotion_data['confidence']
            
            # Draw text background
            cv2.rectangle(frame, (x, y - 80), (x + 300, y), (0, 0, 0), -1)
            
            # Draw text
            cv2.putText(frame, f"Emotion: {emotion.upper()}", (x, y - 60), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            cv2.putText(frame, f"Gaze: {gaze.upper()}", (x, y - 40), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            cv2.putText(frame, f"Conf: {confidence:.2f}", (x, y - 20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        
        return frame

    def _frame_to_base64(self, frame):
        """Convert frame to base64"""
        _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
        return base64.b64encode(buffer).decode('utf-8')

# WebSocket handler
analyzer = WebSocketInterviewAnalyzer()

async def handle_client(websocket, path):
    """Handle WebSocket connections from React frontend"""
    print("Client connected")
    analyzer.clients.add(websocket)
    
    try:
        async for message in websocket:
            data = json.loads(message)
            
            if data['type'] == 'start_interview':
                analyzer.start_interview()
                await websocket.send(json.dumps({
                    'type': 'interview_started',
                    'message': 'Interview analysis started'
                }))
                
            elif data['type'] == 'process_frame':
                processed_frame, emotion_data = analyzer.process_frame_from_frontend(data['frame'])
                
                if processed_frame:
                    response = {
                        'type': 'processed_frame',
                        'frame': processed_frame,
                        'emotion_data': emotion_data,
                        'interview_active': analyzer.interview_active
                    }
                    await websocket.send(json.dumps(response))
            
            elif data['type'] == 'end_interview':
                report = analyzer.end_interview()
                await websocket.send(json.dumps({
                    'type': 'interview_ended',
                    'report': report
                }))
                
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")
    except Exception as e:
        print(f"Error in WebSocket handler: {e}")
    finally:
        if websocket in analyzer.clients:
            analyzer.clients.remove(websocket)

# Replace the last few lines of your script with:
if __name__ == "__main__":
    print("🚀 Starting WebSocket Interview Analysis Server")
    print("📡 Server will run on: ws://localhost:8765")
    print("🎯 Ready for React frontend connection...")
    
    async def main():
        async with websockets.serve(handle_client, "localhost", 8765):
            print("✅ Server is running!")
            await asyncio.Future()  # Run forever
    
    asyncio.run(main())
