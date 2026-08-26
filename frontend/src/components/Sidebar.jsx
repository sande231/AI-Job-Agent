function Sidebar({ activePage, setActivePage }) {
  const menuItems = [
    {
      id: "dashboard",
      label: "Dashboard",
    },
    {
      id: "discover",
      label: "Discover Jobs",
    },
    {
      id: "applications",
      label: "Applications",
    },
    {
      id: "interviews",
      label: "Interviews",
    },
    {
      id: "profile",
      label: "Profile & Resume",
    },
  ];

  return (
    <aside className="sidebar">
      <div className="sidebar-brand">
        <div className="brand-icon">AI</div>

        <div>
          <h2>Job Agent</h2>
          <p>Career Assistant</p>
        </div>
      </div>

      <nav className="sidebar-nav">
        {menuItems.map((item) => (
          <button
            key={item.id}
            className={
              activePage === item.id
                ? "sidebar-link active"
                : "sidebar-link"
            }
            onClick={() => setActivePage(item.id)}
          >
            {item.label}
          </button>
        ))}
      </nav>

      <div className="sidebar-footer">
        <span className="online-dot"></span>
        Backend connected
      </div>
    </aside>
  );
}

export default Sidebar;
