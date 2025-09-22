import { motion } from 'framer-motion'
import { useState } from 'react'

export default function GlowingButton({ 
  children, 
  onClick, 
  variant = 'primary', 
  className = '',
  disabled = false,
  loading = false
}) {
  const [isHovered, setIsHovered] = useState(false)

  const variants = {
    primary: 'bg-gradient-to-r from-neon-blue to-neon-purple border-neon-blue',
    secondary: 'bg-transparent border-neon-purple text-neon-purple',
    danger: 'bg-gradient-to-r from-red-500 to-pink-500 border-red-500'
  }

  return (
    <motion.button
      className={`
        relative px-8 py-4 font-bold text-white border-2 rounded-lg
        transition-all duration-300 transform-gpu
        disabled:opacity-50 disabled:cursor-not-allowed
        ${variants[variant]}
        ${className}
      `}
      whileHover={{ 
        scale: disabled ? 1 : 1.05,
        boxShadow: disabled ? 'none' : '0 0 30px rgba(0,212,255,0.6)'
      }}
      whileTap={{ scale: disabled ? 1 : 0.98 }}
      onHoverStart={() => setIsHovered(true)}
      onHoverEnd={() => setIsHovered(false)}
      onClick={onClick}
      disabled={disabled || loading}
    >
      <span className="relative z-10 flex items-center justify-center gap-2">
        {loading && (
          <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
        )}
        {children}
      </span>
      
      {isHovered && !disabled && (
        <motion.div
          className="absolute inset-0 bg-gradient-to-r from-neon-blue/20 to-neon-purple/20 rounded-lg"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
        />
      )}
      
      <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent transform -skew-x-12 translate-x-[-100%] group-hover:translate-x-[200%] transition-transform duration-1000" />
    </motion.button>
  )
}
