// import { motion } from 'framer-motion';

// export default function QuestionResult({ questionData, questionNumber }) {
//   const getScoreColor = (score) => {
//     if (score >= 0.7) return 'text-green-400';
//     if (score >= 0.5) return 'text-yellow-400';
//     return 'text-red-400';
//   };

//   return (
//     <motion.div
//       key={questionNumber}
//       className="glass-morphism rounded-xl p-6"
//       initial={{ opacity: 0, x: 20 }}
//       animate={{ opacity: 1, x: 0 }}
//     >
//       <div className="mb-6">
//         <h3 className="text-xl font-bold mb-2">Question {questionNumber}</h3>
//         <p className="text-gray-300 bg-gray-800/50 p-4 rounded-lg">
//           {questionData.question}
//         </p>
//       </div>

//       {/* Fluency Score Visualization */}
//       <div className="mb-6">
//         <h4 className="text-lg font-semibold mb-3">Fluency Analysis</h4>
//         <div className="flex items-center space-x-4 mb-4">
//           <div className="flex-1">
//             <div className="flex justify-between text-sm mb-1">
//               <span>Fluency Score</span>
//               <span className={getScoreColor(questionData.fluency_score)}>
//                 {Math.round(questionData.fluency_score * 100)}%
//               </span>
//             </div>
//             <div className="w-full bg-gray-700 rounded-full h-3">
//               <motion.div
//                 className={`h-3 rounded-full ${
//                   questionData.fluency_score >= 0.7 ? 'bg-green-500' :
//                   questionData.fluency_score >= 0.5 ? 'bg-yellow-500' :
//                   'bg-red-500'
//                 }`}
//                 initial={{ width: 0 }}
//                 animate={{ width: `${questionData.fluency_score * 100}%` }}
//                 transition={{ duration: 1 }}
//               />
//             </div>
//           </div>
//           <span className={`px-3 py-1 rounded-lg text-sm font-medium ${
//             questionData.fluency_level === 'Good' ? 'bg-green-500/20 text-green-400' :
//             questionData.fluency_level === 'Fair' ? 'bg-yellow-500/20 text-yellow-400' :
//             'bg-red-500/20 text-red-400'
//           }`}>
//             {questionData.fluency_level}
//           </span>
//         </div>

//         {/* Metrics Grid */}
//         <div className="grid grid-cols-3 gap-4">
//           <div className="bg-gray-800/50 rounded-lg p-3 text-center">
//             <div className="text-2xl font-bold text-yellow-400">{questionData.pause_count}</div>
//             <div className="text-gray-400 text-sm">Pauses</div>
//             <div className="text-xs text-gray-500">{questionData.total_pause_time}s total</div>
//           </div>
//           <div className="bg-gray-800/50 rounded-lg p-3 text-center">
//             <div className="text-2xl font-bold text-purple-400">{questionData.filler_count}</div>
//             <div className="text-gray-400 text-sm">Fillers</div>
//             <div className="text-xs text-gray-500">
//               {questionData.filler_words?.join(', ') || 'None'}
//             </div>
//           </div>
//           <div className="bg-gray-800/50 rounded-lg p-3 text-center">
//             <div className="text-2xl font-bold text-red-400">
//               {questionData.grammatical_errors?.length || 0}
//             </div>
//             <div className="text-gray-400 text-sm">Grammar Errors</div>
//           </div>
//         </div>
//       </div>

//       {/* Answer Transcript */}
//       <div className="mb-6">
//         <h4 className="text-lg font-semibold mb-3">Your Response</h4>
//         <div className="bg-gray-800/30 p-4 rounded-lg">
//           <p className="text-gray-300 leading-relaxed">
//             {questionData.answer_transcript}
//           </p>
//         </div>
//       </div>

//       {/* Grammar Errors */}
//       {questionData.grammatical_errors && questionData.grammatical_errors.length > 0 && (
//         <div className="mb-6">
//           <h4 className="text-lg font-semibold mb-3 text-red-400">Grammar Issues</h4>
//           <div className="space-y-2">
//             {questionData.grammatical_errors.map((error, index) => (
//               <div key={index} className="bg-red-500/10 border border-red-500/20 rounded-lg p-3">
//                 <p className="text-red-400 font-medium">{error.context}</p>
//                 <p className="text-gray-400 text-sm mt-1">
//                   <span className="font-medium">Suggestion:</span> {error.suggestion}
//                 </p>
//               </div>
//             ))}
//           </div>
//         </div>
//       )}

//       {/* Relevancy Analysis */}
//       {questionData.relevancy_status && (
//         <div className="mb-6">
//           <h4 className="text-lg font-semibold mb-3">Relevancy Analysis</h4>
//           <div className={`p-4 rounded-lg border ${
//             questionData.relevancy_status === 'Relevant' 
//               ? 'bg-green-500/10 border-green-500/20' 
//               : 'bg-red-500/10 border-red-500/20'
//           }`}>
//             <div className="flex items-center space-x-2 mb-2">
//               <span className={`px-2 py-1 rounded text-sm font-medium ${
//                 questionData.relevancy_status === 'Relevant' 
//                   ? 'bg-green-500/20 text-green-400' 
//                   : 'bg-red-500/20 text-red-400'
//               }`}>
//                 {questionData.relevancy_status}
//               </span>
//             </div>
//             <p className="text-gray-300">{questionData.reasoning}</p>
//           </div>
//         </div>
//       )}
//     </motion.div>
//   );
// }




// import { motion } from 'framer-motion';

// export default function QuestionResult({ questionData, questionNumber }) {
//   const getScoreColor = (score, isPercent = true) => {
//     const s = isPercent ? score : score * 100;
//     if (s >= 70) return 'text-green-400';
//     if (s >= 50) return 'text-yellow-400';
//     return 'text-red-400';
//   };

//   return (
//     <motion.div
//       key={questionNumber}
//       initial={{ opacity: 0, height: 0 }}
//       animate={{ opacity: 1, height: 'auto' }}
//       className="mt-4 pt-4 border-t border-neon-blue/20"
//     >
//       <div className="space-y-4">
//         <div>
//           <h4 className="font-semibold text-gray-300 mb-2">Your Answer:</h4>
//           <p className="text-gray-400 bg-gray-900/50 p-3 rounded-md text-sm leading-relaxed">{questionData.answer_transcript}</p>
//         </div>

//         <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
//           <div className="bg-gray-900/50 p-3 rounded-md text-center">
//             <div className="text-xs text-gray-400">Fluency Score</div>
//             <div className={`text-xl font-bold ${getScoreColor(questionData.fluency_score, false)}`}>{Math.round(questionData.fluency_score * 100)}%</div>
//           </div>
//           <div className="bg-gray-900/50 p-3 rounded-md text-center">
//             <div className="text-xs text-gray-400">Pauses</div>
//             <div className="text-xl font-bold text-yellow-400">{questionData.pause_count}</div>
//           </div>
//           <div className="bg-gray-900/50 p-3 rounded-md text-center">
//             <div className="text-xs text-gray-400">Filler Words</div>
//             <div className="text-xl font-bold text-purple-400">{questionData.filler_count}</div>
//           </div>
//         </div>

//         {questionData.relevancy_status && (
//           <div>
//             <h4 className="font-semibold text-gray-300 mb-2">Relevancy:</h4>
//             <div className={`p-3 rounded-md border text-sm ${questionData.relevancy_status === 'Relevant' ? 'bg-green-500/10 border-green-500/30 text-green-300' : 'bg-red-500/10 border-red-500/30 text-red-300'}`}>
//               <strong className="mr-2">{questionData.relevancy_status}.</strong>{questionData.reasoning}
//             </div>
//           </div>
//         )}

//         {questionData.grammatical_errors?.length > 0 && (
//            <div>
//             <h4 className="font-semibold text-gray-300 mb-2">Grammar Feedback:</h4>
//             {questionData.grammatical_errors.map((error, i) => (
//               <div key={i} className="bg-red-500/10 border border-red-500/20 p-3 rounded-md text-sm">
//                 <p className="text-red-400">"{error.context}"</p>
//                 <p className="text-gray-400 mt-1">Suggestion: <span className="text-green-400">"{error.suggestion}"</span></p>
//               </div>
//             ))}
//           </div>
//         )}
//       </div>
//     </motion.div>
//   );
// }


import React from 'react';
import { motion } from 'framer-motion';

export default function QuestionResult({ questionData }) {
  // Helper to format filler words for display
  const formatFillerWords = (words) => {
    if (!words || words.length === 0) return 'None';
    // Count occurrences of each word
    const wordCounts = words.reduce((acc, word) => {
      const lowerWord = word.toLowerCase();
      acc[lowerWord] = (acc[lowerWord] || 0) + 1;
      return acc;
    }, {});
    // Create a string like "Uh (2), Um (1)"
    return Object.entries(wordCounts)
      .map(([word, count]) => `${word.charAt(0).toUpperCase() + word.slice(1)}${count > 1 ? ` (${count})` : ''}`)
      .join(', ');
  };

  const hasGrammarErrors = questionData.grammatical_errors?.some(err => err.type !== "Unexpected Error");

  return (
    <motion.div
      initial={{ opacity: 0, height: 0 }}
      animate={{ opacity: 1, height: 'auto' }}
      exit={{ opacity: 0, height: 0 }}
      className="overflow-hidden"
    >
      <div className="space-y-6">
        {/* Section 1: Your Answer */}
        <div>
          <h4 className="font-semibold text-gray-300 mb-2">Your Answer</h4>
          <p className="text-gray-400 bg-gray-900/50 p-3 rounded-md text-sm leading-relaxed">
            {questionData.answer_transcript}
          </p>
        </div>

        {/* Section 2: Fluency & Speech Analysis */}
        <div>
          <h4 className="font-semibold text-gray-300 mb-2">Fluency & Speech Analysis</h4>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-gray-900/50 p-3 rounded-md text-center">
              <div className="text-xs text-gray-400">Fluency Score</div>
              <div className="text-2xl font-bold" style={{ color: questionData.fluency_level === 'Excellent' ? '#22c55e' : questionData.fluency_level === 'Good' ? '#a3e635' : questionData.fluency_level === 'Fair' ? '#facc15' : '#ef4444' }}>
                {Math.round(questionData.fluency_score * 100)}%
              </div>
            </div>
            <div className="bg-gray-900/50 p-3 rounded-md text-center">
              <div className="text-xs text-gray-400">Fluency Level</div>
              <div className="text-lg font-semibold text-gray-200 mt-2">{questionData.fluency_level}</div>
            </div>
            <div className="bg-gray-900/50 p-3 rounded-md text-center">
              <div className="text-xs text-gray-400">Pauses</div>
              <div className="text-2xl font-bold text-yellow-400">{questionData.pause_count}</div>
              <div className="text-xs text-gray-500">{questionData.total_pause_time.toFixed(1)}s total</div>
            </div>
            <div className="bg-gray-900/50 p-3 rounded-md text-center">
              <div className="text-xs text-gray-400">Filler Words</div>
              <div className="text-2xl font-bold text-purple-400">{questionData.filler_count}</div>
              <div className="text-xs text-gray-500 truncate">{formatFillerWords(questionData.filler_words)}</div>
            </div>
          </div>
        </div>
        
        {/* Section 3: Content Analysis */}
        <div>
          <h4 className="font-semibold text-gray-300 mb-2">Content Analysis</h4>
          <div className="space-y-4">
            {/* Relevancy */}
            {questionData.relevancy_status && (
              <div className={`p-3 rounded-md border text-sm ${questionData.relevancy_status === 'Relevant' ? 'bg-green-500/10 border-green-500/30 text-green-300' : 'bg-red-500/10 border-red-500/30 text-red-300'}`}>
                <strong className="mr-2">Relevancy: {questionData.relevancy_status}.</strong>
                {questionData.reasoning}
              </div>
            )}
            {/* Grammar */}
            {hasGrammarErrors ? (
              <div>
                <h5 className="font-medium text-red-400 mb-2">Grammar Feedback:</h5>
                {questionData.grammatical_errors.filter(err => err.type !== "Unexpected Error").map((error, i) => (
                  <div key={i} className="bg-red-900/30 border border-red-500/20 p-3 rounded-md text-sm mt-2">
                    <p className="text-red-300">"{error.context}"</p>
                    <p className="text-gray-300 mt-1">Suggestion: <span className="text-green-400">"{error.suggestion}"</span></p>
                  </div>
                ))}
              </div>
            ) : (
                <div className="p-3 rounded-md border bg-green-500/10 border-green-500/30 text-green-300 text-sm">
                    <strong>Grammar:</strong> No errors detected. Great job!
                </div>
            )}
          </div>
        </div>
      </div>
    </motion.div>
  );
}
