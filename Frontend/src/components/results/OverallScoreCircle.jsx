import React from 'react';
import { motion } from 'framer-motion';

export default function OverallScoreCircle({ score }) {
  const scoreColor = score >= 75 ? '#22c55e' : score >= 50 ? '#f59e0b' : '#ef4444';
  const radius = 85;
  const circumference = 2 * Math.PI * radius;

  return (
    <div className="relative w-48 h-48">
      {/* Background Circle */}
      <svg className="absolute top-0 left-0 w-full h-full" viewBox="0 0 200 200">
        <circle
          cx="100" cy="100" r={radius}
          fill="none"
          stroke="#333"
          strokeWidth="10"
        />
      </svg>
      {/* Progress Circle */}
      <svg className="absolute top-0 left-0 w-full h-full transform -rotate-90" viewBox="0 0 200 200">
        <motion.circle
          cx="100" cy="100" r={radius}
          fill="none"
          stroke={scoreColor}
          strokeWidth="12"
          strokeLinecap="round"
          strokeDasharray={circumference}
          initial={{ strokeDashoffset: circumference }}
          animate={{ strokeDashoffset: circumference - (score / 100) * circumference }}
          transition={{ duration: 1.5, ease: "circOut" }}
        />
      </svg>
      {/* Score Text */}
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <motion.span 
            className="text-5xl font-bold" 
            style={{ color: scoreColor }}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.5 }}
        >
          {Math.round(score)}
        </motion.span>
        <span className="text-sm text-gray-400">Overall Score</span>
      </div>
    </div>
  );
}
