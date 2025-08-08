import google.generativeai as genai
import streamlit as st
from typing import Dict, List, Tuple
import json
from .config import ToxicDetectorConfig

class ToxicDetectorEngine:
    """Main analysis engine for toxic behavior detection"""
    
    def __init__(self, api_key: str = None):
        """Initialize the analysis engine"""
        self.api_key = api_key or ToxicDetectorConfig.GEMINI_API_KEY
        if not self.api_key:
            raise ValueError("Gemini API key is required!")
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Analysis history
        self.analysis_history = []
    
    def analyze_red_flags(self, message: str) -> Dict:
        """Analyze message for red flags"""
        try:
            prompt = ToxicDetectorConfig.RED_FLAG_PROMPT.format(message=message)
            
            response = self.model.generate_content(prompt)
            
            # Extract analysis
            analysis = {
                "message": message,
                "analysis_type": "red_flags",
                "analysis": response.text,
                "severity": self._extract_severity(response.text),
                "flags_found": self._extract_flags(response.text, ToxicDetectorConfig.RED_FLAGS)
            }
            
            self.analysis_history.append(analysis)
            return analysis
            
        except Exception as e:
            st.error(f"Error analyzing red flags: {str(e)}")
            return {"error": str(e)}
    
    def analyze_green_flags(self, message: str) -> Dict:
        """Analyze message for green flags"""
        try:
            prompt = ToxicDetectorConfig.GREEN_FLAG_PROMPT.format(message=message)
            
            response = self.model.generate_content(prompt)
            
            analysis = {
                "message": message,
                "analysis_type": "green_flags",
                "analysis": response.text,
                "positivity_score": self._extract_positivity(response.text),
                "flags_found": self._extract_flags(response.text, ToxicDetectorConfig.GREEN_FLAGS)
            }
            
            self.analysis_history.append(analysis)
            return analysis
            
        except Exception as e:
            st.error(f"Error analyzing green flags: {str(e)}")
            return {"error": str(e)}
    
    def analyze_manipulation(self, message: str) -> Dict:
        """Analyze message for manipulation tactics"""
        try:
            prompt = ToxicDetectorConfig.MANIPULATION_PROMPT.format(message=message)
            
            response = self.model.generate_content(prompt)
            
            analysis = {
                "message": message,
                "analysis_type": "manipulation",
                "analysis": response.text,
                "manipulation_score": self._extract_manipulation_score(response.text),
                "tactics_found": self._extract_flags(response.text, ToxicDetectorConfig.MANIPULATION_TACTICS)
            }
            
            self.analysis_history.append(analysis)
            return analysis
            
        except Exception as e:
            st.error(f"Error analyzing manipulation: {str(e)}")
            return {"error": str(e)}
    
    def analyze_sincerity(self, message: str) -> Dict:
        """Analyze message for sincerity - DID HE MEAN IT?"""
        try:
            prompt = ToxicDetectorConfig.SINCERITY_PROMPT.format(message=message)
            
            response = self.model.generate_content(prompt)
            
            analysis = {
                "message": message,
                "analysis_type": "sincerity",
                "analysis": response.text,
                "sincerity_score": self._extract_sincerity_score(response.text),
                "did_he_mean_it": self._extract_did_he_mean_it(response.text)
            }
            
            self.analysis_history.append(analysis)
            return analysis
            
        except Exception as e:
            st.error(f"Error analyzing sincerity: {str(e)}")
            return {"error": str(e)}
    
    def comprehensive_analysis(self, message: str) -> Dict:
        """Perform comprehensive analysis of a message"""
        try:
            # Run all analyses
            red_flags = self.analyze_red_flags(message)
            green_flags = self.analyze_green_flags(message)
            manipulation = self.analyze_manipulation(message)
            sincerity = self.analyze_sincerity(message)
            
            # Calculate overall risk score
            risk_score = self._calculate_risk_score(red_flags, green_flags, manipulation, sincerity)
            
            comprehensive = {
                "message": message,
                "analysis_type": "comprehensive",
                "red_flags": red_flags,
                "green_flags": green_flags,
                "manipulation": manipulation,
                "sincerity": sincerity,
                "risk_score": risk_score,
                "recommendation": self._generate_recommendation(risk_score)
            }
            
            self.analysis_history.append(comprehensive)
            return comprehensive
            
        except Exception as e:
            st.error(f"Error in comprehensive analysis: {str(e)}")
            return {"error": str(e)}
    
    def _extract_severity(self, analysis_text: str) -> str:
        """Extract severity level from analysis"""
        if "severe" in analysis_text.lower() or "dangerous" in analysis_text.lower():
            return "HIGH"
        elif "moderate" in analysis_text.lower() or "concerning" in analysis_text.lower():
            return "MEDIUM"
        elif "minor" in analysis_text.lower() or "slight" in analysis_text.lower():
            return "LOW"
        else:
            return "UNKNOWN"
    
    def _extract_positivity(self, analysis_text: str) -> int:
        """Extract positivity score (1-10)"""
        positive_words = ["positive", "healthy", "good", "respectful", "supportive"]
        score = 5  # Default neutral
        
        for word in positive_words:
            if word in analysis_text.lower():
                score += 1
        
        return min(score, 10)
    
    def _extract_manipulation_score(self, analysis_text: str) -> int:
        """Extract manipulation score (1-10)"""
        manipulation_words = ["manipulation", "gaslighting", "guilt", "control", "abuse"]
        score = 1  # Default low
        
        for word in manipulation_words:
            if word in analysis_text.lower():
                score += 2
        
        return min(score, 10)
    
    def _extract_sincerity_score(self, analysis_text: str) -> int:
        """Extract sincerity score (1-10)"""
        sincere_words = ["genuine", "sincere", "honest", "authentic", "real"]
        insincere_words = ["fake", "manipulative", "dishonest", "deceptive", "pretending"]
        
        score = 5  # Default neutral
        
        for word in sincere_words:
            if word in analysis_text.lower():
                score += 1
        
        for word in insincere_words:
            if word in analysis_text.lower():
                score -= 1
        
        return max(1, min(score, 10))
    
    def _extract_did_he_mean_it(self, analysis_text: str) -> str:
        """Extract DID HE MEAN IT? verdict"""
        sincerity_score = self._extract_sincerity_score(analysis_text)
        
        if sincerity_score >= 8:
            return "YES, HE MEANT IT! 🟢"
        elif sincerity_score >= 5:
            return "MAYBE, BUT BE CAUTIOUS 🟡"
        else:
            return "NO, HE DIDN'T MEAN IT! 🔴"
    
    def _extract_flags(self, analysis_text: str, flag_list: List[str]) -> List[str]:
        """Extract specific flags found in the analysis"""
        found_flags = []
        for flag in flag_list:
            if flag.lower() in analysis_text.lower():
                found_flags.append(flag)
        return found_flags
    
    def _calculate_risk_score(self, red_flags: Dict, green_flags: Dict, 
                            manipulation: Dict, sincerity: Dict) -> int:
        """Calculate overall risk score (1-10)"""
        score = 5  # Default neutral
        
        # Red flags increase risk
        if "severity" in red_flags and red_flags["severity"] == "HIGH":
            score += 3
        elif "severity" in red_flags and red_flags["severity"] == "MEDIUM":
            score += 2
        
        # Green flags decrease risk
        if "positivity_score" in green_flags:
            score -= (green_flags["positivity_score"] - 5) // 2
        
        # Manipulation increases risk
        if "manipulation_score" in manipulation:
            score += (manipulation["manipulation_score"] - 5) // 2
        
        # Low sincerity increases risk
        if "sincerity_score" in sincerity:
            score += (5 - sincerity["sincerity_score"]) // 2
        
        return max(1, min(score, 10))
    
    def _generate_recommendation(self, risk_score: int) -> str:
        """Generate recommendation based on risk score"""
        if risk_score >= 8:
            return "🚨 HIGH RISK: Consider ending this relationship. Seek support."
        elif risk_score >= 6:
            return "⚠️ MODERATE RISK: Set boundaries and monitor behavior closely."
        elif risk_score >= 4:
            return "🟡 CAUTION: Be aware and communicate clearly."
        else:
            return "🟢 LOW RISK: This appears to be healthy communication."
    
    def get_analysis_history(self) -> List[Dict]:
        """Get analysis history"""
        return self.analysis_history
    
    def clear_history(self):
        """Clear analysis history"""
        self.analysis_history = [] 