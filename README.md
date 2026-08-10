# AI Job Application Agent

An intelligent backend system that helps job seekers automate resume analysis, job matching, and application tracking using Python, FastAPI, and AI integration.

## Overview

The AI Job Application Agent is designed to streamline the job search process by:

- **Resume Parsing**: Extract structured information from PDF resumes
- **Candidate Profiling**: Automatically build candidate profiles from resume data
- **Job Matching**: Compare candidate skills with job requirements using keyword and semantic analysis
- **Application Tracking**: Manage and monitor job applications throughout the hiring process
- **AI Integration**: Leverage LLMs for intelligent resume analysis and recommendations

## Features

### Current Features ✅

- FastAPI REST API with automatic Swagger documentation
- PDF resume upload and text extraction
- Candidate profile creation and management
- Job matching with skill comparison
- SQLite database for persistent storage
- Application tracker (CRUD operations)
- Match score calculation with recommendations

### Upcoming Features 🚀

- AI-powered skill extraction from resumes
- Semantic job matching using embeddings
- Resume tailoring based on job descriptions
- Automated cover letter generation
- Advanced job search and filtering
- Job ranking by match score
- Frontend dashboard

## Technology Stack

### Backend
- **Framework**: FastAPI 0.141.1
- **Web Server**: Uvicorn
- **Data Validation**: Pydantic 2.13.4
- **Database**: SQLite3
- **File Processing**: PyPDF 6.15.0
- **Language**: Python 3.x

### Planned AI Integration
- OpenAI API
- Google Gemini
- Anthropic Claude
- Other LLM providers (pluggable architecture)

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/sande231/AI-Job-Agent.git
   cd AI-Job-Agent
   ```

2. **Navigate to backend**
   ```bash
   cd backend
   ```

3. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # macOS/Linux
   # or
   venv\Scripts\activate  # Windows
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Quick Start

### Run the Server

```bash
uvicorn main:app --reload
```

The server will start at `http://127.0.0.1:8000`

### Access API Documentation

- **Swagger UI**: http://127.0.0.1:8000/docs
- **OpenAPI Schema**: http://127.0.0.1:8000/openapi.json

## API Endpoints

### Profile Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/profile` | Retrieve candidate profile |
| POST | `/profile` | Create/update candidate profile |

### Job Matching

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/match-job` | Analyze job match with candidate |

### Applications

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/applications` | Save new application |
| GET | `/applications` | Retrieve all applications |
| PUT | `/applications/{id}/status` | Update application status |
| DELETE | `/applications/{id}` | Delete application |

### Resume Processing

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/upload-resume` | Upload and extract resume PDF |

### General

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome message |
| GET | `/about` | Project information |

## Usage Examples

### 1. Create Candidate Profile

```bash
curl -X POST http://localhost:8000/profile \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Sandeep Shah",
    "education": "Bachelor in Computer Science",
    "career_goal": "AI Internship",
    "skills": ["Python", "FastAPI", "React", "Machine Learning", "Docker"]
  }'
```

### 2. Upload Resume

```bash
curl -X POST http://localhost:8000/upload-resume \
  -F "file=@resume.pdf"
```

### 3. Analyze Job Match

```bash
curl -X POST http://localhost:8000/match-job \
  -H "Content-Type: application/json" \
  -d '{
    "profile": {
      "name": "Sandeep Shah",
      "skills": ["Python", "FastAPI", "Machine Learning"]
    },
    "job": {
      "title": "AI Intern",
      "company": "Tech Corp",
      "description": "Seeking Python, FastAPI, and ML experience"
    }
  }'
```

### 4. Save Application

```bash
curl -X POST http://localhost:8000/applications \
  -H "Content-Type: application/json" \
  -d '{
    "title": "ML Internship",
    "company": "Google",
    "description": "Machine Learning internship position",
    "status": "Applied"
  }'
```

## Project Structure

```
AI-Job-Agent/
├── README.md
├── .gitignore
│
└── backend/
    ├── main.py                 # FastAPI application entry point
    ├── requirements.txt        # Python dependencies
    ├── applications.db         # SQLite database (local)
    │
    ├── models/                 # Pydantic data models
    │   ├── application.py
    │   ├── job.py
    │   ├── profile.py
    │   ├── match_request.py
    │   └── status_update.py
    │
    ├── services/               # Business logic
    │   ├── job_matcher.py      # Job matching algorithm
    │   └── resume_parser.py    # PDF text extraction
    │
    ├── database/               # Database operations
    │   └── database.py
    │
    └── venv/                   # Virtual environment (git-ignored)
```

## Architecture

The application follows a modular architecture:

```
main.py (Routes & FastAPI setup)
   ├── models/ (Data validation & structure)
   ├── services/ (Business logic)
   └── database/ (Data persistence)
```

**Benefits:**
- Separation of concerns
- Easy to test and maintain
- Scalable for future features
- Clear responsibilities for each module

## Development Roadmap

### Phase 1: Backend Foundation ✅
Core FastAPI setup, basic endpoints, and data models

### Phase 2: Job Matching ✅
Keyword-based job matching with skill comparison

### Phase 3: Application Tracker ✅
CRUD operations for job applications

### Phase 4: Resume Processing 🔄
PDF parsing and skill extraction (In Progress)

### Phase 5: AI Integration 📋
LLM-powered resume analysis and matching

### Phase 6: Resume Tailoring 📋
Automated resume customization for jobs

### Phase 7: Cover Letter Generation 📋
AI-generated customized cover letters

### Phase 8-10: Advanced Features 📋
Job search, ranking, and full AI agent workflow

## Configuration

### Environment Variables

For future AI integration, create a `.env` file (see `.env.example`):

```bash
OPENAI_API_KEY=your_key_here
# Other LLM provider keys can be added here
```

**Important**: Never commit `.env` to version control. It's listed in `.gitignore`.

## Database

The application uses SQLite for local development.

**Database File**: `backend/applications.db`

**Schema**:
```sql
CREATE TABLE applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    company TEXT NOT NULL,
    description TEXT NOT NULL,
    status TEXT NOT NULL
);
```

**Application Status Values:**
- `Saved`
- `Applied`
- `Interview`
- `Rejected`
- `Offer`

## Responsible AI Guidelines

This project follows strict responsible AI principles:

1. ✅ Never invent candidate experience
2. ✅ Never invent education or certifications
3. ✅ Never claim unknown skills
4. ✅ Clearly distinguish required vs. preferred skills
5. ✅ Preserve resume factual accuracy
6. ✅ User controls all submissions
7. ✅ Transparent AI-generated content

## Testing

### Using Swagger UI

1. Navigate to http://localhost:8000/docs
2. Try endpoints directly from the browser interface
3. View request/response examples

### Example Test Workflow

1. Create a candidate profile (`POST /profile`)
2. Upload a resume (`POST /upload-resume`)
3. Save a job application (`POST /applications`)
4. Match candidate with job (`POST /match-job`)
5. Check applications (`GET /applications`)

## Future Enhancements

- [ ] PostgreSQL for production
- [ ] Authentication & authorization
- [ ] Email notifications
- [ ] Calendar integration
- [ ] Advanced filtering & search
- [ ] Data export (PDF, CSV)
- [ ] Job board API integrations
- [ ] Deployment to cloud (AWS, Heroku)

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Learning Outcomes

This project demonstrates:

- Backend API development with FastAPI
- REST API design principles
- Database design and SQL
- File upload and processing
- PDF parsing and text extraction
- Job matching algorithms
- CRUD operations
- Pydantic data validation
- Git and version control
- Responsible AI development
- Clean code architecture

## Roadmap for Interviews

This project can be explained in technical interviews by covering:

1. **Architecture**: Modular design with separate concerns
2. **Features**: Resume parsing, matching, tracking
3. **Technical Decisions**: Why FastAPI, SQLite, Pydantic
4. **Scalability**: Path to PostgreSQL, async processing
5. **AI Integration**: Pluggable LLM architecture
6. **Responsible AI**: Safeguards against hallucination

## License

This project is open source and available under the MIT License.

## Author

**Sandeep Shah**
- GitHub: [@sande231](https://github.com/sande231)
- Email: [Your Email]

## Support

For issues, questions, or suggestions:

- Open an [Issue](https://github.com/sande231/AI-Job-Agent/issues)
- Check existing [Documentation](./backend/README.md)
- Review [API Docs](http://localhost:8000/docs) (when running locally)

---

**Status**: Active Development 🚀

**Last Updated**: 2026