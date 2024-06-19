import React, { useState } from 'react';
import './App.css';
import Dropzone from './Dropzone';
import Sliders from './Sliders';
import Navbar from './Navbar';

function App() {
  const [image, setImage] = useState(null);
  const [processedImages, setProcessedImages] = useState({
    numeriReImageUrl: null,
    cghImageUrl: null,
  });
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
      setProcessedImages({
        numeriReImageUrl: result.numeriReImageUrl,
        cghImageUrl: result.cghImageUrl,
      });
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
        <h1>Drop or Add the Image below that you want to cnvert to Computer Generated Hologram </h1>
      </header>
      <Dropzone onDrop={handleImageUpload} />
      <div className="image-container">
        {image && (
          <div className="image-box">
            <h3>Uploaded Image</h3>
            <img src={image} alt="Uploaded" className="uploaded-image" />
          </div>
        )}
        {processedImages.numeriReImageUrl && (
          <div className="image-box">
            <h3>Numerically Reconstructed Image</h3>
            <img src={processedImages.numeriReImageUrl} alt="Numeri Re Processed" className="processed-image" />
          </div>
        )}
        {processedImages.cghImageUrl && (
          <div className="image-box">
            <h3>Computer Generated Hologram</h3>
            <img src={processedImages.cghImageUrl} alt="CGH Processed" className="processed-image" />
          </div>
        )}
      </div>
      <Sliders parameters={parameters} onChange={handleParameterChange} />
    </div>
  );
}

export default App;
