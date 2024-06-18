const express = require('express');
const multer = require('multer');
const cors = require('cors');
const path = require('path');

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

// Middleware to handle file upload
app.post('/upload', upload.single('file'), (req, res) => {
  res.send('File uploaded successfully');
});

// Serve static files from the uploads directory
app.use('/uploads', express.static(path.join(__dirname, 'uploads')));

// Serve static files (if needed)
app.use(express.static(path.join(__dirname, 'public')));

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
