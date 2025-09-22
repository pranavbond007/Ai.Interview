// import { motion } from 'framer-motion';

// export default function OverallResult({ metrics }) {
//   const getScoreColor = (score) => {
//     if (score >= 80) return 'text-green-400';
//     if (score >= 60) return 'text-yellow-400';
//     return 'text-red-400';
//   };

//   const getScoreGradient = (score) => {
//     if (score >= 80) return 'from-green-500 to-green-600';
//     if (score >= 60) return 'from-yellow-500 to-yellow-600';
//     return 'from-red-500 to-red-600';
//   };

//   return (
//     <div className="glass-morphism rounded-2xl p-8">
//       <h2 className="text-2xl font-bold mb-8 text-center">Overall Performance</h2>
      
//       {/* Main Score Circle */}
//       <div className="flex justify-center mb-8">
//         <div className="relative">
//           <svg className="w-40 h-40 transform -rotate-90" viewBox="0 0 144 144">
//             <circle
//               cx="72"
//               cy="72"
//               r="60"
//               className="fill-none stroke-gray-700"
//               strokeWidth="8"
//             />
//             <motion.circle
//               cx="72"
//               cy="72"
//               r="60"
//               className={`fill-none stroke-2 bg-gradient-to-r ${getScoreGradient(metrics.overallScore)}`}
//               strokeWidth="8"
//               strokeDasharray="377"
//               strokeDashoffset={377 - (377 * metrics.overallScore) / 100}
//               strokeLinecap="round"
//               initial={{ strokeDashoffset: 377 }}
//               animate={{ strokeDashoffset: 377 - (377 * metrics.overallScore) / 100 }}
//               transition={{ duration: 2, ease: "easeOut" }}
//               style={{
//                 stroke: `url(#gradient-${metrics.overallScore >= 80 ? 'green' : metrics.overallScore >= 60 ? 'yellow' : 'red'})`
//               }}
//             />
//             <defs>
//               <linearGradient id="gradient-green" x1="0%" y1="0%" x2="100%" y2="0%">
//                 <stop offset="0%" stopColor="#10b981" />
//                 <stop offset="100%" stopColor="#059669" />
//               </linearGradient>
//               <linearGradient id="gradient-yellow" x1="0%" y1="0%" x2="100%" y2="0%">
//                 <stop offset="0%" stopColor="#f59e0b" />
//                 <stop offset="100%" stopColor="#d97706" />
//               </linearGradient>
//               <linearGradient id="gradient-red" x1="0%" y1="0%" x2="100%" y2="0%">
//                 <stop offset="0%" stopColor="#ef4444" />
//                 <stop offset="100%" stopColor="#dc2626" />
//               </linearGradient>
//             </defs>
//           </svg>
//           <div className="absolute inset-0 flex items-center justify-center">
//             <div className="text-center">
//               <motion.div
//                 className={`text-4xl font-bold ${getScoreColor(metrics.overallScore)}`}
//                 initial={{ opacity: 0, scale: 0.5 }}
//                 animate={{ opacity: 1, scale: 1 }}
//                 transition={{ delay: 1, duration: 0.5 }}
//               >
//                 {metrics.overallScore}
//               </motion.div>
//               <div className="text-gray-400 text-sm">Overall Score</div>
//             </div>
//           </div>
//         </div>
//       </div>

//       {/* Score Breakdown */}
//       <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-8">
//         {[
//           { label: 'Fluency', value: Math.round(metrics.breakdown.fluency), icon: '🗣️' },
//           { label: 'Relevancy', value: Math.round(metrics.breakdown.relevancy), icon: '🎯' },
//           { label: 'Grammar', value: Math.round(metrics.breakdown.grammar), icon: '📝' },
//           { label: 'Pace', value: Math.round(metrics.breakdown.pause), icon: '⏱️' }
//         ].map((item, index) => (
//           <motion.div
//             key={item.label}
//             className="text-center p-4 bg-gray-800/50 rounded-lg"
//             initial={{ opacity: 0, y: 20 }}
//             animate={{ opacity: 1, y: 0 }}
//             transition={{ delay: index * 0.1 }}
//           >
//             <div className="text-2xl mb-2">{item.icon}</div>
//             <div className={`text-2xl font-bold ${getScoreColor(item.value)}`}>
//               {item.value}
//             </div>
//             <div className="text-gray-400 text-sm">{item.label}</div>
//           </motion.div>
//         ))}
//       </div>

//       {/* Statistics */}
//       <div className="grid grid-cols-2 md:grid-cols-5 gap-4 text-center">
//         <div className="bg-gray-800/30 rounded-lg p-3">
//           <div className="text-xl font-bold text-neon-blue">{metrics.totalQuestions}</div>
//           <div className="text-gray-400 text-sm">Questions</div>
//         </div>
//         <div className="bg-gray-800/30 rounded-lg p-3">
//           <div className="text-xl font-bold text-yellow-400">{metrics.totalPauses}</div>
//           <div className="text-gray-400 text-sm">Total Pauses</div>
//         </div>
//         <div className="bg-gray-800/30 rounded-lg p-3">
//           <div className="text-xl font-bold text-purple-400">{metrics.totalFillers}</div>
//           <div className="text-gray-400 text-sm">Filler Words</div>
//         </div>
//         <div className="bg-gray-800/30 rounded-lg p-3">
//           <div className="text-xl font-bold text-red-400">{metrics.totalGrammarErrors}</div>
//           <div className="text-gray-400 text-sm">Grammar Errors</div>
//         </div>
//         <div className="bg-gray-800/30 rounded-lg p-3">
//           <div className="text-xl font-bold text-green-400">
//             {metrics.relevantCount}/{metrics.totalRelevantQuestions}
//           </div>
//           <div className="text-gray-400 text-sm">Relevant Answers</div>
//         </div>
//       </div>
//     </div>
//   );
// }



import { motion } from 'framer-motion';

export default function OverallResult({ metrics }) {
  const getScoreColor = (score) => {
    if (score >= 80) return 'text-green-400';
    if (score >= 60) return 'text-yellow-400';
    return 'text-red-400';
  };

  return (
    <div className="glass-morphism rounded-2xl p-6 md:p-8">
      <h2 className="text-2xl font-bold mb-6 text-center text-gradient">Overall Performance</h2>
      <div className="flex flex-col md:flex-row items-center gap-8">
        <div className="relative">
          <svg className="w-36 h-36 transform -rotate-90" viewBox="0 0 120 120">
            <circle cx="60" cy="60" r="54" fill="none" strokeWidth="12" className="stroke-gray-700" />
            <motion.circle
              cx="60" cy="60" r="54" fill="none" strokeWidth="12"
              className={getScoreColor(metrics.overallScore).replace('text-', 'stroke-')}
              strokeDasharray="339.292"
              strokeLinecap="round"
              initial={{ strokeDashoffset: 339.292 }}
              animate={{ strokeDashoffset: 339.292 - (339.292 * metrics.overallScore) / 100 }}
              transition={{ duration: 1.5, ease: "easeOut", delay: 0.5 }}
            />
          </svg>
          <div className="absolute inset-0 flex flex-col items-center justify-center">
            <span className={`text-4xl font-bold ${getScoreColor(metrics.overallScore)}`}>{metrics.overallScore}</span>
            <span className="text-sm text-gray-400">Overall Score</span>
          </div>
        </div>
        <div className="w-full grid grid-cols-2 gap-4">
          <div className="bg-gray-800/50 p-4 rounded-lg text-center">
            <div className="text-xl font-bold text-neon-blue">{metrics.totalQuestions}</div>
            <div className="text-sm text-gray-400">Questions</div>
          </div>
          <div className="bg-gray-800/50 p-4 rounded-lg text-center">
            <div className={`text-xl font-bold ${getScoreColor(metrics.breakdown.fluency)}`}>{Math.round(metrics.breakdown.fluency)}%</div>
            <div className="text-sm text-gray-400">Avg. Fluency</div>
          </div>
          <div className="bg-gray-800/50 p-4 rounded-lg text-center">
            <div className={`text-xl font-bold ${getScoreColor(metrics.breakdown.relevancy)}`}>{Math.round(metrics.breakdown.relevancy)}%</div>
            <div className="text-sm text-gray-400">Relevancy</div>
          </div>
          <div className="bg-gray-800/50 p-4 rounded-lg text-center">
            <div className="text-xl font-bold text-red-400">{metrics.totalGrammarErrors}</div>
            <div className="text-sm text-gray-400">Grammar Errors</div>
          </div>
        </div>
      </div>
    </div>
  );
}
