export default function Refunds({ refunds = [] }) {
  return (
    <section className="queue-section">
      <div className="queue-header">
        <div>
          <p className="section-kicker">Refunds</p>
          <h3>Approved and pending refund records</h3>
        </div>
      </div>
      <div className="queue-list compact-list">
        {refunds.length === 0 ? (
          <p className="empty-state">No refund records yet.</p>
        ) : (
          refunds.map((refund) => (
            <article className="mini-card" key={refund.refund_id}>
              <div className="ticket-meta">
                <span className="status-badge">{refund.status || "PENDING"}</span>
                <span className="muted">Order {refund.order_id || "n/a"}</span>
              </div>
              <h4>{refund.reason || "Refund request"}</h4>
              <p className="muted">Refund #{refund.refund_id}</p>
            </article>
          ))
        )}
      </div>
    </section>
  );
}
