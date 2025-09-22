import { Link, NavLink } from 'react-router-dom'
import { useState } from 'react'
import { motion } from 'framer-motion'

export default function Navbar() {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <motion.header 
      className="fixed inset-x-0 top-0 z-50 border-b border-white/10 glass-morphism"
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      transition={{ duration: 0.8 }}
    >
      <div className="mx-auto max-w-7xl px-4 py-3 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-2 group">
          <div className="h-8 w-8 rounded-lg bg-neon-blue blur-sm opacity-70 group-hover:opacity-100 transition-all duration-300" />
          <span className="text-lg tracking-wide font-medium">
            Interview<span className="text-neon-blue font-bold text-gradient animate-glow-pulse">AI</span>
          </span>
        </Link>
        
        <nav className="hidden md:flex items-center gap-8">
          <NavLink 
            to="/" 
            className={({isActive}) => `relative hover:text-neon-blue transition-colors duration-300 ${isActive ? 'text-neon-blue' : ''}`}
          >
            Home
          </NavLink>
          <NavLink 
            to="/interview" 
            className={({isActive}) => `relative hover:text-neon-blue transition-colors duration-300 ${isActive ? 'text-neon-blue' : ''}`}
          >
            Practice
          </NavLink>
          <NavLink 
            to="/dashboard" 
            className={({isActive}) => `relative hover:text-neon-blue transition-colors duration-300 ${isActive ? 'text-neon-blue' : ''}`}
          >
            Dashboard
          </NavLink>
        </nav>
        
        <div className="flex items-center gap-3">
          <button className="px-4 py-2 rounded-lg border border-neon-blue/40 text-neon-blue hover:bg-neon-blue/10 transition-all duration-300 hover:shadow-neon-blue">
            Sign In
          </button>
          <button 
            className="md:hidden p-2 text-white hover:text-neon-blue transition"
            onClick={() => setIsOpen(!isOpen)}
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
        </div>
      </div>
      
      {isOpen && (
        <motion.div 
          className="md:hidden border-t border-white/10 bg-black/90 backdrop-blur-xl"
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: 'auto' }}
          exit={{ opacity: 0, height: 0 }}
        >
          <nav className="px-4 py-4 space-y-2">
            <NavLink to="/" className="block py-2 hover:text-neon-blue transition">Home</NavLink>
            <NavLink to="/interview" className="block py-2 hover:text-neon-blue transition">Practice</NavLink>
            <NavLink to="/dashboard" className="block py-2 hover:text-neon-blue transition">Dashboard</NavLink>
          </nav>
        </motion.div>
      )}
    </motion.header>
  )
}
