import { motion } from 'framer-motion'
import { useState, useEffect } from 'react'

export default function AIAvatar({ isActive = false }) {
  const [pulsePhase, setPulsePhase] = useState(0)

  useEffect(() => {
    const interval = setInterval(() => {
      setPulsePhase(prev => prev + 0.1)
    }, 50)
    return () => clearInterval(interval)
  }, [])

  return (
    <div className="text-center">
      <motion.div
        className="relative w-24 h-24 mx-auto mb-4"
        animate={isActive ? { scale: [1, 1.05, 1] } : { scale: 1 }}
        transition={{ duration: 2, repeat: isActive ? Infinity : 0 }}
      >
        {/* Core Avatar */}
        <div className="absolute inset-0 rounded-full bg-gradient-to-br from-neon-blue to-neon-purple p-1">
          <div className="w-full h-full rounded-full bg-black flex items-center justify-center">
            <svg className="w-10 h-10 text-white" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-6-3a2 2 0 11-4 0 2 2 0 014 0zm-2 4a5 5 0 00-4.546 2.916A5.986 5.986 0 0010 16a5.986 5.986 0 004.546-2.084A5 5 0 0010 11z" clipRule="evenodd" />
            </svg>
          </div>
        </div>

        {/* Animated Rings */}
        {isActive && (
          <>
            <motion.div
              className="absolute inset-0 rounded-full border-2 border-neon-blue/50"
              animate={{
                scale: [1, 1.5],
                opacity: [1, 0]
              }}
              transition={{
                duration: 2,
                repeat: Infinity,
                ease: "easeOut"
              }}
            />
            <motion.div
              className="absolute inset-0 rounded-full border-2 border-neon-purple/50"
              animate={{
                scale: [1, 1.3],
                opacity: [1, 0]
              }}
              transition={{
                duration: 2,
                repeat: Infinity,
                delay: 0.5,
                ease: "easeOut"
              }}
            />
          </>
        )}
      </motion.div>

      {/* AI Status */}
      <div className="space-y-2">
        <h3 className="font-semibold text-lg text-gradient">
          AI Assistant
        </h3>
        
        <div className="flex items-center justify-center gap-2">
          <div className={`w-2 h-2 rounded-full ${isActive ? 'bg-green-400' : 'bg-gray-400'} animate-pulse`} />
          <span className="text-sm text-gray-400">
            {isActive ? 'Active' : 'Standby'}
          </span>
        </div>

          {/* I am removing it because This was making issues (Flickerign problem) */}
        {/* Voice Indicator
        {isActive && (
          <motion.div
            className="flex justify-center gap-1 mt-3"
            initial="hidden"
            animate="visible"
            variants={{
              hidden: { opacity: 0 },
              visible: { opacity: 1, transition: { staggerChildren: 0.1 } }
            }}
          >
            {[...Array(5)].map((_, i) => (
              <motion.div
                key={i}
                className="w-1 bg-neon-blue rounded-full"
                variants={{
                  hidden: { height: 4 },
                  visible: {
                    height: [4, 20, 4],
                    transition: {
                      duration: 1,
                      repeat: Infinity,
                      delay: i * 0.1
                    }
                  }
                }}
              />
            ))}
          </motion.div>
        )} */}
      </div>
    </div>
  )
}
