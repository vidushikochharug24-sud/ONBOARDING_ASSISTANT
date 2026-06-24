import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getUserEmail, getCompanyName, logout } from '../utils/auth';
import { analyzeAPI } from '../utils/api';
import Sidebar from '../components/Sidebar';
import NewAnalysisForm from '../components/NewAnalysisForm';
import GuideDisplay from '../components/GuideDisplay';
import CodebaseChat from '../components/CodebaseChat';
import '../styles/dashboard.css';
import LoadingSpinner from '../components/LoadingSpinner';

export default function Dashboard() {
  const navigate = useNavigate();
  const email = getUserEmail();
  const companyName = getCompanyName();
  const [guides, setGuides] = useState([]);
  const [selectedGuide, setSelectedGuide] = useState(null);
  const [loadingGuides, setLoadingGuides] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchGuides();
  }, []);

  const fetchGuides = async () => {
    setLoadingGuides(true);
    setError('');
    try {
      const response = await analyzeAPI.getGuides();
      setGuides(response.data);
    } catch (err) {
      setError('Failed to load guides');
      console.error(err);
    } finally {
      setLoadingGuides(false);
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const handleGuideGenerated = (newGuide) => {
    const normalizedGuide = {
      ...newGuide,
      id: newGuide.id || newGuide.guide_id,
    };

    setSelectedGuide(normalizedGuide);
    setGuides((currentGuides) => [normalizedGuide, ...currentGuides]);
  };

  const handleGuideSelect = (guide) => {
    setSelectedGuide(guide);
  };

  const handleNewAnalysis = () => {
    setSelectedGuide(null);
  };

  const currentGuideId = selectedGuide?.id || selectedGuide?.guide_id;

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <div className="header-left">
          <h1>Onboarding Assistant</h1>
        </div>
        <div className="header-right">
          <span className="user-info">{email}</span>
          <button className="logout-button" onClick={handleLogout}>
            Logout
          </button>
        </div>
      </header>

      <div className="dashboard-container">
        <aside className="dashboard-sidebar">
          <Sidebar
            guides={guides}
            onGuideSelect={handleGuideSelect}
            onNewAnalysis={handleNewAnalysis}
            loadingGuides={loadingGuides}
          />
        </aside>

        <main className="dashboard-main">
          {error && <div className="error-message">{error}</div>}

          {selectedGuide ? (
            <div className="guide-workspace">
              <GuideDisplay guide={selectedGuide} />
              {currentGuideId && (
                <CodebaseChat key={currentGuideId} guide={selectedGuide} />
              )}
            </div>
          ) : (
            <NewAnalysisForm onGuideGenerated={handleGuideGenerated} />
          )}
        </main>
      </div>
    </div>
  );
}
