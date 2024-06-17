import React from 'react';

const Navbar = () => {
  return (
    <nav style={{ 
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      backgroundColor: '#4F46E5', 
      padding: '2rem', 
      boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)' 
    }}>
      {/* Left side */}
      <div>
        <span style={{ 
          color: '#FFFFFF', 
          fontSize: '1.25rem', 
          fontWeight: 'bold' 
        }}>Hologram App</span>
      </div>

      {/* Right side */}
      <div>
        <a href="#version1" style={{ 
          color: '#FFFFFF', 
          marginLeft: '1rem', 
          textDecoration: 'none', 
          padding: '0.5rem 1rem', 
          borderRadius: '0.25rem', 
          backgroundColor: '#6B63FF' 
        }}>Version1</a>
        <a href="#version2" style={{ 
          color: '#FFFFFF', 
          marginLeft: '1rem', 
          textDecoration: 'none', 
          padding: '0.5rem 1rem', 
          borderRadius: '0.25rem', 
          backgroundColor: '#6B63FF' 
        }}>Version2</a>
        <a href="#version3" style={{ 
          color: '#FFFFFF', 
          marginLeft: '1rem', 
          textDecoration: 'none', 
          padding: '0.5rem 1rem', 
          borderRadius: '0.25rem', 
          backgroundColor: '#6B63FF' 
        }}>Version3</a>
        <a href="#version4" style={{ 
          color: '#FFFFFF', 
          marginLeft: '1rem', 
          textDecoration: 'none', 
          padding: '0.5rem 1rem', 
          borderRadius: '0.25rem', 
          backgroundColor: '#6B63FF' 
        }}>Version4</a>
      </div>
    </nav>
  );
}

export default Navbar;
