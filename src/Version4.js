// src/Version1.js
import React from 'react';
import Dropzone from './Dropzone';
import Sliders from './Sliders';

const Version1 = () => {
  const [image, setImage] = React.useState(null);
  const [parameters, setParameters] = React.useState({
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
    <div>
      <h1>Version 1</h1>
      <Dropzone onDrop={handleImageUpload} />
      {image && <img src={image} alt="Uploaded" className="uploaded-image" />}
      <Sliders parameters={parameters} onChange={handleParameterChange} />
    </div>
  );
};

export default Version1;
