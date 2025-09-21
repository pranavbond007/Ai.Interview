
import google.generativeai as genai
from flask import Flask, jsonify, request, session
from flask_cors import CORS  # 1. Add this import
import random
import json
import os


app = Flask(__name__)
CORS(app)  # 2. Add this line right after creating the app
app.secret_key = "supersecret"  # Required for session storage

# --- Configuration ---
# IMPORTANT: Replace with your actual API key
genai.configure(api_key="AIzaSyCb2EhuaIhTKzgaF_9Bo49F63HmrAq_bdU") 
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True) # Creates the upload folder if it doesn't exist

def generate_questions(resume_path):
    """
    Uploads a resume file to the generative AI model and generates interview questions.
    """
    try:
        # Upload the file to Gemini
        resume_file = genai.upload_file(path=resume_path)
        model = genai.GenerativeModel("gemini-1.5-flash")

        prompt = """
        You are an expert technical interviewer. Analyze the attached resume and generate exactly 10 interview questions in plain text.

        The structure of the questions must be as follows:
        - The very first question must be: "So, let’s start the interview. Can you tell me a bit about yourself?"
        - The next 5 questions must be based directly on the candidate's resume (skills, projects, education, or experience).
        - The final 4 questions must be general HR-style questions (e.g., "Why should we hire you?", "What are your career goals?", "Describe a time you failed.").
        
        Follow these rules strictly:
        - The order is critical: 1 introduction, 5 resume-based, 4 HR questions.
        - Do not number the questions or add any bullet points or extra formatting.
        - Each question should be on a new line.
        - Do not repeat questions.
        """

        response = model.generate_content([prompt, resume_file])

        # Clean up the response from the model
        questions = [q.strip() for q in response.text.split("\n") if q.strip()]
        
        # Ensure no duplicate questions
        questions = list(dict.fromkeys(questions))

        return questions[:10]

    finally:
        # Clean up the uploaded resume file from the server
        if os.path.exists(resume_path):
            os.remove(resume_path)

@app.route("/start_interview", methods=["POST"])
def start_interview():
    """
    Starts the interview by generating questions from an uploaded resume.
    """
    if 'resume' not in request.files:
        return jsonify({"error": "No resume file provided"}), 400

    resume_file = request.files['resume']
    if resume_file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if resume_file and resume_file.filename.endswith('.pdf'):

        # --- ✅ ADD THIS BLOCK TO CLEAR PREVIOUS ANALYSIS RESULTS ---
        try:
            # Open the analysis results file in 'w' (write) mode to clear it,
            # and write an empty JSON object.
            with open("fluency_analysis_results.json", "w") as f:
                json.dump({}, f)
            print("✅ Successfully cleared previous fluency analysis results.")
        except Exception as e:
            print(f"⚠️  Could not clear analysis results file: {e}")
        # --- END OF NEW BLOCK ---

        # Save the uploaded file temporarily
        filepath = os.path.join(UPLOAD_FOLDER, resume_file.filename)
        resume_file.save(filepath)

        # Generate a fresh set of questions from the uploaded resume
        questions = generate_questions(filepath)
        


        # --- ✅ ADD THIS BLOCK TO SAVE QUESTIONS TO A JSON FILE ---
        if questions:
            # Create a dictionary with numbered questions
            question_log = {f"Question {i+1}": q for i, q in enumerate(questions)}
            
            # Write the dictionary to a JSON file
            with open("generated_questions.json", "w") as f:
                json.dump(question_log, f, indent=4)
            print("✅ Successfully saved questions to generated_questions.json")
        # --- END OF NEW BLOCK ---

        return jsonify({
            "message": "Interview started successfully.",
            "questions": questions 
        })
    else:
        return jsonify({"error": "Invalid file type. Please upload a PDF."}), 400

if __name__ == "__main__":
    app.run(debug=True, port=4000)