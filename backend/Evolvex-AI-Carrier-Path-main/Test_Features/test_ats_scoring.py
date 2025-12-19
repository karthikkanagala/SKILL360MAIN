"""
Test Script to Demonstrate ATS Scoring Capabilities
Run this to see the ATS/Resume scoring features in action
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from skills import extract_skills
from fit_classifier import predict_fit

# Sample Resume Text
sample_resume = """
John Doe
Software Engineer

SKILLS:
- Python, JavaScript, React, Node.js
- AWS, Docker, Kubernetes
- SQL, MongoDB, PostgreSQL
- Git, CI/CD, Jenkins
- Machine Learning, TensorFlow, Scikit-learn

EXPERIENCE:
Senior Software Engineer at Tech Corp (2020-Present)
- Developed full-stack applications using React and Node.js
- Implemented machine learning models for prediction
- Deployed applications on AWS with Docker and Kubernetes
- Managed databases including PostgreSQL and MongoDB
"""

# Sample Job Description
sample_jd = """
Senior Full Stack Developer

REQUIRED SKILLS:
- Python, JavaScript, React, Node.js
- AWS Cloud Services
- Docker, Kubernetes
- PostgreSQL, MongoDB
- Machine Learning experience
- Git version control
- Agile methodologies

NICE TO HAVE:
- TensorFlow or PyTorch
- CI/CD pipelines
- Microservices architecture
"""

print("=" * 80)
print("🎯 ATS RESUME SCORING DEMONSTRATION")
print("=" * 80)
print()

# Extract skills from both
print("📄 Extracting skills from Resume...")
resume_skills = extract_skills(sample_resume)
print(f"   Found {len(resume_skills)} skills: {', '.join(resume_skills[:10])}...")
print()

print("📋 Extracting skills from Job Description...")
jd_skills = extract_skills(sample_jd)
print(f"   Found {len(jd_skills)} required skills: {', '.join(jd_skills)}")
print()

# Calculate match
matched_skills = set(resume_skills) & set(jd_skills)
missing_skills = set(jd_skills) - set(resume_skills)
extra_skills = set(resume_skills) - set(jd_skills)
match_score = len(matched_skills) / len(jd_skills) * 100 if jd_skills else 0

print("=" * 80)
print("📊 ATS MATCH SCORE ANALYSIS")
print("=" * 80)
print()
print(f"🎯 Overall Match Score:    {match_score:.1f}%")
print(f"✅ Skills Matched:         {len(matched_skills)}/{len(jd_skills)}")
print(f"❌ Missing Skills:         {len(missing_skills)}")
print(f"💼 Bonus Skills:           {len(extra_skills)}")
print()

# Show matched skills
if matched_skills:
    print("✅ MATCHED SKILLS:")
    for skill in sorted(matched_skills):
        print(f"   • {skill}")
    print()

# Show missing skills
if missing_skills:
    print("❌ SKILLS TO DEVELOP:")
    for skill in sorted(missing_skills):
        print(f"   • {skill}")
    print()

# Show extra skills
if extra_skills:
    print("💼 BONUS SKILLS:")
    for skill in list(sorted(extra_skills))[:5]:
        print(f"   • {skill}")
    if len(extra_skills) > 5:
        print(f"   ... and {len(extra_skills) - 5} more")
    print()

# ATS Assessment
print("=" * 80)
print("🤖 ADVANCED AI FIT PREDICTION")
print("=" * 80)
print()

result = predict_fit(
    resume_text=sample_resume,
    job_description=sample_jd,
    match_score=match_score,
    num_matched=len(matched_skills),
    num_missing=len(missing_skills)
)

print(f"🎯 AI Prediction:          {result['prediction']}")
print(f"📊 Confidence Level:       {result['confidence']*100:.1f}%")
print(f"🔧 Model Type:             {result.get('model_type', 'basic').upper()}")
print()

print("📈 PROBABILITY BREAKDOWN:")
for class_name, prob in result['probabilities'].items():
    bar = "█" * int(prob * 40)
    print(f"   {class_name:20s} {prob*100:5.1f}% {bar}")
print()

# Final Assessment
print("=" * 80)
print("🎓 ATS ASSESSMENT SUMMARY")
print("=" * 80)
print()

if match_score >= 80:
    print("🌟 EXCELLENT MATCH!")
    print("   Your resume is highly aligned with the job requirements.")
    print("   You have strong chances of passing ATS screening.")
elif match_score >= 60:
    print("✅ GOOD MATCH!")
    print("   Your resume shows good alignment with the job.")
    print("   Likely to pass ATS screening with current skills.")
elif match_score >= 40:
    print("⚡ MODERATE MATCH")
    print("   Your resume has decent alignment but could be improved.")
    print("   Consider adding the missing skills to improve ATS score.")
else:
    print("🎯 GROWTH OPPORTUNITY")
    print("   Significant skill gaps identified.")
    print("   Focus on developing the missing skills before applying.")

print()
print("=" * 80)
print("✨ This is what the Streamlit app provides in a beautiful UI!")
print("   Run: streamlit run app/main.py")
print("=" * 80)
