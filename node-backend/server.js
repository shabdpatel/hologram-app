// node-backend/server.js

const express = require('express');
const multer = require('multer');
const { spawn } = require('child_process');
const path = require('path');
const app = express();
const port = 3001; // Port for your backend server

// Multer configuration for handling file uploads
const storage = multer.diskStorage({
    destination: function(req, file, cb) {
        cb(null, 'uploads/') // Directory where uploaded files will be stored temporarily
    },
    filename: function(req, file, cb) {
        cb(null, file.originalname)
    }
});

const upload = multer({ storage: storage });

// Example endpoint to handle image upload and processing
app.post('/api/upload', upload.single('image'), (req, res) => {
    // Path to your Python script
    const pythonScriptPath = path.join(__dirname, 'path/to/your/python_script.py');
    // Path to uploaded image file
    const imagePath = req.file.path;

    // Run the Python script as a child process
    const pythonProcess = spawn('python', [pythonScriptPath, imagePath]);

    pythonProcess.stdout.on('data', (data) => {
        console.log(`stdout: ${data}`);
        // Handle data from Python script (if needed)
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`);
        // Handle error output from Python script (if needed)
    });

    pythonProcess.on('close', (code) => {
        console.log(`child process exited with code ${code}`);
        if (code === 0) {
            // Assuming script succeeded, send back processed image path or data
            res.json({ success: true, processedImagePath: 'path/to/processed/image' });
        } else {
            res.status(500).json({ success: false, error: 'Failed to process image' });
        }
    });
});

// Start the server
app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
