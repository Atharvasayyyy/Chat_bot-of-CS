const items = [
  { key: "tickets", label: "Tickets" },
  { key: "refunds", label: "Refunds" },
  { key: "exchanges", label: "Exchanges" },
  { key: "all", label: "All queues" },
];

export default function Sidebar({ activeView, setActiveView }) {
  return (
    <aside className="sidebar">
      <div>
        <p className="eyebrow">Queue control</p>
        <h3>Admin lanes</h3>
      </div>

      <nav className="sidebar-nav">
        {items.map((item) => (
          <button
            key={item.key}
            className={activeView === item.key ? "sidebar-link active" : "sidebar-link"}
            onClick={() => setActiveView(item.key)}
          >
            {item.label}
          </button>
        ))}
      </nav>
    </aside>
  );
}