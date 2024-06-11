import React, { useState } from 'react';
import './App.css';
import Dropzone from './Dropzone';
import Sliders from './Sliders';
import Navbar from './Navbar';
function App() {
  const [image, setImage] = useState(null);
  const [parameters, setParameters] = useState({
    param1: 50,
    param2: 30,
  });

  const handleImageUpload = (file) => {
    const reader = new FileReader();
    reader.onload = (event) => {
      setImage(event.target.result);
    };
    reader.readAsDataURL(file);
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
      <Sliders parameters={parameters} onChange={handleParameterChange} />
    </div>
  );
}

export default App;
