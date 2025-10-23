import os

class FileReader:
    @staticmethod
    def read_file(file_path):
        try:
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as file:
                    return file.read()
            else:
                print("Warning: File not found: " + file_path)
                return None
        except Exception as e:
            print("Error reading file: " + str(e))
            return None
    
    @staticmethod
    def read_all_data_files():
        data_files = {
            "platform_info": "data/botifyhub_platform_info.txt",
            "faq": "data/faq_botifyhub.txt", 
            "investment": "data/investment_features.txt"
        }
        
        content = {}
        for key, file_path in data_files.items():
            content[key] = FileReader.read_file(file_path)
        
        return content