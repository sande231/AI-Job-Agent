import { useEffect, useState } from "react";

function InterviewsPage() {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [generatingPrepId, setGeneratingPrepId] =
    useState(null);

  const [interviewPrep, setInterviewPrep] =
    useState({});

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

  const handleGenerateInterviewPrep = async (
    applicationId
  ) => {
    try {
      setGeneratingPrepId(applicationId);

      const response = await fetch(
        `http://127.0.0.1:8000/applications/${applicationId}/interview-prep`,
        {
          method: "POST",
        }
      );

      const result = await response.json();

      if (!response.ok) {
        throw new Error(
          result.message ||
            "Unable to generate interview preparation"
        );
      }

      setInterviewPrep((previous) => ({
        ...previous,
        [applicationId]: result.preparation,
      }));
    } catch (err) {
      alert(err.message);
    } finally {
      setGeneratingPrepId(null);
    }
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

                  <button
                    className="generate-materials-button"
                    onClick={() =>
                      handleGenerateInterviewPrep(
                        event.id
                      )
                    }
                    disabled={
                      generatingPrepId === event.id
                    }
                  >
                    {generatingPrepId === event.id
                      ? "Generating..."
                      : "Generate Interview Prep"}
                  </button>

                  {interviewPrep[event.id] && (
                    <div className="generated-materials">
                      <div className="generated-section">
                        <h3>Likely Interview Questions</h3>

                        <ul>
                          {interviewPrep[
                            event.id
                          ].likely_interview_questions?.map(
                            (question, index) => (
                              <li key={index}>
                                {question}
                              </li>
                            )
                          )}
                        </ul>
                      </div>

                      <div className="generated-section">
                        <h3>Technical Topics to Review</h3>

                        <ul>
                          {interviewPrep[
                            event.id
                          ].technical_topics_to_review?.map(
                            (topic, index) => (
                              <li key={index}>
                                {topic}
                              </li>
                            )
                          )}
                        </ul>
                      </div>

                      <div className="generated-section">
                        <h3>Project Talking Points</h3>

                        <ul>
                          {interviewPrep[
                            event.id
                          ].project_talking_points?.map(
                            (point, index) => (
                              <li key={index}>
                                {point}
                              </li>
                            )
                          )}
                        </ul>
                      </div>

                      <div className="generated-section">
                        <h3>Questions to Ask the Interviewer</h3>

                        <ul>
                          {interviewPrep[
                            event.id
                          ].questions_to_ask_interviewer?.map(
                            (question, index) => (
                              <li key={index}>
                                {question}
                              </li>
                            )
                          )}
                        </ul>
                      </div>

                      <div className="generated-section">
                        <h3>Preparation Advice</h3>

                        <ul>
                          {interviewPrep[
                            event.id
                          ].preparation_advice?.map(
                            (advice, index) => (
                              <li key={index}>
                                {advice}
                              </li>
                            )
                          )}
                        </ul>
                      </div>
                    </div>
                  )}
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
