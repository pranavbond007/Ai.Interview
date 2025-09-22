import { motion } from 'framer-motion';

export default function LoadingScreen({ message = "Analyzing your interview..." }) {
  const steps = [
    "Analyzing speech patterns...",
    "Checking grammar and fluency...",
    "Evaluating answer relevancy...",
    "Generating comprehensive report..."
  ];

  return (
    <div className="min-h-screen bg-black flex items-center justify-center p-4">
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center"
      >
        <motion.div
          className="w-28 h-28 mx-auto mb-8 relative"
          animate={{ rotate: 360 }}
          transition={{ duration: 4, repeat: Infinity, ease: "linear" }}
        >
          <div className="absolute inset-0 rounded-full border-4 border-neon-blue border-t-transparent animate-spin"></div>
          <div className="absolute inset-4 rounded-full border-4 border-neon-purple border-b-transparent animate-spin" style={{ animationDirection: 'reverse', animationDuration: '2.5s' }}></div>
          <div className="absolute inset-8 bg-gradient-to-br from-neon-blue/20 to-neon-purple/20 flex items-center justify-center rounded-full">
             <svg className="w-8 h-8 text-white animate-pulse" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M12 6V4m0 16v-2M8 8l1.414-1.414M14.586 14.586L16 16m-7.07-8.586L16 6m-8.586 7.07L6 16" />
            </svg>
          </div>
        </motion.div>

        <motion.h2 
          className="text-3xl font-bold text-gradient mb-4"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
        >
          AI Analysis in Progress
        </motion.h2>
        <p className="text-gray-400 mb-8">{message}</p>

        <div className="space-y-3 text-left max-w-sm mx-auto">
          {steps.map((step, index) => (
            <motion.div
              key={step}
              className="flex items-center space-x-3 text-gray-300"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.4 + 0.5, duration: 0.5 }}
            >
              <div className="w-2 h-2 bg-neon-blue rounded-full animate-ping"></div>
              <span className="text-sm">{step}</span>
            </motion.div>
          ))}
        </div>
      </motion.div>
    </div>
  );
}
