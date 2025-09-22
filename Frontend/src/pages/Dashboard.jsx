import { motion } from 'framer-motion'

export default function Dashboard() {
  return (
    <div className="min-h-screen bg-black pt-20">
      <div className="mx-auto max-w-7xl px-4 py-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <h1 className="text-3xl font-bold text-gradient mb-8">
            Performance Dashboard
          </h1>
          
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
            {[
              { label: 'Sessions Completed', value: '12' },
              { label: 'Average Score', value: '85%' },
              { label: 'Improvement', value: '+15%' },
              { label: 'Time Practiced', value: '4.5h' }
            ].map((metric, index) => (
              <motion.div
                key={metric.label}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className="glass-morphism rounded-xl p-6"
              >
                <div className="text-2xl font-bold text-neon-blue mb-2">
                  {metric.value}
                </div>
                <div className="text-sm text-neutral-400">
                  {metric.label}
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </div>
    </div>
  )
}
