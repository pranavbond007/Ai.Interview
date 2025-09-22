import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import GlowingButton from '../components/ui/GlowingButton';

export default function StartPage() {
  const navigate = useNavigate();
  
  // Retrieve the questions from sessionStorage to get the count
  const storedQuestions = sessionStorage.getItem('interviewQuestions');
  const questions = storedQuestions ? JSON.parse(storedQuestions) : [];

  const handleBeginInterview = () => {
    navigate('/interview');
  };

  return (
    <div className="min-h-screen bg-black flex items-center justify-center">
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        className="glass-morphism rounded-2xl p-8 text-center max-w-2xl mx-4"
      >
        <motion.div
          className="w-24 h-24 mx-auto mb-6 rounded-full bg-gradient-to-br from-neon-blue to-neon-purple flex items-center justify-center"
          animate={{ 
            boxShadow: [
              '0 0 20px rgba(0,212,255,0.3)',
              '0 0 40px rgba(139,92,246,0.5)',
              '0 0 20px rgba(0,212,255,0.3)'
            ]
          }}
          transition={{ duration: 2, repeat: Infinity }}
        >
          <svg className="w-12 h-12 text-white" fill="currentColor" viewBox="0 0 20 20">
            <path d="M2 6a2 2 0 012-2h6a2 2 0 012 2v8a2 2 0 01-2 2H4a2 2 0 01-2-2V6zM14.553 7.106A1 1 0 0014 8v4a1 1 0 00.553.894l2 1A1 1 0 0018 13V7a1 1 0 00-1.447-.894l-2 1z" />
          </svg>
        </motion.div>
        
        <h1 className="text-3xl font-bold text-gradient mb-4">
          Your Interview is Ready
        </h1>
        <p className="text-gray-300 mb-8 leading-relaxed">
          The AI has analyzed your resume and prepared {questions.length} questions for you. Press the button below to begin.
        </p>
        
        <GlowingButton onClick={handleBeginInterview}>
          Begin Interview Session
        </GlowingButton>
      </motion.div>
    </div>
  );
}
