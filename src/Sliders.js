import React from 'react';
import Slider from 'rc-slider';
import 'rc-slider/assets/index.css';

const Sliders = ({ parameters, onChange }) => {
  return (
    <div className="sliders">
      <div className="slider-container">
        <label>Parameter 1</label>
        <Slider
          min={0}
          max={100}
          value={parameters.param1}
          onChange={(value) => onChange('param1', value)}
        />
        <span>{parameters.param1}</span>
      </div>
      <div className="slider-container">
        <label>Parameter 2</label>
        <Slider
          min={0}
          max={100}
          value={parameters.param2}
          onChange={(value) => onChange('param2', value)}
        />
        <span>{parameters.param2}</span>
      </div>
    </div>
  );
};

export default Sliders;
