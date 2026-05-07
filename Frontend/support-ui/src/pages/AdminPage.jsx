import { useEffect, useMemo, useState } from "react";
import Sidebar from "../components/admin/Sidebar";
import Tickets from "../components/admin/Tickets";
import Exchanges from "../components/admin/Exchanges";
import Refunds from "../components/admin/Refunds";
import { getDashboard, updateExchange, updateTicket } from "../services/api";

export default function AdminPage() {
  const [activeView, setActiveView] = useState("tickets");
  const [dashboard, setDashboard] = useState({ tickets: [], refunds: [], exchanges: [] });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const loadDashboard = async () => {
    try {
      setLoading(true);
      setError("");
      const res = await getDashboard();
      setDashboard({
        tickets: res.data.tickets || [],
        refunds: res.data.refunds || [],
        exchanges: res.data.exchanges || [],
      });
    } catch (err) {
      setError(err?.message || "Unable to load dashboard data.");
      setDashboard({ tickets: [], refunds: [], exchanges: [] });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDashboard();

    const intervalId = setInterval(() => {
      loadDashboard();
    }, 10000);

    return () => clearInterval(intervalId);
  }, []);

  const summary = useMemo(
    () => [
      { label: "Tickets", value: dashboard.tickets.length },
      { label: "Refunds", value: dashboard.refunds.length },
      { label: "Exchanges", value: dashboard.exchanges.length },
      {
        label: "Needs review",
        value:
          dashboard.tickets.filter((item) => String(item.status || "").includes("REVIEW")).length +
          dashboard.exchanges.filter((item) => String(item.status || "").includes("PENDING")).length,
      },
    ],
    [dashboard]
  );

  const analytics = useMemo(() => {
    const ticketStatuses = dashboard.tickets.reduce((accumulator, item) => {
      const key = String(item.status || "UNKNOWN").toUpperCase();
      accumulator[key] = (accumulator[key] || 0) + 1;
      return accumulator;
    }, {});

    const exchangeStatuses = dashboard.exchanges.reduce((accumulator, item) => {
      const key = String(item.status || "PENDING").toUpperCase();
      accumulator[key] = (accumulator[key] || 0) + 1;
      return accumulator;
    }, {});

    const refundStatuses = dashboard.refunds.reduce((accumulator, item) => {
      const key = String(item.status || "PENDING").toUpperCase();
      accumulator[key] = (accumulator[key] || 0) + 1;
      return accumulator;
    }, {});

    return [
      { label: "Ticket review", data: ticketStatuses },
      { label: "Exchange pipeline", data: exchangeStatuses },
      { label: "Refund health", data: refundStatuses },
    ];
  }, [dashboard]);

  const handleStatusChange = async (ticketId, status) => {
    await updateTicket(ticketId, status);
    await loadDashboard();
  };

  const handleExchangeChange = async (exchangeId, status) => {
    await updateExchange(exchangeId, status);
    await loadDashboard();
  };

  return (
    <div className="page-grid admin-page">
      <Sidebar activeView={activeView} setActiveView={setActiveView} />

      <section className="panel admin-panel">
        <div className="panel-header">
          <div>
            <p className="section-kicker">Admin dashboard</p>
            <h2>Track tickets, refunds, and exchanges in one place.</h2>
          </div>
          <button className="secondary-button" onClick={loadDashboard}>
            Refresh
          </button>
        </div>

        <div className="summary-grid">
          {summary.map((item) => (
            <article key={item.label} className="summary-card">
              <span>{item.label}</span>
              <strong>{item.value}</strong>
            </article>
          ))}
        </div>

        <div className="analytics-grid">
          {analytics.map((block) => (
            <article key={block.label} className="analytics-card">
              <p className="section-kicker">Analytics</p>
              <h3>{block.label}</h3>
              <div className="bar-stack">
                {Object.keys(block.data).length === 0 ? (
                  <p className="empty-state">No data yet.</p>
                ) : (
                  Object.entries(block.data).map(([name, count]) => {
                    const total = Object.values(block.data).reduce((sum, value) => sum + value, 0) || 1;
                    const width = Math.max(12, Math.round((count / total) * 100));
                    return (
                      <div key={name} className="bar-row">
                        <div className="bar-row-label">
                          <span>{name}</span>
                          <strong>{count}</strong>
                        </div>
                        <div className="bar-track">
                          <div className="bar-fill" style={{ width: `${width}%` }} />
                        </div>
                      </div>
                    );
                  })
                )}
              </div>
            </article>
          ))}
        </div>

        {error && <p className="error-banner">{error}</p>}

        {loading ? (
          <p className="muted">Loading dashboard data...</p>
        ) : (
          <div className="stacked-panels">
            {(activeView === "tickets" || activeView === "all") && (
              <Tickets tickets={dashboard.tickets} onStatusChange={handleStatusChange} />
            )}
            {(activeView === "exchanges" || activeView === "all") && (
              <Exchanges exchanges={dashboard.exchanges} onStatusChange={handleExchangeChange} />
            )}
            {(activeView === "refunds" || activeView === "all") && (
              <Refunds refunds={dashboard.refunds} />
            )}
          </div>
        )}
      </section>
    </div>
  );
}