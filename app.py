import streamlit as st
from services.gemini_service import GeminiService
from services.data_extractor import DataExtractor

class BotifyHubAssistant:
    def __init__(self):
        self.gemini_service = GeminiService()
        self.data_extractor = DataExtractor()
        self.knowledge_base = self.data_extractor.load_knowledge_base()
    
    def get_response(self, user_message):
        return self.gemini_service.generate_response(user_message)
    
    def refresh_knowledge_base(self):
        self.data_extractor.build_knowledge_base()
        self.data_extractor.save_knowledge_base()
        self.knowledge_base = self.data_extractor.load_knowledge_base()

def main():
    st.set_page_config(
        page_title="BotifyHub AI Assistant",
        page_icon="",
        layout="wide"
    )
    
    st.title(" BotifyHub AI Assistant")
    st.markdown("**Mohammed Elhusseiny - CEO & Founder**")
    st.markdown("---")
    
    if "assistant" not in st.session_state:
        st.session_state.assistant = BotifyHubAssistant()
        st.session_state.messages = []
    
    with st.sidebar:
        st.header("Knowledge Base Status")
        
        if st.button("Refresh Knowledge Base"):
            st.session_state.assistant.refresh_knowledge_base()
            st.success("Knowledge base refreshed!")
        
        kb = st.session_state.assistant.knowledge_base
        if "platform" in kb:
            st.subheader("Platform Info")
            st.write(f"Company: {kb['platform'].get('company_name', 'N/A')}")
        
        if "investment" in kb:
            st.subheader("Investment Info")
            st.write(f"Funding: {kb['investment'].get('amount', 'N/A')}")
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    user_input = st.chat_input("Ask me about BotifyHub...")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = st.session_state.assistant.get_response(user_input)
                st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
