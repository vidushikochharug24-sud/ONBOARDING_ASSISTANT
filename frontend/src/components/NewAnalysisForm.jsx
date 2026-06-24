import React, { useState } from 'react';
import { analyzeAPI, storageAPI } from '../utils/api';
import GuideTabs from './GuideTabs';
import LoadingSpinner from './LoadingSpinner';
import '../styles/new-analysis.css';

export default function NewAnalysisForm({ onGuideGenerated }) {
  const [activeTab, setActiveTab] = useState('github');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [formData, setFormData] = useState({
    githubUrl: '',
    githubDoc: null,
    zipFile: null,
    zipRepoName: '',
    zipDoc: null,
    docFile: null,
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    setError('');
  };

  const handleFileChange = (e, fieldName) => {
    setFormData((prev) => ({ ...prev, [fieldName]: e.target.files[0] }));
    setError('');
  };

  const handleGithubAnalysis = async (e) => {
    e.preventDefault();
    if (!formData.githubUrl.trim()) {
      setError('Please enter a GitHub URL');
      return;
    }

    setLoading(true);
    setError('');

    try {
      let docPath = null;
      if (formData.githubDoc) {
        const uploadRes = await storageAPI.upload(formData.githubDoc);
        docPath = uploadRes.data.file_path;
      }

      const response = await analyzeAPI.analyzeGithub({
        url: formData.githubUrl,
        doc_file_path: docPath,
      });

      onGuideGenerated(response.data);
      setFormData({ ...formData, githubUrl: '', githubDoc: null });
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to analyze GitHub repository');
    } finally {
      setLoading(false);
    }
  };

  const handleZipAnalysis = async (e) => {
    e.preventDefault();
    if (!formData.zipFile) {
      setError('Please select a ZIP file');
      return;
    }
    if (!formData.zipRepoName.trim()) {
      setError('Please enter a repository name');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const uploadRes = await storageAPI.upload(formData.zipFile);
      const filePath = uploadRes.data.file_path;

      let docPath = null;
      if (formData.zipDoc) {
        const docRes = await storageAPI.upload(formData.zipDoc);
        docPath = docRes.data.file_path;
      }

      const response = await analyzeAPI.analyzeZip({
        file_path: filePath,
        repo_name: formData.zipRepoName,
        doc_file_path: docPath,
      });

      onGuideGenerated(response.data);
      setFormData({ ...formData, zipFile: null, zipRepoName: '', zipDoc: null });
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to analyze ZIP file');
    } finally {
      setLoading(false);
    }
  };

  const handleDocUpload = async (e) => {
    e.preventDefault();
    if (!formData.docFile) {
      setError('Please select a PDF file');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await storageAPI.upload(formData.docFile);
      setError('');
      setFormData({ ...formData, docFile: null });
      alert('Document uploaded successfully: ' + response.data.file_path);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to upload document');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <LoadingSpinner message="Analyzing codebase... this may take 30 seconds" />;
  }

  return (
    <div className="new-analysis-form">
      <h2>New Analysis</h2>

      <GuideTabs activeTab={activeTab} onChange={setActiveTab} />

      {error && <div className="error-message">{error}</div>}

      {activeTab === 'github' && (
        <form onSubmit={handleGithubAnalysis} className="tab-form">
          <div className="form-group">
            <label htmlFor="githubUrl">GitHub Repository URL</label>
            <input
              type="text"
              id="githubUrl"
              name="githubUrl"
              placeholder="https://github.com/owner/repo"
              value={formData.githubUrl}
              onChange={handleInputChange}
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="githubDoc">Optional: Upload Documentation</label>
            <input
              type="file"
              id="githubDoc"
              accept=".pdf"
              onChange={(e) => handleFileChange(e, 'githubDoc')}
              disabled={loading}
            />
            {formData.githubDoc && (
              <p className="file-selected">Selected: {formData.githubDoc.name}</p>
            )}
          </div>

          <button type="submit" className="generate-button" disabled={loading}>
            Generate Guide
          </button>
        </form>
      )}

      {activeTab === 'zip' && (
        <form onSubmit={handleZipAnalysis} className="tab-form">
          <div className="form-group">
            <label htmlFor="zipFile">Upload ZIP File</label>
            <input
              type="file"
              id="zipFile"
              accept=".zip"
              onChange={(e) => handleFileChange(e, 'zipFile')}
              disabled={loading}
            />
            {formData.zipFile && (
              <p className="file-selected">Selected: {formData.zipFile.name}</p>
            )}
          </div>

          <div className="form-group">
            <label htmlFor="zipRepoName">Repository Name</label>
            <input
              type="text"
              id="zipRepoName"
              name="zipRepoName"
              placeholder="my-awesome-repo"
              value={formData.zipRepoName}
              onChange={handleInputChange}
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="zipDoc">Optional: Upload Documentation</label>
            <input
              type="file"
              id="zipDoc"
              accept=".pdf"
              onChange={(e) => handleFileChange(e, 'zipDoc')}
              disabled={loading}
            />
            {formData.zipDoc && (
              <p className="file-selected">Selected: {formData.zipDoc.name}</p>
            )}
          </div>

          <button type="submit" className="generate-button" disabled={loading}>
            Generate Guide
          </button>
        </form>
      )}

      {activeTab === 'docs' && (
        <form onSubmit={handleDocUpload} className="tab-form">
          <p className="docs-description">
            Upload architecture docs, Confluence exports, or design documents to use alongside your codebase analysis.
          </p>

          <div className="form-group">
            <label htmlFor="docFile">Upload PDF Documentation</label>
            <input
              type="file"
              id="docFile"
              accept=".pdf"
              onChange={(e) => handleFileChange(e, 'docFile')}
              disabled={loading}
            />
            {formData.docFile && (
              <p className="file-selected">Selected: {formData.docFile.name}</p>
            )}
          </div>

          <button type="submit" className="generate-button" disabled={loading}>
            Upload Document
          </button>
        </form>
      )}
    </div>
  );
}
