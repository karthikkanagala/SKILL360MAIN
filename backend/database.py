"""
Database Configuration Module
Handles MongoDB connection and Google API integration
"""
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


# ==================== MongoDB Configuration ====================

class MongoDB:
    """MongoDB Database Manager"""
    
    _client = None
    _db = None
    
    @classmethod
    def get_client(cls):
        """Get MongoDB client (lazy initialization)"""
        if cls._client is None:
            try:
                from pymongo import MongoClient
                from pymongo.server_api import ServerApi
                
                # Get credentials from environment
                username = os.getenv("MONGODB_USERNAME", "kanagalakarthik2468_db_user")
                password = os.getenv("MONGODB_PASSWORD", "YU6VScyxJ3ASF0zj")
                
                # Try different MongoDB Atlas cluster formats
                cluster_options = [
                    "cluster0.mongodb.net",
                    "cluster0.hvgvg.mongodb.net",
                    "cluster0.abcde.mongodb.net",
                ]
                
                # First check if full URI is provided
                uri = os.getenv("MONGODB_URI")
                if uri:
                    try:
                        cls._client = MongoClient(uri, server_api=ServerApi('1'))
                        cls._client.admin.command('ping')
                        print("✅ Successfully connected to MongoDB!")
                        return cls._client
                    except Exception as e:
                        print(f"URI connection failed: {e}")
                
                # Try each cluster format
                for cluster in cluster_options:
                    try:
                        uri = f"mongodb+srv://{username}:{password}@{cluster}/?retryWrites=true&w=majority"
                        cls._client = MongoClient(uri, server_api=ServerApi('1'), serverSelectionTimeoutMS=5000)
                        cls._client.admin.command('ping')
                        print(f"✅ Successfully connected to MongoDB ({cluster})!")
                        return cls._client
                    except Exception:
                        continue
                
                print("⚠️ Could not connect to MongoDB - using local fallback")
                cls._client = None
                
            except Exception as e:
                print(f"❌ MongoDB connection failed: {e}")
                cls._client = None
        
        return cls._client
    
    @classmethod
    def get_database(cls, db_name: Optional[str] = None):
        """Get database instance"""
        client = cls.get_client()
        if client is None:
            return None
        
        db_name = db_name or os.getenv("MONGODB_DATABASE", "skill_passport_360")
        return client[db_name]
    
    @classmethod
    def get_collection(cls, collection_name: str, db_name: Optional[str] = None):
        """Get collection instance"""
        db = cls.get_database(db_name)
        if db is None:
            return None
        return db[collection_name]
    
    @classmethod
    def close(cls):
        """Close MongoDB connection"""
        if cls._client:
            cls._client.close()
            cls._client = None
            cls._db = None
            print("MongoDB connection closed")


# ==================== Google API Configuration ====================

class GoogleAPI:
    """Google Generative AI (Gemini) Manager"""
    
    _model = None
    _api_key = None
    
    @classmethod
    def get_api_key(cls) -> Optional[str]:
        """Get Google API key from environment"""
        if cls._api_key is None:
            cls._api_key = os.getenv("GOOGLE_API_KEY")
        return cls._api_key
    
    @classmethod
    def get_model(cls, model_name: str = "gemini-pro"):
        """Get Gemini model instance"""
        if cls._model is None:
            try:
                import google.generativeai as genai
                
                api_key = cls.get_api_key()
                if not api_key:
                    print("Warning: GOOGLE_API_KEY not found in environment")
                    return None
                
                genai.configure(api_key=api_key)
                cls._model = genai.GenerativeModel(model_name)
                print(f"✅ Google Generative AI ({model_name}) initialized!")
                
            except Exception as e:
                print(f"❌ Google API initialization failed: {e}")
                cls._model = None
        
        return cls._model
    
    @classmethod
    def generate_content(cls, prompt: str, model_name: str = "gemini-pro") -> Optional[str]:
        """Generate content using Gemini"""
        model = cls.get_model(model_name)
        if model is None:
            return None
        
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error generating content: {e}")
            return None


# ==================== Database Collections ====================

class Collections:
    """MongoDB Collection Names"""
    USERS = "users"
    PROFILES = "profiles"
    RESUMES = "resumes"
    CAREER_SCORES = "career_scores"
    CERTIFICATES = "certificates"
    GITHUB_ANALYSIS = "github_analysis"
    INTERVIEW_HISTORY = "interview_history"
    LEARNING_PATHS = "learning_paths"


# ==================== Helper Functions ====================

def get_db():
    """Quick access to database"""
    return MongoDB.get_database()


def get_collection(name: str):
    """Quick access to collection"""
    return MongoDB.get_collection(name)


def init_database():
    """Initialize database connection on startup"""
    db = MongoDB.get_database()
    if db is not None:
        # Create indexes for common queries
        try:
            # Users collection
            users = db[Collections.USERS]
            users.create_index("email", unique=True, sparse=True)
            
            # Profiles collection
            profiles = db[Collections.PROFILES]
            profiles.create_index("user_id")
            
            # Career scores collection
            scores = db[Collections.CAREER_SCORES]
            scores.create_index([("user_id", 1), ("timestamp", -1)])
            
            print("✅ Database indexes created successfully!")
        except Exception as e:
            print(f"Warning: Could not create indexes: {e}")
    
    return db


def test_google_api():
    """Test Google API connection"""
    model = GoogleAPI.get_model()
    if model:
        try:
            response = GoogleAPI.generate_content("Say 'API connection successful!' in one line.")
            if response:
                print(f"✅ Google API Test: {response[:50]}...")
                return True
        except Exception as e:
            print(f"Google API test failed: {e}")
    return False


# ==================== Profile Data Operations ====================

class ProfileDB:
    """Profile database operations"""
    
    @staticmethod
    def save_profile(user_id: str, profile_data: dict) -> bool:
        """Save or update user profile"""
        collection = get_collection(Collections.PROFILES)
        if collection is None:
            return False
        
        try:
            from datetime import datetime
            profile_data["user_id"] = user_id
            profile_data["updated_at"] = datetime.utcnow()
            
            collection.update_one(
                {"user_id": user_id},
                {"$set": profile_data},
                upsert=True
            )
            return True
        except Exception as e:
            print(f"Error saving profile: {e}")
            return False
    
    @staticmethod
    def get_profile(user_id: str) -> Optional[dict]:
        """Get user profile"""
        collection = get_collection(Collections.PROFILES)
        if collection is None:
            return None
        
        try:
            profile = collection.find_one({"user_id": user_id})
            if profile:
                profile["_id"] = str(profile["_id"])  # Convert ObjectId to string
            return profile
        except Exception as e:
            print(f"Error getting profile: {e}")
            return None


class CareerScoreDB:
    """Career score database operations"""
    
    @staticmethod
    def save_score(user_id: str, score_data: dict) -> bool:
        """Save career score"""
        collection = get_collection(Collections.CAREER_SCORES)
        if collection is None:
            return False
        
        try:
            from datetime import datetime
            score_data["user_id"] = user_id
            score_data["timestamp"] = datetime.utcnow()
            
            collection.insert_one(score_data)
            return True
        except Exception as e:
            print(f"Error saving career score: {e}")
            return False
    
    @staticmethod
    def get_score_history(user_id: str, limit: int = 50) -> list:
        """Get career score history"""
        collection = get_collection(Collections.CAREER_SCORES)
        if collection is None:
            return []
        
        try:
            cursor = collection.find(
                {"user_id": user_id}
            ).sort("timestamp", -1).limit(limit)
            
            return [
                {**doc, "_id": str(doc["_id"])}
                for doc in cursor
            ]
        except Exception as e:
            print(f"Error getting score history: {e}")
            return []
