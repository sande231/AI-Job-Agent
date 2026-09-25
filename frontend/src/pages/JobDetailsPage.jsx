import { useEffect, useState } from "react";

function JobDetailsPage({
  job,
  onBack,
  onMoveToApplications,
}) {
  const [currentJob, setCurrentJob] = useState(job);
  const [reanalyzing, setReanalyzing] = useState(false);
  const [reanalyzeMessage, setReanalyzeMessage] = useState("");
  const [reanalyzeError, setReanalyzeError] = useState("");

  useEffect(() => {
    setCurrentJob(job);
  }, [job]);
  const handleReanalyze = async () => {
    if (!currentJob?.id) {
      return;
    }

    try {
      setReanalyzing(true);
      setReanalyzeError("");
      setReanalyzeMessage("");

      const response = await fetch(
        `http://127.0.0.1:8000/discovered-jobs/${currentJob.id}/reanalyze`,
        {
          method: "POST",
        }
      );

      const result = await response.json();

      if (!response.ok) {
        throw new Error(
          result.message || "Unable to reanalyze job"
        );
      }

      setCurrentJob(result.job);

      setReanalyzeMessage(
        "Job analysis refreshed successfully."
      );
    } catch (error) {
      setReanalyzeError(error.message);
    } finally {
      setReanalyzing(false);
    }
  };

  if (!currentJob) {
  return (
      <main className="page">
        <div className="page-header">
          <div>
            <p className="eyebrow">AI JOB ANALYSIS</p>
            <h1>Job Details</h1>
          </div>
        </div>

        <section className="dashboard-section">
          <div className="empty-card">
            No job selected.
          </div>

          <button
            className="secondary-button"
            onClick={onBack}
          >
            Back to Discover Jobs
          </button>
        </section>
      </main>
    );
  }

  const breakdown = currentJob.score_breakdown || {};

  return (
    <main className="page job-details-page">
      <div className="page-header">
        <div>
          <p className="eyebrow">
            AI JOB ANALYSIS
          </p>

          <h1>{currentJob.title}</h1>

          <p className="page-subtitle">
            {currentJob.company}
            {currentJob.location
              ? ` • ${currentJob.location}`
              : ""}
          </p>
        </div>

        <button
          className="secondary-button"
          onClick={onBack}
        >
          ← Back to Discover Jobs
        </button>
      </div>

      <section className="job-details-summary">
        <div className="job-details-score">
          <strong>
            {currentJob.match_score ?? 0}%
          </strong>

          <span>Overall Match</span>
        </div>

        <div>
          <p className="job-details-label">
            STATUS
          </p>

          <span
            className={`status ${
              currentJob.status?.toLowerCase() || "review"
            }`}
          >
            {currentJob.status || "Review"}
          </span>
        </div>

        <div>
          <p className="job-details-label">
            SOURCE
          </p>

          <strong>
            {currentJob.source || "Unknown"}
          </strong>
        </div>
      </section>

      {currentJob.score_breakdown && (
        <section className="dashboard-section">
          <div className="section-header">
            <div>
              <h2>Score Breakdown</h2>

              <p className="section-description">
                How the AI calculated your job match.
              </p>
            </div>
          </div>

          <div className="job-score-grid">
            <div className="job-score-item">
              <span>Technical Skills</span>
              <strong>
                {breakdown.technical_skills ?? 0}
                <small> / 40</small>
              </strong>
            </div>

            <div className="job-score-item">
              <span>Experience & Projects</span>
              <strong>
                {breakdown.experience_projects ?? 0}
                <small> / 25</small>
              </strong>
            </div>

            <div className="job-score-item">
              <span>Education</span>
              <strong>
                {breakdown.education ?? 0}
                <small> / 15</small>
              </strong>
            </div>

            <div className="job-score-item">
              <span>Role Relevance</span>
              <strong>
                {breakdown.role_relevance ?? 0}
                <small> / 10</small>
              </strong>
            </div>

            <div className="job-score-item">
              <span>Preferred Qualifications</span>
              <strong>
                {breakdown.preferred_qualifications ?? 0}
                <small> / 10</small>
              </strong>
            </div>
          </div>
        </section>
      )}

      <div className="job-details-columns">
        <section className="dashboard-section">
          <h2>Matching Skills</h2>

          {currentJob.matching_skills?.length > 0 ? (
            <div className="analysis-skills">
              {currentJob.matching_skills.map(
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
            <p className="analysis-empty">
              No matching skills returned.
            </p>
          )}
        </section>

        <section className="dashboard-section">
          <h2>Missing Skills</h2>

          {currentJob.missing_skills?.length > 0 ? (
            <div className="analysis-skills">
              {currentJob.missing_skills.map(
                (skill, index) => (
                  <span
                    className="missing-skill"
                    key={`${skill}-${index}`}
                  >
                    {skill}
                  </span>
                )
              )}
            </div>
          ) : (
            <p className="analysis-empty">
              No major missing skills identified.
            </p>
          )}
        </section>
      </div>

      {currentJob.strengths?.length > 0 && (
        <section className="dashboard-section">
          <h2>Strengths</h2>

          <ul className="analysis-detail-list">
            {currentJob.strengths.map(
              (strength, index) => (
                <li key={index}>
                  {strength}
                </li>
              )
            )}
          </ul>
        </section>
      )}

      {currentJob.gaps?.length > 0 && (
        <section className="dashboard-section">
          <h2>Areas to Improve</h2>

          <ul className="analysis-detail-list">
            {currentJob.gaps.map(
              (gap, index) => (
                <li key={index}>
                  {gap}
                </li>
              )
            )}
          </ul>
        </section>
      )}

      {currentJob.recommendation && (
        <section className="dashboard-section">
          <h2>AI Recommendation</h2>

          <div className="job-ai-recommendation">
            <p>{currentJob.recommendation}</p>
          </div>
        </section>
      )}

      {currentJob.description && (
        <section className="dashboard-section">
          <h2>Job Description</h2>

          <p className="job-description-text">
            {currentJob.description}
          </p>
        </section>
      )}

      {reanalyzeMessage && (
        <div className="profile-success">
          {reanalyzeMessage}
        </div>
      )}

      {reanalyzeError && (
        <div className="discovery-error">
          {reanalyzeError}
        </div>
      )}

      <section className="job-details-actions">
        {currentJob.job_url && (
          <a
            href={currentJob.job_url}
            target="_blank"
            rel="noreferrer"
            className="view-job-secondary"
          >
            View Original Job
          </a>
        )}

        {currentJob.id && (
          <button
            className="reanalyze-button"
            onClick={handleReanalyze}
            disabled={reanalyzing}
          >
            {reanalyzing
              ? "Reanalyzing..."
              : "Reanalyze Job"}
          </button>
        )}

        {currentJob.id && (
          <button
            className="move-application-button"
            onClick={() =>
              onMoveToApplications?.(job)
            }
          >
            Move to Applications
          </button>
        )}
      </section>
    </main>
  );
}

export default JobDetailsPage;
