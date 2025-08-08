import streamlit as st
import os
from dotenv import load_dotenv
from .analysis_engine import ToxicDetectorEngine
from .fake_character import CharacterManager
from .config import ToxicDetectorConfig

# Load environment variables
load_dotenv()

class ToxicDetectorApp:
    """Main Toxic Detector AI Application"""
    
    def __init__(self):
        """Initialize the app"""
        self.setup_page()
        self.initialize_session_state()
        
    def setup_page(self):
        """Setup the Streamlit page configuration"""
        st.set_page_config(
            page_title=ToxicDetectorConfig.APP_NAME,
            page_icon="🚨",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Custom CSS
        st.markdown("""
        <style>
        .main-header {
            font-size: 3rem;
            font-weight: bold;
            color: #FF4444;
            text-align: center;
            margin-bottom: 2rem;
        }
        .sub-header {
            font-size: 1.5rem;
            color: #4A4A4A;
            margin-bottom: 1rem;
        }
        .red-flag {
            background-color: #FFE6E6;
            border: 2px solid #FF4444;
            border-radius: 10px;
            padding: 1rem;
            margin: 1rem 0;
        }
        .green-flag {
            background-color: #E6FFE6;
            border: 2px solid #44FF44;
            border-radius: 10px;
            padding: 1rem;
            margin: 1rem 0;
        }
        .warning-box {
            background-color: #FFF3CD;
            border: 2px solid #FFC107;
            border-radius: 10px;
            padding: 1rem;
            margin: 1rem 0;
        }
        .sincerity-box {
            background-color: #E3F2FD;
            border: 2px solid #2196F3;
            border-radius: 10px;
            padding: 1rem;
            margin: 1rem 0;
        }
        </style>
        """, unsafe_allow_html=True)
    
    def initialize_session_state(self):
        """Initialize session state variables"""
        if 'analysis_engine' not in st.session_state:
            st.session_state.analysis_engine = None
        if 'character_manager' not in st.session_state:
            st.session_state.character_manager = CharacterManager()
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        if 'analysis_history' not in st.session_state:
            st.session_state.analysis_history = []
        if 'current_character' not in st.session_state:
            st.session_state.current_character = "toxic_partner"
    
    def render_header(self):
        """Render the app header"""
        st.markdown('<h1 class="main-header">🚨 Toxic Detector AI</h1>', unsafe_allow_html=True)
        st.markdown("### Your AI-powered relationship safety analyzer")
        st.markdown("---")
    
    def render_sidebar(self):
        """Render the sidebar with configuration options"""
        with st.sidebar:
            st.header("⚙️ Configuration")
            
            # API Key input
            api_key = st.text_input(
                "🔑 Gemini API Key",
                type="password",
                help="Enter your Gemini API key from Google AI Studio"
            )
            
            if api_key:
                if st.button("🔗 Test Connection"):
                    with st.spinner("Testing connection..."):
                        try:
                            engine = ToxicDetectorEngine(api_key)
                            # Test with a simple prompt
                            test_result = engine.analyze_red_flags("Hello")
                            if "error" not in test_result:
                                st.success("✅ Connection successful!")
                                st.session_state.analysis_engine = engine
                            else:
                                st.error("❌ Connection failed. Please check your API key.")
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
            
            # Character selection
            if st.session_state.analysis_engine:
                st.subheader("🎭 Character Selection")
                character_descriptions = st.session_state.character_manager.get_character_descriptions()
                
                selected_character = st.selectbox(
                    "Choose Character to Chat With:",
                    options=list(character_descriptions.keys()),
                    format_func=lambda x: character_descriptions[x],
                    index=0 if st.session_state.current_character == "toxic_partner" else 1
                )
                
                if selected_character != st.session_state.current_character:
                    st.session_state.current_character = selected_character
                    st.session_state.chat_history = []
                    st.rerun()
                
                # Character info
                character = st.session_state.character_manager.get_character(selected_character)
                char_info = character.get_character_info()
                
                st.info(f"**Current Character:** {char_info['name']}")
                st.info(f"**Personality:** {char_info['personality']}")
            
            # Clear data buttons
            if st.session_state.analysis_engine:
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🗑️ Clear Chat"):
                        st.session_state.chat_history = []
                        st.success("Chat cleared!")
                        st.rerun()
                
                with col2:
                    if st.button("📊 Clear Analysis"):
                        st.session_state.analysis_history = []
                        st.success("Analysis history cleared!")
                        st.rerun()
    
    def render_chat_interface(self):
        """Render the chat interface with fake character"""
        st.markdown('<h2 class="sub-header">💬 Chat with AI Character</h2>', unsafe_allow_html=True)
        
        if not st.session_state.analysis_engine:
            st.warning("⚠️ Please enter your API key and test the connection first.")
            return
        
        # Get current character
        character = st.session_state.character_manager.get_character(st.session_state.current_character)
        char_info = character.get_character_info()
        
        # Display character info
        st.info(f"**Chatting with:** {char_info['name']} - {char_info['personality']}")
        
        # Chat input
        user_message = st.text_input(
            "Type your message:",
            key="chat_input",
            placeholder="Start a conversation..."
        )
        
        col1, col2 = st.columns([1, 4])
        
        with col1:
            if st.button("💬 Send", type="primary"):
                if user_message.strip():
                    # Generate character response
                    character_response = character.generate_response(user_message)
                    
                    # Add to chat history
                    st.session_state.chat_history.append({
                        "role": "user",
                        "content": user_message
                    })
                    st.session_state.chat_history.append({
                        "role": "character",
                        "content": character_response,
                        "character_name": char_info['name']
                    })
                    
                    st.rerun()
                else:
                    st.error("Please enter a message.")
        
        # Display chat history
        if st.session_state.chat_history:
            st.markdown("### Chat History:")
            for message in st.session_state.chat_history:
                if message["role"] == "user":
                    st.markdown(f"**👤 You:** {message['content']}")
                else:
                    st.markdown(f"**{message.get('character_name', 'AI')}:** {message['content']}")
                st.markdown("---")
    
    def render_analysis_interface(self):
        """Render the analysis interface"""
        st.markdown('<h2 class="sub-header">🔍 Message Analysis</h2>', unsafe_allow_html=True)
        
        if not st.session_state.analysis_engine:
            st.warning("⚠️ Please enter your API key and test the connection first.")
            return
        
        # Analysis input
        message_to_analyze = st.text_area(
            "Enter message to analyze:",
            height=150,
            placeholder="Paste a message here to analyze for red flags, green flags, manipulation, and sincerity..."
        )
        
        # Analysis options
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            analyze_red = st.button("🚨 Red Flags", type="primary")
        
        with col2:
            analyze_green = st.button("🟢 Green Flags", type="primary")
        
        with col3:
            analyze_manipulation = st.button("🎭 Manipulation", type="primary")
        
        with col4:
            analyze_sincerity = st.button("🤔 DID HE MEAN IT?", type="primary")
        
        # Comprehensive analysis
        if st.button("🔍 Comprehensive Analysis", type="secondary"):
            if message_to_analyze.strip():
                with st.spinner("Performing comprehensive analysis..."):
                    result = st.session_state.analysis_engine.comprehensive_analysis(message_to_analyze)
                    self.display_comprehensive_analysis(result)
            else:
                st.error("Please enter a message to analyze.")
        
        # Individual analyses
        if message_to_analyze.strip():
            if analyze_red:
                with st.spinner("Analyzing red flags..."):
                    result = st.session_state.analysis_engine.analyze_red_flags(message_to_analyze)
                    self.display_red_flag_analysis(result)
            
            if analyze_green:
                with st.spinner("Analyzing green flags..."):
                    result = st.session_state.analysis_engine.analyze_green_flags(message_to_analyze)
                    self.display_green_flag_analysis(result)
            
            if analyze_manipulation:
                with st.spinner("Analyzing manipulation..."):
                    result = st.session_state.analysis_engine.analyze_manipulation(message_to_analyze)
                    self.display_manipulation_analysis(result)
            
            if analyze_sincerity:
                with st.spinner("Analyzing sincerity..."):
                    result = st.session_state.analysis_engine.analyze_sincerity(message_to_analyze)
                    self.display_sincerity_analysis(result)
    
    def display_red_flag_analysis(self, result):
        """Display red flag analysis results"""
        if "error" in result:
            st.error(f"Error: {result['error']}")
            return
        
        st.markdown('<div class="red-flag">', unsafe_allow_html=True)
        st.markdown("### 🚨 Red Flag Analysis")
        st.markdown(f"**Severity:** {result.get('severity', 'Unknown')}")
        st.markdown(f"**Flags Found:** {', '.join(result.get('flags_found', []))}")
        st.markdown("**Analysis:**")
        st.markdown(result.get('analysis', ''))
        st.markdown('</div>', unsafe_allow_html=True)
    
    def display_green_flag_analysis(self, result):
        """Display green flag analysis results"""
        if "error" in result:
            st.error(f"Error: {result['error']}")
            return
        
        st.markdown('<div class="green-flag">', unsafe_allow_html=True)
        st.markdown("### 🟢 Green Flag Analysis")
        st.markdown(f"**Positivity Score:** {result.get('positivity_score', 0)}/10")
        st.markdown(f"**Flags Found:** {', '.join(result.get('flags_found', []))}")
        st.markdown("**Analysis:**")
        st.markdown(result.get('analysis', ''))
        st.markdown('</div>', unsafe_allow_html=True)
    
    def display_manipulation_analysis(self, result):
        """Display manipulation analysis results"""
        if "error" in result:
            st.error(f"Error: {result['error']}")
            return
        
        st.markdown('<div class="warning-box">', unsafe_allow_html=True)
        st.markdown("### 🎭 Manipulation Analysis")
        st.markdown(f"**Manipulation Score:** {result.get('manipulation_score', 0)}/10")
        st.markdown(f"**Tactics Found:** {', '.join(result.get('tactics_found', []))}")
        st.markdown("**Analysis:**")
        st.markdown(result.get('analysis', ''))
        st.markdown('</div>', unsafe_allow_html=True)
    
    def display_sincerity_analysis(self, result):
        """Display sincerity analysis results"""
        if "error" in result:
            st.error(f"Error: {result['error']}")
            return
        
        st.markdown('<div class="sincerity-box">', unsafe_allow_html=True)
        st.markdown("### 🤔 DID HE MEAN IT? Analysis")
        st.markdown(f"**Sincerity Score:** {result.get('sincerity_score', 0)}/10")
        st.markdown(f"**Verdict:** {result.get('did_he_mean_it', 'Unknown')}")
        st.markdown("**Analysis:**")
        st.markdown(result.get('analysis', ''))
        st.markdown('</div>', unsafe_allow_html=True)
    
    def display_comprehensive_analysis(self, result):
        """Display comprehensive analysis results"""
        if "error" in result:
            st.error(f"Error: {result['error']}")
            return
        
        st.markdown("### 🔍 Comprehensive Analysis Results")
        
        # Risk score with color coding
        risk_score = result.get('risk_score', 5)
        if risk_score >= 8:
            st.error(f"🚨 HIGH RISK SCORE: {risk_score}/10")
        elif risk_score >= 6:
            st.warning(f"⚠️ MODERATE RISK SCORE: {risk_score}/10")
        elif risk_score >= 4:
            st.info(f"🟡 CAUTION SCORE: {risk_score}/10")
        else:
            st.success(f"🟢 LOW RISK SCORE: {risk_score}/10")
        
        # Recommendation
        st.markdown(f"**Recommendation:** {result.get('recommendation', '')}")
        
        # Individual analyses
        with st.expander("📊 Detailed Analysis"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Red Flags")
                red_flags = result.get('red_flags', {})
                if 'severity' in red_flags:
                    st.markdown(f"**Severity:** {red_flags['severity']}")
                if 'flags_found' in red_flags:
                    st.markdown(f"**Flags:** {', '.join(red_flags['flags_found'])}")
                
                st.markdown("#### Green Flags")
                green_flags = result.get('green_flags', {})
                if 'positivity_score' in green_flags:
                    st.markdown(f"**Score:** {green_flags['positivity_score']}/10")
                if 'flags_found' in green_flags:
                    st.markdown(f"**Flags:** {', '.join(green_flags['flags_found'])}")
            
            with col2:
                st.markdown("#### Manipulation")
                manipulation = result.get('manipulation', {})
                if 'manipulation_score' in manipulation:
                    st.markdown(f"**Score:** {manipulation['manipulation_score']}/10")
                if 'tactics_found' in manipulation:
                    st.markdown(f"**Tactics:** {', '.join(manipulation['tactics_found'])}")
                
                st.markdown("#### Sincerity")
                sincerity = result.get('sincerity', {})
                if 'sincerity_score' in sincerity:
                    st.markdown(f"**Score:** {sincerity['sincerity_score']}/10")
                if 'did_he_mean_it' in sincerity:
                    st.markdown(f"**Verdict:** {sincerity['did_he_mean_it']}")
    
    def render_main_interface(self):
        """Render the main interface with tabs"""
        tab1, tab2, tab3 = st.tabs(["💬 Chat with AI", "🔍 Analyze Messages", "📊 Analysis History"])
        
        with tab1:
            self.render_chat_interface()
        
        with tab2:
            self.render_analysis_interface()
        
        with tab3:
            self.render_analysis_history()
    
    def render_analysis_history(self):
        """Render analysis history"""
        st.markdown('<h2 class="sub-header">📊 Analysis History</h2>', unsafe_allow_html=True)
        
        if not st.session_state.analysis_engine:
            st.warning("⚠️ Please enter your API key and test the connection first.")
            return
        
        history = st.session_state.analysis_engine.get_analysis_history()
        
        if not history:
            st.info("No analysis history yet. Start analyzing messages to see results here.")
            return
        
        for i, analysis in enumerate(reversed(history)):
            with st.expander(f"Analysis {len(history) - i}: {analysis.get('message', '')[:50]}..."):
                if analysis.get('analysis_type') == 'comprehensive':
                    self.display_comprehensive_analysis(analysis)
                elif analysis.get('analysis_type') == 'red_flags':
                    self.display_red_flag_analysis(analysis)
                elif analysis.get('analysis_type') == 'green_flags':
                    self.display_green_flag_analysis(analysis)
                elif analysis.get('analysis_type') == 'manipulation':
                    self.display_manipulation_analysis(analysis)
                elif analysis.get('analysis_type') == 'sincerity':
                    self.display_sincerity_analysis(analysis)
    
    def run(self):
        """Run the Toxic Detector app"""
        self.render_header()
        self.render_sidebar()
        self.render_main_interface()

def main():
    """Main function to run the app"""
    app = ToxicDetectorApp()
    app.run()

if __name__ == "__main__":
    main() 