import { BrowserRouter, NavLink, Route, Routes } from "react-router-dom";
import ChatPage from "./pages/ChatPage";
import AdminPage from "./pages/AdminPage";
import DatabasePage from "./pages/DatabasePage";

function App() {
  return (
    <BrowserRouter>
      <div className="app-shell">
        <header className="topbar">
          <div>
            <p className="eyebrow">Support Ops Console</p>
            <h1>Customer support that feels fast, clear, and calm.</h1>
          </div>
          <nav className="topbar-nav">
            <NavLink to="/" className={({ isActive }) => (isActive ? "nav-link active" : "nav-link")}>
              Chat
            </NavLink>
            <NavLink to="/admin" className={({ isActive }) => (isActive ? "nav-link active" : "nav-link")}>
              Admin
            </NavLink>
            <NavLink to="/database" className={({ isActive }) => (isActive ? "nav-link active" : "nav-link") }>
              Database
            </NavLink>
          </nav>
        </header>

        <main className="app-main">
          <Routes>
            <Route path="/" element={<ChatPage />} />
            <Route path="/admin" element={<AdminPage />} />
            <Route path="/database" element={<DatabasePage />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;