# 🤖 AI-Powered Interview Coach  

**AI-Powered Interview Coach** is a full-stack platform designed to help users **master their interview skills** with a realistic practice environment.  

It empowers candidates by:  
- Generating **tailored technical and behavioral questions** from uploaded resumes  
- Providing **instant feedback** on fluency, grammar, and content relevance  
- Offering **real-time transcription** with fillers and pauses preserved  
- Presenting **interactive analytics** in a modern, easy-to-use dashboard  

---

## 🎯 Features  

- **Hybrid Transcription System**  
  Real-time verbatim transcription with **Google Gemini 1.5 Flash** and automatic fallback to **Faster-Whisper** for reliability.  

- **Advanced Fluency Analytics**  
  Detects fillers (*um, uh, like*), speech rate, and pauses, generating a **fluency score** using a custom ML model.  

- **Intelligent Grammar Evaluation**  
  Two-stage Gemini evaluation that highlights grammar errors **and** provides corrected transcripts for learning.  

- **Substantive Relevancy Scoring**  
  Unique **AI Judge** checks if answers are truly on-topic, not just keyword-matching.  

- **Comprehensive Reports**  
  Structured **JSON reports** (`analysis_report_final.json`) with detailed performance breakdowns.  

- **Modern UI**  
  Built with **React + Tailwind CSS**, animated via **Framer Motion**, featuring clean data visualizations.  

---

## 🛠 Tech Stack  

- **Frontend**: React, Vite, Tailwind CSS, Framer Motion  
- **Backend**: Flask (Python 3.10)  
- **AI & ML**: Google Gemini API, Faster-Whisper, Scikit-learn  
- **Audio Processing**: FFmpeg, pydub  

---

## 📁 Project Structure  

