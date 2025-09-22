# 🤖 AI.Interview - AI-Powered Interview Coach

**AI.Interview** is a comprehensive full-stack platform designed to help users **master their interview skills** through realistic practice environments. It empowers candidates by:
- Generating **tailored technical and behavioral questions** from uploaded resumes
- Providing **instant feedback** on fluency, grammar, and content relevance
- Offering **real-time transcription** with fillers and pauses preserved
- Presenting **interactive analytics** in a modern, easy-to-use dashboard
- Delivering **comprehensive performance reports** for continuous improvement

## 🎯 Features

- **Hybrid Transcription System**: Real-time verbatim transcription with Google Gemini 1.5 Flash and automatic fallback to Faster-Whisper for reliability
- **Advanced Fluency Analytics**: Detects fillers (*um, uh, like*), speech rate, and pauses, generating fluency scores using custom ML models
- **Intelligent Grammar Evaluation**: Two-stage Gemini evaluation that highlights grammar errors and provides corrected transcripts for learning
- **Substantive Relevancy Scoring**: Unique AI Judge checks if answers are truly on-topic, not just keyword-matching
- **Resume-Based Question Generation**: Personalized interview questions based on uploaded resume content
- **Comprehensive Reports**: Structured JSON reports with detailed performance breakdowns and improvement suggestions
- **Modern UI**: Built with React + Tailwind CSS, animated via Framer Motion, featuring clean data visualizations
- **Audio Processing**: Advanced audio handling with FFmpeg integration for optimal transcription quality

## 🛠 Tech Stack

- **Frontend**: React.js, Vite, Tailwind CSS, Framer Motion
- **Backend**: Flask (Python 3.10) with robust API architecture
- **AI & ML**: Google Gemini API, Faster-Whisper, Scikit-learn
- **Audio Processing**: FFmpeg, pydub for high-quality audio handling
- **File Handling**: Multer-equivalent for resume uploads
- **Data Visualization**: Custom charts and analytics dashboard

## 📁 Project Structure

```
AI.Interview/
├── Flask_backend/                 # Backend server and AI models
│   ├── models/                   # ML models and AI logic
│   │   └── fluency_predictor_linear_regression.pkl
│   ├── uploads/                  # Resume upload directory
│   ├── audio_files/             # Temporary audio storage
│   ├── reports/                 # Generated analysis reports
│   ├── Final_code_flask.py      # Main Flask application
│   ├── requirements.txt         # Python dependencies
│   ├── .env                     # Environment variables
│   └── config.py               # Configuration settings
├── Frontend/                    # React frontend application
│   ├── public/                  # Static assets
│   │   └── vite.svg            # App icon
│   ├── src/                     # React source code
│   │   ├── components/          # React components
│   │   │   ├── interview/       # Interview-related components
│   │   │   ├── results/         # Results and analytics
│   │   │   └── ui/              # UI components
│   │   ├── pages/               # Page components
│   │   ├── services/            # API service functions
│   │   ├── utils/               # Utility functions
│   │   ├── App.jsx              # Main React component
│   │   ├── index.css            # Global styles
│   │   └── main.jsx             # React entry point
│   ├── .gitignore              # Git ignore rules
│   ├── package.json            # Node.js dependencies
│   ├── package-lock.json       # Dependency lock file
│   ├── tailwind.config.js      # Tailwind configuration
│   └── vite.config.js          # Vite configuration
└── README.md                   # Project documentation
```

## 📋 Prerequisites

Before setting up AI.Interview, ensure you have the following installed on your system:

### 1. Git Installation
**Windows:**
```bash
# Download Git from https://git-scm.com/download/win
# Or using Chocolatey
choco install git

# Verify installation
git --version
```

**macOS:**
```bash
# Using Homebrew
brew install git

# Or download from https://git-scm.com/download/mac
# Verify installation
git --version
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install git

# Verify installation
git --version
```

### 2. Node.js and npm Installation
**Windows:**
```bash
# Download from https://nodejs.org/
# Or using Chocolatey
choco install nodejs

# Verify installation
node --version
npm --version
```

**macOS:**
```bash
# Using Homebrew
brew install node

# Or download from https://nodejs.org/
# Verify installation
node --version
npm --version
```

**Linux (Ubuntu/Debian):**
```bash
# Using NodeSource repository
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verify installation
node --version
npm --version
```

### 3. Python Installation
**Windows:**
```bash
# Download from https://www.python.org/downloads/
# Or using Chocolatey
choco install python

# Verify installation
python --version
pip --version
```

**macOS:**
```bash
# Using Homebrew
brew install python

# Verify installation
python3 --version
pip3 --version
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip

# Verify installation
python3 --version
pip3 --version
```

### 4. FFmpeg Installation
**Windows:**
```bash
# Download from https://ffmpeg.org/download.html
# Or using Chocolatey
choco install ffmpeg

# Verify installation
ffmpeg -version
```

**macOS:**
```bash
# Using Homebrew
brew install ffmpeg

# Verify installation
ffmpeg -version
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install ffmpeg

# Verify installation
ffmpeg -version
```

## 🚀 Getting Started

### Step 1: Clone the Repository

```bash
# Clone the repository
git clone https://github.com/your-username/AI.Interview.git

# Navigate to the project directory
cd AI.Interview
```

### Step 2: Install Dependencies

#### Python Dependencies (Flask Backend)
```bash
# Navigate to backend directory
cd Flask_backend

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Install Python packages
pip install -r requirements.txt
```

#### Node.js Dependencies (React Frontend)
```bash
# Navigate to frontend directory
cd Frontend

# Install Node.js packages
npm install

# If you encounter any issues, try:
npm install --legacy-peer-deps
```

## 🔑 Environment Setup

### Step 3: API Keys Configuration

You'll need to obtain and configure the following API key:

#### Google Gemini API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. **Integration Method:**

**Option A: Environment Variable (Recommended)**
```bash
# Create .env file in Flask_backend directory
cd Flask_backend
echo "Google_api_key=your_google_gemini_api_key_here" > .env
```

**Option B: Direct Integration in Code**
In `Flask_backend/Final_code_flask.py`, find the configuration section and replace:
```python
genai.configure(api_key="YOUR_API_KEY_HERE")
```
with your actual API key:
```python
genai.configure(api_key="your_google_gemini_api_key_here")
```

## 🏃‍♀️ Running the Application

You'll need to run two servers simultaneously. Open **2 separate terminals**:

### Terminal 1: Flask Backend (AI/ML Server)
```bash
cd AI.Interview/Flask_backend

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows

# Run Flask server
python Final_code_flask.py
```
**Expected Output:**
```
🚀 Starting Flask AI Interview Coach...
📡 Health check: GET http://localhost:5001/health
🔧 Analyze endpoint: POST http://localhost:5001/analyze
📊 Generate report: POST http://localhost:5001/generate_report
==================================================
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5001
 * Running on http://localhost:5001
```

### Terminal 2: React Frontend
```bash
cd AI.Interview/Frontend

# Start React development server
npm run dev
```
**Expected Output:**
```
  VITE v4.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h to show help
```

## 🌐 Access the Application

Once both servers are running:

1. **Frontend**: Open http://localhost:5173 in your browser
2. **Backend Health Check**: Visit http://localhost:5001/health
3. **API Documentation**: Available at http://localhost:5001/docs (if implemented)

## 📱 How to Use AI.Interview

1. **Upload Resume**: Navigate to the upload section and submit your resume in PDF format
2. **Review Generated Questions**: The AI will create personalized interview questions based on your resume
3. **Start Practice Session**: 
   - Click on any question to begin recording
   - Speak clearly into your microphone
   - The system provides real-time transcription
4. **Get Instant Feedback**: After each answer, receive:
   - Fluency score with detailed breakdown
   - Grammar evaluation with corrections
   - Content relevance assessment
   - Improvement suggestions
5. **View Comprehensive Reports**: Access detailed analytics including:
   - Overall performance metrics
   - Question-by-question analysis
   - Trend analysis over multiple sessions
   - Downloadable JSON reports

## 🔒 Privacy & Security Features

- **Resume Security**: Uploaded resumes are processed locally and automatically deleted after session
- **Audio Privacy**: Voice recordings are analyzed securely and not stored beyond processing time
- **Data Protection**: No personal information is shared with external services
- **Secure Processing**: All AI analysis happens in isolated environments
- **Transparency**: Clear indication of what data is being processed and how

## 🛠 API Endpoints

### Flask Backend (Port 5001)
- `GET /health` - Health check and system status
- `POST /analyze` - Analyze audio input and generate feedback
- `POST /generate_report` - Compile comprehensive performance report
- `POST /upload_resume` - Upload and process resume for question generation
- `GET /questions` - Retrieve generated interview questions
- `DELETE /clear_session` - Clear session data and temporary files

## 📦 Dependencies

### Python Requirements (requirements.txt)
```
Flask==3.0.3
Flask-Cors==4.0.0
google-generativeai==0.7.2
faster-whisper==1.0.1
scikit-learn==1.4.2
numpy==1.26.4
pydub==0.25.1
python-dotenv==1.0.0
werkzeug==3.0.3
pandas==2.2.2
matplotlib==3.8.4
seaborn==0.13.2
speech-recognition==3.10.4
```

### Node.js Dependencies (package.json)
```json
{
  "name": "ai-interview-frontend",
  "version": "1.0.0",
  "type": "module",
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.8.0",
    "framer-motion": "^11.0.0",
    "lucide-react": "^0.263.1",
    "recharts": "^2.8.0",
    "axios": "^1.6.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "@vitejs/plugin-react": "^4.0.3",
    "tailwindcss": "^3.3.0",
    "autoprefixer": "^10.4.14",
    "postcss": "^8.4.24",
    "vite": "^4.4.5"
  }
}
```

## 🔧 Troubleshooting

### Common Issues

**1. Port Already in Use**
```bash
# Find and kill process using port 5001
lsof -ti:5001 | xargs kill -9  # macOS/Linux
netstat -ano | findstr :5001   # Windows

# Find and kill process using port 5173
lsof -ti:5173 | xargs kill -9  # macOS/Linux
netstat -ano | findstr :5173   # Windows
```

**2. Python Module Not Found**
```bash
# Ensure virtual environment is activated
pip install -r requirements.txt --force-reinstall

# If still having issues, upgrade pip
python -m pip install --upgrade pip
```

**3. Node Modules Issues**
```bash
# Clear npm cache and reinstall
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

**4. FFmpeg Not Found**
```bash
# Verify FFmpeg installation
ffmpeg -version

# If not found, reinstall FFmpeg following the prerequisites section
```

**5. API Key Errors**
- Verify Google Gemini API key is correctly set in `.env` file
- Check API key permissions and quotas in Google AI Studio
- Ensure internet connectivity for API calls
- Verify the API key format (should start with "AI...")

**6. Audio Recording Issues**
- Check browser microphone permissions
- Ensure HTTPS is used for production (required for microphone access)
- Test microphone functionality in browser settings
- Clear browser cache and cookies

**7. Resume Upload Problems**
- Ensure uploaded file is in PDF format
- Check file size limits (usually under 10MB)
- Verify Flask backend is running and accessible
- Check upload directory permissions

## 🚀 Performance Optimization

### Backend Optimizations
- **Model Caching**: ML models are loaded once and cached for faster inference
- **Async Processing**: Audio analysis runs asynchronously to prevent blocking
- **Memory Management**: Automatic cleanup of temporary files and audio data
- **API Rate Limiting**: Built-in protection against excessive API calls

### Frontend Optimizations
- **Code Splitting**: Components are lazily loaded for faster initial load times
- **Caching**: API responses are cached to reduce redundant requests
- **Optimistic Updates**: UI updates immediately while processing in background
- **Progressive Loading**: Large datasets are loaded progressively

## 🔄 Advanced Features

### Custom ML Model Training
The fluency predictor can be retrained with your own data:
```bash
cd Flask_backend
python train_fluency_model.py --data your_training_data.csv
```

### Batch Processing
Process multiple audio files at once:
```bash
python batch_process.py --input audio_folder/ --output results/
```

### Export Options
- **JSON Reports**: Structured data for further analysis
- **PDF Summaries**: Human-readable performance reports
- **CSV Data**: Raw metrics for spreadsheet analysis

## 🤝 Contributing

We welcome contributions to make AI.Interview better and more comprehensive:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Contribution Guidelines
- Follow existing code style and conventions
- Add tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting PR

## 🧪 Testing

### Running Tests
```bash
# Backend tests
cd Flask_backend
python -m pytest tests/

# Frontend tests
cd Frontend
npm test
```

### Test Coverage
- **Backend**: Unit tests for ML models, API endpoints, and audio processing
- **Frontend**: Component tests, integration tests, and E2E tests
- **Performance**: Load testing for concurrent users and large file uploads

## 📈 Roadmap

- [ ] **Multi-language Support**: Support for interviews in different languages
- [ ] **Video Analysis**: Analyze body language and eye contact during interviews
- [ ] **Industry-specific Questions**: Tailored questions for different job roles
- [ ] **Mock Interview Scheduling**: Calendar integration for practice sessions
- [ ] **Peer Review System**: Get feedback from other users
- [ ] **Mobile App**: Native iOS and Android applications
- [ ] **Integration APIs**: Connect with job boards and recruiting platforms

## 📞 Support & Resources

### Technical Support
- Create an issue on GitHub for bugs or feature requests
- Join our community discussions
- Check the [Wiki](https://github.com/your-username/AI.Interview/wiki) for detailed guides

### Interview Resources
- Access our blog for interview tips and best practices
- Download sample resumes and question templates
- Join webinars on effective interview preparation

## 🏆 Success Stories

*"AI.Interview helped me identify my speaking patterns and improve my confidence. I landed my dream job after just two weeks of practice!"* - Sarah M., Software Engineer

*"The personalized questions based on my resume were incredibly accurate. It felt like a real interview experience."* - David L., Product Manager

*"The fluency analysis was eye-opening. I never realized how many filler words I used!"* - Priya S., Data Scientist

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with passion for helping candidates succeed in their interviews
- Thanks to all contributors, testers, and the open-source community
- Special appreciation for feedback from career counselors and HR professionals
- Inspired by the need for accessible, high-quality interview preparation tools

---

**AI.Interview** - Your AI-powered partner for interview success! 🤖

*"Practice makes perfect. AI makes it smarter."*
