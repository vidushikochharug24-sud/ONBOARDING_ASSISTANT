import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import '../styles/landing.css';

export default function Landing() {
  const navigate = useNavigate();

  const goSignup = () => navigate('/signup');
  const goLogin = () => navigate('/login');

  return (
    <div className="landing">
      <header className="dl-nav">
        <div className="dl-nav-inner">
          <div className="dl-logo"><span>DevLens</span></div>
          <nav className="dl-links">
            <a className="dl-link">Features</a>
            <a className="dl-link">How it Works</a>
            <a className="dl-link">Pricing</a>
          </nav>
          <div className="dl-actions">
            <button className="dl-signin" onClick={goLogin}>Sign In</button>
            <button className="dl-primary" onClick={goSignup}>Get Started →</button>
          </div>
        </div>
      </header>

      <main className="dl-main">
        <section className="dl-hero">
          <video className="dl-hero-video" autoPlay muted loop playsInline playsInline="true">
            <source src="/hero-video.mp4" type="video/mp4" />
            <source src="https://videos.pexels.com/video-files/3130284/3130284-uhd_2560_1440_30fps.mp4" type="video/mp4" />
          </video>
          <div className="video-overlay" />
          <div className="dl-hero-inner">
            <div className="dl-hero-left">
              <div className="dl-badge">AI-Assisted Onboarding</div>
              <h1 className="dl-title">Onboard new engineers in minutes, not weeks</h1>
              <p className="dl-sub">Automatically generate comprehensive guides for any codebase using retrieval-augmented analysis. New engineers get answers grounded in actual code.</p>
              <div className="dl-hero-ctas">
                <button className="dl-btn dl-btn-white" onClick={goSignup}>Get Started Free →</button>
                <button className="dl-btn dl-btn-outline">View Demo</button>
              </div>

              <ul className="dl-trust">
                <li>✓ Free forever tier</li>
                <li>✓ GitHub integration</li>
                <li>✓ Retrieval-augmented indexing</li>
              </ul>
            </div>

            <div className="dl-hero-right">
              <div className="mock-card">
                <div className="mac-dots"><span></span><span></span><span></span></div>
                <h4 className="card-title">New Engineer Guide</h4>
                <ul className="card-items">
                  <li className="item"><span className="dot green"/> What this project does</li>
                  <li className="item"><span className="dot blue"/> Key files: app.py, judge.py</li>
                </ul>
                <div className="card-status">Guide generated ✓</div>
              </div>
            </div>
          </div>
        </section>

        <section className="dl-stats">
          <div className="dl-stats-inner">
            <div className="stat"><div className="icon-wrap"> <svg className="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><path d="M12 2v4"/><path d="M7 4v2"/><path d="M17 4v2"/><path d="M19 11a7 7 0 1 1-14 0 7 7 0 0 1 14 0z"/></svg></div><span>AI-Assisted</span></div>
            <div className="stat"><div className="icon-wrap"> <svg className="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><path d="M3 7v10a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V7"/><path d="M16 3v4"/><path d="M8 3v4"/></svg></div><span>3 Input Methods</span></div>
            <div className="stat"><div className="icon-wrap"> <svg className="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a7.95 7.95 0 0 0 0-6"/></svg></div><span>Multi-Tenant</span></div>
            <div className="stat"><div className="icon-wrap"> <svg className="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg></div><span>RAG-Powered</span></div>
          </div>
        </section>

        <section className="dl-features">
          <h3 className="section-title">Features</h3>
          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-head"><div className="icon-wrap"><svg className="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><path d="M3 6h18M3 12h18M3 18h18"/></svg></div><h4>Guide Generation</h4></div>
              <p>Produce concise onboarding guides extracted from repository files.</p>
            </div>
            <div className="feature-card">
              <div className="feature-head"><div className="icon-wrap"><svg className="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg></div><h4>RAG-Powered Chat</h4></div>
              <p>Ask targeted questions with answers grounded in code and guides.</p>
            </div>
            <div className="feature-card">
              <div className="feature-head"><div className="icon-wrap"><svg className="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><rect x="3" y="3" width="18" height="14" rx="2"/><path d="M7 21v-4"/></svg></div><h4>Multi-Tenant Workspaces</h4></div>
              <p>Manage teams and access controls per workspace.</p>
            </div>
            <div className="feature-card">
              <div className="feature-head"><div className="icon-wrap"><svg className="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><path d="M3 7v10a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V7"/><path d="M16 3v4"/><path d="M8 3v4"/></svg></div><h4>GitHub, ZIP & PDF</h4></div>
              <p>Import code from repositories, archives, or docs.</p>
            </div>
            <div className="feature-card">
              <div className="feature-head"><div className="icon-wrap"><svg className="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><path d="M21 16V8a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v8"/><rect x="7" y="12" width="10" height="6" rx="2"/></svg></div><h4>Cloud Storage</h4></div>
              <p>Persist guides and artifacts in secure cloud storage.</p>
            </div>
            <div className="feature-card">
              <div className="feature-head"><div className="icon-wrap"><svg className="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a7.95 7.95 0 0 0 0-6"/></svg></div><h4>Vector Search</h4></div>
              <p>Semantic search across indexed code chunks for fast retrieval.</p>
            </div>
          </div>
        </section>

        <section className="dl-how">
          <h3 className="section-title">How it Works</h3>
          <div className="how-steps">
            <div className="step"> <div className="step-num">1</div> <div className="step-body"><strong>Paste GitHub URL or upload ZIP</strong></div> </div>
            <div className="step"> <div className="step-num">2</div> <div className="step-body"><strong>Analyze repository and generate a guide</strong></div> </div>
            <div className="step"> <div className="step-num">3</div> <div className="step-body"><strong>Query your codebase for answers</strong></div> </div>
          </div>
        </section>

        <section className="dl-cta">
          <div className="dl-cta-inner">
            <h2>Ready to onboard faster?</h2>
            <div className="dl-cta-buttons">
              <button className="dl-btn dl-btn-white" onClick={goSignup}>Get Started with GitHub →</button>
              <button className="dl-btn dl-btn-outline">View Pricing</button>
            </div>
          </div>
        </section>

        <footer className="dl-footer">
          <p>© {new Date().getFullYear()} DevLens. All rights reserved.</p>
        </footer>
      </main>
    </div>
  );
}
