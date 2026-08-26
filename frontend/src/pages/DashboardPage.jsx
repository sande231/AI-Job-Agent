import { useEffect, useState } from "react";

function DashboardPage() {
  const [dashboard, setDashboard] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const loadDashboard = async () => {
    try {
      setLoading(true);
      setError("");

      const response = await fetch(
        "http://127.0.0.1:8000/dashboard"
      );

      if (!response.ok) {
        throw new Error("Failed to load dashboard");
      }

      const data = await response.json();
      setDashboard(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDashboard();
  }, []);

  if (loading && !dashboard) {
    return (
      <div className="page">
        <div className="page-placeholder">
          <h2>Loading dashboard...</h2>
        </div>
      </div>
    );
  }

  if (error && !dashboard) {
    return (
      <div className="page">
        <div className="page-placeholder">
          <h2>Unable to load dashboard</h2>
          <p>{error}</p>

          <button
            className="refresh-button dashboard-refresh"
            onClick={loadDashboard}
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  const summary = dashboard?.application_summary || {};
  const topJobs = dashboard?.top_discovered_jobs || [];
  const applications = dashboard?.recent_applications || [];

  return (
    <div className="page">
      <div className="page-header dashboard-page-header">
        <div>
          <h1>Dashboard</h1>
          <p>
            Overview of your job search and application progress.
          </p>
        </div>

        <button
          className="dashboard-refresh"
          onClick={loadDashboard}
          disabled={loading}
        >
          {loading ? "Refreshing..." : "Refresh"}
        </button>
      </div>

      <section className="stats-grid">
        <div className="stat-card">
          <p>Total Applications</p>
          <h2>{summary.total ?? 0}</h2>
        </div>

        <div className="stat-card">
          <p>Applied</p>
          <h2>{summary.Applied ?? 0}</h2>
        </div>

        <div className="stat-card">
          <p>Interviews</p>
          <h2>{summary.Interview ?? 0}</h2>
        </div>

        <div className="stat-card">
          <p>Offers</p>
          <h2>{summary.Offer ?? 0}</h2>
        </div>
      </section>

      <section className="dashboard-section">
        <div className="section-header">
          <div>
            <h2>Top Job Matches</h2>
            <p className="section-description">
              Highest-ranked opportunities currently available.
            </p>
          </div>

          <span>
            {dashboard?.review_jobs_count ?? 0} jobs to review
          </span>
        </div>

        {topJobs.length === 0 ? (
          <div className="empty-card">
            No job matches available right now.
          </div>
        ) : (
          <div className="job-grid">
            {topJobs.slice(0, 4).map((job) => (
              <div
                className="job-card"
                key={job.id}
              >
                <div className="job-card-top">
                  <div>
                    <h3>{job.title}</h3>
                    <p className="company">
                      {job.company}
                    </p>
                  </div>

                  <div className="score">
                    {job.match_score ?? 0}%
                  </div>
                </div>

                <p className="location">
                  {job.location ||
                    "Location not provided"}
                </p>

                <div className="job-footer">
                  <span
                    className={`status ${job.status.toLowerCase()}`}
                  >
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
        )}
      </section>

      <section className="dashboard-section">
        <h2>Recent Applications</h2>

        {applications.length === 0 ? (
          <div className="empty-card">
            No applications yet.
          </div>
        ) : (
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
                {applications.slice(0, 5).map(
                  (application) => (
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

                      <td>
                        {application.date_applied || "—"}
                      </td>
                    </tr>
                  )
                )}
              </tbody>
            </table>
          </div>
        )}
      </section>

      <section className="dashboard-section">
        <h2>Upcoming Interviews</h2>

        {dashboard?.upcoming_interviews?.length === 0 ? (
          <div className="empty-card">
            No upcoming interviews.
          </div>
        ) : (
          <div className="job-grid">
            {dashboard?.upcoming_interviews?.map(
              (interview) => (
                <div
                  className="job-card"
                  key={interview.id}
                >
                  <h3>{interview.title}</h3>

                  <p className="company">
                    {interview.company}
                  </p>

                  <p>
                    {interview.interview_date}
                  </p>
                </div>
              )
            )}
          </div>
        )}
      </section>
    </div>
  );
}

export default DashboardPage;
