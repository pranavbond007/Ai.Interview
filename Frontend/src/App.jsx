import { Routes, Route, useLocation } from 'react-router-dom' // ✅ 1. Import useLocation
import { motion } from 'framer-motion'
import Navbar from './components/layout/Navbar'
import Footer from './components/layout/Footer'; 
import HomePage from './pages/HomePage'
import ResumeUpload from './pages/ResumeUpload'
import InterviewSession from './pages/InterviewSession'
import Dashboard from './pages/Dashboard'
import Results from './pages/Results'
import StartPage from './pages/StartPage';

export default function App() {
  const location = useLocation(); // ✅ 2. Get the current location object

  return (
    <div className="min-h-screen bg-black text-white relative">
      <div className="relative z-10">
        <Navbar />
        
        <motion.main
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 1 }}
        >
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/upload-resume" element={<ResumeUpload />} />
            <Route path="/start" element={<StartPage />} />
            <Route path="/interview" element={<InterviewSession />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/results" element={<Results />} />
          </Routes>
        </motion.main>
        
        {/* ✅ 3. Conditionally render the Footer */}
        {location.pathname === '/' && <Footer />}
      </div>
    </div>
  )
}
