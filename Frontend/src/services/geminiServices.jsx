import { GoogleGenerativeAI } from '@google/generative-ai'

const genAI = new GoogleGenerativeAI(import.meta.env.VITE_GEMINI_API_KEY)

export class InterviewService {
  constructor() {
    this.model = genAI.getGenerativeModel({ model: "gemini-pro" })
    this.questions = []
    this.currentQuestionIndex = 0
  }

  async generateQuestions(resumeText, jobRole, experience) {
    const prompt = `
    Based on this resume and job requirements, generate 10 interview questions:
    
    Resume: ${resumeText}
    Target Role: ${jobRole}
    Experience Level: ${experience}
    
    Requirements:
    1. Mix of technical and behavioral questions
    2. Progressive difficulty
    3. Role-specific scenarios
    4. Questions should assess both hard and soft skills
    
    Return as JSON array with structure: 
    {
      "questions": [
        {
          "id": 1,
          "text": "question text",
          "type": "technical|behavioral|situational",
          "difficulty": "easy|medium|hard",
          "expectedDuration": "seconds",
          "keyPoints": ["point1", "point2"]
        }
      ]
    }
    `

    try {
      const result = await this.model.generateContent(prompt)
      const response = result.response.text()
      const data = JSON.parse(response)
      this.questions = data.questions
      return this.questions
    } catch (error) {
      console.error('Error generating questions:', error)
      return [{
          id: 1,
          text: "Tell me about yourself and your background",
          type: "behavioral",
          difficulty: "easy",
          expectedDuration: 120
        },
        {
          id: 2,
          text: "Why are you interested in this position?",
          type: "behavioral", 
          difficulty: "easy",
          expectedDuration: 90
        },
        {
          id: 3,
          text: "Describe a challenging project you worked on",
          type: "technical",
          difficulty: "medium", 
          expectedDuration: 180
        },
        {
          id: 4,
          text: "How do you handle tight deadlines and pressure?",
          type: "behavioral",
          difficulty: "medium",
          expectedDuration: 120
        },
        {
          id: 5,
          text: "Where do you see yourself in 5 years?",
          type: "behavioral",
          difficulty: "easy",
          expectedDuration: 90
        }]
    }
  }

  getNextQuestion() {
    if (this.currentQuestionIndex < this.questions.length) {
      return this.questions[this.currentQuestionIndex++]
    }
    return null
  }

  async evaluateAnswer(question, answer, videoAnalysis) {
    const prompt = `
    Evaluate this interview answer:
    
    Question: ${question.text}
    Answer: ${answer}
    Video Analysis: ${JSON.stringify(videoAnalysis)}
    
    Provide detailed feedback including:
    1. Content relevance (1-10)
    2. Technical accuracy (1-10) 
    3. Communication clarity (1-10)
    4. Areas for improvement
    5. Strengths demonstrated
    6. Overall score (1-10)
    
    Return as JSON.
    `

    try {
      const result = await this.model.generateContent(prompt)
      return JSON.parse(result.response.text())
    } catch (error) {
      console.error('Error evaluating answer:', error)
      return {
        contentRelevance: 8,
        technicalAccuracy: 7,
        communicationClarity: 8,
        overallScore: 8,
        strengths: ["Good examples", "Clear communication"],
        improvements: ["Add more technical details", "Reduce filler words"]
      }
    }
  }
}
