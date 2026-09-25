import { useState } from "react";

import "./App.css";

import Sidebar from "./components/Sidebar";

import DashboardPage from "./pages/DashboardPage";
import DiscoverJobsPage from "./pages/DiscoverJobsPage";
import ApplicationsPage from "./pages/ApplicationsPage";
import InterviewsPage from "./pages/InterviewsPage";
import ProfilePage from "./pages/ProfilePage";
import JobDetailsPage from "./pages/JobDetailsPage";

function App() {
  const [activePage, setActivePage] =
    useState("dashboard");

  const [selectedJob, setSelectedJob] =
    useState(null);

  const renderPage = () => {
    switch (activePage) {
      case "discover":
        return (
          <DiscoverJobsPage
            onViewJob={(job) => {
              setSelectedJob(job);
              setActivePage("job-details");
            }}
          />
        );

      case "job-details":
        return (
          <JobDetailsPage
            job={selectedJob}
            onBack={() =>
              setActivePage("discover")
            }
            onMoveToApplications={async (job) => {
              try {
                const response = await fetch(
                  `http://127.0.0.1:8000/discovered-jobs/${job.id}/apply`,
                  {
                    method: "POST",
                  }
                );

                const result = await response.json();

                if (!response.ok) {
                  throw new Error(
                    result.message ||
                      "Unable to move job to applications"
                  );
                }

                setSelectedJob(null);
                setActivePage("applications");
              } catch (error) {
                alert(error.message);
              }
            }}
          />
        );

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
