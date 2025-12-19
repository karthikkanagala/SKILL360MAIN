"""
Test script for OpenRouter API integration
Run this to verify the migration from Llama/Ollama to OpenRouter
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_basic_connection():
    """Test basic connection to OpenRouter API"""
    print("=" * 60)
    print("🧪 Test 1: Basic Connection to OpenRouter API")
    print("=" * 60)
    
    try:
        from openrouter_llm import is_openrouter_available
        
        is_available = is_openrouter_available()
        
        if is_available:
            print("✅ SUCCESS: OpenRouter API is available!")
            return True
        else:
            print("❌ FAILED: Cannot connect to OpenRouter API")
            return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def test_simple_call():
    """Test simple API call"""
    print("\n" + "=" * 60)
    print("🧪 Test 2: Simple API Call")
    print("=" * 60)
    
    try:
        from openrouter_llm import call_openrouter_llm
        
        print("Sending test prompt: 'Say hello in a friendly way'")
        response = call_openrouter_llm(
            prompt="Say hello in a friendly way",
            temperature=0.7,
            max_tokens=100
        )
        
        if response and not response.startswith("Error:"):
            print(f"✅ SUCCESS: Got response!")
            print(f"Response: {response[:200]}...")
            return True
        else:
            print(f"❌ FAILED: {response}")
            return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def test_resume_enhancement():
    """Test resume enhancement feature"""
    print("\n" + "=" * 60)
    print("🧪 Test 3: Resume Enhancement Feature")
    print("=" * 60)
    
    try:
        from openrouter_llm import enhance_resume_section
        
        sample_resume = """
        Software Developer
        - Worked on web applications
        - Used Python and JavaScript
        - Developed features for users
        """
        
        sample_jd = """
        Looking for a Senior Software Developer with:
        - 5+ years of Python experience
        - React.js expertise
        - AWS cloud experience
        - Strong problem-solving skills
        """
        
        missing_skills = ["React.js", "AWS", "Docker"]
        
        print("Analyzing resume against job description...")
        improvements = enhance_resume_section(sample_resume, sample_jd, missing_skills)
        
        if improvements and not improvements.startswith("Error:"):
            print(f"✅ SUCCESS: Got resume improvements!")
            print(f"Improvements preview: {improvements[:300]}...")
            return True
        else:
            print(f"❌ FAILED: {improvements}")
            return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def test_project_ideas():
    """Test project ideas generation"""
    print("\n" + "=" * 60)
    print("🧪 Test 4: Project Ideas Generation")
    print("=" * 60)
    
    try:
        from openrouter_llm import generate_project_ideas
        
        sample_resume = "Junior Developer with Python and JavaScript skills"
        skills = ["Python", "JavaScript", "REST APIs"]
        
        print("Generating project ideas...")
        ideas = generate_project_ideas(sample_resume, skills)
        
        if ideas and not ideas.startswith("Error:"):
            print(f"✅ SUCCESS: Got project ideas!")
            print(f"Ideas preview: {ideas[:300]}...")
            return True
        else:
            print(f"❌ FAILED: {ideas}")
            return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def test_career_suggestions():
    """Test AI career suggestions"""
    print("\n" + "=" * 60)
    print("🧪 Test 5: AI Career Suggestions")
    print("=" * 60)
    
    try:
        from openrouter_llm import generate_ai_career_suggestions
        
        interest_data = {
            'academic_interests': ['Computer Science', 'Mathematics'],
            'hobby_interests': ['Coding', 'Problem Solving'],
            'work_environment': 'Remote',
            'motivation': 'Building innovative products',
            'tech_score': 3,
            'creative_score': 1,
            'business_score': 1
        }
        
        skill_data = {
            'learning_interests': ['Python', 'Machine Learning'],
            'current_skills': {'technical': ['Python', 'JavaScript']},
            'experience_level': 'Beginner'
        }
        
        print("Generating career suggestions...")
        careers = generate_ai_career_suggestions(interest_data, skill_data)
        
        if careers and len(careers) > 0:
            print(f"✅ SUCCESS: Got {len(careers)} career suggestions!")
            for i, career in enumerate(careers[:3], 1):
                print(f"  {i}. {career.get('title', 'Unknown')} - {career.get('salary_range', 'N/A')}")
            return True
        else:
            print(f"❌ FAILED: No career suggestions received")
            return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def main():
    """Run all tests"""
    print("\n" + "🚀" * 30)
    print("OpenRouter API Integration Test Suite")
    print("Testing migration from Llama/Ollama to OpenRouter")
    print("🚀" * 30 + "\n")
    
    results = []
    
    # Run tests
    results.append(("Basic Connection", test_basic_connection()))
    
    if results[0][1]:  # Only continue if connection works
        results.append(("Simple API Call", test_simple_call()))
        results.append(("Resume Enhancement", test_resume_enhancement()))
        results.append(("Project Ideas", test_project_ideas()))
        results.append(("Career Suggestions", test_career_suggestions()))
    else:
        print("\n⚠️ Skipping remaining tests due to connection failure")
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Migration successful!")
        print("✅ Your application is ready to use OpenRouter API")
    else:
        print(f"\n⚠️ {total - passed} test(s) failed")
        print("Please check the error messages above")
        print("\nTroubleshooting:")
        print("1. Verify your internet connection")
        print("2. Check if the API key is correct")
        print("3. Ensure OpenRouter API is accessible")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Tests interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
