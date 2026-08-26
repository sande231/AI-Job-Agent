import { useState } from "react";

function DiscoverJobsPage() {
  const [liveJobs, setLiveJobs] = useState([]);
  const [loadingLiveJobs, setLoadingLiveJobs] = useState(false);
  const [discoveringJobs, setDiscoveringJobs] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [analyzedJobs, setAnalyzedJobs] = useState([]);
  const [skippedJobs, setSkippedJobs] = useState([]);
  const [movingJobId, setMovingJobId] = useState(null);

  const previewLiveJobs = async () => {
    try {
      setLoadingLiveJobs(true);
      setError("");
      setMessage("");

      const response = await fetch(
        "http://127.0.0.1:8000/jobs/live-preview"
      );

      const result = await response.json();

      if (!response.ok) {
        throw new Error(
          result.message || "Unable to retrieve live jobs"
        );
      }

      setLiveJobs(result.jobs || []);

      setMessage(
        `${result.total_jobs || 0} live jobs retrieved.`
      );
    } catch (err) {
      setError(err.message);
    } finally {
      setLoadingLiveJobs(false);
    }
  };

  const discoverAndAnalyze = async () => {
    try {
      setDiscoveringJobs(true);
      setError("");

      setMessage(
        "Searching and analyzing jobs against your resume..."
      );

      const response = await fetch(
        "http://127.0.0.1:8000/jobs/live-discover-and-save",
        {
          method: "POST",
        }
      );

      const result = await response.json();

      if (!response.ok) {
        throw new Error(
          result.message || "Unable to analyze jobs"
        );
      }

      setAnalyzedJobs(result.saved_jobs || []);
      setSkippedJobs(result.skipped_jobs || []);

      setMessage(
        `Analysis complete. Saved ${
          result.saved_count ?? 0
        } jobs and skipped ${
          result.skipped_count ?? 0
        }.`
      );
    } catch (err) {
      setMessage("");
      setError(err.message);
    } finally {
      setDiscoveringJobs(false);
    }
  };

  const moveToApplications = async (job) => {
    try {
      setMovingJobId(job.id);

      const response = await fetch(
        `http://127.0.0.1:8000/discovered-jobs/${job.id}/apply`,
        {
          method: "POST",
        }
      );

      const result = await response.json();

      if (!response.ok) {
        throw new Error(
          result.message || "Unable to move job to applications"
        );
      }

      setAnalyzedJobs((currentJobs) =>
        currentJobs.filter(
          (currentJob) => currentJob.id !== job.id
        )
      );

      setMessage(
        `${job.title} moved to Applications successfully.`
      );
    } catch (err) {
      setError(err.message);
    } finally {
      setMovingJobId(null);
    }
  };

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1>Discover Jobs</h1>
          <p>
            Search live internship opportunities and analyze
            them against your resume.
          </p>
        </div>
      </div>

      <section className="dashboard-section live-discovery-section">
        <div className="section-header">
          <div>
            <h2>Live Job Discovery</h2>

            <p className="section-description">
              Preview current listings or let the AI Job Agent
              analyze opportunities for you.
            </p>
          </div>

          <div className="discovery-actions">
            <button
              className="preview-button"
              onClick={previewLiveJobs}
              disabled={
                loadingLiveJobs || discoveringJobs
              }
            >
              {loadingLiveJobs
                ? "Loading..."
                : "Preview Live Jobs"}
            </button>

            <button
              className="discover-button"
              onClick={discoverAndAnalyze}
              disabled={
                discoveringJobs || loadingLiveJobs
              }
            >
              {discoveringJobs
                ? "Analyzing Jobs..."
                : "Discover & Analyze Jobs"}
            </button>
          </div>
        </div>

        {message && (
          <div className="discovery-message">
            {message}
          </div>
        )}

        {error && (
          <div className="discovery-error">
            {error}
          </div>
        )}
      </section>

      {analyzedJobs.length > 0 && (
        <section className="dashboard-section">
          <div className="section-header">
            <div>
              <h2>AI Recommended Jobs</h2>

              <p className="section-description">
                These opportunities were analyzed against your
                uploaded resume.
              </p>
            </div>

            <span>
              {analyzedJobs.length} recommended
            </span>
          </div>

          <div className="analyzed-job-grid">
            {analyzedJobs.map((job) => (
              <article
                className="analyzed-job-card"
                key={job.id}
              >
                <div className="analyzed-job-header">
                  <div>
                    <span
                      className={`status ${job.status.toLowerCase()}`}
                    >
                      {job.status}
                    </span>

                    <h2>{job.title}</h2>

                    <p className="company">
                      {job.company}
                    </p>

                    <p className="location">
                      {job.location ||
                        "Location not provided"}
                    </p>
                  </div>

                  <div className="analysis-score">
                    <strong>
                      {job.match_score ?? 0}%
                    </strong>

                    <span>Match</span>
                  </div>
                </div>

                {job.score_breakdown && (
                  <div className="score-breakdown-card">
                    <h3>Score Breakdown</h3>

                    <div className="score-breakdown-row">
                      <span>Technical Skills</span>
                      <strong>
                        {job.score_breakdown.technical_skills ?? 0} / 40
                      </strong>
                    </div>

                    <div className="score-breakdown-row">
                      <span>Experience & Projects</span>
                      <strong>
                        {job.score_breakdown.experience_projects ?? 0} / 25
                      </strong>
                    </div>

                    <div className="score-breakdown-row">
                      <span>Education</span>
                      <strong>
                        {job.score_breakdown.education ?? 0} / 15
                      </strong>
                    </div>

                    <div className="score-breakdown-row">
                      <span>Role Relevance</span>
                      <strong>
                        {job.score_breakdown.role_relevance ?? 0} / 10
                      </strong>
                    </div>

                    <div className="score-breakdown-row">
                      <span>Preferred Qualifications</span>
                      <strong>
                        {job.score_breakdown.preferred_qualifications ?? 0} / 10
                      </strong>
                    </div>

                    <div className="score-breakdown-total">
                      <span>Overall Match</span>
                      <strong>
                        {job.match_score ?? 0} / 100
                      </strong>
                    </div>
                  </div>
                )}

                <div className="analysis-section">
                  <h3>Matching Skills</h3>

                  {job.matching_skills?.length > 0 ? (
                    <div className="analysis-skills">
                      {job.matching_skills.map(
                        (skill, index) => (
                          <span
                            className="matching-skill"
                            key={`match-${skill}-${index}`}
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
                </div>

                <div className="analysis-section">
                  <h3>Missing Skills</h3>

                  {job.missing_skills?.length > 0 ? (
                    <div className="analysis-skills">
                      {job.missing_skills.map(
                        (skill, index) => (
                          <span
                            className="missing-skill"
                            key={`missing-${skill}-${index}`}
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
                </div>

                {job.recommendation && (
                  <div className="ai-recommendation">
                    <span>AI Recommendation</span>

                    <p>
                      {job.recommendation}
                    </p>
                  </div>
                )}

                <div className="analyzed-job-footer">
                  {job.job_url && (
                    <a
                      href={job.job_url}
                      target="_blank"
                      rel="noreferrer"
                      className="view-job-secondary"
                    >
                      View Job
                    </a>
                  )}

                  <button
                    className="move-application-button"
                    onClick={() =>
                      moveToApplications(job)
                    }
                    disabled={
                      movingJobId === job.id
                    }
                  >
                    {movingJobId === job.id
                      ? "Moving..."
                      : "Move to Applications"}
                  </button>
                </div>
              </article>
            ))}
          </div>
        </section>
      )}

      {skippedJobs.length > 0 && (
        <section className="dashboard-section">
          <div className="section-header">
            <div>
              <h2>Skipped Jobs</h2>
              <p className="section-description">
                Jobs that were not saved after duplicate checking or AI matching.
              </p>
            </div>

            <span>
              {skippedJobs.length} skipped
            </span>
          </div>

          <div className="skipped-job-list">
            {skippedJobs.map((job, index) => (
              <div
                className="skipped-job-card"
                key={`${job.company}-${job.title}-${index}`}
              >
                <div className="skipped-job-main">
                  <div>
                    <h3>{job.title}</h3>

                    <p className="company">
                      {job.company}
                    </p>

                    <p className="location">
                      {job.location ||
                        "Location not provided"}
                    </p>
                  </div>

                  {job.match_score !== undefined && (
                    <div className="skipped-score">
                      {job.match_score}%
                    </div>
                  )}
                </div>

                <div className="skip-reason">
                  {job.reason}
                </div>

                {job.job_url && (
                  <a
                    href={job.job_url}
                    target="_blank"
                    rel="noreferrer"
                    className="view-job-secondary"
                  >
                    View Job
                  </a>
                )}
              </div>
            ))}
          </div>
        </section>
      )}

      {liveJobs.length > 0 && (
        <section className="dashboard-section">
          <div className="section-header">
            <div>
              <h2>Live Opportunities</h2>
              <p className="section-description">
                Showing {liveJobs.length} current listings.
              </p>
            </div>
          </div>

          <div className="discover-job-grid">
            {liveJobs.map((job, index) => (
              <article
                className="discover-job-card"
                key={`${job.company}-${job.title}-${index}`}
              >
                <div className="discover-job-content">
                  <h3>
                    {job.title || "Untitled Position"}
                  </h3>

                  <p className="company">
                    {job.company ||
                      "Company not provided"}
                  </p>

                  <p className="location">
                    {job.location ||
                      "Location not provided"}
                  </p>
                </div>

                <div className="discover-job-actions">
                  {job.job_url ? (
                    <a
                      href={job.job_url}
                      target="_blank"
                      rel="noreferrer"
                      className="view-job-button"
                    >
                      View Job
                    </a>
                  ) : (
                    <span className="job-link-unavailable">
                      Link unavailable
                    </span>
                  )}
                </div>
              </article>
            ))}
          </div>
        </section>
      )}
    </div>
  );
}

export default DiscoverJobsPage;
