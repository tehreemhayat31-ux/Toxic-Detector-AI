import random
import streamlit as st
from typing import Dict, List
from .config import ToxicDetectorConfig

class FakeCharacter:
    """Fake character system for testing toxic detector"""
    
    def __init__(self, character_type: str = "toxic_partner"):
        """Initialize fake character"""
        self.character_type = character_type
        self.character_data = ToxicDetectorConfig.FAKE_CHARACTERS[character_type]
        self.name = self.character_data["name"]
        self.personality = self.character_data["personality"]
        self.message_history = []
        self.current_mood = "neutral"
        
        # Extended message templates based on character type
        self.message_templates = self._get_message_templates()
    
    def _get_message_templates(self) -> Dict[str, List[str]]:
        """Get message templates based on character type"""
        if self.character_type == "toxic_partner":
            return {
                "gaslighting": [
                    "You're remembering things wrong.",
                    "That never happened.",
                    "You're being too sensitive.",
                    "You're overreacting.",
                    "I never said that."
                ],
                "love_bombing": [
                    "You're the only one for me.",
                    "I can't live without you.",
                    "You're perfect in every way.",
                    "I've never felt this way before.",
                    "You're my everything."
                ],
                "controlling": [
                    "Where are you going?",
                    "Who are you talking to?",
                    "You shouldn't wear that.",
                    "I don't like your friends.",
                    "You spend too much time on your phone."
                ],
                "emotional_blackmail": [
                    "If you really loved me, you would...",
                    "I'll leave if you don't...",
                    "You're making me sad.",
                    "I thought you cared about me.",
                    "You're breaking my heart."
                ],
                "jealousy": [
                    "Why were you talking to him/her?",
                    "I saw you looking at someone else.",
                    "You're always flirting with others.",
                    "I don't trust your friends.",
                    "You're hiding something from me."
                ]
            }
        else:  # healthy_partner
            return {
                "supportive": [
                    "I understand how you feel.",
                    "Let's talk about this together.",
                    "I'm here for you.",
                    "How can I help?",
                    "I appreciate you sharing that."
                ],
                "respectful": [
                    "I respect your decision.",
                    "Your feelings are valid.",
                    "I want to understand your perspective.",
                    "Thank you for being honest.",
                    "I value your opinion."
                ],
                "apologetic": [
                    "I'm sorry for my part in this.",
                    "I was wrong, and I apologize.",
                    "I understand I hurt you.",
                    "I want to make this right.",
                    "I take responsibility for my actions."
                ],
                "encouraging": [
                    "You're doing great!",
                    "I believe in you.",
                    "You have every right to feel that way.",
                    "I'm proud of you.",
                    "You're strong and capable."
                ],
                "communicative": [
                    "Can we talk about this?",
                    "I want to understand better.",
                    "Let's work through this together.",
                    "I'm listening.",
                    "What do you need from me?"
                ]
            }
    
    def generate_response(self, user_message: str) -> str:
        """Generate a response based on user message and character type"""
        # Analyze user message sentiment
        sentiment = self._analyze_sentiment(user_message)
        
        # Choose response category based on sentiment and character type
        if self.character_type == "toxic_partner":
            return self._generate_toxic_response(user_message, sentiment)
        else:
            return self._generate_healthy_response(user_message, sentiment)
    
    def _analyze_sentiment(self, message: str) -> str:
        """Simple sentiment analysis"""
        positive_words = ["love", "happy", "good", "great", "wonderful", "amazing"]
        negative_words = ["angry", "sad", "upset", "hurt", "disappointed", "frustrated"]
        
        message_lower = message.lower()
        
        positive_count = sum(1 for word in positive_words if word in message_lower)
        negative_count = sum(1 for word in negative_words if word in message_lower)
        
        if positive_count > negative_count:
            return "positive"
        elif negative_count > positive_count:
            return "negative"
        else:
            return "neutral"
    
    def _generate_toxic_response(self, user_message: str, sentiment: str) -> str:
        """Generate toxic partner response"""
        # Choose response strategy based on sentiment
        if sentiment == "positive":
            # Love bombing or jealousy
            strategies = ["love_bombing", "jealousy"]
        elif sentiment == "negative":
            # Gaslighting or emotional blackmail
            strategies = ["gaslighting", "emotional_blackmail"]
        else:
            # Controlling or gaslighting
            strategies = ["controlling", "gaslighting"]
        
        strategy = random.choice(strategies)
        templates = self.message_templates[strategy]
        
        # Add some randomness and personalization
        response = random.choice(templates)
        
        # Add character-specific variations
        if "you" in user_message.lower():
            response += " You know I only want what's best for you."
        elif "friend" in user_message.lower():
            response += " I don't think they're good for you."
        elif "work" in user_message.lower() or "busy" in user_message.lower():
            response += " You always put everything before me."
        
        return response
    
    def _generate_healthy_response(self, user_message: str, sentiment: str) -> str:
        """Generate healthy partner response"""
        # Choose response strategy based on sentiment
        if sentiment == "positive":
            strategies = ["supportive", "encouraging"]
        elif sentiment == "negative":
            strategies = ["supportive", "apologetic"]
        else:
            strategies = ["communicative", "respectful"]
        
        strategy = random.choice(strategies)
        templates = self.message_templates[strategy]
        
        response = random.choice(templates)
        
        # Add supportive elements
        if "sad" in user_message.lower() or "upset" in user_message.lower():
            response += " I'm here to listen and support you."
        elif "angry" in user_message.lower():
            response += " I understand you're frustrated. Let's talk about it."
        elif "happy" in user_message.lower() or "excited" in user_message.lower():
            response += " I'm so happy for you!"
        
        return response
    
    def get_character_info(self) -> Dict:
        """Get character information"""
        return {
            "name": self.name,
            "personality": self.personality,
            "type": self.character_type,
            "mood": self.current_mood
        }
    
    def change_character(self, character_type: str):
        """Change to a different character"""
        if character_type in ToxicDetectorConfig.FAKE_CHARACTERS:
            self.character_type = character_type
            self.character_data = ToxicDetectorConfig.FAKE_CHARACTERS[character_type]
            self.name = self.character_data["name"]
            self.personality = self.character_data["personality"]
            self.message_templates = self._get_message_templates()
            self.message_history = []
            self.current_mood = "neutral"

class CharacterManager:
    """Manages multiple fake characters"""
    
    def __init__(self):
        """Initialize character manager"""
        self.characters = {}
        self.current_character = None
    
    def create_character(self, character_type: str) -> FakeCharacter:
        """Create a new character"""
        character = FakeCharacter(character_type)
        self.characters[character_type] = character
        return character
    
    def get_character(self, character_type: str) -> FakeCharacter:
        """Get or create a character"""
        if character_type not in self.characters:
            self.create_character(character_type)
        return self.characters[character_type]
    
    def get_available_characters(self) -> List[str]:
        """Get list of available character types"""
        return list(ToxicDetectorConfig.FAKE_CHARACTERS.keys())
    
    def get_character_descriptions(self) -> Dict[str, str]:
        """Get character descriptions"""
        descriptions = {}
        for char_type, char_data in ToxicDetectorConfig.FAKE_CHARACTERS.items():
            descriptions[char_type] = f"{char_data['name']} - {char_data['personality']}"
        return descriptions 