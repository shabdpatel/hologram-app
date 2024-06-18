const express = require('express');
const multer = require('multer');
const cors = require('cors');
const path = require('path');
const { spawn } = require('child_process');
const fs = require('fs');

const app = express();
const port = 5000;

// Use CORS middleware with explicit configuration
app.use(cors({
  origin: 'http://localhost:3000', // Allow only this origin to access the server
  methods: 'GET,HEAD,PUT,PATCH,POST,DELETE',
  credentials: true, // Allow cookies to be sent
  optionsSuccessStatus: 204
}));

// Configure storage for multer
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, path.join(__dirname, 'uploads')); // Folder to store uploaded files
  },
  filename: function (req, file, cb) {
    cb(null, file.originalname); // Use original file name
  },
});

const upload = multer({ storage: storage });

// Middleware to handle file upload and process the image
app.post('/upload', upload.single('file'), (req, res) => {
  const uploadedFilePath = path.join(__dirname, 'uploads', req.file.originalname);

  // Spawn a Python process to process the image
  const pythonProcess = spawn('python3', ['process_image.py', uploadedFilePath]);

  pythonProcess.on('close', (code) => {
    if (code !== 0) {
      return res.status(500).send('Failed to process image');
    }

    // Assuming the processed image is saved in the same directory with '_processed' suffix
    const processedFilePath = uploadedFilePath.replace(/(\.\w+)$/, '_processed$1');
    res.send({ imageUrl: `http://localhost:5000/uploads/${path.basename(processedFilePath)}` });
  });
});

// Serve static files from the uploads directory
app.use('/uploads', express.static(path.join(__dirname, 'uploads')));

// Serve static files (if needed)
app.use(express.static(path.join(__dirname, 'public')));

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
