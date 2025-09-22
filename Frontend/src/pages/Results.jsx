// import { motion } from 'framer-motion'
// import { useState, useEffect } from 'react'
// import { Link } from 'react-router-dom'

// export default function Results() {
//   const [results, setResults] = useState(null)
//   const [loading, setLoading] = useState(true)

//   useEffect(() => {
//     // Get results from localStorage
//     const storedResults = localStorage.getItem('interviewResults')
//     if (storedResults) {
//       setResults(JSON.parse(storedResults))
//       setLoading(false)
//     } else {
//       // Fallback mock data if no stored results
//       setTimeout(() => {
//         setResults({
//           overallScore: 87,
//           sections: {
//             content: 88,
//             delivery: 85,
//             confidence: 89,
//             technical: 86
//           },
//           questionsAnswered: 5,
//           totalQuestions: 5,
//           feedback: [
//             "Excellent communication skills demonstrated",
//             "Strong technical knowledge shown", 
//             "Consider reducing filler words",
//             "Maintain consistent eye contact"
//           ]
//         })
//         setLoading(false)
//       }, 1000)
//     }
//   }, [])

//   if (loading) {
//     return (
//       <div className="min-h-screen bg-black flex items-center justify-center pt-20">
//         <div className="text-center">
//           <div className="w-16 h-16 border-4 border-neon-blue border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
//           <p className="text-xl text-neon-blue">Analyzing your performance...</p>
//         </div>
//       </div>
//     )
//   }

//   return (
//     <div className="min-h-screen bg-black pt-20">
//       <div className="mx-auto max-w-6xl px-4 py-8">
//         {/* Header */}
//         <motion.div
//           initial={{ opacity: 0, y: 20 }}
//           animate={{ opacity: 1, y: 0 }}
//           className="text-center mb-12"
//         >
//           <h1 className="text-4xl font-bold text-gradient mb-4">
//             Interview Results
//           </h1>
//           <p className="text-xl text-neutral-400">
//             Your AI-powered performance analysis
//           </p>
//         </motion.div>

//         {/* Overall Score */}
//         <motion.div
//           initial={{ opacity: 0, scale: 0.9 }}
//           animate={{ opacity: 1, scale: 1 }}
//           transition={{ delay: 0.2 }}
//           className="glass-morphism rounded-2xl p-8 text-center mb-8"
//         >
//           <div className="text-6xl font-bold text-neon-blue mb-4">
//             {results.overallScore}%
//           </div>
//           <div className="text-xl text-neutral-300">Overall Performance</div>
//           <div className="text-sm text-neutral-500 mt-2">
//             {results.questionsAnswered} of {results.totalQuestions} questions completed
//           </div>
//         </motion.div>

//         {/* Section Scores */}
//         <motion.div
//           initial={{ opacity: 0, y: 20 }}
//           animate={{ opacity: 1, y: 0 }}
//           transition={{ delay: 0.4 }}
//           className="grid gap-6 md:grid-cols-2 lg:grid-cols-4 mb-8"
//         >
//         {results.sections && Object.entries(results.sections).map(([section, score], index) => (
//             <div key={section} className="glass-morphism rounded-xl p-6 text-center">
//               <div className="text-3xl font-bold text-neon-purple mb-2">
//                 {score}%
//               </div>
//               <div className="text-sm text-neutral-400 capitalize">
//                 {section.replace(/([A-Z])/g, ' $1')}
//               </div>
//             </div>
//           ))}
//         </motion.div>

//         {/* Feedback */}
//         <motion.div
//           initial={{ opacity: 0, y: 20 }}
//           animate={{ opacity: 1, y: 0 }}
//           transition={{ delay: 0.6 }}
//           className="glass-morphism rounded-2xl p-8 mb-8"
//         >
//           <h2 className="text-2xl font-bold text-neon-blue mb-6">
//             AI Feedback
//           </h2>
//           <div className="space-y-4">
//             {results.feedback && results.feedback.map((item, index) => (
//               <div key={index} className="flex gap-4 p-4 bg-black/40 rounded-lg">
//                 <div className="h-6 w-6 rounded-full bg-neon-blue/20 text-neon-blue flex items-center justify-center text-sm font-bold flex-shrink-0">
//                   {index + 1}
//                 </div>
//                 <div className="text-neutral-300">{item}</div>
//               </div>
//             ))}
//           </div>
//         </motion.div>

//         {/* Actions */}
//         <motion.div
//           initial={{ opacity: 0, y: 20 }}
//           animate={{ opacity: 1, y: 0 }}
//           transition={{ delay: 0.8 }}
//           className="flex flex-col sm:flex-row gap-4 justify-center"
//         >
//           <Link 
//             to="/interview"
//             className="px-8 py-3 bg-neon-blue text-white rounded-lg hover:brightness-110 transition-colors text-center"
//           >
//             Practice Again
//           </Link>
//           <Link 
//             to="/dashboard"
//             className="px-8 py-3 border border-neon-purple text-neon-purple rounded-lg hover:bg-neon-purple/10 transition-colors text-center"
//           >
//             View Dashboard
//           </Link>
//           <Link 
//             to="/"
//             className="px-8 py-3 border border-gray-600 text-gray-300 rounded-lg hover:border-neon-blue transition-colors text-center"
//           >
//             Home
//           </Link>
//         </motion.div>
//       </div>
//     </div>
//   )
// }












// import { useState, useEffect } from 'react';
// import { motion } from 'framer-motion';
// import { useNavigate } from 'react-router-dom';
// import GlowingButton from '../components/ui/GlowingButton';
// import QuestionResult from '../components/results/QuestionResult';
// import OverallResult from '../components/results/OverallResult';

// export default function ResultsPage() {
//   const navigate = useNavigate();
//   const [results, setResults] = useState(null);
//   const [selectedQuestion, setSelectedQuestion] = useState(null);
//   const [overallMetrics, setOverallMetrics] = useState(null);

//   useEffect(() => {
//     // Load results from localStorage
//     const storedResults = localStorage.getItem('interviewAnalysisResults');
//     if (storedResults) {
//       const parsedResults = JSON.parse(storedResults);
//       setResults(parsedResults);
//       calculateOverallMetrics(parsedResults);
//     } else {
//       // If no results found, redirect to home
//       navigate('/');
//     }
//   }, [navigate]);

//   const calculateOverallMetrics = (data) => {
//     const questions = Object.values(data);
//     const totalQuestions = questions.length;
    
//     // Calculate averages
//     const avgFluencyScore = questions.reduce((sum, q) => sum + (q.fluency_score || 0), 0) / totalQuestions;
//     const totalPauses = questions.reduce((sum, q) => sum + (q.pause_count || 0), 0);
//     const totalFillers = questions.reduce((sum, q) => sum + (q.filler_count || 0), 0);
//     const totalGrammarErrors = questions.reduce((sum, q) => sum + (q.grammatical_errors?.length || 0), 0);
    
//     // Relevancy analysis (Questions 2-6)
//     const relevantQuestions = questions.filter(q => q.relevancy_status);
//     const relevantCount = relevantQuestions.filter(q => q.relevancy_status === 'Relevant').length;
    
//     // Overall score calculation
//     const fluencyWeight = 0.4;
//     const relevancyWeight = 0.3;
//     const grammarWeight = 0.2;
//     const pauseWeight = 0.1;
    
//     const fluencyScore = avgFluencyScore * 100;
//     const relevancyScore = relevantQuestions.length > 0 ? (relevantCount / relevantQuestions.length) * 100 : 100;
//     const grammarScore = Math.max(0, 100 - (totalGrammarErrors * 10));
//     const pauseScore = Math.max(0, 100 - (totalPauses * 2));
    
//     const overallScore = Math.round(
//       fluencyScore * fluencyWeight + 
//       relevancyScore * relevancyWeight + 
//       grammarScore * grammarWeight + 
//       pauseScore * pauseWeight
//     );

//     setOverallMetrics({
//       overallScore,
//       avgFluencyScore,
//       totalQuestions,
//       totalPauses,
//       totalFillers,
//       totalGrammarErrors,
//       relevantCount,
//       totalRelevantQuestions: relevantQuestions.length,
//       breakdown: {
//         fluency: fluencyScore,
//         relevancy: relevancyScore,
//         grammar: grammarScore,
//         pause: pauseScore
//       }
//     });
//   };

//   const handleSaveToHistory = () => {
//     // Save to interview history
//     const history = JSON.parse(localStorage.getItem('interviewHistory') || '[]');
//     const newEntry = {
//       id: Date.now(),
//       date: new Date().toISOString(),
//       results: results,
//       overallMetrics: overallMetrics,
//       timestamp: new Date().toLocaleString()
//     };
    
//     history.unshift(newEntry); // Add to beginning
//     localStorage.setItem('interviewHistory', JSON.stringify(history.slice(0, 10))); // Keep only last 10
    
//     alert('Results saved to your interview history!');
//   };

//   if (!results || !overallMetrics) {
//     return (
//       <div className="min-h-screen bg-black flex items-center justify-center">
//         <div className="text-center">
//           <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-neon-blue mx-auto mb-4"></div>
//           <p className="text-white">Loading your results...</p>
//         </div>
//       </div>
//     );
//   }

//   return (
//     <div className="min-h-screen bg-black text-white">
//       {/* Header */}
//       <div className="glass-morphism border-b border-neon-blue/20">
//         <div className="container mx-auto px-6 py-6">
//           <div className="flex justify-between items-center">
//             <h1 className="text-3xl font-bold text-gradient">Interview Analysis Results</h1>
//             <div className="flex gap-3">
//               <GlowingButton onClick={handleSaveToHistory} variant="secondary">
//                 Save to History
//               </GlowingButton>
//               <GlowingButton onClick={() => navigate('/')}>
//                 New Interview
//               </GlowingButton>
//             </div>
//           </div>
//         </div>
//       </div>

//       <div className="container mx-auto px-6 py-8">
//         {/* Overall Results Section */}
//         <motion.div
//           initial={{ opacity: 0, y: 20 }}
//           animate={{ opacity: 1, y: 0 }}
//           className="mb-12"
//         >
//           <OverallResult metrics={overallMetrics} />
//         </motion.div>

//         {/* Question-wise Results */}
//         <motion.div
//           initial={{ opacity: 0, y: 20 }}
//           animate={{ opacity: 1, y: 0 }}
//           transition={{ delay: 0.3 }}
//         >
//           <h2 className="text-2xl font-bold mb-6">Question-wise Analysis</h2>
          
//           <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
//             {/* Questions List */}
//             <div className="lg:col-span-1">
//               <div className="glass-morphism rounded-xl p-4">
//                 <h3 className="text-lg font-semibold mb-4">Questions ({Object.keys(results).length})</h3>
//                 <div className="space-y-2 max-h-96 overflow-y-auto">
//                   {Object.entries(results).map(([key, data], index) => (
//                     <button
//                       key={key}
//                       onClick={() => setSelectedQuestion({ key, data, index: index + 1 })}
//                       className={`w-full text-left p-3 rounded-lg transition-all ${
//                         selectedQuestion?.key === key
//                           ? 'bg-neon-blue/20 border border-neon-blue'
//                           : 'hover:bg-gray-800 border border-transparent'
//                       }`}
//                     >
//                       <div className="flex items-center justify-between">
//                         <span className="font-medium">Question {index + 1}</span>
//                         <div className="flex items-center space-x-2">
//                           <span className={`px-2 py-1 rounded text-xs ${
//                             data.fluency_level === 'Good' ? 'bg-green-500/20 text-green-400' :
//                             data.fluency_level === 'Fair' ? 'bg-yellow-500/20 text-yellow-400' :
//                             'bg-red-500/20 text-red-400'
//                           }`}>
//                             {data.fluency_level}
//                           </span>
//                           {data.relevancy_status && (
//                             <span className={`px-2 py-1 rounded text-xs ${
//                               data.relevancy_status === 'Relevant' 
//                                 ? 'bg-green-500/20 text-green-400' 
//                                 : 'bg-red-500/20 text-red-400'
//                             }`}>
//                               {data.relevancy_status === 'Relevant' ? '✓' : '✗'}
//                             </span>
//                           )}
//                         </div>
//                       </div>
//                       <p className="text-gray-400 text-sm mt-1 truncate">
//                         {data.question}
//                       </p>
//                     </button>
//                   ))}
//                 </div>
//               </div>
//             </div>

//             {/* Question Detail */}
//             <div className="lg:col-span-2">
//               {selectedQuestion ? (
//                 <QuestionResult 
//                   questionData={selectedQuestion.data}
//                   questionNumber={selectedQuestion.index}
//                 />
//               ) : (
//                 <div className="glass-morphism rounded-xl p-8 text-center">
//                   <div className="text-gray-400">
//                     <svg className="w-16 h-16 mx-auto mb-4 opacity-50" fill="currentColor" viewBox="0 0 20 20">
//                       <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
//                     </svg>
//                     <p>Select a question to view detailed analysis</p>
//                   </div>
//                 </div>
//               )}
//             </div>
//           </div>
//         </motion.div>
//       </div>
//     </div>
//   );
// }






















// import { useState, useEffect } from 'react';
// import { motion } from 'framer-motion';
// import { useNavigate } from 'react-router-dom';
// import GlowingButton from '../components/ui/GlowingButton';
// import OverallResult from '../components/results/OverallResult';
// import QuestionResult from '../components/results/QuestionResult';

// export default function Results() {
//   const navigate = useNavigate();
//   const [resultsData, setResultsData] = useState(null);
//   const [overallMetrics, setOverallMetrics] = useState(null);
//   const [activeQuestion, setActiveQuestion] = useState(null);

//   useEffect(() => {
//     const data = localStorage.getItem('interviewAnalysisResults');
//     if (data) {
//       const parsedData = JSON.parse(data);
//       setResultsData(parsedData);
//       calculateOverallMetrics(parsedData);
//     } else {
//       navigate('/');
//     }
//   }, [navigate]);
  
//   const calculateOverallMetrics = (data) => {
//     const questions = Object.values(data);
//     if (questions.length === 0) return;
    
//     const avgFluency = questions.reduce((sum, q) => sum + (q.fluency_score || 0), 0) / questions.length;
//     const totalGrammarErrors = questions.reduce((sum, q) => sum + (q.grammatical_errors?.length || 0), 0);
    
//     const relevantQs = questions.filter(q => q.relevancy_status);
//     const relevantCount = relevantQs.filter(q => q.relevancy_status === 'Relevant').length;
//     const relevancyScore = relevantQs.length > 0 ? (relevantCount / relevantQs.length) * 100 : 100;
    
//     const fluencyScore = avgFluency * 100;
//     const grammarScore = Math.max(0, 100 - (totalGrammarErrors * 10));
    
//     const overallScore = Math.round((fluencyScore * 0.5) + (relevancyScore * 0.3) + (grammarScore * 0.2));

//     setOverallMetrics({
//       overallScore,
//       totalQuestions: questions.length,
//       totalGrammarErrors,
//       breakdown: {
//         fluency: fluencyScore,
//         relevancy: relevancyScore,
//         grammar: grammarScore
//       }
//     });
//   };

//   const handleSaveToHistory = () => {
//     const history = JSON.parse(localStorage.getItem('interviewHistory') || '[]');
//     const newEntry = {
//       id: `interview-${Date.now()}`,
//       date: new Date().toISOString(),
//       overallScore: overallMetrics.overallScore,
//       resultsData: resultsData
//     };
//     history.unshift(newEntry);
//     localStorage.setItem('interviewHistory', JSON.stringify(history.slice(0, 5))); // Keep last 5
//     alert('Results saved to your history!');
//   };

//   if (!resultsData || !overallMetrics) return <div>Loading...</div>;

//   return (
//     <div className="min-h-screen bg-black text-white p-4 md:p-8">
//       <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }}>
//         <div className="max-w-5xl mx-auto">
//           <div className="flex justify-between items-center mb-8">
//             <h1 className="text-3xl font-bold text-gradient">Interview Report</h1>
//             <div className="flex gap-4">
//               <GlowingButton onClick={handleSaveToHistory} variant="secondary">Save</GlowingButton>
//               <GlowingButton onClick={() => navigate('/upload-resume')}>Practice Again</GlowingButton>
//             </div>
//           </div>
//           <OverallResult metrics={overallMetrics} />

//           <h2 className="text-2xl font-bold mt-12 mb-6">Detailed Analysis</h2>
//           <div className="space-y-4">
//             {Object.entries(resultsData).map(([key, data], index) => (
//               <div key={key} className="glass-morphism rounded-xl p-4">
//                 <button 
//                   className="w-full text-left flex justify-between items-center"
//                   onClick={() => setActiveQuestion(activeQuestion === key ? null : key)}
//                 >
//                   <span className="font-semibold text-lg">Question {index + 1}</span>
//                   <span className={`transform transition-transform ${activeQuestion === key ? 'rotate-180' : ''}`}>▼</span>
//                 </button>
//                 {activeQuestion === key && <QuestionResult questionData={data} questionNumber={index + 1} />}
//               </div>
//             ))}
//           </div>
//         </div>
//       </motion.div>
//     </div>
//   );
// }


// import { useState, useEffect } from 'react';
// import { motion } from 'framer-motion';
// import { useNavigate } from 'react-router-dom';
// import GlowingButton from '../components/ui/GlowingButton';
// import OverallScoreCircle from '../components/results/OverallScoreCircle'; // ✅ IMPORT THE NEW COMPONENT
// import QuestionResult from '../components/results/QuestionResult';

// export default function Results() {
//   const navigate = useNavigate();
//   const [resultsData, setResultsData] = useState(null);
//   const [overallMetrics, setOverallMetrics] = useState(null);
//   const [activeQuestion, setActiveQuestion] = useState(null);

//   useEffect(() => {
//     const data = localStorage.getItem('interviewAnalysisResults');
//     if (data) {
//       const parsedData = JSON.parse(data);
//       setResultsData(parsedData);
//       calculateOverallMetrics(parsedData);
//       // Automatically open the first question for a better user experience
//       if (Object.keys(parsedData).length > 0) {
//         setActiveQuestion(Object.keys(parsedData)[0]);
//       }
//     } else {
//       navigate('/');
//     }
//   }, [navigate]);
  
//   const calculateOverallMetrics = (data) => {
//     const questions = Object.values(data);
//     if (questions.length === 0) return;
    
//     const avgFluency = questions.reduce((sum, q) => sum + (q.fluency_score || 0), 0) / questions.length;
    
//     // Correctly count grammar errors, ignoring the API quota error objects
//     const totalGrammarErrors = questions.reduce((sum, q) => {
//       const validErrors = q.grammatical_errors?.filter(err => err.type !== "Unexpected Error") || [];
//       return sum + validErrors.length;
//     }, 0);
    
//     // Only consider questions where relevancy was successfully determined
//     const relevantQs = questions.filter(q => q.relevancy_status && q.relevancy_status !== 'Error');
//     const relevantCount = relevantQs.filter(q => q.relevancy_status === 'Relevant').length;
//     const relevancyScore = relevantQs.length > 0 ? (relevantCount / relevantQs.length) * 100 : 100;
    
//     const fluencyScore = avgFluency * 100;
//     // Make grammar penalty less harsh
//     const grammarScore = Math.max(0, 100 - (totalGrammarErrors * 5));
    
//     const overallScore = Math.round((fluencyScore * 0.5) + (relevancyScore * 0.3) + (grammarScore * 0.2));

//     setOverallMetrics({
//       overallScore,
//       totalQuestions: questions.length,
//       avgFluency: Math.round(fluencyScore),
//       relevancy: Math.round(relevancyScore),
//       grammarErrors: totalGrammarErrors
//     });
//   };

//   const handleSaveToHistory = () => {
//     const history = JSON.parse(localStorage.getItem('interviewHistory') || '[]');
//     const newEntry = {
//       id: `interview-${Date.now()}`,
//       date: new Date().toISOString(),
//       overallScore: overallMetrics.overallScore,
//       resultsData: resultsData
//     };
//     history.unshift(newEntry);
//     localStorage.setItem('interviewHistory', JSON.stringify(history.slice(0, 5)));
//     alert('Results saved to your history!');
//   };

//   if (!resultsData || !overallMetrics) return <div className="bg-black min-h-screen text-white flex items-center justify-center">Loading Report...</div>;

//   return (
//     // ✅ FIX 1: Added pt-24 to push content below the navbar
//     <div className="min-h-screen bg-black text-white pt-24 px-4 md:px-8 pb-12">
//       <motion.div 
//         className="max-w-6xl mx-auto"
//         initial={{ opacity: 0, y: 20 }}
//         animate={{ opacity: 1, y: 0 }}
//       >
//         <div className="flex justify-between items-center mb-8">
//             <h1 className="text-4xl font-bold text-gradient">Interview Report</h1>
//             <div className="flex gap-4">
//               <GlowingButton onClick={handleSaveToHistory} variant="secondary">Save</GlowingButton>
//               <GlowingButton onClick={() => navigate('/upload-resume')}>Practice Again</GlowingButton>
//             </div>
//         </div>
        
//         {/* ✅ FIX 2 & 3: New Overall Performance Layout */}
//         <div className="glass-morphism rounded-2xl p-6 md:p-8 mb-12">
//             <div className="flex flex-col md:flex-row items-center justify-around gap-8">
//                 <OverallScoreCircle score={overallMetrics.overallScore} />
//                 <div className="grid grid-cols-2 gap-x-8 gap-y-6 w-full md:w-auto">
//                     <div className="text-center">
//                         <div className="text-3xl font-bold text-neon-blue">{overallMetrics.totalQuestions}</div>
//                         <div className="text-sm text-gray-400">Questions</div>
//                     </div>
//                     <div className="text-center">
//                         <div className="text-3xl font-bold text-yellow-400">{overallMetrics.relevancy}%</div>
//                         <div className="text-sm text-gray-400">Relevancy</div>
//                     </div>
//                     <div className="text-center">
//                         <div className="text-3xl font-bold text-green-400">{overallMetrics.avgFluency}%</div>
//                         <div className="text-sm text-gray-400">Avg. Fluency</div>
//                     </div>
//                     <div className="text-center">
//                         <div className="text-3xl font-bold text-red-400">{overallMetrics.grammarErrors}</div>
//                         <div className="text-sm text-gray-400">Grammar Errors</div>
//                     </div>
//                 </div>
//             </div>
//         </div>

//         {/* Detailed Analysis Section */}
//         <h2 className="text-3xl font-bold text-gradient mb-6 text-center">Detailed Question Analysis</h2>
//         <div className="space-y-4">
//           {Object.entries(resultsData).map(([key, data], index) => (
//             <div key={key} className="glass-morphism rounded-xl overflow-hidden transition-all duration-300">
//               <button 
//                 className="w-full text-left flex justify-between items-center p-5 hover:bg-gray-800/50"
//                 onClick={() => setActiveQuestion(activeQuestion === key ? null : key)}
//               >
//                 <div className="flex items-center gap-4">
//                     <span className="font-bold text-lg text-neon-blue">Q{index + 1}</span>
//                     <p className="font-semibold text-gray-200">{data.question}</p>
//                 </div>
//                 <motion.span 
//                     className="text-2xl text-gray-500"
//                     animate={{ rotate: activeQuestion === key ? 180 : 0 }}
//                 >
//                     ▼
//                 </motion.span>
//               </button>
//               {activeQuestion === key && <div className="p-5 pt-0"><QuestionResult questionData={data} /></div>}
//             </div>
//           ))}
//         </div>
//       </motion.div>
//     </div>
//   );
// }




import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import GlowingButton from '../components/ui/GlowingButton';
import OverallScoreCircle from '../components/results/OverallScoreCircle';
import QuestionResult from '../components/results/QuestionResult';

export default function Results() {
  const navigate = useNavigate();
  const [resultsData, setResultsData] = useState(null);
  const [overallMetrics, setOverallMetrics] = useState(null);
  const [activeQuestion, setActiveQuestion] = useState(null);

  useEffect(() => {
    const data = localStorage.getItem('interviewAnalysisResults');
    if (data) {
      const parsedData = JSON.parse(data);
      setResultsData(parsedData);
      calculateOverallMetrics(parsedData);
      if (Object.keys(parsedData).length > 0) {
        // Correctly sort and get the first question key
        const firstQuestionKey = Object.keys(parsedData).sort((a, b) => parseInt(a.split(' ')[1]) - parseInt(b.split(' ')[1]))[0];
        setActiveQuestion(firstQuestionKey);
      }
    } else {
      navigate('/');
    }
  }, [navigate]);
  
  const calculateOverallMetrics = (data) => {
    const questions = Object.values(data);
    if (questions.length === 0) return;
    
    const avgFluency = questions.reduce((sum, q) => sum + (q.fluency_score || 0), 0) / questions.length;
    
    const totalGrammarErrors = questions.reduce((sum, q) => {
      const validErrors = q.grammatical_errors?.filter(err => err.type !== "Unexpected Error") || [];
      return sum + validErrors.length;
    }, 0);
    
    const relevantQs = questions.filter(q => q.relevancy_status && q.relevancy_status !== 'Error');
    const relevantCount = relevantQs.filter(q => q.relevancy_status === 'Relevant').length;
    const relevancyScore = relevantQs.length > 0 ? (relevantCount / relevantQs.length) * 100 : 100;
    
    const fluencyScore = avgFluency * 100;
    const grammarScore = Math.max(0, 100 - (totalGrammarErrors * 5));
    
    const overallScore = Math.round((fluencyScore * 0.5) + (relevancyScore * 0.3) + (grammarScore * 0.2));

    setOverallMetrics({
      overallScore,
      totalQuestions: questions.length,
      avgFluency: Math.round(fluencyScore),
      relevancy: Math.round(relevancyScore),
      grammarErrors: totalGrammarErrors
    });
  };

  const handleSaveToHistory = () => {
    // This function remains unchanged
    const history = JSON.parse(localStorage.getItem('interviewHistory') || '[]');
    const newEntry = {
      id: `interview-${Date.now()}`,
      date: new Date().toISOString(),
      overallScore: overallMetrics.overallScore,
      resultsData: resultsData
    };
    history.unshift(newEntry);
    localStorage.setItem('interviewHistory', JSON.stringify(history.slice(0, 5)));
    alert('Results saved to your history!');
  };

  if (!resultsData || !overallMetrics) return <div className="bg-black min-h-screen text-white flex items-center justify-center">Loading Report...</div>;

  // ✅ FIX: Sort the questions numerically before rendering
  const sortedQuestions = Object.entries(resultsData).sort((a, b) => {
    const aNum = parseInt(a[0].replace('Question ', ''));
    const bNum = parseInt(b[0].replace('Question ', ''));
    return aNum - bNum;
  });

  return (
    <div className="min-h-screen bg-black text-white pt-24 px-4 md:px-8 pb-12">
      <motion.div 
        className="max-w-6xl mx-auto"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <div className="flex justify-between items-center mb-8">
            <h1 className="text-4xl font-bold text-gradient">Interview Report</h1>
            <div className="flex gap-4">
              <GlowingButton onClick={handleSaveToHistory} variant="secondary">Save</GlowingButton>
              <GlowingButton onClick={() => navigate('/upload-resume')}>Practice Again</GlowingButton>
            </div>
        </div>
        
        <div className="glass-morphism rounded-2xl p-6 md:p-8 mb-12">
            <div className="flex flex-col md:flex-row items-center justify-around gap-8">
                <OverallScoreCircle score={overallMetrics.overallScore} />
                <div className="grid grid-cols-2 gap-x-8 gap-y-6 w-full md:w-auto">
                    <div className="text-center"><div className="text-3xl font-bold text-neon-blue">{overallMetrics.totalQuestions}</div><div className="text-sm text-gray-400">Questions</div></div>
                    <div className="text-center"><div className="text-3xl font-bold text-yellow-400">{overallMetrics.relevancy}%</div><div className="text-sm text-gray-400">Relevancy</div></div>
                    <div className="text-center"><div className="text-3xl font-bold text-green-400">{overallMetrics.avgFluency}%</div><div className="text-sm text-gray-400">Avg. Fluency</div></div>
                    <div className="text-center"><div className="text-3xl font-bold text-red-400">{overallMetrics.grammarErrors}</div><div className="text-sm text-gray-400">Grammar Errors</div></div>
                </div>
            </div>
        </div>

        <h2 className="text-3xl font-bold text-gradient mb-6 text-center">Detailed Question Analysis</h2>
        <div className="space-y-4">
          {/* ✅ Use the new sortedQuestions array to map */}
          {sortedQuestions.map(([key, data], index) => (
            <div key={key} className="glass-morphism rounded-xl overflow-hidden transition-all duration-300">
              <button 
                className="w-full text-left flex justify-between items-center p-5 hover:bg-gray-800/50"
                onClick={() => setActiveQuestion(activeQuestion === key ? null : key)}
              >
                <div className="flex items-center gap-4">
                    <span className="font-bold text-lg text-neon-blue">Q{index + 1}</span>
                    <p className="font-semibold text-gray-200">{data.question}</p>
                </div>
                <motion.span 
                    className="text-2xl text-gray-500"
                    animate={{ rotate: activeQuestion === key ? 180 : 0 }}
                >
                    ▼
                </motion.span>
              </button>
              {activeQuestion === key && <div className="p-5 pt-0"><QuestionResult questionData={data} /></div>}
            </div>
          ))}
        </div>
      </motion.div>
    </div>
  );
}
