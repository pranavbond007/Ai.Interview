# 🤖 AI-Powered Interview Coach

**AI-Powered Interview Coach** is a full-stack intelligent platform designed to help users master their interview skills. It provides a realistic practice environment by generating tailored questions from an uploaded resume and delivering instantaneous, AI-driven feedback on verbal fluency, grammatical accuracy, and content relevance.

## 🎯 Features

-   **Hybrid Transcription System**: Utilizes **Gemini 1.5 Flash** for primary, real-time verbatim transcription and automatically falls back to **Faster-Whisper** to ensure service reliability and handle API limits.
-   **Advanced Fluency Analytics**: Captures and analyzes speech patterns, including filler words (`um`, `uh`, `like`), speech rate, and pause cadences, to generate a precise fluency score using a custom-trained model.
-   **Intelligent Grammar Evaluation**: Employs a sophisticated two-stage Gemini prompt that not only identifies high-severity grammatical errors but also provides a corrected version of the user's transcript.
-   **Substantive Relevancy Scoring**: A unique "AI Judge" evaluates the substance of a user's answer, distinguishing between genuine responses and those that merely repeat keywords from the prompt.
-   **Comprehensive Reporting**: Generates detailed JSON reports (`analysis_report_final.json`) that consolidate all analytical feedback for a structured and insightful user review.
-   **Modern, Responsive Frontend**: A sleek and intuitive user interface built with **React** and **Tailwind CSS**, featuring animated UI elements and clear data visualizations.

## 🛠 Tech Stack

-   **Frontend**: React, Vite, Tailwind CSS, Framer Motion
-   **Backend**: Flask (Python 3.10)
-   **AI & Machine Learning**: Google Gemini API, Faster-Whisper, Scikit-learn
-   **Audio Processing**: FFmpeg (for audio conversion), `pydub` (for silence detection)

## 📁 Project Structure

AI-Interview-Coach/
├── Flask_backend/
│ ├── Final_code_flask.py
│ ├── fluency_predictor_linear_regression.pkl
│ ├── requirements.txt
│ ├── .env
│ └── ... (other backend files)
│
└── Frontend/
├── src/
│ ├── components/
│ │ ├── interview/
│ │ ├── results/
│ │ └── ui/
│ ├── pages/
│ ├── services/
│ └── App.jsx
├── package.json
├── tailwind.config.js
└── vite.config.js

text

## 📋 Prerequisites

Before you begin, ensure you have the following installed on your system:

-   **Git**
-   **Node.js** (v16 or higher) and **npm**
-   **Python** (v3.9 or higher) and **pip**
-   **FFmpeg** (must be installed and accessible from your system's PATH)

## 🚀 Getting Started

### Step 1: Clone the Repository

git clone https://github.com/your-username/AI-Interview-Coach.git
cd AI-Interview-Coach

text

### Step 2: Install Dependencies

#### Backend (`Flask_backend`)

Open a terminal and run the following commands:

cd Flask_backend
python -m venv venv

Activate the virtual environment
On Windows:
venv\Scripts\activate

On macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt

text

#### Frontend (`Frontend`)

Open a **second terminal** and run:

cd Frontend
npm install

text

## 🔑 Environment Setup

### Step 3: Configure API Key

You will need a Google Gemini API key to run the backend.

1.  Create a file named `.env` inside the `Flask_backend` directory.
2.  Add your API key to this file:

    ```
    Google_api_key="YOUR_GOOGLE_GEMINI_API_KEY_HERE"
    ```

## 🏃‍♀️ Running the Application

You need to run both the frontend and backend servers simultaneously.

### Terminal 1: Run the Backend

Make sure you are in the `Flask_backend` directory with your virtual environment activated.

python Final_code_flask.py

text

The backend server will start on `http://localhost:5001`.

### Terminal 2: Run the Frontend

Make sure you are in the `Frontend` directory.

npm run dev

text

The frontend development server will start, usually on `http://localhost:5173`.

## 🌐 Access the Application

Once both servers are running, open your browser and navigate to `http://localhost:5173`. You should now see the AI Interview Coach interface, ready for use.

## 📱 How to Use

1.  **Upload Resume**: Start by uploading your resume to receive tailored interview questions.
2.  **Record Answers**: For each question, record your answer directly in the browser.
3.  **Receive Feedback**: Once the interview is complete, the platform will process your answers and present a detailed report on your performance, covering fluency, grammar, and the relevance of your responses.

## 🤝 Contributing

Contributions are welcome! If you have ideas for new features or improvements:

1.  Fork the repository.
2.  Create a new feature branch (`git checkout -b feature/NewFeature`).
3.  Commit your changes (`git commit -m 'Add some NewFeature'`).
4.  Push to the branch (`git push origin feature/NewFeature`).
5.  Open a Pull Request.

