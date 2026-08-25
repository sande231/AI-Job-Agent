import { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [dashboard, setDashboard] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch("http://127.0.0.1:8000/dashboard")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to load dashboard");
        }

        return response.json();
      })
      .then((data) => {
        setDashboard(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="page-center">
        <h2>Loading AI Job Agent...</h2>
      </div>
    );
  }

  if (error) {
    return (
      <div className="page-center">
        <h2>Unable to load dashboard</h2>
        <p>{error}</p>
      </div>
    );
  }

  const summary = dashboard.application_summary;

  return (
    <div className="app">
      <header className="header">
        <div>
          <h1>AI Job Agent</h1>
          <p>Your internship and application dashboard</p>
        </div>
      </header>

      <main className="container">
        <section className="stats-grid">
          <div className="stat-card">
            <p>Total Applications</p>
            <h2>{summary.total}</h2>
          </div>

          <div className="stat-card">
            <p>Applied</p>
            <h2>{summary.Applied}</h2>
          </div>

          <div className="stat-card">
            <p>Interviews</p>
            <h2>{summary.Interview}</h2>
          </div>

          <div className="stat-card">
            <p>Offers</p>
            <h2>{summary.Offer}</h2>
          </div>
        </section>

        <section className="dashboard-section">
          <div className="section-header">
            <h2>Top Job Matches</h2>
            <span>{dashboard.review_jobs_count} jobs to review</span>
          </div>

          <div className="job-grid">
            {dashboard.top_discovered_jobs.map((job) => (
              <div className="job-card" key={job.id}>
                <div className="job-card-top">
                  <div>
                    <h3>{job.title}</h3>
                    <p className="company">{job.company}</p>
                  </div>

                  <div className="score">
                    {job.match_score ?? 0}%
                  </div>
                </div>

                <p className="location">
                  {job.location || "Location not provided"}
                </p>

                <div className="job-footer">
                  <span className={`status ${job.status.toLowerCase()}`}>
                    {job.status}
                  </span>

                  {job.job_url && (
                    <a
                      href={job.job_url}
                      target="_blank"
                      rel="noreferrer"
                    >
                      View Job
                    </a>
                  )}
                </div>
              </div>
            ))}
          </div>
        </section>

        <section className="dashboard-section">
          <h2>Recent Applications</h2>

          <div className="table-wrapper">
            <table>
              <thead>
                <tr>
                  <th>Company</th>
                  <th>Position</th>
                  <th>Status</th>
                  <th>Match</th>
                  <th>Date Applied</th>
                </tr>
              </thead>

              <tbody>
                {dashboard.recent_applications.map((application) => (
                  <tr key={application.id}>
                    <td>{application.company}</td>
                    <td>{application.title}</td>
                    <td>
                      <span
                        className={`status ${application.status.toLowerCase()}`}
                      >
                        {application.status}
                      </span>
                    </td>
                    <td>
                      {application.match_score !== null
                        ? `${application.match_score}%`
                        : "—"}
                    </td>
                    <td>{application.date_applied || "—"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        <section className="dashboard-section">
          <h2>Upcoming Interviews</h2>

          {dashboard.upcoming_interviews.length === 0 ? (
            <div className="empty-card">
              No upcoming interviews.
            </div>
          ) : (
            <div className="job-grid">
              {dashboard.upcoming_interviews.map((interview) => (
                <div className="job-card" key={interview.id}>
                  <h3>{interview.title}</h3>
                  <p className="company">{interview.company}</p>
                  <p>{interview.interview_date}</p>
                </div>
              ))}
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;