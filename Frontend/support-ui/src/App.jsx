import { BrowserRouter, NavLink, Navigate, Route, Routes } from "react-router-dom";
import ChatPage from "./pages/ChatPage";
import AdminPage from "./pages/AdminPage";
import DatabasePage from "./pages/DatabasePage";
import LandingPage from "./pages/LandingPage";
import KnowledgeBasePage from "./pages/KnowledgeBasePage";

function SupportLayout() {
  return (
    <div className="app-shell">
      <header className="topbar">
        <div>
          <p className="eyebrow">Support Ops Console</p>
          <h1>Customer support that feels fast, clear, and calm.</h1>
        </div>
        <nav className="topbar-nav">
          <NavLink to="/" className="nav-link">
           Back
          </NavLink>
          <NavLink to="/chat" className={({ isActive }) => (isActive ? "nav-link active" : "nav-link") }>
            Chat
          </NavLink>
          <NavLink to="/admin" className={({ isActive }) => (isActive ? "nav-link active" : "nav-link")}>
            Admin
          </NavLink>
          <NavLink to="/database" className={({ isActive }) => (isActive ? "nav-link active" : "nav-link") }>
            Database
          </NavLink>
          <NavLink to="/knowledge-base" className={({ isActive }) => (isActive ? "nav-link active" : "nav-link") }>
            KB
          </NavLink>
        </nav>
      </header>

      <main className="app-main">
        <Routes>
          <Route path="chat" element={<ChatPage />} />
          <Route path="admin" element={<AdminPage />} />
          <Route path="database" element={<DatabasePage />} />
          <Route path="knowledge-base" element={<KnowledgeBasePage />} />
          <Route path="*" element={<Navigate to="/chat" replace />} />
        </Routes>
      </main>
    </div>
  );
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/*" element={<SupportLayout />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;