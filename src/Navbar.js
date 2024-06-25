import React from 'react';

const Navbar = () => {
  return (
    <nav style={{ 
      display: 'flex',
      justifyContent:'center',
      alignItems: 'center',
      backgroundColor: '#4F46E5', 
      padding: '1rem', 
      boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)' 
    }}>
      
        <span style={{ 
          color: '#FFFFFF', 
          fontSize: '1.75rem', 
          fontWeight: 'bold' 
        }}>Hologram App</span>
      
    </nav>
  );
}

export default Navbar;
