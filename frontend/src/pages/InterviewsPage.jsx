import { useEffect, useState } from "react";

function InterviewsPage() {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const loadEvents = async () => {
    try {
      setLoading(true);
      setError("");

      const response = await fetch(
        "http://127.0.0.1:8000/applications/upcoming"
      );

      if (!response.ok) {
        throw new Error(
          "Unable to load interview information"
        );
      }

      const data = await response.json();

      setEvents(data.events || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadEvents();
  }, []);

  const interviewEvents = events.filter(
    (event) =>
      event.status === "Interview" &&
      event.interview_date
  );

  const otherEvents = events.filter(
    (event) => event.status !== "Interview"
  );

  const formatDate = (dateValue) => {
    if (!dateValue) {
      return "Not scheduled";
    }

    const normalized = dateValue.replace(
      " ",
      "T"
    );

    const date = new Date(normalized);

    if (Number.isNaN(date.getTime())) {
      return dateValue;
    }

    return date.toLocaleString();
  };

  return (
    <div className="page">
      <div className="page-header dashboard-page-header">
        <div>
          <h1>Interviews</h1>
          <p>
            View interview schedules and important
            application events.
          </p>
        </div>

        <button
          className="dashboard-refresh"
          onClick={loadEvents}
          disabled={loading}
        >
          {loading ? "Refreshing..." : "Refresh"}
        </button>
      </div>

      {error && (
        <div className="discovery-error">
          {error}
        </div>
      )}

      <section className="interview-summary-grid">
        <div className="stat-card">
          <p>Interview Records</p>
          <h2>{interviewEvents.length}</h2>
        </div>

        <div className="stat-card">
          <p>Other Events</p>
          <h2>{otherEvents.length}</h2>
        </div>

        <div className="stat-card">
          <p>Total Events</p>
          <h2>{events.length}</h2>
        </div>
      </section>

      <section className="dashboard-section">
        <div className="section-header">
          <div>
            <h2>Interview Schedule</h2>
            <p className="section-description">
              Applications currently marked as Interview.
            </p>
          </div>
        </div>

        {loading && events.length === 0 ? (
          <div className="page-placeholder">
            <h2>Loading interviews...</h2>
          </div>
        ) : interviewEvents.length === 0 ? (
          <div className="empty-card">
            No interview applications found.
          </div>
        ) : (
          <div className="interview-grid">
            {interviewEvents.map((event) => (
              <article
                className="interview-card"
                key={event.id}
              >
                <div className="interview-card-header">
                  <div>
                    <span className="interview-label">
                      Interview
                    </span>

                    <h2>{event.title}</h2>

                    <p className="company">
                      {event.company}
                    </p>
                  </div>

                  <span className="status interview">
                    {event.status}
                  </span>
                </div>

                <div className="interview-details">
                  <div>
                    <span className="meta-label">
                      Interview Date
                    </span>

                    <strong>
                      {formatDate(
                        event.interview_date
                      )}
                    </strong>
                  </div>

                  <div>
                    <span className="meta-label">
                      Deadline
                    </span>

                    <strong>
                      {event.deadline || "—"}
                    </strong>
                  </div>
                </div>

                <div className="interview-preparation">
                  <h3>Preparation Checklist</h3>

                  <ul>
                    <li>
                      Review the job description
                    </li>
                    <li>
                      Review resume projects and skills
                    </li>
                    <li>
                      Prepare questions for the interviewer
                    </li>
                    <li>
                      Test camera, microphone, or meeting link
                    </li>
                  </ul>
                </div>
              </article>
            ))}
          </div>
        )}
      </section>

      {otherEvents.length > 0 && (
        <section className="dashboard-section">
          <div className="section-header">
            <div>
              <h2>Other Application Events</h2>

              <p className="section-description">
                Applications that still contain scheduled
                dates but are no longer in Interview status.
              </p>
            </div>
          </div>

          <div className="event-list">
            {otherEvents.map((event) => (
              <div
                className="event-row"
                key={event.id}
              >
                <div>
                  <h3>{event.title}</h3>

                  <p className="company">
                    {event.company}
                  </p>
                </div>

                <div className="event-row-details">
                  <span
                    className={`status ${event.status.toLowerCase()}`}
                  >
                    {event.status}
                  </span>

                  <span>
                    {event.interview_date
                      ? formatDate(
                          event.interview_date
                        )
                      : event.deadline || "—"}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </section>
      )}
    </div>
  );
}

export default InterviewsPage;
