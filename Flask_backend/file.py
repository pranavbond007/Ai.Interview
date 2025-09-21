








# from flask import Flask, jsonify
# import google.generativeai as genai
# import json
# import re
# import os
# from flask_cors import CORS
# from dotenv import load_dotenv

# load_dotenv()

# # --- 1. Flask App Initialization ---
# app = Flask(__name__)

# CORS(app, resources={r"/*": {"origins": ["http://localhost:5173"]}})

# # --- 2. Configure Gemini API ---
# try:
#     genai.configure(api_key=os.environ["Google_api_key"])
# except KeyError:
#     raise RuntimeError("GEMINI_API_KEY environment variable not set.")

# # --- 3. Load Models ---
# generative_model = genai.GenerativeModel("gemini-1.5-flash")

# # --- Helper Functions ---

# def load_json_file(filename):
#     """Safely loads a JSON file."""
#     try:
#         with open(filename, 'r') as f:
#             return json.load(f)
#     except (FileNotFoundError, json.JSONDecodeError):
#         return None

# def analyze_relevancy_with_reasoning(question, answer):
#     """
#     Analyzes answer relevancy using a generative model with a detailed prompt
#     to avoid flagging answers that merely repeat the question.
#     """
#     prompt = f"""
#     You are an Interview Analyst. Your task is to determine if the provided answer is a relevant and substantive response to the question.

#     **Instructions:**
#     1.  Read the question and the answer carefully.
#     2.  A "Relevant" answer directly addresses the question and provides specific information or examples.
#     3.  A "Not Relevant" answer is one that merely repeats the question, deflects, or fails to provide a substantive response.
#     4.  Your response MUST be a valid JSON object with two keys: "relevancy_status" and "reasoning".
#         - "relevancy_status": Either "Relevant" or "Not Relevant".
#         - "reasoning": A brief, one-sentence explanation for your decision.

#     **Question:** "{question}"
#     **Answer:** "{answer}"
#     """

#     safety_config = {
#         'HARM_CATEGORY_HARASSMENT': 'BLOCK_NONE',
#         'HARM_CATEGORY_HATE_SPEECH': 'BLOCK_NONE',
#         'HARM_CATEGORY_SEXUALLY_EXPLICIT': 'BLOCK_NONE',
#         'HARM_CATEGORY_DANGEROUS_CONTENT': 'BLOCK_NONE'
#     }

#     try:
#         # If the answer is empty, it's not relevant.
#         if not answer.strip():
#             return {"relevancy_status": "Not Relevant", "reasoning": "The answer was empty."}

#         response = generative_model.generate_content(prompt, safety_settings=safety_config)
        
#         if not response.text:
#             raise ValueError("The model returned an empty response.")

#         json_start = response.text.find('{')
#         json_end = response.text.rfind('}') + 1
        
#         if json_start == -1 or json_end == 0:
#             raise ValueError("No valid JSON object found in the model's response.")
            
#         cleaned_json_string = response.text[json_start:json_end]
#         analysis_result = json.loads(cleaned_json_string)

#         return {
#             "relevancy_status": analysis_result.get("relevancy_status", "Error"),
#             "reasoning": analysis_result.get("reasoning", "Could not determine reasoning.")
#         }

#     except (json.JSONDecodeError, ValueError) as e:
#         problematic_text = response.text if 'response' in locals() else "No response object."
#         return {"relevancy_status": "Error", "reasoning": f"Failed to parse model output: {e}. Raw: '{problematic_text}'"}
#     except Exception as e:
#         return {"relevancy_status": "Error", "reasoning": f"An unexpected error occurred: {e}"}

# def check_grammar_gemini(transcript):
#     """
#     Corrects a transcript for audio-to-text errors and then checks for grammatical issues.
#     """
#     prompt = f"""
#     You are a two-stage linguistic processor. First, you will correct a raw transcript for likely audio-to-text errors. Second, you will analyze the corrected text for grammar.

#     **Stage 1: Autocorrect Transcript**
#     - Review the following raw text for obvious spelling errors that likely came from an audio transcription (e.g., 'circlexity' should be 'Perplexity', 'slask fighting' should be 'Flask fighting').
#     - Your goal is to produce a clean, readable version of the text that reflects what the speaker most likely intended to say.

#     **Stage 2: Analyze Corrected Transcript**
#     - Using ONLY the corrected text from Stage 1, identify and report ONLY high-severity, objective grammatical errors.
#     - **High-Severity Errors (Report These)**: Subject-verb disagreement, incorrect tense, objectively wrong word forms (e.g., 'qualities improves').
#     - **Low-Severity Errors (Ignore These)**: Stylistic choices, suggestions for "better flow", comments on tone, or minor article usage.

#     **Output Format:**
#     Your response MUST be ONLY a valid JSON object with two keys: "corrected_text" and "errors".
#     - "corrected_text": The full, cleaned-up transcript from Stage 1.
#     - "errors": A list of high-severity errors from Stage 2. If there are none, the list must be empty.
#     - The 'context' and 'suggestion' fields in the 'errors' list MUST NOT contain any quotation marks (") or backslashes (\\).

#     **Raw Text to Process**: "{transcript}"
#     """
    
#     safety_config = {
#         'HARM_CATEGORY_HARASSMENT': 'BLOCK_NONE',
#         'HARM_CATEGORY_HATE_SPEECH': 'BLOCK_NONE',
#         'HARM_CATEGORY_SEXUALLY_EXPLICIT': 'BLOCK_NONE',
#         'HARM_CATEGORY_DANGEROUS_CONTENT': 'BLOCK_NONE'
#     }

#     try:
#         response = generative_model.generate_content(prompt, safety_settings=safety_config)
#         if not response.text:
#             return {"corrected_text": transcript, "errors": [{"type": "API Error", "context": "The model returned an empty response.", "suggestion": "This may indicate a temporary API issue."}]}
        
#         json_start = response.text.find('{')
#         json_end = response.text.rfind('}') + 1
        
#         if json_start == -1 or json_end == 0:
#             raise ValueError("No valid JSON object found in the model's response.")
            
#         cleaned_json_string = response.text[json_start:json_end]
#         analysis_result = json.loads(cleaned_json_string)
        
#         return {
#             "corrected_text": analysis_result.get("corrected_text", transcript),
#             "errors": analysis_result.get("errors", [])
#         }
#     except (json.JSONDecodeError, ValueError) as e:
#         problematic_text = response.text if 'response' in locals() else "No response object."
#         return {"corrected_text": transcript, "errors": [{"type": "Parsing Error", "context": f"Could not parse model output. Raw: '{problematic_text}'", "suggestion": f"Invalid JSON. Error: {e}"}]}
#     except Exception as e:
#         return {"corrected_text": transcript, "errors": [{"type": "Unexpected Error", "context": str(e), "suggestion": "An unknown error occurred during grammar check."}]}

# def create_final_report_gemini(questions_file, answers_file):
#     """Generates the comprehensive analysis report with the desired flat structure."""
#     questions_data = load_json_file(questions_file)
#     answers_data = load_json_file(answers_file)
#     if not questions_data or not answers_data:
#         raise FileNotFoundError("One or both input files could not be processed.")

#     final_report = {}
#     for i in range(len(questions_data.get("questions", []))):
#         question_number, question_key, answer_key = i + 1, f"Question {i + 1}", f"Answer{i + 1}"
#         question_text = questions_data["questions"][i]
#         answer_details = answers_data.get(answer_key)
#         if not answer_details: continue

#         original_transcript = answer_details.get("verbatim_transcript", "")
        
#         grammar_analysis = check_grammar_gemini(original_transcript)
#         corrected_transcript = grammar_analysis.get("corrected_text", original_transcript)
        
#         fluency_data = answer_details.get("fluency_analysis", {})
#         fluency_details = fluency_data.get("details", {})

#         report_for_question = {
#             "question": question_text,
#             "answer_transcript": corrected_transcript,
#             "grammatical_errors": grammar_analysis.get("errors", []),
#             "fluency_score": fluency_data.get("fluency_score"),
#             "fluency_level": fluency_data.get("fluency_level"),
#             "pause_count": fluency_details.get("pause_count"),
#             "total_pause_time": fluency_details.get("total_pause_time"),
#             "filler_count": fluency_details.get("filler_count"),
#             "filler_words": fluency_details.get("filler_words", [])
#         }
        
#         # Add relevancy analysis for specific questions using the new function
#         if 2 <= question_number <= 6:
#             relevancy_analysis = analyze_relevancy_with_reasoning(question_text, corrected_transcript)
#             report_for_question.update(relevancy_analysis)

#         final_report[question_key] = report_for_question

#             # ✅ ENSURE PROPER FILE OVERWRITING
#     report_filename = "analysis_report_final.json"
    
#     # Delete the old file if it exists
#     if os.path.exists(report_filename):
#         os.remove(report_filename)

#    # Write the new file and flush to disk
#     with open(report_filename, "w", encoding="utf-8") as f:
#         json.dump(final_report, f, indent=4, ensure_ascii=False)
#         f.flush()  # Force write to disk
#         os.fsync(f.fileno())  # Ensure it's written to disk
    
#     print(f"✅ Analysis report saved to {report_filename}")

# @app.route("/generate_report", methods=["POST"])
# def run_analysis_endpoint():
#     """API endpoint that triggers the full interview analysis."""
#     QUESTIONS_FILENAME = "generated_questions.json"
#     ANSWERS_FILENAME = "fluency_analysis_results.json"
#     REFORMATTED_QUESTIONS_FILENAME = "questions_reformatted.json"
    
#     if not (os.path.exists(QUESTIONS_FILENAME) and os.path.exists(ANSWERS_FILENAME)):
#         return jsonify({"error": "Required input file(s) not found."}), 404
#     try:
#         q_data = load_json_file(QUESTIONS_FILENAME)
#         if not q_data:
#             return jsonify({"error": "Question log file is empty or invalid."}), 400
        
#         with open(REFORMATTED_QUESTIONS_FILENAME, "w") as f:
#             json.dump({"questions": list(q_data.values())}, f)
        
#         create_final_report_gemini(REFORMATTED_QUESTIONS_FILENAME, ANSWERS_FILENAME)
        
#         return jsonify({"message": "Analysis complete. Report saved to 'analysis_report_final.json'"}), 200
#     except Exception as e:
#         return jsonify({"error": f"An unexpected error occurred during analysis: {str(e)}"}), 500

# if __name__ == "__main__":
#     app.run(debug=True, port=5001)














from flask import Flask, jsonify
import google.generativeai as genai
import json
import re
import os
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

# --- 1. Flask App Initialization ---
app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": ["http://localhost:5173"]}})

# --- 2. Configure Gemini API ---
try:
    genai.configure(api_key=os.environ["Google_api_key"])
except KeyError:
    raise RuntimeError("GEMINI_API_KEY environment variable not set.")

# --- 3. Load Models ---
generative_model = genai.GenerativeModel("gemini-1.5-flash")

# --- Helper Functions ---

def load_json_file(filename):
    """Safely loads a JSON file."""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def analyze_relevancy_with_reasoning(question, answer):
    """
    Analyzes answer relevancy using a generative model with a detailed prompt
    to avoid flagging answers that merely repeat the question.
    """
    prompt = f"""
    You are an Interview Analyst. Your task is to determine if the provided answer is a relevant and substantive response to the question.

    **Instructions:**
    1.  Read the question and the answer carefully.
    2.  A "Relevant" answer directly addresses the question and provides specific information or examples.
    3.  A "Not Relevant" answer is one that merely repeats the question, deflects, or fails to provide a substantive response.
    4.  Your response MUST be a valid JSON object with two keys: "relevancy_status" and "reasoning".
        - "relevancy_status": Either "Relevant" or "Not Relevant".
        - "reasoning": A brief, one-sentence explanation for your decision.

    **Question:** "{question}"
    **Answer:** "{answer}"
    """

    safety_config = {
        'HARM_CATEGORY_HARASSMENT': 'BLOCK_NONE',
        'HARM_CATEGORY_HATE_SPEECH': 'BLOCK_NONE',
        'HARM_CATEGORY_SEXUALLY_EXPLICIT': 'BLOCK_NONE',
        'HARM_CATEGORY_DANGEROUS_CONTENT': 'BLOCK_NONE'
    }

    try:
        # If the answer is empty, it's not relevant.
        if not answer.strip():
            return {"relevancy_status": "Not Relevant", "reasoning": "The answer was empty."}

        response = generative_model.generate_content(prompt, safety_settings=safety_config)
        
        if not response.text:
            raise ValueError("The model returned an empty response.")

        json_start = response.text.find('{')
        json_end = response.text.rfind('}') + 1
        
        if json_start == -1 or json_end == 0:
            raise ValueError("No valid JSON object found in the model's response.")
            
        cleaned_json_string = response.text[json_start:json_end]
        analysis_result = json.loads(cleaned_json_string)

        return {
            "relevancy_status": analysis_result.get("relevancy_status", "Error"),
            "reasoning": analysis_result.get("reasoning", "Could not determine reasoning.")
        }

    except (json.JSONDecodeError, ValueError) as e:
        problematic_text = response.text if 'response' in locals() else "No response object."
        return {"relevancy_status": "Error", "reasoning": f"Failed to parse model output: {e}. Raw: '{problematic_text}'"}
    except Exception as e:
        return {"relevancy_status": "Error", "reasoning": f"An unexpected error occurred: {e}"}

def check_grammar_gemini(transcript):
    """
    Corrects a transcript for audio-to-text errors and then checks for grammatical issues.
    """
    prompt = f"""
    You are a two-stage linguistic processor. First, you will correct a raw transcript for likely audio-to-text errors. Second, you will analyze the corrected text for grammar.

    **Stage 1: Autocorrect Transcript**
    - Review the following raw text for obvious spelling errors that likely came from an audio transcription (e.g., 'circlexity' should be 'Perplexity', 'slask fighting' should be 'Flask fighting').
    - Your goal is to produce a clean, readable version of the text that reflects what the speaker most likely intended to say.

    **Stage 2: Analyze Corrected Transcript**
    - Using ONLY the corrected text from Stage 1, identify and report ONLY high-severity, objective grammatical errors.
    - **High-Severity Errors (Report These)**: Subject-verb disagreement, incorrect tense, objectively wrong word forms (e.g., 'qualities improves').
    - **Low-Severity Errors (Ignore These)**: Stylistic choices, suggestions for "better flow", comments on tone, or minor article usage.

    **Output Format:**
    Your response MUST be ONLY a valid JSON object with two keys: "corrected_text" and "errors".
    - "corrected_text": The full, cleaned-up transcript from Stage 1.
    - "errors": A list of high-severity errors from Stage 2. If there are none, the list must be empty.
    - The 'context' and 'suggestion' fields in the 'errors' list MUST NOT contain any quotation marks (") or backslashes (\\).

    **Raw Text to Process**: "{transcript}"
    """
    
    safety_config = {
        'HARM_CATEGORY_HARASSMENT': 'BLOCK_NONE',
        'HARM_CATEGORY_HATE_SPEECH': 'BLOCK_NONE',
        'HARM_CATEGORY_SEXUALLY_EXPLICIT': 'BLOCK_NONE',
        'HARM_CATEGORY_DANGEROUS_CONTENT': 'BLOCK_NONE'
    }

    try:
        response = generative_model.generate_content(prompt, safety_settings=safety_config)
        if not response.text:
            return {"corrected_text": transcript, "errors": [{"type": "API Error", "context": "The model returned an empty response.", "suggestion": "This may indicate a temporary API issue."}]}
        
        json_start = response.text.find('{')
        json_end = response.text.rfind('}') + 1
        
        if json_start == -1 or json_end == 0:
            raise ValueError("No valid JSON object found in the model's response.")
            
        cleaned_json_string = response.text[json_start:json_end]
        analysis_result = json.loads(cleaned_json_string)
        
        return {
            "corrected_text": analysis_result.get("corrected_text", transcript),
            "errors": analysis_result.get("errors", [])
        }
    except (json.JSONDecodeError, ValueError) as e:
        problematic_text = response.text if 'response' in locals() else "No response object."
        return {"corrected_text": transcript, "errors": [{"type": "Parsing Error", "context": f"Could not parse model output. Raw: '{problematic_text}'", "suggestion": f"Invalid JSON. Error: {e}"}]}
    except Exception as e:
        return {"corrected_text": transcript, "errors": [{"type": "Unexpected Error", "context": str(e), "suggestion": "An unknown error occurred during grammar check."}]}

def create_final_report_gemini(questions_file, answers_file):
    """Generates the comprehensive analysis report with the desired flat structure."""
    questions_data = load_json_file(questions_file)
    answers_data = load_json_file(answers_file)
    if not questions_data or not answers_data:
        raise FileNotFoundError("One or both input files could not be processed.")

    final_report = {}
    for i in range(len(questions_data.get("questions", []))):
        question_number, question_key, answer_key = i + 1, f"Question {i + 1}", f"Answer{i + 1}"
        question_text = questions_data["questions"][i]
        answer_details = answers_data.get(answer_key)
        if not answer_details: continue

        original_transcript = answer_details.get("verbatim_transcript", "")
        
        grammar_analysis = check_grammar_gemini(original_transcript)
        corrected_transcript = grammar_analysis.get("corrected_text", original_transcript)
        
        fluency_data = answer_details.get("fluency_analysis", {})
        fluency_details = fluency_data.get("details", {})

        report_for_question = {
            "question": question_text,
            "answer_transcript": corrected_transcript,
            "grammatical_errors": grammar_analysis.get("errors", []),
            "fluency_score": fluency_data.get("fluency_score"),
            "fluency_level": fluency_data.get("fluency_level"),
            "pause_count": fluency_details.get("pause_count"),
            "total_pause_time": fluency_details.get("total_pause_time"),
            "filler_count": fluency_details.get("filler_count"),
            "filler_words": fluency_details.get("filler_words", [])
        }
        
        # Add relevancy analysis for specific questions using the new function
        if 2 <= question_number <= 6:
            relevancy_analysis = analyze_relevancy_with_reasoning(question_text, corrected_transcript)
            report_for_question.update(relevancy_analysis)

        final_report[question_key] = report_for_question

            # ✅ ENSURE PROPER FILE OVERWRITING
    report_filename = "analysis_report_final.json"
    
    # Delete the old file if it exists
    if os.path.exists(report_filename):
        os.remove(report_filename)

   # Write the new file and flush to disk
    with open(report_filename, "w", encoding="utf-8") as f:
        json.dump(final_report, f, indent=4, ensure_ascii=False)
        f.flush()  # Force write to disk
        os.fsync(f.fileno())  # Ensure it's written to disk
    
    print(f"✅ Analysis report saved to {report_filename}")

@app.route("/generate_report", methods=["POST"])
def run_analysis_endpoint():
    """API endpoint that triggers the full interview analysis."""
    print("🚀 /generate_report endpoint called")

    QUESTIONS_FILENAME = "generated_questions.json"
    ANSWERS_FILENAME = "fluency_analysis_results.json"
    REFORMATTED_QUESTIONS_FILENAME = "questions_reformatted.json"

    print(f"📁 Checking for files:")
    print(f"   - {QUESTIONS_FILENAME}: {os.path.exists(QUESTIONS_FILENAME)}")
    print(f"   - {ANSWERS_FILENAME}: {os.path.exists(ANSWERS_FILENAME)}")
    
    if not (os.path.exists(QUESTIONS_FILENAME) and os.path.exists(ANSWERS_FILENAME)):
        print("❌ Required input files not found")
        return jsonify({"error": "Required input file(s) not found."}), 404
    try:
        print("📖 Loading question data...")
        q_data = load_json_file(QUESTIONS_FILENAME)
        if not q_data:
            print("❌ Question file is empty or invalid")
            return jsonify({"error": "Question log file is empty or invalid."}), 400
        
        print(f"✅ Loaded {len(q_data)} questions")
        
        print("📝 Creating reformatted questions file...")
        
        with open(REFORMATTED_QUESTIONS_FILENAME, "w") as f:
            json.dump({"questions": list(q_data.values())}, f)
            print(f"✅ Created {REFORMATTED_QUESTIONS_FILENAME}")
        
        print("🔄 Generating final report...")
        
        create_final_report_gemini(REFORMATTED_QUESTIONS_FILENAME, ANSWERS_FILENAME)
        print("✅ Report generation complete!")

        # ✅ NEW: Read the generated file and return its contents
        report_filename = "analysis_report_final.json"
        if os.path.exists(report_filename):
            with open(report_filename, 'r', encoding='utf-8') as f:
                analysis_data = json.load(f)
        
            return jsonify({"message": "Analysis complete. Report saved to 'analysis_report_final.json'","analysis_data": analysis_data}), 200
    
        else:
         return jsonify({"error": "Report file was not created"}), 500
    except Exception as e:
        print(f"❌ Error during analysis: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"An unexpected error occurred during analysis: {str(e)}"}), 500
if __name__ == "__main__":
    app.run(debug=True, port=5001)



