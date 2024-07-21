import React from 'react';

const Navbar = () => {
  return (
    <nav style={{ 
      display: 'flex',
      justifyContent:'center',
      alignItems: 'center',
      backgroundColor: '#4F46E5', 
      padding: '17px', 
      boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)',
      position: 'fixed',  // Make it fixed
      top: 0,  // Position it at the top
      width: '100%',  // Make it span the full width
      zIndex: 1000  // Ensure it stays above other content
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
