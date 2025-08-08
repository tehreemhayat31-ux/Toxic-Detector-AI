import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ToxicDetectorConfig:
    """Configuration for Toxic Detector AI"""
    
    # API Configuration
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
    
    # App Configuration
    APP_NAME = "🚨 Toxic Detector AI"
    APP_VERSION = "1.0.0"
    
    # Analysis Categories
    RED_FLAGS = [
        "Gaslighting",
        "Love bombing", 
        "Emotional blackmail",
        "Controlling behavior",
        "Jealousy and possessiveness",
        "Disrespectful language",
        "Threats or intimidation",
        "Isolation tactics",
        "Financial control",
        "Verbal abuse"
    ]
    
    GREEN_FLAGS = [
        "Respectful communication",
        "Healthy boundaries",
        "Emotional support",
        "Honest and transparent",
        "Encourages independence",
        "Apologizes sincerely",
        "Consistent behavior",
        "Shows empathy",
        "Respects your time",
        "Positive reinforcement"
    ]
    
    MANIPULATION_TACTICS = [
        "Gaslighting",
        "Guilt tripping",
        "Silent treatment",
        "Breadcrumbing",
        "Future faking",
        "Triangulation",
        "Projection",
        "Minimizing feelings",
        "Moving goalposts",
        "Emotional blackmail"
    ]
    
    # Analysis Prompts
    RED_FLAG_PROMPT = """
    Analyze this message for red flags in relationships. Look for:
    - Controlling behavior
    - Manipulation tactics
    - Disrespectful language
    - Threats or intimidation
    - Gaslighting attempts
    - Love bombing
    - Emotional blackmail
    
    Message: {message}
    
    Provide a detailed analysis with specific examples from the text.
    """
    
    GREEN_FLAG_PROMPT = """
    Analyze this message for green flags (healthy relationship behaviors). Look for:
    - Respectful communication
    - Healthy boundaries
    - Emotional support
    - Honest and transparent behavior
    - Encouraging independence
    - Sincere apologies
    - Consistent positive behavior
    
    Message: {message}
    
    Provide a detailed analysis with specific examples from the text.
    """
    
    MANIPULATION_PROMPT = """
    Analyze this message for emotional manipulation tactics. Look for:
    - Gaslighting techniques
    - Guilt tripping
    - Silent treatment threats
    - Breadcrumbing behavior
    - Future faking
    - Triangulation
    - Projection
    - Minimizing feelings
    - Moving goalposts
    - Emotional blackmail
    
    Message: {message}
    
    Provide a detailed analysis with specific examples from the text.
    """
    
    SINCERITY_PROMPT = """
    Analyze this message for sincerity and genuine intent. Consider:
    - Does the person seem genuine?
    - Are they taking responsibility?
    - Is there consistency in their words?
    - Do they show empathy?
    - Are they being honest or defensive?
    - Is there manipulation behind kind words?
    
    Message: {message}
    
    Provide a detailed analysis with a "DID HE MEAN IT?" score (1-10).
    """
    
    # Fake Character Personas
    FAKE_CHARACTERS = {
        "toxic_partner": {
            "name": "Alex",
            "personality": "Manipulative, controlling, and emotionally abusive",
            "messages": [
                "You're overreacting, as usual.",
                "If you really loved me, you would...",
                "I'm the only one who will ever love you.",
                "You're being too sensitive.",
                "Why are you always so dramatic?"
            ]
        },
        "healthy_partner": {
            "name": "Jordan", 
            "personality": "Respectful, supportive, and emotionally healthy",
            "messages": [
                "I understand how you feel.",
                "Let's talk about this together.",
                "I appreciate you sharing that with me.",
                "I'm sorry for my part in this.",
                "How can I support you better?"
            ]
        }
    } 