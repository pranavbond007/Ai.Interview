import google.generativeai as genai
from flask import Flask, jsonify, request, session
import random

app = Flask(__name__)
app.secret_key = "supersecret"   # required for session storage

genai.configure(api_key="AIzaSyCb2EhuaIhTKzgaF_9Bo49F63HmrAq_bdU")


def generate_questions():
    resume_file = genai.upload_file("Priyanshu Resume final.pdf")
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = """
   You are an interviewer. Analyze this resume and create 10 interview questions in plain text.

- The first question must always be “So, <candidate name>, let’s start the interview. Can you tell me a bit about yourself?" 
- After that, ask 5 resume-based questions covering skills, projects, education, and experience.
- After the resume-based questions, ask 4 general HR questions such as "Why should we hire you?", "What are your career goals?", or "Describe a time you failed".
- The order must strictly follow how a real interviewer would ask:
  1. Start with "Tell me about yourself".
  2. Then move into resume-based questions.
  3. Finish with the HR-style questions.
- Do not repeat the "Tell me about yourself" question anywhere else.
- Do not number or categorize the questions. Just output them as plain text, one per line.


    """

    response = model.generate_content([prompt, resume_file])

    # clean questions
    questions = [q.strip("0123456789. ").strip()
                 for q in response.text.split("\n")
                 if q.strip()]

    # remove duplicates
    questions = list(dict.fromkeys(questions))

    # shuffle


    # limit to 10
    return questions[:10]


@app.route("/start_interview", methods=["GET"])
def start_interview():
    # generate fresh set of questions
    questions = generate_questions()
    session["questions"] = questions
    session["index"] = 0
    return jsonify({"message": "Interview started", "total_questions": len(questions)})


@app.route("/next_question", methods=["GET"])
def next_question():
    if "questions" not in session:
        return jsonify({"error": "Interview not started yet"}), 400

    index = session["index"]
    questions = session["questions"]

    if index < len(questions):
        question = questions[index]
        session["index"] = index + 1
        return jsonify({"question": question, "remaining": len(questions) - (index + 1)})
    else:
        return jsonify({"message": "No more questions"})


if __name__ == "__main__":
    app.run(debug=True)
