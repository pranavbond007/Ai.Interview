import { motion } from 'framer-motion'
import { useState, useEffect } from 'react'

export default function InterviewMetrics({ metrics }) {
  const [animatedMetrics, setAnimatedMetrics] = useState({
    fillerWords: 0,
    pauseDuration: 0,
    averageResponseTime: 0,
    confidenceScore: 0
  })

  useEffect(() => {
    // Animate metric changes
    const timer = setTimeout(() => {
      setAnimatedMetrics(metrics)
    }, 500)
    return () => clearTimeout(timer)
  }, [metrics])

  const metricItems = [
    {
      label: 'Confidence',
      value: Math.round(animatedMetrics.confidenceScore * 100),
      unit: '%',
      color: 'text-green-400',
      bgColor: 'bg-green-400/20',
      borderColor: 'border-green-400/40'
    },
    {
      label: 'Response Time',
      value: animatedMetrics.averageResponseTime,
      unit: 's',
      color: 'text-neon-blue',
      bgColor: 'bg-neon-blue/20',
      borderColor: 'border-neon-blue/40'
    },
    {
      label: 'Filler Words',
      value: animatedMetrics.fillerWords,
      unit: '',
      color: 'text-yellow-400',
      bgColor: 'bg-yellow-400/20',
      borderColor: 'border-yellow-400/40'
    },
    {
      label: 'Pause Duration',
      value: Math.round(animatedMetrics.pauseDuration),
      unit: 's',
      color: 'text-neon-purple',
      bgColor: 'bg-neon-purple/20',
      borderColor: 'border-neon-purple/40'
    }
  ]

  return (
    <motion.div
      className="glass-morphism rounded-2xl p-6 border border-white/10"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.8, delay: 0.4 }}
    >
      <h3 className="font-semibold text-lg mb-4 text-gradient">
        Live Metrics
      </h3>
      
      <div className="space-y-4">
        {metricItems.map((metric, index) => (
          <motion.div
            key={metric.label}
            className={`${metric.bgColor} ${metric.borderColor} border rounded-lg p-3`}
            initial={{ width: 0 }}
            animate={{ width: '100%' }}
            transition={{ duration: 0.8, delay: index * 0.1 }}
          >
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-300">{metric.label}</span>
              <motion.span
                className={`font-bold ${metric.color}`}
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: (index * 0.1) + 0.5 }}
              >
                {metric.value}{metric.unit}
              </motion.span>
            </div>
          </motion.div>
        ))}
      </div>

      <div className="mt-6 text-center">
        <motion.div
          className="inline-flex items-center gap-2 text-sm text-gray-400"
          animate={{ opacity: [0.5, 1, 0.5] }}
          transition={{ duration: 2, repeat: Infinity }}
        >
          <div className="w-2 h-2 bg-neon-blue rounded-full" />
          Analyzing in real-time
        </motion.div>
      </div>
    </motion.div>
  )
}
