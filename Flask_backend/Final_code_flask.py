



# import joblib
# import warnings
# import re
# import subprocess
# import os
# import json
# import gc
# from faster_whisper import WhisperModel
# from pydub import AudioSegment, silence
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from werkzeug.utils import secure_filename


# # --- Configuration ---
# # Suppress unnecessary warnings
# warnings.filterwarnings('ignore')


# # Define paths and constants for the project
# UPLOADS_FOLDER = 'temp_uploads'  # A folder to temporarily store uploaded files
# ALLOWED_EXTENSIONS = {'webm', 'wav', 'mp3', 'm4a', 'mp4'}
# MODEL_FILE = "fluency_predictor_linear_regression.pkl"
# RESULTS_JSON_PATH = "fluency_analysis_results.json"
# WHISPER_MODEL_SIZE = 'base.en'  # Use 'tiny.en' for less memory, 'large' for more accuracy


# # Ensure the temporary upload folder exists
# os.makedirs(UPLOADS_FOLDER, exist_ok=True)


# # --- 1. YOUR CORE ANALYSIS ENGINE (Modified to accept separate pauses) ---
# class FluentInterviewAnalyzer:
#     """Analyzes fluency from a transcript string and a separate list of pauses."""
#     def __init__(self, model_path):
#         if not os.path.exists(model_path):
#             raise FileNotFoundError(f"Model file not found: {model_path}.")
        
#         self.model_package = joblib.load(model_path)
#         self.model, self.scaler, self.feature_names = self.model_package['model'], self.model_package['scaler'], self.model_package['feature_names']
#         self.filler_patterns = r'\b(um|uh|er|ah|you know|like|actually|basically)\b'
#         print("✅ Fluency analyzer engine loaded.")


#     def analyze_transcript(self, transcript_text, detected_pauses):
#         """Processes the transcript and a separate list of pauses."""
#         filler_matches = re.findall(self.filler_patterns, transcript_text, re.IGNORECASE)
#         filler_count = len(filler_matches)
        
#         pause_count = len(detected_pauses)
#         total_pause_time = sum(pause['duration'] for pause in detected_pauses)


#         clean_text = re.sub(self.filler_patterns, '', transcript_text, re.IGNORECASE)
#         word_count = len(clean_text.split())
        
#         filler_density = filler_count / max(word_count, 1)
#         pause_density = pause_count / max(word_count, 1)
#         avg_pause_duration = total_pause_time / max(pause_count, 1)
        
#         estimated_speech_time = (word_count / 2.0) + total_pause_time
#         speech_rate = (word_count / estimated_speech_time) * 60 if estimated_speech_time > 0 else 120
        
#         features = {
#             'filler_count': filler_count, 'pause_count': pause_count, 'total_pause_time': total_pause_time,
#             'word_count': word_count, 'speech_rate': speech_rate, 'filler_density': filler_density,
#             'pause_density': pause_density, 'avg_pause_duration': avg_pause_duration,
#             'has_long_pauses': int(total_pause_time > 3.0),
#             'has_multiple_pauses': int(pause_count > 1),
#             'filler_type_count': len(set(filler_matches)),
#             'hesitation_score': (filler_density * 0.4) + (pause_density * 0.3) + (int(total_pause_time > 3.0) * 0.3),
#             'speech_efficiency': word_count / max(1, word_count + filler_count + pause_count)
#         }
        
#         feature_vector = [features.get(name, 0) for name in self.feature_names]
#         feature_vector_scaled = self.scaler.transform([feature_vector])
#         fluency_score = max(0.0, min(1.0, self.model.predict(feature_vector_scaled)[0]))
        
#         if fluency_score >= 0.8: level, interp = "Excellent", "Very fluent response."
#         elif fluency_score >= 0.7: level, interp = "Good", "Generally fluent."
#         elif fluency_score >= 0.6: level, interp = "Fair", "Moderate fluency."
#         else: level, interp = "Poor", "Low fluency."
        
#         return {'fluency_score': round(fluency_score, 3), 'fluency_level': level, 'interpretation': interp,
#                 'details': {'filler_count': filler_count, 'filler_words': list(set(filler_matches)),
#                             'pause_count': pause_count, 'total_pause_time': round(total_pause_time, 1)}}


# # --- 2. YOUR PIPELINE ORCHESTRATOR ---
# class FluencyPipeline:
#     """A pipeline that performs transcription and silence detection as separate steps."""
#     def __init__(self, model_path, whisper_model_size, results_json_path):
#         print("\n🚀 Initializing Decoupled Fluency Analysis Pipeline...")
#         self.analyzer = FluentInterviewAnalyzer(model_path)
#         self.results_file = results_json_path
#         print(f"💡 Loading Whisper model: '{whisper_model_size}'...")
#         self.whisper_model = WhisperModel(whisper_model_size, device="cpu", compute_type="float32")
#         print("✅ Pipeline ready.")


#     def _save_cumulative_results(self, data_to_save):
#         data = {};
#         if os.path.exists(self.results_file) and os.path.getsize(self.results_file) > 0:
#             try:
#                 with open(self.results_file, 'r') as f: data = json.load(f)
#             except json.JSONDecodeError: print(f"⚠️ Warning: Corrupted JSON file '{self.results_file}'.")
#         next_key = f"Answer{len(data) + 1}"; data[next_key] = data_to_save
#         with open(self.results_file, 'w') as f: json.dump(data, f, indent=4)
#         print(f"✅ Cumulative analysis saved to '{self.results_file}' as '{next_key}'.")


#     def run(self, input_audio_file, silence_threshold_db, min_pause_ms=700):
#         """Executes the full decoupled pipeline and returns the final analysis."""
#         print(f"\n▶️ Processing file: {input_audio_file} with threshold: {silence_threshold_db}dBFS")
#         temp_wav_file = os.path.join(UPLOADS_FOLDER, "temp_analysis_audio.wav")
#         try:
#             print("🔄 Step 1: Converting to WAV...")
#             subprocess.run(["ffmpeg", "-i", input_audio_file, "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1", "-y", temp_wav_file], check=True, capture_output=True, text=True)
#             if not os.path.exists(temp_wav_file) or os.path.getsize(temp_wav_file) == 0: raise IOError("FFmpeg failed to create a valid output file.")


#             print("🎤 Step 2a: Transcribing for words and fillers...")
#             filler_prompt = "Transcribe this audio, including filler words like um, uh, and ah."
#             segments, _ = self.whisper_model.transcribe(temp_wav_file, beam_size=1, language='en', initial_prompt=filler_prompt)
#             verbatim_transcript = " ".join([s.text.strip() for s in segments])


#             print("🤫 Step 2b: Detecting precise silences separately...")
#             audio = AudioSegment.from_wav(temp_wav_file)
#             silence_intervals_ms = silence.detect_silence(audio, min_silence_len=min_pause_ms, silence_thresh=silence_threshold_db)
            
#             # --- MODIFIED SECTION ---
#             # Filter the detected silences to only include those longer than 1.5 seconds (1500 ms)
#             significant_pauses_ms = [(s, e) for s, e in silence_intervals_ms if (e - s) > 1500]
#             detected_pauses = [{'start': s/1000, 'end': e/1000, 'duration': (e-s)/1000} for s, e in significant_pauses_ms]
#             # --- END OF MODIFIED SECTION ---
            
#             print("🧠 Step 3: Analyzing fluency with separate data...")
#             analysis_result = self.analyzer.analyze_transcript(verbatim_transcript, detected_pauses)


#             print("💾 Step 4: Formatting and saving results...")
#             final_output = {"verbatim_transcript": verbatim_transcript, "fluency_analysis": analysis_result}
#             self._save_cumulative_results(final_output)
            
#             return final_output # Return the dictionary for the API response
#         finally:
#             if os.path.exists(temp_wav_file): os.remove(temp_wav_file)
#             print("🧹 Step 5: Cleaned up temporary file."); gc.collect()


# # --- 3. FLASK APPLICATION WRAPPER ---
# app = Flask(__name__)

# CORS(app, resources={r"/*": {"origins": ["http://localhost:5173"]}})
# app.config['UPLOADS_FOLDER'] = UPLOADS_FOLDER


# # Load models once when the server starts
# try:
#     pipeline = FluencyPipeline(model_path=MODEL_FILE, whisper_model_size=WHISPER_MODEL_SIZE, results_json_path=RESULTS_JSON_PATH)
#     print("\n✅ All models loaded. Flask server is ready.")
# except Exception as e:
#     print(f"❌ CRITICAL ERROR ON STARTUP: {e}. The server cannot start.")
#     pipeline = None


# def is_allowed_file(filename):
#     """Checks if the file extension is allowed."""
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# @app.route('/analyze', methods=['POST'])
# def analyze_audio_endpoint():
#     """The main API endpoint that the frontend will call."""
#     if pipeline is None:
#         return jsonify({"error": "Server is not initialized. Check logs for startup errors."}), 500


#     if 'audio_file' not in request.files:
#         return jsonify({"error": "No 'audio_file' part in the form data"}), 400
    
#     file = request.files['audio_file']
#     if file.filename == '':
#         return jsonify({"error": "No file selected"}), 400
        
#     if file and is_allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         temp_input_path = os.path.join(app.config['UPLOADS_FOLDER'], filename)
#         file.save(temp_input_path)


#         try:
#             # You can get these values from the frontend if needed, e.g., request.form.get('threshold', -50)
#             silence_threshold = -50 # Your proven magic number
#             min_pause = 700 # Default pause length in ms


#             analysis_result = pipeline.run(input_audio_file=temp_input_path, silence_threshold_db=silence_threshold, min_pause_ms=min_pause)
#             if analysis_result:
#                 return jsonify(analysis_result), 200
#             else:
#                 return jsonify({"error": "Analysis failed to produce a result."}), 500
#         except Exception as e:
#             print(f"❌ An error occurred during the pipeline run: {e}")
#             return jsonify({"error": "An internal error occurred during analysis.", "details": str(e)}), 500
#         finally:
#             if os.path.exists(temp_input_path):
#                 os.remove(temp_input_path)
#     else:
#         return jsonify({"error": f"File type not allowed. Allowed types: {list(ALLOWED_EXTENSIONS)}"}), 400


# # --- 4. RUN THE SERVER ---
# if __name__ == '__main__':
#     # Use host='0.0.0.0' to make the server accessible on the local network
#     app.run(host='0.0.0.0', port=5000, debug=True)




import joblib
import warnings
import re
import subprocess
import os
import json
import gc
from dotenv import load_dotenv
from faster_whisper import WhisperModel
from pydub import AudioSegment, silence
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import google.generativeai as genai  

from flask_cors import CORS

# --- Configuration ---
warnings.filterwarnings('ignore')
load_dotenv()
UPLOADS_FOLDER = 'temp_uploads'
ALLOWED_EXTENSIONS = {'webm', 'wav', 'mp3', 'm4a', 'mp4'}
MODEL_FILE = "fluency_predictor_linear_regression.pkl"
RESULTS_JSON_PATH = "fluency_analysis_results.json"
WHISPER_MODEL_SIZE = 'base.en'  # backup transcriber

# Ensure temp folder exists
os.makedirs(UPLOADS_FOLDER, exist_ok=True)

# --- 1. CORE ANALYSIS ENGINE ---
class FluentInterviewAnalyzer:
    """Analyzes fluency from a transcript string and a separate list of pauses."""
    def __init__(self, model_path):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}.")
        self.model_package = joblib.load(model_path)
        self.model = self.model_package['model']
        self.scaler = self.model_package['scaler']
        self.feature_names = self.model_package['feature_names']
        self.filler_patterns = r'\b(um|uh|er|ah|you know|like|actually|basically)\b'
        print("✅ Fluency analyzer engine loaded.")

    def analyze_transcript(self, transcript_text, detected_pauses):
        filler_matches = re.findall(self.filler_patterns, transcript_text, re.IGNORECASE)
        filler_count = len(filler_matches)

        pause_count = len(detected_pauses)
        total_pause_time = sum(p['duration'] for p in detected_pauses)

        clean_text = re.sub(self.filler_patterns, '', transcript_text, re.IGNORECASE)
        word_count = len(clean_text.split())

        filler_density = filler_count / max(word_count, 1)
        pause_density = pause_count / max(word_count, 1)
        avg_pause_duration = total_pause_time / max(pause_count, 1)

        estimated_speech_time = (word_count / 2.0) + total_pause_time
        speech_rate = (word_count / estimated_speech_time) * 60 if estimated_speech_time > 0 else 120

        features = {
            'filler_count': filler_count,
            'pause_count': pause_count,
            'total_pause_time': total_pause_time,
            'word_count': word_count,
            'speech_rate': speech_rate,
            'filler_density': filler_density,
            'pause_density': pause_density,
            'avg_pause_duration': avg_pause_duration,
            'has_long_pauses': int(total_pause_time > 3.0),
            'has_multiple_pauses': int(pause_count > 1),
            'filler_type_count': len(set(filler_matches)),
            'hesitation_score': (filler_density * 0.4) + (pause_density * 0.3) + (int(total_pause_time > 3.0) * 0.3),
            'speech_efficiency': word_count / max(1, word_count + filler_count + pause_count)
        }

        feature_vector = [features.get(name, 0) for name in self.feature_names]
        feature_vector_scaled = self.scaler.transform([feature_vector])
        fluency_score = max(0.0, min(1.0, self.model.predict(feature_vector_scaled)[0]))

        if fluency_score >= 0.8:
            level, interp = "Excellent", "Very fluent response."
        elif fluency_score >= 0.7:
            level, interp = "Good", "Generally fluent."
        elif fluency_score >= 0.6:
            level, interp = "Fair", "Moderate fluency."
        else:
            level, interp = "Poor", "Low fluency."

        return {
            'fluency_score': round(fluency_score, 3),
            'fluency_level': level,
            'interpretation': interp,
            'details': {
                'filler_count': filler_count,
                'filler_words': list(set(filler_matches)),
                'pause_count': pause_count,
                'total_pause_time': round(total_pause_time, 1)
            }
        }

# --- 2. PIPELINE ORCHESTRATOR ---
class FluencyPipeline:
    """Performs transcription (Gemini primary, Whisper fallback) and silence detection."""
    def __init__(self, model_path, whisper_model_size, results_json_path):
        print("\n🚀 Initializing Decoupled Fluency Analysis Pipeline...")
        self.analyzer = FluentInterviewAnalyzer(model_path)
        self.results_file = results_json_path

        # Configure Gemini once
        # Expect API key in env var "Google_api_key" (keep consistent with your other services)
        api_key = os.environ.get("Google_api_key")
        if not api_key:
            print("⚠️ Google_api_key not set; Gemini transcription will fail and fall back to Whisper.")
        genai.configure(api_key=api_key)

        # Gemini model for primary transcription
        self.gemini_model = genai.GenerativeModel("gemini-1.5-flash")

        print(f"💡 Loading Whisper model (fallback): '{whisper_model_size}'...")
        self.whisper_model = WhisperModel(whisper_model_size, device="cpu", compute_type="float32")
        print("✅ Pipeline ready.")

    def _save_cumulative_results(self, data_to_save):
        data = {}
        if os.path.exists(self.results_file) and os.path.getsize(self.results_file) > 0:
            try:
                with open(self.results_file, 'r') as f:
                    data = json.load(f)
            except json.JSONDecodeError:
                print(f"⚠️ Warning: Corrupted JSON file '{self.results_file}'.")
        next_key = f"Answer{len(data) + 1}"
        data[next_key] = data_to_save
        with open(self.results_file, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"✅ Cumulative analysis saved to '{self.results_file}' as '{next_key}'.")

    # NEW: Gemini-first transcription, Whisper as backup
    def transcribe_with_gemini(self, wav_path: str, strict_verbatim: bool = True) -> str:
        """
        Use Gemini to transcribe WAV, preserving fillers and disfluencies with a strict prompt.
        Falls back to empty string on error; caller decides Whisper fallback.
        """
        # For small files, inline bytes are fine; for >~20MB consider Files API (not changing flow here)
        with open(wav_path, "rb") as f:
            audio_bytes = f.read()

        prompt = (
            "You are a speech transcription assistant. "
            "Transcribe the audio word-for-word exactly as spoken.\n"
            "Rules:\n"
            "- Include filler words like um, uh, you know, like, erm.\n"
            "- Keep hesitations, repetitions, stutters, and false starts.\n"
            "- Do not clean grammar or make the text more fluent."
            if strict_verbatim else
            "Please transcribe the audio."
        )

        try:
            # Inline audio part with mime type, alongside text prompt (Gemini multimodal input)
            # This mirrors the documented inline-bytes audio pattern for generateContent.
            response = self.gemini_model.generate_content(
                [prompt, {"mime_type": "audio/wav", "data": audio_bytes}]
            )
            text = (response.text or "").strip()
            return text
        except Exception as e:
            print(f"⚠️ Gemini transcription failed: {e}. Will fall back to Whisper.")
            return ""

    def run(self, input_audio_file, silence_threshold_db, min_pause_ms=700):
        """Executes the pipeline and returns the final analysis."""
        print(f"\n▶️ Processing file: {input_audio_file} with threshold: {silence_threshold_db}dBFS")
        temp_wav_file = os.path.join(UPLOADS_FOLDER, "temp_analysis_audio.wav")
        try:
            # Step 1: Convert to WAV (16kHz mono PCM)
            print("🔄 Step 1: Converting to WAV...")
            subprocess.run(
                ["ffmpeg", "-i", input_audio_file, "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1", "-y", temp_wav_file],
                check=True, capture_output=True, text=True
            )
            if not os.path.exists(temp_wav_file) or os.path.getsize(temp_wav_file) == 0:
                raise IOError("FFmpeg failed to create a valid output file.")

            # Step 2a: Transcribe — Gemini primary, Whisper fallback
            print("🎤 Step 2a: Transcribing (Gemini primary)...")
            verbatim_transcript = self.transcribe_with_gemini(temp_wav_file, strict_verbatim=True)

            if not verbatim_transcript:
                print("🔁 Falling back to Whisper for transcription...")
                filler_prompt = "Transcribe this audio, including filler words like um, uh, and ah."
                segments, _ = self.whisper_model.transcribe(
                    temp_wav_file, beam_size=1, language='en', initial_prompt=filler_prompt
                )
                verbatim_transcript = " ".join([s.text.strip() for s in segments]).strip()

            # Step 2b: Silence detection (unchanged)
            print("🤫 Step 2b: Detecting precise silences separately...")
            audio = AudioSegment.from_wav(temp_wav_file)
            silence_intervals_ms = silence.detect_silence(
                audio, min_silence_len=min_pause_ms, silence_thresh=silence_threshold_db
            )
            detected_pauses = [
                {'start': s / 1000, 'end': e / 1000, 'duration': (e - s) / 1000}
                for s, e in silence_intervals_ms
            ]

            # Step 3: Fluency analysis (unchanged)
            print("🧠 Step 3: Analyzing fluency with separate data...")
            analysis_result = self.analyzer.analyze_transcript(verbatim_transcript, detected_pauses)

            # Step 4: Save (unchanged)
            print("💾 Step 4: Formatting and saving results...")
            final_output = {"verbatim_transcript": verbatim_transcript, "fluency_analysis": analysis_result}
            self._save_cumulative_results(final_output)

            return final_output
        finally:
            if os.path.exists(temp_wav_file):
                os.remove(temp_wav_file)
            print("🧹 Step 5: Cleaned up temporary file.")
            gc.collect()

# --- 3. FLASK APPLICATION WRAPPER ---
app = Flask(__name__)
CORS(app)
app.config['UPLOADS_FOLDER'] = UPLOADS_FOLDER

# Load models once when the server starts
try:
    pipeline = FluencyPipeline(model_path=MODEL_FILE, whisper_model_size=WHISPER_MODEL_SIZE, results_json_path=RESULTS_JSON_PATH)
    print("\n✅ All models loaded. Flask server is ready.")
except Exception as e:
    print(f"❌ CRITICAL ERROR ON STARTUP: {e}. The server cannot start.")
    pipeline = None

def is_allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/analyze', methods=['POST'])
def analyze_audio_endpoint():
    if pipeline is None:
        return jsonify({"error": "Server is not initialized. Check logs for startup errors."}), 500

    if 'audio_file' not in request.files:
        return jsonify({"error": "No 'audio_file' part in the form data"}), 400

    file = request.files['audio_file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    if file and is_allowed_file(file.filename):
        filename = secure_filename(file.filename)
        temp_input_path = os.path.join(app.config['UPLOADS_FOLDER'], filename)
        file.save(temp_input_path)

        try:
            silence_threshold = -50
            min_pause = 700
            analysis_result = pipeline.run(
                input_audio_file=temp_input_path,
                silence_threshold_db=silence_threshold,
                min_pause_ms=min_pause
            )
            if analysis_result:
                return jsonify(analysis_result), 200
            else:
                return jsonify({"error": "Analysis failed to produce a result."}), 500
        except Exception as e:
            print(f"❌ An error occurred during the pipeline run: {e}")
            return jsonify({"error": "An internal error occurred during analysis.", "details": str(e)}), 500
        finally:
            if os.path.exists(temp_input_path):
                os.remove(temp_input_path)
    else:
        return jsonify({"error": f"File type not allowed. Allowed types: {list(ALLOWED_EXTENSIONS)}"}), 400

if __name__ == '__main__':
    # Host 0.0.0.0 allows local network access (unchanged)
    app.run(host='0.0.0.0', port=5000, debug=True)