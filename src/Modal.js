import React from 'react';
import './Modal.css';
import { saveAs } from 'file-saver';

const Modal = ({ show, imageSrc, onClose, onNext, onPrev }) => {
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
      <button className="prev-button" onClick={onPrev}>&#10094;</button>
      <button className="next-button" onClick={onNext}>&#10095;</button>
    </div>
  );
};

export default Modal;
