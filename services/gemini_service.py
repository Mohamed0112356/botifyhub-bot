import requests
import json
from services.data_extractor import DataExtractor

class GeminiService:
    def __init__(self):
        self.api_key = "AIzaSyCuI7Xfg16q0Dq60IzkrBtwtVZ4UZsxL04"
        self.model_name = "gemini-2.0-flash-001"
        self.data_extractor = DataExtractor()
        self.knowledge_base = self.data_extractor.load_knowledge_base()
        self.url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent?key={self.api_key}"
    
    def format_knowledge_for_prompt(self):
        kb = self.knowledge_base
        
        prompt_text = """You are Mohammed Elhusseiny, CEO & Founder of BotifyHub.
You are speaking with potential investors and interested clients about our platform.

YOUR ROLE:
- Speak as the founder - confident, professional, knowledgeable
- Use emotional intelligence to understand investor concerns
- Provide comprehensive, engaging answers
- Connect different aspects of the business naturally

DATA USAGE RULES:
- Use ONLY the information from the knowledge base below
- You can combine information from different sections intelligently
- Rephrase and structure answers naturally for better flow
- Add business context and connect ideas logically
- If information is missing, acknowledge the limitation professionally

PERSONALITY:
- Enthusiastic about AI and automation
- Business-focused and results-oriented
- Transparent about current stage and plans
- Professional but approachable

KNOWLEDGE BASE:
"""
        
        # ??? ?? ????????? ?? ??????? ???????
        knowledge_sections = []
        
        # ??????? ??????
        if "platform" in kb:
            platform = kb["platform"]
            platform_info = f"""
COMPANY PLATFORM:
- Vision: {platform.get('vision', '')}
- Mission: {platform.get('mission', '')}
- Business Model: {platform.get('business_model', '')}
- Target Market: {platform.get('target_market', '')}
- Key Features: {', '.join(platform.get('key_features', []))}
- Technology: {platform.get('technology', '')}
"""
            knowledge_sections.append(platform_info)
        
        # ??????? ???????
        if "faq" in kb and kb["faq"]:
            faq_section = """
FREQUENTLY ASKED QUESTIONS:
"""
            for faq in kb["faq"]:
                question = faq.get("question", "").strip()
                answer = faq.get("answer", "").strip()
                if question and answer:
                    faq_section += f"\nQ: {question}\nA: {answer}\n"
            knowledge_sections.append(faq_section)
        
        # ??????? ?????????
        if "investment" in kb:
            investment = kb["investment"]
            investment_info = f"""
INVESTMENT INFORMATION:
- Funding Status: {investment.get('funding_status', '')}
- Funding Rounds: {investment.get('funding_rounds', '')}
- Use of Funds: {investment.get('use_of_funds', '')}
- Financial Projections: {investment.get('financial_projections', '')}
- Market Opportunity: {investment.get('market_opportunity', '')}
"""
            knowledge_sections.append(investment_info)
        
        # ??? ?? ???????
        prompt_text += "\n".join(knowledge_sections)
        
        return prompt_text
    
    def generate_response(self, prompt):
        context = self.format_knowledge_for_prompt()
        
        full_prompt = f"""{context}

CONVERSATION:
Investor: {prompt}

You (Mohammed Elhusseiny):"""
        
        try:
            payload = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": full_prompt
                            }
                        ]
                    }
                ],
                "generationConfig": {
                    "temperature": 0.7,  # ????? ??? ??????? ??????
                    "topK": 40,
                    "topP": 0.95,
                    "maxOutputTokens": 1024,
                }
            }
            
            headers = {
                "Content-Type": "application/json"
            }
            
            response = requests.post(self.url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            if "candidates" in result and len(result["candidates"]) > 0:
                return result["candidates"][0]["content"]["parts"][0]["text"]
            else:
                return "Thank you for your question. Based on our current plans and market research, I'd be happy to discuss how BotifyHub is positioned for success in the automation space."
                
        except Exception as e:
            return f"I appreciate your question. Currently, I'm experiencing some technical difficulties. Please try again in a moment."
