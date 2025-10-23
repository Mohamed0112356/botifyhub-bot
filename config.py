import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Data paths
    DATA_PATHS = {
        "platform_info": "data/botifyhub_platform_info.txt",
        "faq": "data/faq_botifyhub.txt",
        "investment": "data/investment_features.txt"
    }
    
    # Knowledge base file
    KNOWLEDGE_BASE_FILE = "data/knowledge_base.json"
