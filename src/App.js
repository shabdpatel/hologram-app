import React, { useState } from 'react';
import './App.css';
import Dropzone from './Dropzone';
import Sliders from './Sliders';
import Navbar from './Navbar';

function App() {
  const [image, setImage] = useState(null);
  const [processedImage, setProcessedImage] = useState(null);
  const [parameters, setParameters] = useState({
    param1: 50,
    param2: 30,
  });

  const handleImageUpload = (file) => {
    const formData = new FormData();
    formData.append('file', file);

    fetch('http://localhost:5000/upload', {
      method: 'POST',
      body: formData,
    })
    .then(response => response.json())
    .then(result => {
      console.log('Success:', result);
      setImage(`http://localhost:5000/uploads/${file.name}`);
      setProcessedImage(result.imageUrl); // Set the URL of the processed image
    })
    .catch(error => {
      console.error('Error:', error);
    });
  };

  const handleParameterChange = (param, value) => {
    setParameters((prevParams) => ({
      ...prevParams,
      [param]: value,
    }));
  };

  return (
    <div className="App">
      <Navbar />
      <header className="App-header">
        <h1>Computer Generated Hologram</h1>
      </header>
      <Dropzone onDrop={handleImageUpload} />
      {image && <img src={image} alt="Uploaded" className="uploaded-image" />}
      {processedImage && <img src={processedImage} alt="Processed" className="processed-image" />}
      <Sliders parameters={parameters} onChange={handleParameterChange} />
    </div>
  );
}

export default App;
