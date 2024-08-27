const express = require('express');
const multer = require('multer');
const cors = require('cors');
const path = require('path');
const { spawn } = require('child_process');
const fs = require('fs');

const app = express();
const port = process.env.PORT || 5000;

// Use CORS middleware with explicit configuration
app.use(cors({
  origin: ['http://localhost:3000', 'https://hologram-app-phi.vercel.app/'], // Add your frontend's URL here
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
  const iterations = req.body.iterations || '8';
  // Spawn a Python process to process the image
  const pythonProcess = spawn('python3', ['uploads/Modified.py', uploadedFilePath, iterations]);

  pythonProcess.on('close', (code) => {
    if (code !== 0) {
      return res.status(500).send('Failed to process image');
    }

    // Assuming the processed images are saved in the same directory with '_numeri_re.bmp' and '_cgh.bmp' suffixes
    const baseName = path.basename(uploadedFilePath, path.extname(uploadedFilePath));
    const numeriReFilePath = path.join(__dirname, 'uploads', `${baseName}_numeri_re.bmp`);
    const cghFilePath = path.join(__dirname, 'uploads', `${baseName}_cgh.bmp`);

    res.send({
      numeriReImageUrl: `http://localhost:5000/uploads/${path.basename(numeriReFilePath)}`,
      cghImageUrl: `http://localhost:5000/uploads/${path.basename(cghFilePath)}`
    });
  });
});

// Serve static files from the uploads directory
app.use('/uploads', express.static(path.join(__dirname, 'uploads')));

// Serve the root route
app.get('/', (req, res) => {
  res.send('Backend server is running!');
});

// Serve static files (if needed)
app.use(express.static(path.join(__dirname, 'public')));

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
