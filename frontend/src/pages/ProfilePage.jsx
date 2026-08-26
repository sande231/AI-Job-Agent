import { useEffect, useState } from "react";

function ProfilePage() {
  const [profile, setProfile] = useState(null);
  const [resumeFile, setResumeFile] = useState(null);

  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);

  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const loadProfile = async () => {
    try {
      setLoading(true);
      setError("");

      const response = await fetch(
        "http://127.0.0.1:8000/profile"
      );

      if (!response.ok) {
        throw new Error("Unable to load profile");
      }

      const data = await response.json();

      setProfile(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadProfile();
  }, []);

  const handleResumeUpload = async () => {
    if (!resumeFile) {
      setError("Please select a PDF resume first.");
      return;
    }

    if (
      resumeFile.type !== "application/pdf" &&
      !resumeFile.name.toLowerCase().endsWith(".pdf")
    ) {
      setError("Please select a PDF file.");
      return;
    }

    try {
      setUploading(true);
      setError("");
      setMessage("");

      const formData = new FormData();

      formData.append("file", resumeFile);

      const response = await fetch(
        "http://127.0.0.1:8000/upload-resume",
        {
          method: "POST",
          body: formData,
        }
      );

      const result = await response.json();

      if (!response.ok) {
        throw new Error(
          result.detail ||
            result.message ||
            "Resume upload failed"
        );
      }

      setMessage(
        result.message ||
          "Resume uploaded successfully."
      );

      setResumeFile(null);

      const fileInput =
        document.getElementById("resume-file");

      if (fileInput) {
        fileInput.value = "";
      }

      await loadProfile();
    } catch (err) {
      setError(err.message);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="page">
      <div className="page-header dashboard-page-header">
        <div>
          <h1>Profile & Resume</h1>

          <p>
            Manage your candidate profile and the resume used
            by the AI Job Agent.
          </p>
        </div>

        <button
          className="dashboard-refresh"
          onClick={loadProfile}
          disabled={loading}
        >
          {loading ? "Refreshing..." : "Refresh Profile"}
        </button>
      </div>

      {message && (
        <div className="profile-success">
          {message}
        </div>
      )}

      {error && (
        <div className="discovery-error">
          {error}
        </div>
      )}

      <section className="profile-layout">
        <div className="profile-main-card">
          <div className="profile-card-header">
            <div className="profile-large-avatar">
              {profile?.name
                ? profile.name
                    .charAt(0)
                    .toUpperCase()
                : "AI"}
            </div>

            <div>
              <span className="profile-label">
                Candidate
              </span>

              <h2>
                {profile?.name ||
                  "Candidate Profile"}
              </h2>

              <p>
                {profile?.career_goal ||
                  "Career goal not available"}
              </p>
            </div>
          </div>

          <div className="profile-information">
            <div>
              <span className="meta-label">
                Education
              </span>

              <strong>
                {profile?.education ||
                  "Not provided"}
              </strong>
            </div>

            <div>
              <span className="meta-label">
                Career Goal
              </span>

              <strong>
                {profile?.career_goal ||
                  "Not provided"}
              </strong>
            </div>
          </div>
        </div>

        <div className="resume-upload-card">
          <div className="resume-upload-icon">
            PDF
          </div>

          <h2>Resume</h2>

          <p>
            Upload a PDF resume and the AI Job Agent will
            extract your skills, education, experience,
            and projects.
          </p>

          <label
            htmlFor="resume-file"
            className="resume-file-label"
          >
            Choose PDF Resume
          </label>

          <input
            id="resume-file"
            type="file"
            accept=".pdf,application/pdf"
            className="resume-file-input"
            onChange={(event) => {
              setResumeFile(
                event.target.files?.[0] || null
              );

              setError("");
              setMessage("");
            }}
          />

          {resumeFile && (
            <div className="selected-resume">
              <span>Selected file</span>

              <strong>
                {resumeFile.name}
              </strong>
            </div>
          )}

          <button
            className="resume-upload-button"
            onClick={handleResumeUpload}
            disabled={
              uploading || !resumeFile
            }
          >
            {uploading
              ? "Analyzing Resume..."
              : "Upload & Analyze Resume"}
          </button>
        </div>
      </section>

      <section className="dashboard-section">
        <div className="section-header">
          <div>
            <h2>Skills</h2>

            <p className="section-description">
              Skills currently associated with your
              candidate profile.
            </p>
          </div>

          <span>
            {profile?.skills?.length || 0} skills
          </span>
        </div>

        {profile?.skills?.length > 0 ? (
          <div className="skills-container">
            {profile.skills.map(
              (skill, index) => (
                <span
                  className="skill-chip"
                  key={`${skill}-${index}`}
                >
                  {skill}
                </span>
              )
            )}
          </div>
        ) : (
          <div className="empty-card">
            No skills found.
          </div>
        )}
      </section>

      <section className="dashboard-section">
        <div className="section-header">
          <div>
            <h2>Experience</h2>
            <p className="section-description">
              Experience extracted from your uploaded resume.
            </p>
          </div>
        </div>

        {profile?.experience?.length > 0 ? (
          <div className="profile-detail-list">
            {profile.experience.map((item, index) => (
              <div
                className="profile-detail-card"
                key={`experience-${index}`}
              >
                {typeof item === "string" ? (
                  <p>{item}</p>
                ) : (
                  <pre>
                    {JSON.stringify(item, null, 2)}
                  </pre>
                )}
              </div>
            ))}
          </div>
        ) : (
          <div className="empty-card">
            No experience extracted from the resume.
          </div>
        )}
      </section>

      <section className="dashboard-section">
        <div className="section-header">
          <div>
            <h2>Projects</h2>
            <p className="section-description">
              Projects extracted from your uploaded resume.
            </p>
          </div>
        </div>

        {profile?.projects?.length > 0 ? (
          <div className="profile-detail-list">
            {profile.projects.map((item, index) => (
              <div
                className="profile-detail-card"
                key={`project-${index}`}
              >
                {typeof item === "string" ? (
                  <p>{item}</p>
                ) : (
                  <pre>
                    {JSON.stringify(item, null, 2)}
                  </pre>
                )}
              </div>
            ))}
          </div>
        ) : (
          <div className="empty-card">
            No projects extracted from the resume.
          </div>
        )}
      </section>

      <section className="dashboard-section">
        <div className="profile-agent-info">
          <div>
            <h2>How your profile is used</h2>

            <p>
              The AI Job Agent compares your candidate
              profile with internship requirements when
              analyzing live jobs.
            </p>
          </div>

          <div className="agent-flow">
            <span>Resume</span>
            <strong>→</strong>
            <span>Profile</span>
            <strong>→</strong>
            <span>Job Matching</span>
            <strong>→</strong>
            <span>Recommendations</span>
          </div>
        </div>
      </section>
    </div>
  );
}

export default ProfilePage;
