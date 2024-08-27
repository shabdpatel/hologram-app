import React, { useState, useEffect } from 'react';
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
  const [previewImage, setPreviewImage] = useState(null);
  const [parameters, setParameters] = useState({
    param1: 8,
    param2: 30,
  });
  const [loading, setLoading] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [modalImageSrc, setModalImageSrc] = useState('');
  const [modalImageIndex, setModalImageIndex] = useState(0);
  const imageList = [image, processedImages.numeriReImageUrl, processedImages.cghImageUrl];

  useEffect(() => {
    if (selectedFile) {
      const reader = new FileReader();
      reader.onload = (e) => {
        setPreviewImage(e.target.result);
      };
      reader.readAsDataURL(selectedFile);
    }
  }, [selectedFile]);

  const handleFileSelected = (file) => {
    setSelectedFile(file);
  };
  const handleConvertClick = () => {
    setLoading(true);
    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('iterations', parameters.param1.toString());

    fetch('https://hologram-app-1.onrender.com/upload', { // Update the URL here
      method: 'POST',
      body: formData,
    })
      .then(response => response.json())
      .then(result => {
        console.log('Success:', result);
        setImage(`https://hologram-app-1.onrender.com/uploads/${selectedFile.name}`); // Update the URL here
        setProcessedImages({
          numeriReImageUrl: result.numeriReImageUrl,
          cghImageUrl: result.cghImageUrl,
        });
        setPreviewImage(null);
        setSelectedFile(null);
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

  const handleImageClick = (index) => {
    setModalImageIndex(index);
    setModalImageSrc(imageList[index]);
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setModalImageSrc('');
  };

  const handleDownload = (src) => {
    saveAs(src, 'image.png'); // you can customize the default name
  };

  const handleNextImage = () => {
    const nextIndex = (modalImageIndex + 1) % imageList.length;
    setModalImageIndex(nextIndex);
    setModalImageSrc(imageList[nextIndex]);
  };

  const handlePrevImage = () => {
    const prevIndex = (modalImageIndex - 1 + imageList.length) % imageList.length;
    setModalImageIndex(prevIndex);
    setModalImageSrc(imageList[prevIndex]);
  };

  return (
    <div className="App">
      <Navbar />
      <div style={{ paddingTop: '4rem' }}>
        <header className="App-header">
          <h1 className='Heading'>Drop or Upload the Image below that you want to convert to Computer Generated Hologram</h1>
        </header>
        <Dropzone onFileSelected={handleFileSelected} />

        {previewImage && (
          <div className="image-box1">
            <h3 className="image-title">Image Preview</h3>
            <img src={previewImage} alt="Preview" className="uploaded-image1" />
          </div>
        )}
        <Sliders parameters={parameters} onChange={handleParameterChange} />
        {selectedFile && (
          <button className="convert-button" onClick={handleConvertClick}>Convert Image to CGH</button>
        )}
        {loading && <div className="loading">Converting...</div>}
        <div className="image-container">
          {image && (
            <div className="image-box">
              <h3 className="image-title">Uploaded Image</h3>
              <img src={image} alt="Uploaded" className="uploaded-image" onClick={() => handleImageClick(0)} />
              <button className="download-button" onClick={() => handleDownload(image)}>Download</button>
            </div>
          )}
          {processedImages.numeriReImageUrl && (
            <div className="image-box">
              <h3 className="image-title">Numerically Reconstructed Image</h3>
              <img src={processedImages.numeriReImageUrl} alt="Numeri Re Processed" className="processed-image" onClick={() => handleImageClick(1)} />
              <button className="download-button" onClick={() => handleDownload(processedImages.numeriReImageUrl)}>Download</button>
            </div>
          )}
          {processedImages.cghImageUrl && (
            <div className="image-box">
              <h3 className="image-title">Computer Generated Hologram</h3>
              <img src={processedImages.cghImageUrl} alt="CGH Processed" className="processed-image" onClick={() => handleImageClick(2)} />
              <button className="download-button" onClick={() => handleDownload(processedImages.cghImageUrl)}>Download</button>
            </div>
          )}
        </div>
        <Modal show={isModalOpen} imageSrc={modalImageSrc} onClose={handleCloseModal} onNext={handleNextImage} onPrev={handlePrevImage} />
      </div>
    </div>
  );
}

export default App;
