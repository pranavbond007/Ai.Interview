import { useState, useEffect, useRef } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { useNavigate } from 'react-router-dom'
import GlowingButton from '../components/ui/GlowingButton'
import AIAvatar from '../components/interview/AIAvatar'
import ProgressBar from '../components/interview/ProgressBar'
import { InterviewService } from '../services/geminiServices'
import { AnalysisService } from '../services/analysisService'
import LoadingScreen from '../components/ui/LoadingScreen'

export default function InterviewSession() {
  const navigate = useNavigate()
  const [currentQuestion, setCurrentQuestion] = useState(0)
  const [sessionStarted, setSessionStarted] = useState(false)
  const [showQuestion, setShowQuestion] = useState(false)
  const [questions, setQuestions] = useState([])
  const [showCompletionModal, setShowCompletionModal] = useState(false)
  const [isRecording, setIsRecording] = useState(false)
  const [recordingTime, setRecordingTime] = useState(0)
  const [savedFiles, setSavedFiles] = useState(0)
  const [stream, setStream] = useState(null)
  const [cameraReady, setCameraReady] = useState(false)
  // Inside InterviewSession component, with other state variables
  //For Python integration.
const [isAnalyzing, setIsAnalyzing] = useState(false);
const [analysisResults, setAnalysisResults] = useState([]);

const [isProcessing, setIsProcessing] = useState(false);


    

  
  // ✅ Keep your working recording setup
  const videoRef = useRef(null)
  const mediaRecorderRef = useRef(null)
  const streamRef = useRef(null)
  const chunksRef = useRef([])
    // Add with the other refs at the top of your component
  const activeQuestionRef = useRef(0);

  // Services for analysis
  const [interviewService] = useState(new InterviewService())
  const [analysisService] = useState(new AnalysisService())
  const [interviewData, setInterviewData] = useState({ answers: [] })

// This useEffect hook now fetches the first question on component load
// useEffect(() => {
//   setSessionStarted(true); // Assuming session starts immediately
//   setShowQuestion(true);
//   fetchNextQuestion();
// }, []); // Runs only once when the component mounts

useEffect(() => {
  const storedQuestions = sessionStorage.getItem('interviewQuestions');
  if (storedQuestions) {
    const parsedQuestions = JSON.parse(storedQuestions);
    setQuestions(parsedQuestions);
    handleStartSession(parsedQuestions[0]); // Start with the first question
  } else {
    // Handle case where user lands here directly without uploading a resume
    alert("Please upload a resume first.");
    navigate('/upload-resume');
  }
}, []);


  // ✅ Keep your working timer
  useEffect(() => {
    let interval
    if (isRecording) {
      interval = setInterval(() => {
        setRecordingTime(prev => prev + 1)
      }, 1000)
    } else {
      setRecordingTime(0)
    }
    return () => clearInterval(interval)
  }, [isRecording])

//   const fetchNextQuestion = async () => {
//   try {
//     const response = await fetch('http://localhost:4000/next_question');
//     const data = await response.json();

//     if (response.ok) {
//       if (data.question) {
//         setActiveQuestion(data.question);
//         setQuestionNumber(data.question_number);
//         if (data.question_number === 1) { // First question
//             setTotalQuestions(data.remaining_questions + 1);
//         }
//         speakQuestion(data.question);
//       } else {
//         // No more questions
//         setIsInterviewOver(true);
//         handleEndInterview();
//       }
//     } else {
//       throw new Error(data.error || 'Failed to fetch next question.');
//     }
//   } catch (error) {
//     console.error("Error fetching question:", error);
//     // Handle error, maybe show a message to the user
//   }
// };


  // ✅ Enhanced speech synthesis
  const speakQuestion = (text) => {
    try {
      if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel()
        const utterance = new SpeechSynthesisUtterance(text)
        utterance.rate = 0.9
        utterance.pitch = 1.1
        utterance.volume = 0.8
        speechSynthesis.speak(utterance)
        console.log('🔊 Speaking:', text.substring(0, 50) + '...')
      }
    } catch (error) {
      console.error('Speech synthesis error:', error)
    }
  }

  // // ✅ Clear previous session (keep your working code)
  // const clearPreviousSession = async () => {
  //   try {
  //     const response = await fetch('http://localhost:3001/api/interview/clear-session', {
  //       method: 'POST'
  //     });
  //     if (response.ok) {
  //       console.log('✅ Previous files cleared');
  //     }
  //   } catch (error) {
  //     console.error('Clear session error:', error);
  //   }
  // };

  // ✅ ADD THIS NEW FUNCTION
const clearPreviousSession = async () => {
  try {
    const response = await fetch('http://localhost:3001/api/interview/clear-session', {
      method: 'POST'
    });
    if (response.ok) {
      console.log('✅ Previous audio files cleared from server.');
    }
  } catch (error) {
    console.error('Error clearing previous session audio:', error);
  }
};


  // ✅ Enhanced camera setup with better error handling
  // ✅ BULLETPROOF: Camera setup that actually works
const setupCamera = async () => {
  try {
    console.log('🎬 Setting up camera...');
    
    const mediaStream = await navigator.mediaDevices.getUserMedia({
      video: true,
      audio: true
    });
    
    console.log('📹 Got media stream:', mediaStream);
    
    streamRef.current = mediaStream;
    setStream(mediaStream);
    
    // ✅ CRITICAL FIX: Use setTimeout to ensure React has finished rendering
    setTimeout(() => {
      if (videoRef.current && mediaStream) {
        videoRef.current.srcObject = mediaStream;
        
        // Try to play and handle autoplay issues
        videoRef.current.play()
          .then(() => {
            console.log('📹 Video playing successfully');
            setCameraReady(true); // Set here as backup
          })
          .catch((error) => {
            console.log('Autoplay blocked, but camera ready');
            setCameraReady(true); // Still set ready even if autoplay fails
          });
      }
    }, 100); // Small delay for React to finish rendering
    
    // Setup MediaRecorder
    const recorder = new MediaRecorder(mediaStream);
    mediaRecorderRef.current = recorder;
    
    recorder.ondataavailable = (e) => {
      if (e.data.size > 0) {
        chunksRef.current.push(e.data);
      }
    };
    
    recorder.onstop = () => {
      saveAudio(activeQuestionRef.current);
    };
    
    console.log('✅ Camera setup complete!');
    return true;
    
  } catch (error) {
    console.error('❌ Camera error:', error);
    alert('Camera permission denied. Please allow camera access and refresh.');
    return false;
  }
};

// Add this new function inside your InterviewSession component
const analyzeFluency = async (audioBlob, filename) => {
  console.log(`🧠 Sending "${filename}" for fluency analysis...`);
  setIsAnalyzing(true);

  const formData = new FormData();
  // CRITICAL: The key MUST be 'audio_file' to match your Flask backend
  formData.append('audio_file', audioBlob, filename);

  try {
    const response = await fetch('http://localhost:5000/analyze', {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      // Throw an error to be caught by the catch block
      const errorData = await response.json();
      throw new Error(errorData.error || 'Fluency analysis failed');
    }

    const result = await response.json();
    console.log('✅ Fluency analysis successful:', result);

    // Store the result
    setAnalysisResults(prev => [...prev, { filename, ...result }]);

  } catch (error) {
    console.error('❌ Fluency analysis error:', error);
    // Optionally, show an error to the user
  } finally {
    setIsAnalyzing(false);
  }
};



  // ✅ Keep your working saveAudio function
  const saveAudio = async (questionNumber) => {
    if (chunksRef.current.length === 0) {
      console.log('No audio chunks')
      return
    }

    console.log('Saving audio with', chunksRef.current.length, 'chunks')

    const audioBlob = new Blob(chunksRef.current, { type: 'audio/webm' })
    const filename = `audio${questionNumber + 1}.webm`
    // --- 🚀 TRIGGER THE ANALYSIS HERE ---
    // Call the new function to send the audio to the Python backend
    await analyzeFluency(audioBlob, filename);
    
    try {
      const formData = new FormData()
      formData.append('audioFile', audioBlob, filename)
      formData.append('audioName', filename)  // ✅ ADD THIS LINE ONLY
      formData.append('questionIndex', questionNumber.toString())
      formData.append('question', questions[questionNumber]); // Use the questions array
      // Add this log to verify correct name
      console.log('📝 Sending filename:', filename, 'for question:', currentQuestion + 1)


      const response = await fetch('http://localhost:3001/api/interview/save-recording', {
        method: 'POST',
        body: formData
      })
      
      if (response.ok) {
        const result = await response.json()
        console.log('✅ Saved:', result.filename)
        setSavedFiles(prev => prev + 1)
      } else {
        console.error('❌ Save failed:', response.status)
      }
    } catch (error) {
      console.error('❌ Network error:', error)
    }
    
    // Update interview data for analysis
    setInterviewData(prev => ({
      answers: [...prev.answers, {
        questionIndex: currentQuestion,
        question: questions[currentQuestion],
        filename: filename,
        timestamp: new Date().toISOString()
      }]
    }))
    
    chunksRef.current = []
  }

  // ✅ Enhanced start session
  const handleStartSession = async (firstQuestion) => {
    console.log('🎬 Starting interview session...')
   if (sessionStarted) return;
   await clearPreviousSession(); // ✅ ADD THIS LINE
    const cameraIsReady = await setupCamera();
    if (cameraIsReady) {
        setSessionStarted(true);
        setShowQuestion(true);
        speakQuestion(firstQuestion);
    }
  }

  // ✅ Keep your working toggle recording
// ✅ SIMPLE: Recording toggle that works
const handleRecordingToggle = () => {
  if (!mediaRecorderRef.current || !cameraReady) {
    alert('Camera not ready yet. Please wait.');
    return;
  }

  if (isRecording) {
    console.log('⏹️ Stopping recording...');
    mediaRecorderRef.current.stop();
    setIsRecording(false);
  } else {
    console.log('🎤 Starting recording...');
    chunksRef.current = [];
    activeQuestionRef.current = currentQuestion; // <-- track this
    mediaRecorderRef.current.start();
    setIsRecording(true);
  }
};


  // ✅ Enhanced repeat question
  const handleRepeatQuestion = (e) => {
    e.preventDefault()
    e.stopPropagation()
    console.log('🔄 Repeating question:', currentQuestion + 1)
    if (questions[currentQuestion]) {
      speakQuestion(questions[currentQuestion])
    }
  }

  const handleNextQuestion = () => {
  if (isRecording) {
    mediaRecorderRef.current?.stop();
    setIsRecording(false);
  }

  if (currentQuestion < questions.length - 1) {
    const nextIndex = currentQuestion + 1;
    setCurrentQuestion(nextIndex);
    setShowQuestion(false);
    setTimeout(() => {
        setShowQuestion(true);
        speakQuestion(questions[nextIndex]);
    }, 500);
  } else {
    handleEndInterview();
  }
};


  // ✅ Enhanced end interview
  // const handleEndInterview = async () => {
  //   console.log('🏁 Ending interview...')
  //   console.log('📁 Files saved:', savedFiles)
    
  //   // Stop camera stream
  //   if (streamRef.current) {
  //     streamRef.current.getTracks().forEach(track => track.stop())
  //   }


  //   // Show loading and generate report
  // setShowCompletionModal(false);
  // setIsProcessing(true); // Add this state

  //   // ✅ ADD THIS: Generate the analysis report
  // try {
  //   console.log('📊 Generating comprehensive analysis report...')
  //   const reportResponse = await fetch('http://localhost:5001/generate_report', {
  //     method: 'POST',
  //     headers: {
  //       'Content-Type': 'application/json'
  //     }
  //   });
    
  //   if (reportResponse.ok) {
  //     const reportResult = await reportResponse.json()
  //     console.log('✅ Analysis report generated:', reportResult.message)

  //     // Fetch the generated analysis file
  //     const analysisResponse = await fetch('/analysis_report_final.json');
  //     const analysisData = reportResult.analysis_data;
  //     if (analysisData) {
  //       // Store in localStorage
  //       localStorage.setItem('interviewAnalysisResults', JSON.stringify(analysisData));
        
  //       // Navigate to results
  //       navigate('/results');
  //     }  else {
  //       console.error('❌ No analysis data received');
  //       alert('Analysis completed but no data received. Please try again.');
  //       setShowCompletionModal(true);
  //     }
      
  //   } else {
  //     const errorText = await reportResponse.text();
  //     console.error('❌ Failed to generate analysis report:', errorText);
  //     alert('Failed to generate analysis report. Please try again.');
  //     setShowCompletionModal(true);
  //   }
  // } catch (error) {
  //   console.error('❌ Error generating analysis report:', error);
  //   alert('Error generating analysis report. Please check your connection and try again.');
  //   setShowCompletionModal(true);
  // }
    
  //   // // Store results
  //   // const results = {
  //   //   overallScore: Math.floor(Math.random() * 20) + 80,
  //   //   sections: {
  //   //     content: Math.floor(Math.random() * 15) + 85,
  //   //     delivery: Math.floor(Math.random() * 15) + 80,
  //   //     confidence: Math.floor(Math.random() * 20) + 75,
  //   //     technical: Math.floor(Math.random() * 15) + 80
  //   //   },
  //   //   questionsAnswered: currentQuestion + 1,
  //   //   totalQuestions: questions.length,
  //   //   savedFiles: savedFiles,
  //   //   interviewData: interviewData
  //   // }
    
  //   // localStorage.setItem('interviewResults', JSON.stringify(results))
  //   // setShowCompletionModal(true)

  //   setIsProcessingResults(false);  
  // }








  const handleEndInterview = async () => {
  console.log('🏁 Ending interview...');
  if (streamRef.current) {
    streamRef.current.getTracks().forEach(track => track.stop());
  }

  // Set the state to show your loading screen
  setIsProcessing(true); 

  try {
    // Call your Python backend to generate the report
    const reportResponse = await fetch('http://localhost:5001/generate_report', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
    });

    if (!reportResponse.ok) {
      // If the server response is not OK (e.g., 404, 500), throw an error
      const errorText = await reportResponse.text();
      throw new Error(`Failed to generate report: ${errorText}`);
    }

    // The backend will now send the analysis data directly in the response.
    // We just need to parse it.
    const reportResult = await reportResponse.json();
    
    // Check if the analysis_data key exists in the response from your backend
    if (reportResult && reportResult.analysis_data) {
      console.log('✅ Analysis data received successfully from backend.');
      
      // Store the received data in localStorage for the Results.jsx page to use
      localStorage.setItem('interviewAnalysisResults', JSON.stringify(reportResult.analysis_data));
      
      // Navigate to the results page
      navigate('/results');

    } else {
      // This error happens if the backend response is malformed
      throw new Error('Backend response is missing "analysis_data".');
    }

  } catch (error) {
    // This will catch any error from the fetch call or the logic above
    console.error('❌ A critical error occurred during report generation:', error);
    alert(`An error occurred: ${error.message}. Please check the console for details.`);
    setIsProcessing(false); // Hide loading screen so the user is not stuck
  }
};




// // Add loading screen to render
// if (isProcessing) {
//   return  (
//     <div className="min-h-screen bg-black flex items-center justify-center">
//       <motion.div
//         initial={{ opacity: 0 }}
//         animate={{ opacity: 1 }}
//         className="text-center"
//       >
//         <motion.div
//           className="w-32 h-32 mx-auto mb-8 relative"
//           animate={{ rotate: 360 }}
//           transition={{ duration: 3, repeat: Infinity, ease: "linear" }}
//         >
//           <div className="absolute inset-0 rounded-full border-4 border-neon-blue border-t-transparent animate-spin"></div>
//           <div className="absolute inset-4 rounded-full border-4 border-neon-purple border-b-transparent animate-spin" 
//                style={{ animationDirection: 'reverse', animationDuration: '2s' }}></div>
//           <div className="absolute inset-8 rounded-full bg-gradient-to-br from-neon-blue to-neon-purple flex items-center justify-center">
//             <svg className="w-8 h-8 text-white" fill="currentColor" viewBox="0 0 20 20">
//               <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
//             </svg>
//           </div>
//         </motion.div>

//         <motion.h2 
//           className="text-2xl font-bold text-white mb-4"
//           animate={{ opacity: [0.5, 1, 0.5] }}
//           transition={{ duration: 1.5, repeat: Infinity }}
//         >
//           AI Analysis in Progress
//         </motion.h2>
//         <p className="text-gray-400 mb-8">Processing your interview performance...</p>

//         <div className="space-y-3 text-left max-w-md">
//           {[
//             "Analyzing speech patterns...",
//             "Checking grammar and fluency...",
//             "Evaluating answer relevancy...",
//             "Generating comprehensive report..."
//           ].map((step, index) => (
//             <motion.div
//               key={step}
//               className="flex items-center space-x-3"
//               initial={{ opacity: 0, x: -20 }}
//               animate={{ opacity: 1, x: 0 }}
//               transition={{ delay: index * 0.5, duration: 0.5 }}
//             >
//               <div className="w-2 h-2 bg-neon-blue rounded-full animate-pulse"></div>
//               <span className="text-gray-300 text-sm">{step}</span>
//             </motion.div>
//           ))}
//         </div>
//       </motion.div>
//     </div>
//   );
// }

  const handleViewResults = () => {
    navigate('/results')
  }

    const handlePracticeAgain = () => {
    console.log('🔄 Starting new practice session...')
    
    // Stop camera if running
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop())
    }

    
    // Reset all state
    // setCurrentQuestion(0)
    setSessionStarted(false)
    setShowQuestion(false)
    setShowCompletionModal(false)
    setIsRecording(false)
    setRecordingTime(0)
    setStream(null)
    setCameraReady(false)
    setSavedFiles(0)
    setInterviewData({ answers: [] })
    
    navigate('/interview', { replace: true })
  }

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
  }

  
  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (streamRef.current) {
        streamRef.current.getTracks().forEach(track => track.stop())
      }
    }
  }, [])

// ✅ THIS IS THE FIX: Use a single return with a ternary operator
  return isProcessing ? (
    <LoadingScreen message="Compiling your detailed performance report..." />
  ) : (
     <div className="h-screen bg-black flex flex-col">
      {/* Enhanced Header */}
      <div className="flex-shrink-0 glass-morphism border-b border-neon-blue/20 z-10">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className={`w-3 h-3 rounded-full ${isRecording ? 'bg-red-500 animate-pulse' : 'bg-green-500'}`} />
              <span className="font-semibold">
                {isRecording ? `Recording... ${formatTime(recordingTime)}` : 'Interview in Progress'}
              </span>
              <div className="text-sm bg-neon-blue/20 px-2 py-1 rounded">
                {savedFiles} files saved
              </div>
            </div>
            
              <div className="flex items-center gap-6">
              <ProgressBar current={currentQuestion + 1} total={questions.length} />
              <div className="text-right">
                <div className="text-sm text-gray-400">Question</div>
                <div className="font-bold text-neon-blue">{currentQuestion + 1}/{questions.length}</div>
                </div>
              </div>
          </div>
        </div>
      </div>

      {/* Enhanced Main Content */}
      <div className="flex-1 flex overflow-hidden">
        {/* Live Video Feed */}
        <div className="flex-1 p-6">
          <div className="h-full rounded-2xl overflow-hidden glass-morphism border border-neon-blue/30 relative">
            <video
              ref={videoRef}
              autoPlay
              muted
              playsInline
              key={stream ? stream.id : 'no-stream'} // ✅ ADD THIS LINE
              onCanPlay={() => {
              console.log('📹 Video can play - setting camera ready!');
              setCameraReady(true);
              }}

              onError={(e) => {
                console.error('❌ Video error:', e);
                alert('Camera error. Please check browser permissions.');
              }}
              className="w-full h-full object-cover bg-gray-900"
              style={{ transform: 'scaleX(-1)' }}
            />


            {!cameraReady && (
              <div className="absolute inset-0 flex items-center justify-center bg-gray-900">
                <div className="text-center">
                  <div className="w-16 h-16 border-4 border-neon-blue border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
                  <p className="text-neon-blue">Loading camera...</p>
                </div>
              </div>
            )}

            {isRecording && (
              <div className="absolute top-4 left-4 flex items-center gap-2 bg-red-500/90 px-3 py-1 rounded-full">
                <div className="w-2 h-2 bg-white rounded-full animate-pulse" />
                <span className="text-white text-sm font-medium">REC</span>
              </div>
            )}

            <div className="absolute bottom-6 left-1/2 transform -translate-x-1/2">
              <GlowingButton
                onClick={handleRecordingToggle}
                variant={isRecording ? 'danger' : 'primary'}
                disabled={!cameraReady}
              >
                {isRecording ? 'Stop Recording' : 'Start Recording'}
              </GlowingButton>
            </div>
          </div>
        </div>

        {/* Enhanced Right Panel */}
        <div className="w-96 p-6 flex flex-col">
          {/* AI Avatar */}
          <div className="glass-morphism rounded-2xl p-6 border border-neon-purple/30 mb-6" style={{ minHeight: '200px' }}>
            <AIAvatar isActive={showQuestion} />
          </div>

          {/* Question Section */}
          <div className="flex-1 relative">
          <AnimatePresence mode="wait">
            {showQuestion && questions.length > 0 && (
              <motion.div
                key={currentQuestion}
                className="absolute inset-0 glass-morphism rounded-2xl p-6 border border-neon-blue/30 flex flex-col"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                transition={{ duration: 0.3 }}
              >
                <div className="flex items-center gap-3 mb-4">
                  <div className="w-8 h-8 rounded-full bg-neon-blue/20 border border-neon-blue flex items-center justify-center text-neon-blue font-bold text-sm">
                    {currentQuestion + 1}
                  </div>
                  <h3 className="font-semibold text-lg">Interview Question</h3>
                </div>
                
                <div className="bg-black/40 rounded-xl p-4 mb-6 flex-1 flex items-center">
                  <p className="text-gray-200 leading-relaxed text-lg">
                    {questions[currentQuestion]}
                  </p>
                </div>

                <div className="flex gap-3">
                  <button
                    onClick={handleRepeatQuestion}
                    className="flex-1 px-4 py-3 border border-neon-purple text-neon-purple rounded-lg hover:bg-neon-purple/10 transition-all duration-300 font-semibold"
                  >
                    🔊 Repeat
                  </button>
                  <button
                    onClick={handleNextQuestion}
                    className="flex-1 px-4 py-3 bg-neon-blue text-white rounded-lg hover:brightness-110 transition-all duration-300 font-semibold"
                  >
                    {currentQuestion === questions.length - 1 ? 'Finish' : 'Next →'}
                  </button>
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          </div>
        </div>
      </div>

      {/* Enhanced Completion Modal */}
      {showCompletionModal && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur flex items-center justify-center z-50">
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            className="glass-morphism rounded-2xl p-8 max-w-md mx-4 text-center"
          >
            <div className="w-16 h-16 bg-green-400 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-white" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
              </svg>
            </div>
            <h2 className="text-2xl font-bold mb-2">Interview Complete! 🎉</h2>
            <p className="text-gray-400 mb-2">
              Great job! {savedFiles} WebM recordings have been saved to your backend for evaluation.
            </p>
            <p className="text-sm text-gray-500 mb-6">
              Each question has its own audio file ready for AI analysis.
            </p>
            <div className="space-y-3">
              <GlowingButton onClick={handleViewResults} className="w-full">
                View Results
              </GlowingButton>
              <button
                onClick={handlePracticeAgain}
                className="w-full px-6 py-3 border border-gray-600 text-gray-300 rounded-lg hover:border-neon-blue transition-colors"
              >
                Practice Again
              </button>
            </div>
          </motion.div>
        </div>
      )}
    </div>
  );




  // // ✅ Enhanced main interface with all original features
  // return (
  //   <div className="h-screen bg-black flex flex-col">
  //     {/* Enhanced Header */}
  //     <div className="flex-shrink-0 glass-morphism border-b border-neon-blue/20 z-10">
  //       <div className="container mx-auto px-6 py-4">
  //         <div className="flex items-center justify-between">
  //           <div className="flex items-center gap-4">
  //             <div className={`w-3 h-3 rounded-full ${isRecording ? 'bg-red-500 animate-pulse' : 'bg-green-500'}`} />
  //             <span className="font-semibold">
  //               {isRecording ? `Recording... ${formatTime(recordingTime)}` : 'Interview in Progress'}
  //             </span>
  //             <div className="text-sm bg-neon-blue/20 px-2 py-1 rounded">
  //               {savedFiles} files saved
  //             </div>
  //           </div>
            
  //             <div className="flex items-center gap-6">
  //             <ProgressBar current={currentQuestion + 1} total={questions.length} />
  //             <div className="text-right">
  //               <div className="text-sm text-gray-400">Question</div>
  //               <div className="font-bold text-neon-blue">{currentQuestion + 1}/{questions.length}</div>
  //               </div>
  //             </div>
  //         </div>
  //       </div>
  //     </div>

  //     {/* Enhanced Main Content */}
  //     <div className="flex-1 flex overflow-hidden">
  //       {/* Live Video Feed */}
  //       <div className="flex-1 p-6">
  //         <div className="h-full rounded-2xl overflow-hidden glass-morphism border border-neon-blue/30 relative">
  //           <video
  //             ref={videoRef}
  //             autoPlay
  //             muted
  //             playsInline
  //             key={stream ? stream.id : 'no-stream'} // ✅ ADD THIS LINE
  //             onCanPlay={() => {
  //             console.log('📹 Video can play - setting camera ready!');
  //             setCameraReady(true);
  //             }}

  //             onError={(e) => {
  //               console.error('❌ Video error:', e);
  //               alert('Camera error. Please check browser permissions.');
  //             }}
  //             className="w-full h-full object-cover bg-gray-900"
  //             style={{ transform: 'scaleX(-1)' }}
  //           />


  //           {!cameraReady && (
  //             <div className="absolute inset-0 flex items-center justify-center bg-gray-900">
  //               <div className="text-center">
  //                 <div className="w-16 h-16 border-4 border-neon-blue border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
  //                 <p className="text-neon-blue">Loading camera...</p>
  //               </div>
  //             </div>
  //           )}

  //           {isRecording && (
  //             <div className="absolute top-4 left-4 flex items-center gap-2 bg-red-500/90 px-3 py-1 rounded-full">
  //               <div className="w-2 h-2 bg-white rounded-full animate-pulse" />
  //               <span className="text-white text-sm font-medium">REC</span>
  //             </div>
  //           )}

  //           <div className="absolute bottom-6 left-1/2 transform -translate-x-1/2">
  //             <GlowingButton
  //               onClick={handleRecordingToggle}
  //               variant={isRecording ? 'danger' : 'primary'}
  //               disabled={!cameraReady}
  //             >
  //               {isRecording ? 'Stop Recording' : 'Start Recording'}
  //             </GlowingButton>
  //           </div>
  //         </div>
  //       </div>

  //       {/* Enhanced Right Panel */}
  //       <div className="w-96 p-6 flex flex-col">
  //         {/* AI Avatar */}
  //         <div className="glass-morphism rounded-2xl p-6 border border-neon-purple/30 mb-6" style={{ minHeight: '200px' }}>
  //           <AIAvatar isActive={showQuestion} />
  //         </div>

  //         {/* Question Section */}
  //         <div className="flex-1 relative">
  //         <AnimatePresence mode="wait">
  //           {showQuestion && questions.length > 0 && (
  //             <motion.div
  //               key={currentQuestion}
  //               className="absolute inset-0 glass-morphism rounded-2xl p-6 border border-neon-blue/30 flex flex-col"
  //               initial={{ opacity: 0 }}
  //               animate={{ opacity: 1 }}
  //               exit={{ opacity: 0 }}
  //               transition={{ duration: 0.3 }}
  //             >
  //               <div className="flex items-center gap-3 mb-4">
  //                 <div className="w-8 h-8 rounded-full bg-neon-blue/20 border border-neon-blue flex items-center justify-center text-neon-blue font-bold text-sm">
  //                   {currentQuestion + 1}
  //                 </div>
  //                 <h3 className="font-semibold text-lg">Interview Question</h3>
  //               </div>
                
  //               <div className="bg-black/40 rounded-xl p-4 mb-6 flex-1 flex items-center">
  //                 <p className="text-gray-200 leading-relaxed text-lg">
  //                   {questions[currentQuestion]}
  //                 </p>
  //               </div>

  //               <div className="flex gap-3">
  //                 <button
  //                   onClick={handleRepeatQuestion}
  //                   className="flex-1 px-4 py-3 border border-neon-purple text-neon-purple rounded-lg hover:bg-neon-purple/10 transition-all duration-300 font-semibold"
  //                 >
  //                   🔊 Repeat
  //                 </button>
  //                 <button
  //                   onClick={handleNextQuestion}
  //                   className="flex-1 px-4 py-3 bg-neon-blue text-white rounded-lg hover:brightness-110 transition-all duration-300 font-semibold"
  //                 >
  //                   {currentQuestion === questions.length - 1 ? 'Finish' : 'Next →'}
  //                 </button>
  //               </div>
  //             </motion.div>
  //           )}
  //         </AnimatePresence>

  //         </div>
  //       </div>
  //     </div>

  //     {/* Enhanced Completion Modal */}
  //     {showCompletionModal && (
  //       <div className="fixed inset-0 bg-black/80 backdrop-blur flex items-center justify-center z-50">
  //         <motion.div
  //           initial={{ opacity: 0, scale: 0.9 }}
  //           animate={{ opacity: 1, scale: 1 }}
  //           className="glass-morphism rounded-2xl p-8 max-w-md mx-4 text-center"
  //         >
  //           <div className="w-16 h-16 bg-green-400 rounded-full flex items-center justify-center mx-auto mb-4">
  //             <svg className="w-8 h-8 text-white" fill="currentColor" viewBox="0 0 20 20">
  //               <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
  //             </svg>
  //           </div>
  //           <h2 className="text-2xl font-bold mb-2">Interview Complete! 🎉</h2>
  //           <p className="text-gray-400 mb-2">
  //             Great job! {savedFiles} WebM recordings have been saved to your backend for evaluation.
  //           </p>
  //           <p className="text-sm text-gray-500 mb-6">
  //             Each question has its own audio file ready for AI analysis.
  //           </p>
  //           <div className="space-y-3">
  //             <GlowingButton onClick={handleViewResults} className="w-full">
  //               View Results
  //             </GlowingButton>
  //             <button
  //               onClick={handlePracticeAgain}
  //               className="w-full px-6 py-3 border border-gray-600 text-gray-300 rounded-lg hover:border-neon-blue transition-colors"
  //             >
  //               Practice Again
  //             </button>
  //           </div>
  //         </motion.div>
  //       </div>
  //     )}
  //   </div>
  // )
}




