import React, { useState } from 'react';
import '../styles/sidebar.css';

export default function Sidebar({
  guides,
  onGuideSelect,
  onNewAnalysis,
  loadingGuides,
}) {
  const [expandedGuide, setExpandedGuide] = useState(null);

  const getSourceBadgeColor = (sourceType) => {
    switch (sourceType) {
      case 'github':
        return '#6366f1';
      case 'zip':
        return '#8b5cf6';
      case 'pdf':
        return '#ec4899';
      default:
        return 'var(--cisco-blue)';
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'Unknown';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    });
  };

  return (
    <div className="sidebar">
      <button className="new-analysis-button" onClick={onNewAnalysis}>
        + New Analysis
      </button>

      <div className="guides-section">
        <h3>Previous Guides</h3>

        {loadingGuides ? (
          <p className="sidebar-loading">Loading...</p>
        ) : guides.length === 0 ? (
          <p className="sidebar-empty">No guides yet. Create one to get started!</p>
        ) : (
          <div className="guides-list">
            {guides.map((guide) => (
              <div
                key={guide.id}
                className="guide-item"
                onClick={() => onGuideSelect(guide)}
              >
                <div className="guide-header">
                  <h4 className="guide-name">{guide.repo_name}</h4>
                  <span
                    className="source-badge"
                    style={{ backgroundColor: getSourceBadgeColor(guide.source_type) }}
                  >
                    {guide.source_type}
                  </span>
                </div>
                <p className="guide-date">{formatDate(guide.created_at)}</p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
