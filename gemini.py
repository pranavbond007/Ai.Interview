import google.generativeai as genai
import random
genai.configure(api_key="AIzaSyCb2EhuaIhTKzgaF_9Bo49F63HmrAq_bdU")

def get_questions():
    # upload resume (PDF/DOCX)
    resume_file = genai.upload_file("Anant_s_Resume (2).pdf")
    print("Uploaded file:", resume_file.name)

    # initialize model
    model = genai.GenerativeModel("gemini-1.5-flash")

    # prompt
    prompt = """
    You are an interviewer. Analyze this resume and create 10 interview questions:
    - 6 based on resume content (skills, projects, education, experience).
    - 4 general HR questions like "Tell me about yourself", "Why should we hire you?".
     Return ONLY the 10 questions in plain text (no categories, no numbering, no explanations).
    """

    response = model.generate_content([prompt, resume_file])

    # split into list
     # split by lines and clean
    questions = [q.strip("0123456789. ").strip()
                 for q in response.text.split("\n")
                 if q.strip()]


    random.shuffle(questions)
    
    return {"questions": questions}

print(get_questions())
