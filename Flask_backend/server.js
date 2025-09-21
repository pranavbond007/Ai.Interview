





const express = require('express');
const multer = require('multer');
const path = require('path');
const fs = require('fs');




console.log('🚀 Starting server...');

const cors = require('cors');
console.log('✅ Imported express and cors');

const app = express();
const PORT = process.env.PORT || 3001;
console.log('✅ Created app, PORT:', PORT);

// Your existing middleware
app.use(cors({
  origin: ['http://localhost:5173', 'http://localhost:3000'],
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));
console.log('✅ CORS configured');

app.use(express.json());
console.log('✅ JSON middleware added');

// Your routes
const interviewRoutes = require('./routes/interview');
app.use('/api/interview', interviewRoutes);
console.log('✅ Routes configured');

// Health check
app.get('/api/health', (req, res) => {
  res.json({ status: 'OK', message: 'Backend server is running' });
});

// Start server
app.listen(PORT, () => {
  console.log(`🚀 Server running on http://localhost:${PORT}`);
  console.log('✅ Server started successfully!');
});

console.log('📝 Server setup complete, attempting to start...');

const router = express.Router();

// ✅ ENSURE UPLOAD DIRECTORY EXISTS FIRST
const uploadsDir = path.join(__dirname, '../uploads/interviews');
if (!fs.existsSync(uploadsDir)) {
  fs.mkdirSync(uploadsDir, { recursive: true });
  console.log('📁 Created uploads directory:', uploadsDir);
}

// ✅ SIMPLE MULTER SETUP - NO FANCY STUFF
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, uploadsDir);
  },
  filename: function (req, file, cb) {
    const filename = `question_${req.body.questionIndex}_${Date.now()}.webm`;
    cb(null, filename);
  }
});

const upload = multer({ 
  storage: storage,
  limits: { fileSize: 50 * 1024 * 1024 },
  fileFilter: function (req, file, cb) {
    // Accept all audio files
    cb(null, true);
  }
});

// ✅ ADD THIS NEW ROUTE TO CLEAR THE AUDIO FILES
app.post('/api/interview/clear-session', (req, res) => {
  const directory = path.join(__dirname, 'uploads', 'interviews');

  fs.readdir(directory, (err, files) => {
    if (err) {
      console.error("Could not list the directory.", err);
      return res.status(500).json({ error: 'Could not clear session files.' });
    }

    // Loop through each file and delete it
    for (const file of files) {
      fs.unlink(path.join(directory, file), err => {
        if (err) {
          console.error("Error deleting file:", file, err);
          // Don't stop on single file error, continue to delete others
        }
      });
    }
    
    console.log('✅ Previous session audio files cleared successfully.');
    res.status(200).json({ message: 'Previous session files cleared.' });
  });
});

// ✅ SIMPLE SAVE ENDPOINT
router.post('/save-recording', upload.single('audioFile'), (req, res) => {
  console.log('📥 Save request received');
  console.log('📁 File:', req.file ? 'YES' : 'NO');
  
  if (!req.file) {
    console.log('❌ No file received');
    return res.status(400).json({ error: 'No file received' });
  }

  console.log('✅ File saved:', req.file.filename);
  console.log('📍 Location:', req.file.path);
  
  res.json({
    success: true,
    filename: req.file.filename,
    size: req.file.size
  });
});

// ✅ CHECK SAVED FILES
router.get('/recordings', (req, res) => {
  try {
    if (!fs.existsSync(uploadsDir)) {
      return res.json({ recordings: [], count: 0 });
    }
    
    const files = fs.readdirSync(uploadsDir);
    res.json({
      recordings: files,
      count: files.length
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

module.exports = router;
