import React from 'react';

const Sliders = ({ parameters, onChange }) => {
  return (
    <div className="sliders-container">
      <div className="slider">
        <label htmlFor="param1">Number of Iterations:</label>
        <input
          type="range"
          id="param1"
          min="1"
          max="20"
          value={parameters.param1}
          onChange={(e) => onChange('param1', parseInt(e.target.value))}
        />
        <span>{parameters.param1}</span>
      </div>
      <div className="slider">
        <label htmlFor="param2">Parameter 2:</label>
        <input
          type="range"
          id="param2"
          min="0"
          max="100"
          value={parameters.param2}
          onChange={(e) => onChange('param2', parseInt(e.target.value))}
        />
        <span>{parameters.param2}</span>
      </div>
    </div>
  );
};

export default Sliders;