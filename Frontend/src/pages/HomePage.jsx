  import { motion } from 'framer-motion'
  import { Link } from 'react-router-dom'
  import { useState, useEffect } from 'react'
  import React from 'react'     //dekhna padega baad mein.
  import { SparklesCore } from '../components/ui/SparklesCore';



  export default function HomePage() {
    const [currentText, setCurrentText] = useState(0)
    const heroTexts = [
      "Master interviews with AI",
      "Practice with real-time feedback",
      "Analyze speech and expressions"
    ]

    useEffect(() => {
      const interval = setInterval(() => {
        setCurrentText((prev) => (prev + 1) % heroTexts.length)
      }, 3000)
      return () => clearInterval(interval)
    }, [])

    return (
      <div className="min-h-screen">
        
        {/* Hero Section */}
        <section className="relative overflow-hidden min-h-screen flex items-center">
        

          {/* Animated Background */}
          <div className="absolute inset-0 pointer-events-none">
            <div className="absolute -top-40 -left-40 h-80 w-80 rounded-full bg-neon-blue/20 blur-3xl animate-pulse-slow" />
            <div className="absolute -bottom-40 -right-40 h-80 w-80 rounded-full bg-neon-purple/10 blur-3xl animate-float" />
            <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 h-96 w-96 rounded-full bg-neon-purple/5 blur-3xl animate-pulse" />
          </div>
          
          {/* Ye abhi latest lagaya he. */}
          {/* Background Particles Effect */}
        <div className="absolute inset-0 z-0">
          <SparklesCore
            id="homepage-particles"
            background="transparent"
            minSize={0.6}
            maxSize={1.4}
            particleDensity={100}
            className="w-full h-full"
            particleColor="#ffffff"
            speed={2}
          />
        </div>
          {/* Content */}
          <div className="relative mx-auto max-w-7xl px-4 py-20 text-center">
            <motion.div
              initial={{ opacity: 0, y: 50 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 1 }}
              className="space-y-8"
            >
              <h1 className="text-5xl md:text-7xl font-bold tracking-tight leading-tight">
                <span className="block">
                  {heroTexts[currentText].split(' ').map((word, index) => (
                    <motion.span 
                      key={`${currentText}-${index}`}
                      className={`inline-block ${word === 'AI' || word === 'feedback' || word === 'expressions' ? 'text-neon-blue animate-glow-pulse' : ''}`}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: index * 0.1 }}
                    >
                      {word}&nbsp;
                    </motion.span>
                  ))}
                </span>
              </h1>
              
              <p className="text-xl md:text-2xl text-neutral-400 max-w-3xl mx-auto leading-relaxed">
                Personalized questions, real-time speech and facial analysis, and actionable feedback to level up your interview performance.
              </p>
              
              <div className="flex flex-col sm:flex-row items-center justify-center gap-6 pt-8">
                <Link 
                  to="/upload-resume" 
                  className="group px-8 py-4 rounded-xl bg-neon-blue text-white text-lg font-semibold shadow-neon-blue hover:brightness-110 hover:shadow-neon-lg transform hover:scale-105 transition-all duration-300"
                >
                  <span className="flex items-center gap-2">
                    Start Practice
                    <svg className="w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                    </svg>
                  </span>
                </Link>
                
                <button className="px-8 py-4 rounded-xl border border-white/20 hover:border-neon-blue/50 hover:text-neon-blue hover:bg-neon-blue/5 transition-all duration-300 text-lg">
                  Watch Demo
                </button>
              </div>
              
              <div className="pt-12 flex items-center justify-center gap-8 text-xs uppercase tracking-wider text-neutral-600">
                <span>Futuristic</span>
                <div className="h-px w-8 bg-neon-blue/40" />
                <span>AI-Powered</span>
                <div className="h-px w-8 bg-neon-blue/40" />
                <span>Real-time</span>
              </div>
            </motion.div>
          </div>
          
          {/* Scroll Indicator */}
          <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 animate-bounce">
            <div className="h-12 w-6 rounded-full border border-white/20 flex justify-center">
              <div className="h-3 w-1 bg-neon-blue rounded-full mt-2 animate-pulse" />
            </div>
          </div>
        </section>

        {/* Features Section */}
        <section className="py-20 relative">
          <div className="mx-auto max-w-7xl px-4">
            <motion.div
              initial={{ opacity: 0, y: 50 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
              viewport={{ once: true }}
              className="text-center mb-16"
            >
              <h2 className="text-3xl md:text-5xl font-bold mb-6">
                Platform <span className="text-neon-blue">Features</span>
              </h2>
              <p className="text-xl text-neutral-400 max-w-3xl mx-auto">
                Advanced AI-powered tools to transform your interview preparation
              </p>
            </motion.div>

            <div className="grid gap-8 sm:grid-cols-2 lg:grid-cols-3">
              {[
                { title: 'AI Question Generation', desc: 'Personalized questions based on your resume and role', icon: '🤖' },
                { title: 'Real-time Analysis', desc: 'Live feedback on speech patterns and body language', icon: '📊' },
                { title: 'Facial Recognition', desc: 'Advanced emotion and confidence detection', icon: '👁️' },
                { title: 'Speech Analytics', desc: 'Analyze pace, clarity, and filler words', icon: '🗣️' },
                { title: 'Performance Tracking', desc: 'Track improvement over multiple sessions', icon: '📈' },
                { title: 'Professional Reports', desc: 'Detailed feedback with actionable insights', icon: '📋' }
              ].map((feature, index) => (
                <motion.div
                  key={feature.title}
                  initial={{ opacity: 0, y: 30 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: index * 0.1 }}
                  viewport={{ once: true }}
                  className="group relative rounded-xl border border-white/10 bg-gray-900/50 p-6 hover:border-neon-blue/40 hover:shadow-neon-blue transition-all duration-500"
                >
                  <div className="text-4xl mb-4">{feature.icon}</div>
                  <h3 className="text-xl font-semibold text-neon-blue mb-3 group-hover:animate-glow-pulse">
                    {feature.title}
                  </h3>
                  <p className="text-neutral-400 group-hover:text-neutral-300 transition-colors">
                    {feature.desc}
                  </p>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-20">
          <div className="mx-auto max-w-5xl px-4">
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              whileInView={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.8 }}
              viewport={{ once: true }}
              className="relative overflow-hidden rounded-2xl border border-neon-blue/30 bg-gradient-to-br from-gray-900/90 to-black/90 p-12 text-center"
            >
              <div className="absolute inset-0 bg-neural-net opacity-30" />
              
              <div className="relative z-10">
                <h3 className="text-3xl md:text-4xl font-bold mb-4">
                  Ready to <span className="text-neon-blue animate-glow-pulse">Ace</span> Your Next Interview?
                </h3>
                <p className="text-xl text-neutral-400 mb-8 max-w-2xl mx-auto">
                  Start practicing with AI-powered feedback and real-time analysis. Transform your interview skills today.
                </p>
                
                <Link 
                  to="/upload-resume"
                  className="inline-block px-8 py-4 rounded-xl bg-neon-blue text-white text-lg font-semibold shadow-neon-blue hover:brightness-110 hover:shadow-neon-lg transform hover:scale-105 transition-all duration-300"
                >
                  Launch Practice Session
                </Link>
              </div>
            </motion.div>
          </div>
        </section>
      </div>
    )
  }
