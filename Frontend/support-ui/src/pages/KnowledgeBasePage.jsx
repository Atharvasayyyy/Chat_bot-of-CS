import { useState } from "react";
import "../styles/KnowledgeBase.css";

export default function KnowledgeBasePage() {
  const [activeTab, setActiveTab] = useState("info");

  return (
    <div className="kb-page">
      {/* Header Section */}
      <div className="kb-header">
        <div>
          <h2 className="kb-title">Knowledge Base Management</h2>
          <p className="kb-subtitle">Manage your support knowledge base for AI-powered responses</p>
        </div>
        <div className="kb-badge">
          <span className="badge-icon">🔒</span>
          <span className="badge-text">Current Data: Amazon Products</span>
        </div>
      </div>

      {/* Restriction Notice */}
      <div className="restriction-banner">
        <div className="restriction-content">
          <div className="restriction-icon">⚠️</div>
          <div className="restriction-text">
            <h3>Import Restricted</h3>
            <p>The knowledge base currently contains Amazon product data. New data imports are not allowed at this time to maintain system stability and data consistency.</p>
          </div>
        </div>
        <div className="restriction-status">
          <span className="status-badge restricted">🚫 Imports Disabled</span>
        </div>
      </div>

      {/* Tabs Navigation */}
      <div className="kb-tabs">
        <button
          className={`kb-tab ${activeTab === "info" ? "active" : ""}`}
          onClick={() => setActiveTab("info")}
        >
          <span className="tab-icon">ℹ️</span>
          Current Status
        </button>
        <button
          className={`kb-tab ${activeTab === "upload" ? "active" : ""}`}
          onClick={() => setActiveTab("upload")}
        >
          <span className="tab-icon">📤</span>
          Upload Options (Preview)
        </button>
        <button
          className={`kb-tab ${activeTab === "history" ? "active" : ""}`}
          onClick={() => setActiveTab("history")}
        >
          <span className="tab-icon">📋</span>
          Import History
        </button>
      </div>

      {/* Tab Content */}
      <div className="kb-content">
        {/* Current Status Tab */}
        {activeTab === "info" && (
          <div className="tab-pane active">
            <div className="kb-stats">
              <div className="stat-card">
                <div className="stat-icon">📚</div>
                <div className="stat-info">
                  <p className="stat-label">Knowledge Base Size</p>
                  <p className="stat-value">12,543 articles</p>
                </div>
              </div>
              <div className="stat-card">
                <div className="stat-icon">🔄</div>
                <div className="stat-info">
                  <p className="stat-label">Last Updated</p>
                  <p className="stat-value">2 months ago</p>
                </div>
              </div>
              <div className="stat-card">
                <div className="stat-icon">✅</div>
                <div className="stat-info">
                  <p className="stat-label">Status</p>
                  <p className="stat-value">Active & Optimized</p>
                </div>
              </div>
              <div className="stat-card">
                <div className="stat-icon">🎯</div>
                <div className="stat-info">
                  <p className="stat-label">Query Accuracy</p>
                  <p className="stat-value">94.2%</p>
                </div>
              </div>
            </div>

            <div className="kb-info-grid">
              <div className="info-card">
                <h3>📊 Current Data Source</h3>
                <div className="info-content">
                  <p><strong>Provider:</strong> Amazon Products Catalog</p>
                  <p><strong>Categories:</strong> 48 product categories</p>
                  <p><strong>Languages:</strong> English, Spanish, French</p>
                  <p><strong>Update Frequency:</strong> Monthly</p>
                </div>
              </div>

              <div className="info-card">
                <h3>🛡️ Why Imports are Restricted</h3>
                <div className="info-content">
                  <ul className="restriction-list">
                    <li>Maintain AI model consistency</li>
                    <li>Prevent data contamination</li>
                    <li>Ensure response accuracy</li>
                    <li>Comply with data policies</li>
                    <li>Protect system performance</li>
                  </ul>
                </div>
              </div>

              <div className="info-card">
                <h3>📝 Feature Roadmap</h3>
                <div className="info-content">
                  <p className="roadmap-item">
                    <span className="roadmap-status planned">Planned</span>
                    <span>Multi-source knowledge base</span>
                  </p>
                  <p className="roadmap-item">
                    <span className="roadmap-status planned">Planned</span>
                    <span>Custom domain imports</span>
                  </p>
                  <p className="roadmap-item">
                    <span className="roadmap-status planned">Planned</span>
                    <span>Real-time sync capabilities</span>
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Upload Options Tab */}
        {activeTab === "upload" && (
          <div className="tab-pane active">
            <div className="upload-preview-notice">
              <p>These upload options will be available once import restrictions are lifted. Below is a preview of the interface:</p>
            </div>

            <div className="upload-options">
              {/* Media Upload */}
              <div className="upload-card disabled">
                <div className="upload-header">
                  <div className="upload-icon">📁</div>
                  <div className="upload-title">
                    <h3>Upload Media Files</h3>
                    <p>Add images, videos, or documents</p>
                  </div>
                </div>

                <div className="upload-body">
                  <div className="upload-area">
                    <svg
                      className="upload-icon-large"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="2"
                    >
                      <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                      <polyline points="17 8 12 3 7 8" />
                      <line x1="12" y1="3" x2="12" y2="15" />
                    </svg>
                    <p className="upload-text">Drag files here or click to browse</p>
                    <p className="upload-hint">Supported: PDF, PNG, JPG, MP4 (Max 50MB)</p>
                  </div>

                  <div className="upload-features">
                    <div className="feature">
                      <span>✓</span>
                      <span>Batch upload multiple files</span>
                    </div>
                    <div className="feature">
                      <span>✓</span>
                      <span>Automatic content extraction</span>
                    </div>
                    <div className="feature">
                      <span>✓</span>
                      <span>OCR for scanned documents</span>
                    </div>
                  </div>
                </div>

                <button className="upload-btn disabled" disabled>
                  Upload Media
                </button>
              </div>

              {/* Website Link */}
              <div className="upload-card disabled">
                <div className="upload-header">
                  <div className="upload-icon">🔗</div>
                  <div className="upload-title">
                    <h3>Import from Website</h3>
                    <p>Add knowledge from URLs</p>
                  </div>
                </div>

                <div className="upload-body">
                  <div className="input-group">
                    <input
                      type="url"
                      placeholder="https://example.com/knowledge-base"
                      disabled
                      className="website-input disabled"
                    />
                    <p className="input-hint">Enter a website URL to crawl and import content</p>
                  </div>

                  <div className="upload-features">
                    <div className="feature">
                      <span>✓</span>
                      <span>Deep crawl nested pages</span>
                    </div>
                    <div className="feature">
                      <span>✓</span>
                      <span>Extract structured content</span>
                    </div>
                    <div className="feature">
                      <span>✓</span>
                      <span>Schedule automatic syncs</span>
                    </div>
                  </div>
                </div>

                <button className="upload-btn disabled" disabled>
                  Import from Website
                </button>
              </div>

              {/* Text Input */}
              <div className="upload-card disabled">
                <div className="upload-header">
                  <div className="upload-icon">📝</div>
                  <div className="upload-title">
                    <h3>Add Text Content</h3>
                    <p>Paste text or create documents</p>
                  </div>
                </div>

                <div className="upload-body">
                  <textarea
                    placeholder="Paste your knowledge base content here..."
                    disabled
                    className="text-input disabled"
                    rows="6"
                  />
                  <p className="input-hint">Supports plain text, markdown, and structured data</p>

                  <div className="upload-features">
                    <div className="feature">
                      <span>✓</span>
                      <span>Support for Markdown formatting</span>
                    </div>
                    <div className="feature">
                      <span>✓</span>
                      <span>Bulk import with CSV</span>
                    </div>
                    <div className="feature">
                      <span>✓</span>
                      <span>Preview before committing</span>
                    </div>
                  </div>
                </div>

                <button className="upload-btn disabled" disabled>
                  Add Text Content
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Import History Tab */}
        {activeTab === "history" && (
          <div className="tab-pane active">
            <div className="history-container">
              <h3 className="history-title">Recent Imports</h3>
              
              <div className="history-list">
                <div className="history-item">
                  <div className="history-icon">📦</div>
                  <div className="history-details">
                    <p className="history-name">Amazon Product Database v2.1</p>
                    <p className="history-meta">Imported on Feb 14, 2025 • 12,543 articles</p>
                  </div>
                  <div className="history-status">
                    <span className="badge success">✓ Complete</span>
                  </div>
                </div>

                <div className="history-item">
                  <div className="history-icon">📦</div>
                  <div className="history-details">
                    <p className="history-name">Amazon Product Database v2.0</p>
                    <p className="history-meta">Imported on Dec 10, 2024 • 11,892 articles</p>
                  </div>
                  <div className="history-status">
                    <span className="badge">Previous</span>
                  </div>
                </div>

                <div className="history-item">
                  <div className="history-icon">📦</div>
                  <div className="history-details">
                    <p className="history-name">Amazon Product Database v1.9</p>
                    <p className="history-meta">Imported on Oct 05, 2024 • 11,456 articles</p>
                  </div>
                  <div className="history-status">
                    <span className="badge">Previous</span>
                  </div>
                </div>

                <div className="history-item">
                  <div className="history-icon">📦</div>
                  <div className="history-details">
                    <p className="history-name">Amazon Product Database v1.8</p>
                    <p className="history-meta">Imported on Aug 22, 2024 • 10,923 articles</p>
                  </div>
                  <div className="history-status">
                    <span className="badge">Previous</span>
                  </div>
                </div>
              </div>

              <div className="history-info">
                <h3>📊 Import Statistics</h3>
                <div className="stats-grid">
                  <div className="stat">
                    <p className="stat-num">4</p>
                    <p className="stat-txt">Total Imports</p>
                  </div>
                  <div className="stat">
                    <p className="stat-num">6 mo</p>
                    <p className="stat-txt">Since First Import</p>
                  </div>
                  <div className="stat">
                    <p className="stat-num">651</p>
                    <p className="stat-txt">Articles Added</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Footer Note */}
      <div className="kb-footer">
        <p>
          💡 <strong>Need help?</strong> Contact the support team to discuss knowledge base expansion options or future import capabilities.
        </p>
      </div>
    </div>
  );
}
