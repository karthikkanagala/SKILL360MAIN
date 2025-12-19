# 🚀 Skill Passport 360 - Backend Technical Documentation

## Overview

Skill Passport 360 is an AI-powered career development platform that analyzes resumes, GitHub profiles, certificates, and other professional data to calculate a holistic career score and provide personalized recommendations.

---

## 🏗️ Architecture

```
backend/
├── main.py                          # FastAPI application entry point
├── requirements.txt                 # Python dependencies
├── career_score_history.json        # Persistent score tracking
├── routers/                         # API route modules
│   ├── resume.py                    # Resume upload & ATS scoring
│   ├── career_score.py              # Holistic career score calculation
│   ├── github.py                    # GitHub profile analysis
│   ├── certificates.py              # Certificate verification
│   ├── interview.py                 # Interview preparation
│   ├── learning.py                  # Course recommendations
│   ├── analytics.py                 # Peer comparison & analytics
│   ├── internship.py                # Internship matching
│   ├── profile.py                   # Profile management
│   ├── mentorship.py                # Mentor matching
│   ├── opportunities.py             # Job opportunities
│   └── gap_analysis.py              # Skill gap analysis
│
└── Evolvex-AI-Carrier-Path-main/src/   # Core ML & processing modules
    ├── parsing.py                   # PDF/DOCX text extraction + OCR
    ├── skills.py                    # Skill extraction engine
    ├── github_analyzer.py           # GitHub API integration
    ├── portfolio_analyzer.py        # Portfolio quality scoring
    ├── certificate_validator.py     # Certificate verification
    ├── internship_matcher.py        # Internship matching algorithm
    ├── interview_prep.py            # Interview question generation
    ├── course_suggestions.py        # Course recommendation engine
    ├── holistic_score.py            # Career score calculation
    ├── fit_classifier.pkl           # Pre-trained ML classifier
    └── local_llm.py                 # Local LLM integration (Ollama)
```

---

## 📊 Data Processing Pipeline

### 1. Resume Processing

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Resume Upload  │───▶│  Text Extraction │───▶│ Skill Extraction│
│  (PDF/DOCX/TXT) │    │  (PyPDF2 + OCR)  │    │ (Pattern Match) │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                        │
                                                        ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐

│   ATS Score     │◀───│  Section Analysis│◀───│  Text Analysis  │
│   (0-100)       │    │  (Keywords/Verbs)│    │  (NLP Features) │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

**How Text Extraction Works:**

| File Type | Method | Library |
|-----------|--------|---------|
| Text PDF | Direct extraction | PyPDF2 |
| Scanned PDF | OCR (Optical Character Recognition) | Tesseract + pdf2image |
| DOCX | Paragraph extraction | python-docx |
| TXT | Direct read | Python built-in |

**ATS Scoring Components:**

| Component | Weight | Description |
|-----------|--------|-------------|
| Length | 15 pts | Resume word count (400+ optimal) |
| Skills | 25 pts | Number of technical skills found |
| Sections | 20 pts | Standard sections (Experience, Education, etc.) |
| Contact | 15 pts | Email, phone, LinkedIn presence |
| Action Verbs | 15 pts | Power verbs (developed, led, implemented) |
| Metrics | 10 pts | Quantified achievements (numbers, %) |

---

### 2. Skill Extraction

**Method: Pattern Matching + NLP**

```python
# Skills are extracted using keyword matching against a curated database
TECH_SKILLS = [
    'Python', 'Java', 'JavaScript', 'TypeScript', 'C++', 'C#',
    'React', 'Angular', 'Vue', 'Node.js', 'Django', 'FastAPI',
    'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes',
    'Machine Learning', 'Deep Learning', 'TensorFlow', 'PyTorch',
    'SQL', 'MongoDB', 'PostgreSQL', 'MySQL', 'Redis',
    # ... 50+ skills
]
```

**Location:** `backend/Evolvex-AI-Carrier-Path-main/src/skills.py`

---

### 3. GitHub Analysis

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  GitHub Username│───▶│  GitHub API      │───▶│  Repository     │
│                 │    │  (Public Data)   │    │  Analysis       │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                        │
                                                        ▼
                       ┌──────────────────┐    ┌─────────────────┐
                       │  Language Stats  │◀───│  Contribution   │
                       │  & Skill Mapping │    │  Scoring        │
                       └──────────────────┘    └─────────────────┘
```

**Metrics Analyzed:**
- Total repositories
- Total stars & forks
- Primary languages used
- Contribution frequency
- Repository quality (README, documentation)

---

### 4. Career Score Calculation (0-1000)

```
┌─────────────────────────────────────────────────────────────┐
│                    HOLISTIC CAREER SCORE                     │
│                         (0 - 1000)                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌───────┐
│  │ Resume  │  │ GitHub  │  │  Certs  │  │Activity │  │Portfolio│
│  │ (200)   │  │ (200)   │  │ (200)   │  │ (200)   │  │ (200)  │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘  └───────┘
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Score Breakdown:**

| Component | Max Points | Based On |
|-----------|------------|----------|
| Resume | 200 | ATS score + skills count |
| GitHub | 200 | Repos, stars, contribution score |
| Certifications | 200 | Verified certificates count |
| Activities | 200 | Extracurricular activities |
| Portfolio | 200 | Project quality & diversity |

---

## 🤖 Machine Learning Components

### 1. Fit Classifier (`fit_classifier.pkl`)

**Purpose:** Classifies job-candidate fit score

**Type:** Scikit-learn classifier (XGBoost/RandomForest)

**Training Data:** Pre-trained on job descriptions vs. candidate profiles

**Usage:**
```python
import joblib
classifier = joblib.load('fit_classifier.pkl')
fit_score = classifier.predict(features)
```

### 2. NER Skill Extractor (`ner_skill_extractor.py`)

**Purpose:** Named Entity Recognition for skill extraction

**Model:** spaCy NER model

**Features:**
- Extracts skills from unstructured text
- Identifies experience levels
- Maps skills to categories

---

## 🧠 How spaCy is Used for NLP Processing

### Overview

spaCy is used in this project for **intelligent skill extraction** from resume text using **PhraseMatcher** - a rule-based matching approach that's faster and more accurate than simple string matching.

### The spaCy Pipeline

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Resume Text   │───▶│   spaCy NLP      │───▶│   Document      │
│   (Raw String)  │    │   Processing     │    │   (Doc Object)  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                        │
                                                        ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Skills List   │◀───│   PhraseMat    │    │   Matching      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### Code Implementation

**File:** `backend/Evolvex-AI-Carrier-Path-main/src/ner_skill_extractor.py`

```python
import spacy
from spacy.matcher import PhraseMatcher

# Step 1: Load spaCy English model
def load_nlp():
    return spacy.load("en_core_web_sm")

def extract_skills_ner(text):
    # Step 2: Process text through spaCy pipeline
    nlp = load_nlp()
    doc = nlp(text)  # Tokenization, POS tagging, NER
    
    # Step 3: Create PhraseMatcher for skill matching
    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    
    # Step 4: Create patterns from skill list
    patterns = [nlp.make_doc(skill) for skill in COMMON_SKILLS]
    matcher.add("SKILLS", patterns)
    
    # Step 5: Find matches in document
    matches = matcher(doc)
    
    # Step 6: Extract matched skill text
    skills_found = list(set([
        doc[start:end].text 
        for match_id, start, end in matches
    ]))
    
    return skills_found
```

### How PhraseMatcher Works

| Step | What Happens | Example |
|------|-------------|---------|
| 1. **Tokenization** | Text split into tokens | "Python developer" → ["Python", "developer"] |
| 2. **Pattern Creation** | Skills converted to Doc patterns | "machine learning" → Doc object |
| 3. **Matching** | Patterns matched against text | Finds "Python" in resume |
| 4. **Extraction** | Matched spans returned | Returns ["Python", "React", "AWS"] |

### Why PhraseMatcher over Simple String Matching?

| Feature | String Match | spaCy PhraseMatcher |
|---------|-------------|---------------------|
| **Speed** | Slower for many patterns | Optimized hash-based lookup |
| **Case Handling** | Manual `.lower()` | Built-in `attr="LOWER"` |
| **Word Boundaries** | Prone to false matches | Respects token boundaries |
| **Multi-word Skills** | Complex regex needed | Handles naturally |

**Example:**
- String match: `"java" in text` might match "java**script**" (false positive)
- PhraseMatcher: Only matches "Java" as complete token ✓

### Skill Database

**File:** `backend/Evolvex-AI-Carrier-Path-main/src/skills.py`

The project maintains a curated list of **200+ skills** across categories:

```python
COMMON_SKILLS = [
    # Programming Languages (27 skills)
    'python', 'java', 'c++', 'javascript', 'typescript', ...
    
    # Web Frameworks (60+ skills)
    'react', 'angular', 'vue', 'django', 'fastapi', 'spring boot', ...
    
    # Data & ML (15 skills)
    'pandas', 'tensorflow', 'pytorch', 'machine learning', ...
    
    # Databases (25 skills)
    'sql', 'mongodb', 'postgresql', 'redis', 'elasticsearch', ...
    
    # Cloud & DevOps (30+ skills)
    'aws', 'azure', 'docker', 'kubernetes', 'terraform', ...
    
    # LLM & AI (10 skills)
    'prompt engineering', 'langchain', 'openai', 'llm', ...
]
```

### Fallback Mechanism

If spaCy model isn't available, the system falls back to **simple pattern matching**:

```python
def extract_skills(text, skills=COMMON_SKILLS):
    found = set()
    text_normalized = re.sub(r'[^a-z0-9]', '', text.lower())
    
    for skill in skills:
        skill_norm = normalize_skill(skill)
        if skill_norm in text_normalized:
            found.add(skill)
    
    return sorted(found)
```

### Installing spaCy Model

```bash
# Install spaCy
pip install spacy

# Download English model
python -m spacy download en_core_web_sm
```

### 3. Local LLM Integration (`local_llm.py`)

**Purpose:** AI-powered text generation and analysis

**Backend:** Ollama with local Llama models

**Capabilities:**
- Resume improvement suggestions
- Project idea generation
- Cover letter writing
- Career path recommendations

---

## 🔄 Data Flow

```
┌──────────────────────────────────────────────────────────────────┐
│                         FRONTEND (React)                          │
│                      http://localhost:3000                        │
└─────────────────────────────┬────────────────────────────────────┘
                              │ API Calls (Axios)
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│                      FASTAPI BACKEND                              │
│                      http://localhost:8000                        │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │   Routers   │  │    Core     │  │     ML      │              │
│  │  (API Endpoints) │  Module    │  │   Models   │              │
│  └─────────────┘  └─────────────┘  └─────────────┘              │
│         │                │                │                      │
│         └────────────────┼────────────────┘                      │
│                          ▼                                        │
│              ┌─────────────────────┐                             │
│              │   Data Processing   │                             │
│              │   & Analysis        │                             │
│              └─────────────────────┘                             │
│                          │                                        │
└──────────────────────────┼───────────────────────────────────────┘
                           ▼
          ┌────────────────────────────────┐
          │     External Services          │
          ├────────────────────────────────┤
          │  • GitHub API                  │
          │  • Ollama (Local LLM)         │
          │  • Web Scraping (Courses)     │
          └────────────────────────────────┘
```

---

## 🗄️ MongoDB Integration

### Configuration

Create a `.env` file in the `backend/` directory:

```env
# MongoDB Configuration
MONGODB_USERNAME=your_username
MONGODB_PASSWORD=your_password
MONGODB_URI=mongodb+srv://username:password@cluster0.mongodb.net/skill_passport_360
MONGODB_DATABASE=skill_passport_360

# Google API Configuration
GOOGLE_API_KEY=your_google_api_key
```

### Database Collections

| Collection | Purpose |
|------------|---------|
| `users` | User accounts |
| `profiles` | User profile data |
| `resumes` | Parsed resume data |
| `career_scores` | Career score history |
| `certificates` | Verified certificates |
| `github_analysis` | GitHub profile analysis |

### Usage Example

```python
from database import MongoDB, get_collection, Collections

# Get database
db = MongoDB.get_database()

# Save profile
profiles = get_collection(Collections.PROFILES)
profiles.insert_one({"user_id": "123", "name": "John"})
```

---

## 🤖 Google Gemini API Integration

### Overview

Google Gemini is integrated as a **fallback** when local ML models (XGBoost) are unavailable.

### Use Cases

| Feature | Primary Method | Fallback (Gemini) |
|---------|---------------|-------------------|
| ATS Scoring | Rule-based + XGBoost | Gemini analysis |
| Skill Extraction | spaCy + Pattern Match | Gemini NER |
| Resume Improvements | Local LLM (Ollama) | Gemini suggestions |
| Interview Questions | Template-based | Gemini generation |

### Fallback Pattern

```python
def analyze_with_fallback(data):
    try:
        # Try XGBoost/ML model first
        result = ml_model.predict(data)
    except Exception:
        # Fallback to Gemini API
        from database import GoogleAPI
        prompt = f"Analyze this data: {data}"
        result = GoogleAPI.generate_content(prompt)
    return result
```

### API Endpoint

```
GET /api/gemini/test    # Test Gemini connection
```

---

## 📁 Data Storage

| Data Type | Storage | Format |
|-----------|---------|--------|
| Career Score History | MongoDB / JSON | BSON/JSON |
| ML Models | `.pkl` files | Pickle (joblib) |
| User Profiles | MongoDB | BSON |
| Session Data | In-memory | Python dict |
| User Uploads | Temporary | Deleted after processing |

---

## 🔌 API Endpoints

### Resume API
```
POST /api/resume/upload          # Upload and analyze resume
POST /api/resume/analyze-text    # Analyze pasted resume text
```

### Career Score API
```
POST /api/career-score/calculate # Calculate holistic score
GET  /api/career-score/history   # Get score history
```

### GitHub API
```
POST /api/github/analyze         # Analyze GitHub profile
POST /api/github/portfolio       # Portfolio analysis
```

### Certificates API
```
POST /api/certificates/verify-url    # Verify certificate URL
POST /api/certificates/analyze-text  # Analyze certificate text
POST /api/certificates/upload-pdf    # Upload certificate PDF
```

### Profile API
```
GET  /api/profile/demo           # Get demo profile data
POST /api/profile/completeness   # Check profile completeness
POST /api/profile/stats          # Get profile statistics
```

---

## 🛠️ Technologies Used

| Category | Technology |
|----------|------------|
| **Backend Framework** | FastAPI |
| **ASGI Server** | Uvicorn |
| **PDF Processing** | PyPDF2, pdf2image |
| **OCR** | Tesseract, pytesseract |
| **NLP** | spaCy |
| **ML** | scikit-learn, XGBoost |
| **Data Processing** | pandas, numpy |
| **HTTP Client** | requests |
| **Document Parsing** | python-docx, BeautifulSoup |
| **PDF Generation** | reportlab |
| **Local LLM** | Ollama |

---

## 🚀 Running the Backend

```bash
# Navigate to backend directory
cd backend

# Install dependencies
pip install -r requirements.txt

# Run the server
python main.py

# Server runs at http://localhost:8000
# API docs at http://localhost:8000/docs
```

---

## 📈 Future Improvements

1. **Deep Learning NER** - Train custom NER model on resume data
2. **Recommendation Engine** - Collaborative filtering for job matching
3. **Resume Generator** - LLM-powered resume writing
4. **Real-time Job Matching** - Integration with job boards APIs
5. **Interview AI** - Voice-based interview practice with feedback

---

## 📝 License

This project is for educational purposes. See main repository for license details.
