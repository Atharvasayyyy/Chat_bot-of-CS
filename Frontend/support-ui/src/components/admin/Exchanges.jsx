export default function Exchanges({ exchanges = [], onStatusChange }) {
  return (
    <section className="queue-section">
      <div className="queue-header">
        <div>
          <p className="section-kicker">Exchanges</p>
          <h3>Replacement requests</h3>
        </div>
      </div>
      <div className="queue-list compact-list">
        {exchanges.length === 0 ? (
          <p className="empty-state">No exchange records yet.</p>
        ) : (
          exchanges.map((exchange) => (
            <article className="mini-card" key={exchange.exchange_id}>
              <div className="ticket-meta">
                <span className="status-badge">{exchange.status || "PENDING"}</span>
                <span className="muted">Order {exchange.order_id || "n/a"}</span>
              </div>
              <h4>{exchange.new_product || "Replacement request"}</h4>
              <p className="muted">Exchange #{exchange.exchange_id}</p>
              <div className="action-row">
                <button className="primary-button" onClick={() => onStatusChange(exchange.exchange_id, "APPROVED") }>
                  Approve
                </button>
                <button className="ghost-button" onClick={() => onStatusChange(exchange.exchange_id, "REJECTED") }>
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
