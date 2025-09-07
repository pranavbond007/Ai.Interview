
# import joblib
# import whisper
# import speech_recognition as sr
# import warnings
# import re
# warnings.filterwarnings('ignore')
# # ==================== STEP 9: INFERENCE PIPELINE ====================
# print("\n🚀 STEP 9: Creating Inference Pipeline")
# print("=" * 60)

# class FluentInterviewAnalyzer:
#     """
#     Complete pipeline for analyzing interview fluency from audio or transcript
#     """
    
#     def __init__(self, model_path):
#         """
#         Load the trained model and initialize the analyzer
#         """
#         self.model_package = joblib.load(model_path)
#         self.model = self.model_package['model']
#         self.scaler = self.model_package['scaler']
#         self.feature_names = self.model_package['feature_names']
#         self.filler_patterns = r'\b(um|uh|er|ah|you know|like|actually|basically)\b'
#         self.pause_pattern = r'\[PAUSE:(\d+\.?\d*)s\]'
        
#         print(f"✅ Fluency analyzer loaded successfully!")
#         print(f"   Model: {self.model_package['model_name']}")
#         print(f"   Test R² Score: {self.model_package['performance_metrics']['test_r2']:.4f}")
    
#     def analyze_transcript(self, enhanced_transcript):
#         """
#         Analyze fluency from an enhanced transcript with pause markers
        
#         Args:
#             enhanced_transcript (str): Transcript with [PAUSE:Xs] markers
            
#         Returns:
#             dict: Analysis results including fluency score and breakdown
#         """
#         # Extract basic features
#         filler_matches = re.findall(self.filler_patterns, enhanced_transcript, re.IGNORECASE)
#         pause_matches = re.findall(self.pause_pattern, enhanced_transcript)
        
#         filler_count = len(filler_matches)
#         pause_count = len(pause_matches)
#         total_pause_time = sum(float(p) for p in pause_matches)
        
#         # Clean transcript for word count
#         clean_text = re.sub(self.pause_pattern, '', enhanced_transcript)
#         clean_text = re.sub(self.filler_patterns, '', clean_text, re.IGNORECASE)
#         word_count = len(clean_text.split())
        
#         # Calculate derived features
#         filler_density = filler_count / max(word_count, 1)
#         pause_density = pause_count / max(word_count, 1)
#         avg_pause_duration = total_pause_time / max(pause_count, 1)
#         has_long_pauses = int(total_pause_time > 3.0)
#         has_multiple_pauses = int(pause_count > 1)
        
#         # Estimate speech rate (approximate)
#         estimated_speech_time = word_count / 2.0 + total_pause_time  # Rough estimate
#         speech_rate = (word_count / estimated_speech_time) * 60 if estimated_speech_time > 0 else 120
        
#         filler_type_count = len(set(filler_matches))
#         hesitation_score = filler_density * 0.4 + pause_density * 0.3 + has_long_pauses * 0.3
#         speech_efficiency = word_count / (word_count + filler_count + pause_count)
        
#         # Create feature vector
#         features = {
#             'filler_count': filler_count,
#             'pause_count': pause_count,
#             'total_pause_time': total_pause_time,
#             'word_count': word_count,
#             'speech_rate': speech_rate,
#             'filler_density': filler_density,
#             'pause_density': pause_density,
#             'avg_pause_duration': avg_pause_duration,
#             'has_long_pauses': has_long_pauses,
#             'has_multiple_pauses': has_multiple_pauses,
#             'filler_type_count': filler_type_count,
#             'hesitation_score': hesitation_score,
#             'speech_efficiency': speech_efficiency
#         }
        
#         # Prepare for prediction
#         feature_vector = [features.get(name, 0) for name in self.feature_names]
#         feature_vector_scaled = self.scaler.transform([feature_vector])
        
#         # Predict fluency
#         fluency_score = self.model.predict(feature_vector_scaled)[0]
#         fluency_score = max(0.0, min(1.0, fluency_score))  # Ensure valid range
        
#         # Generate interpretation
#         if fluency_score >= 0.8:
#             fluency_level = "Excellent"
#             interpretation = "Very fluent response with minimal hesitations"
#         elif fluency_score >= 0.7:
#             fluency_level = "Good"
#             interpretation = "Generally fluent with some minor hesitations"
#         elif fluency_score >= 0.6:
#             fluency_level = "Fair"
#             interpretation = "Moderate fluency with noticeable hesitations"
#         else:
#             fluency_level = "Poor"
#             interpretation = "Low fluency with significant hesitations"
        
#         return {
#             'fluency_score': round(fluency_score, 3),
#             'fluency_level': fluency_level,
#             'interpretation': interpretation,
#             'details': {
#                 'filler_count': filler_count,
#                 'filler_words': list(set(filler_matches)),
#                 'pause_count': pause_count,
#                 'total_pause_time': round(total_pause_time, 1),
#                 'word_count': word_count,
#                 'speech_rate': round(speech_rate, 1)
#             }
            
#         }
    
   

# # Create analyzer instance
# analyzer = FluentInterviewAnalyzer("fluency_predictor_linear_regression.pkl")







# from faster_whisper import WhisperModel
# from pydub import AudioSegment, silence
# import re

# def transcribe_with_all_pauses_integrated(audio_file, pause_threshold=2.0):
#     """
#     Properly integrate ALL detected silences into the transcript
#     """
#     # Get transcription from CrisperWhisper
#     model = WhisperModel('nyrahealth/faster_CrisperWhisper', device="cpu", compute_type="float32")
#     segments, info = model.transcribe(
#         audio_file, 
#         beam_size=1, 
#         language='en', 
#         word_timestamps=True,
#         vad_filter=False
#     )
    
#     segments_list = list(segments)
#     print(f"ASR Segments: {len(segments_list)}")
    
#     # Load audio and detect actual silences
#     audio = AudioSegment.from_wav(audio_file)
#     silences = silence.detect_silence(
#         audio,
#         min_silence_len=int(pause_threshold * 1000),
#         silence_thresh=-40
#     )
    
#     print(f"Audio-based silences found: {len(silences)}")
#     for i, (start_ms, end_ms) in enumerate(silences):
#         duration = (end_ms - start_ms) / 1000
#         print(f"  Silence {i+1}: {start_ms/1000:.2f}s - {end_ms/1000:.2f}s ({duration:.1f}s)")
    
#     # Create timeline events (segments + silences)
#     events = []
    
#     # Add segment events
#     for segment in segments_list:
#         events.append({
#             'type': 'segment',
#             'time': segment.start,
#             'end_time': segment.end,
#             'text': clean_transcript_text(segment.text)
#         })
    
#     # Add silence events
#     for start_ms, end_ms in silences:
#         start_s = start_ms / 1000
#         duration = (end_ms - start_ms) / 1000
#         events.append({
#             'type': 'silence',
#             'time': start_s,
#             'duration': duration
#         })
    
#     # Sort all events by time
#     events.sort(key=lambda x: x['time'])
    
#     # Build transcript chronologically
#     transcript = ""
    
#     for event in events:
#         if event['type'] == 'segment':
#             transcript += event['text'] + " "
#             print(f"Added text: '{event['text']}'")
#         elif event['type'] == 'silence':
#             transcript += f"[PAUSE:{event['duration']:.1f}s] "
#             print(f"Added pause: {event['duration']:.1f}s at {event['time']:.2f}s")
    
#     return  analyzer.analyze_transcript(transcript)

# def clean_transcript_text(text):
#     """Clean transcript text"""
#     text = re.sub(r',([a-z])', r' \1', text)
#     text = re.sub(r',\s*', ' ', text)
#     text = re.sub(r'\s+', ' ', text)
#     text = text.strip()
#     if text:
#         text = text[0].upper() + text[1:]
#     return text









# import subprocess
# import os

# def convert_webm_to_wav_subprocess(input_file, output_file="output.wav"):
#     """Convert WebM to WAV using subprocess"""
    
#     if not os.path.exists(input_file):
#         raise FileNotFoundError(f"Input file not found: {input_file}")
    
#     try:
#         subprocess.run([
#             "ffmpeg", "-i", input_file,
#             "-acodec", "pcm_s16le",
#             "-ar", "16000", 
#             "-ac", "1",
#             "-y",  # overwrite output
#             output_file
#         ], check=True, capture_output=True)
        
#         print(f"Successfully converted {input_file} to {output_file}")
#         return output_file
        
#     except subprocess.CalledProcessError as e:
#         print(f"FFmpeg error: {e}")
#         raise
#     except FileNotFoundError:
#         print("FFmpeg not found. Please install FFmpeg binary.")
#         raise

# # Usage
# output=convert_webm_to_wav_subprocess("question_0_1757221339361.webm", "converted.wav")
# # Usage
# result = transcribe_with_all_pauses_integrated(output, pause_threshold=2.0)













import joblib
import whisper
import speech_recognition as sr
import warnings
import re
import subprocess
import os
from faster_whisper import WhisperModel
from pydub import AudioSegment, silence

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
               
            }
        }

# Create analyzer instance
analyzer = FluentInterviewAnalyzer("fluency_predictor_linear_regression.pkl")

def convert_webm_to_wav_subprocess(input_file, output_file="output.wav"):
    """Convert WebM to WAV using subprocess"""
    
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")
    
    try:
        subprocess.run([
            "ffmpeg", "-i", input_file,
            "-acodec", "pcm_s16le",
            "-ar", "16000", 
            "-ac", "1",
            "-y",  # overwrite output
            output_file
        ], check=True, capture_output=True)
        
        print(f"Successfully converted {input_file} to {output_file}")
        print("\n🎤 Step 2: Transcribing with pause detection...")
        transcribe_with_all_pauses_integrated(output_file, pause_threshold=2.0)
        
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg error: {e}")
        raise
    except FileNotFoundError:
        print("FFmpeg not found. Please install FFmpeg binary.")
        raise

def clean_transcript_text(text):
    """Clean transcript text"""
    text = re.sub(r',([a-z])', r' \1', text)
    text = re.sub(r',\s*', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    if text:
        text = text[0].upper() + text[1:]
    return text

def transcribe_with_all_pauses_integrated(audio_file, pause_threshold=2.0):
    """
    Properly integrate ALL detected silences into the transcript
    """
    try:
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
        print(f"ASR Segments: {len(segments_list)}")
        
        # Load audio and detect actual silences
        try:
            # Try loading as WAV first
            audio = AudioSegment.from_wav(audio_file)
        except:
            # Fallback to general file loading
            audio = AudioSegment.from_file(audio_file)
        
        silences = silence.detect_silence(
            audio,
            min_silence_len=int(pause_threshold * 1000),
            silence_thresh=-40
        )
        
        print(f"Audio-based silences found: {len(silences)}")
        for i, (start_ms, end_ms) in enumerate(silences):
            duration = (end_ms - start_ms) / 1000
            print(f"  Silence {i+1}: {start_ms/1000:.2f}s - {end_ms/1000:.2f}s ({duration:.1f}s)")
        
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
                print(f"Added text: '{event['text']}'")
            elif event['type'] == 'silence':
                transcript += f"[PAUSE:{event['duration']:.1f}s] "
                print(f"Added pause: {event['duration']:.1f}s at {event['time']:.2f}s")
        
        # Return both transcript and analysis
        final_transcript = transcript.strip()
        print(f"\n📝 Final Enhanced Transcript:\n{final_transcript}\n")
        
        analysis_result = analyzer.analyze_transcript(final_transcript)
        
        print("\n✅ ANALYSIS COMPLETE")
        print("=" * 60)
        print(f"\n🗣️ Enhanced Transcript:\n{result['transcript']}")
        print(f"📊 Fluency Score: {result['analysis']['fluency_score']}")
        print(f"📈 Level: {result['analysis']['fluency_level']}")
        print(f"💭 Interpretation: {result['analysis']['interpretation']}")
        
        print("\n📋 Details:")
        for key, value in result['analysis']['details'].items():
            print(f"   {key}: {value}")
        
    except Exception as e:
        print(f"❌ Transcription error: {e}")
        return {
            'transcript': '',
            'analysis': None,
            'error': str(e)
        }




    wav_output = convert_webm_to_wav_subprocess("question_0_1757221339361.webm", "converted.wav")
    
   