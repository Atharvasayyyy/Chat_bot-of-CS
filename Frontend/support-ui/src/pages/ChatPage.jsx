import ChatWindow from "../components/chat/ChatWindow";

export default function ChatPage() {
  return (
    <div className="page-grid chat-page">
      <section className="hero-card">
        <p className="section-kicker">Live assistant</p>
        <h2>Resolve issues faster with guided refunds, exchanges, and order checks.</h2>
        <p className="muted">
          Ask a question, attach a product image, or start a refund / exchange request.
          The chat sends requests directly to the FastAPI backend.
        </p>
        <div className="stat-row">
          <div className="stat-pill">
            <strong>24/7</strong>
            <span>support flow</span>
          </div>
          <div className="stat-pill">
            <strong>Image</strong>
            <span>upload ready</span>
          </div>
          <div className="stat-pill">
            <strong>Backend</strong>
            <span>connected</span>
          </div>
        </div>
      </section>

      <section className="panel chat-panel">
        <ChatWindow />
      </section>
    </div>
  );
}