export default function Tickets({ tickets = [], onStatusChange }) {
  const formatTime = (value) => {
    if (!value) return "Recently";
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) return "Recently";
    const diffInHours = Math.max(1, Math.round((Date.now() - date.getTime()) / (1000 * 60 * 60)));
    return diffInHours === 1 ? "1 hour ago" : `${diffInHours} hours ago`;
  };

  return (
    <section className="queue-section">
      <div className="queue-header">
        <div>
          <p className="section-kicker">Ticket queue</p>
          <h3>Manual review requests</h3>
        </div>
      </div>

      <div className="queue-list">
        {tickets.length === 0 ? (
          <p className="empty-state">No open tickets right now.</p>
        ) : (
          tickets.map((ticket) => (
            <article className="ticket-card" key={ticket.ticket_id}>
              <div className="ticket-meta">
                <span className={`status-badge ${String(ticket.status || "").toLowerCase()}`}>
                  {ticket.status || "OPEN"}
                </span>
                <span className="muted">{formatTime(ticket.created_at)}</span>
              </div>

              <h4>{ticket.issue || "Support request"}</h4>
              <p className="muted">Ticket #{ticket.ticket_id} · Order {ticket.order_id || "n/a"}</p>

              <div className="action-row">
                <button className="primary-button" onClick={() => onStatusChange(ticket.ticket_id, "APPROVED") }>
                  Approve
                </button>
                <button className="ghost-button" onClick={() => onStatusChange(ticket.ticket_id, "REJECTED") }>
                  Reject
                </button>
              </div>
            </article>
          ))
        )}
      </div>
    </section>
  );
}