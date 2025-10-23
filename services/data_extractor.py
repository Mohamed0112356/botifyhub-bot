import json
import os
from utils.file_reader import FileReader

class DataExtractor:
    def __init__(self):
        self.file_reader = FileReader()
        self.knowledge_base = {}
    
    def extract_structured_data(self, content, data_type):
        """استخراج البيانات المهيكلة من المحتوى"""
        if data_type == "platform":
            return self._extract_platform_info(content)
        elif data_type == "faq":
            return self._extract_faq_data(content)
        elif data_type == "investment":
            return self._extract_investment_data(content)
        return {}
    
    def _extract_platform_info(self, content):
        """استخراج معلومات المنصة"""
        lines = content.split('\n')
        platform_data = {
            "vision": "",
            "mission": "", 
            "business_model": "",
            "target_market": "",
            "key_features": [],
            "technology": ""
        }
        
        current_section = ""
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if "vision" in line.lower():
                current_section = "vision"
            elif "mission" in line.lower():
                current_section = "mission"
            elif "business model" in line.lower():
                current_section = "business_model"
            elif "target market" in line.lower():
                current_section = "target_market"
            elif "technology" in line.lower():
                current_section = "technology"
            elif line.startswith('-') or line.startswith(''):
                if "feature" in current_section.lower():
                    platform_data["key_features"].append(line.lstrip('- ').strip())
            elif current_section and line:
                platform_data[current_section] += " " + line if platform_data[current_section] else line
        
        return platform_data
    
    def _extract_faq_data(self, content):
        """استخراج الأسئلة الشائعة"""
        faqs = []
        lines = content.split('\n')
        
        current_question = ""
        current_answer = ""
        in_qa_section = False
        
        for line in lines:
            line = line.strip()
            if line.startswith('Q:') or line.startswith('Q :'):
                if current_question and current_answer:
                    faqs.append({
                        "question": current_question,
                        "answer": current_answer.strip()
                    })
                current_question = line[2:].strip()
                current_answer = ""
                in_qa_section = True
            elif line.startswith('A:') or line.startswith('A :'):
                current_answer = line[2:].strip()
            elif in_qa_section and line and not line.startswith('Q:') and not line.startswith('A:'):
                if current_question and not current_answer:
                    # إذا كان هناك سؤال بدون إجابة بعد، فهو جزء من السؤال
                    current_question += " " + line
                elif current_answer:
                    current_answer += " " + line
        
        # إضافة آخر سؤال
        if current_question and current_answer:
            faqs.append({
                "question": current_question,
                "answer": current_answer.strip()
            })
        
        return faqs
    
    def _extract_investment_data(self, content):
        """استخراج معلومات الاستثمار"""
        investment_data = {
            "funding_status": "",
            "funding_rounds": "",
            "use_of_funds": "",
            "financial_projections": "",
            "market_opportunity": ""
        }
        
        lines = content.split('\n')
        current_section = ""
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if "funding status" in line.lower():
                current_section = "funding_status"
            elif "funding round" in line.lower():
                current_section = "funding_rounds"
            elif "use of fund" in line.lower():
                current_section = "use_of_funds"
            elif "financial projection" in line.lower():
                current_section = "financial_projections"
            elif "market opportunity" in line.lower():
                current_section = "market_opportunity"
            elif current_section and line:
                investment_data[current_section] += " " + line if investment_data[current_section] else line
        
        return investment_data
    
    def build_knowledge_base(self):
        """بناء قاعدة المعرفة من الملفات الثلاثة"""
        
        # تحميل معلومات المنصة
        platform_content = self.file_reader.read_file('data/botifyhub_platform_info.txt')
        if platform_content:
            self.knowledge_base["platform"] = self._extract_platform_info(platform_content)
        
        # تحميل الأسئلة الشائعة
        faq_content = self.file_reader.read_file('data/faq_botifyhub.txt')
        if faq_content:
            self.knowledge_base["faq"] = self._extract_faq_data(faq_content)
        
        # تحميل معلومات الاستثمار
        investment_content = self.file_reader.read_file('data/investment_features.txt')
        if investment_content:
            self.knowledge_base["investment"] = self._extract_investment_data(investment_content)
        
        return self.knowledge_base
    
    def save_knowledge_base(self, file_path=None):
        """حفظ قاعدة المعرفة"""
        if file_path is None:
            file_path = 'data/knowledge_base.json'
        
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(self.knowledge_base, f, indent=2, ensure_ascii=False)
    
    def load_knowledge_base(self, file_path=None):
        """تحميل قاعدة المعرفة"""
        if file_path is None:
            file_path = 'data/knowledge_base.json'
        
        try:
            with open(file_path, "r", encoding="utf-8-sig") as f:
                return json.load(f)
        except FileNotFoundError:
            self.build_knowledge_base()
            self.save_knowledge_base(file_path)
            return self.knowledge_base