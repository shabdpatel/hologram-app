import React from 'react';
import { useDropzone } from 'react-dropzone';

const Dropzone = ({ onFileSelected }) => {
  const { getRootProps, getInputProps } = useDropzone({
    onDrop: (acceptedFiles) => {
      onFileSelected(acceptedFiles[0]);
    },
  });

  return (
    <div {...getRootProps({ className: 'dropzone' })}>
      <input {...getInputProps()} />
      <p>Drag & drop an image here, or click to select one</p>
    </div>
  );
};

export default Dropzone;
