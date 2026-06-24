import React from 'react';
import '../styles/tabs.css';

export default function GuideTabs({ activeTab, onChange }) {
  const tabs = [
    { id: 'github', label: 'GitHub URL' },
    { id: 'zip', label: 'Upload ZIP' },
    { id: 'docs', label: 'Upload Docs' },
  ];

  return (
    <div className="tabs-container">
      {tabs.map((tab) => (
        <button
          key={tab.id}
          className={`tab-button ${activeTab === tab.id ? 'active' : ''}`}
          onClick={() => onChange(tab.id)}
        >
          {tab.label}
        </button>
      ))}
    </div>
  );
}
