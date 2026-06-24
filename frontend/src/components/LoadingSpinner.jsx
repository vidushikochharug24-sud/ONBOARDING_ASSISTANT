import React from 'react';
import '../styles/loading.css';

export default function LoadingSpinner({ message = 'Loading...' }) {
  return (
    <div className="loading-overlay">
      <div className="loading-container">
        <div className="spinner"></div>
        <p>{message}</p>
      </div>
    </div>
  );
}
