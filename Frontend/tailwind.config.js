/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0f9ff',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
          900: '#1e3a8a'
        },
        neon: {
          blue: '#00d4ff',
          purple: '#8b5cf6',
          pink: '#ec4899',
          cyan: '#06b6d4'
        }
      },
      backgroundImage: {
        'cyber-grid': `
          linear-gradient(rgba(0,212,255,0.1) 1px, transparent 1px),
          linear-gradient(90deg, rgba(0,212,255,0.1) 1px, transparent 1px),
          radial-gradient(circle at 20% 50%, rgba(139,92,246,0.15) 0%, transparent 50%),
          radial-gradient(circle at 80% 50%, rgba(0,212,255,0.15) 0%, transparent 50%)
        `,
        'neural-net': `
          radial-gradient(circle at 25% 25%, rgba(139,92,246,0.2) 0%, transparent 50%),
          radial-gradient(circle at 75% 75%, rgba(0,212,255,0.2) 0%, transparent 50%),
          linear-gradient(45deg, transparent 49%, rgba(139,92,246,0.03) 50%, transparent 51%)
        `
      },
      boxShadow: {
        'neon-blue': '0 0 20px rgba(0,212,255,0.5), 0 0 40px rgba(0,212,255,0.3), 0 0 80px rgba(0,212,255,0.1)',
        'neon-purple': '0 0 20px rgba(139,92,246,0.5), 0 0 40px rgba(139,92,246,0.3), 0 0 80px rgba(139,92,246,0.1)',
        'cyber': 'inset 0 1px 0 rgba(0,212,255,0.2), 0 1px 2px rgba(0,0,0,0.3), 0 0 20px rgba(0,212,255,0.1)',
        'glass': '0 8px 32px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.1)'
      },
      animation: {
        'float': 'float 6s ease-in-out infinite',
        'pulse-slow': 'pulse 4s ease-in-out infinite',
        'glow-pulse': 'glow-pulse 2s ease-in-out infinite alternate',
        'slide-up': 'slideUp 0.8s ease-out forwards',
        'fade-in': 'fadeIn 1s ease-out forwards',
        'neural-flow': 'neuralFlow 8s linear infinite',
        'data-stream': 'dataStream 3s linear infinite',
        'hologram': 'hologram 4s ease-in-out infinite',
        'cyber-scan': 'cyberScan 2s linear infinite'
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-20px)' }
        },
        'glow-pulse': {
          '0%': { textShadow: '0 0 5px rgba(0,212,255,0.5), 0 0 10px rgba(0,212,255,0.5)' },
          '100%': { textShadow: '0 0 20px rgba(0,212,255,0.8), 0 0 30px rgba(0,212,255,0.6)' }
        },
        slideUp: {
          '0%': { opacity: '0', transform: 'translateY(60px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' }
        },
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' }
        },
        neuralFlow: {
          '0%': { backgroundPosition: '0% 50%' },
          '100%': { backgroundPosition: '200% 50%' }
        },
        dataStream: {
          '0%': { transform: 'translateX(-100%)' },
          '100%': { transform: 'translateX(100vw)' }
        },
        hologram: {
          '0%, 100%': { opacity: '1', filter: 'hue-rotate(0deg)' },
          '50%': { opacity: '0.8', filter: 'hue-rotate(90deg)' }
        },
        cyberScan: {
          '0%': { transform: 'translateY(-100%)' },
          '100%': { transform: 'translateY(100vh)' }
        }
      },
      backdropBlur: {
        'xs': '2px'
      }
    },
  },
  plugins: [],
}
