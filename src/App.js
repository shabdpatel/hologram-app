import React, { useState } from 'react';
import './App.css';
import Dropzone from './Dropzone';
import Sliders from './Sliders';
import Navbar from './Navbar';
import Modal from './Modal';
import { saveAs } from 'file-saver';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [image, setImage] = useState(null);
  const [processedImages, setProcessedImages] = useState({
    numeriReImageUrl: null,
    cghImageUrl: null,
  });
  const [parameters, setParameters] = useState({
    param1: 50,
    param2: 30,
  });
  const [loading, setLoading] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [modalImageSrc, setModalImageSrc] = useState('');

  const handleFileSelected = (file) => {
    setSelectedFile(file);
  };

  const handleConvertClick = () => {
    setLoading(true);
    const formData = new FormData();
    formData.append('file', selectedFile);

    fetch('http://localhost:5000/upload', {
      method: 'POST',
      body: formData,
    })
    .then(response => response.json())
    .then(result => {
      console.log('Success:', result);
      setImage(`http://localhost:5000/uploads/${selectedFile.name}`);
      setProcessedImages({
        numeriReImageUrl: result.numeriReImageUrl,
        cghImageUrl: result.cghImageUrl,
      });
    })
    .catch(error => {
      console.error('Error:', error);
    })
    .finally(() => {
      setLoading(false);
    });
  };

  const handleParameterChange = (param, value) => {
    setParameters((prevParams) => ({
      ...prevParams,
      [param]: value,
    }));
  };

  const handleImageClick = (src) => {
    setModalImageSrc(src);
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setModalImageSrc('');
  };

  const handleDownload = (src) => {
    saveAs(src, 'image.png'); // you can customize the default name
  };

  return (
    <div className="App">
      <Navbar />
      <header className="App-header">
        <h1>Drop or Add the Image below that you want to convert to Computer Generated Hologram</h1>
      </header>
      <Dropzone onFileSelected={handleFileSelected} />
      <Sliders parameters={parameters} onChange={handleParameterChange} />
      {selectedFile && (
        <button onClick={handleConvertClick}>Convert Image to CGH</button>
      )}
      {loading && <div className="loading">Loading...</div>}
      <div className="image-container">
        {image && (
          <div className="image-box">
            <h3>Uploaded Image</h3>
            <img src={image} alt="Uploaded" className="uploaded-image" onClick={() => handleImageClick(image)} />
            <button className="download-button" onClick={() => handleDownload(image)}>Download</button>
          </div>
        )}
        {processedImages.numeriReImageUrl && (
          <div className="image-box">
            <h3>Numerically Reconstructed Image</h3>
            <img src={processedImages.numeriReImageUrl} alt="Numeri Re Processed" className="processed-image" onClick={() => handleImageClick(processedImages.numeriReImageUrl)} />
            <button className="download-button" onClick={() => handleDownload(processedImages.numeriReImageUrl)}>Download</button>
          </div>
        )}
        {processedImages.cghImageUrl && (
          <div className="image-box">
            <h3>Computer Generated Hologram</h3>
            <img src={processedImages.cghImageUrl} alt="CGH Processed" className="processed-image" onClick={() => handleImageClick(processedImages.cghImageUrl)} />
            <button className="download-button" onClick={() => handleDownload(processedImages.cghImageUrl)}>Download</button>
          </div>
        )}
      </div>
      <Modal show={isModalOpen} imageSrc={modalImageSrc} onClose={handleCloseModal} />
    </div>
  );
}

export default App;
