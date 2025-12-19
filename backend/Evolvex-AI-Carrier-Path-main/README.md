# 🚀 Skill360 - Holistic Career Development Platform

> **AI-powered comprehensive career assessment and development platform combining resume analysis, portfolio evaluation, certificate validation, internship matching, and holistic career scoring.**

[![Python](https://img.shields.io/badge/Python-3.11+-blue)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-Cloud-red)](https://streamlit.io)
[![OpenRouter](https://img.shields.io/badge/OpenRouter-AI-green)](https://openrouter.ai)

---

## 📋 Table of Contents
- [Overview](#-overview)
- [Key Features](#-key-features)
- [Technology Stack](#-technology-stack)
- [Quick Start](#-quick-start)
- [Project Structure](#-project-structure)
- [Features in Detail](#-features-in-detail)
- [API Integration](#-api-integration)
- [Usage Examples](#-usage-examples)
- [Contributing](#-contributing)

---

## 🎯 Overview

**Skill360** is an enterprise-grade AI-powered career development platform that provides:
- **Holistic Career Score** (0-850, like credit score)
- **ATS Resume Analysis** with ML-powered matching
- **Portfolio Evaluation** across 6 dimensions
- **Certificate Validation** from 17+ platforms
- **Extracurricular Tracking** for 10+ activity types
- **Internship Matching** with personalized roadmaps
- **Multi-Source Integration** from GitHub, LinkedIn, and more

---

## ✨ Key Features

### 1. 🎯 **Holistic Career Score (0-850)**
- Credit score-like system for career readiness
- 8 weighted components (Resume, Skills, Projects, Certifications, etc.)
- Percentile ranking and competitive positioning
- Personalized improvement recommendations

### 2. 📊 **Enhanced Portfolio Analysis**
- 6-dimensional evaluation (Technical Depth, Breadth, Impact, Growth, Leadership, Industry Readiness)
- Project quality scoring with 5 criteria
- Industry alignment analysis (AI/ML, Cloud, Web3, Full Stack)
- Portfolio tier classification (Elite to Building)

### 3. 📜 **Certificate Validation**
- Supports 17+ platforms (Coursera, edX, Google, AWS, Microsoft, etc.)
- Trust scoring (0-100) based on provider reputation
- Automatic skill mapping from certifications
- Expiry tracking and portfolio value assessment

### 4. 🏆 **Extracurricular Activities Tracker**
- Tracks 10 activity types (Hackathons, Clubs, Freelancing, Volunteering, etc.)
- Impact scoring with leadership level detection
- Skill demonstration mapping
- Timeline and consistency analysis

### 5. 💼 **Intelligent Internship Matching**
- 12 internship categories with skill-based matching
- Compatibility scoring (0-100) with gap analysis
- Personalized preparation roadmaps
- Readiness assessment (4 levels)

### 6. 🌐 **Multi-Source Data Integration**
- GitHub API integration (repos, stars, languages, contributions)
- Portfolio website analysis
- Certificate aggregation from multiple platforms
- Unified profile creation with quality scoring

### 7. 🤖 **AI-Powered Features**
- Resume enhancement with OpenRouter AI
- Project idea generation
- Career path suggestions
- Interview preparation with real-time feedback
- Course recommendations

### 8. 📈 **ATS Resume Scoring**
- XGBoost ML model (78.14% accuracy, 89.57% ROC AUC)
- Trained on 6,241+ real resume-job pairs
- 10,012 TF-IDF features with advanced NLP
- Multi-class probability distributions

---

## 🛠️ Technology Stack

### **AI/ML Core**
- **Machine Learning**: XGBoost, scikit-learn
- **NLP**: spaCy, TF-IDF vectorization
- **LLM**: OpenRouter API (Google Gemini Flash 1.5)
- **Data Science**: pandas, numpy

### **Backend**
- **Language**: Python 3.11+
- **Framework**: Streamlit
- **APIs**: GitHub API, OpenRouter API
- **Data Processing**: requests, BeautifulSoup (web scraping)

### **Features**
- Certificate validation across 17+ platforms
- Multi-source data integration (8 platforms)
- Real-time GitHub analysis
- Portfolio evaluation system
- Holistic scoring algorithm

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- OpenRouter API key ([Get one here](https://openrouter.ai))
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Sujaltalreja04/skill360.git
cd skill360
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Download spaCy model**
```bash
python -m spacy download en_core_web_sm
```

4. **Set up environment variables**
```bash
# Create .env file
echo "OPENROUTER_API_KEY=your_api_key_here" > .env
```

5. **Run the application**
```bash
streamlit run app/main.py
```

The app will open at `http://localhost:8501`

---

## 📁 Project Structure

```
skill360/
├── app/
│   └── main.py                          # Streamlit main application
├── src/
│   ├── openrouter_llm.py               # OpenRouter AI integration
│   ├── fit_classifier.py               # XGBoost ML model
│   ├── skills.py                       # Skill extraction
│   ├── github_analyzer.py              # GitHub API integration
│   ├── portfolio_analyzer.py           # Basic portfolio analysis
│   ├── enhanced_portfolio_analyzer.py  # 6-dimensional portfolio analysis
│   ├── certificate_validator.py        # Certificate validation (17+ platforms)
│   ├── extracurricular_tracker.py      # Activity tracking (10 types)
│   ├── internship_matcher.py           # Internship matching (12 categories)
│   ├── holistic_score.py               # Career score calculator (0-850)
│   ├── multi_source_integration.py     # Multi-platform integration
│   ├── course_suggestions.py           # AI course recommendations
│   ├── interview_prep.py               # Interview preparation
│   └── learning_resources.py           # Learning path suggestions
├── models/
│   └── ml_pipeline_xgboost_*.pkl       # Trained ML models
├── test_*.py                            # Test scripts
├── requirements.txt                     # Python dependencies
└── README.md                            # This file
```

---

## 🎓 Features in Detail

### **Holistic Career Score Components**

| Component | Weight | Description |
|-----------|--------|-------------|
| Resume Quality | 15% | ATS compatibility, formatting, content quality |
| Skills Portfolio | 20% | Technical and soft skills breadth and depth |
| Project Portfolio | 18% | Quality, diversity, and impact of projects |
| Certifications | 12% | Professional certifications and courses |
| Extracurricular | 10% | Hackathons, clubs, volunteering, leadership |
| GitHub Activity | 10% | Open source contributions and code quality |
| Learning Progress | 8% | Continuous learning and skill development |
| Interview Readiness | 7% | Interview preparation and practice |

### **Score Ranges**

| Range | Rating | Description | Opportunities |
|-------|--------|-------------|---------------|
| 750-850 | 🌟 Exceptional | Outstanding career readiness | Top companies, leadership roles |
| 650-749 | ⭐ Excellent | Highly competitive | Most positions, good internships |
| 550-649 | ✨ Good | Ready for entry-level | Entry-level positions |
| 450-549 | 📈 Fair | Needs improvement | Some internships, skill building |
| 0-449 | 🚀 Building | Focus on fundamentals | Learning and development |

### **Portfolio Evaluation Dimensions**

1. **Technical Depth (25%)** - Project complexity, GitHub activity, technical certifications
2. **Breadth & Diversity (20%)** - Language variety, domain coverage
3. **Impact & Quality (20%)** - Stars, forks, documentation, testing
4. **Professional Growth (15%)** - Certifications, continuous learning
5. **Leadership & Collaboration (10%)** - Leadership roles, team projects
6. **Industry Readiness (10%)** - Real-world projects, internships, freelancing

### **Supported Certificate Platforms**

Coursera • edX • Udemy • LinkedIn Learning • Google • Microsoft • AWS • IBM • Oracle • Cisco • CompTIA • freeCodeCamp • Udacity • Pluralsight • DataCamp • HackerRank • Credly

### **Internship Categories**

Software Development • Data Science/Analytics • Web Development • Mobile App Development • UI/UX Design • Digital Marketing • Content Writing • Business Development • Graphic Design • Cybersecurity • Cloud Computing • Research

---

## 🔌 API Integration

### **GitHub Integration**
```python
from multi_source_integration import integrate_github

github_data = integrate_github('username')
# Returns: repos, stars, languages, contributions, profile info
```

### **Certificate Validation**
```python
from certificate_validator import analyze_certificates

analysis = analyze_certificates(certificates_list)
# Returns: trust scores, skill mapping, recommendations
```

### **Holistic Score Calculation**
```python
from holistic_score import calculate_holistic_score

score = calculate_holistic_score(profile_data)
# Returns: 0-850 score, component breakdown, recommendations
```

### **Internship Matching**
```python
from internship_matcher import find_internship_matches

matches = find_internship_matches(candidate_profile, top_n=5)
# Returns: Top 5 matches with scores and roadmaps
```

---

## 💡 Usage Examples

### Example 1: Complete Profile Analysis
```python
# Analyze complete candidate profile
profile_data = {
    'github_username': 'johndoe',
    'portfolio_url': 'https://johndoe.dev',
    'certifications': [...],
    'extracurricular': [...],
    'learning': {...}
}

# Get holistic score
score = calculate_holistic_score(profile_data)
print(f"Career Score: {score['total_score']}/850")
print(f"Rating: {score['rating']}")
print(f"Percentile: Top {100 - score['percentile']}%")
```

### Example 2: Internship Preparation
```python
# Find best internship matches
candidate = {
    'skills': ['Python', 'JavaScript', 'React'],
    'projects': [...],
    'certifications': [...]
}

matches = find_internship_matches(candidate, top_n=5)
for match in matches:
    print(f"{match['category']}: {match['match_score']}/100")
    
# Get preparation roadmap
roadmap = generate_internship_roadmap(candidate, 'Software Development')
print(f"Timeline: {roadmap['estimated_timeline']}")
```

### Example 3: Portfolio Enhancement
```python
# Analyze portfolio
analysis = analyze_enhanced_portfolio(
    projects=projects_list,
    github_data=github_data,
    certifications=certs_list
)

print(f"Portfolio Tier: {analysis['portfolio_tier']}")
print(f"Overall Score: {analysis['overall_score']}/100")
print("Recommendations:")
for rec in analysis['recommendations']:
    print(f"  - {rec}")
```

---

## 🧪 Testing

Run the test scripts to verify functionality:

```bash
# Test ATS scoring
python test_ats_scoring.py

# Test OpenRouter AI features
python test_openrouter.py

# Test portfolio analysis
python test_portfolio_analysis.py
```

---

## 📊 Performance Metrics

| Metric | Achievement |
|--------|-------------|
| **ML Model Accuracy** | 78.14% (XGBoost) |
| **ROC AUC Score** | 89.57% |
| **Training Dataset** | 6,241 resume-job pairs |
| **Feature Dimensions** | 10,012 TF-IDF features |
| **Supported Platforms** | 17+ certificate platforms |
| **Internship Categories** | 12 categories |
| **Portfolio Dimensions** | 6 evaluation dimensions |
| **Career Score Range** | 0-850 (like credit score) |

---

## 🎯 Key Innovations

1. **Credit Score Model for Careers** - First-of-its-kind 0-850 scoring system
2. **Multi-Dimensional Portfolio Analysis** - 6 comprehensive evaluation dimensions
3. **Intelligent Internship Matching** - Skill-based matching with preparation roadmaps
4. **Certificate Validation** - Trust scoring from 17+ platforms
5. **Holistic Approach** - Combines all career aspects into one platform
6. **AI-Powered Insights** - OpenRouter integration for personalized recommendations

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

---

## 👨‍💻 Team

**Sujal K Talreja** - *Project Lead & Developer*
- 📧 Email: sujaltalreja04@gmail.com
- 📞 Phone: 7574021120
- 🔗 LinkedIn: [Sujal Kishore Kumar Talreja](https://www.linkedin.com/in/sujal-kishore-kumar-talreja-65975b216/)

---

## 🙏 Acknowledgments

- HuggingFace for the resume-job dataset
- OpenRouter for AI API access
- Streamlit for the amazing framework
- All open-source contributors

---

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Email: sujaltalreja04@gmail.com

---

**Built with ❤️ for career development and student success**

---

## 🚀 Quick Links

- [Live Demo](#) (Coming soon)
- [Documentation](#-features-in-detail)
- [API Reference](#-api-integration)
- [Examples](#-usage-examples)

---

**Version**: 2.0  
**Last Updated**: December 2024  
**Status**: ✅ Production Ready
