import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import '../styles/landing.css';

export default function Landing() {
  const navigate = useNavigate();

  const handleGetStarted = () => {
    navigate('/signup');
  };

  return (
    <div className="landing">
      <header className="landing-header">
        <div className="landing-nav">
          <h1>Onboarding Assistant</h1>
          <div>
            <Link to="/login" className="nav-link">Login</Link>
            <Link to="/signup" className="nav-link nav-button">Get Started</Link>
          </div>
        </div>
      </header>

      <main className="landing-main">
        <section className="landing-hero">
          <h1>Intelligent Codebase Onboarding</h1>
          <p>Automatically generate comprehensive guides for new team members and contributors</p>
          <button onClick={handleGetStarted} className="cta-button">Get Started Free</button>
        </section>

        <section className="landing-features">
          <div className="feature-card">
            <h3>📊 Analyze Codebases</h3>
            <p>Upload a GitHub repository, ZIP file, or architecture documentation</p>
          </div>
          <div className="feature-card">
            <h3>📝 Generate Guides</h3>
            <p>Automatically create structured onboarding guides with AI-powered analysis</p>
          </div>
          <div className="feature-card">
            <h3>🚀 Accelerate Onboarding</h3>
            <p>Help new team members understand your codebase in minutes, not days</p>
          </div>
          <div className="feature-card">
            <h3>🔒 Enterprise Ready</h3>
            <p>Secure, private, and built for teams at any scale</p>
          </div>
        </section>

        <section className="landing-how-it-works">
          <h2>How It Works</h2>
          <ol>
            <li><strong>Connect:</strong> Link a GitHub repository, upload a ZIP, or share documentation</li>
            <li><strong>Analyze:</strong> Our AI analyzes your codebase structure and architecture</li>
            <li><strong>Generate:</strong> Get a comprehensive, customizable onboarding guide</li>
            <li><strong>Share:</strong> Copy, download, and share guides with your team</li>
          </ol>
        </section>

        <footer className="landing-footer">
          <p>&copy; 2024 Onboarding Assistant. Enterprise SaaS for Team Productivity.</p>
        </footer>
      </main>
    </div>
  );
}
