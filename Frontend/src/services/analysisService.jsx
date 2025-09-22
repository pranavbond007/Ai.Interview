// Simple frontend-only analysis (placeholders for now)
export class AnalysisService {
  analyzeVideo(videoBlob) {
    // Placeholder - returns mock data
    return {
      facialAnalysis: {
        confidence: Math.random() * 0.3 + 0.7,
        eyeContact: Math.random() * 0.4 + 0.6,
        emotions: { neutral: 0.6, confident: 0.3, nervous: 0.1 },
        engagement: Math.random() * 0.3 + 0.7
      },
      gestureAnalysis: {
        handGestures: Math.floor(Math.random() * 20),
        bodyLanguage: "open",
        posture: "good"
      }
    }
  }

  analyzeAudio(audioBlob) {
    // Placeholder - returns mock data
    return {
      transcript: "This is a sample transcript of what you said.",
      speechMetrics: {
        wordsPerMinute: Math.floor(Math.random() * 50) + 120,
        fillerWords: ["um", "uh", "like"],
        fillerCount: Math.floor(Math.random() * 10),
        pauseDuration: Math.random() * 10 + 2,
        clarity: Math.random() * 0.3 + 0.7,
        volume: Math.random() * 0.5 + 0.5
      },
      sentiment: {
        confidence: Math.random() * 0.4 + 0.6,
        positivity: Math.random() * 0.5 + 0.5
      }
    }
  }
}
