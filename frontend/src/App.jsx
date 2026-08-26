import { useState } from "react";

import "./App.css";

import Sidebar from "./components/Sidebar";

import DashboardPage from "./pages/DashboardPage";
import DiscoverJobsPage from "./pages/DiscoverJobsPage";
import ApplicationsPage from "./pages/ApplicationsPage";
import InterviewsPage from "./pages/InterviewsPage";
import ProfilePage from "./pages/ProfilePage";

function App() {
  const [activePage, setActivePage] =
    useState("dashboard");

  const renderPage = () => {
    switch (activePage) {
      case "discover":
        return <DiscoverJobsPage />;

      case "applications":
        return <ApplicationsPage />;

      case "interviews":
        return <InterviewsPage />;

      case "profile":
        return <ProfilePage />;

      case "dashboard":
      default:
        return <DashboardPage />;
    }
  };

  return (
    <div className="app">
      <Sidebar
        activePage={activePage}
        setActivePage={setActivePage}
      />

      <div className="app-content">
        {renderPage()}
      </div>
    </div>
  );
}

export default App;
