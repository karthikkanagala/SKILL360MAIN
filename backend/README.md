# Skill Passport 360 - FastAPI Backend

RESTful API backend for Skill Passport 360 built with FastAPI.

## Features

- 🚀 **FastAPI** - Modern, fast web framework
- 🔌 **RESTful API** - Clean endpoint structure
- 📦 **Modular Routers** - Organized by feature
- 🔒 **CORS Enabled** - Ready for React frontend
- 🐍 **Python Integration** - Uses existing ML models and logic

## Getting Started

```bash
# Install dependencies
pip install -r requirements.txt

# Run server
python main.py

# Or with uvicorn directly
uvicorn main:app --reload --port 8000
```

The API will run on `http://localhost:8000` with auto-generated docs at `http://localhost:8000/docs`.

## API Endpoints

### Resume
- `POST /api/resume/upload` - Upload and analyze resume
- `POST /api/resume/analyze-text` - Analyze resume text

### Career Score
- `POST /api/career-score/calculate` - Calculate career score
- `GET /api/career-score/history` - Get score history

### GitHub
- `POST /api/github/analyze` - Analyze GitHub profile
- `POST /api/github/portfolio` - Analyze portfolio

### Interview
- `POST /api/interview/generate-questions` - Generate interview questions
- `POST /api/interview/evaluate-answer` - Evaluate answer

### Learning
- `POST /api/learning/courses/search` - Search courses
- `POST /api/learning/courses/ai-recommendations` - AI recommendations
- `POST /api/learning/learning-path` - Generate learning path
- `POST /api/learning/project-ideas` - Generate project ideas

### Analytics
- `POST /api/analytics/peer-comparison` - Peer comparison
- `POST /api/analytics/company-scoring` - Company-specific scoring

### Internship
- `POST /api/internship/match` - Match internships
- `GET /api/internship/list` - List all internships

### Profile
- `POST /api/profile/completeness` - Check profile completeness
- `GET /api/profile/demo` - Get demo profile
- `POST /api/profile/stats` - Get profile stats

## Project Structure

```
backend/
├── main.py              # FastAPI app entry point
├── routers/
│   ├── resume.py
│   ├── career_score.py
│   ├── github.py
│   ├── interview.py
│   ├── learning.py
│   ├── analytics.py
│   ├── internship.py
│   └── profile.py
└── requirements.txt
```

## 📚 Technical Documentation

For detailed information about:
- **How the backend works**
- **Data processing pipeline**
- **ML models and training**
- **Career score calculation**
- **API architecture**

See **[TECHNICAL_DOCUMENTATION.md](./TECHNICAL_DOCUMENTATION.md)**

## 🤖 ML & Data Processing Summary

| Component | Method | Description |
|-----------|--------|-------------|
| **Resume Parsing** | PyPDF2 + OCR | Extracts text from PDF/DOCX files |
| **Skill Extraction** | Pattern Matching | Matches 50+ technical skills |
| **ATS Scoring** | Rule-Based (6 factors) | Scores resume quality 0-100 |
| **Career Score** | Weighted Sum | Combines 5 components (0-1000) |
| **Fit Classifier** | Pre-trained XGBoost | Job-candidate matching |
| **NER Extraction** | spaCy | Named entity recognition |

## 🔧 Dependencies

- **FastAPI** - Web framework
- **PyPDF2** - PDF text extraction
- **Tesseract** - OCR for scanned PDFs
- **spaCy** - NLP processing
- **scikit-learn** - ML models
- **XGBoost** - Classification
