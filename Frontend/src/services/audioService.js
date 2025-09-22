// src/services/audioService.js
export class AudioService {
  constructor() {
    // ✅ FIXED: Use import.meta.env for Vite instead of process.env
    this.apiBaseUrl = import.meta.env.VITE_API_URL || 'http://localhost:3001/api';
  }

  async sendAudioFilesToBackend(recordings, interviewMetadata) {
    const formData = new FormData();
    
    // Add each audio file
    recordings.forEach((recording, index) => {
      formData.append(`audioFile_${index}`, recording.file);
      formData.append(`metadata_${index}`, JSON.stringify({
        questionIndex: recording.questionIndex,
        question: recording.question,
        timestamp: recording.timestamp,
        duration: recording.duration
      }));
    });
    
    // Add interview metadata
    formData.append('interviewMetadata', JSON.stringify(interviewMetadata));

    try {
      const response = await fetch(`${this.apiBaseUrl}/interview/evaluate`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error sending audio files:', error);
      throw error;
    }
  }

  async sendSingleAudioFile(recordingData) {
    const formData = new FormData();
    formData.append('audioFile', recordingData.file);
    formData.append('metadata', JSON.stringify({
      questionIndex: recordingData.questionIndex,
      question: recordingData.question,
      timestamp: recordingData.timestamp,
      duration: recordingData.duration
    }));

    try {
      const response = await fetch(`${this.apiBaseUrl}/interview/evaluate-single`, {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error sending single audio file:', error);
      throw error;
    }
  }
}
