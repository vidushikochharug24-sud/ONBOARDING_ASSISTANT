import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import '../styles/guide-display.css';

export default function GuideDisplay({ guide }) {
  const [copied, setCopied] = useState(false);

  // Debug: log the guide object structure
  console.log('GuideDisplay received guide:', guide);

  // Handle both API response formats
  const guideContent = guide?.guide || guide?.guide_content || '';
  const sourceType = guide?.source_type?.toLowerCase() || guide?.source_type || 'unknown';

  const handleCopyGuide = () => {
    navigator.clipboard.writeText(guideContent);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownloadPDF = () => {
    window.print();
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'Unknown';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const getSourceBadgeColor = (sourceType) => {
    const type = sourceType?.toLowerCase() || 'unknown';
    switch (type) {
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

  return (
    <div className="guide-display">
      <div className="guide-header">
        <div className="guide-title-section">
          <h1>{guide.repo_name}</h1>
          <div className="guide-meta">
            <span
              className="source-badge"
              style={{ backgroundColor: getSourceBadgeColor(sourceType) }}
            >
              {sourceType || 'unknown'}
            </span>
            <span className="guide-date">{formatDate(guide.created_at)}</span>
          </div>
        </div>

        <div className="guide-actions">
          <button
            className="action-button copy-button"
            onClick={handleCopyGuide}
            title="Copy guide text"
          >
            {copied ? '✓ Copied' : '📋 Copy Guide'}
          </button>
          <button
            className="action-button download-button"
            onClick={handleDownloadPDF}
            title="Download as PDF"
          >
            📥 Download
          </button>
        </div>
      </div>

      <div className="guide-content markdown-content">
        {guideContent && guideContent.trim() ? (
          <ReactMarkdown>{guideContent}</ReactMarkdown>
        ) : (
          <p className="no-content">No content available</p>
        )}
      </div>
    </div>
  );
}
