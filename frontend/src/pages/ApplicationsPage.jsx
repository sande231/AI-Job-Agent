import { useEffect, useState } from "react";

function ApplicationsPage() {
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [interviewDates, setInterviewDates] = useState({});
  const [notesDrafts, setNotesDrafts] = useState({});

  const [updatingStatusId, setUpdatingStatusId] = useState(null);
  const [schedulingInterviewId, setSchedulingInterviewId] = useState(null);
  const [savingNotesId, setSavingNotesId] = useState(null);
  const [deletingId, setDeletingId] = useState(null);
  const [generatingMaterialsId, setGeneratingMaterialsId] =
    useState(null);

  const [applicationMaterials, setApplicationMaterials] =
    useState({});

  const loadApplications = async () => {
    try {
      setLoading(true);
      setError("");

      const response = await fetch(
        "http://127.0.0.1:8000/applications"
      );

      if (!response.ok) {
        throw new Error("Failed to load applications");
      }

      const data = await response.json();

      setApplications(data.applications || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadApplications();
  }, []);

  const handleStatusChange = async (
    applicationId,
    newStatus
  ) => {
    try {
      setUpdatingStatusId(applicationId);

      const response = await fetch(
        `http://127.0.0.1:8000/applications/${applicationId}/status`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            status: newStatus,
          }),
        }
      );

      const result = await response.json();

      if (!response.ok) {
        throw new Error(
          result.message ||
            "Unable to update application status"
        );
      }

      await loadApplications();
    } catch (err) {
      alert(err.message);
    } finally {
      setUpdatingStatusId(null);
    }
  };

  const handleScheduleInterview = async (
    applicationId
  ) => {
    const interviewDate =
      interviewDates[applicationId];

    if (!interviewDate) {
      alert("Please select an interview date and time.");
      return;
    }

    try {
      setSchedulingInterviewId(applicationId);

      const formattedDate =
        interviewDate.replace("T", " ") + ":00";

      const response = await fetch(
        `http://127.0.0.1:8000/applications/${applicationId}/interview`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            interview_date: formattedDate,
          }),
        }
      );

      const result = await response.json();

      if (!response.ok) {
        throw new Error(
          result.message ||
            "Unable to schedule interview"
        );
      }

      setInterviewDates((previous) => ({
        ...previous,
        [applicationId]: "",
      }));

      await loadApplications();
    } catch (err) {
      alert(err.message);
    } finally {
      setSchedulingInterviewId(null);
    }
  };

  const handleSaveNotes = async (
    applicationId
  ) => {
    const notes =
      notesDrafts[applicationId];

    if (notes === undefined) {
      alert("Please enter notes first.");
      return;
    }

    try {
      setSavingNotesId(applicationId);

      const response = await fetch(
        `http://127.0.0.1:8000/applications/${applicationId}/notes`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            notes,
          }),
        }
      );

      const result = await response.json();

      if (!response.ok) {
        throw new Error(
          result.message ||
            "Unable to save application notes"
        );
      }

      await loadApplications();
    } catch (err) {
      alert(err.message);
    } finally {
      setSavingNotesId(null);
    }
  };

  const handleDeleteApplication = async (
    applicationId
  ) => {
    const confirmed = window.confirm(
      "Delete this application?"
    );

    if (!confirmed) {
      return;
    }

    try {
      setDeletingId(applicationId);

      const response = await fetch(
        `http://127.0.0.1:8000/applications/${applicationId}`,
        {
          method: "DELETE",
        }
      );

      const result = await response.json();

      if (!response.ok) {
        throw new Error(
          result.message ||
            "Unable to delete application"
        );
      }

      await loadApplications();
    } catch (err) {
      alert(err.message);
    } finally {
      setDeletingId(null);
    }
  };

  const handleGenerateMaterials = async (
    applicationId
  ) => {
    try {
      setGeneratingMaterialsId(applicationId);

      const response = await fetch(
        `http://127.0.0.1:8000/applications/${applicationId}/generate-materials`,
        {
          method: "POST",
        }
      );

      const result = await response.json();

      if (!response.ok) {
        throw new Error(
          result.message ||
            "Unable to generate application materials"
        );
      }

      setApplicationMaterials((previous) => ({
        ...previous,
        [applicationId]: result.materials,
      }));
    } catch (err) {
      alert(err.message);
    } finally {
      setGeneratingMaterialsId(null);
    }
  };

  return (
    <div className="page">
      <div className="page-header dashboard-page-header">
        <div>
          <h1>Applications</h1>
          <p>
            Track and manage every stage of your job
            applications.
          </p>
        </div>

        <button
          className="dashboard-refresh"
          onClick={loadApplications}
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

      {loading && applications.length === 0 ? (
        <div className="page-placeholder">
          <h2>Loading applications...</h2>
        </div>
      ) : applications.length === 0 ? (
        <div className="page-placeholder">
          <h2>No applications yet</h2>
          <p>
            Move a discovered job into Applications to start
            tracking it here.
          </p>
        </div>
      ) : (
        <div className="applications-list">
          {applications.map((application) => (
            <article
              className="application-card"
              key={application.id}
            >
              <div className="application-card-header">
                <div>
                  <h2>{application.title}</h2>

                  <p className="company">
                    {application.company}
                  </p>

                  <p className="location">
                    {application.location ||
                      "Location not provided"}
                  </p>
                </div>

                <div className="application-match">
                  {application.match_score !== null
                    ? `${application.match_score}%`
                    : "—"}
                </div>
              </div>

              <div className="application-meta-grid">
                <div>
                  <span className="meta-label">
                    Status
                  </span>

                  <select
                    className="status-select"
                    value={application.status}
                    disabled={
                      updatingStatusId === application.id
                    }
                    onChange={(event) =>
                      handleStatusChange(
                        application.id,
                        event.target.value
                      )
                    }
                  >
                    <option value="Saved">Saved</option>
                    <option value="Applied">Applied</option>
                    <option value="Assessment">Assessment</option>
                    <option value="Interview">Interview</option>
                    <option value="Offer">Offer</option>
                    <option value="Rejected">Rejected</option>
                  </select>
                </div>

                <div>
                  <span className="meta-label">
                    Date Applied
                  </span>

                  <strong>
                    {application.date_applied || "—"}
                  </strong>
                </div>

                <div>
                  <span className="meta-label">
                    Deadline
                  </span>

                  <strong>
                    {application.deadline || "—"}
                  </strong>
                </div>

                <div>
                  <span className="meta-label">
                    Job Link
                  </span>

                  {application.job_url ? (
                    <a
                      href={application.job_url}
                      target="_blank"
                      rel="noreferrer"
                      className="application-link"
                    >
                      Open Job
                    </a>
                  ) : (
                    <strong>—</strong>
                  )}
                </div>
              </div>

              <div className="application-workflow-grid">
                <div className="application-panel">
                  <h3>Interview</h3>

                  <p className="current-interview">
                    {application.interview_date
                      ? `Current: ${application.interview_date}`
                      : "No interview scheduled"}
                  </p>

                  <div className="interview-controls">
                    <input
                      type="datetime-local"
                      className="interview-input"
                      value={
                        interviewDates[application.id] || ""
                      }
                      onChange={(event) =>
                        setInterviewDates((previous) => ({
                          ...previous,
                          [application.id]:
                            event.target.value,
                        }))
                      }
                    />

                    <button
                      className="schedule-button"
                      onClick={() =>
                        handleScheduleInterview(
                          application.id
                        )
                      }
                      disabled={
                        schedulingInterviewId ===
                        application.id
                      }
                    >
                      {schedulingInterviewId ===
                      application.id
                        ? "Saving..."
                        : application.interview_date
                        ? "Update Interview"
                        : "Schedule Interview"}
                    </button>
                  </div>
                </div>

                <div className="application-panel">
                  <h3>Notes</h3>

                  <textarea
                    className="notes-input"
                    placeholder="Add notes..."
                    value={
                      notesDrafts[application.id] !==
                      undefined
                        ? notesDrafts[application.id]
                        : application.notes || ""
                    }
                    onChange={(event) =>
                      setNotesDrafts((previous) => ({
                        ...previous,
                        [application.id]:
                          event.target.value,
                      }))
                    }
                  />

                  <button
                    className="notes-button"
                    onClick={() =>
                      handleSaveNotes(application.id)
                    }
                    disabled={
                      savingNotesId === application.id
                    }
                  >
                    {savingNotesId === application.id
                      ? "Saving..."
                      : "Save Notes"}
                  </button>
                </div>
              </div>

              <div className="application-materials-panel">
                <button
                  className="generate-materials-button"
                  onClick={() =>
                    handleGenerateMaterials(application.id)
                  }
                  disabled={
                    generatingMaterialsId === application.id
                  }
                >
                  {generatingMaterialsId === application.id
                    ? "Generating..."
                    : "Generate Application Materials"}
                </button>

                {applicationMaterials[application.id] && (
                  <div className="generated-materials">
                    <div className="generated-section">
                      <h3>Cover Letter Draft</h3>

                      <pre className="cover-letter-output">
                        {
                          applicationMaterials[
                            application.id
                          ].cover_letter
                        }
                      </pre>
                    </div>

                    <div className="generated-section">
                      <h3>Resume Suggestions</h3>

                      {applicationMaterials[
                        application.id
                      ].resume_suggestions?.length > 0 ? (
                        <ul>
                          {applicationMaterials[
                            application.id
                          ].resume_suggestions.map(
                            (suggestion, index) => (
                              <li key={index}>
                                {suggestion}
                              </li>
                            )
                          )}
                        </ul>
                      ) : (
                        <p>No resume suggestions returned.</p>
                      )}
                    </div>

                    <div className="generated-section">
                      <h3>Skills to Emphasize</h3>

                      {applicationMaterials[
                        application.id
                      ].skills_to_emphasize?.length > 0 ? (
                        <div className="analysis-skills">
                          {applicationMaterials[
                            application.id
                          ].skills_to_emphasize.map(
                            (skill, index) => (
                              <span
                                className="matching-skill"
                                key={`${skill}-${index}`}
                              >
                                {skill}
                              </span>
                            )
                          )}
                        </div>
                      ) : (
                        <p>No skills returned.</p>
                      )}
                    </div>
                  </div>
                )}
              </div>

              <div className="application-card-footer">
                <span>
                  Application #{application.id}
                </span>

                <button
                  className="delete-application-button"
                  onClick={() =>
                    handleDeleteApplication(
                      application.id
                    )
                  }
                  disabled={
                    deletingId === application.id
                  }
                >
                  {deletingId === application.id
                    ? "Deleting..."
                    : "Delete"}
                </button>
              </div>
            </article>
          ))}
        </div>
      )}
    </div>
  );
}

export default ApplicationsPage;
