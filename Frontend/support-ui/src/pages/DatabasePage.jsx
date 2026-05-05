import { useEffect, useMemo, useState } from "react";
import { getDatabaseTables } from "../services/api";

const TABLE_CONFIG = {
  users: {
    label: "Users",
    subtitle: "Registered users and complaint history",
    empty: "No user rows available.",
  },
  orders: {
    label: "Orders",
    subtitle: "Purchase history and current order status",
    empty: "No order rows available.",
  },
  tickets: {
    label: "Tickets",
    subtitle: "Escalated support cases",
    empty: "No ticket rows available.",
  },
  exchanges: {
    label: "Exchanges",
    subtitle: "Replacement requests",
    empty: "No exchange rows available.",
  },
  refunds: {
    label: "Refunds",
    subtitle: "Refund processing records",
    empty: "No refund rows available.",
  },
};

function formatValue(value) {
  if (value === null || value === undefined || value === "") return "-";
  if (typeof value === "object") return JSON.stringify(value);
  return String(value);
}

function buildColumns(rows) {
  if (!rows.length) return [];

  const preferredOrder = [
    "user_id",
    "order_id",
    "ticket_id",
    "exchange_id",
    "refund_id",
    "name",
    "email",
    "product_name",
    "new_product",
    "issue",
    "reason",
    "status",
    "priority",
    "complaint_count",
    "price",
    "created_at",
  ];

  const keys = Object.keys(rows[0]);
  return [
    ...preferredOrder.filter((key) => keys.includes(key)),
    ...keys.filter((key) => !preferredOrder.includes(key)),
  ];
}

function DataTable({ rows, emptyMessage }) {
  const columns = useMemo(() => buildColumns(rows), [rows]);

  if (!rows.length) {
    return <p className="empty-state">{emptyMessage}</p>;
  }

  return (
    <div className="table-shell">
      <table className="data-table">
        <thead>
          <tr>
            {columns.map((column) => (
              <th key={column}>{column.replaceAll("_", " ")}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, index) => (
            <tr key={row.id || row.user_id || row.order_id || row.ticket_id || row.exchange_id || row.refund_id || index}>
              {columns.map((column) => (
                <td key={column} title={formatValue(row[column])}>
                  {formatValue(row[column])}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default function DatabasePage() {
  const [activeTable, setActiveTable] = useState("users");
  const [database, setDatabase] = useState({
    users: [],
    orders: [],
    tickets: [],
    exchanges: [],
    refunds: [],
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadDatabase = async () => {
      try {
        setLoading(true);
        setError("");
        const res = await getDatabaseTables();
        setDatabase({
          users: res.data.users || [],
          orders: res.data.orders || [],
          tickets: res.data.tickets || [],
          exchanges: res.data.exchanges || [],
          refunds: res.data.refunds || [],
        });
      } catch (requestError) {
        setError(requestError?.message || "Unable to load database tables.");
      } finally {
        setLoading(false);
      }
    };

    loadDatabase();
  }, []);

  const summary = useMemo(
    () => [
      { label: "Users", value: database.users.length },
      { label: "Orders", value: database.orders.length },
      { label: "Tickets", value: database.tickets.length },
      { label: "Exchanges", value: database.exchanges.length },
      { label: "Refunds", value: database.refunds.length },
    ],
    [database]
  );

  const activeConfig = TABLE_CONFIG[activeTable];
  const activeRows = database[activeTable] || [];

  return (
    <div className="database-page">
      <section className="panel database-hero">
        <div className="panel-header">
          <div>
            <p className="section-kicker">Database explorer</p>
            <h2>Browse every table with a simple toggle.</h2>
            <p className="muted">
              Switch between users, orders, tickets, exchanges, and refunds without leaving the page.
            </p>
          </div>
          <button className="secondary-button" onClick={() => window.location.reload()}>
            Refresh
          </button>
        </div>

        <div className="summary-grid database-summary-grid">
          {summary.map((item) => (
            <article key={item.label} className="summary-card">
              <span>{item.label}</span>
              <strong>{item.value}</strong>
            </article>
          ))}
        </div>

        <div className="toggle-bar" role="tablist" aria-label="Database table selector">
          {Object.entries(TABLE_CONFIG).map(([key, config]) => (
            <button
              key={key}
              type="button"
              role="tab"
              aria-selected={activeTable === key}
              className={activeTable === key ? "toggle-chip active" : "toggle-chip"}
              onClick={() => setActiveTable(key)}
            >
              {config.label}
            </button>
          ))}
        </div>
      </section>

      <section className="panel database-panel">
        <div className="panel-header">
          <div>
            <p className="section-kicker">{activeConfig.label}</p>
            <h2>{activeConfig.subtitle}</h2>
          </div>
          <span className="status-dot">{activeRows.length} rows</span>
        </div>

        {error && <p className="error-banner">{error}</p>}

        {loading ? <p className="muted">Loading database tables...</p> : <DataTable rows={activeRows} emptyMessage={activeConfig.empty} />}
      </section>
    </div>
  );
}