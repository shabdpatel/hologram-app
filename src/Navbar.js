import React from 'react';

const Navbar = () => {
  return (
    <nav style={{ backgroundColor: '#4F46E5', padding: '2rem', boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)' }}>
      <div className="max-w-6xl mx-auto">
        <div className="flex justify-between items-center">
          <div className="flex items-center">
            <span style={{ color: '#FFFFFF', fontSize: '1.25rem', fontWeight: 'bold', padding: '5rem' }}>Hologram App</span>
          </div>
          <div className="hidden md:flex">
            <a href="#version1" style={{ color: '#FFFFFF', marginLeft: '1rem', textDecoration: 'none', padding: '0.5rem 1rem', borderRadius: '0.25rem', backgroundColor: '#6B63FF' }}>Version1</a>
            <a href="#version2" style={{ color: '#FFFFFF', marginLeft: '1rem', textDecoration: 'none', padding: '0.5rem 1rem', borderRadius: '0.25rem', backgroundColor: '#6B63FF' }}>Version2</a>
            <a href="#version3" style={{ color: '#FFFFFF', marginLeft: '1rem', textDecoration: 'none', padding: '0.5rem 1rem', borderRadius: '0.25rem', backgroundColor: '#6B63FF' }}>Version3</a>
            <a href="#version4" style={{ color: '#FFFFFF', marginLeft: '1rem', textDecoration: 'none', padding: '0.5rem 1rem', borderRadius: '0.25rem', backgroundColor: '#6B63FF' }}>Version4</a>
          </div>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
