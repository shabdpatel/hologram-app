import React from 'react';
import './Modal.css';
import { saveAs } from 'file-saver';

const Modal = ({ show, imageSrc, onClose }) => {
  if (!show) {
    return null;
  }

  const handleDownload = () => {
    saveAs(imageSrc, 'image.png'); // you can customize the default name
  };

  return (
    <div className="modal">
      <span className="close" onClick={onClose}>&times;</span>
      <img className="modal-content" src={imageSrc} alt="Fullscreen" />
      <button className="download-button" onClick={handleDownload}>Download</button>
    </div>
  );
};

export default Modal;
